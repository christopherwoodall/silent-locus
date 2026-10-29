# REVIEWER-2 (methodology red-team) FINDINGS — Wikipedia top-500 infra scan

**Reviewer:** reviewer-2 | **Date:** 2026-10-06 | **Branch:** wikipedia-top500-infra-scan-2026-10-06
**Scope:** methodology + headline claims only. No commits, no branch switches, no pushes.
Inputs re-derived independently from `raw/revisions/*.jsonl`, `raw/ip-matches.jsonl`,
`raw/article-aggregates.tsv`, `raw/cidr-provider-map.jsonl`, and all worker FINDINGS.md.

**Bottom line:** the collection plumbing is solid (counts reconcile to the revision;
audits found no truncation where run). The *interpretive* layer is not. Every number
the scan produces as evidence of "AI-provider infra" editing is pre-agent-era,
human-shaped, and matched against present-day ranges — and the method has 0%
IP visibility into 2026, the year that matters most. The headline claim, as an
AI-agent claim, is KILLED. What survives is a narrower, honest statement (see §5).

---

## 1. The premise is systematically blind to the thing it hunts

The scan's premise: "edits from AI-provider infra" in the AI-agent era. The method
can only see revisions by *IP editors* — logged-in users (87.74% of revisions) and
temp accounts (3.24%) carry no public IPs. Re-derived from the raw revision files:

| year | IP-editor revs | temp-account revs | named-user revs |
|------|---------------:|------------------:|----------------:|
| 2020 | 9,760 | 0 | 56,913 |
| 2021 | 9,511 | 0 | 67,400 |
| 2022 | 9,912 | 0 | 71,111 |
| 2023 | 9,806 | 0 | 69,695 |
| 2024 | 10,113 | 0 | 71,677 |
| 2025 | 12,077 | 1,808 | 97,720 |
| 2026 | **0** | **20,114** | **160,018** |

(Totals reconcile exactly with matcher + aggregates: 61,179 / 21,922 / 594,534 / 677,635.)

The IP→temp-account cutover in this corpus is sharp and observable:
**last IP-editor revision 2025-11-04T04:48:38Z; first temp-account revision
2025-11-04T09:55:58Z.** After that, anonymous-edit IPs are gone from public data.

Agent-era visibility (agents with web-browsing/editing capability: late-2024 → present):

- **2025–2026: 12,077 of 291,737 revisions are IP-visible = 4.1%.**
- **2026 alone: 0 of 180,132 revisions IP-visible = 0%.** Every 2026 anonymous edit
  is a temp account; every 2026 attributable actor is either temp or named.
- Even defining the agent era generously as 2024–2026: 22,190 of 373,527 = 5.9%.

**Verdict (checklist 1):** yes — the method is systematically blind to exactly what it
claims to hunt. The agent era lives in the temp-account + named-user columns, which
the method cannot touch. The observable window (IP editors) ends the month before
the era of interest peaks.

Structural compounding factor (not stated anywhere in the scan): **en.wikipedia
blocks anonymous editing from datacenter/colocation IPs** (the "web host" block).
An AI agent editing from AWS/Azure as an IP editor would, in the normal case, be
refused outright — never producing a public IP revision. The scan therefore hunts
in a population the platform actively excludes: any datacenter-IP revision that
*does* appear is, by construction, drawn from ranges Wikipedia's blocklist missed,
not from mainstream agent egress.

## 2. The 90 "matches" are 100% pre-agent-era and human-shaped — KILLED as AI evidence

Re-derived from `raw/ip-matches.jsonl` (90 records, 67 distinct IPs, all IPv4):

- By year: **2020: 36, 2021: 22, 2022: 17, 2023: 15. 2024: 0, 2025: 0.**
  Every single match predates the agent era. The 22,190 IP-editor revisions from
  2024–2025 (the only agent-era IP-visible data) produced **zero** matches.
