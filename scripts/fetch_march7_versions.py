#!/usr/bin/env python3
"""Fetch per-version Diffend diff pages for the March-7 modality gems.

Version list comes from JFrog's public inventory (data/gemstuffer-jfrog-2026-09-27.csv)
because Diffend's version-list page renders client-side (no server links).
~1 req/3s via curl, resume-friendly via state.json.
"""
import csv
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(BASE, "data", "march7-rce-modality")
RAW = os.path.join(DIR, "raw")
DIFFEND = "https://my.diffend.io"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0 Safari/537.36")


def now():
    return datetime.now(timezone.utc).isoformat()


def log(msg):
    line = f"{now()} {msg}"
    print(line, flush=True)
    with open(os.path.join(DIR, "progress.log"), "a") as f:
        f.write(line + "\n")


def state_load():
    p = os.path.join(DIR, "state.json")
    return json.load(open(p)) if os.path.exists(p) else {"done": []}


def state_save(st):
    with open(os.path.join(DIR, "state.json"), "w") as f:
        json.dump(st, f, indent=1)


def jfrog_versions(name):
    with open(os.path.join(BASE, "data/gemstuffer-jfrog-2026-09-27.csv")) as f:
        for row in csv.reader(f):
            if row and row[0] == name:
                return row[1].split(";"), row[2] if len(row) > 2 else ""
    return [], ""


def curl_fetch(url):
    try:
        r = subprocess.run(
            ["curl", "-sS", "-m", "60", "-A", UA,
             "-o", "-", "-w", "\n__CURLMETA__:%{http_code}:%{redirect_url}",
             "--max-redirs", "0", url],
            capture_output=True, timeout=90)
        out = r.stdout
        meta = b""
        if b"__CURLMETA__:" in out:
            out, meta = out.rsplit(b"__CURLMETA__:", 1)
        code, _, redir = meta.decode(errors="replace").partition(":")
        return code.strip(), redir.strip(), out
    except Exception as e:
        return "ERR", "", str(e).encode()


def main():
    os.makedirs(RAW, exist_ok=True)
    st = state_load()
    done = set(st["done"])
    targets = []
    for name in ["sampledocpayload624286", "harmlessdoctest624286"]:
        vers, xray = jfrog_versions(name)
        log(f"{name}: JFrog versions={vers} xray={xray}")
        for v in vers:
            targets.append((name, v))

    manifest = json.load(open(os.path.join(DIR, "manifest.json"))) \
        if os.path.exists(os.path.join(DIR, "manifest.json")) else {}
    for name, v in targets:
        key = f"{name}/{v}/diff"
        dpath = os.path.join(RAW, f"{name}.{v}.diff.html")
        if key in done and os.path.exists(dpath):
            continue
        code, redir, body = curl_fetch(f"{DIFFEND}/gems/{name}/{v}")
        if code == "200" and body and b"d2h-file-name" in body:
            sha = hashlib.sha256(body).hexdigest()
            with open(dpath, "wb") as f:
                f.write(body)
            manifest[dpath] = {"sha256": sha, "size": len(body),
                               "url": f"{DIFFEND}/gems/{name}/{v}",
                               "fetched_at": now()}
            log(f"saved {dpath} {len(body)}B sha256={sha}")
        else:
            log(f"{name} {v}: {code} {redir} ({len(body)}B)")
        done.add(key)
        state_save({"done": sorted(done)})
        time.sleep(3.0)

    with open(os.path.join(DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    log("version-diff fetch DONE")


if __name__ == "__main__":
    main()
