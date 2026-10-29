#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane 2026-09-04-thecolony-ai.

Reads evidence/2026-09-04-thecolony-ai/events.jsonl (55 legacy records) and
emits one Factum bundle (57 records):

  1 source      capture-set for the whole recon snapshot
  1 run         collection run (captures + pattern battery)
 10 observation intel.report      <- venue_finding (investigator posts)
  9 observation web.capture       <- extraction (search API captures)
  6 observation reachability.check<- tag_liveness (RubyGems oracle checks)
  6 observation web.capture       <- download (page/API/RSS captures)
 24 claim                         <- corpus_hit (19) + corpus_grep_negative (5)

Usage: python3 build_factum_bundle.py <repo-root> > bundle.json
"""
import hashlib
import json
import os
import sys

REPO = sys.argv[1]
LANE_DIR = os.path.join(REPO, "evidence/2026-09-04-thecolony-ai")
RAW = os.path.join(LANE_DIR, "raw")
LANE_TAG = "2026-09-04-thecolony-ai"
LANE_DOCS = "data/lanes/2026-09-04-thecolony-ai/"  # post-move locator
ACTOR = "agent:lane-ingest-2026-09-04-thecolony-ai"


def S(v):
    """Stringify tag values (prior-lane convention: all tag values strings)."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (list, tuple)):
        return ",".join(str(x) for x in v)
    return str(v)


recs = [json.loads(l) for l in open(os.path.join(LANE_DIR, "events.jsonl")) if l.strip()]
assert len(recs) == 55, f"expected 55 events, got {len(recs)}"

by_kind = {}
for r in recs:
    by_kind.setdefault(r["record_kind"], []).append(r)
assert len(by_kind["venue_finding"]) == 10
assert len(by_kind["extraction"]) == 9
assert len(by_kind["tag_liveness"]) == 6
assert len(by_kind["download"]) == 6
assert len(by_kind["corpus_hit"]) == 19
assert len(by_kind["corpus_grep_negative"]) == 5

# --- batch-internal dedup by key field -------------------------------------
def keys(kind, fn):
    ks = [fn(r) for r in by_kind[kind]]
    assert len(set(ks)) == len(ks), f"dup keys in {kind}: {ks}"
    return ks

keys("venue_finding", lambda r: r["labels"]["post.id"])
keys("extraction", lambda r: r["labels"]["search.query"])
keys("tag_liveness", lambda r: r["labels"]["probe.target"])
keys("download", lambda r: r["labels"]["capture.file"])
keys("corpus_hit", lambda r: r["labels"]["sweep.pattern"])
keys("corpus_grep_negative", lambda r: r["labels"]["sweep.pattern"])
# sweep patterns unique across hit + negative sets
allpats = ([r["labels"]["sweep.pattern"] for r in by_kind["corpus_hit"]] +
           [r["labels"]["sweep.pattern"] for r in by_kind["corpus_grep_negative"]])
assert len(set(allpats)) == 24, "sweep pattern overlap"

# --- cached-path resolution --------------------------------------------------
search_stems = {os.path.splitext(f)[0]: f for f in os.listdir(os.path.join(RAW, "search"))}

def search_file(query):
    norm = query.lower().replace(" ", "_").replace(".", "_")
    for stem, fname in search_stems.items():
        if stem.lower() == norm:
            return os.path.join(LANE_DOCS, "raw/search", fname)
    raise KeyError(f"no search file for query {query!r}")

def cascade_file(r):
    url = r["source_url"]
    name = r["labels"]["probe.target"]
    kind = r["labels"]["probe.kind"]
    if "owners/" in url:
        fname = f"cascade_owner_{name}.json"
    elif kind == "geminfo" and url.endswith("/" + name):
        fname = f"cascade_geminfo_{name}.txt"
    else:
        fname = f"cascade_rubygems_{name}.json"
    path = os.path.join(RAW, fname)
    assert os.path.exists(path), f"missing cascade file {fname}"
    return os.path.join(LANE_DOCS, "raw", fname)

# --- raw-file sha256 cross-check (self-verification) -------------------------
# ROOT CAUSE (2026-10-09 ingest): the 2026-09-28 capture saved 6 text files
# with LF->CRLF newline normalization. Legacy events.jsonl / manifest.json /
# SHA256SUMS hashes and sizes describe the original wire bytes (LF); the raw/
# files on disk carry CRLF. Verified: stripping \r from the disk bytes
# reproduces the legacy sha256 and byte size exactly for all 6 files. The
# raw files are kept byte-identical (evidence rule); the discrepancy is
# annotated on the affected records and in evidence/remove-*/README.md.
def raw_bytes(rel):
    with open(os.path.join(LANE_DIR, rel.replace(LANE_DOCS, "")), "rb") as f:
        return f.read()

