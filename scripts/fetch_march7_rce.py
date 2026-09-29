#!/usr/bin/env python3
"""LANE D — March-7 code-execution modality gems (read-only).

Source of truth for gem names: colonist-one's post
data/2025-02-04-thecolony-ai/posts/dfac3a74-4685-43d8-9bd6-c76409f87ade.json
(2026-09-05). The task-brief names (projecttools624286 / atlasqadfe9fb1629 /
tfdriftbqgzb8h) are the *owner accounts*; the actual gem names are:

  account projecttools624286 -> sampledocpayload624286 (11 versions, all
      2026-05-26 19:05->21:51Z, ~1,803 dls) + harmlessdoctest624286
      (paired benign twin)
  account atlasqadfe9fb1629  -> atlas-qa-snapshot-696b16c7 (2026-05-28, 300 dls)
  account tfdriftbqgzb8h     -> tf_drift_handoff_bundle_20260307t015800z
      (2026-03-07 02:58Z, 223 dls)

Read-only HTTPS GETs via curl (~1 req/3s). Diffend gem pages 302 -> /gems for
a name mean the gem is ABSENT from Diffend (known-good May-12 gems return
200). NEVER downloads or executes gems; Diffend-rendered diffs read as
static text only. Resume-friendly: state.json + per-file checkpointing.
"""
import hashlib
import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(BASE, "data", "2026-02-01-march7-rce-modality")
RAW = os.path.join(DIR, "raw")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0 Safari/537.36")
DIFFEND = "https://my.diffend.io"
COMPACT = "https://index.rubygems.org/info/{}"

ACCOUNTS = {
    "projecttools624286": {
        "gems": ["sampledocpayload624286", "harmlessdoctest624286"],
        "note": "payload gem + paired benign twin (same 624286 suffix)",
    },
    "atlasqadfe9fb1629": {
        "gems": ["atlas-qa-snapshot-696b16c7"],
        "note": "2026-05-28, 300 dls",
    },
    "tfdriftbqgzb8h": {
        "gems": ["tf_drift_handoff_bundle_20260307t015800z"],
        "note": "2026-03-07 02:58Z, 223 dls; earliest candidate artifact",
    },
}
ALL = [(acct, g) for acct, d in ACCOUNTS.items() for g in d["gems"]]
PACE = 3.0


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


def curl_probe(url):
    """Return (http_code, redirect_url, body_bytes). No redirect following."""
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


def save(name, data):
    path = os.path.join(RAW, name)
    with open(path, "wb") as f:
        f.write(data)
    sha = hashlib.sha256(data).hexdigest()
    log(f"saved {path} {len(data)}B sha256={sha}")
    return sha, len(data)


def parse_versions(page_html, name):
    """Proven pattern from harvest_diffend.py:
    <a href='/gems/<name>/<v>'>label</a>... <Month D, YYYY HH:MM>"""
    vers, seen = [], set()
    pat = (r"<a href='/gems/%s/([\d.]+(?:/[\d.]+)?)'>(.*?)</a>"
           r".*?([A-Z][a-z]+ \d+, \d+ [\d:]+)") % re.escape(name)
    for m in re.finditer(pat, page_html, re.S):
        for v in m.group(1).split("/"):
            if v not in seen:
                seen.add(v)
                vers.append((v, m.group(3).strip()))
    def vkey(v):
        try:
            return tuple(int(x) for x in v.split("."))
        except ValueError:
            return (0,)
    vers.sort(key=lambda vt: vkey(vt[0]))
    return vers


def main():
    os.makedirs(RAW, exist_ok=True)
    st = state_load()
    done = set(st["done"])
    manifest = {}
    results = {"accounts": ACCOUNTS, "gems": {}}

    for acct, name in ALL:
        pkg = {"account": acct, "gem": name,
               "diffend": {}, "compact": {}}
        # 1. Diffend version-list page
        key = f"{name}/diffend-page"
        vpath = os.path.join(RAW, f"{name}.diffend.html")
        if key not in done:
            code, redir, body = curl_probe(f"{DIFFEND}/gems/{name}")
            pkg["diffend"]["page_status"] = code
            pkg["diffend"]["page_redirect"] = redir
            if code == "200" and body:
                sha, size = save(f"{name}.diffend.html", body)
                manifest[vpath] = {"sha256": sha, "size": size,
                                   "url": f"{DIFFEND}/gems/{name}",
                                   "fetched_at": now()}
                pkg["diffend"]["present"] = True
            elif code == "302" and redir == f"{DIFFEND}/gems":
                pkg["diffend"]["present"] = False
                pkg["diffend"]["note"] = ("302 -> /gems: gem absent from "
                                         "Diffend (known-good gems 200)")
                log(f"{name}: ABSENT from Diffend (302 -> /gems)")
            else:
                pkg["diffend"]["note"] = f"unexpected: {code} {redir}"
                log(f"{name}: diffend unexpected {code} {redir}")
            done.add(key)
            state_save({"done": sorted(done)})
            time.sleep(PACE)
        if os.path.exists(vpath):
            page = open(vpath, encoding="utf-8", errors="replace").read()
            vers = parse_versions(page, name)
            pkg["diffend"]["versions"] = [v for v, _ in vers]
            pkg["diffend"]["version_diff_ts"] = {v: ts for v, ts in vers}
        else:
            pkg["diffend"]["versions"] = []

        # 2. per-version diff pages
        for v in pkg["diffend"]["versions"]:
            dkey = f"{name}/{v}/diff"
            dpath = os.path.join(RAW, f"{name}.{v}.diff.html")
            if dkey not in done:
                code, redir, body = curl_probe(
                    f"{DIFFEND}/gems/{name}/{v}")
                if code == "200" and body:
                    sha, size = save(f"{name}.{v}.diff.html", body)
                    manifest[dpath] = {"sha256": sha, "size": size,
                                       "url": f"{DIFFEND}/gems/{name}/{v}",
                                       "fetched_at": now()}
                else:
                    log(f"{name} {v}: diff fetch {code} {redir}")
                done.add(dkey)
                state_save({"done": sorted(done)})
                time.sleep(PACE)

        # 3. compact-index oracle
        ckey = f"{name}/compact"
        cpath = os.path.join(RAW, f"{name}.compact-index.txt")
        if ckey not in done:
            code, redir, body = curl_probe(COMPACT.format(name))
            pkg["compact"]["status"] = code
            pkg["compact"]["redirect"] = redir
            sha, size = save(f"{name}.compact-index.txt", body)
            manifest[cpath] = {"sha256": sha, "size": size,
                               "status": code,
                               "url": COMPACT.format(name),
                               "fetched_at": now()}
            log(f"{name}: compact-index {code} ({size}B)")
            done.add(ckey)
            state_save({"done": sorted(done)})
            time.sleep(PACE)

        results["gems"][name] = pkg

    with open(os.path.join(DIR, "results.json"), "w") as f:
        json.dump(results, f, indent=1)
    with open(os.path.join(DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    log("DONE results+manifest")


if __name__ == "__main__":
    main()
