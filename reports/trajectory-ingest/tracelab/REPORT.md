# TraceLab Trajectory Ingest — Report

Date: 2026-10-16. Lane: `tracelab-trajectories`. Branch: `work`.
Fleet: trajectory-ingest, wave 4 (final, ingestor). BigSexyWarlock69 owns the fleet.

This document uses ASD-STE100 style. Short sentences. Simple words.
Terms are defined when first used.

**Terms.** *Ingest* means: copy verified findings into the factum database
as structured records. *Factum* is the shared evidence database. *SECONDARY*
means: the fact comes from a document, not from direct measurement.
*OBSERVED* means: the fact comes from a direct measurement or procedure we
ran. *MEDIUM / HIGH* is the verifier's confidence in the fact.

## Purpose

File the verified TraceLab findings from the wave-3 verifier into factum.
Close the residual novelty gap. Leave a retry path for the five blocked
data artifacts. Close out the fleet.

## What TraceLab is

**TraceLab** (TraceLab Coding Agent Workload Traces) is a dataset by the SyFI
Lab, University of Washington. It holds sanitized traces of real-world
coding-agent use. Providers: Claude Code and Codex. Paper: arXiv:2606.30560.

**Baseline character:** benign real-world coding-agent use. The traces are
production workloads, not attack simulations. The dataset supports
structural-behavior analysis only. Prompts, responses, tool inputs, and tool
outputs are removed by design. Identifiers use stable pseudonyms.

**What this means for the hunt:** TraceLab cannot show agent
misuse by content. It can show misuse by shape. Recovery loops
(RECOVERY class) and tool-misuse patterns (TOOL-MISUSE class) are
structurally visible: retry bursts, error statuses, latency anomalies,
command skeletons. The following classes are unobservable by design:
PROMPT-INJECT (prompts removed), CREDENTIAL (paths and secrets removed),
CAPTCHA (no account surfaces in coding traces), ACCOUNT (users are
pseudonymous, no account data), COORDINATION (single-user sessions, no
cross-agent links published). If the data plane ever becomes reachable,
the useful hunts are structural: recovery-loop mining and tool-misuse
signatures in the 743,819 tool calls.

## Sources

- HuggingFace dataset page: `https://huggingface.co/datasets/UW-SyFI/TraceLab`
- Revision: `7256bbf77e76d5cb83f4ddbd5ad31d8faee9dc7a`
- Retrieved files (4 of 9): README.md, LICENSE-DATASET.md, NOTICE,
  SHA256SUMS. Each carries a `.PROVENANCE.txt` sidecar (source URL,
  retrieval time, method `https-get-curl`, sha256 recompute-match).
- Cached bytes: `data/lanes/tracelab-trajectories/raw/` (9,981 bytes).
- Blocked (5 data artifacts): the jsonl.gz, three parquet configs, and
  the DuckDB build. See "Coverage gap".

## Method

1. **Novelty check.** Searched factum structured records and the legacy
   corpus before filing.
   - `match --text "TraceLab" --mode fuzzy`: noise only
     (Tracefort-io/exploitgym fork, county.json "trace" notes,
     hanzoai/telemetry-go/trace).
   - `match --text "UW-SyFI" --mode fuzzy`: not_found.
   - `match --text "<revision-hex>" --mode fuzzy`: trigram-fragment noise
     only, no exact revision hit.
   - `grep -ri "tracelab|uw-syfi"` over `evidence/` and `lists/`:
     zero hits.
   - Result: no existing factum record, no legacy overlap. The dataset is
     new to the corpus.
2. **Bundle build.** Assembled 25 records: 5 sources, 10 observations,
   9 claims, 1 run. Every record carries `tags.lane =
   "tracelab-trajectories"`, including bundle-local sources. Claims cite
   observations only, never sources. No edges during ingest (separate pass
   rule).
3. **Submit.** `factum.py add --input` with run-scoped idempotency key
   `tracelab-wave4-ingest-20261016`. Retried through sibling lock
   contention (40–60 s sleeps). Exported and validated the batch file.
4. **Commit.** Explicit pathspecs only on the shared `work` branch.

## Findings (as verified, grades as given)

1. **Dataset identity and scale (SECONDARY, MEDIUM).** `UW-SyFI/TraceLab`,
   revision `7256bbf77e76d5cb83f4ddbd5ad31d8faee9dc7a`, release v0.0.2.
   README states: 665,453 agent steps / LLM invocations, 8,058 sessions,
   743,819 normalized tool calls, 52 pseudonymous users, providers
   Claude Code + Codex. README.md L33, L37–42. README sha256
   `d0ff5ce6efe642b0ac9a79683c30acd68e9409d650d76c4174e86fc8518aa0ed`
   recomputed match.
2. **Rounds schema, README-stated (SECONDARY, MEDIUM).** Default config
   `rounds`, 665,453 rows keyed by `round_pk`. Fields: pseudonymous
   provider/session/round identifiers, model, token counts, cache-prefix
   accounting, source store, `trace_key`. Token fields:
   `input_tokens_total`, `prefix_tokens`, `newly_append_tokens`,
   `output_tokens`. README.md L62, L95–96, L102–105. Parquet bytes NOT
   observed.
