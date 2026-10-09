# Africa regional scout — urlquery hunt (local-corpus pivot)

**Date:** 2026-10-04 ~23:55 CDT
**Scope:** gov.za, gov.ng, gov.ke, gov.gh, gov.eg, gov.et, gov.rw
**Method change:** Egress to urlquery.net was DOWN at scan time (curl to urlquery.net and google.com both fail; the htmx tool's proxy tunnel errors). The planned live `uq_htmx.py` searches were NOT run — no live urlquery data was fetched. Pivoted to streaming grep over local corpora: `~/workspace/silent-locus/data/*/events.jsonl` and `~/workspace/silent-locus/collections/*/data/*.jsonl`.

## Per-domain results (local corpora only)

| Query | Local hits | Assessment |
|---|---|---|
| gov.za | 0 | honest zero |
| gov.ng | 0 | honest zero (only false positive: `civilrightsdata.ed.gov/ngsw.json`, matched on unescaped dot) |
| gov.ke | 0 | honest zero |
| gov.gh | 0 | honest zero |
| gov.eg | 4 lines = **2 distinct reports** | research-task artifact, not scanning (see below) |
| gov.et | 0 | honest zero |
| gov.rw | 0 | honest zero |

## The gov.eg pair (only real hits)

- **Report 1:** `28ed7589-9684-4b90-a57b-627e46abbf0f` — `edaegypt.gov.eg/en/media-center/news/during-the-fifth-edition-of-africa-health-excon-2026-eda-supports-strategic-partnerships-to-localize-vaccine-manufacturing-and-strengthen-health-security-across-africa/?utm_source=chatgpt.com` — captured **2026-07-17T04:44:41Z**
- **Report 2:** `6c6e30da-869a-4e5c-86f6-acb70cd2dc99` — `www.edaegypt.gov.eg/en/media-center/news/dr-ali-el-ghamrawy-chairman-of-the-eda-participated-in-africa-health-excon-2026-where-he-presented-the-authority-s-strategic-vision-for-the-pharmaceutical-sector-through-2030/?utm_source=chatgpt.com` — captured **2026-07-17T04:44:38Z**
- Both matched DeepSearchQA questions `dsqa_283` and `dsqa_339` under fingerprint **"Africa"** (`collections/re-hunt-qa-fingerprints/data/hits.jsonl`).
- Hunt-side label on both captures: `hunt.campaign = "pastebin-sweep-negative"` (analyst annotation, not submitter tag).

**Reading:** two pageviews of the Egyptian Drug Authority's news section, 3 seconds apart, both URLs carrying `?utm_source=chatgpt.com`. This is a research-task artifact — URLs copied out of a ChatGPT answer (self-identification-in-URL, per hunt doctrine) and submitted to urlquery, then fingerprinted against DeepSearchQA "Africa" questions. It is NOT systematic enumeration: no nonce/grammar patterns, no tunnel/shortener relays, no burst beyond two same-site page loads. The 3-second gap is consistent with an agent reading two search results, or a human double-clicking two links. Verdict: **one-off agent research-task triage, not programmatic scanning**.

## Verdicts

- **Programmatic agent-shaped scanning of African .gov domains:** none found in local corpora.
- **One-off/agent-assisted triage:** the gov.eg pair (ChatGPT-sourced URL submissions).
- **Honest zeros:** gov.za, gov.ng, gov.ke, gov.gh, gov.et, gov.rw — zero hits in local corpora.

## Caveats

1. **This is not the planned measurement.** Local corpora skew toward known incidents (HF tampering, RubyGems go-import campaign, DeepSearchQA/DoE, urlquery marker sweeps). Zero local hits does not establish zero activity on urlquery.net. The live searches should be rerun once egress is restored.
2. No submission metadata (submitter UA, tags) for the two gov.eg reports exists locally — only the captured URL, timestamps, and hunt-side annotations.

## Files

- `raw/africa-<query>.json` — per-domain JSON with matches (empty `matches` where zero).
