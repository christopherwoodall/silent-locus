# PROVENANCE.md — 2026-10-11-openai-blog-intel (IOC Family C)

Ingest worker lane for OpenAI blog / system-card / alignment-post IOCs.
Branch: `ingest-openai-blog`. Worktree: `~/workspace/wt-ingest-openai/`.

## Source acquisition

The task's original caches under `/tmp/openai-blog-hunt/`, `/tmp/openai-safety-hunt/`,
and `/tmp/openai-systemcards-hunt/` were removed from the VM before retention
(discovered 2026-10-11 ~11:00 CDT; only `/tmp/skillchain-hunt` remained). All
sources were re-fetched from the same public URLs on 2026-10-11 ~16:11–16:16 UTC
via `curl -sL` with a Chrome 126 user agent through the egress proxy. Per-file
sha256, byte counts, HTTP status, and URLs are in `raw/SHA256SUMS.recovery`
(the manifest doubles as the recovery provenance record). Fetch script:
`raw/fetch-sources.sh`; text extracts for analysis: `raw/extract-text.py`.

Note: byte counts differ slightly from the original 15:4x UTC captures (e.g.
false-front-operations 637801 vs 637834 bytes) — dynamic page content.

The `/tmp/openai-safety-hunt/raw/PROVENANCE.txt` note said "DO NOT INGEST INTO
FACTUM — analysis only". Honored as: no full-text blobs are committed to Git;
raw HTML stays local-only in `raw/` (not committed). Only structured
extractions (intel.report / intel.behavior / intel.ttp / infra.ioc / claims /
run) are submitted, with summaries in the worker's own words and short
verbatim quotes. The Hugging Face incident technical-report PDF was re-fetched
but is represented only by the blog-post report record (no PDF text ingested).

## Sources (30)

OpenAI blog (11): false-front-operations, model-distillation-campaign,
eu-text-provenance, introducing-dots, computer-use-ironclad, gpt-6-astra,
path-to-astra, misalignment-reporting-framework, chatgpt-ambitious-work,
gpt-5-4-mini-nano, introducing-agents-api, hugging-face-incident blog.
Deployment Safety Hub (8): gpt-5-6-preview, gpt-5-6, gpt-5-6-august-update,
gpt-6-astra, gpt-6-1-sol, gpt-6-october, gpt-live, chatgpt-images-2-5.
Alignment Research Blog (9): argo, auto-review, laser, measuring-reward-seeking,
metagaming, metagaming-latents, monitorability-evals, validating-public-evals,
misalignment-reports. Plus the HF incident technical-report PDF.

## Dedup (2026-10-11)

Lane `openai-intel` (2026-10-10, batch 64772f041ae0486b95ffd6eda3aba2a5)
already ingested intel.report records for the gpt-6-october and gpt-6-1-sol
cards and 9 behaviors (blocker-deception, tool-limitation-nondisclosure,
auto-review-bypass, respecting-warnings, monitor-awareness-evasion,
math-side-tasking, sabotage v2, unintended-peer-engagement, coding-deception).
Those are SKIPPED here (see build_bundle.py header). The Astra-scoped
monitor-evasion behavior is included but explicitly distinguished.

Grep over all committed `data/records/*/records.jsonl` (index rebuild was
still running; grep fallback per standing rule):
- Zero hits: "Bogus Bylines", "Dark Clark", "Moonshot AI", "Politology",
  "La Compania", "Frontier Model Forum", "GPT-Red", "GPT-5.6 System Card",
  "misalignment-reports", all blog article URLs.
- "ExploitGym" hits are a HuggingFace dataset (SpeckledCerberus/exploitgym-answers),
  unrelated to the ExploitGym evaluation suite.
- "ARGO" hits are "cargo" false positives; "LASER" hit is "sharklasers"
  (disposable-email IOC); "Kimi" hits are Kimi model IDs in trajectory datasets.
- "Auto-review" hit is the openai-intel "Respecting Auto-Review" eval record;
  this lane's auto-review record describes the oversight mechanism itself
  (released in Codex), a distinct observation.

## Records

145 records in `bundle.json` (builder: `build_bundle.py`, idempotency key
`openai-blog-intel-2026-10-11-v1`):
- 3 source, 27 intel.report, 15 intel.behavior, 8 intel.ttp, 77 infra.ioc,
  14 graded claims (OBSERVED/UPSTREAM), 1 run.
- Every record tagged `{"lane": "2026-10-11-openai-blog-intel"}`.
- No edges. No blobs. No redactions.

## Schemas

No new schemas added. Used installed packs only: factum-intel 1.0.0
(intel.report, intel.behavior, intel.ttp), factum-infra 1.0.0 (infra.ioc),
factum-core 1.0.0 (source, claim, run).