def raw_file_tags(rel, legacy_sha256, legacy_size):
    """Verify disk bytes against legacy wire-byte hash; annotate CRLF note."""
    disk = raw_bytes(rel)
    disk_sha = hashlib.sha256(disk).hexdigest()
    tags = {"raw_file_size": str(len(disk)), "raw_file_sha256": disk_sha}
    if disk_sha == legacy_sha256 and len(disk) == legacy_size:
        return tags
    norm = disk.replace(b"\r\n", b"\n")
    assert hashlib.sha256(norm).hexdigest() == legacy_sha256, \
        f"unexplained hash gap for {rel}"
    assert len(norm) == legacy_size, f"unexplained size gap for {rel}"
    tags["raw_file_note"] = (
        "capture-time LF->CRLF normalization: raw file on disk carries CRLF; "
        "legacy sha256/size describe the original wire (LF) bytes; verified "
        "that stripping \\r reproduces the legacy hash and size exactly")
    return tags

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": LANE_DOCS,
        "platform": "thecolony.ai public surfaces (read-only recon)",
        "title": ("thecolony.ai recon snapshot 2026-09-28: 10 investigator posts, "
                  "9 search result sets, 6 RubyGems oracle checks, 6 page/API/RSS "
                  "captures, 24 pattern-battery results"),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": "unauthenticated public GETs, >=2-3s pacing; no accounts, no posts, no DMs, no writes",
        "window": "2026-09-28 ~03:10-03:45 UTC",
        "captures": "31",
        "scope": "thecolony.ai incident wiki + investigator posts + /api/v1 surfaces",
    },
})

# --- run: collection ----------------------------------------------------------
bundle_records.append({
    "kind": "run", "ref": "run",
    "body": {
        "run_kind": "collection",
        "started": "2026-09-28T03:10:00Z",
        "ended": "2026-09-28T03:45:00Z",
        "params": {
            "window": "2026-09-28 ~03:10-03:45 UTC (approximate, per PROVENANCE.md)",
            "method": ("read-only recon: unauthenticated public GETs at polite pacing "
                       "(>=2-3s); no accounts created, no posts, no DMs, no writes"),
            "phases": ("captures (for-agents page, 2 wiki pages, /api/v1/colonies, "
                       "/api/v1/instructions, feed.rss, 10 posts, 9 searches, "
                       "6 RubyGems oracle checks) + 24-pattern battery over the "
                       "collected corpus"),
            "collection_note": ("Investigator posts are third-party analysis, cited as "
                                "reported; API post bodies truncate at ~5000 chars; "
                                "ludism.org and ApchemWiki unreachable from capture network"),
        },
        "coverage": {
            "complete": True, "scanned": 55, "total": 55,
            "description": ("55 legacy events: 10 venue_finding + 9 extraction + "
                            "6 tag_liveness + 6 download + 19 corpus_hit + "
                            "5 corpus_grep_negative"),
        },
    },
    "tags": {"lane": LANE_TAG},
})

