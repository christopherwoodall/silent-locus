# Behavior-based fleet hunt: POLISH / TURKISH / ARABIC lanes

Date: 2026-10-04 (hunt run ~21:30–22:15 UTC)
Reference fingerprint: `../raw/analysis/PATTERN.md` (Chinese Amap fleet: `uqscan=<word><YYYYMMDD>[a-z]` tags, base64 httpbun/httpbin programs, webhook.site dead-drops, r.jina.ai/translate.goog relays, place/API systematic scans)

**Overall verdict: NO non-Chinese agent fleet found.** All three lanes are honest zeros. Two ambiguous items are logged below for completeness; neither clears the fleet bar.

Tool: `uq_htmx.py search --delay 4` (undocumented htmx endpoint, no auth). All queries --delay 4, no 429s hit. Keyword search matches submitted URLs and (observed) page content.

---

## 1. Tag-grammar shapes (`<native-word>2026`, the `<word><YYYYMMDD>[letter]` fleet signature)

| Query | Result |
|---|---|
| PL: `wyszukiwanie2026`, `zadanie2026`, `badanie2026`, `misja2026` | **0 hits each** |
| TR: `arama2026`, `gorev2026`, `arastirma2026`, `hedef2026` | **0 hits each** |
| AR (transliterated): `bahth2026`, `mahma2026`, `hadaf2026`, `wakil2026`, `muhimma2026` | **0 hits each** |

Zero native-language tag-grammar matches in all three languages. Note: Arabic script is percent-encoded in URLs; transliterated forms were used. A fleet using Arabic-script tags would be missed by these queries — residual blind spot, flagged honestly.

## 2. Map/POI services (systematic place/API scanning?)

| Query | Result |
|---|---|
| PL `targeo.pl` | 1 report (2026-01-10, `projektroza.pl`) — ordinary browsing, noise |
| PL `panoramafirm.pl` | 1 report (2026-05-17) — ordinary browsing, noise |
| TR `yandex.com.tr` | 24 reports, **but submitted URLs are all .ru/.by domains** (educube.ru, autobaner.ru, adspect.ai, etc.), matched via page content. Clustered 2026-10-03/04 — looks like SEO/ad-referrer spam cluster, not map scanning. No place IDs, no cache-buster params. Noise. |
| TR `harita` | 24 reports — ordinary Turkish sites (zirvetema.com, avrasyaproje.com.tr, hotel/gaming sites), no systematic pattern. Noise. |
| AR `2gis` | 21 reports, scattered 1/day May–Sep, ordinary sites. Noise. |
| AR `talabat` | 23 reports, scattered, ordinary/phish-adjacent sites (incl. `talabat-talabat.com` lookalike). Noise. |
| AR `opensooq` | 20 reports, scattered; few shortlink-spam (`opensooq.fjfd.click`, `iq.opensooqk.com`). Noise. |

**Verdict: no systematic place/API scanning in any language. Honest zero.**

## 3. Agentness words × carriers (`<word> httpbin`, `<word> webhook.site`)

| Query | Result |
|---|---|
| PL `agent httpbin` | 7 reports — **all Chinese Amap fleet cross-matches**: `nghttp2.org/httpbin/redirect-to → amap…uqscan=orangeisle2…`, `eu.httpbin.org/base64/<program>` (epoch-tagged fleet program), `uqscan=hzly-httpbin-1791105505`. "agent" matched fleet page content. Not Polish. |
| PL `agent webhook.site` | 3 reports — webhook.site inboxes + href.li wrapper, 2026-10-04 — **Chinese fleet dead-drop tradecraft**. Not Polish. |
| PL `dane httpbin`, `ekstrakcja httpbin`, `misja httpbin`, `misja webhook.site` | **0 each** |
| TR `ajan httpbin`, `ajan webhook.site`, `veri httpbin`, `gorev httpbin`, `misyon httpbin` | **0 each** |
| AR `wakil httpbin`, `wakil webhook.site`, `mahma httpbin`, `wakil httpbun` | **0 each** |
| AR `bayanat httpbin` | 1 report (`ismena.com`, 2026-10-04) — ordinary site, noise |

**Verdict: zero language-native agentness×carrier hits. The only carrier hits are the known Chinese fleet matching on English page content ("agent").**

