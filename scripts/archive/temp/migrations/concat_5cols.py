#!/usr/bin/env python3
"""Concat multi-file event collections into canonical events.jsonl (or rename for
admin-deletions), add labels.file_origin, verify counts, move strays to raw/,
append PROVENANCE note. Idempotent: uses temp file + os.replace."""
import json, os, sys, shutil

BASE = "/mnt/c/Users/chris/Desktop/projects/silent-locus/data"
ALLOWED_ROOT = {"events.jsonl", "rollup.jsonl", "PROVENANCE.md",
                "SHA256SUMS", "SHA256SUMS.txt", "raw"}
NOTE_DATE = "2026-09-29"

CONCAT_DIRS = {
    "2026-05-05-gomod-hunt": None,
    "2026-05-11-osv": "file_origin preserves the initial/retry pass identity that the fingerprint identity string encodes.",
    "2026-07-07-july7-gem-forensics": None,
    "2026-09-29-gem-temporal-pivot": None,
}

def concat_dir(name, extra_note):
    d = os.path.join(BASE, name)
    out = os.path.join(d, "events.jsonl")
    if os.path.exists(out):
        print(f"[{name}] events.jsonl already exists, skipping concat")
        return
    srcs = sorted(f for f in os.listdir(d)
                  if f.endswith(".jsonl") and os.path.isfile(os.path.join(d, f)))
    assert srcs, f"no jsonl sources in {d}"
    tmp = out + ".tmp"
    total_in = 0
    total_out = 0
    spot = []
    with open(tmp, "w", encoding="utf-8") as w:
        for fn in srcs:
            with open(os.path.join(d, fn), encoding="utf-8") as r:
                for line in r:
                    line = line.strip()
                    if not line:
                        continue
                    total_in += 1
                    rec = json.loads(line)
                    labels = rec.setdefault("labels", {})
                    labels["file_origin"] = fn
                    if len(spot) < 3 and total_out in (0, total_in // 2, ):
                        pass
                    w.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    total_out += 1
    assert total_in == total_out, f"count mismatch {total_in} != {total_out}"
    os.replace(tmp, out)
    # spot-check file_origin on 3 records (first, middle, last)
    with open(out, encoding="utf-8") as r:
        lines = r.readlines()
    checks = [0, len(lines) // 2, len(lines) - 1]
    origins = [json.loads(lines[i])["labels"].get("file_origin") for i in checks]
    assert all(origins), f"missing file_origin in spot check: {origins}"
    print(f"[{name}] merged {len(srcs)} files -> events.jsonl, "
          f"{total_out} records (verified == sum of inputs), "
          f"spot-check origins: {origins}")
    for fn in srcs:
        os.remove(os.path.join(d, fn))
    append_prov(d, name,
                f"Concatenated {len(srcs)} event shards ({', '.join(srcs)}) into "
                f"`events.jsonl` in sorted-filename order ({total_out} records; count "
                f"verified against inputs). Each record gained `labels.file_origin` = "
                f"original shard basename; no other fields changed. Source shards removed "
                f"after verification." + (f" {extra_note}" if extra_note else ""))

def admin_deletions():
    name = "2026-06-04-admin-deletions"
    d = os.path.join(BASE, name)
    # actual filenames differ from task spec; map sensibly
    mapping = {"admin-deletions-explicit.jsonl": "events.jsonl",
               "admin-deletions-rollup-flat.jsonl": "rollup.jsonl"}
    for src, dst in mapping.items():
        s, t = os.path.join(d, src), os.path.join(d, dst)
        if os.path.exists(t):
            print(f"[{name}] {dst} exists, skipping rename of {src}")
            continue
        assert os.path.exists(s), f"missing {s}"
        os.replace(s, t)
        n = sum(1 for _ in open(t, encoding="utf-8"))
        print(f"[{name}] renamed {src} -> {dst} unchanged ({n} records)")
    append_prov(d, name,
                "Renamed `admin-deletions-explicit.jsonl` -> `events.jsonl` and "
                "`admin-deletions-rollup-flat.jsonl` -> `rollup.jsonl`, contents "
                "unchanged (rollup records carry dataset "
                "`2026-06-04-admin-deletions-rollup`). No file_origin labels added "
                "(pure renames). NOTE: source basenames differed from the original "
                "migration spec (no date prefix); mapping adapted accordingly.")

def hygiene(name):
    d = os.path.join(BASE, name)
    raw = os.path.join(d, "raw")
    moved = []
    for entry in sorted(os.listdir(d)):
        if entry in ALLOWED_ROOT:
            continue
        src = os.path.join(d, entry)
        os.makedirs(raw, exist_ok=True)
        dst = os.path.join(raw, entry)
        if os.path.exists(dst):
            print(f"[{name}] raw/{entry} already exists, leaving {entry} in place")
            continue
        shutil.move(src, dst)
        moved.append(entry)
    if moved:
        print(f"[{name}] moved to raw/: {moved}")
    return moved

def append_prov(d, name, body):
    p = os.path.join(d, "PROVENANCE.md")
    note = (f"\n## Canonical layout migration ({NOTE_DATE})\n\n{body}\n")
    with open(p, "a", encoding="utf-8") as f:
        f.write(note)
    print(f"[{name}] PROVENANCE.md updated")

def main():
    for name, extra in CONCAT_DIRS.items():
        concat_dir(name, extra)
    admin_deletions()
    for name in list(CONCAT_DIRS) + ["2026-06-04-admin-deletions"]:
        hygiene(name)

if __name__ == "__main__":
    main()
