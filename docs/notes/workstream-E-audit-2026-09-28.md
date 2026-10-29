# Workstream E audit — no-consolidation rule enforcement (2026-09-28)

Standing rule (Christopher): **PRIMARY INDEXES HOLD EXPLICIT EVENTS ONLY**
(one doc per observable event). Rollups/summaries/counts go in `<index>-rollup`
support indexes. Audit method: doc granularity of every project index compared
against the dataset's raw evidence files (hits.jsonl etc.); a doc summarizing
N raw rows = violation. Read-only on the cluster (`_count`, `_search`, `_cat`);
**zero Elastic writes** — all unwinds are staged on disk under the 2026-09-28
write pause (see `notes/ELASTIC_WRITE_PAUSE`).

Scope notes: `urlquery-hunt` / `urlquery-incidents` excluded (wrapped hunt is
frozen per Christopher). `july7-wave` and `rubygems-goimport-campaign` are
mid-resweep (workstream A lane running) — audited read-only, no staging, no
unwind until that lane lands.

## VIOLATED — unwind staged on disk, scripts ready (pause-guarded)

| Index | Primary now | Explicit events (staged) | Rollup docs (staged) | After unwind |
|---|---|---|---|---|
| `admin-deletions` | 26 per-day summaries (`admin_cleanup_burst`) | 5,217 delete events from `hits.jsonl` | 26 (original `_id`s) | primary=5,217, `admin-deletions-rollup`=26 |
| `university-shorteners` | 16 slug summaries; 5 `yourls_stats_detail` docs bundle 740/57/285/77/28 referrer rows | 1,492 (1,187 `shortener_referrer_row` + 305 `shortener_daily_hits`) from `*_referrer_urls_daily_*.json` | 16 (original `_id`s) | primary=1,492, `university-shorteners-rollup`=16 |

- admin-deletions: explicit `_id` = row `event_id` (verified unique); `@timestamp`
  = row `time`; `record_kind=delete_event`; `event.dataset=admin-deletions`.
- university-shorteners: referrer `_id = yourlsref:<instance>:<slug>:<sha16(host|url)>#<occurrence>`
  (keep-all: duplicate listings preserved, occurrence-disambiguated);
  daily `_id = yourlsdaily:<instance>:<slug>:<series>:<date>` (dates ISO-normalized).
  No shortener re-explosion lane is actually running — checked subagents,
  processes, git status (~18:20 UTC): this unwind owns the lane.
- Scripts: `scripts/es_unwind_admin_deletions.py`, `scripts/es_unwind_university_shorteners.py`
  (`--verify-only` now; `--execute` refuses while `notes/ELASTIC_WRITE_PAUSE` exists).
  Sequence per script: create `<index>-rollup` from `notes/gems-es-mapping.json`
  → bulk rollup docs → bulk explicit events into primary → bulk-delete rollup
  `_id`s from primary → verify counts + `event.dataset.keyword` on both.

## CLEAN (1:1 doc↔evidence, no bundled rows)
`timeline-anchors` (48), `worldpoverty-task-family` (22), `open-data-api-venues` (46),
`pxweb-national-stats` (12), `july6-staging` (11), `paste-archive-gap` (27),
`jsonhero-docs` (17), `jsonhero-docs-archive` (6), `gem83-reconciliation` (83),
`iowacollab-pastes` (5 = 4 pastes + 1 live_recheck), `counter-channel` (4),
`webhook-deaddrops` (8), `agent-surfaces` (11), `fieldnotes-gem` (7 root docs;
`_cat` shows 13 Lucene docs = 7 + 6 nested `diffend_versions` rows — not a write,
explained), `demowiki` (23), `ludism-wikis` (31), `vanderbilt-shortener` (24),
`thecolony-ai` (27), `termina-digital` (107), `march7-rce-modality` (38),
`collusion-wiki` (80,434), `public-board` (861), `proxy-primitives` (1,522),
`rmn-re-history` (764), `rmn-re-linktable` (764), `tantive-space` (1,124),
`powerbi-fronting` (182), `paste-linuxiarz` (131), `reverse-tunnels` (95),
`cors-bwa-proxy` (154), `paste-archive` (76).

Boundary calls (flagged, not unwound): analytic-synthesis lanes
(`timeline-anchors`, `july6-staging` staging_signal docs, `paste-archive-gap`
census_diff) derive from other indexes' data, but their own raw evidence is
1:1 with docs — the test is same-index granularity, not cross-index derivation.
`jsonhero-docs` carries scalar count fields (`corpus_url_occurrences`) describing
the doc, not bundles of rows — clean.

## DEFERRED (active lane in flight)
- `july7-wave` — count moving (281→264 during audit); Diffend resweep running.
- `rubygems-goimport-campaign` — count moving (8,349→6,619); resweep in flight.
  Read-only sample: one doc per gem (`diffend_versions` is a per-gem attribute
  list), no consolidation violation detected. Re-audit after the lane lands.

## Checklist
`notes/lane-checklist.md` created (binding): explicit-events-only rule +
Elastic write-pause rule + verification bar. `notes/ELASTIC_WRITE_PAUSE`
sentinel created; both unwind scripts honor it.
