# GitHub Code-Search Hunt: Chinese Agent Fleet Fingerprints

Date: 2026-10-05
Method: `gh search code` / `repos` / `commits` + web search. 13 queries total.

## Verdict

**The article's "no public documentation" claim for `hysandbox` is VERIFIED.** Zero relevant hits across GitHub code, repos, commits, and the web. The fleet's fingerprints (`uqscan=`, `sub_poi_navi`, `AMAPREDIRECT`, Amap+Baxia) have **zero presence** in GitHub code. The fleet's tooling is bespoke and ephemeral — generated programs submitted to urlquery, never committed to repos.

## Per-query results

| # | Query | Surface | Hits | Verdict |
|---|---|---|---|---|
| 1 | `hysandbox` | code | 20 | All coincidental "sandbox" substrings (physandbox, why-sandbox, sandboxpool, agent-sandbox, TypographySandbox). No Tencent, no proxy. |
| 2 | `hysandbox-ats` | code | 0 | Exact string absent. |
| 3 | `hysandbox` | repos | 0 | No repositories. |
| 4 | `hysandbox` | commits | 0 | No commits. |
| 5 | `hysandbox tencent proxy` | web | 0 relevant | Only coincidental: Tencent Cloud docs, HunyuanDiT CVE, browser-sandbox papers. |
| 6 | `uqscan` | code | 20 | All coincidental: VB6 `uqscan.frm` (mgrandau/ai-session-tracker-mcp), `uque.h`, OCR text, expired-domain lists. No `uqscan=` param code anywhere. |
| 7 | `getPoiInfo` | code | 15 | All generic "PoiInfo" class names (WoW addons, Alipay SDK, OpenStreetMap). None is Amap's `getPoiInfo` API. |
| 8 | `sub_poi_navi` | code | 0 | Fleet's Amap response field appears nowhere. Strong negative. |
| 9 | `clk_ratio` | code | 10 | All hardware clock ratios (FPGA, firmware). Coincidental. |
| 10 | `AMAPREDIRECT` | code | 10 | Coincidental substring matches (blog posts, Nokia Maps sample). None is the fleet's `AMAPREDIRECT1790825109` title string. |
| 11 | `Amap bootstrap` | code | 10 | Generic map+bootstrap combos. Coincidental. |
| 12 | `Amap Baxia` | code | 0 | Absent. |
| 13 | `amap.com webhook.site` | code | 0 | No combined dead-drop + Amap code. |

## Interpretation

- The fleet leaves no static code footprint on GitHub. Its programs exist only as urlquery submissions (transient scanner artifacts) and webhook.site inboxes (expiring).
- This is itself a finding: the fleet's operational security (or just its architecture — ephemeral generated programs) means **urlquery/webhook.site are the only public surfaces** where it can be observed. GitHub is a dead end for this actor.
- Contrast with the June OpenAI incidents, which left wiki message boards, RubyGems packages, and HF artifacts. The Tencent fleet is quieter by an order of magnitude.
- Watchlist additions (for urlquery/urlscan monitoring, not GitHub): `uqscan=`/`uqtag=` params, `sub_poi_navi`, `AMAPREDIRECT`, `Amap Baxia JSONP`, `hysandbox-ats` Via header.

## Representative coincidental hits (documented to avoid re-triage)

- `cirosantilli/expired-domain-names-by-day-*` — bulk domain lists matching "uq"/"hysandbox" substrings; noise.
- `mgrandau/ai-session-tracker-mcp` `evidence/issue-18/interactions.json` — VB6 `uqscan.frm` filename; unrelated.
- `bububa/opentaobao` `model/campus/PoiInfo.go`, `alipay/alipay-sdk-java-all` — generic POI model classes; unrelated to Amap's API.
