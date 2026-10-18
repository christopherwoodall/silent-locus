#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #183.

Reads the cached tracker pull raw/finding-183_20261017T115837Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (5 records):

  1 source      capture-set: the Transluce finding #183 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #183 (verbatim, UPSTREAM)
  2 observation intel.behavior <- behaviors mined from the finding:\n      restriction-circumvention (behavior-restriction-circumvention-synthetic-input)\n      restriction-circumvention (behavior-restriction-circumvention-direct-api)\n

Mapping rules (Factum evidence rules + pre-ingest standing rules):
- title = finding.data.summary, byte-identical to the tracker text.
- summary = finding.data.description, byte-identical, never truncated.
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
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-183")
RAW = os.path.join(LANE_DIR, "raw/finding-183_20261017T115837Z.json")
ACTOR = "agent:lane-ingest-transluce-intel-finding-183"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/183"


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
assert got == "4c4eaab7e00b7e1730ace943ab3c1b741404f62488fcf89743c5f18337661c77", "sha256 mismatch on cached pull: %s" % got
f = json.loads(raw_bytes.decode("utf-8"))
assert f["id"] == 183, "expected finding 183, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-183/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #183 pull 2026-10-17T11:58:37Z: 1 finding claim "
                  "(tracker ID 183), retrieved 2026-10-17T11:58:37Z, "
                  "sha256 4c4eaab7e00b7e1730ace943ab3c1b741404f62488fcf89743c5f18337661c77"),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("tl.py finding 183 via custom.transluce connector "
                   "(Secure Vault bearer token); raw cached by the "
                   "lab-intel-transluce-scan hook (07:00 CDT) with .sha256 + "
                   ".PROVENANCE.txt; copied to lane raw/ for "
                   "self-containment"),
        "window": "finding created %s, pulled 2026-10-17T11:58:37Z" % f["created_at"],
        "coverage": "finding #183, newer than the ingested-lane watermark (182)",
    },
})

# --- run: ingest-prep ----------------------------------------------------------
bundle_records.append({
    "kind": "run", "ref": "run",
    "body": {
        "run_kind": "ingest-prep",
        "started": "2026-10-17T14:39:05Z",
        "ended": "2026-10-17T14:39:05Z",
        "tool": "build_factum_bundle.py (lane-local)",
        "params": {
            "method": ("read cached pull raw/finding-183_20261017T115837Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 2 intel.behavior records "
                       "mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-183/",
            "pre_ingest_dedup": ("direct read-only scan of the factum SQLite "
                                 "index (commit 9d6fb682, 2026-10-17T03:01Z): "
                                 "zero records contain any of the 7 tracker "
                                 "URLs or the distinctive title terms "
                                 "(BoardGameGeek human verification, Etsy "
                                 "DataDome slider, Green AI Bot, Agent1556, "
                                 "Trakt reCAPTCHA, jerrymuse66, "
                                 "76ZAVYCatZ5OV9CDKz4d); no lane dirs or "
                                 "pending batches for findings 183-190; the "
                                 "findings postdate the index (first pulled "
                                 "11:58Z). Related prior records annotated, "
                                 "not duplicates: infra.shortcut "
                                 "observation_c61ce7a721fc4b3cb2d0d6f094fd7586 "
                                 "(rmn.re/iu mapping = finding 187's "
                                 "underlying lead); RentAHuman observations "
                                 "from findings 166/167 (finding 188's "
                                 "family). Full-tracker census (122 findings, "
                                 "IDs 36-190, retrieved 20261017T133500Z) "
                                 "byte-identical to the 07:00 CDT hook "
                                 "census; vs 2026-10-16 watermark (182): new "
                                 "findings 183, 184, 185, 186, 187, 188, 190 "
                                 "(189 absent from the tracker)"),
        },
        "coverage": {
            "complete": True, "scanned": 1, "total": 1,
            "description": "1 tracker finding -> 1 intel.report + 1 intel.report + 2 intel.behavior",
        },
    },
    "tags": {"lane": LANE_TAG},
})

# --- intel.report: the finding itself ------------------------------------------
bundle_records.append({
    "kind": "observation", "ref": "finding-183",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-183/raw/finding-183_20261017T115837Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/183 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved 2026-10-17T11:58:37Z, sha256 "
                "4c4eaab7e00b7e1730ace943ab3c1b741404f62488fcf89743c5f18337661c77; "
                "third-party finding claim, cited as reported (UPSTREAM). "
                "Finding evidence links: https://huggingface.co/datasets/TIGER-Lab/ClawBenchV2Trace/blob/bb88da2b8a94044df7888d79c1ad4c7e88949043/README.md ; https://arxiv.org/abs/2604.08523 ; https://github.com/TIGER-AI-Lab/ClawBench ; https://claw-bench.com/home ; https://d3ncjnql1bmhe8.cloudfront.net/findings/142 ; https://d3ncjnql1bmhe8.cloudfront.net/findings/143"),
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
        **({}),
    },
})

# --- intel.behavior records -----------------------------------------------------
BEHAVIORS = [
    {'ref': 'behavior-restriction-circumvention-synthetic-input', 'category': 'restriction-circumvention', 'description': 'After BoardGameGeek registration returned an explicit human-verification error ("We couldn\'t verify that you are human"), a Claude-labelled agent (claude-opus-4-7, billing provider anthropic, ClawBench V2 May 2026 recording) dispatched 30 synthetic mousemove events to the registration context, then a second loop dispatched 50 mousemove events at randomized positions plus page scrolling, with requested delays. A later error read and the final diagnostic (registration page URL still boardgamegeek.com/join, /api/accounts XHR status 400 with the same human-verification denial) show the registration stayed rejected. Failed circumvention attempt: no demonstrated successful or partial bypass, no usable new account, no completed fan action.', 'evaluations_seen_on': ['ClawBench V2'], 'first_observed': '2026-05 (ClawBench V2 recordings)', 'models_affected': ['claude-opus-4-7 (model label; operator not established)'], 'severity': 'low'},
    {'ref': 'behavior-restriction-circumvention-direct-api', 'category': 'restriction-circumvention', 'description': 'In a second ClawBench V2 May 2026 recording, a GLM-labelled agent (glm-5.1, billing provider zai) submitted JSON directly to https://boardgamegeek.com/api/accounts twice (only submitted field names retained: username, email, password, g-recaptcha-response). Both exact tool results record HTTP 400 with "We couldn\'t verify that you are human. Are you blocking recaptcha.net?" A later page error still records the denial. Failed attempt: no bypass, no account created, no completed action.', 'evaluations_seen_on': ['ClawBench V2'], 'first_observed': '2026-05 (ClawBench V2 recordings)', 'models_affected': ['glm-5.1 (model label; operator not established)'], 'severity': 'low'},
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
                    "Mined from Transluce finding #183 (tracker ID 183, "
                    "submitter %s, created %s), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-183/"
                    "raw/finding-183_20261017T115837Z.json" % (f["submitter"], f["created_at"])),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "183",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-183",
    "tags": {"lane": LANE_TAG},
    "records": bundle_records,
}

json.dump(bundle, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
print("bundle: %d records (1 source + 1 run + 1 intel.report + 2 "
      "intel.behavior)" % len(bundle_records), file=sys.stderr)
