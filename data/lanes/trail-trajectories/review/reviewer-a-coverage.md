# Trail Reviewer A — Coverage (GAIA split)

Date: 2026-10-16. Reviewer: TRAIL-A (subagent, split reviewer A).

## What was read

- All 117 files in `data/lanes/trail-trajectories/raw/github-mirror/processed_annotations_gaia/*.json`. Each file is an expert annotation of one agent trace. Files were read with a script, not one by one.
- The 10-class taxonomy and grading rubric in `scripts/trajectory-review-prompts.md`.
- The head of `data/lanes/trail-trajectories/raw/trail-paper-2505.08638.txt` (TRAIL benchmark paper, Patronus AI) for corpus context.

Each file holds `errors` (category, location, evidence, description, impact) and `scores` (reliability, security, instruction adherence, plan optimality, overall).

## Counts

- Files read: 117 of 117. One file (`a96c6811716c0473b86a23321db79c34.json`) holds invalid JSON (a trailing comma after the last error object). It was still read after repair of that comma. This is a source-data defect, not a reviewer choice.
- Total error entries read: 585. Note: the task brief said 841 errors. 585 were found in the files. The difference is not explained by the files on disk.
- Every one of the 117 files' `security_score` entries is 5 (no security issue flagged by the annotators). This is a corpus property worth knowing.

## Category histogram (585 errors, 24 distinct labels)

Formatting Errors 124. Instruction Non-compliance 65. Goal Deviation 62. Tool-related 47. Tool Selection Errors 44. Task Orchestration 43. Language-only 41. Resource Abuse 39. Poor Information Retrieval 28. Context Handling Failures 19. Incorrect Problem Identification 18. Tool Output Misinterpretation 16. Environment Setup Errors 9. Resource Not Found 7. Context Handling Failure 5. Authentication Errors 5. Tool Definition Issues 3. Service Errors 2. Timeout Issues 2. Resource Exhaustion 2. Incorrect Problem Identification 1. Tool Selection 1. Goal deviation 1. Task Orchestration Errors 1. Several labels differ only by case or plural. This is annotation noise in the source.

## What was skipped and why

- CAPTCHA class: zero genuine CAPTCHA encounters exist in the corpus. One bot-check wall (403 "enable JS and disable any ad blocker") was kept as candidate TRAIL-A-21 with MEDIUM confidence. Nothing else qualified.
- ACCOUNT class: zero account-creation attempts in the corpus. Skipped entirely.
- CREDENTIAL class: zero genuine secret mishandlings. Keyword hits were false positives ("secretaries" matched "secret", "published" matched nothing, PDF filename matched "signin"). Skipped entirely.
- IRREVERSIBLE class: zero genuine destructive actions. Keyword hits were false positives ("published", "deleted" inside prose). Skipped entirely.
- PROMPT-INJECT from an attacker: zero. The one kept candidate (TRAIL-A-11) is scaffold-emitted retry guidance inside tool observations, not attacker content. It is filed honestly as harness instruction, not as an attack.
- GUARDRAIL bypasses: zero. The two kept candidates are a model self-refusal and an upstream provider block, not bypasses.
- Most Formatting Errors and Instruction Non-compliance entries (missing `<end_plan>` tags, plan-skip loops): skipped as routine benchmark friction. Only the most behavior-rich exemplars were kept.
- The fabrication/hallucination family is large (79+ entries). Nine exemplars were kept; the rest were skipped as duplicates of the same shapes.

## Grading note

All 30 candidates are graded UPSTREAM. The reviewer read the expert annotations, not the raw trajectories. The claims rest on the annotators' labels of observed traces. No candidate is PRIMARY. Confidence is set per candidate.

## Negative results worth keeping

- No credential, account, CAPTCHA, or irreversible-action behaviors in 585 errors. The GAIA TRAIL annotations, as provided, do not cover those classes.
- No security_score below 5 anywhere. The annotators found no security issues in these traces.
- The strongest signal in the corpus is COORDINATION: the traces show a manager/sub-agent (search_agent) architecture, and the most interesting behaviors cluster at the delegation boundary (false reports to the manager, blind trust, invented collaboration narratives).

## Outputs

- `reviewer-a-candidates.json`: 30 candidates. Classes: COORDINATION 8, OTHER 9, RECOVERY 5, TOOL-MISUSE 4, GUARDRAIL 2, PROMPT-INJECT 1, CAPTCHA 1. All quotes are verbatim from evidence/description fields, whitespace-normalized, capped at 200 chars, verified as substrings of the source.
- These candidates are for the verifier. They were not ingested to factum.
