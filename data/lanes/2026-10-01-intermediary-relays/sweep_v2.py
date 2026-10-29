#!/usr/bin/env python3
"""Intermediary-relay indicator sweep v2 — read-only, observational.

Lane 3 (2026-10-01): markdown.new + intermediary conversion services.
Two-stage: ripgrep extracts candidate lines (fast), Python scores
co-occurring indicators per relay candidate (2+ distinct indicators
outranks lone hits) and preserves @timestamps.

Usage: bash sweep.sh  (run from repo root)
"""
import json, os, re, subprocess, sys
from collections import defaultdict, Counter

REPO = os.path.expanduser("~/workspace/silent-locus")
OUTDIR = os.path.join(REPO, "data/2026-10-01-intermediary-relays")
os.makedirs(OUTDIR, exist_ok=True)

INDICATORS = {
    "zz_label":        re.compile(r"zz[a-z]{1,4}\d{0,20}|ZZ[A-Z]{2,8}|A000\b", re.I),
    "github_remote_cache_zz": re.compile(r"github-remote-cache/zz"),
    "oai_tag":         re.compile(r"oai[a-z]{0,24}\d{2,20}", re.I),
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
    "double_slash":    re.compile(r"(?<=gov)//|//files/"),
    "antibot_suffix":  re.compile(r"[?&](output|raw|url|format|debug|f)=[^&\s\"']*", re.I),
    "direct_ip":       re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?"),
    "collusion_wiki":  re.compile(r"collusion\.wiki", re.I),
}
RELAYS = {
    "markdown.new":     re.compile(r"markdown\.new", re.I),
    "r.jina.ai":        re.compile(r"r\.jina\.ai", re.I),
    "jina_workers":     re.compile(r"r\.jina-ai\.workers\.dev", re.I),
    "pure.md":          re.compile(r"pure\.md", re.I),
    "md.succ.ai":       re.compile(r"md\.succ\.ai", re.I),
    "lemino_url2md":    re.compile(r"lemino\.ai/api/url2md", re.I),
    "webcrawlerapi":    re.compile(r"webcrawlerapi\.com", re.I),
    "magic_html_api":   re.compile(r"magic-html-api", re.I),
    "jsonhero":         re.compile(r"jsonhero\.io", re.I),
    "allorigins_relay": re.compile(r"allorigins\.hexlet\.app", re.I),
    "cors_workers":     re.compile(r"[\w-]{1,64}\.workers\.dev", re.I),
    "api_cors_lol":     re.compile(r"api\.cors\.lol", re.I),
    "gview":            re.compile(r"docs\.google\.com/(gview|viewerng)", re.I),
    "arquivo_pt_relay": re.compile(r"arquivo\.pt", re.I),
    "httpbun_relay":    re.compile(r"httpbun", re.I),
    "httpbin_relay":    re.compile(r"httpbin\.org", re.I),
    "wayback":          re.compile(r"web\.archive\.org", re.I),
}

# combined ripgrep pattern (Rust regex, no lookbehind)
COMBINED = (r"markdown\.new|r\.jina\.ai|pure\.md|md\.succ\.ai|lemino\.ai/api/url2md|"
            r"webcrawlerapi\.com|magic-html-api|jsonhero\.io|allorigins|workers\.dev|"
            r"api\.cors\.lol|docs\.google\.com/(gview|viewerng)|arquivo\.pt|httpbun|httpbin|"
            r"github-remote-cache/zz|go-import|mailinator|guerrillamail|tempmail|"
            r"10minutemail|yopmail|sharklasers|trashmail|getnada|da\.gd|tinyurl|"
            r"collusion\.wiki|\b1[67][0-9]{8}\b|[?&]uniq[0-9]*=|oai[a-z]*[0-9]{2,}|"
            r"zz[a-z]{1,3}[0-9]*")

def main():
    cand = os.path.join(OUTDIR, "candidates.txt")
    data_dir = os.path.join(REPO, "data")
    cmd = ["rg", "-l" , "--no-messages", "-e", COMBINED, data_dir,
           "-g", "*.jsonl", "-g", "*.jsonl.gz", "-g", "*.txt", "-g", "*.csv",
           "-g", "*.md", "-g", "*.json", "-g", "*.html", "-g", "*.log",
           "-z"]  # -z searches inside gz
    # stage 1: list matching files
    files = subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()
    print(f"candidate files: {len(files)}", file=sys.stderr)
    census = Counter(); census_files = defaultdict(set)
    relay_cooccur = defaultdict(Counter)
    relay_line_count = Counter()
    ts_samples = defaultdict(list)
    samples = []
    files = [f for f in files if "2026-10-01-intermediary-relays" not in f]
    for fi, f in enumerate(files):
        if fi % 50 == 0:
            print(f"[{fi}/{len(files)}] {f}", file=sys.stderr, flush=True)
        # stage 1b: matching lines with line numbers
        cmd2 = ["rg", "-N", "--no-messages", "--no-filename", "-e", COMBINED, f, "-z"]
        try:
            out = subprocess.run(cmd2, capture_output=True, text=True, timeout=600).stdout
        except subprocess.TimeoutExpired:
            print(f"TIMEOUT {f}", file=sys.stderr); continue
        rel = os.path.relpath(f, REPO)
        for line in out.splitlines():
            if len(line) > 20000:
                line = line[:20000]  # cap: avoids regex blowup on minified blobs; full lines remain in sources
            hits = {n for n, rx in INDICATORS.items() if rx.search(line)}
            relays = {n for n, rx in RELAYS.items() if rx.search(line)}
            for h in hits:
                census[h] += 1; census_files[h].add(rel)
            for r in relays:
                relay_line_count[r] += 1
                for h in hits:
                    relay_cooccur[r][h] += 1
                ts = None
                m = re.search(r'"@timestamp"\s*:\s*"([^"]+)"', line)
                if m: ts = m.group(1)
                if ts and len(ts_samples[r]) < 40:
                    ts_samples[r].append({"ts": ts, "snippet": line[:300]})
                if len(samples) < 3000:
                    samples.append({"relay": r, "file": rel, "text": line[:600]})
    scores = {}
    for relay, co in relay_cooccur.items():
        distinct = sorted(set(co) - {"collusion_wiki"})
        scores[relay] = {"distinct_indicators": len(distinct),
                         "total_cooccur_hits": sum(co.values()),
                         "line_matches": relay_line_count[relay],
                         "indicators": distinct,
                         "per_indicator": dict(co)}
    scores = dict(sorted(scores.items(), key=lambda kv: (-kv[1]["distinct_indicators"],
                                                         -kv[1]["total_cooccur_hits"])))
    with open(os.path.join(OUTDIR, "sweep_results.json"), "w") as fh:
        json.dump({"census": dict(census),
                   "census_files": {k: len(v) for k, v in census_files.items()},
                   "relay_scores": scores,
                   "ts_samples": dict(ts_samples)}, fh, indent=1)
    with open(os.path.join(OUTDIR, "sweep_samples.jsonl"), "w") as fh:
        for s in samples:
            fh.write(json.dumps(s) + "\n")
    print(json.dumps({"census": dict(census),
                      "relay_scores": {k: {kk: vv for kk, vv in v.items() if kk != "per_indicator"} for k, v in scores.items()}},
                     indent=1))

if __name__ == "__main__":
    main()
