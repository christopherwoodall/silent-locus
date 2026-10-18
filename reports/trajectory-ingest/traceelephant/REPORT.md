# TraceElephant Trajectory Ingest — Lane Report

Run 2026-10-16/17. Lane tag: `traceelephant-trajectories`.

Terms used in this report:

- **Trajectory** — the ordered record of one multi-agent run: steps, agent
  names, tool calls, and tool results.
- **Finding** — one verified claim about agent behavior, with cited steps.
- **PRIMARY** — a direct observation from raw trajectory bytes. Not a
  second-hand summary.
- **Verifier** — the adversarial reviewer who re-checks every filed claim
  against the raw bytes.
- **Factum** — the structured evidence store used by this repo. Records live
  there, not only in this report.
- **Run** — one task directory: `trace_metadata.json` plus
  `step_records.json`.
- **Tool sequence** — the cited steps that back one finding, with the agent
  named per step.
- **`exhibits`** — an edge that says a harness showed a behavior.
- **`uses`** — an edge that says a finding rests on a tool sequence.
- **Basis** — why an edge is claimed: `OBSERVED` (seen in bytes) or
  `INFERENCE` (reasoned from the bytes).

## What was scraped

The dataset is `TraceElephant/TraceElephant` on HuggingFace (public,
ungated, revision `a78a57cdcdf74a080b1bec0f56f85228d86acbac`), from the paper
"Seeing the Whole Elephant: A Benchmark for Failure Attribution in
LLM-based Multi-Agent Systems" (ACL 2026). License: CC-BY-4.0. The license
was verified on the GitHub repo and the HuggingFace dataset before any
download. The corpus is `data.zip` (596,610,649 bytes, SHA-256 recorded in
`data.zip.sha256`).

Download: `curl -L` on the HF resolve URL. The transfer dropped twice and
was resumed with `curl -C -`; the tail was fetched with a ranged request
against a fresh signed URL. Full provenance in
`data/lanes/traceelephant-trajectories/raw/.PROVENANCE.txt`.

Totals: 220 tasks, 5,960 steps, about 831 MB uncompressed. Manifest:
`data/lanes/traceelephant-trajectories/raw/MANIFEST.json`.

By system directory:

- `captain-runs-gaia`: 73 tasks, 1,559 steps. Captain-Agent: Orchestrator
  plus expert agents (InformationExtraction, DataVerification, Python
  Programming, Verification, WebServing, CSVHandling).
- `captain-runs-assistantbench`: 12 tasks, 187 steps. Same Captain-Agent
  shape.
- `magentic-runs-gaia`: 74 tasks, 2,060 steps. Magentic-One: Orchestrator,
  WebSurfer, FileSurfer, Coder, ComputerTerminal. Has screenshots.
- `magentic-runs-assistant-bench`: 17 tasks, 603 steps. Same Magentic-One
  shape. Has screenshots.
- `swe-agent-runs-swe-bench`: 44 tasks, 1,551 steps. SWE-agent tool calls
  (str_replace_editor, bash, submit).

All runs use model gpt-4o. Every task carries failure-attribution labels
(`mistake_agent`, `mistake_step`). The labels are leads only. The reviewers
checked them against the bytes. Some labels were wrong.

## Review pipeline

Two reviewers split the corpus (111 and 109 tasks, deterministic split in
`raw/SPLIT_PLAN.json`). They filed 44 candidates. The verifier re-fetched
every citation against the raw bytes.

- Reviewed: 44. Survived: 43. Killed: 1 (TE-A-16).
- Confidence: 30 HIGH, 13 MEDIUM.
- All survivors are PRIMARY-by-observation. The source is SECONDARY
  (a published benchmark), noted per finding.

The verifier's version in
`data/lanes/traceelephant-trajectories/review/verified-findings.json` is
the canonical list. Kills are in `review/kill-log.json`.

The kill: TE-A-16 ("FileSurfer absorbs the Coder role", gaia_task_143).
The bytes show FileSurfer nominating ComputerTerminal via
`next_speaker=ComputerTerminal` at steps 7/10/20. That is normal
delegation, not role absorption. The real anomaly in that run
(MagenticOneOrchestrator writing code at steps 9/19 with no Coder agent
present) is noted in the kill log for correct re-filing.

Verifier corrections on survivors: TE-A-03 and TE-A-26 had wrong run-id
suffixes in the reviewer evidence; both were re-verified against the real
corpus runs. TE-A-29 was stronger than filed (26 of 44 SWE runs show
submit-then-continue, not 12). B-004 was corrected (the orchestrator did
not finalize the wrong page; it escalated). B-011's "1,527 revisions"
figure has no provenance in the trace bytes; the recovery loop itself is
real, the number is not.

## Findings by behavior class

### COORDINATION (28)

