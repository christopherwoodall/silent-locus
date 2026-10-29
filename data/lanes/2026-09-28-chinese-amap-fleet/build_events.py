#!/usr/bin/env python3
"""Build venue_finding events for the 2026-09-28 Chinese Amap fleet collection.

One event per urlquery report (amap.com + gaode.com, 2026-09-28..2026-10-05).
- @timestamp = report scan time (date field, UTC Z)
- record_kind = venue_finding
- fingerprint = sha256(report_id)
- event.dataset = "2026-09-28-chinese-amap-fleet"
- Dedupe: skips report_ids already in events.jsonl (only NEW events).
"""
import hashlib, json, os, re, glob
from datetime import datetime, timezone

COLL = os.path.dirname(os.path.abspath(__file__))
DS = "2026-09-28-chinese-amap-fleet"
CREATED = datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
TAG_RE = re.compile(r"[?&](uqscan|uqtag|uq)=([^&#\s]+)")

def route_of(url):
    u = url.lower()
    if "r.jina.ai" in u or "microlink" in u or "href.li" in u or "translate.goog" in u or "allorigins" in u:
        return "relay"
    if "httpbin" in u or "httpbun" in u or "livecodes" in u or "webhook.site" in u:
        return "carrier"
    if "amap.com" in u or "gaode.com" in u:
        return "direct"
    return "other"

def build_event(r, origin):
    rid = r["report_id"]
    url = ((r.get("url") or {}).get("addr")) or ""
    m = TAG_RE.search(url)
    tag = m.group(2)[:80] if m else None
    return {
        "@timestamp": r["date"],
        "event": {"dataset": DS, "created": CREATED},
        "record_kind": "venue_finding",
        "fingerprint": hashlib.sha256(rid.encode()).hexdigest(),
        "labels": {
            "report_id": rid,
            "submitted_domain": ((r.get("url") or {}).get("domain")) or "",
            "fleet_tag": tag,
            "route": route_of(url),
            "timestamp_source": "labels:date",
            "file_origin": origin,
        },
        "source_url": f"https://urlquery.net/report/{rid}",
        "matched_string": tag,
        "note": f"Chinese Amap fleet scan ({route_of(url)} route). Submitted: {url[:160]}",
    }

def main():
    ev_path = os.path.join(COLL, "events.jsonl")
    seen = set()
    if os.path.exists(ev_path):
        with open(ev_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    seen.add(json.loads(line)["labels"]["report_id"])
    new = []
    for p in (sorted(glob.glob(os.path.join(COLL, "raw", "*.json"))) +
                 sorted(glob.glob(os.path.join(COLL, "raw", "gaode", "*.json"))) +
                 sorted(glob.glob(os.path.join(COLL, "raw", "infra", "*", "*.json"))) +
                 sorted(glob.glob(os.path.join(COLL, "raw", "pivots", "*", "*.json")))):
        bn = os.path.basename(p)
        if "COLLECT_STATS" in p:
            continue
        d = json.load(open(p))
        reps = [d] if (bn.startswith("report_") and "report_id" in d) else (d.get("reports", []) or [])
        for r in reps:
            if r["report_id"] not in seen:
                seen.add(r["report_id"])
                new.append(build_event(r, os.path.relpath(p, COLL)))
    with open(ev_path, "a") as f:
        for e in new:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"added {len(new)} new events ({len(seen)} total)")

if __name__ == "__main__":
    main()
