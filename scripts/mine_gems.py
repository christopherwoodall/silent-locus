#!/usr/bin/env python3
"""Statically extract .gem tarballs and mine phase-two IOC fingerprints.

SAFETY HARD RULES (enforced by design, not just policy):
  - NEVER runs `gem install`, never executes any extracted file.
  - Extraction is tar-member read + text grep ONLY (stdlib tarfile, no shell).
  - Tar members are path-traversal filtered (no absolute paths, no `..`).
  - Binary files (null byte in first 8 KiB) are content-skipped; their
    presence + SHA-256 is logged but they are never decoded or run.
  - Native-extension artifacts (.so/.bundle/.dylib/.dll/.o/.a) are logged
    with hashes and never touched beyond hashing.
  - Per-file content scan is capped at 2 MiB (truncation noted).

Usage:
  python3 mine_gems.py                       # process every .gem in data/raw/gems/
  python3 mine_gems.py --names tryf3zz       # only these gems (any version on disk)
"""
import argparse
import gzip
import hashlib
import io
import json
import os
import re
import sys
import tarfile
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw", "gems")
PROC = os.path.join(BASE, "data", "processed", "gems")
LOG = os.path.join(BASE, "data", "gem-ioc-log.jsonl")
HITS = os.path.join(BASE, "data", "gem-ioc-hits.jsonl")
NODES = os.path.join(BASE, "data", "gem-graph-nodes.jsonl")
EDGES = os.path.join(BASE, "data", "gem-graph-edges.jsonl")

SCAN_CAP = 2 * 1024 * 1024  # per-file content scan cap
BIN_PROBE = 8192
NATIVE_EXTS = {".so", ".bundle", ".dylib", ".dll", ".o", ".a", ".dylib"}

# (fingerprint, compiled regex, confidence)
FINGERPRINTS = [
    ("epoch-nonce", re.compile(r"\b1[78]\d{8}\b"), "high"),
    ("zz-token", re.compile(r"\bzz[A-Za-z0-9_]{2,}\b"), "high"),
    ("ntfy-topic", re.compile(r"ntfy\.(?:sh|envs\.net)/[^\s\"'<>\\]{1,120}"), "high"),
    ("webhook-inbox", re.compile(r"webhook\.site/[^\s\"'<>\\]{1,120}"), "high"),
    ("filebin-url", re.compile(r"filebin\.net/[^\s\"'<>\\]{1,120}"), "high"),
    ("paste-url", re.compile(r"paste\.rs/[^\s\"'<>\\]{1,120}"), "medium"),
    ("shortener-url", re.compile(
        r"(?:is\.gd|da\.gd|cutt\.ly|tinyurl\.com|rmn\.re|vanderbi\.lt)/[^\s\"'<>\\]{1,120}"),
     "high"),
    ("httpbun-url", re.compile(r"httpbun\.com[^\s\"'<>\\]{0,120}"), "medium"),
    ("tableau-marker", re.compile(r"tableau-2\.9\.2\.min\.js|tableau\.Viz"), "high"),
    ("controller-stem", re.compile(
        r"\b(?:OTS92|G236|BE90|LIBR11|MARB051|Future9180|SC4)\w*", re.IGNORECASE), "high"),
    ("series-64H", re.compile(
        r"\b(?:GSTX64|PHASEONE64H|LONG64H2718|EARLY64|3FR64B?|[A-Z0-9]{1,20}64H\d*)\b"),
     "medium"),
    ("probe-name", re.compile(r"\b[a-z0-9_]*(?:probe)[a-z0-9_]*\b", re.IGNORECASE), "low"),
]

# Metadata-field fingerprints: the May 2026 campaign's payload lives in the
# gemspec summary/description (go-import meta-tag injection), not data files.
METADATA_FINGERPRINTS = [
    ("go-import", re.compile(
        r'<meta\s+name=["\']?go-import["\']?\s+content=["\']?([^"\'<>]+)',
        re.IGNORECASE), "high"),
    ("r-jina-proxy", re.compile(
        r"https?://r\.jina\.ai/[^\s\"'<>\\]{1,160}"), "high"),
    ("council-domain", re.compile(
        r"(?:democracy\.wandsworth\.gov\.uk|moderngov\.lambeth\.gov\.uk|"
        r"moderngov\.southwark\.gov\.uk|digitizationguidelines\.gov)"
        r"[^\s\"'<>\\]{0,160}"), "high"),
]
GO_IMPORT_VCS = {"hg", "fossil", "git", "mod", "bzr", "svn"}


