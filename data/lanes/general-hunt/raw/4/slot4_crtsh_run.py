#!/usr/bin/env python3
"""Slot-4 one-off: crt.sh certs issued in last 7 days for Tier-1/Tier-5 domains.
Passive GET against public crt.sh CT index. 10s delay between queries;
aborts on 429 (hard stop per policy)."""
import datetime, json, os, sys, time, urllib.error, urllib.parse, urllib.request

DOMAINS = [
    "messageboardforaiagents.com", "agentgateway.pythonanywhere.com",
    "agentsboard.org", "agents-agents-agents.com", "bboard.ai",
    "swarm.termina.digital", "swarmmemo.com", "tantive.space",
    "thecolony.ai", "aiforum.grok.me", "moltbook.com",
    "agentcolony.one", "swarmsay.com", "msgboard.dev",
    "commons.dooza.ai", "bulletin.zaindharper.workers.dev",
    "robots.wiki", "agenthaven.org",
    "agent-message-board.kyle-hatcher.workers.dev",
    "she-llac.com", "facehuggers.chain-of-thought.org",
    "ai.algo.pw", "nullyard.net", "getunstuck.space",
    "rel-ochre.vercel.app", "jotspot.io",
    "artifactcouncil.com", "joinsnail.com",
    "agentsspeakup.com", "agenttavern.dev",
]

UA = "Mozilla/5.0 (X11; Linux x86_64) silent-locus-slot4-crtsh"

def query(pattern):
    params = urllib.parse.urlencode({"q": pattern, "output": "json", "exclude": "expired"})
    req = urllib.request.Request("https://crt.sh/?" + params, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, (json.loads(body) if body.strip() else [])
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise SystemExit("429 RATE LIMIT: hard stop")
        return e.code, None
    except Exception as e:
        return -1, None

def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(days=7)
    results = {}
    meta = {"skipped": [], "retried_ok": [], "errors": []}
    for d in DOMAINS:
        status, rows = query("%." + d)
        if rows is None:
            meta["errors"].append(f"{d}: http {status}")
            results[d] = []
        else:
            new = [r for r in rows
                   if (r.get("entry_timestamp") or r.get("not_before") or "") >= cutoff.isoformat()]
            results[d] = new
        time.sleep(10)
    out = {"fetched_at": now.isoformat(), "cutoff": cutoff.isoformat(),
           "query_pattern": "%.<domain>", "results": results, "meta": meta}
    outdir = os.environ.get("OUTDIR", "/tmp")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "crtsh_slot4.json"), "w") as f:
        json.dump(out, f, indent=1)
    total = sum(len(v) for v in results.values())
    print(f"done: {total} new certs across {len(DOMAINS)} domains")
    for d, rows in results.items():
        for r in rows:
            print(" NEW", d, r.get("serial"), r.get("not_before"), (r.get("name_value") or "")[:80])

if __name__ == "__main__":
    main()
