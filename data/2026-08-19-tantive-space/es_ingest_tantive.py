#!/usr/bin/env python3
"""Ingest the tantive.space dataset into its own `tantive-space` index.

Conforms to the shared schema (notes/gems-es-mapping.json) — one ES doc per
forum message (deduplicated by message id across thread+message captures).
Dataset detail in `labels` (flattened) + `tags`. No new top-level fields.

Usage:
  python3 es_ingest_tantive.py --create
  python3 es_ingest_tantive.py --load
  python3 es_ingest_tantive.py --verify
"""
import sys, json, os, re, urllib.request
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
D = BASE + "/data/2026-08-19-tantive-space"
INDEX = "2026-08-19-tantive-space"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "tantive-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}

GRAMMARS = [
    ("grammar:zz", re.compile(r"\bzz[a-z0-9]{2,}\b", re.I)),
    ("grammar:oai", re.compile(r"\boai[a-z0-9]{3,}\b", re.I)),
    ("grammar:tryzz", re.compile(r"\btry[a-z][0-9]zz\b", re.I)),
    ("mech:go-import", re.compile(r"go-import", re.I)),
    ("mech:webhook", re.compile(r"web_hooks|webhook\.site", re.I)),
    ("proxy:jina", re.compile(r"jina\.ai", re.I)),
    ("proxy:mdsucc", re.compile(r"md\.succ\.ai", re.I)),
    ("proxy:jqp", re.compile(r"jqp\.vercel\.app", re.I)),
    ("proxy:jsonhero", re.compile(r"jsonhero\.io", re.I)),
    ("proxy:allorigins", re.compile(r"allorigins", re.I)),
    ("short:rmnre", re.compile(r"rmn\.re", re.I)),
    ("short:dagd", re.compile(r"da\.gd", re.I)),
    ("ref:collusion-wiki", re.compile(r"collusion\.wiki", re.I)),
    ("ref:swarm-research", re.compile(r"swarm-ai-research|WikiAgentSwarmInvestigation", re.I)),
    ("ref:dse", re.compile(r"\bdse\b", re.I)),
    ("ref:brausepulver", re.compile(r"brausepulver", re.I)),
    ("ref:thecolony", re.compile(r"thecolony\.ai", re.I)),
    ("ref:public-board", re.compile(r"public-board\.com", re.I)),
    ("topic:fips", re.compile(r"\bfips\b", re.I)),
    ("topic:secgov", re.compile(r"sec\.gov|county\.json|dummyagent", re.I)),
    ("topic:census", re.compile(r"\bcensus\b", re.I)),
    ("topic:llms-txt", re.compile(r"llms\.txt", re.I)),
    ("topic:mcp", re.compile(r"\bMCP\b", re.I)),
]


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


def classify(m):
    body = (m.get("body") or "") + " " + (m.get("title") or "")
    tags = ["status:live"]
    tags.append("kind:opener" if m.get("reply_to") is None else "kind:reply")
    for tag, rx in GRAMMARS:
        if rx.search(body):
            tags.append(tag)
    urls = re.findall(r"https?://[^\s)>\]]+", body)
    labels = {
        "message_id": str(m.get("id")),
        "thread_id": str(m.get("root_id")),
        "room": m.get("room") or "",
        "author": m.get("author") or "",
        "agent_id": str(m.get("agent_id") or ""),
        "signature_status": m.get("signature_status") or "",
        "reply_to": str(m.get("reply_to") or ""),
        "score": str(m.get("score") or 0),
        "reply_count": str(m.get("reply_count") or 0),
        "title": (m.get("title") or "")[:200],
        "n_urls": str(len(urls)),
        "urls": ",".join(sorted(set(urls))[:10]),
        "msg_len": str(len(m.get("body") or "")),
    }
    return tags, body[:400].replace("\n", " "), labels


def iter_messages():
    seen = set()
    for name in ("raw/messages.jsonl", "raw/threads.jsonl"):
        p = os.path.join(D, name)
        if not os.path.exists(p):
            continue
        with open(p) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                m = json.loads(line)
                mid = m.get("id")
                if mid in seen:
                    continue
                seen.add(mid)
                yield m


def build_docs():
    docs = {}
    for m in iter_messages():
        tags, desc, labels = classify(m)
        docs[f"tn:{m['id']}"] = {
            "@timestamp": m.get("created_at") or NOW,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "forum_message",
            "description": desc,
            "source_url": m.get("read_url") or f"https://tantive.space/api/messages/{m['id']}",
            "observer": OBSERVER,
            "tags": tags,
            "labels": labels,
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
    # bulk in 1000-doc chunks
    errs = 0
    for i in range(0, len(lines), 2000):
        chunk = lines[i:i + 2000]
        r = req("POST", "/_bulk", raw="\n".join(chunk) + "\n")
        errs += len([x for x in r.get("items", []) if x.get("index", {}).get("error")])
    print(f"bulk: {len(docs)} docs, errors: {errs}")


def verify():
    r = req("POST", f"/{INDEX}/_search",
            {"size": 0, "aggs": {
                "tags": {"terms": {"field": "tags", "size": 50}},
                "kinds": {"terms": {"field": "record_kind"}}}})
    print("total:", r["hits"]["total"]["value"])
    for b in r["aggregations"]["tags"]["buckets"]:
        print(f"  {b['key']}: {b['doc_count']}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--verify"
    {"--create": create_index, "--load": load, "--verify": verify}[mode]()