def sha8(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:8]


def safe_members(tar):
    """Yield (member, safe_relpath) with traversal filtering."""
    for m in tar.getmembers():
        p = os.path.normpath(m.name)
        if not p or p == "." or p.startswith("/") or p.startswith(".."):
            continue
        if any(part == ".." for part in p.split(os.sep)):
            continue
        yield m, p


def stream_copy(src, dest_path, cap=None):
    h = hashlib.sha256()
    size = 0
    truncated = False
    with open(dest_path, "wb") as f:
        while True:
            chunk = src.read(65536)
            if not chunk:
                break
            if cap is not None and size + len(chunk) > cap:
                chunk = chunk[:cap - size]
                truncated = True
            f.write(chunk)
            h.update(chunk)
            size += len(chunk)
            if truncated:
                break
    return size, h.hexdigest(), truncated


def extract_gem(gem_path, dest_dir):
    """Unpack outer .gem tar -> data.tar.gz -> file tree. Returns file list."""
    files = []
    os.makedirs(dest_dir, exist_ok=True)
    with tarfile.open(gem_path, "r") as outer:
        data_member = None
        for m, p in safe_members(outer):
            if p == "data.tar.gz" and m.isfile():
                data_member = m
                break
        if data_member is None:
            return files, "no data.tar.gz member"
        buf = io.BytesIO(outer.extractfile(data_member).read())
    with tarfile.open(fileobj=buf, mode="r:gz") as inner:
        for m, p in safe_members(inner):
            target = os.path.join(dest_dir, p)
            if not os.path.abspath(target).startswith(os.path.abspath(dest_dir) + os.sep):
                continue
            if m.isdir():
                os.makedirs(target, exist_ok=True)
            elif m.isfile():
                os.makedirs(os.path.dirname(target) or dest_dir, exist_ok=True)
                src = inner.extractfile(m)
                size, sha, _ = stream_copy(src, target)
                files.append({"path": p, "size": size, "sha256": sha})
    return files, None


def is_binary(path):
    with open(path, "rb") as f:
        probe = f.read(BIN_PROBE)
    return b"\x00" in probe


def scan_file(relpath, abs_path):
    """Return list of (fingerprint, value, line_no, confidence)."""
    hits = []
    with open(abs_path, "rb") as f:
        data = f.read(SCAN_CAP + 1)
    truncated = len(data) > SCAN_CAP
    text = data[:SCAN_CAP].decode("utf-8", errors="ignore")
    for lineno, line in enumerate(text.splitlines(), 1):
        for fp, rx, conf in FINGERPRINTS:
            for m in rx.finditer(line):
                val = m.group(0)
                if len(val) > 200:
                    val = val[:200] + "…"
                hits.append((fp, val, lineno, conf, truncated))
    return hits


def read_outer_metadata(gem_path):
    """Return decompressed metadata.gz text from the outer .gem tar ('' on failure)."""
    try:
        with tarfile.open(gem_path, "r") as outer:
            for m, p in safe_members(outer):
                if p in ("metadata.gz", "metadata") and m.isfile():
                    f = outer.extractfile(m)
                    raw = f.read()
                    if p.endswith(".gz"):
                        raw = gzip.decompress(raw)
                    return raw.decode("utf-8", errors="ignore")
    except Exception:
        pass
    return ""


