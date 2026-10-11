#!/usr/bin/env python3
"""urlscan.io sweep for the "what has Transluce missed" hunt.

Runs every planned urlscan.io search query (leftover from the 403-blocked
hot-leads lane) plus IOC follow-ups, via the keyless search API:
  https://urlscan.io/api/v1/search/?q=<query>&size=<n>

Idempotent: state.json keys by query; done queries are skipped on rerun.
Polite: 4s pacing between requests; hard stop on 2 consecutive 403/429
(rate-limit) responses — the probe ends and the report says so.
Read-only: search API only, no submissions.
"""
import json, time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RAW = DATA / "raw"
RAW.mkdir(parents=True, exist_ok=True)
STATE = ROOT / "state.json"
LOG = DATA / "query-log.jsonl"

UA = {"User-Agent": "silent-locus-hunt-urlscan-sweep/1.0 (research)"}
PACE = 4.0

# (query, note, size)
# NOTE 2026-10-03: leading wildcards / regex are 403 for anonymous users
# ("not supported for anonymous users, please create a user-account").
# All queries below use trailing wildcards or exact terms only.
QUERIES = [
    # --- F1: incident hosts in submitted URLs (leftover, 403-blocked) ---
    ("task.url:civilrightsdata*", "F1: CRDC host in submitted URLs", 100),
    ("task.url:bac-lac.gc.ca*", "F1: LAC gc.ca host", 100),
    ("task.url:bac-lac.canada.ca*", "F1: LAC canada.ca host (primary per arquivo.pt)", 100),
    ("task.url:bea.gov*", "F1: BEA host", 100),
    ("task.url:census.gov*", "F1: Census host", 100),
    ("task.url:kansasmemory*", "F1: Kansas memory host", 100),
    # --- F2: filenames (leftover) ---
    ("filename:virginia-projection*", "F2: virginia-projection filename", 100),
    ("filename:xls domain:ed.gov", "F2: xls files on ed.gov", 100),
    ("filename:xls domain:census.gov", "F2: xls files on census.gov", 100),
    ("filename:xls domain:bea.gov", "F2: xls files on bea.gov", 100),
    ("domain:sec.gov filename:county.json", "F2: county.json constrained to sec.gov (prior hit was all Ramsey County noise)", 100),
    # --- F3: incident windows (leftover) ---
    ("task.url:civilrightsdata* date:>2026-06-16 date:<2026-06-19", "F3: DoE incident window Jun 16-19", 100),
    ("task.url:bea.gov* date:>2026-06-15 date:<2026-06-19", "F3: BEA incident window Jun 16-18", 100),
    ("task.url:census.gov* date:>2026-06-15 date:<2026-06-23", "F3: Census incident window Jun 16-22", 100),
    ("task.url:sec.gov* date:>2026-06-17 date:<2026-06-19", "F3: SEC incident window Jun 18", 100),
    ("task.url:kansasmemory* date:>2026-05-06 date:<2026-05-09", "F3: Kansas window May 7", 100),
    ("task.url:bac-lac.gc.ca* date:>2026-05-27 date:<2026-05-29", "F3: LAC window May 28", 100),
    ("task.url:bac-lac.gc.ca* date:>2026-06-08 date:<2026-06-10", "F3: LAC window Jun 9", 100),
    ("task.url:bac-lac.canada.ca* date:>2026-06-08 date:<2026-06-10", "F3: LAC canada.ca window Jun 9", 100),
    ("task.url:max.gov* date:>2026-05-24 date:<2026-05-28", "F3: MAX.gov window May 25-27", 100),
    ("task.url:cdc.gov* date:>2026-07-17 date:<2026-07-20", "F3: CDC WONDER window Jul 18", 100),
    # --- F4: launcher IOC markers (leftover) ---
    ("page.url:oai*", "F4: oai in page.url (size=10 noise grading)", 10),
    ("task.url:zz=oai*", "F4: zz=oai literal in submitted URL", 100),
    ("page.url:zz=oai*", "F4: zz=oai in page.url", 100),
    # --- F5: follow-ups (new in this sweep) ---
    ("task.url:openai_research*", "F5: openai_research variant in submitted URL (fake-org IOC)", 100),
    ("page.url:openai_research*", "F5: openai_research variant in page.url", 100),
    ("task.url:recherche-collection-search*", "F5: LAC collection-search service host specifically", 100),
    ("page.url:survey_Year_Key*", "F5: DoE API param survey_Year_Key in page.url", 100),
    ("task.url:GetStateEstimation*", "F5: DoE CRDC API endpoint in submitted URL", 100),
    ("task.url:civilrightsdata* date:>2026-06-01 date:<2026-07-01", "F5: DoE broader June window", 100),
    ("task.url:bac-lac.gc.ca* date:>2026-06-01 date:<2026-06-20", "F5: LAC broader June window", 100),
    ("task.url:\"sec.gov/files/county.json\"", "F5: exact SEC incident file path in submitted URL (quoted: unquoted slashes trip the anon regex filter)", 100),
]


