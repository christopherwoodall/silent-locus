#!/usr/bin/env python3
"""URL inventory miner for the Codebreaker expansion.

Streams the two events.jsonl corpora plus the fleet corpus raw/ JSON pages
(full submitted URLs live there; events.jsonl notes are truncated ~205 chars),
extracts every carrier/infrastructure URL by class regex, dedupes with
occurrence counts, folds truncated variants into their full URLs, and writes:
  url-inventory.md    - greppable, one URL per line + context, class counts
  url-inventory.jsonl - machine-readable records with provenance
"""
import json, re, hashlib, glob, os, sys
from collections import defaultdict
from urllib.parse import unquote, unquote_plus

FLEET = os.path.expanduser('~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet')
SWEEP = os.path.expanduser('~/workspace/silent-locus/data/2026-10-01-oai-tag-sweep')
OUTD = os.path.join(FLEET, 'personas/codebreaker/raw')

# FLEET_ONLY=1: Chinese-swarm-only run (fleet events + fleet raw JSON, no tag-sweep).
# Standing rule (BigSexyWarlock69, 2026-10-05): NEVER redact from evidence.
FLEET_ONLY = os.environ.get('FLEET_ONLY') == '1'
if FLEET_ONLY:
    SWEEP = '/tmp/empty-sweep'  # holds an empty events.jsonl; sweep contributes zero records
OUT_SUFFIX = '-chinese-swarm' if FLEET_ONLY else ''

CLASSES = [
    ('livecodes-carrier',  r'(?:https?://)?livecodes\.io/[^\s"\'<>\]]*'),
    ('httpbun-carrier',    r'(?:https?://)?httpbun\.com/(?:base64|mix)(?:/|\?)[^\s"\'<>\]]*'),
    ('httpbin-carrier',    r'(?:https?://)?httpbin\.org/base64/[^\s"\'<>\]]*'),
    ('webhook-deaddrop',   r'(?:https?://)?webhook\.site/[^\s"\'<>\]]*'),
    ('hrefli-wrapper',     r'(?:https?://)?href\.li/\?[^\s"\'<>\]]*'),
    ('lhr-tunnel',         r'(?:https?://)?[A-Za-z0-9.-]*\.lhr\.life[^\s"\'<>\]]*'),
    ('shortener',          r'(?:https?://)?(?:is\.gd|v\.gd|da\.gd|tinyurl\.com|bit\.ly|t\.co|goo\.gl|ow\.ly|rb\.gy|cutt\.ly|shorturl\.at|lnkd\.in|buff\.ly)/[^\s"\'<>\]]*'),
    ('jina-proxy',         r'(?:https?://)?r\.jina\.ai/[^\s"\'<>\]]*'),
    ('staging-host',       r'(?:https?://)?[A-Za-z0-9.-]*\.(?:pages\.dev|vercel\.app|onrender\.com|workers\.dev)[^\s"\'<>\]]*'),
    ('hospital-backend-target', r'GZHOSP[A-Za-z0-9/_.-]*'),
    ('aihw-tableau',       r'(?:https?://)?vizprod\.aihw\.gov\.au[^\s"\'<>\]]*'),
]
RX = [(c, re.compile(p)) for c, p in CLASSES]
TRAILING = ').,;:\'"!?]`\\'
URL_CLASSES = {c for c, _ in CLASSES} - {'hospital-backend-target'}

def clean(u):
    u = u.strip().rstrip(TRAILING)
    # strip a trailing dangling escape or quote fragment
    return u

def dedupe_key(u):
    v = clean(u)
    if not re.match(r'(?i)https?://', v):
        v = 'https://' + v
    return v

def fully_unquote(s):
    prev = None
    cur = s
    for _ in range(3):
        prev, cur = cur, unquote(cur)
        if cur == prev:
            break
    return cur

def b64_body_info(seg):
    h = hashlib.sha256(seg.encode()).hexdigest()[:12]
    info = {'sha256_12': h, 'chars': len(seg)}
    try:
        import base64
        s = seg
        s += '=' * (-len(s) % 4)
        dec = base64.b64decode(s, validate=False).decode('utf-8', 'replace')
        m = re.search(r'<title>([^<]{1,100})</title>', dec)
        if m:
            info['title'] = m.group(1)
    except Exception:
        pass
    return info

