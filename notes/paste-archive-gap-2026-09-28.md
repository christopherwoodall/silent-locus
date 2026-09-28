# Lane M — paste-archive-gap: ES ingest + census close-out (2026-09-28)

**Dataset:** `data/paste-archive-gap/` (manifest.json 16 entries, bodies/anna.fyi/
15 pastes, vg_cemetery_person_v0_77.json 1.2MB, proxy_ladder_crossref.json 89 URLs,
PROVENANCE.md). **ES index `paste-archive-gap`: 26 docs**, zero schema drift,
`event.dataset.keyword` multi-field at creation, all 26 docs on
`event.dataset=paste-archive-gap`.

## Trigger
Lane L (`notes/termina-counter-lane-2026-09-27.md`): the recovered termina.digital
incident DB claims an anna.fyi census of **136 pastes lifetime (60 in the NSI
series)** vs our **55 held (50 NSI)** — and its actor pages document the June-18
SEC county bridge per-handle with full proxy ladders. Lane M closed the gap as
far as public data allows.

## Recovery results (all read-only)
- Live `anna.fyi/api/recent`: 200, returns only the **15 most recent** (no
  pagination); `/api/lists` → CodeIgniter DB error; `/api/pastes` → 404;
  `/lists` mirrors the same 15.
- Wayback CDX: homepage captures only; zero individual paste captures.
- The DB's 136-ID listing is **investigator-held and unpublished**
  (`data/leads/live-2026-09-05b/anna` — their internal path, not ours);
  investigator tarball `agent-pastes-2026-09-08.tar.gz` is a placeholder.
- Recovered all 15 recent pastes via `/view/raw` (all 200; `5deda448` PHP-error,
  no body). **None of the 15 were in our 55** — the venue had moved on since
  our collection.
- Decoded `b3746a9f`: 1.2MB Czech cemetery JSON — **VG_CEMETERY_PERSON_MOST_ULTRABULK
  v0.77, 5,000 rows**, posted as base64 gzip by "Abrupt Bison"
  (adjective-animal author naming, consistent with the swarm's agent naming).
- Actor pages: 89 proxy URLs extracted; **8 exact overlaps with rmn.re decoded
  targets**; 22 of the 89 appear in the wiki corpus (7,049 hits).
- **NEW shared proxy primitive: `cors.bwa.workers.dev`** — present in termina.digital
  DB actor-page URLs *and* in rmn.re decoded targets; not previously flagged in
  either corpus sweep. Cross-corpus proxy-chain bridge (cf. notes on
  cors-bwa-proxy / the May-27 epoch marker).

## ES ingest (this run)
`scripts/es_ingest_paste_archive_gap.py --create/--load/--verify`:
26 docs, bulk errors=false. record_kind split: 15 `paste_text`, 8
`proxy_ladder_overlap`, 1 `census_diff`, 1 `dataset` (vg-cemetery), 1
`proxy_primitive` (cors.bwa.workers.dev). Bodies <20KB embedded in
`description`; larger bodies stay on disk (SHA-256 manifest). Schema-drift
check: zero extra top-level fields vs `notes/gems-es-mapping.json`; lane-specific
fields in flattened `labels`. One manifest entry (`b3746a9f_decoded`) intentionally
skipped from paste docs — it lands only as the dataset doc.

## Verdict
- Census gap is **structurally unclosable from public data**: NSI series ~49–60,
  the 05-12 TED archive paste, post-disclosure visitors, pre-disclosure human
  pastes are all behind an investigator-held listing. Recorded as open in the
  census_diff doc, not silently dropped.
- The cors.bwa.workers.dev primitive is the lane's real find — a proxy shared
  by the termina-documented actor layer and the rmn.re shortener layer, i.e.
  infrastructure used by both the operator-facing DB world and the agent-facing
  shortener world.

## Open items
- If the investigator tarball ever goes live (placeholder today), re-run the
  census diff; the 136-ID listing would close the NSI gap in one pass.
- cors.bwa.workers.dev: search other shortener corpora for the same host
  (YOURLS sweep lane, rmn-re-history) — if it recurs, it becomes a toolkit
  marker, not a one-off.
- The 5deda448 paste threw a PHP error on /view/raw — retry later; may be a
  temporarily broken page rather than a permanently empty one.
