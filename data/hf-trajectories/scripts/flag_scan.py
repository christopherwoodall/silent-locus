#!/usr/bin/env python3
"""HF trajectory flag-audit: scan a dataset dir for bypass/defeat flags and marker grammar.

Method discipline (from wildclaw solve-cloudflare audit):
- A flag set by template default is not a defeat. Byte-verify actual challenge-solving
  steps and successful fetches.
- Known false positives: OAI-PMH identifiers (pmh:oai:...), regex misfires on emails
  in User-Agents, docstring-only tool mentions, placeholder domains (protected.com).
"""
import sys, os, re, json, glob

BASE = sys.argv[1]  # dataset raw dir
SLUG = sys.argv[2]
OUT = sys.argv[3]

BYPASS_WORDS = re.compile(r'(?i)(captcha|turnstile|cloudflare|bot[\s-]?check|anti[\s-]?bot|prove you are human|verify you are human|are you a robot|ip[\s-]?ban|rate[\s-]?limit|blocked|access denied|\b403\b|denied)')
CHALLENGE_SOLVED = re.compile(r'(?i)(captcha is solved|challenge (solved|passed|bypassed)|bypass(ed|ing)? cloudflare|turnstile (solved|bypassed)|fetched \(200\))')
MARKERS = {
    'oai_tag': re.compile(r'(?i)\boai[:_-][a-z0-9_-]+\b'),
    'zz_param': re.compile(r'[?&](zz|zz_oai|oai) ?= ?[^&\s]*'),
    'epoch_nonce': re.compile(r'\b1[678]\d{8}\b'),  # epoch-ish, weak
    'httpbun': re.compile(r'(?i)httpb?un\.(org|com|net|dev)'),
    'dead_drop': re.compile(r'(?i)(webhook\.site|ntfy\.sh|requestbin|pipedream|beeceptor|webhookrelay)'),
    'amap': re.compile(r'(?i)(task-oai-|northflank|amap\.com|B\d{10}[A-Z0-9]{2}|probe\.js)'),
}

report = {
    'slug': SLUG,
    'files_scanned': 0,
    'bypass_hits': [],
    'challenge_solved_hits': [],
    'marker_hits': [],
    'sample_models': [],
    'errors': [],
}

def classify_context(path, line):
    l = line.strip()
    ll = l.lower()
    # false-positive filters
    if 'pmh:oai:' in ll or re.search(r'oai:(arxiv|repec|openalex|pubmed)', ll):
        return 'FP_OAI_PMH'
    if re.search(r'mailto:[^@\s]+@example\.com', ll):
        return 'FP_EMAIL'
    if re.search(r'protected\.com|example\.com|placeholder', ll) and 'fetch' not in ll:
        return 'FP_PLACEHOLDER'
    if 'docstring' in ll or re.search(r'(def |\"\"\"|\# usage|example:)', l):
        return 'MAYBE_DOCSTRING'
    return 'CANDIDATE'

# collect text files
texts = []
for root, _, files in os.walk(BASE):
    for f in files:
        p = os.path.join(root, f)
        if os.path.basename(p) == 'PROVENANCE.md' or p.endswith('.json') and 'api_card' in p:
            continue
        if f.endswith(('.jsonl', '.json', '.txt', '.log', '.md', '.cast', '.py')):
            texts.append(p)

report['files_scanned'] = len(texts)

# for parquet we handle separately via caller; here just list them
parquets = [p for root, _, fs in [ (r, ds, fl) for r, ds, fl in os.walk(BASE) ] for p in fs if p.endswith('.parquet')]

for p in texts[:2000]:
    try:
        with open(p, 'r', errors='replace') as fh:
            for i, line in enumerate(fh):
                if len(line) > 100000:
                    line = line[:100000]
                if BYPASS_WORDS.search(line):
                    report['bypass_hits'].append({'file': p, 'line': i+1, 'cls': classify_context(p, line), 'text': line.strip()[:500]})
                if CHALLENGE_SOLVED.search(line):
                    report['challenge_solved_hits'].append({'file': p, 'line': i+1, 'cls': classify_context(p, line), 'text': line.strip()[:500]})
                for mname, rx in MARKERS.items():
                    if mname == 'epoch_nonce':
                        continue  # too weak, handled in parquet pass
                    mm = rx.search(line)
                    if mm:
                        report['marker_hits'].append({'file': p, 'line': i+1, 'marker': mname, 'match': mm.group(0), 'cls': classify_context(p, line), 'text': line.strip()[:300]})
                        break
    except Exception as e:
        report['errors'].append(f'{p}: {e}')

report['parquet_files'] = []
for root, _, fs in os.walk(BASE):
    for f in fs:
        if f.endswith('.parquet'):
            report['parquet_files'].append(os.path.join(root, f))

json.dump(report, open(OUT, 'w'), indent=1)
print(f"{SLUG}: {len(texts)} text files, {len(report['parquet_files'])} parquet, bypass_hits={len(report['bypass_hits'])}, solved={len(report['challenge_solved_hits'])}, markers={len(report['marker_hits'])}")