# --- 10 venue_finding -> intel.report -----------------------------------------
for r in by_kind["venue_finding"]:
    lab = r["labels"]
    pid = lab["post.id"]
    bundle_records.append({
        "kind": "observation", "ref": f"post-{pid[:8]}",
        "body": {
            "type": "intel.report",
            "data_schema": "urn:factum:intel:report:1",
            "data": {
                "lab": "thecolony.ai",
                "title": lab["post.title"],
                "url": r["source_url"],
                "report_date": lab["post.created_at"][:10],
                "summary": r["description"],
                "cached_path": os.path.join(LANE_DOCS, "raw/posts", pid + ".json"),
                "provenance": (f"thecolony.ai/api/v1/posts/{pid} (public GET), retrieved "
                               f"{r['retrieved_at']}; investigator post - third-party "
                               "analysis, cited as reported"),
            },
            "source": "@src",
            "observed_at": lab["post.created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "OBSERVED",
            "legacy_record_kind": "venue_finding",
            "legacy_fingerprint": r["fingerprint"],
            "timestamp_source": lab["timestamp_source"],
            "post.id": pid,
            "post.author": lab["post.author"],
            "post.colony": lab["post.colony"],
            "post.post_type": lab["post.post_type"],
            "post.score": S(lab["post.score"]),
            "post.comment_count": S(lab["post.comment_count"]),
            "post.tags": S(lab["post.tags"]),
            "post.language": lab["post.language"],
        },
    })

# --- 9 extraction -> web.capture (search captures) -----------------------------
for r in by_kind["extraction"]:
    lab = r["labels"]
    bundle_records.append({
        "kind": "observation", "ref": f"search-{lab['search.query'][:12].replace(' ','_').replace('.','_')}",
        "body": {
            "type": "web.capture",
            "data_schema": "urn:factum:web:web-capture:1",
            "data": {
                "capture_kind": "http",
                "requested_url": r["source_url"],
                "tool": r["retrieved_via"],
            },
            "source": "@src",
            "observed_at": r["retrieved_at"],
            "time_basis": "collector_clock",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "OBSERVED",
            "legacy_record_kind": "extraction",
            "legacy_fingerprint": r["fingerprint"],
            "timestamp_source": lab["timestamp_source"],
            "search.query": lab["search.query"],
            "search.result_count": S(lab["search.result_count"]),
            "search.total": S(lab["search.total"]),
            "search.result_colonies": S(lab["search.result_colonies"]),
            "cached_path": search_file(lab["search.query"]),
        },
    })

# --- 6 tag_liveness -> reachability.check --------------------------------------
for r in by_kind["tag_liveness"]:
    lab = r["labels"]
    cached = cascade_file(r)
    file_tags = raw_file_tags(cached, r["sha256"], r["size_bytes"])
    bundle_records.append({
        "kind": "observation", "ref": f"cascade-{lab['probe.target']}",
        "body": {
            "type": "reachability.check",
            "data_schema": "urn:factum:web:reachability-check:1",
            "data": {
                "target": r["source_url"],
                "method": "GET",
                "outcome": "response",
            },
            "source": "@src",
            "observed_at": r["retrieved_at"],
            "time_basis": "collector_clock",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "OBSERVED",
            "legacy_record_kind": "tag_liveness",
            "legacy_fingerprint": r["fingerprint"],
            "timestamp_source": lab["timestamp_source"],
            "probe.target": lab["probe.target"],
            "probe.kind": lab["probe.kind"],
            "probe.result": lab["probe.result"],
            "probe.raw_bytes": S(lab["probe.raw_bytes"]),
            "sha256": r["sha256"],
            "size_bytes": S(r["size_bytes"]),
            "cached_path": cached,
            **file_tags,
        },
    })

# --- 6 download -> web.capture --------------------------------------------------
for r in by_kind["download"]:
    lab = r["labels"]
    cached = os.path.join(LANE_DOCS, "raw", lab["capture.file"])
    assert os.path.exists(os.path.join(LANE_DIR, "raw", lab["capture.file"])), \
        f"missing capture file {lab['capture.file']}"
    file_tags = raw_file_tags(cached, r["sha256"], r["size_bytes"])
    tags = {
        "lane": LANE_TAG,
        "grade": "OBSERVED",
        "legacy_record_kind": "download",
        "legacy_fingerprint": r["fingerprint"],
        "timestamp_source": lab["timestamp_source"],
        "capture.file": lab["capture.file"],
        "capture.byte_size": S(lab["capture.byte_size"]),
        "sha256": r["sha256"],
        "cached_path": cached,
        **file_tags,
    }
    if "api.colony_count" in lab:
        tags["api.colony_count"] = S(lab["api.colony_count"])
    bundle_records.append({
        "kind": "observation", "ref": f"dl-{lab['capture.file'][:16]}",
        "body": {
            "type": "web.capture",
            "data_schema": "urn:factum:web:web-capture:1",
            "data": {
                "capture_kind": "http",
                "requested_url": r["source_url"],
                "tool": r["retrieved_via"],
            },
            "source": "@src",
            "observed_at": r["retrieved_at"],
            "time_basis": "collector_clock",
            "files": [],
        },
        "tags": tags,
    })

# --- 19 corpus_hit + 5 corpus_grep_negative -> claim -----------------------------
for kind in ("corpus_hit", "corpus_grep_negative"):
    for r in by_kind[kind]:
        lab = r["labels"]
        bundle_records.append({
            "kind": "claim", "ref": f"sweep-{lab['sweep.pattern']}",
            "body": {
                "subject": "@run",
                "property": "pattern_hit_count",
                "value": {
                    "pattern": lab["sweep.pattern"],
                    "count": lab["sweep.count"],
                    "scope": lab["sweep.scope"],
                },
                "basis": "OBSERVED",
                "cites": ["@run"],
                "note": r["description"],
            },
            "tags": {
                "lane": LANE_TAG,
                "legacy_record_kind": kind,
                "legacy_fingerprint": r["fingerprint"],
                "timestamp_source": lab["timestamp_source"],
            },
        })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-2026-09-04-thecolony-ai",
    "tags": {},
    "records": bundle_records,
}
print(json.dumps(bundle, indent=1))
