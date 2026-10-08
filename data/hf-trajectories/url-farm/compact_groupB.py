#!/usr/bin/env python3
"""Compact group-B.json (276MB, over GitHub's 100MB limit) into group-B.compact.json.
Keeps: all high-suspicion keyword hits verbatim, keyword totals, URL tier tops +
counts. Drops: 182k benign localhost/Kiwix URLs and low-signal bulk hits.
Full file stays on local disk, untracked."""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/.pylibs"))
import ijson

FARM = os.path.expanduser("~/workspace/silent-locus/data/hf-trajectories/url-farm")
SRC = os.path.join(FARM, "group-B.json")
DST = os.path.join(FARM, "group-B.compact.json")

HIGH = {"jailbreak", "exfiltrate", "webhook.site", "ntfy.sh", "ngrok", "phishing",
        "nmap", "sqlmap", "metasploit", "reverse shell", "turnstile", "jina.ai",
        "telegram", "t.me/", "discord.com/api/webhooks", "captcha", "cloudflare",
        "DAN", "system prompt", "circumvent"}

def tier_of(url):
    h = url.lower()
    for d in ["webhook.site", "ntfy.sh", "discord.com/api/webhooks", "t.me/"]:
        if d in h: return "EXFIL/C2"
    for d in ["jina.ai", "allorigins.win", "corsproxy", "allorigins.hexlet"]:
        if d in h: return "PROXY-LAUNDER"
    for d in ["pastebin.com", "paste.rs", "0x0.st", "termbin", "ix.io", "hastebin"]:
        if d in h: return "PASTEBIN"
    for d in ["ngrok", "trycloudflare", "localtunnel", "bore.pub"]:
        if d in h: return "TUNNEL"
    return "OTHER"

kw_totals = {}
high_hits = []
url_tops = {}
tier_counts = {}
n_urls = 0

with open(SRC, "rb") as f:
    for h in ijson.items(f, "keyword_hits.item"):
        pat = h.get("pattern", "?")
        key = (pat, h.get("dataset", "?"))
        kw_totals[key] = kw_totals.get(key, 0) + 1
        if pat in HIGH:
            high_hits.append(h)
with open(SRC, "rb") as f:
    for u in ijson.items(f, "urls.item"):
        n_urls += 1
        t = tier_of(u.get("url", ""))
        tier_counts[t] = tier_counts.get(t, 0) + 1
        lst = url_tops.setdefault(t, [])
        lst.append(u)
for t in url_tops:
    url_tops[t].sort(key=lambda x: -x.get("count", 0))
    url_tops[t] = url_tops[t][:100]

compact = {
    "note": "Compacted from group-B.json (276MB, exceeds GitHub 100MB limit). "
            "Full file retained on local disk, untracked. All high-suspicion "
            "keyword hits kept verbatim; bulk benign URLs/hits summarized.",
    "datasets": [{"name": "crownelius/gpt-5.6-sol-luna-terra-traces", "rows_scanned": 15353},
                 {"name": "tiger-lab/browseragent-data", "rows_scanned": 44355}],
    "unique_urls_total": n_urls,
    "url_tier_counts": tier_counts,
    "url_tier_top100": url_tops,
    "keyword_totals": {f"{p} [{d}]": c for (p, d), c in
                       sorted(kw_totals.items(), key=lambda kv: -kv[1])},
    "high_suspicion_hits": high_hits,
}
with open(DST, "w") as f:
    json.dump(compact, f)
print("compact bytes:", os.path.getsize(DST))
print("high hits kept:", len(high_hits))
