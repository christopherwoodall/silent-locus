#!/usr/bin/env python3
"""Shodan CLI for hunt personas. Auth via stored custom.shodan credential (surrogate exchange).
Uses curl for egress (urllib chokes on this VM's proxy env)."""
import sys, json, subprocess, urllib.parse
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/templates/skill/bin")
from dynamic_credentials import url_with_surrogate_query_param

HOSTS = ["api.shodan.io"]
BASE = "https://api.shodan.io"

def call(path, params=None, retries=3):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    url = url_with_surrogate_query_param(url, "custom.shodan", allowed_hosts=HOSTS)
    last_err = ""
    for attempt in range(retries):
        r = subprocess.run(["curl", "-s", "--max-time", "90", "-A", "muse-hunt/1.0", url],
                           capture_output=True, text=True, timeout=100)
        if r.returncode == 0 and r.stdout.strip():
            try:
                return json.loads(r.stdout)
            except json.JSONDecodeError:
                last_err = f"non-JSON response: {r.stdout[:200]}"
        else:
            last_err = f"curl rc={r.returncode} stderr={r.stderr.strip()[:200]}"
    raise RuntimeError(last_err or "empty response after retries")

def cmd_search(args):
    q = args[0]
    limit = int(args[1]) if len(args) > 1 else 10
    data = call("/shodan/host/search", {"query": q, "page": 1})
    out = []
    for m in data.get("matches", [])[:limit]:
        out.append({
            "ip": m.get("ip_str"),
            "port": m.get("port"),
            "org": m.get("org"),
            "isp": m.get("isp"),
            "hostnames": m.get("hostnames", []),
            "domains": m.get("domains", []),
            "product": m.get("product"),
            "transport": m.get("transport"),
            "timestamp": m.get("timestamp"),
        })
    print(json.dumps({"total": data.get("total"), "matches": out}, indent=1))

def cmd_host(args):
    ip = args[0]
    data = call(f"/shodan/host/{urllib.parse.quote(ip)}")
    data_list = data.get("data", [])
    if "--full" in args:
        print(json.dumps(data, indent=1)[:12000])
    else:
        slim = {k: data.get(k) for k in ("ip_str", "org", "isp", "asn", "hostnames", "domains", "ports", "vulns", "tags", "last_update")}
        slim["services"] = [
            {"port": s.get("port"), "product": s.get("product"), "transport": s.get("transport"),
             "http_host": (s.get("http") or {}).get("host"), "title": ((s.get("http") or {}).get("title") or "")[:120]}
            for s in data_list
        ]
        data = slim
    print(json.dumps(data, indent=1)[:6000])

def cmd_count(args):
    data = call("/shodan/host/count", {"query": args[0]})
    print(json.dumps({"total": data.get("total"), "facets": data.get("facets", {})}, indent=1))

def cmd_dns(args):
    data = call(f"/dns/domain/{urllib.parse.quote(args[0])}")
    print(json.dumps({k: data.get(k) for k in ("domain", "tags", "subdomains")}, indent=1))

CMDS = {"search": cmd_search, "host": cmd_host, "count": cmd_count, "dns": cmd_dns}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in CMDS:
        print(f"usage: {sys.argv[0]} {{{'|'.join(CMDS)}}} ...", file=sys.stderr)
        sys.exit(2)
    try:
        CMDS[sys.argv[1]](sys.argv[2:])
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
