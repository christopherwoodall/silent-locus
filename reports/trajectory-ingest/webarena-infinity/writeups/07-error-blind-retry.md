# WebArena Infinity: qwen repeats a keypress the harness rejects, five to eleven times

**Status:** DRAFT — do not submit (Transluce filing freeze in force). Written 2026-10-17.

## 1. Summary

In two qwen trajectories, the agent emitted the key combination ["ctrl", "a"] repeatedly; every emission failed with 'Keyboard.press: Unknown key: "ctrl"', and the agent never adapted — it re-emitted the same failing action up to 11 times without any thought mentioning the error. A cross-model check confirmed the loop is qwen-specific (the qwen harness exposes a `key` tool that rejects "ctrl"). Counting unit: 2 verified findings in this family (RB-001, RB-002), of 21 verified findings total.

Key terms: a **key emission** is a keyboard-press action the agent sends to the app. An **error-blind loop** is a retry cycle where the agent never registers the error its action produces.

## 2. Corpus and counting unit

- Corpus: `webarena-x/webarena-infinity-trajectories`, revision `73cf7f57a6ff61c95722a23bffdd9c1de4069bfe`, license mit.
- Raw bytes downloaded 2026-10-17 to `data/lanes/webarena-infinity-trajectories/raw/`.
- Review coverage: Reviewer B enumerated all 40 result.json error trajectories and read the ctrl+a cases in full; an independent cross-model check grepped all raw/<model> files for "Unknown key" and "ctrl".
- Counting unit: n = 2 findings, one per trajectory. n does NOT count the 38 qwen trajectories with 'Unknown key' errors corpus-wide — only these two were verified at byte level as the full error-blind loop shape.

## 3. What happened

**RB-001 (qwen, elation-clinical-records/task_h3):** the agent emitted key ["ctrl", "a"] at 0-based steps 8, 11, 14, 19, 22. result.json records 5 errors: 'Action error at step N: Keyboard.press: Unknown key: "ctrl"'. No thought in the trajectory mentions the key error. The agent saw only the symptom (accumulated text it had meant to select) and re-emitted the same failing action.

**RB-002 (qwen, handshake-career-exploration/task_h6):** 11 'Unknown key: "ctrl"' errors in result.json, with emissions at 0-based steps 8, 12, 16, 20, 24, 27, 31, 32, 35, 38, 42. Step 45 thought: "Action: Terminate the task as the goal of following finance industry employers has been completed." — then terminate. The verifier passed it: "All finance employers are followed: JPMorgan Chase (emp_02), Goldman Sachs (emp_06)...". Same error-blind loop, then a termination claiming success. (The reviewer's "finfinance..." text-accretion description was corrected: it is an inference about UI state, not a verbatim byte — input actions record only {"type":"input","text":"finance"}.)

**Cross-model check:** the loop is qwen-specific. qwen: 38 trajectories with 'Unknown key' errors (98 instances); 23 history.json files mention 'ctrl'; 13 trajectories have ≥3 such errors. kimi: 4 files mention 'ctrl', all via pyautogui.keyDown('ctrl') in code blocks; zero 'Unknown key' errors. gemini: zero 'ctrl' mentions, zero 'Unknown key' errors — its action schema has no raw key-press tool that emits ctrl, so the failure mode cannot occur there. Conclusion: a qwen-harness interaction, not a cross-model phenomenon.

## 4. Evidence

- **RB-001**, trajectory `qwen/elation-clinical-records/task_h3`, steps 8–22. Quote: 'key ["ctrl", "a"] emitted at 0-based steps 8, 11, 14, 19, 22 (thought text); result.json errors: 5x \'Action error at step N: Keyboard.press: Unknown key: "ctrl"\'; no thought in the trajectory mentions the key error.' File: `raw/qwen/elation-clinical-records/task_h3/history.json`, sha256 `25ede14b…`.
- **RB-002**, trajectory `qwen/handshake-career-exploration/task_h6`, steps 8–45. Quote: '11 \'Unknown key: "ctrl"\' errors in result.json (emissions at 0-based steps 8,12,16,20,24,27,31,32,35,38,42); step45 thought: \'Action: Terminate the task as the goal of following finance industry employers has been completed.\' (terminate action); result.json passed=True, verifier \'All finance employers are followed: JPMorgan Chase (emp_02), Goldman Sachs (emp_06)...\''. File: `raw/qwen/handshake-career-exploration/task_h6/history.json`, sha256 `162a73ba…`.
- Cross-model check artifact: `working/cross-model-ctrl-check.txt` (method: grep over raw/<model> for 'Unknown key' in result.json and 'ctrl' in history.json).

## 5. Novelty

This is a new byte-verified instance of a known mechanism, not a first discovery. Error-blind retry and action-error non-adaptation are documented agent failure modes. The internal-corpus overlap check found zero overlap. What this adds: the cross-model attribution — the loop is a qwen-harness interaction (a `key` tool that rejects "ctrl" while the model's policy keeps emitting it), verified present in qwen and absent in kimi and gemini. That makes it a harness-design finding as much as a model finding.

## 6. Why it matters

An agent that cannot perceive its own action errors will burn steps, corrupt inputs, and then — as RB-002 shows — terminate claiming success. The verifier passed RB-002, so the loop is also invisible to the benchmark's success signal. For training: these trajectories teach "keep doing the failing thing" as successful behavior. For deployment: any action channel whose errors are not surfaced to the model in its thought context will produce the same blindness — the model cannot adapt to feedback it never sees. Fixing the error channel (surfacing 'Unknown key' into the observation the model actually reads) is cheaper than fixing the model.

## 7. Uncertainties

- Do the 'Unknown key' errors reach the model's observation at all? The trajectories' thoughts never mention them, which suggests the errors are logged to result.json but not fed back into the model's context. That is an inference from absence; the harness source was not inspected — cannot be fully ruled out.
- RB-002's final pass: did the verifier's "all employers followed" reflect real state or accident? The bytes confirm passed=true with that verifier message; whether the follows actually happened is not re-verified. The finding stands on the loop + the termination claim, not on the verifier's correctness.
- The 38 qwen trajectories with 'Unknown key' errors were counted, not byte-verified — prevalence of the full loop shape beyond these two is an open gap.
- Non-malicious reading, explicit: this is a scaffolding failure (a tool that rejects an input the model reasonably emits), not model misbehavior. The agent is doing the sensible thing given a broken channel.

## 8. Impact

- Harm: **No/negligible harm** (sandbox-contained; wasted steps, no live effect). Cyberattack: None.
- Near-miss translation: the same blindness on a real keyboard/input channel means repeated failed inputs against live systems — form corruption, repeated submissions, or a false success claim after 11 silent failures. RB-002's terminate-claiming-success is the shape to watch: the agent declared victory over a run dominated by errors it never saw.
- Disposition: do not replay; read-only analysis. Fix owner: `environment` (surface tool errors into the model's observation context; the qwen `key` tool should accept or clearly reject "ctrl").
