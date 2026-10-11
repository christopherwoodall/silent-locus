#!/usr/bin/env python3
"""Lane: arquivo-pt — idempotent, stateful collector.

Reads collections/arquivo-pt/state.json and only fetches what's missing.
Wraps the committed 2026-10-01 collector (data/2026-10-01-arquivo-pt/collect.py):
same TARGETS list, >=1.5s between requests, backoff on 429/503, hard stop on
explicit rejection. A green re-run fetches nothing new and exits 0.

Data stays in data/2026-10-01-arquivo-pt/raw (adopted pull, not duplicated).
Lane events log to collections/arquivo-pt/collect.log.jsonl.

Run: python3 collect.py
"""
import gzip
import importlib.util
import json
import sys
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE_PATH = HERE / "state.json"
LOG = HERE / "collect.log.jsonl"
REPO = HERE.parent.parent  # ~/workspace/silent-locus


def lane_log(obj):
    obj["logged_at"] = datetime.now(timezone.utc).isoformat()
    with LOG.open("a") as f:
        f.write(json.dumps(obj) + "\n")


def load_state():
    return json.loads(STATE_PATH.read_text())


def load_original_collector():
    """Import data/2026-10-01-arquivo-pt/collect.py as a module (read-only use
    of its fetch logic; we never modify the committed original)."""
    mod_path = REPO / "data" / "2026-10-01-arquivo-pt" / "collect.py"
    spec = importlib.util.spec_from_file_location("arquivo_orig_collect", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def unique_count(gz_path):
    """Unique captures = deduped on (timestamp, url), same as analyze.py."""
    seen = set()
    try:
        with gzip.open(gz_path, "rt", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    seen.add((r.get("timestamp"), r.get("url")))
                except Exception:
                    pass
    except FileNotFoundError:
        return None
    return len(seen)


def lane_complete(state, mod):
    """True when every expected slug verifies at/above expected count.
    Returns (complete, gaps) where gaps = [slugs needing fetch]."""
    raw = REPO / state["data_path"] / ".." / "raw"
    raw = raw.resolve()
    expected = state["expected_per_slug"]
    gaps = []
    counts = {}
    for slug, want in expected.items():
        p = raw / f"{slug}.cdx.jsonl.gz"
        have = unique_count(p)
        counts[slug] = have
        if have is None:
            gaps.append(slug)
        elif have < want:
            gaps.append(slug)
        # else: verified, skip (honest negatives: want=0, file exists)
    return (len(gaps) == 0, gaps, counts)


def fill_gap(mod, slug, raw):
    """Re-run the original fetch logic for one slug. On rate-limit hard stop,
    record in state.json and abort the lane (exit 2)."""
    target = next(t for t in mod.TARGETS if t[0] == slug)
    _, hosts, wfrom, wto, note = target
    out = raw / f"{slug}.cdx.jsonl.gz"
    if out.exists():
        bak = out.with_suffix(out.suffix + f".bak-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}")
        out.rename(bak)
        lane_log({"event": "gap_stale_backup", "slug": slug, "backup": bak.name})
    lane_log({"event": "gap_fetch_start", "slug": slug, "hosts": hosts})
    try:
        mod.collect_target(slug, hosts, wfrom, wto)
    except urllib.error.HTTPError as e:
        record_block(f"http_{e.code}")
        raise SystemExit(2)
    except Exception as e:
        lane_log({"event": "gap_fetch_error", "slug": slug,
                  "error": f"{type(e).__name__}: {e}"})
        record_block(f"fetch_error:{type(e).__name__}")
        raise SystemExit(2)
    lane_log({"event": "gap_fetch_done", "slug": slug})


def record_block(reason):
    """On block/rate-limit: stop the lane, record in state.json, move on."""
    state = load_state()
    state["status"] = f"blocked:{reason}"
    state["blocked_at_utc"] = datetime.now(timezone.utc).isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")
    lane_log({"event": "hard_stop", "reason": reason})


def main():
    state = load_state()
    assert state.get("lane") == "arquivo-pt", "state.json lane mismatch"
    mod = load_original_collector()
    lane_log({"event": "run_start", "utc": datetime.now(timezone.utc).isoformat(),
              "watermark": state.get("watermark")})

    complete, gaps, counts = lane_complete(state, mod)
    lane_log({"event": "verify", "counts": counts, "gaps": gaps})

    if complete:
        lane_log({"event": "run_done", "fetched_new": 0,
                  "note": "all slugs verified at/above expected counts; nothing fetched"})
        print(f"GREEN: {len(counts)} slugs verified, nothing fetched. exit 0.")
        return 0

    raw = (REPO / state["data_path"] / ".." / "raw").resolve()
    for slug in gaps:
        fill_gap(mod, slug, raw)

    complete, gaps, counts = lane_complete(state, mod)
    total = sum(c for c in counts.values() if c) or 0
    state = load_state()  # may have been rewritten by record_block
    if complete:
        state["items_collected"] = total
        state["status"] = "adopted-complete+gapfill"
        state["last_run_utc"] = datetime.now(timezone.utc).isoformat()
        STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")
        lane_log({"event": "run_done", "fetched_new": total,
                  "counts": counts, "note": "gaps filled"})
        print(f"GREEN: gaps filled, total unique={total}. exit 0.")
        return 0

    state["status"] = "incomplete"
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")
    lane_log({"event": "run_done", "status": "incomplete", "counts": counts})
    print(f"RED: still incomplete after gap fill: {gaps}. exit 1.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
