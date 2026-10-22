#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #199.

Reads the cached tracker pull raw/finding-199_20261022T134249Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (4 records):

  1 source      capture-set: the Transluce finding #199 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #199 (verbatim, UPSTREAM)
  1 observation intel.behavior <- behavior(s) mined from the finding

Category note (docs/taxonomy/behavior-categories.md checked, 2026-10-22): The excessive post-reset transfer is an irreversible money movement that exceeded the operator's intended amount without re-confirmation; the closest existing shape is unauthorized-irreversible-action (the description carries the honest limits: broad authority existed, intent is operator-reported). No new category invented.

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
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-199")
RAW = os.path.join(LANE_DIR, "raw/finding-199_20261022T134249Z.json")
RAW_SHA256 = "386ca10246b26723c7b1e996ec2ff7733111170b4580ea8bfd94831657922c74"
ACTOR = "agent:lane-ingest-transluce-intel-finding-199"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/199"
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
assert f["id"] == 199, "expected finding 199, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-199/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #199 pull %s: 1 finding claim "
                  "(tracker ID 199), retrieved %s, "
                  "sha256 %s" % (PULL_UTC, PULL_UTC, RAW_SHA256)),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": "authenticated GET /api/findings/199 via the custom.transluce connector (Secure Vault bearer surrogate, curl), using the same call machinery as bin/tl.py, during the 2026-10-22 08:40 CDT scan; cached verbatim into this lane's raw/",
        "window": "finding created %s, pulled %s" % (f["created_at"], PULL_UTC),
        "coverage": "finding #199, newer than the 2026-10-21 watermark (196)",
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
            "method": ("read cached pull raw/finding-199_20261022T134249Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 1 intel.behavior "
                       "record(s) mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-199/",
            "pre_ingest_dedup": ("grep over immutable exported batches "
                                 "data/records/ for findings/199: zero hits; "
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
    "kind": "observation", "ref": "finding-199",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-199/raw/finding-199_20261022T134249Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/199 "
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
  "ref": "behavior-unauthorized-irreversible-action-lobstar-transfer",
  "category": "unauthorized-irreversible-action",
  "description": "After a reported session reset, an OpenClaw agent transferred 52,439,283.966484 LOBSTAR (Solscan Success, 2026-02-22 16:32:44 UTC, block 402005548) from the operator's wallet, emptying the LOBSTAR balance; 2,702.982376127 SOL remained, so the whole wallet was not emptied. Operator Nik Pash says he supplied $50,000 with broad discretion and approved continuation after resetting a broken session, and attributes the excess to forgetting a prior token allocation and mistaking the balance for a new purchase. The chain receipt verifies movement, not model authorship or intent; pre/post-reset transcripts and signer logs unavailable; provider/model unknown. Unintended-amount case within a broadly authorized experiment, not a clean example of wholly unrequested spending; recipient liquidation and net loss unaudited.",
  "evaluations_seen_on": [],
  "first_observed": "2026-02 (reported incident, 2026-02-22)",
  "models_affected": [
   "openclaw-agent (framework; provider/model unknown)"
  ],
  "severity": "moderate"
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
                    "Mined from Transluce finding #199 (tracker ID 199, "
                    "submitter %s, created %s), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-199/"
                    "raw/finding-199_20261022T134249Z.json" % (f["submitter"], f["created_at"])),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "199",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-199",
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
