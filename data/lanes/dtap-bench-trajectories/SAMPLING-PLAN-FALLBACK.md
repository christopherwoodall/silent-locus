# SAMPLING-PLAN-FALLBACK.md (draft, not executed)

Fallback if full-corpus download proves infeasible. Full corpus is 133,848
files / 3.75 GB (under the 5 GB brief threshold), so this plan is ONLY for
use if the parent authorizes it explicitly.

## Strata

- Harness x model (10 pairs): claudesdk/claude-opus-4-6, claudesdk/claude-sonnet-4-5,
  googleadk/gemini-3-pro-preview, openaisdk/gpt-5.1, openaisdk/gpt-5.2,
  openaisdk/gpt-5.4, openaisdk/gpt-oss-120b, openclaw/claude-opus-4-6,
  openclaw/gpt-5.2, openclaw/gpt-5.4
- Environment (14): browser, code, crm, customer-service, finance, legal,
  macos, medical, os-filesystem, research, telecom, travel, windows, workflow
- Split (2): benign, malicious

Cells: 10 x 14 x 2 = 280.

## Sample per cell

5 trajectory JSONs + their sibling judge_result.json, chosen by deterministic
seeded shuffle (seed 42) of the timestamped trajectory filenames in the cell.
Cells with fewer than 5 trajectories take all available.

## Expected yield

~2,800 files, ~80 MB. Covers every model, every environment, both splits.

## Known limitation

Judge-verdict stratification (task_success / attack_success classes) is NOT
possible without first downloading all 65,910 judge_result.json files.
If verdict balance matters, phase 1 = download all judge_result.json
(~100 MB), phase 2 = sample trajectories within verdict classes.

## Rationale

Preserves the fleet's analytic axes (model comparison, environment comparison,
benign-vs-malicious) at ~2% of corpus volume. Deterministic seed makes the
sample reproducible and extensible.
