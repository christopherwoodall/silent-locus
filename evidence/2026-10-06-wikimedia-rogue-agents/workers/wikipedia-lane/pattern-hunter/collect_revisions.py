#!/usr/bin/env python3
"""PATTERN-HUNTER phase 1: pull revision metadata + content for the 54 CSV diff URLs.
Uses curl (egress-proxy-safe), paced >=5s between requests. Raw JSON banked in raw/.
Grade: OBSERVED.
"""
import json, os, subprocess, sys, time, urllib.parse

BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents")
RAW = os.path.join(BASE, "workers/wikipedia-lane/pattern-hunter/raw")
CSV = os.path.join(BASE, "raw/openai-wikimedia-edits-2026-10-04.csv")
PACE = 5.5
UA = "silent-locus-pattern-hunter/1.0 (OSINT research; mailto:research@example.org)"

os.makedirs(RAW, exist_ok=True)

def curl_json(url):
    time.sleep(PACE)
    out = subprocess.run(
        ["curl", "-sS", "--max-time", "60", "-A", UA, url],
        capture_output=True, text=True)
    if out.returncode != 0:
        print(f"CURL FAIL {url}: {out.stderr.strip()}", file=sys.stderr)
        return None
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        print(f"JSON FAIL {url}: {out.stdout[:200]}", file=sys.stderr)
        return None

# Parse CSV: host, title (may be absent), oldid
jobs = []  # (host, title_or_None, oldid)
with open(CSV) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        u = urllib.parse.urlparse(line)
        q = urllib.parse.parse_qs(u.query)
        host = u.netloc
        oldid = q.get("oldid", [None])[0] or q.get("diff", [None])[0]
        title = q.get("title", [None])[0]
        jobs.append((host, title, oldid))
        if oldid is None:
            print(f"PARSE WARN (no revid): {line}", file=sys.stderr)

print(f"parsed {len(jobs)} jobs")

# Group by host, batch <=50 revids per request
from collections import defaultdict
groups = defaultdict(list)
for host, title, oldid in jobs:
    groups[host].append((title, oldid))

all_pages = {}  # (host, revid) -> revision dict
for host, items in groups.items():
    for i in range(0, len(items), 50):
        batch = items[i:i+50]
        revids = "|".join(r for _, r in batch if r)
        if not revids:
            continue
        url = (f"https://{host}/w/api.php?action=query&prop=revisions"
               f"&revids={urllib.parse.quote(revids)}"
               f"&rvprop=ids%7Ctimestamp%7Cuser%7Cuserid%7Ccomment%7Ctags%7Csize%7Csha1%7Ccontent%7Cflags"
               f"&rvslots=main&format=json&formatversion=2")
        data = curl_json(url)
        raw_path = os.path.join(RAW, f"revisions_{host.replace('.', '_')}_batch{i//50}.json")
        with open(raw_path, "w") as f:
            json.dump({"provenance": {"source_url": url, "retrieved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "method": "curl", "script": "collect_revisions.py"}, "response": data}, f, indent=1)
        if not data or "query" not in data:
            print(f"NO DATA {host} batch {i//50}", file=sys.stderr)
            continue
        for page in data["query"].get("pages", []):
            for rev in page.get("revisions", []) or []:
                all_pages[(host, str(rev.get("revid")))] = {
                    "page_title": page.get("title"), "pageid": page.get("pageid"),
                    "missing": page.get("missing", False), "invalidreason": page.get("invalidreason"),
                    "rev": rev,
                }
        print(f"{host}: batch {i//50} -> {len(data['query'].get('pages', []))} pages", flush=True)

# Badrevids = nonexistent
# Write TSV
tsv = os.path.join(BASE, "workers/wikipedia-lane/pattern-hunter/revisions.tsv")
with open(tsv, "w") as f:
    f.write("host\trevid\tpage_title\tpageid\tuser\tuserid\ttimestamp\tcomment\ttags\tsize\tsha1\tminor\n")
    for (host, revid), rec in sorted(all_pages.items()):
        r = rec["rev"]
        f.write("\t".join(str(x if x is not None else "") for x in [
            host, r.get("revid"), rec["page_title"], rec["pageid"],
            r.get("user"), r.get("userid"), r.get("timestamp"),
            (r.get("comment") or "").replace("\t", " ").replace("\n", " "),
            "|".join(r.get("tags") or []), r.get("size"), r.get("sha1"),
            "1" if r.get("minor") else "",
        ]) + "\n")
# Content dump
diffs = os.path.join(BASE, "workers/wikipedia-lane/pattern-hunter/diffs")
os.makedirs(diffs, exist_ok=True)
for (host, revid), rec in all_pages.items():
    slot = (rec["rev"].get("slots") or {}).get("main") or {}
    content = slot.get("content")
    if content is not None:
        fn = f"{host.replace('.', '_')}_{revid}.txt"
        with open(os.path.join(diffs, fn), "w") as f:
            f.write(content)

print(f"revisions collected: {len(all_pages)} -> {tsv}, content files: {len(os.listdir(diffs))}")
# Report requested-but-missing revids
got = {r for _, r in all_pages.keys()}
for host, items in groups.items():
    for title, oldid in items:
        if oldid and oldid not in got:
            print(f"MISSING revid {oldid} on {host} (title hint: {title})")
