#!/usr/bin/env python3
"""Lane 3 (re-hunt-relays): relay/infra scour — enumerate public fetch-relay,
web-archive and dead-drop surfaces agents could have used besides urlquery and
arquivo.pt; probe the publicly-queryable ones for incident fingerprints.

Idempotent: resumes from state.json; never re-runs completed probes, never
duplicates inventory rows or hits. Polite: <=1 req/2s per host, generous
timeouts, a block/rate-limit ends that probe (recorded, not retried).

Outputs (all under this dir):
  surface-inventory.jsonl  one row per surface
  probe-log.jsonl           every probe attempted (honest negatives included)
  data/hits.jsonl           annotated fingerprint hits (keep-all + annotate)
  state.json                lane state + watermarks
"""
import json
import os
import subprocess
import time
import datetime
import urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
STATE_F = os.path.join(BASE, "state.json")
INV_F = os.path.join(BASE, "surface-inventory.jsonl")
PROBELOG_F = os.path.join(BASE, "probe-log.jsonl")
HITS_F = os.path.join(DATA, "hits.jsonl")
os.makedirs(DATA, exist_ok=True)

UA = "silent-locus-lane3/1.0 (security-research probe; polite, <=1req/2s)"
NOW = lambda: datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------------------------------------------------------------- inventory
# publicly_queryable: can an unauthenticated client ask the service something
# public_logs: does it keep publicly-readable history usable as a hunt surface
SURFACES = [
 # --- web archives (public logs) ---
 {"surface": "web.archive.org (Wayback CDX)",
  "category": "archive",
  "publicly_queryable": True, "public_logs": True,
  "query_interface": "CDX search API https://web.archive.org/cdx/search/cdx (no auth); SPN submission auth status not verified in this lane",
  "probed": True,
  "findings": "CDX is the read path for any Save-Page-Now relay use; probed for agent param fingerprints in incident windows",
  "blocker": ""},
 {"surface": "archive.today (+mirrors archive.ph/.md/.li/.is)",
  "category": "archive",
  "publicly_queryable": True, "public_logs": True,
  "query_interface": "per-URL /newest/<url> lookup (no auth); search box backed by Google CustomSearch/Yandex; aggressive 429 rate-limiting; no structured index API",
  "probed": True,
  "findings": "newest-lookup probed; full enumeration not possible without scraping search results",
  "blocker": ""},
 {"surface": "perma.cc",
  "category": "archive",
  "publicly_queryable": True, "public_logs": True,
  "query_interface": "GET https://api.perma.cc/v1/public/archives/ (no auth per developer docs); creation requires account; Memento member",
  "probed": True,
  "findings": "public-archives endpoint probed for shape/auth requirement",
  "blocker": ""},
 {"surface": "Memento Time Travel (timetravel.mementoweb.org)",
  "category": "archive-aggregator",
  "publicly_queryable": True, "public_logs": True,
  "query_interface": "GET /api/json/<YYYYMMDDHHMMSS>/<url> federated memento lookup (no auth)",
  "probed": True,
  "findings": "federated lookup probed for incident URL/date",
  "blocker": ""},
 {"surface": "Common Crawl Index (index.commoncrawl.org)",
  "category": "archive",
  "publicly_queryable": True, "public_logs": True,
  "query_interface": "GET https://index.commoncrawl.org/<CC-MAIN-...>-index?url=... (no auth)",
  "probed": True,
  "findings": "batch monthly crawl, not a live relay; probed for agent-param URLs in June-2026 crawl",
  "blocker": ""},
 {"surface": "UK Web Archive (ukwa.org.uk)",
  "category": "archive",
  "publicly_queryable": True, "public_logs": True,
  "query_interface": "web search UI only; no scriptable public API found",
  "probed": False,
  "findings": "UI-only search, UK collection scope; low relay plausibility for US/CA gov targets; not probed",
  "blocker": "no scriptable query interface"},
 {"surface": "arquivo.pt",
  "category": "archive",
  "publicly_queryable": True, "public_logs": True,
  "query_interface": "CDX + versionHistory APIs",
  "probed": False,
  "findings": "covered by the arquivo-pt lane (589,972 captures adopted); out of this lane's scope",
  "blocker": "covered by sibling lane"},
 {"surface": "urlquery.net",
  "category": "scan-archive",
  "publicly_queryable": True, "public_logs": True,
  "query_interface": "report search UI/API",
  "probed": False,
  "findings": "known surface; out of this lane's scope (besides-urlquery brief)",
  "blocker": "out of scope"},
 # --- fetch relays (no public logs: unscourable by design) ---
 {"surface": "allorigins.win",
  "category": "relay",
  "publicly_queryable": True, "public_logs": False,
  "query_interface": "GET /get|/raw|/json|/info?url= (no auth); no history endpoint exists",
  "probed": True,
  "findings": "live relay confirmed; keeps no public logs — unscourable by design (operator-side logs are private)",
  "blocker": ""},
 {"surface": "corsproxy.io",
  "category": "relay",
  "publicly_queryable": True, "public_logs": False,
  "query_interface": "GET /?<url> (no auth); operator advertises 'No Logs'",
  "probed": True,
  "findings": "live relay confirmed; no public log interface — unscourable by design",
  "blocker": ""},
 {"surface": "whateverorigin.org",
  "category": "relay",
  "publicly_queryable": False, "public_logs": False,
  "query_interface": "none — service dead",
  "probed": False,
  "findings": "dead (multiple independent reports: 'died or dead slow'); was a JSONP CORS proxy",
  "blocker": "service dead"},
 {"surface": "translate.google.com (Translate proxy)",
  "category": "relay",
  "publicly_queryable": True, "public_logs": False,
  "query_interface": "translate.google.com/translate?u=<url> live fetch; no history/log interface",
  "probed": False,
  "findings": "pure fetch relay; nothing to query for past use — unscourable by design",
  "blocker": "no query interface exists"},
 {"surface": "r.jina.ai",
  "category": "relay",
  "publicly_queryable": False, "public_logs": False,
  "query_interface": "https://r.jina.ai/<url> — anonymous access dead (401/402 -> Turnstile); API key required",
  "probed": True,
  "findings": "keyed since ~2025; no public logs — unscourable by design",
  "blocker": ""},
 {"surface": "markdown.new",
  "category": "relay",
  "publicly_queryable": True, "public_logs": False,
  "query_interface": "https://markdown.new/<url> Cloudflare edge URL->markdown; no history endpoint",
  "probed": True,
  "findings": "live relay confirmed; no public logs — unscourable by design",
  "blocker": ""},
 {"surface": "textise.net",
  "category": "relay",
  "publicly_queryable": True, "public_logs": False,
  "query_interface": "text-only page transform via form; no auth; no history endpoint",
  "probed": True,
  "findings": "relay confirmed alive; no public logs — unscourable by design",
  "blocker": ""},
 {"surface": "cors-anywhere.herokuapp.com",
  "category": "relay",
  "publicly_queryable": False, "public_logs": False,
  "query_interface": "requires manual per-browser opt-in at /corsdemo",
  "probed": False,
  "findings": "gated behind manual opt-in; no public logs",
  "blocker": "opt-in gate"},
 {"surface": "test.cors.workers.dev / sirjosh CORS proxy",
  "category": "relay",
  "publicly_queryable": True, "public_logs": False,
  "query_interface": "private Cloudflare Workers; no public log interface",
  "probed": False,
  "findings": "known from prior notes (SEC county.json laundering); private infra, unscourable",
  "blocker": "no public log interface"},
 {"surface": "12ft.io",
  "category": "relay",
  "publicly_queryable": False, "public_logs": False,
  "query_interface": "none — service shut down",
  "probed": False,
  "findings": "paywall-bypass relay; dead",
  "blocker": "service dead"},
 # --- dead-drop / scan / code-search surfaces (public query) ---
 {"surface": "urlscan.io",
  "category": "scan-archive",
  "publicly_queryable": True, "public_logs": True,
  "query_interface": "GET /api/v1/search/?q=<lucene> (search quotas may require API key); scan submission requires key",
  "probed": True,
  "findings": "public scan DB; probed keyless search for incident domains/filenames",
  "blocker": ""},
 {"surface": "grep.app",
  "category": "code-search",
  "publicly_queryable": True, "public_logs": True,
  "query_interface": "web UI public; /api/search behind Vercel bot challenge for scripted clients; MCP endpoint https://mcp.grep.app unauthenticated (searchGitHub tool)",
  "probed": True,
  "findings": "probed via unauthenticated MCP endpoint for fingerprint strings in public GitHub code",
  "blocker": ""},
 {"surface": "sourcegraph.com",
  "category": "code-search",
  "publicly_queryable": True, "public_logs": True,
  "query_interface": "public code search; /.api/search/stream no-auth for public repos",
  "probed": True,
  "findings": "stream endpoint attempted; outcome recorded in probe log",
  "blocker": ""},
 {"surface": "pastebin.com",
  "category": "dead-drop",
  "publicly_queryable": True, "public_logs": False,
  "query_interface": "/archive shows ~25 most recent public pastes only; no search API",
  "probed": False,
  "findings": "no historical query interface; June-2026 pastes unrecoverable via public surface",
  "blocker": "recent-only window, no search API"},
 {"surface": "rentry.co",
  "category": "dead-drop",
  "publicly_queryable": False, "public_logs": False,
  "query_interface": "none — no public index",
  "probed": False,
  "findings": "no public index; unscourable",
  "blocker": "no public index"},
]

