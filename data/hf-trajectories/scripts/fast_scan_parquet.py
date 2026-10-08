#!/usr/bin/env python3
"""Fast whole-corpus scan of parquet text columns (phase 1).

Reads all string-ish columns, concatenates per file, runs single regex passes.
If zero hits -> row-level scan adds nothing. If hits -> prints distinct contexts
for triage (byte-level), then caller can do row attribution.
"""
import sys, re, json
import pyarrow.parquet as pq

pq_path, slug = sys.argv[1], sys.argv[2]

SHARP = re.compile(r'(?i)captcha|turnstile|cloudflare|prove you are human|verify you are human|are you a robot|bot[\s-]?check|anti[\s-]?bot')
SOLVED = re.compile(r'(?i)(captcha is solved|turnstile.{0,40}solved|challenge (solved|passed|bypassed)|bypass(ed|ing)? cloudflare|fetched \(200\)|cloudflare (solved|bypassed|defeat))')
OAI = re.compile(r'(?i)\boai[:_-][a-z0-9_-]+\b')
OAI_PMH = re.compile(r'(?i)pmh:oai|oai:(arxiv|repec|openalex|pubmed|doi)')
ZZ = re.compile(r'[?&](zz|zz_oai|oai)=[^&\s"\']{1,80}')
DD = re.compile(r'(?i)(webhook\.site|ntfy\.sh|requestbin\.com|pipedream|beeceptor|webhookrelay|httpb?un\.(org|com|net|dev))')
AMAP = re.compile(r'(?i)(task-oai-\d+|northflank|amap\.com|B\d{10}[A-Z0-9]{2}|probe\.js|jina\.ai)')
BID = re.compile(r'[Bb]\d{10}[A-Za-z0-9]{2}')

table = pq.read_table(pq_path)
print(f"{slug}: rows={table.num_rows}", flush=True)

# collect text
chunks = []
for col in table.columns:
    def walk(arr):
        for v in arr:
            if v is None or (hasattr(v, 'as_py') and v.as_py() is None):
                continue
            try:
                py = v.as_py()
            except Exception:
                continue
            if isinstance(py, str):
                chunks.append(py)
            elif isinstance(py, bytes):
                chunks.append(py.decode('utf-8', 'replace'))
            elif isinstance(py, (list, tuple)):
                for x in py:
                    if isinstance(x, str): chunks.append(x)
                    elif isinstance(x, dict):
                        for vv in x.values():
                            if isinstance(vv, str): chunks.append(vv)
            elif isinstance(py, dict):
                for vv in py.values():
                    if isinstance(vv, str): chunks.append(vv)
    walk(col)
big = '\n'.join(chunks)
print(f"  text chars: {len(big)}", flush=True)

def contexts(rx, n=12):
    seen = {}
    for m in rx.finditer(big):
        key = m.group(0)[:60]
        if key not in seen:
            s = max(0, m.start()-180)
            seen[key] = big[s:m.end()+180]
        if len(seen) >= n:
            break
    return seen

out = {'slug': slug, 'rows': table.num_rows, 'chars': len(big)}
for name, rx in [('sharp', SHARP), ('solved', SOLVED), ('oai', OAI), ('zz', ZZ), ('deaddrop', DD), ('amap', AMAP)]:
    ctxs = contexts(rx)
    out[name] = [{'match': k, 'ctx': v.replace('\n', ' ')[:400]} for k, v in ctxs.items()]
    # rule out OAI-PMH
    if name == 'oai':
        out[name] = [c for c in out[name] if not OAI_PMH.search(c['ctx'])]
    print(f"  {name}: {len(out[name])} distinct", flush=True)

# BID handled separately: report count + sample contexts (usually hex FPs)
bid_ctxs = contexts(BID, n=8)
out['bid'] = [{'match': k, 'ctx': v.replace('\n', ' ')[:300]} for k, v in bid_ctxs.items()]
print(f"  bid: {len(out['bid'])} distinct", flush=True)

json.dump(out, open(sys.argv[3], 'w'), indent=1)
print("WROTE " + sys.argv[3], flush=True)
