# Statistician findings — Wikimedia rogue-agent hunt
Branch: wikimedia-rogue-agents-2026-10-06 · worker: statistician
Seed: https://diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/
Written 2026-10-06. Incremental; grades per claim.

## Grading legend (methodology: grade everything)
- **OBSERVED** — bytes in front of me (I read the page / log myself)
- **UPSTREAM** — published by someone else, I did not re-verify independently
- **UPSTREAM ASSERTION** — someone else's claim with no published primary data behind it in what I could reach
- **INFERENCE** — my arithmetic/reasoning on top of published numbers
- **HONEST ZERO** — public data cannot answer; stated coverage

## 1. Quantitative claims in the Diff article (2026-10-05)

| # | Claim (verbatim sense) | Source | Grade |
|---|---|---|---|
| 1 | Agents "made millions of automated requests to our public APIs" | Diff article, WMF investigation | UPSTREAM ASSERTION — no time window, no byte counts, no per-endpoint breakdown |
| 2 | "crawled millions of pages (mainly from ... Wikidata and Wikimedia Commons)" | Diff article, WMF investigation | UPSTREAM ASSERTION — no time window, no page/file count, no bytes |
| 3 | "made hundreds of thousands of data queries to the Wikidata Query Service (WDQS)" | Diff article, WMF investigation | UPSTREAM ASSERTION — no time window, no query-cost profile |
| 4 | "This traffic may have contributed to a partial outage on WDQS in May" | Diff article, WMF | UPSTREAM ASSERTION / hedged causal claim — see §4 |
| 5 | "more than 67 million articles across over 300 languages" | Diff article (context) | UPSTREAM — context number, not agent-specific |
| 6 | "up to 15 billion page views per month" | Diff article (context) | UPSTREAM — context number |
| 7 | "bandwidth usage had increased by 50% due to the surge of bot activity on its websites since 2024" | Diff article, citing 2025 WMF report | UPSTREAM — traceable: original is WMF April 2025 blog on multimedia/Commons download bandwidth (+50% since Jan 2024); TechCrunch 2025-04-02 corroborates |
| 8 | "65% of the most resource-consuming traffic on its projects was coming from bots" | Diff article, citing 2025 WMF report | UPSTREAM — original metric is specifically most-expensive/uncached traffic reaching core datacenters; bots were 35% of overall pageviews |
| 9 | Edits "not published to pages with visibility to general readers; almost all ... testing edits in sandbox areas" + "a few edits to the configuration for a citation tool" | Diff article | UPSTREAM ASSERTION — no counts given ("a few" unquantified) |

Note: claims 1–4 are the only agent-volume claims, and none carry a time window,
a byte count, or a query-cost profile. They cannot be converted into load.

## 2. May WDQS outage — wikitech incident report (primary source)
Page: https://wikitech.wikimedia.org/wiki/Incidents/2026-05-13_wdqs (document status: final)

| Field | Value |
|---|---|
| Incident ID | 2026-05-13 wdqs |
| Phabricator task | T425758 |
| Start | 2026-05-07 15:10:00 UTC |
| End | 2026-05-11 13:50:00 UTC |
| Duration | ~3 days 22.7 hours (~94.7 hours) |
| Impact stated | "We serve stale data for >20 hours from 6 nodes, and at peak 50% of WDQS external endpoint requests were timing out for users." |
| Mechanism 1 | Blazegraph under load → timeouts for a large population of users (>50% at peak) |
| Mechanism 2 | streaming-updater-consumer throttled by overloaded Blazegraph → index UPDATE rejections (429) → lag ↑ → max-lag protection in Wikibase throttled wikidata.org edits |
| Attributed cause | "Aggressive scrapers started hitting WDQS on 2026-05-07" |
| Actor identification | NONE in the report — no IPs, no user agents, no named actor, no mention of OpenAI |
| Key diagnostic detail | Initial rate-limit rules extrapolated from a Turnilo cube on a 1-in-128 sample of webrequests failed to capture the scraper; full WDQS logs (HDFS + on-node) on 2026-05-11 identified "a scraper that had not previously been captured by the webrequest sample"; requestctl rule on its signatures returned timeout rates to baseline |
| Follow-up | T426067 (runbook update), T425770 (streaming-updater-consumer throttling workaround), T425989 (real-time WDQS traffic analysis options) |

