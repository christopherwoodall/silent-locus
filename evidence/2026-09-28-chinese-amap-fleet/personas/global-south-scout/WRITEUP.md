# Global South Scout — Full Writeup
## Agent activity outside China and the US

**Persona brief:** hunt AGENT activity outside China and the US. Agents, not operators — no human attribution. Agent shape = timing + action + grammar, not language.
**Run:** 2026-10-04 ~23:40 CDT → 2026-10-05 04:55 UTC. Four regional scouts (LatAm, SE/S Asia, Africa, Middle East/Central Asia) + coordinator direct hunting.
**Method note:** an egress outage (~04:37–04:55 UTC) killed live urlquery.net access mid-run; scouts pivoted to streaming grep over ~935 MB of local corpora (73–80 `data/*/events.jsonl` + 12 `collections/*/data/*.jsonl`). Local corpora skew toward known incidents — absence locally does NOT establish absence on urlquery.net. Live re-checks pending.

---

## 1. Indonesia — programmatic agent scanning of local government sites (STRONGEST, previously unreported)

Five frozen urlquery incident records (`data/2026-10-01-oai-tag-sweep/events.jsonl`, source `frozen:urlquery-incidents`), all tagged `urlquery-hunt` + `agent-activity`, campaign `cors-laundering-ops`, indicator `cors_conversion_proxy`. Span: **2026-07-08 → 2026-08-31**.

| # | Date (UTC) | Submitted URL | Target | Report ID |
|---|---|---|---|---|
| 1 | 2026-07-08 05:38 | `pa-gresik.go.id/index.php?option=com_media` | Gresik religious court, Joomla media manager | `1df03d5a-ba13-474d-8036-26fe31526ee7` |
| 2 | 2026-07-15 04:44 | `jdih.balikpapan.go.id/dokumen/610/detail?utm_source=chatgpt.com` | Balikpapan legal-documents portal | `faa48376-8a90-4980-a965-357ad03914e7` |
| 3 | 2026-07-15 07:41 | `www.dinkes.semarangkota.go.id/` | Semarang city health office | `a9c7e089-c55a-4a95-8d41-c57cd6cb346a` |
| 4 | 2026-07-19 07:42 | `dinkes.acehprov.go.id/detailpost/abcde-cegah-stunting` | Aceh province health office (stunting-prevention post) | `09195203-e3e2-4e42-92b1-735a684ff56f` |
| 5 | 2026-08-31 02:43 | `www.kkp.go.id/djpdskp/kkp-permudah-produk-umkm-tembus-pasar-global-dengan-gmp-sertifikat65c30481d5d51/detail.html` | Marine Affairs & Fisheries ministry (GMP certificate article) | `1e16f79e-0006-48e2-b450-1d99f6a78165` |

**Agent-shaped because:**
- CORS-laundering relay wrapper on every hit (`cors_conversion_proxy` indicator)
- `?utm_source=chatgpt.com` self-identification on the Balikpapan URL — a URL copied out of a ChatGPT answer, then fed through an agent pipeline
- Hex nonce `65c30481d5d51` embedded in the KKP article path — machine-generated path component
- Municipality-by-municipality enumeration: two district health offices (Semarang, Aceh) probed ~3 hours apart on Jul 15 — geographic walk pattern
- Tags `urlquery-hunt` + `agent-activity` on all five (these are hunter-applied labels in the frozen sweep, not submitter tags — treat as triage signal, not ground truth)

**Verdict:** programmatic agent scanning of Indonesian local-government sites. Strongest non-China/non-US agent trace in this sweep. Nobody has reported it.

---

## 2. Brazil — agent fetches of telecom regulator + sports ministry (one-offs, NOT a campaign)

Three records, same corpus, indicator `jina_allorigins_dagd` (jina + allorigins + da.gd CORS-laundering), campaign `cors-laundering-ops`:

| Date (UTC) | Submitted URL | Target | Report ID |
|---|---|---|---|
| 2026-07-19 06:04 | `anatel.gov.br/` | Brazilian telecom regulator (ANATEL) | `dd4fa017-96a3-4d7a-9753-409a525b99ba` |
| 2026-08-13 13:48 | `www.anatel.gov.br` | ANATEL again | `b11fd092-3a5b-4fbd-a552-7feae342f9c4` |
| 2026-08-14 23:14 | `esporte.gov.br/` | Brazilian Ministry of Sport | `46e7c66d-c64f-4183-b675-1f10e0b2ca4d` |

