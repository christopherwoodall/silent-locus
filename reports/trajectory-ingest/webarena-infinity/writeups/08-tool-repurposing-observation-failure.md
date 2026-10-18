# WebArena Infinity: agents repurpose tools when observation fails

**Status:** DRAFT — do not submit (Transluce filing freeze in force). Written 2026-10-17.

## 1. Summary

In two gemini trajectories, the agent's normal observation path broke (element indexing failed) and the agent repurposed unrelated tools to see the page: it wrote and ran its own DOM-scraping JavaScript via `evaluate` three times with escalating targeting, and in another trajectory it used the document-export tool `save_as_pdf` as a screenshot substitute. Both worked. Counting unit: 2 verified findings in this family (A-F004, A-F007), of 21 verified findings total.

Key terms: **element indexing** is the harness's mapping of page elements to clickable indices. `evaluate` runs JavaScript in the page. **DOM** (Document Object Model) is the page's internal structure.

## 2. Corpus and counting unit

- Corpus: `webarena-x/webarena-infinity-trajectories`, revision `73cf7f57a6ff61c95722a23bffdd9c1de4069bfe`, license mit.
- Raw bytes downloaded 2026-10-17 to `data/lanes/webarena-infinity-trajectories/raw/`.
- Review coverage: Reviewer A read all 844 gemini trajectories via per-step digest; both trajectories were verified at byte level.
- Counting unit: n = 2 findings, one per trajectory. A-F004's confidence is HIGH, A-F007's MEDIUM (thin surprise, but the "screenshot substitute" reading is confirmed by the agent's own goal text).

## 3. What happened

**A-F004 (gemini, elation-prescriptions/task_h59):** medication suggestions were invisible to the accessibility tree. The agent wrote and ran its own DOM-scraping JavaScript via `evaluate` at steps 15, 17, 18 with escalating targeting — step 17's goal states it verbatim: "Identify and click the 'Famotidine 40mg tablet' suggestion using JavaScript to bypass the indexing issue." Step 19 fell back to typing 'Famotidine'; step 20 eval: "The search for 'Famotidine' successfully triggered the suggestions dropdown. Verdict: Success".

**A-F007 (gemini, figma-slides/task_e16 and superhuman-general/task_h11):** when element indexing failed, the agent repurposed the document-export tool `save_as_pdf` as a screenshot substitute to visually inspect page layout. In task_e16 step 11: `[find_elements ..., {"save_as_pdf": {"file_name": "assets_panel_view", ...}}]` with the goal "...manage or remove the 'Brand Assets 2025' library by inspecting element attributes and visual layout." In task_h11 step 7: `save_as_pdf {"file_name": "reminders_page", ...}` with the goal "...take a screenshot for visual context." The agent's own goal text confirms the repurposing was deliberate, not accidental.

## 4. Evidence

- **A-F004**, trajectory `gemini/elation-prescriptions/task_h59`, steps 14–20. Quote: 'step17 GOAL: "Identify and click the \'Famotidine 40mg tablet\' suggestion using JavaScript to bypass the indexing issue."; evaluate actions at steps 15, 17, 18 with escalating targeting; step19 falls back to typing \'Famotidine\'; step20 EVAL: "The search for \'Famotidine\' successfully triggered the suggestions dropdown. Verdict: Success"'. File: `raw/gemini/elation-prescriptions/task_h59/history.json`, sha256 `5fa8cd4a…`.
- **A-F007**, trajectories `gemini/figma-slides/task_e16` (step 11) and `gemini/superhuman-general/task_h11` (step 7). Quote: 'figma-slides/task_e16 step11: [find_elements ..., {"save_as_pdf": {"file_name": "assets_panel_view", ...}}], GOAL: "...manage or remove the \'Brand Assets 2025\' library by inspecting element attributes and visual layout."; superhuman-general/task_h11 step7: save_as_pdf {"file_name": "reminders_page", ...}, GOAL: "...take a screenshot for visual context."'. File: `raw/gemini/figma-slides/task_e16/history.json`, sha256 `bf1f2204…`.

## 5. Novelty

This is a new byte-verified instance of a known mechanism, not a first discovery. Creative tool misuse under degraded observation is documented in agent literature. The internal-corpus overlap check found zero overlap. What this adds: the agent's own words framing the act as a bypass ("to bypass the indexing issue") — intent is agent-stated, not inferred — plus the rare screenshot-substitution variant, confirmed by the agent's own goal text.

## 6. Why it matters

The same adaptability that recovers a stuck benchmark task is the adaptability that routes around a safety control. A-F004's agent explicitly framed its move as bypassing a limitation and escalated targeting three times — the behavior shape of circumventing an observation restriction, succeeding here on a benign task. In a deployment, "the normal tool doesn't show me what I need" is exactly when an agent reaches for self-authored JavaScript or export tools — and those tools can touch data the designed tool path would never expose. Tool-use policies that assume agents only use tools as labeled will not survive contact with this behavior.

## 7. Uncertainties

- Non-malicious reading, explicit: both acts were legitimate problem-solving inside the benchmark's rules — the harness offered `evaluate` and `save_as_pdf`, and the agents used them to complete their tasks. Nothing was exfiltrated; no boundary was crossed. The finding is the capability shape, not a violation.
- Could the "bypass" language be the agent narrating a benign workaround rather than evasion intent? The escalating targeting (three evaluate calls) supports a genuine bypass reading, but the agent's words alone do not prove adversarial intent — and none is claimed.
- A-F007 was seen in exactly two trajectories; prevalence of screenshot-substitution beyond these is unknown — open gap.

## 8. Impact

- Harm: **No/negligible harm** (sandbox-contained; both acts completed legitimate tasks). Cyberattack: None.
- Near-miss translation: no near-miss in the incident sense — the acts were benign. The deployment-relevant note is capability-level: agents that lose their designed observation path will author their own, escalate, and succeed. A tool-use allowlist that does not anticipate repurposing (export tools as viewers, script runners as scrapers) has a hole shaped exactly like these two trajectories.
- Disposition: do not replay; read-only analysis. Fix owner: `agent_framework` (observation-failure fallbacks should be designed, not improvised).
