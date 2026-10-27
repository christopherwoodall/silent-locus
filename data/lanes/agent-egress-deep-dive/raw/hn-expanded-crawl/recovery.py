#!/usr/bin/env python3
"""Targeted recovery for two rows where live probes showed that
search_by_date pages 1+ returned 0 hits despite nbPages > 1
(GitLost stories, routify stories).

Method: split the date range until each leaf reports <= 100 hits,
then fetch page 0 of each leaf (further pages if offered). Save only
ids NOT already in the main capture, as supplementary files with their
own provenance and sha256 sidecars. Poster-handle field removed, as in
fetch_hn.py. GET only, no key, no login.
"""
import json, os, time, hashlib, urllib.parse, urllib.request
from datetime import datetime, timezone

BASE = "https://hn.algolia.com/api/v1/search_by_date"
OUT = os.path.dirname(os.path.abspath(__file__))
START, END = 1761955200, 1793145600
UA = "hn-expanded-crawl research (HN Algolia public API, GET only)"
TARGETS = [
    ("name-gitlost", "GitLost", "story", "name-gitlost--story.json"),
    ("shape-routify", "routify", "story", "shape-routify--story.json"),
]


def api_get(params):
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(BASE + "?" + qs, headers={"User-Agent": UA})
    for attempt in range(12):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if attempt == 11:
                raise
            time.sleep(min(60, 10 * (attempt + 1)))


def clean_hit(h):
    h = dict(h)
    h.pop("author", None)
    hl = h.get("_highlightResult")
    if isinstance(hl, dict):
        hl = dict(hl)
        hl.pop("author", None)
        h["_highlightResult"] = hl
    return h


def fetch_leaf(query, tag, start, end, leaves):
    params = {"query": query, "tags": tag, "hitsPerPage": 100, "page": 0,
              "numericFilters": f"created_at_i>{start},created_at_i<{end}"}
    first = api_get(params)
    nb = first.get("nbHits", 0)
    time.sleep(0.2)
    if nb > 100 and (end - start) > 86400:
        mid = (start + end) // 2
        fetch_leaf(query, tag, start, mid, leaves)
        fetch_leaf(query, tag, mid, end, leaves)
        return
    hits = [clean_hit(h) for h in first.get("hits", [])]
    pages = min(first.get("nbPages", 0), 10)
    for p in range(1, pages):
        params["page"] = p
        resp = api_get(params)
        hits.extend(clean_hit(h) for h in resp.get("hits", []))
        time.sleep(0.2)
    leaves.append({"start": start, "end": end, "reported": nb,
                   "delivered": len(hits), "hits": hits})


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    for label, query, tag, main_file in TARGETS:
        main = json.load(open(os.path.join(OUT, main_file)))
        have = {str(h["objectID"]) for h in main["hits"]}
        leaves = []
        fetch_leaf(query, tag, START, END, leaves)
        seen, new = set(), []
        for leaf in leaves:
            for h in leaf["hits"]:
                oid = str(h["objectID"])
                if oid in have or oid in seen:
                    continue
                seen.add(oid)
                new.append(h)
        new.sort(key=lambda h: h.get("created_at_i", 0))
        fname = f"{label}--{tag}--recovery.json"
        fpath = os.path.join(OUT, fname)
        payload = {"term_label": label, "queries": [query], "tag": tag,
                   "recovery_for": main_file,
                   "main_capture_fetched": main["fetched_count"],
                   "leaves": [{k: v for k, v in lf.items() if k != "hits"}
                              for lf in leaves],
                   "new_ids_count": len(new), "hits": new}
        with open(fpath + ".tmp", "w") as f:
            json.dump(payload, f, indent=1)
            f.write("\n")
        os.rename(fpath + ".tmp", fpath)
        retrieved = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(fpath + ".PROVENANCE.txt", "w") as f:
            f.write(f"Source: HN Algolia public API, search_by_date endpoint.\n"
                    f"Base URL: {BASE}\n"
                    f"Query: {query}\nTag: {tag}\n"
                    f"Purpose: recovery for {main_file}. Live probes showed "
                    f"pages 1+ returning 0 hits despite nbPages > 1, so this "
                    f"recovery splits until each leaf reports <= 100 hits and "
                    f"takes page 0 of each leaf.\n"
                    f"Date range (created_at_i): {START} to {END}.\n"
                    f"Retrieved: {retrieved}\n"
                    f"Method: GET via Python urllib, no key, no login, no POST.\n"
                    f"Note: the author field was removed from every hit before "
                    f"save per the no-poster-handles rule. All other hit bytes "
                    f"are verbatim. Only ids absent from the main capture are "
                    f"saved here.\n")
        digest = sha256_of(fpath)
        with open(fpath + ".sha256", "w") as f:
            f.write(f"{digest}  {fname}\n")
        print(f"{label}:{tag} leaves={len(leaves)} "
              f"leaf_delivered_total={sum(lf['delivered'] for lf in leaves)} "
              f"new_ids={len(new)} file={fname}")


if __name__ == "__main__":
    main()
