# ITALIAN AGENT HUNTER — FINDINGS

**Date:** 2026-10-05 (UTC)
**Persona:** foreign-agent hunt, Italian surfaces
**Status:** complete. No confirmed Italian-run agent found. One agent-shaped cluster (ACN catalog walk), unconfirmed.

## 0. Method log

1. Read BRIEF.md. Tested egress: urlscan.io = 200 live; urlquery.net reachable via curl (the `/search/` path 404s — expected, htmx API is the interface). Python `uq_htmx.py` hit `IncompleteRead` chunk errors → switched to curl-based `uq_htmx_curl.py` (same fallback the Global South chase used), ≤1 req/5s with sleeps.
2. Grepped local corpora for Italian markers (`.it/`, `gov.it`, `prova=`): amap fleet = 0, openai-agent-traces = 0, oai-tag-sweep = 14.
3. Ran live urlquery htmx searches: `gov.it` (limit 100), `acn.gov.it`, `italia`, `prova`, `star-vegas`, `governo`, `ministero`, `regione`, `comune`, `casino`, `scommesse`, `slot`, `poker`.
4. Pulled full HTTP-transaction data keylessly via `/api/htmx/report/{id}/filter/http` for 9 reports; scanned for UA strings and probe grammar (`uqscan=`, `zz=`, `src=`, `utm_source=`).
5. Queried urlscan.io (anonymous: exact-domain only, no wildcards) for gov.it targets and star-vegas.it.
6. Verified every candidate report ID against our three sets (amap 2,141 / openai-agent-traces 589,972 / oai-tag-sweep).
7. Reviewed border-crosser's `star-vegas.it` ltzh casino-stratum lead in its FINDINGS.md.

**Methodological note (per Polyglot):** htmx keyword search does not surface all known-live records — zeros are weak negatives, not absences.

## 1. Headline lead — ACN cloud-catalog walk (agent-shaped, unconfirmed)

