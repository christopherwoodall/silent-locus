#!/usr/bin/env python3
"""Harvest gem contents from my.diffend.io (Mend Supply Chain Defender).

WHY THIS EXISTS: the May 11-12 2026 probe-gem campaign was yanked from
rubygems.org (all names 404 on the API + compact index), so
fetch_gems.py's rubygems.org/downloads approach cannot retrieve them.
Diffend retains full version diffs of yanked gems, server-rendered as HTML.
This script reconstructs installable-layout .gem tarballs from those diffs.

SAFETY: read-only HTTPS GETs at browsing pace (~1s between requests).
Nothing is installed, unpacked-to-run, or executed. Static extraction is
handled separately by mine_gems.py. Reconstructed .gems are byte-layout
valid tars but NOT byte-identical to the originals (gzip members are
re-compressed); the original checksums.yaml content is preserved inside
the provenance log for reference.

Method per gem version:
  1. GET https://my.diffend.io/gems/<name>                 (version list)
  2. GET https://my.diffend.io/gems/<name>/<version>       (diff vs empty)
     - for versions > first: GET /gems/<name>/<v1>/<v2> and apply the
       unified diff onto the previous version's file tree.
  3. Parse diff2html blocks: <a class="d2h-file-name"> + per-line
     <span class="d2h-code-line-prefix">(+/-/space) + content spans.
  4. Rebuild: metadata -> metadata.gz, data/* -> data.tar.gz,
     checksums.yaml kept as harvested.
  5. Write data/raw/gems/<name>-<version>.gem + provenance log.

Usage:
  python3 harvest_diffend.py --names tryf3zz==0.0.1 wandsworthprobe1778551714
  python3 harvest_diffend.py --pin-file pins.txt   # one name or name==version per line
  python3 harvest_diffend.py --pilot                # 5-gem proof-of-method run
"""
import argparse
import gzip
import hashlib
import html
import io
import json
import os
import re
import sys
import tarfile
import time
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw", "gems")
LOG = os.path.join(BASE, "data", "gem-ioc-log.jsonl")
DIFFEND = "https://my.diffend.io"
UA = "rubygems-goimport-research/1.0 (read-only diff harvest; no install)"
PACE = 1.0
MAX_GEMS = 600

PILOT = [
    ("tryf3zz", "0.0.1"),
    ("oaisurveytestzz", "0.0.1"),
    ("lambprobe4344", "0.0.1"),
    ("wandsworthprobe1778551714", "0.0.2"),
    ("zzjinavcsgit", "0.0.1"),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read().decode("utf-8", "ignore")
    time.sleep(PACE)
    return data


def gem_versions(name):
    """Return [(version, diff_ts)] from the Diffend gem page."""
    h = get("%s/gems/%s" % (DIFFEND, name))
    vers = []
    seen = set()
    pat = r"<a href='/gems/%s/([\d.]+(?:/[\d.]+)?)'>(.*?)</a>.*?([A-Z][a-z]+ \d+, \d+ [\d:]+)"
    for m in re.finditer(pat % re.escape(name), h, re.S):
        vpath = m.group(1)
        label = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2))).strip()
        parts = vpath.split("/")
        for v in parts:
            if v not in seen:
                seen.add(v)
                vers.append((v, m.group(3).strip()))
    # order oldest-first: single versions sort naturally; pairs imply order
    def vkey(v):
        return tuple(int(x) for x in v.split("."))
    vers.sort(key=lambda vt: vkey(vt[0]))
    return vers


def parse_diff_files(h):
    """Parse diff2html page -> {filename: [(prefix, text), ...]} in file order."""
    files = {}
    # split into file blocks at each file-name anchor
    blocks = re.split(r'<a href="[^"]*" class="d2h-file-name">', h)
    for blk in blocks[1:]:
        m = re.match(r"([^<]+)</a>", blk)
        if not m:
            continue
        fname = html.unescape(m.group(1)).strip()
        rows = re.findall(
            r'<span class="d2h-code-line-prefix">([+\- ])</span>\s*'
            r'<span class="d2h-code-line-ctn">(.*?)</span>',
            blk, re.S)
        lines = []
        for prefix, ctn in rows:
            text = html.unescape(re.sub(r"<[^>]+>", "", ctn))
            lines.append((prefix, text))
        files[fname] = lines
    return files


def apply_diff(tree, files):
    """Apply parsed diff files onto {filename: [lines]} tree. Returns new tree."""
    new = {k: list(v) for k, v in tree.items()}
    for fname, rows in files.items():
        if fname not in new:
            # new file: keep '+' lines (and ' ' if any)
            new[fname] = [t for p, t in rows if p in ("+", " ")]
            continue
        old = new[fname]
        out = []
        oi = 0
        for prefix, text in rows:
            if prefix == " ":
                out.append(old[oi] if oi < len(old) else text)
                oi += 1
            elif prefix == "-":
                oi += 1  # drop
            elif prefix == "+":
                out.append(text)
        new[fname] = out
    return new


