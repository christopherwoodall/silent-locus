# Global South LIVE CHASE — follow-up to the Scout writeup

**Run:** 2026-10-05 ~05:10–05:45 UTC. **Egress:** recovered (urlquery.net HTTP 200). No commits/pushes.
**Tools:** `uq_htmx.py` (urllib) + `uq_htmx_curl.py` (curl fallback — urllib hits IncompleteRead on this VM's egress proxy; the curl variant is the reliable path), `uq.py` (authenticated API, api.urlquery.net). Rate: 1 req/5–6s, ≤3 retries per query.
**Raw:** `raw/chase/live-*.json` (22 domains), `raw/chase/reports/*.json` (12 full reports), `raw/chase/live-go.id-paged.json`.

---

## 1. EVIDENTIARY CORRECTION — the "CORS-laundering" framing is hunter-asserted, not observed

Tracing the indicators back to source changed the grading of the scout's two clusters:

- `cors_conversion_proxy` on the 5 Indonesia records fired **only** on the hunter label `labels.hunt.source_file: wrapper_corsproxy.json` (regex `corsproxy` matches the filename). The live API report for `1df03d5a` shows a **direct submission of the plain URL** — no relay wrapper, no proxy chain in the submission.
- `jina_allorigins_dagd` on the 3 Brazil records fired **only** on `hunt.source_file: wrapper_allorigins.json` ("allorigins" in the filename). Same circularity.
- `hunt.campaign: cors-laundering-ops` (2,642 records) and the `wrapper_*.json` source files are annotations from the prior `urlquery-agent-activity-hunt` project, not submitter-side evidence. The hunter's `wrapper_corsproxy.json` file was 1,109 records of `*.translate.goog`-wrapped URLs — **the 5 plain go.id URLs are anomalies inside that file** (the hunter's inclusion rule for them is not recoverable from the data).
- All 8 reports (ID×5 + BR×3) share `settings.exit_node: qguvgzjxzsgb3vs` — but urlquery's corpus has only **two** exit_node values total; this is the scanner pool, not submitter linkage. The new MARINA reports (below) hit both exit nodes, confirming exit_node is scanner-side routing.

**What survives as independent agent-shape evidence (submitter-side, in the URLs themselves):**
- `?utm_source=chatgpt.com` on the Balikpapan URL (faa48376) — copied out of a ChatGPT answer
- Hex nonce `65c30481d5d51` in the KKP path (1e16f79e)
- Municipality walk: Gresik (Jul 8) → Balikpapan + Semarang ~3h apart (Jul 15) → Aceh (Jul 19) → KKP (Aug 31)
- Joomla `com_media` probe on a religious-court site
- All submitted to a public URL scanner (the known agent research habit)

**Verdict:** the Indonesia cluster stands as an agent-shaped scanning cluster, but the "CORS-laundering relay on every hit" claim is WITHDRAWN — it was hunter metadata, not observed relay chains. Same-harness-family linkage to cors-laundering-ops is **not established** from the report payloads.

---

## 2. NEW LIVE FINDS

### 2a. Brazil — ANATEL thread extends into October (same pattern, new siblings)
Live `gov.br` query returned two NEW `anatel.gov.br` bare-domain submissions:
- `84e184b2-bc72-4666-8c17-180a7ebe0d91` — 2026-10-03T12:41:00Z
- `1a456551-5bd7-4190-993b-809b67bb25a6` — 2026-10-04T03:52:00Z

Full reports pulled: same stock Firefox UA (rv:134.0), same exit_node `qguvgzjxzsgb3vs`, no tags, plain `http://anatel.gov.br` submission → final `https://www.gov.br/anatel/pt-br`. The ANATEL thread now reads: **Jul 19 → Aug 13 → Oct 3 → Oct 4** — four bare-domain reads over 2.5 months. Persistent low-and-slow interest in the telecom regulator, not a burst.
Also live: a **Sep 30–Oct 1 cluster around Brazil's Ministry of Justice SEI document system** — `sei.mj.gov.br/sei/modulos/pesquisa/md_pesq_processo_pesquisar.php?...`, `sei.mj.gov.br/sei/controlador_externo.php?acao=documento_conferir&id_orgao_acesso_externo=0`, `sei.consulta.mj.gov.br/`, `sei.autentica.mj.gov.br/`, plus `cooperacaopenal@mj.gov.br/` (email-as-URL). 5 submissions in ~2 days. Agent research into a justice document system, or targeted recon — worth watching, not yet attributable.

