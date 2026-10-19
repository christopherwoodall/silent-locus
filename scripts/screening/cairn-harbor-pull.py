#!/usr/bin/env python3
"""Harbor pull script: paginated Shodan search + full host records + api-info.
Uses the SAME stored-credential surrogate flow as the shodan connector
(custom.legacy-shodan provider); no raw credentials handled here.
Shodan API only. No contact with target hosts.
"""
import sys, json, time, subprocess, urllib.parse
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import url_with_surrogate_query_param

HOSTS = ["api.shodan.io"]
BASE = "https://api.shodan.io"

def call(path, params=None, retries=4):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    url = url_with_surrogate_query_param(url, "custom.shodan", allowed_hosts=HOSTS)
    last_err = ""
    for attempt in range(retries):
        r = subprocess.run(["curl", "-s", "--max-time", "120", "-A", "muse-hunt/1.0", url],
                           capture_output=True, text=True, timeout=130)
        if r.returncode == 0 and r.stdout.strip():
            try:
                return json.loads(r.stdout)
            except json.JSONDecodeError:
                body = r.stdout[:200]
                if "Rate limit" in body or "429" in body:
                    last_err = "rate limited (429-ish)"
                    time.sleep(5 * (attempt + 1))
                    continue
                last_err = f"non-JSON response: {body}"
        else:
            last_err = f"curl rc={r.returncode} stderr={r.stderr.strip()[:200]}"
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(last_err or "empty response after retries")

def cmd_apiinfo(args):
    d = call("/api-info")
    print(json.dumps(d, indent=1))

def cmd_search_all(args):
    """search-all '<query>' <outfile.jsonl> [max_pages] — full match dicts, one per line."""
    q, outfile = args[0], args[1]
    max_pages = int(args[2]) if len(args) > 2 else 1000
    first = call("/shodan/host/search", {"query": q, "page": 1})
    total = first.get("total", 0)
    pages = (total + 99) // 100
    pages = min(pages, max_pages)
    n = 0
    with open(outfile, "w") as f:
        for page in range(1, pages + 1):
            d = first if page == 1 else call("/shodan/host/search", {"query": q, "page": page})
            for m in d.get("matches", []):
                f.write(json.dumps(m) + "\n")
                n += 1
            f.flush()
            time.sleep(1.0)
    print(json.dumps({"query": q, "total": total, "pages": pages, "written": n}, indent=1))

def cmd_host_full(args):
    """host-full <ip> <outfile.json> — untruncated host record. 429-aware."""
    ip, outfile = args[0], args[1]
    try:
        d = call(f"/shodan/host/{urllib.parse.quote(ip)}")
    except RuntimeError as e:
        print(json.dumps({"ip": ip, "error": str(e)}))
        sys.exit(3)
    with open(outfile, "w") as f:
        json.dump(d, f, indent=1)
    print(json.dumps({"ip": ip, "ports": d.get("ports"), "services": len(d.get("data", []))}, indent=1))

CMDS = {"apiinfo": cmd_apiinfo, "search-all": cmd_search_all, "host-full": cmd_host_full}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(f"usage: {sys.argv[0]} {'|'.join(CMDS)} ...", file=sys.stderr)
        sys.exit(2)
    try:
        CMDS[sys.argv[1]](sys.argv[2:])
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