3. **Tool-calls schema, README-stated (SECONDARY, MEDIUM).** 743,819
   normalized tool calls keyed to `rounds.round_pk`. Fields: tool name,
   pseudonymous tool-call id, timestamps, input/result char counts,
   latency, error status, executable labels, command skeletons. "Full
   tool inputs and outputs are not published." README.md L97, L107–110.
   Bytes NOT observed.
4. **Timing-events schema, README-stated (SECONDARY, MEDIUM).**
   2,688,829 ordered events keyed to `rounds.round_pk`. `event_index`
   preserves per-round order. README.md L98, L109. Bytes NOT observed.
5. **Sanitization and responsible use (SECONDARY, MEDIUM).** Identifiers
   replaced with stable pseudonyms. Local paths, cwd, tool inputs,
   prompts, responses, full tool outputs removed. README.md L115–124;
   LICENSE-DATASET.md privacy section. Explicit re-identification
   prohibition. This is out of hunt scope: no operator-identity work.
6. **License (SECONDARY, HIGH on doc text).** Trace data CC-BY-4.0. Source
   code Apache-2.0. Attribution: TraceLab (SyFI Lab, University of
   Washington). LICENSE-DATASET.md sha256
   `1e96a0ec55f98ee0e4e2432626c0201104ebfb7f98cecf0a31d5313ddad92e9a`
   recomputed match. NOTICE agrees.
7. **Coverage gap — data plane egress-stalled (SECONDARY, HIGH).** 4 of 9
   files downloaded (docs only, 9,981 bytes). All 5 data artifacts are
   gaps: jsonl.gz (100,939,722 B), rounds/train.parquet (22,785,108 B),
   tool_calls/train.parquet (25,909,050 B), timing_events/train.parquet
   (28,511,584 B), DuckDB build (160,182,272 B). `raw/data/` has 0 files.
   The XET redirect chain is healthy (public 302s, X-Xet-Cas-Uid=public,
   ETags match SHA256SUMS char-for-char). GETs to `us.aws.cdn.hf.co`
   stall through this VM's egress proxy (curl rc=28, ~96 attempts, one
   transient 36.9 MB window then drop). Evidence: MANIFEST.json +
   XET_EVIDENCE.txt in `raw/`.
8. **Novelty within factum (OBSERVED procedure, MEDIUM).** No existing
   factum record for the dataset. Searches above. Scope: structured
   factum records plus legacy internal corpus.
9. **Provenance completeness (SECONDARY, HIGH).** All 4 docs carry
   `.PROVENANCE.txt`: source_url, retrieval times
   2026-10-16T21:02:35Z–21:04:05Z, method `https-get-curl`, sha256
   recompute-match.

## Killed: none

No finding was killed. The verifier passed 9 of 9. Nothing was
retracted or downgraded during ingest.

## Overlap: none

The novelty searches found zero overlap. Nothing was skipped as
duplicate. No existing record was linked or superseded.

## Ingest record

- Factum batch: `<batch-id from export>` (see EVIDENCE-INDEX.md).
- 25 records: 5 sources, 10 observations, 9 claims, 1 run.
- 0 edge records (edges are a separate pass).
- Actor: `agent:tracelab-ingestor-wave4`. Idempotency key:
  `tracelab-wave4-ingest-20261016`.
- Lane tag on every record: `tracelab-trajectories`.

## Open questions

1. **The five blocked artifacts.** Retry the data plane from a host with
   healthy egress (not through this VM's proxy). Steps:
   - Read `data/lanes/tracelab-trajectories/raw/XET_EVIDENCE.txt` for the
     exact stall signature.
   - Resolve each file: `https://huggingface.co/datasets/UW-SyFI/TraceLab/resolve/7256bbf77e76d5cb83f4ddbd5ad31d8faee9dc7a/<path>`.
     Expect a public 302 to `us.aws.cdn.hf.co/xet-bridge-us/...` with
     `X-Xet-Cas-Uid=public`.
   - Verify `X-Linked-ETag` equals the SHA256SUMS entry char-for-char
     before downloading (sizes and hashes are in
     `data/lanes/tracelab-trajectories/raw/MANIFEST.json`).
   - Download with `curl -C -` (resume) — the redirect chain already
     proved healthy; only this VM's data-plane leg stalls.
   - On success: verify sha256 against MANIFEST.json, then run a new
     ingest wave for the actual bytes (schemas 2–4 can move from
     README-stated to observed).
2. **Byte-level verification of schemas 2–4.** Until the data plane
   works, every schema field stays tagged `README-stated-not-observed`.
   Do not present these fields as measured.
3. **Hunt value after retrieval.** Mine the 743,819 tool calls for
   structural TOOL-MISUSE and RECOVERY signatures (retry bursts, error
   statuses, latency anomalies, command skeletons). Do not attempt
   content analysis: prompts and outputs are not in the dataset.
4. **Re-identification prohibition.** The license bans re-identification.
   All future work on TraceLab stays structural. No operator-identity
   work, ever.
