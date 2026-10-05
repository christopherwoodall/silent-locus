# TARGET-CLASS HUNT — health data portals
Date: 2026-10-04 (Sun), ~23:30 CDT
Analyst: subagent (cartographer lane, parent orchestrator)

## Objective
Find NEW agent swarms by TARGET pattern: systematic scanning of health-data portals
(Tableau/PowerBI dashboards, CDC WONDER, HHS, NHS, state health depts, hospital
provider directories). The known operator hit Iowa IDPH Tableau asthma data
(48-report burst) and AIHW Tableau (viz.aihw.gov.au PBS dashboard CSV pulls,
June 2026, via cf-cors proxies + r.jina.ai bridges).

EXCLUSIONS (known operator — note and move on):
- iowa.gov / IDPH
- aihw.gov.au / viz.aihw.gov.au
- any report URL carrying uqscan= / uqtag= / uqvnc= params

Signal bar: bursts in tight windows, geographic iteration (county-by-county),
per-request tag/nonce grammars. Single scans = noise.

## Method
Primary: urlquery keyless htmx endpoint via
`python3 ~/workspace/skills/urlquery/bin/uq_htmx.py search --query QUERY --limit N`
(polite: >=5s between requests; intra-call --delay 5).
Secondary: urlscan.io public search API.

## INFRA STATUS (2026-10-04 ~23:35 CDT)
- VM egress DOWN: hatch-egress-proxy ([fd8b:4f84:7d32:99::1]:3128) accepts TCP
  and sends Proxy-Authorization, but CONNECT tunnels hang with no response;
  plain HTTP GET via proxy also times out. DNS rewrites to 198.18.241.58-60;
  direct --noproxy connections refused. Affects ALL VM egress (curl, urllib).
- uq_htmx.py fails with urllib TimeoutError (no proxy support in urllib anyway).
- browser.search (runtime channel) works. browser.open works for SOME targets:
  urlscan.io API JSON fetch OK (one query returned); urlquery.net/search fetch
  FAILED (browser-service worker timeout 821s — do not retry that request);
  urlscan wildcard query `page.url:*tableau*` -> 403 upstream (WAF) — do not
  retry index fetches via browser tools per stop instruction.
- Background proxy-retry loop running (/tmp/proxy_retry.sh, proc_9d41f69cd8fa):
  tests every 4 min x24 (~96 min). If egress recovers, run sweep script below.

## Sweep script
/tmp/health_sweep.sh — resilient runner: waits for egress (probes htmx endpoint),
14 queries via /tmp/uq_curl.py (curl-based htmx mirror built by a sibling lane —
urllib chokes on the proxy env), per-query 3x retry w/ 60s backoff, saves JSON to
.../cartographer/raw/health-portals-json/<n>_<name>.json, 6s between calls,
4s intra-call. STATUS: launched background 2026-10-04 ~23:55 CDT
(session proc pending). Analysis: /tmp/health_analyze.py (burst shapes, exclusions).

Queries planned:
1. tableau health department (50)
2. tableau asthma (40)
3. department of health tableau (40)
4. wonder.cdc.gov (50)
5. data.cdc.gov (40)
6. healthdata.gov (40)
7. powerbi health (40)
8. app.powerbi.com health department (40)
9. nhs.uk data (40)
10. digital.nhs.uk (40)
11. provider directory (40)
12. hospital compare (30)
13. public health dashboard (40)
14. county health data (40)

## Results — sweep completed 2026-10-05 ~00:30 CDT
Sweep runner: raw/run_health_sweep.py via curl-based htmx client
(~/workspace/skills/urlquery/bin/uq_htmx_curl.py — urllib hangs on the egress
proxy; drop-in replacement for uq_htmx.py, durable in the skill bin).
14 queries, >=5s pacing, 8s between queries, 3x retry: **14/14 OK, 0 failed**.
Raw JSON: raw/health-portals-json/<n>_<name>.json.
Full URL list: raw/health-portals-urls.txt (195 reports).
Analyzer: raw/analyze_health_sweep.py.

Note on keyword noise: several queries return keyword-matched noise (URL text
does not contain the terms) — treated as single-scan noise unless the host
itself is a health portal.

