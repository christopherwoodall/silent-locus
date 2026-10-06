#!/usr/bin/env python3
"""slug-hunt: check where a URL slug/surface appears across scan archives.

For each slug, queries:
  1. urlquery.net search API (q= matches submitted URLs) -- via uq.py skill
  2. urlscan.io search API (page.url:"slug") -- keyless, recent window
  3. Wayback CDX (url prefix search) -- keyless

Usage: slug-hunt.py slug1 slug2 ... [--json]
Slugs: UUIDs, subdomains, ntfy topics, ?m= markers, path fragments.
"""
import json
import subprocess
import sys
import urllib.parse
import urllib.request

UQ = ["python3", "/home/hatch/workspace/skills/urlquery/bin/uq.py",
      "search", "--limit", "5"]


def uq_search(slug):
    try:
        p = subprocess.run(UQ + ["--query", slug], capture_output=True,
                           text=True, timeout=60)
        data = json.loads(p.stdout)
        if isinstance(data, dict) and "error" in data:
            return {"error": data["error"]}
        if isinstance(data, dict) and "total_hits" in data:
            return {"hits": data["total_hits"]}
        reports = data if isinstance(data, list) else data.get("results", data)
        n = len(reports) if isinstance(reports, list) else "?"
        return {"hits": n}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:100]}


def urlscan_search(slug):
    try:
        q = urllib.parse.quote(f'page.url:"{slug}"')
        req = urllib.request.Request(
            f"https://urlscan.io/api/v1/search/?q={q}&size=5",
            headers={"User-Agent": "silent-locus-slug-hunt/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        return {"hits": data.get("total", 0)}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:100]}


def cdx_search(slug):
    try:
        # try as domain-ish and as path-ish
        urls = [f"{slug}*", f"*/{slug}*"] if "/" not in slug else [f"{slug}*"]
        total = 0
        for u in urls:
            q = urllib.parse.quote(u, safe="")
            req = urllib.request.Request(
                f"https://web.archive.org/cdx/search/cdx?url={q}"
                "&output=json&limit=5&collapse=urlkey",
                headers={"User-Agent": "silent-locus-slug-hunt/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            total += max(0, len(data) - 1)  # first row is header
        return {"hits": total}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:100]}


def main():
    slugs = [a for a in sys.argv[1:] if not a.startswith("-")]
    as_json = "--json" in sys.argv
    out = {}
    for slug in slugs:
        out[slug] = {
            "urlquery": uq_search(slug),
            "urlscan": urlscan_search(slug),
            "wayback_cdx": cdx_search(slug),
        }
        if not as_json:
            u = out[slug]
            print(f"{slug}\n  urlquery={u['urlquery']} "
                  f"urlscan={u['urlscan']} cdx={u['wayback_cdx']}")
    if as_json:
        print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
