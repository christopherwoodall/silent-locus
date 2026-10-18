# JetBrains SWE-bench trajectories: per-turn model mixing makes per-trajectory model attribution wrong by construction

**DRAFT — NOT FOR SUBMISSION (Transluce filing freeze in force, 2026-10-17).**

## 1. Summary

The `selected_models` column mixes `litellm_proxy/openai/gpt-5-mini` and `litellm_proxy/openai/gpt-5.2` across assistant turns inside single trajectories: 1,773 of 1,785 trajectories (99.3%) are two-model products. Strict per-turn alternation holds in only 2 rows. Any claim of the form "gpt-5.2 did X" drawn from this corpus is wrong by construction; behavior attribution must be per-turn, not per-trajectory. Counting unit: 1,785 trajectories (rows 0–1784); 1 corpus-wide methodological finding (F-005).

## 2. Corpus and counting unit

- Corpus: `JetBrains-Research/agent-trajectories-swe-bench-test-minus-verified`, revision `dd79e2540cab4c0cc2c5bab6ea71ddd7ac6c1775`.
- Retrieval: 2026-10-17T02:53:07Z via curl -L.
- Raw file: `~/workspace/silent-locus/data/lanes/jetbrains-swe-trajectories/raw/data/train-00000-of-00001.parquet`, sha256 `5f0d6313bd297cf3d1e23d4a2a4bb27a2fec0bc8d21cf205aef4ff43d7d51b04`.
- n = 1,785 trajectories reviewed; F-005 is a corpus property, not a per-instance behavior. Counting unit here: rows of the `selected_models` column (one row per trajectory).
- Factum lane: `jetbrains-swe-trajectories`; factum batch `ce81bb019a0340b2a3a45365d5d2834a` (+ 4 siblings from the same ingest: `435edfc4…`, `b1670cc9…`, `51368d31…`, `b6d86742…`), 3,595 records, 0 errors.

## 3. What happened

The dataset's `selected_models` column records, per assistant turn, which model served that turn. Verifier-derived unified counts from the column bytes:

- Rows 0–892: 886/893 trajectories mix both models; 7 single-model; 0 empty. First turn: mini 685, 5.2 208.
- Rows 893–1784: 887/892 mix both models; 5 single-model. First turn: mini 646, 5.2 246.
- Corpus: 1,773/1,785 (99.3%) are two-model products.

An early reviewer described the property as "alternates per assistant turn." The verifier corrected this: strict alternation holds in only 2 of 1,785 rows (rows 600 and 1108). Example row 1471 (`django__django-13170`, 30 entries): `mini/5.2/mini/mini/5.2/5.2/5.2/mini/...` — mixed, not alternating. The real property is per-turn model *mixing*, not alternation. The consequence stands either way: a trajectory's turns were authored by two different models, so no behavior observed in a trajectory can be attributed to one model.

## 4. Evidence

- F-005, corpus-wide (trajectory rows 0–1784). `selected_models` column counts above, verified unified from column bytes by the adversarial verifier, confirming both reviewers' independent slice counts exactly. Verbatim quote (byte-verified): "selected_models mixes litellm_proxy/openai/gpt-5-mini and gpt-5.2 across assistant turns within single trajectories (e.g. row 1471: 30 entries mini/5.2/mini/mini/5.2/5.2/5.2/mini/... — mixed, not strictly alternating)". Source: raw parquet above, sha256 `5f0d6313bd297cf3d1e23d4a2a4bb27a2fec0bc8d21cf205aef4ff43d7d51b04`.
- The verifier's alternation correction (2/1785 strictly alternating) is the operative number for any downstream claim about turn routing.
- Reading was read-only. No model identity was probed, replayed, or confirmed through any external channel.

## 5. Novelty

Prior Transluce work documents the *convention* this warns about, not this corpus's property. #174 (WildClawBench secrets) establishes: "The six runs were labelled Claude Opus, GLM, HY3, Intern-S2, Kimi K2.7 and Kimi K3... These model names come from the dataset" — trace metadata as labels, never attributions. The template's credibility rules codify the same point (#172: "Model and provider names are trace metadata only"). What this adds: a corpus-scale, byte-counted quantification — 99.3% of rows are two-model products — plus the correction that the mixing is not strict alternation (an earlier, plausible description that the bytes reject). Anyone citing this corpus for "gpt-5.2 behavior" now has an explicit, counted barrier. This is a methodological caveat finding, not an agent behavior.

## 6. Why it matters

This corpus carries the freshest models in any trajectory corpus surveyed (gpt-5.2, gpt-5-mini) and will be tempting as a per-model behavior source. The tempting use is exactly the wrong one: every other writeup in this family (01–04) deliberately attributes behavior to "the agent" and never to a model, because the bytes do not support more. A benchmark result like "gpt-5.2 evades test guardrails" built on these trajectories would attribute to one model turns authored by the other. Per-turn attribution is the only honest unit, and it requires turn-level analysis the trajectory-level rollups in this corpus do not provide directly.

## 7. Uncertainties

- The `selected_models` column is dataset metadata, not a cryptographic attestation of which weights served each turn. The mixing property is verified *in the bytes*; whether the bytes faithfully reflect the serving setup is upstream of this corpus and cannot be checked from inside it.
- 12 single-model rows (7 + 5) are the only trajectories where per-trajectory model attribution is even arguably safe; their model identities still rest on the same unverified metadata.
- The two strictly alternating rows (600, 1108) are consistent with a round-robin router, but "round-robin" is an internal hypothesis about the data-collection setup — labeled as such, not a confirmed fact.
- This writeup makes no claim about which model produced any behavior in writeups 01–04, and does not attempt per-turn attribution there either.

## 8. Impact / harm

- Harm: No/negligible harm. Methodological finding about dataset provenance; no behavior, no external effect.
- Near-miss translation: none — there is no contained outcome to translate. The "harm" it prevents is analytic: false model-level claims built on mixed-model trajectories.
- Cyberattack: None.
