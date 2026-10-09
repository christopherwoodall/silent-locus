# Top-1000 extension — SCAN LOG

Coordinator: SCAN-1000. Date: 2026-10-05. Study dir:
`~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/`
Scratch clones: `~/workspace/skill-egress-work-1000/` (NEVER committed).
Scanner: `~/workspace/muse-home/projects/skill-tracer/scan/egress_scan.py` (unmodified),
taxonomy `~/workspace/muse-home/projects/skill-tracer/egress-taxonomy.md`.
Scoring: 3×CRITICAL + 2×HIGH + 1×MEDIUM → CRITICAL ≥10 · HIGH ≥6 · MEDIUM ≥3 · LOW ≥1 · NONE 0.

## Enumerated (655 new identities; 1,013 combined)

| lane | method | new | notes |
|---|---|---|---|
| A-ext | 16 GitHub Search queries × pages 2–10, sort=stars, ~8s pacing | 450 | 9,398 items → 8,724 unique → 13 overlapped top-500's 216 → ranked top 450 by stars (~10,595→~1,346). Low-volume queries exhausted before p10. `raw/enum-awesome-ext.md` |
| B-ext | smithery registry pp.4–5 (useCount) · pulsemcp ?page=2,3 · VS Code gallery extensionquery API · mcp.so · mcpso.cc · npm registry search | 205 | 75+70+27+13+8+12. VS Code counts drifted vs lane-B snapshot. cursor.directory: no new entries below lane-B. opencode.ai: no public registry. `raw/enum-marketplaces-ext.md` |

## Fetched (260 repos/packages)

| lane | worker | target | fetched | skipped / failed | notes file |
|---|---|---|---|---|---|
| F1 | FETCH-GH-1 | 46 claude-skill repos | 46/46 | 0 | `raw/fetch-f1-notes.md` |
| F2 | FETCH-GH-2 | 88 mcp repos | 88/88 | 0 (2 transient retries recovered) | `raw/fetch-f2-notes.md` |
| F3 | FETCH-GH-3 | 316 `other` triaged via contents API → cap 60 | 59/60 | 1 skipped: github/gh-aw (clone >300s ×2). 256 triaged out (103 no skill signal, 153 below cap — ranked list kept in lane-f3 `clone-candidates.tsv`) | `raw/fetch-f3-notes.md` |
| H1 | FETCH-MKT-1 | 145 smithery+pulse entries | 16 | 124 skipped (69 remote-only NO SOURCE, 54 unresolvable after npm+GitHub search, 1 repo 404); 1 failed (GitLab clone prompted for creds — not proceeded); 4 already in top-500 lane-e | `raw/fetch-h1-notes.md` |
| H2 | FETCH-MKT-2 | 60 vsc+mcp.so+mcpso+npm | 51 | 8 NO SOURCE (vendor-hosted SaaS, no public repo); 1 skipped (microsoft/wcgw — full coding-agent repo, out of scope per lane-E precedent) | `raw/fetch-h2-notes.md` |

All fetches: public sources only, `git clone --depth 1` / static tarball/.vsix unpack, ~2s pacing (up to 4-way parallel where tolerated), no auth, nothing installed or executed. VS Code `.vsix` quirk: `vspackage` endpoint returns gzip-wrapped content — gunzip before unzip.

## Scanned

| lane | scan file | units | with hits |
|---|---|---|---|
| F1 | `raw/scan-d1.json` | 1,772 | 411 |
| F2 | `raw/scan-d2.json` | 304 | 153 |
| F3 | `raw/scan-d3.json` | 343 | 122 |
| H1 | `raw/scan-f1.json` | 27 | 17 |
| H2 | `raw/scan-f2.json` | 44 | 38 |
| **new total** | | **2,490** | **741** |
| combined w/ top-500 | | 6,343 | 1,541 |

## Analysis
- `raw/known-url-hunt.md` — known-URL set hunt across the 5 new scan JSONs (per-skill hits, code vs fixture/doc grading)
- `raw/new-urls.md` — new-domain extraction (new lanes vs top-500 lanes), ranked, classified, cousin-flags
- `EGRESS_MAP.md` — ranked destinations + corpus verdicts for the extension (top-500 verdicts referenced, not re-derived)

## Evidence policy
Full observed values retained in scan JSONs (never redacted); secrets noted, never used. Grades: confirmed (bytes present) / pattern-match (corpus tradecraft grammar). A high score is NOT an accusation — dual-use network surface on legitimate tools.