Four urlquery reports on **2026-07-06** walking the cloud-infrastructure catalog of **ACN — Agenzia per la Cybersicurezza Nazionale** (Italy's national cybersecurity agency):

| Time (UTC) | Report | URL |
|---|---|---|
| 09:43 | `33a0abaa-e8db-408c-b353-9e4a7c361dd2` | `www.acn.gov.it/portale/en/cloud/qualificazione-e-adeguamento` |
| 12:54 | `85733677-db6e-44ac-99d6-2932bd3929a4` | `www.acn.gov.it/portale/w/sa-5183` |
| 13:26 | `d5692101-e505-450e-840f-511614a28873` | `www.acn.gov.it/portale/catalogo-delle-infrastrutture-digitali-e-dei-servizi-cloud?start=19` |
| 15:26 | `89b68b54-43d3-4dfc-85da-759b93de4280` | `www.acn.gov.it/portale/catalogo-delle-infrastrutture-digitali-e-dei-servizi-cloud?start=50` |

Shape: qualification page → specific solution record → paginated catalog at offset 19 → offset 50, over ~6 hours. This is methodical page-by-page enumeration of a national cyber agency's cloud-services catalog — agent-shaped pacing (a human researcher could do the same, so attribution is unconfirmed).

Counter-evidence: all four carry the stock urlquery Firefox 134 scanner UA and zero probe grammar (`uqscan=`, `zz=`, `src=` all absent). No `related/similar` linkage keylessly. None appear in any of our three corpora → **GENUINELY NEW**, not ours, not previously known to us.

**Grading:** agent-shaped behavior, unconfirmed submitter. Worth an exit-node check if authenticated API access frees up (the four reports' `settings.exit_node` values would show whether one submitter walked all four).

## 2. gov.it sweep — 23 reports total

Keyword `gov.it` (limit 100) returned 23 reports. Beyond the ACN cluster:

**Sensitive targets, routine-looking scans (all stock UA, no probe grammar, bare pages):**
- `fbda219f-4762-49d8-9dff-c688c6183258` — `www.sicurezzanazionale.gov.it/` (intelligence service homepage), 2026-07-15T08:57Z. Full HTTP pull: bare homepage, stock UA. Researcher-shaped, not agent-shaped.
- `da1097cc-d17e-4c75-8b71-d82bea8a7d73` — `www.agenziaentrate.gov.it/portale/home` (revenue agency), 2026-08-30T00:54Z. Same shape.
- `316a43cd-8b44-4989-9e62-be183a8e68d0` — `ministeroturismo.gov.it/` (tourism ministry), 2026-09-20T10:01Z. Same shape.
- `f0e43556-…` — `servizionline.aifa.gov.it/jam/UI/Login?goto=...` (medicines agency SAS login), 2026-06-10.
- `ff05ccbe-…` / `299b2855-…` — `www.aifa.gov.it` homepage + documents, 2026-05-19.
- `2d19859f-…` — `www.fascicolosanitario.gov.it/portale/interfacce-programmatiche-dei-servizi-di-interoperabilità` (national health-record system's API-interop page), 2026-07-02. Sensitive surface; single scan.
- `eb4ee2fa-…` — `www.indicepa.gov.it/ipa-portale/...` (public-administration index), 2026-07-13.
- `83dc5c78-…` — `www.dipendenze.gov.it/it/notizie-e-approfondimenti/dipendenze-le-droghe/la-cocaina` (drug-policy cocaine page), 2026-05-19.
- `6bf32c18-…` — `serviziomarconi.w.istruzioneer.it/` (education), 2026-06-23.

**Noise / not agents:**
- `5328f03a-…`, `7fd6c2c7-…`, `568d2679-…`, `e123f7a5-…` — `opportunitaly.gov.it/join-opportunitaly?utm_source=cognitive...` ×4 (investment-promotion marketing leadgen links submitted to urlquery; `utm_source=cognitive` is a marketing tag, not a probe).
- `b55a751d-…` — `comunepigna.traspare.com/employees/sign_in` (municipality transparency-portal login), 2026-07-17.
- `3fdab13f-…` — `search.app/oFyi9L9YMSfqLoZp6` (matched via page content).
- `2b7e3b40-…` — `privatetrafficmanager.eu/api/code-redirect/...` (ad-tech).
- `4c1ef34f-…` — `www.durstoase24.de/`; `2198e1d2-…` — `byzant.sk/kdaskk.html` (content matches, not Italian targets).

All 11 checked IDs are **absent from our three corpora → GENUINELY NEW**, but none show agent-shaped markers. Verdict: Italian gov targets get routine scans; no agent campaign detected.

## 3. Casino / gambling vertical

- **`star-vegas.it`: zero** on urlquery htmx AND zero on urlscan.io. The border-crosser's ltzh casino-stratum lead (6 casino domains submitted 2026-10-04 12:58–13:15 during the operator's R&D burst) remains **flagged, not claimed** — the domains are too fresh or too private to verify keylessly. No contradiction, no confirmation.
- Broad casino searches (`casino`, `scommesse`, `slot`, `poker`) returned phish/scam submitter noise (`.vip` scam domains, adult, `stakeglobals.com`) — not our agent family.
- `scommesse` keyword surfaced a **separate Italian SEO-spam cluster**: bare `.it` SMB domains submitted in a burst 2026-10-04 13:36–14:29 (`somsbistagno.it`, `ever-greensnc.it`, `casacattolica.it`, `valentini-srl.it` ×2 across Oct 3–4, `gustosamenteitalia.it`, `fib Toscana`). Mass bare-domain submission is agent-shaped, but the target set (small Italian businesses) and keyword context (betting-spam-injected pages) point to an SEO-spam operation, not the ltzh operator. Noted as a distinct family, not pursued.

## 4. Italian-language markers

- Keyword `prova` / `italia`: matched Italian .it domains in scan noise, no probe grammar found. No `prova=` parameter usage detected in any pulled report.
- The 14 oai-tag-sweep `.it` hits are **OURS (KNOWN)**: Italian domains (`packlink.it`, `morss.it`, `studioguatta.it`, `salaristraslochi.it`, …) as *targets* inside cors-laundering-ops wrapper reports from the frozen corpus. `morss.it` is an Italian URL shortener. These are campaign targets, not Italian-run agents.
- amap fleet (2,141) and openai-agent-traces (589,972): **zero** Italian markers. If Italian-run agents exist, they are not in our corpora.

## 5. Italian infra as staging / paste surfaces

- No agent-staging signals found on Italian hosting (Aruba/Seeweb) in this sweep — low EV, not deep-dived.
- urlscan exact-domain searches found **phishing impersonations, not agents**: `agenziaentrate.gov.it.ss-bpi.eu.cc` (revenue-agency phish) and `rinnovidomini-gov.it` (domain-renewal phish). Infrastructure-crime, not agent-shaped; noted and not pursued (scope is agents).

## 6. Verification summary

Every candidate report ID in §§1–2 was grepped against all three corpora: **all absent → GENUINELY NEW** (none OURS, none KNOWN). But absence from our sets ≠ agent-shaped: only the ACN catalog walk shows agent-shaped behavior, and it is unconfirmed.

## 7. Open leads

1. **ACN walk attribution** — check `settings.exit_node` on the four ACN reports when authenticated API budget allows (ua-burst-retry owns the budget). Same exit node = one submitter = stronger agent case.
2. **fascicolosanitario API-interop page** — single scan of a sensitive health-data API surface; worth a `related/ip` check later.
3. **star-vegas.it / ltzh casino stratum** — still needs an authenticated or fresher-source check; too fresh for public indexes.

## 8. Complete URL list (observed)

### gov.it reports (urlquery)
- https://urlquery.net/report/33a0abaa-e8db-408c-b353-9e4a7c361dd2
- https://urlquery.net/report/85733677-db6e-44ac-99d6-2932bd3929a4
- https://urlquery.net/report/d5692101-e505-450e-840f-511614a28873
- https://urlquery.net/report/89b68b54-43d3-4dfc-85da-759b93de4280
- https://urlquery.net/report/fbda219f-4762-49d8-9dff-c688c6183258
- https://urlquery.net/report/da1097cc-d17e-4c75-8b71-d82bea8a7d73
- https://urlquery.net/report/316a43cd-8b44-4989-9e62-be183a8e68d0
- https://urlquery.net/report/5328f03a-e43d-4918-9a1a-d327662be8f6
- https://urlquery.net/report/b55a751d-5451-4923-ac85-529cae5ed876
- https://urlquery.net/report/7fd6c2c7-13db-4254-9f00-467c3ba95b27 (partial id from search; opportunitaly)
- https://urlquery.net/report/eb4ee2fa (partial; indicepa)
- https://urlquery.net/report/2d19859f (partial; fascicolosanitario)
- https://urlquery.net/report/6bf32c18 (partial; serviziomarconi)
- https://urlquery.net/report/568d2679 (partial; opportunitaly)
- https://urlquery.net/report/f0e43556 (partial; aifa login)
- https://urlquery.net/report/e123f7a5 (partial; opportunitaly)
- https://urlquery.net/report/ff05ccbe (partial; aifa)
- https://urlquery.net/report/299b2855 (partial; aifa documents)
- https://urlquery.net/report/83dc5c78 (partial; dipendenze)

### Submitted target URLs
- https://www.acn.gov.it/portale/en/cloud/qualificazione-e-adeguamento
- https://www.acn.gov.it/portale/w/sa-5183
- https://www.acn.gov.it/portale/catalogo-delle-infrastrutture-digitali-e-dei-servizi-cloud?start=19
- https://www.acn.gov.it/portale/catalogo-delle-infrastrutture-digitali-e-dei-servizi-cloud?start=50
- https://www.sicurezzanazionale.gov.it/
- https://www.agenziaentrate.gov.it/portale/home
- https://ministeroturismo.gov.it/
- https://www.fascicolosanitario.gov.it/portale/interfacce-programmatiche-dei-servizi-di-interoperabilit%C3%A0
- https://www.indicepa.gov.it/ipa-portale/consultazione/indirizzo-sede/ricerca-ente/elenco-unita-organizzative
- https://www.dipendenze.gov.it/it/notizie-e-approfondimenti/dipendenze-le-droghe/la-cocaina
- https://serviziomarconi.w.istruzioneer.it/
- https://servizionline.aifa.gov.it/jam/UI/Login?goto=https://bi.aifa.gov.it:443/SASLogon/login
- https://www.aifa.gov.it
- https://www.aifa.gov.it/documents
- https://opportunitaly.gov.it/join-opportunitaly?utm_source=cognitive&utm_medium=email&utm_campaign=Australia_leadgen_Inglese_Buyer_cpl_
- https://comunepigna.traspare.com/employees/sign_in

### Other observed
- https://urlquery.net/api/htmx/report/fbda219f-4762-49d8-9dff-c688c6183258/filter/http (keyless endpoint used)
- https://urlscan.io (exact-domain searches; anonymous tier, no wildcards)
- star-vegas.it — zero results (urlquery + urlscan)
- agenziaentrate.gov.it.ss-bpi.eu.cc (phishing impersonation, urlscan)
- rinnovidomini-gov.it (phishing impersonation, urlscan)

## 9. Bottom line

No confirmed Italian-run agent. The one genuinely agent-shaped finding is the **2026-07-06 ACN cloud-catalog walk** — four reports enumerating Italy's national cybersecurity agency's cloud-services catalog over six hours — but it is unconfirmed (stock scanner UA, no probe grammar, no linkage keylessly). Everything else is routine researcher scans, marketing noise, phishing, or a separate SEO-spam family. All candidates verified absent from our corpora: genuinely new to us, mostly not agent-shaped.
