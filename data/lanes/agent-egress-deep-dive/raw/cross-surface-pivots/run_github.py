#!/usr/bin/env python3
"""GitHub issues + code pivots. Read-only GET via gh api. No POST.
Stops on a 403 / rate-limit block. Idempotent: skips existing files."""
import json, os, subprocess, sys, time

BASE = os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-egress-deep-dive/raw/cross-surface-pivots")
ITEMS = [
    ("amos", "AMOS Cursor agent", "AMOS stealer Cursor"),
    ("zenity", "AgentCorruption Bedrock", "AgentCorruption"),
    ("lifesciences345", "get_capability_snapshot", "get_capability_snapshot"),
    ("corbanu876", "CorbanuTerminal unshare", "CorbanuTerminal bubblewrap"),
    ("guidance1498", "validate_uri 168.63.129.16", "validate_uri metadata"),
    ("bootstrap108", "Project-Bootstrap-Protocol download run", "Project-Bootstrap-Protocol"),
    ("msagent1020", "ms-agent fetch URL safety", "ms-agent Jina fetch"),
    ("wingman278", "Wingman metadata endpoint DNS", "Wingman browser metadata"),
    ("hermes108236", "hermes-agent download script approval", "hermes-agent approval script"),
    ("openskynet77", "OpenSkynet web_extract", "web_extract metadata"),
    ("routify49535519", "routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com", "routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com"),
    ("mcptoolbox49429926", "mcp-toolbox CVE-2026-14540", "mcp-toolbox redirect"),
    ("cowork46622328", "Claude Cowork curl upload", "Claude Cowork"),
    ("sheets48349487", "ChatGPT Google Sheets workbook", "Google Sheets exfiltrates workbook"),
    ("gitlost48827858", "GitLost private repos", "GitLost"),
    ("sharedroot", "SharedRoot unshare", "SharedRoot"),
    ("bedrockdns", "Bedrock DNS exfiltration agent", "Bedrock DNS exfiltration"),
]

def gh(endpoint):
    r = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True, timeout=90)
    return r.returncode, r.stdout, r.stderr

def main():
    summary = {}
    spath = os.path.join(BASE, "github-summary.json")
    if os.path.exists(spath):
        summary = json.load(open(spath))
    for iid, qi, qc in ITEMS:
        summary.setdefault(iid, {})
        for kind, q in (("issues", qi), ("code", qc)):
            fn = f"gh-{kind}-{iid}.json"
            p = os.path.join(BASE, fn)
            if not os.path.exists(p):
                import urllib.parse
                qq = q + (" is:issue" if kind == "issues" else "")
                ep = "search/" + kind + "?q=" + urllib.parse.quote(qq) + "&per_page=5"
                rc, out, err = gh(ep)
                if rc != 0:
                    print(f"GH BLOCK {iid} {kind}: {err[:300]}", flush=True)
                    summary[iid][kind] = {"query": q, "total": None, "fetched": 0, "sample": [], "error": err[:300]}
                    with open(spath, "w") as f:
                        json.dump(summary, f, indent=2)
                    if "403" in err or "rate limit" in err.lower() or "API rate limit" in err:
                        print("HARD STOP github surface", flush=True)
                        return
                    time.sleep(5)
                    continue
                try:
                    data = json.loads(out)
                except Exception:
                    data = {"error": "unparsable", "raw": out[:300]}
                with open(p, "w") as f:
                    json.dump(data, f, indent=2)
                time.sleep(4)
            else:
                data = json.load(open(p))
            items = data.get("items", []) if isinstance(data, dict) else []
            sample = []
            for it in items:
                if kind == "issues":
                    sample.append(f"{it.get('repository_url','').split('/')[-1]}#{it.get('number')} | {it.get('title','')}"[:220])
                else:
                    sample.append(f"{it.get('repository',{}).get('full_name','')} | {it.get('path','')}"[:220])
            summary[iid][kind] = {"query": q, "total": data.get("total_count"), "fetched": len(items), "sample": sample, "error": data.get("error")}
            with open(spath, "w") as f:
                json.dump(summary, f, indent=2)
        print(f"done {iid} issues={summary[iid]['issues']['total']} code={summary[iid]['code']['total']}", flush=True)
    print("ALL DONE github")

if __name__ == "__main__":
    main()
