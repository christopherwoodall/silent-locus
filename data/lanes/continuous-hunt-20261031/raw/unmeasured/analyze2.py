#!/usr/bin/env python3
"""Second analysis: in-window counts, title-match screen, Codex anomaly
probe, PR-shape checks. Aggregate only; no logins, titles, URLs, bodies."""
import json, os
from collections import Counter
D = os.path.dirname(os.path.abspath(__file__))

def load(f):
    with open(os.path.join(D, f)) as fh:
        return json.load(fh)

# --- Codex anomaly probe ---
rows = load("gh-commits-codex.json")
print("codex row keys:", sorted(rows[0].keys()) if rows else "EMPTY")
print("codex commit keys:", sorted(rows[0]["commit"].keys()) if rows else "")
n_codex_any = sum(1 for r in rows if "codex" in json.dumps(r).lower())
n_msg_codex = sum(1 for r in rows if "codex" in (r["commit"]["message"] or "").lower())
n_coauth = sum(1 for r in rows if "co-authored-by" in (r["commit"]["message"] or "").lower())
lens = sorted(len(r["commit"]["message"] or "") for r in rows)
print(f"codex: rows_with_codex_anywhere_in_row={n_codex_any}/30 "
      f"in_message={n_msg_codex}/30 coauthored_any={n_coauth}/30 "
      f"message_len_min={lens[0]} median={lens[15]} max={lens[-1]}")
print("codex author field keys:", sorted((rows[0].get("author") or {}).keys()))
print("codex committer==author login (bool per row, distinct values):",
      Counter(r.get("author", {}).get("login") == r.get("committer", {}).get("login") for r in rows))
print("codex repository keys:", sorted(rows[0]["repository"].keys()))
repkey = "nameWithOwner" if "nameWithOwner" in rows[0]["repository"] else sorted(rows[0]["repository"].keys())[0]
print("codex repository distinct:", len({str(r["repository"].get(repkey)) for r in rows}))
print("codex commit.author.name distinct:", len({r["commit"]["author"]["name"] for r in rows}))
n_codex_footer = sum(1 for r in rows if "co-authored-by: codex" in (r["commit"]["message"] or "").lower())
print(f"codex: codex_coauthor_footer_lowercase={n_codex_footer}/30")

# --- PR shape checks ---
for f, phrase in [("gh-prs-claudecode.json", "generated with claude code"),
                  ("gh-prs-agent-harness.json", "agent harness")]:
    rs = load(f)
    print(f"{f}: row keys={sorted(rs[0].keys())}")
    inwin = sum(1 for r in rs if (r.get("createdAt") or "") >= "2025-11-01")
    tmatch = sum(1 for r in rs if phrase in (r.get("title") or "").lower())
    extra = ""
    if "body" in rs[0]:
        bmatch = sum(1 for r in rs if phrase in (r.get("body") or "").lower())
        extra = f" body_match={bmatch}/30"
    print(f"{f}: in_window={inwin}/30 title_match={tmatch}/30{extra}")

# --- Phrase screens: in-window + title-match ---
import glob
phrases = {}
for line in open(os.path.join(D, "phrase-map.tsv")):
    n, ph, out = line.strip().split("|")
    phrases[out] = ph
for f in sorted(glob.glob(os.path.join(D, "phrase-*.json"))):
    base = os.path.basename(f)
    rs = load(base)
    ph = phrases[base].lower()
    inwin = sum(1 for r in rs if (r.get("createdAt") or "") >= "2025-11-01")
    tmatch = sum(1 for r in rs if ph in (r.get("title") or "").lower())
    print(f"{base}: rows={len(rs)} in_window={inwin} title_match={tmatch}")
