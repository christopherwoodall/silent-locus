#!/usr/bin/env python3
"""Live monitor: poll urlquery for Chinese Amap fleet activity every ~20 min for 6 hours."""
import json, time, subprocess, re, sys, os
from datetime import datetime, timezone

UQ = ["python3", os.path.expanduser("~/workspace/skills/urlquery/bin/uq.py")]
DIR = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/live-monitor")
SEEN_F = os.path.join(DIR, "seen.json")
LOG_F = os.path.join(DIR, "LOG.md")
KNOWN_HOSTS_F = os.path.join(DIR, "known_hosts.json")
KNOWN_TAGS_F = os.path.join(DIR, "known_tagstyles.json")

POLLS = 17          # ~17 more polls after baseline ≈ 6h
INTERVAL = 20 * 60  # seconds

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def search(query, limit=30):
    out = subprocess.run(UQ + ["search", "--query", query, "--limit", str(limit)],
                         capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        return None, out.stderr[:200]
    return json.loads(out.stdout), None

def tag_style(url):
    m = re.search(r'[?&](uqscan|uqtag)=([^&]*)', url)
    if not m: return None
    v = m.group(2)
    # generalize: replace digits with #, keep alpha skeleton
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
    # seed known infra from article + baseline
    known_hosts |= {"amap-pc-ssr.amap.com","www.amap.com","m.amap.com","gaode.com","www.gaode.com",
                    "ditu.gaode.com","r.jina.ai","api.microlink.io","href.li","httpbingo.com",
                    "translate.goog","webhook.site","httpbin.org","httpbun.com","livecodes.io"}
    log = open(LOG_F, "a")
    new_total = 0
    for i in range(1, POLLS + 1):
        ts = now()
        fresh = []
        totals = {}
        for q in ["url.domain:amap.com", "url.domain:gaode.com"]:
            d, err = search(q)
            if d is None:
                log.write(f"\n### Poll {i} ({ts}) — API ERROR: {err}\n"); log.flush()
                time.sleep(60); continue
            totals[q] = d.get("total_hits")
            for r in d.get("reports", []):
                rid = r.get("report_id")
                if rid in seen: continue
                seen.add(rid)
                url = r.get("url", {}).get("addr", "")
                fin = r.get("final", {}).get("url", {}).get("addr", "") if isinstance(r.get("final"), dict) else ""
                hosts = {host_of(url)}
                if fin: hosts.add(host_of(fin))
                new_hosts = {h for h in hosts if h not in known_hosts}
                t = tag_style(url)
                new_tag = False
                if t and t[1] not in known_tags:
                    new_tag = True
                fresh.append({"id": rid[:8], "date": r.get("date"), "url": url[:120],
                              "hosts": sorted(hosts), "new_hosts": sorted(new_hosts),
                              "tag": t[2] if t else None, "new_tag": new_tag})
                known_hosts |= hosts
                if t: known_tags.add(t[1])
        new_total += len(fresh)
        log.write(f"\n### Poll {i} ({ts})\n")
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
        if i < POLLS:
            time.sleep(INTERVAL)
    log.write(f"\n## Monitor complete ({now()}) — {new_total} new reports this run\n")
    log.close()
    print(f"done, {new_total} new reports")

if __name__ == "__main__":
    main()
