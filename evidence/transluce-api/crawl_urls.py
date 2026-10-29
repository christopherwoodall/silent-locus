#!/usr/bin/env python3
"""One-shot crawl of NEW URLs from the Transluce findings inventory.

Reads url-inventory.jsonl, fetches status=NEW URLs with curl (priority:
urlquery reports first, then web.archive.org, then rest), saves raw bytes
under raw/crawl/ and writes raw/crawl/MANIFEST.jsonl.

Doctrine: curl-based; http:// for web.archive.org (port 80, flaky backend);
max ~2 req/sec per host; back off on 429/503; never redact; record errors.
"""
import json, os, sys, time, hashlib, subprocess, urllib.parse
from datetime import datetime, timezone

BASE = os.path.expanduser("~/workspace/silent-locus/data/transluce-api")
INV = os.path.join(BASE, "url-inventory.jsonl")
OUTDIR = os.path.join(BASE, "raw", "crawl")
MANIFEST = os.path.join(OUTDIR, "MANIFEST.jsonl")
UA = "silent-locus/transluce-crawl (security research; volunteer findings tracker)"

os.makedirs(OUTDIR, exist_ok=True)

def host_of(url):
    try:
        return urllib.parse.urlparse(url).netloc.lower()
    except Exception:
        return "unknown"

def ext_for(ctype, url):
    ctype = (ctype or "").split(";")[0].strip().lower()
    mapping = {
        "text/html": "html", "application/json": "json",
        "text/plain": "txt", "text/csv": "csv",
        "application/pdf": "pdf", "application/zip": "zip",
        "image/png": "png", "image/jpeg": "jpg",
    }
    if ctype in mapping:
        return mapping[ctype]
    # fall back to URL path suffix
    path = urllib.parse.urlparse(url).path
    suf = os.path.splitext(path)[1].lstrip(".").lower()[:8]
    return suf if suf and all(c.isalnum() for c in suf) else "bin"

def fetch(url, host_last):
    """Returns (http_code, body_bytes, content_type, error)."""
    target = url
    if "web.archive.org" in target and target.startswith("https://"):
        target = "http://" + target[len("https://"):]
    # per-host pacing: >=0.6s gap
    now = time.time()
    gap = 0.6 if "web.archive.org" not in target else 1.0
    last = host_last.get(host_of(target), 0)
    if now - last < gap:
        time.sleep(gap - (now - last))
    attempts = 2 if "web.archive.org" in target else 2
    err = None
    for attempt in range(attempts):
        cmd = ["curl", "-sS", "-L", "--max-redirs", "5",
               "-m", "90" if "web.archive.org" in target else "60",
               "-A", UA, "--max-filesize", "52428800",
               "-D", "-", "-o", "-", target]
        try:
            p = subprocess.run(cmd, capture_output=True, timeout=120)
        except subprocess.TimeoutExpired:
            err = "curl timeout expired"
            continue
        out = p.stdout
        # split headers/body on last header block
        sep = b"\r\n\r\n"
        idx = out.rfind(sep)
        if idx == -1:
            err = f"curl exit {p.returncode}: {p.stderr.decode()[:200]}"
            code, body, ctype = 0, b"", ""
        else:
            head, body = out[:idx], out[idx + len(sep):]
            lines = head.decode("latin1").split("\r\n")
            code = 0
            ctype = ""
            for ln in lines:
                if ln.startswith("HTTP/"):
                    try:
                        code = int(ln.split()[1])
                    except Exception:
                        pass
                elif ln.lower().startswith("content-type:"):
                    ctype = ln.split(":", 1)[1].strip()
            if code in (429, 503, 504) or (code == 0 and attempt == 0):
                err = f"http {code} (retryable)"
                time.sleep(60 if "web.archive.org" in target else 10)
                continue
            err = None if code else (err or "no http status")
        host_last[host_of(target)] = time.time()
        return code, body, ctype, err
    host_last[host_of(target)] = time.time()
    return 0, b"", "", err or "fetch failed"

def main():
    items = []
    for line in open(INV):
        line = line.strip()
        if line:
            items.append(json.loads(line))
    new = [it for it in items if it.get("status") == "NEW"]
    have = [it for it in items if it.get("status") != "NEW"]

    def prio(it):
        u = it["url"]
        if "urlquery.net/report" in u:
            return 0
        if "web.archive.org" in u:
            return 1
        return 2
    new.sort(key=lambda it: (prio(it), it.get("finding_id", 0)))

    print(f"NEW={len(new)} HAVE(skipped)={len(have)}", flush=True)
    host_last = {}
    ok, failed = 0, 0
    total_bytes = 0
    with open(MANIFEST, "w") as mf:
        for i, it in enumerate(new, 1):
            url = it["url"]
            fid = it.get("finding_id")
            code, body, ctype, err = fetch(url, host_last)
            sha = hashlib.sha256(body).hexdigest() if body else ""
            if code == 200 and body:
                fname = f"f{fid}_{i:03d}.{ext_for(ctype, url)}"
                with open(os.path.join(OUTDIR, fname), "wb") as fh:
                    fh.write(body)
                ok += 1
                total_bytes += len(body)
            else:
                fname = ""
                failed += 1
                if not err:
                    err = f"http {code}"
            rec = {
                "url": url, "finding_id": fid, "filename": fname,
                "retrieved_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "method": "curl", "http_code": code, "sha256": sha,
                "size_bytes": len(body),
            }
            if err:
                rec["error"] = err[:300]
            mf.write(json.dumps(rec) + "\n")
            if i % 15 == 0 or i == len(new):
                print(f"  {i}/{len(new)} ok={ok} failed={failed}", flush=True)
    print(f"DONE ok={ok} failed={failed} bytes={total_bytes}")

if __name__ == "__main__":
    main()