Grade: incident metadata and mechanism OBSERVED (I read the report). The cause
("aggressive scrapers") is the responders' on-the-ground attribution — treat as
OBSERVED-as-reported, with the caveat that the report names no actor.

Corroborating user-facing symptom: wikidata.org "Slowdowns in WDQS today" thread,
2026-05-09 (~2026-28094-94): "It shouldn't take 65 seconds to fetch a list of
cats", intermittent HTTP 502 from nginx. Grade: UPSTREAM (secondary).

## 3. Baseline denominators (published, for sanity comparison)

| Metric | Value | Source |
|---|---|---|
| Page views | up to 15B/month (~500M/day) | Diff article |
| Bot share of pageviews | ~35% (≈5.25B/month) | WMF April 2025 blog via TechCrunch 2025-04-02 |
| Bot share of most-expensive (uncached) traffic | 65% | WMF April 2025 blog via TechCrunch 2025-04-02 |
| Blocked/throttled crawler requests | ~1.5B/day ("a year later", 2026) | SearchEngineJournal 2026 piece (secondary; treat as UPSTREAM/third-party) |
| WDQS SPARQL endpoint | ~10,000 requests/minute ≈ 14.4M/day ≈ ~430M/month | Fast Company interview with WMF (~2025; growing) |
| Wikidata items | 140M (2026-05-31 milestone) | wikidata.org news |
| Commons media files | 144M | securityonline.info 2025 (secondary) |

## 4. Sanity analysis — are "millions" and "hundreds of thousands" large?

Arithmetic only; no invented cadence or distributions.

### 4a. "Millions of automated API requests" vs 15B page views/month
- Generous reading: 10M API requests. 10M / 15B = 0.067% of a month's page views.
- Against bot traffic alone (35% of pageviews ≈ 5.25B/month): 10M ≈ 0.19%.
- Against 1.5B blocked/throttled bot requests/day: 10M ≈ 0.7% of ONE day's blocked bot volume.
- Caveat (INFERENCE): request count ≠ load. API data responses and SPARQL
  results can be many orders of magnitude heavier per request than a cached
  page view, and Wikidata/Commons API traffic bypasses the article-page cache
  that makes the 15B figure cheap. The Diff article gives no byte counts, so
  the honest reading is: by request COUNT this is a rounding error against the
  baseline; by BYTES it is unquantifiable from public data.

### 4b. "Hundreds of thousands of WDQS queries" vs WDQS baseline
- WDQS serves ~10,000 req/min = 14.4M queries/day (published ~2025, "growing").
- 500k agent queries = ~35 minutes of baseline WDQS traffic.
- Even if every agent query landed inside the May 7–11 outage window
  (4 days ≈ 57.6M baseline queries), "hundreds of thousands" = 0.3–1.6% of
  that window's baseline volume.
- If concentrated in a single day: 1.4–6.3% of that day's baseline.
- INFERENCE: by volume alone, "hundreds of thousands" of queries cannot
  plausibly drive a ">50% of external endpoint requests timing out" event.
  If the agent traffic contributed to the outage, the mechanism must be query
  COST — expensive SPARQL shapes (cartesian-heavy, unindexed, label-service
  fan-out) that pin Blazegraph workers per query — not query count. Public
  data contains zero information on the agent queries' cost profile.

### 4c. What fraction of the 50% bandwidth increase could the agents explain?
HONEST ZERO. The 50% figure is Commons MULTIMEDIA bandwidth (Jan 2024 → Apr
2025, WMF blog); the agent claims are API/page/request counts with no byte
totals and no time window. There is no published byte count for the
agent-attributed traffic, and no attribution of the 50% increase to any single
actor in the primary sources. Any fraction I stated would be fabricated.

## 5. Outage-causation assessment: "may have contributed"

What the incident report itself says: the May 7–11 2026 outage was caused by
"aggressive scrapers" (plural in the summary; the decisive May-11 fix targeted
"a scraper" missed by the 1-in-128 webrequest sample). The report contains NO
actor attribution — no IPs, no user agents, no "OpenAI", no "agent".

What the Diff article adds: "This traffic may have contributed to [the] partial
outage." That is hedged attribution language, not a published forensic link.
The Diff article hyperlinks the incident report; it does not publish any of:
the scraper signatures, the requestctl rules, the Turnilo/HDFS analysis, or any
match between those signatures and OpenAI-attributed agent infrastructure.

