#!/usr/bin/env python3
"""Live monitor v3: keyless htmx endpoint (separate rate limit from authed API).

Tracks the Amap fleet + museum task family until ~07:00 UTC 2026-10-05.
Gentle pacing: 90s between calls.
"""
import json, time, subprocess, re, os
from datetime import datetime, timezone

UQ = ["python3", os.path.expanduser("~/workspace/skills/urlquery/bin/uq_htmx.py")]
DIR = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/live-monitor")
SEEN_F = os.path.join(DIR, "seen.json")
LOG_F = os.path.join(DIR, "LOG.md")
KNOWN_HOSTS_F = os.path.join(DIR, "known_hosts.json")
KNOWN_TAGS_F = os.path.join(DIR, "known_tagstyles.json")
TAGWORDS_F = os.path.join(DIR, "tag_words.json")
FAMILIES_F = os.path.join(DIR, "task_families.json")

GAP = 90                      # seconds between htmx calls
POLL_INTERVAL = 30 * 60       # 30 min between polls
END_TS = datetime(2026, 10, 5, 7, 0, tzinfo=timezone.utc).timestamp()

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def search(query, limit=30, retries=3):
    wait = 120
    for _ in range(retries):
        try:
            out = subprocess.run(UQ + ["search", "--query", query, "--limit", str(limit)],
                                 capture_output=True, text=True, timeout=180)
        except subprocess.TimeoutExpired:
            time.sleep(wait); wait *= 2; continue
        body = out.stdout.strip()
        if "429" in body or "too many" in body.lower() or "429" in out.stderr:
            time.sleep(wait); wait *= 2; continue
        try:
            d = json.loads(body)
            if isinstance(d, dict) and "reports" in d:
                return d, None
            return None, f"unexpected payload: {body[:150]}"
        except Exception as e:
            time.sleep(wait); wait *= 2
    return None, "gave up after retries"

def tag_word(url):
    """Leading word of uqscan/uqtag value, e.g. qingdaomuseum from qingdaomuseum20261005b."""
    import urllib.parse
    u = urllib.parse.unquote(url)  # catch %26-encoded params
    m = re.search(r'[?&](uqscan|uqtag|uqm|uqattempt)=([^&]*)', u)
    if not m: return None, None
    v = m.group(2)
    w = re.split(r'[-_0-9]', v, 1)[0] or v
    return w.lower(), v

def family_of(url, word):
    if not word: return "untagged"
    if "museum" in word: return "museum"
    if "mobile" in (word or "") or "m.amap.com" in url: return "mobile"
    return "place"

def host_of(url):
    m = re.search(r'https?://([^/]+)', url)
    return m.group(1).lower() if m else "?"

def load(p, d):
    try: return json.load(open(p))
    except: return d

def main():
    seen = set(load(SEEN_F, []))
    known_hosts = set(load(KNOWN_HOSTS_F, []))
    known_tags = set(load(KNOWN_TAGS_F, []))
    tag_words = load(TAGWORDS_F, {})
    families = load(FAMILIES_F, {})
    log = open(LOG_F, "a")
    log.write(f"\n--- monitor v3: htmx endpoint ({now()}); tracking museum task family; 30min polls ---\n")
    log.flush()
    poll = 1
    new_total = 0
    while True:
        ts = now()
        fresh = []
        ok = True
        # main fleet query every poll; museum pivots every poll too (cheap, one call each)
        queries = ["url.domain:amap.com", "henanmuseum", "qingdaomuseum", "wenzhou-museum"]
        for qi, q in enumerate(queries):
            d, err = search(q, limit=30 if qi == 0 else 15)
            if d is None:
                ok = False
                log.write(f"\n### Poll H{poll} ({ts}) — {q} ERROR: {err}\n"); log.flush()
            else:
                for r in d["reports"]:
                    rid = r.get("report_id")
                    if not rid or rid in seen: continue
                    seen.add(rid)
                    u = r.get("url", {})
                    url = u.get("addr", "") if isinstance(u, dict) else str(u)
                    w, fulltag = tag_word(url)
                    fam = family_of(url, w)
                    hosts = {host_of(url)}
                    new_hosts = {h for h in hosts if h not in known_hosts}
                    new_word = bool(w and w not in tag_words)
                    if w:
                        tag_words[w] = tag_words.get(w, 0) + 1
                    families[fam] = families.get(fam, 0) + 1
                    fresh.append({"id": str(rid)[:8], "date": r.get("date"), "url": url[:130],
                                  "word": w, "new_word": new_word, "fam": fam,
                                  "new_hosts": sorted(new_hosts)})
                    known_hosts |= hosts
                # note: htmx sorts newest-first, no total_hits field
            if qi < len(queries) - 1:
                time.sleep(GAP)
        new_total += len(fresh)
        log.write(f"\n### Poll H{poll} ({ts}) — htmx\n")
        log.write(f"- new reports: {len(fresh)}" + ("" if ok else " (SOME QUERIES ERRORED)") + "\n")
        for f in fresh:
            flags = []
            if f["new_hosts"]: flags.append("NEW-HOST:" + ",".join(f["new_hosts"]))
            if f["new_word"]: flags.append("NEW-TAGWORD:" + str(f["word"]))
            log.write(f"  - {f['id']} {f['date']} [{f['fam']}] {f['url']} {' '.join(flags)}\n".rstrip() + "\n")
        if fresh:
            words = sorted({f["word"] for f in fresh if f["word"]})
            log.write(f"- tag words this poll: {', '.join(words)}\n")
        log.flush()
        json.dump(sorted(seen), open(SEEN_F, "w"))
        json.dump(sorted(known_hosts), open(KNOWN_HOSTS_F, "w"))
        json.dump(sorted(known_tags), open(KNOWN_TAGS_F, "w"))
        json.dump(tag_words, open(TAGWORDS_F, "w"), indent=1)
        json.dump(families, open(FAMILIES_F, "w"), indent=1)
        poll += 1
        if time.time() + POLL_INTERVAL >= END_TS:
            break
        time.sleep(POLL_INTERVAL)
    log.write(f"\n## Monitor v3 complete ({now()})\n")
    log.write(f"- new reports this run: {new_total}\n")
    log.write(f"- tag words seen: {json.dumps(tag_words)}\n")
    log.write(f"- task families: {json.dumps(families)}\n")
    log.close()
    print(f"done, {new_total} new reports")

if __name__ == "__main__":
    main()
