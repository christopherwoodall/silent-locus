# CARTOGRAPHER LANE — Gov domains by country (urlquery-side live map)

Date: 2026-10-05. Source A = urlquery htmx keyless (`uq_htmx.py`, limits 10–50; full JSON in `raw/gov-domains/<tld>.json`).
Source B = urlscan.io API (30d window) via tool fetch, used only where noted.

## Collection log
- VM egress was DOWN at session start (~05:14–05:24 UTC; both urlquery.net and google.com TLS-timeout via egress proxy).
- `sweep-gov-domains.sh` first pass hit the outage; relaunched with a 5-min retry loop → egress recovered **05:24 UTC**, 9/25 queries succeeded (limit 50), 15 failed with `http.client.IncompleteRead`.
- Root cause of failures: large result pages break the chunked reader. Retry pass at limit 15–20 recovered all 15 (go.id needed limit 10).
- All 25 TLDs now have durable JSON. **Zero exclusion hits** (`uqscan=`/`uqtag=`/`uqvnc=`) in any file. **Zero `translate.goog` FPs** (gov.tr clean).

## Per-TLD verdicts

### go.id (Indonesia) — CONFIRMED-PROGRAMMATIC (urlquery, live)
10 reports, 2026-09-23 → 2026-10-04. Municipality walk continues:
- 2026-09-26 01:42–03:43: `siaptindak.satpolpp.tanjungpinangkota.go.id`, `disbunnak.kuansing.go.id`, `sipp.pa-pangkalanbun.go.id` (3 municipalities, ~2h)
- 2026-09-28 08:05/08:07: `lms.kop.go.id/courses/<uuid>` + `simkopdes.go.id` (2 min apart)
- 2026-09-24: `s.kemkes.go.id/8lneowx` (health-ministry shortlink), `file.data.kemendikdasmen.go.id`
- 2026-09-27: `pn-bekasikota.go.id`, `bblabkesmasmakassar.go.id`
- FP: `jawijawiguguk-slk.desa.id` (desa.id ≠ go.id)
Same municipality-by-municipality grammar as the Jul–Aug `cors-laundering-ops` Indonesia campaign (Global South Scout FINDINGS §1). **The Indonesia campaign is still live.**
(urlscan 30d: 6 hits, all `-go.id` private false positives.)

### gov.br (Brazil) — PROGRAMMATIC burst + agent-shaped re-scan (urlquery)
23 reports, 2026-09-27 → 2026-10-04.
- **2026-09-30 11:34–11:51: 5-hit Ministry of Justice SEI burst** — `sei.autentica.mj.gov.br`, `sei.consulta.mj.gov.br`, `sei.mj.gov.br/sei/controlador_externo.php?acao=documento_conferir`, `sei.mj.gov.br/sei/modulos/pesquisa/md_pesq_processo_pesquisar.php` (+ `cooperacaopenal@mj.gov.br`). Subdomain iteration of the SEI e-document system within 17 min. Programmatic.
- 2026-10-03 12:41 / 2026-10-04 03:52: `anatel.gov.br` ×2 — **same target as the Jul 19 / Aug 13 urlquery-hunt campaign records** (`dd4fa017`, `b11fd092`): live re-scan.
- 2026-10-03 16:12/16:26: `agenciasp.sp.gov.br` + `defesacivil.sp.gov.br` (São Paulo state pair, 14 min).
- 2026-10-01 13:42: another `sei.mj.gov.br` pesquisa hit.
(urlscan 30d: 0.)

### gov.in (India) — AGENT-SHAPED one-offs (urlquery)
15 reports, 2026-09-21 → 2026-10-04.
- 2026-09-22 18:10: `ddgmui.imd.gov.in/radar/RadarDisplayStatusRecords.php?uid=dwhyderabad` + root, same minute (IMD weather-radar burst)
- 2026-09-22 21:14/21:19: `www.det.kerala.gov.in` ×2 (5 min)
- 2026-10-01 / 2026-10-03: `aikosh.indiaai.gov.in`, `impact.indiaai.gov.in` (IndiaAI Mission — AI-infrastructure targeting)
- FP/phish: `dc.crsorgi.gov.in.viewcart.life`, `dc.crsorgi.com.cer-verify.com`
(urlscan 30d: 1 true — `hamraazmp8.gov.in` single, plus 2 FPs.)

