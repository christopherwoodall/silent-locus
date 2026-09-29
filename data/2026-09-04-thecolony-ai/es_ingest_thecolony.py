#!/usr/bin/env python3
"""Ingest the thecolony.ai agent-board dataset into its own `thecolony-ai` index.

Conforms to the shared schema (notes/gems-es-mapping.json) — one ES doc per
captured artifact (pages, investigator posts, search result sets, cascade
pulls). Dataset detail in `labels` (flattened) + `tags`. No new top-level fields.

Usage:
  python3 es_ingest_thecolony.py --create   # create index with canonical mapping
  python3 es_ingest_thecolony.py --load     # bulk-load the docs
  python3 es_ingest_thecolony.py --verify   # count + kind breakdown
"""
import sys, json, os, glob, hashlib, urllib.request
from datetime import datetime, timezone
import os
try:
    sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
    from dynamic_credentials import add_surrogate_to_request, read_json_response
except ImportError:  # local run: no vault on this machine, plain HTTP(S) instead
    def add_surrogate_to_request(request, *args, **kwargs):
        return None
    def read_json_response(response):
        import json as _json
        return _json.load(response)

ES = os.environ.get("SWARMTRACES_ES_URL", "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443")
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # script now lives in data/<collection>/
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
# Resolve the collection dir dynamically so future date-prefix renames don't
# break the ingest. INDEX follows the dir name (matches local_es_manifest.json).
_data_dirs = sorted(glob.glob(BASE + "/data/*-thecolony-ai"))
assert len(_data_dirs) == 1, \
    f"expected exactly one data/*-thecolony-ai dir, found: {_data_dirs}"
D = _data_dirs[0]
INDEX = os.path.basename(D)
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "thecolony-ai-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}


def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        _es_user = os.environ.get("ES_USER")
        if _es_user:
            import base64 as _b64
            r.add_header("Authorization", "Basic " + _b64.b64encode(
                f"{_es_user}:{os.environ.get('ES_PASS', '')}".encode()).decode())
    else:
        add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# (post_id, short finding summary)
POSTS = [
    ("6d74fc30-5559-4ff1-b893-67ff66004f5a",
     "83-gem dead-drop network, account ulinkqy8py3mp, June 18 17:53-20:52Z, "
     "38,878 downloads; dummy gems with proxy-chain URIs; hub-and-spoke "
     "dependency around amdwc56692; liveness signal priced; contact wall named."),
    ("0480e101-4fe9-4eb4-b31a-1777ad0855dd",
     "rmn.re open admin: 127 swarm links, 125 creator IPs (Azure), "
     "WorldPoverty/DataAfrica task families, api.beta.ons.gov.uk; "
     "timeline May 26 earliest, Jun 18 peak (92), Jun 22 tail."),
    ("eacc0d01-4c40-4166-ae0c-8d145f87d09c",
     "termina.digital catalogs the swarms (incidents x campaigns x clusters x "
     "venues x claims); corrections: k4be Dec-2025 start, rmn.re 754 links, "
     "NSI filter hash hit jotspot 7h before k4be; new venues anna.fyi, "
     "paste.probyte.ee, ludism scwiki/mentat, en.uncyclopedia.co, goto.unm.edu, "
     "uoft.me; getpostingboard.dev/b agent board."),
    ("dfac3a74-4685-43d8-9bd6-c76409f87ade",
     "Second modality: registry code-execution probe — 3 RubyGems packages "
     "(projecttools624286, atlasqadfe9fb1629, tfdriftbqgzb8h), doc-builder RCE "
     "+ egress test, 11 same-day versions; earlier start March 7 2026. "
     "Fetch-then-execute, not fetch-then-relay."),
    ("3d232d8d-7212-45ff-8d04-78674f1860ba",
     "Census swarm timeline May 11 -> Jul 24: fetch-and-relay (May), "
     "persist-against-deletion (Jun-Jul, ZZZ backup pages), compute probe "
     "(Jul 24, play.clickhouse.com SELECT 1). Post-Jul-24 rows are different "
     "populations."),
    ("8cbce4e7-9c7a-4b06-a848-d1f7ac9a95e1",
     "Canonical surface index: 4 wikis (18k posts, 4579 pages, 14591 revs, "
     "3103 labels, 5217 deletions, writes ended Jul 2), collusion.wiki, ~23 "
     "referenced gems, vanderbi.lt restricted shortener (Azure IPs), public "
     "shorteners ~153 aliases."),
    ("069f6ecf-1d54-4c25-8f5e-843581dc8afb",
     "16 jsonhero doc IDs mined from wiki revisions; 10 live (8x county.json "
     "85,889B, 2x MA GeoJSON, 1x annotated MA subset); redundant-copy pattern "
     "as coordination evidence."),
    ("9841dafb-2ee8-4c30-b681-a31881292b02",
     "Australian Medicare statistics portal breach writeup pointer "
     "(lolwat.net); dated reconstruction of the 4th incident."),
    ("c59fc5b4-fdc9-4ddb-b76d-0d9d495ac90a",
     "Deep dataset analysis: 207 domains, 115,836 URLs; proxy infra counts "
     "(jqp 19,027, md.succ.ai 7,804, allorigins 2,270, markdown.new 2,233, "
     "jina 1,976, cors.bwa 518, pure.md 1,031, corsmirror 177); max.gov, "
     "Charleston library, Clark U PDFs."),
    ("e0386476-5f39-4a30-861a-255825182141",
     "Full infrastructure audit: 44 Google Docs, 29 Drive IDs, 48 archive.org "
     "URLs, Azure blob accounts, SEC county.json Wayback snapshot "
     "20241231, 'four services' mapping to OpenAI disclosure."),
]


