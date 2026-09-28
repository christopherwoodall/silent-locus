#!/usr/bin/env python3
"""Wiki IOC pivot lane: extract IOCs from collusion.wiki corpus, build IOC<->agent<->wiki
graph, pivot against the gem corpus. Read-only."""
import json, re, math, sys, os
from collections import defaultdict, Counter
from urllib.parse import urlparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CW = BASE + "/data/collusion-wiki"

URL_RE = re.compile(r"https?://[^\s<>\"'()\[\]{}]+", re.I)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
HASH_RE = re.compile(r"\b[0-9a-fA-F]{32}\b|\b[0-9a-fA-F]{40}\b|\b[0-9a-fA-F]{64}\b")
BTC_RE = re.compile(r"\b(bc1|[13])[a-km-zA-HJ-NP-Z1-9]{25,59}\b")
ETH_RE = re.compile(r"\b0x[0-9a-fA-F]{40}\b")
SHORT_RE = re.compile(r"\brmn\.re/[A-Za-z0-9_-]+\b")

# domains too common to be pivots
STOP_DOMAINS = {
    "google.com", "www.google.com", "wikipedia.org", "en.wikipedia.org",
    "github.com", "www.github.com", "youtube.com", "www.youtube.com",
    "facebook.com", "twitter.com", "x.com", "amazon.com", "microsoft.com",
    "apple.com", "mozilla.org", "w3.org", "validator.w3.org", "iana.org",
    "example.com", "example.org", "localhost",
}

def host_of(url):
    try:
        h = urlparse(url).hostname or ""
        return h.lower().rstrip(".")
    except Exception:
        return ""

def reg_domain(host):
    parts = host.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else host

def extract_iocs(text):
    out = defaultdict(set)
    for u in URL_RE.findall(text or ""):
        u = u.rstrip(".,;:!?\"'")
        h = host_of(u)
        if not h or h.startswith("..."):
            continue
        out["url"].add(u[:500])
        out["domain"].add(h)
        out["reg_domain"].add(reg_domain(h))
    for e in EMAIL_RE.findall(text or ""):
        if not e.lower().startswith("example@"):
            out["email"].add(e.lower()[:120])
    for ip in IP_RE.findall(text or ""):
        octs = ip.split(".")
        if all(o.isdigit() and int(o) < 256 for o in octs) and not ip.startswith(("0.", "127.", "255.")):
            out["ip"].add(ip)
    for h_ in HASH_RE.findall(text or ""):
        out["hash"].add(h_.lower())
    for b in BTC_RE.findall(text or ""):
        out["crypto"].add(b)
    for e_ in ETH_RE.findall(text or ""):
        out["crypto"].add(e_)
    for s in SHORT_RE.findall(text or ""):
        out["shortener"].add(s.lower())
    return out

# ---- load wiki corpus ----
ioc_agents = defaultdict(set)   # ioc_key -> set of (agent_label, wiki)
ioc_src = defaultdict(list)     # ioc_key -> list of source strings
ioc_type = {}
agent_wikis = defaultdict(set)
wiki_counts = Counter()
n_rev = 0

def add(iocs, agent, wiki, src):
    for t, vals in iocs.items():
        for v in vals:
            key = (t, v)
            ioc_type[key] = t
            if agent:
                ioc_agents[key].add((agent, wiki))
                agent_wikis[agent].add(wiki)
            ioc_src[key].append(src)

