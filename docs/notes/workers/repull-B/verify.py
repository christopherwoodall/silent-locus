#!/usr/bin/env python3
"""Verify repulled JSONL revision files: valid JSONL, article match,
timestamps non-increasing, oldest timestamp <= 2020-06-01."""
import json, os, sys

RAW = os.path.expanduser("~/workspace/silent-locus-top500/data/2026-10-06-wikipedia-top500-infra-scan/raw")
TSV = os.path.join(RAW, "missing-g2.tsv")
REVD = os.path.join(RAW, "revisions")
CUTOFF = "2020-06-01T00:00:00Z"

def check(rank, title):
    path = os.path.join(REVD, "%d.jsonl" % rank)
    errs = []
    if not os.path.exists(path):
        return {"rank": rank, "title": title, "ok": False, "errs": ["file missing"]}
    n = 0
    prev_ts = None
    oldest = None
    newest = None
    article_set = set()
    try:
        with open(path, encoding="utf-8") as f:
            for i, ln in enumerate(f, 1):
                ln = ln.strip()
                if not ln:
                    errs.append("blank line %d" % i)
                    continue
                try:
                    o = json.loads(ln)
                except json.JSONDecodeError as e:
                    errs.append("line %d: bad JSON: %s" % (i, e))
                    continue
                n += 1
                article_set.add(o.get("article"))
                ts = o.get("timestamp")
                if ts:
                    if newest is None:
                        newest = ts
                    if prev_ts is not None and ts > prev_ts:
                        errs.append("line %d: timestamp increasing (%s after %s)" % (i, ts, prev_ts))
                    prev_ts = ts
                    oldest = ts if oldest is None or ts < oldest else oldest
    except OSError as e:
        return {"rank": rank, "title": title, "ok": False, "errs": ["read error: %s" % e]}
    if n == 0:
        errs.append("zero revision lines")
    if article_set != {title}:
        errs.append("article mismatch: %s" % sorted(article_set))
    suspect = bool(oldest and oldest > CUTOFF)
    if suspect:
        errs.append("SUSPECT: oldest timestamp %s newer than 2020-06-01 (incomplete window?)" % oldest)
    return {"rank": rank, "title": title, "ok": not errs, "count": n,
            "oldest": oldest, "newest": newest, "errs": errs}

def main():
    with open(TSV, encoding="utf-8") as f:
        rows = [ln.rstrip("\n").split("\t") for ln in f if ln.strip()]
    results = []
    for rank_s, title in rows:
        r = check(int(rank_s), title)
        results.append(r)
        status = "OK" if r["ok"] else "FAIL"
        print("%s rank=%d %-28s n=%s oldest=%s newest=%s %s" % (
            status, r["rank"], r["title"], r.get("count", 0),
            r.get("oldest"), r.get("newest"),
            ("| " + "; ".join(r["errs"])) if r["errs"] else ""))
    total = sum(r.get("count", 0) for r in results)
    ok = sum(1 for r in results if r["ok"])
    print("\nTOTAL %d revisions across %d articles; %d/%d verified OK" % (total, len(results), ok, len(results)))
    return results

if __name__ == "__main__":
    main()
