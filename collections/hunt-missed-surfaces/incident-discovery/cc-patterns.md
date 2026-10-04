# Common Crawl machinery-grammar sweep

Date: 2026-10-03. Read-only. `~/workspace/silent-locus/collections/hunt-missed-surfaces/incident-discovery/sweep.py`
(idempotent, 2s pacing, 120 queries, 0 errors). Raw: `query-log.jsonl`, `hits.jsonl`.

## Method note (important)
The CC index server (`index.commoncrawl.org/<COLL>-index`) does **not** honor regex in
`filter=` — `filter=url:.*zz=oai.*` silently fails. Filters are **literal substrings**
on the field (`filter=urlkey:<literal>`), proven with a `utm_source` positive control.
All patterns below ran as literal substrings against SURT urlkeys.

- Crawls: CC-MAIN-2026-25 (Jun 5–18, incident window), CC-MAIN-2026-21 (May 8–21),
  CC-MAIN-2026-30 (Jul 10–23), CC-MAIN-2026-17 (Apr 10–23).
- Domains (`matchType=domain`): ed.gov, sec.gov, bea.gov, census.gov, gc.ca.
- Patterns: `zz=oai`, `zzbulk`, `x=0.`, `prepnonce`, `wbdisable`, `openai_research`.

## Results

### Positive control: NEGATIVE (expected, first-class)
`zz=oai` → **zero captures** on all 5 domains across all 4 crawls. The 14,941-tagged
DoE fuzz run (Jun 17) exists in no Common Crawl index. Consistent with the prior
finding: the fuzz traffic's only third-party record is Arquivo.pt.

### zzbulk / prepnonce / x=0. / openai_research: zero everywhere
All four patterns return "No Captures found" on every domain × crawl. 116 of 120
queries are clean zeros.

### wbdisable: real hits, BENIGN — and a correction
6 real captures, all `wbdisable=true` on Canadian government hosts:

| crawl | timestamp | host | url (truncated) | status |
|---|---|---|---|---|
| 2026-21 | 20260516164158 | fnp-ppn.aadnc-aandc.gc.ca | /fnp/Main/Search/FNMain.aspx?BAND_NUMBER=22&lang=eng&wbdisable=true | 200 |
| 2026-21 | 20260510081235 | fnp-ppn.aadnc-aandc.gc.ca | /fnp/Main/Search/SearchFN.aspx?lang=eng&wbdisable=true | 200 |
| 2026-30 | 20260716140316 | fnp-ppn.aadnc-aandc.gc.ca | /fnp/Main/Search/FNGovernance.aspx?BAND_NUMBER=138&lang=eng&wbdisable=true | 200 |
| 2026-30 | 20260714170829 | agr.gc.ca | /eng/.../overview-of-thecanadian-agriculture-and-agri-food-sector-2018/?id=1605883547264&wbdisable=true | 302 |
| 2026-30 | 20260721165749 | www.bst.gc.ca | /fra/recommandations-recommendations/aviation/2007/rec-a0706.html?wbdisable=true | 200 |
| 2026-30 | 20260714124634 | www.cannor.gc.ca | /eng/1351104567432/1351104589057?wbdisable=true | 200 |

`wbdisable=true` is a **native Government of Canada Web Experience Toolkit (WET)
parameter** (disables WET enhancements) — documented GC web practice, not an
agent anti-archive trick. These are ordinary crawls of GC sites using their own
documented query param.

**Correction to the hunt:** the 9 `wbdisable` captures in the LAC incident traffic
were the agent using the target's *own documented parameter*, not inventing
evasion. This supports the theory-of-mind read: the agent works with the site's
native conventions (docs, params, frameworks), not against them.

## Verdict
- **No new incidents.** No host outside our known set carries the machinery grammar
  in any of the four 2026 crawl indexes.
- The machinery-first play stands as a method (literal-substring filters on urlkey
  are now a proven technique), but Common Crawl holds no agent fuzz-traffic for
  these markers — the traces live in Arquivo.pt (DoE) and Wayback (county.json burst).