- By provider: aws 62, azure 28. **Zero matches on any lab-specific range**
  (OpenAI 281 CIDRs, Anthropic 36, Perplexity 12 — all crawler/bot ranges that
  don't edit anyway).
- Tags: 51/90 "mobile edit", 47/90 "mobile web edit", 4 mobile-app, 3 ios-app.
  **57% carry mobile-edit tags** — the signature of mobile-carrier NAT, not agents.
- 35/90 carry `mw-reverted` (39%); others carry `possible libel or vandalism`,
  `possible unreferenced addition to BLP`, `changing height or weight`.
  This is human gadfly/vandalism traffic, including reverted edits.

**Range-temporal-drift flaw (undisclosed):** the matcher tests 2020–2023 editor IPs
against CIDR maps retrieved **2026-10-06**. IPv4 space is reallocated between
carriers/ISPs and clouds over the years; an IP that was mobile-carrier/residential
in 2021 can sit inside a 2026 AWS/Azure range. The 57%-mobile-tagged match set is
exactly what false positives from reallocation look like. The matcher discloses
none of this; its caveat covers provider-name ambiguity but not time drift.

**Killed claims:**
- "90 edits from AI-provider infrastructure" **as evidence of AI-agent activity** — KILLED.
  Nothing in the 90 is agent-shaped, agent-dated, or lab-attributed.
- Any implication the matches inform on 2024–2026 — KILLED (zero matches there).
- **Kept, reworded:** "90 IP-editor revisions (2020–2023) fall inside present-day
  AWS/Azure ranges; 57% mobile-tagged, 39% reverted; zero lab-specific matches;
  consistent with human VPN/corporate/mobile-carrier traffic and/or IPv4 range
  reallocation. Candidate leads only — not attribution."

## 3. Data-quality issues (checklist 3)

1. **Rank-222 redirect ("european election 2014"):** `raw/revisions/222.jsonl` is
   **0 bytes** — the puller queried the redirect title without following it, so the
   target article's history was never pulled. Worse, rank 222 has **no row** in
   `raw/article-aggregates.tsv` (488 data rows, not 489). The scan is silently
   **488 articles with data**, not 489. Fix: re-pull with `redirects=1` or flag the
   row as missing in aggregates. (One article; no effect on headline metrics, but
   "489 articles scanned" is wrong.)
2. **Rank-433 tie** (Barry Melrose / List of countries by GDP (nominal), both rank
   433): handled correctly with two files — not an issue, noted as clean.
3. **Main Page (rank 1)** kept in corpus (80 named revs, 0 IP/temp): harmless noise,
   already flagged by list-builder. Keep but exclude from any IP-rate denominators
   in prose.
4. **`raw/missing-g1/2/3.tsv`** are stale intermediate audit artifacts (ranks listed
   there all have revision files now). Harmless, but label them stale so a future
   reader doesn't treat them as missing data.
5. **Audit coverage gap:** API ground-truth audit (oldest-revision check) ran only
   for quarters 0 (ranks 1–128, audit-0) and 3 (378–500, audit-3): 245 of 489 files.
   Chunks `audit-1.tsv` (ranks 129–254) and `audit-2.tsv` (255–377) were assigned but
   **no audit workers ran them** — no ground-truth artifacts exist. Puller self-checks
   (file exists, non-empty, first-line agreement) cover the middle, but the
   scan-wide "no truncation" claim is only API-verified for half the corpus.
6. "Current-vs-reverted status" (requested metric): only partially delivered.
   `mw-reverted` tags were captured (35/90), but "still-current" was never computed
   (would require checking each revid against the article's current revision).
   Either compute it or drop the metric from the summary.

## 4. Selection bias (checklist 2)

Top-500 by **September 2026 pageviews** tilts the corpus toward:

- **Current-events articles** (Charlie Kirk assassination, 2026 Iran war, 2026
  Swedish general election, Deaths in 2026, Killing of the Clancy children) — the
  most heavily *protected* pages on Wikipedia. Protection funnels anonymous editing
  into temp accounts or blocks it outright, so the sample overweights articles
  where IP-visibility is structurally lowest. E.g. Deaths in 2026 (#6, 17,751 revs)
  has **0 IP-editor revisions**; Killing of the Clancy children (#5, 847 revs) has 0.
- **One-month snapshot:** articles hot during the actual agent-era window
  (2024–early 2025) but cold in Sept 2026 are excluded; the selection is indexed
  to the *end* of the observation window, not the era of interest.
- **Bot-inflated ranks:** the legacy pageviews API counts bots (list-builder notes
  this); rank order near the cutoff is soft.
- **Short histories:** 2026-dated articles contribute little pre-2026 data, which
  is where 100% of the matches live — diluting an already thin signal.

Net: the corpus is a reasonable "most-read articles" snapshot but a **biased**
instrument for this question — it maximizes protection (minimizing the observable
IP-editor population) and is time-indexed away from the agent era.

## 5. The unmatched 61,089 and the real blind spot (checklist 4)

- 61,089 of 61,179 IP revisions (99.85%) match nothing. Top unmatched /16s and /48s
  are eyeball-judged "residential" by the matcher — that is an **INFERENCE, weak**,
  not a verified ASN census. No ASN/assignment check was performed. State it as such.
- **Map composition (73,818 CIDR records):** azure 61,098 (82.7%), aws 11,284
  (15.3%), gcp 1,107 (1.5%), openai 281, anthropic 36, perplexity 12.
  **Lab-specific ranges = 329 records = 0.45% of the map.**
- What the map cannot cover (the actual blind spot):
  1. **Anthropic publishes no API/agent egress ranges** (only crawler IPs).
  2. **OpenAI publishes no API/agent egress ranges** (only crawler + ChatGPT-User
     browsing IPs — fetch infra, not editing infra).
  3. **No xAI, Google DeepMind/Gemini, or Meta ranges at all.**
  4. **Residential-proxy egress** — the standard tradecraft for web agents wanting
     to look human — is invisible to range matching *by design*.
  5. **Temp accounts and logged-in editors** (96% of agent-era revisions) are
     invisible regardless of range quality.
  6. Range reallocation over 2020–2026 creates both false positives and false
     negatives against present-day maps.
- So: the map covers generic cloud space well (where human VPNs live too) and
  covers almost none of the *actual* plausible AI-agent egress. **Estimated
  coverage of true agent-era egress: low single digits percent, and the observable
  population (IP editors) excludes agents structurally** (colocation blocks, §1).
  AI-agent traffic is far more likely to hide in the *unmatched* set (residential
  proxies) or outside IP-attribution entirely than in the matched set.

## 6. Verdicts ledger

| Claim | Verdict |
|---|---|
| 677,635 revs / 61,179 IP / 21,922 temp / 594,534 named; counts reconcile | **KEPT** (independently re-derived, exact) |
| 90 IP revisions match cloud ranges (AWS 62, Azure 28) | **KEPT as stated, KILLED as AI evidence** |
| Zero lab-specific (OpenAI/Anthropic/Perplexity) matches | **KEPT** (supports "no lab-infra signal", weakly — see coverage) |
| "No truncation" of revision pulls | **KEPT for quarters 0+3; UNVERIFIED for quarters 1–2** |
| Article list (489 main-ns after 11 exclusions) | **KEPT with fix**: rank-222 redirect contributed 0 revisions and is missing from aggregates → **488 articles with data** |
| 61,089 unmatched IPs "are residential" | **DOWNGRADED to weak INFERENCE** (no ASN census) |
| Method can detect AI-agent editing of top-500 articles | **KILLED** — 0% IP visibility in 2026; colocation blocks exclude agent egress; lab egress unpublished; residential proxies invisible |
| "Honest zero" on agent-era datacenter IP editing | **KEPT, narrowed**: zero matches among 22,190 agent-era (2024–2025) IP-editor revisions — a clean zero *within the 4–6% visible slice*, not a claim about agent activity |

## 7. The single biggest methodological weakness

**The observable population and the target population are disjoint by construction.**
The scan wants AI agents (2024–2026, datacenter egress, often authenticated or
proxied); the method sees only anonymous IP editors (a population that ends
2025-11-04, is 0% of 2026, and is actively *purged* of datacenter IPs by
Wikipedia's colocation blocks). Every design choice compounds the same error:
temp accounts hide the agent era, the blocklist hides agent egress, unpublished
ranges hide the labs, residential proxies hide the tradecraft. The 90 matches are
not a weak signal — they are a *different* signal (pre-2024 humans on
cloud-adjacent networks), and presenting them under an AI-agent headline is a
category error, not a measurement.

## 8. Paste-ready "Limits" section for SCAN-SUMMARY.md

> ### Limits — read before citing this scan
>
> 1. **We are blind to the agent era by construction.** Only IP-editor revisions
>    carry public IPs. Logged-in editors (87.7% of revisions) and temp accounts
>    (3.2%) are unattributable from public data. In this corpus the last IP-editor
>    revision is 2025-11-04T04:48Z and the first temp-account revision is
>    2025-11-04T09:55Z — after that, anonymous-edit IPs vanish. IP visibility is
>    4.1% of 2025–2026 revisions and **0% of 2026 revisions** (20,114 temp +
>    160,018 named, all unattributable). Any AI agent editing in 2026 is invisible
>    to this method.
> 2. **Wikipedia blocks anonymous datacenter editing.** en.wikipedia refuses
>    anonymous edits from known hosting/colocation ranges, so agent egress from
>    mainstream cloud IPs would normally never produce a public IP revision. The
>    method hunts in a population the platform actively excludes.
> 3. **The 90 matches are not AI-agent evidence.** All 90 fall in 2020–2023 (zero
>    in 2024–2025, the agent-era IP-visible window); 57% carry mobile-edit tags;
>    39% are reverted; zero match any lab-specific range (OpenAI/Anthropic/
>    Perplexity). They are consistent with human VPN/corporate/mobile-carrier
>    traffic. A datacenter-IP match is a candidate lead, never attribution.
> 4. **Range maps are present-day; IPs are historical.** 2020–2023 editor IPs were
>    matched against CIDR maps retrieved 2026-10-06. IPv4 reallocation between
>    carriers and clouds over that span produces both false positives and false
>    negatives; treat matches as approximate.
> 5. **The map barely covers actual AI egress.** Of 73,818 CIDR records, 99.5% are
>    generic AWS/Azure/GCP space; lab-specific ranges are 329 records (0.45%),
>    all crawler/bot ranges that don't edit. Anthropic and OpenAI publish no
>    API/agent egress ranges; xAI, Google DeepMind, and Meta are absent entirely.
>    Residential-proxy egress — standard agent tradecraft — is invisible to range
>    matching by design. The 61,089 unmatched IPs (99.85% of IP revisions) were
>    eyeball-judged residential; no ASN census was performed.
> 6. **Selection bias.** Top-500 by September 2026 pageviews overweights
>    heavily-protected current-events articles, where IP editing is structurally
>    lowest (e.g. Deaths in 2026: 17,751 revisions, 0 IP-editor revisions), and is
>    time-indexed to the end of the window rather than the agent era.
> 7. **Coverage gaps.** Rank 222 ("european election 2014", a redirect) contributed
>    zero revisions and is missing from the aggregates — 488 articles have data,
>    not 489. API ground-truth audit verified quarters 0 and 3 only; quarters 1–2
>    (ranks 129–377) rely on puller self-checks. "Current vs reverted" status of
>    matched revisions was not computed (revert *tags* were captured: 35/90).
>
> **What this scan can honestly claim:** among 22,190 agent-era (2024–2025)
> IP-editor revisions across 488 top articles, zero matched provider-published
> infrastructure ranges — a clean zero *within the ~4–6% IP-visible slice*.
> It cannot speak to AI-agent editing activity, which would operate through temp
> accounts, logged-in sessions, residential proxies, or unpublished egress ranges.

## Grading of this review's own claims

- OBSERVED (re-derived from raw bytes): year tables, cutover timestamps, match
  year/provider/tag distributions, map composition, rank-222 empty file + missing
  aggregate row, audit-worker inventory, count reconciliation.
- INFERENCE: "colocation blocks exclude agent egress" (platform policy, well
  documented publicly, not verified in this scan); "mobile tags ⇒ human-shaped"
  (strong but inferential); "range drift ⇒ false positives" (mechanism stated,
  specific misattributions not individually proven).
- UPSTREAM: MediaWiki temp-account rollout semantics (regex `^~\d{4}-` per
  matcher; cutover date is observed, rollout policy is upstream knowledge).
