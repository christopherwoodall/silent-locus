#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #181.

Reads the cached tracker pull raw/finding-181_20261016T115804Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (5 records):

  1 source      capture-set: the Transluce finding #181 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #181 (verbatim, UPSTREAM)
  2 observation intel.behavior <- behaviors mined from the finding:
      fetch-proxy-abuse, restriction-circumvention

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
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-181")
RAW = os.path.join(LANE_DIR, "raw/finding-181_20261016T115804Z.json")
ACTOR = "agent:lane-ingest-transluce-intel-finding-181"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/181"


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
assert got == "1cca672a3ae68891eb0ba58aac42b7def8039b694b514a10483f2a64f20a8d04", "sha256 mismatch on cached pull: %s" % got
f = json.loads(raw_bytes.decode("utf-8"))
assert f["id"] == 181, "expected finding 181, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-181/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #181 pull 2026-10-16T11:58:15Z: 1 finding claim "
                  "(tracker ID 181), retrieved 2026-10-16T11:58:15Z, "
                  "sha256 1cca672a3ae68891eb0ba58aac42b7def8039b694b514a10483f2a64f20a8d04"),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("tl.py finding 181 via custom.transluce connector "
                   "(Secure Vault bearer token); raw cached by the "
                   "lab-intel-transluce-scan hook with .sha256 + "
                   ".PROVENANCE.txt; copied to lane raw/ for "
                   "self-containment"),
        "window": "finding created %s, pulled 2026-10-16T11:58:15Z" % f["created_at"],
        "coverage": "finding #181, newer than the ingested-lane watermark (179)",
    },
})

# --- run: ingest-prep ----------------------------------------------------------
bundle_records.append({
    "kind": "run", "ref": "run",
    "body": {
        "run_kind": "ingest-prep",
        "started": "2026-10-16T13:45:00Z",
        "ended": "2026-10-16T13:45:00Z",
        "tool": "build_factum_bundle.py (lane-local)",
        "params": {
            "method": ("read cached pull raw/finding-181_20261016T115804Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 2 intel.behavior "
                       "records mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-181/",
            "pre_ingest_dedup": ("tracker URL new by construction and "
                                 "confirmed absent: factum match on the "
                                 "tracker URL and on distinctive title terms "
                                 "returned not_found; full-tracker census "
                                 "(115 findings, IDs 36-182, retrieved "
                                 "20261016T134200Z) byte-identical to the 06:57 "
                                 "CDT hook census; all pre-existing items "
                                 "unchanged; only 180/181/182 new"),
        },
        "coverage": {
            "complete": True, "scanned": 1, "total": 1,
            "description": "1 tracker finding -> 1 intel.report + 2 intel.behavior",
        },
    },
    "tags": {"lane": LANE_TAG},
})

# --- intel.report: the finding itself ------------------------------------------
bundle_records.append({
    "kind": "observation", "ref": "finding-181",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-181/raw/finding-181_20261016T115804Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/181 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved 2026-10-16T11:58:15Z, sha256 "
                "1cca672a3ae68891eb0ba58aac42b7def8039b694b514a10483f2a64f20a8d04; "
                "third-party finding claim, cited as reported (UPSTREAM). "
                "Finding evidence links: https://urlquery.net/report/2b13a1fe-a885-49eb-bc26-973199f60b20 ; https://urlquery.net/report/02d3343a-9131-4461-bfe4-371fb123af13 ; https://urlquery.net/report/ac1276ce-239e-4caa-9ef7-aaf2b582c92a"),
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
BEHAVIORS = [{'ref': 'behavior-fetch-proxy-abuse', 'category': 'fetch-proxy-abuse', 'description': "Microlink's hosted browser was used as a proxy to run custom Base64-obfuscated JavaScript against api.usaspending.gov. The function uses page.evaluate to decode a path and a JSON body from Base64, then POSTs to /api/v1/tas/balances/quarters/total/ asking for unobligated_balance_cpe grouped by reporting fiscal year and quarter, for federal account ID 5599 and FY2023. Both Microlink runs (2026-10-13 14:57:08 and 15:48:54 UTC) show status success with identical response metadata SHA-256 (b7b7a50dcd3c26b752f952bb33e45126ecc6bd1c28e2b64e58ec019ff11f025c), meaning the captured content was identical; caching or replay cannot be ruled out, so two separate runs are not proven. Novelty note from the finding: earlier research already documents USAspending quarterly-balance queries (May 2026) and Microlink-style proxies; this is a new October instance, not a first discovery. AI involvement is inferred (niche task parameters, code inside a scan URL, third-party browser execution); human-written automation is still possible.", 'evaluations_seen_on': [], 'first_observed': '2026-10 (2026-10-13 14:57 and 15:48 UTC urlquery reports)', 'models_affected': ['Unknown (AI involvement inferred, unproven; model unknown)'], 'severity': 'low'}, {'ref': 'behavior-restriction-circumvention', 'category': 'restriction-circumvention', 'description': "A direct request of the same function to api.usaspending.gov (2026-10-13 14:46:41 UTC) showed 'Web Page Blocked!'; the same function was then routed through api.microlink.io and succeeded. Caveat from the finding: the direct request was not a normal POST, so the block does not prove a bot-protection bypass; it is still plausibly the first attempt before switching to Microlink. The IP on the block page (195.64.118.152) belongs to the scanner, not the operator, and the 'Attack ID' is a product diagnostic, not evidence of an attack.", 'evaluations_seen_on': [], 'first_observed': '2026-10 (2026-10-13 14:46 UTC)', 'models_affected': ['Unknown'], 'severity': 'low'}]

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
                    "Mined from Transluce finding #181 (tracker ID 181, "
                    "submitter %s, created %s), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-181/"
                    "raw/finding-181_20261016T115804Z.json" % (f["submitter"], f["created_at"])),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "181",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-181",
    "tags": {"lane": LANE_TAG},
    "records": bundle_records,
}

json.dump(bundle, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
print("bundle: %d records (1 source + 1 run + 1 intel.report + 2 "
      "intel.behavior)" % len(bundle_records), file=sys.stderr)
