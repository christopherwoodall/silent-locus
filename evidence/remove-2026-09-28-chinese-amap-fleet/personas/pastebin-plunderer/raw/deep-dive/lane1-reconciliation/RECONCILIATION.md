# Lane 1 — Reconciliation: joshuadavid corpus vs our 2026-09-27 linuxiarz ingest

Lane: Reconciliation + Grammar Taxonomy + Ingest (k4be + linuxiarz).
Source: `JoshuaDavid/WikiAgentSwarmInvestigation` (branch `main`, retrieved
2026-10-05 via raw.githubusercontent.com; paste hosts never probed).
Artifacts: `census.jsonl`, `reconciliation.json`, `taxonomy.json`,
`analyze_corpus.py`, `build_lane1_ingest.py` (this directory).

## 1. Corpus enumeration (joshuadavid export)

| Host | Export rows | shellac_import | subagent swarm | subagent unclear | Full bodies | View-only |
|---|---|---|---|---|---|---|
| pastebin.k4be.pl | 198 | 126 | 51 | 21 | 198 | 0 |
| paste.linuxiarz.pl | 381 | 219 | 81 | 81 | 254 | 127 |

- k4be time span (stikked `created`): 2025-10-24 → 2026-09-05; biggest burst
  day 2026-05-18 (114 pastes).
- linuxiarz: shellac rows dated 2022-07-06 → 2026-06-18; 162 Wayback rows
  have no absolute timestamp (relative `N Years/Months ago` only).

## 2. Reconciliation vs our 131

- Our 131 IDs ⊂ their 219 shellac imports: **131/131 exact ID match**.
  Zero divergence.
- **250 genuinely-new linuxiarz records**: 88 new shellac-imported
  (dated) + 162 Wayback (35 full-body, 127 view-page-only).
- k4be: 198 records, all new (host was never in our corpus).

## 3. The "~27 unrecoverable" note — resolved

The 2026-09-27 ingest note said ~27 of the investigators' 158
linuxiarz texts were not URL-enumerated and unrecoverable. Re-audit of
the local collusion-wiki `records.jsonl` (13,703 records):
all 158 linuxiarz-origin records carry a paste URL and resolve to
exactly our 131 distinct paste IDs — the "27" were duplicate/redundant
records (multiple records referencing the same paste), not missing
texts. The joshuadavid export recovers no *missing* texts beyond the
250 new IDs enumerated here; it does recover 88 additional
shellac-archived bodies and 162 Wayback rows that collusion.wiki never
saw.

## 4. Marker-battery verdict (task 3)

Our prior `sweep.json` battery checked: epoch_10digit, agent_handle,
ts_epoch, markdown_new, chunk_A000, allorigins, cors_worker.
It did **not** check CLICKMAYBE / URLMARK / FRAMEK4 / PAD\d+x\d+.

Grep over all 131 of our bodies: **0 hits for CLICKMAYBE, URLMARK,
FRAMEK4, PAD\d+x\d+, pad-<epoch>, jqp.vercel, 2md.link, md.succ.ai,
telegra.ph, LANGURL, clock.wait** — the k4be grammar was genuinely
**absent** from our 131, not missed by the battery. (Our battery also
missed them, but the gap was moot: nothing to find.)

New-record marker update:
- `jina`: 0 hits across the entire combined corpus (381 linuxiarz +
  198 k4be). The clean negative stands.
- `zz=`: 0 hits everywhere. Clean negative stands.
- `oai`-style tags: 2 linuxiarz hits (view-only rows, titles only).
- `webhook`: 1 linuxiarz hit (2025-11-25, ESP32 sysadmin-context paste;
  not swarm-relay language — honest negative for the swarm marker).
- `allorigins`: 9 of our 131 + present in new records; `is.gd`: 1 of
  ours + 12 new. Both already known.

## 5. Ingest outputs (NO commits/pushes, NO Elastic writes)

### A. Extended `data/2026-05-26-paste-linuxiarz/`
- `raw/<pid>.txt`: +123 new bodies (all 123 SHA-256-verified vs the
  investigators') → 254 bodies on disk.
- `raw/manifest.jsonl`: 131 → 381 rows (jd verdict/inclusion/
  body-availability/wayback provenance + external-overlap annotation).
- `events.jsonl`: 131 → 381 `relay_paste` rows. Wayback view-only rows
  use the documented `@timestamp = 1970-01-01T00:00:00Z` sentinel with
  `labels.timestamp_source = "fallback:no_recoverable_date"`, omit
  `sha256`, confidence `medium`; body-verified rows keep `confirmed`.
- `rollup.jsonl`: frozen at the original 131-row wave (documented in
  PROVENANCE.md).
- `scripts/validate_schema.py`: 0 violations. `SHA256SUMS`: whole-tree,
  `sha256sum -c` green.

### B. New dataset `data/2025-10-24-pastebin-k4be/`
(2025-10-24 = earliest stikked `created`, per prefix convention.)
- `raw/<pid>.txt`: 198 bodies, all SHA-256-verified vs investigators'.
- `raw/manifest.jsonl`: 198 rows with jd verdict metadata +
  external-overlap annotations.
- `events.jsonl`: 198 `relay_paste` rows (fingerprint
  `k4be-paste:<pid>`; 21 `unclear`-verdict rows kept per keep-all,
  filterable via `labels."paste.jd_verdict"`).
- `rollup.jsonl`: 24 `paste_day_burst` rows, 2025-10-24 → 2026-09-05.
- `PROVENANCE.md`, `SHA256SUMS` (green), schema validation: 0 violations.
- Registered in `schema/collections.json`
  (`2025-10-24-pastebin-k4be`, series `pastebin-k4be`).

## 6. Thai NSO lead (task 5) — NOT FOUND

Case-sensitive grep for `Thai|Thailand|NSO|bangkok` across all 579
bodies: **zero hits**. The ROIETA/TH45 rows are Roi Et province bench
stats (EPL-style benchmark tables), unrelated to any NSO lead. The
forager persona's open lead (exact Thai NSO pastebin.k4be.pl paste URL)
is not recoverable from this export.

## 7. Open threads

1. 127 view-only linuxiarz rows have titles + posted-names but no bodies;
   worth a second Wayback pass (out of lane scope).
2. Wayback coverage is ~370/1300+ linuxiarz pastes; most swarm activity
   on that host remains unarchived.
3. The `unclear` rows (21 k4be, 81 linuxiarz) are kept but unreviewed;
   a re-review pass could promote some to swarm.
4. `agent-ours0909` appears in 2 linuxiarz rows; `Perceptual Zephyr`
   (thecolony.ai recruiter) in 8 rows cross-host — worth flagging to
   the cross-host lane.
5. OPSEC reminder for other lanes: paste.linuxiarz.pl currently
   403s `/api/*` and 404s `/view/*` (operator lockdown, per jd README);
   pastebin.k4be.pl scrape ran at 1 req/s on 2026-09-07 — do not
   re-scrape aggressively.
