# FINDINGS — IRANIAN AGENT HUNTER

**Date:** 2026-10-05 (UTC)
**Persona:** Iranian Agent Hunter — Persian-language / Iranian-surface hunt
**Status:** Lead found (one), honest negatives elsewhere

---

## 1. HEADLINE: Programmatic re-scan campaign against Iranian government domains (GENUINELY NEW)

**What:** 14 urlscan.io submissions, all via the `api` method (programmatic, not web-UI), targeting a FIXED list of Iranian government domains in two waves:

| Wave | Window | Targets scanned |
|---|---|---|
| Wave 1 | 2026-09-07 → 2026-09-12 | my.gov.ir, mfa.ir, mcls.gov.ir, behdasht.gov.ir, ihio.gov.ir |
| Wave 2 | 2026-09-27 → 2026-10-05 | tax.gov.ir, darubank.com (×2), mfa.ir, ihio.gov.ir, ict.gov.ir/en/more/links/affiliated, behdasht.gov.ir, mcls.gov.ir |

**Re-scan pairs (same domain, both waves):**
- `mcls.gov.ir` — Sep 12 02:41 → Oct 5 00:21 (Ministry of Cooperatives, Labour and Social Welfare)
- `behdasht.gov.ir` — Sep 11 07:25 → Oct 4 05:03 (Health Ministry)
- `ihio.gov.ir` — Sep 11 04:30 → Oct 4 02:12 (Iran Health Insurance Organization)
- `mfa.ir` — Sep 8 06:44 → Oct 1 04:26 (Foreign Ministry)
- `my.gov.ir` — Sep 7 10:15 → Sep 21 01:17 (citizen portal)

**Clustering within waves (machine cadence):** Sep 11: three scans 04:30–07:25. Oct 4: four scans 02:12–05:03. All in the 00:00–07:30 UTC band — off-hours, script-shaped.

**Target list character:** ministries + citizen services + health + tax + one pharma distributor (`darubank.com`, scanned twice — an odd inclusion that suggests the list is "Iranian critical infrastructure," not strictly gov).

**Traffic inspection:** Pulled the public result page for the `ict.gov.ir/en/more/links/affiliated` scan (Oct 4) — plain page load of a Telerik ASP.NET site, static resources, no probe parameters. The submission *target choice* is the signal, not the traffic. Notably: an "affiliated links" page — link-graph enumeration, same task-family shape as the Amap fleet's POI/affiliated-entity enumeration.

**Verification:**
- Zero hits for all 8 domains in all three of our sets (`2026-09-28-chinese-amap-fleet/events.jsonl`, `2026-10-03-openai-agent-traces/events.jsonl`, `2026-10-01-oai-tag-sweep/events.jsonl`). → **GENUINELY NEW**, not ours, not known.
- Cross-country control: api-method scanning of gov domains is common globally (gov.tr 659, gov.sa 134, gov.eg 62 results) — so "api method" alone is not the tell. The tell here is the **fixed target list + re-scan cadence + Iran-only scope**.

**Attribution (open, grade honestly):** agent-SHAPED but not agent-PROVEN. Consistent with (a) an agent running a reconnaissance/monitoring task on a schedule, or (b) a security researcher's cron monitoring Iranian gov sites. The two-wave re-scan with identical target list is the strongest machine-schedule indicator. Cannot distinguish (a) from (b) from public urlscan data — the submitter identity is not public.

**Watch item:** if a third wave lands ~Nov 1–5 with the same target list, the cadence becomes monthly and the monitoring hypothesis hardens. Recommend re-checking `domain:gov.ir` on urlscan in early November.

**Raw evidence:** `raw/urlscan_domain-gov.ir_2026-10-05.json` (full 14-result search response)

---

## 2. urlquery: two Iranian MFA reports inspected — researcher-shaped, NOT agent-shaped

- `mikhak.mfa.gov.ir/form/landing.xhtml` — report `b904e35f-52b2-4a71-b86a-40e431dfe3f1`, 2026-05-10. MFA visa/entry portal landing page. Full HTTP transaction dump pulled via keyless htmx endpoint (`/api/htmx/report/{id}/filter/http`): 47 requests, all static assets (SVG icons, JS bundle), zero probe parameters, stock urlquery Firefox UA.
- `kualalumpur.mfa.gov.ir/` — report `f1ed5bc6-5b6c-43be-a738-fa29736cbad0`, 2026-03-29. Iranian embassy in Kuala Lumpur homepage. 63 requests, same plain-load shape.

Verdict: ordinary page scans, no programmatic markers. Classified researcher/manual, eliminated.
Raw: `raw/mikhak.html`, `raw/kualalumpur.html`.

Older hits (`mehriz.gov.ir` Persian-path report from 2024-06, `patogh-tabrizi-ha.rzb.ir` from 2023-11) are stale and predate the hunt window — noted, not chased.

---

## 3. Persian-language keyword sweep — language matches, not behavior matches

