#!/usr/bin/env python3
"""Matcher: Wikipedia top-500 infra scan — match IP editors against CIDR provider map.

Stdlib only. Efficient lookup: CIDRs grouped by (address family, prefix length).
Within one prefix length the ranges are aligned networks, so they are disjoint
except for exact duplicates. Each query is one bisect per prefix length, tried
longest-first: the first containing network is the most specific match, and any
exact duplicates at that same network+plen are all recorded. O(#distinct
prefixlens * log n) per lookup — fully correct, no walk, no truncation.
"""
import json, ipaddress, re, bisect, time, os, glob
from collections import Counter

BASE = os.path.expanduser("~/workspace/silent-locus-top500/data/2026-10-06-wikipedia-top500-infra-scan")
RAW = os.path.join(BASE, "raw")
REVDIR = os.path.join(RAW, "revisions")
CIDRFILE = os.path.join(RAW, "cidr-provider-map.jsonl")
OUT_MATCHES = os.path.join(RAW, "ip-matches.jsonl")
OUT_AGGR = os.path.join(RAW, "article-aggregates.tsv")
FINDINGS = os.path.join(BASE, "workers", "matcher", "FINDINGS.md")

t0 = time.time()

# ---------- 1. Build CIDR lookup ----------
byplen = {4: {}, 6: {}}   # v -> plen -> sorted list of (start, end, provider, service)
n_cidr = 0
skipped = 0
with open(CIDRFILE) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
            net = ipaddress.ip_network(rec["cidr"], strict=False)
        except (ValueError, KeyError):
            skipped += 1
            continue
        v = net.version
        byplen[v].setdefault(net.prefixlen, []).append(
            (int(net.network_address), int(net.broadcast_address),
             rec.get("provider", "?"), rec.get("service", "?")))
        n_cidr += 1

plen_order = {}   # v -> prefix lengths, longest first
plen_starts = {}  # v -> {plen: [start, ...]} for bisect
for v in (4, 6):
    for plen, g in byplen[v].items():
        g.sort(key=lambda r: r[0])
    plen_order[v] = sorted(byplen[v], reverse=True)
    plen_starts[v] = {plen: [r[0] for r in byplen[v][plen]] for plen in byplen[v]}

def lookup(ip_str):
    """Return list of (provider, service) at the most specific matching prefixlen;
    all records sharing that exact network are included. [] if no match."""
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return None
    v = ip.version
    x = int(ip)
    for plen in plen_order[v]:
        g = byplen[v][plen]
        st = plen_starts[v][plen]
        i = bisect.bisect_right(st, x) - 1
        if i < 0:
            continue
        s, e, prov, svc = g[i]
        if s <= x <= e:
            out = [(prov, svc)]
            j = i - 1
            while j >= 0 and g[j][0] == s:      # exact duplicates of this network
                out.append((g[j][2], g[j][3])); j -= 1
            k = i + 1
            while k < len(g) and g[k][0] == s:
                out.append((g[k][2], g[k][3])); k += 1
            return out
    return []

# sanity check on known examples from the map
assert any(p == "anthropic" for p, _ in lookup("136.107.176.208")), "self-test failed"
assert lookup("203.0.113.77") == [], "self-test failed (TEST-NET-3 must not match)"

# ---------- 2. Classification ----------
temp_re = re.compile(r"^~\d{4}-")
cache = {}

def classify(user):
    if not isinstance(user, str):
        return "named"   # null/missing user; counted with named, noted in findings
    c = cache.get(user)
    if c is not None:
        return c
    try:
        ipaddress.ip_address(user)
        c = "ip"
    except ValueError:
        c = "temp" if temp_re.match(user) else "named"
    cache[user] = c
    return c

# sanity
assert classify("1.2.3.4") == "ip" and classify("2001:db8::1") == "ip"
assert classify("~2026-12345-6") == "temp" and classify("MSGJ") == "named"

# ---------- 3. Stream revisions ----------
total = ip_count = temp_count = named_count = 0
unmatched = 0
unmatch16 = Counter()
unmatch6_48 = Counter()
prov_counter = Counter()
prov_svc_counter = Counter()
lookups_cache = {}
n_matched = 0

aggr = {}  # (rank, article) -> [total, ip, temp, named]
files = sorted(glob.glob(os.path.join(REVDIR, "*.jsonl")))
n_files = len(files)

with open(OUT_MATCHES, "w") as out:
    for fp in files:
        with open(fp) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                rank = rec.get("rank")
                article = rec.get("article", "?")
                user = rec.get("user", "")
                key = (rank, article)
                a = aggr.get(key)
                if a is None:
                    a = aggr[key] = [0, 0, 0, 0]
                a[0] += 1
                total += 1
                cls = classify(user)
                if cls == "ip":
                    a[1] += 1
                    ip_count += 1
                    m = lookups_cache.get(user)
                    if m is None:
                        m = lookup(user)
                        lookups_cache[user] = m
                    if m:
                        n_matched += 1
                        provs = sorted({p for p, s in m})
                        svcs = sorted({s for p, s in m})
                        for p in provs:
                            prov_counter[p] += 1
                        for p, s in m:
                            prov_svc_counter[(p, s)] += 1
                        out.write(json.dumps({
                            "rank": rank, "article": article,
                            "revid": rec.get("revid"), "timestamp": rec.get("timestamp"),
                            "ip": user, "providers": provs, "services": svcs,
                            "comment": rec.get("comment", ""), "tags": rec.get("tags", []),
                        }) + "\n")
                    else:
                        unmatched += 1
                        try:
                            ipo = ipaddress.ip_address(user)
                            if ipo.version == 4:
                                unmatch16[str(ipaddress.ip_network(str(ipo) + "/16", strict=False))] += 1
                            else:
                                unmatch6_48[str(ipaddress.ip_network(str(ipo) + "/48", strict=False))] += 1
                        except ValueError:
                            pass
                elif cls == "temp":
                    a[2] += 1
                    temp_count += 1
                else:
                    a[3] += 1
                    named_count += 1

