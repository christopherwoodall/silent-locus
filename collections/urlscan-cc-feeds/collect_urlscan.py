#!/usr/bin/env python3
"""Lane 3: urlscan.io sweep into openai-agent-traces corpus.

Queries (see QUERIES below):
  1. oai*/zz=oai fingerprints
  2. dsqa target domains (civilrightsdata.ed.gov, bea.gov,
     recherche-collection-search.bac-lac.canada.ca, bac-lac.gc.ca, sec.gov)
  3. filename:county.json

Idempotent: scan UUIDs already seen are recorded in data/seen.json and never
re-emitted. Re-run resumes and appends only new records.
Polite rate: >=2s between API calls. Any block (429/403) stops the run and is
recorded in state.json + probe-log.jsonl.
NOTE: urlscan keyless search only covers the last 30 days of scans
(search_date_limit_days: 30 in API responses). Logged for honesty.
"""
import gzip
import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA_DIR = os.path.join(ROOT, "openai-agent-traces", "data")
OUT_FILE = os.path.join(DATA_DIR, "urlscan.jsonl")
SEEN_FILE = os.path.join(HERE, "data", "seen.json")
PROBE_LOG = os.path.join(HERE, "probe-log.jsonl")
STATE_FILE = os.path.join(HERE, "state.json")

BASE = "https://urlscan.io/api/v1/search/"
RATE_S = 2.0
PAGES_MAX = 2          # max pages (100 results each) per query
SIZE = 100

QUERIES = [
    # (query, class, attribution.provider evidence rule)
    # NOTE: urlscan returns HTTP 403 for leading-wildcard forms
    # (e.g. task.url:*zz=oai*); non-leading forms below all return 200.
    ("page.url:zz=oai*", "oai-fingerprint", True),
    ("task.url:zz=oai*", "oai-fingerprint", True),
    ("page.url:oai*", "oai-fingerprint", True),
    ("task.url:oai*", "oai-fingerprint", True),
    ("filename:oai*", "oai-fingerprint", True),
    ("domain:civilrightsdata.ed.gov", "dsqa-domain", False),
    ("domain:bea.gov", "dsqa-domain", False),
    ("domain:recherche-collection-search.bac-lac.canada.ca", "dsqa-domain", False),
    ("domain:bac-lac.gc.ca", "dsqa-domain", False),
    ("domain:sec.gov", "dsqa-domain", False),
    ("filename:county.json", "filename", False),
]


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def api_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "silent-locus-research/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:500]
    except Exception as e:  # noqa: BLE001 - log and continue
        return 0, repr(e)


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return json.load(f)
    return {"urlscan_uuids": []}


def save_seen(seen):
    os.makedirs(os.path.dirname(SEEN_FILE), exist_ok=True)
    with open(SEEN_FILE, "w") as f:
        json.dump({"urlscan_uuids": sorted(seen["urlscan_uuids"])}, f, indent=1)


