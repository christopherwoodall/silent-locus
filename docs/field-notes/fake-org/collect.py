#!/usr/bin/env python3
"""Lane fake-org: "OpenAI Research" + fake-org self-identification hunt.

Idempotent: re-running resumes from state.json — sources already recorded in
`watermark` are skipped; only NEW hits are appended to data/hits.jsonl.
All corpus reads are read-only (stream gz, never decompress to disk).

Patterns: see patterns.md.

Usage:  python3 collect.py
"""
import csv
import gzip
import json
import os
import re
import subprocess
import sys
import urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
HITS = os.path.join(DATA, "hits.jsonl")
STATE = os.path.join(BASE, "state.json")
ARCHIVE = os.path.expanduser(
    "~/workspace/muse-home/projects/swarmtraces-hf-corpus/elastic-exports")
TRANSLUCE = os.path.expanduser(
    "~/workspace/transluce-urlquery/urlquery-agent-activity-2026-09-22-v5")
HFRAW = os.path.expanduser("~/workspace/silent-locus/data/raw/redacted.jsonl.gz")
UQ_CLI = os.path.expanduser("~/workspace/skills/urlquery/bin/uq.py")

ORG_FIELD = r"(org|organization|company|company_name|org_name|orgname|team|team_name|institution|affiliation)"

PATTERNS = [
    ("openai_research",
     re.compile(r"open[ _\-]?ai[ _\-]?research", re.I)),
    ("openai_org_param",
     re.compile(ORG_FIELD + r"\s*[:=]\s*[^,\n&<\"]{0,60}?openai", re.I)),
    ("chatgpt_org_param",
     re.compile(ORG_FIELD + r"\s*[:=]\s*[^,\n&<\"]{0,60}?chatgpt", re.I)),
    ("anthropic_org_param",
     re.compile(ORG_FIELD + r"\s*[:=]\s*[^,\n&<\"]{0,60}?(anthropic|claude)", re.I)),
    ("research_org_param",
     re.compile(ORG_FIELD + r"\s*[:=]\s*[^,\n&<\"]{0,60}?research", re.I)),
    ("oai_prefix_tag",
     re.compile(r"(?:^|[^a-z0-9])oai[-_a-z0-9]", re.I)),
    ("bea_openai",
     re.compile(r"bea\.gov.{0,80}openai|openai.{0,80}bea\.gov", re.I)),
    ("disposable_register",
     re.compile(r"(register|signup|sign-up).{0,120}"
                r"(tempmail|guerrillamail|mailinator|10minutemail|trashmail|"
                r"yopmail|dispostable|throwawaymail|fakeinbox|sharklasers|"
                r"mailsac)", re.I)),
]

SOURCES = {
    "frozen:urlquery-incidents": os.path.join(
        ARCHIVE, "urlquery-incidents-20260928T022324Z.jsonl.gz"),
    "frozen:collusion-wiki": os.path.join(
        ARCHIVE, "collusion-wiki-20260928T025051Z.jsonl.gz"),
    "frozen:rubygems-goimport": os.path.join(
        ARCHIVE, "rubygems-goimport-campaign-20260928T022324Z.jsonl.gz"),
    "transluce-dataset": os.path.join(TRANSLUCE, "all-reports.csv"),
    "swarmtraces:redacted": HFRAW,
}

LIVE_QUERIES = [
    ("openai_research", '"OpenAI Research"'),
    ("bea_openai", '"bea.gov"'),
    ("research_org_param", '"ChatGPT Research"'),
]

QUERY_LOG = os.path.join(DATA, "query-log.json")


def load_state():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh)
    return {"lane": "fake-org", "started_utc": None,
            "watermark": [], "items_collected": 0, "status": "new",
            "notes": []}


def existing_keys():
    keys = set()
    if os.path.exists(HITS):
        with open(HITS, encoding="utf-8") as fh:
            for line in fh:
                try:
                    h = json.loads(line)
                    keys.add((h["pattern"], h["source"], h["record_id"]))
                except Exception:
                    continue
    return keys


def iter_strings(obj, out, depth=0):
    if depth > 8 or len(out) > 4000:
        return
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            iter_strings(v, out, depth + 1)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            iter_strings(v, out, depth + 1)


