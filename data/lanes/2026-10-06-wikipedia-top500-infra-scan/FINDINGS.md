# Findings — Wikipedia top-500 infra scan (2026-10-06)

## Headline verdict (OBSERVED)

Zero verified datacenter-infra edits attributable to any provider, and zero
attributable to any AI lab, in the visible history of the 500 most-viewed
English Wikipedia articles. This is a clean, reviewed negative — not an
absence of looking. Run: `run_6c62149360044bc19a4da3b45fe95157`.

## Graded claims

- **OBSERVED** (`claim_d4ca50ce03214d1bae39c36038d01e17`): 90/90 pre-kill
  matcher attributions KILLED by reviewer-1 on range currency. 0/67 distinct
  IPs in any edit-contemporaneous provider range. Surviving attributions: 0.
- **OBSERVED** (`claim_b7e10b5cacf340efbb55a3f2417319f2`): zero matches on
  AI-lab-published ranges (openai/anthropic/perplexity) across 677,635
  revisions.
- **OBSERVED** (`claim_a4c84d8825dd4fc694fa99ceb3bf7483`): zero provider-range
  matches among 22,190 agent-era (2024–2025) IP-visible revisions — the only
  slice where the method can see the era it hunts.
- **OBSERVED** (`claim_a8159b3fd5dd43c585e372901eb2c174`): the killed set was
  ordinary human IP editing — 57% mobile-edit tags, 39% reverted, no
  bot/OAuth/AWB tags, no burst cadence, no nonce grammars.
- **OBSERVED** (`claim_09f493af957442b0b018f717e266cdb9`): editor split —
  61,179 IP editors (9.03%), 21,922 temp accounts (3.24%), 594,534 named
  users (87.74%). Only IP-editor revisions carry public IPs.
- **OBSERVED** (`claim_36a4a9c7dbfe486383e1b078f7d08951`): CIDR map of 73,818
  validated CIDR→provider records (AWS 61,098 · Azure 11,284 · GCP 1,107 ·
  OpenAI 281 · Anthropic 36 · Perplexity 12).
- **INFERENCE** (`claim_656c7155ad4f457da6687be528ded4b1`): the method is
  systematically blind to the AI-agent era — IP visibility 4.1% of 2025–2026
  revisions, 0% of 2026 (temp accounts hide IPs from 2025-11-04).
- **OBSERVED** (`claim_40d1846801924e4798fa6e675f7d369d`): Wikipedia's
  colocation/webhost range blocks pre-filter datacenter-IP editing from the
  observable population.

## Evidence notes

The 90 pre-kill matcher hits are retained as evidence — flagged, not
endorsed — in `raw/ip-matches.jsonl` and `events.jsonl`. They are NOT IOCs:
the lane's own review says publishing them as IOCs would be publishing
false positives. Kill reason for every hit: range currency (provider CIDR
entered the published feed 1–6 years after the edit).