def run_query(q, size):
    url = "https://urlscan.io/api/v1/search/?q=" + quote(q, safe="") + "&size=" + str(size)
    req = Request(url, headers=UA)
    try:
        with urlopen(req, timeout=45) as resp:
            body = resp.read()
            code = resp.status
    except HTTPError as e:
        return {"http_code": e.code, "error": f"HTTPError {e.code}"}
    except (URLError, TimeoutError) as e:
        return {"http_code": "ERR", "error": f"{type(e).__name__}: {e}"}
    except Exception as e:
        return {"http_code": "ERR", "error": f"{type(e).__name__}: {e}"}
    try:
        data = json.loads(body)
    except Exception as e:
        return {"http_code": code, "error": f"bad json: {e}"}
    return {"http_code": code, "data": data}


def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    consec_block = 0
    n = 0
    with LOG.open("a") as log:
        for qi, (q, note, size) in enumerate(QUERIES):
            if q in state and state[q].get("done"):
                print(f"skip [{qi}] {q[:55]!r} (done)")
                continue
            res = run_query(q, size)
            n += 1
            code = res.get("http_code")
            if code != 200:
                transient = code in (403, 429) or code == "ERR" or (
                    isinstance(code, int) and 500 <= code < 600)
                rec = {"query": q, "note": note, "done": not transient,
                       "http_code": code, "error": res.get("error"),
                       "result_count": None, "examples": []}
                state[q] = rec
                log.write(json.dumps(rec) + "\n"); log.flush()
                STATE.write_text(json.dumps(state, indent=2))
                print(f"[{qi}] {q[:55]!r} -> {code} {str(res.get('error',''))[:60]}"
                      + ("" if transient else " (client error, not retried)"), flush=True)
                if code in (403, 429):
                    consec_block += 1
                if consec_block >= 2:
                    print("HARD STOP: 2 consecutive 403/429 — ending sweep per guard", flush=True)
                    break
                time.sleep(PACE)
                continue
            consec_block = 0
            data = res["data"]
            total = data.get("total")
            results = data.get("results", []) or []
            examples = []
            for r in results[:8]:
                t = r.get("task", {}) or {}
                p = r.get("page", {}) or {}
                examples.append({"uuid": t.get("uuid"), "task_url": t.get("url"),
                                 "page_url": p.get("url"), "date": t.get("time")})
            rec = {"query": q, "note": note, "done": True, "http_code": code,
                   "result_count": total, "returned": len(results), "examples": examples}
            if total:
                RAW.joinpath(f"q{qi:02d}.json").write_text(json.dumps(data)[:2000000])
            state[q] = rec
            log.write(json.dumps(rec) + "\n"); log.flush()
            STATE.write_text(json.dumps(state, indent=2))
            print(f"[{qi}] {q[:55]!r} -> {code} total={total}", flush=True)
            time.sleep(PACE)
    STATE.write_text(json.dumps(state, indent=2))
    done = sum(1 for v in state.values() if v.get("done"))
    print(f"\nsweep finished: {n} attempted this run, {done}/{len(QUERIES)} queries done total")


if __name__ == "__main__":
    main()
