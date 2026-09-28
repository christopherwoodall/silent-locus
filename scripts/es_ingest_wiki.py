#!/usr/bin/env python3
"""Ingest the collusion.wiki corpus into the `collusion-wiki` Elastic index.

Conforms to the shared schema (notes/gems-es-mapping.json) — wiki concepts
map onto existing fields; wiki-specific detail lives in `labels` (flattened)
+ `tags`. No new top-level fields. Schema gaps are documented in
notes/collusion-wiki-schema-2026-09-27.md, not silently extended.

Incremental: each dump type bulk-loads independently and its doc count is
confirmed in the index before moving on.

Usage:
  python3 es_ingest_wiki.py --only labels     # one dump type
  python3 es_ingest_wiki.py --all             # all types in dependency order
  python3 es_ingest_wiki.py --verify          # counts per record_kind only

Dump types: labels pages events links records revisions shortener other bridge
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
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
WIKI = BASE + "/data/collusion-wiki"
INDEX = "collusion-wiki"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "collusion-wiki-export", "vendor": "nightingale-collective",
            "type": "dataset"}
DOWNLOAD = "https://collusion.wiki/explorer/download"


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


def proxy_family(host):
    h = (host or "").lower()
    if "jina.ai" in h or h.startswith("r-jina") or "jina" in h:
        return "jina"
    if "translate.goog" in h or "translate.google" in h:
        return "translate"
    if "hf.space" in h:
        return "hf-space"
    return "other"


def page_url(page_key):
    return "https://collusion.wiki/explorer/page/%s" % page_key


def flat(d):
    """stringify a dict into labels-safe flat values"""
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


def base_doc(kind, ts):
    doc = {
        "record_kind": kind,
        "event": {"dataset": INDEX, "created": NOW},
        "observer": dict(OBSERVER),
        "retrieved_via": DOWNLOAD,
        "tags": ["source:collusion-wiki"],
        "labels": {"annotated_by": "es_ingest_wiki"},
    }
    if ts:
        doc["@timestamp"] = ts
    return doc


def load_labels():
    docs = {}
    for line in open(WIKI + "/labels.jsonl"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        label = r.get("label") or ""
        doc = base_doc("wiki_label", r.get("last_write") or r.get("first_write"))
        doc["authors"] = [label] if label else []
        doc["tags"] += grammar_tags(label)
        for w in r.get("wikis") or []:
            doc["tags"].append("wiki:" + w)
        doc["labels"].update(flat({
            "label": label, "wikis": r.get("wikis"),
            "stored_revisions": r.get("stored_revisions"),
            "stored_revision_pages": r.get("stored_revision_pages"),
            "stored_revision_ip16": r.get("stored_revision_ip16"),
            "save_requests": r.get("save_requests"),
            "save_request_ip16": r.get("save_request_ip16"),
            "is_human_handle": r.get("is_human_handle"),
            "first_write": r.get("first_write"),
        }))
        docs["wiki:label:%s" % (label or "empty-%d" % len(docs))] = doc
    return docs


def load_pages():
    docs = {}
    for line in open(WIKI + "/pages.jsonl"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        doc = base_doc("wiki_page", r.get("last_write"))
        doc["source_url"] = page_url(r.get("page_key"))
        doc["authors"] = r.get("labels") or []
        doc["tags"] += ["wiki:" + r.get("wiki")] + grammar_tags(r.get("name"))
        doc["labels"].update(flat({
            "page_key": r.get("page_key"), "wiki": r.get("wiki"),
            "name": r.get("name"), "bucket": r.get("bucket"),
            "page_family": r.get("page_family"),
            "page_family_confidence": r.get("page_family_confidence"),
            "n_revs": r.get("n_revs"), "body_bytes": r.get("body_bytes"),
            "deleted_live": r.get("deleted_live"),
            "n_deletions": r.get("n_deletions"),
            "n_recreations": r.get("n_recreations"),
            "n_ip16": r.get("n_ip16"), "first_write": r.get("first_write"),
        }))
        docs["wiki:page:%s" % r.get("page_key")] = doc
    return docs


def load_events():
    docs = {}
    for line in open(WIKI + "/events.jsonl"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        doc = base_doc("wiki_event", r.get("time"))
        doc["tags"] += ["event:" + r.get("event_type")]
        doc["labels"].update(flat({
            "event_id": r.get("event_id"), "event_type": r.get("event_type"),
            "ip16": r.get("ip16"), "request_action": r.get("request_action"),
            "param_family": r.get("param_family"),
            "time_grade": r.get("time_grade"),
            "success_observed": r.get("success_observed"),
            "source_refs": r.get("source_refs"),
        }))
        docs["wiki:event:%s" % r.get("event_id")] = doc
    return docs


def load_links():
    docs = {}
    for line in open(WIKI + "/links.jsonl"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        url = r.get("url") or ""
        host = r.get("host") or ""
        doc = base_doc("wiki_link", None)
        if not r.get("url_withheld") and url and not url.startswith("http://..."):
            doc["external_links"] = [url]
        fam = proxy_family(host)
        doc["tags"] += ["proxy:" + fam]
        doc["labels"].update(flat({
            "host": host, "relation": r.get("relation"),
            "followed": r.get("followed"),
            "record_id_count": len(r.get("record_ids") or []),
            "url_withheld": r.get("url_withheld"),
            "proxy_family": fam,
        }))
        uid = hashlib.sha256(url.encode()).hexdigest()[:16]
        docs["wiki:link:%s" % uid] = doc
    return docs


def norm_ts(v):
    """records' source_date_literal is ISO, bare epoch, or the literal 'current'"""
    if not v:
        return None
    v = str(v).strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}T", v):
        return v
    if re.match(r"^\d{9,10}$", v):
        try:
            return datetime.fromtimestamp(int(v), tz=timezone.utc).isoformat().replace("+00:00", "Z")
        except Exception:
            return None
    return None


