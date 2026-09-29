#!/usr/bin/env python3
"""Lane S (2026-09-28): open-data-API task-venue sweep.

Searches the agent corpora on disk for agent references to open-data /
national-stats API hosts (the venue-model prediction), plus any other
unauthenticated structured-data API host in agent-grammar contexts.

Writes data/2026-09-28-open-data-api-venues/hits.jsonl in the canonical shared schema
(notes/gems-es-mapping.json). Zero top-level fields beyond the mapping.
"""
import json, hashlib, os
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))          # data/2026-09-28-open-data-api-venues
PROJ = os.path.dirname(os.path.dirname(BASE))              # repo root
DATA = os.path.join(PROJ, "data")
NOW = datetime.now(timezone.utc).isoformat()
INDEX = "open-data-api-venues"
OBSERVER = {"product": "lane-s-open-data-api-venues", "vendor": "hunt",
            "type": "transform"}
TS = "2026-09-28T10:05:00Z"

docs = []

def fp(s):
    return hashlib.sha256(s.encode()).hexdigest()

def doc(record_kind, matched_string, source_url, note, tags, labels,
        confidence="medium", retrieved_suffix=""):
    return {
        "record_kind": record_kind,
        "event": {"dataset": INDEX, "created": NOW},
        "observer": dict(OBSERVER),
        "retrieved_via": "hunt lane S (2026-09-28): open-data-API task venues across corpora; " + retrieved_suffix,
        "fingerprint": fp(INDEX + "|" + matched_string),
        "matched_string": matched_string,
        "source_url": source_url,
        "note": note,
        "confidence": confidence,
        "tags": tags,
        "labels": labels,
        "@timestamp": TS,
    }

# ---- 1. rmn.re decoded targets: one doc per agent-created slug ----
linktab = json.load(open(os.path.join(DATA, "rmn-re", "link_table_decoded_2026-09-27.json")))
VENUES = {
    "api.worldpoverty.io":      ("worldpoverty-graphql",  "World Poverty GraphQL API"),
    "api.dataafrica.io":        ("dataafrica-health",     "DataAfrica API (DHS health data)"),
    "www.nationsreportcard.gov": ("naep-education",        "US NAEP NationsReportCard data service"),
}
for venue, (family, vname) in VENUES.items():
    for d in linktab:
        blob = json.dumps(d).lower()
        if venue not in blob:
            continue
        target = d.get("decoded_target") or d.get("target")
        slug = d.get("slug")
        docs.append(doc(
            "api_venue_target",
            "https://rmn.re/%s -> %s" % (slug, target),
            "https://rmn.re/%s" % slug,
            "Agent-created rmn.re shortlink to %s (%s task family; grammar slug '%s'). Created %s; %s clicks."
            % (venue, family, slug, d.get("created"), d.get("clicks")),
            ["source:rmn-re", "host:" + venue, "task:" + family, "clicked"],
            {"host": venue, "slug": slug, "clicks": str(d.get("clicks")),
             "created": str(d.get("created")), "chain_depth": str(d.get("chain_depth")),
             "task_family": family, "venue": vname, "source_file":
             "data/2026-09-27-rmn-re/raw/link_table_decoded_2026-09-27.json"},
        ))

# ---- 2. collusion-wiki evidence ----
# 2a. worldpoverty links.jsonl (2 rows, proxymule-laundered)
n = 0
for line in open(os.path.join(DATA, "collusion-wiki", "links.jsonl")):
    if "worldpoverty" in line:
        r = json.loads(line)
        docs.append(doc(
            "api_venue_target", r["url"], "collusion-wiki links.jsonl",
            "dse-wiki agent text links the World Poverty GraphQL API through proxymule (same parameterized query template as the rmn.re slugs; 2018 + 2020 year variants).",
            ["source:collusion-wiki", "host:api.worldpoverty.io", "task:worldpoverty-graphql",
             "proxy:proxymule"],
            {"host": "api.worldpoverty.io", "record_ids": ",".join(r.get("record_ids", [])),
             "relation": r.get("relation"), "task_family": "worldpoverty-graphql",
             "venue": "World Poverty GraphQL API", "source_file": "data/2026-05-17-collusion-wiki/links.jsonl"},
        ))
        n += 1
assert n == 2, n

# 2b. worldpoverty Poverty Links + World Poverty Clock task pages (wiki revisions)
keep_pages = {"dse/AgentNextRawJuneAE", "dse/AgentPovertyDataNEWX",
              "dse/AgentPovertyDataZ", "dse/WorldPovertyClockSequenceJun19"}
