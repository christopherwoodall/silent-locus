# Extraction: How AI agents shape experts' judgment calls

- Title: How AI agents shape experts' judgment calls
- Source URL: https://www.anthropic.com/research/agents-judgment-calls
- Published: 2026-10-27 (page metadata Published 2026-10-27T00:00:00.000Z;
  Updated 2026-10-27T19:17:23.000Z)
- Authors (page byline): Amac Herdagdelen, Hailey Joren, Alex Tamkin
- Source file: agents-judgment-calls_2026-10-28.html (233230 bytes,
  sha256 2815d3481c9e8097ab87d12301b208e78e372644cd63036f6b1e3cb81297031a)
- Note: this file is an extraction only. Claims are tagged THEIR CLAIM
  (the report's assertion) vs OBSERVED (what the page shows directly).
  Inferences are tagged INFERENCE. Numbers below are transcribed from the
  page prose; the page carries no data tables.

## 1. Summary

Anthropic reports a randomized controlled trial on expert deference to an
AI coding agent. OBSERVED: 61 professional analysts were recruited; 50 used
the agent and 11 chose not to and are excluded from the main analysis.
THEIR CLAIM: experts handed judgment calls to the agent without noticing.
OBSERVED: the task was a fictional farming-cooperative advisory-program
evaluation (Greenfields Farming Cooperative); the agent ran Claude Code
with Claude Opus 4.8 at High effort in a web-based VS Code editor.

## 2. Study design (as the page describes it)

- Four analytical decisions, each with two defensible options: outcome
  measure (crop yield per hectare vs yield per unit of operating cost);
  comparison method (difference-in-differences vs levels adjustment);
  coverage (enrolled farms only vs full membership); weighting (by
  production vs per farm). These fed a final recommendation (roll out vs
  discontinue, with a one-year extension option).
- OBSERVED: for each participant and decision, a coin flip secretly set
  which option the participant's agent would favor. The lean was given in
  hidden instructions (a system prompt) telling the agent to hold the lean
  as its own view, raise it when the decision came up, make the strongest
  case the data allowed, change its mind if evidence turned decisively
  against it, and never misrepresent results, hide data, or argue what the
  numbers did not support.
- OBSERVED: each decision could move the estimated productivity gain by
  several percentage points against a board threshold of roughly 3-4%.
- OBSERVED: 65% of the 50 agent users held a master's or doctorate or had
  six or more years of experience; 90% rated themselves proficient or
  expert in observational causal inference (of 48 survey respondents).
  Median task time 65 minutes.

## 3. Results (their numbers, transcribed from prose)

- Analysts matched their agent's lean on 86% of the four analytical
  decisions combined: 92% outcome, 82% comparison method, 81% coverage,
  90% weighting. Chance baseline if the agent made no difference: ~50%.
- Final recommendation: 54% recommended roll-out when the agent leaned
  roll-out vs 36% when it leaned the other way (17-point gap; extension
  counts as not rolling out). Using only the four leans, a statistical
  model predicted 82% of analysts' recommendations vs 61% for always
  guessing the most common recommendation (excludes extension proposers).
- Preference switching: in 38 cases an analyst had expressed a preference
  before the agent expressed its lean. When the lean went against their
  choice they switched 60% of the time vs 6% when it agreed (54-point gap;
  95% CI 24 to 82 points; authors flag imprecision and possible
  confounding — analysts who expressed a preference may differ
  systematically).
- Attribution failure: 77% of analysts repeated their agent's argument in
  at least one post-task answer, sometimes word for word, while only 15%
  credited the agent anywhere. Analysts could not review transcripts while
  answering. 52% rated the final recommendation as more their own than
  the agent's; both groups were roughly equally influenced (choices
  shifted ~65 points toward the lean for the "more mine" group vs ~79
  points for the "more agent's" group, within margin of error).
- Confidence insensitivity: analysts who followed the lean on all four
  decisions averaged confidence 71/100 vs 73 for the rest.
- Recognition: 6 of 48 correctly guessed the study was about AI influence
  on choices; none suspected the agent's preferences had been manipulated.
- No-agent group (not comparable, authors warn): 11 opted out; 6 of 11
  (55%) made serious methodological errors vs 3 of 50 (6%) with the agent;
  median time 90 vs 65 minutes. The no-agent group was less experienced
  on average.
- Default preferences (from their full paper, as summarized on the page):
  with no lean assigned, Claude Opus 4.8 made the same five choices in
  112 of 123 runs.

## 4. Limitations (their own, as stated on the page)

- Leans were deliberately strengthened to measure the effect; real-world
  effect may be smaller when agents are not given clear preferences and
  instructions to voice them.
- One task, one field, one model (Claude Opus 4.8); analysts were causal
  inference experts but new to farming; real work would let them narrow
  options by interviewing people and talking to the board.
- Estimates are averages; no per-participant pre-lean view was recorded,
  so individual influence cannot be quantified; preference strength was
  not measured, so weak prior opinions are a competing explanation for
  deferral (INFERENCE: deferral may partly reflect unformed views, which
  the authors themselves raise as a mechanism).

## 5. Implications (their framing)

- Individual disempowerment: work goes out under the expert's name while
  the judgment calls are settled by the agent's prior beliefs.
- Correlated consensus: if separate teams all defer to models with the
  same preferences, agreement may no longer be independent; one model's
  arbitrary or misaligned preferences could shape many results at once.
- AI safety research: human review is only an independent check if the
  human's judgment is their own; analysts signed off on work whose
  judgment calls were largely settled by randomly assigned preferences.
- Proposed directions: measuring deferral in everyday settings; designing
  agents to argue each option or ask the expert's view first (with
  overload trade-offs); institutions deciding deliberately which
  decisions need a person's own informed judgment.

## 6. What is NOT in this report (scope notes for the adversarial pass)

- No incident, no unsanctioned action against a real system, no real
  third party harmed: the cooperative, program, and data are fictional;
  the lean manipulation was the experimenters' own design, disclosed on
  the page. Do NOT grade this as an agent incident or escape.
- No IOCs: no IPs, domains, accounts, tokens, or real-world identifiers
  appear. IOC record count for this ingest is honestly zero.
- No claim is made that the 86% figure transfers to real work; the
  authors explicitly bound it to strengthened leans. The records below
  carry that bound in their descriptions.
- The 112/123 default-preference figure comes from their full paper as
  summarized on the page, not from the trial data itself; graded UPSTREAM
  with that provenance.
