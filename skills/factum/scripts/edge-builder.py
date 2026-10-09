#!/usr/bin/env python3
"""
Factum edge-builder: finds connections between records and surfaces them as edges.

Generic tool — works with any observation type and tag scheme via CLI config.

For each observation of the configured type without existing edges:
1. Extract the configured term field
2. Match it against the corpus
3. Filter to hits in a different group (per --group-tag)
4. Skip if an edge already exists
5. Create edge records for new connections
6. Report new connections

Usage:
  edge-builder.py --repo PATH --type infra.ioc --term-field data.term --group-tag lane
  edge-builder.py --repo PATH --type web.capture --term-field data.final_url --group-tag lane --dry-run
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
        print(f"factum error: {result.stderr}", file=sys.stderr)
        return None
    return json.loads(result.stdout)


def get_field(record, field_path):
    """Extract a nested field via dot path, e.g. 'data.term'."""
    value = record.get("body", {})
    for part in field_path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Factum repository path")
    parser.add_argument("--type", dest="obs_type", required=True,
                        help="Observation type to process (e.g. infra.ioc)")
    parser.add_argument("--term-field", default="data.term",
                        help="Dot path to the matchable value (default: data.term)")
    parser.add_argument("--group-tag", default="lane",
                        help="Tag key defining groups; only cross-group edges (default: lane)")
    parser.add_argument("--min-term-len", type=int, default=4,
                        help="Skip terms shorter than this (default: 4)")
    parser.add_argument("--categories", default=None,
                        help="Comma-separated IOC categories to process (e.g. proxy,dead-drop,url). Skips generic terms.")
    parser.add_argument("--limit", type=int, default=100,
                        help="Max observations to process (default: 100)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report only, don't create edges")
    parser.add_argument("--actor", default="agent:edge-builder",
                        help="Actor for edge submissions")
    args = parser.parse_args()

    repo = args.repo

    # Load existing edges to avoid duplicates
    existing = set()
    qfile = "/tmp/edge-builder-existing.json"
    Path(qfile).write_text(json.dumps({"kind": "edge", "limit": 500}))
    result = run_factum(repo, "query", "--input", qfile)
    if result and result.get("ok"):
        for r in result.get("records", []):
            body = r.get("body", {})
            existing.add((body.get("from"), body.get("to")))
    print(f"Existing edges: {len(existing)}", file=sys.stderr)

    # Get observations of the configured type
    qfile2 = "/tmp/edge-builder-obs.json"
    Path(qfile2).write_text(json.dumps({"kind": "observation", "limit": args.limit}))
    result = run_factum(repo, "query", "--input", qfile2)
    if not result or not result.get("ok"):
        print("Failed to query observations", file=sys.stderr)
        return 1

    new_edges = []
    checked = 0
    allowed_cats = set(args.categories.split(",")) if args.categories else None

    for record in result.get("records", []):
        body = record.get("body", {})
        if body.get("type") != args.obs_type:
            continue
        # Category filter (for infra.ioc and similar)
        if allowed_cats:
            cat = body.get("data", {}).get("category", "")
            if cat not in allowed_cats:
                continue
        term = get_field(record, args.term_field)
        if not term or not isinstance(term, str) or len(term) < args.min_term_len:
            continue
        checked += 1

        match_result = run_factum(repo, "match", "--text", term, "--mode", "fuzzy")
        if not match_result or match_result.get("status") != "found":
            continue

        record_id = record.get("id")
        record_group = record.get("tags", {}).get(args.group_tag, "unknown")

        for hit in match_result.get("matches", []):
            hit_id = hit.get("id", "")
            if hit_id == record_id or (record_id, hit_id) in existing:
                continue
            # Cross-group filter: match results don't include tags,
            # so we check via the hit's lane if available
            hit_group = hit.get("tags", {}).get(args.group_tag, "unknown")
            if hit_group == "unknown" or hit_group == record_group:
                continue  # Same group or unknown — not a cross-lane connection
            new_edges.append({
                "from": record_id,
                "to": hit_id,
                "term": term,
                "record_group": record_group,
                "hit_group": hit_group,
            })

    print(f"Checked {checked} observations, {len(new_edges)} new edge candidates",
          file=sys.stderr)

    if args.dry_run:
        for e in new_edges:
            print(json.dumps(e))
        return 0

    # TODO: submit edges via `add` with dedup check
    print("Submission not yet implemented — use --dry-run to review candidates",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
