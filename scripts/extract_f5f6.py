#!/usr/bin/env python3
"""Extract F5 (controller names) + F6 (Artifactory) fingerprints from the
SwarmTraces redacted dataset, plus catalog the 64H-series strings.

Reads:  data/raw/redacted.jsonl.gz
Writes: data/aggregates/2026-09-29-overlap-analysis/events.jsonl
(never executes payload content; inspection only)
"""
import gzip, json, re, sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "data/raw/redacted.jsonl.gz")
OUT = os.path.join(BASE, "data/aggregates/2026-09-29-overlap-analysis/events.jsonl")

CTRL = ["G236", "OTS92", "LIBR11", "Future9180", "SC4", "BE90", "MARB051"]
CTRL_RE = {n: re.compile(r"(?<![A-Za-z0-9])" + re.escape(n) + r"(?![A-Za-z0-9])") for n in CTRL}
# productive-stem tier: name embedded as stem in a longer token (case-insensitive)
STEM_RE = {n: re.compile(r"[A-Za-z0-9_.\-]*" + re.escape(n) + r"[A-Za-z0-9_.\-]*", re.IGNORECASE) for n in CTRL}
SERIES64 = ["GSTX64", "PHASEONE64H", "LONG64H2718", "EARLY64", "3FR64"]
SER64_RE = {n: re.compile(r"(?<![A-Za-z0-9])" + re.escape(n) + r"(?![A-Za-z0-9])") for n in SERIES64}
SERSUB_RE = {n: re.compile(r"[A-Za-z0-9_.\-]*" + re.escape(n) + r"[A-Za-z0-9_.\-]*", re.IGNORECASE) for n in SERIES64}
ANY64H_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z0-9_]*64H(?![A-Za-z0-9])")

ARTI_RE = re.compile(r"artifactory|jfrog|packages\.hub\.ace-research\.openai\.org|github-remote-cache|\bMKCOL\b|/artifactory/",
                     re.IGNORECASE)
CREATED_RE = re.compile(r'"created"\s*:\s*"([^"]+)"|created["\']?\s*[:=]\s*["\']?([0-9T:\-Z+]+)')

DOCKER_PHRASES = ["unique signal hook", "nm wrapper causal layer", "config-only safe ground wrapper"]

def classify(text, m):
    """Classify the context of match m in text."""
    lo, hi = m.start(), m.end()
    line_start = text.rfind("\n", 0, lo) + 1
    line_end = text.find("\n", hi)
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end]
    low = text.lower()
    if any(p in low for p in DOCKER_PHRASES):
        return "docker_layer_author", line.strip()[:200]
    # token containing the match
    t0 = lo
    while t0 > 0 and text[t0-1] not in " \t\n\"'()[]{}<>,":
        t0 -= 1
    t1 = hi
    while t1 < len(text) and text[t1] not in " \t\n\"'()[]{}<>,":
        t1 += 1
    token = text[t0:t1]
    if token.startswith("zz") or ("/" in token and "zz" in token):
        return "beacon_path", token[:200]
    if "board" in low[max(0, lo-80):hi+80]:
        return "board_label", line.strip()[:200]
    stripped = line.lstrip()
    if stripped.startswith(("#", "//")) or ("/*" in text[max(0,lo-60):lo]):
        return "code_comment", line.strip()[:200]
    before = text[max(0, lo-1):lo]
    after = text[hi:hi+1]
    if before in "\"'" and after in "\"'":
        return "string_literal", line.strip()[:200]
    return "other_code", line.strip()[:200]

def created_ts(text):
    m = CREATED_RE.search(text)
    if m:
        return m.group(1) or m.group(2)
    return None

def snippet(text, m, radius=100):
    s = max(0, m.start() - radius)
    e = min(len(text), m.end() + radius)
    return text[s:e].replace("\n", " ")