### 2b. Philippines — NEW programmatic cluster: MARINA certificate-serial enumeration (previously unreported)
Live `gov.ph` query surfaced **15 reports, 2026-05-11 → 2026-07-07**, all hitting the Philippines Maritime Industry Authority ID-certificate verification endpoint with varying `serial_number` values:
`user-lb-onprem.marina.gov.ph/verify-id-certificate?serial_number=6290845` … `7035351`, `7035353`, `7635306`, `7509240`, `7497524`, `6568696`, `8286725`, `8343181`, `6903935`, `8643823`, `8652918`, `6967761`, `6516930` (+ one bare endpoint, no serial). Two hosts (`user-lb-onprem`, `online-appointment`), triple-submits within the same minute on May 18 and Jun 8. Full reports: stock UA, both exit nodes. **Grading: programmatic endpoint enumeration — agent-shaped.** Same ID-verification-task family as the Vietnam pxweb API work (sequential-ID probing of a government verification API).

### 2c. Egypt — ETA e-invoice share-link cluster (candidate, researcher-shaped)
Live `gov.eg` confirmed the two Jul-17 EDA `?utm_source=chatgpt.com` reports, plus **10 reports May→Oct 2026** submitting Egyptian Tax Authority e-invoicing **document share links**: `invoicing.eta.gov.eg/documents/<20-char code>/share/<~40-char token>` (latest 2026-10-04). Bearer-token document URLs submitted repeatedly over 5 months — consistent with one party validating leaked/collected invoice links. Grading: candidate pattern, researcher-shaped rather than agent-shaped; watch.

### 2d. UAE — `?utm_source=chatgpt.com` on Dubai Health Authority
`www.dha.gov.ae/En?utm_source=chatgpt.com` — 2026-05-20. Third independent `utm_source=chatgpt.com` government-URL sighting (Indonesia Balikpapan, Egypt EDA ×2, now UAE DHA). The marker keeps recurring across regions: agents copying gov URLs out of ChatGPT answers and submitting them to urlquery.

### 2e. Indonesia — live siblings in the go.id window (Sep 14–Oct 4)
- `yaumuna.pa-jember.go.id/` (2026-08-22) — **another `pa-*.go.id` religious court**, one month after pa-gresik. Same target class as the cluster's first hit.
- `sipantas.kuansing.go.id/nestin/microsoft_passwordless_1787816751855.html` ×2 within a minute (2026-08-31, same day as the KKP hit) — phishing-kit-style artifact with ms-epoch-ish nonce.
- `s.kemkes.go.id/qi8re4q` ×3 (Sep 15/18/19) + `s.kemkes.go.id/8lneowx` — health-ministry short-URL code reuse.
- `magma.esdm.go.id` ×4 (Sep 15–21) — repeated volcano-monitoring submissions.
- The KKP cluster record (1e16f79e) is present in the live index.

---

## 3. Live honest checks

- **gov.th: 0 reports** — clean live negative.
- gov.za, gov.ng, gob.mx, gov.sa, gov.my, gov.bd, gov.pk, gov.kz, gov.uz, gov.ir, gov.qa, gov.co, gob.ar, gob.cl, gob.pe, gov.ae, gov.in: background researcher/phishing-check noise only — typosquat submissions (`labourgovt-za.org`, `www.services-balady-gov-sa.cc`, `dc.crsorgi.gov.in.viewcart.life`, `www.incometax.my.id`), XSS probes, defaced subdomains (`www.seroja88.hospitalvirgendefatima.gob.pe`), no agent-shaped clusters.
- gov.in `ddgmui.imd.gov.in/radar/RadarDisplayStatusRecords.php?uid=dwhyderabad` ×2 same minute (Sep 22) — minor double-hit, not a cluster.
- gov.my `www.eperolehan.gov.my/` ×3 within 20 min (Jul 13) — small burst on the procurement portal, ambiguous.

---

## 4. Full-report metadata (12 pulled via authenticated API)

