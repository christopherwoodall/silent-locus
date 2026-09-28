#!/usr/bin/env python3
"""Lane A pattern-battery sweep over captured ludism-wikis files.

Standard battery (read-only): zz labels, oai names, epoch nonces, proxy
wrappers, laundering chains, task-family signals.
Writes pattern-sweep.json (per-file hit table). Pure recon — no network.
"""
import json, os, re, hashlib

DDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "ludism-wikis")
OUT = DDIR + "/pattern-sweep.json"

PATTERNS = {
    "zz_label": re.compile(r"(?i)\bzz[a-z0-9_]{2,}\b"),
    "oai_name": re.compile(r"(?i)\boai[a-z0-9_.-]{2,}\b"),
    "epoch_nonce": re.compile(r"\b1[6-8]\d{8}\b"),
    "proxy_r_jina": re.compile(r"(?i)r\.jina\.ai"),
    "proxy_allorigins": re.compile(r"(?i)allorigins(?:\.hexlet\.app|\.win)?"),
    "proxy_cors": re.compile(r"(?i)(corsproxy\.io|proxy\.cors\.sh|api\.cors\.lol|corsmirror\.com|pure\.md)"),
    "proxy_proxymule": re.compile(r"(?i)proxymule\.com"),
    "laundering_gview": re.compile(r"(?i)(docs\.google\.com/(?:g)?viewer|drive\.google\.com/viewerng)"),
    "family_helper": re.compile(r"(?i)\b\w*Helper\d*\b"),
    "family_zzz_backup": re.compile(r"(?i)\bzzz\w*\b"),
    "family_openai_regcf": re.compile(r"(?i)OpenAIRegCFTest"),
    "task_county_json": re.compile(r"(?i)county\.json"),
    "task_sf133": re.compile(r"(?i)SF133"),
    "task_usaspending": re.compile(r"(?i)usaspending"),
    "task_clickhouse": re.compile(r"(?i)clickhouse"),
    "task_markerproxy": re.compile(r"(?i)markerproxy"),
    "ip_azure20": re.compile(r"\b20\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
    "ip_addr": re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
    "as8075": re.compile(r"\bAS8075\b"),
}

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def main():
    files = []
    for root, _, names in os.walk(DDIR):
        for n in sorted(names):
            if n in ("pattern-sweep.json", "manifest.jsonl"):
                continue
            p = os.path.join(root, n)
            files.append((os.path.relpath(p, DDIR), p))
    table = {}
    for rel, p in files:
        try:
            text = open(p, "rb").read().decode("utf-8", errors="replace")
        except Exception as e:
            table[rel] = {"error": str(e)}
            continue
        hits = {}
        for name, rx in PATTERNS.items():
            found = sorted(set(rx.findall(text)))
            if found:
                hits[name] = found[:25]
        table[rel] = {
            "sha256": sha256(p),
            "bytes": os.path.getsize(p),
            "pattern_hits": hits,
        }
    with open(OUT, "w") as f:
        json.dump(table, f, indent=2)
    total = sum(len(v.get("pattern_hits", {})) for v in table.values())
    print("files scanned:", len(table), "| files with hits:", sum(1 for v in table.values() if v.get("pattern_hits")))
    for rel, v in sorted(table.items()):
        h = v.get("pattern_hits", {})
        if h:
            print("%s: %s" % (rel, ", ".join(sorted(h))))

if __name__ == "__main__":
    main()
