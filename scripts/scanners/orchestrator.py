#!/usr/bin/env python3
"""Morning swarm-scan orchestrator.

Runs all evidence-lane scanners, collects hits, writes a factum-ready
bundle, and prints the morning breakdown.

Contract:
    run_orchestrator(since_hours=24, dry_run=False) -> dict

CLI:
    orchestrator.py [--since-hours N] [--dry-run] [--json] [--skip-factum]

Pipeline:
    1. Load seen_ids from state (persistent dedup across runs).
    2. Run each lane scanner's scan() with shared seen_ids.
    3. Write hits to dated JSONL staging file.
    4. Build factum bundle JSON (pre-built; cron worker submits via
       factum.py add --input separately -- factum.py is too slow for
       synchronous use on a 116k-record corpus).
    5. Print morning breakdown.

Lane registry: (module_name, lane_id, enabled)
Disabled lanes are skipped but listed in the breakdown.
"""
from __future__ import annotations

import datetime
import importlib
import json
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C

STATE_DIR = os.path.expanduser(
    "~/workspace/silent-locus/scripts/scanners/state")
SEEN_PATH = os.path.join(STATE_DIR, "orchestrator_seen.json")
STAGING_DIR = os.path.join(STATE_DIR, "morning-hits")

# (module, lane_id, enabled)
# webhook_site: sibling agent's swarm-infra-crawler.py is the lane-2
# implementation (creator-IP extraction). It does not yet expose the
# scan() contract; marked disabled until integrated.
LANES = [
    ("urlquery", "urlquery-amap-watch", True),
    ("webhook_site", "webhook-creator-ip", False),
    ("ntfy", "ntfy-monitor", True),
    ("urlscan", "urlscan-amap", True),
    ("wayback", "wayback-infra", True),
    ("crtsh", "crtsh-certs", True),
    ("packages", "package-registries", True),  # tripwire mode per counsel
    ("dbmining", "db-url-mining", True),  # hypothesis feeder per counsel
]

# Counsel verdicts that shape orchestration (2026-10-14):
#  - packages.py: tripwire only (HIGH exact-strings); MEDIUM/LOW cut
#  - dbmining.py: hypothesis feeder; confidence LOW; score is annotation
#  - ntfy.py: reactive enrichment; confidence capped MEDIUM
#  - wayback.py: forensic tool; presence-only MEDIUM


def _load_seen() -> set:
    try:
        with open(SEEN_PATH) as f:
            return set(json.load(f))
    except (OSError, json.JSONDecodeError):
        return set()


def _save_seen(seen: set) -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = SEEN_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(sorted(seen), f)
    os.rename(tmp, SEEN_PATH)


def _build_factum_bundle(hits: list, run_id: str) -> dict:
    """Build a factum bundle from scanner hits (no factum.py invocation).

    Each hit becomes: source (the lane) + observation (web.capture) +
    observables (url, ipv4 where present). Follows the bundle.json
    example shape from the factum skill.
    """
    records = []
    for i, h in enumerate(hits):
        sref, oref = f"source-{i}", f"obs-{i}"
        records.append({
            "ref": sref, "kind": "source",
            "body": {
                "source_type": "scanner",
                "locator": f"scanner:{h.get('lane')}",
            },
        })
        data = {
            "summary": h.get("summary", ""),
            "indicators": h.get("indicators_matched", []),
            "confidence": h.get("confidence", "LOW"),
            "grade": h.get("grade", "SECONDARY"),
        }
        if h.get("ip_classification"):
            data["ip_classification"] = h["ip_classification"]
        if h.get("priority"):
            data["priority"] = True
        records.append({
            "ref": oref, "kind": "observation",
            "body": {
                "type": "web.capture",
                "source": f"@{sref}",
                "data": data,
            },
            "tags": {
                "lane": h.get("lane"),
                "scanner": True,
            },
        })
        # URL observable
        if h.get("source_url"):
            records.append({
                "ref": f"url-{i}", "kind": "observable",
                "body": {"type": "url", "value": h["source_url"]},
            })
        # IP observable
        ip = (h.get("ip_classification") or {}).get("ip")
        if ip:
            records.append({
                "ref": f"ip-{i}", "kind": "observable",
                "body": {"type": "ipv4" if "." in ip else "ipv6",
                         "value": ip},
            })
    return {
        "bundle": 2,
        "idempotency_key": f"swarm-scan/{run_id}",
        "actor": "agent:swarm-scan-orchestrator",
        "tags": {"swarm_scan": True, "run_id": run_id},
        "records": records,
    }


