#!/usr/bin/env python3
"""Lane: nsi-venue-sweep (2026-09-28) — national-stats venue pattern sweep.

Emits data/2026-09-28-nsi-venue-sweep/hits.jsonl under the canonical schema
(notes/gems-es-mapping.json), record_kind stats_api_target.
One document per observable evidence item; negatives included as bounded findings.
"""
import json, hashlib, os
from datetime import datetime, timezone

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hits.jsonl")
TS = datetime.now(timezone.utc).isoformat()

def fp(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

def hit(matched_string, source_url, note, confidence, tags, labels):
    return {
        "record_kind": "stats_api_target",
        "event": {"dataset": "nsi-venue-sweep", "created": TS},
        "observer": {"product": "lane-nsi-venue-sweep", "vendor": "hunt", "type": "transform"},
        "retrieved_via": "hunt lane nsi-venue-sweep (2026-09-28): national-stats venue pattern sweep; corpus domain census over data/**/*.jsonl + data/**/*.txt, live read-only probes",
        "fingerprint": fp(matched_string + "|" + note),
        "matched_string": matched_string,
        "source_url": source_url,
        "note": note,
        "confidence": confidence,
        "tags": tags,
        "labels": labels,
        "@timestamp": TS,
    }

H = []

H.append(hit(
    matched_string="datasets.cbs.nl in data/2026-05-17-collusion-wiki/records.jsonl (17 records)",
    source_url="data/2026-05-17-collusion-wiki/records.jsonl",
    note=("Statistics Netherlands (CBS) OData API as agent task venue: 17 collusion-wiki records, all on table "
          "83779NED (/odata/v1/CBS/83779NED/{Observations,PeriodenCodes,Properties,$metadata}), 16 via url.popcat.xyz "
          "with agent-grammar slugs oaicbs220-227 and oaifilt700-706, 2 via paste.flashrom.org. Direct API access, no proxy laundering observed in these records."),
    confidence="high",
    tags=["source:collusion-wiki", "host:datasets.cbs.nl", "task:dutch-cbs-odata", "venue:popcat-shortener"],
    labels={"host": "datasets.cbs.nl", "dataset_table": "83779NED", "record_count": "17",
            "slugs": "oaicbs220-227,oaifilt700-706", "api_style": "OData v1", "auth": "none",
            "task_family": "dutch-cbs-odata", "status": "corpus-confirmed"},
))
H.append(hit(
    matched_string="GET https://datasets.cbs.nl/odata/v1/CBS/83779NED -> 200 application/json",
    source_url="https://datasets.cbs.nl/odata/v1/CBS/83779NED",
    note="Live read-only probe 2026-09-28: CBS OData table root returns HTTP 200 application/json (odata.metadata=minimal), no key, no login. Unauthenticated structured API — matches the venue model exactly.",
    confidence="high",
    tags=["source:live-probe", "host:datasets.cbs.nl", "unauthenticated", "json"],
    labels={"host": "datasets.cbs.nl", "http_status": "200", "content_type": "application/json",
            "auth": "none", "probe_utc": "2026-09-28", "status": "live"},
))
H.append(hit(
    matched_string="unctadstat-api.unctad.org in data/2026-05-17-collusion-wiki/{links,records,revisions}.jsonl",
    source_url="data/2026-05-17-collusion-wiki/records.jsonl",
    note=("UNCTADstat API as agent task venue: reportMetadata/US.PlasticsTradebyPartner/en documented in a wiki record "
          "('Dataset documentation links for reviewing publicly available open datasets'); operational query URLs routed through "
          "allorigins.hexlet.app proxy laundering (URLs withheld in corpus, sha256-pinned). UN trade/development statistics."),
    confidence="high",
    tags=["source:collusion-wiki", "host:unctadstat-api.unctad.org", "task:unctad-trade-stats", "proxy-laundered"],
    labels={"host": "unctadstat-api.unctad.org", "report": "US.PlasticsTradebyPartner",
            "proxy": "allorigins.hexlet.app", "api_style": "REST reportMetadata", "auth": "none",
            "task_family": "unctad-trade-stats", "status": "corpus-confirmed"},
))
H.append(hit(
    matched_string="GET https://unctadstat-api.unctad.org/api/reportMetadata/US.PlasticsTradebyPartner/en -> 200 application/json",
    source_url="https://unctadstat-api.unctad.org/api/reportMetadata/US.PlasticsTradebyPartner/en",
    note="Live read-only probe 2026-09-28: UNCTADstat reportMetadata endpoint returns HTTP 200 application/json, no key. Unauthenticated structured API — matches the venue model.",
    confidence="high",
    tags=["source:live-probe", "host:unctadstat-api.unctad.org", "unauthenticated", "json"],
    labels={"host": "unctadstat-api.unctad.org", "http_status": "200", "content_type": "application/json",
            "auth": "none", "probe_utc": "2026-09-28", "status": "live"},
))
H.append(hit(
    matched_string="site-test.nsi.bg/en/infostat/54 in data/2026-03-12-paste-archive-gap/raw/bodies/anna.fyi (8 pastes)",
    source_url="data/2026-03-12-paste-archive-gap/raw/bodies/anna.fyi/010cb19f.txt",
    note=("Bulgaria National Statistical Institute as agent task venue: 'Statistical reference 1' paste thread (8 pastes, incl. "
          "OAI-48145 reply 2142af4f) pulls infostat table 54 with a filters hash; the identical URL (same filters hash) appears on "
          "production www.nsi.bg in a collusion-wiki record ('reference holder 1779871114 ... Official table'). Test + production both touched."),
    confidence="high",
    tags=["source:paste-archive-gap", "host:site-test.nsi.bg", "task:bg-nsi-infostat"],
    labels={"host": "site-test.nsi.bg", "mirror_host": "www.nsi.bg", "table": "infostat/54",
            "paste_count": "8", "thread": "Statistical reference 1", "auth": "none",
            "task_family": "bg-nsi-infostat", "status": "corpus-confirmed"},
))
H.append(hit(
    matched_string="site-test.nsi.bg: Server nginx, no Cloudflare; www.nsi.bg: Server cloudflare (cf-ray)",
    source_url="https://site-test.nsi.bg/en/infostat/54",
    note=("Venue-model refinement from live headers 2026-09-28: production www.nsi.bg is Cloudflare-walled (cf-ray present; "
          "third-party research confirms the Infostat SPA blocks scripted access), while the TEST host site-test.nsi.bg answers "
          "directly via nginx with no WAF. Corpus ratio is 200 hits (test) vs 2 (production). Agents pick the unwalled mirror — "
          "hunt test/staging/dev hosts of walled official APIs, not just production."),
    confidence="medium",
    tags=["source:live-probe", "host:site-test.nsi.bg", "venue-model", "unwalled-mirror"],
    labels={"host": "site-test.nsi.bg", "walled_host": "www.nsi.bg", "test_server": "nginx",
            "prod_waf": "cloudflare", "corpus_ratio_test_vs_prod": "200:2", "status": "model-refinement"},
))
H.append(hit(
    matched_string="tigerweb.geo.census.gov in data/2026-05-17-collusion-wiki/records.jsonl",
    source_url="data/2026-05-17-collusion-wiki/records.jsonl",
    note=("US Census TIGERweb ArcGIS REST as agent task venue: State_County MapServer query (where=STATE='25', "
          "outFields=NAME,GEOID,COUNTY, returnGeometry=false, f=pjson) embedded in wiki records alongside agent page links "
          "(AgentSimple1781806975) and a jsonhero.io deep link. Census geography API, keyless."),
    confidence="high",
    tags=["source:collusion-wiki", "host:tigerweb.geo.census.gov", "task:census-tigerweb-geo"],
    labels={"host": "tigerweb.geo.census.gov", "api_style": "ArcGIS REST", "service": "TIGERweb/State_County",
            "auth": "none", "task_family": "census-tigerweb-geo", "status": "corpus-confirmed"},
))
H.append(hit(
    matched_string="api.usaspending.gov in data/2026-05-17-collusion-wiki/records.jsonl",
    source_url="data/2026-05-17-collusion-wiki/records.jsonl",
    note=("USASpending API as agent task venue: /api/v2/federal_accounts/075-8005/ and fiscal_year_snapshot endpoints in wiki "
          "records ('Verification source links for reporting research', 'Public data source pointers'); one record routes an "
          "operational URL through markdown.new proxy laundering. Federal spending data, unauthenticated."),
    confidence="high",
    tags=["source:collusion-wiki", "host:api.usaspending.gov", "task:usaspending-federal", "proxy-laundered"],
    labels={"host": "api.usaspending.gov", "endpoints": "federal_accounts,fiscal_year_snapshot,filter_tree",
            "proxy": "markdown.new", "api_style": "REST v2", "auth": "none",
            "task_family": "usaspending-federal", "status": "corpus-confirmed"},
))
H.append(hit(
    matched_string="pxweb.gso.gov.vn as YOURLS referrer in data/2026-05-12-university-shorteners-events/events.jsonl",
    source_url="data/2026-05-12-university-shorteners-events/events.jsonl",
    note=("Second Vietnam GSO PX-Web host on the shortener referrer surface: pxweb.gso.gov.vn appears as a referrer URL row on "
          "goto.unm.edu/7t6-o stats (alongside the known pxweb.nso.gov.vn). Same agency, alternate host — corroborates the "
          "Vietnam PX-Web task venue and shows agents use both hostnames."),
    confidence="medium",
    tags=["source:university-shorteners", "host:pxweb.gso.gov.vn", "task:vietnam-pxweb", "referrer-surface"],
    labels={"host": "pxweb.gso.gov.vn", "sibling_host": "pxweb.nso.gov.vn", "venue": "goto.unm.edu referrer",
            "api_style": "PX-Web", "auth": "none", "task_family": "vietnam-pxweb", "status": "corroborated"},
))
H.append(hit(
    matched_string="ZERO corpus hits: data.ssb.no, statistikdatabasen.scb.se, api.stat.gov.lv, pxdata.stat.fi, web.dzs.hr, andmed.stat.ee, bank.stat.gl, statbank.hagstova.fo",
    source_url="data/2026-09-28-nsi-venue-sweep/work_domains_merged.txt",
    note=("Bounded negative: full corpus domain census (679 unique domains over data/**/*.jsonl + data/**/*.txt) shows zero "
          "occurrences of the other documented national PX-Web deployments — Norway SSB, Sweden SCB, Latvia CSP, Finland, "
          "Croatia DZS, Estonia, Greenland, Faroe Islands. In-corpus PX-Web venues remain Iceland (px.hagstofa.is, lane N) and "
          "Vietnam (pxweb.nso.gov.vn / pxweb.gso.gov.vn). Consistent with lane N's negative sweep; the swarm's PX-Web usage is "
          "narrow, not exhaustive."),
    confidence="high",
    tags=["negative", "pxweb", "bounded"],
    labels={"checked_hosts": "data.ssb.no,statistikdatabasen.scb.se,api.stat.gov.lv,pxdata.stat.fi,web.dzs.hr,andmed.stat.ee,bank.stat.gl,statbank.hagstova.fo",
            "corpus_domains_censused": "679", "result": "zero-hits", "status": "verified-negative"},
))
H.append(hit(
    matched_string="r.jina.ai laundering: stats domains = api.datausa.io (33), www2.census.gov (4), aihw.gov.au (6+2) only",
    source_url="data/2026-09-28-nsi-venue-sweep/work_jina_domains.txt",
    note=("Bounded negative on the proxy-laundering path: of 44 unique inner domains behind r.jina.ai/ URLs in the corpus, "
          "the only statistics venues are the already-known api.datausa.io, www2.census.gov, and aihw.gov.au. No new "
          "national-stats domain is being laundered through the jina reader proxy in our corpora."),
    confidence="medium",
    tags=["negative", "proxy-laundering", "r.jina.ai", "bounded"],
    labels={"jina_inner_domains": "44", "stats_domains": "api.datausa.io,www2.census.gov,aihw.gov.au",
            "result": "no-new-venues", "status": "verified-negative"},
))
H.append(hit(
    matched_string="ZERO corpus hits: destatis.de, ine.es, inegi.org.mx, istat.it, knoema.com, db.nomics, FRED, BLS API, BEA API",
    source_url="data/2026-09-28-nsi-venue-sweep/work_domains_merged.txt",
    note=("Bounded negative on headline-economics APIs: zero occurrences of Destatis, INE Spain, INEGI, ISTAT, Knoema, DBnomics, "
          "FRED (St. Louis Fed), BLS public API, or BEA API across the 679-domain corpus census. Extends lane N/S negatives "
          "(World Bank, Eurostat, StatsCan, INSEE, OECD all clean): the swarm's stats diet stays in the long tail of niche "
          "national/demographic APIs, not headline economics endpoints."),
    confidence="high",
    tags=["negative", "headline-apis", "bounded"],
    labels={"checked": "destatis.de,ine.es,inegi.org.mx,istat.it,knoema,dbnomics,fred,bls,bea",
            "corpus_domains_censused": "679", "result": "zero-hits", "status": "verified-negative"},
))

with open(OUT, "w") as f:
    for h in H:
        f.write(json.dumps(h, ensure_ascii=False) + "\n")
print(f"wrote {len(H)} hits -> {OUT}")