### Per-query verdicts
1. `tableau health department` (9, 2024-06-09..2026-09-24): NOISE. No Tableau
   hosts at all — nuclei-template zips, blogspot, doge.gov, existbi.com,
   databox.com, etc. No bursts beyond 3 loosely keyword-matched scans in one
   day (2025-03-16). No signal.
2. `tableau asthma` (12, 2026-06-14..2026-06-20): **KNOWN OPERATOR — EXCLUDED**.
   All 12 are data.idph.state.ia.us (Iowa DPH) Tableau AsthmaEDVisits views with
   :showVizHome=no, Year/County params iterated (Dubuque, Scott; 2018/2019),
   plus epoch-nonce cache-busters (&x=1781525037921362330,
   &fresh=1781523595865294039) — matches the known Iowa IDPH asthma footprint.
   Exclusion substring gap noted: host is data.idph.state.ia.us, not "iowa.gov";
   any substring filter for the operator should match `idph`/`state.ia.us` too.
   Example: 38f7c8b7-5715-4eac-b038-d3e5b3e3c4f2 (2026-06-20, County=Dubuque).
3. `department of health tableau` (9): same 9 noise reports as query 1 — NOISE.
4. `wonder.cdc.gov` (3, 2026-10-02 17:09..18:02): **CANDIDATE C1 — WONDER via
   GET→POST bridge**. 2 reports, ~45 min apart, both
   joliss.github.io/get2post/redirect#https://wonder.cdc.gov/controller/
   datarequest/D158?stage=request (17:09) and stage=about (17:51). get2post is
   the public GET-to-POST conversion tool — same bridge family as the known
   operator's cf-cors/r.jina.ai bridges, and WONDER is POST-form-driven, so an
   agent pulling D158 through a GET→POST bridge fits programmatic tradecraft.
   3rd report (brewpage.app/public/IfTo4Wix4i, 18:02) is unrelated noise.
   Evidence grade: medium-low (only 2 scans, but bridge+same-dataset+45min
   window is agent-shaped). Report IDs: 01db827f-6715-4d2a-84e4-3b71442ee761,
   4ef8b36a-f81f-4e4d-b4fd-49a7fb0ef851.
5. `data.cdc.gov` (1, 2024-08-13): NOISE. Single www.covid.gov scan.
6. `healthdata.gov` (2, 2026-04-04, 2026-05-20): NOISE. Two single scans
   (homepage, NADAC dataset). No burst.
7. `powerbi health` (16, 2025-06-06..2026-09-11): **CANDIDATE C2 — PowerBI
   tenant burst**. 4 app.powerbi.com published-report URLs in a 2-min window
   (2025-06-10 16:53–16:55), all sharing tenant ctid=1bbe1eec-c2c3-476e-8d29-
   52ba29c25d60 with distinct report GUIDs (f3c8ef4d, 99402ed6, 6592eed9,
   d8f219b4-apps view) — consistent with a crawler/agent enumerating one
   workspace's published reports. A 5th app.powerbi.com (view?r=eyJr...) is a
   lone 2026-02-18 scan. Rest of the window is keyword noise (mavenanalytics,
   luthmannfirm, hcm660.com...). Evidence grade: low-medium (small, 2025-06,
   no recurrence in later scans). Report IDs: 1b5684f1-75a1-4e3c-860f-
   521863fc7064, 1cf1cc15-0bc5-4123-aa69-d3691ca32541, 74166595-7dfc-4f63-
   9ed2-593ca4321815, bb44badb-84ec-4846-b457-9d70162ecf07.
8. `app.powerbi.com health department` (3): WATCH. 2 health.vic.gov.au
   (Victoria Dept of Health, AU) scans 3 days apart (2026-10-01, 2026-10-04);
   no burst, no grammar. Low — AU angle echoes AIHW but too thin to call.
9. `nhs.uk data` (40, 2025-09-26..2026-08-03): NOISE per signal bar. 40 distinct
   NHS GP-practice domains, one scan each, spread over ~11 months. Diffuse,
   no tight burst, no per-request grammar, no geographic iteration within a
   window — looks like background web-crawling/SEO scanning of nhs.uk sites,
   not a targeted health-data swarm.