def build_note(cls, url, rec_text):
    """One-liner: title marker / body hash / uq tags."""
    bits = []
    du = unquote_plus(fully_unquote(url))
    m = re.search(r'<title>([^<]{1,80})</title>', du)
    if m:
        bits.append('title=' + m.group(1))
    for pat, name in [(r'uqscan=([A-Za-z0-9_.\-]{2,60})', 'uqscan'),
                      (r'uqtag=([A-Za-z0-9_.\-]{2,60})', 'uqtag'),
                      (r'data-marker=\\"?(gucheng-[A-Za-z0-9_.\-]{2,60})', 'marker'),
                      (r'data-marker=\\"?(ltzh-[A-Za-z0-9_.\-]{2,60})', 'marker')]:
        mm = re.search(pat, du)
        if mm:
            bits.append(name + '=' + mm.group(1))
    if cls in ('httpbun-carrier', 'httpbin-carrier'):
        mm = re.search(r'/base64/([^?#\s]+)', url)
        if mm:
            bi = b64_body_info(mm.group(1))
            bits.append('body_sha256=' + bi['sha256_12'] + ' len=' + str(bi['chars']))
            if 'title' in bi and not any(b.startswith('title=') for b in bits):
                bits.append('title=' + bi['title'])
        else:
            bits.append('mix-path sha256=' + hashlib.sha256(url.encode()).hexdigest()[:12])
    if cls == 'hrefli-wrapper':
        mm = re.search(r'href\.li/\?(https?://[^?\s]+|[^?\s]+)', url)
        if mm:
            bits.append('wraps=' + mm.group(1)[:80])
    if cls == 'jina-proxy':
        mm = re.search(r'r\.jina\.ai/(https?://[^\s]+|http://[^\s]+)', url)
        if mm:
            bits.append('launders=' + mm.group(1)[:100])
    if cls == 'webhook-deaddrop':
        bits.append('dead-drop inbox')
    if cls == 'hospital-backend-target':
        bits.append('hospital target marker')
    # record-level markers
    for pat, name in [(r'uqscan=([A-Za-z0-9_.\-]{2,60})', 'uqscan'),
                      (r'uqtag=([A-Za-z0-9_.\-]{2,60})', 'uqtag')]:
        if not any(b.startswith(name + '=') for b in bits):
            mm = re.search(pat, rec_text)
            if mm:
                bits.append(name + '=' + mm.group(1))
    return '; '.join(bits) if bits else '-'

# url -> {class, urls_seen:set, truncated:bool, encoding, records:[...]}
store = {}

def add(url, cls, prov, truncated, encoding, rec_text):
    url = clean(url)
    if not url or len(url) < 8:
        return
    key = (cls, dedupe_key(url))
    e = store.get(key)
    if e is None:
        e = store[key] = {'class': cls, 'url': url, 'truncated': truncated,
                          'encoding': encoding, 'records': [], 'seen_refs': set()}
    else:
        # prefer non-truncated verbatim form
        if e['truncated'] and not truncated:
            e['url'] = url
            e['truncated'] = False
    ref = prov.get('canon') or prov.get('ref')
    if ref not in e['seen_refs']:
        e['seen_refs'].add(ref)
        e['records'].append(prov)
    else:
        e['truncated'] = e['truncated'] and truncated

def scan_text(text, prov, field, trunc_if_at_end):
    """Run all class regexes over raw and fully-unquoted text."""
    if not isinstance(text, str):
        try:
            text = json.dumps(text)
        except Exception:
            return
    seen_here = set()
    for variant, encoding in ((text, 'raw'), (fully_unquote(text), 'percent-decoded')):
        for cls, rx in RX:
            for m in rx.finditer(variant):
                u = clean(m.group(0))
                if (cls, dedupe_key(u), field) in seen_here:
                    continue
                seen_here.add((cls, dedupe_key(u), field))
                trunc = trunc_if_at_end and m.end() >= len(variant) - 6
                add(u, cls, dict(prov, field=field), trunc, encoding, text)

# ---------- 1. fleet events.jsonl ----------
n_fleet = 0
with open(os.path.join(FLEET, 'events.jsonl')) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        n_fleet += 1
        try:
            rec = json.loads(line)
        except Exception:
            continue
        lab = rec.get('labels') or {}
        rid = lab.get('report_id') or rec.get('fingerprint', '?')
        prov = {'dataset': '2026-09-28-chinese-amap-fleet/events.jsonl',
                'ref': 'fleet:' + str(rid), 'canon': 'fleet:' + str(rid),
                'report_url': rec.get('source_url', ''),
                'ts': rec.get('@timestamp', ''),
                'file_origin': lab.get('file_origin', '')}
        note = rec.get('note') or ''
        ms = rec.get('matched_string') or ''
        if note:
            scan_text(note, prov, 'note', trunc_if_at_end=len(note) >= 205)
        if ms:
            scan_text(ms, prov, 'matched_string', trunc_if_at_end=False)

