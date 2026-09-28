#!/usr/bin/env python3
"""Fetch one WARC record's bytes via HTTP Range request and grep mechanism patterns.
Usage: python3 fetch_warc.py '<filename>' <offset> <length>
Looks for: go-import, r.jina.ai, s.jina.ai, /api/v1/web_hooks, A000/ZZEND,
builder alive, YARD RAN, moderngov, county.json"""
import sys, gzip, io, re, urllib.request

PATTERNS = [r'go-import', r'r\.jina\.ai', r's\.jina\.ai', r'/api/v1/web_hooks',
            r'A000', r'ZZEND', r'builder alive', r'YARD RAN', r'moderngov',
            r'county\.json', r'<meta name="description"[^>]*content="([^"]{0,300})',
            r'<title[^>]*>(.*?)</title>']

filename, offset, length = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
req = urllib.request.Request('https://data.commoncrawl.org/' + filename, headers={
    'User-Agent': 'research-bot/1.0',
    'Range': f'bytes={offset}-{offset + length - 1}'})
with urllib.request.urlopen(req, timeout=120) as r:
    data = r.read()
print(f'fetched {len(data)} bytes', file=sys.stderr)
try:
    raw = gzip.decompress(data)
except Exception:
    raw = gzip.GzipFile(fileobj=io.BytesIO(data)).read()
text = raw.decode('utf-8', 'replace')
m = re.search(r'<html', text, re.I)
body = text[m.start():] if m else text
print(f'html chars: {len(body)}', file=sys.stderr)
for pat in PATTERNS:
    hits = re.findall(pat, body, re.I | re.S)
    if hits:
        print(f'### {pat}: {len(hits)} hit(s)')
        seen = set()
        for h in hits:
            s = str(h)[:220].replace('\n', ' ')
            if s not in seen:
                seen.add(s); print('   ', s)
            if len(seen) >= 4: break
