#!/usr/bin/env python3
"""Shape-scoring API pass for burst-analysis candidates. Paced >=5s between requests.
For each candidate burst: list=users (uids) + usercontribs (batched, all accounts).
Caches raw JSON in burst-analysis/raw/ with provenance.
"""
import json, os, sys, time, urllib.parse, subprocess

OUT = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/burst-analysis/raw")
DOM = {
    "commonswiki": "commons.wikimedia.org",
    "mediawikiwiki": "www.mediawiki.org",
    "testwiki": "test.wikipedia.org",
    "incubatorwiki": "incubator.wikimedia.org",
    "metawiki": "meta.wikimedia.org",
}
UA = "burst-analysis-worker/1.0 (wikimedia rogue-agent hunt research; contact via repo)"

def api(wiki, params):
    params = dict(params); params.update({"action":"query","format":"json","formatversion":"2"})
    url = "https://" + DOM[wiki] + "/w/api.php?" + urllib.parse.urlencode(params, doseq=True)
    out = subprocess.run(["curl","-sS","--max-time","60","-A",UA,url],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"curl failed: {out.stderr[:200]}")
    time.sleep(5)  # pacing >=5s
    return json.loads(out.stdout)

bursts = json.load(open(OUT+"/bursts.json"))["bursts"]
targets = [b for b in bursts if b["wiki"] in ("commonswiki","mediawikiwiki","testwiki")]
# Skip the known May-18 mediawiki clean negative (translate-a-thon; see ACCOUNT-29822-53-WRITEUP.md)
targets = [b for b in targets if not (b["wiki"]=="mediawikiwiki" and b["t0_iso"].startswith("2026-05-18"))]
# dedupe: keep one entry per (wiki, date-hour) cluster -> use the 10m/1h as listed; group mediawiki 5/21
seen=set(); todo=[]
for b in targets:
    key=(b["wiki"], b["t0_iso"][:13])
    if key in seen: continue
    seen.add(key); todo.append(b)

results={}
for b in todo:
    wiki=b["wiki"]; names=b["names"]
    tag=f"{wiki}_{b['t0_iso'][:10]}"
    print(f"== {wiki} {b['t0_iso']}..{b['t1_iso']} n={len(names)}", flush=True)
    rec={"burst":b, "users":None, "contribs":None}
    try:
        # uids (50 per request)
        users=[]
        for i in range(0, len(names), 50):
            chunk=names[i:i+50]
            r=api(wiki, {"list":"users","ususers":"|".join(chunk)})
            users.extend(r["query"]["users"])
        rec["users"]=users
        with open(f"{OUT}/uids-{tag}.json","w") as f: json.dump(users,f)
        print(f"   uids: {len(users)}", flush=True)
    except Exception as ex:
        print(f"   users FAILED: {ex}", flush=True); rec["users_error"]=str(ex)
    try:
        contribs=[]
        for i in range(0, len(names), 50):
            chunk=names[i:i+50]
            r=api(wiki, {"list":"usercontribs","ucuser":"|".join(chunk),
                         "uclimit":"max","ucprop":"ids|title|timestamp|comment|sizediff|tags"})
            items=r["query"]["usercontribs"]
            contribs.extend(items)
            while "continue" in r:
                r=api(wiki, {"list":"usercontribs","ucuser":"|".join(chunk),
                             "uclimit":"max","ucprop":"ids|title|timestamp|comment|sizediff|tags",
                             **r["continue"]})
                contribs.extend(r["query"]["usercontribs"])
        rec["contribs"]=contribs
        with open(f"{OUT}/contribs-burst-{tag}.json","w") as f: json.dump(contribs,f)
        editors=sorted(set(c["user"] for c in contribs))
        print(f"   contribs: {len(contribs)} edits by {len(editors)} accounts", flush=True)
    except Exception as ex:
        print(f"   contribs FAILED: {ex}", flush=True); rec["contribs_error"]=str(ex)
    results[tag]= {"n_names":len(names),
                   "n_editors":len(set(c["user"] for c in (rec["contribs"] or []))),
                   "n_edits":len(rec["contribs"] or [])}

with open(OUT+"/shape-pass1.json","w") as f: json.dump(results,f,indent=1)
print(json.dumps(results,indent=1))
