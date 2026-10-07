# newusers pull — provenance (2026-04-01 → 2026-09-30, 9 wikis)

**Completed:** 2026-10-07 ~06:50 UTC. **Total:** 6,922,622 log event
lines across the 24 canonical files (6,901,112 logid-unique; the
burst-analysis worker measured 4,088,327 logid-deduped `~2026-*`
temp-account creation events — the created name lives in `title`
("User:~2026-…"), NOT in `user`, which is null in formatversion=2
newusers logevents).

**Canonical file count is 24, not 25.** `newusers-2026-06.metawiki.resume.jsonl`
(60,000 rows, 2026-06-30 → 2026-06-27) is a redundant fragment from a
killed duplicate worker: all 60,000 of its logids are a strict subset of
`newusers-2026-06b.metawiki.jsonl` (verified 2026-10-07). It is kept on
disk for the record but MUST be excluded from any combined analysis
(the burst-analysis run parsed only the 24 canonical files).

## Layout

Per-month (enwiki) and half-month (metawiki) files — GitHub rejects files
>100MB, so the original combined files were split:
- `newusers-2026-04.enwiki.jsonl` … `newusers-2026-09.enwiki.jsonl`
- `newusers-2026-04.metawiki.jsonl`, `newusers-2026-05a/b.metawiki.jsonl` … `newusers-2026-09a/b.metawiki.jsonl`
- `newusers-2026-04-01_2026-09-30.{bgwiki,commonswiki,incubatorwiki,mediawikiwiki,simplewiki,test2wiki,testwiki}.jsonl` (combined, all under 100MB)

All files: one JSON log event per line, newest-first within month,
logid-deduped. Format: MediaWiki `list=logevents&letype=newusers`
(`formatversion=2`).

## Method

curl, `lelimit=500`, `lecontinue` pagination, `ledir=older`,
`User-Agent: silent-locus-research/1.0`, paced ≥2s (≥5s for the first
passes). 7 wikis pulled Apr–Sep by the lane's original workers;
enwiki/metawiki pulled month-by-month by parallel workers after the
original coordinator errored.

## Known data quirks (do not "fix" — documented)

- April enwiki had 30,000 exact-duplicate rows and April metawiki 30,001
  (pagination bug in the first pull: first N pages appended twice).
  Removed by logid dedupe in the per-month files (Apr unique: enwiki
  335,458 / metawiki 608,286). Commonswiki had 21,500 mid-file dupes
  (different shape, from the original pull — left as-is in the combined
  file; dedupe by logid before clustering).
- Month-boundary rows may duplicate across adjacent files (resume
  overlaps) — dedupe by logid when joining.
- 7-wiki combined files are oldest-month-first at the file level
  (April chunk, then May, …), newest-first within each chunk.

## Coverage

`raw/.newusers-pull-state`: 54/54 (9 wikis × 6 months).
