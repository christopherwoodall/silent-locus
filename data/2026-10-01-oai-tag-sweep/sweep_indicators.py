#!/usr/bin/env python3
"""Lane-4 sweep: full indicator set + timestamps-first timeline scoring.

Steering (BigSexyWarlock69, 2026-10-01): score every candidate against ALL
indicators, rank by indicator count (2+ outranks lone oai), preserve full
timestamps, build per-hit timeline records, flag temporal clustering and
cross-source temporal overlaps with known windows.

SOURCES (all read-only, never modified):
  - ~/workspace/muse-home/projects/swarmtraces-hf-corpus/elastic-exports/
      urlquery-incidents-20260928T022324Z.jsonl.gz   (51,643 frozen records)
      collusion-wiki-20260928T025051Z.jsonl.gz       (80,434 frozen records)
      rubygems-goimport-campaign-20260928T022324Z.jsonl.gz (6,619 frozen records)
  - ~/workspace/transluce-urlquery/urlquery-agent-activity-2026-09-22-v5/
      (Transluce's own published dataset, all-reports.csv etc.)

OUTPUTS (this event dir only - annotated sidecar, never merged into frozen data):
  - events.jsonl           annotated per-hit sidecar (source, timestamps, indicators, evidence)
  - sweep_summary.json     per-indicator counts per source, score histogram
  - timeline.json          per-hit timeline records + burst minutes
  - temporal_overlaps.md   temporal overlap notes vs known windows
  - PROVENANCE.md, SHA256SUMS

No invented IDs: every hit carries its source record _id / report_id / event_id.
"""
import csv, gzip, json, os, re, sys
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE = os.path.expanduser(
    "~/workspace/muse-home/projects/swarmtraces-hf-corpus/elastic-exports")
TRANSLUCE = os.path.expanduser(
    "~/workspace/transluce-urlquery/urlquery-agent-activity-2026-09-22-v5")

FROZEN_SOURCES = {
    "urlquery-incidents": os.path.join(ARCHIVE, "urlquery-incidents-20260928T022324Z.jsonl.gz"),
    "collusion-wiki": os.path.join(ARCHIVE, "collusion-wiki-20260928T025051Z.jsonl.gz"),
    "rubygems-goimport": os.path.join(ARCHIVE, "rubygems-goimport-campaign-20260928T022324Z.jsonl.gz"),
}

# ---- indicator definitions: (name, compiled regex) ----
INDICATORS = [
    ("oai_prefix", re.compile(r"(?:^|[^a-z0-9])oai[-_a-z0-9]", re.I)),
    ("zz_label", re.compile(r"(?:^|[^a-z0-9])zz[a-z0-9_-]", re.I)),
    ("epoch_nonce", re.compile(r"(?:^|[^0-9])(1[78]\d{8})(?:[^0-9]|$)")),
    ("httpbun_httpbin", re.compile(r"httpb[u]?in", re.I)),
    ("jina_allorigins_dagd", re.compile(r"r\.jina\.ai|allorigins|dagd", re.I)),
    # A000/ZZEND dead-drop chunks are standalone tokens in the JFrog grammar;
    # exclude matches embedded in UUID/sha hex runs (e.g. uuid '426a0003-...').
    ("webhook_deaddrop", re.compile(r"(?<![0-9a-fA-F-])(?:A000|ZZEND)(?![0-9a-fA-F-])")),
    ("github_remote_cache_zz", re.compile(r"github-remote-cache/zz", re.I)),
    ("goimport_canary", re.compile(r"go-import", re.I)),
    ("uniq_nonce_param", re.compile(r"[?&](uniq|nonce|_t|cb)=\d{6,}", re.I)),
    ("arquivo_pt", re.compile(r"arquivo\.pt", re.I)),
    ("markdown_new", re.compile(r"markdown\.new", re.I)),
    ("cors_conversion_proxy", re.compile(
        r"corsproxy|cors\.lol|workers\.dev|sirjosh|corsfix|cors-anywhere|"
        r"12ft\.io|1ft\.io|textise|textance|googleusercontent|translate\.google", re.I)),
    ("disposable_email", re.compile(
        r"tempmail|guerrillamail|mailinator|10minutemail|trashmail|yopmail|"
        r"dispostable|throwawaymail|fakeinbox|sharklasers|mailsac", re.I)),
    ("exposed_key_in_url", re.compile(
        r"[?&](api[-_]?key|subscription[-_]?key|access[-_]?key|auth[-_]?token|"
        r"secret|token|private[-_]?key)=", re.I)),
    ("double_slash_path", re.compile(r"https?://[^/\s]+/[^\s?]*//")),
    ("file_suffix_antibot", re.compile(
        r"(\.json|\.xml|\.csv|\.txt|\.pdf)(\?|$|[&#])|[?&](output|raw|url|debug)=", re.I)),
    ("direct_ip_route", re.compile(r"https?://\d{1,3}(\.\d{1,3}){3}")),
    ("collusion_wiki_ref", re.compile(r"collusion\.wiki", re.I)),
]

