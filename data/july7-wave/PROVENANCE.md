# Provenance — LANE J: July-7 wave Diffend sweep

## Sources
- **Candidate list**: JFrog's public GemStuffer inventory CSV,
  `data/gemstuffer-jfrog-2026-09-27.csv` (3,025 rows: Package, Versions, Xray ID),
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
- `diffend_sweep_results_july7.jsonl` — one JSON record per candidate:
  name, xray_id, jfrog_versions, in_diffend, http_status, versions[{version, ts}],
  first_publish, diffend_wave (verified from Diffend timestamp),
  mechanism_notes, mechanism_version_checked, name_grammars, diff_error.
- `progress.log` — timestamped run log.
- Elastic index `july7-wave` (own index; shared canonical schema at
  `notes/gems-es-mapping.json`; `event.dataset.keyword` at creation).
  record_kind: `diffend_sweep_july7`. Keep-all: every sweep record lands,
  discriminated by `in_diffend` / `diffend_wave`.

## Deduplication
Exact-duplicate JSONL records were NOT collapsed (each name is unique);
ES _id = `july7:<name>` makes bulk re-ingest idempotent.

## Constraints honored
- Read-only; agents/infrastructure only — no operator identity, no registrant
  details, no person-focused attribution.
- No credentials were collected, used, or reproduced. No keys are stored.
- Nothing is claimed as verified without tool evidence (wave field is
  diffend_wave, sourced from the Diffend page itself).
