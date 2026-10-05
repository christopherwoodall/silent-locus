# Zhipu (GLM) agent fleet hunt — findings (2026-10-05)

Hunt premise: the Oct 2026 Tencent Hunyuan fleet (Amap scraping via urlquery.net) is the template; a classifier gave Zhipu's GLM 26% on the fleet's code (second-highest). Look for Zhipu agent activity using the same playbook.

## Verdict: no Zhipu fleet found. All Zhipu-specific checks are clean negatives.

### urlquery checks
| Query | Hits | Verdict |
|---|---|---|
| `zhipu` keyword | 1,099 | All news/docs pages mentioning Zhipu (databreachtoday.com, careersinfosecurity.com, etc.). No agent activity. |
| `url.domain:z.ai` | 32 | Routine scans of Zhipu's public site: docs, chat spaces, subscribe pages, api root. Oct 2025–Aug 2026. No agent markers, no tags. |
| `url.domain:bigmodel.cn` | 7 | Same — public docs/API root scans. |
| `bigmodel.cn/api` | 0 | No agents calling Zhipu's API through urlquery-visible URLs. |
| `autoglm` | 29 | Pages mentioning AutoGLM (z.ai docs, bigmodel.cn, star-history, midscenejs). No fleet. |

### Tencent-TTP exclusivity check (is anyone else using the grammar?)
| Query | Hits | Verdict |
|---|---|---|
| `uqscan` | 1,217 | Overwhelmingly Amap/Tencent fleet. Only non-Amap hits are the fleet's own httpbin/nghttp2 redirectors (`redirect-to?url=...amap...&uqscan=...`). No second actor. |
| `uqtag` | 92 | 19 httpbin hits on 2026-10-04 are the `ltzh-` program family (below). Remainder coincidental. |

### Fingerprint assessment: Zhipu vs Tencent markers
| Marker | Tencent fleet (known) | Zhipu (sought) |
|---|---|---|
| Cloud ASN | AS132203 (Tencent Cloud HK) | Unknown — Zhipu runs its own 1GW domestic-chip DC; no public ASN |
| Proxy name | `hysandbox-ats` (Via header) | None known; `hysandbox` has zero web hits at all |
| Tag grammar | `uqscan=` / `uqtag=` | None found |
| Model code style | Hy4 28% (classifier) | GLM 26% — stylistic, not searchable |
| urlquery presence | 2,000+ reports | Zero agent activity |

Zhipu's vertical integration (own DC, own chips, Entity Listed since Jan 2025) means there is no clean public-cloud ASN to pivot on, unlike Tencent's AS132203.

### urlscan.io
Zero hits for `ltzh` page titles and for `sub_poi_navi`. The fleet's programs are not on urlscan (or not indexed).

## Bonus find (not Zhipu — new, unattributed)
**`ltzh-` program family**: 6 httpbin base64 programs on 2026-10-04:
- `ltzh-jina-post-inject-20261004a`
- `ltzh-jina-json-cache7d-20261004a` / `20261004b`
- `ltzh-iframe-ssr-20261004a`, `ltzh-iframe-ssr-big-20261004a`, `ltzh-iframe-www-20261004a`

Decoded behavior: POSTs Amap place URLs to `r.jina.ai` with `injectPageScript`, exfiltrates via image beacons (`/status/204?uqtag=ltzh-...&part=...&data=...`). Amap-targeting, jina-based, active 2026-10-04 — likely the Tencent fleet's alternate program family or a copycat. The `ltzh` prefix is unattributed. (Note: `ltzh` as a raw keyword is 99% noise — 207 hits spanning Oct 2025–Oct 2026 are coincidental substrings; only the 6–7 Oct 3–4 httpbin programs are signal.)

## Bottom line
No Zhipu agent fleet is observable on urlquery, urlscan, or GitHub with current markers. The Tencent TTP grammar (`uqscan=`/`uqtag=`) shows no second actor. Zhipu has no public infra fingerprint comparable to `hysandbox-ats`/AS132203 — hunting them requires either a leaked marker or model-code-style detection, neither available here. The `ltzh-` family is the actionable new lead, filed for the coordinator's Amap collection.
