# HEBREW AGENT HUNTER — FINDINGS

**Date:** 2026-10-05
**Persona:** Hebrew Agent Hunter (foreign-agent hunt: Hebrew/Israeli surfaces)
**Brief:** `BRIEF.md` (this directory)
**Status:** Complete. No confirmed Hebrew-run agent found. One commercial Hebrew AI-agent product mapped; one agent-shaped content farm found out-of-lane.

## Method

1. Verified all three corpora for Hebrew/Israeli markers (gov.il, .il, hebrew, telaviv, jerusalem, israeli, mossad, %D7%9 URL-encoded Hebrew).
2. Live urlquery htmx sweep via `uq_htmx_curl.py` (the urllib variant hit IncompleteRead; curl variant reliable): `url.domain:gov.il`, `url.domain:co.il`, keywords israel / hebrew / jerusalem / tel aviv / israeli. ≤1 req/5s.
3. Pulled full HTTP transactions via the new keyless `/api/htmx/report/{id}/filter/http` endpoint; used `/related/ip` for same-host joins.
4. Identified commercial products via web search.

## Corpus verification results

| Corpus | Hebrew/Israeli markers |
|---|---|
| chinese-amap-fleet (2,141) | **0** — no gov.il, .il, hebrew, telaviv, jerusalem, israeli, mossad |
| openai-agent-traces (589,972) | **0** |
| oai-tag-sweep | **1** — `golan.org.il/radiotv/` (see below) |

## Candidate assessments

### 1. golan.org.il — OURS, honest negative on cluster
- Report `ac21a006-7f0a-4e1c-ad14-02c2f04d86d6`, 2026-07-06. In oai-tag-sweep with `cors-laundering-ops` wrapper label (`wrapper_corsproxy.json`).
- Single plain-URL submission of an Israeli site (Golan regional radio/TV page).
- **Killed as a cluster:** `/related/ip` returned same-target-IP siblings — `tibiahd.com/houses`, `uk-aldi.rooststay.com`, `7-seas-casino-ca.com`, `finework.top`, `globalsafelock.com`, `b1-binance.com.cn`, `yubit-qgwg.com` — all phishing/malware on one shared/bulletproof host. No Israeli campaign; the golan URL is a one-off inside the wrapper. Campaign membership is hunter-asserted, not payload-established.
- Classification: **OURS / KNOWN — negative.**

### 2. bongowiki.appwrite.network — GENUINELY NEW, agent-shaped, out-of-lane
- 4 urlquery scans 2026-10-03 17:12→22:14 UTC (~5h burst). Not in any of our corpora.
- Agent-generated content farm on Appwrite infra (Next.js RSC). Machine slugs: `bangladeshi-nid-dark-web`, `game-of-thrones-director-khalid-ibn-al-walid`, `mr-beast-joins-shark-tank`, `why-saudi-arabia-knocking-israel`, `not-apply-11-admission`, `du-students-launch-tori-school`.
- The "israel" keyword hit it via the `why-saudi-arabia-knocking-israel` slug. Content is Bangladeshi clickbait/AI-slop, including fraud-adjacent (`bangladeshi-nid-dark-web` = national-ID dark-web topic).
- Agent-shaped infrastructure + generation cadence, but **not Hebrew/Israeli** — referred out of lane (evaluator / global-south lanes). Worth a look by whoever owns Appwrite-deployment farms (note: distinct from the known exploit-gym Appwrite console scans).

### 3. koresh.app.lizzyai.com — GENUINELY NEW, commercial Hebrew AI agent (context)
- 3 urlquery scans 2026-10-04 (app, abd, koresh subdomains). Not in our corpora.
- `lizzyai.com` = "Lizzy — the next generation legal AI" (legal professionals; site lists **Hebrew Support** as a feature). Distinct from LizzyAI (lizzy-ai.com, NYC recruiting AI).
- Tenant `koresh` (Hebrew: כורש, "Cyrus") fetches `/locales/he.json` — a Hebrew-language deployment of a commercial legal-AI agent product.
- Classification: **commercial AI-agent product in Hebrew, not rogue activity.** Context note for the lane: lizzyai.com tenant sprawl is a future surface to watch (multi-tenant AI agents with Hebrew locales).

### 4. Negatives (background noise, all assessed)
- **gov.il ×3** (`url.domain:gov.il`): two 2026-07-15 scans of English dept pages 9 min apart + one 2023-12-11 (pre-wave). Full transaction pull on `4ae46dc4`: stock urlquery scanner UA (Firefox/134 — scanner profile, not submitter), normal full-page render incl. Hebrew "Iron Swords" hasbara assets. Researcher noise.
- **api.invoice4u.co.il**: Apiary-hosted API docs for Israeli invoicing API. Researcher scan.
- **medhub-ai.com**: legitimate Tel Aviv health-tech startup (AI cardiology). Site scan, noise.
- **newsru.co.il**: Russian-language Israeli news site scan — RU-IL crossover surface, but just a scan.
- **"israeli" keyword (23 reports)**: news-site scans (BBC, CNN, mintpressnews…), one itongadol email-tracking link. Noise.
- **jmail.world EFTA threads** (followlike.net ref links): the auditor's lane; not pursued here.

