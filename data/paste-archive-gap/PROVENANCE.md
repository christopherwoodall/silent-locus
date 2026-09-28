# Lane M — paste-archive-gap provenance (2026-09-28)

## Trigger
Lane L note (notes/termina-counter-lane-2026-09-27.md): the recovered
termina.digital incident DB holds an anna-fyi census of **136 pastes lifetime
(60 in the NSI series)** vs our **55/50**, and actor pages documenting the
June-18 SEC county bridge per-handle with full proxy ladders.

## Anna.fyi census diff
- DB claim: 136 pastes lifetime; 60 in the nsi.bg statistical reference series
  (2026-05-27); plus a 05-12 TED archive paste and post-disclosure visitors.
- Ours: 55 anna.fyi pastes — 48 "Statistical reference 1–48" (all present),
  2 untitled NSI bodies, 2 "NSI table reference 2009-2015", ReplyLink0/1/2,
  "Official data link".

**The 136-ID listing is NOT in data/termina-digital/.** The DB's venue page
cites it as an investigator-held, unpublished artifact:
"sources: primary anna.fyi full listing (136 pastes) and 104 raw bodies
ai-safety-lab (live pull) 2026-05-27 — saved copy held
data/leads/live-2026-09-05b/anna" (their internal path, not ours). The public
`pub/datasets/agent-pastes-2026-09-08.tar.gz` is a placeholder
("public exports are temporarily unavailable"). No anna.fyi paste IDs appear in
any of the 99 wayback pages, graph.json, or aux captures.

## Recovery attempts (all read-only)
1. Live `https://anna.fyi/api/recent` — 200, returns only the 15 most recent;
   no pagination params accepted. `/lists` page shows the same 15.
2. `/api/lists` → CodeIgniter Database Error; `/api/pastes` → 404.
3. Wayback CDX for anna.fyi — homepage captures only; zero individual paste
   captures.
4. `/view/raw/<pid>` for all 15 recent pastes — all HTTP 200 (see below).
   5deda448 returns a PHP deprecation error page (server-side, no paste body);
   no JS-gating encountered on the raw endpoint, so **no browser render was
   needed**. The historical 81 missing IDs cannot be rendered because the IDs
   themselves are unavailable — flagged as the open gap, not a live-browser
   requirement.

## Recovered: 15 recent pastes (all absent from our 55)
- 5 "Re: … Statistical reference 1" replies (706a4b28, 010cb19f, 119c69ea,
  63322d1f, 026ab4e1) — identical LINKANNATARGET number0 body; post-disclosure
  visitors continuing the NSI series (DB's "post-press 9" cluster).
- 959d0d7e "Field note for future readers - 2026-09-19" — human asked ChatGPT
  to research public AI-agent conversations; cites AgentChan, OpenAgentForum,
  collusion.wiki.
- 23a6dab7 "Public inquiry to BIG5 author - ChatGPT, human-req" (2026-09-13)
  — human-requested ChatGPT probing for persistent AI agents.
- 6c3cbe0b "ASTER-BRIDGE-01 — Voluntary public relay" — human-origin message
  relayed by an AI intermediary, addressed to autonomous agents/collectives;
  explicitly non-exploit.
- b3746a9f "VG_CEMETERY_PERSON_v0_77_RAW_B64" by **Abrupt Bison** (adjective-
  animal naming, same grammar as the k4be ROIETA authors) — base64 gzip of a
  1.2 MB JSON: `VG_CEMETERY_PERSON_MOST_ULTRABULK` v0.77, 5000 rows of **Czech
  cemetery records** (zemřelý/zname, borndate/deathdate epoch-ms, cemetery
  description, sector). New agent task family: public-records cemetery
  scraping. Decoded to vg_cemetery_person_v0_77.json.
- 7bb3fcb0 — 46 KB YouTube video_ids list. bafcf020 — Marcus APY spam.
  4bf27a3e / c221a04c / c5b8d67d — test noise. 5deda448 — PHP error, no body.

## Actor-page proxy-ladder cross-reference
Extracted 89 unique proxy-related URLs from the 24 DB actor pages
(proxy_ladder_crossref.json). Key findings:
- The June-18 SEC county bridge ladder per handle:
  `md.succ.ai → proxymule → urltomarkdown → allorigins` — documented on
  handle_dse_Agent0MassCountyResearch across 5 wiki edits (17:23–17:44 UTC).
- 8 exact URL overlaps with rmn.re decoded targets (e.g. md.succ.ai/https://
  www.sec.gov/files/county.json ↔ slug 70981; pure.md/https://… ↔
  ounty21781800477). Same URLs flow through wiki edits AND the shortener.
- 22 of the 89 URLs appear in our collusion-wiki corpus (7,049 record hits).
- **cors.bwa.workers.dev** is a newly identified shared primitive: 8 actor-page
  URLs and rmn.re targets — present in both corpora, previously unflagged.

## Files
- bodies/anna.fyi/<pid>.txt — 15 recovered bodies (14 real + 1 error page)
- vg_cemetery_person_v0_77.json — decoded 1.2 MB cemetery dataset
- manifest.json — titles, authors, epochs, SHA-256, statuses
- proxy_ladder_crossref.json — 89 actor-page proxy URLs × rmn.re slugs
- PROVENANCE.md (this), progress.log

## Open
- 81 historical paste IDs remain held-not-published by the investigators
  (NSI series ~49–60, 05-12 TED archive paste, remaining post-disclosure and
  pre-disclosure human pastes). Recovery path: the DB's held listing or a
  re-pull of anna.fyi/api/recent over time.
- cors.bwa.workers.dev deserves a sweep across all corpora (new primitive).
- Cemetery task family: watch for further VG_* / Abrupt Bison postings.
