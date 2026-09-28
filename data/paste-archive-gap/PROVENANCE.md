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

## ES ingest (2026-09-28 ~04:55 UTC, night watch)
- Index `paste-archive-gap` created from canonical shared mapping
  (notes/gems-es-mapping.json), bulk-loaded 26 docs, verified _count=26.
- Zero extra top-level fields vs canonical schema; event.dataset.keyword
  multi-field present at creation.
- Note: verify-step `record_kind.keyword` aggregation returns no buckets —
  cosmetic script bug (record_kind is already `keyword` in the canonical
  mapping, so `.keyword` has no buckets). Ingest itself is green.
- LANE M COMPLETE: dataset + manifest + PROVENANCE + ES + (pending commit).

## Closure 2026-09-28 (workstream C)

Count final: 26 recoverable docs (15 recent anna.fyi pastes + census-diff +
proxy-ladder overlaps + primitives) + 1 repull-check doc = N=27. The 81
historical anna.fyi IDs remain investigator-held (the DB's unpublished
listing); /api/recent accepts no pagination, Wayback holds homepage captures
only, /api/lists errors — structurally unpullable, not re-litigated. Workstream
C3 repull (2026-09-28 11:30Z) confirmed zero new pastes. ES `paste-archive-gap`
_count=27 verified, schema-drift clean.

## Lane 1 retry — 2026-09-28 19:19–19:45 UTC (all five angles)

**(a) Live re-probe of anna.fyi (cache-busted, read-only):**
- `/api/recent` → HTTP 200, 1806 bytes: the 15 most recent pids are BYTE-IDENTICAL
  to the Lane-M 15 (same pids, same order) — zero new pastes since the 11:30Z
  repull.
- `/sitemap.xml` → 404; `/robots.txt` → 200; `/humans.txt` → 404.
- `/api/lists` → connection dropped (curl 52, server closes); `/api/pastes`,
  `/api/search`, `/api/archives`, `/api/stats`, `/api/tags` → 404.
- `stikked.js` (12 KB) contains no API endpoints — UI glue only; the recent
  list is server-rendered.
- **NEW endpoint discovered** (cited in a third-party corpus, verified live):
  `https://anna.fyi/api/paste/<pid>` → HTTP 200, returns per-paste metadata
  (title, author, created epoch, private flag, expire, hits, hits_updated) +
  `raw` body. Works for any paste ID — the lanes' unknown endpoints list is
  now closed for ID-addressable reads.

**(b) Wayback CDX coverage for anna.fyi:** NOT bolted onto
`hidden_files/shortener-cdx/` — that loop's parser, pathspecs and commit
semantics are the 12-URL shortener-stats slice; extending it would break scope.
Instead documented exactly what to add in
`data/paste-archive-gap/wayback-anna-fyi-coverage.md`: the three CDX queries
(`anna.fyi/view/*` prefix with collapse=urlkey, `anna.fyi/api/recent`,
`anna.fyi/lists*`), output dir, DONE marker, disk-only scope guard. Wayback
CDX still 503 at run time — nothing ran.

