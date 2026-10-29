#!/usr/bin/env python3
"""Extract readable text from fetched HTML (analysis working copy; raw HTML is the evidence)."""
import re, sys, html, glob, os

def extract(path):
    h = open(path, encoding='utf-8', errors='replace').read()
    h = re.sub(r'<script[\s>].*?</script\s*>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<style[\s>].*?</style\s*>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<[^>]+>', '\n', h)
    h = html.unescape(h)
    lines = [l.strip() for l in h.split('\n')]
    lines = [l for l in lines if l]
    # drop obvious nav/boilerplate runs: lines seen verbatim many times
    from collections import Counter
    c = Counter(lines)
    lines = [l for l in lines if c[l] <= 4]
    return '\n'.join(lines)

raw = os.path.dirname(os.path.abspath(__file__))
for f in sorted(glob.glob(os.path.join(raw, '*.html'))):
    out = f[:-5] + '.txt'
    t = extract(f)
    open(out, 'w', encoding='utf-8').write(t)
    print(os.path.basename(out), len(t))
