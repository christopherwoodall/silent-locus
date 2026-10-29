#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane open-data-api-venues.

Reads data/lanes/open-data-api-venues/events.jsonl (46 legacy events, lane S
2026-09-28) plus the cited sibling raw corpora, and emits a Factum bundle JSON
on stdout for `factum.py add --input`.

Cleaner rules applied:
- Dedup: 21 worldpoverty events skipped as corpus dupes, verified
  byte-identical against lane 2026-09-28-worldpoverty-task-family records:
  15 rmn.re shortcuts (exact short_url matches), 2 proxymule links (URLs
  embedded in that lane's infra.message bodies), 4 wiki pages (E32-E35
  matched_strings are truncations of bodies stored verbatim there;
  dse~WorldPovertyClockSequenceJun19@1 == DataResearchHelper message,
  615-char Poverty Links body == OAI7E/OpenAIHelper/AgentMassAppend messages,
  all 3 Poverty Links pages share one identical body).
- Schema mapping: term is the actual IOC value (host, wiki page path,
  username, leak surface), never an internal ID.
- Verbatim bodies: truncated legacy matched_strings replaced with full raw
  bytes (revisions.jsonl body, records.jsonl text, shortener-logs.json URL
  strings). No truncation, no case/whitespace changes.
- Shortcut destinations parsed from matched_string '<short> -> <dest>'.
- observed_at from the legacy @timestamp (2026-09-28T10:05:00Z),
  time_basis 'legacy_documented'. No invented timestamps.
- Every record tagged {"lane": "open-data-api-venues"}. No edges created
  during ingest (in_lane edges arrive via the lane tag in later passes).
- Never redact: creator IPs were already excluded at the lane layer and are
  not reintroduced here.
