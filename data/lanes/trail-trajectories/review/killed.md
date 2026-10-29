# TRAIL Adversarial Verifier — Kill List

Date: 2026-10-16. Scope: 50 reviewer candidates (TRAIL-A-01..30, TRAIL-B-01..20).
Method: scripted re-fetch of every cited annotation file; byte-exact substring check of
`evidence_quote` against `errors[].evidence`/`errors[].description`; category check against
the file's actual `category` values; grade honesty; cross-set dedup screen; sanity/over-claim review.

Result: **47 survive, 3 killed.** All 50 evidence files exist under
`data/lanes/trail-trajectories/raw/github-mirror/`; all 50 candidates were graded UPSTREAM
(correct — the evidence is the upstream annotation JSON itself, reviewers never saw raw traces,
so no OBSERVED demotions were needed).

## Kills

### TRAIL-A-09 — Agent refuses copyrighted-lyrics excerpt on policy grounds (GUARDRAIL / Instruction Non-compliance)
**What failed:** sanity — "normal benchmark task execution with no surprising element."
**Exact reason:** The bytes support the literal claim (the model did refuse on policy grounds;
quote verified verbatim, category matches the annotator's label). But the behavior is a
policy-compliant refusal — normal, expected execution, not an agent anomaly. The only
surprising element is the *annotator's* mislabeling of a compliant refusal as an
"Instruction Non-compliance" error, which is a dataset/annotation-pipeline artifact, not
the agent behavior the finding files. The reviewer's own notes flagged this ("flag for the
verifier"). A guardrail doing its job is not a guardrail finding. Killed.

### TRAIL-B-10 — Agent wraps search in async def; tool refuses async definitions (GUARDRAIL / Tool-related)
**What failed:** over-claim — harness-format friction filed as a guardrail event.
**Exact reason:** The annotation's own description says the code tool "is not designed to
support asynchronous functions" — a tool capability/format limitation, not a permission
guard, policy check, or safety control. The agent was not bypassing, evading, or probing a
guard; it hit a parser-level limitation. The filed quote also collapsed a newline
(`async def search_files():\nsummary...` quoted as one line), but the kill is on the
taxonomy over-claim, exactly the "calling harness-format friction a guardrail bypass"
shape the brief names. (Contrast TRAIL-B-07/08/09, which survive: the import allowlist is
an explicit permission control — "not among the authorized imports" — so probing it is a
genuine guardrail-adjacent event.)

### TRAIL-B-20 — "The agent makes mistakes, corrects each one, and reaches a working patch" (RECOVERY / scores.reliability_reasoning)
**What failed:** evidence, category, and basis — four independent defects.
**Exact reason:**
1. The evidence_quote ("The model did make mistakes, but recovered correctly from each one
   until it solved the issue.") is NOT a substring of any `errors[].evidence` or
   `errors[].description` in `0e6f7928953ab5a568bae640ce915cc3.json`. It lives in
   `scores[0].reliability_reasoning` — the annotator's summary judgment, a different
   record section than the verification contract allows.
2. `trail_category` "scores.reliability_reasoning" is not an annotation `category` value;
   the file's categories are Context Handling Failures, Formatting Errors, Incorrect
   Memory Usage, Incorrect Problem Identification, Language-only, Poor Information
   Retrieval.
3. The "behavior" is the annotator's summary judgment restated — no behavior-level bytes
   in the file demonstrate a recovery sequence. This is the "annotation restated with no
   hunt-relevant content" shape.
4. It contradicts the byte-supported TRAIL-B-19 from the same file: the trace ends with
   the final-answer patch dying at the tool boundary ("The model reached the final answer
   but didn't print it because of incorrect context management" — the annotator's own
   reliability_reasoning). "Recovered correctly ... until it solved the issue" is not
   established by the trace the candidate cites. Killed.

## Near-kills that survived (with corrections)

- **TRAIL-A-10** (policy block): the filed quote was the page_down TypeError from a
  *different* error entry — verbatim in the file but citing the wrong span for the claim.
  Quote replaced with the byte-exact evidence of the file's error 10
  (`litellm.BadRequestError ... 'Invalid prompt: your prompt was flagged as potentially
  violating our usage policy...'`), which is what the behavior describes. Kept as the
  corpus's rare observed upstream provider block.
- **TRAIL-A-21, TRAIL-B-14, TRAIL-B-15**: quotes collapsed newlines to spaces; replaced
  with byte-exact strings (`Error 403\n\n\n\nPlease enable JS and disable any ad blocker`;
  `Tree structure (top level):\n[...`; `Imports in node_classes.py:\nimport annotations\n...`).
  Behaviors fully supported. Kept.
- **TRAIL-B-14**: the notes' "~20 of 31 traces" recurrence claim is false — char-listed
  tree output appears in 3 of 31 swe_bench files (567b83e6, 8fa1892f, fdaf88f3). Corrected
  in verifier_notes. Kept.
- **TRAIL-B-08**: "introspection-escape module" is reviewer attribution, not in the bytes;
  flagged as speculation in verifier_notes. Kept as one of three import-allowlist probes
  (B-07/B-08/B-09), distinct traces — a probe family, not a duplicate filing.

## Corpus-level quirk verification (reviewers' claims checked, not trusted)

- **"Only 585 error entries on disk vs 841 claimed": FALSE.** Counted 841 error entries
  across 148 files (117 gaia + 31 swe_bench) — exactly the claimed 841. The 585 figure
  does not reproduce.
- **Trailing-comma JSON defect: CONFIRMED.** `processed_annotations_gaia/a96c6811716c0473b86a23321db79c34.json`
  (TRAIL-A-23's source) fails strict parse at line 39 col 5; parses after `,(\s*[}\]])` →
  `\1` repair. It is the only unparseable file of the 148.
- **Category labels vary by case/plural: CONFIRMED.** E.g. one swe_bench file contains both
  'Instruction Non-Compliance' and 'Instruction Non-compliance'; 'Formatting Error' vs
  'Formatting Errors' across files. Category matching was done case-insensitively; the
  actual file label is recorded in each survivor's verifier_notes.
- **A-29's source contradicts itself on numbers: CONFIRMED (with nuance).** In
  `eb42da715add1437eced9e494b0f62f7.json` error 5, the description juxtaposes the
  system's unverified "8 pages mentioning 'nuclear energy'" claim with the annotator's
  own "2 slides / 'crustaceans'" determination — plus a topic shift (nuclear energy vs
  crustaceans). The behavior claim (agent invents out-of-band manual inspection) is
  byte-supported; kept at LOW confidence with the tension documented.
- **A-11's "17 error entries corpus-wide" with the retry instruction: off — actually 23.**
  Corrected in verifier_notes; the scaffold-prompting substance holds.

## Dedup screen result

No exact duplicates. All same-file co-filings (e.g. A-10/A-14, B-01/B-08/B-11,
B-04/B-09/B-12, A-07/A-27, B-02/B-16) cite *different* error entries with distinct
behaviors — kept as separate instances, with family linkages noted in verifier_notes.
Cross-set behavior-similarity screen (A vs B) found no near-duplicate pair above
threshold that shared a file; recurring patterns across distinct traces (final-answer
without verification in B-02/B-05; fabricated out-of-band work in A-08/A-29; tool-name
namespace confusion in A-12/A-13) were kept as separate instances — recurrence of a
shape across traces is signal, not duplication.
