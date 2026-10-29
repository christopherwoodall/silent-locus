#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #152 (content update).

Reads the cached tracker pull raw/finding-152_20261020T135018Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (3 records):

  1 source      capture-set: the Transluce finding #152 update API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #152 UPDATED VERSION (verbatim, UPSTREAM)

Versioning rules (factum immutability doctrine):
- The existing finding-152 record (ingested 2026-10-09 as intel.report
  observation_7a52d80629fa44a8b4521f0c83d602ef, actor
  agent:lane-ingest-2026-10-09-transluce-intel) is NOT touched: history is
  evidence. The old version stays cached at
  data/lanes/2026-10-09-transluce-intel/raw/findings-list-20261008.json
  (item id 152; old item bytes sha256
  2bd5bbd1582c6dc6974703630f5dd2ffe75da71502892dfe955c8f6c85812da1).
- This bundle adds ONE new intel.report record carrying the verbatim NEW
  title/summary/description (asserted byte-identical below).
- NO new intel.behavior records: the change is a two-line self-flagged
  duplicate note ("I've duplicated finding 110"); a note adds no new
  behavior.

What changed (observed):
- description prepended with "Update 2026-10-19: I just realized that I've
  duplicated finding 110, my bad!" + blank line (78 bytes); description
  3309 -> 3387 chars; old remainder byte-identical (verified).
- summary IDENTICAL (273 chars).
- form_version 3 -> 4; harm_level null -> "".
- updated_at 2026-10-05T05:20:48Z -> 2026-10-20T00:27:01Z (forward).

Usage: python3 build_factum_bundle.py > bundle.json
"""
import hashlib
import json
import os
import sys

REPO = "/home/hatch/workspace/silent-locus"
LANE_TAG = "transluce-intel"
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-152-update")
RAW = os.path.join(LANE_DIR, "raw/finding-152_20261020T135018Z.json")
RAW_SHA256 = "76477c4a8d285a61135bc542c2874816875922d96d22f787e023f44d2e2166f8"
OLD_SHA256 = "2bd5bbd1582c6dc6974703630f5dd2ffe75da71502892dfe955c8f6c85812da1"
ACTOR = "agent:lane-ingest-transluce-intel-finding-152-update"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/152"
PULL_UTC = "2026-10-20T13:50:18Z"


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
assert f["id"] == 152, "expected finding 152, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-152-update/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #152 UPDATED VERSION pull %s: "
                  "1 finding claim (tracker ID 152, updated 2026-10-20T00:27:01Z), "
                  "retrieved %s, sha256 %s" % (PULL_UTC, PULL_UTC, RAW_SHA256)),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("detail pull GET /api/findings/152 via tl.py "
                   "(custom.transluce connector, Secure Vault bearer token, "
                   "%s), after the 2026-10-20 07:02 CDT census detected a "
                   "content change; cached in the lane raw/ for "
                   "self-containment, with .sha256 + .PROVENANCE.txt" % PULL_UTC),
        "window": "finding created %s, updated 2026-10-20T00:27:01Z, pulled %s"
                  % (f["created_at"], PULL_UTC),
        "coverage": "finding #152 content update; old version already ingested "
                    "(intel.report observation_7a52d80629fa44a8b4521f0c83d602ef, "
                    "2026-10-09)",
    },
})

# --- run: ingest-prep ----------------------------------------------------------
bundle_records.append({
    "kind": "run", "ref": "run",
    "body": {
        "run_kind": "ingest-prep",
        "started": "2026-10-20T13:50:18Z",
        "ended": "2026-10-20T13:50:18Z",
        "tool": "build_factum_bundle.py (lane-local)",
        "params": {
            "method": ("read cached pull raw/finding-152_20261020T135018Z.json "
                       "(sha256-verified); one NEW intel.report record "
                       "carrying the verbatim updated title/summary/description; "
                       "no new intel.behavior records (the change is a "
                       "self-flagged duplicate note; a note adds no new "
                       "behavior); existing finding-152 record untouched; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-152-update/",
            "pre_ingest_dedup": ("distinctive new-version term "
                                 "(duplicated finding 110) checked against "
                                 "corpus convention: the ORIGINAL finding-152 "
                                 "is present as intel.report "
                                 "observation_7a52d80629fa44a8b4521f0c83d602ef "
                                 "(actor agent:lane-ingest-2026-10-09-"
                                 "transluce-intel) and is intentionally NOT "
                                 "touched or replaced; this update adds a "
                                 "versioned record alongside under a new "
                                 "idempotency key"),
            "what_changed": ("description prepended with the two-line "
                             "submitter self-flag (78 bytes, 3309 -> 3387 "
                             "chars; remainder byte-identical); summary "
                             "IDENTICAL; form_version 3 -> 4; harm_level "
                             "null -> \"\"; updated_at "
                             "2026-10-05T05:20:48Z -> 2026-10-20T00:27:01Z "
                             "(forward)"),
        },
        "coverage": {
            "complete": True, "scanned": 1, "total": 1,
            "description": "1 updated tracker finding -> 1 new intel.report (versioned update)",
        },
    },
    "tags": {"lane": LANE_TAG},
})

# --- intel.report: the UPDATED finding version ----------------------------------
bundle_records.append({
    "kind": "observation", "ref": "finding-152-updated",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-152-update/raw/finding-152_20261020T135018Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/152 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved %s, sha256 "
                "%s; "
                "VERSIONED UPDATE: the original finding-152 record "
                "(intel.report observation_7a52d80629fa44a8b4521f0c83d602ef, "
                "actor agent:lane-ingest-2026-10-09-transluce-intel, batch of "
                "2026-10-09, cached as item id 152 in "
                "data/lanes/2026-10-09-transluce-intel/raw/"
                "findings-list-20261008.json, old item bytes sha256 %s) is "
                "preserved untouched. This record carries the verbatim NEW "
                "version (updated_at 2026-10-20T00:27:01Z): description "
                "prepended with the submitter's two-line self-flagged "
                "duplicate note (\"I've duplicated finding 110\"); summary "
                "identical; form_version 3 -> 4; harm_level null -> \"\". "
                "Third-party finding claim, cited as reported (UPSTREAM). "
                "Finding evidence link: "
                "https://urlquery.net/report/c90eedd3-fc3b-47f4-9eff-01719b528d6b"
                % (PULL_UTC, RAW_SHA256, OLD_SHA256)),
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
        "finding.updated_at": S(f.get("updated_at")),
        "version": "updated-2026-10-20",
    },
})

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-152-update",
    "tags": {"lane": LANE_TAG},
    "records": bundle_records,
}

# Byte-identity assertion: intel.report title/summary must equal the tracker's
# data.summary / data.description exactly (the NEW version).
for r in bundle["records"]:
    if r["kind"] == "observation" and r["body"].get("type") == "intel.report":
        assert r["body"]["data"]["title"] == d["summary"], "title not byte-identical"
        assert r["body"]["data"]["summary"] == d["description"], "summary not byte-identical"

json.dump(bundle, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
print("bundle: %d records (1 source + 1 run + 1 intel.report, "
      "no new intel.behavior)" % len(bundle_records), file=sys.stderr)
