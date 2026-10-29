#!/usr/bin/env python3
"""Dedup Algolia captures; emit one TSV row per unique item with
title/text excerpt, plus per-item query list. No handles in output."""
import json, os, glob, re, html
RAW = os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-bypass-forum-hunt/raw/hn")
OUT = os.path.expanduser("~/workspace/silent-locus/reports/agent-bypass-forum-hunt/working/screen.tsv")
items={}
for fn in sorted(glob.glob(os.path.join(RAW,"*.json"))):
    if fn.endswith("probe.json"): continue
    try: d=json.load(open(fn))
    except Exception as e: print("skip",fn,e); continue
    q=d.get("query"); tag=d.get("tag")
    for h in d.get("hits",[]):
        oid=str(h.get("objectID"))
        e=items.setdefault(oid, {"id":oid,"type":tag,"created":h.get("created_at",""),
            "title":h.get("title") or "","text":h.get("comment_text") or h.get("story_text") or "",
            "story_id":h.get("story_id"),"parent":h.get("parent_id"),"queries":set(),"url":h.get("url") or ""})
        e["queries"].add(q)
        if not e["title"] and h.get("title"): e["title"]=h["title"]
        if not e["text"] and (h.get("comment_text") or h.get("story_text")): e["text"]=h.get("comment_text") or h.get("story_text")
def clean(s):
    s=html.unescape(re.sub(r"<[^>]+>"," ",s or ""))
    return re.sub(r"\s+"," ",s).strip()
rows=sorted(items.values(), key=lambda e:(e["created"],e["id"]))
with open(OUT,"w") as f:
    f.write("id\ttype\tcreated\ttitle\ttext_excerpt\tqueries\tstory_id\turl\n")
    for e in rows:
        t=clean(e["text"])[:600]
        f.write(f"{e['id']}\t{e['type']}\t{e['created']}\t{clean(e['title'])}\t{t}\t{' | '.join(sorted(e['queries']))}\t{e['story_id'] or ''}\t{e['url']}\n")
print(f"unique items: {len(rows)}  stories: {sum(1 for r in rows if r['type']=='story')}  comments: {sum(1 for r in rows if r['type']=='comment')}")
# overlap check vs known exclusion ids
KNOWN={"49535519","49429926","46622328","48349487","48827858","49379079","46725158","47183940","46544454","50246658","48414158","48916975","48838376","46007287","46036247","46344611","46531565","46592424","46710569","46890573","47951786","48182413","48226268","48283191","48403433","48738860","48326276","48417032","48211229","49376549","49501565","49911869","49932357","50099375","45821970","47152609","47136170","47109114","46385982","50249935"}
print("known-id overlap in sweep:", sorted(set(items)&KNOWN))
for oid in sorted(set(items)&KNOWN):
    e=items[oid]; print(f"  OVERLAP {oid} {e['type']} {clean(e['title'])[:80]} queries={sorted(e['queries'])}")