def harvest_version(name, version, prev_tree=None, prev_version=None):
    """Return (tree, diff_url). tree maps filename -> [lines]."""
    if prev_tree is None:
        url = "%s/gems/%s/%s" % (DIFFEND, name, version)
        files = parse_diff_files(get(url))
        tree = {}
        for fname, rows in files.items():
            tree[fname] = [t for p, t in rows if p in ("+", " ")]
        return tree, url
    url = "%s/gems/%s/%s/%s" % (DIFFEND, name, prev_version, version)
    files = parse_diff_files(get(url))
    return apply_diff(prev_tree, files), url


def build_gem(tree):
    """Build .gem tar bytes from {filename: [lines]} tree."""
    metadata = "\n".join(tree.get("metadata", []))
    if metadata and not metadata.endswith("\n"):
        metadata += "\n"
    checksums = "\n".join(tree.get("checksums.yaml", []))
    if checksums and not checksums.endswith("\n"):
        checksums += "\n"
    data_files = {k[5:]: v for k, v in tree.items() if k.startswith("data/")}

    meta_gz = gzip.compress(metadata.encode("utf-8"), mtime=0)
    dt = io.BytesIO()
    with tarfile.open(fileobj=dt, mode="w") as tf:
        for fname, lines in sorted(data_files.items()):
            content = ("\n".join(lines) + "\n").encode("utf-8")
            ti = tarfile.TarInfo(fname)
            ti.size = len(content)
            ti.mtime = 0
            tf.addfile(ti, io.BytesIO(content))
    data_gz = gzip.compress(dt.getvalue(), mtime=0)

    gem = io.BytesIO()
    with tarfile.open(fileobj=gem, mode="w") as tf:
        for fname, content in [("metadata.gz", meta_gz),
                               ("data.tar.gz", data_gz),
                               ("checksums.yaml", checksums.encode("utf-8"))]:
            ti = tarfile.TarInfo(fname)
            ti.size = len(content)
            ti.mtime = 0
            tf.addfile(ti, io.BytesIO(content))
    return gem.getvalue()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--names", nargs="*", default=[])
    ap.add_argument("--pin-file", default=None)
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--i-reviewed-manifest", action="store_true")
    args = ap.parse_args()

    pins = []
    if args.pilot:
        pins = list(PILOT)
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
        sys.exit("REFUSAL: %d gems exceeds the %d-per-run cap." % (len(pins), MAX_GEMS))

    os.makedirs(RAW, exist_ok=True)
    for name, pin in pins:
        rec = {"record_kind": "diffend_harvest", "gem": name,
               "retrieved_via": "my.diffend.io (yanked from rubygems.org)"}
        try:
            vers = gem_versions(name)
            rec["diffend_versions"] = [{"version": v, "diff_ts": ts} for v, ts in vers]
            if pin:
                if pin not in [v for v, _ in vers]:
                    rec["error"] = "pinned version %s not on Diffend page" % pin
                    raise ValueError("version missing")
                targets = [pin]
            else:
                targets = [v for v, _ in vers] or [None]
            tree = None
            prev = None
            for v in [x for x in [vv for vv, _ in vers] if x in targets or True]:
                # harvest in version order so multi-version diffs apply cleanly
                if v not in targets:
                    tree, _ = harvest_version(name, v, tree, prev)
                    prev = v
                    continue
                tree, durl = harvest_version(name, v, tree, prev)
                prev = v
                gem_bytes = build_gem(tree)
                fname = "%s-%s.gem" % (name, v)
                dest = os.path.join(RAW, fname)
                with open(dest, "wb") as f:
                    f.write(gem_bytes)
                rec["version"] = v
                rec["diff_url"] = durl
                rec["sha256"] = hashlib.sha256(gem_bytes).hexdigest()
                rec["size_bytes"] = len(gem_bytes)
                # IOC-bearing metadata fields (mine_gems.py scans data files
                # only, so capture summary/description here)
                meta_text = "\n".join(tree.get("metadata", []))
                for field in ("summary", "description", "authors",
                              "homepage", "licenses"):
                    m = re.search(r"^%s:\s*(.*?)(?=^\w|\Z)" % field,
                                  meta_text, re.M | re.S)
                    if m:
                        rec["meta_" + field] = m.group(1).strip()[:500]
                rec["note"] = ("reconstructed from Diffend rendered diff; "
                               "NOT byte-identical to the original .gem")
        except Exception as e:
            rec["error"] = "harvest failed: %s" % str(e)[:120]
        with open(LOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(json.dumps({k: rec.get(k) for k in
                          ("gem", "version", "sha256", "size_bytes", "error")}))
        time.sleep(PACE)


if __name__ == "__main__":
    main()
