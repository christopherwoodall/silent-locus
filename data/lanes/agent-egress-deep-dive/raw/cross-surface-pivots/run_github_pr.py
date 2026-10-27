#!/usr/bin/env python3
"""PR-side issues search for the 3 PR-origin items. Read-only GET.
The search/issues endpoint needs is:issue OR is:pull-request; one query
cannot carry both, so PR-origin items get a second, labelled query."""
import json, os, subprocess, time, urllib.parse

BASE = os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-egress-deep-dive/raw/cross-surface-pivots")
ITEMS = [
    ("corbanu876", "CorbanuTerminal unshare"),
    ("msagent1020", "ms-agent fetch URL safety"),
    ("hermes108236", "hermes-agent download script approval"),
]

def main():
    spath = os.path.join(BASE, "github-summary.json")
    summary = json.load(open(spath))
    for iid, q in ITEMS:
        fn = f"gh-issuespr-{iid}.json"
        p = os.path.join(BASE, fn)
        if not os.path.exists(p):
            qq = q + " is:pull-request"
            ep = "search/issues?q=" + urllib.parse.quote(qq) + "&per_page=5"
            r = subprocess.run(["gh", "api", ep], capture_output=True, text=True, timeout=90)
            if r.returncode != 0:
                print(f"BLOCK {iid}: {r.stderr[:200]}", flush=True)
                summary[iid]["issues_pr"] = {"query": qq, "total": None, "fetched": 0, "sample": [], "error": r.stderr[:200]}
            else:
                data = json.loads(r.stdout)
                with open(p, "w") as f:
                    json.dump(data, f, indent=2)
                items = data.get("items", [])
                summary[iid]["issues_pr"] = {"query": qq, "total": data.get("total_count"), "fetched": len(items),
                    "sample": [f"{it.get('repository_url','').split('/')[-1]}#{it.get('number')} | {it.get('title','')}"[:220] for it in items], "error": None}
            with open(spath, "w") as f:
                json.dump(summary, f, indent=2)
            time.sleep(4)
        print(f"done {iid} pr={summary[iid].get('issues_pr',{}).get('total')}", flush=True)
    print("ALL DONE pr")

if __name__ == "__main__":
    main()
