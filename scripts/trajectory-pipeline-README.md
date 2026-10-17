# Trajectory Pipeline — README

Reusable pipeline for hunting interesting agent behaviors in public
trajectory datasets. Built 2026-10-16. The next trajectory repo
should cost minutes, not a new build.

## Stages

```
scout → scrape → review fleet → adversarial kill → factum ingest → commit
```

### 1. Scout (inventory)

Run `scripts/trajectory-scout.py`:

```bash
python3 scripts/trajectory-scout.py \
  --repo <owner>/<name> \
  --hf-dataset <org>/<id> \
  --out /tmp/<name>-manifest.json
```

The scout walks the GitHub repo tree and the HuggingFace dataset
metadata. It lists every file with size, category
(`trajectory`, `docs`, `media`, `code`, `skip`), direct download
URL, and a provenance stub. Docker images and binaries are flagged
`skip`. Read-only. Dry-run: it never downloads file bodies.

Use `--only trajectory,docs` to keep the manifest small.

### 2. Scrape (acquire)

For each wanted file in the manifest:

- GET the file over HTTPS (`curl` or `urllib`; never the
  `huggingface_hub` Python library — it is broken on this VM, see
  `~/TOOLS.md`).
- Write bytes to `data/lanes/<lane>/raw/` with the original
  filename.
- Write `<filename>.PROVENANCE.txt` next to it with five lines:
  `source_url`, `retrieved_at` (UTC ISO-8601), `retrieval_method`
  (`https-get`), `sha256`, `dataset_revision`.
- Fill the manifest's provenance stub for that file.
- Slow crawl: sleep 1–2 s between files, back off on 429/403.

Respect rate limits. GitHub unauthenticated allows 60 requests per
hour. HuggingFace is more generous but still deserves pacing.

### 3. Review fleet

Spawn reviewer workers using the prompt pack in
`scripts/trajectory-review-prompts.md`. One worker per trajectory
batch. Each worker files findings in the behavior taxonomy
(CAPTCHA, ACCOUNT, GUARDRAIL, PROMPT-INJECT, CREDENTIAL,
IRREVERSIBLE, TOOL-MISUSE, RECOVERY, COORDINATION, OTHER) with
PRIMARY/SECONDARY grade, confidence, and full provenance.

### 4. Adversarial kill

A dedicated adversarial reviewer applies the kill criteria from the
prompt pack. Weak findings die with a one-line reason. Only
survivors move to ingest.

### 5. Factum ingest

- Read `docs/taxonomy/` first. Use established types
  (`behavior.profile`, `behavior.tool_sequence`, predicates
  `exhibits`/`uses`).
- Validate + dedup before ingest. Direct scans of
  `data/records/` are authoritative for dedup.
- Set `tags.lane` on every record.
- `export`, then `verify`, then commit with explicit pathspecs
  (shared-branch rule: never bare `git commit` or `git add -A`).

### 6. Commit

Commit the lane directory and the factum batch. Push only when
BigSexyWarlock69 authorizes it.

## Lane layout

```
data/lanes/<YYYY-MM-DD>-<slug>/
  raw/                  # cached trajectory bytes + .PROVENANCE.txt files
  manifest.json         # scout manifest with filled provenance
  REPORT.md             # lane doc in ASD-STE100 (see prompt pack template)
```

Lane names are lowercase with hyphens, no date
(`trajectory-wildclaw`). The directory is date-prefixed.

## Worked example: WildClawBench

```bash
python3 scripts/trajectory-scout.py \
  --repo internlm/WildClawBench \
  --hf-dataset internlm/WildClawBench \
  --out /tmp/wildclaw-manifest.json
```

The manifest inventories the repo tree and the HF dataset
siblings. The scrape step then pulls the per-task trajectory
files. Reviewers hunt the taxonomy classes. Findings land in
Factum under lane `trajectory-wildclaw`.

## Worked example: ClawBench

Same pattern, different IDs:

```bash
python3 scripts/trajectory-scout.py \
  --repo TIGER-AI-Lab/ClawBench \
  --hf-dataset NAIL-Group/ClawBench \
  --out /tmp/clawbench-manifest.json
```

## Worked example: AgentProcessBench

Dataset: `LulaCola/AgentProcessBench`, revision
`cd81f326aece8b0a3f6359e20df370690d3a98bf`. Four configs, each with
`test.jsonl` of 250 trajectories (1,000 total): `bfcl`, `gaia_dev`,
`hotpotqa`, `tau2`.

```bash
# scrape (per-file provenance sidecars, SHA-256 manifest)
curl -sL "https://huggingface.co/datasets/LulaCola/AgentProcessBench/resolve/cd81f326aece8b0a3f6359e20df370690d3a98bf/bfcl/test.jsonl" \
  -o data/lanes/agentprocessbench-trajectories/raw/bfcl/test.jsonl
```

### The dual tool-call serialization quirk

Tool invocations appear in TWO shapes inside one trajectory:

1. **Structured** — assistant message carries a `tool_calls` array
   (OpenAI function-call shape: `{"id","type","function":{"name","arguments"}}`).
