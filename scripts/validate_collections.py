#!/usr/bin/env python3
"""Collection validator: naming, registration, and records-in-the-right-place
for data/. Companion to validate_schema.py (which checks record shape against
schema/record.schema.json); this one checks the COLLECTION level against
schema/collections.json + schema/collections.md. Stdlib only, disk only (no ES).

Violations (exit 1): unregistered data/ entry, bad collection name, loose
JSONL not in the registry, records whose event.dataset matches neither the
collection name nor its dataset_override, collections with records that no
ingest path can load (auto-discovered events.jsonl/rollup.jsonl or a
manifest via_script entry), non-event files/dirs at a collection root
(layout: events.jsonl + PROVENANCE.md + SHA256SUMS + raw/ only).

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

REPO = __file__.rsplit("/scripts/", 1)[0]
DATA = os.path.join(REPO, "data")
REGISTRY = os.path.join(REPO, "schema", "collections.json")
MANIFEST = os.path.join(REPO, "scripts", "local_es_manifest.json")
# collection dirs are date-prefixed: YYYY-MM-DD-<slug> (first-event date)
SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*$")
# canonical collection root layout (schema/collections.md)
ROOT_FILES = {"events.jsonl", "rollup.jsonl", "PROVENANCE.md",
              "SHA256SUMS", "SHA256SUMS.txt"}
ROOT_DIRS = {"raw"}
SAMPLE_LINES = 200
MAX_FILES = 4

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


def discover_staged():
    """Mirror of push_to_local_es.discover_staged: canonical layout event
    files -> index (records' event.dataset). Kept standalone (stdlib)."""
    found = {}
    for root in (DATA, os.path.join(DATA, "aggregates")):
        if not os.path.isdir(root):
            continue
        for entry in sorted(os.listdir(root)):
            p = os.path.join(root, entry)
            if not os.path.isdir(p) or (root == DATA and entry in
                                        {"raw", "indexes", "aggregates"}):
                continue
            for fn in ("events.jsonl", "rollup.jsonl"):
                fp = os.path.join(p, fn)
                if not os.path.exists(fp):
                    continue
                idx = None
                with open(fp, encoding="utf-8", errors="replace") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            idx = (json.loads(line).get("event") or {}
                                   ).get("dataset")
                        except ValueError:
                            pass
                        break
                if idx:
                    found.setdefault(idx, []).append(fp)
    return found


def main():
    reg = json.load(open(REGISTRY))
    man = json.load(open(MANIFEST))
    collections = {c["name"]: c for c in reg["collections"]}
    reserved = set(reg["reserved_dirs"])
    loose = {f["file"] for f in reg["loose_files"]}
    staged_idx = discover_staged()
    manifest_idx = {e["index"] for e in man.get("via_script", [])}
    loadable = manifest_idx | set(staged_idx)

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
                    elif item not in ROOT_FILES:
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
            # loadable? (support and aggregate collections are not
            # expected to load; raw-only dirs hold no event records)
            all_files = glob.glob(os.path.join(p, "**", "*.jsonl"),
                                  recursive=True)
            if all_files and not c.get("virtual"):
                idx = c.get("index")
                if idx and idx not in loadable:
                    v(f"{entry}: has records and index {idx!r} but it is "
                      f"neither discovered (events.jsonl) nor via_script")
                if not idx and files and c.get("status") not in (
                        "support",) and c.get("class") != "aggregate":
                    w(f"{entry}: has JSONL records but registry index is null "
                      f"(nothing loads it)")

    # --- pass 2: registry/manifest consistency -----------------------------
    for c in reg["collections"]:
        idx = c.get("index")
        if idx and not c.get("virtual") and c.get("status") in (
                "canonical", "support") and idx not in loadable \
                and os.path.isdir(cpath(c)):
            files = glob.glob(os.path.join(cpath(c), "**", "*.jsonl"),
                              recursive=True)
            if files:
                v(f"registry: {c['name']} has records + index {idx!r} but it "
                  f"is neither discovered nor via_script")
    for e in man.get("via_script", []):
        idx = e["index"]
        base = idx.split("-rollup")[0] if idx.endswith("-rollup") else idx
        if idx not in collections and base not in collections:
            w(f"manifest index {idx!r} has no collections.json entry")
        for s in e.get("scripts", []):
            if not os.path.exists(os.path.join(REPO, s)):
                v(f"manifest via_script missing on disk: {s}")

    # --- report -------------------------------------------------------------
    for m in violations:
        print(f"VIOLATION  {m}")
    for m in warnings:
        print(f"warning    {m}")
    print(f"\n{len(violations)} violations, {len(warnings)} warnings "
          f"({len(collections)} collections, {len(loose)} loose files registered)")
    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
