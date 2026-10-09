# GERMAN AGENT HUNTER II — FINDINGS (undocumented finds only)

**Date:** 2026-10-05 (run ~06:30–07:30 UTC)
**Mission:** find GERMAN AGENTS THAT HAVE NOT BEEN DOCUMENTED. The DseWiki incident is KNOWN — not re-reported here.
**Egress:** UP (urlquery.net 200, urlscan.io search API 200; urlscan result-details API 403 anonymous — submitter IPs not visible).
**Verdict: no undocumented German agent found.** One genuinely new programmatic pipeline discovered and honestly graded (not agent-shaped). All lanes executed; nothing pushed.

---

## Lane 1 — warnung.bund.de singleton follow-up (CLOSED: uncorroborated)

Report `16d07ea9-5ec7-4f45-8c32-85072af9e481` (`warnung.bund.de/m/7GlcRO_ioqoT`, 2026-09-10 09:03):

| Check | Result |
|---|---|
| `/related/ip` | **1 report only** — 185.85.1.149 (SOPRADO GmbH, the warnung.bund.de host). No siblings on the IP. |
| `/related/domain` | 10 rows, all routine: BSI PDFs, geodata zips, ministry homepages. **No probe-shaped siblings.** |
| `/related/similar` | Empty. |
| `/filter/http` | 78 transactions, stock Firefox UA, no agent markers in URLs (confirms prior hunter's read). |

**Grading:** the singleton remains a singleton. No corroboration from any keyless endpoint. Watch item, NOT a find. Lane closed.

---

## Lane 2 — Iranian-hunter playbook: urlscan API-method sweeps of German gov domains

Eight domains swept (`bmi.bund.de`, `bsi.bund.de`, `bka.de`, `bundesregierung.de`, `bundestag.de`, `destatis.de`, `bamf.de`, `zoll.de`), all via anonymous urlscan search API, `method` field analyzed per result.

### FINDING (GENUINELY NEW): newsletter-link detonation pipeline — table.media + bundestag.de

**Not agent-shaped. Documented here as a pattern fingerprint so it isn't mistaken for one.**

- `domain:table.media` → **1,644 total results**, 100 sampled (Sep 30–Oct 4), **100% api method**.
- **Burst 1:** 2026-09-30 19:53 — **65 scans in one minute** + 13 more at 19:54. Targets: 46× `table.media/ueber-uns/<author>` profile pages + spiegel.de, zeit.de, faz.net, taz.de, handelsblatt, sueddeutsche.de, nzz.ch, rbb-online.de, consilium.europa.eu, bundeswirtschaftsministerium.de — every link class in a table.media newsletter edition (author bylines, cited press, EU/gov links).
- **Burst 2:** 2026-10-01 06:53 — 19× `briefing.table.media/` homepage in one minute (redirect-chain resolution of briefing links).
- **bundestag.de pairing:** 65 results; same-minute bursts of `presse/hib/kurzmeldungen-<id>` press releases (Sep 13/21/22/24/28/29, 4–11 scans per burst) **paired with `briefing.table.media/r/<id>ms<digits>.html` newsletter tracking links** in the same minutes. kurzmeldungen IDs increment across bursts (1211456 → 1218038) = sequential press releases as published.
- **Enodia tokens:** many submitted bundestag URLs carry `?enodia=<JWT>` — Enodia is bundestag.de's bot-challenge; the JWT embeds `exp`, `aud:auth`, `Host`, and `SourceIP` (the challenge-solver's IP). Submitter included post-challenge URLs.
- **urlquery cross-check:** `table.media` on urlquery shows the same newsletter-tracking grammar — `briefing.table.media/r/Ot2Hzgg1261804ms17043.html` and an `imgred` image-proxy URL with `timestamp=` + `signature=` (newsletter open-tracking). Confirms these are email-newsletter links.

**Reading:** a secure-email-gateway (or publisher QA) **link-detonation pipeline** — when each table.media newsletter edition sends, every link in it is submitted to urlscan via API within minutes. The bundestag.de press releases are in the newsletter; they get detonated too. Programmatic, bursty, api-method — but no task grammar, no nonces, no enumeration beyond the newsletter's own link set.

