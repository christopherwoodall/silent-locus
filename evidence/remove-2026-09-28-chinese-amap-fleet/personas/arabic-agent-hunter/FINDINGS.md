# Arabic/MENA Agent Hunter — FINDINGS

**Persona:** hunt AGENT-shaped activity in Arabic-language and MENA surfaces. Foreign-agent hunt.
**Date:** 2026-10-05. Nothing pushed.
**Egress:** up but flaky (IncompleteRead mid-chunk on urllib path; curl variant `uq_htmx_curl.py` used as fallback).

## Method
- 13 `url.domain:` queries (gov.sa/ae/eg/qa/kw/bh/om/jo/iq/lb/ma/tn/dz) — **all returned 0, later proven unreliable** (see §5)
- 14 keyword queries (same domains) via curl variant
- 8 Arabic agentness-word queries: وكيل (agent), مهمة (task), استخراج (extraction), استعلام (query), تحقق (verify), مسح (scan), اختبار (test), بحث (search)
- Local verification against our 3 corpora (688,466 records total)
- Ramadan signature test (§4)
- urlscan.io spot check

## 1. FOURTH `utm_source=chatgpt.com` government-URL sighting — Iraq

`www.cert.gov.iq/?utm_source=chatgpt.com` — 2025-03-21, report `96817b7c-…`. This is the fourth independent sighting of the marker on a government URL:
1. Indonesia — `jdih.balikpapan.go.id/…?utm_source=chatgpt.com` (Jul 15, 2026)
2. Egypt — EDA articles ×2 (Jul 17, 2026)
3. UAE — `www.dha.gov.ae/En?utm_source=chatgpt.com` (May 20, 2026)
4. **Iraq — `www.cert.gov.iq/?utm_source=chatgpt.com` (Mar 21, 2025)** — earliest of the four

Same grammar everywhere: an agent (or human) copied a gov URL out of a ChatGPT answer and submitted it to urlquery. Cross-harness, cross-region marker. Not agent-shaped on its own — but the recurrence across four countries makes it a fleet-independent tripwire: any `?utm_source=chatgpt.com` on a gov domain is worth grading.

## 2. Egypt ETA e-invoice cluster — re-verified, Ramadan signature TESTED (negative)

35 live reports, May 2025 → Oct 2026: `invoicing.eta.gov.eg/documents/<20-char>/share/<~40-char token>` bearer-token URLs. Grading stands: researcher-shaped, not agent-shaped.

**Ramadan night-shift test** (cultural-anthropologist-global signature: activity shifts to 19:00–04:00 local during Ramadan weeks):
- Ramadan 2026 window: ~Feb 18 – Mar 19. Egypt = UTC+2.
- In-window reports: 2026-03-05 ×2 at **15:22 local**, 2026-03-16 at **11:05 local** — midday/afternoon, NOT the night-shift pattern.
- Full cluster hour-of-day: overwhelmingly 09:00–17:00 local — a human researcher's workday.
- Eid al-Fitr (~Mar 20): reports on Mar 25 and Mar 30 — no holiday silence.
- **Verdict: Ramadan signature NOT observed in this cluster.** Tested negative, consistent with researcher-shaped grading. The signature itself remains valid as a hunt rule for genuinely agent-shaped MENA clusters.

## 3. MENA gov domains — no agent-shaped clusters anywhere

| Domain | Live reports | Verdict |
|---|---|---|
| gov.sa | 50 | Sparse one-offs. Task-family echoes: GOSI QuickVerify ECertificate ×2 same hour (Aug 16), sfda.gov.sa gibberish-path pairs (Jul 11), freelance.sa cert-validation ×3, ksavisa QR lookup, address.gov.sa proof verification. No enumeration, no nonce grammar. |
| gov.ae | 46 | One-offs. dubaided eservices ×3 (Jun), uaegovsurveys token pair (Jun 8), DHA chatgpt.com sighting (known). No cluster. |
| gov.kw | 43 | One-offs. kff.gov.kw asset bursts (Mar 26, 5× same minute — asset check, not agent), moi QR verify. No cluster. |
| gov.iq | 23 | One-offs + the Iraq chatgpt.com sighting (§1). sis.mohesr.gov.iq login ×2. No cluster. |
| gov.qa | 22 | One-offs. No cluster. |
| gov.jo | 22 | One-offs (cbj, dos, mfa, moenv). One Arabic path: moenv.gov.jo/ar/list/الوزراء. No cluster. |
| gov.om | 21 | One-offs (mol ×4, evisa ROP ×2). No cluster. |
| gov.bh | 21 | One-offs + moh.gov.bh/vaccineverify (ID verification, single). haj.gov.bh session URLs ×2. No cluster. |

No programmatic enumeration, no nonce/tag grammar, no burst cadences on any MENA gov domain. The verification/validation URL task family (GOSI, MARINA, ETA, freelance.sa, moh.bh) recurs across regions but stays at researcher-shaped one-off/double level in MENA.

## 4. Arabic language — the fleet writes nothing in it

- **Zero Arabic script (U+0600–U+06FF) across 688,466 records** in all three corpora (amap 2,141; openai-agent-traces 589,972; oai-tag-sweep 96,353).
- Two percent-encoded Arabic hits in tag-sweep = **target-side SEO spam**, not agent writing: `akramafif.net/زوجة-أكرم-عفيف-…` (Qatar footballer gossip) and `africaconnect.travel/كازينو-888-…` (casino affiliate). Both carry the withdrawn hunter indicator; graded as noise.
- 119 reports across 8 Arabic agentness words = keyword noise (phishing pages, commercial sites, exam sites, casino). No agent-shaped programs.
- **Consistent with the ASCII-only finding:** if these agents operate in MENA, they do it in ASCII/English, not Arabic.

