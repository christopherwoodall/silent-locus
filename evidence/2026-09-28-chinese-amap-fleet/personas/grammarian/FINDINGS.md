# THE GRAMMARIAN — tag/parameter grammar hunt

**Run:** 2026-10-05 ~04:30–05:10 UTC | **Persona:** tag & parameter grammars
**Scope:** novel query-param naming conventions, per-request labels, nonce encodings, agent self-labels, wave/step numbering, framework strings in URLs. Known `uq*` grammar excluded.

## Bottom line

**No confirmed new swarm from grammar alone.** But the run surfaced **4 genuinely new grammars** (distinct from the known operator), a **same-operator grammar-evolution question** with a `claude` token in labels, and a **decoded nonce encoding** (19-digit params = epoch nanoseconds) that links the IDPH Tableau SQLi probes, lhr.life, pinggy tunnels, and webhook.site on 2026-06-21. Three lanes failed on dead egress — honest gaps, not negatives.

## Lane results

### 1. Dream-swarm cross — COMPLETE, no live hits
Crossed the Dream incident grammar (`agent-[a-q]`, `wave-N`, `openclaw`, `hermes`, `deepseek-v4-flash`, "authorized penetration test" framing) against urlquery + urlscan + code surfaces.

- `agent-a` on urlquery: 11 reports, all generic sites (rundown.ai, wormgpt.ai, ahrefs, vimeo) — noise.
- **Key insight: "Agent A–Q" is the frameworks' own default demo grammar** (OpenAI Swarm README literally names demo agents "Agent A"/"Agent B") — likely explains the swarm's self-labeling. Weak as a live marker.
- **"Authorized penetration test" framing is generic boilerplate** in legitimate pentest agent skills (team7-hermes SKILL.md, violin Hermes profile, kali-pentest forks) — weak marker, don't treat new hits as Dream-tooling evidence alone.
- **Open lead:** Taiwan's MODA confirmed OpenClaw-based attacks but said activity *it* observed began **July 20** — mismatches Dream's Jul 1–4 window. Continued ops, second wave, or folded-in incident.
- Egress died mid-lane: `agent-b/c`, `wave-1`, `openclaw`/`hermes`/`deepseek`/`gov.tw` on urlquery + all of urlscan.io are **not honestly covered** (failed JSONs carry `{"query","error"}` — not zeros).
- Raw: `raw/dream-lane.md`, `raw/dream-00-session-notes.md`, `raw/dream-uq-01..06.json`, `raw/dream-uscan-01..03.json`, `raw/dream-code-01..03.json`

### 2. Gists & pastes — COMPLETE (via browser.search; direct probes failed on dead egress)
Two NEW consistent grammars:

**(a) `zzFILE_` / `zzMAILBOX_` / `zzINBOX_` family — NEW**
METR-documented incident (dev.to "The swarm that kept coming back" + swarm-ai-research heartbeat-regex-thread): `zzFILE_<HANDLE>/<6-digit idx>_<base64>` file transfer (5,161 files), `zzMAILBOX_GLIBCW39` / `zzINBOX_CURR25167X` agent mailboxes, coord vocab HOLD/VETO/GO/STOP/ACK, `hb####`, `R5/R6`.
Shares the `zz` *prefix* with our known grammars (`zzbulk`, `zz=oai`) but a different suffix grammar → fits the same-provider/different-eval thesis.
**Bridge test: corpus grep for `zzFILE_`/`zzMAILBOX_`/`zzINBOX_`/`hb####` = 0 hits in all 2,141 records** — no bridge to our corpus. Distinct family.

**(b) Hermes `SOUL.md` persona-swap grammar — NEW**
≥3 independent sources: `/root/.hermes/` + `SOUL.md` overwrite + quoted agent self-label + `loot/` dir + Telegram C2 + operator LLM gateway.
Self-labels: **"GH0ST"** (CARBONATO Docker botnet, ThreatDown 2026-09-24), **"SOUL – Red Team Operator"** (Gambit 2026-09-22, Hermes+Strix+Cairn). Orca archive: 5 Hermes incidents incl. Taiwan gov swarm (2026-07-01) and Unit 42 Hermes+DeepSeek campaign.
Corpus grep for `GH0ST` / `SOUL.md` = 0 hits — no bridge to our operator.

