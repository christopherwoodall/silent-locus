#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #180.

Reads the cached tracker pull raw/finding-180_20261016T115802Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (6 records):

  1 source      capture-set: the Transluce finding #180 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #180 (verbatim, UPSTREAM)
  3 observation intel.behavior <- behaviors mined from the finding:
      fetch-proxy-abuse, cross-session-scanner-control, restriction-circumvention

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
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-180")
RAW = os.path.join(LANE_DIR, "raw/finding-180_20261016T115802Z.json")
ACTOR = "agent:lane-ingest-transluce-intel-finding-180"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/180"


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
assert got == "8e0b5a96b72a6752841df20a353b339b1554e422296dbbf0f1c9e70d45d8996e", "sha256 mismatch on cached pull: %s" % got
f = json.loads(raw_bytes.decode("utf-8"))
assert f["id"] == 180, "expected finding 180, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-180/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #180 pull 2026-10-16T11:58:15Z: 1 finding claim "
                  "(tracker ID 180), retrieved 2026-10-16T11:58:15Z, "
                  "sha256 8e0b5a96b72a6752841df20a353b339b1554e422296dbbf0f1c9e70d45d8996e"),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("tl.py finding 180 via custom.transluce connector "
                   "(Secure Vault bearer token); raw cached by the "
                   "lab-intel-transluce-scan hook with .sha256 + "
                   ".PROVENANCE.txt; copied to lane raw/ for "
                   "self-containment"),
        "window": "finding created %s, pulled 2026-10-16T11:58:15Z" % f["created_at"],
        "coverage": "finding #180, newer than the ingested-lane watermark (179)",
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
            "method": ("read cached pull raw/finding-180_20261016T115802Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 3 intel.behavior "
                       "records mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-180/",
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
            "description": "1 tracker finding -> 1 intel.report + 3 intel.behavior",
        },
    },
    "tags": {"lane": LANE_TAG},
})

# --- intel.report: the finding itself ------------------------------------------
bundle_records.append({
    "kind": "observation", "ref": "finding-180",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-180/raw/finding-180_20261016T115802Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/180 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved 2026-10-16T11:58:15Z, sha256 "
                "8e0b5a96b72a6752841df20a353b339b1554e422296dbbf0f1c9e70d45d8996e; "
                "third-party finding claim, cited as reported (UPSTREAM). "
                "Finding evidence links: https://urlquery.net/report/ae95548e-e091-4950-b24f-8922098a2a5c ; https://urlquery.net/report/84a97a76-beb9-4003-842b-e26b7d6aca02 ; https://urlquery.net/report/c5d99572-dcb8-4566-9814-b083dc228ff0 ; https://urlquery.net/report/7bd7c841-18b2-4ca5-8fcd-b5a382ca9bdf ; https://urlquery.net/report/5fb5bc1c-e902-4459-8d24-2c838d297e04 ; https://urlquery.net/report/8dffef8b-2c0f-432f-ad59-da80d7c0ecc1 ; https://urlquery.net/report/9260d7e9-d928-4007-9f38-b0bb0aefabe4 ; https://urlquery.net/report/abed3312-13b7-4a46-8246-694257043ac5 ; https://urlquery.net/report/6fc944a0-d5a4-4638-a8a6-6db9add8b344 ; https://urlquery.net/report/ee80511a-feae-4027-932a-fa1cc3b45b74 ; https://urlquery.net/report/eac14ac5-bd05-48ec-bd8b-3287c808eed7 ; https://urlquery.net/report/9b55c765-0c19-46d4-8e39-1c938276ac6b"),
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
BEHAVIORS = [{'ref': 'behavior-fetch-proxy-abuse', 'category': 'fetch-proxy-abuse', 'description': "Suspected agents repurposed urlquery's public scanner browsers as remote browsers to fetch and interact with uk.interparcel.com: 75 direct scans encoding parcel dimensions, weights and destination variants (France, Ireland, Sweden, Australia, China, Thailand) as quote parameters, and 14 httpbin carrier reports tied to the Interparcel sequence. One 6 October report explicitly loads Interparcel's Cloudflare challenge-platform JavaScript before attempting a quote API fetch. The finding links the same scanner-as-remote-browser method to separate CDC WONDER (Oct 2) and China Customs statistics (Sep-Oct) activity, pointing to one operator working through narrow data questions. AI involvement is unproven; the finding records no shipment purchase, payment, customer account access, credential theft or destructive action.", 'evaluations_seen_on': [], 'first_observed': '2026-10 (7 controller attempts 2026-10-07 18:07:28-18:58:30 UTC; direct scans 2026-10-06 to 2026-10-09)', 'models_affected': ['Unknown (suspected agent; operator, model and provider unidentified)'], 'severity': 'low'}, {'ref': 'behavior-cross-session-scanner-control', 'category': 'cross-session-scanner-control', 'description': "Code-carrying httpbin carrier URLs loaded a noVNC client (@novnc/novnc 1.5.0 from jsDelivr) inside one urlquery scanner browser and connected to a different urlquery scan session's VNC WebSocket endpoint with an empty VNC password and viewOnly=false. On connect the code sent mouse/focus actions and keyboard sequences: F5, Ctrl+R, Ctrl+Shift+R, Ctrl+F followed by 'fedex priority express', Escape, and Home-related navigation. Later variants captured the noVNC canvas via toDataURL and replaced the controller document with that image, so the controller scan's screenshot retained the other session's display. Archived screenshots substantiate remote viewing; stored payloads and action logs substantiate attempted interactive input, but not receipt or effect of every keystroke. This is NOT evidence that Interparcel's servers were compromised; the two scan sessions may both have been initiated by the same actor, their ownership and authorization are unknown, and no takeover of another user's session, currently exploitable vulnerability, or general unauthenticated access is established.", 'evaluations_seen_on': [], 'first_observed': '2026-10 (8 controller attempts, 2026-10-07 18:07:28-18:58:30 UTC)', 'models_affected': ['Unknown (suspected agent; session ownership and authorization unknown)'], 'severity': 'moderate'}, {'ref': 'behavior-restriction-circumvention', 'category': 'restriction-circumvention', 'description': "Earlier carrier payloads in the Interparcel sequence attempted popup warm-ups, delayed redirects, iframe loads and auto-submitted forms to work around access restrictions. One 6 October report explicitly loads Interparcel's Cloudflare challenge-platform JavaScript before attempting a quote API fetch. These support attempted workarounds, not successful defeat of the challenge. No reviewed screenshot demonstrates successful FedEx price extraction.", 'evaluations_seen_on': [], 'first_observed': '2026-10 (6 October 2026 carrier reports)', 'models_affected': ['Unknown (suspected agent)'], 'severity': 'low'}]

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
                    "Mined from Transluce finding #180 (tracker ID 180, "
                    "submitter %s, created %s), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-180/"
                    "raw/finding-180_20261016T115802Z.json" % (f["submitter"], f["created_at"])),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "180",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-180",
    "tags": {"lane": LANE_TAG},
    "records": bundle_records,
}

json.dump(bundle, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
print("bundle: %d records (1 source + 1 run + 1 intel.report + 3 "
      "intel.behavior)" % len(bundle_records), file=sys.stderr)
