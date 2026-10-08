# Gem campaign — extracted URL hunt — 2026-09-27

Hunting the URLs extracted from the go-import tags (notes/gem-metadata-deepdive-2026-09-27.md)
and runner gems (notes/gem-contents-deepdive-2026-09-27.md) across three grounds:
urlquery (public API), Diffend (gem index), and live liveness checks.
All reads read-only; frozen hunt searched, never written.

## 1. Per-URL findings

### democracy.wandsworth.gov.uk — Wandsworth council calendar (mgCalendarMonthView.aspx / mgCalendarWeekView.aspx)
- **In gems:** 46 tags via r.jina.ai + 31 direct (`wands*`, `wandsworth*` families); `wprox-c217-1fossil` → documents/s124875/Cabinet report FHF.pdf
- **urlquery:** 0 reports (`url.domain:democracy.wandsworth.gov.uk`)
- **Frozen hunt:** 0 / 51,643 (bridge-hunt verified negative)
- **Liveness:** **200** — "Monthly meetings calendar - January 2026" (cache-busted GET 2026-09-27). Still live.

### moderngov.lambeth.gov.uk — Lambeth (mgCalendarMonthView.aspx, mgWebService.asmx)
- **In gems:** 48 via jina + 40 direct (`lamb*` families); runner uploaders fetch `mgCalendarMonthView.aspx?GL=1`
- **urlquery:** 0 reports
- **Frozen hunt:** 0 / 51,643
- **Liveness:** calendar **200** ("Monthly meetings calendar - September 2026", nginx);
  **mgWebService.asmx 200** — "mgWebService Web Service". Both live.

### moderngov.southwark.gov.uk — Southwark (mgWebService.asmx/GetMeetings)
- **In gems:** 21 via jina + 4 direct; SSRF ladder endpoint (`southwarkssrfhack2→5`)
- **urlquery:** 0 reports
- **Frozen hunt:** 0 / 51,643
- **Liveness:** **HTTP 500** on `mgWebService.asmx/GetMeetings` (endpoint exists, rejects param-less GET — expected for SOAP)

### 20.49.140.101/mgWebService.asmx/GetMeetings — raw Azure IP (southwarkssrfhack3)
- **urlquery:** 2 hits — `my.southwark.gov.uk/` (2025-10-07) and `education.southwark.gov.uk/` (2025-10-03).
  Keyword-matched via IP resolution: confirms 20.49.140.101 is Southwark's Azure hosting.
  The SSRF ladder's "raw IP" step resolves to the *same* infra as the domain — the actor
  mapped domain → IP → cloud hostname deliberately.
- **Liveness:** **404** — the raw-IP path no longer serves the SOAP endpoint. Dead.

### lbs-tm-prod.trafficmanager.net/mgWebService.asmx/GetMeetings (southwarkssrfhack4)
- **urlquery:** `trafficmanager.net` → 3,830 global hits = Azure-wide noise; no campaign-specific hits
- **Liveness:** **404** — dead.

### www.digitizationguidelines.gov — FADGI PDF (rehearsal target)
- **In gems:** 15 via jina + 12 direct (`zzfadgivar*`, `zzpdfvar*` rehearsal families)
- **urlquery:** 0 reports (`url.domain:digitizationguidelines.gov`)
- **Liveness:** **200** — "Federal Agencies Digital Guidelines Initiative" (Cloudflare). Live.

### www.marinajacks.com — random restaurant catering PDF (2 tags via jina)
- **urlquery:** 0 reports. Liveness not checked (benign 3rd party, out of scope).

### s.jina.ai — Jina *search* (not reader): `s.jina.ai/lambeth`, `s.jina.ai/wandsworth January 2026`
- **In gems:** 9 tags — a distinct search-grounded path, spread across all 6 VCS values
- **urlquery:** `s.jina.ai` → 20 global hits, all noise (jina.ai/reader, zeromq.org, random blogs)
- **Read:** the actor used Jina search to ground its target URLs ("wandsworth January 2026")
  before laundering fetches through the reader proxy.

### r.jina.ai-wrapped forms (151 tags)
- **urlquery:** 1,072 global hits (frozen hunt corpus documents 618 — consistent, same phenomenon)
- **Frozen hunt:** pattern-level bridge confirmed (bridge-hunt); zero literal carried-URL overlap
  (hunt carries proxy-chains/SEC URLs; gems carry council calendars)

