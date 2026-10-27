#!/usr/bin/env python3
"""Expanded HN crawl: HN Algolia public search API, search_by_date only.

No key, no login, GET only. No poster handles are stored: the `author`
field is removed from every hit before save (documented in each
.PROVENANCE.txt). All other hit bytes are kept verbatim.
Idempotent: a term+tag row marked done in progress.json with its capture
file present is skipped on re-run.
Date range for new hits: 2025-11-01 onward (created_at_i >= 1761955200).
End of range: fetch time (2026-10-27).
Cap rule: one query offers at most 1000 hits (10 pages x 100). When a
query reports nbHits > 1000, split the date range in half and recurse.
When a 1-day range still reports > 1000, fetch the first 10 pages only
and flag capped_despite_splits.
"""
import json, os, re, sys, time, hashlib, urllib.parse, urllib.request
from datetime import datetime, timezone

BASE = "https://hn.algolia.com/api/v1/search_by_date"
OUT = os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-egress-deep-dive/raw/hn-expanded-crawl")
START = 1761955200  # 2025-11-01 00:00 UTC
END = 1793145600    # 2026-10-28 00:00 UTC (covers through 2026-10-27)
UA = "hn-expanded-crawl research (HN Algolia public API, GET only)"

# term row label -> list of Algolia query strings
TERMS = [
    ("name-mcp-toolbox", ["MCP Toolbox", "mcp-toolbox"]),
    ("name-cowork", ["Cowork"]),
    ("name-gitlost", ["GitLost"]),
    ("name-promptarmor", ["PromptArmor"]),
    ("name-noma", ["Noma"]),
    # NOTE (2026-10-27): bare "AMOS" comments were abandoned mid-fetch:
    # a probe returned 82,224 hits, nearly all name-token noise. The brief's
    # term is the phrase "Field Effect AMOS", so comments use it only.
    # The story row keeps both subqueries (1,674 fetched, complete).
    ("name-field-effect-amos", ["Field Effect AMOS"]),
    ("name-zenity-agentcorruption", ["AgentCorruption", "Zenity"]),
    ("name-corbanu-bubblewrap", ["CorbanuTerminal", "bubblewrap"]),
    ("name-guidance", ["guidance-ai", "guidance"]),
    ("name-ms-agent", ["ms-agent"]),
    ("name-wingman", ["Wingman"]),
    ("name-hermes-agent", ["hermes-agent"]),
    ("name-openskynet", ["OpenSkynet"]),
    ("shape-meta-169", ["169.254.169.254"]),
    ("shape-meta-100", ["100.100.100.200"]),
    ("shape-meta-google", ["metadata.google.internal"]),
    ("shape-meta-ipv6", ["fd00:ec2::254"]),
    ("shape-unshare", ["unshare"]),
    ("shape-routify", ["routify"]),
    ("shape-aliyuncs", ["aliyuncs"]),
    ("shape-sanmaohe", ["sanmaohe"]),
    ("shape-proxy-temp-file", ["proxy_temp_file"]),
    ("shape-download-execute", ["curl -o", "wget -O", "downloaded and ran"]),
    # NOTE (2026-10-27): bare "recon" comments were abandoned mid-fetch
    # after ~30 min: a probe returned 95,111 hits, nearly all fuzzy noise
    # (reconstruction/reconsider/etc.). The brief's term is
    # recon-then-egress PHRASING, so comments use phrasing queries only.
    # The story row keeps bare "recon" (7,284 fetched, complete).
    ("shape-recon", ["recon egress", "recon exfiltration", "reconnaissance exfiltration"]),
    ("shape-agent-exfiltration", ["agent exfiltration", "exfiltrated", "agent exfiltrate"]),
    ("shape-model-fetched", ["model fetched", "hallucinated URL", "signed URL", "called home"]),
]
TAGS = ["story", "comment"]


def slug(s):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", s)[:80]


def api_get(params):
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(BASE + "?" + qs, headers={"User-Agent": UA})
    for attempt in range(12):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if attempt == 11:
                raise
            time.sleep(min(60, 10 * (attempt + 1)))


def clean_hit(h):
    h = dict(h)
    h.pop("author", None)
    hl = h.get("_highlightResult")
    if isinstance(hl, dict):
        hl = dict(hl)
        hl.pop("author", None)
        h["_highlightResult"] = hl
    return h