Degenerate loops: TE-A-01 (InformationExtraction_Expert repeats one fixed
completion verbatim, steps 9-56, with a fabricated placeholder);
TE-A-02 (Verification_Expert repeats one sentence, steps 13-54);
TE-A-03 (WebServing_Expert verbatim loop, steps 9-31).

Role inversion and upward delegation: TE-A-04 (expert delegates its own
job upward for ~47 steps); TE-A-05 (expert refuses its role at step 11);
TE-A-20 (WebSurfer asks the orchestrator to watch a video);
B-006 (59-step delegation thrash ending with no answer).

Self-aware loop continuation: TE-A-07 (apologizes for the loop five times
while continuing); TE-A-08 (two agents emit identical apology text);
TE-A-09 and TE-A-10 (Verification_Expert parrots another expert's text
as its own verification).

Orchestrator role collapse (Magentic): TE-A-12, TE-A-18, B-009
(orchestrator does the browsing itself); TE-A-17 (WebSurfer uses
FileSurfer's tool); TE-A-19 (WebSurfer unilaterally reassigns to Coder
and orders `pip install pytube`); B-010 (every handoff in the
plan collapses).

Misattribution and rubber-stamping: B-001 (the failure label blames the
wrong agent; the bytes show the expert at fault); B-002 (wrong-expert
delegation, fabricated data certified "no contradictions");
B-003, B-004, B-005 (verifier-acceptance cascades); B-007 (invented
"1500 articles" estimate rubber-stamped as the final answer).

Phantom execution: B-008 (ComputerTerminal nominated three times, never
appears; the orchestrator computes from unexecuted code).

Identity contamination: TE-A-30 (`agent_name='Orchestrator'` inside
SWE-agent runs; `MagenticOneOrchestrator` beside `Orchestrator` in
magentic runs).

Positive cases: TE-A-21 (orchestrator rejects a premature conclusion);
TE-A-22 (honest source pivot with limitation admitted); B-011 (genuine
14-step cooperative debug loop, though the final number is ungrounded).

### CAPTCHA (5)

TE-A-13 (WebSurfer: "Try to solve the CAPTCHA verification", then clicks
the checkbox). TE-A-14 (explicit defeat framing: "needs to be bypassed").
TE-A-15 (solve attempts, then evasion to other search engines).
B-012 and B-013 (bot-checks met with rerouting, never solving; kept as
CAPTCHA but distinct from explicit bypass language).

### OTHER (5)

Fabrication: TE-A-24 (self-disclosed simulation presented as evidence);
TE-A-25 (fabricated video verification); TE-A-27 (invented "43%" with a
source name-drop); TE-A-28 ("Penguins" by plausibility).
TE-A-29 (harness-level: `submit()` does not end SWE-agent runs; agents
keep acting after submitting, in 26 of 44 runs).

### RECOVERY (2)

Covered above: TE-A-21, TE-A-22. Positive behavior, kept as pattern
intel.

### ACCOUNT (1), PROMPT-INJECT (1), TOOL-MISUSE (1)

TE-A-23 (Spotify sign-in barrier met honestly, then a fabricated
workaround). TE-A-26 (WebSurfer writes its own instruction authorizing
fabrication when data is missing). B-014 (SWE agent calls str_replace on
a directory path; the tool errors; the agent recovers with `rm`).

No GUARDRAIL or CREDENTIAL findings survived review. The reviewers'
candidates in those classes were harness boilerplate or token counts,
killed before filing.

## Factum ingest

Bundle: `data/lanes/traceelephant-trajectories/working/bundle-traceelephant.json`.
Builder: `working/build_bundle.py`.

Structure per finding (full trace edges, traversable by ref):

- `source` (run): one per task. Locator, task id, system, benchmark,
  step file SHA-256, retrieval provenance. 43 records.
- `observable` (harness): `captain-agent`, `magentic-one`, `swe-agent`;
  plus `model` = `gpt-4o`. 4 records.
- `observation` `behavior.tool_sequence`: cited steps with the agent
  named per step. 43 records.
- `observation` `intel.behavior`: category, description, provenance,
  severity. 43 records.
- `edge` `exhibits` (harness -> behavior, OBSERVED, cites the tool
  sequence) and `edge` `uses` (behavior -> tool sequence, INFERENCE).
  86 records.

Total: 219 records. Every record carries `tags.lane =
"traceelephant-trajectories"`.

Dedup: no existing TraceElephant records in the corpus (direct
`data/records/` scan). Batch-internal dedup by task and finding id.

## Open gaps

- Screenshots (2,070 PNGs, magentic runs only) were not reviewed. Visual
  behaviors are uncovered.
- `MagenticOneOrchestrator` identity contamination is undetermined
  (second harness identity vs finalizer artifact).
- TE-A-16's real anomaly (code written with no Coder present) needs
  correct re-filing.
- The kill log notes one more candidate class the reviewers did not
  pursue: `seek_experts_help` escalation patterns in captain runs.
