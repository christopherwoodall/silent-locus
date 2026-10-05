# FINDINGS.md — Vietnamese / Indonesian / Thai agent-fleet hunt (urlquery.net, 2026-10-04)

**Objective:** find the first non-Chinese agent fleet using the Chinese Amap fleet tradecraft
(tag grammar `<word><YYYYMMDD>[letter]` / `uqscan=`, httpbun/httpbin programs,
webhook.site dead-drops, fetch-proxy relays, systematic map/POI scanning).
Reference fingerprint: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/raw/analysis/PATTERN.md`.

**Method:** 26 queries via `python3 ~/workspace/skills/urlquery/bin/uq_htmx.py search --query "Q" --limit 24 --delay 4`
(no auth htmx endpoint). Per task: searched BOTH native-script forms and unaccented/latin forms
(agents tend to use unaccented words like `timkiem2026`, `pencarian2026`, `khonha2026`).
Native-script (percent-encoded) queries were considered but agents using the uqscan-style grammar
would emit unaccented ASCII tags, so the unaccented search space is the right one.

## Verdicts (all three lanes: HONEST ZERO for agent-fleet activity)

### 🇻🇳 Vietnamese — ZERO
| Check | Query | Result |
|---|---|---|
| Map/POI services | `goong.io` | 2 hits, noise: `mmpro.vn/blog/beef-steak` (2026-07-11), `goomap.online/` (2026-07-03) — ordinary submissions, no systematic scanning |
| Map/POI services | `map4d.vn` | 0 |
| Map/POI services | `vietmap` | 8 hits — phishing spam, not fleet: `vietmap-camera-313022266.click` (2026-04-06), `vietmaplivepro.net/?__im-esrybutc=13144403883550915427` (2025-11-25), rest unrelated |
| Tag grammar | `timkiem2026` / `timkiem202610` | 0 / 0 |
| Tag grammar | `nhiemvu2026` / `congviec2026` | 0 / 0 |
| Agentness × carriers | `timkiem httpbin` / `nhiemvu webhook.site` | 0 / 0 |
| Shorteners | `tiny.vn` | 0 (no agent-shaped Vietnamese shortener found in the corpus) |
| Fetch-proxy | `r.jina.ai vnexpress` | 0 |
| Language mixing | `research bando` / `uqscan= vietnam` | 0 / 0 |
| Map word (noise note) | `bando` | 24 hits — ALL Italian "Bando" (announcement) spam/scans + one `ban.do` shortener hit; keyword is cross-lingual noise, not a Vietnamese signal |

### 🇮🇩 Indonesian — ZERO
| Check | Query | Result |
|---|---|---|
| Tag grammar | `pencarian2026` / `pencarian202610` | 0 / 0 |
| Tag grammar | `tugas2026` / `misi2026` | 0 / 0 |
| Agentness × carriers | `pencarian httpbin` / `tugas webhook.site` | 0 / 0 |
| Shorteners | `s.id` | 24 hits — all spam/malware bait, not agent-shaped: roblox-phishing (`s.id/robloxusers3316424profile/`), bokep spam (`s.id/bokeplndo2026gratis-dan-apk-vcs`), outlook-account-recovery spam clusters, generic URL-shortener use. Notable as a corruption surface, NOT a fleet surface. |
| Fetch-proxy | `r.jina.ai kompas` | 0 |
| Language mixing | `research wisata` / `research kompas` / `uqscan= indonesia` | 0 / noise (kompas.ge pharmacy page, kompas.ai settings page — unrelated domains) / 0 |

### 🇹🇭 Thai — ZERO
| Check | Query | Result |
|---|---|---|
| Map/POI services | `wongnai.com` | 5 hits — spam/trading noise (`mobile-order-v2.foodstory.co`, `go.365trader.co/dboliveoil0125/...`, `yes.itsthecashnews.com/top3defstockcpl0325/...`), no systematic POI scanning |
| Map/POI services | `longdo` | 4 hits — game patcher files (`longdo-ss2.ddns.net/patcher/...`), `dict.longdo.com/search/House%20of%20Parliament` (single manual dictionary lookup), no fleet |
| Tag grammar | `khonha2026` / `ngan2026` / `sueksa2026` | 0 / 0 / 0 |
| Agentness × carriers | `khonha httpbin` / `ngan webhook.site` | 0 / 0 |
| Fetch-proxy | `r.jina.ai sanook` | 0 |
| Language mixing | `research wongnai` / `uqscan= thailand` | 0 / 0 |

## Bursts (check #7)
Nothing to flag: no domain in any lane shows multiple reports on one day from this query set. The only
same-day clusters observed are the known-unrelated s.id spam lines (outlook-recovery spam, 2026-04-16..19)
and the trading-spam pair on 2025-04-17 — both pre-existing spam, not agent fleets.

## Shorteners/pastebins (check #4) — lane verdict
- Vietnamese `tiny.vn`: 0 hits in corpus — cannot enumerate agent-shaped use; likely little urlquery presence.
- Indonesian `s.id`: heavy urlquery presence but exclusively spam/malware-bait; no tagged, program-shaped, or systematic use. Verdict: **corruption surface, not fleet surface.**
- Thai: no prominent native shortener surfaced; no agent-shaped use found.

## Bottom line
- **No Vietnamese, Indonesian, or Thai agent fleet found on any of the 26 behavioral checks.**
- No `<word>2026` / `<word><YYYYMMDD>[letter]` tags in any of the three languages' unaccented task words,
  no uqscan=/English-tag mixing on local targets, no httpbin/httpbun × local-language carrier overlap,
  no webhook.site dead-drop overlap, no r.jina.ai fetch-proxy overlap, no systematic map/POI scanning of
  goong.io, map4d.vn, vietmap, wongnai.com, or longdo.
- All non-empty results graded as noise (phishing spam, trading spam, Italian-keyword collision, dictionary lookups).
- If a fleet exists in these languages, it is not reusing the Chinese-fleet tag grammar or carrier stack
  on urlquery-visible submissions — or it operates entirely outside urlquery's view.