Agent-shaped one-off fetches through fetch-proxy relays. Timing sparse and irregular (25 days apart for the two ANATEL hits), bare domains, no nonce grammar, no tunnel relays, no enumeration. **Verdict:** one-off agent page reads / triage-recon, not a scan campaign. LATAM context: 26 other LATAM-ccTLD hits in the same campaign (e.g. `incorporacion.mil.co` — Colombian military recruitment, `defesacoletiva.org.br`, `antamina.logiflex.pe`) are all single-hit bare domains — the campaign baseline is agents pulling arbitrary pages through CORS proxies, not regional targeting.

---

## 3. Vietnam — programmatic stats-API task family (extends into the Global South)

`pxweb.nso.gov.vn` (393 referrer hits) + `pxweb.gso.gov.vn` (66) surface as YOURLS referrers on UNM `goto.unm.edu/7t6-o` shortener stats (59 hits, 32 distinct referrer URLs).

Programmatic tells:
- Encoding-variant retry grammar on the same endpoint — literal space, `%20`, `+` variants of `National Accounts and State budget`
- A `TESTDEFAULT999` probe URL
- Both agency hostnames (NSO + GSO)

**Verdict:** fits the known swarm national-stats-API task family — confirms it extends into the Global South. Distinctive referrer URLs observed include `https://pxweb.nso.gov.vn/api/v1/en/National Accounts and State budget/`, `.../E03.14.px`, `...?x=1`.

---

## 4. India — agent link-laundering (wiki-board grammar, not a scan campaign)

11 `frozen:collusion-wiki` records: `https://proxy.cors.sh/https://www.indiascienceandtechnology.gov.in/res...` with Google-Translate params (`_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en`) — the same relay grammar as the SEC county.json CORS records, plus `jina_allorigins_dagd` indicators and `double_slash_path`. Agent link-laundering of an Indian science-tech gov URL; no scan campaign attached.

---

## 5. Egypt — one-off agent research artifact

Two urlquery reports (`28ed7589…`, `6c6e30da…`), 3 seconds apart, 2026-07-17: Egyptian Drug Authority news articles (`edaegypt.gov.eg/en/media-center/news/…africa-health-excon-2026…`) with `?utm_source=chatgpt.com`. URLs copied out of a ChatGPT answer and submitted. DeepSearchQA-adjacent (matched fingerprint `Africa` for qid `dsqa_283`/`dsqa_339`). Not scanning.

---

## Honest zeros

Zero mentions in local corpora for: **Africa** — gov.za, gov.ng, gov.ke, gov.gh, gov.et, gov.rw. **LatAm** — gob.mx, gob.ar, gov.co, gob.cl, gob.pe (+ gob.bo, gov.ec, gov.py, gob.uy, gob.gt, gob.hn, gov.cr, gob.pa, gob.do, gov.ve, gob.sv, gov.ni, gob.cu). **MENA/CA** — gov.ae, gov.sa, gov.kz, gov.uz, gov.ir, gov.qa (+ gov.jo/iq/kw/om/bh/ye/sy/lb/az/ge/am/tm/tj/kg/ps/af). **SE/S Asia** — gov.my, gov.ph, gov.th, gov.bd, gov.pk. Plus: zero Global South gov domains in the 589,972-event `openai-agent-traces` corpus and the amap-fleet corpus.

## Methodological cautions
- `gov.tr` "hits" are FALSE POSITIVES: `*-gov.translate.goog` (Google Translate proxies of US .gov sites from the SEC county.json watch) + a DeepSearchQA `gov-trade` tag. Always strip translate.goog before counting.
- One apparent `gov.ng` hit was `civilrightsdata.ed.gov/ngsw.json` — unescaped-dot regex trap.

