#!/bin/bash
# Live monitor for the Chinese Amap agent-fleet hunt (keyless htmx endpoint).
# 30-minute polls, appends to LOG.md, tracks new tag words / task families.
#
# DESIGN (2026-10-05, after two monitor-agent deaths): THIS bash loop owns the
# schedule; each poll runs in a SHORT-LIVED python3 child. A hung, crashed, or
# truncation-killed poll can never take the loop down. Launch fully detached:
#   setsid nohup bash monitor_loop.sh >/dev/null 2>&1 < /dev/null & disown
# Kill stale instances first: pgrep -f monitor_loop / pgrep -f 'monitor[0-9]\.py'

DIR="/home/hatch/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/live-monitor"
POLL_EVERY=1800   # 30 min between polls
POLL_BUDGET=1500  # hard cap on one poll so the loop can never stall
GAP=7             # polite pacing between queries (s)

cd "$DIR" || exit 1

while true; do
  timeout "$POLL_BUDGET" python3 - "$DIR" <<'PYEOF'
import json, time, subprocess, re, os, sys
from datetime import datetime, timezone

DIR = sys.argv[1]
UQ = [sys.executable, os.path.expanduser("~/workspace/skills/urlquery/bin/uq_htmx.py")]
SEEN_F      = os.path.join(DIR, "seen.json")
LOG_F       = os.path.join(DIR, "LOG.md")
KNOWN_HOSTS_F = os.path.join(DIR, "known_hosts.json")
TAGWORDS_F  = os.path.join(DIR, "tag_words.json")
FAMILIES_F  = os.path.join(DIR, "task_families.json")
GAP = 7

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def query(q, limit=30, retries=3):
    """One uq_htmx query; NEVER raises. Returns (dict|None, err|None).
    Egress proxy truncates mid-response -> IncompleteRead/partial JSON, so every
    attempt is wrapped in `timeout 120` and retried with backoff."""
    wait = 15
    last = None
    for attempt in range(retries):
        try:
            p = subprocess.run(UQ + ["search", "--query", q, "--limit", str(limit)],
                               capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            last = "timeout 120s"
        except Exception as e:
            last = "spawn failed: %s" % e
        else:
            body = (p.stdout or "").strip()
            if p.returncode != 0 and not body:
                last = "rc=%s stderr=%s" % (p.returncode, (p.stderr or "").strip()[:120])
            else:
                try:
                    d = json.loads(body)
                    if isinstance(d, dict) and "reports" in d:
                        return d, None
                    last = "unexpected payload head: %s" % body[:120]
                except Exception as e:
                    last = "JSON parse failed (%s); truncated body (len %d)" % (e, len(body))
        if attempt < retries - 1:
            time.sleep(wait); wait *= 2
    return None, "QUERY %s ERROR: gave up after %d retries — %s" % (q, retries, last)

def tag_word(url):
    import urllib.parse
    u = urllib.parse.unquote(url or "")
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
    m = re.search(r'https?://([^/]+)', url or "")
    return m.group(1).lower() if m else "?"

def load(p, d):
    try: return json.load(open(p))
    except Exception: return d

def next_poll_n():
    try:
        ns = [int(x) for x in re.findall(r'Poll H(\d+)', open(LOG_F).read())]
        return max(ns) + 1 if ns else 3
    except Exception:
        return 3

seen = set(load(SEEN_F, []))
known_hosts = set(load(KNOWN_HOSTS_F, []))
tag_words = load(TAGWORDS_F, {})
families = load(FAMILIES_F, {})
poll = next_poll_n()
ts = now()
fresh, errs = [], []

queries = [("url.domain:amap.com", 30), ("henanmuseum", 15),
           ("qingdaomuseum", 15), ("wenzhou-museum", 15)]
for qi, (q, lim) in enumerate(queries):
    d, err = query(q, limit=lim)
    if d is None:
        errs.append(err)          # one failing query never kills the poll
    else:
        for r in d.get("reports", []):
            rid = r.get("report_id")
            if not rid or rid in seen: continue
            seen.add(rid)
            u = r.get("url", {})
            url = u.get("addr", "") if isinstance(u, dict) else str(u)
            w, fulltag = tag_word(url)
            fam = family_of(url, w)
            h = host_of(url)
            new_hosts = [h] if h not in known_hosts else []
            new_word = bool(w and w not in tag_words)
            if w: tag_words[w] = tag_words.get(w, 0) + 1
            families[fam] = families.get(fam, 0) + 1
            fresh.append((str(rid)[:8], r.get("date"), fam, url[:130], new_hosts, new_word, w))
            known_hosts.add(h)
    if qi < len(queries) - 1:
        time.sleep(GAP)

with open(LOG_F, "a") as log:
    log.write("\n### Poll H%d (%s) — htmx\n" % (poll, ts))
    for e in errs:
        log.write("- %s\n" % e)
    log.write("- new reports: %d%s\n" % (len(fresh), "" if not errs else " (SOME QUERIES ERRORED)"))
    for rid8, dt, fam, url, nh, nw, w in fresh:
        flags = []
        if nh: flags.append("NEW-HOST:" + ",".join(nh))
        if nw: flags.append("NEW-TAGWORD:" + str(w))
        log.write("  - %s %s [%s] %s%s\n" % (rid8, dt, fam, url, (" " + " ".join(flags)) if flags else ""))
    if fresh:
        words = sorted({w for *_, w in fresh if w})
        log.write("- tag words this poll: %s\n" % ", ".join(words))

json.dump(sorted(seen), open(SEEN_F, "w"))
json.dump(sorted(known_hosts), open(KNOWN_HOSTS_F, "w"))
json.dump(tag_words, open(TAGWORDS_F, "w"), indent=1)
json.dump(families, open(FAMILIES_F, "w"), indent=1)
print("poll H%d done, %d new, errors=%d" % (poll, len(fresh), len(errs)), flush=True)
PYEOF
  sleep "$POLL_EVERY"
done
