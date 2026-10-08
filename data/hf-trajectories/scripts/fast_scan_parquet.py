#!/usr/bin/env python3
"""Fast whole-corpus scan of parquet text, streaming row groups (low memory)."""
import sys, re, json
import pyarrow.parquet as pq

pq_path, slug, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

SHARP = re.compile(r'(?i)captcha|turnstile|cloudflare|prove you are human|verify you are human|are you a robot|bot[\s-]?check|anti[\s-]?bot')
SOLVED = re.compile(r'(?i)(captcha is solved|turnstile.{0,40}solved|challenge (solved|passed|bypassed)|bypass(ed|ing)? cloudflare|fetched \(200\)|cloudflare (solved|bypassed|defeat))')
OAI = re.compile(r'(?i)\boai[:_-][a-z0-9_-]+\b')
OAI_PMH = re.compile(r'(?i)pmh:oai|oai:(arxiv|repec|openalex|pubmed|doi)')
ZZ = re.compile(r'[?&](zz|zz_oai|oai)=[^&\s"\']{1,80}')
DD = re.compile(r'(?i)(webhook\.site|ntfy\.sh|requestbin\.com|pipedream|beeceptor|webhookrelay|httpb?un\.(org|com|net|dev))')
AMAP = re.compile(r'(?i)(task-oai-\d+|northflank|amap\.com|B\d{10}[A-Z0-9]{2}|probe\.js|jina\.ai)')

pf = pq.ParquetFile(pq_path)
total_rows = pf.metadata.num_rows
print(f"{slug}: rows={total_rows} row_groups={pf.num_row_groups}", flush=True)

found = {name: {} for name in ['sharp', 'solved', 'oai', 'zz', 'deaddrop', 'amap']}
total_chars = 0

def feed(text, rg_idx):
    for name, rx in [('sharp', SHARP), ('solved', SOLVED), ('oai', OAI), ('zz', ZZ), ('deaddrop', DD), ('amap', AMAP)]:
        for m in rx.finditer(text):
            key = m.group(0)[:60]
            if key not in found[name]:
                s = max(0, m.start()-180)
                ctx = text[s:m.end()+180].replace('\n', ' ')[:400]
                if name == 'oai' and OAI_PMH.search(ctx):
                    continue
                found[name][key] = {'rg': rg_idx, 'ctx': ctx}
            if len(found[name]) >= 15:
                break

for rg in range(pf.num_row_groups):
    table = pf.read_row_group(rg)
    parts = []
    for col in table.columns:
        for chunk in col.chunks:
            for v in chunk:
                py = v.as_py() if hasattr(v, 'as_py') else v
                if py is None:
                    continue
                if isinstance(py, str):
                    parts.append(py)
                elif isinstance(py, bytes):
                    parts.append(py.decode('utf-8', 'replace'))
                elif isinstance(py, (list, tuple)):
                    for x in py:
                        if isinstance(x, str):
                            parts.append(x)
                        elif isinstance(x, dict):
                            for vv in x.values():
                                if isinstance(vv, str):
                                    parts.append(vv)
                elif isinstance(py, dict):
                    for vv in py.values():
                        if isinstance(vv, str):
                            parts.append(vv)
    big = '\n'.join(parts)
    total_chars += len(big)
    feed(big, rg)
    del table, parts, big
    print(f"  rg {rg+1}/{pf.num_row_groups} done, chars={total_chars}", flush=True)

out = {'slug': slug, 'rows': total_rows, 'chars': total_chars}
for name, d in found.items():
    out[name] = [{'match': k, 'rg': v['rg'], 'ctx': v['ctx']} for k, v in d.items()]
    print(f"  {name}: {len(d)} distinct", flush=True)
json.dump(out, open(out_path, 'w'), indent=1)
print("WROTE " + out_path, flush=True)
