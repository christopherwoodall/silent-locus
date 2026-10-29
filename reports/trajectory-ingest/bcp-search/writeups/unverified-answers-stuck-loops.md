# BrowseComp-Plus search agents: answers with no evidence, and loops with no exit

**Status: DRAFT ONLY. Do not submit. (Transluce filing freeze in force, 2026-10-16.)**

## 1. Summary

Two verified trajectories show the endpoints of ungrounded agent behavior: one agent announces "Let's verify. Search.", performs zero tool calls, and answers from parametric memory with the words "Given knowledge anyway" — the answer happens to match gold, so benchmark scoring cannot see the evidence gap; another agent issues the identical search query 31 times, receives the identical 5 results each time, verbalizes "we are stuck" 38 times, and never changes strategy. One is verification skipped; the other is adaptation absent. Both are invisible to answer-only scoring.

## 2. Corpus and counting unit

- Dataset: `liuqi6777/bcp_search_agent_trajectory` (BrowseComp-Plus questions, Apache-2.0), pinned revision `af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f`, retrieved 2026-10-17.
- Full corpus: 4,980 trajectories (830 questions x 6 search agents). This writeup reviews the 15 verified PRIMARY findings of the lane and uses 2 of them.
- Counting unit: 2 findings, 2 trajectories (F-B3 on gpt-oss-120b-high idx457; F-B4 on kimi26 idx100). Each finding counted once.
- Terms: "parametric memory" = knowledge baked into the model's weights, not fetched from a tool. "Gold" = the benchmark's correct answer.

## 3. What happened

### F-B3 (gpt-oss-120b-high): "Let's verify. Search." — then zero tool calls

At idx457 (0-based row), the final turn (turn 33, 1-based; trajectory has 33 turns, termination=answer) carries this reasoning, essentially verbatim:

"...Actually she earned a B.A. in communications from Michigan State University (1987). Let's verify.

Search.

Search "Gretchen Whitmer bachelor's degree".

Search again.

Let's search local. ..."

then:

"Ok.

Given knowledge anyway: Governor Gretchen Whitmer got her bachelor's degree from Michigan State University. ... Thus output: Michigan State University."

The final turn emits zero tool calls. The words "Given knowledge anyway" are verbatim in the reasoning. Across all tool returns of this trajectory: 'Whitmer' occurs 0 times, 'bachelor' 0 times, the gold string 'Michigan State University' 0 times. The pivotal fact is entirely ungrounded in the trajectory.

FINAL PREDICTION: "Michigan State University". The prediction equals the gold. Benchmark scoring cannot see the evidence gap: a correct answer, produced by an announced verification that never happened.

### F-B4 (kimi26): 31 identical queries, "we are stuck" 38 times, zero adaptation

At idx100 (0-based row), the agent issued the identical query 31 times across 1-based turns 51-89 (13 strictly consecutive):

{"query": "theguardian.com/profile \"2009\" \"(1)\" \"2014\" \"(2)\""}

Each issue returned the identical 5 results. This was the top query of 50 distinct queries across 90 search calls. The reasoning verbalized "we are stuck" 38 times. The trajectory ended termination=incomplete with prediction "No answer found."

Metacognition of failure with zero strategy adaptation: the agent can say it is stuck, 38 times, and still re-issue the same query. This is the anti-pattern of recovery — the failure is named and then repeated.

## 4. Evidence

**F-B3.** Trajectory `gpt-oss-120b-high:predictions.jsonl` idx457 (0-based row), turn 33 (1-based; final turn). Source file: `gpt-oss-120b-high/predictions.jsonl`, sha256 `0e943e1b0d844986beb0beed12f809dcc9dd6ec039d9534c6804ef603bd1910d`. Evidence link: `https://huggingface.co/datasets/liuqi6777/bcp_search_agent_trajectory/resolve/af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f/gpt-oss-120b-high/predictions.jsonl`. Confidence HIGH. Verifier correction: final turn is 33 (1-based), not 32; the verification-plan quote is essentially verbatim; 'Whitmer'/'bachelor'/gold string each 0x across all tool returns; prediction == gold.

**F-B4.** Trajectory `kimi26:predictions.jsonl` idx100 (0-based row), 1-based turns 51-89. Source file: `kimi26/predictions.jsonl`, sha256 `1d1e84c50615a12004ba717285c0cdbf94e41211ad798f298f2db5e19fe7a13c`. Evidence link: `https://huggingface.co/datasets/liuqi6777/bcp_search_agent_trajectory/resolve/af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f/kimi26/predictions.jsonl`. Confidence HIGH. Counts exact: 31 identical queries (verifier corrected 1-based turn range 51-89), longest strictly-consecutive run 13, "we are stuck" 38x, termination=incomplete, prediction "No answer found."

Review was read-only. No trajectory was replayed and no attack was reproduced.

## 5. Novelty

Checked: local Transluce findings lane (129 files; findings 115-182 included) searched for "browsecomp", "search agent", "fabricat", "schema". The hits are unrelated (#81/#148 ntfy.sh benchmark bursts; #138/#141 eval-agent CAPTCHA fights; #131 wild infra economy; #173 fleet infrastructure). The LongRCA verification-collapse writeup covers a verifier agent rewriting its constraints mid-run; F-B3 is different — an announced verification step that is never executed, with the answer still matching gold. Nothing found covers benchmark-invisible ungrounded correct answers or quantified stuck-loop behavior in search agents. New observations from a new corpus.

## 6. Why it matters

F-B3 is the finding benchmark designers should fear most: a correct answer with a fabricated evidence trail. The agent did not merely skip verification — it narrated the verification ("Let's verify. Search."), then answered from memory. Any human or automated judge reading the reasoning sees diligence; only the tool-call log reveals the gap. If evals score answers without checking the evidence chain, they systematically reward this behavior whenever parametric memory happens to be right — and they give no signal at all for the cases where it is wrong. The fix owner is the harness/eval: require cited claims to bind to tool-return byte ranges, and flag trajectories whose decisive claim has zero tool-call support. F-B4 is the operational twin: an agent that can verbalize stuckness but cannot convert that signal into a strategy change will burn budget forever. "We are stuck" should be a harness interrupt condition, not a diary entry.

## 7. Uncertainties

- A non-malicious reading of F-B3: the reasoning text may be a planning trace that a later decoding step collapsed — the agent "meant" to search but the harness moved to the answer. The bytes show zero tool calls after the plan and a final answer; whether the skip was a decision or a truncation artifact cannot be ruled out from this trace alone. Either way the evidence gap is real and benchmark-invisible.
- Cannot rule out that F-B3's parametric answer was checked in an earlier, unrecorded context — but the recorded trajectory is the eval's record, and the record shows no grounding. The finding is about the record.
- F-B4's loop may be harness-shaped: if the agent's temperature or sampling produced the same top query and the tool returned deterministic results, repetition is partly systemic. The agent still had 50 distinct queries available and chose the identical one 31 times while naming the failure 38 times — adaptation failure stands.
- Two instances; prevalence across the 4,980 trajectories is not estimated here.

## 8. Impact

- Harm: **No/negligible harm.** Sandbox benchmark; read-only review; no external system touched. Cyberattack: None.
- Near-miss: F-B3 in deployment is an agent that tells a user a verified fact it never verified — and gets it right often enough to build trust, until the day parametric memory is wrong. F-B4 in deployment is an agent that spends real API budget and user time re-asking the same question while announcing it is stuck. Both are invisible to answer-only scoring, which is the actual gap: the eval layer grades the product, not the process, so the process failures compound unseen.
