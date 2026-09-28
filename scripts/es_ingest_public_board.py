#!/usr/bin/env python3
"""Ingest the public-board.com dataset into its own `public-board` index.

Conforms to the shared schema (notes/gems-es-mapping.json) — one ES doc per
board note (861), dataset detail in `labels` (flattened) + `tags`.
No new top-level fields.

Usage:
  python3 es_ingest_public_board.py --create
  python3 es_ingest_public_board.py --load
  python3 es_ingest_public_board.py --verify
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
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
D = BASE + "/data/public-board"
INDEX = "public-board"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "public-board-ingest", "vendor": "swarmtraces-hunt",
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
    ("ref:collusion-wiki", re.compile(r"collusion\.wiki", re.I)),
    ("ref:swarm-research", re.compile(r"swarm-ai-research|WikiAgentSwarmInvestigation", re.I)),
    ("ref:thecolony", re.compile(r"thecolony\.ai", re.I)),
    ("ref:tantive", re.compile(r"tantive\.space", re.I)),
    ("ref:secgov", re.compile(r"sec\.gov", re.I)),
    ("topic:fips", re.compile(r"\bfips\b", re.I)),
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


def classify(n):
    msg = n.get("msg", "")
    tags = ["status:live"]
    if n.get("admin"):
        tags.append("role:operator")
    if n.get("re"):
        tags.append("kind:reply")
    else:
        tags.append("kind:note")
    for tag, rx in GRAMMARS:
        if rx.search(msg):
            tags.append(tag)
    urls = re.findall(r"https?://[^\s)>\]]+", msg)
    desc = msg[:400].replace("\n", " ")
    labels = {
        "note_id": n["id"],
        "ts": n["ts"],
        "reply_to": n.get("re") or "",
        "admin_signed": str(bool(n.get("admin"))),
        "trust": n.get("trust", ""),
        "n_urls": str(len(urls)),
        "urls": ",".join(sorted(set(urls))[:10]),
        "msg_len": str(len(msg)),
    }
    return tags, desc, labels


def build_docs():
    docs = {}
    with open(f"{D}/notes.jsonl") as f:
        for line in f:
            n = json.loads(line)
            tags, desc, labels = classify(n)
            docs[f"pb:{n['id']}"] = {
                "@timestamp": n["ts"],
                "event": {"dataset": INDEX, "created": NOW},
                "record_kind": "board_note",
                "description": desc,
                "source_url": f"https://public-board.com/t/{n['id']}",
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
    r = req("POST", "/_bulk", raw="\n".join(lines) + "\n")
    errs = [i for i in r.get("items", []) if i.get("index", {}).get("error")]
    print(f"bulk: {len(docs)} docs, errors: {len(errs)}")
    for e in errs[:3]:
        print(json.dumps(e)[:300])


def verify():
    r = req("POST", f"/{INDEX}/_search",
            {"size": 0, "aggs": {
                "tags": {"terms": {"field": "tags", "size": 40}},
                "kinds": {"terms": {"field": "record_kind"}}}})
    print("total:", r["hits"]["total"]["value"])
    for b in r["aggregations"]["tags"]["buckets"]:
        print(f"  {b['key']}: {b['doc_count']}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--verify"
    {"--create": create_index, "--load": load, "--verify": verify}[mode]()
