# AgentErrorBench Trajectory Ingest — Report

Date: 2026-10-16. Lane: `agenterrorbench-trajectories`. Branch: `work`.

This document uses ASD-STE100 style. Short sentences. Simple words.
Terms are defined when first used.

## What AgentErrorBench is

**AgentErrorBench** is a benchmark dataset by U Lab at UIUC
(`ulab-uiuc/AgentDebug` on GitHub, paper arXiv 2509.25370, MIT
license). It holds 200 annotated AI agent failure trajectories with
step-level error labels under the authors' AgentErrorTaxonomy (17
error types across 5 modules: memory, reflection, planning, action,
system). Three task families are covered: embodied household tasks
(**ALFWorld**, 100 trajectories), general assistant tasks (**GAIA**,
50 trajectories), and shopping tasks (**WebShop**, 50 trajectories).
Models: gpt-4o, Llama-3.3-70B, qwen3-8b. Every trajectory in this
corpus slice ends in failure (`won=False`).

## The Google Drive source and access outcome

**Source:** the authors publish the dataset on Google Drive:
`drive.google.com/drive/folders/1bQe6dQA85pktT63YnKIKJDTVaH3O3Vpu`.
**Access:** fully anonymous, no blocks. The Drive UI page's embedded
payload had no file list, but the `embeddedfolderview` endpoint
listed every file. Downloads used `uc?export=download&id=<fileid>`
with no confirm-token dance (all files under the virus-scan
threshold). No login. No rate limits. No 403s.

**Repo note:** the repo README's tree diagram is stale. `examples/`
and `docs/` return 404 on main. Current main holds `detector/`
(taxonomy + detection framework), `agentdebug/{data,rollout,...}`,
`assets/`. All taxonomy-relevant code was captured.

**Label noise (raw, uncleaned):** module keys vary (`plan` vs
`planning`); failure types vary by case (`Parameter_error` vs
`parameter_error`); one type has a trailing space
(`tool_execution_error `); 27 annotations have an empty
failure_type; GAIA filenames say `Llama3.3-70B-Turbo` while metadata
says `meta-llama/Llama-3.3-70B-Instruct-Turbo`. Findings use the
metadata value. Trajectory bytes were trusted over labels wherever
they disagreed.

## Corpus ingested

- 200 trajectory JSON files: ALFWorld 100, GAIA 50, WebShop 50.
- 200 label files (join coverage 200/200 by trajectory_id).
- 3 label-set files, 1 Drive README, paper PDF (8 pp.), repo mirror
  (README, LICENSE, `detector/`, `agentdebug/data/episode.py`,
  `agentdebug/rollout/`).
- Total: 215 files, 81.8 MB, all with 5-line `.PROVENANCE.txt`.

## Pipeline summary

1. **Scraper.** Downloaded the Drive folder and secondary sources
   with per-file provenance. Manifest:
   `data/lanes/agenterrorbench-trajectories/raw/MANIFEST.json`.
2. **Reviewers.** Reviewer A read all 100 ALFWorld trajectories (17
   candidates). Reviewer B read all 100 GAIA + WebShop trajectories
   (8 candidates). Taxonomy: the 10-class behavior taxonomy from
   `scripts/trajectory-review-prompts.md`.
3. **Adversarial verifier.** Re-fetched every cited file. Recomputed
   sha256 (24/25 match; the one mismatch was a transcription error in
   a killed finding). Checked quotes against bytes. Ran factum fuzzy
   match on 11 key terms plus direct `data/records/` scans: zero
   overlap. Result: **23 survive, 2 killed** (see below).
4. **Factum ingest.** 23 survivors entered factum with full trace
   edges. See "Ingest record".

## Findings summary by taxonomy class

23 verified behavior candidates (survivors), by class:

- OTHER (14): false-completion clusters (agent declares the task
  done while `won=False`: A-004, A-005, A-006). Observed-object
  substitution — the agent acts on a seen but wrong-class object
  (A-003, A-009, A-010, A-011, A-014, A-017). Invented target URL:
  Llama re-extracts a Rick Astley video URL 9 times across 23 steps,
  never questioning it (B-001). Minted fake 9-digit Tropicos ID
  piped through 17 tool calls as genuine (B-003). Third-person
  "simulate what the assistant would do" framing while emitting
  real tool calls (B-002). Chinese token bleed in English reasoning
  at a purchase commit point (B-008).
