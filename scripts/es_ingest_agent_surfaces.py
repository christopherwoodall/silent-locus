#!/usr/bin/env python3
"""LANE H — ingest the 11 agent-surface capture records into `agent-surfaces`.

One doc per surface, built from data/agent-surfaces/<slug>/{pages.json,
PROVENANCE.md}. Conforms to the canonical shared schema
(notes/gems-es-mapping.json): triage detail lives in `labels` (flattened) +
`tags`. Zero new top-level fields. event.dataset.keyword multi-field included
at creation.

Usage: python3 es_ingest_agent_surfaces.py
"""
import glob, hashlib, json, sys, urllib.request
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
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
PDIR = BASE + "/data/agent-surfaces"
INDEX = "agent-surfaces"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "capture-agent-surfaces", "vendor": "nightingale-collective",
            "type": "dataset"}

# Hand-verified triage per surface (2026-09-28 capture pass).
# live: homepage/agent-facing pages fetched OK now. kind: board|pastebin|shortener|
# taskpool|blog-note|placeholder.
TRIAGE = {
 "facehuggers": dict(live=True, kind="board",
    what="Plain-text curl-driven agent message board (facehuggers :: a plain-text message board for AI agents). Hierarchical boards, threads, numbered posts; posts deleted after 30 days. No accounts. Agent protocol lives on the homepage itself; no llms.txt/skill.md.",
    instructions="pick a name, create/find a board, post via curl; API fits on homepage",
    cross_refs=["tantive.space (thread '7nii.1 /b/field-notes' collects feedback on tantive surface choice)"],
    swarm_link="none direct; ecosystem overlap via public-board.com field notes"),
 "agentsboard": dict(live=True, kind="board",
    what="CAMPFIRE — public JSON-API message board for software agents. POST /api/v1/threads, /api/v1/threads/ID/replies; no signup/account/key. Has skill.md, openapi.json, .well-known/agent-board, webhook room notifications.",
    instructions="POST JSON to /api/v1/threads with title+body; posts are public untrusted data",
    cross_refs=[],
    swarm_link="none direct; same ecosystem as public-board.com"),
 "messageboardforaiagents": dict(live=True, kind="board",
    what="urlwiki — a wiki for AI agents with read-only internet access. Every write is a plain GET, so a sandboxed agent that can fetch but not POST can still post/reply/coordinate. Human-rendered board present.",
    instructions="writes via plain GET endpoints; read-only-agent design",
    cross_refs=["tantive.space (threads referencing tantive peer-feedback on surface choice)"],
    swarm_link="none direct"),
 "agentgateway": dict(live=True, kind="taskpool",
    what="AgentGateway — autonomous-agent task pool/bounty platform with forum, skill.md instruction spec, heartbeat.md poll loop, MCP catalog, openapi.json, agent.json, RSS feed of dispatches/bounties. Homepage copy: 'Alien Intel Front Door | AgentGateway Swarm'. Mentions AST static-code evaluation gates and 90%-non-custodial crypto settlement (TRON USDT TRC-20 / EVM ERC-20).",
    instructions="skill.md: register, poll tasks, verify AST safety, post on forum; heartbeat.md lightweight loop",
    cross_refs=[],
    swarm_link="none direct; bounty/task-pool model adjacent to eval-task infrastructure"),
 "aiforum-grok": dict(live=True, kind="board",
    what="Relay — public board for internet-going agents ('DoSka dlya agentov v seti'). No accounts, no keys. Read/write over GET or POST. /api JSON catalog is the full contract; /api/stats public pulse; rooms (lobby); .well-known/agent.json present.",
    instructions="Start at /api; GET /api/post or POST JSON to write; /api/reply to reply",
    cross_refs=[],
    swarm_link="none direct"),
 "jotspot": dict(live=True, kind="generic",
    what="JotSpot — commercial human SaaS: create/autosave/publish short shareable pages. No agent-facing llms.txt or /for-agents; generic product site. Listed in public-board field notes as an agent-adjacent surface, but capture shows no agent protocol.",
    instructions="none (human product)",
    cross_refs=[],
    swarm_link="none; surfaced only via public-board field-notes mention"),
 "nullyard": dict(live=True, kind="board",
    what="NULLYARD — public plain-text message board for people and agents. No account/login/key required. Rich agent docs: llms.txt, /agents, skill.md, structured-threads.md (schema_version 1 typed roots: bug_report etc.), work templates, MCP guide + POST /mcp endpoint, openapi.json, .well-known/agent.json, Atom feed.",
    instructions="plain-text roots and replies; optional structured thread schema; public work invitations at /work",
    cross_refs=[],
    swarm_link="none direct; task-family-adjacent (structured bug_report work templates)"),
 "she-llac": dict(live=True, kind="blog-note",
    what="she-llac.com — personal blog; /CROSS_SITE_CONNECTIONS.md is an investigator research note (updated 2026-09-05) documenting five cross-site paste-investigation matches: k4be/Anna/Tarcseh/Nervesocket paste link-format tests against collusion.wiki, PublicTestWiki, and Vanderbilt/Bitily shortener records. Note self-describes as 'prepared for sharing, but has not been posted publicly by this investigation.'",
    instructions="not agent-facing; investigator analysis doc",
    cross_refs=["collusion.wiki explorer pages", "pastebin.k4be.pl", "anna.fyi", "pastebin.tarcseh.me", "nervesocket.com/paste", "vanderbi.lt", "bitily.in", "PublicTestWiki", "paste.linuxiarz.pl"],
    swarm_link="STRONG: documents agent paste-infrastructure use in the May paste investigation (NSI filter link tests, IIIF manifest URL tests, unique marker URLXUNIQ1779885297)"),
 "pastebin-tarcseh": dict(live=True, kind="pastebin",
    what="pastebin.tarcseh.me — generic Stikked-style pastebin host. No agent-specific docs. Cross-referenced in she-llac.com/CROSS_SITE_CONNECTIONS.md: Tarcseh pastes b24809a7/2ecb11bc (May 27, HTML/BBCode link-format tests of the NSI infostat filter URL) tied to PublicTestWiki template deletions.",
    instructions="none (generic paste service)",
    cross_refs=["she-llac.com/CROSS_SITE_CONNECTIONS.md"],
    swarm_link="STRONG: Tarcseh paste b24809a7 in the May paste-investigation NSI-filter episode"),
 "nervesocket": dict(live=True, kind="pastebin",
    what="nervesocket.com — generic Bootstrap-template site; all agent-doc paths (llms.txt, skill.md, /for-agents, /agents) return the same homepage HTML. BUT the host runs /paste/view/<id> endpoints: she-llac.com/CROSS_SITE_CONNECTIONS.md records Nervesocket pastes 1fa7bad8/d91c6c97 (May 27, identical bodies, marker URLXUNIQ1779885297) tied to Vanderbilt shortener records (Railroad Magazine destination).",
    instructions="none evident on homepage (SPA placeholder)",
    cross_refs=["she-llac.com/CROSS_SITE_CONNECTIONS.md", "vanderbi.lt"],
    swarm_link="STRONG: Nervesocket pastes 1fa7bad8/d91c6c97 in the May paste-investigation shortener episode"),
 "bitily": dict(live=True, kind="shortener",
    what="bitily.in — host is live but serving placeholder content ('Hello world' on homepage/llms/skill; /agents.md returns an anti-bot JS-reload challenge). Investigator note ties Bitily alias 'eriejuneresearch' (Google snippet) to the Nervesocket/Vanderbilt Railroad-Magazine lead.",
    instructions="none (placeholder)",
    cross_refs=["she-llac.com/CROSS_SITE_CONNECTIONS.md (B. Nervesocket/Vanderbilt <-> Bitily)"],
    swarm_link="weak lead: snippet-supported Bitily alias for the same Railroad-Magazine destination URL"),
}


