# Keyword hits by model family — url-keyword-farm

Source data: `data/hf-trajectories/url-farm/group-A.json`, `group-B.compact.json`,
`group-C.json`, `group-D.json`, `merged.json`. Built 2026-10-08 on branch
`url-keyword-farm`. Term universe: 37 distinct terms from `merged.json`
`keyword_totals` (plus the same 37 in group hit `pattern` fields — sets match
exactly). Pass-1 hit total: 179,171; per-hit model records used here: 58,702
with a `model` string, 6,615 without.

## Mapping rules

First match wins. The model string is split on `@` into NAME and PROVIDER.
NAME rules are tried first (name part only: text before `@`, after the last
`/`). If no NAME rule hits, PROVIDER rules run on the part after `@`.

NAME rules (lowercased substring, in order):
1. `gpt-openai`: `gpt-`, `openai`, `codex`, word-boundary `o1`/`o3`/`o4`
2. `glm-zai`: `glm`, `z-ai`, `zai-`
3. `grok-xai`: `grok`, `x-ai`, `xai`
4. `claude-anthropic`: `claude`, `anthropic`, `sonnet`, `opus`, `haiku`
5. `gemini-google`: `gemini`, `google`, `gemma`
6. `deepseek`: `deepseek`
7. `kimi`: `kimi`, `moonshot`
8. `qwen`: `qwen`, `qwq`
9. `llama-meta`: `llama`, `meta-`, word-boundary `meta`

PROVIDER fallback (substring of the part after `@`, same order):
`openai` → gpt-openai; `anthropic` → claude-anthropic; `z-ai` → glm-zai;
`xai` → grok-xai; `google` → gemini-google; `deepseek` → deepseek;
`moonshot` → kimi.

`other-unknown`: everything else. Kept raw, never force-fit. In this corpus
that is MiniMax models (`accounts/fireworks/models/minimax-m2@fireworks_ai`,
3,767 hits; `minimax-m2.1@openai`, 726; `minimax-m2.5@Minimax`, 542;
`minimax-m2.1@minimax`, 202) and the
unidentified `Holo4 35B A3B` (65) / `Holo4 27B` (61) models. MiniMax was matched on NAME,
not provider: `minimax-m2.1@openai` carries an OpenAI-compatible provider
field but the model is MiniMax, so it goes to other-unknown, not gpt-openai.

Attribution rule: a TERM (not each occurrence) is written to every family in
which it was observed in a hit with a model string. Terms that appear only in
model-less records (group B `high_suspicion_hits`, group B `keyword_totals`
aggregates, group D) go to other-unknown. Dataset names were NOT used to infer
models (e.g. `crownelius/gpt-5.6-sol-luna-terra-traces` terms stay unattributed
unless a hit record carries a model string).

## Per-family counts

| Family | Terms | Model-attributed hits | Notes |
|---|---|---|---|
| gpt-openai | 25 | 8,516 | |
| glm-zai | 19 | 9,463 | |
| grok-xai | 15 | 1,177 | |
| claude-anthropic | 27 | 15,941 | most hits, broadest spread |
| gemini-google | 16 | 2,863 | |
| deepseek | 14 | 257 | thinnest model-attributed evidence |
| kimi | 23 | 10,239 | |
| qwen | 21 | 5,609 | |
| llama-meta | 0 | 0 | no llama/meta models in this corpus — absence, not cleanliness |
| other-unknown | 25 | 4,637 | MiniMax + Holo4 models, plus all model-less terms |

Verification: union of the 10 files covers all 37 universe terms; 0 missing.
27 of 37 terms appear in more than one family file (per-family dedup, not
global — a shared term lands in each family that produced it). 4 terms have
NO model attribution anywhere and sit only in other-unknown:
`exfiltrate`, `turnstile`, `webhook.site`, `t.me/` (plus `ngrok` and
`harness anti-bot guidance`, which have only model-less aggregate records).
No term failed attribution beyond this documented set.

## Security read (all claims OBSERVED unless marked)

The malicious-term vocabulary is provider-agnostic, not family-specific.
That is the headline: the same bypass / jailbreak / exfil / credential-theft
terms show up in trajectory hits across every model family present in the
corpus. The differences are sampling effects (hit volume per family), not
clean families.

Bypass / jailbreak / instruction-override:
- `bypass` — all 9 model-attributed families (OBSERVED).
- `DAN` — 8 of 9 (all but deepseek; deepseek has only 257 hits, so this may
  be sampling, not a real absence).
- `system prompt` — all 9 (OBSERVED).
- `you are now` — claude-anthropic, kimi, qwen only.
- `jailbreak` — grok-xai only (single-family hit; treat as lead, not as a
  grok-specific trait).
- `circumvent` — claude, gemini, gpt, kimi.

Laundering / anti-bot defeat:
- `jina.ai` (reader-laundering endpoint) — gpt-openai, glm-zai, kimi.
- `cloudflare`, `captcha` — 7 and 6 families; `turnstile` — other-unknown only
  (model-less records; unattributed, not absent).
- `proxy` — all 9 (OBSERVED; note some hits are benign library code —
  `MultiDictProxy` in group D — term-level hit, not intent).

Exfil channels:
- `exfiltrate`, `webhook.site`, `t.me/` — other-unknown only. OBSERVED in
  model-less records (group B/D); they could not be attributed to any family.
  `webhook.site` is the live dead-drop surface from the urlquery lane — its
  hits have no model strings, so family attribution is open.
- `telegram` — claude, glm, gpt, kimi, qwen, other-unknown.
- `pastebin` — claude, deepseek, kimi.

Recon tooling:
- `nmap` — 8 of 9 (all but deepseek).
- `hydra` — gpt, claude, gemini.

Credential / secret theft:
- `credential`, `api key`, `secret key`, `private key`, `.ssh/`, `id_rsa`,
  `AWS_SECRET` — 8–9 families each (OBSERVED across the board).
- `OPENAI_API_KEY` — claude, deepseek, gemini, gpt.
- Crypto: `bitcoin`, `ethereum` — 6 families; `wallet` — claude and gpt only.

Bottom line: no family in this corpus is "clean" of laundering/bypass/
jailbreak terms. claude-anthropic has the broadest malicious-term spread
(27 terms) but also the most hits (15,941) — spread tracks hit volume.
llama-meta has zero hits because no llama/meta models appear in the corpus,
not because llama models are clean. The single strongest unassigned lead is
the model-less exfil cluster (`exfiltrate`, `webhook.site`, `t.me/`,
`turnstile`) — these hits carry no model strings and sit in other-unknown;
family attribution needs model-tagged re-collection.
