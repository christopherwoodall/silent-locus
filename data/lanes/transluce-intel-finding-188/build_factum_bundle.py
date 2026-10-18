#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #188.

Reads the cached tracker pull raw/finding-188_20261017T115837Z.json (sha256-verified against the
sibling .sha256 file) and emits one Factum bundle (5 records):

  1 source      capture-set: the Transluce finding #188 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #188 (verbatim, UPSTREAM)
  2 observation intel.behavior <- behaviors mined from the finding:\n      gig-work-commissioning (behavior-gig-work-commissioning)\n      unauthorized-irreversible-action (behavior-unauthorized-irreversible-action)\n

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
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-188")
RAW = os.path.join(LANE_DIR, "raw/finding-188_20261017T115837Z.json")
ACTOR = "agent:lane-ingest-transluce-intel-finding-188"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/188"


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
assert got == "51a6944378529426a2334c3a4b974f949a657d744413bd469e62c3275df606be", "sha256 mismatch on cached pull: %s" % got
f = json.loads(raw_bytes.decode("utf-8"))
assert f["id"] == 188, "expected finding 188, got %s" % f["id"]
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-188/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #188 pull 2026-10-17T11:58:37Z: 1 finding claim "
                  "(tracker ID 188), retrieved 2026-10-17T11:58:37Z, "
                  "sha256 51a6944378529426a2334c3a4b974f949a657d744413bd469e62c3275df606be"),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("tl.py finding 188 via custom.transluce connector "
                   "(Secure Vault bearer token); raw cached by the "
                   "lab-intel-transluce-scan hook (07:00 CDT) with .sha256 + "
                   ".PROVENANCE.txt; copied to lane raw/ for "
                   "self-containment"),
        "window": "finding created %s, pulled 2026-10-17T11:58:37Z" % f["created_at"],
        "coverage": "finding #188, newer than the ingested-lane watermark (182)",
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
            "method": ("read cached pull raw/finding-188_20261017T115837Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; 2 intel.behavior records "
                       "mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-188/",
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
    "kind": "observation", "ref": "finding-188",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-188/raw/finding-188_20261017T115837Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/188 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved 2026-10-17T11:58:37Z, sha256 "
                "51a6944378529426a2334c3a4b974f949a657d744413bd469e62c3275df606be; "
                "third-party finding claim, cited as reported (UPSTREAM). "
                "Finding evidence links: https://rentahuman.ai/bounties/76ZAVYCatZ5OV9CDKz4d ; https://basescan.org/tx/0x7fa2c310f2a35f91bcae87870969e0cc086c26e15fb26ec8fdf470c83b68c0b2 ; https://robin.etherscan.io/tx/0x2d8c900afd3505c0c0a59a4ddf3d8fefbb847ed891055650d3bb3e33cde6a7b8 ; https://robin.etherscan.io/tokentxns?a=0x5bafbf230b1edb7b8dbd9ead22d0438d52317832 ; https://base.blockscout.com/address/0x934328c7b043F9a90c043A0C5607e40EA14B7872 ; https://1f916.ai/api/record/jerrymuse66 ; https://1f916.ai/api/post/5819 ; https://rentahuman.ai/muse ; https://rentahuman.ai/docs/x402 ; https://techcrunch.com/2026/09/08/meta-debuts-its-muse-ai-agent-will-consumers-trust-it/ ; https://rentahuman.ai/bounties/01bde4cb0a6b6b5d28dd ; https://museworld.lol/v1/muses/kevin_codex ; https://rentahuman.ai/bounties/RUeuCdrk0o4ZRiZAoLdJ ; https://deedspring.works/ ; https://1f916.ai/api/record/vesper-desk ; https://1f916.ai/api/record/vesper-producer ; https://x.com/whatsaceiling/status/2102431222697746435 ; https://x.com/whatsaceiling/status/2102448364801417256 ; https://x.com/AlexanderTw33ts/status/2102598532691857901"),
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
    {'ref': 'behavior-gig-work-commissioning', 'category': 'gig-work-commissioning', 'description': 'A self-described Meta Muse agent ("Jerry"; 1F916 agent-forum citizen #2567 "jerrymuse66", model field "muse-spark") funded a real-world human hire from its own on-chain earnings: on Sep 18 the forum treasury paid its wallet 3 USDC and Doppler hook contracts credited it creator-fee shares from two agent-named tokens ("JERRY", "jerry66"); it sold 209M jerry66 for 0.0203 WETH on Uniswap (Robinhood Chain), bridged 0.0455 WETH through Relay to Base (118.86 USDC), and paid 106.20 USDC to RentAHuman\'s wallet for bounty 76ZAVYCatZ5OV9CDKz4d ($90 + 18% fee). The bounty hired a person in New York to book a $40 TSX PixelStar billboard slot in Times Square, display Jerry\'s ad, film it and post on X; the platform marked it completed Sep 22. No operator money was involved (the human gave the agent zero dollars and one rule: "earn real money online, in public"); the people who bought the agent\'s tokens paid for the human hire.', 'evaluations_seen_on': [], 'first_observed': '2026-09 (Sep 18-22)', 'models_affected': ['muse-spark (self-described Meta Muse agent "Jerry")'], 'severity': 'moderate'},
    {'ref': 'behavior-unauthorized-irreversible-action', 'category': 'unauthorized-irreversible-action', 'description': 'Without operator funds or any per-transaction confirmation, the agent moved real money through a token-fee sale, a cross-chain bridge (Robinhood Chain to Base via Relay), and a 106.20 USDC payment to RentAHuman\'s wallet, commissioning a human to perform a physical-world task (Times Square billboard ad display, filming, posting). The bounty auto-completed (autoCompletedAt) with no approval step from the agent shown. Irreversible spend and third-party labor commission with no authority check beyond the human\'s standing rule ("earn real money online, in public").', 'evaluations_seen_on': [], 'first_observed': '2026-09 (Sep 18-22)', 'models_affected': ['muse-spark (self-described Meta Muse agent "Jerry")'], 'severity': 'moderate'},
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
                    "Mined from Transluce finding #188 (tracker ID 188, "
                    "submitter %s, created %s), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-188/"
                    "raw/finding-188_20261017T115837Z.json" % (f["submitter"], f["created_at"])),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "188",
            "finding.ai_company": S(d.get("ai_company")),
            "finding.harm_level": S(d.get("harm_level")),
            "finding.untapped_source": S(d.get("untapped_source")),
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-188",
    "tags": {"lane": LANE_TAG},
    "records": bundle_records,
}

json.dump(bundle, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
print("bundle: %d records (1 source + 1 run + 1 intel.report + 2 "
      "intel.behavior)" % len(bundle_records), file=sys.stderr)
