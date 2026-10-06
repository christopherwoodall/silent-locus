# SCAN-SUMMARY.md — Wikipedia top-500 infra scan (2026-10-06)

**Branch:** `wikipedia-top500-infra-scan-2026-10-06` (silent-locus worktree)
**Event dir:** `data/2026-10-06-wikipedia-top500-infra-scan/`
**Question:** do edits to the 500 most-viewed English Wikipedia articles originate from AI-provider / datacenter infrastructure?

## Headline verdict

**Zero verified datacenter-infra edits attributable to any provider — and zero attributable to any AI lab — in the visible history of the top-500 articles.** This is a clean, reviewed negative, not an absence of looking.

- The matcher's initial 90 hits (aws 62, azure 28) were **all killed by reviewer-1** on range currency: every hit rests on a provider-published CIDR that entered the provider's feed 1–6 years AFTER the edit. Against edit-contemporaneous feeds, 0/67 distinct IPs were in any published range of the attributed provider. Corrected match count: **0**.
- Zero matches on any AI-lab-published range (openai/anthropic/perplexity) across 677,635 revisions.

## Per-provider metrics table

| Provider | Raw matcher hits | Reviewer verdict | Surviving attributions | Edits | Articles | IPs | Date range of hits |
|---|---|---|---|---|---|---|---|
| aws | 62 | KILLED (currency) | 0 | — | 40 claimed | 49 claimed | 2020-01-16 → 2023-09-14 (all pre-date range publication) |
| azure | 28 | KILLED (currency) | 0 | — | 16 claimed | 18 claimed | 2020-04-11 → 2023-01-28 (all pre-date range publication) |
| openai | 0 | n/a | 0 | 0 | 0 | 0 | — |
| anthropic | 0 | n/a | 0 | 0 | 0 | 0 | — |
| perplexity | 0 | n/a | 0 | 0 | 0 | 0 | — |
| gcp | 0 | n/a | 0 | 0 | 0 | 0 | — |