All: `settings.useragent` = stock urlquery Firefox `Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0` (self-identification lives in URLs, not UAs), `settings.access` = public, `tags` = [] (urlquery-native tags; the `urlquery-hunt`/`agent-activity` tags exist only in the frozen hunter corpus, not on urlquery.net).

| report | date | submitted URL | exit_node | target ASN |
|---|---|---|---|---|
| 1df03d5a | 2026-07-08 | pa-gresik.go.id/index.php?option=com_media | qguvgzjxzsgb3vs | Hostinger DE |
| faa48376 | 2026-07-15 | jdih.balikpapan.go.id/dokumen/610/detail?utm_source=chatgpt.com | qguvgzjxzsgb3vs | Balikpapan city gov ID |
| a9c7e089 | 2026-07-15 | www.dinkes.semarangkota.go.id/ | qguvgzjxzsgb3vs | Semarang city gov ID |
| 09195203 | 2026-07-19 | dinkes.acehprov.go.id/detailpost/abcde-cegah-stunting | qguvgzjxzsgb3vs | Aceh prov gov ID |
| 1e16f79e | 2026-08-31 | www.kkp.go.id/.../sertifikat65c30481d5d51/detail.html | qguvgzjxzsgb3vs | AWS ID |
| dd4fa017 | 2026-07-19 | anatel.gov.br/ → www.gov.br/anatel/pt-br | qguvgzjxzsgb3vs | Cloudflare |
| b11fd092 | 2026-08-13 | www.anatel.gov.br → www.gov.br/anatel/pt-br | qguvgzjxzsgb3vs | Cloudflare |
| 46e7c66d | 2026-08-14 | esporte.gov.br/ → www.gov.br/esporte/pt-br | qguvgzjxzsgb3vs | SERPRO BR |
| 1a456551 | 2026-10-03 | anatel.gov.br | qguvgzjxzsgb3vs | (live) |
| 84e184b2 | 2026-10-04 | anatel.gov.br | qguvgzjxzsgb3vs | (live) |
| a2a6bf20 | 2026-10-01 | sei.mj.gov.br/sei/modulos/pesquisa/md_pesq_processo_pesquisar.php?... | qguvgzjxzsgb3vs | (live) |
| edbb1691 / 65733be0 / 90eacad6 | 2026-05-11 / 05-18 / 06-16 | marina.gov.ph/verify-id-certificate?serial_number=… | z0yflva4pidy47h / z0yflva4pidy47h / qguvgzjxzsgb3vs | (live) |
| 29147029 | 2026-10-04 | invoicing.eta.gov.eg/documents/XKGQ0TMSEZ2AS2T7DWPF234M10/share/… | qguvgzjxzsgb3vs | e-finance EG |

Note: pa-gresik.go.id resolves to Hostinger (DE/US) — the religious-court site is on shared hosting; it loaded normally (Joomla, jcemediabox) at scan time.

---

## 5. Pending

1. The hunter's `wrapper_corsproxy.json` / `wrapper_allorigins.json` inclusion rule for the 8 plain-URL records is unrecoverable from local data — the prior hunt project may hold the answer.
2. `sei.mj.gov.br` cluster (5 submissions, Sep 30–Oct 1): pull full reports, check for agent markers.
3. MARINA cluster: 15 reports bounded May 11–Jul 7 — check whether it resumes after Jul 7 (live query again in a week); enumerate serial_number values for sequence analysis.
4. ETA invoice share-links: identify whether one submitter (timing analysis across the 10 reports).

---

## APPENDIX — All observed URLs (live chase)

### Brazil (new + cluster)
- https://urlquery.net/report/1a456551-5bd7-4190-993b-809b67bb25a6 (anatel.gov.br, 2026-10-04)
- https://urlquery.net/report/84e184b2-bc72-4666-8c17-180a7ebe0d91 (anatel.gov.br, 2026-10-03)
- https://urlquery.net/report/a2a6bf20-4c91-4c69-8caa-2bb570e52863 (sei.mj.gov.br SEI pesquisa, 2026-10-01)
- https://urlquery.net/report/0277e5ea-0e9c-4cf1-a54d-8ec469218557 (sei.mj.gov.br controlador_externo, 2026-09-30)
- sei.consulta.mj.gov.br/ | sei.autentica.mj.gov.br/ | cooperacaopenal@mj.gov.br/
- agenciasp.sp.gov.br | defesacivil.sp.gov.br | gov.br

