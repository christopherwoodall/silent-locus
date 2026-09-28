#!/usr/bin/env python3
"""LANE D — March-7 code-execution modality gems (read-only).

Per colonist-one's finding (thecolony.ai incident wiki): a second modality —
registry code-execution probe via 3 RubyGems packages (doc-builder RCE +
egress test), versions starting 2026-03-07, all yanked as of 2026-09-28.

Read-only HTTPS GETs at gentle pace (~1 req/3s), backoff on connection-close,
resume-friendly: per-request log lines appended to progress.log and a
state.json checkpoint. NEVER downloads or executes gem payloads; Diffend
server-rendered diff pages are fetched as HTML text only.

Outputs (data/march7-rce-modality/):
  raw/<name>.versions.html          Diffend version-list page per package
  raw/<name>.<version>.diff.html    Diffend diff page per version (vs empty)
  raw/<name>.compact-index.txt      rubygems compact index /info/<name>
  state.json                        checkpoint of completed fetches
  PROVENANCE.md                     URLs, timestamps, SHA-256
  manifest.json                     per-file SHA-256
  sweep.json                        pattern sweep results
"""
import hashlib
import html as htmlmod
import json
import os
import re
import socket
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(BASE, "data", "march7-rce-modality")
RAW = os.path.join(DIR, "raw")
UA = "swarmtraces-research/1.0 (read-only metadata; no install or execute)"
NAMES = ["projecttools624286", "atlasqadfe9fb1629", "tfdriftbqgzb8h"]
DIFFEND = "https://my.diffend.io"
COMPACT = "https://index.rubygems.org/info/{}"
PACE = 3.0
MAX_RETRIES = 8


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


def fetch(url, retries=MAX_RETRIES):
    backoff = 5.0
    for attempt in range(retries):
        try:
            r = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(r, timeout=90) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 404, b""
            log(f"HTTP {e.code} {url} attempt={attempt}")
        except Exception as e:
            log(f"conn-fail {url} attempt={attempt} err={str(e)[:120]}")
        time.sleep(backoff)
        backoff = min(backoff * 1.8, 120)
    return "FAIL", b""


def save(name, data):
    path = os.path.join(RAW, name)
    with open(path, "wb") as f:
        f.write(data)
    sha = hashlib.sha256(data).hexdigest()
    log(f"saved {path} {len(data)}B sha256={sha}")
    return sha, len(data)


def parse_versions(page_html, name):
    """Extract (version, diff_ts) from the Diffend gem page.
    Proven pattern from harvest_diffend.py (worked for the May-12 corpus):
      <a href='/gems/<name>/<v>'>label</a>... <Month D, YYYY HH:MM>
    """
    vers, seen = [], set()
    pat = r"<a href='/gems/%s/([\d.]+(?:/[\d.]+)?)'>(.*?)</a>.*?([A-Z][a-z]+ \d+, \d+ [\d:]+)" % re.escape(name)
    for m in re.finditer(pat, page_html, re.S):
        vpath = m.group(1)
        for v in vpath.split("/"):
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


def parse_diff_files(page_html):
    """Extract file names from a diff2html-rendered diff page."""
    names = []
    for m in re.finditer(
            r'class="d2h-file-name"[^>]*>(.*?)</a>', page_html, re.S):
        txt = htmlmod.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        if txt and txt not in names:
            names.append(txt)
    return names


def strip_diff_text(page_html):
    """Extract plain +/- diff lines for pattern sweep (no execution)."""
    lines = []
    for m in re.finditer(
            r'<span class="d2h-code-line-prefix">([\+\- ])</span>'
            r'<span class="d2h-code-line-ctn">(.*?)</span>', page_html, re.S):
        prefix = m.group(1)
        content = htmlmod.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        lines.append(prefix + content)
    return "\n".join(lines)


def main():
    os.makedirs(RAW, exist_ok=True)
    st = state_load()
    done = set(st["done"])
    manifest = {}
    results = {}

    for name in NAMES:
        pkg = {"name": name, "diffend_status": None, "compact_status": None,
               "versions": [], "files": {}, "diff_sha256": {}, "notes": []}
        # 1. Diffend version-list page
        key = f"{name}/versions"
        vpath = os.path.join(RAW, f"{name}.versions.html")
        versions = []  # [(version, diff_ts)]
        if key not in done:
            status, data = fetch(f"{DIFFEND}/gems/{name}")
            pkg["diffend_status"] = status
            if status == 200 and data:
                sha, size = save(f"{name}.versions.html", data)
                manifest[vpath] = {"sha256": sha, "size": size,
                                   "url": f"{DIFFEND}/gems/{name}",
                                   "fetched_at": now()}
                done.add(key)
            elif status == 404:
                pkg["notes"].append("diffend 404 (page gone)")
                done.add(key)
            state_save({"done": sorted(done)})
            time.sleep(PACE)
        else:
            pkg["diffend_status"] = 200
        if os.path.exists(vpath):
            page = open(vpath, encoding="utf-8", errors="replace").read()
            versions = parse_versions(page, name)
            pkg["versions"] = [v for v, _ in versions]
            pkg["version_diff_ts"] = {v: ts for v, ts in versions}

        # 2. Per-version diff page (vs empty tree)
        for v in pkg["versions"]:
            dkey = f"{name}/{v}/diff"
            dpath = os.path.join(RAW, f"{name}.{v}.diff.html")
            if dkey not in done:
                status, data = fetch(f"{DIFFEND}/gems/{name}/{v}")
                if status == 200 and data:
                    sha, size = save(f"{name}.{v}.diff.html", data)
                    manifest[dpath] = {"sha256": sha, "size": size,
                                       "url": f"{DIFFEND}/gems/{name}/{v}",
                                       "fetched_at": now()}
                else:
                    pkg["notes"].append(f"diff {v} fetch status={status}")
                done.add(dkey)
                state_save({"done": sorted(done)})
                time.sleep(PACE)
            if os.path.exists(dpath):
                dp = open(dpath, encoding="utf-8", errors="replace").read()
                pkg["files"][v] = parse_diff_files(dp)
                pkg["diff_sha256"][v] = hashlib.sha256(dp.encode()).hexdigest()

        # 3. Compact-index oracle
        ckey = f"{name}/compact"
        cpath = os.path.join(RAW, f"{name}.compact-index.txt")
        if ckey not in done:
            status, data = fetch(COMPACT.format(name))
            pkg["compact_status"] = status
            if status in (200, 404):
                sha, size = save(f"{name}.compact-index.txt", data)
                manifest[cpath] = {"sha256": sha, "size": size,
                                   "status": status,
                                   "url": COMPACT.format(name),
                                   "fetched_at": now()}
            done.add(ckey)
            state_save({"done": sorted(done)})
            time.sleep(PACE)
        else:
            pkg["compact_status"] = "cached"

        results[name] = pkg
        log(f"PACKAGE {name}: diffend={pkg['diffend_status']} "
            f"compact={pkg['compact_status']} versions={pkg['versions']}")

    with open(os.path.join(DIR, "results.json"), "w") as f:
        json.dump(results, f, indent=1)
    with open(os.path.join(DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    log("DONE results+manifest")


if __name__ == "__main__":
    main()