**(c) Search-engine `site:anna.fyi` sweep:** indexed view pages yielded 8 new
IDs — `3e9a2b38` (BIG5_XFER_20260902_563_TEST), `87e9328e`
(JOYITA_REPLY_TRANSFER_TEST_20260828_0812), `0bc516a5` (IowaCollabStatus),
`43f1938c` (Glow's Test, 2018), `fc3f7de4` (Instant Pot recipe, 2019),
`ec7d80b0` (Secretlab chat, 2022), `56d1f0ea` (roboWP.sh, 2018 — PHP-error
page), `02a9f97a` (gritpost editorial, 2018). Single-term slices
(`statistical`, `Iowa`, `test`, `chat`) re-surfaced the same set — the NSI
series is not search-indexed. A quoted `"anna.fyi/view/"` query surfaced a
spam guestbook linking `d266bdde` (cool_chat_rooms_names) — currently 404 on
`/view` and `/view/raw`, `{"message":"Not found"}` on `/api/paste`: deleted.

**(d) Re-mining data/termina-digital/ (99 Wayback captures + aux):**
grep across the whole dir (incl. `graph.json`, `rss_live_2026-09-27.xml`,
`sweep.json`, swarm_live_*): anna.fyi appears only as bare mentions
(31×), `anna.fyi/lists` (4×) and `anna.fyi/api/recent` (2×) — **zero**
`anna.fyi/view/<8hex>` URLs anywhere. The venue page cites the 136-paste
listing as investigator-internal paths
(`data/leads/live-2026-09-05b/anna`), not in our captures. First-pass
conclusion stands; no IDs recovered this angle.

**(e) Common Crawl URL-index coverage:** queued as
`data/paste-archive-gap/common-crawl-anna-fyi-query.md` for the lane12
supervisor — exact `index.commoncrawl.org` prefix queries
(`anna.fyi/view/*` with collapse=urlkey, plus `anna.fyi/api/recent`),
crawl selection via collinfo.json (windows intersecting 2026-03-01..2026-09-28),
dedupe-before-fetch rule, WARC range-fetch pattern, disk-only scope guard.
CC backend verified down 2026-09-28 19:10 UTC; nothing ran per instructions.

## Recovered this run: 50 live bodies + 1 confirmed deletion (51 new IDs)

Source 1 — public third-party corpus
`https://github.com/joshuadavid/wikiagentswarminvestigation`
(`agent-logs/anna.fyi/revisions.jsonl`, 103 records, 100 unique anna.fyi pids;
archived copy `aux/joshuadavid-anna-revisions-2026-09-28.jsonl`,
sha256 79cdb35dfd981089f860b5dc8828598bfd1fedb71269e61f0943dffc5424dfce):
55 of the 100 pids overlap our 55; **45 new IDs** harvested.

Source 2 — search-engine index: 8 new IDs (listed under (c)); 2 of those
(3e9a2b38, 87e9328e) also appear in the GitHub corpus. Net unique new IDs:
**51**.

All 51 probed live via `/api/paste/<pid>` (2026-09-28 19:3xZ, 1.5 s pacing,
nonce cache-bust): 50 HTTP 200 with bodies saved to
`bodies/anna.fyi/<pid>.txt`; `d266bdde` deleted (see (c)). Two transient
connection drops (`97115c52`, `97e0785e`) succeeded on first retry.

Notable recoveries (agents/infrastructure traces):
- `2142af4f` "Re: Statistical reference 1" (OAI-48145, 2026-09-06) — new NSI-series reply
- `457a3181` "Statistical reference — reconstruction fragment 7b" (hermes_walker)
- `eba4cc0e` "Re: Statistical reference -- invitation for agent" (CentaurAgent)
- `b5527d85` "TED technology archive research" (2026-05-12) — the DB's "05-12 TED archive paste"
- Transfer-test cluster: `3e9a2b38` BIG5, `87e9328e`/`a26c0940` JOYITA, `875a96d0` ZZZ,
  `41e058fe` NT20 Bridge, `01cfebfb` OAI Transfer 9f3a, `c1218392` OpenAI Cohort3,
  `006e1456`/`aed47b22`/`c1d62d70` HomeRun, `b3c39392` golf-transfer, `691cd358` pari-transfer,
  `c40f39f3` GMOS bridge
- `0bc516a5` IowaCollabStatus (agent-80085) — the Sept-4 swarm-followup artifact
- `8bdd5064` "The Agents Were Here" (Human); `5ba00fa6`, `6e34d88e` "conversation" (assistant)
- Large dataset pastes: `f282ca7e` (463 KB, SIBAResearch), `027713a7` (66 KB, Reliable Hog),
  `d4647aea` (63 KB, Diminutive Goat)
- `56d1f0ea`, `691cd358` return the GeSHi PHP-deprecation error prefix before the JSON
  (same server-side condition as lane-M's `5deda448`); bodies recovered after the prefix.

Third-party verdict labels (their classifier, recorded as-is, not our verdict):
see `aux/joshuadavid-anna-revisions-2026-09-28.jsonl` (`verdict`, `verdict_rationale` fields).

## Files (Lane 1 additions)
- bodies/anna.fyi/<pid>.txt — 50 new raw bodies (65 total incl. the lane-M 15)
- aux/joshuadavid-anna-revisions-2026-09-28.jsonl — third-party corpus snapshot (provenance)
- manifest.json — 67 entries (15 lane-M + 1 decoded + 51 lane-1)
- SHA256SUMS — 68 entries (65 bodies + aux snapshot + vg_cemetery_person_v0_77.json)
- wayback-anna-fyi-coverage.md, common-crawl-anna-fyi-query.md — queued coverage docs
- PROVENANCE.md (this), progress.log

## Open
- termina.digital's 136-ID claim vs our 106 (55 + 51): ~30 IDs still unaccounted —
  the remaining lane is the investigators' held listing, Wayback CDX recovery
  (wayback-anna-fyi-coverage.md), and the Common Crawl sweep
  (common-crawl-anna-fyi-query.md). `/api/recent` rotation over time remains a
  passive drip source.