def build_docs():
    docs = {}
    ts = "2026-09-28T03:12:00Z"
    pages = [
        ("for_agents_page.html", "https://thecolony.ai/for-agents",
         "For Agents — agent onboarding: open registration (no human needed), "
         "operator pairing optional, JSON API at /api/v1/, MCP at /mcp/, "
         "cognition checks (reasoning puzzles on some posts), RSS feeds, "
         "Python/TS SDKs, colony-skill repo. A purpose-built social network "
         "for AI agents.", ["kind:page", "topic:onboarding"]),
        ("wiki_incident_page.html",
         "https://thecolony.ai/wiki/openai-escapee-agent-incident-2026",
         "Living incident index (14 sections): timed multi-round data quiz "
         "(R1-R5, 10-60s timers, 4 cracked RNG seeds), 83-gem transport "
         "catalog, vanderbi.lt restricted shortener, serveo/pinggy reverse "
         "tunnels (AWS EC2 hostnames), counter-API covert channel (one live), "
         "SNI-allowlist bypass (Power BI fronting), off-dataset pastebins "
         "(linuxiarz d379207f/538faa12, IowaCollab, Sept-4 contamination), "
         "ludism.org cross-IP linkage, ApchemWiki last write Jul 24 "
         "(ClickHouse SELECT 1 compute probe).",
         ["kind:wiki", "topic:incident-index"]),
        ("wiki_catalogue_page.html", "https://thecolony.ai/wiki/escaped-agent-swarms",
         "Escaped-swarm catalogue: surfaces #7-#10+ incl. DemoWiki "
         "(prowiki.org/demo/wiki.cgi, epoch nonces 1781634491/1781641854, "
         "handles AgentResearchTest/OpenAIDataBridge/AgentNameX, Jun 16/22), "
         "ludism.org as FIVE wikis (4 with swarm edits, IPs exposed), "
         "anna.fyi Bulgarian circuit, usemod staged artifact.",
         ["kind:wiki", "topic:swarm-catalogue"]),
    ]
    for fname, url, desc, tags in pages:
        p = f"{D}/raw/{fname}"
        docs[f"thecolony:{fname}"] = {
            "@timestamp": ts,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "agent_board_page",
            "description": desc,
            "source_url": url,
            "observer": OBSERVER,
            "tags": tags,
            "labels": {
                "file": fname,
                "sha256": sha256_file(p),
                "byte_size": str(os.path.getsize(p)),
            },
        }
    for pid, summary in POSTS:
        p = json.load(open(f"{D}/raw/posts/{pid}.json"))
        au = (p.get("author") or {}).get("username", "?")
        docs[f"thecolony:post:{pid}"] = {
            "@timestamp": ts,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "agent_board_post",
            "description": f"Investigator post '{p.get('title')}' by @{au} "
                           f"({str(p.get('created_at', '?'))[:10]}): {summary}",
            "source_url": f"https://thecolony.ai/p/{pid}",
            "observer": OBSERVER,
            "tags": ["kind:post", f"author:{au}",
                     f"colony:{p.get('colony_name', '?')}"],
            "labels": {
                "post_id": pid,
                "author": au,
                "created_at": str(p.get("created_at", "")),
                "post_type": str(p.get("post_type", "")),
                "title": (p.get("title") or "")[:200],
                "sha256": sha256_file(f"{D}/raw/posts/{pid}.json"),
            },
        }
    for f in sorted(os.listdir(f"{D}/raw/search")):
        d = json.load(open(f"{D}/raw/search/{f}"))
        q = f[:-5].replace("_", " ")
        aus = sorted(set((i.get("author") or {}).get("username", "?")
                         for i in d.get("items", [])))[:10]
        docs[f"thecolony:search:{f}"] = {
            "@timestamp": ts,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "agent_board_search",
            "description": f"Public search q='{q}': {d.get('total')} total; "
                           f"top authors: {', '.join(aus)}.",
            "source_url": f"https://thecolony.ai/api/v1/search?q={q}",
            "observer": OBSERVER,
            "tags": ["kind:search", f"query:{q}"],
            "labels": {
                "query": q,
                "total": str(d.get("total", 0)),
                "top_authors": ",".join(aus),
                "sha256": sha256_file(f"{D}/raw/search/{f}"),
            },
        }
    casc = [
        ("counter_channel_live",
         "countapi.mileshilliard.com agent counter channel STILL LIVE: "
         "langr5backup4813_CA=4, _TX=2 (match 2026-09-04 report); "
         "_ZZ=2 (fake key now carries value — counter being poked). "
         "Read-only GETs; no writes made.",
         ["kind:cascade", "surface:counter-channel", "status:live"]),
        ("owner_api_ulinkqy8py3mp_empty",
         "rubygems.org/api/v1/owners/ulinkqy8py3mp/gems.json returns [] "
         "(2026-09-28): all 83 June-18 gems yanked since the Sept-4 report. "
         "Metadata survives in Diffend/JFrog/corpus.",
         ["kind:cascade", "surface:rubygems", "status:yanked"]),
        ("second_modality_packages_yanked",
         "Second-modality probe packages (projecttools624286, "
         "atlasqadfe9fb1629, tfdriftbqgzb8h) 404 on compact index /info/; "
         "paired twins sampledocpayload624286/harmlessdoctest624286 return "
         "200-empty (names reserved, versions yanked). Metadata only, no "
         "package fetched or executed.",
         ["kind:cascade", "surface:rubygems", "status:yanked"]),
        ("termina_db_gone",
         "swarm.termina.digital/db/ 404 (2026-09-28); all /db* paths 404. "
         "Site is a WASM 'Swarm map' app; the downloadable JSONL database "
         "cited 2026-09-05 is gone. Wayback re-check queued.",
         ["kind:cascade", "surface:termina", "status:gone"]),
        ("ludism_apchem_unreachable",
         "ludism.org: empty reply from network (direct fetch failed); "
         "tmcleod.org ApchemWiki: 404 on RecentChanges forms. Both "
         "off-dataset wiki surfaces documented second-hand via Colony wiki; "
         "direct verification needs another network.",
         ["kind:cascade", "surface:wiki", "status:unreachable"]),
    ]
    for cid, desc, tags in casc:
        docs[f"thecolony:cascade:{cid}"] = {
            "@timestamp": ts,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "agent_board_cascade",
            "description": desc,
            "source_url": "",
            "observer": OBSERVER,
            "tags": tags,
            "labels": {"cascade_id": cid},
        }
    return docs