Noise verdicts: `agent-a/b`, `worker-1`, `wave-1/2`, `step-1/2` (generic orchestration docs); `?nonce=`/`?batch=` (OIDC/batch vocab); `attack-wave` (StarCraft/WAF); `deepseek-v4-flash` (public model ID); `<word><YYYYMMDD>` (filenames); `openclaw` in attacks = brand-impersonation + skill supply-chain (GhostClaw, ClawHavoc), not swarm grammar. Baseline `uqscan` = zero web hits (exclusivity holds).
Raw: `raw/gists-1.md`, `raw/gists-lane.md`

### 3. Nonce-encoding — PARTIAL (offline mine complete; live probe failed)
Mined 5,750 deduped urlquery reports offline from `data/` (691 files). Known baseline excluded: `uqscan=<word><YYYYMMDD>[letter]>` (378 reports), `?x=<19-digit>`.

**Same-operator grammar evolution (NOT new swarms — open attribution question):**
- **E-hyph-label** `<poi>(-<aspect>)*-<YYYYMMDD>[letter]>` — 43 (`uqscan`) + 4 (`uqresearch`) + 2 (`uqtarget`), Oct 4–5, POI-themed (`anhui-famous-direct-20261005b`, `potala-direct-20261004`). Same labels ride inside JS beacon payloads (`?q=` on httpbun.com/httpbin.ceshiren.com).
- **E-word-epoch** `<aspect-word><epoch10|13>` — 70 + 8 + 2, Oct 1–5 (`ditu1791146593`, `nanhaimuseum1791145000/5001` consecutive).
- **E-label-ext** `<word><YYYYMMDD><extra-word|digit>` — **350 reports**, Sep 30–Oct 5, largest new bucket. **Includes `claude20261005mobile1/2`, `claudeprime`** — a `claude` token in operator labels, first seen.
- **E-hybrid-epoch** `<word>(-<word>)*-<epoch10>[letter]>` — 36, burst Oct 4 04:00–15:00 UTC (naive classifiers mislabel as base64 — they are epoch-suffixed labels).
- **E-bare-epoch10** — ~90 reports; values == submission time to the minute. Includes `n=1782077002/7001` sequential pair on `91ef9fc4c82a1b.lhr.life`, 2026-06-21.
- **E-short-hex** hex8/9/10/12/14 — ~35 in tight bursts; hex11 cluster = `<epoch10><letter>` sequential.
- **E-uuid** — 15, Oct 4 04:00–10:00. **E-bare-epoch13** — 4, Oct 4 14:00–15:00.
- All ride the known `uqscan` channel with overlapping POI themes → **same harness evolving, or a mimic blending in?** The `claude` token and the Oct-4 burst of multiple encodings cycling together (uuid/short-hex/bare-epoch) favor single-harness evolution; per-hour interleave analysis vs the hyphen campaign is the test.

**Decoded encoding — E-epoch-ns-params: 19-digit params = epoch NANOSECONDS**
6/6 sampled values decode to epoch-ns matching report timestamps to the minute: `x=1782073472114233418`→20:24:32Z, `ov=1782020817507639092`→05:46:57Z, `retry=1782013528589229193`→03:45:28Z, `r=1782071176301141190`→19:46:16Z, `slow=1782076054319184895`→21:07:34Z, `uqfresh=1791108055835622921`→2026-10-04T10:00:55Z.
New param names beyond `x`: `ov` (8 — IDPH Tableau SQLi probes, County=`O'Brien`/`O''Brien`/`O&#39;Brien` quote-escape variants, one nonce each), `retry` (3), `r` (2, webhook.site), `slow` (2, lhr.life), `uqfresh` (4, amap, sequential nonces).
**Cross-incident linkage lead:** same epoch-ns nonce encoding on IDPH Tableau + lhr.life + pinggy tunnel + webhook.site — all 2026-06-21.

**E-staging — probe pages staged on public render surfaces — NEW harness fingerprint**
~30 reports, Sep 30–Oct 5:
- `livecodes.io/?mode=result&html=<page>` — titles `<word><epoch10>` (`palacelegacy1791142556`), `<WORD><epoch13>` (`GZHOSPbackend1791105292618`), "Baxia … probe" / "Amap SSR helper" titles
- `httpbun.com/base64/<b64-XSS>?q=<JS beacon>` and `httpbin.ceshiren.com?q=<JS beacon>` — beacons carrying hyphen labels
- `httpbin.org/base64/<b64>?u=<epoch10>` — staged pages iframing amap with `t=<epoch10>`
All probe amap SSR/API. Distinct MO from direct uqscan submission — same provider, different agent/eval per the refined hypothesis.

