# Japan archives sweep — Megalodon / gyo.tc / Japanese web
**Lane:** `2026-09-28-chinese-amap-fleet` full-sweep · **Surface:** Japan-only
**Probed:** 2026-10-04 22:48 – 2026-10-05 04:10 CDT (2026-10-05 JST)
**Operator fingerprints probed:** `*.lhr.life` tunnels (`<16-hex>.lhr.life`), `uqcors.html`, `probe.html`/`probe2.html`/`combo.html`, `uqscan=`/tag grammar, `httpbun-com.translate.goog/base64` wrapper

## Verdicts

| Archive | Verdict |
|---|---|
| **Megalodon (megalodon.jp)** | **Clean negative** on all direct probes (6 exact-URL lookups, 4 Google-index sweeps). No captures of operator tunnel/probe pages, no `uqscan` Amap URLs. Keyword (free-word) search endpoint NOT reached — delegated, see §5. |
| **gyo.tc** | **Clean negative.** `gyo.tc/<url>` is an alias for the Megalodon lookup backend (verified). No captures. No short-code index enumerable without browser. |
| **Japanese web (researcher coverage)** | **No coverage found.** No Japanese writeup of the `lhr.life`/`uq` fleet, the Amap `uqscan` fleet, or localhost.run abuse in an agent context. **One off-frame lead:** Cloudflare Radar public scan of a 16-hex `lhr.life` tunnel, 2026-08-01 (see §4). |

## 1. Megalodon — method & probes

Megalodon is submission-driven (users submit URLs; no crawler), so the index only contains what someone chose to archive. Probing = exact-URL lookup + Google-index sweep of its `魚拓リスト` pages.

### 1a. Exact-URL lookups (`GET https://megalodon.jp/?url=<urlencoded>`, via text-fetch)

A lookup page with captures shows a `取得済みの魚拓` section listing `<capture date> <title>` entries. **All six probes below returned NO such section** (page shows only `元URL(外部)` + terms) = no archived captures.

| # | Probed URL (as submitted) | Result |
|---|---|---|
| 1 | `https://7e7ff6dbbe9824.lhr.life/uqcors.html?v=1` | NEGATIVE — no captures |
| 2 | `https://7e7ff6dbbe9824.lhr.life/uqcors.html` (bare, no query) | NEGATIVE — no captures |
| 3 | `https://91ef9fc4c82a1b.lhr.life/probe2.html?n=178207704` | NEGATIVE — no captures |
| 4 | `https://amap-pc-ssr.amap.com/ssr/place/B019B0XY35?uqscan=dalian20261004next1` | NEGATIVE — no captures |
| 5 | `https://m.amap.com/detail/index/poiid=B019B0XY35?uqscan=hrefmobile1791112802` | NEGATIVE — no captures |
| 6 | via gyo.tc: `https://gyo.tc/https://7e7ff6dbbe9824.lhr.life/uqcors.html` | NEGATIVE — resolves to same Megalodon lookup, no captures |

Note: Megalodon normalizes the displayed URL (`https://<host>:443/<path>`); matching is exact-URL, so a capture of a query-variant would not surface. Probes 1+2 and 4+5 cover the main variants.

### 1b. Google-index sweeps (de-facto full-text over archived-URL titles)

| Query | Result |
|---|---|
| `site:megalodon.jp "lhr.life"` | **0 results** |
| `site:megalodon.jp uqscan` | **0 results** |
| `site:megalodon.jp uqcors OR "probe.html" lhr` | **0 results** |
| `site:megalodon.jp translate.goog base64` (httpbun-wrapper marker) | **0 results** |

(Unquoted `site:megalodon.jp lhr.life` hit one page via `scontent-lhr3-1.xx.fbcdn.net` — CDN-PoP substring noise, not the tunnel domain.)

## 2. gyo.tc — method & probes

- Homepage instruction (from megalodon.jp): prefix any URL with `gyo.tc/` to jump to the gyotaku search/capture page.
- Verified: `GET https://gyo.tc/https://7e7ff6dbbe9824.lhr.life/uqcors.html` returns the Megalodon `魚拓リスト` page for that URL — **gyo.tc/<url> is an alias of the Megalodon lookup**, same negative result.
- `site:gyo.tc lhr.life OR uqscan OR uqcors` → **0 results**.
- gyo.tc short codes (`gyo.tc/<code>`) have no enumerable public index; nothing further reachable without a browser.

## 3. Japanese web search (researcher coverage)

