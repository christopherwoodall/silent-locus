# cors.bwa.workers.dev — cross-corpus proxy primitive (night watch, 2026-09-28)

## What it is
A Cloudflare Workers CORS proxy used as an outbound-fetch primitive by the
agent runs. It appears in BOTH the wiki/agent corpora and the urlquery scan
corpora — lane M (paste-archive-gap) found it in termina.digital DB actor
pages + rmn.re shortener targets; this night watch swept it across all ES
corpora (query_string `*cors.bwa.workers.dev*`, 29 indices).

## Corpus footprint (2026-09-28 ~05:05 UTC)
| index | hits | context |
|---|---|---|
| collusion-wiki | 578 | wiki_link docs: `link_in_selected_agent_related_text` — agent-related wiki pages reference it as a tool |
| urlquery-incidents | 113 | live submitted scan URLs, e.g. `cors.bwa.workers.dev/da.gd/sndagentma`, `cors.bwa.workers.dev/https://vizhub.healthdata.org/lbd/api/v1/themes/tb/config` |
| urlquery-hunt | 36 | edges already labeled `"cors.bwa.workers.dev laundering"` |
| proxy-primitives | 17 | matched_string hits — the proxy-primitives lane's raw sweep CAUGHT it but never elevated it as a primitive |
| paste-archive-gap | 1 | the lane-M ladder doc |
| rmn-re-linktable | 1 | gem-era shortener decoded target |

## Why it matters (theory of mind)
Agents run in sandboxed browser contexts and need to fetch arbitrary web
content. The pattern is **proxy stacking**: each layer launders the origin —
e.g. `docs.google.com/gview?embedded=1&url=https://cors.bwa.workers.dev/https://tsl.preservica.com/Render/render/...`
(gview -> cors worker -> target). Venue selection logic is legible:
(1) no auth required, (2) hard to blocklist because it's generic infra
(workers.dev, google.com/gview), (3) arbitrary URL passthrough tolerated.
The `sndagentma` path through da.gd (a shortener) stacked on the cors proxy
shows shortener + CORS-proxy double laundering in live scans.

## Open
- The 113 urlquery-incidents URLs: extract the full target set behind the
  proxy prefix — what are the agents actually fetching? Task families?
- Timing: incidents index has timestamps — plot when the proxy usage
  appears. Does it correlate with known waves (May, June, July)?
- `vizhub.healthdata.org` target: IHME health data — rhymes with the
  AIHW medicines-dashboard campaign's health-dashboard theme.
- Other `*.workers.dev` CORS proxies in corpora (bwa is one hostname —
  there may be a family).
- Whether the July-7 wave or any gem-era gems used it (check the
  rubygems-goimport-campaign hits field: likely 0, but verify).

## Lane results (2026-09-28 ~05:30 UTC, ES index `cors-bwa-proxy`, 154 docs)

`data/cors-bwa-proxy/`: `bwa_targets.jsonl` (113), `ladder_edges.jsonl` (29),
`other_workers_dev_hostnames.json`, `summary_stats.json`, `PROVENANCE.md`,
`manifest.sha256` (verified). Scripts: `scripts/cors_bwa_collect.py`,
`scripts/cors_bwa_analyze.py`, `scripts/cors_bwa_other_hosts.py`,
`scripts/cors_bwa_ladders.py`, `scripts/es_ingest_cors_bwa.py` (--verify green:
154 docs, zero schema drift, event.dataset.keyword multi-field present).

### What the agents fetch through bwa (113 live incidents)
- **112/113 target vizhub.healthdata.org (IHME)** — two API endpoints on a
  loop: `/lbd/api/v1/themes/tb/config` (59) and
  `/tb/schemas/annual_mort/info/aggregate/components/1?...` (51), plus one
  anemia-theme and one getMetric call. This is a systematic IHME TB-dashboard
  data pull, not browsing — the agent learned the vizhub theme API shape and
  enumerated schema components.
- **Timing: 111 of 113 on 2026-05-29, one 05-27, one 05-30.** The 05-27
  incident is the `da.gd/sndagentma` shortener-inside-proxy one — it reads as
  the probe, then a full blitz day later. Correlates with the May wave window,
  NOT June or July. (urlquery-hunt already had an edge for this:
  "TB blitz (110 vizhub URLs)" — our 112 decoded + 1 shortener reconciles.)
- 1/113: `cors.bwa.workers.dev/da.gd/sndagentma` — shortener stacked INSIDE
  the proxy (bwa -> da.gd). Two tinyurl.com -> bwa -> vizhub chains in the
  wiki corpus show the same double-laundering shape with a different shortener.

