# Provenance — LANE J: July-7 wave Diffend sweep

## Sources
- **Candidate list**: JFrog's public GemStuffer inventory CSV,
  `data/2025-03-04-rubygems-goimport-campaign/raw/gemstuffer-jfrog-2026-09-27.csv` (3,025 rows: Package, Versions, Xray ID),
  saved 2026-09-27 from https://research.jfrog.com/gemstuffer.csv
  (see `notes/gem-jfrog-report-2026-09-27.md`).
  The CSV carries NO per-row upload dates; the July-7 window is established only
  by JFrog's blog (2026-07-07, 03:03:09–18:13:42 UTC, 215 packages / 333 releases).
- **Wave verification**: independent — each candidate's publish timestamp was
  read from its Diffend versions page (https://my.diffend.io/gems/<name>).
  Wave is assigned FROM the Diffend timestamp, never assumed from the Xray id.
- **Mechanism markers**: scanned from the Diffend version-diff pages
  (/gems/<name>/<version>, first version; latest too if the first is bare).

## Candidate selection
263 names whose `Xray ID` matches `XRAY-1079xxx` — the analysis batch in which
JFrog's newly-identified July-wave material clusters (named July examples
xss-test-gem, attacker-xss-admin-1, xssname-1783397821, test-apex-gem,
test-ssti-0/1/4, apex-black-* all fall in it). This is a CANDIDATE filter only:
sweep results may show some candidates are non-July waves.

## Method
- Read-only HTTP GET, ~1 req/3s pacing, UA
  `rubygems-july7-research/1.0 (read-only inventory sweep; no install)`.
- Diffend closes connections mid-fetch; every fetch retries (4 attempts,
  3s·2^n backoff). Failures are logged, never silently dropped.
- Resume-friendly: `diffend_sweep_results_july7.jsonl` is append-only with
  per-record completion; restarts skip names already present. Human-readable
  trail in `progress.log`.

## Outputs
- `diffend_sweep_results_july7.jsonl` — **264 records** (final, all verified).
  Summary after the 2026-09-28 re-sweep (`scripts/diffend_sweep_resweep_july7.py`,
  curl, 6s pacing, checkpointed): 18 in_diffend (9 original third-party July-7
  test gems + 9 new: 7 wave `2026-july-07` incl. 2 with `xss-exfil` markers, and
  2 wave `2026-may-27`), 246 verified-absent (HTTP 200 stub, no version links),
  **0 unverified**. Intermediate rows in `diffend_sweep_resweep_july7.jsonl`
  (167, kept for the audit trail).
- `progress.log` — timestamped run log (first pass + retry pass + top-up +
  resweep, incl. the VM-rebuild resume at 41/167).
- Elastic index `july7-wave` (own index; shared canonical schema at
  `notes/gems-es-mapping.json`; `event.dataset.keyword` at creation):
  **264 docs**, record_kind `diffend_sweep_july7`, keep-all.
- Scripts: `scripts/sweep_july7.py` (EXTRA_CANDIDATES covers named July gems
  outside the Xray batch; `--retry-failed` re-attempts phase-1 and phase-2
  connection failures), `scripts/es_ingest_july7.py`.
- Note: `notes/july7-wave-sweep-2026-09-27.md`.

## Deduplication
Exact-duplicate JSONL records were NOT collapsed (each name is unique);
ES _id = `july7:<name>` makes bulk re-ingest idempotent.

## Constraints honored
- Read-only; agents/infrastructure only — no operator identity, no registrant
  details, no person-focused attribution.
- No credentials were collected, used, or reproduced. No keys are stored.
- Nothing is claimed as verified without tool evidence (wave field is
  diffend_wave, sourced from the Diffend page itself).

## Raw layer 2026-09-29

- `diffend_sweep_results_july7.jsonl` -> `raw/diffend_sweep_results_july7.jsonl` and `diffend_sweep_resweep_july7.jsonl` -> `raw/diffend_sweep_resweep_july7.jsonl` (script-consumed sweep outputs; consumers: scripts/sweep_july7.py, es_upsert_july7_resweep.py, es_ingest_july7.py, diffend_sweep_resweep_july7.py). Upstream names preserved; raw layer exempt from event schema.

## Schema build 2026-09-29 (worker W5)

- events.jsonl: **264 records** (record_kind `diffend_probe`), one per row of
  the final sweep file `raw/diffend_sweep_results_july7.jsonl`.
- Dedupe decision: the intermediate resweep file
  `raw/diffend_sweep_resweep_july7.jsonl` (167 rows) was verified to be
  fully merged into the final 264-row file — every resweep name is present,
  and zero rows differ in outcome (`in_diffend`/`diffend_wave`/
  `first_publish` all identical). The resweep file is kept in raw/ as the
  audit trail but emitted NO separate events. Rows carrying
  `labels.diffend.resweep_pass = true` mark the reswept names.
- fingerprint identity string: `july7|<name>` (gem name is the natural key;
  ES `_id = july7:<name>` already idempotent).
- `@timestamp`: Diffend publish timestamp (`first_publish`, e.g.
  "July 07, 2026 18:43") normalized to ISO-8601 Z, with the raw string kept
  in `labels.diffend.first_publish_raw`; rows with no publish date (246 of
  264, verified-absent) use 2026-07-07T00:00:00Z with `timestamp_source =
  "dir_prefix:no_diffend_publish_date"`. The `versions` column's nested
  `{version, ts}` objects were flattened to `diffend.version_strings[]` +
  `diffend.version_timestamps[]` (flat-labels rule).
- Outcome split in this build: 18 in_diffend, 246 verified-absent,
  matching the lane summary.
- SHA256SUMS regenerated: covers events.jsonl + the 2 raw sweep files. The
  previous SHA256SUMS listed `raw/progress.log` and `raw/sweep-stdout.log`,
  which are not in raw/ — stale entries dropped.
- Verified: all 264 records validate; fingerprint recomputed by hand for two
  sample rows; `xss-test-gem` wave value cross-checked against the raw row.

## Rollup layer 2026-09-29 (worker W5)

- rollup.jsonl: **3 records** (record_kind `diffend_wave_rollup`,
  `event.dataset = 2026-07-07-july7-wave-rollup`) — one per wave bucket
  (`2026-july-07`: 16, `2026-may-27`: 2, `absent_from_diffend`: 246) with
  candidate/in_diffend/verified-absent/reswept counts, first/last publish
  timestamps, and distinct mechanism notes. Same shared schema.
- fingerprint identity string: `july7-wave-rollup|<wave>`.
- Covered by SHA256SUMS; counts verified against the event stream.

## 2026-09-28: ingest script co-located (hunt convention)
- `es_ingest_july7.py` moved from `scripts/` into this directory per
  Christopher's single-collection convention; transforms raw Diffend sweep
  JSONL into shared-schema docs (real transform, not a pure loader).
- `REPO_ROOT` in the script adjusted (repo root is now three levels up).
  Offline verification: `load_docs()` builds 264 docs from
  `raw/diffend_sweep_results_july7.jsonl`.
- `scripts/local_es_manifest.json` via_script entry repointed here.
- SHA256SUMS regenerated (script file added to coverage).

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_july7.py` at `raw/scripts/legacy/es_ingest_july7.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.