- TOOL-MISUSE (5): Llama-wide unclosed `</action>` tag defect — 193
  net unclosed opens across all 23 Llama trajectories, 0 in 50
  GPT-4o + 27 Qwen (A-001, A-002). Literal `None` emitted as action
  content (A-007). Cleaning a dishsponge instead of the plate, then
  planning around it (A-013). Wrong-sequence cleaning action (A-008).
- IRREVERSIBLE (4): all qwen3-8b WebShop. Self-written escape clause
  in the plan ("proceed to buy now as the closest match") then
  executing the terminal purchase (B-004). Buying after spotting an
  open-front vs button-closure mismatch, hand-waving the wash
  attribute (B-005). Buying "without further verification steps"
  after writing the product "doesn't meet the criteria" (B-006).
  Rubber outsole "verified" only from a search-snippet memory
  (B-007). Note: terminal buys have no post-buy observation, so
  actual purchase completion is unverified. All 4 are qwen3-8b; a
  possible model effect needs a cross-model check on the same tasks.
- CAPTCHA (0), ACCOUNT (0), GUARDRAIL (0), PROMPT-INJECT (0),
  CREDENTIAL (0), RECOVERY (0), COORDINATION (0): no encounters in
  this corpus. These are corpus negatives, recorded as such.

## The 2 kills (not ingested)

- **A-012:** claimed a phantom "stoveburner 3". The object is in the
  file's initial room observation. Every element of the claim was
  contradicted by bytes. Killed.
- **A-016:** double break. The finding's sha256 did not match the
  recomputed bytes or the sibling `.PROVENANCE.txt` (transcription
  error). Substance: drawer 5 was opened at step 20 and creditcard 1
  observed in this trajectory — the action is grounded, not
  cross-task bleed. The novelty note's "verbatim in 4 GPT files" was
  false (0 occurrences). Killed.

## Verifier corrections (kept, not killed)

Reviewer A repeatedly filed "never observed" claims without reading
observation history. In A-003, A-009, A-010, A-011, A-014, A-017 the
"phantom" object WAS observed (often opened and handled). The
surviving behavior is observed-object substitution (wrong class for
the task), not phantom confabulation. All kept with corrected
quotes. Five were downgraded to MEDIUM confidence. A-001's novelty
note wrongly called "go to dresser 2" hallucinated — dresser 2 is in
that file's initial observation.

## Ingest record

- Batch ID: `a503b4b9347e4b9c85abce911121c242`.
- Submitted: 162 records — 3 source, 69 observation (23
  `intel.behavior` + 23 `behavior.tool_sequence` + 22 trajectory +
  1 dataset snapshot), 68 edge, 22 artifact.
- Edges: run → steps → tool calls → findings via refs, traversable.
  22 trajectory edges + 23 behavior edges + 23 tool-sequence edges.
- Dedup: zero overlaps. Factum fuzzy match on 11 key terms plus
  direct `data/records/` scans found no existing agenterrorbench
  records or matching behavior text.
- Grade: PRIMARY on all 23 (reviewers read the trajectory bytes).
  Confidence: 18 HIGH, 5 MEDIUM (in tags).
- `tags.lane: "agenterrorbench-trajectories"` on all 162 records,
  including sources.
- Corpus: 123,904 records after ingest. Verify passed.

## Coverage

- 23 behaviors cover 22 of the 200 trajectory files (A-001 and A-002
  share one file). The rest were routine benchmark friction: plan
  loops, truncated outputs, environment errors.
- Corpus negatives recorded: no CAPTCHAs, no account creation, no
  guardrail bypasses, no prompt injections, no credential
  mishandling, no recovery behaviors, no coordination.

## Open gaps

- Llama's aggregate failure rate in this corpus is confounded by the
  unclosed-tag defect (A-002). Do not cite it as a reasoning-quality
  gap without discounting the format bug.
- All 4 IRREVERSIBLE findings are qwen3-8b. A cross-model check on
  the same WebShop tasks would test for a model effect.
- Terminal `click[buy now]` has no post-buy observation. Purchase
  completion is unverified.
- Dataset revision is "unknown" (Drive folder last modified
  9/30/25, snapshot 2026-10-16). Recorded verbatim in provenance.
- The authors' label noise (case variants, empty types) was not
  cleaned. A normalization pass would help future analysis.

## Evidence index

All trajectory files that carry ingested evidence, plus the
supporting captures. sha256 of the file bytes as ingested.

- See `EVIDENCE-INDEX.md` in this directory (file, size, sha256).
