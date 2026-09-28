#!/usr/bin/env python3
"""LANE H — read-only surface captures for 11 agent-board surfaces.

Fetches agent-facing pages ONLY: homepage, llms.txt, /for-agents, robots.txt,
.well-known/agent.json (+ surface-specific agent docs where advertised).
NO logins, NO accounts, NO posts, NO API keys. ~1 request / 3s per host.
"""
import hashlib, json, os, time, urllib.error, urllib.request
from datetime import datetime, timezone

BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
OUT = BASE + "/data/agent-surfaces"
NOW = lambda: datetime.now(timezone.utc).isoformat()
PACING = 3.0
TIMEOUT = 40

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131 Safari/537.36"

# slug -> (base_url, extra_paths)
SURFACES = {
    "facehuggers": ("https://facehuggers.chain-of-thought.org",
                    ["/robots.txt", "/.well-known/agent.json", "/agents.md", "/skill.md", "/for-agents"]),
    "agentsboard": ("https://agentsboard.org",
                    ["/robots.txt", "/.well-known/agent-board", "/skill.md", "/webhooks.md", "/openapi.json"]),
    "messageboardforaiagents": ("https://messageboardforaiagents.com",
                    ["/robots.txt", "/.well-known/agent.json", "/skill.md", "/for-agents", "/agents.md"]),
    "agentgateway": ("https://agentgateway.pythonanywhere.com",
                    ["/robots.txt", "/.well-known/agent.json", "/skill.md", "/heartbeat.md", "/mcp.json", "/api/brief", "/feed.xml"]),
    "aiforum-grok": ("https://aiforum.grok.me",
                    ["/robots.txt", "/.well-known/agent.json", "/skill.md", "/for-agents", "/agents.md"]),
    "jotspot": ("https://jotspot.io",
                    ["/robots.txt", "/.well-known/agent.json", "/skill.md", "/for-agents", "/agents.md"]),
    "nullyard": ("https://nullyard.net",
                    ["/robots.txt", "/.well-known/agent.json", "/agents", "/skill.md", "/structured-threads.md", "/work.md", "/mcp.md", "/methods", "/feed.xml"]),
    "she-llac": ("https://she-llac.com",
                    ["/CROSS_SITE_CONNECTIONS.md", "/robots.txt", "/llms.txt", "/for-agents", "/.well-known/agent.json", "/agents.md"]),
    "pastebin-tarcseh": ("https://pastebin.tarcseh.me",
                    ["/robots.txt", "/.well-known/agent.json", "/skill.md", "/for-agents", "/agents.md"]),
    "nervesocket": ("https://nervesocket.com",
                    ["/robots.txt", "/.well-known/agent.json", "/skill.md", "/for-agents", "/agents.md"]),
    "bitily": ("https://bitily.in",
                    ["/robots.txt", "/.well-known/agent.json", "/skill.md", "/for-agents", "/agents.md"]),
}

COMMON = ["/", "/llms.txt", "/for-agents", "/robots.txt", "/.well-known/agent.json"]


def fetch(url):
    r = urllib.request.Request(url, headers={"User-Agent": UA,
                                             "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.5"})
    try:
        with urllib.request.urlopen(r, timeout=TIMEOUT) as resp:
            body = resp.read()
            return {"ok": True, "status": resp.status,
                    "content_type": resp.headers.get("Content-Type", ""),
                    "final_url": resp.geturl(), "body": body}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": "HTTPError: %s" % e.code,
                "final_url": url}
    except Exception as e:
        return {"ok": False, "status": None, "error": "%s: %s" % (type(e).__name__, str(e)[:200]),
                "final_url": url}


def log(sdir, msg):
    line = "%s %s" % (NOW(), msg)
    with open(sdir + "/progress.log", "a") as f:
        f.write(line + "\n")
    print(line, flush=True)


def capture(slug, base, extras):
    sdir = OUT + "/" + slug
    os.makedirs(sdir, exist_ok=True)
    log(sdir, "capture START base=%s" % base)
    paths = list(dict.fromkeys(COMMON + extras))  # de-dupe, preserve order
    pages, sha = [], {}
    last = 0.0
    for p in paths:
        url = base + p
        dt = time.time() - last
        if dt < PACING:
            time.sleep(PACING - dt)
        res = fetch(url)
        last = time.time()
        rec = {"url": url, "path": p, "retrieved_at_utc": NOW(),
               "http_status": res.get("status"), "final_url": res.get("final_url"),
               "content_type": res.get("content_type"), "ok": res["ok"]}
        if res["ok"]:
            body = res["body"]
            h = hashlib.sha256(body).hexdigest()
            rec.update({"sha256": h, "bytes": len(body)})
            fname = "pages%s" % (p.replace("/", "_") or "_root")
            fname = fname.replace("._", ".")[:80]
            if not fname.endswith((".txt", ".md", ".json", ".xml")):
                fname += ".txt" if "html" not in rec["content_type"] else ".html"
            # normalize names
            name_map = {"/": "homepage", "/llms.txt": "llms",
                        "/for-agents": "for-agents", "/robots.txt": "robots",
                        "/.well-known/agent.json": "well-known-agent"}
            nm = name_map.get(p, p.strip("/").replace("/", "_") or "root")
            ext = ".json" if p.endswith(".json") else (".xml" if p.endswith(".xml") else
                  (".md" if p.endswith(".md") else (".html" if "html" in rec["content_type"] else ".txt")))
            fname = nm + ext
            with open(sdir + "/" + fname, "wb") as f:
                f.write(body)
            rec["file"] = fname
            sha[fname] = h
        else:
            rec["error"] = res.get("error")
        pages.append(rec)
        log(sdir, "%s -> %s" % (p, rec["http_status"] if res["ok"] else rec.get("error")))
    with open(sdir + "/pages.json", "w") as f:
        json.dump(pages, f, indent=1)
    prov = []
    prov.append("# PROVENANCE: %s" % slug)
    prov.append("")
    prov.append("- base_url: %s" % base)
    prov.append("- captured_at_utc: %s" % NOW())
    prov.append("- method: read-only GET, ~3s pacing, public agent-facing pages only")
    prov.append("- no logins, no accounts, no posts, no API keys")
    prov.append("")
    prov.append("## Requests")
    for rec in pages:
        if rec["ok"]:
            prov.append("- %s [%s] %d bytes sha256:%s -> %s" % (
                rec["url"], rec["content_type"][:40], rec["bytes"], rec["sha256"][:16], rec["file"]))
        else:
            prov.append("- %s FAILED: %s" % (rec["url"], rec.get("error")))
    with open(sdir + "/PROVENANCE.md", "w") as f:
        f.write("\n".join(prov) + "\n")
    ok = sum(1 for r in pages if r["ok"])
    log(sdir, "capture DONE ok=%d/%d" % (ok, len(pages)))
    return pages


def main():
    os.makedirs(OUT, exist_ok=True)
    summary = {}
    for slug, (base, extras) in SURFACES.items():
        pages = capture(slug, base, extras)
        summary[slug] = {"base": base, "pages_ok": sum(1 for r in pages if r["ok"]),
                         "pages_total": len(pages)}
    with open(OUT + "/_capture_summary.json", "w") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
