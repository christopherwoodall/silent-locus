#!/usr/bin/env python3
"""HN Algolia collector A, pass 2 (hpp=100, correct paging).
Pass 1 used hitsPerPage=1000, which the API mishandles (nbPages=1,
page>=1 empty). This pass re-fetches everything with hitsPerPage=100
and follows nbPages. Two match variants per query:
  fuzzy = API default (typo-tolerant; 'routify' also matches
          route/routine/routing noise)
  exact = typoTolerance=false (literal term only)
Polite pace: >=1s between calls. Public API only, no key/login.
"""
import json
import subprocess
import time
import urllib.parse
from datetime import datetime, timezone

OUT = "/home/hatch/workspace/silent-locus/data/lanes/hackernews-egress-hunt/raw/algolia-A"
EPOCH = 1761955200  # 2025-11-01T00:00:00Z
HPP = 100
TERMS = ["routify", "aliyuncs", "oss-cn", "sanmaohe", "proxy_temp_file"]
TAGS = ["story", "comment"]


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
    for variant in ("fuzzy", "exact"):
        for term in TERMS:
            for tag in TAGS:
                for mode in ("filtered", "unfiltered"):
                    q = urllib.parse.quote(term)
                    base = (f"https://hn.algolia.com/api/v1/search?query={q}"
                            f"&tags={tag}&hitsPerPage={HPP}")
                    if variant == "exact":
                        base += "&typoTolerance=false"
                    if mode == "filtered":
                        base += (f"&numericFilters="
                                 f"created_at_i%3E%3D{EPOCH}")
                    key = f"{term}/{tag}/{mode}/{variant}"
                    print(f"== {key} ==", flush=True)
                    url0 = base + "&page=0"
                    try:
                        data, raw = fetch(url0)
                    except RuntimeError as e:
                        print(f"  ERROR {e}", flush=True)
                        summary[key] = {"error": str(e)}
                        continue
                    nb_hits = data.get("nbHits")
                    nb_pages = data.get("nbPages", 0)
                    capped = bool(nb_hits and nb_hits > HPP * nb_pages)
                    print(f"  nbHits={nb_hits} nbPages={nb_pages} "
                          f"capped={capped}", flush=True)
                    pages = [(0, data, raw, url0)]
                    for p in range(1, nb_pages):
                        time.sleep(1.2)
                        url = base + f"&page={p}"
                        d, rb = fetch(url)
                        pages.append((p, d, rb, url))
                        print(f"  page {p}: {len(d.get('hits', []))} hits",
                              flush=True)
                    saved = 0
                    for p, d, rb, url in pages:
                        fname = (f"{term}-{tag}-{mode}-{variant}"
                                 f"-p{p}.json")
                        path = f"{OUT}/{fname}"
                        with open(path, "w") as f:
                            f.write(rb)
                        prov = (f"Source URL: {url}\n"
                                f"Retrieval time (UTC): "
                                f"{datetime.now(timezone.utc).isoformat()}\n"
                                f"Method: curl -s to HN Algolia public API "
                                f"(https://hn.algolia.com/api/v1/search), "
                                f"no key, no login\n"
                                f"Query: term={term} tags={tag} mode={mode} "
                                f"variant={variant} page={p} "
                                f"hitsPerPage={HPP}\n"
                                f"Query nbHits (page 0 response): {nb_hits}\n"
                                f"Query nbPages (page 0 response): {nb_pages}\n"
                                f"API-browse-cap hit (nbHits > 1000): {capped}\n"
                                f"File: {fname} (verbatim API response bytes)\n")
                        with open(path + ".PROVENANCE.txt", "w") as f:
                            f.write(prov)
                        h = subprocess.run(
                            ["sha256sum", path], capture_output=True,
                            text=True).stdout.strip()
                        with open(path + ".sha256", "w") as f:
                            f.write(h + "\n")
                        saved += len(d.get("hits", []))
                    summary[key] = {"nbHits": nb_hits, "nbPages": nb_pages,
                                    "pages_fetched": len(pages),
                                    "hits_saved": saved, "capped": capped}
                    time.sleep(1.2)
    with open(f"{OUT}/_fetch2-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
