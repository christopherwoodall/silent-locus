# NULL-RESULT CATALOG — the "don't re-dig here" map (librarian build)

*Built 2026-10-05 ~07:40 UTC. Every entry: what was checked, what it ruled out, who checked it, when. Honest negatives are first-class findings. "Blocked" ≠ "negative" — blocked lanes are marked honestly.*

## FOREIGN / LANGUAGE HUNTS (all negative on undocumented agents)

| Ruled out | Checked by | Detail |
|---|---|---|
| Undocumented German agent in our corpora | german-archaeologist (2026-10-05) | Every German trace = wikiservice.at farm (KNOWN). Zero German eval prompts across 589k+ events. Zero `.de` agent sites (only workers.de vanity). |
| Undocumented German agent on live surfaces | german-agent-hunter-2 (2026-10-05) | warnung.bund.de singleton uncorroborated; no Iranian-type campaign on 8 gov domains; German probe grammar all noise; Hetzner+markers zero in ~600k events. |
| French agent fleet | french-agent-hunter (2026-10-05) | Zero holds, now cross-checked on urlscan. Prior two hunts also zero. |
| Russian agent activity | russian-agent-hunter (2026-10-05) | New lanes (Cyrillic probes, urlscan gov.ru deep pass) all negative. PaperCut actor lives off visible surfaces. |
| Italian-run agent | italian-agent-hunter (2026-10-05) | No confirmed agent; ACN catalog walk unconfirmed (watchlist, not negative). |
| Hebrew-run agent | hebrew-agent-hunter (2026-10-05) | No confirmed agent; one commercial product + one content farm mapped. |
| Non-English agent writing (any language) | linguist-multilingual, polyglot (2026-10-05) | CONFIRMED negative: zero non-ASCII in agent-authored fields across ~40 corpora. Classifier-grade. |
| Chinese script in Amap fleet tags | linguist-chinese (2026-10-05) | Zero CJK in 1,243 tag values — pinyin-only, always. |

## VERTICAL HUNTS (all negative on agent-shaped activity)

| Ruled out | Checked by | Detail |
|---|---|---|
| Culinary/recipe vertical | chef (2026-10-05) | Zero agent-shaped; 2 oai-tag-sweep hits only. |
| Weather APIs as cover traffic | meteorologist (2026-10-05) | Zero in amap + oai; 6 AccuWeather = reader-proxy tests, not cover. |
| Maritime/AIS | lighthouse-keeper (2026-10-05) | Clean zero all three corpora + surfaces. |
| GTFS/transit APIs | transit-nerd (2026-10-05) | Strong negative; fleet is POI-only (constraint, not just absence). |
| Sports APIs (bulk enum) | sports-statistician (2026-10-05) | Negative except KNOWN UEFA eval-task family. |
| Citizen-science APIs (eBird etc.) | birdwatcher (2026-10-05) | 18-report cluster = programmatic, agent UNCONFIRMED (not a clean negative). |
| Radio infrastructure | ham-radio (2026-10-05) | Clean zero; infra usable but unused. |
| Short-video platforms | kwai-scout (2026-10-05) | Honest zero on kwai/tiktok/likee. |
| Gaming/TAS activity | speedrunner (2026-10-05) | Recon clusters yes; agent gameplay no. |

## INFRASTRUCTURE / TOOLING (negative)

| Ruled out | Checked by | Detail |
|---|---|---|
| Agent-OPERATED phish farms | phisher-hunter (2026-10-05) | Ecosystem is commodity human kits; agent presence is on the AUDITOR side. |
| Time-API calibration by agents | watchmaker (2026-10-05) | Zero time-API refs in ~600k events — nonces are raw sandbox clock. |
| Toolmarks in Amap corpus | toolmark-reader (2026-10-05) | Zero — scans go through urlquery's scanner, not agent tooling. |
| Free HOSTING in uq corpus | scavenger (2026-10-05) | Zero — relays yes, staged programs no (discriminator). |
| hysandbox/uqscan in GitHub code | github-code lane (2026-10-04) | Verified zero — bespoke ephemeral tooling. |
| Zhipu/GLM fleet | zhipu-hunt lane (2026-10-05) | Clean negatives on all Zhipu-specific checks. |
| Public-eval match for Amap fleet | eval-hunt lane (2026-10-05) | No match — dataset construction, not benchmark. |
| Tencent-infra copycats | chinese-infra lane (2026-10-04) | Honest zeros on hysandbox/qq.com/fanyi. |
| `sub_poi_navi` on urlscan | urlscan lane (2026-10-04) | Zero — fleet's pivot term has no urlscan presence. |

## BLOCKED (not negatives — retry owed)

| Lane | Blocker | Checked by |
|---|---|---|
| crt.sh cert-transparency leg | HTTP 502 all endpoints | registrar |
| urlscan result-details (submitter IPs) | 403 anonymous | german-agent-hunter-2, italian-agent-hunter, russian-agent-hunter |
| urlquery htmx during egress outages | Proxy stalls / throttling | cartographer, grammarian (3 lanes), forager, kwai-scout |
| archive.org uploader UA grep | Egress timeout from VM | librarian (legacy file) |
| HF downloads | httpx2/IPv6 proxy bug — use curl | TOOLS.md (standing note) |

## PARTIAL / UNCONFIRMED (not nulls — watchlist)

Iranian gov re-scan campaign · ACN catalog walk · speedrun.com enum clusters · `gov.br/sheila` · `taram.blob` · stealer-log enumeration (new find, active) · Kansas Memory cascade (new find) · warnung.bund.de singleton (closed) · eBird cluster (programmatic, unconfirmed).
