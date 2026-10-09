# archive-diver FINDINGS — Wikimedia rogue-agent hunt
Lane: ARCHIVE-DIVER | Branch: wikimedia-rogue-agents-2026-10-06
Work dir: data/2026-10-06-wikimedia-rogue-agents/
Seed: https://diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/
Started: 2026-10-06 ~11:35 CDT

Grade key: OBSERVED = bytes I fetched; INFERENCE = reasoned link; UPSTREAM ASSERTION = someone else's claim.
Rule: passive/public OSINT only; CDX/API queries only (curl); NEVER live-fetch candidate suspicious URLs (log them); NEVER redact evidence (annotate sensitivity).
Methodology: map the archive's coverage window BEFORE drawing conclusions. A CDX zero is a weak negative, never a clean zero. Positive-control recall check required before any negative.

## Incident window (UPSTREAM ASSERTION, from seed article + press)
- Incident activity: agent traffic spring/summer 2026; WDQS partial outage May 7-11 2026.
- Disclosure: Wikimedia Diff blog published 2026-10-05.
- "Predates the incident window" here = captures dated before 2026-05-01 (pre-activity), and note any captures between May and Oct disclosure.

## Targets
1. Seed article: https://diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/ (OBSERVED — read via browser.open)
2. security.wikimedia.org writeup (URL TBD — see discovery log)
3. metr.org / transluce.org / rubyhack.ai disclosure pages (URLs discovered via search, see below)
4. en.wikipedia.org Etherpad article (URL TBD — discover via CDX prefix, do not guess)
5. wiki revision-history pages for suspect sandbox/citation-tool edits — PENDING (wiki-surgeon lane had named none as of 11:35 CDT; workers/wiki-surgeon/FINDINGS.md only at Phase 1)

## URL discovery log (OBSERVED from browser.open on seed + web search)
- Seed link [0] "multiple" -> metr.org (domain only). Candidate exact URLs (UPSTREAM ASSERTION from third-party GitHub source lists):
  - https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ (cited as METR/Redwood independent investigation, 2026-08-26)
  - https://metr.org/hugging-face-incident-report-aug-2026.pdf (cited as 7.4 MB PDF of same report)