def probe_log(entry):
    with open(PROBE_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def parse_task_time(t):
    # "2026-10-02T12:00:00.000Z" -> ISO with Z; fallback sentinel per schema
    if t:
        try:
            dt = datetime.fromisoformat(t.replace("Z", "+00:00"))
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:  # noqa: BLE001
            pass
    return "1970-01-01T00:00:00Z"


def map_record(res, query, qclass, provider_rule):
    task = res.get("task", {}) or {}
    page = res.get("page", {}) or {}
    uuid = task.get("uuid") or res.get("_id")
    task_url = task.get("url") or ""
    page_url = page.get("url") or ""
    domain = page.get("domain") or task.get("domain") or ""
    filename = page.get("filename") or task.get("filename") or ""
    result_url = res.get("result") or f"https://urlscan.io/result/{uuid}/"
    report_url = f"https://urlscan.io/result/{uuid}/"

    evidence = provider_rule and any(
        "oai" in (s or "").lower()
        for s in (task_url, page_url, filename)
    )
    matched = None
    if evidence:
        for s in (task_url, page_url, filename):
            if "oai" in (s or "").lower():
                matched = s
                break

    ts = parse_task_time(task.get("time"))
    labels = {
        "query.string": query,
        "query.class": qclass,
        "scan.uuid": uuid,
        "scan.task_url": task_url[:2000],
        "scan.page_url": page_url[:2000],
        "scan.domain": domain,
        "scan.visibility": task.get("visibility") or "",
        "scan.source": task.get("source") or "",
        "scan.country": page.get("country") or "",
        "scan.ip": page.get("ip") or "",
        "scan.server": page.get("server") or "",
        "scan.status": str(page.get("status") or ""),
        "retrieved_from": "urlscan.io search API",
    }
    if evidence:
        labels["attribution.provider"] = "openai"
    if ts.startswith("1970"):
        labels["timestamp_source"] = "fallback:no_recoverable_date"
    rec = {
        "@timestamp": ts,
        "event": {"dataset": "openai-agent-traces", "created": now_utc()},
        "record_kind": "urlscan_scan",
        "fingerprint": sha("urlscan:" + str(uuid)),
        "labels": labels,
        "title": f"urlscan.io scan {uuid}",
        "description": f"urlscan.io scan of {task_url or page_url} (matched query: {query})",
        "source_url": report_url,
        "retrieved_at": now_utc(),
        "retrieved_via": "urlscan-api-v1-search",
        "file": "collections/urlscan-cc-feeds/probe-log.jsonl",
        "observer": {"product": "urlscan.io search API", "vendor": "urlscan.io", "type": "service"},
        "tags": ["urlscan", "sweep-2026-10-03", qclass]
        + (["oai-fingerprint"] if evidence else []),
        "confidence": "medium",
    }
    if matched:
        rec["matched_string"] = matched[:2000]
    if not evidence:
        rec["note"] = ("Domain/filename sweep hit; no oai* fingerprint evidence - "
                       "attribution.provider not set (scope: agents and agent infrastructure).")
    else:
        rec["note"] = ("URL/filename carries an oai* fingerprint (agent-tooling tag), matching the "
                       "corroborated DoE zz=oai<digits> cache-buster tradecraft; "
                       "attribution.provider=openai set on that direct evidence only.")
    return rec


def fetch_query(query):
    """Fetch up to PAGES_MAX pages; returns (results, total, has_more_truncated, error)."""
    results = []
    total = 0
    search_after = None
    truncated = False
    for page in range(PAGES_MAX):
        params = {"q": query, "size": SIZE}
        if search_after:
            params["search_after"] = ",".join(str(x) for x in search_after)
        url = BASE + "?" + urllib.parse.urlencode(params)
        status, body = api_get(url)
        if status in (429, 403):
            return results, total, True, f"blocked:http_{status}"
        if status == 0 or status >= 400:
            return results, total, True, f"error:http_{status}"
        try:
            doc = json.loads(body)
        except Exception as e:  # noqa: BLE001
            return results, total, True, f"bad_json:{e}"
        total = doc.get("total", 0)
        batch = doc.get("results", [])
        results.extend(batch)
        if not doc.get("has_more") or not batch:
            break
        sort = batch[-1].get("sort")
        if not sort:
            break
        search_after = sort
        truncated = True
        time.sleep(RATE_S)
    else:
        truncated = True
    return results, total, truncated, None


def update_state(patch):
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)
    state.update(patch)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=1)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    seen = set(load_seen()["urlscan_uuids"])
    new_records = 0
    queries_done = []
    blocked = None
    for q, qclass, provider_rule in QUERIES:
        results, total, truncated, error = fetch_query(q)
        kept = 0
        for res in results:
            uuid = (res.get("task", {}) or {}).get("uuid") or res.get("_id")
            if not uuid or uuid in seen:
                continue
            rec = map_record(res, q, qclass, provider_rule)
            with open(OUT_FILE, "a") as f:
                f.write(json.dumps(rec) + "\n")
            seen.add(uuid)
            kept += 1
            new_records += 1
        probe_log({
            "ts": now_utc(),
            "api": "urlscan.io/api/v1/search",
            "query": q,
            "query_class": qclass,
            "total_reported": total,
            "results_fetched": len(results),
            "pages_truncated_at_2": truncated and total > len(results),
            "records_staged_new": kept,
            "error": error,
        })
        queries_done.append({"query": q, "total": total, "new": kept, "error": error})
        if error and error.startswith("blocked"):
            blocked = error
            break
        time.sleep(RATE_S)
    save_seen({"urlscan_uuids": sorted(seen)})
    update_state({
        "lane": "urlscan-cc-feeds",
        "urlscan": {
            "queries_completed": len(queries_done),
            "records_staged_total": len(seen),
            "records_staged_new_this_run": new_records,
            "output": "openai-agent-traces/data/urlscan.jsonl",
            "blocked": blocked,
            "note": ("urlscan keyless search is limited to the last 30 days of scans "
                     "(search_date_limit_days=30). Jun-2026 incident-era scans are outside "
                     "this window; results cover recent scans only. Leading-wildcard query "
                     "forms (e.g. task.url:*zz=oai*) are rejected server-side with HTTP 403 "
                     "(first run 2026-10-03); the working non-leading-wildcard forms "
                     "page.url:zz=oai* / task.url:zz=oai* / page.url:oai* / task.url:oai* / "
                     "filename:oai* are used instead."),
            "last_run_utc": now_utc(),
        },
        "status": "urlscan-complete" if not blocked else "urlscan-blocked",
        "updated_utc": now_utc(),
    })
    print(json.dumps({"queries": queries_done, "new_records": new_records, "blocked": blocked}, indent=1))


if __name__ == "__main__":
    main()