def _breakdown(hits: list, lane_stats: dict, since_hours: float) -> str:
    """Morning breakdown text for BigSexyWarlock69."""
    lines = []
    now = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=-5))
    ).strftime("%Y-%m-%d %H:%M CDT")
    lines.append(f"# Swarm scan — {now} (last {since_hours}h)")
    lines.append("")
    if not hits:
        lines.append("Quiet. No new hits across all lanes.")
        lines.append("")
    else:
        # Priority hits first
        pri = [h for h in hits if h.get("priority")]
        if pri:
            lines.append(f"## Priority ({len(pri)}) — cloud/known-swarm IPs")
            for h in pri:
                ipc = h.get("ip_classification", {})
                lines.append(
                    f"- [{h['confidence']}] {h.get('summary','')[:120]} "
                    f"(IP {ipc.get('ip')} → {ipc.get('label')})")
            lines.append("")
        # Per-lane counts
        lines.append("## Per-lane hits")
        for lane, stats in sorted(lane_stats.items()):
            lines.append(
                f"- {lane}: {stats['hits']} hits "
                f"({stats['status']})")
        lines.append("")
        # Top findings (HIGH first, max 10)
        high = [h for h in hits if h.get("confidence") == "HIGH"][:10]
        if high:
            lines.append("## Top findings")
            for h in high:
                lines.append(f"- {h.get('summary','')[:160]}")
                lines.append(f"  {h.get('source_url','')}")
            lines.append("")
    # Lane status footer
    lines.append("## Lane status")
    for lane, stats in sorted(lane_stats.items()):
        lines.append(f"- {lane}: {stats['status']}")
    return "\n".join(lines)


def run_orchestrator(since_hours: float = 24,
                     dry_run: bool = False) -> dict:
    """Run all lanes. Returns {hits, lane_stats, breakdown, bundle_path}."""
    seen = _load_seen()
    hits = []
    lane_stats = {}
    run_id = datetime.datetime.now(
        datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for mod_name, lane_id, enabled in LANES:
        stats = {"hits": 0, "status": "ok"}
        if not enabled:
            stats["status"] = "disabled"
            lane_stats[lane_id] = stats
            continue
        try:
            mod = importlib.import_module(mod_name)
        except ImportError as e:
            stats["status"] = f"import failed: {e}"
            lane_stats[lane_id] = stats
            C.report_error(
                module=f"orchestrator/{lane_id}",
                error_type="ImportError",
                message=str(e),
                context={"lane_id": lane_id, "mod_name": mod_name},
            )
            continue
        try:
            lane_hits = mod.scan(since_hours=since_hours,
                                 seen_ids=seen, dry_run=dry_run)
            stats["hits"] = len(lane_hits)
            hits.extend(lane_hits)
        except Exception as e:
            stats["status"] = f"error: {type(e).__name__}: {e}"
            print(f"[orchestrator] lane {lane_id} failed:",
                  file=sys.stderr)
            traceback.print_exc()
            # Structured error for the self-modifier swarm
            C.report_error(
                module=f"orchestrator/{lane_id}",
                error_type=type(e).__name__,
                message=str(e),
                context={"lane_id": lane_id,
                         "since_hours": since_hours},
            )
        lane_stats[lane_id] = stats

    # Priority sort: priority flag first, then confidence
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (
        0 if h.get("priority") else 1,
        rank.get(h.get("confidence"), 3),
    ))

    bundle_path = None
    if hits and not dry_run:
        os.makedirs(STAGING_DIR, exist_ok=True)
        # JSONL staging
        jl_path = os.path.join(STAGING_DIR, f"hits-{run_id}.jsonl")
        with open(jl_path, "w") as f:
            for h in hits:
                f.write(json.dumps(h, ensure_ascii=False) + "\n")
        # Factum bundle (pre-built; worker submits separately)
        bundle = _build_factum_bundle(hits, run_id)
        bundle_path = os.path.join(STAGING_DIR, f"bundle-{run_id}.json")
        with open(bundle_path, "w") as f:
            json.dump(bundle, f, indent=1, ensure_ascii=False)
        _save_seen(seen)

    breakdown = _breakdown(hits, lane_stats, since_hours)
    return {
        "hits": hits,
        "lane_stats": lane_stats,
        "breakdown": breakdown,
        "bundle_path": bundle_path,
        "run_id": run_id,
    }


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Morning swarm-scan orchestrator")
    ap.add_argument("--since-hours", type=float, default=24)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = run_orchestrator(since_hours=args.since_hours,
                             dry_run=args.dry_run)
    if args.json:
        print(json.dumps({
            "run_id": result["run_id"],
            "lane_stats": result["lane_stats"],
            "hit_count": len(result["hits"]),
            "bundle_path": result["bundle_path"],
        }, indent=2))
    else:
        print(result["breakdown"])
        if result["bundle_path"]:
            print(f"\nBundle staged: {result['bundle_path']}",
                  file=sys.stderr)


if __name__ == "__main__":
    main()
