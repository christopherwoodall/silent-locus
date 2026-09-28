# Workstream C3 — small open gaps recovery (2026-09-28)

Recovered per gap (all read-only, polite pacing):

## 1. anna.fyi 81 historical paste IDs — 0/81 recovered, gap STILL OPEN
- Re-pulled `https://anna.fyi/api/recent` (HTTP 200): the 15 most recent pids
  are byte-identical to the 15 already captured in Lane M (same order) — zero
  new pastes since the lane pull.
- The 81 IDs remain investigator-held/unpublished (termina.digital DB's held
  anna.fyi listing); `/api/recent` accepts no pagination; `/api/lists` ->
  CodeIgniter error; `/api/pastes` -> 404; Wayback holds homepage captures
  only. No duplicates created.
- ES: `paste-archive-gap` 26 -> **27 docs** (added deterministic
  `paste-archive-gap:repull:2026-09-28`, record_kind=recovery_check).

## 2. iowacollab 7 relay IDs — 0/7 recovered, gap STILL OPEN
- Live re-check: `/view/df40f1f1` -> 404, `/view/raw/df40f1f1` -> 404,
  `/api/recent` -> 403 anonymous (all unchanged since lane G).
- Wayback availability endpoint -> 429 (rate-limited); backed off per policy,
  no retry storm.
- The 7 other relay IDs were deliberately unenumerated by the source report
  (guessing them would read strangers' pastes); no new IDs surfaced.
- ES: `iowacollab-pastes` 4 -> **5 docs** (added deterministic
  `recheck:2026-09-28`, record_kind=live_recheck).

## 3. goto.unm.edu July 5-6 referrer rows — NOT publicly retrievable (structural)
- Pulled raw HTML of all 4 public stats pages (7t6-o, discvr, reso, urphy21)
  and parsed offline. YOURLS public stats expose: decimated all-time daily
  series (~6-week sampling, zero-hit days included — no 2026-07-05/06 point
  sampled on any slug), last-30d daily (Aug 30–Sep 28 2026), and per-URL
  referrer detail tables with NO per-day drill-down. No per-day-per-referrer
  endpoint exists in the public UI.
- Recovered instead: **1,159 full per-URL referrer rows** (7t6-o 740/35 hosts,
  reso 285/11, urphy21 77/8, discvr 57/9) + daily series per slug.
  Evidence: `data/university-shorteners/goto-unm-edu/*_referrer_urls_daily_2026-09-28.json`
  (4 files; Census API key values redacted as `[REDACTED]`, 24 rows).
- New markers: `jqp.vercel.app/OAIDATAUSATESTXYZ` (oai+XYZ grammar, Data USA
  API test); `tinyurl.com/2dhwlfmj` inside 6 wrapper chains (allorigins x2,
  api.allorigins.win x2, jsonhero.io, proxy.cors.sh, corsproxy.io);
  `yourls-infos.php/CTXWIN12ZZ0?id=7t6-o` (ZZ-grammar stats-page probe, 4 hits);
  `win13=<decimal-nonce>` on county.json via allorigins (8 rows).
- Dataset: `build_dataset.py` extended (kind `yourls_stats_detail`,
  deterministic doc IDs `yourls:<instance>:<slug>#detail-2026-09-28`);
  `university-shorteners.jsonl` 7 -> 11 docs; SHA256SUMS regenerated (all
  11 files covered).
- ES: ingested via workstream A's canonical consolidated script
  (`scripts/es_ingest_university_shorteners_consolidated.py`; its
  expected-count assertion updated 8 -> 12 for the 4 new detail docs).
  `university-shorteners` **12 docs** (buckets: university-shorteners 11,
  batch2 1), zero field drift, unique deterministic IDs.

Coordination with workstream A (155f815, consolidated shortener batches):
used A's consolidated ingest path; did not touch the retired batch2 index or
frozen lane notes; SHA256SUMS regenerated so the manifest covers the 4 new
evidence files.