# ---------- 4. article aggregates ----------
with open(OUT_AGGR, "w") as f:
    f.write("rank\tarticle\ttotal_revs\tip_revs\ttemp_revs\tnamed_revs\n")
    def rankkey(k):
        return k[0] if isinstance(k[0], int) else 999999
    for (rank, article) in sorted(aggr, key=rankkey):
        t, i, te, n = aggr[(rank, article)]
        f.write(f"{rank}\t{article}\t{t}\t{i}\t{te}\t{n}\n")

runtime = time.time() - t0

# ---------- 5. FINDINGS.md ----------
os.makedirs(os.path.dirname(FINDINGS), exist_ok=True)
top16 = unmatch16.most_common(15)
top48 = unmatch6_48.most_common(15)
ps = "\n".join(f"- {p}: {c}" for p, c in prov_counter.most_common())
psvc = "\n".join(f"- {p} / {s}: {c}" for (p, s), c in prov_svc_counter.most_common(25))
t16 = "\n".join(f"- {r}: {c}" for r, c in top16)
t48 = "\n".join(f"- {r}: {c}" for r, c in top48)
pct = lambda c: f"{100.0*c/max(total,1):.2f}%"
with open(FINDINGS, "w") as f:
    f.write(f"""# FINDINGS — Wikipedia top-500 infra scan: matcher (2026-10-06)

## IMPORTANT CAVEAT (read first)
**A datacenter-IP match is NOT proof of AI-agent use.** The CIDR map covers
provider-published ranges (AI labs' crawlers/tool IPs, cloud providers, VPNs,
hosting ASNs). A revision whose editor IP falls in one of these ranges shows
only that the edit came from infrastructure space — it is consistent with a
human on a VPN, a corporate NAT, a misattributed range, or crawler traffic, and
it says nothing about the edit's authorship. Treat every match as a *candidate
lead for further review*, never as attribution.

## Method
- Loaded {n_cidr:,} CIDR records from `raw/cidr-provider-map.jsonl`
  ({skipped} skipped as unparsable), grouped by (address family, prefix length).
- Within one prefix length, ranges are aligned networks, hence disjoint except
  for exact duplicates — so each query is a single `bisect` per prefix length,
  tried longest-first. The first containing network is the most specific match;
  if several records share that exact network, all providers/services recorded.
- Query complexity is O(distinct-prefixlens x log n); exact, no walk, no
  truncation. Per-IP results cached across revisions.
- Classification of `user` is strict full-string: `ipaddress.ip_address()`
  success → IP (IPv4 + IPv6); else `^~\\d{{4}}-` → temp account; else named user.

## Volume
- Revision files processed: {n_files}
- Total revisions scanned: {total:,}
- IP-editor revisions: {ip_count:,} ({pct(ip_count)})
- Temp-account revisions: {temp_count:,} ({pct(temp_count)})
- Named-user revisions: {named_count:,} ({pct(named_count)})
- Distinct editor IP strings seen: {len(lookups_cache):,}
- IP-editor revisions matching the CIDR map: {n_matched:,}
- IP-editor revisions with NO match (unmatched): {unmatched:,}

## Match counts per provider
{ps if ps else "(none)"}

## Match counts per provider/service (top 25)
{psvc if psvc else "(none)"}

## Top unmatched IPv4 /16s
{t16 if t16 else "(none)"}

## Top unmatched IPv6 /48s
{t48 if t48 else "(none)"}

## Outputs
- `raw/ip-matches.jsonl` — one record per matched IP-editor revision
  (rank, article, revid, timestamp, ip, providers, services, comment, tags)
- `raw/article-aggregates.tsv` — per-article counts: total/ip/temp/named revisions

## Runtime
Matcher ran in {runtime:.1f}s (pure local computation, python3 stdlib only).

## Limitations
- Provider names are whatever the upstream CIDR source claimed; overlaps between
  cloud ranges and lab-published tool ranges are both recorded (most-specific
  network wins).
- Temp-account regex `^~\\d{{4}}-` matches MediaWiki's temporary-account grammar;
  IP editors behind masked accounts are not recoverable from this data.
""")

print(json.dumps({
    "files": n_files, "total": total, "ip": ip_count, "temp": temp_count,
    "named": named_count, "matched": n_matched, "unmatched": unmatched,
    "providers": dict(prov_counter), "runtime_s": round(runtime, 1),
}, indent=1))
