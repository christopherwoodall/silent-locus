#!/usr/bin/env python3
"""Extract proxy-primitive URLs from local collusion-wiki corpus files.

For each hit: primitive, source record, laundered target (what URL the
primitive wraps), and first-seen = earliest revision write_date containing
that exact URL. Merges into data/aggregates/2026-05-26-proxy-primitives/proxy-primitives.jsonl with the
earlier sweep's hits; collapses exact duplicates.
"""
import gzip, json, re, hashlib, os, urllib.parse
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = BASE + "/data"
OUT = DATA + "/proxy-primitives"

PRIM_RX = re.compile(
    r"pure(\.|%2e|%252e)md|api\.cors\.lol|corsmirror|gview|docs\.google\.com/viewer",
    re.IGNORECASE)
URL_RX = re.compile(r"https?://[^\s\"'<>\\]+", re.IGNORECASE)

def classify(url):
    u = url.lower()
    if "pure" in u and "md" in u:
        return "pure.md"
    if "cors.lol" in u:
        return "api.cors.lol"
    if "corsmirror" in u:
        return "corsmirror.com"
    if "gview" in u or "docs.google.com/viewer" in u:
        return "gview"
    return "unknown"

def laundered_target(url):
    """What URL the proxy primitive wraps (best-effort parse)."""
    if not url or len(url) <= 40 and re.search(r"(%2|:|/)$", url):
        return None  # truncated in the source dump; target unrecoverable
    try:
        p = urllib.parse.urlparse(url)
        host = (p.hostname or "").lower()
        path = p.path or ""
        qs = urllib.parse.parse_qs(p.query)
        # query-param proxies: ?url=<inner> (cors.lol, corsmirror, gview...)
        for k in ("url", "u", "embedded"):
            if qs.get(k) and qs[k][0]:
                inner = urllib.parse.unquote(urllib.parse.unquote(qs[k][0]))
                if re.match(r"https?://", inner, re.I):
                    return inner
                if re.match(r"[a-z0-9.-]+\.[a-z]{2,}/", inner, re.I):
                    return "https://" + inner
        if "gview" in host or "viewer" in path:
            return None
        # path-embedded form: https://pure.md/<inner-url>
        inner = (path.lstrip("/") + ("?" + p.query if p.query else ""))
        inner = urllib.parse.unquote(urllib.parse.unquote(inner))
        if re.match(r"https?://", inner, re.I):
            return inner
        if re.match(r"[a-z0-9.-]+\.[a-z]{2,}/", inner, re.I):
            return "https://" + inner
        return inner or None
    except Exception:
        return None