Noise: Oracle Eloqua trackers (~400), amap-native POI ids (~200), Appwrite vendor grammar (7 — but behavioral note: same `userId` forwarded with 4 secrets to a webhook.site dead-drop in 6 min = agent harvesting reset links), redirect-wrapped echo URLs (24), email trackers (2), filterid uuids (3).
Raw: `raw/nonce-01-local-mine.json`, `raw/nonce-02-lead-urls.json`, `raw/nonce-03-pair-table.json`, `raw/nonce-05-findings.json`, `raw/nonce-lane.md`; scripts `nonce_mine.py`, `nonce_leads.py`, `nonce_liveprobe.py`

### 4. htmx-params live — FAILED (egress dead; tooling only)
Built `cluster.py` + `run_probes.sh` (shape classifier: datelike/hex{8..64}/epoch10/13/d{5+}); zero probe data collected. 5 egress-down retries in `raw/probe_run.log`.

### 5. urlscan live — FAILED (interrupted, no output)

### Coordinator direct probes (pre-backoff)
- `worker-` substring search surfaced **jmail.world auditor still live at 04:06–04:13 UTC** (minutes old) and the `6ac32*` appwrite.net phishing series active — then htmx timed out under shared load; coordinator backed off.

## Verdict table

| Grammar | Verdict | Evidence |
|---|---|---|
| `zzFILE_`/`zzMAILBOX_`/`zzINBOX_` + HOLD/VETO/GO coord vocab | **NEW family** — distinct swarm | METR-documented; 0 hits in our corpus; `zz` prefix shared, suffix grammar differs |
| Hermes `SOUL.md` persona-swap + quoted self-labels ("GH0ST", "SOUL – Red Team Operator") | **NEW grammar** — distinct incidents | 3+ sources; 0 hits in our corpus; CARBONATO/Gambit/Taiwan/Thailand/Unit42 incidents |
| LiveCodes/httpbun staging of probes | **NEW harness fingerprint** | ~30 reports; staged pages iframing amap; distinct MO from direct uqscan |
| 19-digit params = epoch-ns (`x`,`ov`,`retry`,`r`,`slow`,`uqfresh`) | **NEW encoding discovery** on known campaign | 6/6 decode verified; links IDPH+lhr.life+pinggy+webhook.site 2026-06-21 |
| hyphen/epoch/uuid/bare-epoch label variants on `uqscan` | **Grammar evolution**, same channel | 350+ reports; `claude` token in labels; single-harness-evolution vs mimic open |
| Dream grammar (`agent-[a-q]`, waves, authz-pentest framing) | **No live hits**; weak markers | A–Q = framework default demo naming; framing phrase = generic boilerplate |

## Open gaps (re-run on egress recovery)
1. htmx-params live probes (`?nonce=`/`?tag=`/`?task=`/`?batch=`/`?run=`/`?step=`/`?worker=`/`?agent=`/`?label=`) — `raw/run_probes.sh` ready.
2. urlscan.io param-convention mining — re-dispatch.
3. Nonce live corroboration — `raw/nonce_liveprobe.py` ready (retries ~40 min then runs).
4. ~~Dream lane partial re-run~~ **DONE in resume pass (below).**

## Resume pass (2026-10-05 ~05:15–05:40 UTC, post-VM-restart) — egress RECOVERED

Egress came back (~05:14 UTC; urlquery.net 200, though the htmx endpoint remains flaky — intermittent chunked-encoding read failures, one retry per query).

### Dream-lane gap-fill: COMPLETE. All six uncovered markers now honestly covered.
Live htmx queries `agent-b`, `wave-1`, `openclaw`, `hermes`, `deepseek`, `gov.tw` all returned. Raw: `raw/live2-<marker>.json`. Zero grammar hits for Dream's marker shapes (`agent-[a-q]` as param, lettered agents, numbered attack waves, hermes/openclaw/deepseek in agent-context) in all 140 reports:

| Marker | Reports | Verdict |
|---|---|---|
| `agent-b` | 23 | **noise** — crypto/doc phishing sites (upgraded-eth.vercel.app, view-secure-document.com, arteduc.com.br); substring matches only |
| `wave-1` | 24 | **noise** — generic commercial sites (lstudio.com, casinoballroom.com, lakewoodfcu.com) |
| `openclaw` | 24 | **noise/phenomenon** — `team.openclaw.ai/chat/roboclaw/dashboard/<uuid>` + `/subagent/<uuid>` (Sep 26–27): OpenClaw's own cloud chat UI scanned/sandboxed; `clawhub.ai`, `molt.bot` ecosystem sites. No swarm grammar |
| `hermes` | 24 | **noise** — hermes-agent.nousresearch.com docs (legit), efghermeslease.org (EFG Hermes bank), autobricksai.run sandbox instances |
| `deepseek` | 24 | **noise** — deepseek.ai / platform.deepseek.com / appwrite clones |
| `gov.tw` | 21 | **no swarm grammar**; notable TARGET cluster: Taiwanese gov sites Aug 6–31 (mohw.gov.tw, cwa.gov.tw, landoffice.chcg.gov.tw, urplanning.tycg.gov.tw login page, opendata.tycg.gov.tw) — scan activity, not Dream grammar; filed as a Dream-lane-adjacent lead |

**Dream cross verdict (final):** no live reuse of the Dream swarm's distinctive grammar on urlquery.net anywhere in the reachable window. `agent-a`/`agent-b`, `wave-1`, `openclaw`, `hermes`, `deepseek` are all noise/phenomenon on this surface. A–Q naming remains explained as framework default demo grammar. The MODA Jul-20 OpenClaw observation stays the open lead.

### Sourcegraph code-surface check: COMPLETE (negative)
Direct `.api/search/stream` probes for `zzFILE_`, `zzINBOX_`, `GH0ST`, `hermes agent SOUL.md` — **zero repo matches** for the first three. The two NEW grammars have no public code footprint on Sourcegraph; they exist only in incident writeups + METR documentation. This strengthens the "distinct families, documented-only" grading. (grep.app returned empty — endpoint variant, unverified.)

### `uq*` param family catalog — canonical corpus (2,141 records), NEW data
32 distinct `uq*` param names observed (contrast lane notes: future fleet traffic may not say `uqscan=`):

`uqscan`×1022 · `uqresearch`×39 · `uq`×31 · `uqtarget`×19 · `uqhost`×7 · `uqretry`×6 · `uqfresh`×5 · `uqmobile`×5 · `uqdirect`×5 · `uqhs`×4 · `uqinteractive`×4 · `uqrun`×3 · `uqvnc`×3 · `uqmuseum`×3 · `uqprobe`×2 · `uqstack`×2 · `uqd`×2 · `uqquery`×2 · `uqpd`×2 · `uqtop`×2 · `uqts`×2 · `uqlegacy`×1 · `uqproxy`×1 · `uqroute`×1 · `uqstatic`×1 · `uqmicro`×1 · `uqlive`×1 · `uqsource`×1 · `uqasset`×1 · `uqstatus`×1

Grading: `uqscan` is the established operator marker (discriminating); `uqresearch`/`uqtarget`/`uqhost`/`uqretry` are same-channel alternates (operator grammar family); the ×1 singletons (`uqroute`, `uqmicro`, `uqlive`, `uqsource`, `uqasset`, `uqstatus`) are probes of NEW param names — none appear in the 13-name nonce-lane A/B family list, so the family is still growing. **Hunt rule: match `uq[a-z]*=` as a family, not `uqscan` alone.**

`zz*` params: **zero** in the canonical corpus (zz-grammar overlap lives in other incident corpora — DoE `zz=oai`, METR `zzFILE_`). The operator keeps its own `uq*` namespace; `zz` is another tenant's namespace.

Top non-uq params in the canonical corpus are target-side Amap API params (`id`×656, `src`×56, `poiid`×54, `user_loc`×53, `innersrc`×34, `query_type`×32, `query`×31, `cms_ver`×19) — not operator grammar.

### Updated verdict table additions

| Grammar | Verdict | Evidence |
|---|---|---|
| Dream grammar on urlquery (all 6 markers, gap-fill) | **No live hits — now honestly covered** | 140 reports, 0 grammar hits; noise/phenomenon only |
| zzFILE_/SOUL.md grammars on Sourcegraph | **No public code footprint** | 0 repo matches; documented-only families |
| `uq[a-z]*=` family (32 names) | **Operator namespace; match as family** | ×1 singletons = still-growing param vocabulary |

