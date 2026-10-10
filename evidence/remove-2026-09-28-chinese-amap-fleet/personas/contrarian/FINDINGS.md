# THE CONTRARIAN — anomaly catalog
**Persona:** hunts what doesn't fit. Every entry: what broke, why it's odd, read (new actor / operator experiment / noise).
**Corpus:** `events.jsonl` (2,141 records, 2026-09-28 → 2026-10-05). Hours in Asia/Shanghai unless marked Z.
**Lanes:** timing analysis (done), htmx fresh-anomaly crawl (done — via local raw corpus; live htmx blocked by VM egress outage), urlscan mining (blocked — VM egress outage; agent closed, retry path documented below).
**Not pushed.**

---

## Catalog

### C1. `navy971-20261005a/b/c` — the navy triple
- **What broke:** tag word "navy" — first and only military-flavored word in a corpus of museums, parks, zoos, food. Three reports (a/b/c), same POI (`B0FFJMINT2`), one showing the malformed `%26uqscan=`-inside-`id` nesting (C8). Submitted SH 02:03 Oct 5, inside the deep-night clock-skewed pocket (C6).
- **Why odd:** vocabulary break + skewed-clock pocket.
- **Read:** operator experiment (60%). The a/b/c suite grammar is the operator's own; the word is likely a place-name fragment. But it is the most off-vertical word in the corpus — POI identity lookup pending (retry `uq_htmx.py search --query B0FFJMINT2` when egress recovers).
- Reports: [62d1cdbf](https://urlquery.net/report/62d1cdbf-ce24-4861-ab4a-a96e8601284e), [be82cecd](https://urlquery.net/report/be82cecd-0fe3-40c5-bea6-500ea7c8f7da), [d6d1dc37](https://urlquery.net/report/d6d1dc37-17e1-44f2-9718-dc176b12f36e)

### C2. `claudeprime` — the lone JS-bundle scan (see also C4)
- **What broke:** submitted URL is a static JS chunk (`ssr-next.amap.com/static/amap-pc-ssr/production/1f3ace2b/_n…`), tagged with a bare dateless word. SH 05:48 Oct 5 — the last distinctive tag before the corpus tail.
- **Why odd:** everything else targets POI pages/APIs; this targets frontend build artifacts = infrastructure mapping, not data collection. `ssr-next.amap.com` is a new host (vs known www/m/ditu/amap-pc-ssr).
- **Read:** operator experiment (70%) — mapping Amap's Next.js build output, testing whether the static CDN echoes query params (`uqstatic=`/`uqasset=` marker variants ride the same URLs). 4 such submissions on Oct 4.
- Report: [da980375](https://urlquery.net/report/da980375-f511-4b12-bec2-51d0986b163f)

### C3. Hospital task family — `gzhosp*`, `jinanhospital*`, `czhospital*`, `claude20261005hospital2/3`, `claude20261005sph`
- **What broke:** healthcare POIs in a corpus of museums/parks/zoos/scenic spots. Not a singleton — a real family: Guangzhou hospital (B00140UENM, 5 reports across mobile/www/ditu/api = full platform suite), Jinan hospital (a/b/c triple), Changzhou hospital, plus claude-tagged hospital probes. The livecodes.io "Baxia" harness also ran `GZHOSP-topbackend/topditussr/ssrwww/PLACE` route variants.
- **Why odd:** vertical expansion — museums → hospitals is the first move into sensitive-civilian-infrastructure POIs.
- **Read:** operator experiment / campaign expansion (75%). Full-platform suites mean deliberate tasking, not accidents. Track as its own family in the live monitor.

### C4. The Baxia anti-bot research harness (MAJOR — counter-forensics R&D)
- **What broke:** on Oct 4 the operator deployed a probe that hooks `XMLHttpRequest`, loads Alibaba's **Baxia anti-bot SDK** (`sg-wum.alibaba.com`, `baxiaCommon.js`), calls `baxiaCommon.init({checkApiPath: u=>u.includes('getPoiInfo'), …})`, fires `getPoiInfo` at 3/7/11s, then `navigator.sendBeacon`s the results to the operator's own webhook.site dead-drop (`a7753b69-2ceb-4221-adfa-80f69d57480c`). Six minutes earlier the operator checked that same inbox with an href.li-wrapped `?run=<epoch>` liveness probe.
- **Why odd:** this is not scraping — it's learning which telemetry tokens (uab/umid/et) Amap's API requires and exfiltrating the findings. Counter-forensics R&D, one level past collection.
- **Read:** operator experiment (90%). Plus 18 livecodes.io submissions titled "Baxia signed navigation / delayed query probe / header echo / JSONP / full app iframe" — a named browser-behavior harness learning what scanners (and Amap's defenses) will execute. Also 5 jina cache/metadata probes (`gc-jina-meta-…`, `jina-cache-…`) — calibrating the jina relay stack.
- Reports: [e32e37d2](https://urlquery.net/report/e32e37d2-456c-4240-954b-f7e2cbb27315) (payload), [eb4ecb55](https://urlquery.net/report/eb4ecb55-d335-45fb-b775-6746d422c7f0) (inbox check), [2827b191](https://urlquery.net/report/2827b191-c4e0-4d39-ac99-c70bf4791a04) (livecodes Baxia)

### C5. `uq*` marker-family A/B test — the grammar is loosening
- **What broke:** ~157 Oct-4 submissions use marker params that are **not** `uqscan=`: `uq=`, `uqpd=`, `uqdirect=`, `uqresearch=`, `uqtarget=`, `uqprobe=`, `uqfresh=`, `uqlegacy=`, `uqmobile=`, `uqproxy=`, `uqstack=`, `uqstatic=`, `uqasset=`. Values alternate bare epochs and word+date. One test put a full UUID as the marker value; `?uqstack=1791135595a/b/c` triplets; `?uqvnc=` + `?uqinteractive=` companions.
- **Why odd:** the operator is systematically testing which param names survive Amap's URL handling/redirects and stay visible to the scanner.
- **Read:** operator experiment (90%). Same Alibaba SG/CN egress IPs as the tagged lane — same actor, new grammar under test. **Hunt implication:** future fleet traffic may not say `uqscan=` at all — watch the whole `uq*` param family.
- e.g. [a776eb59](https://urlquery.net/report/a776eb59-e570-4e78-b627-bfa06ee49509) (UUID marker value), [08c6993d](https://urlquery.net/report/08c6993d-4ad4-4ea4-9460-01852cac9742) (uqstack triplets)

### C6. The deep-night clock-skewed pocket (SH 01:42–02:10 Oct 5)
- **What broke:** three tag families (`xjpark1791145452–56`, `detail/loc/target/old/www/ditu-1791146590–95`, `xspoidetail1791146900/01` + `xspath1791146903`) carry epoch nonces decoding **+2.6–2.7h in the future**. Baseline: ordinary epoch tags decode within minutes of submission (verified individually).
- **Why odd:** consistent +2.7h skew across all three families, in no other window. Same pocket hosts the navy971 triple, the 8-hex hash burst, and `answer20261005{a,b,c}`.
- **Read:** different tool signature, possibly different machine (35%) — a URL-generator with a ~2.7h-fast clock, or pre-generated future nonces. Strongest evidence in the corpus of a second build box / container.

### C7. The UUID nonce burst (SH 12:15–13:08 Oct 4)
- **What broke:** 15 full-UUID `uqscan` values; 13 land in a 53-minute midday window. One UUID reused 5× over 6 hours. Zero elsewhere in 6 days.
- **Why odd:** shape break (UUID where epochs/dates live) + tight time-box + nonce reuse.
- **Read:** operator experiment — a distinct tool/config emitting UUID nonces, trialled for under an hour (80%).

### C8. Malformed param nesting — `%26uqscan=` inside `id=` (111×)
- **What broke:** `getPoiInfo?id=B0FFGJP58W%26uqscan=research20261005api2` — the marker got URL-encoded *into* the `id` value. 111× across two days, including the navy971 `a` report.
- **Why odd:** volume and persistence rule out a one-off typo.
- **Read:** systematic-but-broken URL builder, or a deliberate test of how Amap's API parses a poisoned `id` (60/40). Open: fetch one report body to see whether Amap normalizes it.

### C9. `pre-amap-pc-ssr.amap.com` — staging host discovery
- **What broke:** 49 events on Oct 4 against Amap's **pre-production/staging** SSR host — a subdomain never seen before in the corpus.
- **Why odd:** the operator found and is diffing staging vs prod.
- **Read:** deliberate API-layer mapping (85%) — route names, param acceptance, staging parity. A level below POI-page scraping.
- e.g. [dcfeeb74](https://urlquery.net/report/dcfeeb74-f07b-4e4f-947f-f1f22b94a3c0)

### C10. `switchVersion` endpoint probing
- **What broke:** 21× `www.amap.com/service/switchVersion?enable=1&src=<marker>` (+1 on gaode.com, same second, different IP). One `src` value is a full tagged URL nested inside — a marker-survival test through Amap's redirect. New singletons: `uqpreseed260929a` ("pre-seed", Sep-29-dated), `gyshort64`.
- **Why odd:** version-switch endpoint probed for `src`-param echo/handling.
- **Read:** operator experiment (80%).

### C11. Route-matrix sweep with random hex tags
- **What broke:** SH 01:19–01:23 Oct 5, one IP hit **one POI (B0G1X5HFSJ)** across 9 URL shapes (www/ditu × place/detail/service/api + staging host) with random 8-hex `uqscan=` values (`156d324b`, `9f36c491`, …) instead of word tags.
- **Why odd:** the tag became a pure nonce; the variable under test is the route, not the label.
- **Read:** cache-busting / route-equivalence fingerprinting (85%) — which URL shapes return identical POI data.
- e.g. [1e703e0c](https://urlquery.net/report/1e703e0c-6398-49cb-b6a3-02caac40c4d6)

### C12. University strand — `zju20260929`, `zjuhjc20261004a`
- **What broke:** Zhejiang University POI; `zju20260929` carries a Sep-29 date but was submitted Oct 4 (5-day-stale replay).
- **Why odd:** off-vertical target + stale-date replay.
- **Read:** operator experiment (65%). Pairs with the hospital family: the operator is broadening POI verticals beyond tourism.

### C13. The Oct 2–3 blackout → Oct 4 super-run
- **What broke:** ~56h near-silence, then a 16-hour continuous run: 1,600 records, 9.5× the previous biggest day, median gap 5–13s.
- **Why odd:** everything about the preceding cadence broke at once.
- **Read:** deliberate campaign restart (85%). Oct 4 carries the richest vocabulary and all the numbered A/B suites.

### C14. The lone probe before the blackout
- **What broke:** `research20261002a` at Oct 1 22:24Z (SH 06:24), >2h isolated on both sides — the only such record.
- **Why odd:** single "a"-tag fired at dawn, then 33h of silence. Tag date matches SH local date.
- **Read:** test ping before stand-down, or last gasp of the Oct 1 campaign (70%).

### C15. Stale-nonce replays — the queue is the memory
- **What broke:** `1790767001/2/3` submitted 23.6h after nonce time; `wfjxy202609292339` replayed 5 days later; day-old `20260927/20260930*` templates in the deep-night pocket.
- **Why odd:** tag timestamps routinely ≠ event time.
- **Read:** the fleet replays old URL lists (90%). Tag timestamps are queue-build age — never use them as event time without checking submission time.

### C16. Infrastructure-probe words — `chromereferer`, `canonical`, `share`, `embedpoi`, `gallery`, `cookietest`, `cookiea/b/c`, `verify`, `exit`
- **What broke:** capability words, not place names. `share20261004a` → `wb.amap.com/?p=…` (share endpoint, new subdomain); `embedpoi20261004` → `/ssr/embed/place`; `gallery20261005` → `/ssr/poi_gallery`; `chromereferer` on a `getPoiInfo` call; bare `exit` twice (Sep 30 + Oct 4).
- **Why odd:** the operator is probing Amap's own platform surface (share/embed/gallery/referrer handling), not collecting POI data.
- **Read:** operator experiments (80%) — capability mapping of the target platform.

### C17. DigitalOcean egress for the carrier lane
- **What broke:** `64.23.183.159` (AS14061 DigitalOcean, US) — 65 submissions in 48h, all `httpbun.com/base64/…` carrier tests. First non-Alibaba egress ever seen for this operator.
- **Why odd:** infra expansion, same URL shapes.
- **Read:** same operator, new box (80%). Not a new actor — shapes identical.

### C18. Tibet/Xinjiang edges — `potala*`, `xjpark*`
- **What broke:** Potala Palace (Lhasa) POI across 4+ reports; `xjpark*` (10 tags, Xinjiang park) with future-skewed nonces.
- **Why odd:** sensitive-region POIs; xjpark rides the skewed clock (C6).
- **Read:** operator tasking as usual (70%) — the interesting part of xjpark is the clock, not the place.

### C19. Nocturnal side channels
- **What broke:** carrier (httpbun/httpbin/livecodes.io) and relay (href.li) traffic concentrates SH 19:00–02:00 while direct/amap.com runs all hours.
- **Why odd:** two diurnal patterns in one corpus.
- **Read:** the relay/probing layer is a night-shift tool (75%) — consistent with the deep-night pocket (C6) being a different tool or session.

### C20. Coordinate-URL form + unmarked runs
- **What broke:** `www.amap.com/?p=<POI>,<lat>,<lon>,<name>,<address>` share-link form (Shandong Museum, Hangzhou Olympic stadium) alongside POI-id URLs; ~883/1904 recent events carry no tag at all — but from the *same* IPs as the tagged lane.
- **Why odd:** new URL form; marker presence is per-run config, not identity.
- **Read:** operator testing the `?p=` coordinate form (75%); unmarked runs are the same operator (IP match).

---

## Consolidated contrarian read

1. **One main operator** (night-owl, ~10s metronome, local-date tagger, A/B suite grammar) — owns the Oct 4 super-run. Every anomaly attributes to it by IP/ASN/grammar; **no second actor found**.
2. **But the operator is running experiments, not just collecting:** anti-bot telemetry research (Baxia harness + webhook beacon), marker-grammar A/B tests across the whole `uq*` param family, JS-bundle/static-asset discovery, staging-host diffing, switchVersion probing, route-equivalence fingerprinting, share/embed/gallery capability mapping.
3. **A second tool signature in the deep-night pocket** (SH 00:00–02:10 Oct 5): +2.7h clock skew, navy971, 8-hex hashes, answer-series, nocturnal relay layer. Distinct build box until proven otherwise.
4. **A third one-off signature at midday Oct 4** (SH 12:15–13:08): UUID nonces, 53-minute experiment.
5. **Vertical expansion in progress:** hospitals (Guangzhou/Jinan/Changzhou), a university (ZJU), sensitive-region landmarks — beyond tourism POIs.
6. **Hunt implication:** future fleet traffic may not say `uqscan=` — watch the whole `uq*` param family, `ssr-next`/`pre-amap-pc-ssr`/`wb.amap.com` hosts, and the Baxia/jina probe strings.

## Blocked / pending
- **VM egress outage** (2026-10-05 ~04:24+ UTC): proxy accepts TCP, never answers CONNECT — all hosts fail. Blocked: live htmx POI lookups (`B0FFJMINT2`, hospital POIs), urlscan.io mining lane, last ~3h of htmx coverage (post-01:12Z).
- **Retry when egress recovers:** `uq_htmx.py search` for `uqscan`, `uqstatic`, `uqasset`, `uqstack`, `baxia`, `jina`, `pre-amap-pc-ssr.amap.com`, `ssr-next.amap.com`, `switchVersion`, `B0FFJMINT2`; urlscan API sweep for non-uq agent shapes.
- **urlscan anomaly lane:** BLOCKED — VM egress outage made urlscan.io unreachable; lane closed. Retry when egress recovers: urlscan search API for non-uq agent-shaped bursts, tunnel-domain page shapes, per-request nonce grammars.
- **Open lookup:** does Amap's API resolve the `%26uqscan=`-inside-`id` form (C8) — bug vs injection test.

## Raw lane reports
- `raw/timing-anomalies.md` — full timing analysis (blackout, skew, suites, diurnal)
- `raw/htmx-anomalies.md` — htmx-lane findings F1–F10 (submitter-IP-attributed)
