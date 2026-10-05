# FINDINGS.md — Hindi/Japanese/Korean behavior-based agent-fleet hunt (2026-10-04)

Target: ANY non-Chinese agent fleet in Hindi, Japanese, or Korean — the first non-Chinese fleet anywhere is the prize.
Fingerprint baseline: `../raw/analysis/PATTERN.md` (Tencent Amap fleet: `uqscan=<word><YYYYMMDD>[letter]` tags, Amap place/API scans, httpbun/httpbin base64 programs, webhook.site dead-drops, r.jina.ai/translate.goog/fanyi.baidu relays, `<place>-<descriptor>-<epoch>` program titles).

Tool: `python3 ~/workspace/skills/urlquery/bin/uq_htmx.py search --query "Q" --limit 24 --delay 4` throughout (30 queries total).

## VERDICT: NO FLEET FOUND in any of the three languages. All three lanes are honest zeros.

Every query either returned zero results or returned results that were exclusively (a) the already-known Chinese Amap fleet, or (b) unrelated noise / ordinary submissions. Details per language below.

## Korean (highest priority) — ZERO

**Map/POI services (Amap analogs):**
- `map.naver.com` → 15 fuzzy-noise hits (naver.me short links, mokaair.com, random .cfd/phishing), none are map.naver.com submissions. `url.domain:map.naver.com` → 0.
- `map.kakao.com` → 2 hits: a punycode shopping domain (2026-04) and a `kko.to` short link (2026-01). `url.domain:map.kakao.com` → 0.
- No systematic place/API scanning, no place IDs, no cache-buster params on any Korean map service.

**Tag grammar (romaji + native):**
- `geomsaek2026`, `eobmu2026`, `tamsaek2026`, `jeongbo2026` → all 0.
- `검색2026` (native script) → 0 (tool does not handle CJK encoding anyway — known blind spot, see Limitations).
- `seoul-1791` (program-title grammar `<place>-<epoch>`) → 0.
- `20261004 naver` → 0.

**Carriers / shorteners / relays:**
- `kko.to` (Kakao native shortener) → 8 short links, 2023–2026, no burst, no tags, ordinary shares. Not agent-shaped.
- `me2.do` (Korean shortener) → short links, ordinary. Not agent-shaped.
- `translate.goog naver` → 1 unrelated (translate.google.co.jp 2024).
- `r.jina.ai` results → only Amap-fleet relays + unrelated (Iowa health-data CSV ×3, newspapers.com). Zero Korean map targets.
- `webhook.site` results → Amap-fleet dead-drops + codesandbox noise. Zero Korean links.

## Japanese (highest priority) — ZERO

**Map/POI services:**
- `map.yahoo.co.jp` → 10 fuzzy-noise hits (foodre.jp restaurant pages, suzuki-otolaryngology.or.jp, cybertrust.co.jp), none are map.yahoo.co.jp submissions. `url.domain:map.yahoo.co.jp` → 0.
- `mapion` → 1 legit `www.mapion.co.jp` (2024-08-06, single ordinary submission), rest noise (hottomotto.com shops).
- `zenrin` → 0 relevant (phishing .top domains only).

**Tag grammar (romaji):**
- `kensaku2026`, `tasuku2026`, `chousa2026` → all 0.
- `tokyo-1791` → 0.

## Hindi — ZERO

**Map/POI services:**
- `mapmyindia` → 3 fuzzy-noise hits (baanknet.com, elektrobit.info, a maillist-manage.net tracker). Zero MapMyIndia submissions.

**Tag grammar:**
- `khoj2026`, `karya2026` → 0.
- `खोज2026` (Devanagari) → 0.

## Language-agnostic cross-checks (fleet signature on non-Chinese targets)

- `uqscan` → 100% Amap fleet (latest 2026-10-05, fleet still active). NO non-Chinese reuse of the param.
- `20261004a` (generic `<word><YYYYMMDD>[letter]` shape) → 100% Amap fleet. The shape has not been adopted by any other operator on urlquery.
- `research2026` → 1 unrelated (familylawconsulting.org, 2026-06). `scan2026` → SharePoint-hosted `scan2026-*.html` phishing-ish noise, no agent shape. `target2026` → 0.
- `agent2026` → 8 reports of `ai-sales-agent2026.appwrite.network` (Feb–Mar 2026): an agent-shaped single deployment (AI sales agent test site) but one target, one domain, no fleet behavior, and English-language — not a non-Chinese fleet.
- `httpbun` → 1 hit, Amap fleet (`httpbun.com/redirect?url=...amap...uqscan=peoplepark1791134555752612150`). `httpbun.com/base64` and `httpbun.com/base64/` → 0 via this endpoint.
- `httpbin.org/base64` → 0 via htmx (the ltzh-family httpbin programs from PATTERN.md do not surface through this endpoint — known tool limitation).
- `fanyi.baidu.com/transpage` → 100% Amap fleet (6 relay reports, all Amap getPoiInfo).
- No bursts: no Korean/Japanese/Hindi domain showed many same-day reports.

## Limitations (honest scope notes)

1. The htmx endpoint fuzzy-matches rather than doing exact URL matching; `url.domain:` scoping syntax returned 0 across the board (unsupported). Direct-domain hits may be missed by fuzziness — but the tag-grammar and carrier cross-checks (which return exact matches, e.g. all `uqscan` = Amap) bound the miss risk.
2. CJK/Devanagari native-script queries return 0 regardless of truth (encoding blind spot). Romaji/transliterated forms were used instead per the task's note; agents that use native-script-only tags would be missed.
3. Staged base64 programs on httpbun/httpbin are only findable via their submitted URLs, not their decoded content — a Korean/Japanese program staged there would only surface if submitted directly or via redirector (the `httpbun.com/redirect?url=` shape was checked; `httpbun` returned only the Amap case).
4. Did not enumerate Hindi pastebins (no dominant India-specific pastebin surfaced); generic `pastebin.com` hits are in the negative-space record of PATTERN.md (×2, neither fleet-related).

## Bottom line

The `<word><YYYYMMDD>[letter]` tag grammar, the `uqscan`/`uq`/`uqtarget` param family, the httpbun→Amap redirector shape, and the webhook.site dead-drop lane are, as of 2026-10-04/05, exclusively used by the Chinese Amap fleet. No Hindi, Japanese, or Korean fleet counterpart exists on urlquery.net with this tradecraft. Pushed to no branch per task instructions (uncommitted).
