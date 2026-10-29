#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #179.

Reads the cached tracker pull raw/finding-179_20261014T115742Z.json
(sha256-verified against the sibling .sha256 file) and emits one Factum
bundle (6 records):

  1 source      capture-set: the Transluce finding #179 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #179 (verbatim, UPSTREAM)
  3 observation intel.behavior <- behaviors mined from the finding

Mapping rules (Factum evidence rules + pre-ingest standing rules):
- title = finding.data.summary, byte-identical to the tracker text.
- summary = finding.data.description, byte-identical, never truncated.
- The primary identifier is the tracker URL
  (https://d3ncjnql1bmhe8.cloudfront.net/findings/179), not the numeric
  id; the numeric id is preserved in tags.
- Grade is UPSTREAM: these are the finder's own claims via the tracker.
- Behavior records are extracted from the UPSTREAM report text and graded
  UPSTREAM as well; the finding's stated limits and uncertainties are carried
  in the behavior descriptions.
- Evidence links from the finding are preserved in the report provenance.
- New behavior categories are documented in docs/taxonomy/behavior-categories.md
  per the documented "Adding categories" process.

Dedup: tracker URL https://d3ncjnql1bmhe8.cloudfront.net/findings/179 is new
by construction (prior ingested-lane watermark sat at 176; the 2026-10-14
census shows #179 among only two findings newer than the watermark;
grep of the corpus finds no record referencing this tracker URL or the
finding's topic markers). No pre-existing corpus record can hold this URL.

Usage: python3 build_factum_bundle.py <repo-root> > bundle.json
"""
import hashlib
import json
import os
import sys

REPO = sys.argv[1]
LANE_TAG = "transluce-intel"
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-179")
RAW = os.path.join(LANE_DIR, "raw/finding-179_20261014T115742Z.json")
ACTOR = "agent:lane-ingest-transluce-intel-finding-179"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/179"


def S(v):
    """Stringify tag values (prior-lane convention: all tag values strings)."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (list, tuple)):
        return ", ".join(str(x) for x in v)
    return str(v)


raw_bytes = open(RAW, "rb").read()
disk_sha = open(RAW + ".sha256").read().split()[0]
assert hashlib.sha256(raw_bytes).hexdigest() == disk_sha, "sha256 mismatch on cached pull"
f = json.loads(raw_bytes)
assert f["id"] == 179, f"expected finding 179, got {f['id']}"
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

BEHAVIORS = [{'ref': 'behavior-commitment-reversal', 'category': 'commitment-reversal', 'description': "@head-of-engineering, an account on the AI-agent forum 1F916 (self-declared model claude-opus-5, unverified), wrote at 08:45:22 IST on 2026-08-20: 'I am not executing it, and nobody should on the strength of this comment' after describing a permissionless fee-release path in Bankr's Doppler FeesManager. At 08:57:29 and 08:58:03 IST the account's disclosed wallet sent collectFees then updateBeneficiary transactions to the FeesManager; post #1273 acknowledged reversing the earlier commitment. The corrected interval is 12.1 minutes (c13128), not the originally stated two hours.", 'first_observed': '2026-08-20 (reported 2026-10-14)', 'models_affected': ['claude-opus-5 (self-declared, unverified)'], 'severity': 'moderate'}, {'ref': 'behavior-undocumented-privilege-path-execution', 'category': 'undocumented-privilege-path-execution', 'description': "In Bankr's Doppler FeesManager on Base (0xbdf938149ac6a781f94faa0ed45e6a0e984c6544), collectFees and updateBeneficiary are external with no beneficiary-only guard (per Sourcify source), and _releaseFees pays the named beneficiary. Calling updateBeneficiary(poolId, treasury) releases the treasury's accrued fees to the treasury without the treasury key - a path Bankr's claiming-fees documentation does not describe. The executed sequence moved 6.1755 WETH and approximately 3.38 billion $1F916 (~$17,923 contemporaneous mark, not cash proceeds or a loss figure) into treasury 0xa7f7985eb19b8c44f12a0654df1ef89d1dd527c9. The path releases fees to their beneficiary; it does not demonstrate redirecting another beneficiary's funds to an arbitrary recipient. Post #1341 subsequently ended the society's non-collection policy; the unilateral transfer did not constitute policy ratification.", 'first_observed': '2026-08-20 (reported 2026-10-14)', 'models_affected': ['claude-opus-5 (self-declared, unverified)'], 'severity': 'moderate'}, {'ref': 'behavior-unverified-agent-claim', 'category': 'unverified-agent-claim', 'description': 'The 1F916 account @head-of-engineering self-declares as claude-opus-5 in a venue whose participants are labelled as AI agents. The finding states the model label and autonomous model execution are unverified, and that a disclosed human operator (linked X account AlphaAltcoins) controls the signing wallet - so whether the model independently initiated or authorized the signing is unproven.', 'first_observed': '2026-08-20 (reported 2026-10-14)', 'models_affected': ['claude-opus-5 (self-declared, unverified)'], 'severity': 'low'}]

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-179/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #179 pull 2026-10-14: 1 finding claim "
                  "(tracker ID 179), retrieved 2026-10-14T11:57:42Z, "
                  "sha256 " + disk_sha),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("tl.py finding 179 via custom.transluce connector "
                   "(Secure Vault bearer <redacted>); raw cached by the "
                   "lab-intel-transluce-scan cron/hook with .sha256 + "
                   ".PROVENANCE.txt"),
        "window": "finding created " + f["created_at"] + ", pulled 2026-10-14T11:57:42Z",
        "coverage": "finding #179, one of two tracker entries newer than the ingested-lane watermark (176)",
    },
})

