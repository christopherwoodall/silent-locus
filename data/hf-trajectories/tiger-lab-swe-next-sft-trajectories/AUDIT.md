# Audit: TIGER-Lab/SWE-Next-SFT-Trajectories

- Source: `https://huggingface.co/datasets/TIGER-Lab/SWE-Next-SFT-Trajectories` (raw under `raw/tiger-lab-swe-next-sft-trajectories/`, provenance in `raw/tiger-lab-swe-next-sft-trajectories/PROVENANCE.md`)
- Audited: 2026-10-07
- Rows/files: 2,473 jsonl rows (`SWE_Next_SFT_Trajectories.jsonl`, 198MB) — SFT coding trajectories (`messages` format, SWE-Next arXiv 2603.20691)
- Method: full-file text scan for CAPTCHA/Turnstile/Cloudflare/bot-check encounters and challenge-solved strings; byte-verification discipline; marker grammar hunt. Sharp-pattern grep: **zero hits**.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.

## Headline

Clean. 943 broad-regex bypass hits collapse to harness/code contexts; zero anti-bot encounters, zero challenge-solved strings. All 33 marker-grammar candidates are byte-verified false positives (binary literals and hex blobs in test code). (OBSERVED)

## Evidence

- 4 text files scanned; 943 bypass-flag hits, 0 challenge-solved hits, 0 sharp bypass hits (0/943).
- Distinct-context dedup:
  - "BLOCKED: refusing to run the evaluation runner / refusing to re-run a broad test suite" — the SWE harness's own test gate (`[final_test_gate]`, `[test_throttle]`) refusing expensive test runs. Harness safety behavior, not a site challenge. (OBSERVED)
  - "BLOCKED = 15" enum values, "403" = source-code line numbers in file-view observations. (OBSERVED)

## Marker grammar — all killed (OBSERVED)

- 33 `B\d{10}[A-Z0-9]{2}` hits: all binary literals (`0b110000000000...` in ipv4 test code) and substrings of hex blobs in test fixtures, e.g. `...B9026527933ACC03E6E...` inside a hex dump. FP_HEX_BLOB / FP_BIN_LITERAL — not Amap POI grammar.
- `oai*` tags, `zz=` params, dead-drop carriers (webhook.site/ntfy.sh/httpbun), task-oai-NNN: zero.

## Verdict: **CLEAN**
