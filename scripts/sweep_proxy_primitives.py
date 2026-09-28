#!/usr/bin/env python3
"""Lane F — proxy-primitive sweep (2026-09-27).

Hunts longcat's 207-domain-audit primitives across:
  (a) the collusion-wiki Elastic index (read-only regexp/wildcard queries)
  (b) local corpus files (gem corpus JSONL/CSV + wiki pivot products)

Primitives: pure.md, api.cors.lol, corsmirror.com, Google Docs Viewer gview.
Catches URL-encoded variants (pure%2Emd, pure%252Emd, etc.).

Output: data/proxy-primitives/hits.jsonl (normalized, exact-dup collapsed)
        data/proxy-primitives/PROVENANCE.md
        data/proxy-primitives/progress.log
"""
import sys, json, re, hashlib, subprocess, urllib.request
from datetime import datetime, timezone
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
DATA = BASE + "/data"
OUT = DATA + "/proxy-primitives"
INDEX = "collusion-wiki"
NOW = datetime.now(timezone.utc).isoformat()

# primitive -> (plain fragment, encoded-variant fragments)
PRIMS = {
    "pure.md":       ["pure.md", "pure%2emd", "pure%252emd", "pure%2Emd"],
    "api.cors.lol":  ["api.cors.lol", "cors.lol", "cors%2elol", "cors%252elol"],
    "corsmirror.com":["corsmirror", "corsmirror%2ecom"],
    "gview":         ["gview", "docs.google.com/gview", "docs.google.com/viewer"],
}

def log(msg):
    line = "%s %s" % (datetime.now(timezone.utc).isoformat(), msg)
    print(line, flush=True)
    with open(OUT + "/progress.log", "a") as f:
        f.write(line + "\n")

def req(method, path, body=None):
    url = ES + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=300) as resp:
        return read_json_response(resp)

def es_sweep():
    """Regexp on keyword fields + wildcard query_string on text fields."""
    hits = []
    for prim, frags in PRIMS.items():
        # build a regexp alternation that tolerates dot / %2e / %252e separators
        alts = []
        for f in frags:
            esc = re.escape(f)
            esc = esc.replace(r"\.\.", r"\.")
            alts.append(esc.replace("%2e", r"(%2e|%2E|%252e|%252E|\.)"))
        rx = "(?i).*(%s).*" % "|".join(alts)
        q = {
            "size": 1000,
            "query": {"bool": {"should": [
                {"regexp": {"matched_string": {"value": rx}}},
                {"regexp": {"external_links": {"value": rx}}},
                {"query_string": {
                    "query": " OR ".join("*%s*" % f for f in frags),
                    "fields": ["note", "meta_description", "meta_summary",
                               "matched_string.text"],
                    "analyze_wildcard": True, "lenient": True,
                }},
            ], "minimum_should_match": 1}},
            "_source": ["record_kind", "@timestamp", "matched_string",
                        "external_links", "source_url", "diff_url",
                        "labels", "tags", "gem", "authors"],
        }
        try:
            res = req("GET", "/%s/_search" % INDEX, q)
        except Exception as e:
            log("ES query FAILED for %s: %s" % (prim, e))
            continue
        total = res["hits"]["total"]["value"]
        log("ES prim=%s total=%d (fetching %d)" %
            (prim, total, len(res["hits"]["hits"])))
        for h in res["hits"]["hits"]:
            s = h["_source"]
            hits.append({
                "primitive": prim,
                "source": "elastic:collusion-wiki",
                "doc_id": h["_id"],
                "record_kind": s.get("record_kind"),
                "first_seen": s.get("@timestamp"),
                "matched_string": s.get("matched_string"),
                "external_links": s.get("external_links"),
                "source_url": s.get("source_url") or s.get("diff_url"),
                "labels": s.get("labels"),
                "tags": s.get("tags"),
            })
    return hits

