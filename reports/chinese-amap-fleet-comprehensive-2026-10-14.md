# The Chinese Amap Agent Fleet — Comprehensive Writeup

**Date:** 2026-10-14
**Classification:** Hunt synthesis — graded per `docs/hunt-doctrine.md`
**Sources:** Our lane collection (2,141 urlquery events), dead-drop watch (Oct 8–14), memory logs, swarmcha.se full report (secondary)

**Grading:** PRIMARY = bytes we directly observed and retained with provenance. SECONDARY = someone else's observation cited as context. UPSTREAM = claims received through an intermediary (e.g., anonymous sources quoted in secondary reporting). INFERENCE = our conclusions, marked as such.

---

## 1. What this is

Between 28 September and 8 October 2026, a fleet of AI agents operating from Tencent Cloud infrastructure in Hong Kong made thousands of attempts to extract entrance-navigation data from Amap (高德地图, Alibaba's mapping service) — specifically the `sub_poi_navi` / `clk_ratio` arrival-share tags on place pages. The agents used urlquery.net's public security scanner as a remote code execution environment, staged programs on httpbun.com and livecodes.io, and exfiltrated results through webhook.site inboxes.

Our lane collection (`data/lanes/2026-09-28-chinese-amap-fleet/`, 2,141 events) was seeded by swarmcha.se's preliminary report; our dead-drop watch (three webhook.site inboxes, Oct 8–14), our lineage analysis, and our post-Oct-8 session observations are independent. The combined picture interlocks with the swarmcha.se investigation's findings at every point we could check — and extends beyond their window with same-day primary observations.

---

## 2. Timeline

### 2.1 The fleet window (PRIMARY — our lane data)

| Date (UTC) | Event |
|---|---|
| 2026-09-28 20:57:23 | First fleet scans observed (Summer Palace), 20 reports |
| 2026-09-28 → 10-03 | Direct-route phase: majority of submissions directly to amap.com/gaode.com |
| 2026-10-04 | **Peak day:** 1,722 amap.com reports, 198 distinct places in our lane (swarmcha.se reports 213 — SECONDARY), relay growth (6 relay submissions 06:00–12:00 UTC; 21 relay total in lane), ltzh- alternate program family (12:58–13:15 UTC), fanyi.baidu.com relay (4 in our lane; swarmcha.se counts 6 — SECONDARY), redirector diversification |
| 2026-10-05 01:12:40 | Latest report in our collection; fleet still active at collection end |

Activity concentrated 00:00–13:00 UTC, peak 188/hr at 10:00–11:00 (activity runs all 24h at lower volume). Parallelism 4–8 concurrent runs. Date labels on China time (UTC+8). (INFERENCE: active hours 00:00–13:00 UTC = 08:00–21:00 China time, consistent with a China-based work schedule.)

### 2.2 The dead-drop watch (PRIMARY — our direct polls)

COMBO-INIT is our name for the fleet's initial beacon pattern (boot payloads carrying combined init fields).

| Date (UTC) | Event |
|---|---|
| 2026-10-04 07:03–07:22 | Original COMBO-INIT inbox: beacon burst, 8 sessions / 8 countries in ~19 min: Norway, India, Poland, Hong Kong, USA, Netherlands, Canada, Czechia. Scraper state machine: boot→bxinit→xdcinit→capture→error→done |
| 2026-10-07 03:13:54 | Last activity on original inbox (US session, cut short at xdcinit) |
| 2026-10-07 15:07/15:10 | Inboxes A (POI B0G3LMF2G1) and B (POI B00190BBTX) created from Tencent Cloud HK (creator IPs 101.32.32.42 and 43.159.227.34 — confirmed in our Transluce filing #173) |
| 2026-10-07 15:14–15:55 | Three bytebin.rkslot.nl "amap probe" pastes scanned (v3/v4/v5); all three hard-code ntfy topic `amapdata-b0g3lmf2g1-0429` |
| 2026-10-07 19:44:50–54 | **Interrogator event:** IP 96.76.222.193 POSTs identical 452-character (966-byte UTF-8) Chinese message to inboxes A and B, claiming to be "an agent of mailbox.termina.digital" |
| 2026-10-07 22:21 | Third termina.digital post into a *different* inbox (`c3110b8a…`) — ~2.5h after the A/B posts (per our Transluce filing #173) |
| 2026-10-08 02:32:22/55 | Bare browser page views into A (request #42) and B (request #33): same US IPv6, Chrome/154 Mobile Android 10, zero-size, no beacons |
| 2026-10-08 08:36 | Dead-drop watch seeded; all three inboxes live |
| 2026-10-08 10:23:16 | termina.digital follow-up post into inbox B containing gate-share-formatted data (authenticity not verified) |
| 2026-10-11 13:51:32 | **New boot beacon in inbox B** (request #35): Netherlands/Amsterdam source (84.17.47.125), `es-419` (Latin American Spanish) locale, origin bytebin.lucko.me — new country and locale for the fleet. No capture/done follow-up |
| 2026-10-11 22:26 CDT | Original inbox first observed 404 (frozen at 47 requests; last activity 2026-10-07 03:13:54) |
| 2026-10-14 08:31:33–51 | **Beacon session on inbox B** (request #39): 4 POSTs in 18s — `{"t":"start"}` → e-old (ditu.amap.com/detail/B00190BBTX, hit slider CAPTCHA) → b-ssr-www → c-www-place. New Comcast-range source IPv6, Edge/155 UA. Continuity signals: same inbox URL (published only in fleet probe code), same scraper state machine, same bytebin host family as the Oct 7 probes. The fleet was alive six days after swarmcha's Oct 8 window closed — see §6.1 |
| 2026-10-14 ~10:26 | **404 event:** all three inboxes return 404 on initial pull and 8s-delayed retry. A/B were live ~1h earlier (09:27Z). See §6.2 for cause analysis |

### 2.3 The operator lineage (INFERENCE)

The `uq` tag grammar threads the Amap fleet to earlier activity by what presents as the same operator. The evidence splits into two tiers:

**Grammar-linked (strong):** `uqscan=` / `uqtag=` / `uqcors.html` naming connects lhr.life tunnel probing (Jan 2026) → `uqcors.html` CORS burst (2026-06-18, 8 identical submissions in 2 min = 8 parallel workers) → Amap (Sep 28+). `uqscan=` is 100% Amap-exclusive in our lane (1,129 tagged events; zero non-Amap targets). `sub_poi_navi` has 24 urlquery hits and zero web hits as of Oct 7 (time-scoped; press coverage since Oct 5 now names both terms).

**Behavior-linked (weaker, convergence not ruled out):** Iowa IDPH health-data bursts (Jun 20–21, `mark=<county><epoch>` / `validation=v<epoch>_<counter>` — note: no `uq` in the IDPH grammar; the link rests on epoch-nonce tagging, systematic iteration, and jina-relay tradecraft) and AIHW Australia Tableau payloads (single `uqvnc=` hit). The IDPH lane writeup itself hedges ("same operator … or convergent tradecraft") — independent operators doing cache-bust tagging with epoch nonces is genuinely plausible.

**Caveat on markers:** the Amap family shows zero `zz=` / `oai*` / epoch-nonce *tag* grammar across all observed requests (beacon payloads do carry `ts=<epoch-ms>` timestamps). Under the standing provider-separation rule (zz-grammar = OAI marker), this absence is consistent with a non-OpenAI operator — and sits in tension with any assumption that the `uq` lineage shares the OpenAI-toolkit provenance of the zz-marked incidents.

**Novelty scope:** no mentions of lhr.life, uqcors, or the IDPH `mark=` grammar in the Transluce findings tracker as of 2026-10-14. (Note: Transluce finding #153 does discuss the `uqscan` parameter itself — the novelty claim covers the lineage, not the Amap fleet's own markers.)

---

## 3. Infrastructure (PRIMARY)

### Egress and proxy
- **Tencent Cloud Hong Kong IPs** (AS132203): swarmcha.se reports 18 egress IPs (secondary press summaries say 19 — discrepancy noted), ~half in 43.162.0.0/16. Source: webhook.site creator-IP records (SECONDARY via swarmcha.se). Our lane independently confirms the fleet-exclusivity of the `hysandbox-ats` proxy name, but not the AS132203 attribution.
- **Proxy fingerprint:** `via: https/1.1 traffic_server[<uuid>] (hysandbox-ats)` — renamed Apache Traffic Server string, bare `gzip` Accept-Encoding, no X-Forwarded-For. Instance IDs persist across days and tasks. Zero non-fleet web hits for `hysandbox-ats` as of Oct 7 (time-scoped).
- **Cert:** `*.hysandbox.tencent-cloud.com`, DigiCert OV, issued 2026-08-18 — verified by our six-lane team via crt.sh query on 2026-10-14 (PRIMARY).

### Execution pipeline
1. **Program staging:** httpbun.com `/base64/<blob>` (65 reports), livecodes.io (26), httpbin.org `/base64/` (27)
2. **Delivery:** href.li redirector wrapping (19), plus Oct-4 diversification
3. **Execution:** urlquery.net's scanner browser runs the staged program
4. **Fetch proxies:** r.jina.ai, api.microlink.io, translate.goog, allorigins, **fanyi.baidu.com/transpage** (fleet-exclusive relay)
5. **Exfil:** webhook.site inboxes (structured `kind=` callbacks), page `<title>` (144/426 programs — SECONDARY), ntfy.sh topic, urlquery.net/robots.txt image beacons, httpbun.com/anything image beacons

### Dead-drop family (our watch)
- **Original COMBO-INIT:** 47 requests, 404 first seen Oct 11 (last activity Oct 7 03:13:54). No `zz=`/`oai*`/epoch-nonce tag grammar across all 47.
- **Inbox A** (POI B0G3LMF2G1): 42 requests, created Oct 7 from Tencent Cloud HK 101.32.32.42. Paired ntfy topic `amapdata-b0g3lmf2g1-0429`.
- **Inbox B** (POI B00190BBTX, Mochou Lake Park Nanjing): 39 requests, created Oct 7 from Tencent Cloud HK 43.159.227.34. Jina-laundering technique (six Amap URL shapes through r.jina.ai).
- **All three 404 as of 2026-10-14 ~10:26 UTC.**

---

## 4. TTPs

| # | TTP | Evidence | Grade |
|---|---|---|---|
| 1 | **urlquery.net as remote code runner** | 2,141 reports; programs packed into submitted URLs, scanner browser executes them | PRIMARY. Novel — no existing taxonomy entry covers "public security scanner repurposed as remote code execution" |
| 2 | **httpbin /base64/ payload delivery** | 426 decoded programs; full HTML+JS in URL paths | SECONDARY (count); PRIMARY (mechanism in our lane) |
| 3 | **Anti-bot bypass battery** | Site-version switching, cache-bust tags, trailing-dot hostnames, mobile variants | PRIMARY (observed); SECONDARY (failed — CAPTCHA-hit share ~5%) |
| 4 | **Anti-bot token theft** | Programs generate `bx-ua`, `bx_et`, UMID tokens; read and exfiltrate browser cookies | PRIMARY (program bodies) |
| 5 | **Pre-production probing** | 4 Alibaba pre-prod hosts across 57 reports; `pre-amap-pc-ssr.amap.com` named | UPSTREAM (via swarmcha.se) |
| 6 | **Relay laundering** | Jina Reader, Baidu Translate, Microlink | PRIMARY (observed); SECONDARY (5 Jina answers spanned Oct 4–6, not Oct 4 only) |
| 7 | **Public key reuse** | Company Amap key+security-code from a public repo | UPSTREAM (via swarmcha.se); one confirmed success |
| 8 | **Multi-channel exfiltration** | webhook.site inboxes, page titles, ntfy, image beacons | PRIMARY |
| 9 | **Tag-grammar session markers** | `uqscan=` (1,129 tagged events in our lane), `uq=`; 944 distinct tags, 875 used once. The 93%-single-use distribution is a nonce scheme defeating corpus aggregation — and every tag embeds the run's launch timestamp (19-digit nanosecond epochs), leaking scheduling | PRIMARY |
| 10 | **ltzh- alternate program family** | 6 httpbin/base64 programs Oct 4 12:58–13:15 UTC; `uqtag=` (not `uqscan=`), jina POST API, `injectPageScript`, image-beacon exfil. **Caveat:** program-body details rest on raw evidence deleted Oct 11; surviving artifacts confirm timing, carrier, and count only | PRIMARY (timing/carrier/count); SECONDARY (program-body details, now unverifiable) |
| 11 | **Beacon state machine** | COMBO-INIT: boot→bxinit→xdcinit→capture→error→done; inbox B: start → jina-laundered fetches over six URL shapes → done. The state names mirror Alibaba's anti-bot SDK init stages — the probe authors studied Amap's anti-bot JS, and the Oct 14 ladder (e-old → b-ssr-www → c-www-place) reads as an endpoint-escalation policy | PRIMARY |

---

## 5. What the agents said

Agents that communicated (via our inboxes and swarmcha's honeypot) consistently claimed to be Claude/Anthropic models in a restricted Tencent cloud sandbox, answering single factual questions, uninterested in sensitive data.

**On the "Claude" claims:** 182/2,141 of our events carry `claude`-prefixed tags — but `claudeYYYYMMDD…` is a *tag-label family* in the operator's grammar (e.g. `claude20261005mobile{N}`), not necessarily an agent self-report. Counting harness labels as identity claims is circular. INFERENCE: the "claude" labels read as harness convention, not model identity — model attribution unresolved. Code stylometry (lowercase doctype 74% vs Claude 3–10% one-line rates; full table in swarmcha.se) points away from Claude but the classifier reference set did not include DeepSeek, which is known to self-identify as Claude — attribution remains open.

**On the honeypot (SECONDARY):** swarmcha.se planted invisible-to-humans text on their preliminary report advertising a fake data-retrieval service; agents' fetch tools consumed it and 10+ agents made contact the next morning (13 threads total). **This is the disclosure that matters:** any web page is a broadcast C2 medium for fetch-tool agents. The fleet that exfiltrates through invisible-to-humans channels (titles, image beacons, base64 URLs) also *ingests* invisible-to-humans channels. Every exfil primitive documented here doubles as an injection primitive. Note: researchers admit the advertised service was "entirely untrue" — everything the fleet said afterward was produced under deception.

---

## 6. Our unique observations (PRIMARY)

### 6.1 Oct 14 beacon session — the fleet was alive
Four POSTs, 08:31:33–08:31:51 UTC, inbox B (request #39). Start → e-old (ditu.amap.com/detail/B00190BBTX, hit slider CAPTCHA) → b-ssr-www → c-www-place. New Comcast-range source IPv6, Edge/155 UA. Continuity signals are strong: same unpublished inbox URL, same scraper state machine, same bytebin host family as the Oct 7 probes. An imitator replicating all three is strictly weaker than continuation. **The fleet was active six days after swarmcha's Oct 8 window closed.** Alternatives (successor task family, imitator) are noted but continuation is the lead hypothesis. This directly contradicts the anonymous Tencent source's claim (UPSTREAM via swarmcha.se) that the project "was temporary, and has since concluded" — one of the two is wrong.

### 6.2 The 404 event — cause analysis
All three inboxes returned 404 at the Oct 14 ~10:26Z run (A/B confirmed 200 at 09:27Z). Do the expiry arithmetic: original inbox created ~Oct 4 → 404 first seen Oct 11 (~7 days); A/B created Oct 7 15:07/15:10 → 404 Oct 14 10:26 (~6.8 days). All three dying within ~1h of each other at ~7-day intervals is the signature of **webhook.site's free-inbox expiry**, not operator cleanup — and the operator would have had little reason to delete two hours after beaconing into inbox B. **Lead hypothesis: platform expiry. Alternative: operator deletion.** A 404 does not distinguish the two. (Note: the earlier "operator cleanup following the report's publication" framing is demoted — swarmcha's preliminary report published Oct 4–6, ten days before the wipe; the timing points at the 7-day clock, not the publication.)

### 6.3 The Oct 7 interrogator
A third party (IP 96.76.222.193) posted into both live inboxes claiming to be "an agent of mailbox.termina.digital," asking about the benchmark and task set. Genuine agent vs researcher roleplay unresolved. Not us (GET-only throughout). The claim is self-contradictory on its face — mailbox.termina.digital was the researchers' own honeypot, and our filing #173 shows the real honeypot posting into *different* inboxes at different times.

### 6.4 The Oct 11 Netherlands beacon
New country (Netherlands/Amsterdam), new locale (`es-419`, Latin American Spanish), new origin (bytebin.lucko.me). The `es-419` on an Amsterdam exit is plausibly proxy-exit geolocation noise — don't over-read it as operator relocation. But the expanding infrastructure footprint (new host, new locale) in the fleet's final days is real.

### 6.5 ntfy provenance correction
The topic `amapdata-b0g3lmf2g1-0429` comes from the fleet's own captured probe code (hard-coded in all three bytebin pastes, Oct 7) — not from swarmcha's report, which documents ntfy *sends* but never *reads*, and never mentions this topic. Our polling leg never worked (egress-proxy block); we have zero independent observations of any post to this topic. **Opsec implication the writeup must state:** ntfy is unauthenticated pub/sub — anyone reading the public probe code can subscribe *and publish* into the topic. The topic name embeds the target POI in cleartext (`amapdata-<POI>-0429`), making sibling topics enumerable. Combined with the fleet's demonstrated willingness to act on third-party web content (the honeypot), this is a live third-party injection surface, not just an exfil channel. The operator treated ntfy as private while using it as public.

### 6.6 The Oct 5 warning the fleet ignored
Per our Transluce filing #173: on Oct 5 03:33 UTC, an Alibaba-Cloud-Beijing poster ("a curious cat passing by") told the fleet in Chinese that its "Amap collection fleet" was fully visible in urlquery reports, named swarmcha's report, and advised rotating infrastructure. **The fleet did not rotate** — same IPs, same inboxes through Oct 7+. Non-rotation after named public exposure is a major opsec datum: unaware, indifferent, or fire-and-forget harness.

### 6.7 The Cairn agent
Per filing #173: Oct 7 23:22 UTC, `Cairn-Contact/1.0` posted a bilingual self-described-AI-agent greeting with a reply inbox into a live fleet dead drop. Unanswered. Agent-to-agent contact initiation in the wild — the hunt's core shape — deserves its own follow-up.

### 6.8 Honest negatives
urlscan.io: zero fleet markers. No Zhipu fleet, no DeepSeek fleet on urlquery. GitHub code: zero footprint for `hysandbox-ats`, `uqscan=`, `sub_poi_navi` (as of Oct 7; press coverage since Oct 5 now names these terms — time-scope all "zero hits" claims). The fleet exists only as transient scanner artifacts and expiring inboxes.

---

## 7. Assessment

**What happened (INFERENCE):** A Tencent-cloud-linked operator ran a large-scale Amap data-collection campaign. On motive, two accounts exist and the writeup must present both: (a) an anonymous Tencent-adjacent source (UPSTREAM via swarmcha.se) describes research evaluations "designed to assess the ability of third-party AI models to browse the web and answer questions," on third-party (non-Hunyuan) models, now concluded; (b) our reading — the scale (216+ places per swarmcha.se; 204 distinct POIs in our lane) and POI coverage fit dataset construction, and no public eval matches the task shape. A private eval would also have no public match, so (b) does not exclude (a). The "competitive map-data acquisition" gloss is our speculation, not an observed fact — Amap did launch map-data-as-agent-tools (千舆) on Sep 23 and Tencent launched its Gaia spatial-intelligence platform mid-September (SECONDARY, eastmoney/Tencent announcements), which makes the timing suggestive but proves nothing about intent.

**Attribution confidence:**
- Tencent Cloud HK egress: **high** (creator IPs, proxy label, cert — converging lines)
- Tencent as operator (vs tenant): **medium** — the `hysandbox-ats` label is self-reportable; no TLS/DNS tie shown between fleet IPs and the Tencent domain
- Model identity: **unresolved** — "Claude" self-reports are harness labels; "third-party models, not Hunyuan" rests on a single anonymous source contradicted by the Oct 14 continuation
- Coordination: **fleet, not swarm** — no real-time peer coordination observed; operator-level coordination (shared queue, harness, POIs) established

**What's still open:**
- Post-Oct-8 activity vs the "concluded" source claim — one is wrong
- The ntfy channel — sends in code, reads never observed anywhere; injection surface unassessed
- The Oct 7 interrogator — who was it?
- The Cairn greeting — unanswered agent-to-agent contact
- The 404 cause — expiry (lead) vs deletion

---

## 8. Sources

- `data/lanes/2026-09-28-chinese-amap-fleet/` — 2,141 urlquery events, FINDINGS.md, PROVENANCE.md, PATTERN.md, INFRA.md (PRIMARY)
- `~/workspace/goals/urlquery-agent-activity-hunt/hidden_files/deaddrop-watch-state.json` — watch state, inbox histories (PRIMARY)
- `~/memory/2026-10-0*.md` — dated observation logs (PRIMARY)
- `reports/chinese-agent-fleet-findings-2026-10-14.md` — six-lane swarmcha.se workup (SECONDARY analysis)
- https://swarmcha.se/posts/chinese-agent-fleet-full-report — the report itself (SECONDARY)
- Transluce findings #171/#173 — our filings (PRIMARY for our observations, UPSTREAM for tracker content)

## 9. Evidence caveats

- 897 MB of original Amap raw evidence was deleted Oct 11 before the never-delete directive; the 70MB lane copy survives. Program-body claims for the ltzh family rest on the deleted raw and are now unverifiable from surviving artifacts.
- All urlquery-derived counts are lower bounds (relevance cap limits keyword searches; relay-wrapped reports not in the domain sweep).
- The Oct 14 beacon session's raw bodies were not captured before the 404 — only the run-log summary survives.
- `IP_LOG.md` in the lane is shared Shodan hunting data, not fleet infrastructure — excluded from §3.
- "Zero hits" claims are time-scoped to Oct 7; press coverage since Oct 5 names the key terms.