- Seed link [1] "organisations" -> transluce.org. Exact URL (OBSERVED in search results, verbatim): https://transluce.org/agent-activity ("Early rogue AI agent activity and attempts to hack found on urlquery.net", published 2026-09-23)
- Seed link [2] "disclosed" -> rubyhack.ai. Exact root (OBSERVED in search results, verbatim): https://rubyhack.ai (report by Spencer Kitts, Thomas Larsen, Sydney Von Arx / Nightingale Collective, published 2026-09-11; no deeper URL returned by search — will CDX prefix-map)
- Seed link [3] "public wikis" -> en.wikipedia.org (domain only; context = "other public wikis ... to communicate and coordinate" — NOT in my target list, noting only)
- Seed link [5] "edits to Wikimedia wikis" -> security.wikimedia.org (domain only; writeup URL not returned by 2 web searches; will CDX prefix-map security.wikimedia.org/* to discover slug)
- Seed link [6] "Etherpad" -> en.wikipedia.org (domain only; will CDX prefix-map en.wikipedia.org/wiki/Etherpad* to discover canonical article slug)
- Seed link [8] "a partial outage on WDQS in May" -> wikitech.wikimedia.org (domain only; not in my assigned target list — logged as optional extra)

## CDX run log
- TRANSPORT (OBSERVED): `https://web.archive.org:443` TCP-connect times out via this VM's egress proxy (tested 2x, 25-60s); `http://web.archive.org` (port 80) to same host returns CDX 200. Same public documented API; using port 80.
- Gotcha (OBSERVED): CDX `matchType=prefix` takes a BARE prefix — a trailing `*` in the url param yields `[]`. First batch run wasted on this; rerun fixed.
- Positive control PASSED (OBSERVED): `en.wikipedia.org/wiki/Etherpad` prefix → 228 captures, earliest 20090614123544, latest 20260929163452 (full result; the earlier "latest 20260310104248" was from a limit=10 peek). CDX recall proven working before any negative is filed.
- 2026-10-06 ~11:47 CDT: seed-article exact query returned "Internet Archive: Temporarily Offline" HTML (transient CDX backend hiccup; retry with wider spacing).
- Batch v2 done (/tmp/archive-diver/run_cdx.sh, 8s pacing). Retry round 1 (45s spacing): metr_blog SUCCEEDED; seed + metr_pdf hit "Temporarily Offline"/504. Retry round 2 (90s spacing, retry2.sh): seed SUCCEEDED (4 captures), metr_pdf failed again. Retry round 3 (75s spacing, standalone): metr_pdf SUCCEEDED (76 captures). All 8 target queries now resolved.
- Raw CDX JSON kept at /tmp/archive-diver/cdx_*.json (ephemeral scratch; key numbers transcribed below).

## Per-target capture inventory (all OBSERVED via CDX, filter=statuscode:200)

### 0. POSITIVE CONTROL — en.wikipedia.org/wiki/Etherpad (prefix, bare)
- 228 captures | window 2009-06-14 → 2026-09-29 | 12 distinct URLs (canonical: https://en.wikipedia.org/wiki/Etherpad, 164 captures; also EtherPad/Etherpad_Lite variants)
- Predate incident window (pre-2026-05): YES, ~200 of them. Control proves CDX recall works.

### 1. Seed article — diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/
- 4 captures | window 2026-10-05 17:53 UTC → 2026-10-06 04:03 UTC. Archived from publication day (2026-10-05).
- Took 3 attempts (2x backend flakiness: "Temporarily Offline" HTML, 504) — succeeded on retry with 90s spacing.

### 2. security.wikimedia.org writeup — URL UNDISCOVERED
- Web search: 3 queries ("security.wikimedia.org OpenAI agents investigation", quoted-domain, citation-tool phrasing) returned NO security.wikimedia.org URL. The Diff seed links "edits to Wikimedia wikis" → security.wikimedia.org (domain only; href not exposed in text fetch).
- CDX domain prefix (security.wikimedia.org/): 158 captures | 23 distinct URLs | window 2020-10-23 → 2026-05-13. NO /blog/<post-slug> URLs captured anywhere — only the /blog/ index (8 captures: 2020, 2021, 2024-11, 2025-02, 2025-05, 2025-06, 2025-10, 2026-03-12; deep prefix query on security.wikimedia.org/blog/ confirms zero post slugs).
- COVERAGE GAP (not a negative): latest capture anywhere on the domain is 2026-05-13 (contact/, favicon.ico, hall-of-fame/). Wayback has NOTHING on security.wikimedia.org after 2026-05-13 — five months before the Oct 2026 disclosure. An October 2026 writeup is INVISIBLE to Wayback regardless of slug.
- OPEN LEAD: resolving the Diff article's link-[5] href needs a browser-capable route (page-source/href inspection). Logged, not fetched.

### 3a. METR — https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/
- 258 captures | window 2026-08-26 20:00 UTC → 2026-10-05 20:35 UTC. Heavily archived from publication day.
- URL grade: UPSTREAM ASSERTION (came from third-party GitHub source lists, not from metr.org itself) → now corroborated by 258 archived captures at exactly this path (INFERENCE: high confidence this is the canonical METR/Redwood investigation page).

### 3b. METR PDF — https://metr.org/hugging-face-incident-report-aug-2026.pdf
- 76 captures | window 2026-08-28 02:06 UTC → 2026-10-06 08:51 UTC (today). Archived from two days after the report's publication (2026-08-26).
- Took 4 attempts (3x "Temporarily Offline"/504) — succeeded with 75s+ spacing. URL corroborated as the genuine METR report PDF.

### 3c. Transluce — https://transluce.org/agent-activity
- 29 captures | window 2026-09-24 03:10 UTC → 2026-10-05 22:48 UTC. Archived from the day after publication (2026-09-23). Single URL.

### 3d. rubyhack.ai
- Root exact query: 23 captures | 2026-09-11 23:46 UTC → 2026-10-06 01:00 UTC (today). Early captures on www.rubyhack.ai, later on bare rubyhack.ai.
- Site prefix (rubyhack.ai/): 211 captures | 41 distinct URLs | window 2026-09-11 → 2026-10-05. Single-page report site: root page + styles.css, site.js, figures (uploads-per-day.html), fonts, img/ (openai-report-quote.png, rubydoc-rce-flow.png, rubyhack-social.png). NO sub-page report paths — the report IS the root page.
- Predate incident window: NO (site/report did not exist before 2026-09-11; earliest capture is publication day).

### 4. en.wikipedia.org Etherpad article
- Covered by positive control (target 0): canonical slug discovered via CDX = https://en.wikipedia.org/wiki/Etherpad. 164 captures of the canonical URL, window 2009-06-14 → 2026-09-29. Captures predate incident window: YES.

### 5. Wiki revision-history pages (suspect sandbox/citation-tool edits)
- PENDING. wiki-surgeon lane (workers/wiki-surgeon/FINDINGS.md) was still in Phase 1 (fetching seed) as of 11:35 CDT and had named no pages/usernames. No CDX work possible until they name targets.

## Coverage map / gaps
- Wayback is STRONG on: en.wikipedia.org (decades deep), metr.org disclosure (258 captures from pub day), transluce.org (29 from pub day+1), rubyhack.ai (full-site, 211 captures from pub day).
- Wayback is STALE on: security.wikimedia.org — coverage ends 2026-05-13; the October 2026 writeup cannot be assessed via CDX at all. Any "no archived writeup" claim from this lane would be a coverage artifact, not a finding.
- Wayback was FLAKY on: two queries needed 3-4 attempts ("Temporarily Offline" HTML / 504s); all eventually succeeded with 45-90s retry spacing. Lesson: intermittent CDX errors are transport noise, never evidence.
- No captures anywhere predate the May-2026 incident window except the Etherpad Wikipedia article (expected — all disclosure pages postdate the activity they describe).

## Positive-control recall checks
- en.wikipedia.org/wiki/Etherpad prefix → 228 captures incl. 2009 earliest. PASSED before any negative was considered.

## Clean negatives
- NONE filed. (The only empty results were my own malformed wildcard queries — discarded as invalid, not filed. A clean negative needs healthy transport + empty result; none occurred.)
