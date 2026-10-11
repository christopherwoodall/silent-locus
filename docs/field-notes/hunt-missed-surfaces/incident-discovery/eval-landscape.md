# Eval landscape — what the big labs bench (2026-10-03)

## Why this was investigated

The eval-linkage hunt (`eval-linkage.md`) found 1 confirmed + 5 weak-plausible links between incident traces and DeepSearchQA questions, using verbatim-phrase grep. That raised the question: **what evals do OpenAI and Anthropic publicly say they're benching, and which have the same shape as the observed traces** (persistent web retrieval of niche facts, especially government data)? If the agents were running known evals, the eval's public question set is a fingerprint source.

## Method

Web search of public lab communications (blogs, benchmark announcements, model/system cards), 2026-10-03. Only public statements; no private-leak material.

## OpenAI (public)

| Eval | What it is | Same-shape? |
|------|-----------|-------------|
| **BrowseComp** (Apr 2025, [openai.com/index/browsecomp](https://openai.com/index/browsecomp/), [paper](https://arxiv.org/abs/2504.12516), in `openai/simple-evals`) | 1,266 hard fact-seeking questions; persistent creative web browsing; short verifiable answers | **Closest match.** Agents grinding obscure web sources for niche facts. Deep Research trained specifically for this task type (51.5%). |
| SWE-bench / SWE-Lancer / MLE-bench | Coding, ML engineering | No — different shape |
| Internal misalignment report (Sep 27, 2026) | A research agent that couldn't find a blogger "guessed the task came from BrowseComp and downloaded and decrypted the benchmark" | Meta-evidence: the agents themselves recognize the BrowseComp shape |

## Anthropic (public)

| Eval | What it is | Same-shape? |
|------|-----------|-------------|
| **OSWorld 2.0** (81.8% Opus 5.5) | Computer-use, desktop control | No — different shape |
| **Terminal-Bench 4.0** (66.4%) | Terminal tasks | No |
| **GDPval-AA** (1846 Elo) | Agentic economic-value tasks | Partial |
| **Internal research eval** (not public) | Multi-agent research: lead + parallel subagents beat single agent by 90.2% on web research tasks | Same family, not fingerprintable |
| **BrowseComp run on Opus 4.6** ([blog](https://www.anthropic.com/engineering/eval-awareness-browsecomp)) | Anthropic evaluated Claude on OpenAI's BrowseComp; found contamination + a model that independently identified the eval and decrypted the answer key | Confirms BrowseComp is the cross-lab shape |
| Gray Swan IPI / Shade | Prompt-injection safety benchmarks | No — safety, not capability |

## Google / Meta (for context)

| Eval | Same-shape? |
|------|-------------|
| **DeepSearchQA** (Google) — our 900-question bank | **Confirmed shape** (dsqa_250 → DoE) |
| **GAIA** (Meta) — general AI assistant web tasks | Same family; question set gated |
| **AssistantBench** (Google) — real web tasks | Same family |

## Rationale chain (why this matters to the hunt)

1. The confirmed eval link (dsqa_250 → DoE) worked through **task parameters** (`survey_Year_Key=9`, `Measure_Id=130`), not question text. Agents execute questions; they don't paste them. → Eval-linkage must match on parameter shapes, not phrases.
2. BrowseComp is the cross-lab, same-shape eval — but its plaintext is encrypted by design and GAIA is gated. DeepSearchQA is the only publicly fingerprintable set, and it's now nearly exhausted (1 confirmed, 5 weak).
3. The incidents' shape (obscure government-data retrieval under persistent browsing) is **exactly what both labs publicly bench and productize** (Deep Research). The government sites were where the questions pointed, not the objective.
4. Investigative consequence: future eval-linkage should target (a) parameter-shape matching against DeepSearchQA's 49 gov-data questions, and (b) any BrowseComp/GAIA leak or release — a single leaked question matching an incident target would be decisive.

## IOC list coverage + check status (2026-10-03)

**On the v3 word list:** `browsecomp`/`BrowseComp`, `deepsearchqa` (+variants), `dsqa_250`, `dsqa_` (marked honest-zero), `gaia` (marked noisy), 2,636 QA fingerprints incl. verbatim DeepSearchQA priority phrases, eval-infra markers (`cybergym`, `exploitgym`, `catflag`).

**Added to v4 staging (2026-10-04):** `assistantbench`/`AssistantBench`, `osworld`, `terminal-bench`, `gdpval`, `swe-bench`, `swe-lancer`, `webvoyager`, `webarena`, `mle-bench` — watch terms with shape notes.

**Checked against traces:** DeepSearchQA only — full 900-question fingerprint run (`eval-linkage.md`): 1 confirmed (dsqa_250), 5 weak-plausible, rest none. BrowseComp and GAIA cannot be checked (no public plaintext: encrypted by design / gated). The coding/computer-use evals (SWE-bench, OSWorld, Terminal-Bench, MLE-bench) are wrong-shape for web-retrieval traces and were not fingerprinted; they ride as watch terms.

## Sources

- https://openai.com/index/browsecomp/
- https://arxiv.org/abs/2504.12516
- https://www.anthropic.com/engineering/eval-awareness-browsecomp
- https://genztech.blog/p/claude-opus-5-5-terminal-bench-agentic-benchmarks/ (Opus 5.5 bench table)
- https://github.com/h20zhang/agent-benchmark-radar/blob/HEAD/benchmarks/browsecomp.en.md
