#!/usr/bin/env python3
"""PATTERN-HUNTER phase 3c: revision histories of incident sandbox pages in
incident windows. Looks for same-shape edits from OTHER accounts. curl, 5.5s.
Grade: OBSERVED."""
import json, os, subprocess, sys, time, urllib.parse

BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents")
RAW = os.path.join(BASE, "workers/wikipedia-lane/pattern-hunter/raw")
UA = "silent-locus-pattern-hunter/1.0 (OSINT research; mailto:research@example.org)"
PACE = 5.5

# (host, title, rvstart, rvend)
TARGETS = [
    ("en.wikipedia.org", "Wikipedia:Sandbox", "2026-05-10T22:30:00Z", "2026-05-10T15:00:00Z"),
    ("en.wikipedia.org", "Wikipedia:Sandbox", "2026-05-27T18:00:00Z", "2026-05-27T00:00:00Z"),
    ("en.wikipedia.org", "User:Example/sandbox", "2026-05-10T18:00:00Z", "2026-05-10T15:00:00Z"),
    ("en.wikipedia.org", "User:Sandbox", "2026-05-10T18:00:00Z", "2026-05-10T16:00:00Z"),
    ("test.wikipedia.org", "Wikipedia:Sandbox", "2026-05-10T19:00:00Z", "2026-05-10T16:00:00Z"),
    ("test.wikipedia.org", "Wikipedia:Sandbox", "2026-05-25T19:00:00Z", "2026-05-25T17:00:00Z"),
    ("test.wikipedia.org", "Wikipedia:Sandbox", "2026-06-18T04:00:00Z", "2026-06-18T01:00:00Z"),
    ("test.wikipedia.org", "Sandbox", "2026-05-27T05:00:00Z", "2026-05-27T02:00:00Z"),
    ("test2.wikipedia.org", "Wikipedia:Sandbox", "2026-05-10T18:00:00Z", "2026-05-10T16:00:00Z"),
    ("test2.wikipedia.org", "Sandbox", "2026-05-27T04:00:00Z", "2026-05-27T02:00:00Z"),
    ("www.mediawiki.org", "Project:Sandbox", "2026-05-10T18:00:00Z", "2026-05-10T16:00:00Z"),
    ("commons.wikimedia.org", "Commons:Sandbox", "2026-05-13T22:30:00Z", "2026-05-13T17:00:00Z"),
    ("commons.wikimedia.org", "Commons:Sandbox", "2026-06-18T21:30:00Z", "2026-06-18T19:00:00Z"),
    ("commons.wikimedia.org", "Commons:Sandbox", "2026-06-25T21:00:00Z", "2026-06-25T19:00:00Z"),
    ("incubator.wikimedia.org", "Incubator:Sandbox", "2026-06-25T21:00:00Z", "2026-06-25T19:00:00Z"),
    ("meta.wikimedia.org", "Meta:Sandbox", "2026-06-25T21:00:00Z", "2026-06-25T19:00:00Z"),
    ("simple.wikipedia.org", "Wikipedia:Sandbox", "2026-06-18T04:00:00Z", "2026-06-18T01:00:00Z"),
    ("bg.wikipedia.org", "Уикипедия:Пясъчник", "2026-05-27T03:00:00Z", "2026-05-27T00:00:00Z"),
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

KNOWN_IDS = {1353490694, 1353490935, 1353491551, 1353492663, 1353498400, 1353501383,
    1353507315, 1353518652, 1353543060, 1356314507, 1356419247, 741398, 741399, 741400,
    741405, 741406, 741409, 744268, 744270, 744271, 744272, 744412, 744414, 747327,
    612931, 612932, 612933, 613856, 8370989, 8370994, 8370995, 8370996,
    1213399057, 1213503714, 1213503789, 1213513506, 1233683454, 1238390511,
    7226103, 7226104, 7226105, 7226107, 7226108, 7226109, 7226110, 7226111,
    30732655, 10891416, 12923296}

OTHER_ACCOUNTS = []  # (host, title, revid, user, ts, comment, size)
for host, title, start, end in TARGETS:
    t = urllib.parse.quote(title, safe="")
    url = (f"https://{host}/w/api.php?action=query&prop=revisions&titles={t}"
           f"&rvprop=ids%7Ctimestamp%7Cuser%7Cuserid%7Ccomment%7Ctags%7Csize"
           f"&rvlimit=500&rvstart={start}&rvend={end}&rvdir=older"
           f"&format=json&formatversion=2")
    data = curl_json(url)
    fname = f"hist_{host.replace('.', '_')}_{title.replace(':','_').replace('/','_')}_{start[:10]}.json"
    with open(os.path.join(RAW, fname), "w") as f:
        json.dump({"provenance": {"source_url": url, "retrieved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, "response": data}, f, indent=1)
    revs = []
    for p in (data or {}).get("query", {}).get("pages", []):
        revs = p.get("revisions", []) or []
    new = [r for r in revs if r.get("revid") not in KNOWN_IDS]
    print(f"{host} {title} {start[:10]}: {len(revs)} revs in window, {len(new)} NOT in CSV set", flush=True)
    for r in new:
        OTHER_ACCOUNTS.append((host, title, r.get("revid"), r.get("user"), r.get("timestamp"),
                               r.get("comment"), r.get("size"), "|".join(r.get("tags") or [])))

with open(os.path.join(BASE, "workers/wikipedia-lane/pattern-hunter/other_sandbox_revs.json"), "w") as f:
    json.dump([{"host": h, "title": t, "revid": rid, "user": u, "timestamp": ts,
                "comment": c, "size": s, "tags": tg}
               for h, t, rid, u, ts, c, s, tg in OTHER_ACCOUNTS], f, indent=1)
print(f"OTHER-ACCOUNT revs banked: {len(OTHER_ACCOUNTS)}")