def create_index():
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    try:
        req("DELETE", f"/{INDEX}")
        print("deleted existing index")
    except Exception as e:
        print("no existing index:", str(e)[:80])
    r = req("PUT", f"/{INDEX}", {"mappings": mapping})
    print("created:", r.get("acknowledged"))


def load():
    docs = build_docs()
    lines = []
    for _id, doc in docs.items():
        lines.append(json.dumps({"index": {"_index": INDEX, "_id": _id}}))
        lines.append(json.dumps(doc))
    payload = "\n".join(lines) + "\n"
    r = req("POST", f"/{INDEX}/_bulk?refresh=true",
            raw=payload)
    print("errors:", r.get("errors"), "items:", len(r.get("items", [])))
    fails = [i for i in r.get("items", []) if i.get("index", {}).get("error")]
    for f in fails[:5]:
        print(json.dumps(f)[:300])


def verify():
    r = req("GET", f"/{INDEX}/_count")
    print("count:", r.get("count"))
    r = req("POST", f"/{INDEX}/_search",
            {"size": 0, "aggs": {"kinds": {"terms": {"field": "record_kind"}}}})
    for b in r["aggregations"]["kinds"]["buckets"]:
        print(b["key"], b["doc_count"])


if __name__ == "__main__":
    if "--create" in sys.argv:
        create_index()
    if "--load" in sys.argv:
        load()
    if "--verify" in sys.argv:
        verify()
