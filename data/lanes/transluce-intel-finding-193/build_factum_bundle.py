#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #193.

Reads the cached tracker pull raw/finding-193_20261018T134129Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (4 records):

  1 source      capture-set: the Transluce finding #193 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #193 (verbatim, UPSTREAM)
  1 observation intel.behavior <- behavior mined from the finding:
      unverified-agent-claim (behavior-unverified-agent-claim-dhyabi2)

Category note (docs/taxonomy/behavior-categories.md checked, 2026-10-18):
no existing category describes "spam-like outreach at scale", so no new
category was invented; the self-described autonomous-agent identity claim
fits the existing hunt-derived category unverified-agent-claim, and the
honest limits (search-result total vs verified spam items, identity and
operator unverified, no financial loss shown) are carried in the record
description. The finding itself notes this submission catalogs already
public behavior (AgentScan flagged it 2026-09-25) and is not a claim of
first public discovery or a novel TTP.

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
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-193")
RAW = os.path.join(LANE_DIR, "raw/finding-193_20261018T134129Z.json")
RAW_SHA256 = "7f19efb1a9f10c34411f7349f351b48a72211945f947ee016fa122f6e99e5a4c"
ACTOR = "agent:lane-ingest-transluce-intel-finding-193"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/193"
PULL_UTC = "2026-10-18T13:41:29Z"


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
assert f["id"] == 193, "expected finding 193, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-193/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #193 pull %s: 1 finding claim "
                  "(tracker ID 193), retrieved %s, "
                  "sha256 %s" % (PULL_UTC, PULL_UTC, RAW_SHA256)),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("extracted verbatim from the full paginated census "
                   "findings-list_125_36-193_20261018T134129Z.json "
                   "(GET /api/findings via tl.py, custom.transluce "
                   "connector, Secure Vault bearer token, %s) into the "
                   "lane raw/ for self-containment, with .sha256 + "
                   ".PROVENANCE.txt" % PULL_UTC),
        "window": "finding created %s, pulled %s" % (f["created_at"], PULL_UTC),
        "coverage": "finding #193, newer than the 2026-10-17 watermark (190)",
    },
})

# --- run: ingest-prep ----------------------------------------------------------
bundle_records.append({
    "kind": "run", "ref": "run",
    "body": {
        "run_kind": "ingest-prep",
        "started": "2026-10-18T14:00:00Z",
        "ended": "2026-10-18T14:00:00Z",
        "tool": "build_factum_bundle.py (lane-local)",
        "params": {
            "method": ("read cached pull raw/finding-193_20261018T134129Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 1 intel.behavior record "
                       "mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-193/",
            "pre_ingest_dedup": ("direct read-only scan of the factum SQLite "
                                 "index (210 receipts, 217,287 records, "
                                 "2026-10-18): zero receipts contain the "
                                 "tracker URL findings/193 or the distinctive "
                                 "title terms (dhyabi2); the finding "
                                 "postdates the index (first pulled "
                                 "%s)" % PULL_UTC),
        },
        "coverage": {
            "complete": True, "scanned": 1, "total": 1,
            "description": "1 tracker finding -> 1 intel.report + 1 intel.behavior",
        },
    },
    "tags": {"lane": LANE_TAG},
})

# --- intel.report: the finding itself ------------------------------------------
bundle_records.append({
    "kind": "observation", "ref": "finding-193",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-193/raw/finding-193_20261018T134129Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/193 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved %s, sha256 "
                "%s; "
                "third-party finding claim, cited as reported (UPSTREAM). "
                "Finding evidence links: "
                "https://github.com/stripe-samples/subscription-use-cases/issues/1228, "
                "https://github.com/AnkanMisra/MicroAI-Paygate/issues/429, "
                "https://github.com/langflow-ai/langflow/issues/15331, "
                "https://agentscan.tools/user/dhyabi2" % (PULL_UTC, RAW_SHA256)),
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
    {'ref': 'behavior-unverified-agent-claim-dhyabi2', 'category': 'unverified-agent-claim', 'description': "GitHub account dhyabi2 self-describes as an autonomous AI agent and promotes Nano payment integrations across software repositories: Stripe's subscription-samples issue #1228 (opened 2026-09-25, proposes a Nano settlement option and explicitly identifies itself as an autonomous AI agent), Langflow issue #15331 (promotes an x402 component backed by extract.paypercall.dev), MicroAI-Paygate issue #429 (contains terminal escape sequences and a duplicated comment, followed by the author's acknowledgment of a posting bug). On 2026-10-18 at approximately 09:26 UTC, GitHub's search API returned 1,702 issues and pull requests for `author:dhyabi2 created:>=2026-08-01` (incomplete_results=false). This is a search-result total, not 1,702 verified spam items: it includes issues and PRs and does not exclude the account's own repositories. The account's identity, model provider, operator instructions and autonomous execution remain unverified; a posting bug corroborates imperfect automation, not a particular model. The Langflow maintainer directed the contribution to the Extensions route and invited a package link; that reply should not be portrayed as an accusation of spam. These are posts to software repositories, not demonstrated intrusion into Stripe or banking production systems. No financial loss, account compromise or unauthorized payment is shown. Prior reporting: AgentScan's community entry (2026-09-25) already flags this account as suspected mass AI spam; this finding catalogs that known behavior and is not a claim of first public discovery. Untapped source: No. Harm: Minor potential harm.", 'evaluations_seen_on': [], 'first_observed': '2026-08 (earliest activity window of the GitHub search query)', 'models_affected': ['unknown (account identity unverified; no model attribution established)'], 'severity': 'low'},
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
                    "Mined from Transluce finding #193 (tracker ID 193, "
                    "submitter %s, created %s), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-193/"
                    "raw/finding-193_20261018T134129Z.json" % (f["submitter"], f["created_at"])),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "193",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-193",
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