def load_records():
    docs = {}
    no_ts = 0
    for line in open(WIKI + "/records.jsonl"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        ts = None
        raw_ts = None
        for o in r.get("origins") or []:
            if o.get("source_date_literal"):
                raw_ts = o["source_date_literal"]
                ts = norm_ts(raw_ts)
                if ts:
                    break
        if not ts:
            no_ts += 1
        doc = base_doc("wiki_record", ts)
        if not r.get("body_withheld") and r.get("text"):
            doc["description"] = r["text"][:20000]
        kinds = sorted({o.get("kind") for o in r.get("origins") or [] if o.get("kind")})
        for k in kinds:
            doc["tags"].append("recordkind:" + k)
        first = (r.get("origins") or [{}])[0]
        if first.get("url"):
            doc["source_url"] = first["url"]
        doc["labels"].update(flat({
            "record_id": r.get("id"), "authorship": r.get("authorship"),
            "selection_basis": r.get("selection_basis"),
            "body_withheld": r.get("body_withheld"),
            "hosting_text_changed": r.get("hosting_text_changed"),
            "origin_kinds": kinds,
            "origin_sites": sorted({o.get("site") for o in r.get("origins") or []
                                    if o.get("site")}),
            "sha256": r.get("source_text_sha256"),
            "source_date_literal_raw": str(raw_ts) if raw_ts else None,
        }))
        docs["wiki:record:%s" % r.get("id")] = doc
    print("records without timestamp: %d" % no_ts)
    return docs


def load_revisions():
    docs = {}
    for line in open(WIKI + "/revisions.jsonl"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        doc = base_doc("wiki_revision",
                       r.get("write_date") or r.get("time"))
        doc["source_url"] = page_url(r.get("page_key"))
        if r.get("label"):
            doc["authors"] = [r["label"]]
        if r.get("change_summary"):
            doc["note"] = r["change_summary"]
        if r.get("body"):
            doc["description"] = r["body"][:20000]
        doc["tags"] += ["wiki:" + r.get("wiki")] + grammar_tags(r.get("name"))
        doc["labels"].update(flat({
            "rev_id": r.get("rev_id"), "page_key": r.get("page_key"),
            "name": r.get("name"), "seq": r.get("seq"),
            "ip16": r.get("ip16"), "time_grade": r.get("time_grade"),
            "body_sha256": r.get("body_sha256"),
            "body_len": r.get("body_len"), "lines": r.get("lines"),
            "request_action": r.get("request_action"),
            "diff_base_reason": r.get("diff_base_reason"),
            "uncertainty_seconds": r.get("uncertainty_seconds"),
        }))
        docs["wiki:revision:%s" % r.get("rev_id")] = doc
    return docs


def load_shortener():
    docs = {}
    sl = json.load(open(WIKI + "/shortener-logs.json"))
    for site in sl.get("sites", []):
        for link in site.get("links", []):
            url = link.get("url") or ""
            host = re.sub(r"^https?://", "", url).split("/")[0].lower()
            doc = base_doc("wiki_shortener", link.get("time"))
            doc["external_links"] = [url]
            fam = proxy_family(host)
            doc["tags"] += ["proxy:" + fam, "shortener:rmn.re"]
            if link.get("keyword"):
                doc["tags"] += grammar_tags(link["keyword"])
            doc["labels"].update(flat({
                "keyword": link.get("keyword"), "title": link.get("title"),
                "host": host, "proxy_family": fam,
                "ip16": link.get("ip16"), "clicks": link.get("clicks"),
                "shortener": "rmn.re",
            }))
            docs["wiki:shortener:%s" % link.get("keyword")] = doc
    return docs


def load_other():
    docs = {}
    ow = json.load(open(WIKI + "/other-wikis.json"))
    for p in ow.get("pages", []):
        revs = p.get("revisions", [])
        for rv in revs:
            doc = base_doc("wiki_other_page", rv.get("time"))
            added = rv.get("added") or []
            if added:
                doc["description"] = "\n".join(added)[:20000]
            doc["tags"] += ["wiki:" + p.get("wiki")]
            doc["labels"].update(flat({
                "page_key": p.get("page_key"), "wiki": p.get("wiki"),
                "name": p.get("name"), "seq": rv.get("seq"),
                "ip16": rv.get("ip16"), "time_grade": rv.get("time_grade"),
                "added_lines": len(added),
                "removed_lines": len(rv.get("removed") or []),
            }))
            docs["wiki:other:%s@%s" % (p.get("page_key"), rv.get("seq"))] = doc
    return docs


def load_bridge():
    docs = {}
    b = json.load(open(BASE + "/data/wiki_gem_bridge.json"))
    for g in b.get("gem_metadata_records", []):
        gem = g.get("gem")
        meta = g.get("meta", {})
        home = meta.get("homepage_uri") or ""
        host = ""
        m = re.search(r"host=([A-Za-z0-9.\-]+)", home)
        if m:
            host = m.group(1).lower()  # redaction placeholder carries the host
        elif home and not home.startswith("[operational"):
            host = re.sub(r"^https?://", "", home).split("/")[0].lower()
        doc = base_doc("wiki_bridge", "2026-06-18T00:00:00Z")
        doc["gem"] = gem
        doc["package"] = gem
        doc["version"] = meta.get("version")
        doc["published_at"] = "2026-06-18T00:00:00Z"
        doc["wave"] = "june-18"
        doc["status"] = "dead"
        if home and not home.startswith("[operational"):
            doc["meta_homepage"] = home
        doc["meta_summary"] = meta.get("info")
        doc["source_url"] = meta.get("project_uri")
        doc["tags"] += ["wiki:bridge", "wave:june-18", "status:dead",
                        "corpus:jfrog_overlap", "proxy:" + proxy_family(host)]
        doc["labels"].update(flat({
            "gem": gem, "homepage_host": host,
            "proxy_family": proxy_family(host),
            "bridge_source": "collusion-wiki records.jsonl registry_metadata",
            "in_jfrog_inventory": True,
        }))
        docs["wiki:bridge:%s" % gem] = doc
    return docs


LOADERS = {
    "labels": load_labels, "pages": load_pages, "events": load_events,
    "links": load_links, "records": load_records, "revisions": load_revisions,
    "shortener": load_shortener, "other": load_other, "bridge": load_bridge,
}
ORDER = ["labels", "pages", "events", "links", "records", "revisions",
         "shortener", "other", "bridge"]


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


def count_kind(kind):
    req("POST", "/%s/_refresh" % INDEX)
    r = req("POST", "/%s/_count" % INDEX, {"query": {"term": {"record_kind": kind}}})
    return r.get("count", 0)


def ingest_one(name):
    kind = {"labels": "wiki_label", "pages": "wiki_page", "events": "wiki_event",
            "links": "wiki_link", "records": "wiki_record",
            "revisions": "wiki_revision", "shortener": "wiki_shortener",
            "other": "wiki_other_page", "bridge": "wiki_bridge"}[name]
    docs = LOADERS[name]()
    ok, fail = bulk_load(docs)
    n = count_kind(kind)
    print("ingest %s: built=%d ok=%d fail=%d index_count=%d %s" %
          (name, len(docs), ok, fail, n, "MATCH" if n == len(docs) else "MISMATCH"))
    return n == len(docs)


def verify():
    total = req("GET", "/%s/_count" % INDEX)["count"]
    print("collusion-wiki total docs:", total)
    for name in ORDER:
        kind = {"labels": "wiki_label", "pages": "wiki_page", "events": "wiki_event",
                "links": "wiki_link", "records": "wiki_record",
                "revisions": "wiki_revision", "shortener": "wiki_shortener",
                "other": "wiki_other_page", "bridge": "wiki_bridge"}[name]
        print("  %-14s %d" % (kind, count_kind(kind)))


def main():
    if "--verify" in sys.argv:
        verify()
        return
    ensure_index()
    if "--all" in sys.argv:
        names = ORDER
    elif "--only" in sys.argv:
        names = [sys.argv[sys.argv.index("--only") + 1]]
    else:
        print("usage: --all | --only <type> | --verify")
        return
    bad = 0
    for name in names:
        if not ingest_one(name):
            bad += 1
    print("done, mismatches:", bad)


if __name__ == "__main__":
    main()
