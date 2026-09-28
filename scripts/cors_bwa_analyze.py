#!/usr/bin/env python3
"""Analyze the cors-bwa-proxy raw pulls: target extraction, classification,
ladder chains, timing, other workers.dev hostnames. Writes:
  data/cors-bwa-proxy/bwa_targets.jsonl
  data/cors-bwa-proxy/ladder_edges.jsonl
  data/cors-bwa-proxy/other_workers_dev_hostnames.json
  data/cors-bwa-proxy/summary_stats.json
Passive dataset work only — no live fetches."""
import json, os, re
from urllib.parse import urlparse, unquote
from collections import Counter, defaultdict

D = "data/cors-bwa-proxy"
RAW = f"{D}/raw"

BWA = "cors.bwa.workers.dev"


def load(name):
    with open(f"{RAW}/{name}.jsonl") as f:
        return [json.loads(l) for l in f]


def find_strings(obj, needle, out, path=""):
    """Collect every string value containing needle, with its path."""
    if isinstance(obj, str):
        if needle.lower() in obj.lower():
            out.append((path, obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            find_strings(v, needle, out, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find_strings(v, needle, out, f"{path}[{i}]")


# ---- shape inspection: where does the bwa string live per index? ----
for name in ["collusion-wiki", "urlquery-hunt", "proxy-primitives",
             "paste-archive-gap", "rmn-re-linktable"]:
    docs = load(name)
    path_counts = Counter()
    for d in docs[:20]:
        hits = []
        find_strings(d["_source"], BWA, hits)
        for p, _ in hits:
            path_counts[p] += 1
    print(f"== {name}: field paths (first 20 docs)")
    for p, c in path_counts.most_common(6):
        print(f"   {p}: {c}")


def strip_bwa(url):
    """Strip cors.bwa.workers.dev/ prefix, return decoded target URL."""
    u = url.strip()
    # find the bwa marker (with or without scheme)
    m = re.search(r"(https?://)?cors\.bwa\.workers\.dev/", u, re.I)
    if not m:
        return None
    rest = u[m.end():]
    # strip inner scheme prefix like "https://vizhub..." stays as is
    rest = unquote(rest)
    # sometimes the rest starts with scheme, sometimes bare host/path
    if not re.match(r"https?://", rest, re.I):
        rest = "https://" + rest
    return rest


def host_of(url):
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def task_family(h):
    h = h.lower()
    if not h:
        return "unknown"
    if any(k in h for k in ["vizhub.healthdata", "healthdata.org"]):
        return "health-dashboard"
    if any(k in h for k in ["iiif", "digit", "library", "archive", "preservica"]):
        return "digital-archive"
    if "docs.google.com" in h:
        return "google-viewer"
    if "drive.google.com" in h:
        return "google-drive"
    if any(k in h for k in ["tableau", "public.tableau", "qlik", "powerbi"]):
        return "bi-dashboard"
    if any(k in h for k in ["data.", "opendata", "catalog", "api."]):
        return "open-data-api"
    if any(k in h for k in ["wikipedia.org", "wiktionary", "mediawiki"]):
        return "wiki"
    if any(k in h for k in ["github", "gitlab", "raw.githubusercontent"]):
        return "code-hosting"
    if any(k in h for k in ["httpbin", "httpbun"]):
        return "http-echo"
    if any(k in h for k in ["pastebin", "paste.rs", "hastebin", "termbin"]):
        return "pastebin"
    return "other"


# known shortener hosts for ladder detection
SHORTENERS = {"da.gd", "is.gd", "tinyurl.com", "bit.ly", "t.ly", "rb.gy",
              "cutt.ly", "goo.gl", "ow.ly", "rmn.re", "shorturl.at"}

targets = []       # per-incident records
edge_set = set()
host_counter = Counter()
family_counter = Counter()
monthly = Counter()
shortener_stack = Counter()
gview_stack = Counter()

docs = load("urlquery-incidents")
for d in docs:
    doc_id = d["_id"]
    src = d["_source"]
    orig = ((src.get("url") or {}).get("original") or "")
    ts = src.get("@timestamp") or ""
    bwa_url = None
    for tok in re.split(r"[\s\"'<>]+", orig):
        if "cors.bwa.workers.dev" in tok.lower():
            bwa_url = tok
            break
    if not bwa_url:
        hits = []
        find_strings(src, BWA, hits)
        bwa_url = hits[0][1] if hits else orig
    tgt = strip_bwa(bwa_url)
    th = host_of(tgt) if tgt else ""
    fam = task_family(th)
    host_counter[th] += 1
    family_counter[fam] += 1
    if len(ts) >= 7:
        monthly[ts[:7]] += 1
    # chain layers: parse the full original URL stack
    layers = []
    o = orig.strip()
    if re.match(r"https?://", o, re.I):
        m = re.search(r"https?://([A-Za-z0-9.\-]+)(/[^?\s]*)?", o)
        if m:
            layers.append(m.group(1).lower())
    else:
        # bare host/path form like cors.bwa.workers.dev/https://...
        h0 = re.split(r"[/:?#]", o)[0].lower()
        if "." in h0:
            layers.append(h0)
    layers.append("cors.bwa.workers.dev")
    if tgt:
        layers.append(th)
    layers = list(dict.fromkeys(layers))  # dedupe, keep order
    # detect shortener in the proxied path (e.g. cors.bwa.workers.dev/da.gd/xxx)
    inner = re.sub(r"(https?://)?cors\.bwa\.workers\.dev/", "", bwa_url, flags=re.I)
    inner_host = re.split(r"[/:?#]", inner)[0].lower()
    if inner_host in SHORTENERS:
        shortener_stack[inner_host] += 1
    if "docs.google.com/gview" in orig.lower():
        gview_stack["gview_wraps_bwa"] += 1
    chain = " -> ".join([l for l in layers if l])
    if th:
        edge_set.add((layers[0], "cors.bwa.workers.dev", th))
    rec = {"source_index": "urlquery-incidents", "doc_id": doc_id,
           "full_proxied_url": bwa_url,
           "decoded_target": tgt, "target_host": th,
           "task_family": fam, "chain_layers": layers,
           "chain": chain, "incident_ts": ts}
    targets.append(rec)

# sort monthly
monthly = dict(sorted(monthly.items()))

# ---- other workers.dev hostnames ----
other_hosts = Counter()
for name in ["urlquery-incidents-allworkersdev", "collusion-wiki-allworkersdev"]:
    for d in load(name):
        hits = []
        find_strings(d["_source"], "workers.dev", hits)
        for _, s in hits:
            for mm in re.findall(r"https?://([A-Za-z0-9.\-]+\.workers\.dev)",
                                 s, re.I):
                h = mm.lower()
                if h != BWA:
                    other_hosts[h] += 1

with open(f"{D}/bwa_targets.jsonl", "w") as f:
    for r in targets:
        f.write(json.dumps(r) + "\n")

with open(f"{D}/ladder_edges.jsonl", "w") as f:
    for src_h, via, dst in sorted(edge_set):
        f.write(json.dumps({"source": src_h, "via": via,
                            "target": dst}) + "\n")

# other_workers_dev_hostnames.json is owned by scripts/cors_bwa_other_hosts.py
# (do not write the v1 sketch here)

summary = {
    "n_incident_targets": len(targets),
    "top_target_hosts": dict(host_counter.most_common(25)),
    "task_families": dict(family_counter),
    "monthly_incidents": monthly,
    "shortener_inside_proxy": dict(shortener_stack),
    "gview_wrapping_bwa": dict(gview_stack),
    "n_ladder_edges": len(edge_set),
    "n_other_workers_dev_hosts": len(other_hosts),
    "other_workers_dev_top": dict(other_hosts.most_common(20)),
}
json.dump(summary, open(f"{D}/summary_stats.json", "w"), indent=1)

print("\n== top target hosts")
for h, c in host_counter.most_common(15):
    print(f"   {c:4d} {h}")
print("\n== task families")
for f2, c in family_counter.most_common():
    print(f"   {c:4d} {f2}")
print("\n== monthly")
for m2, c in monthly.items():
    print(f"   {m2}: {c}")
print("\n== shortener inside proxy:", dict(shortener_stack))
print("== gview wrapping bwa:", dict(gview_stack))
print("\n== other workers.dev hostnames:", len(other_hosts))
for h, c in other_hosts.most_common(15):
    print(f"   {c:5d} {h}")
print("\n== sample decoded targets")
for r in targets[:8]:
    print(f"   {r['full_proxied_url'][:90]}")
    print(f"     -> {str(r['decoded_target'])[:120]}")