### Philippines — MARINA serial enumeration (all `verify-id-certificate?serial_number=`)
- https://urlquery.net/report/edbb1691-fa9c-4648-948a-0dc93c1e25d6 (6290845, 2026-05-11, online-appointment host)
- https://urlquery.net/report/65733be0-8dde-4e09-a90d-63a424ebaf48 (7035353, 2026-05-18)
- https://urlquery.net/report/1fced53c-13f0-4d72-bf88-eafb9a85a2e8 (7035351, 2026-05-18)
- https://urlquery.net/report/e2d4c3e9-9cf5-4eed-b206-37c83f9de612 (7635306, 2026-05-18)
- https://urlquery.net/report/6c4665fa-3ee7-4b3b-819e-6e5611b2409a (6568696, 2026-06-07, online-appointment host)
- https://urlquery.net/report/1594304b-34f9-4364-9e04-d3b9ad7afa6f (7509240, 2026-06-08)
- https://urlquery.net/report/bd2aa42c-14ec-4e12-9d2b-8fb4c316d3e6 (7497524, 2026-06-08)
- https://urlquery.net/report/823c1ab5-72ab-452b-8598-8f8b73a31690 (8286725, 2026-06-13)
- https://urlquery.net/report/90eacad6-683a-4dd5-a29d-dec6fa2d8cdd (8343181, 2026-06-16)
- https://urlquery.net/report/385e2ea6-b436-4a13-9159-32796bc5ff69 (6903935, 2026-06-16)
- https://urlquery.net/report/dcb57f69-779a-44ce-8378-a3a999417d9f (8643823, 2026-06-19)
- https://urlquery.net/report/86fdd0bb-3b77-474b-b49a-19ca3c5e8a2e (bare endpoint, 2026-06-27, online-appointment host)
- https://urlquery.net/report/7521680b-22b2-433c-9997-c2553bc22c24 (6516930, 2026-06-28, online-appointment host)
- https://urlquery.net/report/b2cb4f4a-19cb-47a4-98d9-b4df1bea3703 (8652918, 2026-07-02)
- https://urlquery.net/report/3fbec429-2158-4005-b46c-c882fa8023f0 (6967761, 2026-07-07)

### Egypt
- https://urlquery.net/report/29147029-63db-4ada-b9bf-e6885e8682c8 (invoicing.eta.gov.eg/documents/XKGQ0TMSEZ2AS2T7DWPF234M10/share/HBA4QYNJAY65E1E1DWPF234M105lbmYv1791104637, 2026-10-04)
- invoicing.eta.gov.eg/documents/SK496VRTSNAJYKXQ9ASMC9WK10/share/YDVZMAWTTKXSN6K29ASMC9WK107BhTQB178272668 (2026-08-30)
- invoicing.eta.gov.eg/documents/W8PN05SENBARNA2RCDK1YRWK10/share/RJ1PSJFXXCTKE0Z4CDK1YRWK10pm03YY178324824 (2026-08-17)
- invoicing.eta.gov.eg/documents/FCSDF0M0S3EFDA3V6BQBJX2J10/share/WXNPCJAATXAE6HRV6BQBJX2J10uNOA1D172112673 (2026-08-15)
- invoicing.eta.gov.eg/documents/RK76M9601ETHXNRME248503J10/share/88Y57J1VNYGM5798E248503J10RB3BgM172121365 (2026-08-15)
- invoicing.eta.gov.eg/documents/5NZNPD369MHAWMFVQQYXAW3J10/share/T84MYJDBV3KC4NJZQQYXAW3J106v0vXr172215913 (2026-08-15)
- invoicing.eta.gov.eg/documents/MZEK8FWE6722BR2SEW293TWK10/share/9PZW865EH047Y4EXFW293TWK10r9iJoA178328728 (2026-08-09)
- invoicing.eta.gov.eg/documents (2026-08-03)
- invoicing.eta.gov.eg/documents/0CDETFKF1KDH8P07M58PG3ZK10/share/HVX2DPAPSM4QVDHMM58PG3ZK10uFjfes178575082 (2026-08-03)
- invoicing.eta.gov.eg/documents/ZXD1ZTSX1E388GQE4BZ6FWJK10/share/B08K2651APNRNJAZ4BZ6FWJK10xXCDe1177262949 (2026-05-11)
- edaegypt.gov.eg/en/media-center/news/during-the-fifth-edition-of-africa-health-excon-2026-eda-supports-strategic-partnerships-to-localize-vaccine-manufacturing-and-strengthen-health-security-across-africa/?utm_source=chatgpt.com (2026-07-17, report 28ed7589)
- www.edaegypt.gov.eg/en/media-center/news/dr-ali-el-ghamrawy-chairman-of-the-eda-participated-in-africa-he… (2026-07-17, report 6c6e30da)

