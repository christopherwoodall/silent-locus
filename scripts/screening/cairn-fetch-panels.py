#!/usr/bin/env python3
"""Lantern Phase 2 fetcher: passive GET profiling of open panels.

GET only. Follows redirects (curl -L). No POST, no login attempts, no forms,
no session creation. 1.5s politeness sleep between requests, 20s max per request.
One pass only. Saves raw body + headers + provenance + sha256 per (ip,port).
"""
import json, os, subprocess, time, hashlib, sys
from datetime import datetime, timezone

BASE = os.path.expanduser("~/workspace/silent-locus/data/lanes/cairn-panels")
RAW = os.path.join(BASE, "raw/panels")
WORK = os.path.join(BASE, "working")
os.makedirs(RAW, exist_ok=True)

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
# Ports we will NOT touch with HTTP: mail/ssh/dns/snmp/ldap/db/rdp/vnc/ftp/pptp + 50050 (Cobalt Strike C2, do not touch)
SKIP_PORTS = {21, 22, 25, 53, 110, 143, 161, 389, 465, 587, 993, 995,
              1433, 1723, 3268, 3269, 3270, 3306, 3389, 5432, 5900, 50050}
HTTPS_FIRST = {443, 8443, 9443}

def load_targets():
    hosts = []
    inv = {}
    for line in open(os.path.join(WORK, "host-inventory.jsonl"), encoding="utf-8"):
        d = json.loads(line)
        inv[d["ip"]] = d
        if d["panel_status"] == "open_dashboard":
            hosts.append(d)
    targets = []  # (ip, port, harness)
    def add(ip, port, harness):
        if (ip, port, harness) not in targets:
            targets.append((ip, port, harness))
    # Priority 1: 47.97.206.32 (port 8000 only; never 50050)
    d = inv.get("47.97.206.32")
    if d and 8000 in d["ports"]:
        add("47.97.206.32", 8000, d["harness"])
    # Priority 2: AS56971 open_dashboard hosts
    for h in hosts:
        if h["asn"] == "AS56971":
            for p in h["ports"]:
                add(h["ip"], p, h["harness"])
    # Priority 3: 71.185.26.179
    d = inv.get("71.185.26.179")
    if d:
        for p in d["ports"]:
            add("71.185.26.179", p, d["harness"])
    # Priority 4: OpenClaw co-located
    for ip in ("1.12.52.103", "208.73.203.9"):
        d = inv.get(ip)
        if d:
            for p in d["ports"]:
                add(ip, p, d["harness"])
    # Priority 5: everything else
    for h in hosts:
        for p in h["ports"]:
            add(h["ip"], p, h["harness"])
    return targets

def fetch_one(ip, port, harness):
    stem = f"{ip}_{port}"
    body_p = os.path.join(RAW, stem + ".html")
    head_p = os.path.join(RAW, stem + ".headers.txt")
    prov_p = os.path.join(RAW, stem + ".PROVENANCE.txt")
    sha_p = os.path.join(RAW, stem + ".sha256")
    if port in SKIP_PORTS:
        return {"ip": ip, "port": port, "harness": harness, "reachable": None,
                "skipped": True, "skip_reason": "non_http_port"}
    schemes = ["https", "http"] if port in HTTPS_FIRST else ["http", "https"]
    rec = {"ip": ip, "port": port, "harness": harness, "reachable": False,
           "http_status": None, "final_url": None, "url": None,
           "scheme": None, "fetch_error": None, "size": 0}
    ts = datetime.now(timezone.utc).isoformat()
    for scheme in schemes:
        url = f"{scheme}://{ip}:{port}/"
        tmp_body = body_p + ".tmp"
        try:
            r = subprocess.run(
                ["curl", "-sS", "-k", "-L", "--max-redirs", "5",
                 "--connect-timeout", "10", "--max-time", "20",
                 "-A", UA, "-D", head_p, "-o", tmp_body,
                 "-w", "%{http_code}|%{url_effective}|%{size_download}|%{content_type}",
                 url],
                capture_output=True, text=True, timeout=40)
        except subprocess.TimeoutExpired:
            rec["fetch_error"] = "curl_subprocess_timeout"
            continue
        parts = (r.stdout or "").strip().split("|")
        code = parts[0] if parts else ""
        final = parts[1] if len(parts) > 1 else url
        size = parts[2] if len(parts) > 2 else "0"
        ctype = parts[3] if len(parts) > 3 else ""
        rec.update({"url": url, "scheme": scheme, "http_status": code,
                    "final_url": final, "size": int(size or 0),
                    "content_type": ctype})
        if code == "000" or code == "":
            # connection failed -> try other scheme
            rec["fetch_error"] = (r.stderr or "").strip()[:200]
            if scheme == schemes[0]:
                continue
            break
        # got an HTTP response
        rec["reachable"] = True
        rec["fetch_error"] = None
        try:
            os.replace(tmp_body, body_p)
        except OSError as e:
            rec["fetch_error"] = f"body_write_failed: {e}"
            if os.path.exists(tmp_body):
                os.remove(tmp_body)
            break
        digest = hashlib.sha256(open(body_p, "rb").read()).hexdigest()
        with open(sha_p, "w") as f:
            f.write(digest + "  " + stem + ".html\n")
        with open(prov_p, "w") as f:
            f.write(
                f"url: {url}\nfinal_url: {final}\nhttp_status: {code}\n"
                f"timestamp_utc: {ts}\nmethod: GET\ntool: curl (passive)\n"
                f"note: single-pass passive collection; GET only, no POST/login/interaction\n")
        break
    if not rec["reachable"] and os.path.exists(body_p + ".tmp"):
        os.remove(body_p + ".tmp")
    return rec

def main():
    targets = load_targets()
    # resume: skip (ip,port) already fetched with a real HTTP response
    done = set()
    fl_path = os.path.join(WORK, "fetch-log.jsonl")
    if os.path.exists(fl_path):
        for line in open(fl_path, encoding="utf-8"):
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("reachable"):
                done.add((d["ip"], d["port"]))
    todo = [t for t in targets if (t[0], t[1]) not in done]
    print(f"targets: {len(targets)}, already fetched: {len(done)}, remaining: {len(todo)}", flush=True)
    log = open(fl_path, "a", encoding="utf-8")
    for i, (ip, port, harness) in enumerate(todo):
        rec = fetch_one(ip, port, harness)
        log.write(json.dumps(rec) + "\n")
        log.flush()
        print(f"[{i+1}/{len(todo)}] {ip}:{port} -> {rec.get('http_status') or rec.get('skip_reason') or rec.get('fetch_error')}",
              flush=True)
        time.sleep(1.5)
    log.close()
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
