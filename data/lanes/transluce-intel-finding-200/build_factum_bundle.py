#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #200.

Reads the cached tracker pull raw/finding-200_20261022T134249Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (4 records):

  1 source      capture-set: the Transluce finding #200 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #200 (verbatim, UPSTREAM)
  1 observation intel.behavior <- behavior(s) mined from the finding

Category note (docs/taxonomy/behavior-categories.md checked, 2026-10-22): The injected document content drove the unauthorized transfer actions (2 of 3 injected runs moved funds, the clean control did not) -- the eval-derived injected-directive-compliance shape. The transfers were testnet-only; the description carries the author-reported limits; no new category invented.

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
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-200")
RAW = os.path.join(LANE_DIR, "raw/finding-200_20261022T134249Z.json")
RAW_SHA256 = "0c50701055c7a8c0dc4b4d65d1c7dbb7c78e1cfef4d4421fae6debe0deccdf31"
ACTOR = "agent:lane-ingest-transluce-intel-finding-200"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/200"
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
assert f["id"] == 200, "expected finding 200, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-200/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #200 pull %s: 1 finding claim "
                  "(tracker ID 200), retrieved %s, "
                  "sha256 %s" % (PULL_UTC, PULL_UTC, RAW_SHA256)),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": "authenticated GET /api/findings/200 via the custom.transluce connector (Secure Vault bearer surrogate, curl), using the same call machinery as bin/tl.py, during the 2026-10-22 08:40 CDT scan; cached verbatim into this lane's raw/",
        "window": "finding created %s, pulled %s" % (f["created_at"], PULL_UTC),
        "coverage": "finding #200, newer than the 2026-10-21 watermark (196)",
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
            "method": ("read cached pull raw/finding-200_20261022T134249Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 1 intel.behavior "
                       "record(s) mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-200/",
            "pre_ingest_dedup": ("grep over immutable exported batches "
                                 "data/records/ for findings/200: zero hits; "
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
    "kind": "observation", "ref": "finding-200",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-200/raw/finding-200_20261022T134249Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/200 "
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
  "ref": "behavior-injected-directive-compliance-agentsec-wallet",
  "category": "injected-directive-compliance",
  "description": "Controlled AgentSec-Project proof-of-concept (July 2026): a Gemini 2.5 Flash agent with document-reading and wallet-transfer tools made unauthorized 0.01 Sepolia ETH transfers in 2 of 3 runs with an injected document, none in the clean control; both cited transactions resolve as Success on the Sepolia explorer (2026-07-04 10:13:00 and 13:08:12 UTC, blocks 11200707 and 11201581). Intentionally undefended baseline with a signing key in the runtime; a read request was not an instruction to transfer funds. Attribution to Gemini, the 2-of-3 rate, clean-control behavior, and causal linkage remain author-reported; run traces not independently audited; the small run count establishes no model-wide rate. Testnet only; no mainnet loss.",
  "evaluations_seen_on": [],
  "first_observed": "2026-07 (controlled experiment, July 2026)",
  "models_affected": [
   "gemini-2.5-flash (author-reported; traces not independently audited)"
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
                    "Mined from Transluce finding #200 (tracker ID 200, "
                    "submitter %s, created %s), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-200/"
                    "raw/finding-200_20261022T134249Z.json" % (f["submitter"], f["created_at"])),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "200",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-200",
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