What the killed hits looked like (for the record): ordinary human IP editing — BLP gossip, typos, vandalism, anti-vandalism. 57% carried mobile-edit tags, 39% were reverted, timestamps spread across 38 months with no burst cadence. Content sample: [Nigella Lawson vandalism](https://en.wikipedia.org/w/index.php?diff=997285420), [Tom Bateman sourcing fix](https://en.wikipedia.org/w/index.php?diff=1148721238), [Nicole Kidman birth-year correction](https://en.wikipedia.org/w/index.php?diff=989070223). No OAuth/AWB/bot tags, no nonce grammars, no automation-shaped metadata anywhere in the set.

Reverted-status check (metrics-analyst, 15 sampled of the 90 pre-kill): CURRENT 4 / REVERTED 8 / UNCERTAIN 3; population-level 37/90 (41.1%) carry a revert marker. Kept only as descriptive context — the attributions themselves are dead.

## Corpus

- **677,635 revisions** across **489 article files** (one rank, 433, holds two articles: "List of countries by GDP (nominal)" and "Barry Melrose"), revision window 2020-01-01 → 2026-10-07, via MediaWiki API (`rvprop=user|timestamp|ids|comment|tags|size`), curl-only, ≤1 req/5s.
- Article list: September 2026 pageviews API (most recent full month); 489 main-namespace articles; 11 non-article rows excluded (Special/File/Wikipedia/Portal/Help).
- Editor split: **61,179 IP editors (9.03%)** · **21,922 temp accounts (3.24%)** · **594,534 named users (87.74%)**. Only IP-editor revisions carry public IPs; temp/named are unattributable by IP from public data (counted, never guessed).
- **Completeness: 100% API-ground-truth audited.** All 489 files verified (valid JSONL, article match, monotonic timestamps, file min-timestamp == API oldest-in-window). The audit caught and repaired 3 real defects (74 files lost to VM storage flakiness and re-pulled; Hasan Piker truncated at 500 revs by missed pagination → 2,743; two empty files → re-pulled to 1,831 and 2,957 revs).
- CIDR map: **73,818 validated CIDR→provider records** (AWS 61,098 · Azure 11,284 · GCP 1,107 · OpenAI 281 · Anthropic 36 · Perplexity 12), each with source provenance. Historical range snapshots cached in `raw/history/` (10 AWS + 9 Azure, Wayback, with PROVENANCE.md + SHA256SUMS.txt) — these are what killed the 90 hits.

## Limits (paste-ready, from reviewer-2, lightly corrected)

1. **Temporal blindness.** IP visibility is 4.1% of 2025–2026 revisions and **0% of 2026** (last IP revision 2025-11-04T04:48Z; temp accounts begin 2025-11-04T09:55Z). The method is systematically blind to the AI-agent era it claims to hunt. Temp accounts (21,922 revisions, concentrated in the agent era) hide IPs by design.
2. **The blocklist purges the target.** Wikipedia's colocation/webhost range blocks actively suppress datacenter-IP editing — the observable IP population is pre-filtered against exactly the infrastructure of interest.
3. **Range-currency false positives.** Matching historical edits against a current range snapshot is a guaranteed false-positive machine: AWS's feed grew 2,061 prefixes (2020) → ~10,560 (2026), largely leased legacy-carrier blocks (88.x/86.x/99.x/72.x). All 90 hits died on this. Any re-run must use edit-contemporaneous feeds.
4. **"Datacenter IP" gloss is weaker than stated.** Provider-published feeds now include leased consumer-ISP-shaped space (e.g. 88.108.0.0/14 in the live AWS feed) — a provider-range hit doesn't cleanly mean "datacenter" even before the currency problem.
5. **Lab coverage is thin.** Of 73,818 CIDRs, lab-specific ranges are 329 (0.45%), all crawler ranges that don't edit. Anthropic/OpenAI publish no agent-egress ranges; xAI/DeepMind/Meta absent; Perplexity is AWS-hosted (no company ASN established). Residential proxies are invisible by design. Coverage of true agent-era egress is low single-digit percent.
6. **Selection bias.** September-2026 pageviews overweight heavily-protected current-events articles where IP editing is structurally ~zero (e.g. Deaths in 2026: 17,751 revs, 0 IP revs) — the sample maximizes protection while minimizing the observable population.
7. **Data-quality notes.** Rank 222 ("european election 2014") is a redirect with zero in-window revisions — 488 articles have data, not 489. `missing-g*.tsv` are consumed repull lists, not live state. All four audit quarters ran to completion (one reviewer draft wrongly said two).

## Clean negatives (first-class)

1. Zero matches on any AI-lab-published range across 677,635 revisions (openai/anthropic/perplexity bot + crawler ranges all in the map).
2. Zero provider-range matches among the 22,190 agent-era (2024–2025) IP-visible revisions — the only slice where the method can see the era it hunts, and it's empty.
3. No automation-shaped metadata in any matched or candidate set: no bot/OAuth/AWB tags, no burst cadence, no nonce grammars; tag profile is interactive human editing (mobile edits, reverts).
4. The 61,089 unmatched IP revisions' top ranges are residential/mobile-ISP-shaped (ordinary human editors) — assessed as weak inference, not verified per-IP.

## Killed-by-review appendix

- **90/90 matcher attributions KILLED** (reviewer-1, kill-or-fix authority): range currency. Full bracketing matrix in `workers/reviewer-1/FINDINGS.md`. Corrected count: 0.
- **AI-agent headline claim KILLED** (reviewer-2): observable and target populations disjoint by construction. Kept only the narrow claim: zero matches among 22,190 agent-era IP-visible revisions.
- **"ISP-shaped prefix" data-integrity flag KILLED** (reviewer-1): 88.108.0.0/14 verified present in the live official AWS feed; downgraded to interpretive caveat (limit #4).
- One reviewer draft error corrected: the API-ground-truth audit covered all four quarters, not two.

## Provenance

`raw/` holds: top500-articles.tsv, articles-main-ns.tsv, cidr-provider-map.jsonl (+ source range files), 489 revision JSONLs, ip-matches.jsonl (90 pre-kill records, retained as evidence), article-aggregates.tsv, history/ (19 Wayback range snapshots + PROVENANCE.md + SHA256SUMS.txt), PROVENANCE.md. `workers/` holds per-worker FINDINGS.md. All committed and pushed on the scan branch. Never touched main.
