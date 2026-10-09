#!/usr/bin/env python3
"""German follow-up: priority queries only, very gentle pacing."""
import json, subprocess, time
from collections import Counter

HERE = "/home/hatch/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/german-hunt"
UQ = ["python3", "/home/hatch/workspace/skills/urlquery/bin/uq.py", "search"]
STATE = HERE + "/sweep_state.json"
LOG = HERE + "/sweep.log"
DELAY = 45

def log(msg):
    with open(LOG, "a") as f:
        f.write(msg + "\n")
    print(msg, flush=True)

def load():
    try: return json.load(open(STATE))
    except Exception: return {}

def save(r): json.dump(r, open(STATE, "w"), indent=1)

def search(q, limit=50):
    try:
        out = subprocess.run(UQ + ["--query", q, "--limit", str(limit)],
                             capture_output=True, text=True, timeout=180)
        d = json.loads(out.stdout)
        if "error" in d: return None, d["error"]
        return d.get("total_hits", -1), d.get("reports") or []
    except Exception as e:
        return None, str(e)

PRIORITY = [
    ("httpbun_aufgabe", "httpbun aufgabe", 50),
    ("httpbun_agent", "httpbun agent", 50),
    ("webhook_aufgabe", "webhook.site aufgabe", 50),
    ("burst_linkvertise", "url.domain:linkvertise.com", 100),
    ("burst_deepl", "url.domain:deepl.com", 100),
    ("burst_kleinanzeigen", "url.domain:kleinanzeigen.de", 100),
    ("xs_uqscan_de", "uqscan berlin", 50),
    ("xs_uqtag_de", "uqtag berlin", 50),
    ("xs_claude_httpbun_de", "claude httpbun", 50),
    ("xs_ltzh_de", "ltzh berlin", 50),
    ("xs_zz_2026", "zz=oai", 50),
    ("xs_subpoinavi_de", "sub_poi_navi berlin", 50),
]

def main():
    results = load()
    log(f"priority run: {len(results)} have, {len(PRIORITY)} priority queries")
    for key, q, limit in PRIORITY:
        if key in results and results[key].get("total_hits", -1) >= 0:
            log(f"{key}: already have")
            continue
        hits, reps = search(q, limit)
        if hits is None:
            em = str(reps)[:80]
            log(f"{key}: FAILED {em}")
            results[key] = {"query": q, "total_hits": -1, "error": em}
            save(results)
            time.sleep(120)
            continue
        dates = [r.get("date", "")[:13] for r in reps if r.get("date")]
        burst = Counter(dates).most_common(5)
        addrs = [(r.get("date", "")[:16], r.get("url", {}).get("addr", "")[:120])
                 for r in reps[:10]]
        results[key] = {"query": q, "total_hits": hits, "sampled": len(reps),
                        "top_hours": burst, "sample": addrs}
        save(results)
        log(f"{key}: hits={hits} top_hours={burst[:3]}")
        time.sleep(DELAY)
    log("PRIORITY DONE")

if __name__ == "__main__":
    main()
