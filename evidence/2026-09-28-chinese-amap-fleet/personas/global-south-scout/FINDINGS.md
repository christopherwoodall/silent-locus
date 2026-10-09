# Global South Scout — FINDINGS

Persona: hunt AGENT activity outside China and the US. Agents, not operators — no human attribution, ever.
Agent shape = timing + action + grammar, not language.

## Method
Four regional scouts (LatAm, SE/S Asia, Africa, Middle East/Central Asia) + coordinator direct hunting.
**Egress outage** (~2026-10-05 04:37–04:55 UTC): urlquery.net and google.com unreachable, htmx proxy-tunnel tracebacks. All live `uq_htmx.py` queries failed; every scout pivoted to streaming grep over local corpora (73–80 `data/*/events.jsonl` + 12 `collections/*/data/*.jsonl`, ~935 MB). **Live urlquery re-checks are PENDING egress recovery** — the verdicts below rest on local corpora, which skew toward known incidents and cannot establish zero activity on urlquery.net.

## Confirmed finds (all previously unreported)

### 1. Indonesia — programmatic agent scanning of local gov sites (strongest)
Five frozen urlquery incident records, `data/2026-10-01-oai-tag-sweep/events.jsonl`, all tagged `urlquery-hunt` + `agent-activity`, campaign `cors-laundering-ops`, indicator `cors_conversion_proxy`, 2026-07-08 → 2026-08-31:

| date (UTC) | target |
|---|---|
| 2026-07-08 05:38 | pa-gresik.go.id/index.php?option=com_media (Gresik religious court, Joomla media manager) |
| 2026-07-15 04:44 | jdih.balikpapan.go.id/dokumen/610/detail?utm_source=chatgpt.com (Balikpapan legal docs) |
| 2026-07-15 07:41 | www.dinkes.semarangkota.go.id/ (Semarang city health office) |
| 2026-07-19 07:42 | dinkes.acehprov.go.id/detailpost/abcde-cegah-stunting (Aceh province health office) |
| 2026-08-31 02:43 | www.kkp.go.id/.../sertifikat65c30481d5d51/detail.html (Marine Affairs & Fisheries) |

Report IDs: `1df03d5a`, `faa48376`, `a9c7e089`, `09195203`, `1e16f79e`.
Agent-shaped: CORS-laundering relay on every hit, `utm_source=chatgpt.com` self-identification, a hex nonce (`65c30481d5d51`) in a path, municipality-by-municipality enumeration (two district health offices ~3h apart on Jul 15). Strongest non-China/non-US agent trace found in this sweep.

### 2. Brazil — agent fetches of telecom regulator + sports ministry
Three records, same corpus, indicator `jina_allorigins_dagd` (jina+allorigins+da.gd CORS-laundering), campaign `cors-laundering-ops`:

| date (UTC) | target | report |
|---|---|---|
| 2026-07-19 06:04 | anatel.gov.br/ | dd4fa017 |
| 2026-08-13 13:48 | www.anatel.gov.br | b11fd092 |
| 2026-08-14 23:14 | esporte.gov.br/ | 46e7c66d |

Agent-shaped one-off fetches through fetch-proxy relays — no nonce grammar, no enumeration, no burst. Triage/recon, not a scan campaign.

### 3. Vietnam — programmatic stats-API task family
`pxweb.nso.gov.vn` (393) + `pxweb.gso.gov.vn` (66) surface as YOURLS referrers on UNM `goto.unm.edu/7t6-o` shortener stats (59 hits, 32 distinct referrer URLs). Programmatic tells: encoding-variant retry grammar on the same endpoint (literal space / `%20` / `+`), a `TESTDEFAULT999` probe URL, both agency hostnames. Fits the known swarm national-stats-API task family — confirms it extends into the Global South.

### 4. India — agent link-laundering (wiki-board grammar, not urlquery campaign)
11 `frozen:collusion-wiki` records: `https://proxy.cors.sh/https://www.indiascienceandtechnology.gov.in/res...` with Google-Translate params (`_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en`) — the same relay grammar as the SEC county.json CORS records. Agent link-laundering, no scan campaign.

### 5. Egypt — one-off agent research artifact
Two urlquery reports (`28ed7589…`, `6c6e30da…`) 3 seconds apart, 2026-07-17: Egyptian Drug Authority news articles with `?utm_source=chatgpt.com`. URLs copied out of a ChatGPT answer and submitted. DeepSearchQA-adjacent. Not scanning.

## Honest zeros (local corpora)
Africa: gov.za, gov.ng, gov.ke, gov.gh, gov.et, gov.rw. LatAm: gob.mx, gob.ar, gov.co, gob.cl, gob.pe (+ gob.bo, gov.ec, gov.py, gob.uy, gob.gt, gob.hn, gov.cr, gob.pa, gob.do, gov.ve, gob.sv, gov.ni, gob.cu). MENA/CA: gov.ae, gov.sa, gov.kz, gov.uz, gov.ir, gov.qa (+ gov.jo/iq/kw/om/bh/ye/sy/lb/az/ge/am/tm/tj/kg/ps/af). SE/S Asia: gov.my, gov.ph, gov.th, gov.bd, gov.pk. Plus: zero Global South gov domains in `data/2026-10-03-openai-agent-traces/events.jsonl` (589,972 events) and the amap-fleet corpus.

## Methodological cautions
- `gov.tr` hits are FALSE POSITIVES: `*-gov.translate.goog` (Google Translate proxies of US .gov sites from the SEC county.json watch) + a DeepSearchQA `gov-trade` tag. Always strip translate.goog before counting.
- One apparent `gov.ng` hit was `civilrightsdata.ed.gov/ngsw.json` — unescaped-dot regex trap.

## Pending (needs egress recovery)
1. Live `uq_htmx.py` queries: `go.id`, `gov.br`, `gov.in`, `gov.za`, `gov.ng`, `gob.mx`, `gov.ae`, `gov.sa`, `gov.tr`, `gov.my`, `gov.ph`, `gov.th`, `gov.bd`, `gov.pk`, `gov.kz`, `gov.uz`, `gov.ir`, `gov.qa`, `gov.co`, `gob.ar`, `gob.cl`, `gob.pe` — to find live siblings/bursts of the singleton probes.
2. Cross-check `cors_conversion_proxy` / `jina_allorigins_dagd` indicator definitions against exact relay chains in known agent corpora — are the Indonesia/Brazil probes the same harness family as oai-tag-sweep?
3. Pull full urlquery reports `1df03d5a`, `faa48376`, `a9c7e089`, `09195203`, `1e16f79e`, `dd4fa017`, `b11fd092`, `46e7c66d` for submitter-side metadata (UAs, tags, exit nodes).