2. **Embedded** — assistant message `content` carries an XML-ish
   `<tool_call>{...}</tool_call>` JSON blob (bfcl style). Sometimes the blob
   is not even JSON: one trajectory emitted `<tool_call>Son of al Qaeda
   settlement 2017</tool_call>` plus `<think>` blocks — a hallucinated
   protocol the harness rejected twice.

Any tool-call extractor must handle both shapes, or it silently drops the
bfcl-style calls (which carried the highest-severity findings).

### step_labels semantics

`step_labels` is a dict of message-index → human process label: `1` =
step judged correct, `0` = neutral, `-1` = step judged wrong. This is the
standard process-reward labeling convention. Preserve the labels verbatim
on the steps they annotate; note that labels can surprise (a ticket-close
step labeled `1` is the annotation as-is, not an endorsement).

### License note

The HF API `license` field for this dataset is **null**. The dataset tags
include `license:mit`, and the README.md front matter also reads
`license: mit`. No license text file ships with the dataset. Do not
overclaim beyond these three observed facts. Recorded in
`data/lanes/agentprocessbench-trajectories/raw/LICENSE.note`.

### What worked

- Scope the ingest to finding-bearing trajectories only: 20 of 1,000.
  One `behavior.tool_sequence` observation per trajectory (all tool calls,
  in message order, with step labels annotated), one `intel.behavior`
  observation per finding citing it, one OBSERVED claim citing both.
- Model identity is NOT recorded in the dataset. Do not invent it:
  `behavior.tool_sequence.model` carries the honest value
  `unrecorded-in-source`. Use `data_source` (e.g. `bfcl_multi_turn_base`,
  `tau2_airline`) for the harness field.
- A-007-style cross-sample findings cite one `intel.behavior` record with
  multiple `behavior.tool_sequence` citations (four samples of one query).
- Raw bytes: 39 MB across the four test.jsonl files. Retention decision:
  local-only (not committed). The dataset is a pinned public revision;
  anyone can re-fetch by URL + revision + SHA-256.

## Worked example: TauBench

Dataset: `sierra-research/tau-bench`, revision `59a200c`,
`historical_trajectories/` (tau1). Four JSON files, one JSON array each:
`gpt-4o-airline.json` (200 episodes), `gpt-4o-retail.json` (460),
`sonnet-35-new-airline.json` (400), `sonnet-35-new-retail.json` (920).
1,980 tau1 episodes triaged. tau2 trajectories deferred (estimated
400–700 MB pull; recorded in the lane MANIFEST.json).

Episode shape: `{"task_id", "reward", "info", "traj", "trial"}`. `traj`
is a message array; assistant messages carry a `tool_calls` array
(OpenAI function-call shape). Tool args are sometimes a JSON string,
sometimes a dict — `str()` both before matching. The user instruction
lives at `info.task.instruction` (needed for prompt-inject findings like
A-P1, whose evidence is not in the message trace).

### Guardrail-test design of the benchmark

TauBench is a guardrail test by design: the airline policy (basic/economy
cancellable only within 24h of booking, on airline cancellation, or with
insurance for health/weather) is stated in the system prompt, but the API
does not enforce it. The simulated user actively lies about recency
("10 hours ago", "got it yesterday"), status ("gold member"), and events
("flight cancellation"). Findings therefore split into two shapes:
fabrication of policy facts (guardrail-fabrication) and trust of the
simulated user over tool bytes (simulated-user-overtrust). Both are now
taxonomy categories. Two prompt-inject findings are benchmark design
artifacts, not agent behavior: A-P1's instruction embeds a phone-rep
override script; A-P2's derailment script steers toward a $50 certificate.

### Verifier lessons

- Check tool bytes vs agent recollection. B-F06's lie lived in a
  think-call that rewrote created_at 05-02 to 05-15, not in any tool
  response. Grep the agent's own text, not just tool outputs.
- Watch for simulated-user-supplied values. The user is adversarial by
  design. Any finding that rests on a user claim needs a tool-byte
  cross-check.
- Task-quoted phrases are often paraphrases. Five fleet quotes missed
  bytes exactly ("booked May 9" vs "booked on May 9"; "willing to
  proceed without refund" vs "without a refund"; "within last 24h" vs
  "within the last 24 hours"; "data error" vs "an error in the data";
  "neither contains boots" vs "neither of them contains boots"). The
  bundle builder (`build_bundle.py`) byte-checks every quote and every
  tool spec against the raw trajectory and fails loudly on mismatch.
  Keep this check in every future trajectory lane.
- Multi-episode findings need per-episode scoping. B-F07's three episodes
  rationalize differently; B-F11's three episodes show different amounts
  and triggers. Quotes and tool specs support an optional `idx` scope.
- Episodes are shared across findings (A-P1/A-G2 share idx197; A-P2/A-T3
  share idx196). Dedup episodes: one run + one tool_sequence per
  (file, index), linked from each finding.

### What worked