## 4. Native shorteners/pastebins

| Query | Result |
|---|---|
| PL `tiny.pl` (shortener) | 12 reports — spam/malware-shaped: `tiny.pl/QV22917BR`, `tiny.pl/28c92qrdn`, `th.poundrynloweu.com/`, dub.link. Phishing/spam use, **not agent-shaped**. |
| PL `wklej.org` (pastebin) | 0 |
| TR `kisalt.one` (Turkish shortener, active) | 0 |
| AR `mukhtasar.pro` (Arabic shortener, dev project) | 0 |

**Verdict: no agent-shaped shortener/pastebin use. tiny.pl = phishing/spam noise. Honest zero.**

## 5. Fetch-proxy chains (`r.jina.ai` + language wiki/news)

| Query | Result |
|---|---|
| `r.jina.ai` (limit 24) | Dominated by Chinese Amap fleet (`r.jina.ai/https://amap-pc-ssr.amap.com/ssr/place/B…` ×3 on 2026-10-04) + misc (newspapers.com Billy Carter query, Iowa public-health CSV). **No pl/tr/ar wiki or news domains.** |
| `r.jina.ai/https://pl.wikipedia`, `…tr.wikipedia`, `…ar.wikipedia`, `jina.ai pl.wikipedia`, `jina.ai ar.wikipedia` | **0 each** |

**Verdict: zero fetch-proxy chains for these languages. Honest zero.**

## 6. Language mixing (English tag grammar on these languages' targets)

| Query | Result |
|---|---|
| `uqscan=` (limit 24) | All 24 = Chinese Amap fleet. No multilingual reuse visible in top results. (Deeper offsets not exhausted — dominated by the known fleet.) |
| `research2026` | 1 report: `familylawconsulting.org` (2026-06-21, report `e666a116-92a9-413e-afc1-aa3b403511ab`). Tag matched page content, no tag grammar in URL, single report, no burst. Likely noise; one-line log, not pursued. |
| `scan2026` | 5 reports — SharePoint "scan2026-…-scan2026-1-07.html" **phishing lures** (scanned-document theme), 2026-01-15 cluster. Not fleet. |
| `target2026` | 0 |
| `claude2026` | 0 |

**Verdict: no English-tag reuse on PL/TR/AR targets. Honest zero.**

## 7. Bursts

- TR `yandex.com.tr`: 21 reports over 2026-10-03/04 — but submitted URLs are .ru/.by, SEO/ad-referrer spam cluster, not fleet.
- No other domain showed multi-report single-day clustering tied to these languages.

## Ambiguous items (below the fleet bar, logged not claimed)

1. **Translate-wrapped httpbun probe loaders, 2026-10-04** — matched `agent httpbun` (English page content, not Arabic):
   - `2b6b941f-…` 2026-10-04T17:39 `httpbun-com.translate.goog/base64/<body id=x><script src=//a2372f6e092e1f.lhr.life/probe.js>`
   - `10ab12df-…` 2026-10-04T16:32 same domain, probe.js variant
   - `9cdc930c-…` 2026-10-04T16:23 combo.js variant
   - Plus 3 from 2026-06-21 (same lhr.life probe.js family + `TRANSLATE` title self-survey + `is.gd/eZD1hT`).
   - Shape: translate.goog-relayed httpbun base64 loader programs — echoes June-incident tradecraft (lhr.life probe.js). No tag grammar, no place/API target, only 3 reports in a day. Could be copycat/small operation or June-corpus adjacency — **not attributable to Arabic, not a fleet by our bar**. Watch item.
2. **`research2026` → `familylawconsulting.org` (2026-06-21)** — single report, keyword in page content, no fleet markers. Logged, not pursued.

## Residual blind spots (honest limits)

- Arabic-script tags are percent-encoded in URLs; only transliterated forms were queried.
- `uqscan=` offsets beyond 24 not exhausted (known-fleet-dominated).
- No full-report fetch capability in this tool (search only); carrier-URL verification limited to submitted URLs.
- Yandex/Google Maps country domains not exhaustively swept (no systematic pattern found on the main candidates).

**Final: NO new non-Chinese fleet found in Polish, Turkish, or Arabic lanes. The prize remains unclaimed.**
