#!/usr/bin/env python3
"""Build events.jsonl proxy_ladder_entry records from raw/proxy_ladder_crossref.json.

Lane M extracted 89 unique proxy-related URLs from the 24 termina.digital DB
actor pages (the June-18 SEC county bridge per-handle proxy ladders, e.g.
md.succ.ai -> proxymule -> urltomarkdown -> allorigins). This file materializes
one schema-valid event per URL, deterministic fingerprints from the actor_url.

record_kind: proxy_ladder_entry (registered in schema/README.md)
fingerprint: sha256(actor_url)
@timestamp: 1970-01-01T00:00:00Z sentinel -- the actor-page URL observation has
    no recoverable event time; labels.timestamp_source = fallback:no_recoverable_date
"""
import hashlib
import json
import os
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "proxy_ladder_crossref.json")
OUT = os.path.join(HERE, "events.jsonl")
CREATED = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def fp(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()

def main():
    entries = json.load(open(RAW, encoding="utf-8"))
    records = []
    for e in entries:
        url = e["actor_url"]
        slugs = e.get("rmn_re_slugs", [])
        in_rmn = bool(e.get("in_rmn_re", False))
        rec = {
            "@timestamp": "1970-01-01T00:00:00Z",
            "event": {"dataset": "2026-03-12-paste-archive-gap", "created": CREATED},
            "record_kind": "proxy_ladder_entry",
            "fingerprint": fp(url),
            "labels": {
                "ladder.actor_url": url,
                "ladder.in_rmn_re": in_rmn,
                "ladder.rmn_re_slugs": slugs,
                "ladder.extraction": "lane-m termina.digital DB actor pages (24 pages)",
                "timestamp_source": "fallback:no_recoverable_date",
            },
            "source_url": url,
            "file": "data/2026-03-12-paste-archive-gap/raw/proxy_ladder_crossref.json",
            "status": "rmn_re_overlap" if in_rmn else "actor_page_only",
            "confidence": "high",
            "tags": ["proxy-ladder"] + (["rmn-re-overlap"] if in_rmn else []),
            "description": "proxy-ladder URL extracted from termina.digital DB actor page%s: %s"
            % (" (also a decoded rmn.re target)" if in_rmn else "", url),
        }
        records.append(rec)
    with open(OUT, "a", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"appended {len(records)} proxy_ladder_entry records to events.jsonl")

if __name__ == "__main__":
    main()
