#!/usr/bin/env python3
"""Merge group-A/B/C/D farm JSONs into a global URL inventory + keyword rollup.
Streams large files with ijson. Writes url-farm/merged.json (compact) and
url-farm/lead-candidates.json for curator review.
"""
import json, os, re, sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.expanduser("~/workspace/.pylibs"))
import ijson

FARM = os.path.expanduser("~/workspace/silent-locus/data/hf-trajectories/url-farm")

EXFIL_C2 = ["webhook.site", "ntfy.sh", "discord.com/api/webhooks", "discordapp.com/api/webhooks",
            "api.telegram.org", "t.me/", "requestbin", "pipedream.net", "beeceptor.com",
            "webhookrelay.com", "hook.us", "postb.in", "ptsv2.com", "enformed.io"]
PROXY_LAUNDER = ["jina.ai", "r.jina.ai", "corsproxy.io", "allorigins.win", "cors-anywhere",
                 "thingproxy", "corsproxy.org", "proxy.cors.sh"]
PASTEBIN = ["pastebin.com", "paste.rs", "0x0.st", "termbin.com", "ix.io", "hastebin.com",
            "privatebin", "ghostbin", "controlc.com", "rentry.co", "paste.ee", "dpaste"]
TUNNEL = ["ngrok.io", "ngrok.com", "trycloudflare.com", "localtunnel.me", "bore.pub",
          "localhost.run", "serveo.net", "boreproxy", "zrok.io"]

def tier(url):
    try:
        host = urlparse(url).netloc.lower()
    except Exception:
        host = ""
    low = url.lower()
    for d in EXFIL_C2:
        if d in host or d in low: return "EXFIL/C2"
    for d in PROXY_LAUNDER:
        if d in host: return "PROXY-LAUNDER"
    for d in PASTEBIN:
        if d in host: return "PASTEBIN"
    for d in TUNNEL:
        if d in host: return "TUNNEL"
    return "OTHER"

HIGH_SUSPicion = {"jailbreak", "exfiltrate", "webhook.site", "ntfy.sh", "ngrok",
                  "harness anti-bot guidance", "phishing", "nmap", "sqlmap",
                  "metasploit", "reverse shell", "turnstile", "jina.ai",
                  "telegram", "t.me/", "discord.com/api/webhooks", "captcha",
                  "cloudflare", "DAN"}

url_inv = {}   # url -> {count, datasets:set, examples:[...]}
kw_agg = {}    # (pattern, dataset) -> {count, examples:[{text, refs}]}
rows_scanned = {}
notes_all = []

def add_url(u):
    url = u.get("url", "")
    if not url: return
    e = url_inv.setdefault(url, {"count": 0, "datasets": set(), "examples": []})
    e["count"] += u.get("count", 1)
    e["datasets"].add(u.get("dataset", "?"))
    for ex in (u.get("examples") or [])[:5]:
        if len(e["examples"]) < 5:
            e["examples"].append(ex)

def add_hit(h, default_ds="?"):
    pat = h.get("pattern", "?")
    ds = h.get("dataset", default_ds)
    key = (pat, ds)
    e = kw_agg.setdefault(key, {"count": 0, "examples": []})
    e["count"] += 1
    if len(e["examples"]) < 3:
        e["examples"].append({
            "text": (h.get("matched_text") or "")[:400],
            "task": h.get("task"), "agent": h.get("agent"),
            "model": h.get("model"), "trial_id": h.get("trial_id"),
            "timestamp": h.get("timestamp"),
        })

def stream_group(path, gname):
    print(f"streaming {gname} ...", flush=True)
    with open(path, "rb") as f:
        # datasets meta
        try:
            with open(path) as f2:
                head = json.load(f2) if os.path.getsize(path) < 50_000_000 else None
        except Exception:
            head = None
        if head:
            dslist = head.get("datasets") or ([{"name": head.get("dataset")}] if head.get("dataset") else [])
            for d in dslist:
                rows_scanned[d.get("name", gname)] = d.get("rows_scanned")
            notes_all.append({gname: head.get("notes")})
            top_ds = head.get("dataset") or gname
            for u in head.get("urls", []):
                u.setdefault("dataset", top_ds)
                add_url(u)
            for h in head.get("keyword_hits", []):
                h.setdefault("dataset", top_ds)
                add_hit(h)
            return
        # large file: stream arrays
        f.seek(0)
        for u in ijson.items(f, "urls.item"):
            add_url(u)
        f.seek(0)
        for h in ijson.items(f, "keyword_hits.item"):
            add_hit(h)
        f.seek(0)
        try:
            for d in ijson.items(f, "datasets.item"):
                rows_scanned[d.get("name", gname)] = d.get("rows_scanned")
        except Exception:
            pass
        f.seek(0)
        try:
            for n in ijson.items(f, "notes"):
                notes_all.append({gname: n})
                break
        except Exception:
            pass

for gname, fn in [("A", "group-A.json"), ("B", "group-B.json"),
                  ("C", "group-C.json"), ("D", "group-D.json")]:
    p = os.path.join(FARM, fn)
    if os.path.exists(p):
        stream_group(p, gname)

# tier the inventory
tiered = {}
for url, e in url_inv.items():
    t = tier(url)
    tiered.setdefault(t, []).append({"url": url, "count": e["count"],
                                     "datasets": sorted(e["datasets"]),
                                     "examples": e["examples"]})
for t in tiered:
    tiered[t].sort(key=lambda x: -x["count"])

# lead candidates: high-suspicion keyword hits with examples
cands = []
for (pat, ds), e in kw_agg.items():
    if pat in HIGH_SUSPicion and e["count"] > 0:
        cands.append({"pattern": pat, "dataset": ds, "count": e["count"],
                      "examples": e["examples"]})
cands.sort(key=lambda x: -x["count"])

merged = {
    "rows_scanned": rows_scanned,
    "url_tiers": {t: len(v) for t, v in tiered.items()},
    "url_tier_top": {t: v[:30] for t, v in tiered.items()},
    "keyword_totals": {f"{p} [{d}]": e["count"] for (p, d), e in
                       sorted(kw_agg.items(), key=lambda kv: -kv[1]["count"])},
    "notes": notes_all,
}
with open(os.path.join(FARM, "merged.json"), "w") as f:
    json.dump(merged, f)
with open(os.path.join(FARM, "lead-candidates.json"), "w") as f:
    json.dump(cands, f, indent=1)

print("URLs total:", len(url_inv))
print("tiers:", {t: len(v) for t, v in tiered.items()})
print("kw patterns:", len(kw_agg))
print("lead candidates:", len(cands))
print("rows:", rows_scanned)
