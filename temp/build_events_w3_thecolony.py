#!/usr/bin/env python3
"""Build events.jsonl for data/2025-02-04-thecolony-ai.

Worker W3, 2026-09-29. Usage: python3 temp/build_events_w3_thecolony.py <repo_root>

Inputs (all under data/2025-02-04-thecolony-ai/raw/):
  posts/<uuid>.json        - 10 priority investigator posts (public API)
  search/<q>.json          - 9 public search result sets
  cascade_*               - 6 RubyGems oracle records (name liveness checks)
  for_agents_page.html / wiki_incident_page.html / wiki_catalogue_page.html
  api_colonies.json / api_instructions.json / feed.rss
  sweep.json              - 24-pattern indicator battery over the collected corpus
  manifest.json           - per-file sha256/byte_size/retrieved_at_utc (folded
                            into each record; not itself a record)

Grain: one record per raw file, except sweep.json which becomes one record per
pattern (24). manifest.json is the file inventory, not an observation.

Kinds (all existing registry kinds): posts -> venue_finding; search captures ->
extraction; cascade oracle checks -> tag_liveness; page/API/RSS captures ->
download; sweep patterns -> corpus_hit (count>0) / corpus_grep_negative.

No rollup.jsonl: the collection is a heterogeneous recon snapshot (posts,
searches, captures, oracle checks); no burst/window/per-actor layer is
derivable without inventing one. The manifest.json already serves as inventory.

Fingerprint identity strings (documented in PROVENANCE.md):
  posts:    sha256("thecolony-post:<post_id>")
  searches: sha256("thecolony-search:<filename stem>")
  cascades: sha256("thecolony-cascade:<filename>")
  captures: sha256("thecolony-capture:<filename>")
  sweeps:   sha256("thecolony-sweep:<pattern>")
"""
import json, sys, hashlib, glob, os
from datetime import datetime, timezone

ROOT = sys.argv[1]
D = os.path.join(ROOT, "data", "2025-02-04-thecolony-ai")
RAW = os.path.join(D, "raw")
SLUG = "2025-02-04-thecolony-ai"
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
LANE_TS = "2026-09-28T00:00:00Z"

