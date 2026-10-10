#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane 2026-10-09-transluce-intel.

Reads evidence/2026-10-09-transluce-intel/events.jsonl (109 legacy records,
all record_kind=transluce_finding) and emits one Factum bundle (111 records):

  1 source      capture-set: the 2026-10-08 Transluce findings-tracker pull
  1 run         ingest-prep: lane reconstruction + bundle extraction
109 observation intel.report <- transluce_finding (one per tracker finding)

Mapping rules (Factum evidence rules + pre-ingest standing rules):
- title = finding.data.summary, byte-identical to the tracker text.
- summary = finding.data.description, byte-identical, never truncated.
- The primary identifier is the tracker URL (source_url), not the numeric
  tracker id; the numeric id is preserved in tags, not used as a title.
- Grade is UPSTREAM: these are the finders' own claims via the tracker.
- Verbatim text also persists in the lane's raw/ cached pull JSON.

Usage: python3 build_factum_bundle.py <repo-root> > bundle.json
"""
import json
import os
import sys

REPO = sys.argv[1]
LANE_DIR = os.path.join(REPO, "evidence/2026-10-09-transluce-intel")
LANE_TAG = "transluce-intel"
LANE_DOCS = "data/lanes/2026-10-09-transluce-intel/"  # post-move locator
ACTOR = "agent:lane-ingest-2026-10-09-transluce-intel"
RETRIEVAL = "2026-10-08T12:41Z"
RAW_PULL = os.path.join(LANE_DOCS, "raw/findings-list-20261008.json")


def S(v):
    """Stringify tag values (prior-lane convention: all tag values strings)."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (list, tuple)):
        return ",".join(str(x) for x in v)
    return str(v)


evs = [json.loads(l) for l in open(os.path.join(LANE_DIR, "events.jsonl")) if l.strip()]
assert len(evs) == 109, f"expected 109 events, got {len(evs)}"

# --- batch-internal dedup by key field --------------------------------------
kinds = set(e["record_kind"] for e in evs)
assert kinds == {"transluce_finding"}, f"unexpected kinds: {kinds}"
ids = [e["labels"]["finding.id"] for e in evs]
assert len(set(ids)) == 109, "duplicate finding ids inside batch"
urls = [e["source_url"] for e in evs]
assert len(set(urls)) == 109, "duplicate source_urls inside batch"

# --- verbatim completeness ---------------------------------------------------
for e in evs:
    f = e["finding"]
    d = f["data"]
    assert d["summary"] == e["labels"]["finding.summary"], (
        f"event label summary differs from verbatim finding for id {f['id']}")
    assert d["description"], f"empty description for id {f['id']}"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": LANE_DOCS,
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce findings-tracker pull 2026-10-08: 109 finding "
                  "claims (tracker IDs 36-174), retrieved "
                  "2026-10-08T12:41Z"),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("tl.py pagination GET /api/findings via custom.transluce "
                   "connector (Secure Vault bearer token); "
                   "tl.py findings returns only first 25; "
                   "tl.py export json truncates at 200KB"),
        "window": "pull retrieved 2026-10-08T12:41Z (findings dated 2026-09-27 to 2026-10-08)",
        "coverage": "109 of 109 tracker findings in the pull; 30 tracker IDs in range absent (likely deleted/restricted)",
    },
})

# --- run: ingest-prep ----------------------------------------------------------
bundle_records.append({
    "kind": "run", "ref": "run",
    "body": {
        "run_kind": "ingest-prep",
        "started": "2026-10-09T23:11:00Z",
        "ended": "2026-10-10T01:02:00Z",
        "tool": "build_factum_bundle.py (lane-local)",
        "params": {
            "method": ("read cached pull raw/findings-list-20261008.json; one "
                       "legacy-lane event per finding preserving the full "
                       "verbatim finding record (id, submitter, submitter_id, "
                       "form_version, sensitive, created_at, updated_at, and "
                       "the complete data object); one intel.report per event; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "evidence/2026-10-09-transluce-intel/",
            "pre_ingest_dedup": ("match --url against Factum corpus for all "
                                 "109 tracker URLs: zero pre-existing records; "
                                 "in-batch dedup by finding id and source_url"),
        },
        "coverage": {
            "complete": True, "scanned": 109, "total": 109,
            "description": "109 legacy events, all transluce_finding -> 109 intel.report observations",
        },
    },
    "tags": {"lane": LANE_TAG},
})

# --- 109 transluce_finding -> intel.report --------------------------------------
for e in evs:
    lab = e["labels"]
    f = e["finding"]
    d = f["data"]
    fid = f["id"]
    bundle_records.append({
        "kind": "observation", "ref": f"finding-{fid}",
        "body": {
            "type": "intel.report",
            "data_schema": "urn:factum:intel:report:1",
            "data": {
                "lab": "Transluce",
                "title": d["summary"],
                "url": e["source_url"],
                "report_date": f["created_at"][:10],
                "summary": d["description"],
                "cached_path": RAW_PULL,
                "provenance": (
                    "Transluce volunteer findings tracker API "
                    "(d3ncjnql1bmhe8.cloudfront.net), paginated GET /api/findings "
                    "via tl.py (custom.transluce connector, Secure Vault bearer), "
                    f"retrieved {RETRIEVAL}; third-party finding claim, cited as "
                    "reported (UPSTREAM)"),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "legacy_record_kind": "transluce_finding",
            "legacy_fingerprint": e["fingerprint"],
            "timestamp_source": lab["timestamp_source"],
            "finding.id": S(f["id"]),
            "finding.submitter": f["submitter"],
            "finding.submitter_id": S(f["submitter_id"]),
            "finding.form_version": S(f["form_version"]),
            "finding.sensitive": S(f["sensitive"]),
            "finding.ai_company": S(d.get("ai_company")),
            "finding.cyberattack": S(d.get("cyberattack")),
            "finding.government": S(d.get("government")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-2026-10-09-transluce-intel",
    "tags": {"lane": LANE_TAG},
    "records": bundle_records,
}

json.dump(bundle, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
print(f"bundle: {len(bundle_records)} records "
      f"(1 source + 1 run + 109 intel.report)", file=sys.stderr)
