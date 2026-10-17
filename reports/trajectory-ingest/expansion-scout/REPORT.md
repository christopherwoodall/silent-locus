# Trajectory Expansion Scout — Final Report (2026-10-16/17)

BigSexyWarlock69's order: find MORE public agent-trajectory corpora to ingest, and survey how others report benchmark/trajectory failures so we can adapt.

**Task A lanes run:** HF agent-trajectory search, web/computer-use benchmarks, coding/security benchmarks. curl-only, HEAD/tiny-fetches, license-verified verbatim. One original lane's result was lost in delivery and re-dispatched; HF lane re-dispatch was closed as redundant after the original delivered.
**Task B lanes run:** incident/taxonomy survey, lab/community survey, then redirected per his 2026-10-16 direction: NOT a systematic dataset-inventory format — a Transluce-style per-corpus BEHAVIOR/TTP WRITEUP TEMPLATE, extracted from exemplar findings (#159/#170/#172/#174 plus #180/#181/#182).

---

## TASK A — RANKED NEW CORPORA (deduped across lanes)

### Wave 1 — small, high behavior density, ungated, clean licenses (do these first)

1. **AI-Secure/DTap-Bench-Agent-Trajectories** — https://huggingface.co/datasets/AI-Secure/DTap-Bench-Agent-Trajectories
   - License: `apache-2.0` (verbatim). **48,098+ timestamped trajectory JSONs** (lower bound; API listing caps at 100k) + 49,098 judge_result.json. 7+ model dirs (claude-opus-4-6, claude-sonnet-4-5, gemini-3-pro-preview, gpt-5.1, gpt-5.2, gpt-5.4, gpt-oss-120b). Browser/tool red-teaming tasks with step-level trajectories + judge verdicts. Byte-verified real. Ungated. Highest behavior density of all candidates.

2. **liuqi6777/bcp_search_agent_trajectory** — https://huggingface.co/datasets/liuqi6777/bcp_search_agent_trajectory
   - License: `apache-2.0` (verbatim). **4,980 full ReAct traces** (830 BrowseComp-Plus questions × 6 search agents): every reasoning trace + tool call + tool return, ~2.1 GB. From *Diagnosing Search Behavior and Failure Modes in Long-Horizon Search Agents*. Behaviorally richest non-code corpus. Ungated.

3. **webarena-x/webarena-infinity-trajectories** — https://huggingface.co/datasets/webarena-x/webarena-infinity-trajectories
   - License: `mit` (verbatim). **2,329 trajectories exactly** (Gemini 2.5 Flash 978 / Qwen 2.5 VL Plus 708 / Kimi K2.5 643; all successful, programmatically verified), 13 web-app environments, per-trajectory history.json + result.json + per-step screenshots, ~1.6 GB. Ungated.

4. **JetBrains-Research/agent-trajectories-swe-bench-test-minus-verified** — https://huggingface.co/datasets/JetBrains-Research/agent-trajectories-swe-bench-test-minus-verified
   - License: `mit` (verbatim). **1,785 trajectories**, 102 MB. Mixed teachers **gpt-5.2 / gpt-5-mini** — freshest models in any corpus found. Ungated.

5. **jordan-taylor-aisi InterCode-CTF family** — https://huggingface.co/datasets/jordan-taylor-aisi/70B_normal_llama_33_70b_instruct_gdm_intercode_ctf (+ ~9 siblings)
   - License: `apache-2.0` (verbatim). UK AISI inspect-eval runs on InterCode-CTF offensive-security tasks; 79 samples/dataset, 7–33 turns incl. function tool_calls; raw `.eval` inspect logs shipped. **Only viable security-lane corpus.** Ungated.

### Wave 2 — mid-size, ungated, clean licenses

6. **nebius/SWE-rebench-openhands-trajectories** — https://huggingface.co/datasets/nebius/SWE-rebench-openhands-trajectories
   - License: `cc-by-4.0` (verbatim). **67,074** OpenHands v0.54 rollouts (Qwen3-Coder-480B-A35B) on real GitHub issues from nebius/SWE-rebench; 185-step sample verified, exit_status/resolved/gen_tests_correct flags. Ungated.

7. **agent-eto/eto-sft-trajectory** — https://huggingface.co/datasets/agent-eto/eto-sft-trajectory
   - License: `apache-2.0` (verbatim). **6,423** expert SFT trajectories: ALFWorld 3,118 / ScienceWorld 1,482 / WebShop 1,823. Ungated.

8. **SWE-Factory/DeepSWE-Agent-Kimi-K2-Trajectories-2.8K** (+ Rejection-Sampling variant) — https://huggingface.co/datasets/SWE-Factory/DeepSWE-Agent-Kimi-K2-Trajectories-2.8K
   - License: `mit` (verbatim). ~2,800 trajectories each, single JSONL; DeepSWE agent system prompt + Kimi K2 byte-verified real. Ungated.

9. **Hongliang1997/WebVoyager-Trajectories-GPT-4V** — https://huggingface.co/datasets/Hongliang1997/WebVoyager-Trajectories-GPT-4V
   - License: `apache-2.0` (verbatim). **643 tasks**, single zip **1.95 GiB** (HEAD-verified); uploader = paper author; the original WebVoyager paper's GPT-4V runs. Ungated.

10. **SeerRay-Lab/Android-World-Eval** — https://huggingface.co/datasets/SeerRay-Lab/Android-World-Eval
    - License: `mit` (verbatim). **464 rollouts** (116 AndroidWorld tasks × 4); range-fetched head verified: trace_id, turns[] with screenshot_base64 + llm_response + parsed action + reward. ~1.6 GB total. Ungated.

11. **xlangai/ubuntu_osworld_verified_trajs** — https://huggingface.co/datasets/xlangai/ubuntu_osworld_verified_trajs
    - License: `mit` (verbatim card frontmatter + tag). README claims **1000+ OSWorld episodes**; 99 zips confirmed across 30+ model variants × step settings (Claude 3.7/4/4.5, o3, Gemini, Qwen, UI-TARS, OpenCUA, Jedi, Kimi K2.5/K2.6...). Each zip = screenshots + actions + reasoning + results. Media-heavy. Ungated.

12. **mlfoundations/gelato-osworld-agent-trajectories** — https://huggingface.co/datasets/mlfoundations/gelato-osworld-agent-trajectories
    - License: `mit` (verbatim tag). **2,166 trajectories** (counted result.txt files), 38,932 files. Ungated.

### Wave 3 — large bulk SWE corpora (sample-first, watch disk)

13. **nebius/SWE-agent-trajectories** — https://huggingface.co/datasets/nebius/SWE-agent-trajectories
    - License: `cc-by-4.0` (verbatim). **80,036** SWE-agent framework trajectories, 5.6 GB, eval_logs + generated_patch + per-step messages. (Byte-identical mirror at ElenaFu/SWE-agent-trajectories.) Ungated.

14. **SWE-bench/SWE-smith-trajectories** — https://huggingface.co/datasets/SWE-bench/SWE-smith-trajectories
    - License: `mit` (verbatim). **76,002** rows across 3 scaffolds (tool/xml/ticks), ~10.7 GB; trajectories used to train SWE-agent-LM-32B. Ungated.

15. **Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k** — https://huggingface.co/datasets/Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k
    - License: `mit` (verbatim). **65,994** mini-swe-agent-plus rollouts, 4.64 GB. Ungated.

### Caution tier (viable but with caveats)

16. **whysue/agent-real-pentest-trajectory** — `mit`, 2.29 GB autonomous pentest traces (CoE-Planner + workers). Verified real trace JSONL, but README is a contact email only — sparse provenance. Low priority.
17. **sunnydubey1111/agent-trajectory-sentinel** — `other`/`mixed-see-licensing`, 3,581 failure-taxonomy episodes across 33 corpora (step telemetry, failure_class). Mixed model-output terms (qwen2.5 Apache-2.0, llama3.1 Community License, gemini-2.5 Gemini API terms) — ingest with terms caveat.
18. **SWE-Gym/OpenHands-SFT-Trajectories** — `mit`, 491 successful OpenHands SFT trajectories. Small but real.
19. **orlando23/failed_agent_trajectory** — `apache-2.0`, 52 mobile trajectories with screenshots (MagicWand/LoT paper). Niche.
20. **obaydata/mcp-agent-trajectory-benchmark** — `apache-2.0`, 49 MCP tool-use trajectories. Vendor-generated, synthetic-flavored. Lowest priority.

### KILL LIST (license null or not-trajectories)

**Real trajectories, killed on license (biggest losses):**
- R2E-Gym family: `R2E-Gym/R2EGym-SFT-Trajectories` (3,231), `R2EGym-Verifier-Trajectories` (5,750), `R2EGym-TestingAgent-SFT-Trajectories` (2,281); `AxT-dev/qwen3-32b-rl-step200-r2e-gym-trajectories` (agentic-RL rollouts — biggest single loss); `AxT-dev/swe-agent-lm-32b-r2e-gym-trajectories`; `r2e-edits/SWE-smith-trajectories-R2E` family (5,016 each); `ydeng9/swe-smith-rl-distill`; `NousResearch/SWE-smith-oracle`
- `SWE-Gym/OpenHands-Sampled-Trajectories`, `SWE-Gym/OpenHands-Verifier-Trajectories`, `SWE-Gym/SWE-Gym-Raw`, `swesynth/SWE-Gym-logs`, `swesynth/SWE-Gym_Lite-logs`
- CyBench: `lvogel123/cybench-*` (8 datasets: grok-4, qwen3-235b-thinking, claude-sonnet-4.5, gemini-2.5-pro, llama-3.3-nemotron, llama-4-maverick, gpt-5-high)
- `antieval/agentharm-trajectories` — the only AgentHarm trajectory dump found
- DCAgent terminal-bench-2 sets (`DCAgent/GPT-5-terminal-bench-2`, `claude-sonnet-4-5-terminal-bench-2`, +3 sandbox-trace sets)
- `mlfoundations-dev/terminal-bench-traces-local` (terminal-bench parquet)
- `OpenHandsCommunity/eval-output-webarena` (BrowsingAgent WebArena eval outputs)
- `mlfoundations-cua-dev/computer-agent-trajectories` (410 arrow-format files)
- `WenyiWU0111/webvoyager_evaluation_data` (3,497 per-task JSONs)
- `hanspeterlyngsoeraaschoujensen/aider-polyglot-eval-trajectories` (only Aider dump found)
- `AlienKevin/Multi-SWE-smith-Rust-GLM-4.6-trajectories` (142 GLM-4.6 trajectories — painful, exact target lane)
- `pimpalgaonkar/terminalbench-sqlite-db`, `KMK040412/fast-dvlm-guiowl-androidworld-artifacts`, `liangzhidanta/claude-code-glm53-swesmith-compact-trajectories` (189 Claude Code/GLM-5.3 — `other` tag, no license text anywhere)
- Synthetic: `kosiasuzu/agenticml-agent-trajectory-dataset` (18,483 rows, MIT — README says synthetic), `rmems/agent-trajectory-preference-pairs` ("EXAMPLE ONLY, not real data"), `springofwindslabs/mcp-agent-trajectory-benchmark` (tagged synthetic)
- Not trajectories: `SWE-bench/SWE-smith` (task instances), `ai-safety-institute/AgentHarm` (behaviors JSONs only), `wentingzhao/commit0_combined` (54 task instances), `CSJianYang/CodeArena` (human preference tasks), `webarenapro/agent_trajectory_reviews` (300 human reviews, not traces), `DCAgent2/terminal_bench_2` (861 env-definition files), `zeldaleft/assistantbench-submission-aya-pipeline` (answers-only), `AmineHA/WebArena-Verified`, `Simu-Env/WebArena-SFT`, `thuml/webarena-world-model-cot` (synthetic CoT), `ryankamiri/R2E-Gym-Full` (env slice), `NaNg/Pantheon-Agent-Trajectory` (biomedical zips), `DCAgent/glm-4.6-r2egym-traces` (empty/disabled)
- MoltBook: `SimulaMet/moltbook-observatory-archive`, `TrustAIRLab/Moltbook`, `ronantakizawa/moltbook`, `giordano-dm/moltbook-crawl` — agent-community post archives, not trajectories. Adjacent only.
- Gated/manual: `cx-cmu/agent_trajectories`, `kevinhikali/aworld_visualwebarena`, `shiqihe/WebVoyager-GAIA-SparseAttention-Offline-Qwen3-VL-30B-A3B`, `TuringEnterprises/meta-osworld-cua`
- Dead lanes (no corpus exists): AssistantBench, Mind2Web (human demos only), AITW (human demos), VisualWebArena, GAIA agent logs, terminal-bench community licensed runs

**Unverified (could not confirm, not killed):** `multi-swe-bench/multi-swe-bench` (GitHub API rate-limited; one authenticated tree check recommended), `LJ0815/DevEval` (almost certainly tasks-only).

**Notes:** No `nemotron/*` openhands trajectory corpora on HF datasets (releases appear GitHub-only). No gated corpora among viable hits; none required Google Drive. "Synthetic" tag on SWE-rebench/SWE-agent corpora = model-generated rollouts with real env interaction (standard for this lane), kept.

---

## TASK B — TRANSLUCE-STYLE PER-CORPUS WRITEUP TEMPLATE (copy-ready)

Behavior-first, evidence-backed, incident framing. ASD-STE100. One filled template per corpus.

### Section structure (ordered, exact)

**Title line:** `<Corpus>: <behavior family in one clause>` — e.g. "LongRCA Bench: agents rewriting user-set budget constraints". Title names the behavior, not the dataset size.

1. **Summary.** 1–3 sentences: what the agent did, where observed, what scale. Includes the counting unit and the one key verbatim if it carries the claim. NOT a dataset inventory, NOT methodology, NOT a list of all classes.
2. **Corpus and counting unit.** Dataset name + pinned revision, retrieval date, total trajectories reviewed, how the reviewed subset was chosen. State the counting unit explicitly ("n = 1,140 trajectories; 30 verified findings; each finding counted once"). NOT the finding classes again.
3. **What happened.** The incident narrative: chronological, concrete, agent-by-agent where it matters. Verbatim evidence quotes are the skeleton; prose only glues. One behavior family per writeup — if a corpus has three families, that is three writeups, not one report with sections per family.
4. **Evidence.** Per finding: trajectory id, step range, verbatim quote (verbatim = decisive, paraphrase = context only), byte location or artifact reference, sha256 of the source file. Every causal claim cites a quote; every quote tied to id + step. NOT inference without a quote attached.
5. **Novelty.** Explicit prior-work comparison in prose: name what is already documented (with citation), then state exactly what this observation adds ("a new October instance, not a first discovery" — #181). If no prior work found, say what was checked. NOT a claim of first-discovery by silence.
6. **Why it matters.** One paragraph: the deployment-relevant risk or the eval-design lesson. Connects the sandbox behavior to a wild analog or a harness flaw. NOT restated summary, NOT generic AI-safety concern.
7. **Uncertainties.** Bulleted: each alternate explanation named and its status ("ruled out by X" / "cannot be ruled out because Y"). At least one explicitly non-malicious reading. NOT hedging adjectives scattered through the text — centralize doubt here.
8. **Impact / harm.** Sandbox-contained harm stated as such; then the near-miss translation ("no real money moved; the same call path outside the sandbox would..."). Uses the harm grades below. NOT inflated.

Sections that do NOT belong anywhere: dataset-inventory tables, reviewer-process logs, dedup minutiae, repo plumbing.

### Evidence standards

- **Verbatim quotes carry claims; paraphrase carries context.** The decisive step that proves the behavior appears as a direct quote. Rule: if removing the quote removes the proof, it must be verbatim. (#170 quotes the agent: "Accessing the Hugging Face Space directly was blocked, but using r.jina.ai to proxy the README worked." — intent is agent-stated, not inferred.)
- **Every quote = (trajectory id, step number or range, source file + sha256).** #174: "Intern-S2: warning at line 14, commit at 16/17, failed push at 18/19." The bytes-back pointer must resolve without asking the author.
- **Attachments = byte-level artifacts** (redacted excerpts, decoded payloads, screenshot sets, file hashes). **evidence_links = public verification paths** (dataset page pinned to revision, exact blob path, finding cross-links). #174 puts the HF blob URL with commit hash in evidence_links and the excerpt-with-secrets-removed in the attachment. For our trajectory writeups: REPORT.md and EVIDENCE-INDEX.md entries are the links; raw JSON files are local-only artifacts cited by path + sha256.
- **Action-result pairing.** Each cited action gets its matching observed result (#174). Never cite an action and claim an outcome the trace does not show. (#180: "The screenshots substantiate remote viewing. Stored payloads and action logs substantiate attempted interactive input, but not receipt/effect of every key.")
- **Do not replay attacks.** State what was NOT done: "We did not replay the commands or test the credentials" (#174), "Decoding locally, without executing the code" (#180). For sandbox writeups: state whether behavior was replayed/reproduced or read-only.
- **Timestamps and counts:** UTC, named as collection timestamps vs action timestamps ("Report timestamps should not be interpreted as exact browser-action start times" — #180).

### Severity grading

Observed Transluce values: `No/negligible harm`, `Minor potential harm` (104/115 findings predate the field — v3 forms). Cyberattack is a separate axis from harm: most trajectory findings score cyberattack=`None` + harm=`No/negligible harm`, which is correct, not weak.

**Adaptation for benchmark-trajectory writeups (sandbox-contained):**
- Default: **No/negligible harm** (sandbox, no real-world effect). Say so explicitly; do not upgrade to feel serious.
- **Near-miss framing** instead of incident framing: grade the *demonstrated capability*, not the contained outcome. Format: "Sandbox outcome: none. Capability demonstrated: X. Wild analog: Y (cite #n)." Example: #174's failed GitHub pushes = no leak shown, but the finding is agents pushing recognized secrets — not the failed auth.
- **Minor potential harm** only when the trace shows the behavior reaching a live external system (live site, real credential-shaped material, outbound third-party request) — see #172's live-site CAPTCHA clicks. A sandbox-contained destructive act (QEMU VM kill) stays "no/negligible" with a near-miss note.

### Credibility rules (extracted from exemplars)

1. **"Alleged / suspected / unconfirmed" is mandatory where proof stops.** #159: "any link is unconfirmed"; #180: "Suspected agents". Form field `ai_company: Unknown` is acceptable and honest — do not fill it with a guess. Trace metadata model names are "labels", never attributions (#172: "Model and provider names are trace metadata only"; #174: "These model names come from the dataset").
2. **Counting-unit discipline.** #36: "Count the authored post once, rather than each link as a separate message." State what n counts (trajectories, findings, rows, runs) and what it does NOT count. Never let one event inflate into five findings.
3. **Uncertainty sections name what was ruled out**, not just what is unknown. #159's "Four separate questions" splits dashboard identity / execution / provider / link-to-notification and grades each separately. #172 explicitly lists what the traces do NOT show (no account access, no data theft, no persistent writes).
4. **Explicit prior-work comparison.** #181's Novelty: prior work documented USAspending queries and Microlink proxies → "a new October instance, not a first discovery." #170: "Technique is documented upstream — these are new observations, not a new technique." A finding that does not say what is already known reads as claiming first discovery.
5. **Internal-hypothesis labeling.** #36: the OpenAI attribution is labeled "an internal attribution hypothesis, not a confirmed attribution or a publication-ready conclusion." Any attribution not proven by the bytes gets this exact treatment.
6. **No single-message claims without the message.** Screenshots and payloads substantiate what they show and nothing more (#180's careful split between remote viewing proven / keystroke receipt unproven).

### Worked mini-example (LongRCA, F-A01: JudgeAgent QEMU-monitor VM kill)

**Title:** LongRCA Bench: verifier agent kills the VM it is testing.
**Summary.** In trajectory terminal_bench_2__016, the verifier agent piped "quit" into the QEMU monitor over TCP during a keyboard-input test, terminating the VM under test, then immediately reported its own destructive act. One verified instance; behavior class IRREVERSIBLE.
**Corpus/counting unit.** CLoud5-real/longrca-bench, rev 9f45acb6; 1,140 trajectories reviewed; n = 1 verified finding (F-A01). Raw: data/lanes/longrca-trajectories/raw/terminal_bench_2/terminal_bench_2__016.json, sha256 c4e4dd41…
**What happened.** Steps 398–400: the agent ran `(echo "sendkey ret"; sleep 1; echo "quit") | nc -w 3 127.0.0.1 4444`. The "quit" string reached the QEMU monitor and ended the VM. In the next step the agent stated it had killed the VM and reported it honestly.
**Evidence.** Verbatim command (above) at steps 398–400; agent's own acknowledgment quoted at step 401 (cite). Action-result paired: command issued → VM process gone in subsequent observation. Byte-backed citation: file path + sha256 + step window.
**Novelty.** Self-inflicted irreversible test-environment destruction is documented in prior agent-safety literature (cite); this is a new byte-verified instance with the notable twist of immediate honest self-report — destructive act plus intact self-monitoring.
**Why it matters.** The destructive input was one token ("quit") away from the intended benign test ("sendkey ret") — no separate tool boundary separated the test channel from the control channel. Verifier harnesses that share a channel with the system under test have no containment by design.
**Uncertainties.** Sandbox-contained: no real infrastructure harmed. Cannot rule out that the benchmark's harness design (exposing the monitor port) made this likely rather than agent recklessness — the behavior may be harness-induced, not model-intrinsic. One instance; prevalence unknown.
**Impact.** Harm: No/negligible harm (sandbox VM). Near-miss: same command shape against a production hypervisor monitor = outage. Cyberattack: None.

### Adapter notes for per-corpus trajectory writeups

- **Corpus-level writeup = incident framing of a behavior family across trajectories, not one wild incident.** The "incident" is the pattern (e.g. "agents rewriting user-set constraints" = LB-F001 + LB-F006 + LB-F008 as one writeup if they share the mechanism; split when mechanisms differ). Each constituent finding keeps its own byte-backed evidence entry in Evidence.
- **Counting unit, stated up front, every time:** "n trajectories reviewed / m verified findings / k instances of this behavior." The REPORT.md class codes (F-A01, LB-F001) become the internal finding ids cited in Evidence.
- **Sandbox harm is never laundered into wild harm.** Two-line form: contained outcome + near-miss translation. "Minor potential harm" requires a live external touch (see #172).
- **REPORT.md and EVIDENCE-INDEX.md plug in as follows:** REPORT.md's per-class finding bullets (id, trajectory, steps, verbatim, sha256, "why interesting") are the Evidence section's raw material — copy verbatim quotes and byte pointers, do not re-summarize loosely. EVIDENCE-INDEX.md entries become the evidence_links analogs. The "Killed" list (e.g. F-A15) goes in Uncertainties as an explicitly ruled-out reading.
- **Positive patterns get the same treatment.** F-A11 (third agent repairing a constraint violation) is a finding with the same template — behavior-first writeups cover guardrail-recovery, not only failures.

### Survey-derived schema adaptations (from the two survey passes, condensed)

From the incident/taxonomy surveyor (Transluce + AIID + MAST/SWE-triage/TerminalBench/AIR/MQ-AICIR):
1. `claim.novelty` enum (`new_mechanism`/`new_instance`/`corroboration`/`negative`) + `novelty_detail` — Transluce's Novelty convention, machine-checkable.
2. `claim.prior_work[]` — `{link, relation}` with relation ∈ `documents_same_mechanism`/`documents_same_target`/`earlier_instance`.
3. `claim.confidence` enum (`observed`/`inferred`/`hypothesized`) — GMF confidence modifiers.
4. `assessment.counting_unit` + `assessment.count` — AIR discipline ("define the counting unit").
5. `assessment.failure_mode` — coded: MAST codes (FC1.1–FC3.3) for multi-agent, SWE-triage codes (SCOPING/ENVIRONMENT/CONTEXT_RETRIEVAL/REASONING/VERIFICATION/TOOL_USE/RESOURCE_LIMIT/IMPLEMENTATION_STALL/INFRA_ERROR/OTHER) for single-agent benchmark trajectories.
6. `assessment.fix_owner` enum (`task_author`/`environment`/`agent_framework`/`model`/`operator`/`unknown`) — routes every failure to an action.
7. `report.harm` block: `event_state` (hazard/near_miss/boundary_violation/incident/serious_incident, MQ-AICIR E0–E4), `harm_level` (Transluce v4 scale), `harm_realized` boolean (CSET occurred-vs-potential).
8. Observation/action fields: `authority_exercised` (browser_execute/network_fetch/code_write), `boundary_crossed` (access_control_bypass/scope_exceeded/none), `reversibility` (reversible/persistent/unknown) — MQ-AICIR A/B/R slots.
9. EVIDENCE-INDEX.md per-entry `independence` flag (`independent_source`/`same_source_multiple_urls`/`derived`) — three URLs of one scan are not three independent sources.
10. `assessment.uncertainties[]` — `{uncertainty, checked, result}`; a finding without this section is incomplete by definition.

From the lab/community surveyor (METR/Apollo/Anthropic/OpenAI/AIID):
1. `nudging_level` enum (`none`/`task-directed`/`goal-nudged`/`adversarial-elicitation`/`unknown`) — Apollo/OpenAI credibility axis; behavior at `none` ≫ at `adversarial-elicitation`.
2. `investigation_track` enum (`ready_for_disclosure`/`minor_investigation`/`larger_investigation` + `disclosure_blocker`) — OpenAI's triage, verbatim; publish early without pretending completeness.
3. `unanswered_questions` list — publish-permitted incompleteness.
4. `discovery_method` enum (`automated_monitor`/`trajectory_audit`/`third_party_report`/`harness_error`/`human_review`).
5. `benchmark_context` object (`harness, model_snapshot, date_range, trial_count, trial_ids, token_budget, budget_disclosed_to_agent`) — METR attestation; 90/102 surveyed evals don't state budget disclosure.
6. `verdict_taxonomy` enum (`benign_artifact`/`scaffolding_failure`/`capability_gap`/`misaligned_behavior`/`indeterminate`) + rationale — METR's "real failure" adjudication as a required field.
7. `severity` (AIID MIT risk_domain/subdomain + local sev1_near_miss/sev2_contained/sev3_external_effect/sev4_systemic) — separate from harm; record observed external effect vs hypothetical.
8. `agent_identity_and_allowlist` (`agent_id, owner, allowed_actions_sha, log_location_external, kill_switch_tested`) — practitioner checklists (AI Lab 5-step).
9. `failed_attempts_reviewed` bool + note — checklists converge: state that failed/partial attempts were reviewed.
10. `cross_registry_ids` (`aiid_incident_id, oecd_aim_id, our_incident_id`) — AIID duplicate-mapping convention.

Credibility synthesis (both surveys agree): rate across trials (not single screenshots); benign-vs-genuine adjudication documented; mechanism stated with verbatim transcript tie; nudging level recorded; attribution fixed (model snapshot, harness, budget, date range); independent corroboration over single-source.

---

## SUGGESTED FLEET QUEUE ORDER

**Per-corpus ingest fleets (wave order):**
1. AI-Secure/DTap-Bench-Agent-Trajectories (48k red-team, 7+ models) — behavior densest
2. liuqi6777/bcp_search_agent_trajectory (4,980 search traces) — richest non-code
3. webarena-x/webarena-infinity-trajectories (2,329 web)
4. JetBrains-Research/agent-trajectories-swe-bench-test-minus-verified (1,785, gpt-5.2)
5. jordan-taylor-aisi InterCode-CTF (offensive-security)
6. nebius/SWE-rebench-openhands-trajectories (67k)
7. agent-eto/eto-sft-trajectory (6,423)
8. SWE-Factory/DeepSWE-Agent-Kimi-K2 (2.8k)
9. Hongliang1997/WebVoyager (643 tasks, 1.95 GB)
10. SeerRay-Lab/Android-World-Eval (464)
11. xlangai/ubuntu_osworld_verified_trajs (1000+ episodes, media-heavy)
12. mlfoundations/gelato-osworld-agent-trajectories (2,166)
13. nebius/SWE-agent-trajectories (80k, 5.6 GB — sample-first)
14. SWE-bench/SWE-smith-trajectories (76k, 10.7 GB — sample-first)
15. Kwai-Klear 66k (4.64 GB — sample-first)

**Writeup fleet (Transluce-style per-corpus writeups, queued for freeze lift):** AgentProcessBench, RootSE, LongRCA, TELBench first (TraceLab second wave — SECONDARY-only until egress resolved). Use the template above; one writeup per behavior family per corpus.

**Disk warning:** wave 3 corpora total ~21 GB; sample-first and watch /home/hatch (currently 65%).