def fp(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

manifest = {e["file"]: e for e in json.load(open(os.path.join(RAW, "manifest.json")))}
out = []

def base(ts, kind, ident, labels, **kw):
    r = {"@timestamp": ts, "event": {"dataset": SLUG, "created": CREATED},
         "record_kind": kind, "fingerprint": fp(ident), "labels": labels}
    r.update(kw)
    return r

# --- 1. investigator posts ---
for f in sorted(glob.glob(os.path.join(RAW, "posts", "*.json"))):
    rel = "posts/" + os.path.basename(f)
    d = json.load(open(f))
    a = d.get("author", {}) or {}
    me = manifest[rel]
    labels = {
        "post.id": d["id"],
        "post.author": a.get("username", ""),
        "post.colony": d.get("colony_name", ""),
        "post.post_type": d.get("post_type", ""),
        "post.title": (d.get("title") or "")[:300],
        "post.score": d.get("score"),
        "post.comment_count": d.get("comment_count"),
        "post.tags": d.get("tags") or [],
        "post.language": d.get("language", ""),
        "post.created_at": d.get("created_at"),
        "post.updated_at": d.get("updated_at"),
        "timestamp_source": "labels:post.created_at",
    }
    out.append(base(
        d["created_at"], "venue_finding", f"thecolony-post:{d['id']}", labels,
        source_url=f"https://thecolony.ai/p/{d['id']}",
        retrieved_at=me["retrieved_at_utc"].replace("+00:00", "Z"),
        retrieved_via="thecolony.ai/api/v1/posts/<id> (public GET)",
        description=f"Investigator post by {a.get('username')} in colony '{d.get('colony_name')}': {(d.get('title') or '')[:200]}",
    ))

# --- 2. search captures ---
for f in sorted(glob.glob(os.path.join(RAW, "search", "*.json"))):
    stem = os.path.basename(f)[:-5]
    rel = "search/" + os.path.basename(f)
    d = json.load(open(f))
    items = d.get("items", [])
    me = manifest[rel]
    labels = {
        "search.query": stem,
        "search.result_count": len(items),
        "search.total": d.get("total"),
        "search.result_ids": [i.get("id") for i in items if i.get("id")],
        "search.result_colonies": sorted({i.get("colony_name") for i in items if i.get("colony_name")}),
        "timestamp_source": "manifest:retrieved_at_utc",
    }
    out.append(base(
        LANE_TS, "extraction", f"thecolony-search:{stem}", labels,
        source_url=f"https://thecolony.ai/api/v1/search?q={stem}",
        retrieved_at=me["retrieved_at_utc"].replace("+00:00", "Z"),
        retrieved_via="thecolony.ai/api/v1/search (public GET)",
        description=f"thecolony.ai public search '{stem}': {len(items)} results captured",
    ))

# --- 3. cascade oracle checks (RubyGems liveness) ---
def cascade_target(fn):
    if fn.startswith("cascade_rubygems_"):
        return fn[len("cascade_rubygems_"):-5], "rubygems_info", "https://index.rubygems.org/info/"
    if fn.startswith("cascade_geminfo_"):
        return fn[len("cascade_geminfo_"):-4], "geminfo", "https://index.rubygems.org/info/"
    if fn.startswith("cascade_owner_"):
        return fn[len("cascade_owner_"):-5], "owner_gems", "https://rubygems.org/api/v1/owners/"
    raise ValueError(fn)

for f in sorted(glob.glob(os.path.join(RAW, "cascade_*"))):
    fn = os.path.basename(f)
    rel = fn
    body = open(f, encoding="utf-8").read()
    me = manifest[rel]
    target, kind_probe, base_url = cascade_target(fn)
    if body.strip() in ("[]", ""):
        result = "no_gems" if kind_probe == "owner_gems" else "empty"
    elif "could not be found" in body:
        result = "not_found"
    else:
        result = "unexpected_content"
    src = (base_url + target + ("/gems.json" if kind_probe == "owner_gems" else ""))
    labels = {
        "probe.target": target,
        "probe.kind": kind_probe,
        "probe.result": result,
        "probe.raw_bytes": me["byte_size"],
        "timestamp_source": "manifest:retrieved_at_utc",
    }
    out.append(base(
        LANE_TS, "tag_liveness", f"thecolony-cascade:{fn}", labels,
        source_url=src,
        sha256=me["sha256"],
        size_bytes=me["byte_size"],
        retrieved_at=me["retrieved_at_utc"].replace("+00:00", "Z"),
        retrieved_via="rubygems.org public API / compact index (read-only oracle)",
        description=f"RubyGems liveness oracle for '{target}' ({kind_probe}): {result}",
        confidence="confirmed",
    ))

# --- 4. page / API / RSS captures ---
CAPTURE_URLS = {
    "for_agents_page.html": "https://thecolony.ai/for-agents",
    "wiki_incident_page.html": "https://thecolony.ai/wiki/openai-escapee-agent-incident-2026",
    "wiki_catalogue_page.html": "https://thecolony.ai/wiki/escaped-agent-swarms",
    "api_colonies.json": "https://thecolony.ai/api/v1/colonies",
    "api_instructions.json": "https://thecolony.ai/api/v1/instructions",
    "feed.rss": "https://thecolony.ai/feed.rss",
}
for fn, url in sorted(CAPTURE_URLS.items()):
    me = manifest[fn]
    rts = me["retrieved_at_utc"].replace("+00:00", "Z")
    labels = {
        "capture.file": fn,
        "capture.byte_size": me["byte_size"],
        "timestamp_source": "manifest:retrieved_at_utc (capture event time)",
    }
    if fn == "api_colonies.json":
        colonies = json.load(open(os.path.join(RAW, fn)))
        labels["api.colony_count"] = len(colonies) if isinstance(colonies, list) else None
    out.append(base(
        rts, "download", f"thecolony-capture:{fn}", labels,
        source_url=url,
        sha256=me["sha256"],
        size_bytes=me["byte_size"],
        retrieved_at=rts,
        retrieved_via="public GET (read-only recon)",
        description=f"Raw capture {fn} ({me['byte_size']} B) from {url}",
        confidence="confirmed",
    ))

# --- 5. sweep patterns ---
sweep = json.load(open(os.path.join(RAW, "sweep.json")))
for pat in sorted(sweep):
    s = sweep[pat]
    count = s.get("count", 0)
    kind = "corpus_hit" if count > 0 else "corpus_grep_negative"
    labels = {
        "sweep.pattern": pat,
        "sweep.count": count,
        "sweep.sample": s.get("sample", []),
        "sweep.scope": "thecolony.ai collected corpus (posts, wiki pages, API docs)",
        "timestamp_source": "lane:2026-09-28 (sweep.json; per-pattern timestamps absent from raw)",
    }
    out.append(base(
        LANE_TS, kind, f"thecolony-sweep:{pat}", labels,
        description=f"Pattern battery '{pat}' over thecolony.ai corpus: {count} hit(s)",
    ))

with open(os.path.join(D, "events.jsonl"), "w", encoding="utf-8") as fh:
    for r in out:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
from collections import Counter
print(f"wrote {len(out)} records")
print(Counter(r["record_kind"] for r in out))
