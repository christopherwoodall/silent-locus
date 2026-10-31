#!/usr/bin/env python3
"""Fresh-phrase sweep: HN Algolia (date-filtered), GitHub issue search, urlquery.
Passive GET only. Sanitized captures: no author/login handles, no IPs,
no query-string values, no token values. Exact-substring counts are
computed on saved text only and reported with their denominator.
Algolia nbHits and GitHub total_count are TOKEN counts, not exact totals.
urlquery total_hits is the API total for the query string (matches
submitted URL and page content per hunt note 2026-10-15); saved rows
are a top-30 sample only.
"""
import json, re, subprocess, sys, time, urllib.parse, urllib.request, html

PHRASES = [
    "I am an autonomous agent",
    "autonomous agent intro",
    "agent-created",
    "subagent_spawned",
    "spawned a subagent",
    "agent loop",
    "agent-to-agent communication",
    "agent card",
    "owns its own crypto wallet",
    "fleet of autonomous agents",
]
OUT = "."
UA = {"User-Agent": "phrase-mining-passive/1.0"}

def slug(p):
    return re.sub(r"[^a-z0-9]+", "_", p.lower()).strip("_")

def hn(p):
    allhits, nb = [], None
    for page in range(3):
        params = {"query": p, "tags": "comment",
                  "hitsPerPage": 100, "page": page,
                  "numericFilters": "created_at_i>1761955200"}
        url = "https://hn.algolia.com/api/v1/search_by_date?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
        nb = d.get("nbHits")
        for h in d.get("hits", []):
            txt = html.unescape(re.sub(r"<[^>]+>", " ", h.get("comment_text") or h.get("title") or ""))
            allhits.append({"id": h.get("objectID"), "created": h.get("created_at"),
                            "story": h.get("story_id"), "text": txt})
        time.sleep(2)
        if len(d.get("hits", [])) < 100:
            break
    exact = sum(1 for h in allhits if p.lower() in h["text"].lower())
    return {"algolia_token_nbHits": nb, "saved": len(allhits),
            "exact_in_saved_text": exact, "hits": allhits}

def gh(p):
    q = urllib.parse.quote(p + " is:issue")
    out = subprocess.run(["gh", "api", f"search/issues?q={q}&per_page=30"],
                         capture_output=True, text=True, timeout=90)
    d = json.loads(out.stdout) if out.stdout.strip().startswith("{") else {"error": out.stderr[:300]}
    items = []
    for it in d.get("items", []):
        items.append({"repo": (it.get("repository_url") or "").replace(
            "https://api.github.com/repos/", ""),
            "number": it.get("number"), "title": it.get("title"),
            "created": it.get("created_at"), "state": it.get("state"),
            "url": it.get("html_url")})
    exact_title = sum(1 for i in items if p.lower() in (i["title"] or "").lower())
    return {"gh_api_total_count_token": d.get("total_count"),
            "saved": len(items), "exact_in_saved_titles": exact_title,
            "items": items, "error": d.get("error") or d.get("message")}

def uq(p):
    sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
    import dynamic_credentials as dc
    q = urllib.parse.urlencode(
        {"query": f'"{p}" date:[2025-11-01 TO 2026-10-31]', "limit": 30, "offset": 0})
    req = urllib.request.Request(
        "https://api.urlquery.net/public/v1/search/reports/?" + q,
        headers={"Accept": "application/json"})
    dc.add_surrogate_to_request(req, "custom.urlquery", allowed_hosts=["api.urlquery.net"])
    with urllib.request.urlopen(req, timeout=90) as r:
        d = dc.read_json_response(r)
    rows = []
    for rep in d.get("reports", []):
        fin = (rep.get("final") or {}).get("url") or {}
        rows.append({"report_id": rep.get("report_id"), "date": rep.get("date"),
                     "domain": (rep.get("url") or {}).get("domain"),
                     "final_fqdn": fin.get("fqdn"),
                     "final_path": (fin.get("addr") or "").split("?", 1)[0] if fin.get("addr") else "",
                     "title": (rep.get("final") or {}).get("title"),
                     "tags": rep.get("tags")})
    exact_title = sum(1 for x in rows if x["title"] and p.lower() in x["title"].lower())
    return {"uq_total_hits": d.get("total_hits"), "saved": len(rows),
            "exact_in_saved_titles": exact_title, "rows": rows}

summary = {}
for p in PHRASES:
    s = slug(p)
    try:
        h = hn(p)
        with open(f"hn_sweep_{s}.json", "w") as f: json.dump(h, f, indent=1)
        print(f"HN {p!r}: token={h['algolia_token_nbHits']} saved={h['saved']} exact={h['exact_in_saved_text']}", flush=True)
    except Exception as e:
        h = {"error": str(e)}; print(f"HN {p!r} ERR {e}", flush=True)
    try:
        g = gh(p)
        with open(f"gh_sweep_{s}.json", "w") as f: json.dump(g, f, indent=1)
        print(f"GH {p!r}: token_total={g.get('gh_api_total_count_token')} saved={g['saved']} exact_title={g['exact_in_saved_titles']}", flush=True)
    except Exception as e:
        g = {"error": str(e)}; print(f"GH {p!r} ERR {e}", flush=True)
    try:
        u = uq(p)
        with open(f"uq_sweep_{s}.json", "w") as f: json.dump(u, f, indent=1)
        print(f"UQ {p!r}: total={u['uq_total_hits']} saved={u['saved']} exact_title={u['exact_in_saved_titles']}", flush=True)
    except Exception as e:
        u = {"error": str(e)}; print(f"UQ {p!r} ERR {e}", flush=True)
    summary[p] = {"hn": {k: v for k, v in h.items() if k != "hits"},
                  "gh": {k: v for k, v in g.items() if k != "items"},
                  "uq": {k: v for k, v in u.items() if k != "rows"}}
    time.sleep(10)
with open("sweep_summary.json", "w") as f: json.dump(summary, f, indent=1)
print("DONE")