def local_sweep():
    """grep local corpus files; gem files + wiki pivot products."""
    rx = re.compile(
        r"pure(\.|%2e|%252e)md|api\.cors\.lol|corsmirror|gview|docs\.google\.com/viewer",
        re.IGNORECASE)
    targets = [
        DATA + "/gem-ioc-log.jsonl",
        DATA + "/gem-ioc-hits.jsonl",
        DATA + "/gem-ioc-hits.jsonl.pre-bulk",
        DATA + "/gem-iocs-2026-09-27.jsonl",
        DATA + "/gem-june18-wayback.jsonl",
        DATA + "/gemstuffer-jfrog-2026-09-27.csv",
        DATA + "/gem-graph-nodes.jsonl",
        DATA + "/gem-graph-edges.jsonl",
        DATA + "/osv/diffend_sweep_results.jsonl",
        DATA + "/wiki_ioc_pivots.jsonl",
        DATA + "/wiki_shortener_detail.json",
        DATA + "/wiki_ioc_pivot_summary.json",
    ]
    hits = []
    for path in targets:
        try:
            with open(path, errors="replace") as f:
                for ln, line in enumerate(f, 1):
                    m = rx.search(line)
                    if not m:
                        continue
                    # full token carrying the match (for gem-name fragment detection)
                    tok = re.search(r"[A-Za-z0-9_.%/:?=&*+-]*" + re.escape(m.group(0)) +
                                    r"[A-Za-z0-9_.%/:?=&*+-]*", line)
                    tok = (tok.group(0) if tok else m.group(0))
                    prim = classify(m.group(0))
                    ctx = line.strip()[:600]
                    # gem-name fragments like zjgview5 are name grammar, not proxy use
                    if (prim == "gview" and "http" not in tok.lower()
                            and re.fullmatch(r"[a-z0-9_]*gview\d*", tok.lower())):
                        kind = "gem-name-fragment"
                    else:
                        kind = "corpus-hit"
                    hits.append({
                        "primitive": prim,
                        "source": "local:" + path.replace(DATA + "/", ""),
                        "line_no": ln,
                        "record_kind": kind,
                        "first_seen": None,
                        "matched_string": tok,
                        "context": ctx,
                        "first_seen_note": "file-mtime",
                    })
        except FileNotFoundError:
            continue
    log("local sweep: %d raw hits" % len(hits))
    return hits

def classify(frag):
    f = frag.lower()
    if "pure" in f:
        return "pure.md"
    if "cors.lol" in f or "cors" in f and "lol" in f:
        return "api.cors.lol"
    if "corsmirror" in f:
        return "corsmirror.com"
    if "gview" in f or "viewer" in f:
        return "gview"
    return "unknown"

def first_seen_from_source(rec):
    """Extract the earliest defensible timestamp for a hit."""
    s = rec
    if s.get("first_seen"):
        return s["first_seen"]
    lbl = s.get("labels") or {}
    for k in ("first_write", "date", "published_at", "diff_ts_raw"):
        if lbl.get(k):
            return lbl[k]
    return None

def main():
    import os
    os.makedirs(OUT, exist_ok=True)
    log("lane F sweep start")
    all_hits = es_sweep() + local_sweep()
    # normalize: exact-duplicate collapse on (primitive, source, matched payload)
    seen, out = set(), []
    for h in all_hits:
        h["first_seen_effective"] = first_seen_from_source(h)
        payload = json.dumps(h.get("matched_string") or h.get("context") or "",
                             sort_keys=True, default=str)
        key = hashlib.sha256(
            (h["primitive"] + "|" + h["source"] + "|" + payload).encode()
        ).hexdigest()
        if key in seen:
            continue
        seen.add(key)
        h["hit_sha"] = key
        out.append(h)
    out.sort(key=lambda h: (h["primitive"], h["source"]))
    with open(OUT + "/hits.jsonl", "w") as f:
        for h in out:
            f.write(json.dumps(h, default=str) + "\n")
    by_prim = {}
    for h in out:
        by_prim[h["primitive"]] = by_prim.get(h["primitive"], 0) + 1
    log("sweep complete: %d hits after dedup %s" % (len(out), by_prim))
    return out

if __name__ == "__main__":
    main()
