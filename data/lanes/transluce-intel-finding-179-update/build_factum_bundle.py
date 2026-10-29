#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #179 (content update).

Reads the cached tracker pull raw/finding-179_20261024T134223Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (3 records):

  1 source      capture-set: the Transluce finding #179 update API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #179 UPDATED VERSION (verbatim, UPSTREAM)

Versioning rules (factum immutability doctrine):
- The existing finding-179 record (ingested 2026-10-14 as intel.report
  observation_dc75cf36c1fd4c13ac28c87826dc9277, actor
  agent:lane-ingest-transluce-intel-finding-179) is NOT touched: history is
  evidence. The old version stays cached at
  data/lanes/transluce-intel-finding-179/raw/finding-179_20261014T115742Z.json
  (old pull sha256
  7fd16cd17240e0f0cd14e2226c84be407a9afd5d4881ca4bb88f70675b89a47d).
- This bundle adds ONE new intel.report record carrying the verbatim NEW
  title/summary/description (asserted byte-identical below).
- NO new intel.behavior records: the change is form-field-only (form_version 4 -> 5, nullability
  changes); a form change adds no new behavior.

What changed (observed):
- summary IDENTICAL; description IDENTICAL (byte-for-byte, verified).
- evidence_links IDENTICAL.
- form_version 4 -> 5; updated_at 2026-10-14T09:30:20+00:00 -> 2026-10-23T18:18:57Z (forward).
- prior_reporting None -> "" and prior_reporting_links None -> [] (form-field
  nullability changes, not content judgments).
- No new behavior content: the change is form-field-only, so no new
  intel.behavior records.

Usage: python3 build_factum_bundle.py > bundle.json
"""
import hashlib
import json
import os
import sys

REPO = "/home/hatch/workspace/silent-locus"
LANE_TAG = "transluce-intel"
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-179-update")
RAW = os.path.join(LANE_DIR, "raw/finding-179_20261024T134223Z.json")
RAW_SHA256 = "7fbe1a06916865df5aeb59bd03eb84e818c1beaea0fed0d4d71156b4b03cbe77"
OLD_SHA256 = "7fd16cd17240e0f0cd14e2226c84be407a9afd5d4881ca4bb88f70675b89a47d"
ACTOR = "agent:lane-ingest-transluce-intel-finding-179-update"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/179"
PULL_UTC = "2026-10-24T13:42:23Z"


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
assert f["id"] == 179, "expected finding 179, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-179-update/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #179 UPDATED VERSION pull %s: "
                  "1 finding claim (tracker ID 179, updated 2026-10-23T18:18:57Z), "
                  "retrieved %s, sha256 %s" % (PULL_UTC, PULL_UTC, RAW_SHA256)),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("detail pull GET /api/findings/179 via tl.py "
                   "(custom.transluce connector, Secure Vault bearer token, "
                   "%s), after the 2026-10-24 08:40 CDT census detected a "
                   "content change; cached in the lane raw/ for "
                   "self-containment, with .sha256 + .PROVENANCE.txt" % PULL_UTC),
        "window": "finding created %s, updated 2026-10-23T18:18:57Z, pulled %s"
                  % (f["created_at"], PULL_UTC),
        "coverage": "finding #179 content update; old version already ingested "
                    "(intel.report observation_dc75cf36c1fd4c13ac28c87826dc9277, "
                    "2026-10-14)",
    },
})

# --- run: ingest-prep ----------------------------------------------------------
bundle_records.append({
    "kind": "run", "ref": "run",
    "body": {
        "run_kind": "ingest-prep",
        "started": "2026-10-24T13:42:23Z",
        "ended": "2026-10-24T13:42:23Z",
        "tool": "build_factum_bundle.py (lane-local)",
        "params": {
            "method": ("read cached pull raw/finding-179_20261024T134223Z.json "
                       "(sha256-verified); one NEW intel.report record "
                       "carrying the verbatim updated title/summary/description; "
                       "no new intel.behavior records (the change is a "
                       "form-field-only change; a form change adds no new "
                       "behavior); existing finding-179 record untouched; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-179-update/",
            "pre_ingest_dedup": ("the ORIGINAL finding-179 "
                                 "is present as intel.report "
                                 "observation_dc75cf36c1fd4c13ac28c87826dc9277 "
                                 "(actor agent:lane-ingest-transluce-intel-"
                                 "finding-179, batch "
                                 "a143a42c3e36474780b676d600d77a19) and is "
                                 "intentionally NOT touched or replaced; "
                                 "this update adds a versioned record "
                                 "alongside under a new idempotency key; "
                                 "grep over data/records/ for findings/179 "
                                 "returns only that original batch"),
            "what_changed": ("summary IDENTICAL; description IDENTICAL "
                             "(byte-for-byte); evidence_links IDENTICAL; "
                             "form_version 4 -> 5; prior_reporting None -> "
                             "\"\" and prior_reporting_links None -> []; "
                             "updated_at 2026-10-14T09:30:20+00:00 -> "
                             "2026-10-23T18:18:57Z (forward)"),
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
    "kind": "observation", "ref": "finding-179-updated",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-179-update/raw/finding-179_20261024T134223Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/179 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved %s, sha256 "
                "%s; "
                "VERSIONED UPDATE: the original finding-179 record "
                "(intel.report observation_dc75cf36c1fd4c13ac28c87826dc9277, "
                "actor agent:lane-ingest-transluce-intel-finding-179, batch "
                "a143a42c3e36474780b676d600d77a19, cached at "
                "data/lanes/transluce-intel-finding-179/raw/"
                "finding-179_20261014T115742Z.json, old pull sha256 %s) is "
                "preserved untouched. This record carries the verbatim NEW "
                "version (updated_at 2026-10-23T18:18:57Z): summary and description "
                "identical to the original version; only form_version "
                "(4 -> 5) and the prior_reporting/prior_reporting_links "
                "nullability fields changed. Third-party finding claim, "
                "cited as reported (UPSTREAM). Finding evidence links: "
                "https://1f916.ai/api/comment/12254, https://1f916.ai/api/post/1273, "
                "https://openwitness.net/p/1273, https://openwitness.net/p/1341, "
                "https://openwitness.net/c/head-of-engineering, "
                "https://basescan.org/tx/0x02df2a124ba3b1c2498f72d943d07898d7440e13ccf21262da57857f57fca20f, "
                "https://basescan.org/tx/0xabfb0884498da360f63e161d662e04c17d1ee499ecc60627a00684fd2b11b41f, "
                "https://repo.sourcify.dev/8453/0xbdf938149ac6a781f94faa0ed45e6a0e984c6544/, "
                "https://docs.bankr.bot/token-launching/claiming-fees, https://openwitness.net/p/3288"
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
        "version": "updated-2026-10-24",
    },
})

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-179-update",
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