### gov.vn (Vietnam) — AGENT-SHAPED one-off cluster (urlquery)
18 reports, 2026-07-16 → 2026-09-25.
- `dieutraio2026_doanhnghiep.nso.gov.vn/Phieu01` (2026-09-25) — NSO 2026 enterprise **survey form**; connects to the known VN national-stats-API task family (Global South Scout FINDINGS §3)
- `quymong.laocai.gov.vn/Controller/BasicController.aspx?csource=<ciphertext>` (2026-09-25) — ASP.NET endpoint with encrypted query param
- `mof.gov.vn` ×2, 28 min apart (2026-09-05)
- `vss.gov.vn`, `moet.gov.vn`, `agritrade.mard.gov.vn`, `phapluat.gov.vn`, `co.moit.gov.cn`/`downloadCO/<uuid>`, `dichvuthongtin.dkkd.gov.vn`
(urlscan 30d: 3 true — `tailieu-verify`/`home-verify`/`shop-verify.gs1.gov.vn` tagged @ecarlesi/gv, Sep 19–28 — human-researcher cluster.)

### gov.eg (Egypt) — AGENT-SHAPED one-off cluster (urlquery)
20 reports, 2026-06-07 → 2026-10-04.
- **`invoicing.eta.gov.eg/documents/<NONCE>/share/<NONCE>` ×9** (2026-08-03 → 2026-10-04) — per-document nonce-share links of the ETA e-invoicing portal, scanned individually. Possible shared-invoice harvesting.
- Known Jul-17 `edaegypt.gov.eg` pair (`28ed7589`, `6c6e30da`) present in file (utm_source=chatgpt.com).
- `sis.gov.eg`, `www.nosi.gov.eg`, `ess.eta.gov.eg/?fbclid=…`, `mohp.gov.eg`, `digital.gov.eg` ×2, `library.statecouncil.gov.eg`, `fineart.gov.eg`, `awkafonline.gov.eg`
(urlscan 30d: 0.)

### gov.uk — HONEST-NEGATIVE (systematic) (urlquery + urlscan)
45 urlquery (Sep 3–Oct 4), 20 urlscan. Scattered dev/research reads: GOV.UK Design System previews on vercel/netlify (many), councils (oldham, bristol ×2, lambeth, newham, camden ×4), `ons.gov.uk` ×2 (8 min, incl. `/testforinvestigation`), `rontranet.gro.gov.uk` ×2 (4 min), `gchq.gov.uk`, `hmrc.gov.uk`, `fcdo.gov.uk`. No enumeration; the `-gov.uk` phish/test noise (bodgeham, eta-gov.uk, viewandproove) is phishing-research, not gov scanning.

### gov.au — AGENT-SHAPED / programmatic-leaning (urlquery) ⭐
20 reports, 2026-09-25 → 2026-10-02.
- **2026-10-02 13:25–15:20: `aihw.gov.au` ×3 in 2h** — `viz.aihw.gov.au/t/Public/views/PBSdashboardallATC1-…/PBSDashboard` (Tableau), `www.aihw.gov.au/getmedia/…/…pbs-atc1-prescriptions-monthly-data_keep.zip` (dataset), `www.aihw.gov.au/reports/hospitals/dry-chemistry-pathology-trial-part-1/contents/summary`. **This is the same PBS Tableau dashboard family Transluce documented as an agent intrusion attempt (Jun 20–21). Re-targeted.**
- **2026-09-29 15:01–15:54: medicare cluster** — `medicarestatistics.humanservices.gov.au/SASStoredProcess/do` + `/statistics/mbs_group.jsp` + `www.medicare.gov.au` within 1h
- `data.gov.au` ×2, `nt.gov.au`, `dfat.gov.au`, `www.cdc.gov.au`, NSW park sites
(urlscan 30d: 3 hits, all `gov.au.<ip>.cpanel.site` phish FPs.)

