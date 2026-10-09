#!/usr/bin/env python3
"""Group-C URL + escape/risky-cyber keyword farm.

Datasets (read-only):
  - tiger-lab-swe-next-sft-trajectories : SWE_Next_SFT_Trajectories.jsonl (2,473 rows)
  - 0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces : traces/<task>/... (89 tasks)
  - djlougen-hermes-agent-traces-filtered : data/train.jsonl (3,679 rows)

Writes data/hf-trajectories/url-farm/group-C2.json. Commits nothing.

Method note: keyword scan uses lowercased text + str.find per pattern (C speed,
Two's-complement BMH) with manual \\b checks for the WORD_BOUND set. Semantics
are identical to the case-insensitive alternation used by farm_groupA.py
(leftmost, non-overlapping per pattern; no two patterns share a start offset).
"""
import json, os, re, time
from collections import defaultdict

BASE = "/home/hatch/workspace/silent-locus/data/hf-trajectories/raw"
OUT = "/home/hatch/workspace/silent-locus/data/hf-trajectories/url-farm/group-C2.json"

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
LOWER_PATTERNS = [p.lower() for p in PATTERNS]
WORD_BOUND = {"dan", "hydra", "proxy", "wallet", "nikto", "sqlmap", "nmap", "masscan"}
WORD_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789_")

url_counts = defaultdict(int)        # (dataset, url) -> count
url_examples = defaultdict(list)    # (dataset, url) -> [example refs]
kw_hits = []


def find_keyword_hits(text):
    """Yield (pattern, start, end) for every keyword occurrence in text."""
    low = text.lower()
    n = len(text)
    for idx, p in enumerate(LOWER_PATTERNS):
        pat = PATTERNS[idx]
        wb = p in WORD_BOUND
        s = low.find(p)
        while s != -1:
            e = s + len(p)
            ok = True
            if wb:
                if s > 0 and low[s - 1] in WORD_CHARS:
                    ok = False
                elif e < n and low[e] in WORD_CHARS:
                    ok = False
            if ok:
                yield pat, s, e
            s = low.find(p, s + 1)


def record_urls(dataset, text, ref):
    for m in URL_RE.finditer(text):
        url = m.group(0).rstrip(TRAILING)
        key = (dataset, url)
        url_counts[key] += 1
        if len(url_examples[key]) < 5:
            url_examples[key].append(ref)


def record_kws(dataset, text, ref):
    for pat, s, e in find_keyword_hits(text):
        lo = max(0, s - 100)
        hi = min(len(text), e + 100)
        ctx = text[lo:hi].replace("\n", " ").replace("\r", " ")
        hit = {"pattern": pat, "matched_text": ctx, "dataset": dataset}
        hit.update(ref)
        kw_hits.append(hit)


