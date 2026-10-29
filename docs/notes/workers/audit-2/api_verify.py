#!/usr/bin/env python3
"""API ground-truth verification + repair for audit-2 chunk. Pace <=1 req/5s to en.wikipedia.org."""
import json, os, sys, time, subprocess, urllib.parse
from datetime import datetime, timezone

BASE = os.path.expanduser("~/workspace/silent-locus-top500")
REVDIR = os.path.join(BASE, "data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions")
UA = "silent-locus-top500-scan/1.0 (research)"
OUT = os.path.join(BASE, "workers/audit-2/api_results.json")
PROG = os.path.join(BASE, "workers/audit-2/api_progress.json")
GAP = 5.2  # seconds between API calls

API_CALLS = [0]

def api_get(params):
    """Single API GET via curl. Returns parsed JSON."""
    API_CALLS[0] += 1
    q = urllib.parse.urlencode(params)
    url = "https://en.wikipedia.org/w/api.php?" + q
    r = subprocess.run(["curl", "-sS", "--max-time", "60", "-A", UA, url],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl failed: {r.stderr[:200]}")
    return json.loads(r.stdout)

def oldest_in_window(title):
    """Oldest revision with timestamp >= 2020-01-01. Returns (revid, timestamp) or (None,None)."""
    p = {"action": "query", "prop": "revisions", "titles": title,
         "rvlimit": 1, "rvdir": "newer", "rvstart": "2020-01-01T00:00:00Z",
         "rvprop": "ids|timestamp", "format": "json", "formatversion": 2}
    d = api_get(p)
    pages = d.get("query", {}).get("pages", [])
    if not pages:
        return None, None
    pg = pages[0]
    if pg.get("missing"):
        return None, None
    revs = pg.get("revisions", [])
    if not revs:
        return None, None
    return revs[0].get("revid"), revs[0].get("timestamp")

def repull(rank, title):
    """Full re-pull older->newer window into temp file, fsync, atomic rename."""
    recs = []
    cont = None
    while True:
        paced()
        p = {"action": "query", "prop": "revisions", "titles": title,
             "rvlimit": 500, "rvdir": "older", "rvstart": "2026-10-07T00:00:00Z",
             "rvend": "2020-01-01T00:00:00Z",
             "rvprop": "user|timestamp|ids|comment|tags|size",
             "format": "json", "formatversion": 2}
        if cont:
            p.update(cont)
        d = api_get(p)
        last_call[0] = time.time()
        pages = d.get("query", {}).get("pages", [])
        if pages and not pages[0].get("missing"):
            for rv in pages[0].get("revisions", []):
                recs.append({
                    "rank": rank, "article": title,
                    "revid": rv.get("revid"), "parentid": rv.get("parentid"),
                    "user": rv.get("user"), "timestamp": rv.get("timestamp"),
                    "comment": rv.get("comment", ""), "tags": rv.get("tags", []),
                    "size": rv.get("size"),
                })
        cont = d.get("continue")
        if not cont:
            break
    tmp = os.path.join(REVDIR, f"{rank}.jsonl.tmp.audit2")
    final = os.path.join(REVDIR, f"{rank}.jsonl")
    with open(tmp, "w", encoding="utf-8") as f:
        for rec in recs:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, final)
    return len(recs)

def iso_to_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

locals_ = {r["rank"]: r for r in json.load(open(os.path.join(BASE, "workers/audit-2/local_results.json")))}
done = {}
if os.path.exists(PROG):
    done = {int(k): v for k, v in json.load(open(PROG)).items()}

last_call = [0.0]

def paced():
    dt = time.time() - last_call[0]
    if dt < GAP:
        time.sleep(GAP - dt)

results = {}
for rank in sorted(locals_):
    if rank in done:
        results[rank] = done[rank]
        continue
    rec = {"rank": rank, "title": locals_[rank]["title"]}
    rec["local_lines"] = locals_[rank]["lines"]
    rec["local_min_ts"] = locals_[rank]["min_ts"]
    rec["local_issues"] = locals_[rank]["issues"]
    try:
        paced()
        revid, ts = oldest_in_window(rec["title"])
        last_call[0] = time.time()
    except Exception as e:
        rec["verdict"] = "API_ERROR"
        rec["error"] = str(e)
        results[rank] = rec
        continue
    rec["api_oldest_revid"] = revid
    rec["api_oldest_ts"] = ts
    rec["verdict"] = "OK"
    if ts is None:
        rec["verdict"] = "API_NO_REVISIONS"
    elif rec["local_lines"] == 0:
        rec["verdict"] = "BROKEN"
    else:
        try:
            delta_days = (iso_to_dt(rec["local_min_ts"]) - iso_to_dt(ts)).total_seconds() / 86400.0
            rec["delta_days"] = round(delta_days, 2)
            if delta_days > 1.0:
                rec["verdict"] = "TRUNCATED"
        except Exception as e:
            rec["verdict"] = "COMPARE_ERROR"
            rec["error"] = str(e)
    # repair
    if rec["verdict"] in ("BROKEN", "TRUNCATED"):
        try:
            before = rec["local_lines"]
            new_n = repull(rank, rec["title"])
            rec["repaired"] = True
            rec["lines_before"] = before
            rec["lines_after"] = new_n
            # re-verify: reload file, get min/max ts
            mn = mx = None
            ok = True
            prev = None
            for raw in open(os.path.join(REVDIR, f"{rank}.jsonl"), encoding="utf-8"):
                r2 = json.loads(raw)
                t = r2["timestamp"]
                if mn is None or t < mn: mn = t
                if mx is None or t > mx: mx = t
                if prev is not None and t > prev: ok = False
                prev = t
            rec["new_min_ts"] = mn
            rec["new_max_ts"] = mx
            rec["reverify_ok"] = ok and mn is not None
        except Exception as e:
            rec["repaired"] = False
            rec["repair_error"] = str(e)
    results[rank] = rec
    done[rank] = rec
    json.dump({str(k): v for k, v in results.items()}, open(PROG, "w"))
    print(f"rank {rank}: {rec['verdict']}" + (f" repaired {rec.get('lines_before')}->{rec.get('lines_after')}" if rec.get("repaired") else ""), flush=True)

json.dump(results, open(OUT, "w"), indent=1)
json.dump({"api_calls": API_CALLS[0]}, open(os.path.join(BASE, "workers/audit-2/api_call_count.json"), "w"))
print(f"DONE. articles={len(results)} api_calls={API_CALLS[0]}")
