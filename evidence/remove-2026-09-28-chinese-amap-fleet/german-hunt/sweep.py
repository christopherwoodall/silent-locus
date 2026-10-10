#!/usr/bin/env python3
"""German follow-up sweep: agentness words, time blasts, cross-swarm vocab.
Incremental persistence, gentle pacing (20s between queries)."""
import json, subprocess, time
from collections import Counter

HERE = "/home/hatch/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/german-hunt"
UQ = ["python3", "/home/hatch/workspace/skills/urlquery/bin/uq.py", "search"]
STATE = HERE + "/sweep_state.json"
LOG = HERE + "/sweep.log"
DELAY = 20

def log(msg):
    with open(LOG, "a") as f:
        f.write(msg + "\n")
    print(msg, flush=True)

def load():
    try:
        return json.load(open(STATE))
    except Exception:
        return {}

def save(results):
    json.dump(results, open(STATE, "w"), indent=1)

def search(q, limit=50):
    try:
        out = subprocess.run(UQ + ["--query", q, "--limit", str(limit)],
                             capture_output=True, text=True, timeout=180)
        d = json.loads(out.stdout)
        if "error" in d:
            return None, d["error"]
        return d.get("total_hits", -1), d.get("reports") or []
    except Exception as e:
        return None, str(e)

def record(results, key, q, limit=50):
    if key in results and results[key].get("total_hits", -1) >= 0:
        log(f"{key}: already have")
        return
    for attempt in range(3):
        hits, reps = search(q, limit)
        if isinstance(reps, str) and "429" in reps:
            log(f"{key}: 429, waiting 90s (attempt {attempt+1})")
            time.sleep(90)
            continue
        break
    if hits is None:
        results[key] = {"query": q, "total_hits": -1, "error": str(reps)[:100]}
        save(results)
        log(f"{key}: FAILED {str(reps)[:60]}")
        time.sleep(DELAY)
        return
    dates = [r.get("date", "")[:13] for r in reps if r.get("date")]
    burst = Counter(dates).most_common(5)
    addrs = [(r.get("date", "")[:16], r.get("url", {}).get("addr", "")[:120])
             for r in reps[:10]]
    results[key] = {"query": q, "total_hits": hits, "sampled": len(reps),
                    "top_hours": burst, "sample": addrs}
    save(results)
    log(f"{key}: hits={hits} top_hours={burst[:3]}")
    time.sleep(DELAY)

QUERIES = []
words = ["agent", "suche", "analyse", "daten", "extraktion", "sammlung",
         "roboter", "automatisch", "aufgabe", "mission", "ergebnis",
         "standort", "abfrage"]
for w in words:
    QUERIES.append((f"httpbin_{w}", f"httpbin {w}", 50))
for w in ["agent", "aufgabe", "ergebnis", "standort", "abfrage", "suche"]:
    QUERIES.append((f"httpbun_{w}", f"httpbun {w}", 50))
for w in ["agent", "aufgabe", "ergebnis"]:
    QUERIES.append((f"webhook_{w}", f"webhook.site {w}", 50))
for city in ["berlin", "muenchen", "hamburg", "koeln", "frankfurt"]:
    QUERIES.append((f"httpbun_city_{city}", f"httpbun {city}", 50))
for w in ["agent", "aufgabe", "standort"]:
    QUERIES.append((f"b64_{w}", f"base64 {w}", 50))
for d in ["kleinanzeigen.de", "check24.de", "spiegel.de", "tagesschau.de",
          "deepl.com", "t1p.de", "linkvertise.com", "pastebin.de",
          "here.com", "tomtom.com", "outdooractive.com", "meinestadt.de",
          "immobilienscout24.de", "lieferando.de", "11880.com", "bahn.de",
          "openrouteservice.org"]:
    QUERIES.append((f"burst_{d}", f"url.domain:{d}", 100))
QUERIES += [
    ("xs_uqscan_de", "uqscan berlin", 50),
    ("xs_uqscan_de2", "uqscan deutschland", 50),
    ("xs_uqtag_de", "uqtag berlin", 50),
    ("xs_claude_httpbin_de", "claude httpbin berlin", 50),
    ("xs_claude_httpbun_de", "claude httpbun", 50),
    ("xs_ltzh_de", "ltzh berlin", 50),
    ("xs_zz_2026", "zz=oai", 50),
    ("xs_research_de", "research berlin httpbun", 50),
    ("xs_subpoinavi_de", "sub_poi_navi berlin", 50),
]

def main():
    results = load()
    log(f"resuming with {len(results)} done, {len(QUERIES)} total queries")
    for key, q, limit in QUERIES:
        record(results, key, q, limit)
    log(f"DONE {len(results)}")

if __name__ == "__main__":
    main()
