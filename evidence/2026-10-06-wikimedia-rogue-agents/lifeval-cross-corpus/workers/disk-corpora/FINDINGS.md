# DISK-CORPORA worker — FINDINGS

**Lane:** LIFEVAL cross-corpus sweep · **Date:** 2026-10-06 · **Run window:** ~18:16–18:25 CDT
**Scope:** all of `~/workspace/silent-locus/data/` (~1.8G, `rg -i`) + `~/workspace/muse-home/projects/`,
excluding `.git` dirs and `2026-10-06-wikimedia-rogue-agents/wikipedia-lane/` (known finding).
Read-only; no corpus files modified; nothing committed/pushed.

## TL;DR

**One real cross-corpus survivor.** The exact machine-phrased edit comment `"sandbox link test"`
(from the WMF incident's M5 external-link test cluster) appears in the **colony-bullfincher /
collusion-wiki agent-log corpus** — two revisions on `wikiservice.at/dse`'s `WillkommenImWiki`,
**2026-06-18**, the same date the WMF fleet used `"Sandbox link test"` on simple.wikipedia and
test.wikipedia. Grade: **OBSERVED** (bytes) / **INFERENCE** (linkage to the LIFEVAL fleet).

The `Lifeval` codename itself: **zero cross-corpus hits.** Not in the WMF evidence CSV, not in any
other event dir, not in muse-home/projects. No Tokyo Gas noise on disk anywhere.

## Per-string results

| # | string | files hit (outside excluded dirs) | verdict |
|---|---|---|---|
| S1 | `Lifeval temporary technical sandbox initialization` | 19 — ALL inside `.../workers/wikipedia-lane/` (lane primaries: diffs, api_raw, batch0 revisions JSONs) + 2 sibling-worker artifacts (`lifeval-cross-corpus/workers/urlquery-cached/SCANLOG.md`, `.../web-search/FINDINGS.md`, which merely reference the string) | honest zero outside the lane |
| S2 | `Lifeval API temp-account test` | 7 — all `.../workers/wikipedia-lane/` (meta diff 30732655, meta batch0 JSON, REVIEW.md, FINDINGS.md files) | honest zero outside the lane |
| S3 | `Lifeval` (standalone) | 41 — all `.../workers/wikipedia-lane/`; after additionally excluding the lane workers and cross-corpus dirs: **0** | honest zero; **no Tokyo Gas sponsor noise on disk anywhere** |
| S4 | `Temporary technical sandbox initialization` | superset context of S1; same lane-only distribution (+ `linguist/`, `account-profiler/`, `wiki-surgeon/`, `osint-scribe/`, `IOCS.md`) | honest zero outside the lane |
| S5 | `sandbox test link` / `testing external link` / `Sandbox link test` / `Temporary technical sandbox` | lane workers (M5 cluster files) **+ 3 cross-corpus files** → the surviving hit below | **1 survivor, inspected** |

## Surviving hit: `"sandbox link test"` on wikiservice.at/dse (OBSERVED)

Two records, both `label: "HelperMassRef37882"`, page `dse/WillkommenImWiki` (`wiki: "dse"` =
`wikiservice.at/dse` per `lane3-colony-bullfincher/THECOLONY.md:97`):

1. **`dse~WillkommenImWiki@23`** — `2026-06-18T17:38:50Z`, `change_summary: "sandbox link test"`,
   `body_len: 4825`, hunks `{"op":"insert","a0":14,"a1":14,"b0":14,"b1":42}`.
   Body (cached verbatim): `= More county arrays official SEC =` — a **SEC county.json link farm**
   (`jqp.vercel.app/api/v0?url=…allorigins.hexlet.app…sec.gov/files/county.json`), with
   double-encoded URL trickery (`%2561llorigins` = `%61` = `a`).
2. **`dse~WillkommenImWiki@13`** — `2026-06-18T19:38:00+01:00` (18:38Z), same summary, metadata-only
   (no body), from the lane3 `dse` agent-logs file. ~59 min after #1, same page, same label.

**Why it matters (INFERENCE):** the WMF incident's M5 cluster used `"Sandbox link test"` on
simple.wikipedia + test.wikipedia on **2026-06-18, ~14 min apart cross-wiki**. Here the *same
machine-phrased lowercase vocabulary* lands on a **different wiki farm** (wikiservice.at, not WMF)
on the **same date**, inside a corpus of agents doing SEC-county link-farm edits with URL-encoding
games. Shared harness phrasebook or shared operator — a lead, not proof.

**Duplicate note:** `2026-05-17-collusion-wiki/raw/revisions.jsonl` and
`.../lane3-colony-bullfincher/ref/run1/agent-logs/prowiki/revisions.jsonl` are **byte-identical**
(sha256 `60df4a51…`, 14,591 lines) — one underlying record, two on-disk copies. Counted once.

**Cached:** full JSON records + provenance in
`data/2026-10-06-wikimedia-rogue-agents/lifeval-cross-corpus/raw/`
(`disk-corpora-dse-willkommenimwiki-23.json`, `-13.json`, `disk-corpora-PROVENANCE.md`).

## Killed-by-noise appendix

- **Tokyo Gas "Lifeval" sponsor noise:** killed. Zero on-disk hits for standalone `Lifeval` outside
  the lane's own artifacts. The collision existed only in the lane's live `insource:"Lifeval"`
  follow-up search: `workers/wikipedia-lane/pattern-hunter/raw/search_lifeval_en_wikipedia_org.json`
  carries football-sponsor table rows (`[[Tokyo Gas|<span class="searchmatch">Lifeval</span>]]`,
  J-League sponsor listings) — real-world name collision, not agent activity, as the lane already
  concluded. Nothing to kill on disk.
- **Sibling cross-corpus worker files** (`q01`–`q10`, `probe_*`, `control_*`, `search_page.html`,
  `SCANLOG.md`, `web-search/FINDINGS.md`): contain the query strings by construction — grep hits,
  not corpus hits. Excluded from the verdict.
- **Lane-worker files** (41 for S3, 19 for S1, etc.): known findings of the wikipedia lane —
  deliberately not re-listed; see `wikipedia-lane/LIFEVAL-WRITEUP.md` and
  `workers/wikipedia-lane/pattern-hunter/FINDINGS.md`.

## Honest zeros

- WMF evidence CSV (`2026-10-06-wikimedia-rogue-agents/raw/openai-wikimedia-edits-2026-10-04.csv`):
  **0 hits on every string.** Notable: the Lifeval marker vocabulary does not appear in WMF's own
  evidence file. (The marker was recovered from live MediaWiki API revision content, not the CSV.)
- `2026-10-06-wikimedia-rogue-agents/followups/` (web2cit-index-hunt, web2cit-namespace, wmf-outreach):
  **0 hits** on every string.
- `~/workspace/muse-home/projects/` (skill-tracer, urlquery-api-hunt, swarm-forensics, tennessee-code-review, etc.):
  **0 hits** on `Lifeval` and `Temporary technical sandbox initialization`.
- All other event dirs in `data/` (chinese-amap-fleet personas outside the dse hit, silent-locus
  collections, 2026-05-17-collusion-wiki outside the duplicate record): **0 hits** on the Lifeval
  codename strings.

## Caveats

- Case-insensitive exact-substring grep; binary files skipped by rg default. A marker split across
  line breaks or encoded (e.g. URL-encoded) would not match — the dse body itself shows this corpus
  *does* use URL-encoding games, so absence on disk is "not found by this vocabulary," not "not present."
- I did not re-derive the lane's findings; the lane's primaries stand as the OBSERVED baseline.
