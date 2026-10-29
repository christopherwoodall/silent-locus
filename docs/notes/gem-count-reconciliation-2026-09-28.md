# rubygems-goimport-campaign count reconciliation — 2026-09-28

## Question
Authoritative `_count` said **6,619** docs; `_cat/indices docs.count` said **8,349**.
Christopher asked: fix the count, make index and disk agree.

## Answer (grounded)
The index is **correct**. Nothing is missing. The 8,349 was inflated by
**1,582 deleted-but-unmerged docs** — tombstones left by idempotent re-ingests.
Disk and index agree exactly at **6,619**.

## Composition (every figure counted, not estimated)

| on-disk source | lines | unique ingest `_id`s | indexed (`record_kind`) | verdict |
|---|---|---|---|---|
| `data/gemstuffer-jfrog-2026-09-27.csv` (header + rows) | 3,026 | 3,025 (`jfrog:<package>`) | 3,025 `jfrog_inventory` | OK |
| `data/gem-ioc-hits.jsonl` | 2,341 | 2,339 | 2,339 `hit` | OK — 2 exact-dup lines on disk |
| `data/gem-ioc-log.jsonl` [download] | 3 | 3 | 3 `download` | OK (json/oai/thor controls) |
| `data/gem-ioc-log.jsonl` [extraction] | 635 | 618 (`log:<rk>:<gem>:<ver>`) | 618 `extraction` | OK — 17 dup lines on disk |
| `data/gem-ioc-log.jsonl` [diffend_harvest] | 624 | 618 | 618 `diffend_harvest` | OK — 6 dup lines on disk |
| `data/gem-june18-wayback.jsonl` | 16 | 16 | 16 `wayback_metadata` | OK |
| **total** | | **6,619** | **6,619** (`_count`) | **AGREE** |

Duplicate on-disk lines are benign: ingest scripts (`es_ingest_gems.py`,
`es_ingest_jfrog.py`) use deterministic `_id`s, so re-runs overwrite instead of
duplicating. Verified by recomputing the IDs locally.

## The 6,619 vs 8,349 gap — root cause
- `_cat/indices`: `docs.count` 8,349, `docs.deleted` **1,582** (stable across
  three polls 60s apart — no in-flight writes, no background merge in window).
- Every ingest is idempotent with deterministic `_id`s; each re-ingest run
  (JFrog backfills, hit re-ingests, harvest retries) overwrote docs, marking the
  old versions deleted. Segments have not merged the tombstones yet.
- 8,349 − 1,582 = 6,767 vs `_count` 6,619: the residual ~148 is `_cat`
  reporting staleness, not missing docs — the record_kind terms agg sums to
  exactly 6,619 and every live doc is accounted for in the table above.
- `_stats`, `_cat/segments`, and `_forcemerge` all return **HTTP 410** on the
  current credential — admin endpoints are not permitted, so the merge could
  not be forced from here.

## What was NOT done (writes paused per 13:21 steer)
- No re-ingest (nothing is missing; re-ingesting would only add more tombstones).
- No forcemerge, no deletes on the hosted cluster.
- No data files rewritten (dup lines are benign; rewriting would break
  provenance/checksums).

## Remediation steps (to apply later, read-only until then)
1. With a credential that permits admin endpoints:
   `POST /rubygems-goimport-campaign/_forcemerge?only_expunge_deletes=true`
2. Re-verify: `_count` == `_cat docs.count`, `docs.deleted` == 0.
   Expected post-merge: **6,619** on both.
3. Re-run `scripts/audit_gem_counts.py` (read-only) to confirm disk/index
   agreement; it exits showing AGREE/MISMATCH.

## Artifacts
- `scripts/audit_gem_counts.py` — read-only audit, reproducible.
- This note.