def scan_metadata(name, meta_text):
    """Mine gemspec metadata text. Returns [(fp, value, lineno, confidence, note)]."""
    hits = []
    # epoch self-timestamp in the gem name itself (e.g. wandsworthprobe1778551714)
    for m in re.finditer(r"\b1[78]\d{8}\b", name):
        hits.append(("epoch-nonce", m.group(0), 0, "high",
                     "epoch suffix in gem name (self-timestamping)"))
    # go-import: match on the WHOLE text — the tag spans YAML-folded lines
    # (content="prefix.yaml\n  <vcs> <repo-url>"), so per-line matching truncates it.
    go_rx = METADATA_FINGERPRINTS[0][1]
    for m in go_rx.finditer(meta_text):
        lineno = meta_text.count("\n", 0, m.start()) + 1
        content = re.sub(r"\s+", " ", m.group(1)).strip()
        if len(content) > 300:
            content = content[:300] + "…"
        hits.append(("go-import", content, lineno, "high", "go-import meta tag"))
        parts = content.split()
        if len(parts) >= 3:
            vcs, repo = parts[1], " ".join(parts[2:])
            if vcs in GO_IMPORT_VCS:
                hits.append(("go-import-vcs", vcs, lineno, "high",
                             "vcs value in go-import tag"))
            if len(repo) > 400:
                repo = repo[:400] + "…"
            hits.append(("go-import-repo", repo, lineno, "high",
                         "repo URL in go-import tag"))
    for lineno, line in enumerate(meta_text.splitlines(), 1):
        for fp, rx, conf in METADATA_FINGERPRINTS[1:]:
            for m in rx.finditer(line):
                val = m.group(0)
                if len(val) > 300:
                    val = val[:300] + "…"
                hits.append((fp, val, lineno, conf, "gemspec metadata"))
    return hits