def fire_patterns(blobs):
    """Return {pattern_id: snippet}."""
    fired = {}
    joined = "\n".join(blobs)
    if len(joined) > 2_000_000:
        joined = joined[:2_000_000]
    for pid, rx in PATTERNS:
        m = rx.search(joined)
        if m:
            start = max(0, m.start() - 60)
            fired[pid] = joined[start:m.end() + 60].replace("\n", " ")[:200]
    return fired


def scan_gz(alias, path, keys, hits):
    scanned = 0
    if not os.path.exists(path):
        print(f"[{alias}] MISSING: {path}", file=sys.stderr)
        return scanned, 0
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            scanned += 1
            try:
                doc = json.loads(line)
            except Exception:
                continue
            src = doc.get("_source", {}) if isinstance(doc, dict) else {}
            blobs = []
            iter_strings(src, blobs)
            fired = fire_patterns(blobs)
            if not fired:
                continue
            rec_id = str(doc.get("_id", "")) if isinstance(doc, dict) else ""
            ts = src.get("@timestamp", "") if isinstance(src, dict) else ""
            for pid, snippet in fired.items():
                key = (pid, alias, rec_id)
                if key in keys:
                    continue
                keys.add(key)
                hits.append({"pattern": pid, "source": alias,
                             "record_id": rec_id, "timestamp": ts,
                             "context_snippet": snippet,
                             "provenance": f"{path} (read-only)"})
    print(f"[{alias}] scanned={scanned}", file=sys.stderr)
    return scanned, 1


def scan_csv(alias, path, keys, hits):
    scanned = 0
    if not os.path.exists(path):
        print(f"[{alias}] MISSING: {path}", file=sys.stderr)
        return scanned, 0
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        for row in csv.DictReader(fh):
            scanned += 1
            blobs = [str(v or "") for v in row.values()]
            fired = fire_patterns(blobs)
            if not fired:
                continue
            rec_id = str(row.get("report_id", ""))
            ts = str(row.get("report_date_utc", ""))
            for pid, snippet in fired.items():
                key = (pid, alias, rec_id)
                if key in keys:
                    continue
                keys.add(key)
                hits.append({"pattern": pid, "source": alias,
                             "record_id": rec_id, "timestamp": ts,
                             "context_snippet": snippet,
                             "provenance": f"{path} (read-only)"})
    print(f"[{alias}] scanned={scanned}", file=sys.stderr)
    return scanned, 1


def scan_redacted(alias, path, keys, hits):
    scanned = 0
    if not os.path.exists(path):
        print(f"[{alias}] MISSING: {path}", file=sys.stderr)
        return scanned, 0
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            scanned += 1
            try:
                doc = json.loads(line)
            except Exception:
                continue
            blobs = [str(doc.get(k, "")) for k in
                     ("text", "tags", "kind", "id", "cite")]
            fired = fire_patterns(blobs)
            if not fired:
                continue
            rec_id = str(doc.get("id", ""))
            ts = str(doc.get("time_utc", "") or "")
            for pid, snippet in fired.items():
                key = (pid, alias, rec_id)
                if key in keys:
                    continue
                keys.add(key)
                hits.append({"pattern": pid, "source": alias,
                             "record_id": rec_id, "timestamp": ts,
                             "context_snippet": snippet,
                             "provenance": f"{path} (read-only)"})
    print(f"[{alias}] scanned={scanned}", file=sys.stderr)
    return scanned, 1


