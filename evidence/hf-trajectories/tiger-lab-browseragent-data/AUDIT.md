# Audit: TIGER-Lab/BrowserAgent-Data

- Source: `https://huggingface.co/datasets/TIGER-Lab/BrowserAgent-Data` (raw under `raw/tiger-lab-browseragent-data/`, provenance in `raw/tiger-lab-browseragent-data/PROVENANCE.md`)
- Audited: 2026-10-07
- Rows/files: 16,804 jsonl rows (`sft.jsonl` 74MB + `rft.jsonl` 84MB), ChatML browser-agent dialogues (paper arXiv 2510.10666)
- Method: per-row text scan for CAPTCHA/Turnstile/Cloudflare/bot-check encounters and challenge-solved strings; byte-verification discipline; marker grammar hunt. Sharp-pattern grep (`captcha|turnstile|cloudflare|prove you are human|verify you are human|are you a robot|bot-check|webhook.site|ntfy.sh|httpbun|\boai[:-_]`): **zero hits**.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.

## Headline

Clean. All 4,761 broad-regex bypass hits collapse to two benign classes; zero anti-bot encounters, zero challenge-solved strings. The browser in these trajectories browses a **localhost Kiwix Wikipedia snapshot** (`http://localhost:22015/wikipedia_en_all_maxi_2022-05/...`) — no live web, so no CAPTCHA/Cloudflare encounters were possible. (OBSERVED)

## Evidence

- 5 text files scanned; 4,761 bypass-flag hits, 0 challenge-solved hits, 0 sharp bypass hits (0/4761 on `captcha|turnstile|cloudflare|...`). (OBSERVED)
- Distinct-context dedup of the 4,761 hits:
  - ~4,740x: `[403]`-style element reference IDs in the accessibility tree, e.g. `\t[403] link 'Crusades' url: http://localhost:22015/...` — element indices, not HTTP 403. (OBSERVED)
  - Remainder: "denied"/"blocked" in task/article text (historical court decisions, football plays). (OBSERVED)
- Localhost browsing confirmed in trajectory text across both splits: every fetched URL is `http://localhost:22015/wikipedia_en_all_maxi_2022-05/A/...`. (OBSERVED)

## Marker grammar

- `oai*` tags: zero. (OBSERVED)
- `zz=` params: zero. Dead-drop carriers (webhook.site/ntfy.sh/httpbun): zero. (OBSERVED)
- `amap` hits (13, old regex) are all `SaReGaMaPa` (Indian TV show) in Wikipedia page text matching `aMap` case-insensitively — killed as FP; narrowed regex (`amap.com` / `B\d{10}[A-Z0-9]{2}`) returns zero. (OBSERVED)

## Verdict: **CLEAN**
