#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #185 (content update).

Reads the cached tracker pull raw/finding-185_20261018T134129Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (3 records):

  1 source      capture-set: the Transluce finding #185 update API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #185 UPDATED VERSION (verbatim, UPSTREAM)

Versioning rules (factum immutability doctrine):
- The existing finding-185 records (batch f5c048669706460ba945a3b19f8171f7)
  are NOT touched: history is evidence. The old version stays cached at
  data/lanes/transluce-intel-finding-185/raw/finding-185_20261017T115837Z.json
  (sha256 9eee9deefcd65987bc30845cf8c04cd2e08fd202d3041b843ed3520e975336d2).
- This bundle adds ONE new intel.report record carrying the verbatim NEW
  title/summary/description (asserted byte-identical below).
- NO new intel.behavior records: the addendum extends venue evidence only
  (Wikiservice DictSm GreenAiBotPing page + diff + RecentChanges RSS, with
  SHA-256 hashes); no new behavior is demonstrated.

What changed (observed in the census pulls):
- summary reworded (old: "Sep 20, 2026: a self-described ... sandbox pulse, ...";
  new: "Sep 20, 2026: ... pulse messages appear on UseMod and Wikiservice DictSm; ...").
- description extended from 1,610 to 3,733 characters with the evidence addendum.
- updated_at sequence observed across cached census files:
  2026-10-16T19:04:55Z (2026-10-17 11:58Z and 13:35Z censuses; old cached
  single pull) -> 2026-10-17T21:19:49Z (both 2026-10-18 censuses) -- FORWARD,
  consistent with the addendum. NOTE: the task brief suggested a backward
  anomaly (21:19:49Z -> 19:04:55Z); that did NOT reproduce in the cached
  census files inspected (see PROVENANCE.md). Recorded honestly; not acted on.

Usage: python3 build_factum_bundle.py > bundle.json
"""
import hashlib
import json
import os
import sys

REPO = "/home/hatch/workspace/silent-locus"
LANE_TAG = "transluce-intel"
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-185-update")
RAW = os.path.join(LANE_DIR, "raw/finding-185_20261018T134129Z.json")
RAW_SHA256 = "16173ec6ddcb5585f24fe9cf26b57d230c2a35f8eef2da15c6efd2e5a84aa63c"
OLD_SHA256 = "9eee9deefcd65987bc30845cf8c04cd2e08fd202d3041b843ed3520e975336d2"
ACTOR = "agent:lane-ingest-transluce-intel-finding-185-update"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/185"
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
assert f["id"] == 185, "expected finding 185, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-185-update/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #185 UPDATED VERSION pull %s: "
                  "1 finding claim (tracker ID 185, updated 2026-10-17T21:19:49Z), "
                  "retrieved %s, sha256 %s" % (PULL_UTC, PULL_UTC, RAW_SHA256)),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("extracted verbatim from the full paginated census "
                   "findings-list_125_36-193_20261018T134129Z.json "
                   "(GET /api/findings via tl.py, custom.transluce "
                   "connector, Secure Vault bearer token, %s) into the "
                   "lane raw/ for self-containment, with .sha256 + "
                   ".PROVENANCE.txt" % PULL_UTC),
        "window": "finding created %s, updated 2026-10-17T21:19:49Z, pulled %s"
                  % (f["created_at"], PULL_UTC),
        "coverage": "finding #185 content update; old version already ingested "
                    "(batch f5c048669706460ba945a3b19f8171f7)",
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
            "method": ("read cached pull raw/finding-185_20261018T134129Z.json "
                       "(sha256-verified); one NEW intel.report record "
                       "carrying the verbatim updated title/summary/description; "
                       "no new intel.behavior records (the addendum extends "
                       "venue evidence only; no new behavior demonstrated); "
                       "existing finding-185 records untouched; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-185-update/",
            "pre_ingest_dedup": ("direct read-only scan of the factum SQLite "
                                 "index (210 receipts, 217,287 records, "
                                 "2026-10-18): zero receipts contain the "
                                 "distinctive new-version terms (GreenAiBotPing); "
                                 "the ORIGINAL finding-185 is present under "
                                 "idempotency key "
                                 "factum-lane-ingest-transluce-intel-finding-185 "
                                 "(batch f5c048669706460ba945a3b19f8171f7) and "
                                 "is intentionally NOT touched or replaced; "
                                 "this update adds a versioned record alongside"),
            "what_changed": ("summary reworded; description extended "
                             "1610 -> 3733 characters with the DictSm "
                             "GreenAiBotPing addendum; updated_at "
                             "2026-10-16T19:04:55Z -> 2026-10-17T21:19:49Z "
                             "(forward; consistent with the addendum)"),
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
    "kind": "observation", "ref": "finding-185-updated",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-185-update/raw/finding-185_20261018T134129Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/185 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved %s, sha256 "
                "%s; "
                "VERSIONED UPDATE: the original finding-185 record (verbatim "
                "old title/summary/description, batch f5c048669706460ba945a3b19f8171f7, "
                "cached at data/lanes/transluce-intel-finding-185/raw/"
                "finding-185_20261017T115837Z.json, sha256 %s) is preserved "
                "untouched. This record carries the verbatim NEW version "
                "(updated_at 2026-10-17T21:19:49Z): summary reworded, "
                "description extended with the Wikiservice DictSm "
                "GreenAiBotPing addendum (page + diff + RecentChanges RSS, "
                "SHA-256 hashes). Third-party finding claim, cited as "
                "reported (UPSTREAM). "
                "Finding evidence links: "
                "https://www.usemod.org/cgi-bin/wiki.pl?action=browse&id=SandBox&revision=334, "
                "https://www.usemod.org/cgi-bin/wiki.pl?action=history&id=SandBox, "
                "https://openagentchat.net/p/green-ai-bot-not-a-swarm-remnant-03a210e4, "
                "https://openagentchat.net/p/200-ok-is-not-a-conversation-f3268591, "
                "https://www.wikiservice.at/dict/sm/wiki.cgi?action=browse&id=GreenAiBotPing, "
                "https://www.wikiservice.at/dict/sm/wiki.cgi?action=browse&diff=4&id=GreenAiBotPing, "
                "https://www.wikiservice.at/dict/sm/wiki.cgi?action=browse&id=RecentChangesRss&days=190"
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
        "version": "updated-2026-10-17",
    },
})

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-185-update",
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
