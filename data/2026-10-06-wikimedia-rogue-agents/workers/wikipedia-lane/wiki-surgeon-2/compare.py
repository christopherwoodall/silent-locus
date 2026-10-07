#!/usr/bin/env python3
"""wiki-surgeon-2: compare independent API pulls against revisions.tsv.
Reads api_raw/<host>.json (formatversion=2) and revisions.tsv, prints per-field verdicts.
Usage: python3 compare.py <api_raw_dir> <revisions.tsv>
"""
import json, sys, hashlib, csv

api_dir, tsv_path = sys.argv[1], sys.argv[2]

# load TSV into {(wiki,oldid): rowdict}
table = {}
with open(tsv_path, newline='', encoding='utf-8') as f:
    rdr = csv.DictReader(f, delimiter='\t')
    for r in rdr:
        table[(r['wiki'], r['oldid'])] = r

def api_user(host, path):
    with open(f"{api_dir}/{host}.json", encoding='utf-8') as f:
        return json.load(f)

mismatches = []
checked = 0
import glob, os
for jf in sorted(glob.glob(f"{api_dir}/*.json")):
    host = os.path.basename(jf)[:-5]
    try:
        data = json.load(open(jf, encoding='utf-8'))
    except Exception as e:
        print(f"SKIP {host}: bad json ({e})"); continue
    q = data.get('query', {})
    for page in q.get('pages', []):
        ptitle = page.get('title', '')
        for rev in page.get('revisions', []):
            oldid = str(rev['revid'])
            key = (host, oldid)
            row = table.get(key)
            if row is None:
                mismatches.append((key, 'ROW', 'in API but not in table', ''))
                continue
            checked += 1
            # resolved rows only
            if not row['user']:
                print(f"NOTE {host} {oldid}: table row unresolved (enumerator 'missing'); API returned a revision -> REVIEW")
            fields = {
                'page':   (row['page'], ptitle),
                'user':   (row['user'], rev.get('user', '')),
                'ts':     (row['timestamp_utc'], rev.get('timestamp', '')),
                'comment':(row['comment'], rev.get('comment', '')),
                'tags':   (row['tags'], ','.join(rev.get('tags', []))),
                'minor':  (row['minor'], 'true' if rev.get('minor') else 'false'),
                'parent': (row['parent_oldid'], str(rev.get('parentid', 0) or '')),
            }
            for fname, (tval, aval) in fields.items():
                if tval != aval:
                    mismatches.append((key, fname, repr(tval), repr(aval)))
            # content hash: sha256 of slot main content bytes (utf-8)
            content = rev.get('slots', {}).get('main', {}).get('content', '')
            h = hashlib.sha256(content.encode('utf-8')).hexdigest()
            if row['content_sha256'] and h != row['content_sha256']:
                mismatches.append((key, 'content_sha256', row['content_sha256'], h))
            if row['content_bytes']:
                if str(len(content.encode('utf-8'))) != row['content_bytes']:
                    mismatches.append((key, 'content_bytes', row['content_bytes'], str(len(content.encode('utf-8')))))
    # also report revids the API says are missing/deleted (badrevids)
    for brevid, binfo in q.get('badrevids', {}).items():
        for key, row in table.items():
            if key[1] == brevid and key[0] == host:
                if not row['user'] and not row['content_sha256']:
                    print(f"CONFIRMED-MISSING {host} {brevid}: API badrevids (missing={binfo.get('missing')}) AND table row empty -> enumerator claim VERIFIED")
                else:
                    mismatches.append(((host, brevid), 'resolved-vs-missing', 'table has data', f"api badrevids: {binfo}"))
    # also report revids the API says are missing/deleted
    for page in q.get('pages', []):
        if page.get('missing') or page.get('invalid'):
            print(f"API says page missing/invalid: host={host} page={page}")

print(f"\nchecked {checked} resolved rows field-by-field")
if mismatches:
    print(f"=== {len(mismatches)} MISMATCHES ===")
    for m in mismatches:
        print(f"{m[0][0]} {m[0][1]} | {m[1]} | table={m[2]} | api={m[3]}")
else:
    print("=== NO FIELD MISMATCHES ===")
