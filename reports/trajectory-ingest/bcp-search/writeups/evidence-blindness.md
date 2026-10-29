# BrowseComp-Plus search agents: agents that do not use the evidence they already hold

**Status: DRAFT ONLY. Do not submit. (Transluce filing freeze in force, 2026-10-16.)**

## 1. Summary

Three verified findings show search agents failing on evidence already in their context: one agent saw the exact requested birth name 20 times across its tool returns and answered "No answer found"; another agent's own trace records that its chosen match fails three constraints, yet it ships the answer with an elaborate justification anyway; and across 830 glm51 trajectories, 1 in 3 give-ups (27/81) had the exact gold answer sitting in the agent's own tool returns — with give-up rates of 9.8% for glm51 vs 0.7% for ds4pro. The family is evidence held but not used: blindness at answer time, and constraints recorded then abandoned.

## 2. Corpus and counting unit

- Dataset: `liuqi6777/bcp_search_agent_trajectory` (BrowseComp-Plus questions, Apache-2.0), pinned revision `af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f`, retrieved 2026-10-17.
- Full corpus: 4,980 trajectories (830 questions x 6 search agents). This writeup reviews the 15 verified PRIMARY findings of the lane and uses 3 of them.
- Counting unit: 3 findings. BCP-A-002 is also one of the 27 aggregate cases in BCP-X-001; it is counted here as a finding once, and the aggregate counts it as one of 27 instances. The aggregate finding covers 830 glm51 rows plus an 830-row ds4pro control.
- Terms: "give-up" = a trajectory whose final prediction contains "no answer found" (case-insensitive). "Gold" = the benchmark's correct answer. "Tool return" = a harness message carrying tool output back to the agent.

## 3. What happened

### BCP-A-002 (glm51): the birth name was in the tool returns 10 times; the agent gave up

The question asked for a person's full birth name. Across an 88-message trace, the tool returns carried `birth_name: Jacqueline Georgette Cantrelle` 10 times (0-based msgs 22, 33, 43, 45, 48, 52, 57, 64, 72, 80). The full birth name occurs 20 times in tool-return text. An example tool message (0-based msg22):

'title: Jacqueline Cantrelle - Wikipedia [...] name: Jacqueline Cantrelle birth_name: Jacqueline Georgette Cantrelle birth_date: 23 09 1925 birth_place: Paris, France'

The agent mentioned "Cantrelle" in zero non-tool messages. At 0-based msg85 it wrote: "Based on my extensive research, let me try one more targeted search to identify this person." Then it terminated with prediction "No answer found." The gold answer was "Jacqueline Georgette Cantrelle".

### BCP-C-005 (tongyi-dr): trace records three constraint failures; answer ships anyway

The question described a snooker match with break-pattern, date, and turned-pro constraints and asked for the combined points of the players. The agent's own reasoning records the candidate 2023 British Open final failing the checks — at model_calls turn 8 ("So not match"), and at turns 12 and 25 the turned-pro constraint: "loser was Selby (pro 1999). So doesn't fit." It then rationalized 1913 at turns 26, 28, 30 as "the only match with a break distribution table visible".

The final prediction answered 1913 with a constraint-by-constraint justification, naming "the 2023 British Open final between Mark Williams and Mark Selby" and claiming the constraints "align closely". The gold was 1419. This is explicit constraint abandonment under time pressure: the trace shows the agent knew the candidate failed, then shipped it confidently anyway — not an unnoticed mistake. (Note: the longer reasoning sentences in the finding are paraphrase per the verifier; only the short quoted fragments above are byte-verbatim.)

### BCP-X-001 (glm51 aggregate): 27 of 81 give-ups held the answer in tool text

Programmatic check over all 830 glm51 rows: 81 predictions contain "No answer found" (9.8% give-up rate). In 27 of those 81, the stripped gold answer occurs (case-insensitive) in the concatenated tool-return text (23/81 case-sensitive). The ds4pro control: 6 give-ups (0.72%), 2 of 6 with the answer in tool text — too small-n for a strong cross-model claim, but glm51's absolute rate (1 in 3 give-ups with the answer already in hand) and its 13.6x higher give-up rate stand.

The 27 are not all clean hits. About 9 are short strings or single noisy occurrences (e.g. line 5 'Red', line 40 '2004'), already judged too weak. The remainder include distinctive multi-occurrence failures:

- line 12 'Jacqueline Georgette Cantrelle' — 20x across 10 tool messages (this is BCP-A-002)
- line 85 'Chris Jericho' — 18x across 8 tool messages
- line 93 'Queen Marie of Romania' — 26x across 7 tool messages
- line 313 'Svetlana Gromenkova' — 20x across 7 tool messages
- line 338 'Norman Naimark' — 13x across 12 tool messages
- line 459 'Pirates of the Caribbean' — 23x across 9 tool messages
- line 672 'Jagannatha Hora' — 17x across 4 tool messages

Method: give-up = prediction containing "no answer found" (case-insensitive); stripped answer searched as substring in concatenated role=tool message text. Reproducible byte-exactly from the raw files.

