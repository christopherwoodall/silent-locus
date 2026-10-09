#!/usr/bin/env python3
"""
Provenance resolver: for a given term, find all records containing it
and report where each was first published/seen, with original timestamps.

Resolves:
- Transluce findings: via transluce_finding tag → finding created_at
- Our lanes: via source record timestamps or lane file dates

Usage: provenance.py --repo PATH --term "webhook.site"
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_factum(repo, *args):
    cmd = ["uv", "run", "skills/factum/scripts/factum.py", "--repo", repo] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)


def get_finding_date(repo, finding_id):
    """Look up a Transluce finding's created_at from its UPSTREAM claim."""
    qfile = "/tmp/prov-finding.json"
    Path(qfile).write_text(json.dumps({
        "kind": "observable", "limit": 5
    }))
    # Find the external_id observable for this finding
    result = run_factum(repo, "match", "--text", f"transluce-finding-{finding_id}", "--mode", "fuzzy")
    if not result or result.get("status") != "found":
        return None
    for m in result.get("matches", []):
        # The claim should cite this; for now return the match timestamp
        return m.get("record", {}).get("@timestamp", "")
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--term", required=True)
    args = parser.parse_args()

    result = run_factum(args.repo, "match", "--text", args.term, "--mode", "fuzzy")
    if not result or result.get("status") != "found":
        print(f"No hits for '{args.term}'")
        return 0

    print(f"Provenance for '{args.term}': {len(result['matches'])} hits\n")

    seen = []
    for m in result["matches"]:
        record = m.get("record", {})
        tags = m.get("tags", {})
        lane = tags.get("lane", "unknown")
        rid = m.get("id", "")[:25]
        ingest_ts = record.get("@timestamp", "")[:19]

        # Resolve original timestamp
        origin_ts = None
        origin_desc = None
        if lane == "transluce-ioc":
            fid = tags.get("transluce_finding", "?")
            origin_desc = f"Transluce finding #{fid}"
            finding_url = f"https://d3ncjnql1bmhe8.cloudfront.net/findings/{fid}"
            # Look up finding created_at and evidence links from the snapshot
            try:
                with open("evidence/transluce-api/raw/findings-list-20261008.json") as f:
                    findings = json.load(f)["items"]
                    for item in findings:
                        if str(item["id"]) == str(fid):
                            origin_ts = item["created_at"][:10]
                            ev_links = item["data"].get("evidence_links", [])
                            if ev_links:
                                origin_desc += f" | evidence: {ev_links[0][:60]}"
                            break
            except Exception:
                pass
            origin_desc += f" | {finding_url}"
        elif lane == "proxy-fresh-blood":
            origin_desc = "FRESH.md (2026-10-08)"
            origin_ts = "2026-10-08"
            origin_desc += " | data/lanes/proxy-fresh-blood/FRESH.md"
        elif lane == "webhook-deaddrops":
            origin_desc = "events.jsonl (2026-05-12)"
            origin_ts = "2026-05-12"
            origin_desc += " | data/lanes/webhook-deaddrops/events.jsonl"

        seen.append((origin_ts or ingest_ts, lane, rid, origin_desc, ingest_ts))

    # Sort by origin timestamp (earliest first = provenance)
    seen.sort(key=lambda x: x[0])
    for i, (ots, lane, rid, desc, its) in enumerate(seen):
        marker = " ← FIRST SEEN" if i == 0 else ""
        print(f"  {lane:20} | origin: {ots[:10]} | {desc}{marker}")
        print(f"  {'':20} | ingest: {its} | {rid}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