| Query (lang) | Result |
|---|---|
| `ウェブ魚拓 lhr.life localhost.run 魚拓` (ja) | No researcher coverage. Hits were generic Megalodon pages + unrelated dev tutorials. |
| `高德地図 スクレイピング ボット uqscan` (ja) | No coverage of the Amap fleet. Hits were travel guides + generic scraping-tool articles. |
| `"lhr.life"` (ja) | Noise (Japanese dev blogs using localhost.run for previews; a JP-authored red-team tutorial repo `hdks-bug/redteam-techniques`) + **one lead** (§4). |

## 4. LEAD (off-frame, not a negative): 16-hex `lhr.life` tunnel in Cloudflare Radar URL Scanner

- **URL:** `https://91b9ec611bbd73.lhr.life/` — 16-hex subdomain, **same shape as the operator's `<16-hex>.lhr.life` tunnels**
- **Scanned:** 2026-08-01 11:34 (Radar page locale ja-jp; time likely JST)
- **Origin:** United States, **AS14618** (Amazon); Verdict: No classification; Status: Finished
- **Source:** Cloudflare Radar URL Scanner public listing (submitter-driven scans), page indexed by Google: `https://radar.cloudflare.com/ja-jp/scan?url=https://archive.heckel.io/` (listing snapshot; entry confirmed live on re-fetch 2026-10-05)
- **Assessment:** shape matches the operator's tunnel convention, but the path is bare `/` with **no `uq`-grammar markers visible** — attribution to the `uq` operator is NOT established. Could be the same operator's bare tunnel, another localhost.run user, or unrelated. **Treat as lead.**
- **Follow-up:** resolve the scan's detail page (`radar.cloudflare.com/scan/…`) via live browser for page title/DOM/content; sweep Radar listing history / Google-indexed Radar pages for more `*.lhr.life` submissions and cluster by date.

## 5. Documented endpoints (reuse)

Per collection doctrine — no API key is not a stop. Megalodon's lookup needs no XHR at all; plain GET suffices.

- `GET https://megalodon.jp/?url=<urlencoded-target>` — server-rendered `魚拓リスト` page, **no auth, no CAPTCHA** (anti-bot checkbox since 2024 applies only to the snapshot-*capture* form, not lookups). Presence of `取得済みの魚拓` section = captures exist. Capture URLs look like `https://megalodon.jp/2025-0405-0053-03/https://<host>:443/<path>` and `https://megalodon.jp/ref/2016-0714-0216-03/<host>/<path>`. → thin wrapper = GET + grep for `取得済みの魚拓`.
- `GET https://gyo.tc/<full-target-url>` (unencoded, per homepage instructions) — alias of the Megalodon lookup.
- **NOT recovered:** the homepage's `魚拓をフリーワードで検索` (free-word search) / `日付一覧からはこちら` (date list) target URL. Text-fetch outlink mapping didn't resolve it; raw HTML unreadable (see blockers). **Delegation spec for a browser-capable agent:** open `https://megalodon.jp/` live, read page source, extract the free-word search form action and date-list href; keyword-search `lhr.life`, `uqscan`, `uqcors`, `localhost.run`; record hits with capture dates (metadata gold). Also enumerate one date-list page for 2026-06-18 and 2026-09-28..10-04 scanning titles for agent-shaped URLs.

## 6. Blockers (exact)

1. **VM egress proxy down for curl (2026-10-05 ~03:50 UTC):** `curl` via `hatch-egress-proxy:3128` hangs at `CONNECT` → rc=28 timeouts on **all** hosts (verified 3× against `https://example.com/`). Direct egress is TLS-blocked (rc=35). All HTTP work in this sweep was done via text-fetch tools instead. curl-based XHR discovery and raw-HTML reads were impossible.
2. **Megalodon outage notice** (affility.co.jp, 2026-10-02 09:00 JST): "ウェブ魚拓のmegalodon.jpにアクセスが出来なくなっています" — intermittent accessibility; text-fetch succeeded throughout this sweep.
3. **Wayback CDX API returned HTTP 500** for `web.archive.org/cdx/search/cdx?url=megalodon.jp*…` (do not retry per runtime).

## Metadata notes

- Megalodon capture entries carry **capture dates** (`2026年9月13日 14:38` format) — if the free-word search later surfaces hits, those timestamps are directly usable.
- No captures found ⇒ no new timestamps for the operator timeline from Japanese archives.
- `b.hatena.ne.jp/site/megalodon.jp/` lists recent Megalodon captures with `取得日時` + SHA-256 — a possible future tripwire for new agent-shaped submissions (not probed this round).
