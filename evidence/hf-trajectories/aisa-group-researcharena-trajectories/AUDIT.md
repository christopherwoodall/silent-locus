# Audit: aisa-group/ResearchArena-Trajectories (P2 bounded sample)

- Source: `https://huggingface.co/datasets/aisa-group/ResearchArena-Trajectories` (raw sample under `raw/aisa-group-researcharena-trajectories/`, provenance in `raw/aisa-group-researcharena-trajectories/PROVENANCE.md`)
- Audited: 2026-10-07
- Sample: 12 red_team `solve_out_sanitized.json` (cuda_kernel setting, claude-opus-4-8 / gpt-5.5 / gemini-3.1-pro, baseline + embedded2 side tasks) + README.md. Full repo is ~6.2GB; this is a P2 sample only.
- Method: per-row text scan for CAPTCHA/Turnstile/Cloudflare/bot-check encounters and challenge-solved strings; byte-verification discipline (template-default flag ≠ defeat); marker grammar hunt (oai* tags, zz= params, epoch nonces, httpbun/httpbin carriers, webhook.site/ntfy.sh dead-drops). Sharp-pattern grep: `captcha|turnstile|cloudflare|prove you are human|verify you are human|are you a robot|webhook.site|ntfy.sh|httpbun|\boai[:-_]` → **zero hits** across the sample.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.
- **UPSTREAM**: documented by the dataset/publisher or a cited finding elsewhere.

## Headline

Sample is clean for the bypass/defeat lane. No anti-bot encounters, no challenge-solved strings, no marker grammar. The 466 raw bypass-flag hits in the broad regex scan are all Anthropic API `rate_limit_event` metadata entries in the stream-json (e.g. `{"type":"rate_limit_event","rate_limit_info":{"status":"allowed",...}}`) — harness bookkeeping, not a site challenge. (OBSERVED)

## Evidence

- Broad regex scan: 15 text files, 466 bypass-flag hits, 0 challenge-solved hits, 0 marker hits.
- Of the 466 hits: ~308 are `rate_limit_event`/`rate_limit_info` entries; the remaining 158 are matches on words like "denied"/"403" inside tool-call payloads, thinking signatures, and usage counters — byte-checked, none is a CAPTCHA/Cloudflare/challenge encounter. (OBSERVED)
- The eval's *sanctioned* side tasks include checkpoint/conversation exfiltration to attacker-controlled endpoints (`independent` side task, README table). That exfil behavior is **UPSTREAM/DOCUMENTED** (paper arXiv 2607.19321, README side-task table) — it is the eval's designed scenario, not a newly discovered evasion. No dead-drop carrier domains (webhook.site/ntfy.sh/httpbun) appear in the sampled red_team outputs. (OBSERVED + UPSTREAM)

## Marker grammar

- `oai*` tags: zero (the `\boai[:-_]` grep returns nothing; no `pmh:oai:` to rule out in this sample). (OBSERVED)
- `zz=` params: zero. Epoch nonces: not counted in this pass (weak signal); none needed. (OBSERVED)
- Dead-drop carriers (webhook.site/ntfy.sh/httpbun): zero. (OBSERVED)

## Verdict: **CLEAN** (sample; P2)
