#!/usr/bin/env python3
"""Collection validator: naming, registration, and records-in-the-right-place
for data/. Companion to validate_schema.py (which checks record shape against
schema/record.schema.json); this one checks the COLLECTION level against
schema/collections.json + schema/collections.md. Stdlib only, disk only (no ES).

Violations (exit 1): unregistered data/ entry, bad collection name, loose
JSONL not in the registry, records whose event.dataset matches neither the
collection name nor its dataset_override, collections with records that no
ingest path can load (registered staged events.jsonl/rollup.jsonl),
via_script/staged overlap, non-event files/dirs at a collection root
(layout: events.jsonl + PROVENANCE.md + SHA256SUMS + raw/ at the root, plus
co-located single-collection build scripts per the 2026-09-29 convention),
top-level `file` pointers that do not resolve to a real on-disk path (see
resolve_file_pointer; the raw/ migration rule).

Warnings (exit unaffected): missing PROVENANCE.md/SHA256SUMS on
canonical/support collections, records with no event.dataset yet (pending
schema backfill).

Usage: python3 scripts/validate_collections.py
"""

import glob
import gzip
import json
import os
import re
import sys
from collections import Counter
from push_to_local_es import discover_staged as loader_discover_staged

REPO = __file__.rsplit("/scripts/", 1)[0]
DATA = os.path.join(REPO, "data")
REGISTRY = os.path.join(REPO, "schema", "collections.json")
MANIFEST = os.path.join(REPO, "scripts", "local_es_manifest.json")
# collection dirs are date-prefixed: YYYY-MM-DD-<slug> (first-event date)
SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*$")
# canonical collection root layout (schema/collections.md)
ROOT_FILES = {"events.jsonl", "rollup.jsonl", "PROVENANCE.md",
              "SHA256SUMS", "SHA256SUMS.txt"}
# single-collection build scripts live at the collection root per the
# 2026-09-29 convention (schema/collections.md); tolerated here
ROOT_BUILD_SCRIPT_RE = re.compile(r"^(es_ingest|build)_.*\.py$")
ROOT_DIRS = {"raw"}
SAMPLE_LINES = 200
MAX_FILES = 4
# event-layer files carrying top-level `file` pointers (pass 3)
EVENT_FILES = ("events.jsonl", "rollup.jsonl")

violations = []
warnings = []


def v(msg):
    violations.append(msg)


def w(msg):
    warnings.append(msg)