**Classification: GENUINELY NEW** (zero `table.media` / zero `kurzmeldungen` in all three of our corpora) — but **NOT agent-shaped**. Filed as a pipeline fingerprint: api-method + same-minute burst + newsletter-redirect URL grammar (`/r/<id>ms<digits>.html`, `imgred?...&signature=`).

### Watch items (German gov, programmatic but sub-agent-bar)

| Domain | Pattern | Grading |
|---|---|---|
| destatis.de | 10× api homepage re-scans, Sep 19–Oct 3, ~2–3 day cadence + 1 Verwaltungsregister/Basisregister page | Monitoring-shaped (uptime/content-watch), not agent-shaped |
| zoll.de | 3× api scans of the EORI-number application page within 2 min (Sep 23 15:21–15:23), incl. lowercase-URL variant | Machine re-scan of a single customs-ID page; target is interesting (trade-compliance), cadence is thin |
| bamf.de | 2× api homepage scans, 10 days apart (Sep 17/27) | Monitoring |
| bundesregierung.de | `breg-de` repeats (monitoring); `sportundehrenamt.de.schulung.bundesregierung.de` re-scan pair 35 min apart (Sep 17); `akkreditierung.bundesregierung.de/.enodia/challenge` (bot-challenge page scanned); `m.cvd.bundesregierung.de` single | Mixed routine + monitoring |
| bka.de | 1× api homepage scan (Sep 27) | Nothing |
| bmi.bund.de | 0 results | Clean |
| bsi.bund.de | 5 results: newsletter form, DNSSEC pdf, doku-pruefung.de, rechnungsvergabe.de, zeroservices.eu — diffuse | Noise |

**No fixed-target-list re-scan campaign of the Iranian type found on any German gov domain.**

---

## Lane 3 — German probe-grammar hunt (urlquery htmx)

| Query | Result |
|---|---|
| `aufgabe` | 7 hits: Austrian/German commercial sites (combi.de, pfalzlexikon.de) — noise |
| `pruefung` | 7 hits: tax-exam courses, mailing-tracked links — noise |
| `bundestag` | 8 hits: routine scans (committees page, dserver PDFs) — no probe grammar |
| `enodia` | 1 hit: enodia.gr (Greek domain, false positive) |

**No agent-shaped German probe grammar on urlquery.** (Prior hunter already zeroed `httpbun aufgabe/agent`, `claude httpbun`, `uqscan berlin`, `sub_poi_navi berlin`.)

---

## Lane 4 — Hetzner with agent-marker co-occurrence

| Check | Result |
|---|---|
| `hetzner` in Amap fleet (2,141) | **0** |
| `hetzner` in openai-agent-traces (589,972) | **0** |
| `hetzner` in oai-tag-sweep | **0** |
| hetzner + (epoch_nonce\|uqscan\|zz=\|jina\|webhook) co-occurrence | **0** |
| urlquery htmx `hetzner` (15 hits) | All keyword noise — sites *hosted on* Hetzner (corrector.de, scinexx.de, shop.jadatoys.de…), not hetzner.com |

**No agent-shaped Hetzner staging visible on any surface checked.** The 12 routine hits from the prior pass stand; marker-gated re-pass adds nothing.

---

## Bottom line

**No undocumented German agent found.** The detection net that caught the Iranian re-scan campaign and the Amap fleet catches nothing German-shaped beyond the known DseWiki incident:
- warnung.bund.de singleton: uncorroborated, lane closed
- German gov domains: monitoring cadences + one newsletter-detonation pipeline (new pattern, not an agent)
- German probe grammar: noise only
- Hetzner: zero marker co-occurrence across ~600k corpus events and live surfaces

**What would change this:** a German-language eval-task family (the archaeologist lane is digging the corpora for this), or agent self-labels in German on a non-DseWiki surface.

---

## APPENDIX — All observed URLs

### Lane 1 (warnung.bund.de)
- https://urlquery.net/report/16d07ea9-5ec7-4f45-8c32-85072af9e481
- https://urlquery.net/api/htmx/report/16d07ea9-5ec7-4f45-8c32-85072af9e481/filter/http
- https://urlquery.net/api/htmx/report/16d07ea9-5ec7-4f45-8c32-85072af9e481/related/ip
- https://urlquery.net/api/htmx/report/16d07ea9-5ec7-4f45-8c32-85072af9e481/related/domain
- https://urlquery.net/api/htmx/report/16d07ea9-5ec7-4f45-8c32-85072af9e481/related/similar
- warnung.bund.de/m/7GlcRO_ioqoT