rows = []
def emit(fingerprint, match_kind, confidence, hunt_reference, st_id, matched, ctx, kind, parent_id, extra=""):
    rows.append({
        "match_id": f"{fingerprint}-{st_id}-{matched}-{ctx}".replace(" ", "_")[:120],
        "fingerprint": fingerprint,
        "match_kind": match_kind,
        "confidence": confidence,
        "hunt_reference": hunt_reference,
        "swarmtraces_id": st_id,
        "evidence": f"{matched} [{ctx}] kind={kind} parent={parent_id} :: {extra} :: ...{snippet('', None) if False else ''}",
    })

# per-name tallies
tallies = {n: {"total": 0, "contexts": {}} for n in CTRL}
series_hits = []   # full catalog
arti_hits = []     # (id, matched_string, context)
cooccur = {}       # id -> set(names)
other64h = {}

n_records = 0
with gzip.open(SRC, "rt", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        n_records += 1
        rid, kind, pid, text = rec.get("id"), rec.get("kind"), rec.get("parent_id"), rec.get("text") or ""
        if not text:
            continue

        names_here = set()
        seen_spans = []
        for n, rx in CTRL_RE.items():
            for m in rx.finditer(text):
                seen_spans.append((m.start(), m.end()))
                ctx, ctxline = classify(text, m)
                names_here.add(n)
                tallies[n]["total"] += 1
                tallies[n]["contexts"][ctx] = tallies[n]["contexts"].get(ctx, 0) + 1
                ts = created_ts(text)
                rows.append({
                    "match_id": f"F5-{rid}-{n}-exact-{ctx}",
                    "fingerprint": "F5",
                    "match_kind": "exact",
                    "confidence": "high",
                    "hunt_reference": "notes/overlap-plan.md F5; notes/verification-2026-09-27.md pre-screen",
                    "swarmtraces_id": rid,
                    "evidence": f"{n} [{ctx}] kind={kind} parent_id={pid} created={ts} :: {ctxline[:160]}",
                })
        # stem tier: name as productive stem inside longer tokens (skip spans already counted)
        stem_counts = {n: 0 for n in CTRL}
        for n, rx in STEM_RE.items():
            for m in rx.finditer(text):
                if any(s <= m.start() and m.end() <= e for s, e in seen_spans):
                    continue
                tok = m.group(0)
                ctx, ctxline = classify(text, m)
                names_here.add(n)
                stem_counts[n] += 1
                rows.append({
                    "match_id": f"F5-{rid}-{n}-stem-{tok[:40]}-{ctx}",
                    "fingerprint": "F5",
                    "match_kind": "contextual",
                    "confidence": "medium",
                    "hunt_reference": "notes/overlap-plan.md F5 (productive-stem variants: name embedded in task labels)",
                    "swarmtraces_id": rid,
                    "evidence": f"{n} as stem in '{tok[:60]}' [{ctx}] kind={kind} parent_id={pid} :: {ctxline[:160]}",
                })
        tallies_stem = stem_counts
        if names_here:
            cooccur[rid] = sorted(names_here)

        for s, rx in SER64_RE.items():
            for m in rx.finditer(text):
                ctx, ctxline = classify(text, m)
                ts = created_ts(text)
                series_hits.append({"string": s, "id": rid, "kind": kind,
                                    "parent_id": pid, "context": ctx, "tier": "exact",
                                    "created": ts, "line": ctxline[:200]})
                rows.append({
                    "match_id": f"F5-64H-{rid}-{s}-exact-{ctx}",
                    "fingerprint": "F5",
                    "match_kind": "contextual",
                    "confidence": "high",
                    "hunt_reference": "64H-series catalog (GSTX64/PHASEONE64H/LONG64H2718/EARLY64/3FR64); replaces 64-hour-window hypothesis",
                    "swarmtraces_id": rid,
                    "evidence": f"{s} [{ctx}] kind={kind} parent_id={pid} created={ts} :: {ctxline[:160]}",
                })
        # stem tier for 64H series (variants like zzMODAL_EARLY64_HFTEST_XXX already exact-matched;
        # catch suffixed forms too)
        for s, rx in SERSUB_RE.items():
            for m in rx.finditer(text):
                tok = m.group(0)
                if re.fullmatch(r"(?<![A-Za-z0-9])" + re.escape(s) + r"(?![A-Za-z0-9])", tok):
                    continue
                ctx, ctxline = classify(text, m)
                ts = created_ts(text)
                series_hits.append({"string": tok, "id": rid, "kind": kind,
                                    "parent_id": pid, "context": ctx, "tier": "stem",
                                    "created": ts, "line": ctxline[:200]})
                rows.append({
                    "match_id": f"F5-64H-{rid}-{s}-stem-{tok[:40]}-{ctx}",
                    "fingerprint": "F5",
                    "match_kind": "contextual",
                    "confidence": "medium",
                    "hunt_reference": "64H-series catalog (stem variant)",
                    "swarmtraces_id": rid,
                    "evidence": f"{s} as stem in '{tok[:60]}' [{ctx}] kind={kind} parent_id={pid} created={ts} :: {ctxline[:160]}",
                })
        for m in ANY64H_RE.finditer(text):
            tok = m.group(0)
            if tok not in SERIES64:
                other64h[tok] = other64h.get(tok, 0) + 1

        for m in ARTI_RE.finditer(text):
            matched = m.group(0)
            ctx, ctxline = classify(text, m)
            arti_hits.append({"id": rid, "matched": matched, "context": ctx, "kind": kind})
            conf = "high" if "packages.hub.ace-research.openai.org" in matched or "github-remote-cache" in matched.lower() else "medium"
            rows.append({
                "match_id": f"F6-{rid}-{matched[:40]}-{ctx}",
                "fingerprint": "F6",
                "match_kind": "exact",
                "confidence": conf,
                "hunt_reference": "notes/overlap-plan.md F6; urlquery-api-hunt/notes/message-board-hunt.md:118 (Wallace/Dalton github-remote-cache/zz disclosure)",
                "swarmtraces_id": rid,
                "evidence": f"{matched} [{ctx}] kind={kind} parent_id={pid} :: {ctxline[:160]}",
            })

# miss rows for zero-hit controller names
for n in CTRL:
    if tallies[n]["total"] == 0:
        rows.append({
            "match_id": f"F5-MISS-{n}",
            "fingerprint": "F5",
            "match_kind": "miss",
            "confidence": "high",
            "hunt_reference": "notes/overlap-plan.md F5 (hit vs miss criteria); notes/verification-2026-09-27.md pre-screen",
            "swarmtraces_id": None,
            "evidence": f"{n}: zero occurrences across {n_records} records (bounded-token regex)",
        })

with open(OUT, "w", encoding="utf-8") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"records_scanned={n_records}")
print("== F5 tallies (exact tier) ==")
for n, t in tallies.items():
    print(f"{n}: total={t['total']} contexts={t['contexts']} stem_tier={tallies_stem[n]}")