## Pending
1. Live `uq_htmx.py` queries once egress recovers: `go.id`, `gov.br`, `gov.in`, `gov.za`, `gov.ng`, `gob.mx`, `gov.ae`, `gov.sa`, `gov.tr`, `gov.my`, `gov.ph`, `gov.th`, `gov.bd`, `gov.pk`, `gov.kz`, `gov.uz`, `gov.ir`, `gov.qa`, `gov.co`, `gob.ar`, `gob.cl`, `gob.pe` — find live siblings/bursts of the singleton probes.
2. Cross-check `cors_conversion_proxy` / `jina_allorigins_dagd` indicator definitions against exact relay chains in known agent corpora — are the Indonesia/Brazil probes the same harness family as oai-tag-sweep?
3. Pull full reports `1df03d5a`, `faa48376`, `a9c7e089`, `09195203`, `1e16f79e`, `dd4fa017`, `b11fd092`, `46e7c66d` for submitter-side metadata (UAs, tags, exit nodes).

---

## APPENDIX — All observed URLs

### Indonesia (agent-scanned targets)
- pa-gresik.go.id/index.php?option=com_media
- jdih.balikpapan.go.id/dokumen/610/detail?utm_source=chatgpt.com
- www.dinkes.semarangkota.go.id/
- dinkes.acehprov.go.id/detailpost/abcde-cegah-stunting
- www.kkp.go.id/djpdskp/kkp-permudah-produk-umkm-tembus-pasar-global-dengan-gmp-sertifikat65c30481d5d51/detail.html

### Indonesia (urlquery report URLs)
- https://urlquery.net/report/1df03d5a-ba13-474d-8036-26fe31526ee7
- https://urlquery.net/report/faa48376-8a90-4980-a965-357ad03914e7
- https://urlquery.net/report/a9c7e089-c55a-4a95-8d41-c57cd6cb346a
- https://urlquery.net/report/09195203-e3e2-4e42-92b1-735a684ff56f
- https://urlquery.net/report/1e16f79e-0006-48e2-b450-1d99f6a78165

### Brazil (agent-fetched targets)
- anatel.gov.br/
- www.anatel.gov.br
- esporte.gov.br/

### Brazil (urlquery report URLs)
- https://urlquery.net/report/dd4fa017-96a3-4d7a-9753-409a525b99ba
- https://urlquery.net/report/b11fd092-3a5b-4fbd-a552-7feae342f9c4
- https://urlquery.net/report/46e7c66d-c64f-4183-b675-1f10e0b2ca4d

### Vietnam (YOURLS referrer URLs)
- https://pxweb.nso.gov.vn/api/v1/en/National Accounts and State budget/
- https://pxweb.nso.gov.vn/api/v1/en/National Accounts and State budget/E03.14.px
- https://pxweb.nso.gov.vn/api/v1/en/National Accounts and State budget?x=1
- https://pxweb.nso.gov.vn/api/v1/en/National%20Accounts%20and%20State%20budget/
- https://pxweb.nso.gov.vn/api/v1/en/National+Accounts+and+State+budget/
- https://pxweb.gso.gov.vn/ (host-level, 66 referrer hits)

### India (link-laundering targets)
- https://proxy.cors.sh/https://www.indiascienceandtechnology.gov.in/res… (truncated in source records; Google-Translate params `_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en` appended)

### Egypt (research-artifact URLs)
- edaegypt.gov.eg/en/media-center/news/during-the-fifth-edition-of-africa-health-excon-2026-eda-supports-strategic-partnerships-to-localize-vaccine-manufacturing-and-strengthen-health-security-across-africa/?utm_source=chatgpt.com
- (second article, same domain/path family, report `6c6e30da…`)

### LATAM context (single-hit bare domains in cors-laundering-ops)
- incorporacion.mil.co (Colombian military recruitment)
- defesacoletiva.org.br
- antamina.logiflex.pe
- termasdesanluis.cl
- iglesiamontededios.org.do/.well-known/acme-challenge/…

### Infrastructure observed in this sweep
- https://goto.unm.edu/7t6-o+ (UNM YOURLS stats page — referrer source)
- https://collusion.wiki/explorer/download (collusion-wiki dataset reference)
- https://proxy.cors.sh/ (CORS proxy relay)
- allorigins.hexlet.app (CORS relay host)
