# THE HISTORIAN — Operator Timeline & Other Campaigns (2026-10-05)

**Persona brief**: reconstruct timelines. Campaigns evolve; the evolution is the fingerprint. A campaign with a history is a swarm; a single burst is an incident.

## 1. The definitive operator timeline (the `uq`-grammar operator)

Thread: the `uq` tag grammar (`uqn` → `uqtag` → `uqvnc` → `uqscan` + `uq*` family), plus behavioral shape (systematic geographic iteration, per-request nonce/tag grammar, bursts, fetch proxies).

### Phase 0 — Tunnel R&D (Jan–May 2026): infra before grammar

| Date | Activity |
|---|---|
| 2026-01 | lhr.life (localhost.run) probing begins — bare hex-subdomain tunnels, no `uq` grammar yet. ~25 reports Jan. |
| 2026-02 | Continues (~9 reports). Same shape. |
| 2026-03 | Continues (~7 reports). |
| 2026-04 | Continues (~6 reports). |
| 2026-05 | ~12 reports. One tunnel (87e0bbc636999b) independently surfaces in CIRCL/Maltrail daily-IOC feeds tagged `hacked_npmrepos`/`metasploit` — the operator's tunnels were already being misclassified by threat intel. |

Reading: 5 months of tunnel-laying and probe-harness development before any named tag grammar appears. The operator was building the delivery mechanism (ephemeral localhost.run tunnels + probe pages) before the collection campaigns.

### Phase 1 — Grammar birth + health-data task family (Jun 2026)

| Date | Activity |
|---|---|
| 2026-06-03 | Earliest observed `uq` grammar: `uqn=988806031057` on a translate.goog-wrapped httpbun base64 probe-loader (`httpbun-com.translate.goog/base64/...` loading `//<hex>.lhr.life/probe.js`). httpbun + Google Translate + tunnel trifecta in place. |
| 2026-06-18 | **CORS burst**: 8 identical `uqcors.html?v=1` submissions in 2 min (14:37–14:38 UTC) = 8 parallel workers. Same day: `uqvnc=1781776074.018263` on AIHW aged-care data (report 5b1c95bb) — first health-data target, first named `uq*` param. |
| 2026-06-20 | **AIHW strand**: 4× `httpbun.com/base64` probes embedding a Tableau module from `vizprod.aihw.gov.au` (Australian gov health) with `uqtag=AGEDATA23` (12:52–13:02). Base64-embedded HTML probes + `uqtag=` markers + httpbun = the ltzh-family tradecraft, 3.5 months before the Amap fleet. |
| 2026-06-20/21 | **IDPH burst**: 48 reports against Iowa public-health Tableau (`data.idph.state.ia.us`, asthma ED visits). County-by-county CSV iteration with `mark=<county-fragment><epoch>` (`mark=dub1782035071`) and `validation=v<epoch>_<counter>` grammar. **is.gd layer**: 81 reports Jun 20/21 (`is.gd/3JlIp7?uqscan=1781977000`, `?x=<19-digit>`, slugs `mf075827`, `sum074114`, `kf073634`). **lhr.life probe burst**: 17 reports Jun 21 (probe.html/probe2.html/combo.html with `?x=`/`?slow=`/`?fix=`/`?cached=` 19-digit nonces). |

Reading: June is the operator's R&D crucible — grammar crystallizes (`uqn`/`uqtag`/`uqvnc`/`mark=`/`validation=`), infra stack assembles (tunnels + httpbun + translate.goog + is.gd + webhook dead-drops), and the task family is **health data** (AIHW Australia, IDPH Iowa). Parallelism proven (8-worker CORS burst).

### Phase 2 — Quiet period (Jul–Aug 2026)

| Date | Activity |
|---|---|
| 2026-07 | lhr.life trickle (3 reports). No new grammar. |
| 2026-08 | lhr.life trickle (2 reports). |
| 2026-09-01 | `probe2-start` on httpbin.org/base64 — XOR-obfuscated `b(tag,data)` Image-beacon exfil skeleton (ltzh-family payload). |
| 2026-09-27 | **IDPH returns**: 3 Scott County reports via `r.jina.ai` — the day before the Amap fleet's first scan. Bridge between task families. |