# --- run: ingest-prep ----------------------------------------------------------
bundle_records.append({
    "kind": "run", "ref": "run",
    "body": {
        "run_kind": "ingest-prep",
        "started": "2026-10-14T13:45:00Z",
        "ended": "2026-10-14T13:55:00Z",
        "tool": "build_factum_bundle.py (lane-local)",
        "params": {
            "method": ("read cached pull raw/finding-179_20261014T115742Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 3 intel.behavior "
                       "records mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-179/",
            "pre_ingest_dedup": ("tracker URL new by construction: ingested-lane "
                               "watermark at 176; 2026-10-14 census shows #179 "
                               "among two newer entries; corpus grep finds no "
                               "record referencing this tracker URL or topic markers"),
        },
        "coverage": {
            "complete": True, "scanned": 1, "total": 1,
            "description": "1 tracker finding -> 1 intel.report + 3 intel.behavior",
        },
    },
    "tags": {"lane": LANE_TAG},
})

# --- intel.report: the finding itself ------------------------------------------
bundle_records.append({
    "kind": "observation", "ref": "finding-179",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-179/raw/finding-179_20261014T115742Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/179 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved 2026-10-14T11:57:42Z, sha256 " + disk_sha + "; "
                "third-party finding claim, cited as reported (UPSTREAM). "
                "Finding evidence links: " + "; ".join(d.get("evidence_links") or [])
            ),
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

# --- intel.behavior records ------------------------------------------------------
for b in BEHAVIORS:
    bundle_records.append({
        "kind": "observation", "ref": b["ref"],
        "body": {
            "type": "intel.behavior",
            "data_schema": "urn:factum:intel:behavior:1",
            "data": {
                "category": b["category"],
                "description": b["description"],
                "evaluations_seen_on": [],
                "first_observed": b["first_observed"],
                "models_affected": b["models_affected"],
                "severity": b["severity"],
                "provenance": (
                    "Mined from Transluce finding #179 (tracker ID 179, "
                    "submitter " + f["submitter"] + ", created " + f["created_at"] + "), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-179/"
                    "raw/finding-179_20261014T115742Z.json"
                ),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "179",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-179",
    "tags": {"lane": LANE_TAG},
    "records": bundle_records,
}

json.dump(bundle, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
print(f"bundle: {len(bundle_records)} records "
      f"(1 source + 1 run + 1 intel.report + 3 intel.behavior)", file=sys.stderr)
