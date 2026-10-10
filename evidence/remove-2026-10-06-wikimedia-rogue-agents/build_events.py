#!/usr/bin/env python3
"""Build events.jsonl for 2026-10-06-wikimedia-rogue-agents.

One `incident_revision` record per row of wikipedia-lane/records.json (the 54
diff URLs from WMF's openai-wikimedia-edits-2026-10-04.csv, resolved to
revision records). Columns per wikipedia-lane/_emit_list.py:
[host, oldid, title, user, ts, comment, tags, minor, parentid, content, status].
Diff URLs are joined from raw/openai-wikimedia-edits-2026-10-04.csv by oldid.
"""
import csv
import hashlib
import json
import re
from datetime import datetime, timezone

LANE = "2026-10-06-wikimedia-rogue-agents"
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fp(*parts):
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


diff_urls = {}
with open("raw/openai-wikimedia-edits-2026-10-04.csv", encoding="utf-8") as f:
    for row in csv.reader(f):
        for cell in row:
            cell = cell.strip()
            m = re.search(r"[?&](?:oldid|diff)=(\d+)", cell)
            if m:
                diff_urls[m.group(1)] = cell

records = []
with open("wikipedia-lane/records.json", encoding="utf-8") as f:
    rows = json.load(f)

for r in rows:
    host, oldid, title, user, ts, comment, tags, minor, parentid, content, status = r
    # the 5 nonexistent Web2Cit oldids have no timestamp (confirmed missing
    # via API badrevids); fall back to the hunt date, marked as fallback
    if ts:
        rec_ts, tsrc = ts, "record"
    else:
        rec_ts, tsrc = "2026-10-06T00:00:00Z", (
            "fallback:dir_date_prefix;revision nonexistent (badrevids)"
        )
    records.append(
        {
            "@timestamp": rec_ts,
            "event": {"dataset": LANE, "created": CREATED},
            "record_kind": "incident_revision",
            "fingerprint": fp(LANE, "incident-rev", host, str(oldid)),
            "labels": {
                "wiki.host": host,
                "rev.oldid": str(oldid),
                "rev.parentid": str(parentid),
                "rev.title": title,
                "rev.user": user,
                "rev.comment": comment,
                "rev.tags": tags,
                "rev.minor": minor,
                "content.status": status,
                "evidence.grade": "upstream" if status == "ok" else "observed-missing",
                "timestamp_source": tsrc,
            },
            "source_url": diff_urls.get(str(oldid)),
            "description": (
                f"WMF-evidence incident revision {oldid} on {host} ({title}) by "
                f"{user} at {ts}: comment '{comment}'; content "
                f"{'recovered' if status == 'ok' else 'UNRECOVERABLE via API'}"
            ),
            "confidence": "upstream" if status == "ok" else "confirmed",
        }
    )

with open("events.jsonl", "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("records:", len(records), "| csv diff URLs:", len(diff_urls))
