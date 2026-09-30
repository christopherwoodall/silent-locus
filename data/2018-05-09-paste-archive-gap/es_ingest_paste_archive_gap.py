#!/usr/bin/env python3
"""Ingest the lane-M paste-archive-gap dataset into its own `paste-archive-gap` index.

Conforms to the shared schema (notes/gems-es-mapping.json) — one ES doc per
recovered paste (15 anna.fyi) + census-diff + proxy-ladder-crossref docs.
Dataset-specific fields live in flattened `labels`. No new top-level fields.

Usage:
  python3 es_ingest_paste_archive_gap.py --create
  python3 es_ingest_paste_archive_gap.py --load
  python3 es_ingest_paste_archive_gap.py --verify
"""
import sys, json, os, hashlib
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
import urllib.request

ES = os.environ.get("SWARMTRACES_ES_URL", "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443")
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # script lives in data/<collection>/
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
D = BASE + "/data/2018-05-09-paste-archive-gap"
INDEX = "2018-05-09-paste-archive-gap"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "paste-archive-gap-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}
TS = "2026-09-28T04:30:00Z"


def req(method, path, body=None):
    r = urllib.request.Request(ES + path,
                               data=json.dumps(body).encode() if body is not None else None,
                               method=method)
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


def build_docs():
    docs = {}
    manifest = json.load(open(f"{D}/raw/manifest.json"))
    for m in manifest:
        if m.get("id") == "b3746a9f_decoded":
            continue
        pid = m["id"]
        body = open(f"{D}/raw/bodies/anna.fyi/{pid}.txt").read()
        tags = ["host:anna.fyi", f"body:{m['status']}"]
        title = m.get("title") or ""
        if title.startswith("Statistical reference") or title.startswith("Re: "):
            tags.append("content:statistical-reference-series")
        if "cemetery" in title.lower() or "VG_CEMETERY" in title:
            tags.append("content:cemetery-dataset")
        if "ChatGPT" in title or "human-requested" in title.lower():
            tags.append("content:human-requested-inquiry")
        if "ASTER-BRIDGE" in title:
            tags.append("content:agent-directed-relay")
        desc = (f"anna.fyi paste '{title}' by {m.get('author','')}. "
                f"Created {m.get('created_utc')}. Status: {m['status']}. "
                f"Recovered 2026-09-28 via /view/raw (Lane M gap recovery).")
        doc = {
            "@timestamp": m.get("created_utc") or TS,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "paste_text", "description": desc,
            "source_url": m["source_url"], "observer": OBSERVER,
            "tags": tags, "file": pid + ".txt",
            "sha256": m.get("sha256"), "size_bytes": m.get("bytes"),
            "labels": {"paste_id": pid, "host": "anna.fyi", "title": title,
                       "author": m.get("author", ""), "body_status": m["status"],
                       "lane": "M", "recovery_method": "view_raw_endpoint"},
        }
        if m["status"] == "body_ok" and m["bytes"] < 20000:
            doc["description"] = body
        docs[f"paste-archive-gap:anna:{pid}"] = doc
    # decoded cemetery dataset doc
    cem = next(m for m in manifest if m.get("id") == "b3746a9f_decoded")
    docs["paste-archive-gap:dataset:vg-cemetery"] = {
        "@timestamp": TS,
        "event": {"dataset": INDEX, "created": NOW},
        "record_kind": "dataset",
        "description": ("Decoded agent-posted dataset VG_CEMETERY_PERSON_MOST_ULTRABULK "
                        f"v0.77 ({cem['rows']} rows Czech cemetery records, generated "
                        f"{cem['generated_at']}). Posted to anna.fyi as base64 gzip by "
                        "'Abrupt Bison' (adjective-animal author naming). Local file "
                        "vg_cemetery_person_v0_77.json."),
        "source_url": "https://anna.fyi/view/raw/b3746a9f",
        "observer": OBSERVER,
        "tags": ["host:anna.fyi", "content:cemetery-dataset", "task-family:public-records-scraping"],
        "file": "vg_cemetery_person_v0_77.json", "sha256": cem["sha256"],
        "size_bytes": cem["bytes"],
        "labels": {"dataset_kind": cem["kind"], "rows": str(cem["rows"]),
                   "generated_at": cem["generated_at"], "paste_id": "b3746a9f",
                   "author": "Abrupt Bison", "lane": "M"},
    }
    # census diff doc
    docs["paste-archive-gap:census:anna-fyi"] = {
        "@timestamp": TS,
        "event": {"dataset": INDEX, "created": NOW},
        "record_kind": "census_diff",
        "description": ("termina.digital DB claims 136 anna.fyi pastes lifetime "
                        "(60 NSI series); we hold 55 (48 Statistical reference 1-48, "
                        "2 untitled NSI, 2 NSI-table, ReplyLink0/1/2, Official data link). "
                        "The 136-ID listing is investigator-held and unpublished "
                        "(data/leads/live-2026-09-05b/anna); live /api/recent returns only "
                        "the 15 most recent (no pagination); Wayback holds homepage captures "
                        "only; investigator tarball is a placeholder. Gap: NSI series ~49-60, "
                        "05-12 TED archive paste, 9 post-disclosure visitors, pre-disclosure "
                        "human pastes."),
        "source_url": "https://swarm.termina.digital/db/venue/anna-fyi.html",
        "observer": OBSERVER,
        "tags": ["venue:anna.fyi", "census:gap-open"],
        "labels": {"db_claim_lifetime": "136", "db_claim_nsi_series": "60",
                   "held_by_us": "55", "held_nsi": "50", "recovered_lane_m": "15",
                   "gap_status": "historical_ids_unpublished", "lane": "M"},
    }
    # proxy ladder crossref docs
    xref = json.load(open(f"{D}/raw/proxy_ladder_crossref.json"))
    for x in xref:
        if not x["in_rmn_re"]:
            continue
        uid = hashlib.sha256(x["actor_url"].encode()).hexdigest()[:12]
        docs[f"paste-archive-gap:ladder:{uid}"] = {
            "@timestamp": TS,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "proxy_ladder_overlap",
            "description": ("Actor-page (termina.digital DB) proxy-ladder URL also present "
                            f"in rmn.re shortener: {x['actor_url']} — rmn.re slugs: "
                            f"{', '.join(x['rmn_re_slugs'][:6])}."),
            "source_url": "https://swarm.termina.digital/db/actor/",
            "observer": OBSERVER,
            "tags": ["proxy-ladder", "corpus:rmn-re", "corpus:termina-digital"],
            "labels": {"actor_url": x["actor_url"][:500],
                       "rmn_re_slugs": ",".join(x["rmn_re_slugs"][:6]),
                       "lane": "M"},
        }
    docs["paste-archive-gap:ladder:cors-bwa"] = {
        "@timestamp": TS,
        "event": {"dataset": INDEX, "created": NOW},
        "record_kind": "proxy_primitive",
        "description": ("NEW shared proxy primitive identified in Lane M: "
                        "cors.bwa.workers.dev appears in 8 termina.digital DB actor-page "
                        "URLs AND in rmn.re decoded targets. Not previously flagged in "
                        "either corpus sweep."),
        "observer": OBSERVER,
        "tags": ["proxy-primitive:new", "host:cors.bwa.workers.dev"],
        "labels": {"host": "cors.bwa.workers.dev", "actor_page_hits": "8",
                   "in_rmn_re": "true", "lane": "M"},
    }
    # workstream C3 recovery check (2026-09-28): /api/recent re-pull
    docs["paste-archive-gap:repull:2026-09-28"] = {
        "@timestamp": TS,
        "event": {"dataset": INDEX, "created": NOW},
        "record_kind": "recovery_check",
        "description": ("Workstream C3 re-pull of https://anna.fyi/api/recent "
                        "(2026-09-28 ~11:30 UTC): the 15 most recent pastes are "
                        "identical to the 15 already recovered in Lane M (same pids, "
                        "same order) — zero new pastes since the Lane M pull. The 81 "
                        "historical IDs remain investigator-held and unpublished "
                        "(termina.digital DB's held anna.fyi listing); /api/recent "
                        "accepts no pagination params, Wayback holds homepage captures "
                        "only. Gap still open."),
        "source_url": "https://anna.fyi/api/recent",
        "observer": OBSERVER,
        "tags": ["venue:anna.fyi", "gap:still-open", "recovery-check"],
        "labels": {"recent_ids_returned": "15", "new_pastes": "0",
                   "gap_status": "historical_ids_unpublished", "lane": "M",
                   "workstream": "C3"},
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
    req_obj = urllib.request.Request(ES + "/_bulk", data=payload.encode(), method="POST")
    req_obj.add_header("Content-Type", "application/x-ndjson")
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        _es_user = os.environ.get("ES_USER")
        if _es_user:
            import base64 as _b64
            req_obj.add_header("Authorization", "Basic " + _b64.b64encode(
                f"{_es_user}:{os.environ.get('ES_PASS', '')}".encode()).decode())
    else:
        add_surrogate_to_request(req_obj, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(req_obj, timeout=300) as resp:
        res = read_json_response(resp)
    print("bulk:", res.get("errors"), "items:", len(res.get("items", [])))
    errs = [i for i in res.get("items", []) if i.get("index", {}).get("status") not in (200, 201)]
    for e in errs[:5]:
        print("ERR:", json.dumps(e)[:300])


def verify():
    r = req("GET", f"/{INDEX}/_count")
    print("count:", r.get("count"))
    r = req("GET", f"/{INDEX}/_mapping")
    tops = set(r[INDEX]["mappings"]["properties"].keys())
    canon = set(json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]["properties"].keys())
    print("extra top-level fields:", tops - canon)
    r = req("POST", f"/{INDEX}/_search",
            {"size": 0, "aggs": {"kinds": {"terms": {"field": "record_kind.keyword"}}}})
    print("kinds:", [(b["key"], b["doc_count"]) for b in r["aggregations"]["kinds"]["buckets"]])


if __name__ == "__main__":
    if "--create" in sys.argv:
        create_index()
    elif "--load" in sys.argv:
        load()
    elif "--verify" in sys.argv:
        verify()
    else:
        print("usage: --create|--load|--verify")
