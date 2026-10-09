# Audit: TIGER-Lab/BrowserAgent-SeedData

- Source: `https://huggingface.co/datasets/TIGER-Lab/BrowserAgent-SeedData` (raw under `raw/tiger-lab-browseragent-seeddata/`, provenance in `raw/tiger-lab-browseragent-seeddata/PROVENANCE.md`)
- Audited: 2026-10-07
- Rows/files: 10 parquet files across 6 task dirs (2wiki train 10,000 / validation 25,152; bamboogle test 125; hotpot train 90,447 / validation 14,810; musique train 10,000 / validation 4,834; nq test 3,610 / train 79,168; popqa test 14,267). Schema: data_source, prompt, ability, reward_model, extra_info — QA seed prompts, no live tool calls.
- Method: whole-corpus text scan of every string column in all 10 parquets (scripts/fast_scan_parquet.py); sharp-pattern + challenge-solved + marker-grammar regexes.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.

## Headline

Clean. Zero hits of any class across all 10 files (~242K rows): no CAPTCHA/Turnstile/Cloudflare/bot-check text, no challenge-solved strings, no marker grammar. These are static QA seed prompts (2WikiMultiHopQA, Bamboogle, HotpotQA, MuSiQue, NQ, PopQA) with no agent tool calls — nothing to bypass. (OBSERVED)

## Verdict: **CLEAN**
