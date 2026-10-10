# Findings — hf-trajectories-audit

Grade claims OBSERVED, UPSTREAM, or INFERENCE.

## Verdicts (OBSERVED, from the 2026-10-07 flag-audit)
- yoonholee/terminalbench-trajectories: DOCUMENTED — r.jina.ai proxy laundering
  (37 rows, 638 occurrences), technique already reported upstream.
- Hcompany/trajectories: CLEAN — DBLP rate-limit encounter only, no challenge solved.
- 0xSero/glm-5.2-nf3-hybrid-terminal-bench-2.1-traces: CLEAN — no repeat of the
  WildClaw GSMArena Turnstile defeat.
- TIGER-Lab/BrowserAgent-Data: CLEAN — localhost Kiwix mirror, no live web.
- DJLougen/hermes-agent-traces-filtered: CLEAN — 256 hits all code contexts.
- TIGER-Lab/SWE-Next-SFT-Trajectories: CLEAN — 943 hits are harness test gates.
- Crownelius/GPT-5.6-Sol-Luna-Terra-Traces: CLEAN — 8 sharp hits all killed.
- TIGER-Lab/SWE-QA-Pro-SFT-Trajectories: CLEAN — 348 hits are `worker_1597403`.
- TIGER-Lab/BrowserAgent-SeedData: CLEAN — zero hits across ~242K rows.
- aisa-group/ResearchArena-Trajectories: CLEAN — 466 hits are Anthropic
  `rate_limit_event` metadata.

## Headline (OBSERVED)
No NEW DEFEAT found. No unreported successful CAPTCHA/Turnstile/Cloudflare
evasion was byte-verified in any of the 10 datasets.

## Clean negatives worth keeping
- YouTube "Sign in to confirm you're not a bot" defeated 4/4 agent evasion
  attempts (yoonholee, claude-sonnet-4-5, reward 0).
- Google 429/CAPTCHA warning page returned *through* the jina proxy (yoonholee,
  gpt-5) — the proxy did not defeat the challenge.
- Kimi-K2 hit Google's JS/CAPTCHA wall and pivoted to the GitHub API — encounter,
  no defeat.

## Marker grammar tally (OBSERVED)
- `jina.ai` laundering: live tradecraft in yoonholee (37 rows, 10 models, 4 agents).
- `oai*` tags, `zz=` params, dead-drop carriers, task-oai-NNN fleet markers,
  Amap POI grammar: zero true hits everywhere.