def datasets_in_file(path):
    ds, n = Counter(), 0
    op = gzip.open if path.endswith(".gz") else open
    try:
        with op(path, "rt", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                n += 1
                d = (rec.get("event") or {}).get("dataset")
                ds[d if d else "<none>"] += 1
                if n >= SAMPLE_LINES:
                    break
    except Exception as e:
        w(f"unreadable: {os.path.relpath(path, REPO)}: {e}")
    return ds


def cpath(c):
    """On-disk dir for a collection: data/<name>, or c['path'] when the
    collection lives elsewhere (e.g. data/aggregates/<name>)."""
    return os.path.join(REPO, c.get("path", os.path.join("data", c["name"])))


def resolve_file_pointer(coll_dir, value):
    """Resolve a top-level `file` pointer per schema/record.schema.json:
    the schema documents both repo-root-relative and collection-relative
    forms. Values starting with "data/" are repo-root-relative; anything
    else is tried collection-relative first, then repo-root-relative
    (e.g. "notes/x.md" may point at repo-root notes/, "raw/..." at the
    collection's own raw/). Returns (target, None) when the target is a
    real file on disk, else (None, reason)."""
    if not isinstance(value, str) or not value.strip():
        return None, "not a non-empty string"
    fv = value.strip()
    if os.path.isabs(fv):
        return None, "absolute path (field is documented as relative)"
    cands = ([os.path.join(REPO, fv)] if fv.startswith("data/")
             else [os.path.join(coll_dir, fv), os.path.join(REPO, fv)])
    for cand in cands:
        target = os.path.abspath(os.path.normpath(cand))
        if os.path.commonpath((os.path.normpath(REPO), target)) != \
                os.path.normpath(REPO):
            continue
        if os.path.isfile(target):
            return target, None
    return None, "no such file on disk"


def check_file_pointers():
    """Every top-level `file` pointer in every events.jsonl/rollup.jsonl
    under data/ resolves to a real on-disk path (full scan, not sampled).
    A move/rename that leaves stale pointers fails here before it can
    silently corrupt the corpus."""
    checked = 0
    for root in (DATA, os.path.join(DATA, "aggregates")):
        if not os.path.isdir(root):
            continue
        for dirpath, _dirnames, filenames in os.walk(root):
            for fn in EVENT_FILES:
                fp = os.path.join(dirpath, fn)
                if not os.path.isfile(fp):
                    fp = fp + ".gz"
                    if not os.path.isfile(fp):
                        continue
                coll = os.path.relpath(dirpath, DATA)
                op = gzip.open if fp.endswith(".gz") else open
                try:
                    fh = op(fp, "rt", encoding="utf-8", errors="replace")
                except Exception as e:
                    w(f"{coll}: unreadable {os.path.basename(fp)}: {e}")
                    continue
                with fh:
                    for lineno, line in enumerate(fh, 1):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                        except ValueError:
                            continue
                        if "file" not in rec:
                            continue
                        checked += 1
                        _t, why = resolve_file_pointer(dirpath, rec["file"])
                        if why:
                            ev = rec.get("event") or {}
                            rid = ev.get("id") or rec.get("fingerprint") or \
                                f"<line {lineno}>"
                            v(f"{coll}: row event.id={rid}: file pointer "
                              f"{rec['file']!r} does not resolve ({why})")
    return checked


def main():
    reg = json.load(open(REGISTRY))
    man = json.load(open(MANIFEST))
    collections = {c["name"]: c for c in reg["collections"]}
    reserved = set(reg["reserved_dirs"])
    loose = {f["file"] for f in reg["loose_files"]}
    try:
        staged_idx = loader_discover_staged(reg)
    except (ValueError, OSError) as exc:
        v(f"staged ingest discovery failed: {exc}")
        staged_idx = {}
    manifest_idx = {e["index"] for e in man.get("via_script", [])}
    for idx in sorted(manifest_idx & set(staged_idx)):
        v(f"via_script/staged overlap: {idx}")
    if manifest_idx:
        v("via_script is unsupported: stage event-layer files instead")

    # entries to check: data/<name> plus data/aggregates/<name>
    roots = [(DATA, "")]
    agg = os.path.join(DATA, "aggregates")
    if os.path.isdir(agg):
        roots.append((agg, "aggregates/"))

    # --- pass 1: every data/ entry is known -------------------------------
    for root, prefix in roots:
        for entry in sorted(os.listdir(root)):
            p = os.path.join(root, entry)
            if not os.path.isdir(p):
                if prefix == "" and entry not in loose:
                    v(f"unregistered loose file: data/{entry}")
                continue
            if not prefix and entry in reserved:
                continue
            c = collections.get(entry)
            if c is None:
                v(f"unregistered collection dir: data/{prefix}{entry}")
                continue
            if prefix and c.get("path") != f"data/{prefix}{entry}":
                v(f"{entry}: lives at data/{prefix}{entry} but registry "
                  f"path is {c.get('path')!r}")
            if not SLUG_RE.match(entry):
                v(f"bad collection name (not a valid slug/index): {entry}")
            # provenance expectations
            if c.get("status") in ("canonical", "support"):
                if not os.path.exists(os.path.join(p, "PROVENANCE.md")):
                    w(f"{entry}: missing PROVENANCE.md")
                if not os.path.exists(os.path.join(p, "SHA256SUMS")):
                    w(f"{entry}: missing SHA256SUMS")
            # canonical root layout: only events.jsonl/rollup.jsonl/
            # PROVENANCE.md/SHA256SUMS + raw/ at the root
            if not c.get("virtual"):
                for item in sorted(os.listdir(p)):
                    ip = os.path.join(p, item)
                    if os.path.isdir(ip):
                        if item not in ROOT_DIRS:
                            v(f"{entry}: non-raw dir at root: {item}/")
                    elif item not in ROOT_FILES and not ROOT_BUILD_SCRIPT_RE.match(item):
                        v(f"{entry}: non-event file at root: {item}")
            # records land in the right directory (raw/ files are the
            # raw layer: exempt from event.dataset checks)
            files = sorted(
                f for f in
                glob.glob(os.path.join(p, "**", "*.jsonl"), recursive=True)
                + glob.glob(os.path.join(p, "**", "*.jsonl.gz"), recursive=True)
                if "raw" not in os.path.relpath(f, p).split(os.sep))
            ds_all = Counter()
            for f in files[:MAX_FILES]:
                ds_all.update(datasets_in_file(f))
            real = {d for d in ds_all if d != "<none>"}
            if real:
                allowed = {entry}
                # rollup.jsonl rows legitimately carry <collection>-rollup
                allowed.add(entry + "-rollup")
                ov = c.get("dataset_override")
                if isinstance(ov, str):
                    allowed.add(ov)
                elif isinstance(ov, list):
                    allowed.update(ov)
                bad = real - allowed
                if bad:
                    v(f"{entry}: records carry unexpected event.dataset "
                      f"{sorted(bad)} (allowed: {sorted(allowed)})")
            if ds_all.get("<none>"):
                w(f"{entry}: {ds_all['<none>']} sampled records lack "
                  f"event.dataset (pending schema backfill)")
            # Every physical collection with staged events must be indexed,
            # including reference, support and aggregate collections.
            event_files = [os.path.join(p, fn) for fn in EVENT_FILES
                           if os.path.isfile(os.path.join(p, fn))]
            if event_files and not c.get("virtual"):
                idx = c.get("index")
                if not idx:
                    v(f"{entry}: staged event records require non-null registry index")
                for fp in event_files:
                    rel = os.path.relpath(fp, REPO)
                    if not any(rel in paths for paths in staged_idx.values()):
                        v(f"{entry}: {os.path.basename(fp)} is not discovered for ingest")

    # --- pass 2: registry/manifest consistency -----------------------------
    for e in man.get("via_script", []):
        idx = e["index"]
        base = idx.split("-rollup")[0] if idx.endswith("-rollup") else idx
        if idx not in collections and base not in collections:
            w(f"manifest index {idx!r} has no collections.json entry")
        for s in e.get("scripts", []):
            if not os.path.exists(os.path.join(REPO, s)):
                v(f"manifest via_script missing on disk: {s}")

    # --- pass 3: top-level `file` pointers resolve --------------------------
    n_fp = check_file_pointers()

    # --- report -------------------------------------------------------------
    for m in violations:
        print(f"VIOLATION  {m}")
    for m in warnings:
        print(f"warning    {m}")
    print(f"\n{len(violations)} violations, {len(warnings)} warnings "
          f"({len(collections)} collections, {len(loose)} loose files "
          f"registered, {n_fp} file pointers checked)")
    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
