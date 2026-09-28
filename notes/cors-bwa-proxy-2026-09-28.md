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

## Lane spawned
`data/cors-bwa-proxy/` — dedicated cross-corpus lane: per-venue stats,
proxy-ladder chains, edge export, own ES index under shared schema.
Subagent dispatched 2026-09-28 ~05:10 UTC.