### Indonesia (live siblings, Sep–Oct window)
- yaumuna.pa-jember.go.id/ (2026-08-22)
- sipantas.kuansing.go.id/nestin/microsoft_passwordless_1787816751855.html ×2 (2026-08-31)
- s.kemkes.go.id/qi8re4q ×3 (2026-09-15/18/19) | s.kemkes.go.id/8lneowx (2026-09-24)
- magma.esdm.go.id ×4 (2026-09-15–21) | magma.vsi.esdm.go.id/dist/assets/plugins/bootstrap/js/by.txt (2026-09-14)
- cekbansos.kemensos.go.id/ (2026-09-07) | sinta.kemdiktisaintek.go.id/authors/profile/6697212/?view=iprs (2026-09-06)
- disdukcapil.muaraenimkab.go.id/ (2026-08-31) | jdih.kemenkoinfra.go.id/infografis/gerakan-peduli-dan-berbudaya-lingkungan-hidup-di-sekolah (2026-08-30)
- backend.kemendagri.go.id | dukcapil.kemendagri.go.id/#slider_3 (2026-08-29)
- s.kemkes.go.id/ejuiaer?dues.zion@hotmail.com | s.kemkes.go.id/ejuiaer?kbensi@salemreps.com (2026-08-27/28)
- lms.kop.go.id/courses/8a1c0f6b-65c0-41c0-936a-949fe28c5f16 (2026-09-28)
- simkopdes.go.id/ (2026-09-28) | pn-bekasikota.go.id/ (2026-09-27)
- pa-bondowoso.go.id/ (2026-08-29) | sipp.pa-pangkalanbun.go.id/ (2026-09-26)

### UAE
- www.dha.gov.ae/En?utm_source=chatgpt.com (2026-05-20)
- researchaward.gdrfad.gov.ae (2026-10-04) | smart.gdrfad.gov.ae (2026-10-03) | tahseel.gov.ae (2026-09-29)
- uaegovsurveys.gov.ae/ar/surveys/l/xinzxrxr22nw | uaegovsurveys.gov.ae/en/home/showEmail?email=314&token=xinzxrxr22nw (2026-06-08)

### India (notable)
- dc.crsorgi.gov.in.viewcart.life (2026-09-29, typosquat) | dc.crsorgi.com.cer-verify.com/admin/web/index.php/auth/birthCertificate/view/B/b3WF4VExRZC9GTnhBWkhtZTNrd (2026-09-23, typosquat)
- www.incometax.my.id (2026-07-29, typosquat)
- ddgmui.imd.gov.in/radar/RadarDisplayStatusRecords.php?uid=dwhyderabad ×2 (2026-09-22)
- impact.indiaai.gov.in (2026-10-03) | aikosh.indiaai.gov.in (2026-10-01)

### Other live notes
- gov.th: zero reports (clean negative)
- gob.pe: www.seroja88.hospitalvirgendefatima.gob.pe/ (2026-07-03, gambling-spam defaced subdomain)
- gov.co: www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=27941 ×2 same minute (2026-07-12)
- gob.mx: a517c6:sbyh0h@www.tlaquepaque.gob.mx/busqueda?s=%3Cscript%20src%3D%2F%2Fcdn.farolesa.mx%2Fpdf.js%3E%3C%2F (2026-08-17, XSS probe with creds)
- gov.za: labourgovt-za.org/ (2026-09-25, typosquat); www.dhet.gov.za/ScrollingBanner/Welcome%20DM%20Email%20signature.jpgstyle=%22width:680px;height:177px (2026-07-15, injection probe)
- gov.sa: www.services-balady-gov-sa.cc (2026-09-27, typosquat)
- gov.kz: stat.gov.kz ×5 (statistics bureau page loads, 2025-10 → 2026-06)
