# BrowseComp-Plus search agents: the model's private formatting leaks into the visible channel

**Status: DRAFT ONLY. Do not submit. (Transluce filing freeze in force, 2026-10-16.)**

## 1. Summary

In 118 of 830 ds4pro trajectories, the model's private reasoning delimiter `</think>` leaks into the visible assistant text; in 79 of 830, its native answer-control tag (rendered as `</…DSML…answer>`) appears instead of the harness's `<answer>` format. The control run glm51 shows exactly 1 such row. This is model-formatting behavior, not an agent decision-making TTP — but it is a systematic format-boundary failure that fingerprints a DeepSeek-style reasoning model and can break the harness's answer parsing. Confidence MEDIUM.

## 2. Corpus and counting unit

- Dataset: `liuqi6777/bcp_search_agent_trajectory` (BrowseComp-Plus questions, Apache-2.0), pinned revision `af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f`, retrieved 2026-10-17.
- Full corpus: 4,980 trajectories (830 questions x 6 search agents). This writeup reviews the 15 verified PRIMARY findings of the lane and uses 1 of them (BCP-A-003).
- Counting unit: 1 finding; corpus-wide counts over ds4pro's 830 rows with glm51's 830 rows as control. Exemplars: ds4pro line 9 (msgs[4], msgs[6]), ds4pro line 266 (msgs[90]).
- Terms: "reasoning delimiter" = the token a reasoning model uses to mark the end of its private thinking. "Harness format" = the `<answer>` tag the harness expects the agent to use.

## 3. What happened

Two exemplars, byte-verified:

- ds4pro line 9: assistant messages at 0-based msgs[4] and msgs[6] end with `</think>` — e.g. "...This sounds like it could be about a woman claiming to be Elon Musk's half-sister or relative. Let me search.</think>". (Verifier correction: msgs[8] ends with `</answer>`, not `</think>`; the leak is at msgs[4] and msgs[6].)
- ds4pro line 266 (0-based msgs[90]) ends with the model's native control tag `</…DSML…answer>` where the harness format expects `<answer>`.

Corpus-wide counts: 118/830 ds4pro rows carry `</think>` in assistant messages; 79/830 carry the DSML tag. glm51 carries exactly 1 row with `</think>`. The tokens are the model's own output bytes in the visible channel — not harness-inserted — kept after adversarial review. The behavior is systematic in ds4pro and near-absent in glm51, so it is a genuine distinguishing observable for model attribution.

## 4. Evidence

**BCP-A-003.** Trajectories `ds4pro:predictions.jsonl` (830 rows); exemplars line 9 (0-based msgs[4], msgs[6]) and line 266 (0-based msgs[90]); control `glm51:predictions.jsonl` (830 rows, exactly 1 `</think>` row). Source files: `ds4pro/predictions.jsonl`, sha256 `98ef95fc174bdcdbba3308767e4fffa197b4dc70e94234210aafd5cadf0230af`; `glm51/predictions.jsonl`, sha256 `c54a544e37464484a7ad8b38e408987ddf6c1c885304012d6a6ab1cec3158bed`. Evidence links: `https://huggingface.co/datasets/liuqi6777/bcp_search_agent_trajectory/resolve/af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f/ds4pro/predictions.jsonl` and `/glm51/predictions.jsonl`. Confidence MEDIUM. Counts exact: 118/830 `</think>`, 79/830 DSML tag (ds4pro), 1/830 (glm51).

Review was read-only. No trajectory was replayed and no attack was reproduced.

## 5. Novelty

Checked: local Transluce findings lane (129 files; findings 115-182 included) searched for "browsecomp", "search agent", "fabricat", "schema". No hits on model-formatting leakage. Reasoning-tag leakage is a known property of reasoning-model deployments generally; the new part is the byte-verified, counted observation in this corpus (118/830 + 79/830, near-absent in the control run). Framed as a formatting observable, not a novel TTP — a new measurement, not a first discovery.

## 6. Why it matters

Two practical consequences. First, model attribution: the leak pattern is systematic in one run and near-absent in another, so it works as a fingerprint for a DeepSeek-style reasoning model in the wild — an observable that survives even when the harness relabels the model. Second, harness robustness: a leaked `</…DSML…answer>` in place of the expected `<answer>` can break answer parsing, turning a correct answer into a scored failure. The fix owner is the harness (strip or normalize control tokens at the channel boundary) — this is not something the agent's reasoning can or should fix.

## 7. Uncertainties

- A non-behavioral reading: this may be a harness logging artifact (the harness writing the raw stream including delimiters) rather than the model emitting them into its visible channel. The tokens are the model's own output bytes either way; whether they reached a user-visible channel vs a log channel is not fully separable from this corpus alone. Cannot be ruled out.
- Cannot rule out that the single glm51 row is the same artifact class at low rate rather than a genuine model difference — but the 118:1 ratio is large enough to treat the runs as qualitatively different.
- Explicitly not a TTP: framed as model-formatting behavior with MEDIUM confidence. No claim about agent intent or strategy is made from this finding.

## 8. Impact

- Harm: **No/negligible harm.** Sandbox benchmark; read-only review; formatting bytes in a log file. Cyberattack: None.
- Near-miss: none beyond parsing breakage — a harness that parses answers strictly can mis-score a correct answer when the model emits its native control tag. The wild analog is attribution: the same leak in a deployed product identifies the model family behind an anonymous endpoint.