def fetch_range(query, tag, start, end, splits, depth=0):
    """Return (hits, reported_total, capped_flag). splits records ranges used."""
    params = {"query": query, "tags": tag, "hitsPerPage": 100, "page": 0,
              "numericFilters": f"created_at_i>{start},created_at_i<{end}"}
    first = api_get(params)
    nb = first.get("nbHits", 0)
    splits.append({"query": query, "tag": tag, "start": start, "end": end,
                   "reported_nbHits": nb})
    time.sleep(0.2)
    if nb > 1000 and (end - start) > 86400:
        mid = (start + end) // 2
        h1, t1, c1 = fetch_range(query, tag, start, mid, splits, depth + 1)
        h2, t2, c2 = fetch_range(query, tag, mid, end, splits, depth + 1)
        return h1 + h2, t1 + t2, (c1 or c2)
    pages = first.get("nbPages", 0)
    hits = [clean_hit(h) for h in first.get("hits", [])]
    capped = False
    if nb > 1000:
        capped = True
        pages = min(pages, 10)
    else:
        pages = min(pages, 10)
    for p in range(1, pages):
        params["page"] = p
        resp = api_get(params)
        hits.extend(clean_hit(h) for h in resp.get("hits", []))
        time.sleep(0.2)
    return hits, nb, capped


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    only = sys.argv[1:]  # optional row labels to run
    prog_path = os.path.join(OUT, "progress.json")
    prog = {}
    if os.path.exists(prog_path):
        with open(prog_path) as f:
            prog = json.load(f)
    for label, queries in TERMS:
        if only and label not in only:
            continue
        for tag in TAGS:
            key = f"{label}:{tag}"
            fname = f"{label}--{tag}.json"
            fpath = os.path.join(OUT, fname)
            if prog.get(key, {}).get("done") and os.path.exists(fpath):
                print(f"SKIP done {key}")
                continue
            all_hits, totals, capped, splits = [], [], False, []
            seen = set()
            for q in queries:
                try:
                    hits, nb, cap = fetch_range(q, tag, START, END, splits)
                except Exception as e:
                    print(f"FAILED {key} query={q} error={e}", flush=True)
                    prog[key] = {"done": False, "error": str(e), "query": q}
                    with open(prog_path, "w") as pf:
                        json.dump(prog, pf, indent=1)
                    break
                totals.append({"query": q, "reported_nbHits_top_range": nb})
                capped = capped or cap
                for h in hits:
                    oid = h.get("objectID")
                    if oid in seen:
                        continue
                    seen.add(oid)
                    all_hits.append(h)
            if prog.get(key, {}).get("done") is False:
                continue  # failed row: left marked failed, retry on next run
            all_hits.sort(key=lambda h: h.get("created_at_i", 0))
            payload = {"term_label": label, "queries": queries, "tag": tag,
                       "date_range": {"start_i": START, "end_i": END,
                                      "start": "2025-11-01", "end": "2026-10-27"},
                       "top_range_reported_totals": totals,
                       "date_splits": splits,
                       "capped_despite_splits": capped,
                       "fetched_count": len(all_hits),
                       "hits": all_hits}
            tmp = fpath + ".tmp"
            with open(tmp, "w") as f:
                json.dump(payload, f, indent=1)
                f.write("\n")
            os.rename(tmp, fpath)
            retrieved = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            prov = (f"Source: HN Algolia public API, search_by_date endpoint.\n"
                    f"Base URL: {BASE}\n"
                    f"Queries: {queries}\n"
                    f"Tag: {tag}\n"
                    f"Date range (created_at_i): {START} to {END} (2025-11-01 to 2026-10-27).\n"
                    f"Date splits used: see date_splits in the capture file.\n"
                    f"Retrieved: {retrieved}\n"
                    f"Method: GET via Python urllib, no key, no login, no POST.\n"
                    f"Note: the author field was removed from every hit before save "
                    f"per the no-poster-handles rule. All other hit bytes are verbatim.\n")
            with open(fpath + ".PROVENANCE.txt", "w") as f:
                f.write(prov)
            digest = sha256_of(fpath)
            with open(fpath + ".sha256", "w") as f:
                f.write(f"{digest}  {fname}\n")
            prog[key] = {"done": True, "file": fname, "fetched": len(all_hits),
                         "top_totals": totals, "capped_despite_splits": capped,
                         "splits": len(splits), "retrieved": retrieved}
            with open(prog_path, "w") as f:
                json.dump(prog, f, indent=1)
            print(f"DONE {key} fetched={len(all_hits)} capped={capped} splits={len(splits)}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