Reading: 2.5 months of near-silence on urlquery. Either the operator worked off-radar (different submission venues, private tooling) or paused. The Sep 27 jina-bridged IDPH hit is the reactivation signal.

### Phase 3 — Map-data task family (Sep 28–Oct 5, 2026)

| Date | Activity |
|---|---|
| 2026-09-28 | **Amap fleet begins**: `uqscan=` grammar at scale (2,141-record corpus). 38 `uqscan` Sep hits → 984 in Oct. |
| 2026-09-29 | **UA experiment day**: 10-report `httpbin agent` burst at 20:00 UTC (exact UA strings pending `ua-burst-retry` cron). Minimal-UA tests (`Mozilla/5.0`, `mobile`, `desktop`, `0`). |
| 2026-10-02 | AIHW PBS dashboard + data files (health strand reactivated concurrently with maps). |
| 2026-10-04 | `probe2-start` / `qjprobe-start` siblings on httpbin (10:25/10:37) — ~2.5h before the ltzh burst. `ltzh-` six-program family (jina POST + `injectPageScript` + image-beacon exfil). Ta'er Temple UA progression (`taersi-pre-mobile` → `-jm` → `-jmseg` → `-ua`). `pandalegacy`/`UA="0"` = **our own prior experiment** (closed as self-footprint). |
| 2026-10-04/05 | **Museum task family**: `uqscan=qingdaomuseum20261005b`, `henanmuseum_page_20261005a`, `wenzhou-museum-20261004`. Fleet still active 2026-10-05 03:17 UTC. |

### Grammar evolution (backfill results below; preliminary)

`uqn` (Jun 3) → `uqtag`/`uqvnc` (Jun 18–20) → `mark=`/`validation=` (Jun 21, IDPH-specific) → `uqscan` (Sep 28+) + `uq*` family expansion (`uqresearch`, `uqhs`, `uqretry`, `uqinteractive`, `uqvnc`, `uqmuseum`, `uqpd`, `uqdirect`, `uqts`, `uqprobe`, `uqfresh`, `uqmobile`, `uqtarget`, `uqhost` — 36 param names in corpus).

### Infrastructure adoption order

1. **lhr.life** (Jan 2026) — tunnel backbone, 5 months before grammar.
2. **httpbun + translate.goog** (Jun 2026) — staged probe programs.
3. **is.gd** (Jun 20/21 2026) — shortener layer.
4. **webhook.site** (date TBD — backfill) — dead-drops.
5. **r.jina.ai** (Sep 27 2026+) — fetch proxy for jina laundering.
6. **href.li / microlink / allorigins** (Oct 2026) — redirect/proxy rotation.
7. **livecodes** (Sep–Oct 2026) — staged programs.

### Task-family sequence

**Health data** (Jun: AIHW, IDPH) → **maps** (Sep 28: Amap) → **museums** (Oct 4–5: Qingdao/Henan/Wenzhou) → health reactivated concurrently (Oct 2: AIHW PBS).

### UA experiment phases

1. Sep 29: minimal-UA tests (`Mozilla/5.0`, `mobile`, `desktop`, `0`) + httpbin agent burst.
2. Oct 4: `uqcustomua20261004` (Googlebot-style UA), `uqmobile=<epoch>` a/b/c suffixes.
3. Progressive: `taersi-pre-mobile-*` → `taersi-mobile-jm-*` → `taersi-mobile-jmseg-*` → `taersi-mobile-ua-*`.
4. 15× Chrome 140 desktop UA (vs 1,931 Firefox 134 default).

### htmx backfill results

<!-- to be filled from backfill agent -->

---

## 2. Other timelines hunted

**Verdict rule**: a campaign with a history (early tests → scaled runs → infra shifts) is a swarm; a single burst is an incident.

### 2a. jmail.world — INCIDENT (not a campaign)

