#!/usr/bin/env python3
"""Build events.jsonl for data/2026-09-28-paste-linuxiarz (normalization sweep, worker W7).

Usage: build_events_w7.py <repo-root>
One record per paste .txt in raw/ (131 pastes), paste id = filename stem,
manifest.jsonl folded into labels. Body sha256/size verified against manifest.
Fingerprint identity string: "linuxiarz-paste:<paste_id>".
@timestamp: epoch(source_date_literals[0]) -> ISO Z (all 131 present, in range).
"""
import json
import hashlib
import os
import sys
import datetime

ROOT = sys.argv[1]
D = os.path.join(ROOT, "data", "2026-09-28-paste-linuxiarz")
RAW = os.path.join(D, "raw")
DATASET = "2026-09-28-paste-linuxiarz"
CREATED = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def to_z(s):
    dt = datetime.datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


out = []
n_in = 0
for line in open(os.path.join(RAW, "manifest.jsonl"), encoding="utf-8"):
    d = json.loads(line)
    n_in += 1
    pid = d["id"]
    txt_path = os.path.join(RAW, pid + ".txt")
    body = open(txt_path, "rb").read()
    assert hashlib.sha256(body).hexdigest() == d["body_sha256"], f"sha256 mismatch {pid}"
    assert len(body) == d["body_bytes"], f"size mismatch {pid}"
    epoch = int(d["source_date_literals"][0])
    ts = datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    labels = {
        "paste.id": pid,
        "paste.title": d.get("title"),
        "paste.source_date_literal": d["source_date_literals"][0],
        "paste.origin_kinds": d.get("origin_kinds", []),
        "paste.live_status": d.get("live_status"),
        "paste.corpus_record_ids": d.get("corpus_record_ids", []),
        "paste.source_references": d.get("source_references", []),
        "paste.retrieval_method": d.get("retrieval_method"),
        "timestamp_source": "labels:paste.source_date_literal",
    }
    rec = {
        "@timestamp": ts,
        "event": {"dataset": DATASET, "created": CREATED},
        "record_kind": "relay_paste",
        "fingerprint": hashlib.sha256(f"linuxiarz-paste:{pid}".encode()).hexdigest(),
        "labels": labels,
        "source_url": d["source_urls"][0],
        "sha256": d["body_sha256"],
        "size_bytes": d["body_bytes"],
        "retrieved_at": to_z(d["retrieval_timestamp"]),
        "retrieved_via": d.get("retrieval_method"),
        "confidence": "confirmed",
        "description": (
            f"paste.linuxiarz.pl paste '{d.get('title')}' ({d['body_bytes']} B): "
            "investigator-archived agent-text copy; live site returns 404"
        ),
    }
    out.append(rec)

with open(os.path.join(D, "events.jsonl"), "w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"{DATASET}: in={n_in} manifest entries, out={len(out)} records")
