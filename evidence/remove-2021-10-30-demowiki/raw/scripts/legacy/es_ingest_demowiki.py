#!/usr/bin/env python3
"""Ingest the DemoWiki corpus into the `demowiki` Elastic index.

Source: read-only crawl of prowiki.org/demo/wiki.cgi (data/2021-10-30-demowiki/raw/demowiki_crawl.json).
Conforms to the shared schema (notes/gems-es-mapping.json); wiki concepts map
onto existing fields; wiki-specific detail lives in `labels` (flattened) +
`tags`. No new top-level fields.

Usage: python3 es_ingest_demowiki.py --all | --verify
"""
import sys, json, re, hashlib, urllib.request
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
# Moved into the collection dir 2026-09-28 (per build-script convention):
# self-locating paths so the script runs from anywhere.
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
WIKI = HERE
INDEX = "2021-10-30-demowiki"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "demowiki-crawl", "vendor": "swarmtraces-hunt",
            "type": "research-crawl"}
CRAWL_URL = "https://prowiki.org/demo/wiki.cgi"


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


def grammar_tags(name):
    tags = []
    n = (name or "")
    nl = n.lower()
    if nl.startswith("zz"):
        tags.append("grammar:zz")
    if re.search(r"\d{10}", n):
        tags.append("grammar:epoch10")
    if "oai" in nl:
        tags.append("grammar:oai")
    if "999" in n:
        tags.append("grammar:999")
    return tags


def proxy_family(url):
    h = (url or "").lower()
    if "jina.ai" in h:
        return "jina"
    if "datausa.io" in h:
        return "datausa"
    if "public-board.com" in h:
        return "agent-board"
    if "translate.goog" in h or "translate.google" in h:
        return "translate"
    return "other"


def flat(d):
    out = {}
    for k, v in d.items():
        if v is None:
            continue
        if isinstance(v, bool):
            out[k] = "true" if v else "false"
        elif isinstance(v, (list, tuple)):
            out[k] = ", ".join(str(x) for x in v[:20])
        else:
            out[k] = str(v)
    return out