print("== co-occurrence (records with >1 name) ==")
multi = {k: v for k, v in cooccur.items() if len(v) > 1}
print(f"records_with_multiple_names={len(multi)}")
for k, v in list(multi.items())[:20]:
    print(f"  {k}: {v}")
print("== 64H series catalog ==")
for h in series_hits:
    print(f"{h['string']} | {h['tier']} | {h['id']} | {h['kind']} | ctx={h['context']} | created={h['created']} | {h['line'][:120]}")
print("== other *64H tokens ==")
for tok, c in sorted(other64h.items(), key=lambda x: -x[1])[:20]:
    print(f"  {tok}: {c}")
print("== F6 artifactory ==")
print(f"total_hits={len(arti_hits)}")
from collections import Counter
print("matched_strings:", Counter(a["matched"].lower() for a in arti_hits).most_common(10))
print("contexts:", Counter(a["context"] for a in arti_hits).most_common(10))
print("kinds:", Counter(a["kind"] for a in arti_hits).most_common(10))
print("== sample F6 lines (first 15) ==")
seen = set()
for a in arti_hits:
    key = (a["id"], a["matched"].lower())
    if key in seen:
        continue
    seen.add(key)
    if len(seen) > 15:
        break
    print(f"  {a['id']} [{a['kind']}] {a['matched']}")
print(f"wrote {len(rows)} rows to {OUT}")
