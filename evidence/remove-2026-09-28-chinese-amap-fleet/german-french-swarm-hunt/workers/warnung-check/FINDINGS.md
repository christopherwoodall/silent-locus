# WARNUNG-CHECK — Findings

Worker: WARNUNG-CHECK (EUROSWARM wave-3)
Date: 2026-10-05
Lead: german-archaeologist singleton — `warnung.bund.de` (German federal civil-protection warning portal, backend of the NINA warning app) touched by one urlquery report in an agent-suggestive context.
Grade: **HONEST NEGATIVE** (ordinary scan; no agent-shaped markers)

Method: passive/public OSINT only — urlquery htmx index queries (65s pacing between queries) + web search snippets. `warnung.bund.de` itself was NEVER fetched or probed (German federal infrastructure — log, don't touch). No auth bypass, no exploitation, no payloads. Scope: agents/swarms only — no human/operator identity work.

---

## OBSERVED

### Query 1 — keyword `warnung.bund.de` (limit 50)
Exactly **1 report** returned:

| Field | Value |
|---|---|
| report_id | `16d07ea9-5ec7-4f45-8c32-85072af9e481` |
| submitted URL | `warnung.bund.de/m/7GlcRO_ioqoT` (schema https) |
| fqdn | `warnung.bund.de` |
| domain / tld | `bund.de` / `de` |
| report date | `2026-09-10T09:03:00Z` (detail record: `2026-09-10T09:03:36Z`) |
| status | `done`, version 0 |
| tags | `[]` (empty) |
| submit.tags | `null` |
| submit.meta | `null` |

### Query 2 — `url.domain:warnung.bund.de` (limit 50)
**0 reports returned.** Note: the htmx endpoint appears not to honor the `url.domain:` operator the same way the web UI does (it returned 0 while the keyword form returned 1). The singleton claim rests on the keyword search, which keyword-matches submitted URLs — with limit 50 it returned exactly 1 report, so there are no additional reports containing the string `warnung.bund.de` in the submitted URL.

### Full report detail (`uq.py report 16d07ea9-5ec7-4f45-8c32-85072af9e481`)
- **Final URL** (no redirect): `https://warnung.bund.de/m/7GlcRO_ioqoT` — submit URL == final URL.
- **Page title:** `Aktuelle Warnmeldung` ("Current Warning Message")
- **Settings:**
  - `access`: `public`
  - `device_type`: `desktop`
  - `useragent`: `Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0`
  - `referer`: `""` (empty)
  - `cookies`: `null`
  - `exit_node`: `qguvgzjxzsgb3vs`
  - `expires_at`: `2027-10-15T09:03:36Z`
- **Resolved server IP:** `185.85.1.149`, port 0, ASN `20546`, AS `SOPRADO GmbH`, country `Germany` (DE). Page-load hosts also hit `185.85.0.244` on the same AS/host.
- **Third-party hosts loaded during scan** (all normal page dependencies):
  - `fonts.gstatic.com` (142.250.178.99, AS15169 GOOGLE) — 1 request
  - `maps.googleapis.com` (172.217.112.4, AS15169 GOOGLE) — 66 requests
  - `fonts.googleapis.com` (142.250.178.42, AS15169 GOOGLE) — 2 requests
  - `warnung.bund.de` (185.85.0.244, AS20546 SOPRADO GmbH) — 6 requests
  - `maps.gstatic.com` (142.250.178.35, AS15169 GOOGLE) — 3 requests
- **Embedded Google Maps script URL (as observed in page source):** `maps.googleapis.com/maps/api/js?key=AIzaSyBq_RZMBNb7DJ1PXvGFPcUqh1rbxh7pIAo&callback=initMap&language=de&region=DE` — this is the site's own public browser Maps API key, embedded by the portal itself; recorded here unredacted per evidence rule, noted as public-by-construction.
- **Detection/alerts:** `alert_count`: ids 0, urlquery 0, analyzer 0; `detection`: ids null, analyzer null, urlquery null. `files`: null. `artifacts`: all null. DOM size 94707 bytes, `text/html; charset=utf-8`.
- **DOM hashes (as observed):** md5 `5ee346e4d0271b5ecc1cfca021836a36`, sha1 `594c32e361815d9a9cb6d1c9a836a23ca816691a`, sha256 `2e69fb2c284230139a1c11e0ba62bc4259f7cc750ce136222dd815ce9cb14d80`.

### Sibling check — keyword `bund.de` (limit 30)
21 reports returned (keyword matching is substring-loose; many are not actual `bund.de` domains). Actual federal-domain reports, all temporally scattered:

| date | url | report_id |
|---|---|---|
| 2026-10-02T09:57:00Z | kulturerbe-eifel-mosel.de/ | 00398f0e-c1d0-41d8-8546-8eb1dc363bd3 |
| 2026-09-10T09:03:00Z | warnung.bund.de/m/7GlcRO_ioqoT | 16d07ea9-5ec7-4f45-8c32-85072af9e481 |
| 2026-08-09T23:12:00Z | unixhosts.org/ | ff606eee-9545-4663-957e-b422c8930c87 |
| 2026-07-19T00:14:00Z | polizei-bund.de/ | 19864f10-d050-49ba-8a1a-efaef9c6e2fc |
| 2026-07-05T22:15:00Z | ulornilentani.netlify.app/ | 664d4aad-1c30-4b66-aac8-166b74c8a356 |
| 2026-07-02T13:23:00Z | www.bfit-bund.de/DE/Ueberuns/Veranstaltungen/Einsatz-von-Overlaytools/veranstaltung_node.html | d93bf5d8-421d-4f95-93f8-1a55c2fa08b1 |
| 2026-06-16T10:31:00Z | bag-bund.de/ | 6ac99772-e3ac-4bc6-bdcf-60ec9f428d66 |
| 2026-06-10T09:55:00Z | www.ib-nord.de/ | 83b61169-b856-42af-ace3-0aee923fe16d |
| 2026-06-05T21:13:00Z | bmwsb.bund.de/ | 3b24d0c0-849c-479f-8da6-e19f2f8f25e9 |
| 2026-05-27T15:42:00Z | dserver.bundestag.de/btd/21/060/2106029.pdf | e5a35c83-b9f3-4e52-a395-6ddd2e00149b |
| 2026-05-26T20:17:00Z | bmwsb.bund.de/ | 1d49b595-fbd2-4c7c-8a7b-1176a66de0fa |
| 2026-05-23T04:47:00Z | bmv.de/ | 5cac2f26-a29e-4f0a-ba8c-6c397dede708 |
| 2026-05-18T14:27:00Z | sprachinstitut-tuebingen.de/ | faab6a2b-f037-4af2-94fd-9885b81b9bb9 |
| 2026-05-18T14:27:00Z | www.besucherzentrum.bnd.de/ | 791a7526-52f5-447e-9b54-b5d63c9ac689 |
| 2026-05-14T22:45:00Z | rheinmarkt.com/ | c7653654-ff14-45dd-9a1f-2dda24588b73 |
| 2026-05-01T19:40:00Z | rheinmarkt.com/ | 94b7fa37-6aa5-4a02-bebb-c774304d2faf |
| 2026-04-13T08:23:00Z | eichekapital.com/ | a7ba0b07-bb26-4072-bdc3-1cb8f2964f80 |
| 2026-03-27T23:54:00Z | bav.volkswohl-bund.de/arbeitnehmer/ | ae028c91-7c98-49ba-8ea1-5821ab22d60f |
| 2026-03-25T23:52:00Z | web.jugendclub18.de/ | f40a0f2a-07a6-4a880e2a1e66 |
| 2026-03-01T23:54:00Z | mbhessen.de | cbb282d0-00c7-4845-b7b0-0a880e2a1e66 |
| 2026-02-19T13:14:00Z | alpenpresse.com/ | 7bc9571d-3f56-4d30-8b21-c64c992f515c |

No temporal clustering around the 2026-09-10 warnung hit; no shared burst geometry across sibling federal domains. `warnung.bund.de` appears exactly once in the index.

### Web search — public writeups
Three searches run:
1. `warnung.bund.de AI agent activity NINA app backend` (en)
2. `"warnung.bund.de" Schwachstelle Agenten Sicherheit` (de)
3. `NINA warning app AI agent prompt injection warnung.bund.de security` (en)

**Result: zero public writeups connect agent activity to warnung.bund.de or the NINA app backend.** The only agent-related German hits were about the already-known German-wiki evaluation incident (interestingengineering.com "OpenAI agents hijacked German site"; mlq.ai "OpenAI confirms agents used a public German wiki to coordinate during evaluations") — a different surface, already in the hunt corpus. Remaining hits were generic prompt-injection/agent-security coverage (TechRadar/AppOmni, DarkReading/Manus, Kaspersky/Gemini, NCSC assessment) with no warnung.bund.de connection, plus NINA app background (BBK pages, Play Store listing, T-Systems infra flyer).

---

## INFERENCE (graded against agent-shaped criteria)

| Criterion | Finding |
|---|---|
| Burst timing | n=1. Single report, 2026-09-10T09:03:36Z, no repeats, no hourly histogram possible. **Absent.** |
| Program hosts | Resolved infra is the portal's own hoster (SOPRADO GmbH, AS20546, DE) + Google CDN (maps/fonts). Nothing agent-operated. **Absent.** |
| Agent grammar | tags `[]`, submit.tags `null`, submit.meta `null`. No oai/zz tags, no epoch nonces, no agent markers. **Absent.** |
| Non-browser UA | UA is stock `Firefox/134.0` on Windows desktop — the urlquery public scanner's default UA family (consistent with the established 9,979-report UA sweep: stock browsers only). **Absent.** |

- The submitted URL `warnung.bund.de/m/7GlcRO_ioqoT` is the NINA app's mobile share-link format (`/m/<token>`), title "Aktuelle Warnmeldung". The most economical reading: someone pasted a NINA warning share link into urlquery to check it — the canonical human use case for the service. No redirect, no exploit artifacts, zero detections.
- Sibling federal domains show ordinary, temporally scattered scans with no clustering or shared pattern — no swarm-shaped session across `.bund.de`.

## Caveats
- This is a passive-index negative: it establishes that no agent-shaped scan of warnung.bund.de was *submitted to urlquery*, not that no agent ever touched the portal.
- The `url.domain:` operator returned 0 on the htmx endpoint (likely a syntax quirk); the singleton claim rests on the keyword search (limit 50, exactly 1 hit).
- The portal itself was never fetched, per the hard rule.

---

## FINAL GRADE: HONEST NEGATIVE

The german-archaeologist singleton lead is exhausted: one ordinary urlquery scan of a NINA warning share link (2026-09-10, stock Firefox UA, no tags/meta, zero detections), no sibling-domain clustering, no public writeup tying agent activity to warnung.bund.de or the NINA backend. No wave-4 follow-up warranted on this lead.
