#!/usr/bin/env python3
"""Benchmark Factum CLI operations.

Times each operation and outputs JSON with timing results.
Exit code 0 on success, 1 if any operation fails.

Usage: benchmark.py --repo <path> --output <json_path> [--timeout <seconds>]
"""

import argparse
import json
import subprocess
import sys
import time
import os

# Operations to benchmark: (name, argv)
# Each uses --repo <repo> prefix added at runtime.
# NB: match --mode key is omitted -- it requires a valid observable type and
# fails closed otherwise; exact/fuzzy are the critical perf paths.
OPERATIONS = [
    # match modes
    ("match_exact", ["match", "--text", "da.gd", "--mode", "exact", "--limit", "25"]),
    ("match_fuzzy", ["match", "--text", "exploitgym", "--mode", "fuzzy", "--limit", "25"]),
    # query with tag filter (count only, fast path)
    ("query_tag_count", None),  # special-cased: needs --input file
    # graph on a node (node ID resolved at runtime from match_exact)
    ("graph_depth1", None),  # special-cased
    # status and verify
    ("status", ["status"]),
    ("verify", ["verify"]),
]

QUERY_INPUT = {"tags": {"lane": "da-gd-shortener"}, "count": True}


def run_factum(factum_py, repo, argv, timeout, env):
    """Run one factum command, return (elapsed_seconds, stdout, stderr, returncode)."""
    cmd = [sys.executable, factum_py, "--repo", repo] + argv
    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            cwd=os.path.dirname(factum_py),
        )
        elapsed = time.monotonic() - start
        return elapsed, proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - start
        return elapsed, "", f"TIMEOUT after {timeout}s", -1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to factum repo")
    parser.add_argument("--output", required=True, help="Output JSON path")
    parser.add_argument("--timeout", type=int, default=600,
                        help="Per-operation timeout in seconds (default 600)")
    args = parser.parse_args()

    repo = os.path.abspath(args.repo)
    factum_py = os.path.join(repo, "skills", "factum", "scripts", "factum.py")
    if not os.path.exists(factum_py):
        print(f"ERROR: factum.py not found at {factum_py}", file=sys.stderr)
        sys.exit(1)

    # Ensure uv-installed deps are importable: use the same python invocation
    # the repo's workers use. We call factum.py directly with sys.executable.
    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.local/bin") + ":" + env.get("PATH", "")

    results = {"repo": repo, "operations": {}, "errors": []}

    # Write query input file
    query_input_path = os.path.join(os.path.dirname(args.output), "_query_input.json")
    with open(query_input_path, "w") as f:
        json.dump(QUERY_INPUT, f)

    node_id = None  # resolved from match_exact for graph test

    for name, argv in OPERATIONS:
        if name == "query_tag_count":
            argv = ["query", "--input", query_input_path]
        elif name == "graph_depth1":
            if node_id is None:
                results["operations"][name] = {
                    "status": "skipped",
                    "reason": "no node_id from match_exact",
                }
                continue
            argv = ["graph", node_id, "--depth", "1", "--limit", "25"]

        print(f"  timing {name} ...", flush=True)
        elapsed, stdout, stderr, rc = run_factum(factum_py, repo, argv, args.timeout, env)

        op = {
            "elapsed_seconds": round(elapsed, 2),
            "returncode": rc,
            "status": "ok" if rc == 0 else "failed",
        }
        if rc != 0:
            op["stderr_tail"] = stderr[-500:] if stderr else ""
            results["errors"].append(name)
        else:
            # Try to extract a result count for sanity
            try:
                data = json.loads(stdout)
                if isinstance(data, dict):
                    if "count" in data:
                        op["result_count"] = data["count"]
                    elif "records" in data and isinstance(data["records"], list):
                        op["result_count"] = len(data["records"])
                    elif "matches" in data and isinstance(data["matches"], list):
                        op["result_count"] = len(data["matches"])
            except (json.JSONDecodeError, TypeError):
                pass

        results["operations"][name] = op

        # Resolve a node ID from match_exact for the graph test
        if name == "match_exact" and rc == 0:
            try:
                data = json.loads(stdout)
                matches = data.get("matches", [])
                if matches:
                    node_id = matches[0].get("id")
                    print(f"  graph test node: {node_id}", flush=True)
            except (json.JSONDecodeError, TypeError, IndexError):
                pass

    # Cleanup
    try:
        os.remove(query_input_path)
    except OSError:
        pass

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nBenchmark complete: {args.output}")
    failed = results["errors"]
    if failed:
        print(f"FAILED operations: {failed}")
        sys.exit(1)
    print("All operations completed successfully.")


if __name__ == "__main__":
    main()
