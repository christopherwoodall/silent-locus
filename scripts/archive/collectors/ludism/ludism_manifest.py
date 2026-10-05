#!/usr/bin/env python3
"""Build manifest.jsonl (per-file SHA-256, bytes, source URLs, timestamps)
for data/2026-09-28-ludism-wikis/. Resume-friendly: regenerates from scratch.
"""
import json, os, hashlib
from datetime import datetime, timezone

DDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "2026-09-28-ludism-wikis")

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def main():
    metas = {}
    for root, _, names in os.walk(DDIR):
        for n in names:
            if n.endswith(".meta.json"):
                try:
                    m = json.load(open(os.path.join(root, n)))
                    tgt = "%s__%s.txt" % (m["target"], m["via"])
                    metas[tgt] = m
                except Exception:
                    pass
    rows = []
    for root, _, names in os.walk(DDIR):
        for n in sorted(names):
            if n in ("manifest.jsonl",):
                continue
            p = os.path.join(root, n)
            rel = os.path.relpath(p, DDIR)
            row = {
                "file": rel,
                "sha256": sha256(p),
                "bytes": os.path.getsize(p),
                "manifested_at": datetime.now(timezone.utc).isoformat(),
            }
            if rel in metas:
                m = metas[rel]
                row["source_url"] = m.get("proxy_url")
                row["retrieval_timestamp"] = m.get("fetched_at")
                row["fetch_ok"] = m.get("ok")
                row["fetch_error"] = m.get("error")
            if n == "thecolony-claims-ludism.md":
                row["source_url"] = "https://thecolony.ai/wiki/openai-escapee-agent-incident-2026 (§13) + /wiki/escaped-agent-swarms (Surface #10)"
                row["verification"] = "not_independently_verified"
            if n == "thecolony-claims-apchemwiki.md":
                row["source_url"] = "https://thecolony.ai/wiki/openai-escapee-agent-incident-2026 (§14) + /wiki/escaped-agent-swarms (§2)"
                row["verification"] = "not_independently_verified"
            rows.append(row)
    with open(DDIR + "/raw/manifest.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print("manifest rows:", len(rows))

if __name__ == "__main__":
    main()
