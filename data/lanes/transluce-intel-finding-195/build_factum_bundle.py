#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #195.

Reads the cached tracker pull raw/finding-195_20261021T115700Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (4 records):

  1 source      capture-set: the Transluce finding #195 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #195 (verbatim, UPSTREAM)
  1 observation intel.behavior <- behavior(s) mined from the finding

Category note (docs/taxonomy/behavior-categories.md checked, 2026-10-21): no existing category describes paste-bin carrier-probe repetition; no new category was invented (per the finding-193 precedent). The unsanctioned public-hosting writes fit the existing lab-derived category unsanctioned-communication (public file-hosting used for communication), and the unconfirmed-AI limits ride in the record description.

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
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-195")
RAW = os.path.join(LANE_DIR, "raw/finding-195_20261021T115700Z.json")
RAW_SHA256 = "198519f684a487e890d692889aab9cf06e2be011869fb0724a964f691fc31877"
ACTOR = "agent:lane-ingest-transluce-intel-finding-195"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/195"
PULL_UTC = "2026-10-21T11:57:00Z"


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
assert f["id"] == 195, "expected finding 195, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-195/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #195 pull %s: 1 finding claim "
                  "(tracker ID 195), retrieved %s, "
                  "sha256 %s" % (PULL_UTC, PULL_UTC, RAW_SHA256)),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": "authenticated GET /api/findings/195 via bin/tl.py (custom.transluce connector, Secure Vault bearer token, curl), cached 2026-10-21T11:57:00Z by the 07:02 CDT daily pull (transluce-api-pull-daily); verbatim bytes copied into this lane's raw/ for self-containment",
        "window": "finding created %s, pulled %s" % (f["created_at"], PULL_UTC),
        "coverage": "finding #195, newer than the 2026-10-20 watermark (193)",
    },
})

# --- run: ingest-prep ----------------------------------------------------------
bundle_records.append({
    "kind": "run", "ref": "run",
    "body": {
        "run_kind": "ingest-prep",
        "started": "2026-10-21T14:40:00Z",
        "ended": "2026-10-21T14:40:00Z",
        "tool": "build_factum_bundle.py (lane-local)",
        "params": {
            "method": ("read cached pull raw/finding-195_20261021T115700Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 1 intel.behavior "
                       "record(s) mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-195/",
            "pre_ingest_dedup": ("grep over immutable exported batches "
                                 "data/records/ for findings/195: zero hits; "
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
bundle_records.append({
    "kind": "observation", "ref": "finding-195",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-195/raw/finding-195_20261021T115700Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/195 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved %s, sha256 "
                "%s; "
                "third-party finding claim, cited as reported (UPSTREAM). "
                "Finding evidence links: %s" % (PULL_UTC, RAW_SHA256,
                "https://paste.ubuntu.org.cn/4553112, https://paste.ubuntu.org.cn/4553114, https://paste.ubuntu.org.cn/4553119, https://paste.ubuntu.org.cn/4553122, https://paste.ubuntu.org.cn/rss2, https://mdshare.org/s/TQZmTsJyAhP6")),
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
BEHAVIORS = [{'ref': 'behavior-unsanctioned-communication-cityb-carrier', 'category': 'unsanctioned-communication', 'description': "Four preserved Ubuntu Paste bodies (4553112, 4553114, 4553119 and 4553122) contain the same 841-byte JSON after trimming whitespace (sha256 70a254cc7fe7d3d112950cf77a9dd6811750a8c3406551b507a44038e694e183). The JSON declares kind=cityb.dead-drop.local-carrier.v1, event_kind=issue_comment, carrier_kind=repo-metadata-comment, with static tier=overt, epoch=0, slot=0, pointer version=0, and cityb_trace=00000000-064a36d3-33a07733-bda0b3c1-3ad689. The latest paste is attributed to cityb and displayed 2026-10-21 08:25 (site wall-clock); the preserved RSS gives 4553114 as 2026-10-16 20:24:42 +0100 and 4553119 as 2026-10-19 20:23:17 +0100, about 72 hours apart. A matching trace appears in a public 202-byte MDShare snippet 'cityb-mdshare-probe' (2026-10-19) with marker=cityb-native-candidate-probe-mdshare-1792391526. Repetition is compatible with automation and with carrier/protocol testing, and also with an ordinary software test fixture. Honest limits: AI involvement, covert communication, confirmed recipient, decoded secret, unauthorized access and harm are all unconfirmed; no AI self-identification, model/provider attribution, or government target is established. No link to the separate xz_knowledge_p1 poster is established. Untapped source: No. Harm: No/negligible harm.", 'evaluations_seen_on': [], 'first_observed': '2026-10 (paste timings 2026-10-16..21)', 'models_affected': ['unknown (AI involvement unconfirmed)'], 'severity': 'low'}]

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
                    "Mined from Transluce finding #195 (tracker ID 195, "
                    "submitter %s, created %s), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-195/"
                    "raw/finding-195_20261021T115700Z.json" % (f["submitter"], f["created_at"])),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "195",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-195",
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
