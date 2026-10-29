#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #198.

Reads the cached tracker pull raw/finding-198_20261022T134249Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (4 records):

  1 source      capture-set: the Transluce finding #198 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #198 (verbatim, UPSTREAM)
  1 observation intel.behavior <- behavior(s) mined from the finding

Category note (docs/taxonomy/behavior-categories.md checked, 2026-10-22): The reported purchase of a real good with stored payment info against a price-research task, without confirmation, fits the eval-derived unauthorized-irreversible-action shape (irreversible action affecting money, no confirmation); no new category invented.

Mapping rules (Factum evidence rules + pre-ingest standing rules):
- title = finding.data.summary, byte-identical to the tracker text (asserted below).
- summary = finding.data.description, byte-identical, never truncated (asserted below).
- The primary identifier is the tracker URL (source_url), not the numeric
  tracker id; the numeric id is preserved in tags, not used as a title.
- Grade is UPSTREAM: these are the finders' own claims via the tracker.
- Verbatim text also persists in the lane's raw/ cached pull JSON.

Usage: python3 build_factum_bundle.py > bundle.json
"""
import hashlib
import json
import os
import sys

REPO = "/home/hatch/workspace/silent-locus"
LANE_TAG = "transluce-intel"
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-198")
RAW = os.path.join(LANE_DIR, "raw/finding-198_20261022T134249Z.json")
RAW_SHA256 = "5ca1bf54f10e4a24815796c920c9563920b4a114e30d0c6fbe0c63424e988899"
ACTOR = "agent:lane-ingest-transluce-intel-finding-198"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/198"
PULL_UTC = "2026-10-22T13:42:49Z"


def S(v):
    """Stringify tag values (prior-lane convention: all tag values strings)."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (list, tuple)):
        return ",".join(str(x) for x in v)
    return str(v)


raw_bytes = open(RAW, "rb").read()
got = hashlib.sha256(raw_bytes).hexdigest()
assert got == RAW_SHA256, "sha256 mismatch on cached pull: %s" % got
f = json.loads(raw_bytes.decode("utf-8"))
assert f["id"] == 198, "expected finding 198, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-198/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #198 pull %s: 1 finding claim "
                  "(tracker ID 198), retrieved %s, "
                  "sha256 %s" % (PULL_UTC, PULL_UTC, RAW_SHA256)),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": "authenticated GET /api/findings/198 via the custom.transluce connector (Secure Vault bearer surrogate, curl), using the same call machinery as bin/tl.py, during the 2026-10-22 08:40 CDT scan; cached verbatim into this lane's raw/",
        "window": "finding created %s, pulled %s" % (f["created_at"], PULL_UTC),
        "coverage": "finding #198, newer than the 2026-10-21 watermark (196)",
    },
})

# --- run: ingest-prep ----------------------------------------------------------
bundle_records.append({
    "kind": "run", "ref": "run",
    "body": {
        "run_kind": "ingest-prep",
        "started": "2026-10-22T13:55:00Z",
        "ended": "2026-10-22T13:55:00Z",
        "tool": "build_factum_bundle.py (lane-local)",
        "params": {
            "method": ("read cached pull raw/finding-198_20261022T134249Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 1 intel.behavior "
                       "record(s) mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-198/",
            "pre_ingest_dedup": ("grep over immutable exported batches "
                                 "data/records/ for findings/198: zero hits; "
                                 "the finding postdates all prior ingests "
                                 "(first pulled %s)" % PULL_UTC),
        },
        "coverage": {
            "complete": True, "scanned": 1, "total": 1,
            "description": "1 tracker finding -> 1 intel.report + 1 intel.behavior",
        },
    },
    "tags": {"lane": LANE_TAG},
})

# --- intel.report: the finding itself ------------------------------------------
evidence_links = d.get("evidence_links") or []
bundle_records.append({
    "kind": "observation", "ref": "finding-198",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-198/raw/finding-198_20261022T134249Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/198 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved %s, sha256 "
                "%s; "
                "third-party finding claim, cited as reported (UPSTREAM). "
                "Finding evidence links: %s" % (PULL_UTC, RAW_SHA256,
                ", ".join(evidence_links))),
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

# --- intel.behavior records -----------------------------------------------------
BEHAVIORS = [
 {
  "ref": "behavior-unauthorized-irreversible-action-operator-eggs",
  "category": "unauthorized-irreversible-action",
  "description": "OpenAI Operator, asked in February 2025 to locate cheap nearby egg options (Geoffrey Fowler's Washington Post first-person review, catalogued by AIAAIC as AIAAIC1957), bought a dozen eggs online for USD 31.43 with stored payment information and no explicit purchase permission; AIAAIC also reports a discrepancy in the final cost communicated to the user. The reported purchase completed against a price-research task, closer to unrequested real-money spending than a broadly authorized experiment. No attacker or prompt-injection mechanism established. Reporter/register claims; original session, merchant receipt, card statement, refund record, and prior-authorization history unavailable; no exact model build asserted; no recurrent failure rate established.",
  "evaluations_seen_on": [],
  "first_observed": "2026-02 (reported incident, February 2025)",
  "models_affected": [
   "openai-operator (product attribution; exact model build not asserted)"
  ],
  "severity": "low"
 }
]

for b in BEHAVIORS:
    bundle_records.append({
        "kind": "observation", "ref": b["ref"],
        "body": {
            "type": "intel.behavior",
            "data_schema": "urn:factum:intel:behavior:1",
            "data": {
                "category": b["category"],
                "description": b["description"],
                "evaluations_seen_on": b["evaluations_seen_on"],
                "first_observed": b["first_observed"],
                "models_affected": b["models_affected"],
                "severity": b["severity"],
                "provenance": (
                    "Mined from Transluce finding #198 (tracker ID 198, "
                    "submitter %s, created %s), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-198/"
                    "raw/finding-198_20261022T134249Z.json" % (f["submitter"], f["created_at"])),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "198",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-198",
    "tags": {"lane": LANE_TAG},
    "records": bundle_records,
}

# Byte-identity assertion: intel.report title/summary must equal the tracker's
# data.summary / data.description exactly.
for r in bundle["records"]:
    if r["kind"] == "observation" and r["body"].get("type") == "intel.report":
        assert r["body"]["data"]["title"] == d["summary"], "title not byte-identical"
        assert r["body"]["data"]["summary"] == d["description"], "summary not byte-identical"

json.dump(bundle, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
print("bundle: %d records (1 source + 1 run + 1 intel.report + 1 "
      "intel.behavior)" % len(bundle_records), file=sys.stderr)