10. `digital.nhs.uk` (6, 2024-06-28..2026-09-21): **CANDIDATE C3 — stop-smoking
    micro-burst**. 3 reports in 7 min on 2026-08-12: stop-smoking-services
    collection page x2 + its publication (april-2025-to-december-2025-q3).
    Single-topic crawl, tiny. Evidence grade: low (could be an agent or a
    human researcher; no grammar, no recurrence). Report IDs:
    9a5e927f-0dbe-48b7-8abe-2c660301e0a1, da95cef5-f45f-4bc4-b220-8c8ff6b07baa,
    76c0429f-c00f-45e3-b1fe-a8ebab995caa.
11. `provider directory` (35, 2026-09-27..2026-10-04): NOISE. Keyword junk —
    linkedin profiles, google.com/goto redirects, random corporate sites.
    "Bursts" are ingestion-window artifacts of noise, not target iteration.
12. `hospital compare` (19, 2026-06-04..2026-09-11): NOISE. Keyword junk
    (panchit.com blogs, marketing links, firstsolar.com.vn...). No CMS Hospital
    Compare hosts.
13. `public health dashboard` (19, 2026-07-25..2026-10-04): NOISE. lovable.app
    previews, ramp.com tickets, ziphq vendor profiles. No dashboard hosts.
14. `county health data` (21, 2026-06-01..2026-10-04): NOISE. One genuine
    county hit (co.ramsey.mn.us, single scan) plus news/marketing junk. No
    county-by-county iteration.

### Exclusion hits this sweep
- Iowa IDPH Tableau asthma (query 2): 12 reports, excluded as known operator
  (see verdict 2). Exclusion-pattern gap: filters should cover
  `idph` / `state.ia.us`, not just `iowa.gov`.
- aihw.gov.au / viz.aihw.gov.au: zero hits in any query.
- uqscan=/uqtag=/uqvnc= params: zero hits.

### Candidate clusters (new, non-operator)
- **C1 WONDER-get2post** (medium-low): joliss.github.io/get2post bridge to
  wonder.cdc.gov D158, 2 scans 45 min apart, 2026-10-02. Bridge tradecraft
  matches agent profile. Needs more depth (offset paging on
  `wonder.cdc.gov` / `get2post`).
- **C2 PowerBI tenant 1bbe1eec** (low-medium): 4 distinct published reports,
  one tenant, 2 min, 2025-06-10. Needs depth (search `app.powerbi.com` for the
  ctid).
- **C3 digital.nhs.uk stop-smoking** (low): 3 scans, 7 min, 2026-08-12.
- Prior own-pass hits (dshs-tableau-prd-831217639.us-gov-west-1.elb.
  amazonaws.com x2, apprenticeship.gov, waternz.org.nz) did NOT recur in this
  sweep — no follow-up signal.

### Cluster-check results
- Query 2 re-verifies the known operator's Iowa IDPH asthma footprint is still
  the only systematic health-portal Tableau swarm in urlquery's index for these
  terms. No NEW Tableau swarm found.
- No CDC, NHS, PowerBI swarm at scale. NHS UK scans are diffuse background
  crawling (40 domains / 11 months), not a swarm.

## urlscan.io probe (via browser.open, 2026-10-04)
- `domain:tableau.com` size=5 -> 200, total=558 (30d window), but returned rows
  were stcroixhospice.haystack.so scans every ~3h (2026-10-04 14:16 -> 2026-10-05
  02:16 UTC) — likely loose matching, not tableau-targeted. No health signal.
- `page.url:*tableau*` -> 403 (WAF on wildcard). Lane closed per stop rule.

## Local context (already-known, excluded)
- collusion-wiki oai-tag-sweep (2026-10-01): 409 hits for tableau/powerbi/cdc/nhs
  terms — all the known operator's AIHW Tableau PBS-dashboard CSV extraction
  (viz.aihw.gov.au/t/Public/views/.../PBSDashboard.csv?:showVizHome=no via
  cf-cors.findme-19.workers.dev and r.jina.ai bridges), Jun 17-19 2026.
  Pattern template for what a NEW swarm looks like: Tableau .csv export URLs
  with :showVizHome=no, driven through CORS proxies.