### gov.ca — HONEST-NEGATIVE (1 hyphenated one-off: `gosj-gov.ca`, 2026-06-15)

### gov.cn — HONEST-NEGATIVE on urlquery; CONFIRMED-PROGRAMMATIC sweep on urlscan.io ⭐
urlquery: 15 reports, zero true .gov.cn (all .com/.cn/.net private keyword FPs).
urlscan (30d): **389 results; Oct 2–5 continuous province-walk**:
- `<province>.12388.gov.cn` + `/xinfang/servlet/randimg` (captcha polling): fujian, hebei ×3, hainan ×2, shaanxi ×2, hubei, ningxia, guizhou, shanghai, chongqing, shanxi, yunnan — 纪委 anti-corruption reporting portals
- `<prov>.ysbz.119.gov.cn` ×15+ (hn, jl, sn, xj, tj, fj, yf, hl, gd, xjsl, sc, sd, xz, js…) — **all resolve to one WAF host 58.48.55.72 (CT2-WAAP), all return identical NWAF 405** = subdomain iteration against a single backend
- `<prov>.119.gov.cn` (fire/emergency): tj, gz, fj, yf, ldxx.yn119 ×3, mhjyywxl, xfhyjd
- `12380.gov.cn` ×2, `xiangyang12380.gov.cn`, `yb12380.gov.cn` (org-dept reporting); `jl.12348.gov.cn`, `ha.12348.gov.cn` (legal aid)
All method=api, public, untagged, resubmits common. **A scanner campaign walking Chinese gov complaint/reporting portals province-by-province, live Oct 2–5.** Agent-shaped; attribution open (human-run scanner vs agent).

### gov.tw — AGENT-SHAPED burst, stale (urlquery)
21 reports, 2026-05-25 → 2026-08-31.
- **2026-05-26 03:30–09:08: 7 hits in 5.5h** — `www.pet.gov.tw`, `news.lgps.tn.edu.tw`, `chacha.tainan.gov.tw`, `csreports.ntsec.gov.tw`, `twps.chc.edu.tw`, `mental.tycg.gov.tw` (+ `data.gov.tw/dataset/22230` 05-27). Tainan/Taichung municipal cluster.
- 2026-07-21 04:44–12:48: 4 hits (`sunology.yatsen`, `vdi.ntuh`, `opendata.tycg`, …)
- Not agent-live: window is May–Aug; urlscan 30d has 2 one-offs (`6000.gov.tw`, `500.gov.tw` sports admin).
FP: `gov-invoice.longhanng.icu`.

### gov.hk — HONEST-NEGATIVE (urlquery 22, May–Oct, spread; urlscan 30d: 0)
`immd.gov.hk` ×2, `hkma.gov.hk` ×3, `vpr.hkma.gov.hk` ×2, `news.gov.hk`, `secure4.epd.gov.hk`, `core2.iamsmart.gov.hk`, `customs.gov.hk`, `sehk.gov.hk`, `gohk.gov.hk`, `access.gov.hk`, `td.gov.hk`, `edb.gov.hk`, `epd.gov.hk`, `ptfss.gov.hk`, `vhis.gov.hk` (utm_source=chatgpt.com).

### gov.sg — HONEST-NEGATIVE (systematic) (urlquery + urlscan)
urlquery 21 (Jul–Oct): `moh.gov.sg`, `app.singpass.gov.sg`, `iras.gov.sg` ×3 (Jul 8; Sep 14 ×2 `/getrefund` phish-lure pair), `adm.vica.gov.sg`, `www.mycareersfuture.gov.sg`, `homes.hdb.gov.sg`, `www.singstat.gov.sg`, `go.gov.sg/askgov-gpls`, `home.booking.gov.sg`, `legacy.postman.gov.sg`, `www.caas.gov.sg`.
urlscan 30d: dominated by programmatic **LTA phishing-kit scans** (`lta.<rand>.top/gov.sg`, `onemotoring.toller*.top/gov.sg`, `lta-billcenter.com`) — phishing research, not gov.sg scanning. One true: `avbcsummit-26.gov.sg`.