def open_maybe_gz(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt", errors="replace")
    return open(path, errors="replace")

def main():
    # pass 1: URL -> earliest write_date from revisions
    first_seen = {}
    rev_count = 0
    with open_maybe_gz(DATA + "/collusion-wiki/raw/revisions.jsonl.gz") as f:
        for line in f:
            line = line.strip()
            if not line or not PRIM_RX.search(line):
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            wd = r.get("write_date") or r.get("time")
            for um in URL_RX.finditer(r.get("body") or ""):
                u = um.group(0).rstrip(".,;)")
                if not PRIM_RX.search(u):
                    continue
                if u not in first_seen or (wd and wd < first_seen[u]):
                    first_seen[u] = wd
                rev_count += 1
    print("revisions pass: %d primitive-url occurrences, %d distinct urls"
          % (rev_count, len(first_seen)), flush=True)

    hits = []

    def add(primitive, source, url, extra):
        target = laundered_target(url)
        h = {
            "primitive": primitive,
            "source": source,
            "matched_string": url,
            "laundered_target": target,
            "first_seen_effective": first_seen.get(url) or extra.get("time"),
        }
        h.update(extra)
        hits.append(h)

    # links.jsonl.gz + records.jsonl.gz
    for fname in ("collusion-wiki/raw/links.jsonl.gz", "collusion-wiki/raw/records.jsonl.gz"):
        n = 0
        with open_maybe_gz(DATA + "/" + fname) as f:
            for line in f:
                line = line.strip()
                if not line or not PRIM_RX.search(line):
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                url = r.get("url") or ""
                if not PRIM_RX.search(url):
                    continue
                add(classify(url), "local:" + fname, url, {
                    "record_kind": "wiki_link",
                    "host": r.get("host"),
                    "relation": r.get("relation"),
                    "n_record_ids": len(r.get("record_ids") or []),
                })
                n += 1
        print("%s: %d hits" % (fname, n), flush=True)

    # wiki_ioc_pivots.jsonl (structured pivot rows)
    n = 0
    with open(DATA + "/wiki_ioc_pivots.jsonl", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or not PRIM_RX.search(line):
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            url = r.get("ioc") or ""
            if not PRIM_RX.search(url):
                continue
            add(classify(url), "local:wiki_ioc_pivots.jsonl", url, {
                "record_kind": "wiki_ioc_pivot",
                "wikis": r.get("wikis"),
                "n_agents": len(r.get("agents") or []),
                "agents_sample": (r.get("agents") or [])[:5],
            })
            n += 1
    print("wiki_ioc_pivots.jsonl: %d hits" % n, flush=True)

    # wiki_shortener_detail.json (api.cors.lol / pure.md shortener rows)
    n = 0
    with open(DATA + "/wiki_shortener_detail.json", errors="replace") as f:
        d = json.load(f)
    rows = d.get("entries") if isinstance(d, dict) else d
    for r in rows or []:
        if not isinstance(r, dict):
            continue
        blob = json.dumps(r)
        if not PRIM_RX.search(blob):
            continue
        url = r.get("target") or r.get("url") or ""
        if not PRIM_RX.search(url):
            # fall back: first primitive-bearing URL anywhere in the row
            m2 = None
            for um in URL_RX.finditer(blob):
                if PRIM_RX.search(um.group(0)):
                    m2 = um.group(0)
                    break
            url = m2 or blob[:300]
        add(classify(url), "local:wiki_shortener_detail.json", url, {
            "record_kind": "wiki_shortener",
            "target_host": r.get("target_host"),
        })
        n += 1
    print("wiki_shortener_detail.json: %d hits" % n, flush=True)

    # records.jsonl.gz: agent record *text* annotating primitive use
    # (operational URL omitted in-dump; host + sha256 survive)
    n = 0
    with open_maybe_gz(DATA + "/collusion-wiki/raw/records.jsonl.gz") as f:
        for line in f:
            line = line.strip()
            if not line or not PRIM_RX.search(line):
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            txt = r.get("text") or ""
            m = PRIM_RX.search(txt)
            if not m:
                continue
            tok = re.search(r"[A-Za-z0-9_.%/:?=&*+;,\[\]-]*" + re.escape(m.group(0)) +
                            r"[A-Za-z0-9_.%/:?=&*+;,\[\]-]*", txt)
            frag = tok.group(0) if tok else m.group(0)
            sha = re.search(r"sha256=([0-9a-f]{8,64})", txt)
            add(classify(frag), "local:collusion-wiki/raw/records.jsonl.gz", frag, {
                "record_kind": "wiki_record_annotation",
                "record_id": r.get("id"),
                "selection_basis": r.get("selection_basis"),
                "omitted_url_sha256": sha.group(1) if sha else None,
                "time": None,
            })
            n += 1
    print("records.jsonl.gz annotations: %d hits" % n, flush=True)

    # merge with existing hits.jsonl (earlier sweep); the new structured
    # extractors supersede the old raw "corpus-hit" rows for the two files
    # they now cover
    SUPERSEDED = {("corpus-hit", "local:wiki_ioc_pivots.jsonl"),
                  ("corpus-hit", "local:wiki_shortener_detail.json")}
    prev = []
    hp = OUT + "/hits.jsonl"
    if os.path.exists(hp):
        with open(hp) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                if (r.get("record_kind"), r.get("source")) in SUPERSEDED:
                    continue
                prev.append(r)
    all_hits = prev + hits
    seen, out = set(), []
    for h in all_hits:
        key = hashlib.sha256(
            (h.get("primitive", "") + "|" + h.get("source", "") + "|" +
             (h.get("doc_id") or "") + "|" +
             json.dumps(h.get("matched_string") or h.get("context") or "",
                        sort_keys=True, default=str)).encode()).hexdigest()
        if key in seen:
            continue
        seen.add(key)
        h["hit_sha"] = key
        # recompute laundered target with fixed parser for wiki rows
        if h.get("source", "").startswith("local:") and h.get("matched_string"):
            ms = h["matched_string"]
            if isinstance(ms, str) and re.match(r"https?://", ms):
                h["laundered_target"] = laundered_target(ms)
        out.append(h)
    out.sort(key=lambda h: (h.get("primitive", ""), h.get("source", "")))
    with open(hp, "w") as f:
        for h in out:
            f.write(json.dumps(h, default=str) + "\n")
    by_prim = {}
    for h in out:
        by_prim[h.get("primitive")] = by_prim.get(h.get("primitive"), 0) + 1
    print("merged total: %d hits %s" % (len(out), by_prim), flush=True)
    # per-primitive distinct-URL counts (wiki corpus)
    urls = {}
    for h in out:
        if h.get("source", "").startswith("local:collusion-wiki"):
            urls.setdefault(h["primitive"], set()).add(h["matched_string"])
    print("distinct wiki-corpus URLs:", {k: len(v) for k, v in urls.items()})

if __name__ == "__main__":
    main()