urlquery htmx keyword searches for `farsi`, `persian`, `tehran` return language-detected content, not agent-shaped behavior:
- Persian e-commerce / download sites (`gorjico.com`, `sarzamindownload.com`, `iridco.ir`, `app.hubin.ir`)
- Persian-language betting sites (`delbet.com`, `dubibet724.com`) — overlaps the border-crosser's casino-stratum theme but no agent markers observed
- Two Islamic Azad University branches (`shirazartu.ac.ir` 2026-09-26, `iaoemarkazi.ir` 2026-07-22)
- One IP-literal scan: `http://159.223.173.76/` (2026-09-06, report `e6de37c8-3512-452d-aceb-fabf62550bef`) — IP-literal submissions are mildly interesting but a single one-off is not a campaign
- `tehran` hits are news sites (tehrantimes.com, irannewswire.org) — noise

Verdict: honest negative for agent-shaped Persian-language activity on urlquery.

---

## 4. Our corpora — clean

- Amap fleet (2,141): zero `gov.ir` / iran / farsi / persian / tehran
- openai-agent-traces (589,972): zero
- oai-tag-sweep: 1 hit — **false positive**, "PERSIANN" is a precipitation dataset (Precipitation Estimation from Remotely Sensed Information using Artificial Neural Networks) in a cors-laundering-ops report URL, not Persian language. Eliminated with prejudice.

---

## 5. RTL tradecraft coordination

arabic-agent-hunter and hebrew-agent-hunter lanes exist (BRIEF.md + raw only, no findings yet at time of writing) — no tradecraft to coordinate with yet. RTL-specific tells to share when they report: mixed-direction probe parameters, percent-encoded Hebrew/Arabic/Persian path segments in scan URLs, right-to-left override characters (U+202E) in payloads. None observed in this lane's data.

---

## 6. Method notes (for the durable record)

- urlquery.net root was timing out from this VM during the run; the keyless htmx report-data endpoints (`/api/htmx/report/{id}/filter/http`) still worked — they appear to be served from a different path than the homepage.
- urlscan.io `/api/v1/search/?q=domain:gov.ir` works keyless (the earlier `domain:*.gov.ir` form with asterisk returned empty — use bare `domain:gov.ir`).
- urlscan full-result API (`/api/v1/result/{uuid}/`) returns 403 "You're not logged in!" without auth — but public result pages (`/result/{uuid}/`) are fetchable as text.
- Remember the Polyglot warning: urlquery htmx search misses known-live records — every htmx zero here is a weak negative.

---

## URL LIST (all observed)

**Gov.ir re-scan campaign (urlscan, GENUINELY NEW):**
- https://urlscan.io/result/01a1096f-9c14-71bf-a64a-96813ba27c29/ (mcls.gov.ir, 2026-10-05)
- https://urlscan.io/result/01a1054b-18ed-76aa-a6ac-c360a9ead855/ (behdasht.gov.ir, 2026-10-04)
- https://urlscan.io/result/01a1053d-133a-727a-a829-ece4c43e785d/ (darubank.com, 2026-10-04)
- https://urlscan.io/result/01a104bb-7dad-7479-8a5f-717c3afeb625/ (ict.gov.ir/en/more/links/affiliated, 2026-10-04)
- https://urlscan.io/result/01a104ae-27c4-7189-9448-c20e98d41692/ (ihio.gov.ir, 2026-10-04)
- https://urlscan.io/result/01a0f5b5-3037-7799-9fbd-deb80f4271de/ (mfa.ir, 2026-10-01)
- https://urlscan.io/result/01a0f7e8-c904-7698-afd9-14b07e315933/ (darubank.com, 2026-10-01)
- https://urlscan.io/result/01a0e092-e919-76f0-a7da-75eff35a081d/ (tax.gov.ir, 2026-09-27)
- https://urlscan.io/result/01a0c18a-0f66-731d-97c1-c7a98dea8894/ (my.gov.ir, 2026-09-21)
- https://urlscan.io/result/01a0937d-5528-73da-bbad-714bea677e10/ (mcls.gov.ir, 2026-09-12)
- https://urlscan.io/result/01a08f5b-29e2-74ce-b516-556b41965305/ (behdasht.gov.ir, 2026-09-11)
- https://urlscan.io/result/01a08ebb-04ba-753b-8ff1-44f710c31dfa/ (ihio.gov.ir, 2026-09-11)
- https://urlscan.io/result/01a07fc1-1dca-758a-824c-44893687fb45/ (mfa.ir, 2026-09-08)
- https://urlscan.io/result/01a07b5d-777c-72ee-972b-99e3d7a52f89/ (my.gov.ir, 2026-09-07)

**urlquery MFA reports (eliminated, researcher-shaped):**
- https://urlquery.net/report/b904e35f-52b2-4a71-b86a-40e431dfe3f1 (mikhak.mfa.gov.ir/form/landing.xhtml)
- https://urlquery.net/report/f1ed5bc6-5b6c-43be-a738-fa29736cbad0 (kualalumpur.mfa.gov.ir/)

**Persian keyword sweep (language matches, not agent-shaped):**
- https://urlquery.net/report/e6de37c8-3512-452d-aceb-fabf62550bef (http://159.223.173.76/, IP-literal one-off)
- https://urlquery.net/report/adb20a38-fc2e-4116-8308-8b580a1d4f8e (shirazartu.ac.ir/)
- https://urlquery.net/report/eaec267e-ee0a-4df3-ac79-8e7886d67b3b (iaoemarkazi.ir/)

**False positive (documented for the record):**
- https://urlquery.net/report/df9708c1-9c8d-428e-9e6a-36f813d8ec14 ("PERSIANN" = precipitation dataset, not Persian)
