#!/usr/bin/env python3
"""HN Algolia collector A: page each term/tag query, save verbatim pages.
Polite pace: >=1s between calls. No auth, no login. Public API only.
Usage: python3 fetch_algolia.py
Writes into the directory this script lives in (algolia-A/).
"""
import json
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone

OUT = "/home/hatch/workspace/silent-locus/data/lanes/hackernews-egress-hunt/raw/algolia-A"
EPOCH = 1761955200  # 2025-11-01T00:00:00Z
HPP = 1000

# (term, tag, mode, page_cap) — page_cap None = full pages
QUERIES = [
    ("routify", "story", "filtered", None),
    ("routify", "comment", "filtered", None),
    ("routify", "story", "unfiltered", None),
    ("routify", "comment", "unfiltered", 2),   # 115382 hits: CAPPED at 2 pages
    ("aliyuncs", "story", "filtered", None),
    ("aliyuncs", "comment", "filtered", None),
    ("aliyuncs", "story", "unfiltered", None),
    ("aliyuncs", "comment", "unfiltered", None),
    ("oss-cn", "story", "filtered", None),
    ("oss-cn", "comment", "filtered", None),
    ("oss-cn", "story", "unfiltered", None),
    ("oss-cn", "comment", "unfiltered", None),
    ("sanmaohe", "story", "filtered", None),
    ("sanmaohe", "comment", "filtered", None),
    ("sanmaohe", "story", "unfiltered", None),
    ("sanmaohe", "comment", "unfiltered", None),
    ("proxy_temp_file", "story", "filtered", None),
    ("proxy_temp_file", "comment", "filtered", None),
    ("proxy_temp_file", "story", "unfiltered", None),
    ("proxy_temp_file", "comment", "unfiltered", None),
]


def fetch(url):
    for attempt in (1, 2, 3):
        r = subprocess.run(["curl", "-s", "-w", "\n%{http_code}", url],
                           capture_output=True, text=True, timeout=180)
        body, _, code = r.stdout.rpartition("\n")
        if code.strip() == "200":
            try:
                return json.loads(body), body
            except json.JSONDecodeError:
                print(f"  BAD JSON attempt {attempt}", flush=True)
        else:
            print(f"  HTTP {code.strip()} attempt {attempt}", flush=True)
        time.sleep(5)
    raise RuntimeError(f"failed after 3 attempts: {url}")


def main():
    summary = {}
    for term, tag, mode, cap in QUERIES:
        q = urllib.parse.quote(term)
        base = (f"https://hn.algolia.com/api/v1/search?query={q}&tags={tag}"
                f"&hitsPerPage={HPP}")
        if mode == "filtered":
            base += f"&numericFilters=created_at_i%3E%3D{EPOCH}"
        print(f"== {term}/{tag}/{mode} ==", flush=True)
        # page 0 to learn nbPages
        url0 = base + "&page=0"
        data, raw = fetch(url0)
        nb_hits = data.get("nbHits")
        nb_pages = data.get("nbPages", 0)
        pages_to_fetch = nb_pages if cap is None else min(nb_pages, cap)
        print(f"  nbHits={nb_hits} nbPages={nb_pages} fetching={pages_to_fetch}",
              flush=True)
        pages = [(0, data, raw, url0)]
        for p in range(1, pages_to_fetch):
            time.sleep(1.2)
            url = base + f"&page={p}"
            d, rb = fetch(url)
            pages.append((p, d, rb, url))
            print(f"  page {p}: {len(d.get('hits', []))} hits", flush=True)
        saved = 0
        for p, d, rb, url in pages:
            fname = f"{term}-{tag}-{mode}-p{p}.json"
            path = f"{OUT}/{fname}"
            with open(path, "w") as f:
                f.write(rb)
            prov = (f"Source URL: {url}\n"
                    f"Retrieval time (UTC): "
                    f"{datetime.now(timezone.utc).isoformat()}\n"
                    f"Method: curl -s to HN Algolia public API "
                    f"(https://hn.algolia.com/api/v1/search), no key, no login\n"
                    f"Query: term={term} tags={tag} mode={mode} "
                    f"page={p} hitsPerPage={HPP}\n"
                    f"Query nbHits (page 0 response): {nb_hits}\n"
                    f"Query nbPages (page 0 response): {nb_pages}\n"
                    f"Pages fetched for this query: {pages_to_fetch}\n"
                    f"Cap applied: {cap}\n"
                    f"File: {fname} (verbatim API response bytes)\n")
            with open(path + ".PROVENANCE.txt", "w") as f:
                f.write(prov)
            h = subprocess.run(["sha256sum", path], capture_output=True,
                               text=True).stdout.strip()
            with open(path + ".sha256", "w") as f:
                f.write(h + "\n")
            saved += len(d.get("hits", []))
        summary[f"{term}/{tag}/{mode}"] = {
            "nbHits": nb_hits, "nbPages": nb_pages,
            "pages_fetched": pages_to_fetch, "hits_saved": saved,
            "cap": cap,
        }
        time.sleep(1.2)
    with open(f"{OUT}/_fetch-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