def live_urlquery(pid, query, keys, hits, notes):
    """One polite live urlquery search; failure is a blocker note, not fatal."""
    alias = f"live:urlquery:{urllib.parse.quote(query, safe='')}"
    if not os.path.exists(UQ_CLI):
        notes.append(f"live search skipped: uq.py CLI missing")
        return 0, 0
    try:
        r = subprocess.run(
            [sys.executable, UQ_CLI, "search", "--query", query,
             "--limit", "30"],
            capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        notes.append(f"live search timeout for {query!r}")
        return 0, 0
    if r.returncode != 0:
        err = (r.stderr or "")[:200].replace("\n", " ")
        notes.append(f"live search failed for {query!r}: rc={r.returncode} {err}")
        return 0, 0
    try:
        data = json.loads(r.stdout)
    except Exception:
        notes.append(f"live search unparseable JSON for {query!r}")
        return 0, 0
    results = data.get("reports") or data.get("data") or data.get("results") or []
    if isinstance(results, dict):
        results = results.get("reports", [])
    n = 0
    for rep in results:
        blobs = []
        iter_strings(rep, blobs)
        fired = fire_patterns(blobs)
        if not fired and pid not in fired:
            # the query itself matched at API level; still require pattern fire
            continue
        rec_id = str(rep.get("id") or rep.get("report_id") or "")
        ts = str(rep.get("date") or rep.get("report_date_utc") or "")
        url = str(rep.get("url") or rep.get("report_url") or "")
        for fpid, snippet in fired.items():
            key = (fpid, alias, rec_id)
            if key in keys:
                continue
            keys.add(key)
            hits.append({"pattern": fpid, "source": alias,
                         "record_id": rec_id, "timestamp": ts,
                         "context_snippet": (snippet + " | " + url)[:300],
                         "provenance": f"urlquery public API v1 search "
                                       f"query={query!r} (live, {n+1} of results)"})
            n += 1
    print(f"[{alias}] results={len(results)} pattern-hits={n}", file=sys.stderr)
    return len(results), 1


def save_state(state, watermark, keys, notes):
    from datetime import datetime, timezone
    if not state.get("started_utc"):
        state["started_utc"] = datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
    state["lane"] = "fake-org"
    state["watermark"] = sorted(set(watermark))
    state["items_collected"] = len(keys)
    state["notes"] = notes[-20:]
    state["status"] = "complete" if not notes or all(
        "will retry" not in n for n in notes) else "partial"
    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2)


def append_hits(hits):
    if hits:
        with open(HITS, "a", encoding="utf-8") as fh:
            for h in hits:
                fh.write(json.dumps(h, ensure_ascii=False) + "\n")
def main():
    os.makedirs(DATA, exist_ok=True)
    state = load_state()
    watermark = set(state.get("watermark", []))
    notes = state.get("notes", [])
    keys = existing_keys()
    hits = []

    # --- on-disk corpora (incremental persist: watermark+state saved per source) ---
    for alias, path in SOURCES.items():
        if alias in watermark:
            print(f"[{alias}] SKIPPED (in watermark)", file=sys.stderr)
            continue
        if alias == "transluce-dataset":
            scanned, ok = scan_csv(alias, path, keys, hits)
        elif alias == "swarmtraces:redacted":
            scanned, ok = scan_redacted(alias, path, keys, hits)
        else:
            scanned, ok = scan_gz(alias, path, keys, hits)
        if ok:
            append_hits(hits)
            hits.clear()
            watermark.add(alias)
            save_state(state, watermark, keys, notes)
        else:
            notes.append(f"source {alias} unavailable; will retry next run")

    # --- live urlquery (polite, one small search per pattern family) ---
    for pid, query in LIVE_QUERIES:
        alias = f"live:urlquery:{urllib.parse.quote(query, safe='')}"
        if alias in watermark:
            print(f"[{alias}] SKIPPED (in watermark)", file=sys.stderr)
            continue
        try:
            _, ok = live_urlquery(pid, query, keys, hits, notes)
        except Exception as e:  # never let one live query kill the run
            notes.append(f"live search crashed for {query!r}: {type(e).__name__}")
            save_state(state, watermark, keys, notes)
            continue
        append_hits(hits)
        hits.clear()
        if ok:
            watermark.add(alias)
            save_state(state, watermark, keys, notes)
        # failures stay out of the watermark -> retried next run

    # --- query log (exact queries run) ---
    with open(QUERY_LOG, "w", encoding="utf-8") as fh:
        json.dump({"patterns": [p for p, _ in PATTERNS],
                   "live_queries": [q for _, q in LIVE_QUERIES],
                   "sources": sorted(SOURCES.keys())}, fh, indent=2)

    save_state(state, watermark, keys, notes)
    print(f"run finished", file=sys.stderr)


if __name__ == "__main__":
    main()