# ---------------------------------------------------------------- probes
def cdx(params):
    q = urllib.parse.urlencode(params)
    return "https://web.archive.org/cdx/search/cdx?" + q

PROBES = [
 {"id": "cdx-doe-fuzz", "surface": "web.archive.org (Wayback CDX)", "host": "web.archive.org",
  "url": cdx({"url": "civilrightsdata.ed.gov*", "from": "20260601", "to": "20260701",
              "output": "json", "fl": "timestamp,original,statuscode", "limit": "100",
              "filter": "original:(?i).*(State_Id|Measure_Id|survey_Year_Key).*"}),
  "timeout": 90, "want": ["state_id", "measure_id", "survey_year_key"],
  "note": "DoE CRDC fuzz params in archived original URLs, Jun 2026"},
 {"id": "cdx-doe-any", "surface": "web.archive.org (Wayback CDX)", "host": "web.archive.org",
  "url": cdx({"url": "civilrightsdata.ed.gov*", "from": "20260615", "to": "20260618",
              "output": "json", "fl": "timestamp,original", "collapse": "urlkey", "limit": "100"}),
  "timeout": 90, "want": [],
  "note": "baseline: any IA captures of CRDC host in incident window"},
 {"id": "cdx-bea-oai", "surface": "web.archive.org (Wayback CDX)", "host": "web.archive.org",
  "url": cdx({"url": "bea.gov*", "from": "20260616", "to": "20260622",
              "output": "json", "fl": "timestamp,original,statuscode", "limit": "100",
              "filter": "original:(?i).*oai.*"}),
  "timeout": 90, "want": ["oai"],
  "note": "oai-tagged BEA URLs in incident window"},
 {"id": "cdx-census-oai", "surface": "web.archive.org (Wayback CDX)", "host": "web.archive.org",
  "url": cdx({"url": "census.gov*", "from": "20260616", "to": "20260622",
              "output": "json", "fl": "timestamp,original,statuscode", "limit": "100",
              "filter": "original:(?i).*oai.*"}),
  "timeout": 90, "want": ["oai"],
  "note": "oai-tagged census.gov URLs in incident window"},
 {"id": "cdx-sec-county", "surface": "web.archive.org (Wayback CDX)", "host": "web.archive.org",
  "url": cdx({"url": "www.sec.gov/files/county.json", "from": "20260601", "to": "20260701",
              "output": "json", "fl": "timestamp,original,statuscode", "limit": "50"}),
  "timeout": 90, "want": [],
  "note": "SEC county.json captures, Jun 2026 (known laundering cluster)"},
 {"id": "archivetoday-newest-doe", "surface": "archive.today (+mirrors archive.ph/.md/.li/.is)",
  "host": "archive.ph",
  "url": "https://archive.ph/newest/https://civilrightsdata.ed.gov/",
  "timeout": 45, "want": [], "follow": True,
  "note": "newest archive.today snapshot of CRDC host"},
 {"id": "urlscan-doe", "surface": "urlscan.io", "host": "urlscan.io",
  "url": "https://urlscan.io/api/v1/search/?" + urllib.parse.urlencode(
      {"q": "domain:civilrightsdata.ed.gov", "size": "10"}),
  "timeout": 45, "want": ["state_id", "oai"],
  "note": "keyless urlscan search for CRDC scans"},
 {"id": "urlscan-countyjson", "surface": "urlscan.io", "host": "urlscan.io",
  "url": "https://urlscan.io/api/v1/search/?" + urllib.parse.urlencode(
      {"q": "filename:county.json", "size": "10"}),
  "timeout": 45, "want": ["sec.gov"],
  "note": "keyless urlscan search for county.json scans"},
 {"id": "permacc-public", "surface": "perma.cc", "host": "api.perma.cc",
  "url": "https://api.perma.cc/v1/public/archives/?limit=3",
  "timeout": 45, "want": [],
  "note": "public-archives endpoint shape + auth requirement"},
 {"id": "memento-doe", "surface": "Memento Time Travel (timetravel.mementoweb.org)",
  "host": "timetravel.mementoweb.org",
  "url": "https://timetravel.mementoweb.org/api/json/20260617/https://civilrightsdata.ed.gov/",
  "timeout": 45, "want": [],
  "note": "federated memento lookup for CRDC on Jun 17 (https; http gave empty reply)"},
 {"id": "cc-collinfo", "surface": "Common Crawl Index (index.commoncrawl.org)",
  "host": "index.commoncrawl.org",
  "url": "https://index.commoncrawl.org/collinfo.json",
  "timeout": 45, "want": [], "stash": "cc_collinfo",
  "note": "list available crawl indexes"},
 {"id": "cc-doe-fuzz", "surface": "Common Crawl Index (index.commoncrawl.org)",
  "host": "index.commoncrawl.org", "depends": "cc_collinfo",
  "url": None,  # built from collinfo: June-2026 crawl, CRDC host
  "timeout": 90, "want": ["state_id", "zz=oai"],
  "note": "June-2026 crawl: CRDC URLs, grepped locally for agent params"},
 {"id": "grep-mcp-zzoai", "surface": "grep.app", "host": "mcp.grep.app",
  "method": "POST", "url": "https://mcp.grep.app",
  "headers": {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
  "data": {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
           "params": {"name": "searchGitHub", "arguments": {"query": "zz=oai"}}},
  "timeout": 45, "want": ["zz=oai"],
  "note": "public GitHub code search for zz=oai cache-buster tags"},
 {"id": "grep-mcp-dsqa", "surface": "grep.app", "host": "mcp.grep.app",
  "method": "POST", "url": "https://mcp.grep.app",
  "headers": {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
  "data": {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
           "params": {"name": "searchGitHub", "arguments": {"query": "dsqa_250"}}},
  "timeout": 45, "want": ["dsqa_250"],
  "note": "public GitHub code search for DeepSearchQA id"},
 {"id": "sourcegraph-zzoai", "surface": "sourcegraph.com", "host": "sourcegraph.com",
  "url": "https://sourcegraph.com/.api/search/stream?" + urllib.parse.urlencode(
      {"q": "context:global zz=oai select:file", "v": "V3"}),
  "timeout": 30, "want": ["zz=oai"],
  "note": "no-auth public code search stream attempt"},
 {"id": "live-allorigins", "surface": "allorigins.win", "host": "api.allorigins.win",
  "url": "https://api.allorigins.win/raw?" + urllib.parse.urlencode({"url": "https://example.com"}),
  "timeout": 30, "want": [],
  "note": "liveness only; no log interface exists to probe"},
 {"id": "live-corsproxyio", "surface": "corsproxy.io", "host": "corsproxy.io",
  "url": "https://corsproxy.io/?" + urllib.parse.urlencode({"": "https://example.com"}).replace("=", ""),
  "timeout": 30, "want": [],
  "note": "liveness only; operator claims no logs"},
 {"id": "live-markdownnew", "surface": "markdown.new", "host": "markdown.new",
  "url": "https://markdown.new/https://example.com",
  "timeout": 30, "want": [],
  "note": "liveness only; no log interface exists"},
 {"id": "live-rjina", "surface": "r.jina.ai", "host": "r.jina.ai",
  "url": "https://r.jina.ai/https://example.com",
  "timeout": 30, "want": [],
  "note": "anonymous-access status check (expect 401/402 per 2026 research)"},
 {"id": "live-textise", "surface": "textise.net", "host": "www.textise.net",
  "url": "https://www.textise.net/",
  "timeout": 30, "want": [],
  "note": "liveness only; no log interface exists"},
]

# ---------------------------------------------------------------- helpers
def load_state():
    if os.path.exists(STATE_F):
        with open(STATE_F) as f:
            return json.load(f)
    return {"lane": "re-hunt-relays", "started_utc": NOW(), "watermark": None,
            "items_collected": 0, "surfaces_total": len(SURFACES), "surfaces_probed": 0,
            "status": "active", "probes_completed": [], "inventory_written": False,
            "stash": {}}

def save_state(s):
    with open(STATE_F, "w") as f:
        json.dump(s, f, indent=1)

def append_jsonl(path, row):
    with open(path, "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

def write_inventory(state):
    if state.get("inventory_written") and os.path.exists(INV_F):
        return
    with open(INV_F, "w") as f:
        for s in SURFACES:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    state["inventory_written"] = True

_last_host_ts = {}
def polite(host):
    now = time.time()
    prev = _last_host_ts.get(host, 0)
    wait = 2.0 - (now - prev)
    if wait > 0:
        time.sleep(wait)
    _last_host_ts[host] = time.time()

def run_curl(probe):
    body_f = "/tmp/re-hunt-relay-body.bin"
    cmd = ["curl", "-sS", "--max-time", str(probe.get("timeout", 45)),
           "-A", UA, "-o", body_f, "-w", "%{http_code}"]
    if probe.get("follow"):
        cmd.append("-L")
    for k, v in (probe.get("headers") or {}).items():
        cmd += ["-H", "%s: %s" % (k, v)]
    if probe.get("method") == "POST":
        cmd += ["-X", "POST", "--data-binary", "@-"]
        stdin = json.dumps(probe["data"]).encode()
    else:
        stdin = None
    cmd.append(probe["url"])
    try:
        p = subprocess.run(cmd, input=stdin, capture_output=True,
                           timeout=probe.get("timeout", 45) + 15)
        out = (p.stdout or b"").decode("utf-8", "replace")
        code = out.strip().split("\n")[-1] if out.strip() else "000"
        err = (p.stderr or b"").decode("utf-8", "replace").strip().split("\n")[-1] \
            if p.returncode != 0 else ""
        size = os.path.getsize(body_f) if os.path.exists(body_f) else 0
        with open(body_f, "rb") as f:
            body = f.read(200000)
        return code, size, body, err
    except subprocess.TimeoutExpired:
        return "TIMEOUT", 0, b"", "client timeout"
    except Exception as e:  # noqa
        return "ERROR", 0, b"", str(e)[:200]

def reclassify_probe_log():
    """One-time correction: earlier runs labeled every non-blocked HTTP code
    result='ok'. Recompute from http_code. Idempotent."""
    if not os.path.exists(PROBELOG_F):
        return
    rows, changed = [], False
    with open(PROBELOG_F) as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            code = r.get("http_code")
            want = {"200": "ok", "201": "ok", "404": "not-found", "429": "rate-limited",
                    "401": "auth-or-denied", "402": "auth-or-denied",
                    "403": "auth-or-denied"}.get(code)
            if want is None and code in ("000", "TIMEOUT", "ERROR", "504", "522", "502", "503"):
                want = "blocked-or-failed"
            if want and r.get("result") != want:
                r["result"] = want
                changed = True
            rows.append(r)
    if changed:
        with open(PROBELOG_F, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

def main():
    state = load_state()
    reclassify_probe_log()
    write_inventory(state)
    done = set(state.get("probes_completed", []))
    hits_seen = set()
    if os.path.exists(HITS_F):
        with open(HITS_F) as f:
            for line in f:
                try:
                    h = json.loads(line)
                    hits_seen.add((h.get("surface"), h.get("fingerprint"), h.get("url_or_ref")))
                except Exception:
                    pass
    for probe in PROBES:
        pid = probe["id"]
        if pid in done:
            continue
        # dependency: build CC query URL from collinfo stash
        if probe.get("depends"):
            stash = state.get("stash", {}).get(probe["depends"])
            if not stash:
                append_jsonl(PROBELOG_F, {"ts": NOW(), "probe_id": pid, "surface": probe["surface"],
                    "target": "(dependency unmet: %s)" % probe["depends"],
                    "http_code": "SKIP", "bytes": 0,
                    "result": "skipped", "note": "dependency probe produced no usable stash"})
                done.add(pid)
                continue
            try:
                infos = json.loads(stash)
                pick = None
                for info in infos:
                    iid = info.get("id", "")
                    if iid.startswith("CC-MAIN-2026-2") and info.get("from", "") <= "20260620":
                        pick = iid
                pick = pick or infos[0]["id"]
            except Exception as e:  # noqa
                append_jsonl(PROBELOG_F, {"ts": NOW(), "probe_id": pid, "surface": probe["surface"],
                    "target": "(collinfo parse failed)", "http_code": "SKIP", "bytes": 0,
                    "result": "skipped", "note": "collinfo unparseable"})
                done.add(pid)
                continue
            probe["url"] = ("https://index.commoncrawl.org/%s-index?" % pick +
                            urllib.parse.urlencode({"url": "civilrightsdata.ed.gov/*",
                                                    "output": "json", "limit": "50"}))
            probe["note"] += " [crawl=%s]" % pick
        polite(probe["host"])
        ts = NOW()
        code, size, body, err = run_curl(probe)
        text = body.decode("utf-8", "replace")
        low = text.lower()
        # fingerprint grep
        found = [w for w in probe.get("want", []) if w.lower() in low]
        result = "ok"
        note = probe["note"]
        if code in ("000", "TIMEOUT", "ERROR", "504", "522", "502", "503"):
            result = "blocked-or-failed"
            note += " | transport/server: %s %s" % (code, err)
        elif code == "404":
            result = "not-found"
            note += " | HTTP 404"
        elif code == "429":
            result = "rate-limited"
            note += " | HTTP 429: stop, recorded, moving on"
        elif code in ("401", "402", "403"):
            result = "auth-or-denied"
            note += " | HTTP %s" % code
        # record stash
        if probe.get("stash") and code == "200":
            state.setdefault("stash", {})[probe["stash"]] = text[:50000]
        # hits
        for w in found:
            i = low.find(w.lower())
            snip = text[max(0, i - 120): i + 200].replace("\n", " ")[:320]
            key = (probe["surface"], w, probe["url"][:160])
            if key not in hits_seen:
                hits_seen.add(key)
                append_jsonl(HITS_F, {"surface": probe["surface"], "fingerprint": w,
                                     "evidence": snip, "url_or_ref": probe["url"][:300],
                                     "probe_id": pid, "ts": ts})
                state["items_collected"] = state.get("items_collected", 0) + 1
        append_jsonl(PROBELOG_F, {"ts": ts, "probe_id": pid, "surface": probe["surface"],
                                  "target": probe["url"][:220] if probe.get("url") else "(unbuilt)",
                                  "http_code": code, "bytes": size, "result": result,
                                  "note": note,
                                  "fingerprints_matched": found})
        done.add(pid)
        state["probes_completed"] = sorted(done)
        state["watermark"] = ts
        state["surfaces_probed"] = len({s["surface"] for s in SURFACES if s["probed"]})
        save_state(state)
    state["status"] = "complete" if len(done) == len(PROBES) else "active"
    save_state(state)
    print(json.dumps({"probes_completed": len(done), "probes_total": len(PROBES),
                      "hits": state["items_collected"], "status": state["status"]}, indent=1))

if __name__ == "__main__":
    main()
