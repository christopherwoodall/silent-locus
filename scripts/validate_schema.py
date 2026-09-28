#!/usr/bin/env python3
"""Corpus validator: every JSONL record under data/ must match
schema/record.schema.json. Stdlib only.

Usage:
    python3 scripts/validate_schema.py [path ...]   # files or dirs (default: data/)
Exit 0 when all records validate, 1 otherwise. Prints per-file error counts
and the first few violations.
"""

import glob
import json
import os
import re
import sys
from datetime import datetime

REPO = __file__.rsplit("/scripts/", 1)[0]

REQUIRED = ["@timestamp", "event", "record_kind", "fingerprint", "labels"]
OPTIONAL = ["source_url", "description", "confidence", "tags", "observer",
            "retrieved_at", "retrieved_via", "sha256", "size_bytes",
            "note", "status", "matched_string", "file"]
ALLOWED = set(REQUIRED) | set(OPTIONAL)
FP_RE = re.compile(r"^[0-9a-f]{64}$")
KIND_RE = re.compile(r"^[a-z0-9_]+$")
LABEL_KEY_RE = re.compile(r"^[a-z0-9_.]+$")
DS_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def parse_ts(v):
    if not isinstance(v, str) or not v:
        return False
    try:
        datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        return False
    return v.endswith("Z") or v.endswith("+00:00")


def check(rec, ctx):
    errs = []
    if not isinstance(rec, dict):
        return ["not an object"]
    for k in REQUIRED:
        if k not in rec:
            errs.append(f"missing required key: {k}")
    for k in rec:
        if k not in ALLOWED:
            errs.append(f"unexpected top-level key: {k}")
    if "event" in rec:
        ev = rec["event"]
        if not isinstance(ev, dict):
            errs.append("event not an object")
        else:
            if not DS_RE.match(str(ev.get("dataset", ""))):
                errs.append(f"bad event.dataset: {ev.get('dataset')!r}")
            if not parse_ts(ev.get("created", "")):
                errs.append(f"bad event.created: {ev.get('created')!r}")
    if "record_kind" in rec and not KIND_RE.match(str(rec["record_kind"])):
        errs.append(f"bad record_kind: {rec['record_kind']!r}")
    if "fingerprint" in rec and not FP_RE.match(str(rec["fingerprint"] or "")):
        errs.append(f"bad fingerprint: {str(rec['fingerprint'])[:24]!r}")
    if "@timestamp" in rec and not parse_ts(rec["@timestamp"]):
        errs.append(f"bad @timestamp: {str(rec['@timestamp'])[:40]!r}")
    lab = rec.get("labels")
    if isinstance(lab, dict):
        if not lab:
            errs.append("labels empty")
        for k, v in lab.items():
            if not LABEL_KEY_RE.match(k):
                errs.append(f"bad labels key: {k!r}")
            if isinstance(v, dict):
                errs.append(f"labels.{k} is a nested object")
            elif isinstance(v, list) and any(isinstance(i, (dict, list)) for i in v):
                errs.append(f"labels.{k} is a nested array")
    elif "labels" in rec:
        errs.append("labels not an object")
    if "tags" in rec and not (isinstance(rec["tags"], list)
                              and all(isinstance(t, str) for t in rec["tags"])):
        errs.append("tags not a string array")
    if "observer" in rec:
        ob = rec["observer"]
        if not isinstance(ob, dict) or not ob.get("product"):
            errs.append("observer missing product")
    for tf in ("retrieved_at",):
        if tf in rec and not parse_ts(rec[tf]):
            errs.append(f"bad {tf}: {str(rec[tf])[:40]!r}")
    if "sha256" in rec and not FP_RE.match(str(rec["sha256"] or "")):
        errs.append("bad sha256")
    if "size_bytes" in rec and not isinstance(rec["size_bytes"], int):
        errs.append("size_bytes not int")
    return errs


def main():
    targets = sys.argv[1:] or ["data"]
    files = []
    for t in targets:
        t = t if os.path.isabs(t) else os.path.join(REPO, t)
        if os.path.isdir(t):
            files += glob.glob(os.path.join(t, "**", "*.jsonl"), recursive=True)
        elif os.path.isfile(t):
            files.append(t)
    total_errs = 0
    bad_files = 0
    checked = 0
    for p in sorted(files):
        ferrs = []
        with open(p) as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                checked += 1
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError as e:
                    ferrs.append(f"line {i}: invalid JSON: {e}")
                    continue
                for e in check(rec, f"{p}:{i}"):
                    ferrs.append(f"line {i}: {e}")
                    if len(ferrs) >= 6:
                        break
            # noqa: inner break only caps per-file detail
        if ferrs:
            bad_files += 1
            total_errs += len(ferrs)
            rel = os.path.relpath(p, REPO)
            print(f"FAIL {rel} ({len(ferrs)} shown)")
            for e in ferrs[:6]:
                print(f"    {e}")
    print(f"checked {checked} records in {len(files)} files; "
          f"{bad_files} files with violations")
    sys.exit(1 if total_errs else 0)


if __name__ == "__main__":
    main()