## 5. Methodological warning — htmx `url.domain:` is unreliable

`url.domain:gov.eg` returned **0 reports** while keyword `gov.eg` / `invoicing.eta.gov.eg` returns **35 live reports**. Same gap the Polyglot found for `go.id`. The `url.domain:` operator misses known-live records — every domain-query zero is a weak negative. Use keyword queries + curl fallback.

## Honest negatives
- No Arabic-marker agent fleet on urlquery.net.
- No MENA gov enumeration cluster (agent-shaped) found.
- Ramadan night-shift signature: tested against the ETA cluster, negative.
- Eid al-Adha (~May 27, 2026) window: ETA cluster has reports May 4 and May 11 — no silence either side.

## Open leads
- GOSI QuickVerify ×2 same hour — watch for a third.
- sfda.gov.sa gibberish-path pairs — possible fuzzer; check siblings.
- The chatgpt.com-on-gov tripwire: hunt `?utm_source=chatgpt.com` + gov domains as a cross-harness early-warning.
- Ramadan signature retest if a genuinely agent-shaped MENA cluster appears.

---

## APPENDIX — All observed URLs

### Iraq chatgpt.com sighting
- https://urlquery.net/report/96817b7c (www.cert.gov.iq/?utm_source=chatgpt.com, 2025-03-21)

### Egypt ETA e-invoice cluster (sample; 35 total)
- https://urlquery.net/report/29147029-63db-4ada-b9bf-e6885e8682c8 (2026-10-04)
- https://urlquery.net/report/930c0bde-d303-432d-9114-2879174337b1 (2026-08-30)
- https://urlquery.net/report/c0223605-5ba1-49e9-9992-b64a28c6e3b9 (2026-08-17)
- invoicing.eta.gov.eg/documents/XKGQ0TMSEZ2AS2T7DWPF234M10/share/HBA4QYNJAY65E1E1DWPF234M105lbmYv1791104637

### Saudi verification echoes
- www.gosi.gov.sa/ar/QuickVerify/ECertificate?Type=4&StakeholderValue=1045617105&CertificateNumber=11811594
- www.sfda.gov.sa/ZRQXS/YibQa/kbmLR/
- www.sfda.gov.sa/YibQa/kbmLR/
- freelance.sa/certificate-validation/certificate-validation-details/rkwtntkxntuznzew
- services.ksavisa.sa/Home/PrintTourVisitByQRCode?AppNo=E816295566&Passport=A40940518&NatIso=EGY
- proof.address.gov.sa/verifyproofna.aspx?type=i&ID=1061169791&doc=1069396775

### UAE
- eservices.dubaided.gov.ae/rt/3050962793.0
- eservices.dubaided.gov.ae/rt/3966750516.0
- uaegovsurveys.gov.ae/ar/surveys/l/xinzxrxr22nw
- uaegovsurveys.gov.ae/en/home/showEmail?email=314&token=xinzxrxr22nw
- cbws.cbuae.gov.ae/Web/shadowfax/reg/register.html?passresetid=0E62A3F8B5B7290050DA72EE56A3D0E56B0E44
- emsat-uat.moe.gov.ae/emsatregistration/home/setlanguage?culture=en-gb&retrunurl=https://harenssip.co
- www.dha.gov.ae/En?utm_source=chatgpt.com

### Jordan / Oman / Bahrain / Kuwait / Qatar (one-offs)
- www.moenv.gov.jo/ar/list/%D8%A7%D9%84%D9%88%D8%B2%D8%B1%D8%A7%D8%A1 (الوزراء = ministers)
- moepayment.cspd.gov.jo/link/MOFA?BillingNumber=302000186204368164
- evisa.rop.gov.om/en/track-your-application?visanumber=rosjgqwnzyvlt6jbxrb1ea==
- www.moh.gov.bh/vaccineverify?cprnumber=900567112&vaccinationdatedose2=20210423&creationtimedose2=21:
- haj.gov.bh/ords/r/haj/hajj_platform/home?session=32077674713127
- eservices.moi.gov.kw:45314/verify/qrcode?wtleU4q0ez8=ZaQ4drJwnRYzPIAPWQIY1Q%3D%3D

### Arabic-script target pages (noise, not agent writing)
- akramafif.net/%D8%B2%D9%88%D8%AC%D8%A9-%D8%A3%D9%83%D8%B1%D9%85-%D8%B9%D9%81%D9%8A%D9%81-%D8%A7%D9%84%D9%88%D8%AC%D9%87-%D8%A7%D9%84%D8%AE%D9%81%D9%8A-%D9%88%D8%B1%D8%A7%D8%A1-%D8%AA%D8%A3%D9%84%D9%82-%D8%B3%D8%A7/
- africaconnect.travel/%D9%83%D8%A7%D8%B2%D9%8A%D9%86%D9%88-888-%D8%AA%D8%B3%D8%AC%D9%8A%D9%84-%D8%A7%D9%84%D8%AF%D8%AE%D9%88%D9%84-%D8%A7%D9%84%D9%85%D9%88%D9%82%D8%B9-%D8%A7%D9%84%D8%B1%D8%B3%D9%85%D9%8A-%D8%A8%D8%A7-2/
- https://urlquery.net/report/bcf89ad7-68d3-41ce-959a-8a38c943051e
- https://urlquery.net/report/78a5697e-c071-433d-bd10-65f146f96d04
