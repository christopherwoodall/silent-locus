# CHECKPOINT — account-profiler (wikipedia-lane)
Branch: `wikipedia-edit-hunt-2026-10-06`. Last update: 2026-10-06 18:40 CDT (finisher session).

## Status: RESUMED AFTER DRAIN — enwiki+metawiki pulls re-launched 18:38 CDT
- 6-month newusers pull: 7/9 wikis COMPLETE (42/54 chunks). enwiki: April chunk COMPLETE (365,458 lines, 2026-04-01T00:00:01Z..2026-04-30T23:59:55Z, marked in state); May chunk partial (May31→May16 at death). metawiki: April chunk partial (Apr30→Apr05 at death, unmarked).
- Both resume pulls launched 18:38 CDT in background (`resume_chunk.py`, curl, 5s pacing): metawiki resumes April from 2026-04-05T17:58:05Z then chains `pull_newusers_6mo.sh metawiki` (May..Sep); enwiki resumes May from 2026-05-16T23:06:34Z then chains `pull_newusers_6mo.sh enwiki` (Jun..Sep). ETA ~6h enwiki / ~11h metawiki (parallel, different hosts).
- VERIFIED (finisher): both files gap-free within pulled ranges (pages append atomically; tails are complete JSON); unions cover their windows; worker-restart double-append blocks identified and quantified (enwiki/metawiki: exact 30,000-line repeat of lines 0-29999; commonswiki: 21,500-line repeat of preceding August block — restart artifact, union gap-free). All analysis dedupes by logid; PROVENANCE records raw vs unique counts.
- Everything else from the 17:05 checkpoint stands: accounts.tsv (28), per-account contribs cached, registration/lock/block status done, burst clustering done on 7 wikis, SHAPE-SCORES ranked, EventStreams answered, lifeval-cross-corpus assessed (below).
- lifeval-cross-corpus/ (event-level, untracked): NOT a mystery dir — 3 of 4 workers complete with FINDINGS.md (web-search: no public-web cross-corpus hit, LIFBench collision footnote; disk-corpora: 1 real survivor — "sandbox link test" on wikiservice.at/dse WillkommenImWiki 2026-06-18, same date as incident M5 cluster; urlquery-live: zero Lifeval markers in htmx index, weak negative). urlquery-cached: SCANLOG only, scans redundant with disk-corpora (superseded, noted).
- PROVENANCE.md: account-profiler section appended (endpoints, params, per-file raw/unique counts; sha256 + enwiki/metawiki rows pending pull completion).

## Status: DATASET CACHED (7/9 wikis; enwiki+metawiki pulls continue in background)
- accounts.tsv: DONE — `wikipedia-lane/raw/accounts.tsv` (28 accounts, factual columns incl. registration_utc).
- Per-account contribs: DONE — all cached in `wikipedia-lane/raw/`:
  - `contribs-2026-28355-02-{enwiki,testwiki,test2wiki,mediawikiwiki}.json` (19 edits total)
  - `contribs-2026-31087-50-*`: NOT pulled separately — global editcount=4=testwiki incident edits; full history = 4 rows in revisions.tsv. (Rationale: editcount match.)
  - `contribs-2026-31558-62-testwiki.json` (3 edits: 2 adjacent non-CSV sandbox edits, cached)
  - `contribs-2026-36867-71-incubatorwiki.json` (1) + `-metawiki.json` (0 live; 5 deleted)
  - `contribs-2026-36837-35-metawiki.json` (1)
  - All other 22 accounts: global editcount=1 = single incident row in revisions.tsv (full history by construction).
- Registration: DONE — `registration-*.json` in raw/ (`list=users&usprop=registration` per wiki) + `newusers-probe-*.json` (autocreate log entries for the 3 seed accounts).
- Lock status: DONE — `globaluserinfo/*.json` (locked=False for all 28) + `locklog-globalauth/*.json` (0 events for 25 accounts; 3 checked earlier also 0) + `blocklog-2026-36867-71-metawiki.json` (the single local indef block "Unauthorized bot").
- 6-month newusers pull: 7/9 wikis COMPLETE (testwiki, test2wiki, incubatorwiki, mediawikiwiki, simplewiki, bgwiki, commonswiki — 42/54 chunks). enwiki and metawiki workers RUNNING in background (proc_690254d4ceaf, proc_921f5fdf8320); their April chunks are very large (>140k events each). Will complete unattended.
- Burst clustering: DONE for 7 complete wikis. BURST-6 (commonswiki, 5× n=15–18) added; 60/79 dormant; shape 2/5 → CLEAN NEGATIVE (shape), dormancy lead filed.
- SHAPE-SCORES: DONE — ranked table in FINDINGS.md. BURST-1 (testwiki) 3/5 → zoom-in lead. All others 2–2.5/5 → clean negatives with feature comparisons stated.
  Scope: 2026-04-01–2026-09-30, `letype=newusers&leaction=newusers/autocreate` (autocreate-only is NOT sampling: all ~2026-* temp accounts are autocreated, verified 3/3; regular `create` signups can never be `~2026-*`). Fully paged via lecontinue, lelimit=500. Resume via `raw/.newusers-pull-state` (per wiki:month). Files: `raw/newusers-2026-04-01_2026-09-30.<shortwiki>.jsonl` (one event/line; fields logid,ns,title,pageid,logpage,type,action,timestamp).
  NOTE: sequential pull was replaced by parallel at ~14:20 CDT; partial enwiki 2026-04 data (18.5k lines, no completed chunk) was truncated for a clean restart — no dupes.
- Burst clustering: PENDING pull completion. Threshold to use: ≥5 `~2026-*` creations within 10 min (stated in analysis). Dormant-account usercontribs checks: pending.
- EventStreams question: DONE (see FINDINGS.md — retention test proved no May–June 2026 history; no public archive found).

## Pending
1. 6-month pull completion → sha256 + row counts → PROVENANCE.md section.
2. Burst clustering + dormant-account leads.
3. PROVENANCE.md append (account-profiler section).
4. Commit + push `wikipedia-edit-hunt-2026-10-06`.

## Key facts banked (all OBSERVED unless noted)
- 28 distinct temp accounts across 54 CSV rows; waves: 05-10 (4 accts), 05-13 (4, commons), 05-25 (1, test×4), 05-27 (6), 06-18 (3), 06-25 (10).
- Registration ≈ first edit for all (temp auto-create); stated plainly, not a signup event.
- Zero global locks across all 28. One local block: ~2026-36867-71 on metawiki indef "Unauthorized bot" 2026-06-25T22:29:53Z.
- 5 meta Web2Cit oldids confirmed-absent (badrevids/missing; independently verified by revision-enumerator's batch). Attribution of those 5 to ~2026-36867-71 is INFERENCE (strong).
- ~2026-31558-62: the only account with non-CSV edits (2 adjacent sandbox edits); still sandbox-only.
- Temp-account IDs look globally sequential (~2026-24351 on bg in April → ~2026-36920 on incubator June 25) — INFERENCE, useful for fleet analysis.
