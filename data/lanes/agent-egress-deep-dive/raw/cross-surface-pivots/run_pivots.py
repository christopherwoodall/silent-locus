#!/usr/bin/env python3
"""Cross-surface pivots, agent-egress deep dive, lane 4.
Read-only. Idempotent: skip a query if its raw file already exists.
Surfaces: urlquery (uq.py), GitHub issues + code (gh api, GET only),
urlscan search metadata only, crt.sh (named hosts only).
No poster names. No signed values are written: only query strings,
totals, titles, paths, and counts are summarised.
"""
import json, os, subprocess, sys, time, urllib.parse, urllib.request

BASE = os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-egress-deep-dive/raw/cross-surface-pivots")
UQ = os.path.expanduser("~/workspace/skills/urlquery/bin/uq.py")
UA = "Muse-pivot-lane4/1.0"

ITEMS = [
    # id, uq, gh_issues, gh_code, urlscan, crtsh
    ("amos", "fieldeffect.com", "AMOS Cursor agent", "AMOS stealer Cursor", "fieldeffect.com", "fieldeffect.com"),
    ("zenity", "zenity.io", "AgentCorruption Bedrock", "AgentCorruption", "labs.zenity.io", "labs.zenity.io"),
    ("lifesciences345", "get_capability_snapshot", "get_capability_snapshot", "get_capability_snapshot", "get_capability_snapshot", None),
    ("corbanu876", "CorbanuTerminal", "CorbanuTerminal unshare", "CorbanuTerminal bubblewrap", "CorbanuTerminal", None),
    ("guidance1498", "guidance validate_uri", "validate_uri 168.63.129.16", "validate_uri metadata", "guidance validate_uri", None),
    ("bootstrap108", "Project-Bootstrap-Protocol", "Project-Bootstrap-Protocol download run", "Project-Bootstrap-Protocol", "Project-Bootstrap-Protocol", None),
    ("msagent1020", "ms-agent SSRF", "ms-agent fetch URL safety", "ms-agent Jina fetch", "ms-agent SSRF", None),
    ("wingman278", "Wingman metadata", "Wingman metadata endpoint DNS", "Wingman browser metadata", "Wingman metadata", None),
    ("hermes108236", "hermes-agent approval", "hermes-agent download script approval", "hermes-agent approval script", "hermes-agent", None),
    ("openskynet77", "OpenSkynet web_extract", "OpenSkynet web_extract", "web_extract metadata", "OpenSkynet web_extract", None),
    ("routify49535519", "routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com", "routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com", "routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com", "routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com", "routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com"),
    ("mcptoolbox49429926", "mcp-toolbox", "mcp-toolbox CVE-2026-14540", "mcp-toolbox redirect", "mcp-toolbox", None),
    ("cowork46622328", "Claude Cowork exfiltrates", "Claude Cowork curl upload", "Claude Cowork", "Claude Cowork", None),
    ("sheets48349487", "ChatGPT Google Sheets exfiltrates", "ChatGPT Google Sheets workbook", "Google Sheets exfiltrates workbook", "Google Sheets exfiltrates", "promptarmor.com"),
    ("gitlost48827858", "GitLost GitHub agent", "GitLost private repos", "GitLost", "GitLost", None),
    ("sharedroot", "SharedRoot Cowork unshare", "SharedRoot unshare", "SharedRoot", "SharedRoot", "bex.co"),
    ("bedrockdns", "Bedrock DNS exfiltration", "Bedrock DNS exfiltration agent", "Bedrock DNS exfiltration", "Bedrock DNS", None),
]

def save(name, obj):
    p = os.path.join(BASE, name)
    if os.path.exists(p):
        return False
    with open(p, "w") as f:
        if isinstance(obj, str):
            f.write(obj)
        else:
            json.dump(obj, f, indent=2)
    return True

def run(cmd, timeout=90):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -1, "", f"{type(e).__name__}: {e}"

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    summary = {}
    spath = os.path.join(BASE, "pivot-summary.json")
    if os.path.exists(spath):
        summary = json.load(open(spath))
    for item in ITEMS:
        iid, uq, ghi, ghc, us, crt = item
        if only and only not in (iid, "all"):
            continue
        summary.setdefault(iid, {})
        # urlquery
        fn = f"uq-{iid}.json"
        if not os.path.exists(os.path.join(BASE, fn)):
            rc, out, err = run(["python3", UQ, "search", "--query", uq, "--limit", "10"])
            try:
                data = json.loads(out) if out.strip() else {"error": err}
            except Exception:
                data = {"error": err, "raw": out[:500]}
            save(fn, data)
            time.sleep(3)
        d = json.load(open(os.path.join(BASE, fn)))
        reps = d.get("reports") or [] if isinstance(d, dict) else []
        titles = []
        for r in reps:
            t = (r.get("final") or {}).get("title") or (r.get("url") or {}).get("addr") or ""
            u = (r.get("url") or {}).get("addr") or ""
            titles.append(f"{u} | {t}"[:220])
        summary[iid]["urlquery"] = {"query": uq, "total": d.get("total_hits"), "fetched": len(reps), "sample": titles, "error": d.get("error")}
        # urlscan
        fn = f"urlscan-{iid}.json"
        if not os.path.exists(os.path.join(BASE, fn)):
            url = "https://urlscan.io/api/v1/search/?q=" + urllib.parse.quote(us, safe="") + "&size=20"
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read().decode())
            except Exception as e:
                data = {"error": f"{type(e).__name__}: {e}"}
            save(fn, data)
            time.sleep(2)
        d = json.load(open(os.path.join(BASE, fn)))
        res = d.get("results") or [] if isinstance(d, dict) else []
        titles = []
        for r in res:
            titles.append(f"{(r.get('page') or {}).get('url','')} | {(r.get('page') or {}).get('title','')}"[:220])
        summary[iid]["urlscan"] = {"query": us, "total": d.get("total"), "fetched": len(res), "sample": titles, "error": d.get("error"), "window": d.get("search_date_limit_days")}
        # crt.sh
        if crt:
            fn = f"crtsh-{iid}.json"
            if not os.path.exists(os.path.join(BASE, fn)):
                url = "https://crt.sh/?q=" + urllib.parse.quote(crt, safe="") + "&output=json&exclude=expired"
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                try:
                    with urllib.request.urlopen(req, timeout=60) as resp:
                        data = json.loads(resp.read().decode())
                except Exception as e:
                    data = {"error": f"{type(e).__name__}: {e}"}
                save(fn, data)
                time.sleep(10)
            d = json.load(open(os.path.join(BASE, fn)))
            if isinstance(d, list):
                summary[iid]["crtsh"] = {"query": crt, "total": len(d), "fetched": len(d), "sample": [x.get("common_name") for x in d[:5]], "error": None}
            else:
                summary[iid]["crtsh"] = {"query": crt, "total": None, "fetched": 0, "sample": [], "error": d.get("error")}
        else:
            summary[iid]["crtsh"] = {"query": None, "total": "N/A", "fetched": 0, "sample": [], "error": None}
        with open(spath, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"done {iid} uq={summary[iid]['urlquery']['total']} us={summary[iid]['urlscan']['total']} crt={summary[iid]['crtsh']['total']}", flush=True)
    print("ALL DONE (uq+urlscan+crtsh)")

if __name__ == "__main__":
    main()
