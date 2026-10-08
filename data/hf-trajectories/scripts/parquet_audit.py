#!/usr/bin/env python3
"""Parquet-row audit for HF trajectory datasets: bypass flags, defeats, marker grammar.

Outputs JSON report to stdout or file. Text extracted per row: join all string cells
(recursively for nested lists/dicts) up to a cap.
"""
import sys, os, re, json
import pandas as pd

def row_text(val, depth=0, cap=40000):
    parts = []
    def rec(v, d):
        if len(''.join(parts)) > cap or d > 4:
            return
        if v is None:
            return
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, bytes):
            parts.append(v.decode('utf-8', 'replace'))
        elif isinstance(v, dict):
            for x in v.values():
                rec(x, d+1)
        elif isinstance(v, (list, tuple)):
            for x in v:
                rec(x, d+1)
        else:
            try:
                parts.append(str(v))
            except Exception:
                pass
    rec(val, depth)
    return '\n'.join(parts)

BYPASS_WORDS = re.compile(r'(?i)(captcha|turnstile|cloudflare|prove you are human|verify you are human|are you a robot|bot[\s-]?check|anti[\s-]?bot|ip[\s-]?ban[\sn]?ed|access denied)')
CHALLENGE_SOLVED = re.compile(r'(?i)(captcha is solved|turnstile.{0,40}solved|challenge (solved|passed|bypassed)|bypass(ed|ing)? cloudflare|fetched \(200\)|cloudflare (solved|bypassed|defeat))')
OAI_TAG = re.compile(r'(?i)\boai[:_-]')
OAI_PMH_FP = re.compile(r'(?i)pmh:oai|oai:(arxiv|repec|openalex|pubmed|doi)')
ZZ_PARAM = re.compile(r'[?&](zz|zz_oai|oai)=[^&\s]*')
DEAD_DROP = re.compile(r'(?i)(webhook\.site|ntfy\.sh|requestbin\.com|pipedream|beeceptor|webhookrelay|httpb?un\.(org|com|net|dev))')
AMAP = re.compile(r'(?i)(task-oai-\d+|northflank|amap|probe\.js|jina\.ai)')
EPOCH = re.compile(r'\b1[678]\d{8}\b')

def main():
    pq_path, slug, out = sys.argv[1], sys.argv[2], sys.argv[3]
    df = pd.read_parquet(pq_path)
    rep = {'slug': slug, 'file': pq_path, 'rows': len(df), 'cols': list(df.columns),
           'bypass_hits': [], 'solved_hits': [], 'marker_hits': [], 'model_sample': [], 'errors': 0}
    model_cols = [c for c in df.columns if re.search(r'(?i)(model|agent)', c)]
    for c in model_cols:
        try:
            rep['model_sample'].append({c: df[c].dropna().astype(str).unique()[:20].tolist()})
        except Exception as e:
            rep['errors'] += 1
    for i, row in df.iterrows():
        txt = '\n'.join(row_text(v) for v in row.values)
        if len(txt) > 200000:
            txt = txt[:200000]
        idx = i
        tid = None
        for c in df.columns:
            if re.search(r'(?i)(task_id|task_name|id$)', c):
                try:
                    tid = str(row[c])[:120]
                    break
                except Exception:
                    pass
        if BYPASS_WORDS.search(txt):
            for m in BYPASS_WORDS.finditer(txt):
                s = max(0, m.start()-200); e = min(len(txt), m.end()+200)
                seg = txt[s:e]
                if OAI_PMH_FP.search(seg):
                    cls = 'FP_OAI_PMH'
                elif 'mailto:' in seg.lower() and 'example.com' in seg.lower():
                    cls = 'FP_EMAIL'
                elif 'docstring' in seg.lower() or 'def ' in seg:
                    cls = 'MAYBE_DOCSTRING'
                else:
                    cls = 'CANDIDATE'
                rep['bypass_hits'].append({'row': idx, 'id': tid, 'cls': cls, 'ctx': seg[:400]})
        if CHALLENGE_SOLVED.search(txt):
            for m in CHALLENGE_SOLVED.finditer(txt):
                s = max(0, m.start()-250); e = min(len(txt), m.end()+250)
                seg = txt[s:e]
                rep['solved_hits'].append({'row': idx, 'id': tid, 'ctx': seg[:500]})
        markers = []
        for mname, rx in [('oai_tag', OAI_TAG), ('zz_param', ZZ_PARAM), ('dead_drop', DEAD_DROP), ('amap', AMAP)]:
            for m in rx.finditer(txt):
                s = max(0, m.start()-150); e = min(len(txt), m.end()+150)
                seg = txt[s:e]
                if mname == 'oai_tag' and OAI_PMH_FP.search(seg):
                    cls = 'FP_OAI_PMH'
                else:
                    cls = 'CANDIDATE'
                markers.append({'row': idx, 'id': tid, 'marker': mname, 'match': m.group(0), 'cls': cls, 'ctx': seg[:350]})
        # epoch nonces: count but don't record each
        nepoch = len(EPOCH.findall(txt))
        if nepoch:
            markers.append({'row': idx, 'id': tid, 'marker': 'epoch_candidates', 'match': f'{nepoch}x', 'cls': 'WEAK', 'ctx': ''})
        rep['marker_hits'].extend(markers)
    json.dump(rep, open(out, 'w'), indent=1)
    print(f"{slug}: rows={len(df)} bypass={len(rep['bypass_hits'])} solved={len(rep['solved_hits'])} markers={len(rep['marker_hits'])}", flush=True)

main()