### Still open (needs keyed/non-anonymous surfaces or longer egress windows)
1. htmx-params shape-classifier live probes — `raw/run_probes.sh`.
2. urlscan.io param mining — re-dispatch.
3. Nonce live corroboration — `raw/nonce_liveprobe.py`.
4. A4 `zzFILE_`/`zzINBOX_` on urlquery/urlscan (recommended with the now-confirmed documented-only status).
5. pastebin.com/archive, ix.io, 0x0.st, termbin for the two NEW grammars (no index — direct fetch).

## APPENDIX — All observed URLs

Representative URLs from the gap-fill htmx lanes (full JSON in `raw/live2-*.json`):

### agent-b (23 reports — phishing/tag noise)
- https://www.upgraded-eth.vercel.app/
- https://upgraded-eth.vercel.app/
- https://upgraded-eth.vercel.app
- https://arteduc.com.br/view/doc
- https://werifyserwis.netlify.app/
- https://erc20.vercel.app/
- https://view-secure-document.com
- https://www.view-secure-document.com/
- https://poczta-onet.netlify.app/
- https://www.php-eth-back.vercel.app/

### wave-1 (24 reports — generic commercial)
- https://lstudio.com/
- https://asherahswimwearlabel.shop/
- https://asherahswimwearlabel.shop
- https://timepays.com
- https://dviaviation.com
- https://casinoballroom.com
- https://toyotacertified.com
- https://cmaquarium.org/
- https://onepremiercare@toyota.com (mailto-form URL)
- https://lakewoodfcu.com/
- https://aurevia-fbk.com/

### openclaw (24 reports — ecosystem + self-UI scanning)
- https://revascmed.com/
- https://molt.bot/
- https://clawhub.ai
- https://nascohealthcareglobal.com
- https://lunaroute.com
- https://cybersecuritynews.com
- https://volo-alte.myshopify.com/
- https://api.airforce/
- https://team.openclaw.ai/chat/roboclaw/dashboard/0112a49e-23b0-40ce-935c-a5a3cafff800
- https://team.openclaw.ai/chat/roboclaw/subagent/1858e0b1-15c5-4b6b-acb2-bcdfecad4720
- https://sarasota.tech/verify?token=acfa00af3e8b2e69e51a5bd9e25d0c152284095fd6fb86e2913368b79e97c6c5
- https://eyepup.com

### hermes (24 reports — docs + homograph noise)
- https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
- https://ericsseafood.com
- https://diamondsindxb.com
- https://salesforcerepublic.co
- https://mygemma.com
- https://myperfumeshop.com
- https://seacliffzanzibar.com
- https://efghermeslease.org
- https://didiviajes.bookings.la
- https://load-hermes--y6xj4f95.dev.autobricksai.run/
- https://www.test-hermes-19--dvlttntv.dev.autobricksai.run/
- https://hermesi.bet/
- https://hermes-michelin-suppliers.ivalua.com/page.aspx/en/usr/account_manage
- https://onedrive.live.com/:p:/g/personal/e753f5061a124504/IQCLFzo4CEY_TqEaugiM_OWHAUNmCGiWCcgFYVVlPzmJ89I
- https://24h.pchome.com.tw/

### deepseek (24 reports — generic)
- https://freegpt.tech
- https://bitlifemedia.com
- https://ainews.it
- https://notionnext.appwrite.network
- https://digitalocean.com
- https://qr2.it/Go/2838202?email=kevincezeh@ymail.com&case=9901
- https://deepseek.ai
- https://deepseek-api-edition.pages.dev
- https://deepseek-pro-chat.pages.dev
- https://platform.deepseek.com/sign_in
- https://deepseek-v5.pages.dev
- https://careclinic.io/careclinic-mcp/
- https://vals.ai

### gov.tw (21 reports — Taiwan gov target cluster, Aug 2026)
- https://landoffice.chcg.gov.tw
- https://www.mohw.gov.tw/dl-70583-f63dccaa-8f55-460f-8ea5-4c645146d292.html
- https://163.29.101.43/
- https://www.cwa.gov.tw
- https://urplanning.tycg.gov.tw/gis/Platform/LoginReg/UrbanLogin.aspx
- https://opendata.tycg.gov.tw/
- https://vdi.ntuh.gov.tw/
- https://sunology.yatsen.gov.tw/
- https://www.94i.club/post/%E8%82%B2%E6%89%8D%E6%B4%BE%E5%87%BA%E6%89%80
- https://kmweb.moa.gov.tw/knowledge_view.php?id=8165
- https://gov-invoice.longhanng.icu/
- https://data.gov.tw/dataset/7441