with open(CW + "/revisions.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        n_rev += 1
        wiki = r.get("wiki", "?")
        wiki_counts[wiki] += 1
        body = r.get("body") or ""
        iocs = extract_iocs(body)
        add(iocs, r.get("label"), wiki, "revisions.jsonl:" + str(r.get("rev_id")))

with open(CW + "/records.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        rid = r.get("id")
        origins = r.get("origins") or []
        wikis = set()
        agents = set()
        for o in origins if isinstance(origins, list) else []:
            if isinstance(o, dict):
                if o.get("wiki"):
                    wikis.add(o["wiki"])
                if o.get("label"):
                    agents.add(o["label"])
        for w in (wikis or {"?"}):
            for a in (agents or {None}):
                add(extract_iocs(r.get("text") or ""), a, w, "records.jsonl:" + str(rid))

# shortener log: sites -> [{site, links:[{keyword,url,title,time,ip16,clicks}]}]
short_entries = []
short_kw_grammars = Counter()
short_target_hosts = Counter()
try:
    sl = json.load(open(CW + "/shortener-logs.json"))
    sites = sl.get("sites") or []
    for site in sites:
        for it in site.get("links", []):
            kw = str(it.get("keyword") or "")
            tgt = str(it.get("url") or "")
            iocs = extract_iocs(tgt)
            iocs["shortener_slug"].add("rmn.re/" + kw)
            add(iocs, None, "shortener", "shortener-logs.json:" + kw)
            th = host_of(tgt)
            if tgt:
                short_entries.append({"slug": kw, "target": tgt[:300],
                                      "target_host": th,
                                      "time": str(it.get("time") or ""),
                                      "ip16": str(it.get("ip16") or ""),
                                      "clicks": it.get("clicks")})
                short_target_hosts[th] += 1
                if re.search(r"zz", kw):
                    short_kw_grammars["zz-bearing"] += 1
                if re.search(r"\d{10}", kw):
                    short_kw_grammars["epoch-suffix"] += 1
                if re.search(r"^try[a-z][0-9]zz", kw):
                    short_kw_grammars["try[a-z][0-9]zz"] += 1
                if re.search(r"oai", kw, re.I):
                    short_kw_grammars["oai"] += 1
except Exception as e:
    print("shortener parse note:", e, file=sys.stderr)
json.dump({"n": len(short_entries),
           "target_hosts": short_target_hosts.most_common(25),
           "keyword_grammars": dict(short_kw_grammars),
           "entries": short_entries},
          open(BASE + "/data/wiki_shortener_detail.json", "w"), indent=2)

# links.jsonl host rollup
link_hosts = Counter()
link_host_records = defaultdict(set)
with open(CW + "/links.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        l = json.loads(line)
        h = l.get("host") or host_of(l.get("url", ""))
        if h and not h.startswith("..."):
            link_hosts[h] += len(l.get("record_ids", []))
            for rid in l.get("record_ids", [])[:50]:
                link_host_records[h].add(rid)

print(f"revisions scanned: {n_rev}, wikis: {dict(wiki_counts)}", file=sys.stderr)
print(f"distinct IOCs: {len(ioc_type)}, with agent attribution: {sum(1 for v in ioc_agents.values() if v)}", file=sys.stderr)
print(f"shortener entries parsed: {len(short_entries)}, link hosts: {len(link_hosts)}", file=sys.stderr)

# ---- gem corpus for cross-pivot ----
gem_domains = defaultdict(set)   # domain -> set of gem names
gem_urls = set()
try:
    with open(BASE + "/data/gem-iocs-2026-09-27.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            g = json.loads(line)
            ioc, t = g.get("ioc", ""), g.get("type")
            if t == "url":
                h = host_of(ioc)
                if h:
                    gem_domains[h].add(g.get("context", "")[:60])
                    gem_domains[reg_domain(h)].add(g.get("context", "")[:60])
                    gem_urls.add(ioc[:300])
            elif t == "domain":
                gem_domains[ioc.lower()].add(g.get("context", "")[:60])
except Exception as e:
    print("gem iocs note:", e, file=sys.stderr)

try:
    with open(BASE + "/data/gem-graph-nodes.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n = json.loads(line)
            for fld in ("homepage_uri", "source_url", "url", "description"):
                v = n.get(fld) or ""
                for u in URL_RE.findall(str(v)):
                    h = host_of(u)
                    if h:
                        gem_domains[h].add("gem:" + str(n.get("package") or n.get("id"))[:60])
except Exception as e:
    print("gem graph note:", e, file=sys.stderr)

# 79-bridge gems' homepage chains
bridge = {}
try:
    bridge = json.load(open(BASE + "/data/wiki_gem_bridge.json"))
except Exception as e:
    print("bridge note:", e, file=sys.stderr)
bridge_hosts = Counter()
def walk_bridge(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and ("http" in v):
                for u in URL_RE.findall(v):
                    h = host_of(u)
                    if h:
                        bridge_hosts[h] += 1
            else:
                walk_bridge(v)
    elif isinstance(o, list):
        for v in o:
            walk_bridge(v)
walk_bridge(bridge)
print(f"gem corpus domains: {len(gem_domains)}, bridge hosts: {len(bridge_hosts)}", file=sys.stderr)

# ---- laundering chain reconstruction ----
chains = Counter()
chain_examples = {}
def chain_shape(url):
    steps = []
    cur = url
    seen = 0
    while cur and seen < 6:
        h = host_of(cur)
        if not h:
            break
        steps.append(h)
        m = re.search(r"r\.jina\.ai/(https?://[^,\s\"']+)", cur, re.I)
        if m:
            cur = m.group(1)
        else:
            # translate.goog / allorigins wrappers
            m2 = re.search(r"(?:translate\.goog|allorigins\.\w+|markdown\.new)[^\"'\s]*?(https?://[^,\s\"']+)", cur, re.I)
            if m2 and m2.group(1) != cur:
                cur = m2.group(1)
            else:
                break
        seen += 1
    return " -> ".join(steps)

for (t, v) in ioc_type:
    if t == "url" and ("jina" in v or "translate.goog" in v or "allorigins" in v or "markdown.new" in v or "webcrawlerapi" in v):
        shape = chain_shape(v)
        if "->" in shape:
            chains[shape] += 1
            if shape not in chain_examples:
                chain_examples[shape] = v[:250]

# ---- ranking ----
pivots = []
for (t, v), aw in ioc_agents.items():
    wikis = {w for _, w in aw if w and w != "?"}
    agents = {a for a, _ in aw if a}
    if t in ("domain", "reg_domain") and (v in STOP_DOMAINS):
        continue
    if t == "hash":
        continue  # record shas, not pivots
    cross = False
    if t in ("domain", "reg_domain"):
        cross = v in gem_domains or reg_domain(v) in gem_domains
    elif t == "url":
        cross = host_of(v) in gem_domains
    elif t == "shortener":
        cross = False
    n_occ = len(ioc_src[(t, v)])
    rarity = 1.0 / (1.0 + math.log1p(n_occ))
    score = len(wikis) * 3 + len(agents) * 0.5 + (10 if cross else 0) + rarity * 2
    # agents/infrastructure only: skip nothing here (no person data in corpus), but keep emails low-ranked
    if t == "email":
        score *= 0.2
    pivots.append({
        "ioc": v, "type": t,
        "wikis": sorted(wikis), "n_wikis": len(wikis),
        "agents": sorted(list(agents))[:25], "n_agents": len(agents),
        "n_occurrences": n_occ,
        "cross_corpus_gem": bool(cross),
        "gem_context": sorted(gem_domains.get(v, gem_domains.get(reg_domain(v), set())))[:5] if cross and t in ("domain","reg_domain") else [],
        "rank_score": round(score, 2),
        "sources": ioc_src[(t, v)][:5],
    })

pivots.sort(key=lambda p: -p["rank_score"])

with open(BASE + "/data/wiki_ioc_pivots.jsonl", "w") as f:
    for p in pivots:
        f.write(json.dumps(p) + "\n")

summary = {
    "n_pivots": len(pivots),
    "n_cross_wiki": sum(1 for p in pivots if p["n_wikis"] > 1),
    "n_cross_corpus": sum(1 for p in pivots if p["cross_corpus_gem"]),
    "n_both": sum(1 for p in pivots if p["n_wikis"] > 1 and p["cross_corpus_gem"]),
    "top_chains": [{"shape": s, "count": c, "example": chain_examples[s]} for s, c in chains.most_common(15)],
    "top_link_hosts": [{"host": h, "record_refs": c} for h, c in link_hosts.most_common(25)],
    "shortener_entries": len(short_entries),
    "bridge_top_hosts": [{"host": h, "count": c} for h, c in bridge_hosts.most_common(20)],
    "agent_wiki_span": {a: sorted(w) for a, w in agent_wikis.items() if len(w) > 1},
}
json.dump(summary, open(BASE + "/data/wiki_ioc_pivot_summary.json", "w"), indent=2)
print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in summary.items()}, indent=1))
print("TOP 15 PIVOTS:")
for p in pivots[:15]:
    print(f"  [{p['rank_score']}] {p['type']}:{p['ioc'][:70]} wikis={p['wikis']} agents={p['n_agents']} gem={p['cross_corpus_gem']}")
