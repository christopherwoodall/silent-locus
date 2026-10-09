# Chinese-infra-equivalents lane — FINDINGS

Lane: pivot urlquery on the Tencent Hunyuan agent fleet's infrastructure markers to find
the same actor or copycat infrastructure on Chinese infra (Tencent/Alibaba Cloud).
Session: 2026-10-04 ~20:35–21:05 CDT. All queries via `uq.py search`, 2s sleeps, no 429s.
Raw JSON in this directory. Nothing pushed to git.

## Queries and counts

| Query | Hits | Verdict |
|---|---|---|
| `hysandbox` (all-time) | 0 | **Honest zero.** Proxy name `hysandbox-ats` appears nowhere in urlquery outside the known fleet. |
| `url.domain:qq.com date:[2026-09-28 TO 2026-10-05]` | 0 | Honest zero. |
| `url.domain:alibaba.com date:[2026-09-28 TO 2026-10-05]` | 1 | Background. Plain `alibaba.com` homepage scan, 2026-09-29; target IP 47.246.131.198 (AS45102 Alibaba US); default urlquery Firefox UA; no tags, no agent shape. |
| `fanyi.baidu.com date:[2026-09-28 TO 2026-10-05]` | 11 | 6 = fleet's own Amap scraping (see below); 5 background (wenruya.com, ruoto.se, 737f.7370294.cc, connectmeinforma.com webinar, baidu.com homepage). |
| `url.domain:fanyi.baidu.com date:[2026-05-01 TO 2026-09-27]` | 0 | Honest zero. |
| `fanyi.baidu.com/transpage date:[2026-05-01 TO 2026-09-27]` | 0 | Honest zero. |
| `fanyi.baidu.com` (all-time, 593 hits, all 6 pages pulled) | 593 | **Transpage relay has NO other users.** Only 6 `transpage` URLs in the entire May–Oct corpus and all 6 are the fleet's own 2026-10-04 Amap scrapes. The other 587 are routine fanyi.baidu.com homepage/main-path scans. |
| `url.domain:amap.com date:[2026-09-28 TO 2026-10-05]` | 1977 (1973 unique) | Fleet window footprint: 391 × `getPoiInfo` API scrapes; date spike 2026-10-04 (1722 reports); remainder is regular place/poi-detail/search page shapes. |
| `url.domain:amap.com date:[2026-05-01 TO 2026-09-27]` | 1 | Background. `ditu.amap.com/place/B00155IVBV`, 2026-08-25; plain place page, no API shape, no markers. |
| `uq=baidu` (all-time) | 0 | **Fleet-exclusive program marker.** The fleet's in-window transpage URLs carry inner nonce params `uq=baidupc20261004` / `uq=baidumobile20261004` (`<platform><date>` nonce scheme); zero other users in the corpus. |
| `url.domain:webhook.site date:[2026-09-28 TO 2026-10-05]` | 3 | Fleet's own: 2 inbox-UUID URLs on 2026-10-04 (`webhook.site/0a947514-…`, `webhook.site/6ddc559e-…`) + 1 homepage scan. Consistent with fleet inbox creation; no second actor. |
| `python-requests amap` | 2465 (keyword OR) | Not discriminative; 0 `python-requests` scan-UAs in first page. |
| `python-requests/2.32.5` (keyword) | 3 | Background noise: casino/spam domains (levos-casino.xyz, la-taille-rouge.webnode.fr, goldicasinos.xyz), May/Jul 2026 + Jan 2026, no Chinese targets, none in fleet window. |

## Fleet's confirmed in-window Amap/transpage shapes (for cross-lane reference)

- `fanyi.baidu.com/transpage?query=https%3A%2F%2Famap-pc-ssr.amap.com%2Fssr%2Fapi%2FgetPoiInfo%3Fid%3D<POIID>[%26user_loc%3D<lng>%2C<lat>]&from=zh&to=en&source=url&render=1`
- `fanyi.baidu.com/transpage?query=https%3A%2F%2Fm.amap.com%2Fpoi%2Fdetail%3Fpoiid%3D<POIID>%26uq%3Dbaidumobile20261004%26from%3Dzh%26to%3Den%26source%3Durl%26render%3D1`
- `fanyi.baidu.com/transpage?query=https%3A%2F%2Fditu.amap.com%2Fssr%2Fplace%2F<POIID>%3Fuq%3Dbaidupc20261004%26from%3Dzh%26to%3Den%26source%3Durl%26render%3D1`
- One `href.li/?https://fanyi.baidu.com/transpage?...` redirect-wrapped variant (same fleet run).
- Report IDs (2026-10-04): `968009e0-4728-499c-8ebd-ef47cf6ae8b8`, `a255dfb9-18b9-4994-904f-2cc57ae9f611`, `c8b94294-6a88-49d0-ade0-0d1ab25ea88f`, `426aad05-92e6-4cbb-a92d-3615b8784113`, `0210ba6e-b7b8-430f-92b6-aaa5b58632b6`, `d1e61961-648d-42a5-8fb7-77476f1dc7ff`.

## Verdicts

1. **No copycat / second actor found on Chinese infra.** The `hysandbox` proxy name, the `fanyi.baidu.com/transpage?...&from=zh&to=en&source=url&render=1` relay signature, and the `uq=baidu<platform><date>` nonce marker are all fleet-exclusive in urlquery's corpus — zero other users.
2. **Pre-fleet Amap activity is background noise** (1 plain place page, Aug 2026).
3. **Attribution limit (honest):** urlquery reports expose scan-target IPs and the urlquery scanner's UA, not the submitter's IP/UA — so same-actor attribution across reports must rest on URL program shapes, which is exactly what was pivoted on. The `python-requests/2.32.5` fleet UA is not recoverable from urlquery reports (only appears as page-content keyword hits: 3 casino-spam false positives).
4. **Open follow-up (not run this session):** a live pivot on Tencent Cloud HK netblocks (AS132203) in urlscan.io or other scan corpora for `getPoiInfo`-shaped URLs, and the `uq=baidu<date>` nonce with future dates — the nonce embeds the run date, so new runs would be `uq=baidupc20261005+`.