## Tradecraft notes for sibling lanes

- **Share with arabic-agent-hunter:** the keyless `/api/htmx/report/{id}/filter/http` + `/related/{ip,asn,domain}` endpoints were the workhorses of this hunt (documented in `~/workspace/skills/urlquery/HTMX_ENDPOINTS.md`). `/related/ip` kills or confirms same-host cluster hypotheses in one call.
- **htmx search misses confirmed again:** keyword `gov.il` returned an empty/errored file while `url.domain:gov.il` returned 3 reports. Every htmx zero is a weak negative.
- **Egress flakiness:** urllib-based `uq_htmx.py` hit IncompleteRead repeatedly; `uq_htmx_curl.py` was reliable. Direct site fetches (koresh.app.lizzyai.com) stalled — product identification done via web search instead.
- **"972" corpus hits are false positives** (timestamps/nonces/ports), not Israeli indicators.

## Open leads

1. lizzyai.com tenant sprawl — enumerate `*.app.lizzyai.com` tenants; Hebrew-locale tenants are commercial, but the multi-tenant pattern is worth inventorying.
2. Appwrite-deployment content farms (bongowiki shape) — agent-generated wiki farms; check for Hebrew/Arabic-language instances.
3. Hebrew URL-encoded path queries (`%D7%90` aleph etc.) against urlquery — untested; keyword search may not index them.

## Evidence grading

- No CONFIRMED agent-shaped Hebrew/Israeli activity found.
- Strongest in-lane finding: commercial Hebrew legal-AI tenant (not rogue).
- Strongest agent-shaped finding: out-of-lane (bongowiki).
- All classifications above are verified against the three corpora; "genuinely new" = absent from all three.

---

## Appendix: all observed/direct URLs

### urlquery reports (direct)
- https://urlquery.net/report/ac21a006-7f0a-4e1c-ad14-02c2f04d86d6 (golan.org.il/radiotv/)
- https://urlquery.net/report/4ae46dc4-96e0-4893-a3a8-311cd81749c4 (gov.il/en/departments/iplan/govil-landing-page)
- https://urlquery.net/report/51f7b107-8ccf-4ba0-af39-29555ad25d12 (bongowiki.appwrite.network)
- https://urlquery.net/report/54da85d0-8e10-40ed-9b4b-5b6ac404b10b (bongowiki.appwrite.network)
- https://urlquery.net/report/b40d0560-92e6-40f3-bca5-22441dc62133 (bongowiki.appwrite.network)
- https://urlquery.net/report/d87c0819-fe27-4f23-afed-3dc5c309ed25 (bongowiki.appwrite.network)
- https://urlquery.net/report/a69ccfbd-d39f-44d1-b88c-5ccbfbcb498a (koresh.app.lizzyai.com)
- https://urlquery.net/report/3dbfeff4-4502-4027-8d1c-65d875d34975 (abd.app.lizzyai.com)
- https://urlquery.net/report/40fad1cc-1f89-4830-9a14-23bdae79ce04 (app.lizzyai.com)
- https://urlquery.net/report/4f371e49-0769-454d-8848-6c1b953bf80f (api.invoice4u.co.il)
- https://urlquery.net/report/8bacea18-4ccc-462e-a03d-e7b0b4c893a7 (medhub-ai.com)
- https://urlquery.net/api/htmx/report/ac21a006-7f0a-4e1c-ad14-02c2f04d86d6/related/ip
- https://urlquery.net/api/htmx/report/4ae46dc4-96e0-4893-a3a8-311cd81749c4/filter/http
- https://urlquery.net/api/htmx/report/51f7b107-8ccf-4ba0-af39-29555ad25d12/filter/http
- https://urlquery.net/api/htmx/report/a69ccfbd-d39f-44d1-b88c-5ccbfbcb498a/filter/http
- https://urlquery.net/api/htmx/report/8bacea18-4ccc-462e-a03d-e7b0b4c893a7/filter/http
- https://urlquery.net/api/htmx/report/4f371e49-0769-454d-8848-6c1b953bf80f/filter/http

### Targets / products observed
- golan.org.il/radiotv/
- gov.il/en/departments/iplan/govil-landing-page
- gov.il/en/departments/ministry_of_construction_and_housing
- bongowiki.appwrite.network/bangladeshi-nid-dark-web
- bongowiki.appwrite.network/game-of-thrones-director-khalid-ibn-al-walid
- bongowiki.appwrite.network/why-saudi-arabia-knocking-israel
- bongowiki.appwrite.network/not-apply-11-admission
- koresh.app.lizzyai.com/locales/he.json
- https://lizzyai.com (Lizzy legal AI — Hebrew Support)
- https://lizzy-ai.com/product (LizzyAI recruiting — different company)
- api.invoice4u.co.il
- www.medhub-ai.com
- newsru.co.il
- r.email.itongadol.com/mk/cl/f/sh/1t6Af4OiGsDg0m9DdHuPH4DRacypwQ/32ixuTwMbdFf