def rc_ts(entry):
    """rc_day like '16. Juni 2026' + time_str '20:28' -> ISO"""
    day = entry.get("rc_day") or ""
    tm = entry.get("time_str") or "00:00"
    months = {"Januar": 1, "Februar": 2, "März": 3, "April": 4, "Mai": 5,
              "Juni": 6, "Juli": 7, "August": 8, "September": 9,
              "Oktober": 10, "November": 11, "Dezember": 12}
    m = re.match(r"(\d{1,2})\.\s*(\w+)\s*(\d{4})", day)
    if not m:
        return None
    try:
        return datetime(int(m.group(3)), months[m.group(2)], int(m.group(1)),
                        int(tm.split(":")[0]), int(tm.split(":")[1]),
                        tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception:
        return None


def base_doc(kind, ts):
    doc = {
        "record_kind": kind,
        "event": {"dataset": INDEX, "created": NOW},
        "observer": dict(OBSERVER),
        "retrieved_via": CRAWL_URL,
        "tags": ["source:demowiki", "wiki:demo"],
        "labels": {"annotated_by": "es_ingest_demowiki"},
    }
    if ts:
        doc["@timestamp"] = ts
    return doc


def build():
    c = json.load(open(WIKI + "/raw/demowiki_crawl.json"))
    docs = {}
    # wiki_page docs
    for p in c.get("pages", []):
        pid = p["page_id"]
        urls = re.findall(r"https?://[^\s'\"]+", p.get("body_text") or "")
        doc = base_doc("wiki_page", None)
        doc["source_url"] = "%s?%s" % (CRAWL_URL, pid)
        if p.get("body_text"):
            doc["description"] = p["body_text"][:20000]
        if urls:
            doc["external_links"] = urls
            fams = {proxy_family(u) for u in urls}
            doc["tags"] += ["proxy:" + f for f in fams]
        doc["tags"] += grammar_tags(pid)
        doc["labels"].update(flat({
            "page_id": pid, "wiki": "demo", "body_sha256": p.get("body_sha256"),
            "n_external_urls": len(urls), "body_text_head": (p.get("body_text") or "")[:500],
        }))
        docs["demowiki:page:%s" % pid] = doc
    # wiki_revision docs from RC entries + diff text
    # NOTE: OddMuse diff=N renders the last N changes of a page, not revision N,
    # so multiple RC entries for one page share a diff view. Each RC entry still
    # gets its own doc (unique _id) under the keep-all policy.
    diff_by_rev = {}
    for d in c.get("diffs", []):
        diff_by_rev[(d["page_id"], d["rev"])] = d
    n_rev = 0
    for e in c.get("rc_entries", []):
        pid, rev = e.get("page_id"), e.get("diff_rev")
        if not pid or rev is None:
            continue
        n_rev += 1
        ts = rc_ts(e)
        doc = base_doc("wiki_revision", ts)
        doc["source_url"] = "%s?%s" % (CRAWL_URL, pid)
        if e.get("author"):
            doc["authors"] = [e["author"]]
        if e.get("summary"):
            doc["note"] = e["summary"]
        d = diff_by_rev.get((pid, rev))
        if d and d.get("diff_text"):
            doc["description"] = d["diff_text"][:20000]
        doc["tags"] += grammar_tags(pid) + grammar_tags(e.get("author"))
        doc["labels"].update(flat({
            "page_id": pid, "wiki": "demo", "rev": rev,
            "author": e.get("author"), "summary": e.get("summary"),
            "rc_day": e.get("rc_day"),
            "is_agent_handle": (e.get("author") or "") in
                ("AgentResearchTest", "OpenAIDataBridge", "AgentNameX", "CollusionWikiTest"),
        }))
        docs["demowiki:rev:%s@%s#%d" % (pid, rev, n_rev)] = doc
    # wiki_link docs for external URLs
    seen = set()
    for p in c.get("pages", []):
        for u in re.findall(r"https?://[^\s'\"]+", p.get("body_text") or ""):
            if u in seen:
                continue
            seen.add(u)
            host = re.sub(r"^https?://", "", u).split("/")[0].lower()
            doc = base_doc("wiki_link", None)
            doc["external_links"] = [u]
            fam = proxy_family(u)
            doc["tags"] += ["proxy:" + fam]
            doc["labels"].update(flat({
                "host": host, "proxy_family": fam, "source_page": p["page_id"],
            }))
            uid = hashlib.sha256(u.encode()).hexdigest()[:16]
            docs["demowiki:link:%s" % uid] = doc
    # cross-corpus bridge doc
    cross = [
        {"handle": "AgentResearchTest", "wikis": ["dse"], "revs": 3,
         "first": "2026-06-16T18:35:52Z", "demo_activity": "2026-06-16"},
        {"handle": "OpenAIDataBridge", "wikis": ["dse", "probier"], "revs": 22,
         "first": "2026-06-16T09:42:32Z", "demo_activity": "2026-06-16"},
        {"handle": "AgentResearchTestName", "wikis": ["dse"], "revs": 1,
         "first": "2026-06-17T03:05:17Z", "demo_activity": None},
        {"handle": "AgentNameX", "wikis": [], "revs": 0,
         "first": None, "demo_activity": "2026-06-22"},
    ]
    for x in cross:
        doc = base_doc("wiki_bridge", "2026-06-16T00:00:00Z")
        doc["authors"] = [x["handle"]]
        doc["tags"] += ["wiki:bridge", "bridge:collusion-wiki"] + grammar_tags(x["handle"])
        doc["labels"].update(flat({
            "handle": x["handle"], "collusion_wiki_wikis": x["wikis"],
            "collusion_wiki_revisions": x["revs"],
            "collusion_wiki_first_write": x["first"],
            "demowiki_activity": x["demo_activity"],
            "bridge_source": "collusion-wiki labels.jsonl grep",
        }))
        docs["demowiki:bridge:%s" % x["handle"]] = doc
    return docs


def ensure_index():
    try:
        req("GET", "/%s" % INDEX)
        print("index exists:", INDEX)
        return
    except Exception:
        pass
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
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


def main():
    if "--verify" in sys.argv:
        req("POST", "/%s/_refresh" % INDEX)
        total = req("GET", "/%s/_count" % INDEX)["count"]
        print(INDEX, "total:", total)
        return
    ensure_index()
    docs = build()
    ok, fail = bulk_load(docs)
    req("POST", "/%s/_refresh" % INDEX)
    n = req("GET", "/%s/_count" % INDEX)["count"]
    print("built=%d ok=%d fail=%d index_count=%d %s" %
          (len(docs), ok, fail, n, "MATCH" if n == len(docs) else "MISMATCH"))


if __name__ == "__main__":
    main()
