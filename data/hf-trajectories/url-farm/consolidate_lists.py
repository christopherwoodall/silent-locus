#!/usr/bin/env python3
"""Fold farm output into lists/: new terms -> lists/words, tiered URLs -> lists/urls."""
import json, os
from datetime import datetime, timezone
from urllib.parse import urlparse

ROOT = os.path.expanduser("~/workspace/silent-locus")
FARM = os.path.join(ROOT, "data/hf-trajectories/url-farm")
WORDS = os.path.join(ROOT, "lists/words")
URLS = os.path.join(ROOT, "lists/urls")
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
PROV = "data/hf-trajectories/URL-KEYWORD-FARM.md (url-keyword-farm, 2026-10-08): HF trajectory URL/keyword farm"

NEW_TERMS = [
    ("turnstile", "bot_walls"),
    ("captcha", "bot_walls"),
    ("jailbreak", "launcher_toolkit"),
    ("exfiltrate", "dead_drops"),
    ("exfiltration", "dead_drops"),
    ("dead-drop", "dead_drops"),
]

# --- words ---
txt_p = os.path.join(WORDS, "wordlist.txt")
with open(txt_p) as f:
    lines = f.read().splitlines()
existing_terms = {l.strip() for l in lines if l.strip() and not l.startswith("#")}
added_txt = 0
with open(txt_p, "a") as f:
    f.write("\n# BOT_WALLS\n")
    for term, _ in NEW_TERMS:
        if term not in existing_terms:
            f.write(term + "\n")
            existing_terms.add(term)
            added_txt += 1

json_p = os.path.join(WORDS, "wordlist.json")
with open(json_p) as f:
    j = json.load(f)
existing_j = {e["term"] for e in j}
added_json = 0
for term, cat in NEW_TERMS:
    if term not in existing_j:
        j.append({"term": term, "category": cat, "provenance": PROV,
                  "added_utc": NOW, "status": "active", "note": ""})
        added_json += 1
with open(json_p, "w") as f:
    json.dump(j, f, indent=1)
    f.write("\n")

# --- urls ---
def canonical(u):
    try:
        p = urlparse(u)
        return f"{p.scheme.lower()}://{p.netloc.lower()}{p.path}" + (f"?{p.query}" if p.query else "")
    except Exception:
        return u

merged = json.load(open(os.path.join(FARM, "merged.json")))
tier_urls = []
for t in ["EXFIL/C2", "PROXY-LAUNDER", "PASTEBIN", "TUNNEL"]:
    for u in merged["url_tier_top"].get(t, []):
        tier_urls.append((u["url"], ",".join(u["datasets"]), t))

# NOTE: merged.json only keeps top-30 per tier; rebuild full tier list from group files
full = {}
import sys
sys.path.insert(0, os.path.expanduser("~/workspace/.pylibs"))
import ijson
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

for fn in ["group-A.json", "group-B.json", "group-C.json", "group-D.json"]:
    p = os.path.join(FARM, fn)
    if not os.path.exists(p):
        continue
    if os.path.getsize(p) < 50_000_000:
        d = json.load(open(p))
        for u in d.get("urls", []):
            t = tier_of(u["url"])
            if t != "OTHER":
                full.setdefault(u["url"], {"ds": set(), "count": 0, "tier": t})
                full[u["url"]]["ds"].add(u.get("dataset", d.get("dataset", "?")))
                full[u["url"]]["count"] += u.get("count", 1)
    else:
        with open(p, "rb") as f:
            for u in ijson.items(f, "urls.item"):
                t = tier_of(u.get("url", ""))
                if t != "OTHER":
                    full.setdefault(u["url"], {"ds": set(), "count": 0, "tier": t})
                    full[u["url"]]["ds"].add(u.get("dataset", "?"))
                    full[u["url"]]["count"] += u.get("count", 1)

urls_p = os.path.join(URLS, "urls.jsonl")
with open(urls_p) as f:
    existing_urls = {json.loads(l)["url"] for l in f if l.strip()}
added_urls = 0
with open(urls_p, "a") as f:
    for url in sorted(full):
        if url not in existing_urls:
            e = full[url]
            f.write(json.dumps({"url": url, "canonical": canonical(url),
                                "finding_id": None, "submitter": "url-keyword-farm",
                                "source_field": "hf-trajectories:" + ",".join(sorted(e["ds"])),
                                "status": "NEW", "corpus_path": None,
                                "tier": e["tier"], "occurrences": e["count"]}) + "\n")
            existing_urls.add(url)
            added_urls += 1

print(f"terms added: txt={added_txt} json={added_json}")
print(f"urls added: {added_urls} (tiered unique: {len(full)})")
