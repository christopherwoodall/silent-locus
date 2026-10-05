#!/usr/bin/env python3
"""Intermediary-relay indicator sweep — read-only, observational.

Lane 3 (2026-10-01): markdown.new + intermediary conversion services.
Full indicator set per steering update: scores relay candidates by
co-occurring indicator count (2+ outranks lone hits), preserves timestamps
where present.

Usage: python3 sweep_indicators.py  (run from repo root)
Output: data/2026-10-01-intermediary-relays/sweep_results.json
"""
import gzip, json, os, re, sys
from collections import defaultdict, Counter

REPO = os.path.expanduser("~/workspace/silent-locus")
OUTDIR = os.path.join(REPO, "data/2026-10-01-intermediary-relays")
os.makedirs(OUTDIR, exist_ok=True)

# ---------- indicator definitions (regex -> name) ----------
INDICATORS = {
    "zz_label":        re.compile(r"zz[a-z]{1,3}\d*|ZZ[A-Z]{2,}|A000\b", re.I),
    "github_remote_cache_zz": re.compile(r"github-remote-cache/zz"),
    "oai_tag":         re.compile(r"oai[a-z]*\d{2,}", re.I),
    "epoch_nonce":     re.compile(r"\b1[67]\d{8}(?:\.\d+)?\b"),
    "uniq_nonce":      re.compile(r"[?&]uniq\d*=", re.I),
    "httpbun":         re.compile(r"httpbun", re.I),
    "httpbin":         re.compile(r"httpbin", re.I),
    "allorigins":      re.compile(r"allorigins", re.I),
    "dagd":            re.compile(r"(?<!\w)da\.gd", re.I),
    "go_import":       re.compile(r"go-import"),
    "arquivo_pt":      re.compile(r"arquivo\.pt", re.I),
    "disposable_email":re.compile(r"mailinator|guerrillamail|tempmail|10minutemail|yopmail|sharklasers|trashmail|getnada|fakeinbox|mohmal", re.I),
    "apikey_reuse":    re.compile(r"api[_-]?key", re.I),
    "double_slash":    re.compile(r"(?<=gov)//|(?<=sec)//|//files/|//\?"),
    "antibot_suffix":  re.compile(r"[?&](output|raw|url|format|debug|f)=[^&\s]*", re.I),
    "direct_ip":       re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?"),
    "collusion_wiki":  re.compile(r"collusion\.wiki", re.I),
}

# relay candidates (conversion/reader/relay services)
RELAYS = {
    "markdown.new":        re.compile(r"markdown\.new", re.I),
    "r.jina.ai":           re.compile(r"r\.jina\.ai", re.I),
    "jina_workers":        re.compile(r"r\.jina-ai\.workers\.dev", re.I),
    "pure.md":             re.compile(r"(?<![\w.])pure\.md", re.I),
    "md.succ.ai":          re.compile(r"md\.succ\.ai", re.I),
    "lemino_url2md":       re.compile(r"lemino\.ai/api/url2md", re.I),
    "webcrawlerapi":       re.compile(r"webcrawlerapi\.com", re.I),
    "magic_html_api":      re.compile(r"magic-html-api", re.I),
    "jsonhero":            re.compile(r"jsonhero\.io", re.I),
    "allorigins_relay":    re.compile(r"allorigins\.hexlet\.app", re.I),
    "cors_workers":        re.compile(r"[\w-]+\.workers\.dev", re.I),
    "api_cors_lol":        re.compile(r"api\.cors\.lol", re.I),
    "gview":               re.compile(r"docs\.google\.com/(gview|viewerng)", re.I),
    "arquivo_pt_relay":    re.compile(r"arquivo\.pt", re.I),
    "httpbun_relay":       re.compile(r"httpbun", re.I),
    "httpbin_relay":       re.compile(r"httpbin\.org", re.I),
    "wayback":             re.compile(r"web\.archive\.org", re.I),
}

