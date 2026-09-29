#!/usr/bin/env python3
"""Diff re-sweep captures against morning baselines.

Parses new stats HTML (traffic summary + referrer host rows) and compares
with the morning evidence (txt summaries + referrer JSONs). Prints deltas
and flags NEW referrer hosts (the proxy-ladder tripwire).
"""
import os, re, json

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EV = os.path.join(BASE, "data", "yourls-resweep-2026-09-28", "evidence")
OLD = os.path.join(BASE, "data")

def parse_new(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    out = {}
    m = re.search(r"Last 24 hours (\d+) hits?.*?Last 7 days (\d+) hits?.*?Last 30 days (\d+) hits?.*?All time (\d+) hits?", text)
    if m:
        out["traffic"] = {"24h": int(m.group(1)), "7d": int(m.group(2)),
                          "30d": int(m.group(3)), "all": int(m.group(4))}
    refs = {}
    for hm in re.finditer(r"class='sites_list'[^>]*>.*?([\w.\-]+(?:\.[\w.\-]+)+): <strong>([\d,]+)</strong>", html):
        refs[hm.group(1).lower()] = int(hm.group(2).replace(",", ""))
    out["referrers"] = refs
    dm = re.search(r"Direct traffic:?\s*([\d,]+)", text, re.I)
    if dm:
        out["direct"] = int(dm.group(1).replace(",", ""))
    return out

def old_referrers_from_txt(path):
    refs = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"^([a-zA-Z0-9.\-]+(?:\.[a-zA-Z0-9.\-]+)+): (\d+)\s*$", line.strip())
        if m:
            refs[m.group(1).lower()] = int(m.group(2))
    return refs

def old_traffic_from_txt(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"last 24h (\d+).*?last 7d (\d+).*?last 30d (\d+).*?ALL TIME (\d+)", txt)
    if m:
        return {"24h": int(m.group(1)), "7d": int(m.group(2)),
                "30d": int(m.group(3)), "all": int(m.group(4))}
    return None

PAGES = [
    ("7t6-o",   "unm_7t6-o",    "university-shorteners/goto-unm-edu/7t6-o_stats_2026-09-28.txt"),
    ("discvr",  "unm_discvr",   "university-shorteners/goto-unm-edu/discvr_stats_2026-09-28.txt"),
    ("reso",    "unm_reso",     "university-shorteners/goto-unm-edu/reso_stats_2026-09-28.txt"),
    ("urphy21", "unm_urphy21",  "university-shorteners/goto-unm-edu/urphy21_stats_2026-09-28.txt"),
]

for slug, newname, oldrel in PAGES:
    newp = os.path.join(EV, "%s_resweep_2026-09-28.html" % newname)
    oldp = os.path.join(OLD, oldrel)
    if not os.path.exists(newp):
        print("%s: NEW capture missing" % slug); continue
    new = parse_new(newp)
    old_refs = old_referrers_from_txt(oldp)
    old_tr = old_traffic_from_txt(oldp)
    print("=" * 60)
    print("%s  traffic old=%s new=%s" % (slug, old_tr, new.get("traffic")))
    if old_tr and new.get("traffic"):
        d = {k: new["traffic"][k] - old_tr[k] for k in old_tr}
        print("  delta:", d)
    new_refs = new["referrers"]
    added = {h: new_refs[h] for h in new_refs if h not in old_refs}
    changed = {h: (old_refs[h], new_refs[h]) for h in new_refs
               if h in old_refs and new_refs[h] != old_refs[h]}
    print("  NEW referrer hosts:", added if added else "none")
    print("  changed hosts:", changed if changed else "none")
    print("  host count old=%d new=%d" % (len(old_refs), len(new_refs)))
