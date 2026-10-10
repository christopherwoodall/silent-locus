#!/usr/bin/env python3
"""Resumed live monitor: gentle pacing, 429 backoff, runs until ~07:00 UTC 2026-10-05."""
import json, time, subprocess, re, os
from datetime import datetime, timezone

UQ = ["python3", os.path.expanduser("~/workspace/skills/urlquery/bin/uq.py")]
DIR = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/live-monitor")
SEEN_F = os.path.join(DIR, "seen.json")
LOG_F = os.path.join(DIR, "LOG.md")
KNOWN_HOSTS_F = os.path.join(DIR, "known_hosts.json")
KNOWN_TAGS_F = os.path.join(DIR, "known_tagstyles.json")

INTERVAL = 40 * 60        # 40 min between polls
GAP = 75                  # 75s between the two search calls
END_TS = datetime(2026, 10, 5, 7, 0, tzinfo=timezone.utc).timestamp()
POLL_START = 5  # poll 4 hit silent 429s; fixed error-payload detection, resuming at 5

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def search(query, limit=30, retries=4):
    wait = 180  # 3 min, doubling — quota is tight, other lanes are also polling
    for attempt in range(retries):
        out = subprocess.run(UQ + ["search", "--query", query, "--limit", str(limit)],
                             capture_output=True, text=True, timeout=180)
        body = out.stdout.strip()
        err = out.stderr[:300]
        # detect rate-limit in body OR stderr, regardless of return code
        blob = body + " " + err
        if "429" in blob or "too many requests" in blob.lower():
            time.sleep(wait); wait *= 2
            continue
        if out.returncode == 0 and body:
            try:
                d = json.loads(body)
            except Exception as e:
                return None, f"parse error: {e}"
            if isinstance(d, dict) and d.get("error"):
                return None, f"api error: {str(d['error'])[:200]}"
            return d, None
        return None, err or f"rc={out.returncode}"
    return None, f"gave up after {retries} retries (429/backoff)"

def tag_style(url):
    m = re.search(r'[?&](uqscan|uqtag|uq|uqtarget|uqhost)=([^&]*)', url)
    if not m: return None
    v = m.group(2)
    style = re.sub(r'\d+', '#', v)
    return (m.group(1), style, v)

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
    known_hosts |= {"amap-pc-ssr.amap.com","www.amap.com","m.amap.com","gaode.com","www.gaode.com",
                    "ditu.gaode.com","r.jina.ai","api.microlink.io","href.li","httpbingo.com",
                    "translate.goog","webhook.site","httpbin.org","httpbun.com","livecodes.io"}
    log = open(LOG_F, "a")
    log.write(f"\n--- monitor resumed ({now()}), gentle pacing (40min polls, 75s gaps, 429 backoff) ---\n")
    log.flush()
    i = POLL_START
    new_total = 0
    first_totals = {}
    while True:
        ts = now()
        fresh = []
        totals = {}
        api_ok = True
        qs = ["url.domain:amap.com", "url.domain:gaode.com"]
        for qi, q in enumerate(qs):
            d, err = search(q)
            if d is None:
                api_ok = False
                log.write(f"\n### Poll {i} ({ts}) — {q} API ERROR: {err}\n"); log.flush()
            else:
                totals[q] = d.get("total_hits")
                for r in d.get("reports", []):
                    rid = r.get("report_id")
                    if rid in seen: continue
                    seen.add(rid)
                    url = r.get("url", {}).get("addr", "")
                    fin = r.get("final", {}).get("addr", "") if isinstance(r.get("final"), dict) else ""
                    hosts = {host_of(url)}
                    if fin: hosts.add(host_of(fin))
                    new_hosts = {h for h in hosts if h not in known_hosts}
                    t = tag_style(url)
                    new_tag = bool(t and t[1] not in known_tags)
                    fresh.append({"id": rid[:8], "date": r.get("date"), "url": url[:140],
                                  "new_hosts": sorted(new_hosts), "tag": t[2] if t else None,
                                  "new_tag": new_tag})
                    known_hosts |= hosts
                    if t: known_tags.add(t[1])
            if qi < len(qs) - 1:
                time.sleep(GAP)
        if not first_totals:
            first_totals = totals
        new_total += len(fresh)
        log.write(f"\n### Poll {i} ({ts})\n")
        if not api_ok:
            log.write(f"- totals: amap={totals.get('url.domain:amap.com','?')} gaode={totals.get('url.domain:gaode.com','?')} | API ERRORS — counts unreliable\n")
        else:
            log.write(f"- totals: amap={totals.get('url.domain:amap.com','?')} gaode={totals.get('url.domain:gaode.com','?')} | new reports: {len(fresh)}\n")
        for f in fresh:
            flags = []
            if f["new_hosts"]: flags.append("NEW-HOST:" + ",".join(f["new_hosts"]))
            if f["new_tag"]: flags.append("NEW-TAG:" + str(f["tag"]))
            log.write(f"  - {f['id']} {f['date']} {f['url']} {' '.join(flags)}\n".rstrip() + "\n")
        log.flush()
        json.dump(sorted(seen), open(SEEN_F, "w"))
        json.dump(sorted(known_hosts), open(KNOWN_HOSTS_F, "w"))
        json.dump(sorted(known_tags), open(KNOWN_TAGS_F, "w"))
        i += 1
        # stop at 07:00 UTC (with a little slack for the final sleep)
        if time.time() + INTERVAL >= END_TS:
            break
        time.sleep(INTERVAL)
    log.write(f"\n## Monitor complete ({now()})\n")
    log.write(f"- new reports this resumed run: {new_total}\n")
    log.write(f"- totals first poll: {first_totals}, last poll: {totals}\n")
    log.write(f"- known hosts now: {len(known_hosts)}, known tag styles: {len(known_tags)}\n")
    log.close()
    print(f"done, {new_total} new reports")

if __name__ == "__main__":
    main()
