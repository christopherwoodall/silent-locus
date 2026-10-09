#!/usr/bin/env python3
"""Chunk-level streaming scan of a single parquet row group (low memory)."""
import sys, re, json
import pyarrow.parquet as pq

pq_path, rg_idx, slug, out_path = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]

SHARP = re.compile(r'(?i)captcha|turnstile|cloudflare|prove you are human|verify you are human|are you a robot|bot[\s-]?check|anti[\s-]?bot')
SOLVED = re.compile(r'(?i)(captcha is solved|turnstile.{0,40}solved|challenge (solved|passed|bypassed)|bypass(ed|ing)? cloudflare|fetched \(200\)|cloudflare (solved|bypassed|defeat))')
OAI = re.compile(r'(?i)\boai[:_-][a-z0-9_-]+\b')
OAI_PMH = re.compile(r'(?i)pmh:oai|oai:(arxiv|repec|openalex|pubmed|doi)')
ZZ = re.compile(r'[?&](zz|zz_oai|oai)=[^&\s"\']{1,80}')
DD = re.compile(r'(?i)(webhook\.site|ntfy\.sh|requestbin\.com|pipedream|beeceptor|webhookrelay|httpb?un\.(org|com|net|dev))')
AMAP = re.compile(r'(?i)(task-oai-\d+|northflank|amap\.com|B\d{10}[A-Z0-9]{2}|probe\.js|jina\.ai)')

pf = pq.ParquetFile(pq_path)
table = pf.read_row_group(rg_idx)
print(f"{slug} rg{rg_idx}: rows={table.num_rows}", flush=True)

found = {name: {} for name in ['sharp', 'solved', 'oai', 'zz', 'deaddrop', 'amap']}
n_chunks = 0

def feed(text):
    for name, rx in [('sharp', SHARP), ('solved', SOLVED), ('oai', OAI), ('zz', ZZ), ('deaddrop', DD), ('amap', AMAP)]:
        for m in rx.finditer(text):
            key = m.group(0)[:60]
            if key not in found[name]:
                s = max(0, m.start()-180)
                ctx = text[s:m.end()+180].replace('\n', ' ')[:400]
                if name == 'oai' and OAI_PMH.search(ctx):
                    continue
                found[name][key] = ctx
            if len(found[name]) >= 15:
                break

for col in table.columns:
    for chunk in col.chunks:
        # process each scalar separately to bound memory
        for v in chunk:
            py = v.as_py() if hasattr(v, 'as_py') else v
            if py is None:
                continue
            if isinstance(py, str):
                feed(py)
            elif isinstance(py, bytes):
                feed(py.decode('utf-8', 'replace'))
            elif isinstance(py, (list, tuple)):
                for x in py:
                    if isinstance(x, str):
                        feed(x)
                    elif isinstance(x, dict):
                        for vv in x.values():
                            if isinstance(vv, str):
                                feed(vv)
            elif isinstance(py, dict):
                for vv in py.values():
                    if isinstance(vv, str):
                        feed(vv)
        n_chunks += 1
        if n_chunks % 20 == 0:
            print(f"  {n_chunks} chunks", flush=True)

out = {'slug': slug, 'rg': rg_idx, 'rows': table.num_rows}
for name, d in found.items():
    out[name] = [{'match': k, 'ctx': v} for k, v in d.items()]
    print(f"  {name}: {len(d)} distinct", flush=True)
json.dump(out, open(out_path, 'w'), indent=1)
print("WROTE " + out_path, flush=True)