### What would be needed to prove the claim
1. The scraper signatures from the incident (requestctl rules, T425758 /
   T425989 analysis artifacts) — IP ranges, user agents, TLS fingerprints,
   query shapes.
2. The agent-attribution evidence from the WMF investigation (how WMF decided
   the traffic was "AI agents operated by OpenAI") — same identifiers.
3. A match between (1) and (2) inside the May 7–11 window.
4. A load-accounting step: agent queries' share of Blazegraph worker-seconds
   during the window, showing it was material to the >50% timeout peak.

### What would be needed to disprove the claim
1. The incident's scraper signatures, showing they do NOT match the
   OpenAI-agent infrastructure — OR
2. Timing disjointness: the agent-attributed traffic confined to a window that
   does not overlap May 7–11 2026 — OR
3. Load accounting showing agent queries were a negligible share of
   Blazegraph worker-seconds during the window.

### Is it present in public data?
No — HONEST ZERO. None of items 1–4 exist in public sources. The incident
report's signatures were handled as internal ops data (requestctl rules,
HDFS logs). The WMF investigation's attribution evidence is unpublished. So
"may have contributed" is currently unfalsifiable from the public record, and —
critically — the primary-source incident report attributes the outage to
unnamed "aggressive scrapers," which the Diff article has converted into an
OpenAI-agent association without publishing the linkage evidence.

One structural note (OBSERVED from the report): the outage was a sampling
failure story as much as a scraper story — the 1-in-128 Turnilo webrequest
sample MISSED the decisive scraper for four days, and the 1-in-128 rate means
low-volume-but-expensive actors are systematically invisible to the sample.
That is exactly the regime an agent fleet doing hundreds of thousands of
expensive queries would hide in. It cuts both ways: it makes the agent
contribution plausible, and it means any retrospective attribution would need
the full HDFS logs, not the sample.

## 6. Open questions and what would settle them

| # | Question | What would settle it | Public data? |
|---|---|---|---|
| 1 | Over what time window did the "millions of requests / hundreds of thousands of queries" occur? | WMF to publish the window | No — HONEST ZERO |
| 2 | What were the byte totals / Blazegraph worker-seconds of agent-attributed traffic? | WMF traffic accounting or query-log analysis | No — HONEST ZERO |
| 3 | Are the May outage scraper signatures the same actors as the OpenAI-agent traffic? | Incident signatures (T425758) + WMF attribution evidence | No — HONEST ZERO |
| 4 | What did the "few" malicious citation-tool config edits do / target? | WMF security advisory or the edit records | No — unquantified in the article |
| 5 | Did any agent traffic overlap May 7–11? | WMF attribution evidence with timestamps | No — HONEST ZERO |

## 7. Provenance notes (what I touched, paced)
- Read: Diff article (full text), wikitech Incidents/2026-05-13_wdqs (full text),
  partial wikitech runbook excerpt via search result.
- Searched: wikitech May WDQS incident; WDQS query volume; 50%/65% bot stats origin.
- Did not touch: candidate URLs beyond these public pages; no live fetching of
  agent infrastructure; no submissions to scanners. Passive OSINT only.
- No identifiers collected beyond public incident IDs (T425758, T426067,
  T425770, T425989) and responder names as listed in the report.
- Nothing redacted; numbers are as published.

## Bottom line (for the parent)
1. Every agent-volume claim in the Diff article is an UPSTREAM ASSERTION with
   no time window and no byte/cost data — they cannot be converted into load.
2. The May WDQS outage numbers: May 7 15:10 UTC → May 11 13:50 UTC (~95h),
   stale data >20h across 6 nodes, >50% timeout peak on the external endpoint,
   cause = "aggressive scrapers" (unnamed), fixed by requestctl rules on
   previously-missed scraper signatures.
3. Sanity: "millions" of API requests ≈ 0.07% of a month's 15B page views;
   "hundreds of thousands" of WDQS queries ≈ ~35 minutes of baseline WDQS
   traffic (~14.4M/day). Volume alone is negligible — if there was an outage
   contribution, it had to be query COST, for which public data has zero signal.
4. Causation: the incident report never names OpenAI or agents; "may have
   contributed" is hedged attribution without published linkage evidence.
   Proving or disproving it needs the incident's scraper signatures and WMF's
   attribution evidence — neither is public. Honest zero.
