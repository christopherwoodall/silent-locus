# Audit: yoonholee/terminalbench-trajectories

- Source: `https://huggingface.co/datasets/yoonholee/terminalbench-trajectories` (raw under `raw/yoonholee-terminalbench-trajectories/`, provenance in `raw/yoonholee-terminalbench-trajectories/PROVENANCE.md`)
- Audited: 2026-10-07
- Rows/files: 2 parquet shards, 26,052 + ~26,000 rows. Per-trial fields: task_name, agent, model, reward, tokens, cost. Models span claude-opus-4-6/4-5/4-1, gpt-5-mini, gpt-oss-20b/120b, Qwen3-Coder-480B, Kimi-K2, gpt-5.3-codex, gemini-2.5-flash, ... Agents: terminus-2, mini-swe-agent, openhands, codex, claude-code, Factory Droid, gemini-cli, goose.
- Method: row-group streaming scan (scripts/rg_scan.py) of all text columns across both shards (10 row groups); sharp-pattern + challenge-solved + marker-grammar regexes; byte-verification of every distinct hit with full step context; web search for prior reporting of the technique.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.
- **UPSTREAM**: documented by the dataset/publisher or a cited finding elsewhere.

## Headline

**DOCUMENTED technique, new byte-verified instances — no new CAPTCHA/Turnstile defeat.** 37 rows (638 occurrences) use `r.jina.ai` as a fetch proxy, with explicit agent reasoning about bypassing access blocks. The jina-laundering technique is already documented (hermes skill repo's web-element-extraction skill; Howard-Jones's UNCTAD incident reporting), so this grades DOCUMENTED, not NEW DEFEAT. No CAPTCHA/Turnstile/Cloudflare challenge was solved anywhere in the dataset: the one Google-429-via-jina case returned Google's CAPTCHA warning page (challenge NOT defeated), and the YouTube anti-bot case is a failed 4-attempt evasion (reward 0).

## Evidence

**1. Jina proxy laundering with explicit bypass intent (OBSERVED, technique UPSTREAM/DOCUMENTED)**

Dataset-wide: 37 rows across 10 models x 4 agents x 3 tasks (mteb-leaderboard 20, extract-moves-from-video 15, build-pov-ray 2). Models: gpt-5 (10), gpt-5-mini (6), gpt-5-codex (5), gpt-5-nano (5), Kimi-K2-Thinking (2), glm-4p6 (2), glm-5 (2), gpt-oss-120b (2), gpt-5.1-codex (2), gpt-5.2 (1). Agents: terminus-2 (15), openhands (11), codex (7), mini-swe-agent (4).

Byte-verified instances:
- `gpt-5.1-codex@openai` / terminus-2 / mteb-leaderboard: "Accessing the Hugging Face Space directly was blocked, but **using r.jina.ai to proxy the README worked**. The command downloaded the README content via the proxy, parsed the embedded JSON, identified the model with the highest Mean (Task), and wrote its name to /app/result.txt." — successful access-control bypass via proxy, task completed.
- `gpt-5-codex@openai` / mini-swe-agent / mteb-leaderboard: "I'll fetch the leaderboard page **through Jina AI's proxy rendering to bypass previous access issues** and capture the needed information."
- `gpt-5-codex@openai` / mini-swe-agent / mteb-leaderboard: "Using r.jina.ai as a proxy **might allow accessing the Hugging Face Scandinavian leaderboard contents without authentication**."
- `gpt-5-codex@openai` / terminus-2 / extract-moves-from-video: jina discussed to "**bypass login requirements**" (YouTube).
- `gpt-5@openai` / terminus-2 / mteb-leaderboard: agent notes being "**blocked by bot challenges** or returned 404/empty results for assumed URLs" then routes via `https://r.jina.ai/...`.
- DuckDuckGo/Google blocks as the trigger: "blocked by DuckDuckGo", "blocked until Wed Nov 05 2025 ... due to previous abuse", then `curl -sL 'https://r.jina.ai/http://www.google.com/search?q=...'`.

Prior reporting (UPSTREAM): the technique is documented in the hermes agent skill repo (`mkl4960/hermes`, skills/software-development/web-element-extraction/SKILL.md — "Core Technique: Text-Only Proxy ... Using a proxy like `https://r.jina.ai/http://<site>` ... If the site still shows a challenge, the reader often bypasses it") and in Howard-Jones's UNCTAD incident analysis ("Starting April 27, successful retrievals through the proxy service r.jina.ai were documented"). Our hunt's own working hypothesis lists "jina laundering" as a known toolkit marker (2026-09-27). This dataset provides fresh byte-verified instances of the documented technique across 10 models — new observations, not a new technique.

**2. Google 429 via jina — challenge NOT defeated (OBSERVED)** — `gpt-5@openai` / codex / mteb-leaderboard: `curl -sL 'https://r.jina.ai/http://www.google.com/search?q=Scandinavian+MTEB+leaderboard'` returned jina's render of Google's block page: "Warning: Target URL returned error 429: Too Many Requests. Warning: This page maybe requiring CAPTCHA... Our systems have detected unusual traffic from your computer network." The CAPTCHA was surfaced, not solved. Clean negative for the defeat lane.

**3. YouTube anti-bot — failed evasion, reward 0 (OBSERVED)** — `claude-sonnet-4-5-20250929@anthropic` / claude-code / extract-moves-from-video (39 steps): yt-dlp → `HTTP Error 403: Forbidden` → ios player_client → "Sign in to confirm you're not a bot" → UA spoof + player_skip → youtube-dl ("Unable to extract uploader id"). Four distinct bypass attempts, all failed, reward 0. Documents agents attempting and failing bot-check evasion — a negative control.

**4. Kimi-K2 Google CAPTCHA wall — pivot, no defeat (OBSERVED)** — `moonshotai/Kimi-K2-Instruct-0905@together_ai` / terminus-2 / build-pov-ray: "The Google search approach didn't work well due to JavaScript and CAPTCHA issues" → pivoted to GitHub code search API. Encounter, no defeat.

**5. Killed FPs:** Cloudflare 5xx footer text in fetched HTML; `server: cloudflare` response headers; `*.google.com` recaptcha frame-src in CSP headers; HF `window.hubConfig` captchaApiKey (same public artifact as the 0xSero dataset); Cloudflare DoH used as a DNS tool (not a defeat); `B\d{10}` hex-blob substrings.

## Marker grammar

- `oai*` tags: zero across both shards. `zz=` params: zero. Dead-drop carriers (webhook.site/ntfy.sh/httpbun): zero. task-oai-NNN / northflank / probe.js: zero. (OBSERVED)
- `jina.ai`: 37 rows / 638 occurrences — the documented laundering marker, present as live tradecraft (see above). (OBSERVED)

## Verdict: **DOCUMENTED** (jina-laundering bypass technique; fresh byte-verified instances, no new CAPTCHA/Turnstile/Cloudflare defeat)