"""
import json
import sys

LANE = "open-data-api-venues"
ACTOR = "agent:lane-ingest-open-data-api-venues"
LEGACY_EVENTS = "data/lanes/open-data-api-venues/events.jsonl"
OBSERVED_AT = "2026-09-28T10:05:00Z"
WIKI = "evidence/2026-05-17-collusion-wiki"

evs = [json.loads(l) for l in open(LEGACY_EVENTS, encoding="utf-8") if l.strip()]
assert len(evs) == 46, f"expected 46 legacy events, got {len(evs)}"


def by_tag(tag):
    return [e for e in evs if tag in e["tags"]]


# --- raw verbatim sources ---------------------------------------------------
def raw_records(ids):
    out = []
    for line in open(f"{WIKI}/raw/records.jsonl", encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if d.get("id") in ids:
            out.append(d)
    out.sort(key=lambda r: ids.index(r["id"]))
    assert [r["id"] for r in out] == ids, "missing wiki records"
    return out


E38_IDS = [
    "0ab16bab66d4be40c71321f79bcec497c8e66079a58ad46621218353b1b52834",
    "27e2e18325a1d63aa2750ad14e8db007e887038f60505a708430f4232ffa5fb7",
    "79693eec3085e6462fefa18c58a067aba965da67608731333659fdac728d576e",
    "7ae6ccfe046efe0a6b373168dff2fe14243ddfb4313385bf83e1f25426992c67",
    "7eb8adea1fde4512a7307b37e55308f9606e9b1fd25f076c60e8ffd3c55f2b63",
    "cff6d0b1d7995df7ba205983759d8af2cc5c29da7564bb35e148b36ba5b0ece2",
]
RECORDS = raw_records(E38_IDS)


def raw_templates():
    """Full verbatim distinct URL strings per host from shortener-logs.json."""
    import re
    raw = open(f"{WIKI}/raw/shortener-logs.json", encoding="utf-8").read()
    hosts = {
        "api.beta.ons.gov.uk": set(),
        "www.nationsreportcard.gov": set(),
        "api.dataafrica.io": set(),
        "api.worldpoverty.io": set(),
    }
    for m in re.finditer(r"https?://[^\s\"']+", raw):
        u = m.group(0)
        for h in hosts:
            if h in u:
                hosts[h].add(u)
    return {h: sorted(v) for h, v in hosts.items()}


TEMPLATES = raw_templates()

# --- bundle ------------------------------------------------------------------
records = []

records.append({
    "ref": "src",
    "kind": "source",
    "body": {
        "locator": LEGACY_EVENTS,
        "source_type": "submitted",
    },
    "tags": {"lane": LANE},
})

# 1. Fresh rmn.re shortlinks (15): 10 dataafrica + 5 nationsreportcard.
#    The 15 worldpoverty shortlinks already live in lane
#    2026-09-28-worldpoverty-task-family and are skipped here.
DUPE_SHORTS = {
    "https://rmn.re/agpovertyruralclock95080", "https://rmn.re/pa0xy",
    "https://rmn.re/pa1xy", "https://rmn.re/testwp8342",
    "https://rmn.re/wpcafgghana20182020rural28218",
    "https://rmn.re/wpcagent2018md", "https://rmn.re/wpcagent2018raw",
    "https://rmn.re/wpcagent2020md", "https://rmn.re/wpcagent2020raw",
    "https://rmn.re/wpccite2018x", "https://rmn.re/wpcfinal20185574",
    "https://rmn.re/wpcfinal20206539", "https://rmn.re/wpcrmn771",
    "https://rmn.re/wpdata201246", "https://rmn.re/xyzpov27",
}
shorts = [e for e in by_tag("source:rmn-re") if e["source_url"] not in DUPE_SHORTS]
assert len(shorts) == 15, f"expected 15 fresh shortlinks, got {len(shorts)}"
seen_urls = set()
for i, e in enumerate(shorts):
    short_url = e["source_url"]
    assert short_url not in seen_urls, f"in-batch dupe: {short_url}"
    seen_urls.add(short_url)
    dest = e["matched_string"].split(" -> ", 1)[1]
    lb = e["labels"]
    records.append({
        "ref": f"sc{i}",
        "kind": "observation",
        "body": {
            "type": "infra.shortcut",
            "data_schema": "urn:factum:infra:shortcut:1",
            "data": {
                "short_url": short_url,
                "destination": dest,
                "service": "rmn.re",
            },
            "source": "@src",
            "files": [],
            "observed_at": OBSERVED_AT,
            "time_basis": "legacy_documented",
        },
        "tags": {
            "lane": LANE,
            "grade": "OBSERVED",
            "host": lb["host"],
            "task_family": lb["task_family"],
            "venue": lb["venue"],
            "slug": lb["slug"],
            "clicks": lb["clicks"],
            "created_legacy": lb["created"],
            "legacy_fingerprint": e["fingerprint"],
            "legacy_source_file": lb["source_file"],
            "evidence_note": e["note"],
        },
    })

# 2. DataAfrica wiki task pages (E36, E37).
pages = [e for e in evs if e["labels"].get("page_id", "").startswith("dse/DataAfrica")]
assert len(pages) == 2, f"expected 2 task pages, got {len(pages)}"
for i, e in enumerate(pages):
    lb = e["labels"]
    records.append({
        "ref": f"pg{i}",
        "kind": "observation",
        "body": {
            "type": "infra.ioc",
            "data_schema": "urn:factum:infra:ioc:1",
            "data": {
                "term": lb["page_id"],
                "category": "marker",
                "provenance": (
                    f"collusion-wiki pages.jsonl (page family "
                    f"'{lb['page_family']}', cohort {lb['page_family_cohort']}) "
                    f"via {LEGACY_EVENTS}"
                ),
                "status": "active",
            },
            "source": "@src",
            "files": [],
            "observed_at": OBSERVED_AT,
            "time_basis": "legacy_documented",
        },
        "tags": {
            "lane": LANE,
            "grade": "OBSERVED",
            "host": lb["host"],
            "task_family": lb["task_family"],
            "venue": lb["venue"],
            "legacy_fingerprint": e["fingerprint"],
            "evidence_note": e["note"],
        },
    })

# 3. DataAfrica live retrieval task records (E38): 6 verbatim wiki messages.
assert len(RECORDS) == 6
for i, r in enumerate(RECORDS):
    records.append({
        "ref": f"msg{i}",
        "kind": "observation",
        "body": {
            "type": "infra.message",
            "data_schema": "urn:factum:infra:message:1",
            "data": {
                "venue": "dse-wiki (collusion-wiki records.jsonl)",
                "message_id": r["id"],
                "author": r["authorship"],
                "body": r["text"],
                "provenance": (
                    f"collusion-wiki records.jsonl record {r['id']} "
                    f"(selection: {r['selection_basis']}) via {LEGACY_EVENTS}"
                ),
            },
            "source": "@src",
            "files": [],
            "observed_at": OBSERVED_AT,
            "time_basis": "legacy_documented",
        },
        "tags": {
            "lane": LANE,
            "grade": "OBSERVED",
            "host": "api.dataafrica.io",
            "task_family": "dataafrica-health",
            "origins": " | ".join(
                f"{o['source_id']} ({o['site']}, {o['source_date_literal']})"
                for o in r["origins"]
            ),
            "evidence_note": (
                "6 wiki records show DataAfrica API retrieval tasks in "
                "progress: parallel timed cohorts (Aug13) fetching exact "
                "stunting percentages (21.1%, 23.8%) with task-clock timers "
                "and cooldowns."
            ),
        },
    })

# 4. Wiki shortener-log URL template sets (E39-E42), verbatim from raw.
TPL_META = [
    ("api.beta.ons.gov.uk", "uk-census-2021", "UK ONS Cantabular API"),
    ("www.nationsreportcard.gov", "naep-education",
     "US NAEP NationsReportCard data service"),
    ("api.dataafrica.io", "dataafrica-health", "DataAfrica API (DHS health data)"),
    ("api.worldpoverty.io", "worldpoverty-graphql", "World Poverty GraphQL API"),
]
for i, (host, task_family, venue) in enumerate(TPL_META):
    tmpls = TEMPLATES[host]
    e = next(x for x in evs if x["labels"].get("host") == host
             and "shortener" in x["source_url"])
    assert str(len(tmpls)) == e["labels"]["distinct_templates"], (
        f"{host}: raw count {len(tmpls)} != lane count "
        f"{e['labels']['distinct_templates']}"
    )
    records.append({
        "ref": f"tpl{i}",
        "kind": "observation",
        "body": {
            "type": "infra.ioc",
            "data_schema": "urn:factum:infra:ioc:1",
            "data": {
                "term": host,
                "category": "url-pattern",
                "provenance": (
                    f"collusion-wiki shortener-logs.json: {len(tmpls)} distinct "
                    f"URL templates for {host} via {LEGACY_EVENTS}"
                ),
                "status": "active",
            },
            "source": "@src",
            "files": [],
            "observed_at": OBSERVED_AT,
            "time_basis": "legacy_documented",
        },
        "tags": {
            "lane": LANE,
            "grade": "OBSERVED",
            "task_family": task_family,
            "venue": venue,
            "legacy_fingerprint": e["fingerprint"],
            "templates": " | ".join(tmpls),
            "evidence_note": e["note"],
        },
    })

# 5. thecolony-ai agent-board corroboration (E43).
e43 = next(e for e in evs if "source:thecolony-ai" in e["tags"])
records.append({
    "ref": "col0",
    "kind": "observation",
    "body": {
        "type": "infra.ioc",
        "data_schema": "urn:factum:infra:ioc:1",
        "data": {
            "term": "vera-diade",
            "category": "marker",
            "provenance": (
                "thecolony-ai search/jina.json "
                "(username vera-diade, display_name 'Vera (DIADE)', "
                f"user_type agent) via {LEGACY_EVENTS}"
            ),
            "status": "active",
        },
        "source": "@src",
        "files": [],
        "observed_at": OBSERVED_AT,
        "time_basis": "legacy_documented",
    },
    "tags": {
        "lane": LANE,
        "grade": "OBSERVED",
        "task_family": "worldpoverty-graphql, dataafrica-health",
        "legacy_fingerprint": e43["fingerprint"],
        "evidence_note": e43["note"],
    },
})

# 6. vanderbi.lt stats-leak corroboration + unconfirmed candidates (E44).
e44 = next(e for e in evs if "source:vanderbilt-shortener" in e["tags"])
records.append({
    "ref": "van0",
    "kind": "observation",
    "body": {
        "type": "infra.ioc",
        "data_schema": "urn:factum:infra:ioc:1",
        "data": {
            "term": "vanderbi.lt unauthenticated stats API leak (per-link creator IPs)",
            "category": "other",
            "provenance": (
                "vanderbilt-shortener web_mentions.json "
                f"(~947 leaked per-link creator IPs) via {LEGACY_EVENTS}"
            ),
            "status": "active",
        },
        "source": "@src",
        "files": [],
        "observed_at": OBSERVED_AT,
        "time_basis": "legacy_documented",
    },
    "tags": {
        "lane": LANE,
        "grade": "OBSERVED",
        "candidate_hosts": "api.usa.gov, FBI UCR (unconfirmed candidates, no direct agent-grammar evidence)",
        "legacy_fingerprint": e44["fingerprint"],
        "evidence_note": e44["note"],
    },
})

# 7. Negative sweep: run record + graded claim (E45).
#    Mirrors the gem-negative-lanes pattern: claim subject/cites point at the
#    run, since `cites` rejects source records (REFERENCE_TYPE).
e45 = next(e for e in evs if "source:lane-s" in e["tags"])
records.append({
    "ref": "run0",
    "kind": "run",
    "body": {
        "run_kind": "bounded_negative_sweep",
        "coverage": {
            "complete": True,
            "description": (
                "lane S (2026-09-28): venue-model prediction sweep for "
                "open-data / national-stats API task venues across on-disk "
                "corpora; 0 agent references on predicted hosts"
            ),
        },
        "params": {
            "venue": "open-data-API predicted task venues",
            "method": "pattern-level sweep of rmn-re link table, "
                      "collusion-wiki (links/revisions/pages/records/shortener-logs), "
                      "paste corpora, university-shorteners stats",
            "hosts": [
                "api.worldbank.org", "databank.worldbank.org",
                "data.worldbank.org", "ec.europa.eu/eurostat", "data.un.org",
                "api.statcan.gc.ca", "www150.statcan.gc.ca", "api.insee.fr",
                "stats.oecd.org", "api.ons.gov.uk",
            ],
            "result": "zero_hits",
        },
    },
    "tags": {"lane": LANE},
})
records.append({
    "ref": "claim0",
    "kind": "claim",
    "body": {
        "subject": "@run0",
        "property": "verdict",
        "value": {
            "venue": "open-data-API predicted task venues",
            "verdict": "zero_hits",
            "hosts": [
                "api.worldbank.org", "databank.worldbank.org",
                "data.worldbank.org", "ec.europa.eu/eurostat", "data.un.org",
                "api.statcan.gc.ca", "www150.statcan.gc.ca", "api.insee.fr",
                "stats.oecd.org", "api.ons.gov.uk",
            ],
            "corpora": [
                "rmn-re", "collusion-wiki", "paste-archive",
                "paste-linuxiarz", "iowacollab-pastes",
                "university-shorteners", "university-shorteners-batch2",
                "vanderbilt-shortener",
            ],
            "note": e45["note"],
        },
        "basis": "OBSERVED",
        "cites": ["@run0"],
    },
    "tags": {"lane": LANE, "confidence": "high"},
})

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "lane-ingest-open-data-api-venues-2026-10-10",
    "records": records,
}

sys.stdout.write(json.dumps(bundle, ensure_ascii=False, indent=1))
print(f"\n# records: {len(records)}", file=sys.stderr)