### gov.my — HONEST-NEGATIVE (urlquery 19, Jul–Oct; two small pairs)
`eperolehan.gov.my` ×2 (8 min, Jul 13), `skas.sarawak.gov.my` + `johorpay.johor.gov.my` (5 min, Jul 21). Rest spread.
(urlscan 30d: 0.)

### gov.ph — AGENT-SHAPED: MARINA certificate-serial iteration (urlquery) ⭐
20 reports, 2026-06-18 → 2026-10-04.
- **`marina.gov.ph/verify-id-certificate?serial_number=<N>` ×4**: 8643823 (Jun 19), 6516930 (Jun 28), 8652918 (Jul 2), 6967761 (Jul 7) — numeric serial iteration on a certificate-verification endpoint. Programmatic probe family.
- `catbaloganwd.gov.ph` (Oct 4), `iregis-applicant-v2.dti.gov.ph`, `clearance.nbi.gov.ph`, `platforms.e.gov.ph/login`, `dmw.gov.ph` ×2, `www.comelec.gov.ph/?r=2025BARMMPE/ProjectOfPrecincts`, `www.unesco.gov.ph`
- FP: `pcso-gov.ph` (hyphenated), `ncap.vjqmwt.club/gov.ph`
(urlscan 30d: 643 hits — all `-gov.ph` phish-kit cluster on **45.79.222.138** (`dswd`/`dilg`/`pco`/`ncsc`/`denr`/`pnp`-named impersonations), some tagged @ecarlesi/gv. Not gov scanning — flag as separate phish-infra finding.)

### gov.th — HONEST-NEGATIVE (0 urlquery, 0 urlscan)

### gov.pk — AGENT-SHAPED one-off, stale (urlquery)
23 reports, 2026-02-24 → 2026-10-03.
- **2026-05-13 01:03–01:19: tourism triplet** — `visitgilgitbaltistan.gov.pk`, `tourism.punjab.gov.pk`, `dts.punjab.gov.pk` (16 min)
- `cms.balochistanpolice.gov.pk/client%20scripts/`, `gbpay.gov.pk`, `www.ispr.gov.pk/page-army`, `cfmis.kpst.gov.pk`, `bospnd.balochistan.gov.pk`, `fst.gov.pk` ×2, `www.commerce.gov.pk`, `anfbalochistan.gov.pk/locususa`, `pabalochistan.gov.pk`, `pid.gov.pk/site/press_detail/28138`, `www.nr3c.gov.pk`, `hit.gov.pk`, `lgdsindh.gov.pk`, `rescue.gov.pk`
(urlscan 30d: 1 FP `cons-mofa-gov.pk-hqr-online.site`.)

### gov.bd — HONEST-NEGATIVE (urlquery 19, May–Oct, spread)
`mail.lged.gov.bd`, `web.comillaboard.gov.bd`, `bangladeshpost.gov.bd`, `roc.gov.bd`, `mpemr.gov.bd`, `fima.gov.bd`, `customs.gov.bd`, `smef.gov.bd`, `taxeszonecoxsbazar.gov.bd`, `cafocabinet.gov.bd`, `jgtdsl.gov.bd`, `everify.bdris.gov.bd`, `vat.gov.bd`, `bsec.gov.bd`, `brri.gov.bd`. FP: `apostille-mygovbd.online`.
(urlscan 30d: 0.)

