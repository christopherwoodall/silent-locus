#!/usr/bin/env python3
"""Download RubyGems tarballs (read-only public API), verify SHA-256, log everything.

SAFETY: download only. Nothing here installs, unpacks-to-run, or executes
anything. Static extraction is handled separately by mine_gems.py.

Usage:
  python3 fetch_gems.py --names tryf3zz wandsworthprobe1778551714
  python3 fetch_gems.py --names foo==1.2.3            # pinned version
  python3 fetch_gems.py --pin-file pins.txt           # one name or name==version per line
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw", "gems")
LOG = os.path.join(BASE, "data", "gem-ioc-log.jsonl")
MAX_GEMS = 500
UA = "rubygems-goimport-research/1.0 (read-only metadata fetch; no install)"


def api_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def resolve_version(name, pin=None):
    meta = api_json("https://rubygems.org/api/v1/gems/%s.json" % name)
    if pin:
        return pin, meta
    return meta["version"], meta


def version_meta(name, version):
    try:
        vers = api_json("https://rubygems.org/api/v1/versions/%s.json" % name)
    except urllib.error.HTTPError:
        return {}
    for v in vers:
        if v.get("number") == version:
            return v
    return {}


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    h = hashlib.sha256()
    size = 0
    with urllib.request.urlopen(req, timeout=180) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            f.write(chunk)
            h.update(chunk)
            size += len(chunk)
    return size, h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--names", nargs="*", default=[])
    ap.add_argument("--pin-file", default=None)
    ap.add_argument("--i-reviewed-manifest", action="store_true",
                    help="required when downloading >500 gems in one run")
    args = ap.parse_args()

    pins = []
    for n in args.names:
        if "==" in n:
            name, ver = n.split("==", 1)
            pins.append((name.strip(), ver.strip()))
        else:
            pins.append((n.strip(), None))
    if args.pin_file:
        with open(args.pin_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "==" in line:
                    name, ver = line.split("==", 1)
                    pins.append((name.strip(), ver.strip()))
                else:
                    pins.append((line, None))

    if not pins:
        sys.exit("no gems requested")
    if len(pins) > MAX_GEMS and not args.i_reviewed_manifest:
        sys.exit("REFUSAL: %d gems exceeds the %d-per-run cap. Review the manifest "
                 "and re-run with --i-reviewed-manifest." % (len(pins), MAX_GEMS))

    os.makedirs(RAW, exist_ok=True)
    for name, pin in pins:
        rec = {"record_kind": "download", "gem": name,
               "retrieved_at": datetime.now(timezone.utc).isoformat()}
        try:
            version, meta = resolve_version(name, pin)
        except urllib.error.HTTPError as e:
            rec["error"] = "version resolution failed: %s" % e
            version = pin
        rec["version"] = version
        if version is None:
            rec["error"] = rec.get("error", "no version available")
        else:
            vmeta = version_meta(name, version)
            rec["published_at"] = vmeta.get("created_at")
            rec["authors"] = meta.get("authors")
            rec["expected_sha256"] = vmeta.get("sha")
            fname = "%s-%s.gem" % (name, version)
            dest = os.path.join(RAW, fname)
            rec["download_url"] = "https://rubygems.org/downloads/%s" % fname
            try:
                if os.path.exists(dest):
                    data = open(dest, "rb").read()
                    rec["sha256"] = hashlib.sha256(data).hexdigest()
                    rec["size_bytes"] = len(data)
                    rec["note"] = "already present on disk; re-verified hash"
                else:
                    size, sha = download(rec["download_url"], dest)
                    rec["sha256"] = sha
                    rec["size_bytes"] = size
                if rec.get("expected_sha256") and rec["sha256"] != rec["expected_sha256"]:
                    rec["sha_mismatch"] = True
            except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
                rec["error"] = "download failed: %s" % e
        with open(LOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(json.dumps({k: rec.get(k) for k in
                          ("gem", "version", "sha256", "size_bytes",
                           "sha_mismatch", "error", "note")}))


if __name__ == "__main__":
    main()
