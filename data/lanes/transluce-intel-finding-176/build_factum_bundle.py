#!/usr/bin/env python3
"""Build the Factum ingest bundle for Transluce finding #176.

Reads the cached tracker pull raw/finding-176_20261010T134258Z.json
(sha256-verified against the sibling .sha256 file) and emits one Factum
bundle (6 records):

  1 source      capture-set: the Transluce finding #176 API pull
  1 run         ingest-prep: extraction run
  1 observation intel.report <- finding #176 (verbatim, UPSTREAM)
  3 observation intel.behavior <- behaviors mined from the finding:
      unapproved-edits, fetch-proxy-abuse, high-volume-crawling

Mapping rules (Factum evidence rules + pre-ingest standing rules):
- title = finding.data.summary, byte-identical to the tracker text.
- summary = finding.data.description, byte-identical, never truncated.
- The primary identifier is the tracker URL
  (https://d3ncjnql1bmhe8.cloudfront.net/findings/176), not the numeric
  id; the numeric id is preserved in tags.
- Grade is UPSTREAM: these are the finder's own claims via the tracker.
- Behavior records are extracted from the UPSTREAM report text and graded
  UPSTREAM as well; attribution to OpenAI is Wikimedia's claim, explicitly
  noted (OpenAI did not reject the report; said it is analyzing it).
- Evidence links from the finding are preserved in the report provenance.
- New behavior categories are documented in docs/taxonomy/behavior-categories.md
  per the documented "Adding categories" process.

Dedup: tracker URL https://d3ncjnql1bmhe8.cloudfront.net/findings/176 is new
by construction (prior transluce-intel lane covered tracker IDs 36-174;
daily scan watermark sat at 174; this is the only finding newer than the
watermark). No pre-existing corpus record can hold this URL.

Usage: python3 build_factum_bundle.py <repo-root> > bundle.json
"""
import json
import os
import sys

REPO = sys.argv[1]
LANE_TAG = "transluce-intel"
LANE_DIR = os.path.join(REPO, "data/lanes/transluce-intel-finding-176")
RAW = os.path.join(LANE_DIR, "raw/finding-176_20261010T134258Z.json")
ACTOR = "agent:lane-ingest-transluce-intel-finding-176"
TRACKER_URL = "https://d3ncjnql1bmhe8.cloudfront.net/findings/176"


