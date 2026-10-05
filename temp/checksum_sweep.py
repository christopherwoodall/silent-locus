#!/usr/bin/env python3
"""Regenerate/verify SHA256SUMS for every collection dir from schema/collections.json.

Convention: <sha256>  <relative-path> per line, covering every file under
the collection dir except SHA256SUMS, SHA256SUMS.txt, and PROVENANCE.md.
Subdirectory files (e.g. raw/) are included with relative paths.
Honors per-entry "path"; skips virtual entries, reserved dirs, duplicate names.
"""
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE = {"SHA256SUMS", "SHA256SUMS.txt", "PROVENANCE.md"}
RESERVED = set(json.load(open(os.path.join(ROOT, "schema", "collections.json")))["reserved_dirs"])

registry = json.load(open(os.path.join(ROOT, "schema", "collections.json")))
targets = []  # (name, abs_dir)
seen = set()
for c in registry["collections"]:
    if c.get("virtual"):
        continue
    rel = c.get("path", os.path.join("data", c["name"]))
    if rel in seen:
        continue
    seen.add(rel)
    top = rel.split("/", 2)[1] if rel.startswith("data/") and "/" in rel[5:] else rel
    if rel.split("/")[1] in RESERVED and rel.count("/") < 2:
        continue
    targets.append((c["name"], os.path.join(ROOT, rel)))

created, regenerated, valid, skipped, failed = [], [], [], [], []

for name, d in targets:
    if not os.path.isdir(d):
        skipped.append(name)
        continue
    entries = []
    for dirpath, _dirnames, filenames in os.walk(d):
        for fn in sorted(filenames):
            rel = os.path.relpath(os.path.join(dirpath, fn), d).replace(os.sep, "/")
            if rel in EXCLUDE:
                continue
            h = hashlib.sha256()
            with open(os.path.join(d, rel), "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            entries.append(f"{h.hexdigest()}  {rel}")
    content = "\n".join(entries) + ("\n" if entries else "")
    target = os.path.join(d, "SHA256SUMS")
    existed = os.path.exists(target)
    if existed:
        with open(target, "rb") as f:
            if f.read().decode() == content:
                valid.append(name)
                if name == "2026-09-28-dockerhub-trojan-images":
                    txt = os.path.join(d, "SHA256SUMS.txt")
                    if not os.path.exists(txt) or open(txt, "rb").read().decode() != content:
                        open(txt, "w").write(content)
                        regenerated.append(name + " (SHA256SUMS.txt)")
                continue
    with open(target, "w") as f:
        f.write(content)
    (regenerated if existed else created).append(name)
    if name == "2026-09-28-dockerhub-trojan-images":
        with open(os.path.join(d, "SHA256SUMS.txt"), "w") as f:
            f.write(content)

# verify every written/existing file with sha256sum -c (silent)
for name, d in targets:
    if not os.path.isdir(d) or not os.path.exists(os.path.join(d, "SHA256SUMS")):
        continue
    r = subprocess.run(["sha256sum", "-c", "SHA256SUMS"], cwd=d,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if r.returncode != 0:
        failed.append(name)
    if name == "2026-09-28-dockerhub-trojan-images":
        r2 = subprocess.run(["sha256sum", "-c", "SHA256SUMS.txt"], cwd=d,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if r2.returncode != 0:
            failed.append(name + " (SHA256SUMS.txt)")

print(f"CREATED ({len(created)}): {created}")
print(f"REGENERATED ({len(regenerated)}): {regenerated}")
print(f"ALREADY-VALID ({len(valid)}): {valid}")
print(f"SKIPPED no dir ({len(skipped)}): {skipped}")
print(f"VERIFY FAILED ({len(failed)}): {failed}")
sys.exit(1 if failed else 0)