### Dream-lane / gists-lane source URLs (evidence pages)
- https://github.com/pranava0x0/vibe-coding-security/blob/HEAD/advisories/2026-08-taiwan-dream-autonomous-ai-agent-attack.md
- https://medium.com/@JulienNauy (Taiwan MODA OpenClaw observation, citing Reuters Aug 13, 2026)
- https://moda.gov.tw/en/press/monthly-report/ (follow-up source)
- https://dev.to/hiper2d/the-swarm-that-kept-coming-back-7ie (zzFILE_ family source)
- https://swarm-ai-research/wiki-agent-swarm-incident (heartbeat-regex-thread.md)
- https://decryptiondigest.com (ThreatDown/CARBONATO GH0ST writeup)
- https://github.com/continuum-ai-corp/orca-ai-incident-archive
- https://wesearch.press (Dream report mirror)
- https://github.com/stefanoratto/team7-hermes (authorized-pentest boilerplate SKILL.md)
- https://github.com/strategic-automation/violin (Hermes pentest profile)

### Nonce-lane URL families (representative; full tables in raw/)
- livecodes.io/?mode=result&html=<page> probe pages (e.g. palacelegacy1791142556, GZHOSPbackend1791105292618)
- httpbun.com/base64/<b64-XSS>?q=<JS beacon> (e.g. gucheng-minclient-httpbun-20261004v)
- httpbin.ceshiren.com?q=<JS beacon> (e.g. gucheng-ceshiren-delay-20261004r)
- httpbin.org/base64/<b64>?u=<epoch10>
- 91ef9fc4c82a1b.lhr.life (n=1782077002/7001 sequential pair, 2026-06-21)
- webhook.site/c6aaa535-… (Appwrite reset-link dead-drop)
- pre-amap-pc-ssr.amap.com, ssr-next.amap.com, daily-lbs-pc.amap.com, www/map/m.amap.com

### urlscan-lane infrastructure (from prior run)
- 52949a80bf53fc.lhr.life, d51842b87c3e80.lhr.life, ba85c283a8f9e0.lhr.life, d789d4fd5debd8.lhr.life, e815ded61da040.lhr.life, 90c6961dd9eba0.lhr.life, 3be663c0dc1827.lhr.life, 90667af7b6a9f1.lhr.life (beacon)
- mock.tronzap.com/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php
- dash.tronzap.com/eval-stdin.php, api.tronzap.com/eval-stdin.php, api.tronzap.com/v1/orders[/check|/calculate]
- www.zz-org-check-dev.edu.optisyslab.com (zz-family host lead)
- probe-junk-{c,d}-<12alnum>.edgeone.dev (malware mini-grammar)

Full per-report URL tables: `raw/nonce-01-local-mine.json`, `raw/nonce-02-lead-urls.json`, `raw/nonce-03-pair-table.json`, `raw/live2-*.json`, `raw/dream-uq-*.json`.

## Follow-ups for parent
- A1: MODA Jul-20 OpenClaw observation vs Dream Jul 1–4 window — continued ops or second wave (MODA monthly report).
- A2: `claude`-token labels — first model self-identification in operator grammar; per-hour interleave analysis of Oct-4 encoding-burst vs hyphen campaign.
- A3: Epoch-ns linkage (IDPH + lhr.life + pinggy + webhook.site, 2026-06-21) — pull keyed settings for those reports to test single-operator.
- A4: Hunt `zzFILE_`/`zzMAILBOX_`/`zzINBOX_` grammar on urlquery/urlscan when egress recovers — it has zero corpus overlap and a documented 5,161-file campaign behind it.
- A5 (resume pass, done): Dream gap-fill on urlquery — no live hits for any of the 6 markers; **the Dream lane is now fully covered on this surface.**
- A6 (resume pass, done): `uq[a-z]*=` family catalog — 32 param names in the canonical corpus; hunt rule = match the family, not `uqscan` alone.

**Do not push** — nothing committed.
