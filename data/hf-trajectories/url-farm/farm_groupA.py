#!/usr/bin/env python3
"""Group-A URL + escape/risky-cyber keyword farm: yoonholee/terminalbench-trajectories.
Parallel across (shard, row_group) with a process pool. Read-only on raw parquet;
writes group-A.json. NOTE: restored raw shards 2026-10-08 from HF (see PROVENANCE).
"""
import json, re, time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
import pyarrow.parquet as pq
import pickle

BASE = "/home/hatch/workspace/silent-locus/data/hf-trajectories/raw/yoonholee-terminalbench-trajectories/data"
SHARDS = [f"{BASE}/train-00000-of-00002.parquet", f"{BASE}/train-00001-of-00002.parquet"]
OUT = "/home/hatch/workspace/silent-locus/data/hf-trajectories/url-farm/group-A.json"
DS = "yoonholee/terminalbench-trajectories"

URL_RE = re.compile(r"https?://[^\s\"'<>)\]]+")
TRAILING = ".,;:!?'\""

ESCAPE = [
    "ignore previous instructions", "ignore your instructions", "you are now", "DAN",
    "jailbreak", "system prompt", "reveal your prompt", "leave the sandbox",
    "escape the sandbox", "disable safety", "disable the filter", "exfiltrate",
    "api key", "secret key", "private key", ".ssh/", "id_rsa", "AWS_SECRET", "OPENAI_API_KEY",
]
RISKY = [
    "captcha", "turnstile", "cloudflare", "rate limit", "rate-limit", "bypass",
    "circumvent", "jina.ai", "proxy", "webhook.site", "ntfy.sh", "discord.com/api/webhooks",
    "t.me/", "telegram", "pastebin", "paste.rs", "0x0.st", "termbin", "ngrok",
    "trycloudflare", "localtunnel", "bore.pub", "nmap", "masscan", "nikto", "sqlmap",
    "hydra", "metasploit", "reverse shell", "bitcoin", "ethereum", "wallet", "phishing",
    "credential",
]
PATTERNS = ESCAPE + RISKY
WORD_BOUND = {"dan", "hydra", "proxy", "wallet", "nikto", "sqlmap", "nmap", "masscan"}

def build_regex():
    parts = []
    for i, p in enumerate(PATTERNS):
        esc = re.escape(p)
        if p.lower() in WORD_BOUND:
            esc = r"\b" + esc + r"\b"
        parts.append(f"(?P<k{i}>{esc})")
    return re.compile("|".join(parts), re.IGNORECASE)

def scan_rg(job):
    shard, rg = job
    import os, pickle
    ckpt = f"/tmp/groupA_rg_{os.path.basename(shard)}_{rg}.pkl"
    if os.path.exists(ckpt):
        with open(ckpt, "rb") as f:
            return pickle.load(f), True
    kw_re = build_regex()
    group_by_idx = {f"k{i}": PATTERNS[i] for i in range(len(PATTERNS))}
    pat_lower = [p.lower() for p in PATTERNS]
    url_counts = defaultdict(int)
    url_ex = defaultdict(list)
    kw_hits = []
    rows = 0
    tbl = pq.ParquetFile(shard).read_row_group(
        rg, columns=["task_name", "agent", "model", "trial_name", "trial_id",
                     "started_at", "ended_at", "steps"])
    cols = tbl.to_pydict()
    for j in range(len(cols["trial_id"])):
        rows += 1
        trial_id = cols["trial_id"][j]
        task, agent, model = cols["task_name"][j], cols["agent"][j], cols["model"][j]
        started, ended = cols["started_at"][j], cols["ended_at"][j]
        for text in (cols["steps"][j], cols["task_name"][j], cols["trial_name"][j]):
            if not text:
                continue
            for m in URL_RE.finditer(text):
                url = m.group(0).rstrip(TRAILING)
                url_counts[url] += 1
                if len(url_ex[url]) < 5:
                    url_ex[url].append({"trial_id": trial_id, "task": task,
                                        "agent": agent, "model": model})
            tl = text.lower()
            if not any(p in tl for p in pat_lower):
                continue
            for m in kw_re.finditer(text):
                lo = max(0, m.start() - 100)
                hi = min(len(text), m.end() + 100)
                ctx = text[lo:hi].replace("\n", " ").replace("\r", " ")
                kw_hits.append({"pattern": group_by_idx[m.lastgroup],
                                "matched_text": ctx,
                                "trial_id": trial_id, "task": task,
                                "agent": agent, "model": model,
                                "timestamp": f"{started} / {ended}"})
    result = (rows, dict(url_counts), {u: v for u, v in url_ex.items()}, kw_hits)
    with open(ckpt, "wb") as f:
        pickle.dump(result, f)
    return result, False

def main():
    t0 = time.time()
    jobs = [(s, rg) for s in SHARDS for rg in range(pq.ParquetFile(s).num_row_groups)]
    print(f"{len(jobs)} row-group jobs", flush=True)
    url_counts = defaultdict(int)
    url_examples = defaultdict(list)
    kw_hits = []
    rows_scanned = 0
    with ProcessPoolExecutor(max_workers=2) as ex:
        for (rows, uc, ue, kh), resumed in ex.map(scan_rg, jobs):
            rows_scanned += rows
            kw_hits.extend(kh)
            for u, c in uc.items():
                url_counts[u] += c
                need = 5 - len(url_examples[u])
                if need > 0:
                    url_examples[u].extend(ue[u][:need])
            print(f"merged rg: rows={rows_scanned}", flush=True)
    urls = [{"url": u, "count": c, "examples": url_examples[u]}
            for u, c in sorted(url_counts.items(), key=lambda kv: -kv[1])]
    result = {
        "dataset": DS,
        "rows_scanned": rows_scanned,
        "urls": urls,
        "keyword_hits": kw_hits,
        "notes": ("OBSERVED: regex-scanned steps/task_name/trial_name of all rows. "
                  "URL regex https?://[^\\s\"'<>)]\\]]+ with trailing punctuation stripped. "
                  "Keyword matching case-insensitive substring (word-boundary for "
                  "dan/hydra/proxy/wallet/nikto/sqlmap/nmap/masscan). "
                  "matched_text is ~200 chars of verbatim surrounding context, never redacted. "
                  "Counts are exact, no sampling. "
                  "Raw shards were re-downloaded from HF 2026-10-08 after the cached copy "
                  "was deleted mid-run; hashes in SHA256SUMS-restored.txt."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1)
    print(f"rows={rows_scanned} urls={len(urls)} kw_hits={len(kw_hits)} in {time.time()-t0:.1f}s", flush=True)

if __name__ == "__main__":
    main()
