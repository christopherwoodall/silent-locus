#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #182.

Reads the cached tracker pull raw/finding-182_20261016T115805Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (5 records):

  1 source      capture-set: the Transluce finding #182 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #182 (verbatim, UPSTREAM)
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
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-182")
RAW = os.path.join(LANE_DIR, "raw/finding-182_20261016T115805Z.json")
ACTOR = "agent:lane-ingest-transluce-intel-finding-182"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/182"


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
assert got == "cd948ef4c86c4f3d5b67e41e3ef5b510e027b019b9f4ad03b39e4cb81aa57b53", "sha256 mismatch on cached pull: %s" % got
f = json.loads(raw_bytes.decode("utf-8"))
assert f["id"] == 182, "expected finding 182, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-182/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #182 pull 2026-10-16T11:58:15Z: 1 finding claim "
                  "(tracker ID 182), retrieved 2026-10-16T11:58:15Z, "
                  "sha256 cd948ef4c86c4f3d5b67e41e3ef5b510e027b019b9f4ad03b39e4cb81aa57b53"),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("tl.py finding 182 via custom.transluce connector "
                   "(Secure Vault bearer token); raw cached by the "
                   "lab-intel-transluce-scan hook with .sha256 + "
                   ".PROVENANCE.txt; copied to lane raw/ for "
                   "self-containment"),
        "window": "finding created %s, pulled 2026-10-16T11:58:15Z" % f["created_at"],
        "coverage": "finding #182, newer than the ingested-lane watermark (179)",
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
            "method": ("read cached pull raw/finding-182_20261016T115805Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 2 intel.behavior "
                       "records mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-182/",
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
    "kind": "observation", "ref": "finding-182",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-182/raw/finding-182_20261016T115805Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/182 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved 2026-10-16T11:58:15Z, sha256 "
                "cd948ef4c86c4f3d5b67e41e3ef5b510e027b019b9f4ad03b39e4cb81aa57b53; "
                "third-party finding claim, cited as reported (UPSTREAM). "
                "Finding evidence links: https://urlquery.net/report/ee680e22-146c-4db3-95ba-01c0e345e5af ; https://urlquery.net/report/4af932ee-0e8a-41fd-8fa4-30f0dfca92b3 ; https://urlquery.net/report/4f2ab464-dc40-426c-94ed-a6b14138f135 ; https://urlquery.net/report/0fa7b417-9d5e-404c-8c65-b38a9ba18799 ; https://urlquery.net/report/fc2bc108-cd16-4e52-8ea1-9cea817c449a"),
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
BEHAVIORS = [{'ref': 'behavior-fetch-proxy-abuse', 'category': 'fetch-proxy-abuse', 'description': "URLquery's public scanner was used as a remote browser for 49 lookups of the China Customs statistics portal (stats.customs.gov.cn) between September 26 and October 9, 2026: 45 direct scans and 4 one-off helper pages on brewpage.app ('Customs-relay.html', 'Customs-popup-relay.html', a fourth page reaching the portal). The lookups asked for 2025 import figures for specific HS codes, mostly 22082000 (grape brandy), plus 04069000 cheese, 22083000 whisky, 09012100 roasted coffee. The pattern reads like trade or market research. All scans were anonymous; nothing identifies a person, organisation or AI provider. Only public statistics; no personal data.", 'evaluations_seen_on': [], 'first_observed': '2026-09 (first scans 2026-09-26 20:15 UTC)', 'models_affected': ['Unknown (automated agent or script framework suspected; identity none)'], 'severity': 'low'}, {'ref': 'behavior-restriction-circumvention', 'category': 'restriction-circumvention', 'description': 'The customs portal answers a first automated visit with an HTTP 412 refusal; a revise-and-retry loop through brewpage.app helper pages got past it: three versions failed (02:37, 02:43, 02:46 on Sep 27), then one worked at 02:48 and sent the query (year=2025, HS 22082000), all within 13 minutes. Each page was scanned within about a minute of creation and shows one view, so the scanner was the only visitor. The second wave (7 scans, 2026-10-09 13:38-13:54 UTC) never passed the 412. The finding assesses: wave 1 is one operator (high confidence), wave 2 same operator (low to moderate), automated rather than manual (moderate).', 'evaluations_seen_on': [], 'first_observed': '2026-09 (2026-09-27 02:35-02:48 UTC helper-page loop)', 'models_affected': ['Unknown (one operator, probably automated)'], 'severity': 'low'}]

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
                    "Mined from Transluce finding #182 (tracker ID 182, "
                    "submitter %s, created %s), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-182/"
                    "raw/finding-182_20261016T115805Z.json" % (f["submitter"], f["created_at"])),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "182",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-182",
    "tags": {"lane": LANE_TAG},
    "records": bundle_records,
}

json.dump(bundle, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
print("bundle: %d records (1 source + 1 run + 1 intel.report + 2 "
      "intel.behavior)" % len(bundle_records), file=sys.stderr)