### Lane 2 (urlscan German gov sweeps)
- https://urlscan.io/api/v1/search/?q=domain:bmi.bund.de&size=100
- https://urlscan.io/api/v1/search/?q=domain:bsi.bund.de&size=100
- https://urlscan.io/api/v1/search/?q=domain:bka.de&size=100
- https://urlscan.io/api/v1/search/?q=domain:bundesregierung.de&size=100
- https://urlscan.io/api/v1/search/?q=domain:bundestag.de&size=100
- https://urlscan.io/api/v1/search/?q=domain:destatis.de&size=100
- https://urlscan.io/api/v1/search/?q=domain:bamf.de&size=100
- https://urlscan.io/api/v1/search/?q=domain:zoll.de&size=100
- https://urlscan.io/api/v1/search/?q=domain:table.media&size=100
- https://www.bundestag.de/presse/hib/kurzmeldungen-1217984 (representative; see raw JSON for full burst lists)
- https://www.bundestag.de/presse/hib/kurzmeldungen-1218038
- https://www.bundestag.de/presse/hib/kurzmeldungen-1211456
- https://briefing.table.media/r/LUByciw1752812ms26598.html
- https://briefing.table.media/r/LUByciw1752768ms26598.html
- https://briefing.table.media/r/zI1HCVE1717854ms25747.html
- https://briefing.table.media/r/PnWhJNS1691684ms25139.html
- https://briefing.table.media/r/Ot2Hzgg1261804ms17043.html (urlquery d1ae71a0)
- https://briefing.table.media/r/bMUXZAv1261796ms17043.html (urlquery b0978fa9)
- https://dserver.bundestag.de/btd/21/080/2108008.pdf
- https://epetitionen.bundestag.de/petitionen/_2026/_06/_01/Petition_201787.$$$.a.u.html
- https://www.lobbyregister.bundestag.de/startseite
- https://www.destatis.de/DE/Home/_inhalt.html
- https://www.destatis.de/Verwaltungsregister/DE/Basisregister/_inhalt.html
- https://www.zoll.de/DE/Fachthemen/Zoelle/EORI-Nummer/Beantragung-einer-EORI-Nummer/beantragung-einer-eori-nummer.html
- https://www.bamf.de/DE/Startseite/startseite_node.html
- https://www.bka.de/DE/Home/home_node.html
- https://www.bundesregierung.de/breg-de
- https://www.sportundehrenamt.de.schulung.bundesregierung.de/
- https://akkreditierung.bundesregierung.de/.enodia/challenge
- https://www.m.cvd.bundesregierung.de/
- https://www.bsi.bund.de/SiteGlobals/Forms/Newsletter/Newsletter_Bestellen_Formular.html
- https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Cyber-Sicherheit/Themen/Umsetzung_von_DNSSEC.pdf

### Lane 3 (htmx German probe grammar — all noise, recorded for the negative)
- ifam-aufsichtsrat.at, gokraka.com/, rieker-berlin.com, www.combi.de/, digitaler-gwb.de/, pfalzlexikon.de/
- notebookcheck.it, feld12.de/, www.steuerkurse.de/webinar/5504_intensiv-klausurenkurs-ertragsteuern-tag-2-der-stb-pruefung-tag, protecto.li/, uid-check.at
- afd-monschau.de, www.bundestag.de/en/committees/a24, dserver.bundestag.de/btd/21/060/2106029.pdf

### Raw evidence
- `raw/warnung_filter_http.html`, `raw/warnung_related_ip.html`, `raw/warnung_related_domain.html`, `raw/warnung_related_similar.html`
- `raw/urlscan_bmi_bund_de.json`, `raw/urlscan_bsi_bund_de.json`, `raw/urlscan_bka_de.json`, `raw/urlscan_bundesregierung_de.json`, `raw/urlscan_bundestag_de.json`, `raw/urlscan_destatis_de.json`, `raw/urlscan_bamf_de.json`, `raw/urlscan_zoll_de.json`, `raw/urlscan_tablemedia.json`, `raw/enodia_scan.json`