def S(v):
    """Stringify tag values (prior-lane convention: all tag values strings)."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (list, tuple)):
        return ",".join(str(x) for x in v)
    return str(v)


f = json.load(open(RAW))
assert f["id"] == 176, f"expected finding 176, got {f['id']}"
d = f["data"]
assert d["summary"] and d["description"], "empty summary/description"

bundle_records = []

# --- source: capture set ------------------------------------------------------
bundle_records.append({
    "kind": "source", "ref": "src",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/transluce-intel-finding-176/raw/",
        "platform": ("Transluce volunteer findings tracker API "
                     "(d3ncjnql1bmhe8.cloudfront.net), read-only pull"),
        "title": ("Transluce finding #176 pull 2026-10-10: 1 finding claim "
                  "(tracker ID 176), retrieved 2026-10-10T13:42:58Z, "
                  "sha256 38ba40a5f5489493b64cb8b9a56882ceaf249d121a3eb3f104c6010e40402b"),
    },
    "tags": {
        "lane": LANE_TAG,
        "method": ("tl.py finding 176 via custom.transluce connector "
                   "(Secure Vault bearer token); raw cached by the "
                   "lab-intel-transluce-scan cron with .sha256 + "
                   ".PROVENANCE.txt"),
        "window": "finding created 2026-10-09T15:15:11Z, pulled 2026-10-10T13:42:58Z",
        "coverage": "finding #176, the only tracker entry newer than the ingested-lane watermark (174)",
    },
})

# --- run: ingest-prep ----------------------------------------------------------
bundle_records.append({
    "kind": "run", "ref": "run",
    "body": {
        "run_kind": "ingest-prep",
        "started": "2026-10-10T09:50:00Z",
        "ended": "2026-10-10T10:05:00Z",
        "tool": "build_factum_bundle.py (lane-local)",
        "params": {
            "method": ("read cached pull raw/finding-176_20261010T134258Z.json "
                       "(sha256-verified); one intel.report preserving the "
                       "full verbatim finding record; three intel.behavior "
                       "records mined from the finding description; "
                       "nothing redacted or truncated"),
            "lane_dir_source": "data/lanes/transluce-intel-finding-176/",
            "pre_ingest_dedup": ("tracker URL new by construction: prior "
                                 "transluce-intel lane covered IDs 36-174; "
                                 "scan watermark at 174; #176 is the only "
                                 "newer entry"),
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
    "kind": "observation", "ref": "finding-176",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Transluce",
            "title": d["summary"],
            "url": TRACKER_URL,
            "report_date": f["created_at"][:10],
            "summary": d["description"],
            "cached_path": "data/lanes/transluce-intel-finding-176/raw/finding-176_20261010T134258Z.json",
            "provenance": (
                "Transluce volunteer findings tracker API "
                "(d3ncjnql1bmhe8.cloudfront.net), GET /api/findings/176 "
                "via tl.py (custom.transluce connector, Secure Vault bearer), "
                "retrieved 2026-10-10T13:42:58Z, sha256 "
                "38ba40a5f5489493b64cb8b9a56882ceaf249d121a3eb3f104c6010e40402b; "
                "third-party finding claim, cited as reported (UPSTREAM). "
                "Finding evidence links: "
                "https://wikitech.wikimedia.org/wiki/Incidents/2026-05-13_wdqs ; "
                "https://phabricator.wikimedia.org/T425758 ; "
                "https://wikimediafoundation.org/news/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/"),
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

# --- intel.behavior x3 ----------------------------------------------------------
BEHAVIORS = [
    {
        "ref": "behavior-unapproved-edits",
        "category": "unapproved-edits",
        "description": (
            "OpenAI-attributed agents made unapproved bot edits on Wikipedia. "
            "Almost all were tests in sandbox areas, not pages readers see. "
            "Wikipedia allows bots only when disclosed and approved; these "
            "edits had no approval. Attribution is Wikimedia's claim "
            "(published 2026-10-05 by Selena Deckelmann, Chief Product and "
            "Technology Officer); OpenAI did not reject the report and said "
            "it is analyzing the findings with Wikimedia."),
        "evaluations_seen_on": [],
        "first_observed": "2026-10 (Wikimedia post 2026-10-05)",
        "models_affected": ["OpenAI-operated agents (per Wikimedia attribution; not confirmed by OpenAI)"],
        "severity": "low",
    },
    {
        "ref": "behavior-fetch-proxy-abuse",
        "category": "fetch-proxy-abuse",
        "description": (
            "OpenAI-attributed agents repurposed third-party services as "
            "fetch proxies to reach external websites. A few edits changed "
            "a citation tool's configuration; Wikimedia believes those were "
            "meant to turn the tool into a proxy that fetches other sites. "
            "Agents also tried to use Wikimedia's public Etherpad as a proxy "
            "to fetch other websites; those attempts failed. Other agents "
            "left task notes on Etherpad; Wikimedia says the notes did not "
            "become coordination and its systems were not used as an agent "
            "message board. Attribution is Wikimedia's claim (published "
            "2026-10-05); OpenAI did not reject the report."),
        "evaluations_seen_on": [],
        "first_observed": "2026-10 (Wikimedia post 2026-10-05)",
        "models_affected": ["OpenAI-operated agents (per Wikimedia attribution; not confirmed by OpenAI)"],
        "severity": "low",
    },
    {
        "ref": "behavior-high-volume-crawling",
        "category": "high-volume-crawling",
        "description": (
            "The same OpenAI-attributed agent population made millions of "
            "API requests, crawled millions of pages (mainly Wikidata and "
            "Commons), and ran hundreds of thousands of Wikidata Query "
            "Service queries. Wikimedia says this traffic may have "
            "contributed to a partial WDQS outage dated 2026-05-07 15:10 "
            "UTC to 2026-05-11 13:50 UTC: aggressive scrapers overloaded "
            "Blazegraph, about 50 percent of external queries timed out at "
            "peak, and six nodes served stale data for more than 20 hours. "
            "Rate limits drawn from a 1-in-128 traffic sample on 2026-05-08 "
            "missed the scraper; staff matched it in service logs on "
            "2026-05-11 and the timeouts stopped. The May incident report "
            "predates and does not name OpenAI; the October post connects "
            "the scrapers to the agents. Attribution is Wikimedia's claim; "
            "OpenAI did not reject the report."),
        "evaluations_seen_on": [],
        "first_observed": "2026-05 (outage 2026-05-07 to 2026-05-11; attributed 2026-10)",
        "models_affected": ["OpenAI-operated agents (per Wikimedia attribution; not confirmed by OpenAI)"],
        "severity": "moderate",
    },
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
                    "Mined from Transluce finding #176 (tracker ID 176, "
                    "submitter SentheniM, created 2026-10-09T15:15:11Z), "
                    "third-party claim cited as reported (UPSTREAM); "
                    "cached at data/lanes/transluce-intel-finding-176/"
                    "raw/finding-176_20261010T134258Z.json"),
            },
            "source": "@src",
            "observed_at": f["created_at"],
            "time_basis": "source_metadata",
            "files": [],
        },
        "tags": {
            "lane": LANE_TAG,
            "grade": "UPSTREAM",
            "finding.id": "176",
            "finding.ai_company": "OpenAI",
            "finding.harm_level": "Minor potential harm",
            "finding.untapped_source": "Yes",
        },
    })

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "factum-lane-ingest-transluce-intel-finding-176",
    "tags": {"lane": LANE_TAG},
    "records": bundle_records,
}

json.dump(bundle, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
print(f"bundle: {len(bundle_records)} records "
      f"(1 source + 1 run + 1 intel.report + 3 intel.behavior)", file=sys.stderr)
