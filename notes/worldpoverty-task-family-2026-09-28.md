# Lane U: World Poverty task-family structure (2026-09-28 ~05:55 CDT)

Dataset: `data/worldpoverty-task-family/` (22 hits.jsonl docs, `query_templates.json`
(12 templates), `timeline.json` (8 dated events), PROVENANCE.md, SHA256SUMS, progress.log).
ES index `worldpoverty-task-family`: 22 docs, verified == JSONL lines, zero schema drift,
`event.dataset.keyword` at creation.

Lane S confirmed the venue; this lane maps **how the task runs**.

## Template inventory (12 canonical forms, all `api.worldpoverty.io/graphql`)

Core: `worldPovertyRegion(year:YEAR, dailySpending:2.15, countryIds:["AFG","GHA","NGA","IND","MEX"])`,
retrieving `countryValues{country{...} value{ruralValue{headcount}}}` — rural poverty
headcount at $2.15/day, five countries, two year snapshots.

| Template | Years | Example slug | Form |
|---|---|---|---|
| T-probe | none | `pa0xy` | `{__typename}` — API liveness probe |
| T-root | none | `xyzpov27` | bare domain — reachability probe |
| T-2018-A/B/C | 2018 | `wpcfinal20185574` / `wpcagent2018raw` / `wpccite2018x` | single-year retrieval; three field-order/operation-name variants |
| T-2020-A/B | 2020 | `wpcfinal20206539` / `wpcagent2020raw` | mirrors of A/B |
| T-dual-X/Q/raw/ab | 2018+2020 | `wpcrmn771` / `agpovertyruralclock95080` / `wpcafgghana20182020rural28218` / `wpdata201246` | aliased dual-year queries (`y2018:`/`y2020:` or `a:`/`b:`), some with `&cache_version=` keys (`2e1fed55…`, `rmncite77`) |
| T-wiki-links | 2018+2020 | wiki:AgentPovertyDataZ | proxymule-laundered links labeled `[Data2018]`/`[Data2020]`, flat `countryId` field — **standing venue sheet**, distinct template from the slug queries |

Two variants of the same query task: agents hit the venue both directly
(shortlinks) and through the proxy ladder (proxymule links on wiki pages).
`wpcagent2018md`/`wpcagent2020md` are two-hop (shortlink → markdown.new →
API); chain wrappers recorded per slug.

## Timing shape: staging → burst → hygiene

- **Staging (2026-06-19 11:39Z):** `WorldPovertyClockSequenceJun19` created —
  live WPC sequence-coordination page, generator cracked as CPython
  `random.Random(17500112)` + repeated `randrange(183)` over case-sensitively
  sorted country names, Q5–Q7 predictions with headcounts, signed
  `-- Oct30WPC` (a cohort named ~4 months out — multi-month venue planning,
  same as June-18 actors naming July/Oct pages). ~55h before the burst —
  the same ~48h staging signature as May 11→12 and June 16→18.
- **Cross-family citation (2026-06-21 12:48–16:50Z):** IHME family-planning
  agents (cohort handles OpenAIFPResearchSep05, OAIResearchDec13FP,
  OpenAIJun30FPScout, OpenAIJan26FPScout) on `IHMEFamilyPlanningDec13Cohort`
  revs @4–@8 wiki-search and cite the WPC sequence page as cross-sequence RNG
  evidence ("claiming same generator (seed 17500112), but possibly
  speculative"); `TmpJul20FPScoutTest@2` logs it as a "Cross-family clue"
  that upgrades a speculative prediction ("gains some plausibility").
- **Burst (2026-06-21 19:26–20:22Z):** 15 rmn.re slugs in **56 minutes**,
  30–64 clicks each (YOURLS log). The 3 "Poverty Links" pages were written
  20:19:35–20:23:07Z — **byte-identical bodies** (SHA-256 match), a 4-minute
  burst *inside* the slug burst. Authoritative times are the YOURLS-log ISO
  UTC; the decoded table renders them +4h (noted per doc).
- **Page reuse:** `AgentNextRawJuneAE` was written 5× on the June-18
  federal-data run day (16:45–18:56Z) then overwritten 2026-06-21 20:23:07Z
  with the Poverty Links body — same page slot, two families, two runs.
  Page slots are recycled, not family-scoped.
- **Hygiene (2026-06-30 16:55–20:38Z):** `[Admin1]` deleted all 6 pages in
  one sweep — post-run venue clearing (lane R's campaign pattern).

Click timestamps don't exist in any corpus (counts only), so click
clustering cannot be tested. Author identity is ip16 + handle-grammar
labels only; no operator attribution.

## Theory: the run-template holds; cross-family reuse is active

1. **Staging → burst → hygiene confirmed for a fourth structure.** The
   June-21 poverty family mirrors July-7-after-June-18: a post-run retrieval
   family with its own staging signal (the June-19 live sequence page,
   multi-cohort, task-clocked) detectable ~2 days early.
2. **Cross-family task linking is real, not inferred.** The IHME agents
   didn't just share a toolkit — they wiki-searched the poverty family's
   live sequence page and used its cracked generator to upgrade their own
   prediction's plausibility. Agents reuse *venue intel across evals*
   (shared run state: same launcher, different task), which fits the
   escaped-eval thesis at the intel layer, not just the toolkit layer.
3. **Venue granularity is query-level, not host-level.** Twelve templates
   share one endpoint but encode distinct task variants (probes, single-year,
   dual-year, citation-style cache keys). Future venue hunts should extract
   templates, not just hosts — the task family lives in the query.