### gov.za — HONEST-NEGATIVE (urlquery 19, Jun–Oct, spread)
`justice.gov.za` (Oct 4), `gems.gov.za` (Oct 3), `webdev.statssa.gov.za`, `www.buffalocity.gov.za`, `www.jics.gov.za`, `sars.gov.za` ×3, `www.education.gov.za`, `cederberg.gov.za`, `okhahlamba.gov.za`, `www.gov.za`, `wmail.dsdmpu.gov.za`, `umzimvubu.gov.za`, `www.dikgatlong.gov.za/view-pdf-document/`. Note: `www.dhet.gov.za/…signature.jpgstyle="width:680px;height:177px` — injection-shaped URL one-off.
(urlscan 30d: 0.)

### gov.ng — AGENT-SHAPED one-off: budget-office cluster (urlquery)
18 reports, 2026-06-25 → 2026-09-18.
- **`budgetoffice.gov.ng` ×4**: Sep 3, Sep 17 13:36, Sep 18 10:30, Sep 18 14:08 — triple in 25h
- `admin.njc.gov.ng` + `njc.gov.ng` (Jul 1/4), `dta.education.gov.ng`, `nogicjqs.gov.ng`, `nhia.gov.ng`, `ncdmb.gov.ng`, `www.osgf.gov.ng`, `publicreg.vaccination.gov.ng`, `pmi.naptin.gov.ng`, `autoconfig.purimatahari.data.napri.gov.ng`
(urlscan 30d: 8 hits, all `-gov.ng` phish lookalikes — FPs.)

### gov.ke — HONEST-NEGATIVE (0 urlquery, 0 urlscan)

### gob.mx (Mexico) — AGENT-SHAPED one-offs (urlquery)
19 reports, 2026-08-10 → 2026-10-04.
- Oct 3–4: `dgis.salud.gob.mx`, `cmas-coatepec.gob.mx`, `merida.gob.mx` — 3 distinct municipalities in 23h
- **2026-08-17: XSS-probe URL** — `a517c6:sbyh0h@www.tlaquepaque.gob.mx/busqueda?s=<script src=//cdn.farolesa.mx/pdf.js></script>?id=1784822841550?b24mpu=gkg417&abht43=das2bl&f34yf0=0r08wx=ege2vl` (basic-auth userinfo + script injection + gibberish params — vulnerability probing)
- `coronavirus.gob.mx` ×2 (Aug 10), `miportal-siaf.seafi.campeche.gob.mx`, `311locatel.cdmx.gob.mx`, `sds.nayarit.gob.mx`, `sedatu.gob.mx`, `tekaxyucatan.gob.mx`, `www.congresojal.gob.mx`, `irct.tamaulipas.gob.mx`, `cuautlancingo.gob.mx`
- FP: `miregistrocivil-actas.com.mx`, `santaluciamiahuatlan2628.gob.mx` (urlscan only, certstream auto-scan), `-gob.mx` phish lookalikes on urlscan
(urlscan 30d: 15 hits — 1 true `santaluciamiahuatlan2628.gob.mx`, rest `siiat-sat-gob.mx`/`mat-sat-gob.mx`/`acta-mi-registrocivil-gob.mx` phish.)

### gov.ae — AGENT-SHAPED one-off clusters (urlquery)
20 reports, 2026-06-07 → 2026-10-04.
- Oct 3/4: `smart.gdrfad.gov.ae` + `researchaward.gdrfad.gov.ae` (20h, same apex — GDRFA Dubai)
- Sep 29 13:36/13:38: `elicense.fanr.gov.ae` + `tahseel.gov.ae` (2 min)
- `eservices.dubaided.gov.ae/rt/<n>.0` ×2 (Jun 7 / Jun 29)
- `uaegovsurveys.gov.ae/ar/surveys/l/xinzxrxr22nw` + `…/showEmail?email=314&token=xinzxrxr22nw` (same minute, tokenized)
- `beta.smartservices.icp.gov.ae/…index.html` ×2, `moi.gov.ae`, `dubaipolice.gov.ae`, `www.dewa.gov.ae`, `atlas.fgic.gov.ae/uaeatlas/Environment/Climate`, `investindubai.gov.ae`, `www.ng.gov.ae`
(urlscan 30d: 1 FP `dubaizpolice.com/gov.ae`.)