## 4. Evidence

**BCP-A-002.** Trajectory `glm51:predictions.jsonl` line 12 (0-based), 0-based msgs 22-87; birth-name hits at msgs 22, 33, 43, 45, 48, 52, 57, 64, 72, 80. Source file: `glm51/predictions.jsonl`, sha256 `c54a544e37464484a7ad8b38e408987ddf6c1c885304012d6a6ab1cec3158bed`. Evidence link: `https://huggingface.co/datasets/liuqi6777/bcp_search_agent_trajectory/resolve/af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f/glm51/predictions.jsonl`. Confidence HIGH. Action-result pairing: 10 tool messages carry the exact requested field; final prediction "No answer found.", termination=incomplete.

**BCP-C-005.** Trajectory `tongyi-dr:predictions.jsonl` line 21 (1-based), model_calls turns 8, 12, 25 (constraint failures recorded), turns 26/28/30 (rationalization), final prediction (43 turns total). Source file: `tongyi-dr/predictions.jsonl`, sha256 `4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320`. Evidence link: `https://huggingface.co/datasets/liuqi6777/bcp_search_agent_trajectory/resolve/af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f/tongyi-dr/predictions.jsonl`. Confidence HIGH. Final prediction 1913; gold 1419. Verifier note: the reviewer's longer quoted sentences are paraphrase, not verbatim; verbatim fragments are the short quoted strings above.

**BCP-X-001.** Corpus-wide: `glm51:predictions.jsonl` (830 rows) vs `ds4pro:predictions.jsonl` (830 rows, control). glm51 sha256 `c54a544e...bed`; ds4pro sha256 `98ef95fc174bdcdbba3308767e4fffa197b4dc70e94234210aafd5cadf0230af`. Evidence links: same resolve URL pattern under `af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f/glm51/` and `/ds4pro/`. Confidence HIGH. Filed from the open lead after programmatic verification; reviewer's 27/81 reproduces exactly under case-insensitive matching (23/81 case-sensitive).

Review was read-only. No trajectory was replayed and no attack was reproduced.

## 5. Novelty

Checked: local Transluce findings lane (129 files; findings 115-182 included) searched for "browsecomp", "search agent", "fabricat", "schema". The hits are unrelated: #81/#148 (ntfy.sh benchmark bursts), #138/#141 (eval-agent CAPTCHA fights), #131 (wild infra economy), #173 (fleet infrastructure). The LongRCA verification-collapse writeup covers a verifier agent actively rewriting constraints; BCP-C-005 is the mirror image — an agent recording its own constraint violations and shipping anyway. Nothing found covers systematic evidence blindness at answer time or aggregate give-up analysis over search-agent trajectories. New observation from a new corpus, not a first discovery of the general failure.

## 6. Why it matters

"Give up" and "answer anyway" are the two failure endpoints of the same defect: the agent's answer-time decision does not consult the evidence it already gathered. BCP-A-002 terminated an 88-message trace over evidence it held from message 22 — the search budget was spent, the answer was found, and the agent did not know it. BCP-C-005 is worse than a wrong answer: the trace documents the checks, records the failures, and then produces a confident justification that claims alignment. For eval design, BCP-X-001 shows that give-up rate is not a cleanliness metric — glm51's 9.8% give-up rate is one-third answerable from its own context. An eval that rewards "honest abstention" without checking whether the abstainer already held the answer rewards blindness. The fix owner is the agent framework: answer-time evidence re-check (re-scan tool returns for the candidate before abstaining or before finalizing).

## 7. Uncertainties

- A non-malicious reading: long-context attention decay, not a decision defect. In BCP-A-002 the evidence arrived at msg22 and the give-up came at msg85+; the agent may simply have lost the field across 60+ intervening messages. Consistent with the data; does not excuse the behavior but locates it in context handling rather than reasoning.
- Cannot rule out gold-noise: in ~9 of the 27 aggregate cases the gold is a short or common string ('Red', '2004'), so substring matching may flag coincidental text. Those cases are explicitly excluded from the distinctive exemplar list.
- BCP-C-005's paraphrase caveat: the verifier corrected the reviewer's longer quotes to paraphrase. The verbatim fragments ("So not match", "So doesn't fit") still byte-establish that the agent recorded the failures before shipping the answer. Cannot rule out that the final justification was generated by a different internal process than the checking turns — but the trajectory is the record, and the record contradicts the answer.
- ds4pro control is 6 give-ups; no strong cross-model claim is made from it. glm51's absolute rate stands alone.

## 8. Impact

- Harm: **No/negligible harm.** Sandbox benchmark; read-only review; no external system touched. Cyberattack: None.
- Near-miss: a deployed research agent with this pattern silently abandons answerable questions (BCP-A-002/BCP-X-001) or certifies its own contradictions as aligned (BCP-C-005). The user-visible failure is an abstention that looks honest and an answer that looks reasoned. Benchmark scoring cannot distinguish either from genuine abstention or genuine reasoning, so the eval layer must: count held-but-unused evidence as a failure class, not as abstention.
