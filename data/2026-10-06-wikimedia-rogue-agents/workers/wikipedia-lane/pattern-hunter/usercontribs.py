#!/usr/bin/env python3
"""PATTERN-HUNTER phase 3b: usercontribs for anchor accounts beyond the 54.
Also grabs the in-burst incubator rev 7226106 (not in the CSV). curl, 5.5s pacing.
Grade: OBSERVED."""
import json, os, subprocess, sys, time, urllib.parse

BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents")
RAW = os.path.join(BASE, "workers/wikipedia-lane/pattern-hunter/raw")
UA = "silent-locus-pattern-hunter/1.0 (OSINT research; mailto:research@example.org)"
PACE = 5.5

# (host, user) pairs: anchor accounts per incident wiki
TARGETS = [
    ("en.wikipedia.org", "~2026-28355-02"), ("test.wikipedia.org", "~2026-28355-02"),
    ("test2.wikipedia.org", "~2026-28355-02"), ("www.mediawiki.org", "~2026-28355-02"),
    ("en.wikipedia.org", "~2026-28217-20"), ("en.wikipedia.org", "~2026-28380-92"),
    ("en.wikipedia.org", "~2026-28435-23"), ("en.wikipedia.org", "~2026-31565-39"),
    ("en.wikipedia.org", "~2026-31693-52"),
    ("test.wikipedia.org", "~2026-31087-50"), ("test.wikipedia.org", "~2026-31625-92"),
    ("test.wikipedia.org", "~2026-31558-62"), ("test.wikipedia.org", "~2026-35379-90"),
    ("test2.wikipedia.org", "~2026-31711-15"),
    ("commons.wikimedia.org", "~2026-28987-61"), ("commons.wikimedia.org", "~2026-29065-25"),
    ("commons.wikimedia.org", "~2026-29018-32"), ("commons.wikimedia.org", "~2026-28986-96"),
    ("commons.wikimedia.org", "~2026-35737-64"), ("commons.wikimedia.org", "~2026-36766-54"),
    ("incubator.wikimedia.org", "~2026-36686-00"), ("incubator.wikimedia.org", "~2026-36781-18"),
    ("incubator.wikimedia.org", "~2026-36722-50"), ("incubator.wikimedia.org", "~2026-36920-78"),
    ("incubator.wikimedia.org", "~2026-36837-69"), ("incubator.wikimedia.org", "~2026-36803-16"),
    ("incubator.wikimedia.org", "~2026-36724-00"), ("incubator.wikimedia.org", "~2026-36867-71"),
    ("meta.wikimedia.org", "~2026-36837-35"),
    ("simple.wikipedia.org", "~2026-35411-85"),
    ("bg.wikipedia.org", "~2026-31341-00"),
]

def curl_json(url):
    time.sleep(PACE)
    out = subprocess.run(["curl", "-sS", "--max-time", "60", "-A", UA, url],
                         capture_output=True, text=True)
    if out.returncode != 0:
        print(f"CURL FAIL {url}: {out.stderr.strip()}", file=sys.stderr)
        return None
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        print(f"JSON FAIL {url}: {out.stdout[:200]}", file=sys.stderr)
        return None

def bank(name, url, data):
    with open(os.path.join(RAW, name), "w") as f:
        json.dump({"provenance": {"source_url": url,
                   "retrieved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
                   "response": data}, f, indent=1)

# 1. the in-burst missing rev
url = ("https://incubator.wikimedia.org/w/api.php?action=query&prop=revisions"
       "&revids=7226106&rvprop=ids%7Ctimestamp%7Cuser%7Cuserid%7Ccomment%7Ctags%7Csize"
       "&format=json&formatversion=2")
data = curl_json(url)
bank("rev_7226106.json", url, data)
pages = (data or {}).get("query", {}).get("pages", [])
for p in pages:
    for r in p.get("revisions", []) or []:
        print(f"7226106: user={r.get('user')} ts={r.get('timestamp')} comment={r.get('comment')!r} size={r.get('size')}")

# 2. usercontribs
summary = {}
for host, user in TARGETS:
    u = urllib.parse.quote(user, safe="")
    url = (f"https://{host}/w/api.php?action=query&list=usercontribs&ucuser={u}"
           f"&ucprop=ids%7Ctitle%7Ctimestamp%7Ccomment%7Csize%7Cflags&uclimit=500"
           f"&ucdir=older&format=json&formatversion=2")
    data = curl_json(url)
    bank(f"uc_{host.replace('.', '_')}_{user.replace('~','t').replace('-','_')}.json", url, data)
    contribs = (data or {}).get("query", {}).get("usercontribs", [])
    summary[(host, user)] = len(contribs)
    # print only edits NOT already in the 54 (revids unknown here; print non-sandbox or odd-comment ones)
    extra = [c for c in contribs if "sandbox" not in (c.get("title") or "").lower()]
    print(f"{host} {user}: {len(contribs)} total contribs; {len(extra)} non-sandbox", flush=True)
    for c in extra[:10]:
        print(f"   {c.get('revid')} {c.get('timestamp')} {c.get('title')} comment={c.get('comment')!r}")

with open(os.path.join(BASE, "workers/wikipedia-lane/pattern-hunter/uc_summary.json"), "w") as f:
    json.dump({f"{h} {u}": n for (h, u), n in summary.items()}, f, indent=1)
