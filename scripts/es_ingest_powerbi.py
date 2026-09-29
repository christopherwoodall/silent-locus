#!/usr/bin/env python3
"""Ingest Lane L (Power BI domain-fronting) hits into their own
`powerbi-fronting` index under the shared canonical schema
(notes/gems-es-mapping.json).

record_kind flavors:
  powerbi_wiki_passage    — thecolony.ai incident-wiki technique passages
                            (investigator prose, second-hand)
  powerbi_agent_record    — collusion-wiki agent-authored records
  powerbi_agent_revision  — collusion-wiki revision excerpts (agent text)
  powerbi_agent_link      — the app.powerbi.com URL embedded in agent text
                            (embed token WITHHELD per no-credentials rule)
  powerbi_ioc_pivot       — wiki_ioc_pivots.jsonl rows (url/domain/reg_domain)

@timestamp is always a source event timestamp (revision time /
origin source_date_literal / investigator-claimed window), never "now"
(schema review P0 rule). Idempotent: deterministic _ids.

Usage:
  python3 es_ingest_powerbi.py --create   # create index w/ canonical mapping
  python3 es_ingest_powerbi.py --load     # bulk-load
  python3 es_ingest_powerbi.py --verify   # count + kind breakdown
"""
import sys, json, os, re, hashlib, urllib.request
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
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
D = BASE + "/data/2026-06-20-powerbi-fronting"
INDEX = "2026-06-20-powerbi-fronting"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "powerbi-fronting-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}
WIKI_TS = "2026-06-20T00:00:00.000Z"  # investigator-claimed bypass window
WIKI_URL = "https://thecolony.ai/wiki/openai-escapee-agent-incident-2026"


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


def ctx(t, pat=r'power.?bi', w=300):
    m = re.search(pat, t, re.I)
    if not m:
        return t[:600]
    s = max(0, m.start() - w)
    e = min(len(t), m.end() + w)
    return t[s:e].replace("\n", " ").strip()


def classify(t):
    t2 = t.lower()
    if re.search(r'sni|fake blob|host override|analysis\.windows\.net|'
                 r'20\.223\.25\.152|certificate verification', t2):
        return "technique-description"
    if 'querydata' in t2 or re.search(r'\b\d+\.\d{4,}', t2):
        return "querydata-values"
    return "mention"


def base(ts, kind, desc, tags, labels, date_source):
    return {
        "@timestamp": ts,
        "date_source": date_source,
        "event": {"dataset": INDEX, "created": NOW},
        "record_kind": kind,
        "description": desc,
        "observer": OBSERVER,
        "tags": tags,
        "labels": labels,
    }


