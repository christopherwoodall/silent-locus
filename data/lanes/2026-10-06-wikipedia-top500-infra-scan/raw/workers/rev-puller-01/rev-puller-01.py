#!/usr/bin/env python3
"""REV-PULLER-01: pull revision history for chunk-01 articles.

HTTP via curl ONLY (this VM's Python HTTP stacks break on the egress proxy).
python3 used solely for URL-encoding (urllib.parse.quote) and JSON processing.

Methodology: ~/workspace/silent-locus/docs/methodology.md
  - Pace <=1 request per 5s to en.wikipedia.org
  - UA: silent-locus-top500-scan/1.0 (research)
  - Log, don't stop: one failure never kills the chunk.
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone

EVENT = os.path.expanduser(
    "~/workspace/silent-locus-top500/data/2026-10-06-wikipedia-top500-infra-scan")
CHUNK = os.path.join(EVENT, "raw", "chunks", "chunk-01")
OUTDIR = os.path.join(EVENT, "raw", "revisions")
WORKER = os.path.join(EVENT, "raw", "workers", "rev-puller-01")
ERRLOG = os.path.join(WORKER, "errors.log")
FINDINGS = os.path.join(WORKER, "FINDINGS.md")

UA = "silent-locus-top500-scan/1.0 (research)"
PACE_S = 5.0
MAX_RETRIES = 3
RETRY_WAIT_S = 30

BASE = ("https://en.wikipedia.org/w/api.php?action=query&prop=revisions"
        "&rvprop=user%7Ctimestamp%7Cids%7Ccomment%7Ctags%7Csize"
        "&rvlimit=500&rvdir=older"
        "&rvstart=2026-10-07T00%3A00%3A00Z&rvend=2020-01-01T00%3A00%3A00Z"
        "&format=json&formatversion=2")


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)


def errlog(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(ERRLOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")


def fetch(url, rank, title):
    """One API request via curl. Returns (data_dict, error_str)."""
    for attempt in range(1, MAX_RETRIES + 1):
        if attempt > 1:
            time.sleep(RETRY_WAIT_S)
        else:
            time.sleep(PACE_S)  # pace every request, including the first
        try:
            p = subprocess.run(
                ["curl", "-sS", "--max-time", "90", "-A", UA,
                 "-w", "\n%{http_code}", url],
                capture_output=True, text=True, timeout=120)
        except Exception as e:  # noqa: BLE001
            err = f"rank={rank} title={title!r} curl exception attempt={attempt}: {e}"
            log("WARN " + err)
            continue
        out = p.stdout.rstrip("\n")
        if not out:
            err = (f"rank={rank} title={title!r} attempt={attempt}: empty response "
                   f"(rc={p.returncode} stderr={p.stderr.strip()[:200]})")
            log("WARN " + err)
            continue
        try:
            code = int(out.rsplit("\n", 1)[-1])
            body = out.rsplit("\n", 1)[0]
        except ValueError:
            log(f"WARN rank={rank} title={title!r} attempt={attempt}: unparsable http code")
            continue
        if code == 429:
            log(f"WARN rank={rank} attempt={attempt}: HTTP 429, backing off")
            time.sleep(RETRY_WAIT_S)
            continue
        if code != 200:
            log(f"WARN rank={rank} title={title!r} attempt={attempt}: HTTP {code}")
            continue
        try:
            data = json.loads(body)
        except json.JSONDecodeError as e:
            log(f"WARN rank={rank} attempt={attempt}: bad JSON: {e}")
            continue
        if "error" in data:
            log(f"WARN rank={rank} attempt={attempt}: API error: {data['error']}")
            continue
        if "warnings" in data:
            log(f"NOTE rank={rank} API warnings: {json.dumps(data['warnings'])[:200]}")
        return data, ""
    final = f"FAILED rank={rank} title={title!r} after {MAX_RETRIES} attempts"
    log("ERROR " + final)
    errlog(final)
    return None, final


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(WORKER, exist_ok=True)
    t0 = time.time()
    log("REV-PULLER-01 starting")

    with open(CHUNK) as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]

    results = []   # (rank, title, count or None-on-failure, requests)
    total_revs = 0
    total_reqs = 0
    failures = 0

    for ln in lines:
        rank_s, title = ln.split("\t", 1)
        rank = int(rank_s)
        enc = urllib.parse.quote(title, safe="")
        url = f"{BASE}&titles={enc}"
        outpath = os.path.join(OUTDIR, f"{rank}.jsonl")
        if os.path.exists(outpath) and os.path.getsize(outpath) > 0:
            log(f"SKIP rank={rank} {title!r}: already cached ({os.path.getsize(outpath)} bytes)")
            continue

        count = 0
        reqs = 0
        cont = None
        failed = False
        with open(outpath, "w") as out:
            while True:
                rurl = url if cont is None else url + "&rvcontinue=" + urllib.parse.quote(cont, safe="")
                data, errm = fetch(rurl, rank, title)
                reqs += 1
                total_reqs += 1
                if data is None:
                    failed = True
                    break
                pages = data.get("query", {}).get("pages", [])
                if not pages:
                    msg = f"FAILED rank={rank} title={title!r}: no pages in response"
                    log("ERROR " + msg); errlog(msg)
                    failed = True
                    break
                page = pages[0]
                if page.get("missing"):
                    msg = f"FAILED rank={rank} title={title!r}: article missing (deleted/renamed)"
                    log("ERROR " + msg); errlog(msg)
                    failed = True
                    break
                for rev in page.get("revisions", []):
                    out.write(json.dumps({
                        "rank": rank,
                        "article": title,
                        "revid": rev.get("revid"),
                        "parentid": rev.get("parentid"),
                        "user": rev.get("user"),
                        "timestamp": rev.get("timestamp"),
                        "comment": rev.get("comment"),
                        "tags": rev.get("tags", []),
                        "size": rev.get("size"),
                    }, ensure_ascii=False) + "\n")
                    count += 1
                cont = (data.get("continue") or {}).get("rvcontinue")
                if not cont:
                    break
        if failed:
            failures += 1
            if os.path.exists(outpath) and os.path.getsize(outpath) == 0:
                os.remove(outpath)  # no partial cache on failure
            results.append((rank, title, None, reqs))
            continue
        total_revs += count
        log(f"OK rank={rank} {title!r}: {count} revisions, {reqs} requests")
        results.append((rank, title, count, reqs))

    wall = time.time() - t0
    # FINDINGS.md
    with open(FINDINGS, "w") as f:
        f.write("# rev-puller-01 FINDINGS — chunk-01 revision pulls\n\n")
        f.write(f"- Worker: rev-puller-01 (branch `wikipedia-top500-infra-scan-2026-10-06`)\n")
        f.write(f"- Run start: {datetime.fromtimestamp(t0, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n")
        f.write(f"- Run end: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n")
        f.write(f"- Wall time: {wall/60:.1f} min ({wall:.0f} s)\n")
        f.write(f"- Articles in chunk: {len(results)}\n")
        f.write(f"- Articles pulled OK: {sum(1 for r in results if r[2] is not None)}\n")
        f.write(f"- Articles failed: {failures}\n")
        f.write(f"- Total API requests: {total_reqs}\n")
        f.write(f"- Total revisions cached: {total_revs}\n")
        f.write(f"- Window: rvstart=2026-10-07T00:00:00Z (older), rvend=2020-01-01T00:00:00Z, rvlimit=500\n")
        f.write(f"- UA: {UA}; pacing 1 req / 5 s; curl-only HTTP\n\n")
        f.write("## Per-article revision counts\n\n")
        f.write("| rank | article | revisions | api_requests | cache |\n")
        f.write("|------|---------|-----------|--------------|-------|\n")
        for rank, title, count, reqs in results:
            c = str(count) if count is not None else "FAILED"
            cache = f"raw/revisions/{rank}.jsonl" if count is not None else "—"
            f.write(f"| {rank} | {title} | {c} | {reqs} | {cache} |\n")
        f.write("\n## Failures\n\n")
        if failures:
            f.write(f"{failures} article(s) failed — see errors.log for detail. "
                    "Partial JSONL removed on failure; safe to re-run (skip-on-existing).\n")
        else:
            f.write("None.\n")
    log(f"DONE: {total_revs} revisions, {failures} failures, {wall/60:.1f} min, FINDINGS.md written")


if __name__ == "__main__":
    main()
