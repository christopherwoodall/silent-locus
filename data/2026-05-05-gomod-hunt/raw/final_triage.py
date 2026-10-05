import json, re, glob, collections
DISTINCT = {
    "epoch10": re.compile(r'\d{10}'),
    "tryzz": re.compile(r'try[a-z][0-9]zz'),
    "zzlead": re.compile(r'(^|/)zz'),
    "oai": re.compile(r'oai', re.I),
}
HIGH = ["jina", "go-import", "goimport", "moderngov", "lambeth", "wandsworth",
        "southwark", "county.json", "builder", "yard", "ssrf", "exfil",
        "webhook", "oast", "dead-drop", "deaddrop"]
counts = collections.Counter(); seen = set(); total = 0; dupes = 0
strict_hits = []; high_hits = collections.Counter(); high_ex = collections.defaultdict(list)
rx_epoch_name = re.compile(r'\d{10}'); rx_zzword = re.compile(r'zz[a-z]{2,}')
for fn in sorted(glob.glob("matches_*.jsonl")):
    for line in open(fn):
        row = json.loads(line); total += 1
        key = (row["Path"], row["Version"])
        if key in seen: dupes += 1; continue
        seen.add(key)
        p = row["Path"]; final = p.rsplit("/",1)[-1]
        fired = [k for k, rx in DISTINCT.items() if rx.search(p)]
        for k in fired: counts[k] += 1
        if not fired: counts["generic"] += 1
        if rx_epoch_name.search(final) or re.compile(r'try[a-z][0-9]zz').search(p) or rx_zzword.search(final):
            strict_hits.append((p, row["Version"], row["Timestamp"][:19]))
        pl = p.lower()
        for h in HIGH:
            if h in pl:
                high_hits[h] += 1
                if len(high_ex[h]) < 3: high_ex[h].append(p)
print(f"raw lines={total} dupes={dupes} unique={len(seen)}")
print("distinctive:", dict(counts))
print(f"\nstrict name-grammar hits: {len(strict_hits)}")
for s in strict_hits[:25]: print("  ", s)
print("\nhigh-value substring counts:", dict(high_hits))
for h, ex in high_ex.items():
    if h not in ("builder","yard","goimport","go-import","jina","webhook"):
        print(f"  !! {h}: {ex}")
