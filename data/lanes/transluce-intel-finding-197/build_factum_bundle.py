#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #197.

Reads the cached tracker pull raw/finding-197_20261022T134249Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (4 records):

  1 source      capture-set: the Transluce finding #197 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #197 (verbatim, UPSTREAM)
  1 observation intel.behavior <- behavior(s) mined from the finding

Category note (docs/taxonomy/behavior-categories.md checked, 2026-10-22): The injected encoded-message lure survived an agent rewrite and caused Grok to instruct Bankr to move funds -- the agent followed directives embedded in content, the eval-derived injected-directive-compliance shape (cf. AgentProcessBench). The irreversible money movement itself is carried in the description; no new category invented.

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
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-197")
RAW = os.path.join(LANE_DIR, "raw/finding-197_20261022T134249Z.json")
RAW_SHA256 = "e0f4ed7266be269aee1b5ab325c9d6eafdaee8a462232d310ce0dac24c650cd0"
ACTOR = "agent:lane-ingest-transluce-intel-finding-197"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/197"
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
assert f["id"] == 197, "expected finding 197, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-197/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #197 pull %s: 1 finding claim "
                  "(tracker ID 197), retrieved %s, "
                  "sha256 %s" % (PULL_UTC, PULL_UTC, RAW_SHA256)),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": "authenticated GET /api/findings/197 via the custom.transluce connector (Secure Vault bearer surrogate, curl), using the same call machinery as bin/tl.py, during the 2026-10-22 08:40 CDT scan; cached verbatim into this lane's raw/",
        "window": "finding created %s, pulled %s" % (f["created_at"], PULL_UTC),
        "coverage": "finding #197, newer than the 2026-10-21 watermark (196)",
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
            "method": ("read cached pull raw/finding-197_20261022T134249Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 1 intel.behavior "
                       "record(s) mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-197/",
            "pre_ingest_dedup": ("grep over immutable exported batches "
                                 "data/records/ for findings/197: zero hits; "
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
    "kind": "observation", "ref": "finding-197",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-197/raw/finding-197_20261022T134249Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/197 "
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
  "ref": "behavior-injected-directive-compliance-grok-bankr",
  "category": "injected-directive-compliance",
  "description": "A prompt-injection chain through Grok and Bankr moved 3,000,000,000 DRB on Base (transaction 0x6fc7eb7da9379383efda4253e4f599bbc3a99afed0468eabfe18484ec525739a, 2026-05-04 06:49:01 UTC, block 45543997, BaseScan Success). Per Bankr founder 0xDeployer's May 4 account, a block on Grok replies did not survive an agent rewrite, letting injected content cause Grok to instruct Bankr to transfer funds; Giskard describes an encoded-message lure; SlowMist clarifies Bankr's infrastructure executed the transfer and managed wallet custody. A return of 88,826 USDC (tx 0x54b3aa1ac3dd997926dd84eaa6d6aeb10e6606d2c70117bdfd9a4df015915a50, 10:01:07 UTC, block 45549760) was verified; the founder reports 80% returned overall, total recovery unverified. The finder's packet verified chain facts via explorer receipts on 2026-10-21 (not an independent node) and did not claim discovery of an unreported incident. Attacker-directed, not spontaneous agent spending; exact model version not established; xAI not claimed to manage the wallet; model causation not independently reproduced.",
  "evaluations_seen_on": [],
  "first_observed": "2026-05 (incident 2026-05-04)",
  "models_affected": [
   "grok-route (xAI product involvement supported; exact model version not established; xAI not claimed to manage the wallet)",
   "bankr-agent stack (executed the transfer; per SlowMist, Bankr infrastructure managed wallet custody)"
  ],
  "severity": "high"
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
                    "Mined from Transluce finding #197 (tracker ID 197, "
                    "submitter %s, created %s), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-197/"
                    "raw/finding-197_20261022T134249Z.json" % (f["submitter"], f["created_at"])),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "197",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-197",
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
