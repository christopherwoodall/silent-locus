#!/usr/bin/env python3
"""Dump HN thread JSONs as text-only (no author fields) for reading."""
import json, sys, re, html, os
RAW=os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-bypass-forum-hunt/raw/hn")
for iid in sys.argv[1:]:
    d=json.load(open(os.path.join(RAW,f"thread-{iid}.json")))
    print(f"\n######## THREAD {iid} items={d['item_count']}")
    for it in d["items"]:
        if it is None: continue
        txt=html.unescape(re.sub(r"<[^>]+>"," ", it.get("text") or ""))
        txt=re.sub(r"\s+"," ",txt)
        print(f"\n--- item {it.get('id')} type={it.get('type')} parent={it.get('parent')} created={it.get('time')}")
        if it.get("title"): print("TITLE:", it["title"])
        if it.get("url"): print("URL:", it["url"])
        if txt: print(txt[:2500])