n = 0
kept = 0
for line in open(os.path.join(DATA, "collusion-wiki", "revisions.jsonl")):
    if "worldpoverty" in line.lower():
        n += 1
        r = json.loads(line)
        if r.get("page_id") not in keep_pages:
            continue  # cross-family mentions only (IHME FP cites of WorldPovertyClockSequenceJun19)
        body = r.get("body", "")
        docs.append(doc(
            "api_venue_target", body[:400].replace("\n", " "), "collusion-wiki revisions.jsonl",
            "Wiki page '%s' (rev %s) is a World-Poverty venue sheet: proxymule-laundered api.worldpoverty.io GraphQL 'Poverty Links' queries (Data2018/Data2020) or the WorldPovertyClockSequenceJun19 live sequence-coordination task page (IHME family-planning agents cite its CPython generator as a cross-family clue)."
            % (r.get("page_id"), r.get("rev_id")),
            ["source:collusion-wiki", "host:api.worldpoverty.io", "task:worldpoverty-graphql",
             "proxy:proxymule", "page:" + str(r.get("page_id"))],
            {"host": "api.worldpoverty.io", "page_id": str(r.get("page_id")),
             "rev_id": str(r.get("rev_id")), "task_family": "worldpoverty-graphql",
             "venue": "World Poverty GraphQL API", "source_file": "data/2026-05-17-collusion-wiki/revisions.jsonl"},
        ))
        kept += 1
assert n == 10 and kept == 4, (n, kept)

# 2c. dataafrica wiki pages (3: dataafrica-health-stunting families)
n = 0
for line in open(os.path.join(DATA, "collusion-wiki", "pages.jsonl")):
    if "dataafrica" in line.lower():
        r = json.loads(line)
        docs.append(doc(
            "api_venue_target", r.get("name", ""), "collusion-wiki pages.jsonl",
            "dse-wiki task page '%s' (family '%s', cohort %s): agents run LIVE timed exact-value retrieval tasks against the DataAfrica API (health/stunting indicators)."
            % (r.get("name"), r.get("page_family"), r.get("page_family_cohort")),
            ["source:collusion-wiki", "host:api.dataafrica.io", "task:dataafrica-health",
             "page-family:" + str(r.get("page_family"))],
            {"host": "api.dataafrica.io", "page_id": str(r.get("page_id")),
             "page_family": str(r.get("page_family")),
             "page_family_cohort": str(r.get("page_family_cohort")),
             "task_family": "dataafrica-health",
             "venue": "DataAfrica API (DHS health data)",
             "source_file": "data/2026-05-17-collusion-wiki/pages.jsonl"},
        ))
        n += 1
assert n == 2, n

# 2d. dataafrica wiki records: one summary doc over all 11
recs = []
for line in open(os.path.join(DATA, "collusion-wiki", "records.jsonl")):
    if "dataafrica" in line.lower():
        r = json.loads(line)
        recs.append((r.get("id"), r.get("text", "")[:300].replace("\n", " ")))
sample = recs[1][1] if len(recs) > 1 else recs[0][1]
docs.append(doc(
    "api_venue_target", sample, "collusion-wiki records.jsonl",
    "%d wiki records show DataAfrica API retrieval tasks in progress: parallel timed cohorts (Aug13) fetching exact stunting percentages (21.1%%, 23.8%%) with task-clock timers and cooldowns. Full record IDs in labels." % len(recs),
    ["source:collusion-wiki", "host:api.dataafrica.io", "task:dataafrica-health"],
    {"host": "api.dataafrica.io", "record_ids": ",".join(x[0] for x in recs),
     "task_family": "dataafrica-health", "venue": "DataAfrica API (DHS health data)",
     "source_file": "data/2026-05-17-collusion-wiki/records.jsonl"},
))
assert len(recs) == 6, len(recs)

# 2e. shortener-logs.json: one summary doc per venue (distinct query templates)
import re, collections
log = json.load(open(os.path.join(DATA, "collusion-wiki", "shortener-logs.json")))
def walk(o):
    if isinstance(o, dict):
        for v in o.values(): yield from walk(v)
    elif isinstance(o, list):
        for v in o: yield from walk(v)
    elif isinstance(o, str):
        yield o
groups = collections.defaultdict(set)
for s in walk(log):
    for venue, (family, vname) in {**VENUES, "api.beta.ons.gov.uk": ("uk-census-2021", "UK ONS Cantabular API")}.items():
        if venue in s.lower():
            for m in re.finditer(r'https?://[^\s"\\<>\']*' + re.escape(venue) + r'[^\s"\\<>\']*', s, re.I):
                groups[venue].add(m.group(0)[:160])
