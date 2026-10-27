#!/usr/bin/env python3
"""Shodan harness scanner (Hermes port of lane 10).

Runs Shodan count queries for agent harnesses (Cairn, Strix,
Hermes Agent) and reports NEW exposure as count changes.

API LIMITATION (verified 2026-10-19): on the source plan,
/shodan/host/search returns empty. Only /shodan/host/count
works. This module tracks per-query banner COUNTS, not banners.
A count change means hosts appeared or disappeared. Context
uses count FACETS (org/asn/domain snapshots in state, refreshed
every run). Facet values are unvalidated provider context,
never a tier input. New facet values and movers of 5 or more
are reported on the hit.

Triage rule, enforced in code: a count change emits a hit
only if the absolute delta is over 10% of the previous count,
or the change is sustained across two runs (same direction
as the previous run's delta), or the query is tied to an
active investigation (active_investigation:true in config).
Any other change is logged only, not emitted.

Port changes vs the source:
- Transport: the source called a vault-backed CLI. This port
  calls the Shodan /shodan/host/count API directly with a key
  read at run time from the env var named in config
  (api_key_env). No key set means every query fails safe and
  the stored baseline is untouched. No secret value is stored.
- Config: tools/config.json, resolved relative to this file.
- State: hermes/workspace/state/shodan_facets.json.
- Passive only. GET-equivalent API calls. No host interaction.

Count-level hits record no individual IPs, so no IP
classification is attached. A follow-up host-detail pass must
classify each IP before it ships.

Usage: shodan.py [--dry-run] [--since-hours 24] [--json]
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    USER_AGENT, load_config, make_hit, utcnow_iso,
    is_new, mark_seen, parse_args, emit, report_error, STATE_DIR,
    scanner_enabled,
)

LANE = "shodan"
FACET_STATE_PATH = os.path.join(STATE_DIR, "shodan_facets.json")
FACET_FAMILIES = ("org", "asn", "domain")
FACET_TOPN = 8


def _count_query(block: dict, api_key: str, query: str,
                 facets: str | None = None):
    """Run the count API. Returns (total, facet_map) or (None, {})."""
    base = block.get("api_base", "https://api.shodan.io")
    params = {"key": api_key, "query": query}
    if facets:
        params["facets"] = facets
    url = f"{base}/shodan/host/count?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[shodan] count failed for {query!r}: HTTP {e.code}",
              file=sys.stderr)
        return None, {}
    except Exception as e:
        print(f"[shodan] count exception for {query!r}: "
              f"{type(e).__name__}: {e}", file=sys.stderr)
        return None, {}
    try:
        total = data.get("total")
        total = int(total) if total is not None else None
    except (TypeError, ValueError):
        total = None
    facet_map = {}
    for family, rows in (data.get("facets") or {}).items():
        try:
            facet_map[family] = {str(x["value"]): int(x["count"])
                                 for x in rows[:FACET_TOPN]}
        except (TypeError, KeyError, ValueError):
            continue
    return total, facet_map


def _last_count_for(seen_ids, label: str) -> int | None:
    prefix = f"shodan:count:{label}:"
    best = None
    for key in seen_ids:
        if key.startswith(prefix):
            try:
                best = int(key[len(prefix):])
            except ValueError:
                continue
    return best


def _prev_count_for(facet_state: dict, seen_ids, label: str) -> int | None:
    prev_entry = facet_state.get(label)
    if isinstance(prev_entry, dict):
        try:
            return int(prev_entry.get("total")) \
                if prev_entry.get("total") is not None else None
        except (TypeError, ValueError):
            pass
    return _last_count_for(seen_ids, label)


def _load_facet_state() -> dict:
    try:
        with open(FACET_STATE_PATH) as f:
            state = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}
    return state if isinstance(state, dict) else {}


def _save_facet_state(state: dict) -> None:
    os.makedirs(os.path.dirname(FACET_STATE_PATH), exist_ok=True)
    tmp = f"{FACET_STATE_PATH}.tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1)
    os.replace(tmp, FACET_STATE_PATH)


def _diff_facets(prev: dict, cur: dict) -> list:
    lines = []
    for family in FACET_FAMILIES:
        p, c = prev.get(family, {}), cur.get(family, {})
        for val, cnt in c.items():
            if val not in p:
                lines.append(f"[{family}] NEW {val!r} (n={cnt})")
            else:
                d = cnt - p[val]
                if abs(d) >= 5:
                    lines.append(f"[{family}] {val!r}: "
                                 f"{p[val]} -> {cnt} ({d:+d})")
        for val, cnt in p.items():
            if val not in c:
                lines.append(f"[{family}] GONE {val!r} (was n={cnt})")
    if not lines:
        lines.append("no facet value crossed the +/-5 or new/gone "
                     "threshold (attribution unclear)")
    return lines


def _store_count(seen_ids, label: str, total: int) -> None:
    prefix = f"shodan:count:{label}:"
    for key in [k for k in seen_ids if k.startswith(prefix)]:
        seen_ids.discard(key)
    mark_seen(seen_ids, f"{prefix}{total}")


def scan_query(block: dict, api_key: str, query_cfg: dict, seen_ids,
               collected_at: str, dry_run: bool,
               facet_state: dict) -> list:
    query = query_cfg["q"]
    label = query_cfg.get("label", query)
    indicators = query_cfg.get("indicators", [query])
    baseline = query_cfg.get("baseline")
    hits = []
    if dry_run:
        print(f"[dry-run] shodan query: {label} (q={query!r}, "
              f"baseline={baseline})", file=sys.stderr)
        return hits
    facets = ",".join(block.get("facet_families", list(FACET_FAMILIES)))
    total, facet_map = _count_query(block, api_key, query, facets)
    if total is None:
        report_error("shodan", "count_failed",
                     f"query {label!r} returned no count",
                     {"query": query[:200]})
        return hits
    prev = _prev_count_for(facet_state, seen_ids, label)
    print(f"[shodan] {label}: count={total} "
          f"(prev={prev}, baseline={baseline})", file=sys.stderr)
    old_snapshot = facet_state.get(label) \
        if isinstance(facet_state.get(label), dict) else {}
    facet_state[label] = {"total": total, "at": collected_at,
                          "facets": facet_map}
    if prev is None:
        _store_count(seen_ids, label, total)
        print(f"[shodan] {label}: first run, storing count={total}",
              file=sys.stderr)
        return hits
    if total == prev:
        return hits
    delta = total - prev
    direction = "grew" if delta > 0 else "shrank"
    _store_count(seen_ids, label, total)
    prev_facets = old_snapshot.get("facets", {})
    facet_state[f"prev:{label}"] = old_snapshot
    facet_moves = _diff_facets(prev_facets, facet_map)
    # Triage rule: emit only on a large delta, a sustained
    # change, or an active investigation. Otherwise log only.
    pct = (abs(delta) / prev) if prev else 1.0
    trend = facet_state.get(f"trend:{label}")
    last_delta = trend.get("last_delta") if isinstance(trend, dict) \
        else None
    sustained = (last_delta is not None and last_delta != 0
                 and (last_delta > 0) == (delta > 0))
    active = query_cfg.get("active_investigation", False) is True
    facet_state[f"trend:{label}"] = {"last_delta": delta,
                                     "at": collected_at}
    if not (pct > 0.10 or sustained or active):
        print(f"[shodan] {label}: count {direction} {prev} -> "
              f"{total} (delta {delta:+d}, {pct:.1%}); below the "
              f"10% triage rule, not sustained, no active "
              f"investigation — logged only, no hit",
              file=sys.stderr)
        return hits
    confidence = "MEDIUM"
    hits.append(make_hit(
        lane=LANE,
        source_url=f"https://www.shodan.io/search?query={query}",
        indicators_matched=list(indicators),
        confidence=confidence,
        summary=f"[shodan] {label}: banner count {direction} "
                f"{prev} -> {total} (delta {delta:+d}); "
                f"top facet moves: {'; '.join(facet_moves[:4])}",
        provenance={
            "method": "Shodan /shodan/host/count API with facets",
            "query": query,
            "previous_count": prev,
            "current_count": total,
            "delta": delta,
            "hunt_baseline": baseline,
            "retrieved_at": collected_at,
            "facet_moves": facet_moves,
            "limitation": "/shodan/host/search returns empty on "
                          "the source plan; context via count "
                          "facets (org/asn/domain), not banner "
                          "enumeration. Facet org/asn/domain values "
                          "are unvalidated provider context, never "
                          "a tier input",
        },
        extra={
            "query_label": label,
            "previous_count": prev,
            "current_count": total,
            "delta": delta,
            "facet_moves": facet_moves,
        },
        grade="SECONDARY",
    ))
    return hits


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Run Shodan count queries, report count changes.

    since_hours is accepted for contract compliance. Shodan
    counts are point-in-time; newness is a count delta vs the
    last stored count, not a time window.
    """
    if not dry_run and not scanner_enabled("shodan"):
        print("[shodan] live scan refused: shodan.enabled is not "
              "true in config.json (module ships disabled)",
              file=sys.stderr)
        raise SystemExit(2)
    cfg = load_config()
    if seen_ids is None:
        seen_ids = set()
    block = cfg.get("scanners", {}).get("shodan", {})
    queries = block.get("queries", [])
    collected_at = utcnow_iso()
    facet_state = _load_facet_state()
    if not queries:
        print("[shodan] no queries in config 'shodan' block",
              file=sys.stderr)
        return []
    if dry_run:
        for q in queries:
            scan_query(block, "", q, seen_ids, collected_at, True,
                       facet_state)
        return []
    from _common import resolve_env
    api_key = resolve_env(block.get("api_key_env"))
    if not api_key:
        print(f"[shodan] no API key env var set "
              f"({block.get('api_key_env')}); no network calls, "
              "baseline untouched", file=sys.stderr)
        return []
    spacing = float(block.get("rate_limit_seconds", 5))
    hits = []
    for i, q in enumerate(queries):
        if q.get("enabled", False) is not True:
            print(f"[shodan] {q.get('label')}: disabled "
                  f"({q.get('disabled_reason', 'no reason')})",
                  file=sys.stderr)
            continue
        try:
            hits.extend(scan_query(block, api_key, q, seen_ids,
                                   collected_at, dry_run, facet_state))
        except Exception as e:
            report_error("shodan", "query_failed",
                         f"{q.get('label', q.get('q'))}: {e}",
                         {"query": str(q.get("q"))[:200]})
            print(f"[shodan] query {q.get('label')!r} failed: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
        if i < len(queries) - 1:
            time.sleep(spacing)
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    _save_facet_state(facet_state)
    return hits


def main():
    args = parse_args("Shodan harness scanner (Hermes port)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
