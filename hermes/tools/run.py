#!/usr/bin/env python3
"""Hermes hunt-profile scanner runner.

Runs standalone from tools/. Config is tools/config.json,
resolved relative to this file, not the working directory.
Captures go to hermes/workspace/raw/. State goes to
hermes/workspace/state/.

Counsel gate, enforced from day one: ALL scanners ship
DISABLED. Enabling any scanner needs the operator's word
(TIER-B rule). Set enabled:true in that scanner's config
block only after the operator says so.

Commands:
  list
    Print each scanner, its enabled state, and its confidence
    cap. Makes no network call. This is the safe first check.

  run <scanner>
    Run one scanner. When the scanner is disabled, refuse with
    a clear message and a non-zero exit, and make NO network
    call. The enabled check happens BEFORE the scanner module
    is imported or any scan code runs. Only when
    enabled:true does the runner import the module and call
    scan(). Hits print as JSON when --json is given, else as
    short lines.

Options for run:
  --since-hours N  Look-back window in hours (default 24).
  --dry-run        Print the scan plan only. Zero network
                   calls, zero writes. Works even for a
                   disabled scanner, because a plan is not a scan.
                   Dry-run needs no operator approval: it prints
                   the plan only, with zero network calls and
                   zero writes.
  --json           Print hits as a JSON array.

Examples:
  python3 tools/run.py list
  python3 tools/run.py run urlscan
  python3 tools/run.py run prcomment --dry-run --json

Scanners: urlquery, urlscan, prcomment, shodan, crtsh,
wayback, iocfeeds, intel_slot5, telegraph.

Read-only, passive scanners only. GET only. No POST. No
login. No new session. No new account. No paid upgrade and
no account creation; keyed APIs use only operator-supplied
keys and consume operator plan quota.
API keys appear in config only as env-var names
("${NAME}"), never as values.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS_DIR)
import _common as C  # noqa: E402

SCANNERS = {
    "urlquery": "urlquery.net report watch (tag grammar, Amap "
                "targeting, payload and exfil shapes).",
    "urlscan": "urlscan.io anonymous search (fleet fingerprints "
               "in other people's scan metadata).",
    "prcomment": "GitHub PR/issue comment behavior patterns "
                 "(local regex match on fetched comments).",
    "shodan": "Shodan banner-count deltas for harness panels "
               "(Cairn, Strix, Hermes Agent).",
    "crtsh": "crt.sh Certificate Transparency watch for fleet "
             "proxy certs.",
    "wayback": "Wayback CDX watch for new fleet captures.",
    "iocfeeds": "AlienVault OTX third-party pulses on watched "
                "indicators (keyless lookup).",
    "intel_slot5": "New-post watch on swarmcha.se and "
                   "norforge.com via the jina reader.",
    "telegraph": "Content/view delta watch on watched "
                 "telegra.ph pages (public API).",
}


def _config() -> dict:
    return C.load_config()


def cmd_list() -> int:
    """Print each scanner, its enabled state, its confidence cap.

    No network call. Reads config only.
    """
    cfg = _config()
    blocks = cfg.get("scanners", {})
    print(f"{'scanner':<12} {'enabled':<9} {'cap':<7} description")
    for name in sorted(SCANNERS):
        block = blocks.get(name, {})
        enabled = block.get("enabled", False) is True
        cap = block.get("confidence_cap", "unknown")
        grade = block.get("grade", "")
        print(f"{name:<12} {str(enabled):<9} {cap:<7} "
              f"{SCANNERS[name]} (grade {grade})")
    print("\nAll scanners ship disabled. Enabling one needs the "
          "operator's word (TIER-B rule).")
    return 0


def cmd_run(name: str, since_hours: float, dry_run: bool,
            as_json: bool) -> int:
    """Run one scanner, or refuse when it is disabled.

    Refusal path: clear message, exit code 2, NO network call.
    The enabled check runs before the scanner module import.
    """
    if name not in SCANNERS:
        print(f"error: unknown scanner {name!r}. Known scanners: "
              f"{', '.join(sorted(SCANNERS))}", file=sys.stderr)
        return 2
    cfg = _config()
    block = cfg.get("scanners", {}).get(name, {})
    if not dry_run and block.get("enabled", False) is not True:
        print(f"refused: scanner {name!r} is disabled in "
              f"tools/config.json (enabled:false). All scanners ship "
              f"disabled. Enabling one needs the operator's word "
              f"(TIER-B rule). No network call was made.",
              file=sys.stderr)
        return 2
    try:
        module = importlib.import_module(name)
    except Exception as e:
        print(f"error: could not import scanner {name!r}: "
              f"{type(e).__name__}: {e}", file=sys.stderr)
        return 1
    try:
        hits = module.scan(since_hours=since_hours, dry_run=dry_run)
    except SystemExit:
        raise
    except Exception as e:
        print(f"error: scanner {name!r} failed: "
              f"{type(e).__name__}: {e}", file=sys.stderr)
        return 1
    C.emit(hits, as_json, dry_run)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="run.py",
        description="Hermes hunt-profile scanner runner. "
                    "list prints each scanner, its enabled state, "
                    "and its confidence cap (no network). "
                    "run <scanner> runs one scanner, but refuses "
                    "with a non-zero exit and no network call when "
                    "the scanner is disabled. All scanners ship "
                    "disabled; enabling one needs the operator's "
                    "word (TIER-B rule).")
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="Print each scanner, its enabled "
                                "state, and its confidence cap. "
                                "No network call.")
    run_p = sub.add_parser("run", help="Run one scanner. Refuses "
                                       "with exit 2 and no network "
                                       "call when disabled; only "
                                       "executes when enabled:true.")
    run_p.add_argument("scanner", choices=sorted(SCANNERS),
                       help="Scanner name (see list).")
    run_p.add_argument("--since-hours", type=float, default=24,
                       help="Look-back window in hours (default 24).")
    run_p.add_argument("--dry-run", action="store_true",
                       help="Print the scan plan only; zero network "
                            "calls, zero writes. Needs no operator "
                            "approval.")
    run_p.add_argument("--json", action="store_true",
                       help="Print hits as a JSON array.")
    args = ap.parse_args(argv)
    if args.command == "list":
        return cmd_list()
    return cmd_run(args.scanner, args.since_hours, args.dry_run,
                   args.json)


if __name__ == "__main__":
    sys.exit(main())