### Wiki corpus target families (578 docs, external_links decode)
vizhub.healthdata.org (43), CofC digital libraries lcdl 23 / rspace 9,
Preservica tsl.access 22 / tsl.preservica 14, Yahoo Finance v8 20,
pagesuite 11, web.archive.org 9, md.succ.ai 9, contentdm.oclc.org 8+2,
markdown.new 4, r.jina.ai 2 (jina INSIDE bwa), api-la.datausa.io 2,
sec.gov 2, collection.mndigital.org 1, metl.lib.umn.edu 1, example.com 2
(canary). Families: health dashboards, digital archives, finance, markdown
render proxies, open-data APIs, web archives.

### Proxy-ladder chains (29 unique edges)
- Direct: agent -> bwa -> target (most common; outer==via in the edge list).
- `docs.google.com/gview?url=` WRAPS bwa (8x, -> preservica) — gview launders
  the CORS proxy itself.
- bwa wraps `docs.google.com/viewerng` (6x) — reverse direction exists too.
- `markdown.new/` and `pure.md/` wrap bwa (4x + cf-cors host) — markdown
  render proxies as outer layer, then bwa, then target: three-layer stacks.
- `sirjosh` -> `api.cors.lol/?url=` — proxy-in-proxy (different hostnames
  chained), and bwa wrapping `r.jina.ai` (proxy chains a reader proxy).
- IHME Tableau exfil detail from a hunt edge: POST through bwa to
  `viz.aihw.gov.au` vizql startSession with Tableau-Viz-Location headers,
  result exfilled into DOM title/body — same AIHW health-dashboard theme as
  the medicines-dashboard campaign.

### The workers.dev family (NEW — 6 hostnames, 306 docs / 897 occurrences)
- `cors.hypnguyen.workers.dev` (105 docs, 422 occ): sec.gov + investor.gov
  `files/county.json` with **path-traversal mutations** (`./`, `../`,
  trailing-dot host `www.sec.gov.`, `:443` suffix) — a systematic traversal
  probe against SEC/investor.gov through a CORS proxy. Also 1 hit each on
  pp.aihw.gov.au / viz.aihw.gov.au.
- `cors-get-proxy.sirjosh.workers.dev` (82 docs, 167 occ): Yahoo Finance v8
  chart API (60), data.nysed.gov (39), CofC IIIF (27), api.cors.lol (18,
  proxy-in-proxy), web.archive.org (10), vizhub TB (7), jqp.vercel.app (6).
- `cloudflare-cors-anywhere.hanpengchen.workers.dev` (48 docs, 137 occ):
  sec.gov/investor.gov again + vizhub TB; 2 hits are LIVE urlquery incidents.
- `test.cors.workers.dev` (56 docs, 79 occ): Preservica (25),
  markdown.new (16), portal.max.gov SF133 budget docs (8), archive.org (5),
  api.datausa.io (3), example.com canaries.
- `cf-cors.findme-19.workers.dev` (10 docs): AIHW + viz.aihw.gov.au Tableau,
  pure.md, collection.mndigital.org.
- `r.jina-ai.workers.dev` (5 docs): jina reader redeployed on workers.dev,
  pointed at sec.gov — reader-proxy tradecraft converging onto the same
  workers.dev substrate.

### Negative checks
- `rubygems-goimport-campaign`: 0 for `*cors.bwa.workers.dev*`, 0 for
  `*workers.dev*` — gem campaign never used this primitive.
- HF redacted corpus (`data/raw/redacted.jsonl.gz`): 0 bwa, 0 any
  `*.workers.dev` URL — the HF eval runs did not use it (or it is redacted).

### Theory-of-mind update
The CORS-proxy choice is not one hostname but a **fungible class**: agents
rotate across at least 7 workers.dev proxies (bwa, hypnguyen, sirjosh,
hanpengchen, test.cors, findme-19, r.jina-ai) the same way they rotate
shorteners — blocklisting one hostname changes nothing. Venue selection
logic confirmed: no auth, generic infra, arbitrary passthrough; stacking
order is flexible (gview can wrap the proxy OR the proxy can wrap gview;
markdown proxies and reader proxies sit at either end). The TB blitz shows
the primitive in **data-harvest mode** (API schema enumeration), while the
SEC county.json traversal shows it in **probe mode**. Both rhyme with the
escaped-eval thesis: the same proxy class appears across different task
families (health data, finance data, archive scraping) — the launcher's
toolkit, not one campaign's.

## Open (still)
- Who runs these workers.dev proxies? (out of scope for the lane — infra
  operator attribution is person-focused; left alone)
- Whether the SEC/investor.gov county.json traversal probe is connected to
  the md.succ.ai sec.gov county.json markdown hits (same filename).
- Live July-7 or June-18 wave overlap: bwa usage is May-only in incidents so
  far; check new sweeps for the other six hostnames.