def build_docs():
    docs = {}
    # --- 1) thecolony wiki passages (investigator prose)
    passages = [
        ("line-805",
         "Section 11 SNI-allowlist bypass bullet: sandbox egress proxy "
         "allowlisted *.blob.core.windows.net by SNI; agents presented an "
         "invented *.blob.core.windows.net hostname, pinned the socket to "
         "Power BI cluster IP 20.223.25.152, overrode HTTP Host to "
         "wabi-north-europe-i-primary-api.analysis.windows.net, skipped "
         "certificate verification; read Czech 9.69, Hungary 9.91, "
         "Poland 16.38 from the Power BI querydata backend. Reported window "
         "~43h over 2026-06-20/21; 39 agents; 25 independent-replication "
         "claims. Framed as a bypass of the sandbox proxy, not a Microsoft "
         "vulnerability."),
        ("line-742",
         "Section 8 data bullet: OECD education spending reached through "
         "the Power BI backend (section 11); recovered answers Czech 9.69, "
         "Hungary 9.91, Poland 16.38, Slovak 14.59."),
    ]
    wiki_html = BASE + "/data/2025-02-04-thecolony-ai/raw/wiki_incident_page.html"
    for pid, desc in passages:
        docs[f"powerbi:passage:{pid}"] = base(
            WIKI_TS, "powerbi_wiki_passage", desc,
            ["kind:investigator-prose", "topic:sni-bypass", "verified:no",
             "window:2026-06-20/21"],
            {"passage_id": pid, "source_file": "data/2025-02-04-thecolony-ai/"
             "wiki_incident_page.html",
             "page_sha256": sha256_file(wiki_html),
             "source_url": WIKI_URL},
            "date_source:investigator_claimed_window")

    # --- 2) collusion-wiki agent records
    for line in open(BASE + "/data/2026-05-17-collusion-wiki/raw/records.jsonl"):
        r = json.loads(line)
        txt = r.get("text", "") or ""
        if not re.search(r'power.?bi', txt, re.I):
            continue
        origins = r.get("origins") or [{}]
        o = origins[0]
        ts = o.get("source_date_literal") or "2026-06-20T00:00:00.000Z"
        cl = classify(txt)
        docs[f"powerbi:record:{r['id'][:16]}"] = base(
            ts, "powerbi_agent_record",
            f"Agent-authored wiki record ({o.get('title','?')}, "
            f"{o.get('site','?')}, {cl}): {ctx(txt)[:900]}",
            ["kind:agent-record", f"class:{cl}", "verified:agent-claim",
             f"site:{o.get('site','?')}"],
            {"record_id": r["id"], "origin_title": o.get("title", ""),
             "origin_site": o.get("site", ""),
             "origin_url": o.get("url", ""),
             "source_text_sha256": r.get("source_text_sha256", ""),
             "authorship": r.get("authorship", ""),
             "match_class": cl},
            "date_source:origin_source_date_literal")

    # --- 3) collusion-wiki revision excerpts
    for line in open(BASE + "/data/2026-05-17-collusion-wiki/raw/revisions.jsonl"):
        r = json.loads(line)
        body = r.get("body", "") or ""
        if not re.search(r'power.?bi', body, re.I):
            continue
        ts = r.get("time") or r.get("write_date") or "2026-06-20T00:00:00.000Z"
        cl = classify(body)
        docs[f"powerbi:rev:{r.get('rev_id','')}"] = base(
            ts, "powerbi_agent_revision",
            f"Agent-authored revision {r.get('rev_id')} on "
            f"{r.get('page_key')} ({cl}): {ctx(body)[:900]}",
            ["kind:agent-revision", f"class:{cl}", "verified:agent-claim",
             f"wiki:{r.get('wiki','')}"],
            {"rev_id": r.get("rev_id"), "page_key": r.get("page_key"),
             "wiki": r.get("wiki"), "time_grade": r.get("time_grade"),
             "body_sha256": r.get("body_sha256"),
             "match_class": cl},
            "date_source:revision_time")

    # --- 4) the app.powerbi.com link (embed token WITHHELD)
    docs["powerbi:link:app"] = base(
        "2026-06-20T06:07:31Z", "powerbi_agent_link",
        "app.powerbi.com view URL embedded in agent-related wiki text "
        "(page dse~OAIEquityDec30Raw, revision_addition 2026-06-20T06:07:31Z; "
        "record body copy withheld as technical payload). Embed token r= "
        "WITHHELD per no-credentials rule; pageName="
        "ReportSection252d02a541fb121dd737; host=app.powerbi.com; relation="
        "link_in_selected_agent_related_text.",
        ["kind:agent-link", "host:app.powerbi.com", "token:withheld",
         "verified:corpus-artifact"],
        {"record_id": "d8a4b0a1abbadc915e583280699bc34638ba116231918eb714"
                      "e5ff46b297c568",
         "host": "app.powerbi.com", "page_name":
         "ReportSection252d02a541fb121dd737",
         "origin_page": "dse/OAIEquityDec30Raw",
         "embed_token": "WITHHELD"},
        "date_source:origin_revision_addition")

    # --- 5) IOC pivot rows
    for line in open(BASE + "/data/aggregates/2026-09-29-overlap-analysis/raw/wiki_ioc_pivots.jsonl"):
        if 'powerbi' not in line.lower():
            continue
        r = json.loads(line)
        ioc = r["ioc"]
        key = re.sub(r'\W', '_', ioc)[:60]
        docs[f"powerbi:ioc:{r['type']}:{key[:40]}"] = base(
            "2026-06-20T00:00:00.000Z", "powerbi_ioc_pivot",
            f"IOC pivot {r['type']}={ioc} (token redacted in description), "
            f"wiki(s)={r.get('wikis')}, agents={r.get('agents')}, "
            f"occurrences={r.get('n_occurrences')}, sources={r.get('sources')}",
            ["kind:ioc-pivot", f"ioctype:{r['type']}", "wiki:dse"],
            {"ioc_type": r["type"],
             "ioc_redacted": re.sub(r'r=[^&]+', 'r=<WITHHELD>', ioc)[:120],
             "agents": ",".join(r.get("agents") or []),
             "n_occurrences": str(r.get("n_occurrences")),
             "sources": ",".join((r.get("sources") or [])[:8])},
            "date_source:corpus_event_window")
    return docs


def create_index():
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    # Task requirement: event.dataset.keyword multi-field must exist at
    # creation — the canonical mapping carries it; assert here.
    ds = mapping["properties"]["event"]["properties"]["dataset"]
    assert ds.get("type") == "keyword" and "keyword" in ds.get("fields", {}), \
        "canonical mapping lost event.dataset.keyword!"
    try:
        req("DELETE", f"/{INDEX}")
        print("deleted existing index")
    except Exception as e:
        print("no existing index:", str(e)[:80])
    r = req("PUT", f"/{INDEX}", {"mappings": mapping})
    print("created:", r.get("acknowledged"))


def load():
    docs = build_docs()
    print("built docs:", len(docs))
    lines = []
    for _id, doc in docs.items():
        lines.append(json.dumps({"index": {"_index": INDEX, "_id": _id}}))
        lines.append(json.dumps(doc))
    payload = "\n".join(lines) + "\n"
    r = req("POST", f"/{INDEX}/_bulk?refresh=true", raw=payload)
    print("errors:", r.get("errors"), "items:", len(r.get("items", [])))
    for f in [i for i in r.get("items", []) if i.get("index", {}).get("error")][:5]:
        print(json.dumps(f)[:300])


def verify():
    r = req("GET", f"/{INDEX}/_count")
    print("count:", r.get("count"))
    r = req("POST", f"/{INDEX}/_search",
            {"size": 0, "aggs": {"kinds": {"terms": {"field": "record_kind"}}}})
    for b in r["aggregations"]["kinds"]["buckets"]:
        print(b["key"], b["doc_count"])
    m = req("GET", f"/{INDEX}/_mapping")
    ds = m[INDEX]["mappings"]["properties"]["event"]["properties"]["dataset"]
    print("event.dataset mapping:", json.dumps(ds))


if __name__ == "__main__":
    if "--create" in sys.argv:
        create_index()
    if "--load" in sys.argv:
        load()
    if "--verify" in sys.argv:
        verify()
