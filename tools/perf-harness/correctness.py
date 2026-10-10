#!/usr/bin/env python3
"""Correctness verification for Factum performance experiments.

Two modes:
  --save-golden : capture reference results from the current repo state
  --compare     : compare current repo state against saved golden results

Checks:
  1. Record count matches (from verify)
  2. match results identical for a fixed query set (by record ID set)
  3. query tag-filter count matches
  4. verify passes (verified=true, pending=0)

Exit code 0 if all checks pass, 1 otherwise.
"""

import argparse
import json
import os
import subprocess
import sys

# Fixed query set for result comparison.
# Each entry: (name, argv). Results compared by sorted record ID list.
MATCH_QUERIES = [
    ("exact_da.gd", ["match", "--text", "da.gd", "--mode", "exact", "--limit", "50"]),
    ("exact_zz", ["match", "--text", "zz", "--mode", "exact", "--limit", "50"]),
    ("fuzzy_exploitgym", ["match", "--text", "exploitgym", "--mode", "fuzzy", "--limit", "50"]),
    ("fuzzy_da.gd", ["match", "--text", "da.gd", "--mode", "fuzzy", "--limit", "50"]),
]

QUERY_TAG_INPUT = {"tags": {"lane": "da-gd-shortener"}, "count": True}


def run_factum(factum_py, repo, argv, timeout, env, input_file=None):
    cmd = [sys.executable, factum_py, "--repo", repo] + argv
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            env=env, cwd=os.path.dirname(factum_py),
        )
        return proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        return "", f"TIMEOUT after {timeout}s", -1


def extract_match_ids(stdout):
    """Extract sorted list of matched record IDs from match output."""
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return None
    matches = data.get("matches", [])
    ids = sorted(m.get("id") for m in matches if m.get("id"))
    return ids


def capture_state(factum_py, repo, timeout, env, workdir):
    """Run all correctness probes, return state dict."""
    state = {"match_results": {}, "query_counts": {}, "verify": {}}

    for name, argv in MATCH_QUERIES:
        stdout, stderr, rc = run_factum(factum_py, repo, argv, timeout, env)
        if rc != 0:
            state["match_results"][name] = {"error": stderr[-300:], "rc": rc}
        else:
            ids = extract_match_ids(stdout)
            if ids is None:
                state["match_results"][name] = {"error": "unparseable output", "rc": rc}
            else:
                state["match_results"][name] = {"ids": ids, "count": len(ids)}

    # query tag count
    qpath = os.path.join(workdir, "_correctness_query.json")
    with open(qpath, "w") as f:
        json.dump(QUERY_TAG_INPUT, f)
    stdout, stderr, rc = run_factum(
        factum_py, repo, ["query", "--input", qpath], timeout, env)
    try:
        os.remove(qpath)
    except OSError:
        pass
    if rc != 0:
        state["query_counts"]["da-gd-shortener"] = {"error": stderr[-300:], "rc": rc}
    else:
        try:
            data = json.loads(stdout)
            state["query_counts"]["da-gd-shortener"] = {"count": data.get("count")}
        except json.JSONDecodeError:
            state["query_counts"]["da-gd-shortener"] = {"error": "unparseable"}

    # verify
    stdout, stderr, rc = run_factum(factum_py, repo, ["verify"], timeout, env)
    if rc != 0:
        state["verify"] = {"error": stderr[-300:], "rc": rc}
    else:
        try:
            data = json.loads(stdout)
            state["verify"] = {
                "verified": data.get("verified"),
                "records": data.get("records"),
                "pending": data.get("pending"),
            }
        except json.JSONDecodeError:
            state["verify"] = {"error": "unparseable"}

    return state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--golden", required=True,
                        help="Path to golden JSON file")
    parser.add_argument("--timeout", type=int, default=600)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--save-golden", action="store_true")
    mode.add_argument("--compare", action="store_true")
    args = parser.parse_args()

    repo = os.path.abspath(args.repo)
    factum_py = os.path.join(repo, "skills", "factum", "scripts", "factum.py")
    if not os.path.exists(factum_py):
        print(f"ERROR: factum.py not found at {factum_py}", file=sys.stderr)
        sys.exit(1)

    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.local/bin") + ":" + env.get("PATH", "")
    workdir = os.path.dirname(os.path.abspath(args.golden))
    os.makedirs(workdir, exist_ok=True)

    print("Capturing correctness state (this may take several minutes)...", flush=True)
    state = capture_state(factum_py, repo, args.timeout, env, workdir)

    if args.save_golden:
        with open(args.golden, "w") as f:
            json.dump(state, f, indent=2)
        print(f"Golden state saved to {args.golden}")
        # Report any capture errors
        errors = []
        for name, res in state["match_results"].items():
            if "error" in res:
                errors.append(f"match {name}: {res['error'][:100]}")
        for name, res in state["query_counts"].items():
            if "error" in res:
                errors.append(f"query {name}: {res['error'][:100]}")
        if "error" in state["verify"]:
            errors.append(f"verify: {state['verify']['error'][:100]}")
        if errors:
            print("WARNINGS during golden capture:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        print("Golden capture clean.")
        return

    # Compare mode
    with open(args.golden) as f:
        golden = json.load(f)

    failures = []

    # 1. Verify must pass on both
    gv, cv = golden.get("verify", {}), state.get("verify", {})
    if gv.get("verified") is not True:
        failures.append(f"golden verify was not clean: {gv}")
    if cv.get("verified") is not True:
        failures.append(f"current verify failed: {cv}")
    if gv.get("records") != cv.get("records"):
        failures.append(
            f"record count changed: golden={gv.get('records')} current={cv.get('records')}")
    if cv.get("pending") not in (0, None) and cv.get("pending") != 0:
        failures.append(f"pending batches nonzero: {cv.get('pending')}")

    # 2. Match results must have identical ID sets
    for name in golden.get("match_results", {}):
        g = golden["match_results"][name]
        c = state["match_results"].get(name, {})
        if "error" in g or "error" in c:
            failures.append(f"match {name}: capture error golden={g.get('error','')} current={c.get('error','')}")
            continue
        if g.get("ids") != c.get("ids"):
            gset, cset = set(g.get("ids", [])), set(c.get("ids", []))
            failures.append(
                f"match {name}: ID set changed "
                f"(lost={sorted(gset - cset)[:5]}, gained={sorted(cset - gset)[:5]}, "
                f"golden_n={len(gset)}, current_n={len(cset)})")

    # 3. Query counts must match
    for name in golden.get("query_counts", {}):
        g = golden["query_counts"][name]
        c = state["query_counts"].get(name, {})
        if g.get("count") != c.get("count"):
            failures.append(
                f"query {name}: count changed golden={g.get('count')} current={c.get('count')}")

    print("\n=== Correctness comparison ===")
    if failures:
        print("FAILURES:")
        for f_ in failures:
            print(f"  FAIL: {f_}")
        sys.exit(1)
    print("All correctness checks PASSED:")
    print(f"  - verify clean, {cv.get('records')} records, 0 pending")
    print(f"  - {len(golden.get('match_results', {}))} match queries returned identical ID sets")
    print(f"  - {len(golden.get('query_counts', {}))} query counts matched")


if __name__ == "__main__":
    main()
