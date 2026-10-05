#!/usr/bin/env python3
"""v2: refine other-workers.dev hostname analysis (strip ?/ ?url= prefixes,
classify target hosts, doc-level counts per index). Appends results into
data/aggregates/2025-09-26-cors-bwa-proxy/raw/other_workers_dev_hostnames.json and prints summary."""
import json, re
from urllib.parse import urlparse, unquote, parse_qs
from collections import Counter, defaultdict

D = "data/aggregates/2025-09-26-cors-bwa-proxy"
HOSTS = ["cors.hypnguyen.workers.dev", "cors-get-proxy.sirjosh.workers.dev",
         "cloudflare-cors-anywhere.hanpengchen.workers.dev",
         "test.cors.workers.dev", "cf-cors.findme-19.workers.dev",
         "r.jina-ai.workers.dev"]


def decode_target(raw):
    """raw = path captured after hostname/"""
    r = raw.strip()
    for _ in range(3):  # nested percent-encoding is common in wiki HTML
        n = unquote(r)
        if n == r:
            break
        r = n
    # strip leading query markers
    r = re.sub(r"^\?+(url=)?", "", r)
    qs = parse_qs(r)
    # if the value itself is a URL carried in a param
    for k in ("url", "u"):
        if k in qs and qs[k][0].startswith(("http://", "https://")):
            r = qs[k][0]
            break
    if not re.match(r"https?://", r, re.I):
        # bare host/path
        h = r.split("/")[0].split("?")[0].split(":")[0]
        if "." in h:
            r = "https://" + r
        else:
            return ""
    try:
        return urlparse(r).netloc.lower() or ""
    except Exception:
        return ""


stats = {}
for h in HOSTS:
    per_index_docs = Counter()
    targets = Counter()
    samples = {}
    for name in ["urlquery-incidents-allworkersdev",
                 "collusion-wiki-allworkersdev"]:
        idx = name.replace("-allworkersdev", "")
        for l in open(f"{D}/raw/{name}.jsonl"):
            d = json.loads(l)
            s = str(d["_source"])
            found = False
            for mm in re.finditer(re.escape(h) + r"/([^\s\"<>)]{1,200})",
                                  s, re.I):
                tgt = decode_target(mm.group(1))
                if tgt:
                    targets[tgt] += 1
                    found = True
                    samples.setdefault(tgt, mm.group(1)[:140])
            if found:
                per_index_docs[idx] += 1
    stats[h] = {"docs_per_index": dict(per_index_docs),
                "n_docs": sum(per_index_docs.values()),
                "n_occurrences": sum(targets.values()),
                "targets": dict(targets.most_common(15)),
                "sample_raw": {t: samples[t] for t in list(targets)[:5]}}

json.dump(stats, open(f"{D}/other_workers_dev_hostnames.json", "w"), indent=1)

for h, st in stats.items():
    print(f"== {h}  docs={st['n_docs']} occ={st['n_occurrences']} {st['docs_per_index']}")
    for t, c in list(st["targets"].items())[:8]:
        print(f"   {c:4d} {t}")
