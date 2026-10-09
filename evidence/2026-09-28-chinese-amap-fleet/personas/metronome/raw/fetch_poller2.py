#!/usr/bin/env python3
"""POLLER persona fetch — COMPLETION RUN (previous worker killed by runtime restart).

Patient mode: 3 passes over ~40+ min, 60s between service calls,
180s HTTP timeout (wrapper default 60s was throttling out),
union-merge of all reports ever seen per service.

Writes:
  htmx_<name>.json        (task-named canonical file)
  poller_safe_<name>.json (backup: sibling fetch_timing.py may overwrite
                           htmx_requestbin/pipedream/ntfy/file.io/0x0/paste.rs/
                           hastebin/rentry/telegra.ph while it runs its queue)
  fetch_poller2.log

Sibling fetch_timing.py is still running: do NOT re-run it; be gentle.
"""
import importlib.util
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "uq_htmx", os.path.expanduser("~/workspace/skills/urlquery/bin/uq_htmx.py"))
uq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uq)

# Longer timeouts: the endpoint was throttling/timeouts at 60s.
# Also tolerate IncompleteRead (flaky close mid-body): parse whatever arrived.
LONG_TIMEOUT = 180
import http.client


def fetch_long(path, current_url):
    h = dict(uq.HEADERS)
    h["HX-Current-URL"] = current_url
    req = urllib.request.Request(uq.BASE + path, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=LONG_TIMEOUT) as resp:
            return resp.read().decode("utf-8", "replace")
    except http.client.IncompleteRead as e:
        return e.partial.decode("utf-8", "replace")


uq.fetch = fetch_long

SERVICES = {
    "webhook_site": "url.domain:webhook.site",
    "ntfy_sh": "url.domain:ntfy.sh",
    "requestbin": "url.domain:requestbin.com",
    "pipedream": "url.domain:pipedream.net",
    "telegra_ph": "url.domain:telegra.ph",
    "file_io": "url.domain:file.io",
    "0x0_st": "url.domain:0x0.st",
    "paste_rs": "url.domain:paste.rs",
    "rentry": "url.domain:rentry.co",
    "hastebin": "url.domain:hastebin.com",
    "temp_sh": "url.domain:temp.sh",
    "catbox_moe": "url.domain:catbox.moe",
    "filebin_net": "url.domain:filebin.net",
}

LIMIT = 50
PASSES = 3
GAP_BETWEEN_CALLS = 60  # seconds between service calls (task requirement)

LOG = os.path.join(HERE, "fetch_poller2.log")


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def load_reports(path):
    """Load report list + attempts from a file; tolerant of corrupt data."""
    try:
        d = json.load(open(path))
    except Exception:
        return [], 0
    if isinstance(d, dict):
        rs = d.get("reports", [])
        att = d.get("fetch_meta", {}).get("attempts", 0)
        if not isinstance(rs, list) or (rs and not isinstance(rs[0], dict)):
            # corrupt shapes like {"reports": ["reports","query"]} -> treat as empty
            return [], att
        return rs, att
    return [], 0


def union_reports(*lists):
    seen = {}
    for lst in lists:
        for r in lst:
            rid = r.get("report_id") if isinstance(r, dict) else None
            if rid and rid not in seen:
                seen[rid] = r
    return list(seen.values())


def save(slug, query, reports, attempts):
    payload = {
        "query": query,
        "reports": reports,
        "fetch_meta": {"attempts": attempts,
                       "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                       "fetcher": "fetch_poller2.py"},
    }
    canon = os.path.join(HERE, f"htmx_{slug}.json")
    safe = os.path.join(HERE, f"poller_safe_{slug}.json")
    with open(safe, "w") as f:
        json.dump(payload, f, indent=1)
    with open(canon, "w") as f:
        json.dump(payload, f, indent=1)


def attempt(slug, query):
    """One attempt: returns new reports (list)."""
    res = uq.search(query, limit=LIMIT, delay=6)
    return res.get("reports", [])


def main():
    log(f"POLLER completion fetch start: {len(SERVICES)} services, {PASSES} passes, "
        f"{GAP_BETWEEN_CALLS}s between calls, {LONG_TIMEOUT}s timeout")
    attempts = {slug: 0 for slug in SERVICES}
    for p in range(1, PASSES + 1):
        log(f"--- PASS {p}/{PASSES} ---")
        for i, (slug, query) in enumerate(SERVICES.items()):
            existing, att = load_reports(os.path.join(HERE, f"poller_safe_{slug}.json"))
            attempts[slug] = max(attempts[slug], att)
            union = union_reports(existing, load_reports(os.path.join(HERE, f"htmx_{slug}.json"))[0])
            if len(union) >= LIMIT and attempts[slug] >= 1:
                log(f"[{i+1}/{len(SERVICES)}] {slug}: saturated ({len(union)}), skipping)")
            else:
                try:
                    new = attempt(slug, query)
                    union = union_reports(union, new)
                    attempts[slug] += 1
                    log(f"[{i+1}/{len(SERVICES)}] {slug} pass{p} attempt{attempts[slug]}: "
                        f"+{len(new)} new -> union {len(union)}")
                except Exception as e:
                    attempts[slug] += 1
                    log(f"[{i+1}/{len(SERVICES)}] {slug} pass{p} attempt{attempts[slug]} FAILED: "
                        f"{type(e).__name__}: {str(e)[:160]}")
                save(slug, query, union, attempts[slug])
            if i < len(SERVICES) - 1:
                time.sleep(GAP_BETWEEN_CALLS)
        log(f"--- PASS {p} done ---")
    log("POLLER completion fetch done.")


if __name__ == "__main__":
    main()
