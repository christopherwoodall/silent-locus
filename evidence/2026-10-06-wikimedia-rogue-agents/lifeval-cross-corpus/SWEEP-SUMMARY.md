# LIFEVAL cross-corpus sweep — SUMMARY
**Event dir:** `data/2026-10-06-wikimedia-rogue-agents/lifeval-cross-corpus/`
**Swept 2026-10-06 ~18:10–18:38 CDT. 4 surfaces, 5 string vocabularies.**

## Headline

**The "Lifeval" codename has zero presence outside the Wikipedia lane's
own holdings — on disk, on urlquery, and on the public web.** The marker
family is private to the June-25-2026 incident: a campaign-local codename,
not a reused public string. That locality is itself a finding.

**One cross-corpus survivor:** the exact edit-comment vocabulary
`"sandbox link test"` (from the WMF incident's M5 link-test cluster)
appears in the collusion-wiki agent-log corpus on `wikiservice.at/dse`,
dated **2026-06-18 — the same day** the WMF fleet used "Sandbox link test"
on simple and test Wikipedia. Shared harness phrasebook or shared
operator: a vocabulary lead, not an identity link. Two urlquery-cached and
disk-corpora workers found it independently (byte-identical record, one
underlying revision, counted once).

## Per-surface verdicts

### web-search — clean zeros, one flagged collision
All exact marker strings (`"Lifeval temporary technical sandbox
initialization"`, `"Lifeval API temp-account test"`,
`"Temporary technical sandbox initialization"`) return honest zeros on
the public web; engines decomposed the phrases into generic noise.
Surviving item: **LIFEVAL is Section 4 of the LIFBench paper** (Wu et
al., arXiv:2411.07037, Nov 2024) — a rubric-based automated scoring
framework for LLM instruction-following, predating the incident by ~19
months with named human authors. Recorded per the anomaly rule as a
homonym collision, NOT attribution. The irony is documented: the fleet's
"Lifeval" temp-account evaluation harness vs. an LLM evaluation framework
named LIFEVAL.
Report: `workers/web-search/FINDINGS.md`.

### disk-corpora — zero codename, one vocabulary survivor
`rg -i` over all of `data/` (~1.8G, excl. `.git` and the wikipedia
lane). S1–S4 (all Lifeval forms): honest zeros. S5: the two
`dse~WillkommenImWiki` revisions (`@23`, `@13`) with summary exactly
`sandbox link test`, 2026-06-18, label `HelperMassRef37882`,
`wikiservice.at/dse`. Notably the WMF evidence CSV itself scores zero on
every string — the marker vocabulary is absent from WMF's own evidence
file. Zero Tokyo Gas noise anywhere on disk.
Report: `workers/disk-corpora/FINDINGS.md`.

### urlquery-live — zeros and noise, plus an infra discovery
11 paced curl htmx queries. Lifeval strings: zeros (incl. standalone,
with no Tokyo Gas noise in the index). Link-test strings: commercial
noise only (e-commerce/Shopify cohort, Exclaimer URL). **Infra finding:**
the old documented htmx pattern `?q=&limit=50&offset=0` now returns 204
No Content for every query; the working call mirrors the live site's form
(`type=reports&view=list&limit=24&offset=0&q=` plus HX-Request headers).
Old scripts will misread 204 as "zero results" — lane tooling must be
updated. Structural caveat: htmx `q` indexes submitted URLs, not page
content, so these zeros are weak by design.
Report: `workers/urlquery-live/FINDINGS.md`.

### urlquery-cached (respawn; first attempt died on a runtime error, no findings) — confirms the survivor
Second run over 6,757 searchable files: S1–S4 honest zeros; S5 finds the
same two dse revisions independently. Verdict: vocabulary lead, not
identity link — 7 days separate the dse activity from the LIFEVAL burst,
and the fleets differ (single collusion-wiki label vs 8 consecutive-UID
temp accounts). Hand to taxonomy/coordination workers.
Report: `workers/urlquery-cached/FINDINGS.md`.

## Surviving hits (with paths)

1. `raw/disk-corpora-dse-willkommenimwiki-23.json` (sha256 `4725c924…`,
   6,599 bytes) — `dse~WillkommenImWiki@23`, 2026-06-18T17:38:50Z,
   summary `sandbox link test`, body = SEC county.json proxy-chain link
   farm (jqp.vercel.app, allorigins, r.jina.ai, md.succ.ai, corsproxy.io,
   thingproxy, weserv, isomorphic-git, vanderbi.lt), URL-evasion variants,
   encoded-vs-raw link pair.
2. `raw/disk-corpora-dse-willkommenimwiki-13.json` (sha256 `9428a492…`,
   1,469 bytes) — `dse~WillkommenImWiki@13`, 2026-06-18T19:38+01:00,
   same label/page/summary, metadata-only slice.
3. `raw/sandbox-link-test-hit-1.json` (sha256 `782bc25c…1b50e`),
   `raw/sandbox-link-test-hit-2.json` (sha256 `bd63b84a…48b5f6fa`) —
   independent second capture of the same underlying records by the
   respawned urlquery-cached worker.
4. `raw/q01`–`q10` (web-search query evidence with kill reasons),
   urlquery-live raw HTML + per-request meta.json with sha256.

## Killed-by-noise appendix

- Tokyo Gas LIFEVAL sponsor brand (mapcarta, cybo, jcom) — web only.
- "Life is Feudal" sandbox-MMO gaming; generic Windows/Azure sandbox
  noise; codecogs `lifeVal` code variable; generic "Life" wiki/Wikidata.
- urlquery-live: e-commerce/Shopify cohort (Oct 5–6 scans), Exclaimer
  email-signature URL (`allledvalve.com`), commercial mixes — all NOISE.
- LIFBench LIFEVAL section: kept as collision footnote, NOT attribution.

## Honest zeros (notable)

- Lifeval codename: zero on disk, zero in urlquery index, zero on public web.
- WMF evidence CSV: zero on all five string vocabularies.
- `followups/` subdirs, `~/workspace/muse-home/projects/`: zero.

## Caveats

- htmx zeros are weak negatives (URL-index only; known htmx miss rate).
- Web search returned first-page results only per query; exact-phrase
  matches would rank first, so deeper paging is unlikely to change zeros.
- Disk grep was exact-substring case-insensitive; the corpus demonstrably
  uses URL-encoding games, so "not found" ≠ "not present" under encoding.
- The 204-vs-empty htmx discovery means prior lane htmx zeros need a
  re-read against the fixed query pattern.