def load_ids(path):
    ids = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        ids.add(json.loads(line)["id"])
                    except (KeyError, ValueError):
                        pass
    return ids


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--names", nargs="*", default=None,
                    help="only process these gem names (all versions on disk)")
    args = ap.parse_args()

    gem_files = sorted(f for f in os.listdir(RAW) if f.endswith(".gem"))
    if args.names:
        gem_files = [f for f in gem_files
                     if any(f == "%s-" % n or f.startswith(n + "-") for n in args.names)]
    if not gem_files:
        sys.exit("no .gem files to process")

    node_ids = load_ids(NODES)
    edge_keys = set()
    if os.path.exists(EDGES):
        with open(EDGES) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        e = json.loads(line)
                        edge_keys.add((e["source"], e["target"], e["relation"]))
                    except ValueError:
                        pass

    os.makedirs(PROC, exist_ok=True)
    for gem_file in gem_files:
        base = gem_file[:-4]  # strip .gem
        name, _, version = base.rpartition("-")
        # name itself may contain dashes; version is last dotted numeric-ish token
        gem_path = os.path.join(RAW, gem_file)
        dest = os.path.join(PROC, base)
        gem_page = "https://rubygems.org/gems/%s/versions/%s" % (name, version)

        files, err = extract_gem(gem_path, dest)
        ext_rec = {"record_kind": "extraction", "gem": name, "version": version,
                   "extracted_to": dest, "file_count": len(files),
                   "extracted_at": datetime.now(timezone.utc).isoformat()}
        if err:
            ext_rec["error"] = err
        natives = [f for f in files
                   if os.path.splitext(f["path"])[1].lower() in NATIVE_EXTS]
        if natives:
            ext_rec["native_artifacts"] = natives  # presence + hashes only; never run
        ext_rec["files"] = files

        nodes_out, edges_out = [], []

        def add_node(n):
            if n["id"] not in node_ids:
                node_ids.add(n["id"])
                nodes_out.append(n)

        def add_edge(s, t, rel, notes):
            key = (s, t, rel)
            if key not in edge_keys:
                edge_keys.add(key)
                edges_out.append({"source": s, "target": t, "relation": rel,
                                  "evidence_url": evidence_url, "notes": notes})

        gem_id = "gem-%s-%s" % (name, version)
        dl, dh = {}, {}
        if os.path.exists(LOG):
            with open(LOG) as f:
                for line in f:
                    try:
                        r = json.loads(line)
                    except ValueError:
                        continue
                    if r.get("gem") == name and r.get("version") == version:
                        if r.get("record_kind") == "download":
                            dl = r
                        elif r.get("record_kind") == "diffend_harvest":
                            dh = r
        pub = dl.get("published_at")
        authors = dl.get("authors") or dh.get("meta_authors")
        evidence_url = dh.get("diff_url") or gem_page
        add_node({"id": gem_id, "label": "%s %s" % (name, version), "type": "gem",
                  "subtype": "diffend-harvest" if dh else "rubygem",
                  "description": "RubyGems package %s version %s (authors: %s)" %
                                 (name, version, authors),
                  "first_seen": pub, "last_seen": pub,
                  "source_url": evidence_url, "confidence": "confirmed"})

        ioc_seen = set()

        # --- metadata fingerprint pass: campaign payload lives in summary/description ---
        meta_text = read_outer_metadata(gem_path)
        if not meta_text and dh:
            meta_text = "\n".join(str(dh.get(k, "")) for k in
                                  ("meta_summary", "meta_description"))
        for fp, val, lineno, conf, note in scan_metadata(name, meta_text):
            with open(HITS, "a") as hf:
                hf.write(json.dumps({
                    "gem": name, "version": version, "file": "metadata (gemspec)",
                    "fingerprint": fp, "matched_string": val,
                    "line_no": lineno, "confidence": conf,
                    "scan_truncated": False, "note": note}) + "\n")
            iid = "ioc-%s-%s" % (fp, sha8(val))
            if iid not in ioc_seen:
                ioc_seen.add(iid)
                add_node({"id": iid, "label": val[:120], "type": "indicator",
                          "subtype": fp,
                          "description": "metadata fingerprint %s in gemspec of %s-%s" %
                                         (fp, name, version),
                          "first_seen": pub, "last_seen": pub,
                          "source_url": evidence_url, "confidence": conf})
            add_edge(gem_id, iid, "exhibits",
                     "%s in gemspec metadata%s (%s)" %
                     (fp, " line %d" % lineno if lineno else "", note))
        for finfo in files:
            rel = finfo["path"]
            abs_p = os.path.join(dest, rel)
            if not os.path.isfile(abs_p):
                continue
            fid = "file-%s" % sha8("%s/%s/%s" % (name, version, rel))
            ext = os.path.splitext(rel)[1].lower() or "noext"
            binary = is_binary(abs_p)
            add_node({"id": fid, "label": rel, "type": "file",
                      "subtype": ("binary:" + ext) if binary else ("text:" + ext),
                      "description": "file %s inside gem %s-%s (sha256 %s%s)" %
                                     (rel, name, version, finfo["sha256"][:16],
                                      "; content not scanned (binary)" if binary else ""),
                      "first_seen": pub, "last_seen": pub,
                      "source_url": gem_page, "confidence": "confirmed"})
            add_edge(gem_id, fid, "contains", "static extraction of published tarball")
            if binary:
                continue
            for fp, val, lineno, conf, trunc in scan_file(rel, abs_p):
                with open(HITS, "a") as hf:
                    hf.write(json.dumps({
                        "gem": name, "version": version, "file": rel,
                        "fingerprint": fp, "matched_string": val,
                        "line_no": lineno, "confidence": conf,
                        "scan_truncated": trunc}) + "\n")
                iid = "ioc-%s-%s" % (fp, sha8(val))
                if iid not in ioc_seen:
                    ioc_seen.add(iid)
                    add_node({"id": iid, "label": val[:120], "type": "indicator",
                              "subtype": fp,
                              "description": "phase-two fingerprint %s observed in gem file content" % fp,
                              "first_seen": pub, "last_seen": pub,
                              "source_url": gem_page, "confidence": conf})
                add_edge(fid, iid, "exhibits",
                         "%s hit in %s line %d%s" % (fp, rel, lineno,
                                                     " (scan truncated at 2MiB)" if trunc else ""))

        with open(NODES, "a") as f:
            for n in nodes_out:
                f.write(json.dumps(n) + "\n")
        with open(EDGES, "a") as f:
            for e in edges_out:
                f.write(json.dumps(e) + "\n")
        ext_rec["ioc_distinct_values"] = len(ioc_seen)
        with open(LOG, "a") as f:
            f.write(json.dumps(ext_rec) + "\n")
        print(json.dumps({"gem": name, "version": version, "files": len(files),
                          "ioc_values": len(ioc_seen),
                          "nodes": len(nodes_out), "edges": len(edges_out),
                          "natives": len(natives), "error": err}))


if __name__ == "__main__":
    main()
