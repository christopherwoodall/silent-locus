#!/usr/bin/env python3
"""Build events.jsonl for 2026-10-01-arquivo-pt.

One `capture_collection_summary` record per timeline/<slug>.summary.json
(14 incident slugs; per-slug capture counts, Transluce claim match, peak
burst minutes). Hosts transcribed from the PROVENANCE.md slug table.
@timestamp is the incident-window start, marked in labels.timestamp_source.

NOTE: the per-capture rows in raw/<slug>.cdx.jsonl.gz were mapped into
trace events by the 2026-10-03-openai-agent-traces lane; this lane's
events describe the collection itself (per-slug reconciliation), not
duplicate those traces.
"""
import glob
import hashlib
import json
from datetime import datetime, timezone

LANE = "2026-10-01-arquivo-pt"
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Hosts per PROVENANCE.md slug table (domain match targets)
HOSTS = {
    "kansas-kansasmemory": ["kansasmemory.gov"],
    "maryland-edstats": ["msde.maryland.gov"],
    "illinois-iquery": ["iquery.illinois.gov"],
    "lac-collectionsearch": ["bac-lac.gc.ca"],
    "doe-crdc": ["civilrightsdata.ed.gov"],
    "bea-api": ["apps.bea.gov"],
    "omb-max": ["portal.max.gov"],
    "navy-history": ["history.navy.mil"],
    "doj-ojjdp": ["ojjdp.ncjrs.gov", "ojjdp.ojp.gov"],
    "sec": ["www.sec.gov"],
    "cdc-wonder": ["wonder.cdc.gov"],
    "calaccess": ["cal-access.sos.ca.gov"],
    "nysed-enrollment": ["data.nysed.gov"],
    "texas-dshs": ["dshs.texas.gov"],
}


def fp(*parts):
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


records = []
for path in sorted(glob.glob("timeline/*.summary.json")):
    with open(path, encoding="utf-8") as f:
        s = json.load(f)
    slug = s["slug"]
    window = s.get("incident_window") or []
    ts = f"{window[0]}T00:00:00Z" if window else "2026-10-01T00:00:00Z"
    tsrc = "labels:incident_window_start" if window else "fallback:dir_date_prefix"
    collected = s.get("captures_collected_unique", 0)
    records.append(
        {
            "@timestamp": ts,
            "event": {"dataset": LANE, "created": CREATED},
            "record_kind": "capture_collection_summary",
            "fingerprint": fp(LANE, "collection-summary", slug),
            "labels": {
                "slug": slug,
                "hosts": HOSTS.get(slug, []),
                "incident.window": window,
                "captures.collected_unique": collected,
                "captures.in_window": s.get("captures_in_incident_window"),
                "captures.outside_before": s.get("captures_outside_window_before"),
                "captures.outside_after": s.get("captures_outside_window_after"),
                "transluce.claimed_volume": s.get("transluce_claimed_volume"),
                "transluce.claimed_peak_per_min": s.get(
                    "transluce_claimed_peak_per_min"
                ),
                "volume.vs_claim": s.get("volume_vs_claim"),
                "burst.minutes_ge100": s.get("burst_minutes_ge100"),
                "peak.minute": (
                    s.get("peak_minutes_top10", [{}])[0].get("minute_utc")
                    if s.get("peak_minutes_top10")
                    else None
                ),
                "savepagenow.share": s.get("savepagenow_share"),
                "zero.source": collected == 0,
                "notes": s.get("notes", []),
                "timestamp_source": tsrc,
            },
            "description": (
                f"Arquivo.pt collection for slug '{slug}': {collected} unique "
                f"captures (Transluce claimed "
                f"{s.get('transluce_claimed_volume')}); "
                f"{s.get('burst_minutes_ge100')} burst minutes >=100/min"
                if collected
                else f"Arquivo.pt collection for slug '{slug}': 0 captures — "
                f"honest negative (Transluce claim: "
                f"{s.get('transluce_claimed_volume')})"
            ),
            "confidence": "confirmed",
        }
    )

with open("events.jsonl", "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("records:", len(records))
