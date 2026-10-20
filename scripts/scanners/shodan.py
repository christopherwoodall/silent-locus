#!/usr/bin/env python3
"""Lane 10 — Shodan harness scanner: agent-harness panel enumeration.

Runs the refined Shodan queries for agent harnesses (Cairn, Strix,
Hermes Agent) on a schedule and reports NEW exposure.

API LIMITATION (verified 2026-10-19): on the current Shodan plan,
`/shodan/host/search` returns empty; only `/shodan/host/count` and
`/shodan/host/{ip}` work. This module therefore tracks per-query
banner COUNTS, not individual banners. A count change means hosts
appeared or disappeared since the last run. Attribution of a delta
uses count FACETS (org/asn/domain snapshots in
state/shodan_facets.json, refreshed every run) -- new facet values
and movers >= +/-5 are reported on the hit (A4, 2026-10-20).

Queries come from the 2026-10-19 Cairn/Strix/Hermes hunt
(refined-queries.json). Baselines from that hunt:

  - http.title:"Cairn"          -> 223 banners
  - http.title:"Strix"          -> 152 banners
  - http.html:"Cairn"           -> 324 banners
  - product:"Hermes Agent"      -> ~5,499 banners (partial: 4,200 seen)

Auth goes through the existing CLI at
~/workspace/custom-connectors/custom.legacy-shodan/bin/shodan.py
(surrogate credential exchange via dynamic_credentials). This module
calls it via subprocess to avoid import-path conflicts.

Passive only. GET-equivalent API calls. No host interaction, no
probing beyond what Shodan already scanned.

IP-classification note (standing rule): count-level hits record no
individual IPs, so no ip_classification is attached. When a
follow-up host-detail pass resolves specific IPs, each must be
classified via _common.attach_ip_classification before it ships.

Usage:
    shodan.py [--dry-run] [--since-hours 24] [--json]

Queries come from ~/workspace/silent-locus/scripts/swarm-infra-config.json
("shodan" block).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    USER_AGENT, load_config, make_hit, utcnow_iso,
    is_new, mark_seen, parse_args, emit, report_error,
)

LANE = "shodan"
SHODAN_CLI = os.path.expanduser(
    "~/workspace/custom-connectors/custom.legacy-shodan/bin/shodan.py")
# shodan.py imports dynamic_credentials; the orchestrator's env may not
# have the connector bin dir on PYTHONPATH, so set it explicitly for the
# subprocess (connector doc: CONNECTOR.md Tooling).
CONNECTOR_BIN = os.path.expanduser(
    "/opt/muse/skills/custom-connector-setup/bin")
REQUEST_SPACING = 5  # seconds between count queries
# Count-facet families requested alongside each query (A4, 2026-10-20:
# attribution for count deltas; the search endpoint returns empty on
# this plan, verified, so facets are the attribution path).
FACET_FAMILIES = ("org", "asn", "domain")
FACET_TOPN = 8  # stored per family
FACET_STATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "state", "shodan_facets.json")


def _count_query(query: str, facets: str | None = None):
    """Run `shodan.py count <query> [facets]`, return (total, facet_map).

    facet_map: {family: {value: count}} trimmed to FACET_TOPN each.
    Returns (None, {}) on failure."""
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = CONNECTOR_BIN + os.pathsep + env.get(
            "PYTHONPATH", "")
        cmd = [sys.executable, SHODAN_CLI, "count", query]
        if facets:
            cmd.append(facets)
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120, env=env,
        )
        if r.returncode != 0:
            print(f"[shodan] count failed for {query!r}: "
                  f"{r.stderr.strip()[:200]}", file=sys.stderr)
            return None, {}
        data = json.loads(r.stdout)
        total = data.get("total")
        total = int(total) if total is not None else None
        facet_map = {}
        for family, rows in (data.get("facets") or {}).items():
            facet_map[family] = {str(x["value"]): int(x["count"])
                                 for x in rows[:FACET_TOPN]}
        return total, facet_map
    except Exception as e:
        print(f"[shodan] count exception for {query!r}: "
              f"{type(e).__name__}: {e}", file=sys.stderr)
        return None, {}


def _last_count_for(seen_ids, label: str) -> int | None:
    """Find the most recent stored count for a query label."""
    prefix = f"shodan:count:{label}:"
    best = None
    for key in seen_ids:
        if key.startswith(prefix):
            try:
                total = int(key[len(prefix):])
                if best is None or True:  # last write wins; set is unordered
                    best = total
            except ValueError:
                continue
    return best


def _load_facet_state() -> dict:
    try:
        with open(FACET_STATE_PATH) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _save_facet_state(state: dict) -> None:
    tmp = f"{FACET_STATE_PATH}.general-hunt.tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1)
    os.replace(tmp, FACET_STATE_PATH)


def _diff_facets(prev: dict, cur: dict, total_delta: int) -> list:
    """Human-readable facet moves between two snapshots.

    prev/cur: {family: {value: count}}. Flags new values and big movers.
    """
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
    # Remove old count keys for this label (keep set small)
    prefix = f"shodan:count:{label}:"
    for key in [k for k in seen_ids if k.startswith(prefix)]:
        seen_ids.discard(key)
    mark_seen(seen_ids, f"{prefix}{total}")


def scan_query(query_cfg: dict, seen_ids, collected_at: str,
               dry_run: bool, facet_state: dict) -> list:
    query = query_cfg["q"]
    label = query_cfg.get("label", query)
    indicators = query_cfg.get("indicators", [query])
    baseline = query_cfg.get("baseline")
    hits = []

    if dry_run:
        print(f"[dry-run] shodan query: {label} (q={query!r}, "
              f"baseline={baseline})", file=sys.stderr)
        return hits

    total, facet_map = _count_query(query, ",".join(FACET_FAMILIES))
    if total is None:
        report_error("shodan", "count_failed",
                     f"query {label!r} returned no count",
                     {"query": query[:200]})
        return hits

    prev = _last_count_for(seen_ids, label)
    print(f"[shodan] {label}: count={total} "
          f"(prev={prev}, baseline={baseline})", file=sys.stderr)

    # store the facet snapshot every run (not just on delta) so the
    # attribution window always has a fresh reference point
    facet_state[label] = {"total": total, "at": collected_at,
                          "facets": facet_map}

    # First run: store baseline, no hit (nothing is "new" yet)
    if prev is None:
        _store_count(seen_ids, label, total)
        print(f"[shodan] {label}: first run, storing count={total}",
              file=sys.stderr)
        return hits

    if total == prev:
        return hits  # no change, no hit

    delta = total - prev
    direction = "grew" if delta > 0 else "shrank"
    _store_count(seen_ids, label, total)

    # attribute the delta through facet moves (A4)
    prev_facets = (facet_state.get(f"prev:{label}") or {}).get("facets",
                                                               {})
    facet_state[f"prev:{label}"] = facet_state[label]
    facet_moves = _diff_facets(prev_facets, facet_map, delta)

    # Confidence: growth in harness exposure is HIGH (new panels
    # appeared); shrinkage is MEDIUM (panels went dark, less urgent
    # but worth noting for coverage tracking)
    confidence = "HIGH" if delta > 0 else "MEDIUM"

    hits.append(make_hit(
        lane=LANE,
        source_url=f"https://www.shodan.io/search?query={query}",
        indicators_matched=list(indicators),
        confidence=confidence,
        summary=f"[shodan] {label}: banner count {direction} "
                f"{prev} -> {total} (delta {delta:+d}); "
                f"top facet moves: {'; '.join(facet_moves[:4])}",
        provenance={
            "method": "Shodan /shodan/host/count API with facets via "
                      "shodan.py CLI",
            "query": query,
            "previous_count": prev,
            "current_count": total,
            "delta": delta,
            "hunt_baseline": baseline,
            "retrieved_at": collected_at,
            "facet_moves": facet_moves,
            "limitation": "/shodan/host/search returns empty on "
                           "current plan; attribution via count "
                           "facets (org/asn/domain), not banner "
                           "enumeration",
        },
        extra={
            "query_label": label,
            "previous_count": prev,
            "current_count": total,
            "delta": delta,
            "facet_moves": facet_moves,
        },
        grade="PRIMARY",
    ))
    return hits


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Run Shodan count queries, report count changes. Returns hit dicts.

    Note: since_hours is accepted for contract compliance. Shodan
    counts are point-in-time; newness is determined by count delta
    vs the last stored count, not a time window.
    """
    cfg = load_config()
    if seen_ids is None:
        seen_ids = set()
    queries = cfg.get("shodan", {}).get("queries", [])
    collected_at = utcnow_iso()
    facet_state = _load_facet_state()

    if not queries:
        print("[shodan] no queries in config 'shodan' block",
              file=sys.stderr)
        return []

    if not os.path.exists(SHODAN_CLI):
        report_error("shodan", "cli_missing",
                     f"Shodan CLI not found at {SHODAN_CLI}")
        print(f"[shodan] CLI missing: {SHODAN_CLI}", file=sys.stderr)
        return []

    hits = []
    for i, q in enumerate(queries):
        if q.get("enabled", True) is False:
            print(f"[shodan] {q.get('label')}: disabled "
                  f"({q.get('disabled_reason', 'no reason')})",
                  file=sys.stderr)
            continue
        try:
            hits.extend(scan_query(q, seen_ids, collected_at, dry_run,
                                   facet_state))
        except Exception as e:
            report_error("shodan", "query_failed",
                         f"{q.get('label', q.get('q'))}: {e}",
                         {"query": str(q.get("q"))[:200]})
            print(f"[shodan] query {q.get('label')!r} failed: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
        if not dry_run and i < len(queries) - 1:
            time.sleep(REQUEST_SPACING)
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    if not dry_run:
        _save_facet_state(facet_state)
    return hits


def main():
    args = parse_args("Lane 10 — Shodan harness scanner (Cairn/Strix/Hermes)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
