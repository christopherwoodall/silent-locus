# Audit: TIGER-Lab/SWE-QA-Pro-SFT-Trajectories

- Source: `https://huggingface.co/datasets/TIGER-Lab/SWE-QA-Pro-SFT-Trajectories` (raw under `raw/tiger-lab-swe-qa-pro-sft-trajectories/`, provenance in `raw/tiger-lab-swe-qa-pro-sft-trajectories/PROVENANCE.md`)
- Audited: 2026-10-07
- Rows/files: 1,000 jsonl rows (`train.jsonl`, 65MB) — SFT coding trajectories, `tools` = view_codebase/file_editor/bash-style function tools
- Method: per-row text scan for CAPTCHA/Turnstile/Cloudflare/bot-check encounters and challenge-solved strings; byte-verification discipline; marker grammar hunt. Sharp-pattern grep: `captcha|turnstile|cloudflare|prove you are human|verify you are human|are you a robot|webhook.site|ntfy.sh|httpbun|\boai[:-_]` → **zero hits**.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.

## Headline

Clean. All 348 broad-regex bypass hits are a single false-positive class: the literal `403` inside the harness worker directory name `repos_tmp/worker_1597403/...` (matched by a bare-`403` regex; killed by word-boundary `\b403\b`). Zero anti-bot encounters, zero challenge-solved strings. (OBSERVED)

## Evidence

- 4 text files scanned; 348 bypass-flag hits, 0 challenge-solved hits.
- Distinct-context dedup of the 348 hits: every one is `worker_1597403` path text in file-view tool observations. No CAPTCHA/Turnstile/Cloudflare/bot-check encounter anywhere in the 1,000 rows. (OBSERVED)
- Tooling lesson recorded: bare `403` in the bypass regex fires on numeric IDs (worker_1597403). Fixed to `\b403\b` in `scripts/flag_scan.py`; re-run pending on remaining datasets.

## Marker grammar

- `oai*` tags: zero; no `pmh:oai:` to rule out. (OBSERVED)
- `zz=` params: zero. Dead-drop carriers (webhook.site/ntfy.sh/httpbun): zero. (OBSERVED)
- `amap` regex initially hit 3x — all false positives: the AMap (Gaode) JavaScript mapping library named inside the repeated `view_codebase` tool docstring (`"description"` mentions `AMap`). Not the hunt's Amap POI grammar (`B\d{10}[A-Z0-9]{2}` / amap.com). Regex narrowed accordingly; killed as FP_AMAP_MAPLIB. (OBSERVED)

## Verdict: **CLEAN**