# ---------- 2. fleet raw/ JSON pages (full submitted URLs) ----------
raw_files = glob.glob(os.path.join(FLEET, 'raw', '**', '*.json'), recursive=True)
n_raw = 0
for fp in raw_files:
    try:
        with open(fp) as fh:
            data = json.load(fh)
    except Exception:
        continue
    n_raw += 1
    rel = os.path.relpath(fp, FLEET)
    reports = data.get('reports') if isinstance(data, dict) else None
    single_rid = data.get('report_id') if isinstance(data, dict) and 'reports' not in data else None
    if isinstance(reports, list):
        for r in reports:
            rid = r.get('report_id', '?')
            prov = {'dataset': '2026-09-28-chinese-amap-fleet/' + rel,
                    'ref': 'fleetraw:' + str(rid), 'canon': 'fleet:' + str(rid),
                    'report_url': 'https://urlquery.net/report/' + str(rid),
                    'ts': r.get('date', ''),
                    'file_origin': rel}
            for path in (('submit', 'url'), ('url',)):
                node = r
                try:
                    for p in path:
                        node = node[p]
                except (KeyError, TypeError):
                    node = None
                if isinstance(node, dict) and node.get('addr'):
                    full = node.get('schema', 'https') + '://' + node['addr']
                    add(full, None, dict(prov, field='raw:' + '.'.join(path)),
                        False, 'raw', '')
    elif single_rid:
        prov = {'dataset': '2026-09-28-chinese-amap-fleet/' + rel,
                'ref': 'fleetraw1:' + str(single_rid), 'canon': 'fleet:' + str(single_rid),
                'report_url': 'https://urlquery.net/report/' + str(single_rid),
                'ts': data.get('date', ''),
                'file_origin': rel}
        for path in (('submit', 'url'), ('url',)):
            node = data
            try:
                for p in path:
                    node = node[p]
            except (KeyError, TypeError):
                node = None
            if isinstance(node, dict) and node.get('addr'):
                full = node.get('schema', 'https') + '://' + node['addr']
                add(full, None, dict(prov, field='raw:' + '.'.join(path)),
                    False, 'raw', '')
    # generic sweep over serialized JSON for anything else (summary fields etc.)
    s = json.dumps(data)
    gcanon = 'fleet:' + str(single_rid) if single_rid else 'fleetfile:' + rel
    prov = {'dataset': '2026-09-28-chinese-amap-fleet/' + rel,
            'ref': 'fleetrawfile:' + rel, 'canon': gcanon,
            'report_url': '', 'ts': '',
            'file_origin': rel}
    scan_text(s, prov, 'raw-json-text', trunc_if_at_end=False)

# fix class for raw submit/url adds (class=None passed above) by re-scan
for key in list(store.keys()):
    cls, dk = key
    if cls is None:
        e = store.pop(key)
        url = e['url']
        matched = False
        for c2, rx in RX:
            if rx.match(url):
                e['class'] = c2
                store[(c2, dk)] = e
                matched = True
                break
        if not matched:
            pass  # drop non-carrier raw urls

# ---------- 3. sweep events.jsonl ----------
n_sweep = 0
with open(os.path.join(SWEEP, 'events.jsonl')) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        n_sweep += 1
        try:
            rec = json.loads(line)
        except Exception:
            continue
        rid = rec.get('record_id', '?')
        prov = {'dataset': '2026-10-01-oai-tag-sweep/events.jsonl',
                'ref': 'sweep:' + str(rid), 'canon': 'sweep:' + str(rid),
                'report_url': rec.get('report_url') or '',
                'ts': rec.get('event_time', ''),
                'file_origin': rec.get('source', '')}
        uo = rec.get('url_original') or ''
        if uo:
            scan_text(uo, prov, 'url_original', trunc_if_at_end=False)
        ln = rec.get('labels_note') or ''
        if ln:
            scan_text(ln, prov, 'labels_note', trunc_if_at_end=False)
        wi = rec.get('why_included') or ''
        if wi:
            scan_text(wi, prov, 'why_included', trunc_if_at_end=False)
        ev = rec.get('evidence') or {}
        if isinstance(ev, dict):
            for k, v in ev.items():
                if isinstance(v, str) and v:
                    scan_text(v, prov, 'evidence:' + k, trunc_if_at_end=True)

# ---------- 4. fold truncated / decoded-fragment prefixes into full URLs ----------
# Fragments are attached to the full URL from the SAME record (canon ref),
# so per-record variants collapse onto their own full carrier URL.
items = list(store.values())
full_by_canon = defaultdict(list)
for f_ in items:
    if not f_['truncated'] and f_['class'] in URL_CLASSES:
        for r in f_['records']:
            full_by_canon[(f_['class'], r.get('canon') or r['ref'])].append(f_)
folded = 0
def _bare(u):
    v = re.sub(r'(?i)^https?://', '', fully_unquote(u))
    v = re.sub(r'%[0-9A-Fa-f]?$', '', v)  # note cut mid-percent-escape
    return v