def iter_json_values(path):
    """Yield parsed JSON values from a file, tolerant of embedded newlines."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        buf = f.read()
    dec = json.JSONDecoder()
    i, n = 0, len(buf)
    while i < n:
        while i < n and buf[i] in " \t\r\n":
            i += 1
        if i >= n:
            break
        obj, j = dec.raw_decode(buf, i)
        yield obj
        i = j


def flatten_strings(obj, sep="\n"):
    """Concatenate all string values; separator blocks cross-field URL glue."""
    parts = []

    def walk(o):
        if isinstance(o, str):
            parts.append(o)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, (list, tuple)):
            for v in o:
                walk(v)

    walk(obj)
    return sep.join(parts)


def main():
    t0 = time.time()
    rows_scanned = {}

    # ---- Dataset 1: tiger-lab ----
    ds = "tiger-lab/swe-next-sft-trajectories"
    n = 0
    path = f"{BASE}/tiger-lab-swe-next-sft-trajectories/SWE_Next_SFT_Trajectories.jsonl"
    if not os.path.exists(path):
        print(f"{ds}: INPUT MISSING ({path}) - raw data deleted, see notes", flush=True)
        rows_scanned[ds] = 0
    else:
        for i, row in enumerate(iter_json_values(path)):
            n += 1
            for msg in (row.get("messages") or []):
                content = msg.get("content") or ""
                ref = {"file": "SWE_Next_SFT_Trajectories.jsonl", "row": i,
                       "role": msg.get("role"), "task": None, "agent": None,
                       "model": None, "timestamp": None}
                record_urls(ds, content, ref)
                record_kws(ds, content, ref)
            if n % 500 == 0:
                print(f"  {ds}: {n} rows", flush=True)
        rows_scanned[ds] = n
        print(f"{ds}: {n} rows", flush=True)

    # ---- Dataset 2: djlougen ----
    ds = "djlougen/hermes-agent-traces-filtered"
    n = 0
    path = f"{BASE}/djlougen-hermes-agent-traces-filtered/data/train.jsonl"
    if not os.path.exists(path):
        print(f"{ds}: INPUT MISSING ({path}) - raw data deleted, see notes", flush=True)
        rows_scanned[ds] = 0
    else:
        for i, row in enumerate(iter_json_values(path)):
            n += 1
            text = flatten_strings(row)
            ref = {"file": "data/train.jsonl", "row": i, "id": row.get("id"),
                   "task": row.get("task"), "agent": None, "model": None,
                   "timestamp": None}
            record_urls(ds, text, ref)
            record_kws(ds, text, ref)
            if n % 500 == 0:
                print(f"  {ds}: {n} rows", flush=True)
        rows_scanned[ds] = n
        print(f"{ds}: {n} rows", flush=True)

    # ---- Dataset 3: 0xsero ----
    ds = "0xsero/glm-5.2-nf3-hybrid-terminal-bench-2.1-traces"
    traces = f"{BASE}/0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces/traces"
    files = 0
    tasks = 0
    if not os.path.isdir(traces):
        print(f"{ds}: INPUT MISSING ({traces}) - raw data deleted, see notes", flush=True)
        rows_scanned[ds] = 0
    else:
        for task in sorted(os.listdir(traces)):
            tdir = os.path.join(traces, task)
            if not os.path.isdir(tdir):
                continue
            tasks += 1
            for root, _dirs, fns in os.walk(tdir):
                for fn in fns:
                    fp = os.path.join(root, fn)
                    rel = os.path.relpath(fp, traces)
                    files += 1
                    if fn == "trajectory.json":
                        try:
                            traj = json.load(open(fp, encoding="utf-8", errors="replace"))
                        except Exception as e:
                            print(f"  PARSE FAIL {rel}: {e}", flush=True)
                            continue
                        ag = traj.get("agent") or {}
                        agent = ag.get("name")
                        model = ag.get("model_name")
                        for step in (traj.get("steps") or []):
                            msg = step.get("message")
                            text = msg if isinstance(msg, str) else json.dumps(msg, ensure_ascii=False)
                            ref = {"file": rel, "row": step.get("step_id"), "task": task,
                                   "agent": agent, "model": model,
                                   "timestamp": step.get("timestamp")}
                            record_urls(ds, text, ref)
                            record_kws(ds, text, ref)
                    else:
                        with open(fp, "rb") as f:
                            text = f.read().decode("utf-8", errors="replace")
                        ref = {"file": rel, "row": None, "task": task,
                               "agent": "terminus-2", "model": "openai/GLM-5.2",
                               "timestamp": None}
                        record_urls(ds, text, ref)
                        record_kws(ds, text, ref)
    rows_scanned[ds] = files
    print(f"{ds}: {files} files across {tasks} tasks", flush=True)

    urls = []
    for (dataset, url), c in sorted(url_counts.items(), key=lambda kv: -kv[1]):
        urls.append({"url": url, "count": c, "dataset": dataset,
                     "examples": url_examples[(dataset, url)]})

    result = {
        "datasets": [{"name": d, "rows_scanned": c} for d, c in rows_scanned.items()],
        "urls": urls,
        "keyword_hits": kw_hits,
        "notes": ("RESTORED RUN 2026-10-08 (group-C2): raw data for all three group-C datasets was re-downloaded "
                  "from HuggingFace via curl after the 2026-10-08 ~03:11 UTC wipe (OBSERVED: dir mtimes) that left "
                  "group-C.json a partial run (0/0/86 trial.log-only). Revs pinned at restore time: "
                  "tiger-lab/swe-next-sft-trajectories=e378a60ddd7050fe9519a31a4d41d4872eeec6ac, "
                  "djlougen/hermes-agent-traces-filtered=f91a8ef669194408a706741cd6f32a1686a8fd78, "
                  "0xsero/glm-5.2-nf3-hybrid-terminal-bench-2.1-traces=6020a41cb40ca06761d96250d80afef96d086e2a. "
                  "Per-dataset PROVENANCE.md keeps the original retrieval; SHA256SUMS-restored.txt in each raw dir "
                  "records the fresh retrieval time, method, and sha256 of every restored file. "
                  "0xsero: all traces/<task>/* files restored; pre-restore trial.log hashes preserved in "
                  "trial-log-pre-restore-hashes.txt for upstream-change comparison. "
                  "ANOMALIES OBSERVED at restore: (1) tiger-lab jsonl is 215,812,925 bytes / 3,693 rows vs "
                  "2026-10-07 PROVENANCE 2 files / 197,571,616 bytes and farm docstring 2,473 rows; "
                  "(2) djlougen train.jsonl is 365,720,348 bytes / 3,679 rows vs 2026-10-07 7 files / 83,401,798 bytes "
                  "(same 3,679 rows, ~4.4x larger); (3) 0xsero totals 88MB vs prior 89.6MB, but all 86 surviving "
                  "trial.logs are byte-identical to pre-wipe hashes (0 changed) - 0xsero appears stable. "
                  "Old bulk files were wiped so no direct old-hash comparison is possible for tiger-lab/djlougen; "
                  "upstream datasets were republished between the two retrievals (INFERENCE from byte/row deltas). "
                  "OBSERVED: regex-scanned all text of every row/file actually present. "
                  "URL regex https?://[^\\s\"'<>)]\\]]+ with trailing punctuation stripped; "
                  "deduped per dataset with exact occurrence counts. "
                  "Keyword matching case-insensitive (word-boundary for DAN/hydra/proxy/wallet/nikto/sqlmap/nmap/masscan); "
                  "matched_text is ~200 chars of verbatim surrounding context, never redacted. "
                  "Counts are exact over scanned input, no sampling. "
                  "INFERENCE: none in this file; interpretation of hits belongs to the audit lanes."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1)

    print(f"done in {time.time()-t0:.1f}s: urls={len(urls)} kw_hits={len(kw_hits)}", flush=True)
    per_pat = defaultdict(int)
    for h in kw_hits:
        per_pat[(h["dataset"], h["pattern"])] += 1
    for (d, p), c in sorted(per_pat.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {d} :: {p!r}: {c}")


if __name__ == "__main__":
    main()
