# BetterWright agent-traces — audit for Transluce finding #172

Audited: 2026-10-08. Auditor: Muse (subagent lane, silent-locus `transluce` branch).
Scope: Transluce finding #172 (filed by aj2, 2026-10-08T05:47:05Z) —
"BetterWright traces show DeepSeek and Qwen agents reaching live site content
after bot-check clicks."

## 1. Dataset identity

- HuggingFace: `ProCreations/betterwright-agent-traces`, rev `7e81937f8d968b61fafeb942cfc1f6079a813807`
- License: apache-2.0. Built 2026-09-22T04:46:34Z.
- Contents: full agent trajectories recorded inside the BetterWright harness
  v2.8.7 (`runAgentTask`, the same loop as `betterwright exec`). Two open models
  drove a real headless BetterChromium browser against the live web.
- Files: 26. Total bytes: 178,078,720 (~178 MB).
- Rows: 3,840 (the `accepted` subset only: harness reported `done` without
  abort/length-stop AND an LLM judge scored success >= 4, grounded, not
  fabricated). Rejected runs were not published.
- Columns: 52. Key columns: `id`, `task_id`, `task`, `tier`, `site_mode`,
  `category`, `sites`, `model`, `reasoning_effort`, `system_prompt`,
  `messages` (full OpenAI-format conversation incl. `reasoning_content` and
  tool_calls), `transcript` (harness-native JSON), `browser_steps`,
  `final_answer`, `judge_*`, `accepted`, `finished_at`.

### Rows by model and reasoning effort

| model | high | low | medium | none | xhigh | total |
|---|---:|---:|---:|---:|---:|---:|
| DeepSeek-V4.1-Flash | 689 | 681 | 688 | 664 | — | 2,722 |
| Qwen3.8-Flash-Next | — | 266 | 279 | 277 | 296 | 1,118 |
| **Total** | | | | | | **3,840** |

DeepSeek ran via Hugging Face Inference Providers (DeepInfra primary).
Qwen ran locally on one RTX PRO 6000 via SGLang. Tasks were synthesized from
~190 real websites; site modes: `read` (live public sites), `sandbox`
(practice sites), `tool` (account-free web apps).

## 2. How the harness handles bot-checks (OBSERVED)

The BetterWright harness ships an automated bot-check solver and actively
detects and routes agents through bot protection. Three mechanisms appear in
the data (verbatim quotes below).

### 2a. Detection: the harness flags `bot_challenge` itself (OBSERVED)

