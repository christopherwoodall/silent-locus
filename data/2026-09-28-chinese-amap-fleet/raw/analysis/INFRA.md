# INFRA.md — Fleet web infrastructure inventory (2026-09-28 → 2026-10-05)

Enumerated from urlquery reports in the fleet window. Counts are urlquery submissions (lower bounds — the fleet's full traffic is larger).

## JS sandboxes / live-code pages
| Service | Reports | Used for | Example |
|---|---|---|---|
| `livecodes.io` | 26 | Staging agent programs ("Amap Baxia JSONP" anti-bot loader) | report `f79e94fb` (per swarmcha.se) |
| `httpbun.com` | 65 | Staging base64-encoded programs (`/base64/<blob>`), exfil endpoints (`/anything/gcresult`) | `51ca21be` (AMAPREDIRECT program) |

## Redirectors
| Service | Reports | Used for | Example |
|---|---|---|---|
| `href.li` | 19 | Wrapping httpbun programs and Amap URLs (`href.li/?https://…`) | `563ba9f6` (Chengdu Zoo readout chain) |
| `httpbingo` | (per report) | Redirect to Amap place pages | report `7517916e` (per swarmcha.se) |

## CORS proxies / text-extraction relays
| Service | Reports | Used for | Example |
|---|---|---|---|
| `r.jina.ai` | (per report; 0 in amap.com-submitted set — relay reports carry jina URLs) | Fetching Amap pages as Markdown, bypassing login | `437d7a14` (`r.jina.ai/https://amap-pc-ssr.amap.com/ssr/place/B001C94YUZ`) |
| `api.microlink.io` | (per report) | Puppeteer interception of `getPoiInfo` + anti-bot headers | report `6694c078` (per swarmcha.se) |
| `translate.goog` | (per report) | Translate-proxy fetch | cited in report relay taxonomy |
| `allorigins` | (per report) | CORS proxy | cited in report relay taxonomy |
| `fanyi.baidu.com` | 2 (fleet use) | **Baidu Translate as fetch proxy** (`/transpage?query=<amap-url>&from=zh&to=en&source=url&render=1`) — NEW, not in the report | `968009e0`, `a255dfb9` (both 2026-10-04) |

## URL shorteners
| Service | Reports | Used for | Example |
|---|---|---|---|
| `spoo.me` | 1 (in getPoiInfo pivot) | Shortened link in fleet-adjacent traffic | (pivot find, verify) |

## Dead-drop / exfil
| Service | Reports | Used for | Example |
|---|---|---|---|
| `webhook.site` | 3 (urlquery submissions; 14 inboxes via webhook.site API per report) | Result exfiltration; inboxes created from Tencent Cloud via `python-requests/2.32.5` | `97f0619b` (inbox `6ddc559e…` as submitted URL) |

## Paste sites
| Service | Reports | Used for | Example |
|---|---|---|---|
| `dpaste.com` | (per report) | Fleet-internal pastes | `dpaste.com/H49755QXK` |
| `paste.page` | (per report) | Fleet-internal pastes | `paste.page/amap-wangshan-6s3kvk5i` |
| `paste.c-net.org` | (per report) | Fleet-internal pastes | `paste.c-net.org/EventRefined` |

## Watchlist (new IOCs from this hunt)
- `fanyi.baidu.com/transpage` — Baidu Translate used as agent fetch proxy (mirrors translate.goog tradecraft, Chinese infra).
- `hysandbox-ats` — Via-header proxy marker (Tencent Cloud).
- `httpbun.com/base64/` + `href.li/?` — program staging + redirector chain.
- `uqscan=` / `uq=` tag grammar with pinyin fragments.