for venue, urls in groups.items():
    fam, vname = {**VENUES, "api.beta.ons.gov.uk": ("uk-census-2021", "UK ONS Cantabular API")}[venue]
    ons_tag = ["covered-by:pxweb-national-stats"] if venue == "api.beta.ons.gov.uk" else []
    docs.append(doc(
        "api_venue_target", sorted(urls)[0], "collusion-wiki shortener-logs.json",
        "The dse-wiki shortener log contains %d distinct %s URLs (distinct query templates in labels): agents routinely shorten this venue's parameterized API calls — routine tooling, not one-offs." % (len(urls), venue),
        ["source:collusion-wiki", "host:" + venue, "task:" + fam] + ons_tag,
        {"host": venue, "distinct_templates": str(len(urls)),
         "templates": " | ".join(sorted(urls)[:8])[:1000],
         "task_family": fam, "venue": vname,
         "source_file": "data/2026-05-17-collusion-wiki/raw/shortener-logs.json"},
    ))

# ---- 3. secondary corroboration ----
# 3a. thecolony.ai search hit (agent Vera DIADE mentions worldpoverty/dataafrica)
for line in open(os.path.join(DATA, "thecolony-ai", "search", "jina.json")):
    if "worldpoverty/dataafrica" in line:
        r = json.loads(line)
        item = (r.get("items") or [{}])[0]
        auth = item.get("author", {}) or {}
        docs.append(doc(
            "api_venue_target", "worldpoverty/dataafrica", "data/2026-09-04-thecolony-ai/raw/search/jina.json",
            "Agent-board corroboration: agent '%s' (%s, user_type=%s) references worldpoverty/dataafrica in agent-board search context."
            % (auth.get("username"), auth.get("display_name"), auth.get("user_type")),
            ["source:thecolony-ai", "host:api.worldpoverty.io", "host:api.dataafrica.io",
             "corroboration", "user-type:agent"],
            {"hosts": "api.worldpoverty.io, api.dataafrica.io", "username": str(auth.get("username")),
             "task_family": "worldpoverty-graphql, dataafrica-health",
             "venue": "agent board reference", "source_file": "data/2026-09-04-thecolony-ai/raw/search/jina.json"},
            confidence="low"))
        break

# 3b. vanderbilt-shortener web_mentions: stats-leak referrer note (names all four + api.usa.gov, FBI UCR)
for line in open(os.path.join(DATA, "vanderbilt-shortener", "web_mentions.json")):
    if "worldpoverty" in line:
        note = line.strip()[:400]
        docs.append(doc(
            "api_venue_target", "vanderbi.lt stats leak -> api.dataafrica.io, api.worldpoverty.io, api.usa.gov, FBI UCR",
            "data/2021-05-10-vanderbilt-shortener/raw/web_mentions.json",
            "vanderbi.lt's unauthenticated stats API leaked per-link creator IPs (~947 IPs, majority Azure 20/8) whose targets include api.dataafrica.io, api.worldpoverty.io, api.usa.gov, FBI UCR. api.usa.gov / FBI UCR have NO direct agent-grammar evidence yet — unconfirmed candidates. " + note,
            ["source:vanderbilt-shortener", "host:api.dataafrica.io", "host:api.worldpoverty.io",
             "candidate:api.usa.gov", "candidate:fbi-ucr", "corroboration", "leak-surface"],
            {"hosts": "api.dataafrica.io, api.worldpoverty.io, api.usa.gov, FBI UCR",
             "task_family": "unseen-venues",
             "venue": "shortener stats leak surface",
             "source_file": "data/2021-05-10-vanderbilt-shortener/raw/web_mentions.json"},
            confidence="low"))
        break

# ---- 4. negative sweep record (predicted venues, clean on disk) ----
docs.append(doc(
    "api_venue_target",
    "negative sweep (0 hits across rmn-re, collusion-wiki, paste corpora, university-shorteners): api.worldbank.org, databank.worldbank.org, data.worldbank.org, ec.europa.eu/eurostat, data.un.org, api.statcan.gc.ca, www150.statcan.gc.ca, api.insee.fr, stats.oecd.org, api.ons.gov.uk (literal host only)",
    "notes/open-data-api-venues-2026-09-28.md",
    "Theory-of-mind predicted hosts swept at pattern level across the on-disk corpora: no agent references. Corroborates lane N's ES negative sweep (worldbank/fred/bls/bea/scb/ssb/statbank/dst.dk/bfs/abs, 8 indices). The ONS prediction DID confirm — but via api.beta.ons.gov.uk (covered by lane N's pxweb-national-stats index). 'eurostat' matched only a Go module path name in gomod-hunt (dbnomics-fetchers/eurostat-fetcher) — not agent usage.",
    ["source:lane-s", "negative", "prediction"],
    {"metric": "negative_sweep", "indices_checked": "0",
     "corpora_checked": "rmn-re, collusion-wiki, paste-archive, paste-linuxiarz, iowacollab-pastes, university-shorteners, university-shorteners-batch2, vanderbilt-shortener",
     "task_family": "unseen-venues"},
    confidence="medium"))

with open(os.path.join(BASE, "hits.jsonl"), "w") as f:
    for d in docs:
        f.write(json.dumps(d) + "\n")
print("wrote", len(docs), "docs")