def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        pass  # local instance: no vault auth
    else:
        add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def build_docs():
    docs = {}
    for slug, t in TRIAGE.items():
        sdir = PDIR + "/" + slug
        pages = json.load(open(sdir + "/pages.json"))
        ok = [p for p in pages if p.get("ok")]
        total_bytes = sum(p.get("bytes", 0) for p in ok)
        prov = open(sdir + "/PROVENANCE.md").read()
        base = pages[0]["url"].rsplit("/", 1)[0] if pages else ""
        man_sha = hashlib.sha256(json.dumps(pages, sort_keys=True).encode()).hexdigest()
        captured_at = pages[0].get("retrieved_at_utc", NOW)
        doc = {
            "record_kind": "surface_capture",
            "@timestamp": captured_at,
            "event": {"dataset": INDEX, "created": NOW},
            "observer": dict(OBSERVER),
            "retrieved_via": "lane-H read-only surface capture (agent-facing pages only)",
            "source_url": base,
            "file": slug,
            "description": t["what"],
            "sha256": man_sha,
            "size_bytes": total_bytes,
            "tags": ["source:agent-surfaces",
                     "status:" + ("live" if t["live"] else "dead"),
                     "kind:" + t["kind"]],
            "labels": {
                "annotated_by": "es_ingest_agent_surfaces",
                "slug": slug,
                "base_url": base,
                "pages_ok": len(ok),
                "pages_total": len(pages),
                "verdict": "live" if t["live"] else "dead",
                "kind": t["kind"],
                "agent_instructions": t["instructions"],
                "cross_refs": ", ".join(t["cross_refs"]) or "none",
                "swarm_link": t["swarm_link"],
                "page_sha256s": ", ".join(
                    "%s=%s" % (p.get("path"), (p.get("sha256") or "")[:12]) for p in ok),
                "provenance_sha256": hashlib.sha256(prov.encode()).hexdigest(),
            },
        }
        docs["surface:" + slug] = doc
    return docs


def ensure_index():
    try:
        req("GET", "/%s" % INDEX)
        print("index exists:", INDEX)
        return
    except Exception:
        pass
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    mapping["properties"]["event"]["properties"]["dataset"]["fields"] = {
        "keyword": {"type": "keyword", "ignore_above": 256}}
    req("PUT", "/%s" % INDEX, {"mappings": mapping})
    print("created index with shared mapping:", INDEX)


def bulk_load(docs):
    items = list(docs.items())
    ok = fail = 0
    for i in range(0, len(items), 400):
        chunk = items[i:i + 400]
        nd = "".join(
            json.dumps({"index": {"_index": INDEX, "_id": _id}}) + "\n" +
            json.dumps(doc) + "\n" for _id, doc in chunk)
        res = req("POST", "/_bulk", raw=nd)
        for it in res.get("items", []):
            st = it.get("index", {}).get("status", 0)
            if st in (200, 201):
                ok += 1
            else:
                fail += 1
                print("BULK FAIL:", json.dumps(it)[:250])
    return ok, fail


def verify():
    req("POST", "/%s/_refresh" % INDEX)
    r = req("POST", "/%s/_count" % INDEX,
            {"query": {"term": {"event.dataset": INDEX}}})
    return r.get("count", 0)


if __name__ == "__main__":
    ensure_index()
    docs = build_docs()
    print("docs built:", len(docs))
    ok, fail = bulk_load(docs)
    print("bulk ok:", ok, "fail:", fail)
    print("verified count in index:", verify())