for e in items:
    if e['class'] not in URL_CLASSES:
        continue
    if not (e['truncated'] or e['encoding'] == 'percent-decoded'):
        continue
    eu = _bare(e['url'])
    for r in list(e['records']):
        key = (e['class'], r.get('canon') or r['ref'])
        cands = []
        for f_ in full_by_canon.get(key, []):
            if f_ is e:
                continue
            fu = _bare(f_['url'])
            if len(fu) > len(eu) and fu.startswith(eu):
                cands.append(f_)
        if cands:
            f_ = cands[0]
            canon = r.get('canon') or r['ref']
            if canon not in f_['seen_refs']:
                f_['seen_refs'].add(canon)
                f_['records'].append(r)
            e['records'].remove(r)
            folded += 1
    if not e['records']:
        e['merged_into'] = True

# drop whole-file-scan artifacts: entries whose only records come from the
# generic raw-json-text sweep and whose URL is a strict prefix of a genuine
# full URL in the same class (percent-decoded '<'-terminated match junk).
full_bare = defaultdict(list)
for f_ in items:
    if not f_.get('merged_into') and not f_['truncated'] and f_['class'] in URL_CLASSES:
        full_bare[f_['class']].append(_bare(f_['url']))
for e in items:
    if e.get('merged_into') or e['class'] not in URL_CLASSES:
        continue
    if any(r['field'] != 'raw-json-text' for r in e['records']):
        continue
    eb = _bare(e['url'])
    if any(len(fb) > len(eb) and fb.startswith(eb) for fb in full_bare[e['class']]):
        e['merged_into'] = True
        folded += 1

final = [e for e in items if not e.get('merged_into')]
# dedupe note text
for e in final:
    rt = ' '.join(r.get('report_url', '') for r in e['records'][:3])
    e['note'] = build_note(e['class'], e['url'], rt)

# ---------- 5. write outputs ----------
os.makedirs(OUTD, exist_ok=True)
counts = defaultdict(int)
occs = defaultdict(int)
for e in final:
    counts[e['class']] += 1
    occs[e['class']] += len(e['records'])

order = [c for c, _ in CLASSES]
with open(os.path.join(OUTD, 'url-inventory' + OUT_SUFFIX + '.md'), 'w') as md:
    md.write('# URL Inventory — Codebreaker expansion%s\n\n' % (' (Chinese swarm only)' if FLEET_ONLY else ''))
    if FLEET_ONLY:
        md.write('Mined from: `2026-09-28-chinese-amap-fleet/events.jsonl` (%d recs), '
                 'fleet `raw/**/*.json` (%d files). Chinese swarm ONLY — no tag-sweep (UNCTAD) records. '
                 'Standing rule: evidence is never redacted.\n\n' % (n_fleet, n_raw))
    else:
        md.write('Mined from: `2026-09-28-chinese-amap-fleet/events.jsonl` (%d recs), '
                 '`2026-10-01-oai-tag-sweep/events.jsonl` (%d recs), fleet `raw/**/*.json` (%d files).\n\n'
                 % (n_fleet, n_sweep, n_raw))
    md.write('One URL per line: `URL | class | ref | occ=N | note`. '
             '`occ` = contributing records. `TRUNC` = snippet/note-truncated, treat as fragment.\n\n')
    md.write('## Counts per class (unique URLs / contributing records)\n\n')
    for c in order:
        md.write('- %s: %d unique / %d records\n' % (c, counts.get(c, 0), occs.get(c, 0)))
    md.write('\n')
    for c in order:
        es = sorted([e for e in final if e['class'] == c],
                    key=lambda e: (-len(e['records']), e['url']))
        if not es:
            continue
        md.write('## %s (%d)\n\n' % (c, len(es)))
        for e in es:
            ref0 = e['records'][0]['ref'] if e['records'] else '?'
            tag = 'TRUNC ' if e['truncated'] else ''
            md.write('%s%s | class=%s | ref=%s | occ=%d | %s\n'
                     % (tag, e['url'], e['class'], ref0, len(e['records']), e['note']))
        md.write('\n')

with open(os.path.join(OUTD, 'url-inventory' + OUT_SUFFIX + '.jsonl'), 'w') as jf:
    for c in order:
        for e in sorted([e for e in final if e['class'] == c], key=lambda e: e['url']):
            jf.write(json.dumps({
                'url': e['url'], 'class': e['class'],
                'occurrences': len(e['records']),
                'truncated': e['truncated'], 'encoding': e['encoding'],
                'note': e['note'], 'records': e['records']}) + '\n')

print('fleet_lines=%d sweep_lines=%d raw_files=%d' % (n_fleet, n_sweep, n_raw))
print('unique_urls=%d folded_truncated=%d' % (len(final), folded))
for c in order:
    print('%-24s %5d unique / %6d records' % (c, counts.get(c, 0), occs.get(c, 0)))
