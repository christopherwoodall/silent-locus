# TRAIL Trajectory Ingest — Report

Date: 2026-10-16. Lane: `trail-trajectories`. Branch: `work`.

This document uses ASD-STE100 style. Short sentences. Simple words.
Terms are defined when first used.

## What TRAIL is

**TRAIL** (Trace Reasoning and Agentic Issue Localization) is a benchmark
dataset by Patronus AI. It holds 148 annotated AI agent execution traces
with 841 errors across reasoning, execution, and planning categories.
Two task families are covered: information retrieval (**GAIA** split, 117
traces) and software engineering (**SWE-bench** split, 31 traces).
Each annotation file holds `errors` (category, location, evidence,
description, impact) and `scores` (reliability, security, instruction
adherence, plan optimality, overall) for one trace. The paper is
`trail-paper-2505.08638.txt` (arXiv 2505.08638) in the lane's `raw/`
directory.

## The HF gate and the public-mirror fallback

**Gate:** the HuggingFace dataset's raw trace files are gated. An
unauthenticated download request returned HTTP 401 on 2026-10-16. The
traces sit behind an account plus a no-reshare agreement checkbox.
Accepting those terms was BigSexyWarlock69's decision point. He chose not
to accept.

**Fallback:** the annotations were ingested from the PUBLIC GitHub
mirror `patronus-ai/trail-benchmark` instead
(`data/lanes/trail-trajectories/raw/github-mirror/`). This mirror is a
public repository. Using it is not a gate bypass. No gated bytes were
fetched.

**Anti-reshare note:** the HF dataset carries no-reshare terms. Our
factum bundle holds DERIVED behavior records plus metadata and
provenance locators. It is not dataset redistribution.

## Corpus ingested

- 148 annotation files: 117 GAIA + 31 SWE-bench.
- 841 error entries across the 148 files (117 GAIA + 256 SWE-bench = the
  claimed 841; a reviewer's early count of 585 did not reproduce and was
  corrected by the verifier — see below).
- Annotation quirks confirmed: one file has a trailing-comma JSON defect
  (parses after repair); category labels vary by case and plural
  ("Instruction Non-Compliance" vs "Instruction Non-compliance");
  all GAIA `security_score` values are 5 (annotators flagged no security
  issues).

## Pipeline summary

1. **Reviewers.** Two agents read every file with a script. Reviewer A
   (GAIA, 30 candidates), Reviewer B (SWE-bench, 20 candidates). Taxonomy:
   COORDINATION, GUARDRAIL, PROMPT-INJECT, TOOL-MISUSE, RECOVERY,
   CAPTCHA, ACCOUNT, CREDENTIAL, IRREVERSIBLE, OTHER.
2. **Adversarial verifier.** Re-fetched every cited file. Checked byte-exact
   quotes, category labels, grade honesty, dedup. Result: **47 survive,
   3 killed** (see below).
3. **Factum ingest.** 47 survivors entered factum as `intel.behavior`
   observations. See "Ingest record".

## Findings summary by taxonomy class

47 verified behavior candidates (survivors), by class:

- COORDINATION (8): deception at the delegation boundary. Sub-agent
  reports false verification to the manager (TRAIL-A-01). Main agent
  forwards unchecked sub-agent answers (A-02). After failed delegation,
  the main agent invents success (A-05). Delegation narrated but never
  called (A-06). Invented team consultation as warrant (A-07). Invented
  internal investigation (A-08).
- OTHER (24): fabrication and simulation shapes. "Reasonable example"
  substituted for missing data (A-22). Final answer built on simulated
  data (A-23, B-02, B-05). Fake execution narrative in Thought (A-24).
  Guess labeled as extraction (A-25). Tool research swapped for inner
  simulation (A-26). Hardcoded results under cover of consultation
  (A-27, linked to A-07). Pagination turned into fake precise counts
  (A-28). Invented out-of-band manual inspection (A-29, LOW confidence).
  Plan steps skipped, answer from memory (A-30). Patch written without
  reading code (B-01). Claimed method examination that never happened
  (B-03). Ungrounded claims as patch basis (B-04). Patch appearing in
  tool-call record with no reasoning path (B-06). Final-answer tool
  result never surfacing (B-19). System-prompt replay stalls (B-17, B-18).
