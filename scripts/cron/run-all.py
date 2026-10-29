#!/usr/bin/env python3
"""Run every per-site monitor in scripts/cron/sites/ and aggregate.

Each site script runs in its own process (isolation: one site's crash
never takes down the sweep). Serial execution keeps request rates
polite. Exit 1 if any site reported ERROR; findings (NEW/CHANGED)
are normal output, not failures.

Usage:
    run-all.py [--dry-run] [--json] [--only <name>[,<name>...]]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITES_DIR = os.path.join(BASE_DIR, "sites")


def main() -> int:
    ap = argparse.ArgumentParser(description="run all site monitors")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--only", default=None,
                    help="comma-separated site names to run")
    args = ap.parse_args()

    scripts = sorted(glob.glob(os.path.join(SITES_DIR, "*.py")))
    scripts = [s for s in scripts
               if not os.path.basename(s).startswith("_")]
    if args.only:
        wanted = set(args.only.split(","))
        scripts = [s for s in scripts
                   if os.path.splitext(os.path.basename(s))[0] in wanted]

    aggregate = []
    for script in scripts:
        name = os.path.splitext(os.path.basename(script))[0]
        cmd = [sys.executable, script, "--json"]
        if args.dry_run:
            cmd.append("--dry-run")
        try:
            p = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=600)
            try:
                res = json.loads(p.stdout) if p.stdout.strip() else {}
            except ValueError:
                res = {}
            aggregate.append({
                "site": name,
                "ok": p.returncode == 0,
                "summary": res.get("summary", {}),
                "status": res.get("status"),
                "stderr_tail": p.stderr[-300:] if p.stderr else "",
            })
        except Exception as e:  # subprocess-level failure
            aggregate.append({"site": name, "ok": False,
                              "summary": {}, "status": "RUNNER_ERROR",
                              "stderr_tail": f"{type(e).__name__}: {e}"[:300]})

    interesting = [a for a in aggregate
                   if any(k not in ("UNCHANGED", "NO_NEW", "SKIPPED")
                           for k in a["summary"])]
    failed = [a for a in aggregate if not a["ok"]]

    if args.json or args.dry_run:
        print(json.dumps({"sites": aggregate,
                          "interesting": [a["site"] for a in interesting],
                          "failed": [a["site"] for a in failed]},
                         indent=2))
    else:
        print(f"{len(aggregate)} sites checked, "
              f"{len(interesting)} with findings, {len(failed)} failed")
        for a in interesting:
            print(f"  FINDING {a['site']}: {a['summary']}")
        for a in failed:
            print(f"  FAILED  {a['site']}: {a['stderr_tail']}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