### gov.sa — AGENT-SHAPED one-offs: verification-endpoint probing (urlquery)
20 reports, 2026-07-18 → 2026-10-04.
- **Aug 16, same minute: `www.gosi.gov.sa/ar/QuickVerify/ECertificate?Type=4&StakeholderValue=1045617105&CertificateNumber=118115946` ×2** — certificate-verification probe pair
- Aug 17: `proof.address.gov.sa/verifyproofna.aspx?type=i&ID=1061169791&doc=1069396775` — address-proof ID verification
- Sep 17: `haseen.gov.sa` ×2 (25 min); Jul 24: `my.gov.sa` ×2 (same minute)
- `momah.gov.sa` (Oct 4), `moc.gov.sa`, `www.sfda.gov.sa`, `www.citc.gov.sa`, `www.jeddah.gov.sa` (mangled QR param), `www.iam.sa`, `najiz.sa`, `www.pif.gov.sa`, `www.spa.gov.sa`
- FP: `www.services-balady-gov-sa.cc`
(urlscan 30d: 8 hits — 3 true `vision2030.gov.sa` tranco-tagged, rest `sa-m.blog`/`sa-gov.net` phish FPs.)

### gov.tr — HONEST-NEGATIVE (urlquery 20, Aug–Oct)
True: `ktb.gov.tr` ×2 (1 min, Sep 25), `medya.ilan.gov.tr`, `utsuygulama.saglik.gov.tr`, `server02.turkseker.gov.tr`, `ptt.etebligat.gov.tr`. Rest: private news sites. **No translate.goog FPs** (prior lane's caution confirmed unnecessary here). (urlscan 30d: 0.)

### gov.ru — HONEST-NEGATIVE (urlquery + urlscan)
urlquery 20 (May–Oct): true — `duma.gov.ru/duma/persons/1055905/`, `nalog.gov.ru/rn77/`, `ervk.gov.ru`, `belogorskiy.rk.gov.ru`, `sgo.mari-el.gov.ru`; rest are regional news keyword FPs + `minfin-gov.ru` lookalike.
urlscan 30d (136): all `-gov.ru` lookalike/parked noise (`info-sfr-gov.ru` ×~130, `spisanie-dol-gov.ru`, `ustinovaaifoms-gov.ru`, `sud-gov.ru`); one true agent-shaped one-off: `auth.92.gov.ru` ×3 (Sep 22–23) with emoji auto-tags (🎯-92.gov.ru, 🏢-sub-auth, 🤖-urlscan-submit) — single-submitter subdomain inventory bot.

## Notable side-findings (not gov-domain agent scanning, recorded for other lanes)
1. **PH `-gov.ph` phish-kit wave** (urlscan): 643 scans of `*-gov.ph` impersonation domains (dswd/dilg/pco/ncsc/denr/pnp), all → 45.79.222.138, Oct 3–4 dense.
2. **SG LTA phish-kit sweep** (urlscan): programmatic scans of `lta.*.top/gov.sg`, `onemotoring.toller*.top/gov.sg` lookalikes.
3. **MX `-gob.mx` / NG `-gov.ng` / RU `-gov.ru` lookalike noise** — phishing-research surface, not gov scanning.

## Method notes
- urlquery htmx search is keyword-substring: expect FPs (hyphenated lookalikes, redirect-chain matches like `pcragov.com`, `investhk.getproven.com`). All hits above were manually filtered for true `.govTLD` hosts.
- urlscan.io API has a 30-day search window and ~1/10s rate limit; one 403 encountered on a wildcard query (`domain:*.go.id`) — did not retry that form per policy; used quoted-substring queries throughout.
- urlquery htmx chunked reader breaks on large result pages (IncompleteRead); limit ≤20 is reliable.
