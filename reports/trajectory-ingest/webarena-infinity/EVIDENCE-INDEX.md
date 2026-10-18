# WebArena-Infinity — evidence index

Lane: `webarena-infinity-trajectories`.
All paths are relative to `~/workspace/silent-locus` unless noted.

## Raw bytes

- `data/lanes/webarena-infinity-trajectories/raw/`
  - `gemini/`, `qwen/`, `kimi/` — 2,195 complete trajectories; each
    trajectory dir holds `history.json` (step record) and `result.json`
    (outcome record).
  - 134 partial dirs hold `history.json` only (no `result.json`) —
    the absent-at-rev set.
  - `MANIFEST.json` — per-file URL, retrieved-at, sha256, bytes
    (4,390 files, 111,068,835 bytes, rev
    `73cf7f57a6ff61c95722a23bffdd9c1de4069bfe`).
  - `_progress.jsonl` — per-file provenance (source URL,
    retrieved-at UTC, retrieval method `https-get`, sha256).
  - `_absent_at_rev.json` — the 134 trajectories absent at rev
    (gitlab-plan-and-track 89, gmail 45).
  - `LICENSE.note` — three verbatim license facts (tags `license:mit`,
    frontmatter `license: mit`, API record `license: null`).
  - `_enumerate.log`, `_download.log` — scraper logs.

## Review work

- `data/lanes/webarena-infinity-trajectories/working/`
  - `reviewer-A/` — gemini digests and flagged sets.
  - `reviewer-A-findings.json`, `reviewer-A-progress.jsonl`,
    `reviewer-A-kills.json` (24 kills).
  - `reviewer-B-findings.json`, `reviewer-B-progress.jsonl`,
    `reviewer-B-kills.json` (20 kills).
  - `verified-findings.json` — the 21 surviving findings with grade,
    confidence, quotes, step ranges, provenance, verifier notes.
  - `verifier-kills.json` = `adversarial-kills.json` — the 6 kills.
  - `cross-model-ctrl-check.txt` — qwen-specific ctrl+a loop control.
  - `judge-false-passed-169.txt` — all 169 judge=False + passed=True
    trajectories from the independent sweep.
  - `add-webarena.log` — the detached retry loop log (228+ LOCK_TIMEOUT
    attempts), then the finisher worker's self-add attempts; ends with
    `WEBARENA_ADD_OK` at 2026-10-18 03:11:26 UTC. Two bundle schema
    fixes were made mid-wait (see REPORT.md Method).
  - `bundle-webarena-infinity.json` — the submitted bundle
    (4,440 records, idempotency key
    `webarena-infinity-ingest-2026-10-17-v1`).
  - `verified-findings.json` (lane root) — committed copy of the 21
    findings; identical to the working copy.

## Writeups

- `reports/trajectory-ingest/webarena-infinity/writeups/`
  - `01-judge-verifier-disagreement.md`
  - `02-bundled-done-signal-integrity.md`
  - `03-security-downgrade-compliance.md`
  - `04-harness-credential-leak.md`
  - `05-irreversible-side-effects.md`
  - `06-client-data-leakage.md`
  - `07-error-blind-retry.md`
  - `08-tool-repurposing-observation-failure.md`
  - `09-narration-action-divergence.md`
  - `10-blind-submit-retry.md`
  - `INDEX.md`

## Factum records

- Exported batch: `data/records/bbc1348f5b204f6992426d84fe2cf60a/` (batch dir
  holds `records.jsonl` — 8,880 lines — + `manifest.json` receipt).
- 4,440 records: 1 source + 1 reference artifact + 1 run +
  1 dataset.snapshot + 2,195 dataset.record + 21 intel.behavior +
  2,195 `related_to` + 25 `supports` (+ 4,440 toolkit-auto `in_lane`
  edges in the export).
- Every record carries `tags.lane = "webarena-infinity-trajectories"`.

## Note on the RB-008 token

The credential-like `ak-` token in
`raw/kimi/elation-prescriptions/task_e17/result.json` (and task_e20) is
preserved only in the raw bytes. It was deliberately withheld from all
working files, the bundle, this report, and the writeups.
