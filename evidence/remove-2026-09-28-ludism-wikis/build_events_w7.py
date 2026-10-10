#!/usr/bin/env python3
"""Build events.jsonl for data/2026-09-28-ludism-wikis (normalization sweep, worker W7).

Usage: build_events_w7.py <repo-root>
One record per proxy-fetch sidecar raw/<target>__<via>.txt.meta.json
(27 target fetches + 2 proxy controls = 29 records); the .txt body, where
present, is paired into the same record (sha256/size_bytes).
Fingerprint identity string: "ludism-probe:<target>|<via>".
@timestamp: meta fetched_at (probe time).
confidence: high for jina fetches (control-verified working proxy),
low for allorigins fetches (its example.com control also failed -> inconclusive).
"""
import json
import hashlib
import os
import sys
import glob
import datetime

ROOT = sys.argv[1]
D = os.path.join(ROOT, "data", "2026-09-28-ludism-wikis")
RAW = os.path.join(D, "raw")
DATASET = "2026-09-28-ludism-wikis"
CREATED = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def to_z(s):
    dt = datetime.datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


out = []
for meta_path in sorted(glob.glob(os.path.join(RAW, "*.meta.json"))):
    meta = json.load(open(meta_path, encoding="utf-8"))
    target = meta["target"]
    via = meta["via"]
    is_control = target == "proxy_control"
    labels = {
        "probe.target": target,
        "probe.via": via,
        "probe.ok": meta["ok"],
        "probe.proxy_url": meta["proxy_url"],
        "probe.proxy_control": is_control,
        "timestamp_source": "labels:probe.fetched_at",
    }
    for k in ("http_status", "error", "content_type"):
        if meta.get(k) is not None:
            labels[f"probe.{k}"] = meta[k]
    rec = {
        "@timestamp": to_z(meta["fetched_at"]),
        "event": {"dataset": DATASET, "created": CREATED},
        "record_kind": "venue_probe",
        "fingerprint": hashlib.sha256(f"ludism-probe:{target}|{via}".encode()).hexdigest(),
        "labels": labels,
        "source_url": meta["proxy_url"],
        "confidence": "high" if via == "jina" else "low",
    }
    txt_path = meta_path[: -len(".meta.json")]
    if os.path.exists(txt_path):
        body = open(txt_path, "rb").read()
        if len(body) != meta.get("bytes"):
            print(f"WARN size drift {os.path.basename(txt_path)}: meta={meta.get('bytes')} actual={len(body)}")
        rec["sha256"] = hashlib.sha256(body).hexdigest()
        rec["size_bytes"] = len(body)
    if meta["ok"]:
        rec["description"] = (
            f"{via} probe of {target}: HTTP {meta.get('http_status')}, "
            f"{meta.get('bytes')} B body captured"
        )
    else:
        rec["description"] = f"{via} probe of {target}: FAILED ({meta.get('error')})"
    if is_control:
        rec["description"] += " [proxy control fetch]"
    out.append(rec)

with open(os.path.join(D, "events.jsonl"), "w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"{DATASET}: in={len(glob.glob(os.path.join(RAW, '*.meta.json')))} sidecars, out={len(out)} records")