TEXT_EXTS = (".jsonl", ".jsonl.gz", ".txt", ".csv", ".md", ".json", ".html", ".log")

def iter_lines(path):
    try:
        if path.endswith(".gz"):
            fh = gzip.open(path, "rt", encoding="utf-8", errors="replace")
        else:
            fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return
    with fh:
        for line in fh:
            yield line

def scan():
    census = Counter()                       # indicator -> total hits
    census_files = defaultdict(set)          # indicator -> set of files
    relay_lines = defaultdict(list)          # relay -> list of (file, lineno, line) up to cap
    relay_cooccur = defaultdict(Counter)     # relay -> indicator -> co-occurrence lines
    ts_samples = defaultdict(list)           # relay -> list of (timestamp, snippet)
    files_scanned = 0
    skipped = []
    for root, dirs, files in os.walk(os.path.join(REPO, "data")):
        if "frames" in root:  # animation work dirs, not corpus
            continue
        for fn in files:
            if not fn.lower().endswith(TEXT_EXTS):
                continue
            p = os.path.join(root, fn)
            try:
                if os.path.getsize(p) > 200_000_000:
                    skipped.append(p); continue
            except OSError:
                continue
            files_scanned += 1
            for ln, line in enumerate(iter_lines(p)):
                hits = {name for name, rx in INDICATORS.items() if rx.search(line)}
                relays_hit = {name for name, rx in RELAYS.items() if rx.search(line)}
                for h in hits:
                    census[h] += 1
                    census_files[h].add(os.path.relpath(p, REPO))
                if relays_hit:
                    # timestamp: parse @timestamp from events-style json lines
                    ts = None
                    if '"@timestamp"' in line:
                        m = re.search(r'"@timestamp"\s*:\s*"([^"]+)"', line)
                        if m: ts = m.group(1)
                    for r in relays_hit:
                        if len(relay_lines[r]) < 400:
                            relay_lines[r].append({"file": os.path.relpath(p, REPO),
                                                   "line": ln, "text": line.strip()[:600]})
                        for h in hits:
                            relay_cooccur[r][h] += 1
                        if ts and len(ts_samples[r]) < 30:
                            ts_samples[r].append({"ts": ts, "snippet": line.strip()[:300]})
    return {
        "files_scanned": files_scanned,
        "skipped_too_large": [os.path.relpath(s, REPO) for s in skipped],
        "census": dict(census),
        "census_files": {k: len(v) for k, v in census_files.items()},
        "relay_cooccur": {r: dict(c) for r, c in relay_cooccur.items()},
        "ts_samples": dict(ts_samples),
    }

def main():
    res = scan()
    # score relays: distinct co-occurring indicators (2+ outranks lone)
    scores = {}
    for relay, co in res["relay_cooccur"].items():
        distinct = [i for i in co if i not in ("collusion_wiki",)]
        scores[relay] = {"distinct_indicators": len(distinct),
                         "total_cooccur_hits": sum(co.values()),
                         "indicators": sorted(distinct)}
    res["relay_scores"] = dict(sorted(scores.items(),
                                     key=lambda kv: (-kv[1]["distinct_indicators"],
                                                     -kv[1]["total_cooccur_hits"])))
    with open(os.path.join(OUTDIR, "sweep_results.json"), "w") as f:
        json.dump({k: v for k, v in res.items() if k != "relay_lines"}, f, indent=1)
    with open(os.path.join(OUTDIR, "sweep_samples.jsonl"), "w") as f:
        for relay, rows in relay_lines.items():
            for row in rows:
                f.write(json.dumps({"relay": relay, **row}) + "\n")
    print(json.dumps({
        "files_scanned": res["files_scanned"],
        "census": res["census"],
        "census_files": res["census_files"],
        "relay_scores": res["relay_scores"],
    }, indent=1))

if __name__ == "__main__":
    main()