- 72 reports, 2026-10-04 23:54 → 2026-10-05 03:58 UTC only (5 on Oct 4, 67 on Oct 5). Median gap 3.0 min — one metronomic 4-hour run.
- No earlier activity, no evolution arc. Detection/verification workload (audit of phishing-redirector farm), inverse of our operator's collection TTP.
- **Verdict**: single incident. Not a swarm. (Watch: if the auditor returns, it becomes a campaign.)

### 2b. Tronzap localhost.run campaign — CAMPAIGN WITH ARC (separate actor)

- **Sep 5–Oct 4, 2026**: systematic SSTI/RCE test-matrix through localhost.run tunnels at tronzap.com (TRON energy rental).
- **Evolution visible**: early root scans → Sep 26 intense test-matrix burst (~40 scans/2h, parameterized families: `k-ext-ssti`, `c-rc-{php,mustache}`, `o-rc-{php,nl,dollar,semi}`, `calc`/`ev` series) → single-letter rapid probes (10 pages/15 min) → one tunnel scanned ~daily (27×, monitoring pattern).
- **Agent-shapedness**: programmatic submissions, parameterized naming, iterative refinement, full-estate enumeration (405 urlscan results across dash/api/bo/dev/mock/ref). Human pentester's script produces the same shape — payload content (behind urlscan login) would settle it.
- **Verdict**: a campaign with history = swarm-shaped, but NOT our operator (zero subdomain/grammar overlap) and NOT clearly an agent (could be a human's harness). Noted per user direction; no separate track.

### 2c. Dream Security Taiwan swarm — CAMPAIGN WITH ARC (separate actor, from reporting)

- **Jul 1–4, 2026**: 12 named attack waves, 8 parallel sub-agents (Agent A–Q), Hermes + OpenClaw, DeepSeek-V4-Flash implicated.
- **Evolution within the campaign**: initial government-account access → 85 accounts compromised → 2,500+ personnel records exfiltrated → expansion to nuclear safety agency → 7+ energy companies → supply-chain vendors → government email system. Self-correction between waves, Bayesian attack-path reprioritization.
- **Framework lineage**: Hermes recurs across 5 incidents Jul–Sep 2026 (Taiwan gov Jul 1, Thailand MoF Jul 9–13, Unit 42 Chinese-speaking campaign Jul 30, Gambit Sep 22, CARBONATO botnet Sep 22) — the framework, not one campaign, is the repeating element.
- **Corpus cross-check**: zero overlap with our 2,141 records; urlquery `gov.tw`/`openclaw`/`agent-a`/`attack-wave` hunts surfaced no Jul 1–4 activity.
- **Verdict**: separate swarm, offensive-intrusion TTP vs our data-collection TTP. No shared infra found. Noted as the strongest new-species lead.

### 2d. Clean negatives (no second `uq`-family timeline found)

- Wayback CDX + Arquivo.pt + Common Crawl: `uqscan=`, `uqcors.html`, `sub_poi_navi`, is.gd slugs → zero captures. The operator's 10-month timeline exists only on urlquery's live index.
- GitHub code search: zero `uqscan=` / `sub_poi_navi` in public code.
- No second tag-grammar fleet (`zz=`-style, non-`uq` nonce params) at fleet scale in sampled urlquery windows.

---

## 3. The fingerprint: what the timeline itself proves

1. **The Amap fleet is the third act, not the opening** — 10 months of tunnel R&D (Jan–May) → health-data campaigns (Jun) → quiet (Jul–Aug) → maps (Sep–Oct).
2. **Grammar crystallized in June 2026**; `uqscan=` is the scaled-production tag, `uqtag=`/`uqvnc=`/`uqn` the R&D-era forms.
3. **Infra accretes, never replaces**: tunnels → httpbun/translate → is.gd → webhook.site → jina → redirect proxies. Each new layer adds, old layers persist.
4. **Task families rotate; tradecraft persists**: health → maps → museums, same burst/iteration/tag shape.
5. **Parallelism is the constant**: 8-worker CORS burst (Jun 18) → 2,141-report fleet (Oct). The operator never works single-threaded.
6. **Single pipeline**: 2 `exit_node` values across 2,159 reports — one submitter, not a swarm of submitters. One operator, many workers.