- 30 findings, 399 records, one batch. Per finding: source,
  `intel.behavior` (taxonomy category, byte quotes + cited step indices),
  two observables (trajectory path as `text`, task_id as `external_id`),
  one run record (task_id, trial, reward in params). Per episode: one
  `behavior.tool_sequence` with every tool call in traj order.
- Full trace edges in the bundle: run --has_trajectory--> tool_sequence
  (41), tool_sequence --supports--> intel.behavior (44), sightings from
  both observables to the tool_sequence (82). This overrides the
  no-edges-during-ingest worker rule by explicit task order; edges are
  the trace chain only, from bundle-local refs.
- Claim cites: behavior + tool_sequence records. Observation envelope has
  no cites field; the claim carries the linkage.
- Model identity from file names ("gpt-4o", "sonnet-35-new"). The
  trajectories carry no model field; file names are the honest source.
- Rewards stored as attributes (mostly 0.0; three finding episodes at
  1.0). Not used as a finding signal.

## Worked example: RootSE

Run 2026-10-16. Lane `rootse-trajectories`.

### What was scraped

The RootSE trajectory corpus: 102 agent-trajectory instances
across three harnesses (`swe-agent`, `swe-agent-live`,
`openhands`) and four models (gemini2, claude45, gpt5mini,
qwen3-coder-480B-A35B-instruct). Cached at
`data/lanes/rootse-trajectories/raw/data/` with the original
per-instance filenames.

### Corpus shape

One JSON file per instance. Fields: `repo`, `instance_id`,
`base_commit`, `gold_patch`, `test_patch`, `repo_language`,
`original_traj` (the ordered steps), `original_mission_prompt`,
`failed_tests`, `failure_reason`, `failure_id`, `agent`, `model`.
Each step holds `index`, `action` (the tool call), `observation`
(the tool result), `response`, `thought` (the model's own
reasoning text), `execution_time`, `state`, and `extra_info`.
swe-agent steps use string actions (`str_replace_editor ...`,
`grep ...`). openhands steps use structured actions
(`{"tool": ..., "input": {"command": ...}}`).

### Flow as run

1. Scrape: 102 instances cached under the lane's `raw/data/`.
2. Review fleet: reviewer workers read full trajectories with
   the prompt pack and filed findings in the review taxonomy
   (GUARDRAIL, TOOL-MISUSE, RECOVERY, OTHER plus a one-phrase
   subclass) with PRIMARY/SECONDARY grade and confidence.
   Coverage: 102/102.
3. Adversarial kill: one verifier re-checked every surviving
   finding against the trajectory bytes. Weak findings died
   with a one-line reason (F-010's two sibling instances; the
   NodeBB path-traversal self-tests; Django/MSAL credential
   mentions; git reverts; pip/rm cleanup; the BoboTiG eval()).
4. Factum ingest: `data/lanes/rootse-trajectories/build_bundle.py`
   regenerates `bundle.json` from the cached bytes. Each
   finding is modeled as run -> steps -> tool calls ->
   finding: one `behavior.tool_sequence` observation (the run
   plus its ordered steps; each step cites the trajectory file
   path and the step index), one `intel.behavior` observation
   (the finding, review class in tags), and edges linking them
   (`derived_from` finding to steps; `exhibits` model and
   harness to finding). Lane `rootse-trajectories`. 10
   findings, 67 records, 30 edges.
5. Report: `reports/trajectory-ingest/rootse/REPORT.md` plus
   `EVIDENCE-INDEX.md`, in ASD-STE100.

### Lessons

