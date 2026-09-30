#!/usr/bin/env python3
"""Build final raw/ladder_edges.jsonl: (outer_wrapper -> cors.bwa.workers.dev -> target)
chains parsed from wiki external_links, proxy-primitives matched_strings,
and the urlquery-incident stacks. Each edge: {edge, layers, venue, n_docs}."""
import json, re
from urllib.parse import urlparse, unquote
from collections import Counter

D = "data/aggregates/2025-09-26-cors-bwa-proxy"
edges = Counter()
edge_meta = {}


def target_host(r):
    for _ in range(3):
        n = unquote(r)
        if n == r:
            break
        r = n
    if not re.match(r"https?://", r, re.I):
        h0 = r.split("/")[0]
        if "." in h0:
            r = "https://" + r
        else:
            return ""
    return urlparse(r).netloc.lower()


def add_chain(url, venue):
    """Parse full URL string into (wrapper..., bwa, target) edge."""
    s = url.strip()
    # if the string itself starts with bwa (no scheme), outer = bwa (direct use)
    if re.match(r"cors\.bwa\.workers\.dev/", s, re.I):
        outer = "cors.bwa.workers.dev"
    else:
        m = re.search(r"https?://([A-Za-z0-9.\-]+)(/[^?#]*)?(\?([^#]*))?", s, re.I)
        if not m:
            return
        outer = m.group(1).lower()
    bm = re.search(r"cors\.bwa\.workers\.dev/([^\s\"<>)]+)", s, re.I)
    if not bm:
        return
    th = target_host(bm.group(1))
    if not th:
        return
    key = (outer, "cors.bwa.workers.dev", th)
    edges[key] += 1
    edge_meta.setdefault(key, set()).add(venue)


# incident stacks
for l in open(f"{D}/raw/bwa_targets.jsonl"):
    r = json.loads(l)
    inner = re.sub(r"(https?://)?cors\.bwa\.workers\.dev/", "", r["full_proxied_url"], flags=re.I)
    inner_h = inner.split("/")[0].lower()
    if "." in inner_h and r["target_host"] != inner_h:
        key = ("cors.bwa.workers.dev", inner_h, r["target_host"] or "shortener-target")
        edges[key] += 1
        edge_meta.setdefault(key, set()).add("urlquery-incidents")
    else:
        key = (r["chain_layers"][0], "cors.bwa.workers.dev", r["target_host"])
        edges[key] += 1
        edge_meta.setdefault(key, set()).add("urlquery-incidents")

# wiki external_links
for l in open(f"{D}/raw/collusion-wiki.jsonl"):
    d = json.loads(l)
    for el in (d["_source"].get("external_links") or []):
        add_chain(str(el), "2026-05-17-collusion-wiki")

# proxy-primitives matched_string
for l in open(f"{D}/raw/proxy-primitives.jsonl"):
    d = json.loads(l)
    ms = d["_source"].get("matched_string")
    if ms:
        add_chain(str(ms), "2026-05-26-proxy-primitives")

with open(f"{D}/raw/ladder_edges.jsonl", "w") as f:
    for (outer, via, tgt), n in edges.most_common():
        f.write(json.dumps({"edge": f"{outer} --{via}--> {tgt}",
                            "layers": [outer, via, tgt],
                            "occurrences": n,
                            "venues": sorted(edge_meta[(outer, via, tgt)])}) + "\n")

print("edges:", len(edges))
for (o, v, t), n in edges.most_common(18):
    print(f"  {n:4d}  {o} --{v}--> {t}")