# Known windows (steering): earliest origin, visible middle, incident bursts
WINDOWS = {
    "nov2025_origin": ("2025-11-01", "2025-12-01"),
    "may2026_visible_middle": ("2026-05-01", "2026-09-26"),
    "maryland_may6": ("2026-05-06", "2026-05-07"),
    "kansas_may7": ("2026-05-07", "2026-05-08"),
    "lac_may28": ("2026-05-28", "2026-05-29"),
    "lac_jun9": ("2026-06-09", "2026-06-10"),
    "bea_jun16_18": ("2026-06-16", "2026-06-19"),
    "doe_jun17": ("2026-06-17", "2026-06-18"),
}


def iter_strings(obj, out):
    """Collect all string values from a nested structure (bounded)."""
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            iter_strings(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            iter_strings(v, out)


def scan_doc(text_blobs):
    """Return {indicator_name: [evidence_snippet]} for fired indicators."""
    fired = {}
    joined = "\n".join(text_blobs)
    for name, rx in INDICATORS:
        m = rx.search(joined)
        if m:
            start = max(0, m.start() - 40)
            fired[name] = joined[start:m.end() + 40].replace("\n", " ")[:140]
    return fired


def short_id(src_id):
    return (src_id or "")[:12]


def process_frozen():
    hits = []
    per_source_counts = {s: Counter() for s in FROZEN_SOURCES}
    per_source_total = {}
    score_hist = {s: Counter() for s in FROZEN_SOURCES}
    per_minute = Counter()
    per_day_source = defaultdict(lambda: defaultdict(int))
    for source, path in FROZEN_SOURCES.items():
        n = 0
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                n += 1
                try:
                    doc = json.loads(line)
                except Exception:
                    continue
                s = doc.get("_source", {})
                blobs = []
                iter_strings(s, blobs)
                fired = scan_doc(blobs)
                if not fired:
                    continue
                for ind in fired:
                    per_source_counts[source][ind] += 1
                score = len(fired)
                score_hist[source][score] += 1
                ts = s.get("@timestamp", "")
                minute = ts[:16] if len(ts) >= 16 else ts
                day = ts[:10] if len(ts) >= 10 else ts
                per_minute[(source, minute)] += 1
                per_day_source[day][source] += 1
                url = (s.get("url") or {}).get("original", "") if isinstance(s.get("url"), dict) else ""
                ref = (s.get("event") or {}).get("url", "")
                lbl = s.get("labels") or {}
                hits.append({
                    "source": "frozen:" + source,
                    "record_id": doc.get("_id", ""),
                    "event_time": ts,
                    "indicator_count": score,
                    "indicators": sorted(fired.keys()),
                    "evidence": fired,
                    "url_original": url[:300] if isinstance(url, str) else "",
                    "report_url": ref if isinstance(ref, str) else "",
                    "tags": s.get("tags", []) if isinstance(s.get("tags"), list) else [],
                    "labels_note": {k: str(v)[:80] for k, v in lbl.items()
                                    if k in ("hunt.report_id", "hunt.campaign",
                                             "hunt.sha256_submitted_url",
                                             "event_id", "event_type",
                                             "label", "record_kind")} ,
                    "record_kind": s.get("record_kind", ""),
                })
        per_source_total[source] = n
        print(f"{source}: scanned {n}, hits {sum(score_hist[source].values())}", file=sys.stderr)
    return hits, per_source_counts, per_source_total, score_hist, per_minute, per_day_source


def process_transluce():
    """Sweep Transluce's published dataset for the same indicators."""
    hits = []
    counts = Counter()
    csv_path = os.path.join(TRANSLUCE, "all-reports.csv")
    if not os.path.exists(csv_path):
        return hits, counts
    with open(csv_path, newline="", encoding="utf-8", errors="replace") as fh:
        for row in csv.DictReader(fh):
            blobs = [str(v or "") for v in row.values()]
            fired = scan_doc(blobs)
            if fired:
                for ind in fired:
                    counts[ind] += 1
                hits.append({
                    "source": "transluce-dataset",
                    "record_id": row.get("report_id", ""),
                    "event_time": row.get("report_date_utc", ""),
                    "indicator_count": len(fired),
                    "indicators": sorted(fired.keys()),
                    "evidence": fired,
                    "report_url": row.get("report_url", ""),
                    "why_included": (row.get("why_included", "") or "")[:300],
                    "disposition": row.get("disposition", ""),
                })
    return hits, counts


def window_overlap(day):
    return [w for w, (a, b) in WINDOWS.items() if a <= day < b]


def main():
    hits, counts, totals, score_hist, per_minute, per_day_source = process_frozen()
    thits, tcounts = process_transluce()

    all_hits = hits + thits
    # rank: indicator count desc, then time
    all_hits.sort(key=lambda h: (-h["indicator_count"], h["event_time"]))

    ev_path = os.path.join(BASE, "events.jsonl")
    with open(ev_path, "w", encoding="utf-8") as fh:
        for h in all_hits:
            fh.write(json.dumps(h, ensure_ascii=False) + "\n")

    # bursts: per (source, minute) with >= 8 hits
    bursts = [{"source": s, "minute": m, "hits": c}
              for (s, m), c in per_minute.items() if c >= 8]
    bursts.sort(key=lambda b: -b["hits"])

    # timeline records: hit times by source for overlap analysis
    tl = [{"event_time": h["event_time"], "source": h["source"],
           "indicators": h["indicators"], "indicator_count": h["indicator_count"],
           "record_id": short_id(h["record_id"]),
           "url": (h.get("report_url") or h.get("url_original") or "")[:120]}
          for h in all_hits]
    with open(os.path.join(BASE, "timeline.json"), "w") as fh:
        json.dump({"timeline": tl, "bursts_per_minute_ge8": bursts}, fh, indent=1)

    # overlap days: days with hits in >= 2 sources
    overlap_days = sorted(
        (d, dict(s)) for d, s in per_day_source.items() if len(s) >= 2)
    days_with_windows = [
        {"day": d, "sources": s, "known_windows": window_overlap(d)}
        for d, s in per_day_source.items() if window_overlap(d)
    ]

    summary = {
        "run_date_utc": "2026-10-01",
        "frozen_totals_scanned": totals,
        "hits_per_indicator_per_source": {s: dict(c) for s, c in counts.items()},
        "transluce_dataset_hits_per_indicator": dict(tcounts),
        "transluce_hits": len(thits),
        "score_histogram": {s: {str(k): v for k, v in h.items()} for s, h in score_hist.items()},
        "total_annotated_events": len(all_hits),
        "events_ge2_indicators": sum(1 for h in all_hits if h["indicator_count"] >= 2),
        "overlap_days_ge2_sources": len(overlap_days),
    }
    with open(os.path.join(BASE, "sweep_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1)

    with open(os.path.join(BASE, "temporal_overlaps.md"), "w") as fh:
        fh.write("# Temporal overlaps vs known windows (2026-10-01 sweep)\n\n")
        fh.write("Days in the annotated hit set that fall inside known windows:\n\n")
        for d in sorted(days_with_windows, key=lambda x: x["day"]):
            fh.write(f"- {d['day']}: sources={d['sources']} windows={d['known_windows']}\n")
        fh.write("\nDays with annotated hits in >=2 sources (cross-source join key):\n\n")
        for d, s in overlap_days[:60]:
            fh.write(f"- {d}: {s}\n")

    print(json.dumps(summary, indent=1)[:2000])


if __name__ == "__main__":
    main()
