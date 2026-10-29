#!/usr/bin/env python3
"""Intermediary-relay indicator sweep v3 — read-only, observational.

Lane 3 (2026-10-01): markdown.new + intermediary conversion services.
- census: ripgrep counts per indicator (fast, whole corpus)
- co-occurrence: only lines that mention a relay candidate are scored in
  Python (relay hit -> indicator regexes), preserving @timestamps.
Relay candidates scored by distinct co-occurring indicators (2+ outranks lone).
"""
import json, os, re, subprocess, sys
from collections import defaultdict, Counter

REPO = os.path.expanduser("~/workspace/silent-locus")
OUTDIR = os.path.join(REPO, "data/2026-10-01-intermediary-relays")
os.makedirs(OUTDIR, exist_ok=True)

INDICATORS = {
    "zz_label":        r"zz[a-z]{1,4}[0-9]{0,20}|ZZ[A-Z]{2,8}|A000\b",
    "github_remote_cache_zz": r"github-remote-cache/zz",
    "oai_tag":         r"oai[a-z]{0,24}[0-9]{2,20}",
    "epoch_nonce":     r"\b1[67][0-9]{8}(\.[0-9]+)?\b",
    "uniq_nonce":      r"[?&]uniq[0-9]*=",
    "httpbun":         r"httpbun",
    "httpbin":         r"httpbin",
    "allorigins":      r"allorigins",
    "dagd":            r"da\.gd",
    "tinyurl":         r"tinyurl",
    "go_import":       r"go-import",
    "arquivo_pt":      r"arquivo\.pt",
    "disposable_email":r"mailinator|guerrillamail|tempmail|10minutemail|yopmail|sharklasers|trashmail|getnada|fakeinbox|mohmal",
    "apikey_reuse":    r"api[_-]?key",
    "double_slash":    r"(?<=gov)//|//files/",
    "antibot_suffix":  r"[?&](output|raw|url|format|debug|f)=",
    "direct_ip":       r"https?://[0-9]{1,3}(\.[0-9]{1,3}){3}(:[0-9]+)?",
    "collusion_wiki":  r"collusion\.wiki",
}
RELAYS = {
    "markdown.new":     r"markdown\.new",
    "r.jina.ai":        r"r\.jina\.ai",
    "jina_workers":     r"r\.jina-ai\.workers\.dev",
    "pure.md":          r"pure\.md",
    "md.succ.ai":       r"md\.succ\.ai",
    "lemino_url2md":    r"lemino\.ai/api/url2md",
    "webcrawlerapi":    r"webcrawlerapi\.com",
    "magic_html_api":   r"magic-html-api",
    "jsonhero":         r"jsonhero\.io",
    "allorigins_relay": r"allorigins\.hexlet\.app",
    "cors_workers":     r"[a-z0-9-]{1,64}\.workers\.dev",
    "api_cors_lol":     r"api\.cors\.lol",
    "corsmirror":       r"corsmirror\.com",
    "gview":            r"docs\.google\.com/(gview|viewerng)",
    "httpbun_relay":    r"httpbun",
    "httpbin_relay":    r"httpbin\.org",
    "wayback":          r"web\.archive\.org",
}
GLOBS = ["-g", "*.jsonl", "-g", "*.jsonl.gz", "-g", "*.txt", "-g", "*.csv",
         "-g", "*.md", "-g", "*.json", "-g", "*.html", "-g", "*.log",
         "-g", "!*2026-10-01-*"]
DATA = os.path.join(REPO, "data")
EXCL = "2026-10-01-intermediary-relays"
SIBLING = "data/2026-10-01-"

def rg(args, **kw):
    return subprocess.run(["rg"] + args, capture_output=True, text=True,
                          timeout=kw.get("timeout", 900))

def main():
    ind_rx = {n: re.compile(p, re.I) for n, p in INDICATORS.items()}
    relay_rx = {n: re.compile(p, re.I) for n, p in RELAYS.items()}

    # --- census: per-indicator line counts + file counts (rg, fast) ---
    census, census_files = {}, {}
    for name, pat in INDICATORS.items():
        out = rg(["--no-messages", "-c", "-e", pat, DATA, "-z"] + GLOBS).stdout
        total, files = 0, 0
        for line in out.splitlines():
            if EXCL in line:
                continue
            f, _, c = line.rpartition(":")
            try:
                total += int(c); files += 1
            except ValueError:
                pass
        census[name] = total
        census_files[name] = files
        print(f"census {name}: {total} lines / {files} files", file=sys.stderr, flush=True)

    # --- relay candidate lines only (much smaller set) ---
    relay_pat = "|".join(f"(?:{p})" for p in RELAYS.values())
    out = rg(["--no-messages", "-N", "--no-filename", "-e", relay_pat, DATA, "-z"] + GLOBS).stdout
    relay_cooccur = defaultdict(Counter)
    relay_line_count = Counter()
    ts_samples = defaultdict(list)
    samples = []
    n = 0
    for line in out.splitlines():
        if EXCL in line:
            continue
        n += 1
        if len(line) > 20000:
            line = line[:20000]
        relays = {rn for rn, rx in relay_rx.items() if rx.search(line)}
        if not relays:
            continue
        hits = {hn for hn, rx in ind_rx.items() if rx.search(line)}
        for r in relays:
            relay_line_count[r] += 1
            for h in hits:
                relay_cooccur[r][h] += 1
            m = re.search(r'"@timestamp"\s*:\s*"([^"]+)"', line)
            if m and len(ts_samples[r]) < 40:
                ts_samples[r].append({"ts": m.group(1), "snippet": line[:300]})
            if len(samples) < 3000:
                samples.append({"relay": r, "text": line[:600]})
    print(f"relay lines scanned: {n}", file=sys.stderr, flush=True)

    scores = {}
    for relay, co in relay_cooccur.items():
        distinct = sorted(set(co) - {"collusion_wiki"})
        scores[relay] = {"distinct_indicators": len(distinct),
                         "total_cooccur_hits": sum(co.values()),
                         "line_matches": relay_line_count[relay],
                         "indicators": distinct,
                         "per_indicator": dict(co)}
    scores = dict(sorted(scores.items(),
                         key=lambda kv: (-kv[1]["distinct_indicators"],
                                         -kv[1]["total_cooccur_hits"])))
    with open(os.path.join(OUTDIR, "sweep_results.json"), "w") as fh:
        json.dump({"census": census, "census_files": census_files,
                   "relay_scores": scores, "ts_samples": dict(ts_samples)}, fh, indent=1)
    with open(os.path.join(OUTDIR, "sweep_samples.jsonl"), "w") as fh:
        for s in samples:
            fh.write(json.dumps(s) + "\n")
    print(json.dumps({"census": census,
                      "relay_scores": {k: {kk: vv for kk, vv in v.items() if kk != "per_indicator"}
                                       for k, v in scores.items()}}, indent=1))

if __name__ == "__main__":
    main()