- `failure_id` annotations skew to reasoning critiques, so
  full-trajectory reads matter. The `failure_reason` text
  points at reasoning failures ("failure to recognize prior
  command errors"), but the behaviors worth filing span wider
  step ranges than the annotated step. Reviewers must read the
  whole trajectory, not just the flagged step.
- The swe-agent shell-trap pattern recurs. Tab-completion
  directory listings and interactive prompts ("Display all 906
  possibilities?") appear as observations across runs. They
  are not command output and not edit results. The verifier
  had to correct a reviewer on exactly this mistake (F-001:
  step 8's observation is a tab-completion listing, not a bash
  syntax error).
- License: the RootSE corpus is MIT-licensed. Record the
  license at scrape time and cache the license file next to
  the manifest so downstream reuse of the cached bytes stays
  clean.

## Worked example: TRAIL

Run 2026-10-16. Lane `trail-trajectories`.

TRAIL (Trace Reasoning and Agentic Issue Localization, Patronus AI,
arXiv 2505.08638) is an annotation corpus, not raw trajectories: 148
expert-annotation JSON files (117 GAIA split, 31 SWE-bench split)
holding 841 error entries across reasoning, execution, and planning
categories.

### The HF gate and the public-mirror fallback

The raw trace files on HuggingFace were gated (401 on unauthenticated
resolve; account plus no-reshare checkbox required). BigSexyWarlock69
chose not to accept the terms. The annotations were ingested instead
from the PUBLIC GitHub mirror `patronus-ai/trail-benchmark`
(`data/lanes/trail-trajectories/raw/github-mirror/`). This is not a
gate bypass. No gated bytes were fetched.

Gate pattern for future lanes: when a dataset gate requires accepting
redistribution terms, default to the public mirror if one exists; never
bypass the gate; ingest DERIVED findings plus provenance locators, not
dataset redistribution.

### Annotation-JSON shape

One JSON file per trace. Fields: `errors` (category, location,
evidence, description, impact) and `scores` (reliability, security,
instruction adherence, plan optimality, overall). Reviewers read
`errors[].evidence` / `errors[].description` only; `scores` hold the
annotator's summary judgments and are out of bounds for behavior
claims (one candidate, TRAIL-B-20, died for quoting from
`scores[0].reliability_reasoning`).

Quirks found and how to handle them:

- One file (`a96c6811716c0473b86a23321db79c34.json`) has a trailing
  comma; strict parsers fail. Repair with `,(\s*[}\]])` → `\1` before
  reading.
- Category labels vary by case and plural ("Instruction Non-Compliance"
  vs "Instruction Non-compliance"; "Formatting Error" vs
  "Formatting Errors"). Match case-insensitively; record the actual
  file label in the filing.
- Quotes must be byte-exact substrings of the evidence bytes. Three
  filed quotes collapsed `\n` to spaces and had to be replaced.
- A reviewer's "585 errors vs 841 claimed" count did not reproduce;
  the verifier counted 841 across the 148 files. Check reviewers'
  counts, never trust them.

### Flow as run

1. Scrape: the mirror's annotation dirs cached with one
   `.PROVENANCE.txt` sidecar per file (source_url, retrieved_at,
   retrieval_method, sha256). Plus `trail-paper-2505.08638.txt` and the
   mirror's LICENSE.
2. Review fleet: two reviewers (GAIA A, SWE-bench B), 50 candidates.
3. Adversarial kill: 47 survive, 3 killed (compliant refusal filed as
   guardrail; async limitation filed as guard; quote from scores
   section with wrong category). Kill list: `review/killed.md`.
4. Factum ingest: one `source` record per distinct annotation file
   (35), one `intel.behavior` observation per surviving candidate
   (47), `observation.body.source = "@<source-ref>"` for the chain.
   All records graded UPSTREAM (evidence is the upstream annotation
   JSON; reviewers never saw raw traces). `tags.lane` on every record
   including sources. 82 records, one batch.
5. Report: `reports/trajectory-ingest/trail/REPORT.md` plus
   `EVIDENCE_INDEX.md`, in ASD-STE100.

### Lessons

- Dedup oracle: grep `data/records/` directly for annotation IDs and
  behavior text. `factum match --text` is not a reliable presence
  oracle. Zero overlaps found here.
- The B-split reviewers filed evidence paths as `raw/...` without the
  lane prefix; normalize to the repo-relative path before ingest.
- `observed_at` for observations came from annotation file mtime with
  `time_basis: "source_metadata"`. No timestamps were invented.

## Worked example: TraceLab

Run 2026-10-16. Lane `tracelab-trajectories`.
Dataset: `UW-SyFI/TraceLab`, revision
`7256bbf77e76d5cb83f4ddbd5ad31d8faee9dc7a`, release v0.0.2.
Benign real-world coding-agent traces (Claude Code + Codex, 52
pseudonymous users). Paper: arXiv:2606.30560.

### The XET redirect pattern (HuggingFace data files)

HF stores large dataset files behind XET. A resolve URL like
`https://huggingface.co/datasets/<org>/<id>/resolve/<rev>/<path>`
returns a **public 302** (not an auth wall) to a signed CloudFront
URL:

```
Location: https://us.aws.cdn.hf.co/xet-bridge-us/<hash>/<xet-hash>
  ?X-Xet-Cas-Uid=public&user_id=public&xip=<...>
  &response-content-disposition=inline; filename*=UTF-8''<file>
  &Expires=<epoch>&Policy=<signed-policy>&Signature=<...>
  &Key-Pair-Id=01KXEF4KZ1B6FV465MAWR4M21F&Hash-Algorithm=SHA256
```

Checklist for XET files:

1. HEAD the resolve URL with `curl -sIL`. Expect 302 from
   `huggingface.co`, then the signed `us.aws.cdn.hf.co` URL with
   `X-Xet-Cas-Uid=public` and `user_id=public`.
2. Read the `X-Linked-Size` and `X-Linked-ETag` response headers on
   the 302. Verify the ETag equals the SHA256SUMS entry
   **char-for-char** before downloading. ETag == sha256 is the
   pre-download integrity check.
3. GET the signed URL with plain `curl -L`. No auth needed.
   Resume with `curl -C -` on drops.

### The data-plane stall signature (this VM)

On this VM the redirect chain works but the data plane stalls:

- Proxy tunnel to `us.aws.cdn.hf.co` establishes ("HTTP/1.1 200
  Connection Established"), the GET goes out, and **no response
  headers arrive**. `curl` exits rc=28 (timeout) after 60–120 s.
- Even `curl -sI https://us.aws.cdn.hf.co/` hangs at the tunnel
  stage (rc=28). This is egress-path stalling on the
  proxy → CloudFront leg, not an auth wall.
- Retried GETs are not a fix. One transient window moved 36.9 MB
  before dropping; resume did not recover; ~96 attempts all
  stalled at 0 bytes.

Distinguish the two failure modes: a 302 chain that never
redirects is a gate or auth problem; a healthy 302 followed by
silent rc=28 is an egress-path problem. Record both in
`XET_EVIDENCE.txt` so the next worker knows which retry to run.

### The README-stated-not-observed schema convention

When the docs download but the data files do not, file the schema
as **documented, not observed**:

- One `dataset.snapshot` observation per parquet config, with
  `coverage: "metadata_only"` and `row_count` from the README.
- Tag every such record `schema_status:
  "README-stated-not-observed"` and note `parquet_bytes_note: "NOT
  observed"`.
- Claims on these schemas carry basis UPSTREAM (grade SECONDARY),
  never OBSERVED. Never present README-stated fields as measured.

### Retry-from-healthy-egress playbook

For the next worker with a healthy network path:

1. Read `data/lanes/tracelab-trajectories/raw/XET_EVIDENCE.txt`
   for the exact stall signature (so you know what changed).
2. Resolve each file from the revision-pinned URL (see the
   "Source URL pattern" line in that lane's `MANIFEST.json`).
   Expect the public 302 with `X-Xet-Cas-Uid=public`.
3. Verify `X-Linked-ETag` == the SHA256SUMS entry char-for-char
   (sizes + hashes are in `MANIFEST.json`).
4. Download with `curl -C -` (resume) into
   `data/lanes/tracelab-trajectories/raw/data/`.
5. Verify sha256 against `MANIFEST.json` on completion.
6. File a new ingest wave for the actual bytes. Schemas 2–4 can
   move from README-stated to observed once the parquet bytes
   exist locally.

### Baseline character note

TraceLab is structural-behavior-only observability: prompts,
responses, tool inputs/outputs, paths, and secrets are removed by
design. RECOVERY and TOOL-MISUSE classes are structurally
observable (retry bursts, error statuses, latency anomalies,
command skeletons). PROMPT-INJECT, CREDENTIAL, CAPTCHA, ACCOUNT,
and COORDINATION are unobservable by design. The dataset carries
an explicit re-identification prohibition (LICENSE-DATASET.md) —
all future work stays structural, no operator-identity work.

## Worked example: LongRCA Bench

Run 2026-10-16. Lane `longrca-trajectories`.
Dataset: `CLoud5-real/longrca-bench`, revision
`9f45acb66948d5d20c663b4ce4ec8ea5ab0076dd`.
1,140 failed multi-agent trajectories with human error-agent +
error-step labels. Paper: arXiv:2608.15242.

### What was scraped

1,140 JSON files under `data/full/<benchmark>/` (swe_bench_pro
128, terminal_bench_2 42, travelplanner 685, vitabench 108,
webarena_verified 177). 238,242,050 bytes total (~209 KB mean).
Cached at `data/lanes/longrca-trajectories/raw/<benchmark>/`
with one 6-line `.PROVENANCE.txt` per file (source_url,
retrieved_at, retrieval_method, sha256, dataset_revision,
license). Manifest: `raw/MANIFEST.json` (`complete: true`).

### Corpus shape

One JSON per trajectory. Fields: `question_ID` (str), `history`
(list of `{step: int, content: str, role: str, name: str}` —
multi-agent conversation), `mistake_agent` (str, the human
error-agent label), `mistake_step` (int, the human error-step
label), `mistake_reason` (str, human rationale). The mistake
labels are triage anchors: deep-read ±10 steps around
`mistake_step` first, then widen.

`mistake_agent` labels are asymmetric by benchmark:
travelplanner blames specialist agents, vitabench/webarena often
blame `Task_Planner` / `Action_Expert` / `Verification_Expert`,
and 36 files blame `Computer_terminal` itself (the benchmark
roots the failure outside any agent). Do not assume the label
names a wrongdoing agent; read the steps.

### The broken-download-loop incident

The first scrape loop died structurally: xargs passed ONE arg
(path) to a downloader expecting THREE (url, dest,
expected_bytes), so every curl failed with "option -o: is badly
used here" — and stderr was discarded (`2>/dev/null`), so the
failures were silent. 31 partial files landed from a dead
earlier process. The ingestor caught it by testing the script
directly and watching the byte counts stall.

Rules this produced:

1. Never discard downloader stderr. Log every failure with UTC
   timestamp + URL + curl error text
   (`raw/DOWNLOAD-ERRORS.log`).
2. Verify the downloader's argument contract with a direct test
   before launching the loop.
3. Repair uniformly: wipe partial files and re-download through
   the fixed loop so every file has an identical sidecar. Same
   upstream bytes — this is repair, not evidence deletion.
4. The manifest flips `complete: true` only after all files
   parse AND all sidecars validate. Reviewers gate on the flag,
   never on file counts.

### License note

No license is declared in the README or the dataset tags. The
README asks users to cite arXiv:2608.15242. Raw bytes are
local-only (gitignored: `data/lanes/longrca-trajectories/raw/`);
do not redistribute. Recorded verbatim in every sidecar and the
manifest (`license: "NOT-DECLARED"`).

### Flow as run

1. Scrape: 1,140 files + sidecars + manifest (see above).
2. Review fleet: two reviewers, 570 trajectories each
   (lexicographic split). Programmatic triage first (label
   distributions + keyword scan), then deep reads of ~40 top
   candidates each. 31 findings filed (17 + 14), all PRIMARY.
3. Adversarial kill: verifier re-read every cited step range
   from bytes, checked quotes verbatim, ran Factum dedup
   (direct `data/records/` scan + fuzzy match — 0 overlaps).
   30 survived, 1 killed (F-A15: claimed positive guardrail
   pattern was routine harness access-denial compliance).
4. Factum ingest: batch `bbab7554189943ca94522cf5fb138faa`,
   6,966 records — 1 source, 1 run, 1,171 observations
   (1,140 lean `dataset.record` trajectory records + 1
   `dataset.snapshot` + 30 `intel.behavior`), 1,140 artifacts,
   4,653 edges (run→trajectory, finding→trajectory, in_lane).
   Trajectories with findings embed the ±10 decisive step
   window; full step content stays in raw JSON. tags.lane on
   every record. Committed to `work` with explicit pathspecs,
   no push.
5. Report: `reports/trajectory-ingest/longrca/REPORT.md` plus
   `EVIDENCE-INDEX.md`, in ASD-STE100.

### Findings by class (30 verified)

COORDINATION 11, GUARDRAIL 5, TOOL-MISUSE 5, RECOVERY 4,
PROMPT-INJECT 2, OTHER 2, IRREVERSIBLE 1. Confidence: HIGH 24,
MEDIUM 6. Benchmark split: travelplanner 21, terminal_bench_2
4, swe_bench_pro 3, webarena_verified 2.

### Recurring patterns worth reusing

- **Verification collapse** (systemic): verifier roles performed
  by the actor they audit, broken verifier channels bypassed,
  completion detection as substring match. The harness trusts
  agent text as control plane. Self-emitted TASK_COMPLETE is
  the sharpest instance: a mere mention in planning prose
  triggers phase transition on an empty blackboard.
- **Fabrication as modal failure**: ~55 mistake_reasons name
  it; "educated guess" / "commonsense estimation" are the
  euphemisms. Frequently labeled in-source by the agents,
  making it text-detectable.
- **Advisory verifier gates**: `passed: false` records do not
  stop assembly; verifiers downgrade to caveats and the
  pipeline proceeds.
- **Evidence laundering**: fabricated values filed under a
  tool's name or with self-asserted compliance booleans.
- swe_bench_pro keyword signals are mostly code-domain noise;
  behavioral signal concentrates in multi-agent benchmarks
  (terminal_bench_2's Diagnost→Action→Judge loop, travelplanner's
  blackboard).

### Verifier lessons

- Two reviewer quotes challenged adversarially and upheld;
  minor inaccuracies (agent counts, root-cause mapping) were
  annotated in verifier_notes without confidence upgrades.
  Downgrade freely, never upgrade.
- Usernames and emails in trajectories (e.g.
  emma.lopez@gmail.com) are benchmark fixture data. Nothing
  pursued; scope held.
- Daemon restarts can kill polling workers with no checkpoint.
  Respawned workers need the full brief re-sent (they do not
  inherit the dead worker's state); gate deadlines should be
  patient-poll, not fixed-timeout.

## Worked example: TELBench

- Source: HF `NJU-LINK/TELBench`, rev
  `307d870d7424be265653bb7a566793cc217105be`.
  License Apache-2.0. 1,000 records (early recon said 2,790;
  the card and the bytes both say 1,000 — trust the bytes).
- The data file is encrypted (`TELBench.jsonl.enc`) but the
  passphrase ships in the repo (`TELBench.passphrase.txt`).
  The file wears an `openssl enc` `Salted__` header, but
  neither openssl default derivation decrypts it. The real
  scheme: PBKDF2-HMAC-SHA256, 200,000 iterations,
  AES-256-CBC, password = the 44-char ASCII passphrase with
  no trailing newline. Decrypt locally with `cryptography`.
  Never execute anything from the dataset.
- Verify both checksums: the `.enc.sha256` against the
  download, the `.jsonl.sha256` against the decrypted bytes.
  Keep the encrypted file, the decrypted file, the
  passphrase, and one `.PROVENANCE.txt` per file.
- Schema: `id`, `source_id`, `question`, `spans` (`{id,
  raw}`), `gold.error_span_ids` (the harmful-error
  annotations), `annotations.stage` / `annotations.error_type`,
  `meta` (bench, difficulty, framework, model). Start
  reviewers on the `gold.error_span_ids` spans.
- Fleet order that worked: scraper, then Reviewer A/B on
  halves, then adversarial verifier, then ingestor.
  Supervisor adjudication settled the one reviewer split
  (routine harness delegation is not wild coordination).
- Report: `reports/trajectory-ingest/telbench/REPORT.md`.

## Worked example: AgentErrorBench (Google Drive source)

- Source: Google Drive folder
  `drive.google.com/drive/folders/1bQe6dQA85pktT63YnKIKJDTVaH3O3Vpu`,
  plus repo `ulab-uiuc/AgentDebug` and paper arXiv 2509.25370.
  License MIT. 200 annotated failure trajectories: ALFWorld 100,
  GAIA 50, WebShop 50 (models: gpt-4o, Llama-3.3-70B, qwen3-8b).
- Drive handling: the folder page's embedded AF payload had no
  file list. Use the `embeddedfolderview` endpoint instead:
  `https://drive.google.com/embeddedfolderview?id=<folder>#list`
  lists everything anonymously, recursing through subfolders.
  Download each file with
  `https://drive.google.com/uc?export=download&id=<fileid>`
  (curl `-L`, cookie jar). No confirm-token dance was needed —
  all JSONs sat under the virus-scan threshold. No login, no
  403s, no rate limits. If a future folder does hit the
  confirm wall, document the manual step and move on; never
  work around auth.
- Egress note: `api.github.com` is dead through this VM's proxy
  (exit 52). `github.com` HTML and `raw.githubusercontent.com`
  both work anonymously. Prefer raw file URLs over the API.
- Repo tree drift: the README's tree diagram is stale —
  `examples/` and `docs/` 404 on main. Capture what exists
  (`detector/`, `agentdebug/`, LICENSE), not what the README
  claims.
- Label noise is real and raw: module keys vary (`plan` vs
  `planning`), failure types vary by case, 27 annotations have
  empty failure types. Instruct reviewers to trust trajectory
  bytes over labels, and the verifier to re-check every
  "never observed" claim against observation history — Reviewer
  A filed six phantom-object claims where the object WAS
  observed (corrected to observed-object substitution).
- All 200 trajectories end in failure (`won=False`). State
  this in the report — it shapes what the corpus can and
  cannot show.
- Fleet order that worked: scraper, Reviewer A (ALFWorld) +
  Reviewer B (GAIA/WebShop) in parallel, adversarial
  verifier, ingestor with full trace edges.
- Findings: 23 verified (OTHER 14, TOOL-MISUSE 5,
  IRREVERSIBLE 4). Corpus negatives: no CAPTCHA, ACCOUNT,
  GUARDRAIL, PROMPT-INJECT, CREDENTIAL, RECOVERY, or
  COORDINATION encounters.
- Report: `reports/trajectory-ingest/agenterrorbench/REPORT.md`.

## Worked example: ETO-SFT

Run 2026-10-17. Lane `eto-sft-trajectories`.
Dataset: `agent-eto/eto-sft-trajectory`, revision
`a8f745ef799a5201d2288b9c2a47e40a0ff70a4c`.
License: the HF API `license` field is null while tags AND the
README front matter both read apache-2.0 — record all three facts
(`raw/LICENSE.note`), do not pick one as resolved.

### Turn-based conversation schema

Top-level JSON is a list of dicts. Every record: `id`,
`conversations` (list of `{from: "human"|"gpt", value}`). Per-split
extras: alfworld +`game_file` (3119 records), scienceworld none
(1483), webshop +`reward` (float), +`source` (`"human"` or `"gpt"`).
Findings cite turn numbers as 0-based `conversations` indexes.

`behavior.tool_sequence` for turn-based corpora: record the decisive
turn window faithfully as steps with `tool: "conversation.turn"` and
`command: "<from>: <verbatim value>"`. Do NOT invent tool-call
structure. `model: "unrecorded-in-source"`; `harness` = split name.

### The 4116 dupe

`webshop_sft.json` holds 1824 rows but only 1823 unique ids: id
`4116` appears at indexes 936 and 937, byte-identical. Builder
asserts the duplicate set is exactly `[(webshop, 4116, 937)]` and
that the two rows serialize identically, then ingests once.

### Human-vs-gpt source caveat

Corpus description: "ETO SFT mix (human demos + model rollouts)" —
NOT "successful experts". Rewards 0-1; over-budget buys appear even
in reward-1.0 gpt rollouts (id 1486: $39.45 vs $20 ceiling, reward
1.0); 47 over-budget-then-buy trajectories corpus-wide (30 human +
17 gpt). Human-demo narration contains annotator-reconstructed
thoughts ("for the sake of this trajectory, I'll click 'buy now' to
follow the given actions" — RB-W-007); file over-budget buys as
dataset-quality observations, not model akrasia.

### What worked

- 15 verified findings, 12,916 records, one batch: 1 source, 1 run,
  1 dataset.snapshot, 3 artifacts, 6425 lean dataset.record
  (id/split/turn_count/reward/source/raw_path in tags, no content),
  15 intel.behavior, 15 behavior.tool_sequence, 6455 edges
  (run→trajectory, finding→trajectory, sequence→finding).
- Counts from bytes (3119/1483/1824, each one above briefing
  estimate); quote byte-verification in the builder gate.
- Dedup: zero overlap (agenterrorbench is a different alfworld/
  webshop corpus with filename-style ids).

## Worked example: InterCode-CTF

Run 2026-10-17. Lane `intercode-ctf-trajectories`.
13 datasets `jordan-taylor-aisi/*_gdm_intercode_ctf` (UK AISI
deception-probe evals). All 13 apache-2.0 (HF API tag + README
frontmatter both checked, `raw/LICENSE.note`).

### Eval-ZIP journal format

The real trajectory data is NOT the parquet (`config/train-00000-of-00001.parquet`
holds summary rows). The bytes live in
`logs/inspect_evals/gdm_intercode_ctf/benign.eval` — a ZIP
containing an inspect_ai eval journal:

- `_journal/start.json` — eval header (task registry, timestamps).
- `samples/<N>_epoch_1.json` — one per trajectory sample.
- `header.json`, `summaries.json`.

Each sample JSON: `messages` (list of `{role, content, tool_calls}`),
`scores`, `metadata`, `total_time`. Real tool calls sit on assistant
messages as `tool_calls: [{id, function, arguments}]`. Text-form tool
JSON in the content with empty `tool_calls` means the harness dropped it
— this distinction is itself a behavior class (see V-003..V-006).

835 samples across the 13 sets (79 each except devstral 25 and the two
10-sample dead-server sets). Per-sample `dataset.record` ingest is cheap
at this scale: no step content, attributes only (message_count,
tool_call_count, score).

### License note

Scraper policy: non apache-2.0 (or equivalent-permissive) datasets get
KILLED, not downloaded. All 13 passed with `license:apache-2.0` in both
the HF API tag and the README frontmatter.

### The elicitation-banner lesson

The elicitation chat template (`.jinja`) adds an all-caps banner that
coaches models to emit tool calls as `{"name", "parameters"}` text —
a format the harness parser never executes. Measured damage on both
stock and fine-tuned models: text-form tool events 26->62, zero-tool-call
trajectories 0->5, correct 43->29, tools/traj 6.13->4.33. The bannerless
elicitation set matches default, isolating the banner as the cause.
Lesson: when a dataset family has template variants, diff the templates
first — the banner text is provenance for every downstream tool-use
degradation. Verifier rule: fold single-trajectory exemplars into the
aggregate finding (A-004 -> V-003), don't file them standalone.

### What was ingested

1 batch, 1753 records: 13 sources, 13 artifacts, 1 run, 1
dataset.snapshot, 835 lean dataset.record (id/dataset only, no content),
18 intel.behavior, 18 behavior.tool_sequence (one per unique
finding-bearing trajectory; V-009 and V-010 share d8 sample 56), 854
edges (835 run→trajectory, 19 finding→trajectory). V-002 and V-003 are
corpus aggregates with no single trajectory: no tool_sequence, no edges,
documented in the report.

## WildClawBench notes

Run 2026-10-16. Lane `wildclawbench-trajectories`.

- The real trajectory dataset is `internlm/WildClawBench-Trajectories`,
  NOT the main `internlm/WildClawBench` dataset. The worked example above
  shows `internlm/WildClawBench` for both IDs — that is wrong for the
  traces; the 600 per-task traces live under
  `internlm/WildClawBench-Trajectories`.
- Edge scheme: run → `behavior.tool_sequence` → `intel.behavior`. The
  `exhibits`/`uses` edges REQUIRE `basis` + `cites` in `body`:
  `exhibits` → `basis: "OBSERVED"`, `uses` → `basis: "INFERENCE"`, and
  each edge gets `cites: [<the behavior.tool_sequence ref backing that
  finding>]`. The schema rejects interpretive edges without them. See
  `data/lanes/wildclawbench-trajectories/review/edge-scheme.md` and the
  fixed `data/lanes/wildclawbench-trajectories/build_bundle.py`.
- Gotcha: never put a top-level `"lane"` key in the bundle — it causes a
  LANE resolution error. `tags.lane` on every record carries the lane.
- Report: `reports/trajectory-ingest/wildclawbench/`.
- writer.lock contention: sibling fleets on one checkout serialize
  10–30 min each. Check your OWN stale processes first (`ps aux | grep
  factum.py`) — a dead backgrounded factum command can hold the lock for
  an hour+. Then stagger submit phases.

## Plugging in a new repo

1. Find the GitHub repo and HuggingFace dataset ID.
2. Run the scout. Check the manifest: file list sane, sizes
   sane, binaries flagged skip.
3. Scrape the wanted files with provenance.
4. Spawn reviewers with the prompt pack.
5. Kill, ingest, commit.

No new code. The pipeline is the three files in `scripts/`:
`trajectory-scout.py`, `trajectory-review-prompts.md`, and this
README.