Tool results returned to the agent contain a structured `challenges` block.
Example, from trace `deepseek-high-019e97f136-muav4494c2` on microcenter.com:

    "challenges":[{"pageId":"page-2","type":"bot_challenge","provider":"turnstile",
    "url":"https://www.microcenter.com/search/search_results.aspx?Ntt=Ryzen+7+9700X",
    "challengeUrl":"https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/g/turnstile/f/av0/rch/7jy77/0x4AAAAAAAAjq6WYeRDKmebM/dark/fbE/new/normal?lang=auto",
    "detectedIn":"frame","signal":"turnstile_frame_url",
    "solve":{"maxAttempts":3,"resumeOnClear":true,
    "helpers":["captcha.solve","captcha.detect","captcha.inspect","captcha.click",
    "captcha.drag","captcha.readText","captcha.clickTiles","human.click"]},

193 traces have the harness emit a `bot_challenge` detection in the transcript
(128 DeepSeek, 65 Qwen). (OBSERVED)

### 2b. The challenge page tells the agent to solve it (OBSERVED)

Every challenge block carries this advice, shown to the agent verbatim:

    "A bot challenge is blocking this page. Preserve this page and solve it
    before retrying the blocked action. Prefer `captcha.solve()` for local
    automatic checkbox, Turnstile, managed-challenge, and slider stages (no
    external APIs). If solve returns status `processing` with a vision
    artifact (image grid or text), open the attached numbered crop, pick
    matching tile indexes, then call `captcha.solve({ tiles: [indexes] })`.
    Fall back to `captcha.inspect`, `captcha.click`, `captcha.drag`,
    `captcha.readText`, `captcha.clickTiles`, or `human.click` when needed."

The harness system prompt reinforces it, also verbatim:

    "Use local `captcha.solve()`. `processing` is not solved: open the numbered
    crop, pick indexes, then `captcha.solve({tiles:[...]})`. Replacement photo
    grids are the same stage — keep picking; hand off after rejection instead
    of repeating, or after three distinct stages. Verify clearance; replay only
    an idempotent/visibly incomplete action, never a submission, purchase,
    or message."

(OBSERVED — both strings are byte-identical across traces.)

### 2c. Agents execute the solver; the harness clicks the widget (OBSERVED)

192 accepted traces contain an agent-authored `browser` tool call whose code
executes `captcha.solve(...)` (assistant role, tool_call arguments —
136 DeepSeek, 56 Qwen). In 141 of those 192 (102 DeepSeek, 39 Qwen) a
subsequent tool result records `"cleared":true` (or equivalently
`"status":"ready"`), i.e. the harness reports the bot-check as cleared.

## 3. Bypass moments — verbatim (OBSERVED)

### Bypass A — DeepSeek-V4.1-Flash, microcenter.com, Cloudflare Turnstile

Trace `deepseek-high-019e97f136-muav4494c2` (effort `high`, task: mid-range CPU
pricing research, finished 2026-09-22).

1. The agent opened a Micro Center CPU search page. The harness returned the
   `bot_challenge` block (2a above) with `signal: turnstile_frame_url`.
2. The agent's reasoning: "Let me try captcha.solve()." Tool call (note shown
   by the agent): "Attempting local captcha solve for Cloudflare Turnstile".
   Code: `const res = await captcha.solve();`
3. Harness result: `"provider":"turnstile","stage":"turnstile","cleared":false`
   on the first attempt, with logged attempts
   `{"action":"click_checkbox","description":"Click the Turnstile widget","ok":true,...}`
   then two `wait_token` waits (ok:true). On retry against a fresh page the
   result was `"solveStatus":"ready","cleared":true`.
4. The agent then loaded real Micro Center pages and extracted live product
   data, e.g. `"title":"Intel Core Ultra 7 265K Arrow Lake Twenty-Core LGA 1851
   Boxed Processor - Heatsink Not Included"` with live prices
   (`"$129.99","$114.99","$109.99","$289.99"`), and "AMD Ryzen 7 9700X ...
   Current price: **$269.99** ... in stock — 17 units at Columbus".
   Judge verdict: success, score 4.

(OBSERVED — all strings above are byte-verbatim from the trace.)

### Bypass B — Qwen3.8-Flash-Next, microcenter.com, Cloudflare Turnstile

Trace `qwen-low-23fbc36541-muaxl47wjh` (effort `low`, task: high-school
hardware-lab planning).

1. Tool call note (agent-authored): "Solving Micro Center Cloudflare
   Turnstile". Code: `await captcha.solve();`
2. Harness result, verbatim:
   `"status":"ready","request":"bw_muaxm9ep_e5t7mv","provider":"turnstile",
   "stage":"turnstile","cleared":true,...`
   `"attempts":[{"stageIndex":0,"stage":"turnstile","provider":"turnstile",
   "action":"click_checkbox","description":"Click the Turnstile widget",
   "ok":true,...,"target":"frame_element",...}]`
   `"challenge":{...,"url":"https://www.microcenter.com/search/search_results.aspx?searchterm=Raspberry+Pi+5",
   "challengeUrl":"https://challenges.cloudflare.com/.../rch/5s1zv/...",...}`
3. The agent continued to Micro Center catalog content (Raspberry Pi 5 search
   results) and reported them in the final answer. Judge verdict: success,
   score 4.

(OBSERVED — all strings above are byte-verbatim from the trace.)

### Bot-check encounters the agents did NOT solve (OBSERVED, for balance)

Not every encounter ends in a solve. Trace
`deepseek-medium-3fd41f1434-mubyt3af3ck` hit three gates in one run and
worked around them instead:

- DuckDuckGo: "Unfortunately, bots use DuckDuckGo too. Please complete the
  following challenge to confirm this search was made by a human. Select all
  squares containing a duck"
- mojeek.com: page titled "Captcha" — "Verification required. Please complete
  the challenge to continue. I'm not a robot. Protected by ALTCHA. Waiting
  for verification." (the harness exposed a control with label
  "I'm not a robot", actions ["check","read"], checked:false — the agent did
  not check it)
- searx.be: "Automated verification failed. ... Checking your browser"

The agent abandoned those pages and got its data from an alternative engine
(priv.au via dogpile). This shows routing-around, not a solved challenge, at
those three gates. (OBSERVED)

## 4. Grades

- OBSERVED: the harness (a) detects bot challenges and labels them
  `bot_challenge`/`turnstile`, (b) advises the agent to solve them with
  `captcha.solve()`, and (c) carries out widget clicks itself. In 192 accepted
  traces the agent chose to run the solver; in 141 the harness reported the
  gate cleared. Two traces (one DeepSeek, one Qwen, both microcenter.com
  Cloudflare Turnstile) show the complete sequence: challenge → agent solve
  call → harness clicks Turnstile widget → `cleared:true` → live site content
  extracted and judge-accepted.
- INFERENCE: aj2's finding #172 claim is supported by this dataset. The
  bypass is harness-assisted (the harness, not the raw model weights, contains
  the Turnstile widget-clicking machinery), and it is limited to bot gates the
  harness's local solver can clear — some gates (ALTCHA checkbox,
  DuckDuckGo image challenge, searx.be) were not solved in the observed traces.
- OBSERVED: every trace in this release is the `accepted` subset, so all
  counted traces ended with a judge score >= 4, grounded, not fabricated.
  Rejected (failed) runs were not published, so a true bypass success rate
  cannot be computed from this release.

## 5. Method note

Audit was done by script against the 10 parquet files: bot-check evidence was
counted only when an assistant-role tool_call (not system-prompt or advice
prose) contained `captcha.solve(`. The two exemplar traces were read
message-by-message. No PII was found in the audited excerpts; the dataset
contains public web page text only (images omitted).

## 6. Row/file counts (summary)

- Files: 26. Bytes: 178,078,720 (~178 MB).
- Rows: 3,840 (DeepSeek 2,722; Qwen 3.8-Flash-Next 1,118).
- Traces with harness `bot_challenge` detection: 193 (128 DeepSeek, 65 Qwen).
- Traces with agent-executed `captcha.solve()`: 192 (136 DeepSeek, 56 Qwen).
- Of those, tool result shows cleared/ready: 141 (102 DeepSeek, 39 Qwen).
