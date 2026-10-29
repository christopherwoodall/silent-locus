# Wayback CDX lane — Chinese Amap fleet (2026-09-28 → 2026-10-05)

Agent: Wayback CDX lane · run 2026-10-04 ~20:35–20:55 CDT · ~20 min API work
Raw data: this dir (`cdx_*.json`)

## Queries run (CDX API, via curl)

| # | URL pattern | Window | Collapse | Result file | Rows |
|---|-------------|--------|----------|-------------|------|
| 1 | `amap-pc-ssr.amap.com*` | 20260928–20261005 | urlkey | `cdx_ssrhost_window.json` | 1,849 |
| 2 | `www.amap.com/ssr/api/getPoiInfo*` | 20260928–20261005 | urlkey | `cdx_getpoiinfo_window.json` | 0 (`[]`) |
| 3 | `amap.com/ssr*` | 20260928–20261005 | urlkey | `cdx_amapcom_ssr_window.json` | 47 |
| 4 | `m.amap.com/service*` | 20260928–20261005 | urlkey | `cdx_mamap_window.json` | 13 |
| 5 | `amap-pc-ssr.amap.com*` | 20260901–20260907 (baseline) | urlkey | `cdx_ssrhost_baseline.json` | 0 (`[]`) |
| 6 | `amap-pc-ssr.amap.com/ssr/place*` | 20260901–20260907 (baseline) | urlkey | `cdx_place_baseline.json` | 0 (`[]`) |
| 7 | `amap-pc-ssr.amap.com/ssr/place/*` | 20260928–20261005 | none | `cdx_place_nocollapse.json` | 14 |
| — | `amap-pc-ssr.amap.com/ssr/api/getPoiInfo*` | 20260901–20260907 | urlkey | `cdx_getpoiinfo_baseline.json` | 504 timeout (not retried) |
| — | `amap.com*` | 20260901–20260907 | urlkey | `cdx_amapcom_baseline.json` | 504 timeout (query too broad) |

No rate-limiting encountered (504s were query-cost timeouts, not blocks). No `uqscan=`/`uq=` tags in any captured URL (tags live in urlquery scan submissions, not archived URLs — expected negative).

## Agent-shaped patterns: FOUND (3 of 4 signals)

**1. POI overlap with fleet target set: 72/87 (83%).**
Of 87 distinct `B…` POI IDs appearing in the SSR-host captures during the fleet window,
72 match the 217 fleet target IDs mined from the raw urlquery corpus (`raw/page_*.json`).
These are the exact POIs the fleet was scraping (parks, museums, zoos, hospitals).

**2. Timing aligns with fleet activity.**
Fleet-shaped captures (place pages + bare `/ssr/api/getPoi{Info,Detail,Comment}` and
`/detail/` endpoints, anti-bot `_____tmd_____` telemetry excluded): 115 total,
heaviest on the fleet's peak day — Oct 4 contributes 84, with a burst 00:00–02:00 UTC
(17+24+7 captures) inside the fleet's 00:00–13:00 UTC active window.

**3. Parallel-capture signature.**
On Oct 4, 20 of 84 fleet-shaped captures land <60s apart, some in the same second
on different POIs (e.g. `20261004001005` and `20261004001006` on two distinct IDs) —
consistent with the fleet's 4–8 concurrent runs, not human browsing.

**4. Baseline is a clean zero.**
`amap-pc-ssr.amap.com*` and `amap-pc-ssr.amap.com/ssr/place*` both return `[]` for
Sep 1–7, 2026 — zero captures — vs 1,849 rows / 115 fleet-shaped captures in the
fleet window. (Caveat: one baseline pattern, `getPoiInfo*`, 504'd, so the baseline
for that exact path is unestablished; the host-level and place-path zeros stand.)

## Composition note

~1,700 of the 1,849 SSR-host captures are Amap's Alibaba anti-bot telemetry
(`_____tmd_____/report`, `punishTextFetch`, `page/feedback`) — the same token/beacon
endpoints the fleet's programs generate `bx-ua`/UMID tokens for. Their volume in the
archive is consistent with many agent-driven page loads being archived with the
anti-bot JS firing.

## Honest negatives

- Zero captures of `www.amap.com/ssr/api/getPoiInfo*` in-window — the fleet's API
  target as seen in urlquery submissions has no Wayback presence under that host path
  (captures live under the `amap-pc-ssr` host instead).
- No `web.archive.org/save/` URLs visible (CDX host filters can't show save-initiated
  records directly); initiator attribution is correlation, not proof.
- m.amap.com (13 rows) and amap.com/ssr (47 rows) show no fleet-shaped clustering.

## Verdict

NEW trace: Wayback holds 115 captures of the fleet's exact POI/API targets during the
fleet window — 83% POI-ID overlap, peak-day burst, parallel timing, zero baseline.
Consistent with the fleet's archive-first TTP. Not proof of agent-initiated saves,
but agent-shaped beyond reasonable coincidence.