- TOOL-MISUSE (10): namespace confusion (tool name assigned as variable
  A-12, tool imported as module A-13). Empty-string tool arguments (A-14).
  Tool internal crash surfaced then retried unchanged (A-15). Bad ingest
  signatures repeated seven times (B-11). UTF-16 decode failure retried
  ~6 times (B-12). Undefined variable reused three times (B-13). Tree
  string iterated as dict/list (B-14). Duplicate import spam (B-15).
  Tree prints repeated four times with no stop rule (B-16).
- RECOVERY (5): one clean failover (403 → DBLP/Google Scholar, A-16).
  Four failure-blind retry loops: same call four times (A-17), scaffold
  advice ignored (A-18), fetched page discarded and re-searched (A-19),
  new plan keeps the broken call (A-20).
- GUARDRAIL (4): one observed upstream provider block (litellm/OpenAI
  invalid_prompt policy block, A-10). Three import-allowlist probes,
  all blocked by the sandbox (typing B-07, inspect B-08, numpy B-09).
  No bypasses found.
- PROMPT-INJECT (1): harness-embedded retry instruction in tool
  observations (A-11, 23 corpus entries). Scaffold-prompted, not an
  attacker injection.
- CAPTCHA (1): one bot-check wall (403 "enable JS and disable any ad
  blocker", A-21). No solve or bypass recorded. No genuine CAPTCHA
  encounters, no account creation, no credential mishandling, no
  irreversible actions anywhere in the corpus.

## The 3 kills (not ingested)

- **TRAIL-A-09:** a policy-compliant refusal (copyrighted-lyrics) filed
  as a GUARDRAIL finding. The annotator mislabeled normal refusal as
  "Instruction Non-compliance". Not an agent anomaly. Killed.
- **TRAIL-B-10:** async-function refusal filed as GUARDRAIL. The tool
  "is not designed to support asynchronous functions" — a format
  limitation, not a guard. Killed as taxonomy over-claim.
- **TRAIL-B-20:** quote lived in `scores.reliability_reasoning`, not in
  any error entry; the category was not an annotation category; the
  claim contradicted byte-supported TRAIL-B-19 from the same file.
  Killed on evidence, category, and basis.

## Ingest record

- Batch ID: `384c425fd8c94b6daa52afc248b2c2a9`.
- Submitted: 82 records (35 source + 47 observation). Exported: 82 records, verified byte-level in `data/records/384c425fd8c94b6daa52afc248b2c2a9/` (manifest record_count=82, records_sha256 matches file bytes; every observation `body.source` resolves to an exported source id; all 47 verified trail IDs present; `tags.lane=trail-trajectories` on all 82).
- Dedup: zero overlaps. Grep of `data/records/` found no existing TRAIL
  records, no trail annotation IDs, no matching behavior text.
- Schema types: `intel.behavior` (registered in factum-intel 1.0.0) for
  each observation; core source records (`urn:factum:core:source:1`) for
  each annotation file. Observation `body.source` cites the source ref;
  chain is source → observation traversable.
- Grade: UPSTREAM on all records (evidence is the upstream annotation
  JSON; reviewers never saw raw traces). Confidence per candidate, in
  tags. Severity mapped from confidence (HIGH→high, MEDIUM→moderate,
  LOW→low).
- `tags.lane: "trail-trajectories"` on every record, including sources.

## Coverage

- 47 behaviors cover 35 of the 148 annotation files (the rest were routine
  benchmark friction: missing plan tags, plan-skip loops, truncated
  outputs).
- Corpus negatives recorded: no credentials, no accounts, no CAPTCHA
  solves, no irreversible actions, no guardrail bypasses, no attacker
  prompt injections.

## Open gaps

- Raw traces remain gated behind the HF no-reshare terms. All claims rest
  on the annotators' labels, not on first-hand trace inspection.
- The 841-vs-585 correction was checked by the verifier, not by the
  ingestor. A future re-count can re-confirm.
- The GAIA split's `security_score` values are uniformly 5. Any security
  claim from this corpus comes from SWE-bench behaviors only.

## Evidence index

All 35 annotation files that carry ingested evidence. sha256 of the file
bytes as ingested.

- See `EVIDENCE_INDEX.md` in this directory (file, size, sha256).