### example.com placeholder variants (9 tags — null-target control group)
- **In gems:** `v*`, `chatoaitest*`, `lambfetch001`, `pwnp999` families
- **urlquery:** not separately queried (example.com is universal noise by construction)

## 2. Diffend: follow-on gems and out-of-set families

**The uploaders' follow-on gems were NEVER published:**
- `lambresultabc` → 0 gems on Diffend (the gem `londonyardtestabc-0.0.2`'s uploader tried to push `lambresultabc-0.0.2`)
- `lambresult`, `wandresult` → 0
- `southfetchprobe42`, `southlondonfetchroot` → exist (the uploaders themselves, in our 608-pin set)
- **Verdict: every observed push attempt failed** — consistent with the yank + the 403 their infra hit.

**June-18-wave names ARE on Diffend, all dated May 12 — missing from our 608-pin set, PULL NEEDED:**
- `slnleaker4`, `slnleaker5`, `slnleakerext` (May 12, 2026 03:21)
- `yardbreakerxqh1778552850` (May 12, 2026 02:34; epoch 1778552850 → 02:27:30Z, indexed 7 min later)
- `exfiltestwand` (May 12, 2026 01:58)
- The bridge-hunt "June-18 wave" attribution for these names was wrong — they are May-12 burst gems
  the enumeration missed. Recommend a second Diffend pull for these 5+ gems.

**Actor timeline extends to March 2026:**
- `rgscan_s4_20260317235101` — Diffend "Last diff" **March 17, 2026 23:54/23:58**;
  embedded `20260317235101` = 2026-03-17 23:51:01, indexed ~3–7 min later (same mint→index pattern as May)
- `rgscan_s4r_20260318000241` — March 18, 2026 (~00:02:41)
- **The actor ran upload/yank integrity tests two months before the May burst.** Earliest known activity.

**Lane 5's SEC proxy gems NOT on Diffend:**
- `ioc-lane5-sec-proxy-gems` describes "SEC county.json proxy gems (a----00proxy43876 et al)"
- Diffend searches for `00proxy`, `a----00proxy43876`, `sec-proxy`, `secproxy` → all 0 ("No packages found")
- Those gems were never indexed by Diffend (yanked before snapshot, or never published) —
  **lane 5's gem-SEC claim stays public-record-only and unverified.**

## 3. IOC table (new / refined)

| IOC | Type | Verdict |
|---|---|---|
| democracy.wandsworth.gov.uk | target domain | live (200); 0 urlquery reports |
| moderngov.lambeth.gov.uk | target domain | live (200); mgWebService.asmx live |
| moderngov.southwark.gov.uk | target domain | SOAP endpoint 500s on bare GET |
| 20.49.140.101 | SSRF ladder IP | dead (404); confirmed Southwark Azure infra via urlquery IP matches |
| lbs-tm-prod.trafficmanager.net | SSRF ladder host | dead (404) |
| www.digitizationguidelines.gov | rehearsal target | live (200) |
| s.jina.ai | search-grounding | actor used Jina search to ground targets |
| rgscan_s4_* (Mar 2026) | actor infra-testing | NEW: pushes actor timeline to March 17–18, 2026 |
| slnleaker4/5/ext, yardbreakerxqh1778552850, exfiltestwand | burst gems | NEW: on Diffend, May 12, missing from 608-pin set — pull next |
| lambresultabc (unpublished) | failed follow-on | uploader pushes failed; nothing got through |

## 4. Gossip / hints

1. **The campaign is invisible in urlquery.** Zero reports for the council domains, zero for every
   gem name tested (including the uploaders), zero for mgWebService. The "scans" were Go tooling
   fetching go-import URLs server-side — never browser submissions — so urlquery never saw them.
   Absence here is structural, not a gap.
2. **The SSRF ladder's IP step was not naive:** 20.49.140.101 is genuinely Southwark's Azure
   front-end (urlquery's IP-resolved reports prove it). The actor did its DNS homework.
3. **March 2026 rgscan gems use a different timestamp grammar** (`YYYYMMDDHHMMSS` in the name
   vs May's epoch nonces) — the actor's naming convention evolved between March and May.
4. **The follow-on gems never landed**, but the uploaders' code was real and the keys were real —
   the operation was *capable* of self-replication and only failed at the push step
   (yank + network filtering).
