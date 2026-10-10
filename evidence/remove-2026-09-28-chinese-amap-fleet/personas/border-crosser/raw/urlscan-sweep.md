# urlscan.io border-crosser sweep — raw notes
**Persona:** BORDER-CROSSER (urlscan.io multi-country sweep)
**Date:** 2026-10-05 (queries run ~04:40–05:10 UTC)
**Operator:** subagent (depth 2)
**Method note:** Direct VM egress is DEAD (python urllib, curl, and curl --proxy all time out —
even to https://example.com through the hatch-egress-proxy). All queries were run via the
browser text-fetch path against the unauthenticated urlscan.io search API
(`https://urlscan.io/api/v1/search/?q=...`). Unauthenticated search is limited to the
**last 30 days** (`search_date_limit_days: 30` in every response). One wildcard query
(`page.url:*mark=*`) returned HTTP 403 and was dropped without retry.
Result API (`/api/v1/result/<uuid>/`) requires login — analysis is from search-result
fields only (task.url, task.time, task.method, task.tags, page.url, page.ip, page.asn,
page.country, page.title).

## 1. Known-pipeline marker cross-check (does the Chinese `uq` pipeline show on urlscan?)

| Query | total |
|---|---|
| `uqtag` | 0 |
| `uqscan` | 0 |
| `AGEDATA23` | 0 |
| `validation=v` | 0 |
| `domain:vizprod.aihw.gov.au` | 0 |
| `domain:data.idph.state.ia.us` | 0 |
| `page.url:*mark=*` | 403 (blocked, not retried) |
| `task.url:mark` | 311 — all "mark"-in-hostname matches (mark-fisher-oil-trading-fortune.pages.dev, eventservice-mark-z.de, mark-bud.pl, …), zero nonce grammar |
| `x-client-OS=linux` | 0 (text index does not cover page-URL query strings) |
| `msal.js.node` | 0 (same caveat) |

**Verdict: the known `uq` pipeline does NOT appear on urlscan in the visible 30-day window.**
Caveat: the June-2026 AU (AIHW) and IA (IDPH) activity is outside the 30-day window regardless;
only the Sep–Oct amap `uqscan=<word><date>` leg falls inside it, and it shows zero.

## 2. Gov-domain sweeps (non-US / non-CN), `domain:<gov>` size=100

All submissions are `task.method: api` (public) unless noted. `submitter` is `{}` throughout —
no submitter identity to join on. Query-bearing URLs were enumerated per country via
text-find on `?`.

### go.jp — CLEAN (phishing-kit / techsupport-scam noise)
- Burst: ~8 scans of `www.e-tax.nta.go.jp` 2026-10-05 00:16–03:45Z with malformed paths
  (`info_center/)|`, `toiawase/toiawase.htm)|`) → 404. Lookalikes scanned same window:
  `drfapad.com/etax/info/refund`, `rivalcastmed-jp.com/` → both off-domain redirect to real
  e-tax. Reads as phishing-kit QA or researcher re-checking a tax-phish cluster.
- Several `jeed.go.jp` / `jfc.go.jp` scans carry tags `techsupport-scam` (compromised gov
  pages in tech-support scams).
- Query-URLs found: Google-Ads UTM (`utm_source=Google&utm_medium=cpc...`),
  `accounts.google.com` OAuth, `flysafe.ccwu.cc/?_=1790974912477` (jQuery cache-buster,
  epoch-ms → 2026-10-02; Chinese aviation-wx site), `jglobal.jst.go.jp/detail?JGLOBAL_ID=200901094408447014`.
  No nonce-shaped agent grammar.

### gov.br — CLEAN (one compromised host)
- `hom.igeologico.sp.gov.br` serving Indonesian gambling page
  ("LangitQQ: Situs Pkv Games DominoQQ BandarQQ QQ Online Terpercaya"),
  page.country=ID, IP 70.153.161.0 (MICROSOFT-CORP, US). Compromised/seo-poisoned staging host.
- `login.acessocidadao.es.gov.br/?urlRetorno=...&nonce=123123123&state=des456456456` —
  hardcoded demo OIDC nonce, not agent-shaped.
- Other query-URLs: `cohabsp.sp.gov.br/owa/auth/logon.aspx?...` (OWA login),
  `sso.validacao.acesso.gov.br/login?client_id=...&authorization_id=1a1073982b9`.
  No nonce grammar.

### gov.in — CLEAN (one SEO-spam compromise)
- `wb.gov.in/apps-game-cash-withdrawal-online-real-money.html` tagged `aitm, malicious`
  (SEO-spam injection on West Bengal gov).
- Query-URLs: `careerjobportalonline.in/?m=1` (blogger),
  `www.pib.gov.in/PressReleasePage.aspx?PRID=2135728&reg=48&lang=2`,
  `www.indianrail.gov.in/enquiry/StaticPages/StaticEnquiry.jsp?StaticPage=index.html`.
  No nonce grammar.

### gouv.fr — LEAD 1 (agent-shaped, single-country)
- **6 scans of `sondage.apps.education.fr/poll/answer/<16-char-token>?type=MEETING`**,
  Sep 27 → Oct 3 2026, all `method: api`, submitter `{}`, same target IP 51.159.8.37
  (Scaleway), near-identical byte sizes (~6.887MB data, ~2.414MB encoded — same page template):
  | time (UTC) | token | page title |
  |---|---|---|
  | 2026-09-27 09:24:15 | 9qnrohj3mgyLsCuqB | Sondage 2.5.0 \| Rdv parent enseignant début d'année |
  | 2026-09-27 10:52:14 | 4Gsm2BQAyRjJ3dC4A | Sondage 2.5.0 \| RDV évaluations nationales |
  | 2026-09-27 18:27:18 | n3fiGDufNvon7biyH | Sondage 2.5.0 \| Remise des résultat évaluations nationales de votre enfant |
  | 2026-09-28 15:21:24 | faQdQnzdrSBxur3hb | Sondage 2.5.0 \| RDV Évaluations CE1 |
  | 2026-09-28 17:39:20 | tyJtyW7ymWXT9iWZh | Sondage 2.5.0 \| Résultats évaluations nationales |
  | 2026-10-03 08:45:20 | XNqxswr7ag3kTGLi9 | Sondage 2.5.0 \| Rendez-vous restitution des évaluations nationales |
- Steady drip (not burst). Each URL is a distinct real meeting-poll (French Education
  Ministry survey app). Agent-shaped (unique random tokens, API submissions) or a human
  submitting poll links they received. Single-country (FR) — NOT a cross-border join.
- Result page: `https://urlscan.io/result/01a100f0-5bc4-741a-be8c-d48d7998cd25/` (latest).

### gov.za — CLEAN
- Single query-URL: `auth-dev.provshare.health.gov.za/realms/master/protocol/openid-connect/auth?...&nonce=73f9d29e-ccb0-49e5-aa96-ce319c579330&...` — normal
  Keycloak UUID nonce. No agent grammar.

### gov.uk — LEAD 2 (script-shaped submitter stack, single-country)
- Scan `01a109f0-e3c2-71c7-bdc3-484faf4eebfa` (2026-10-05T02:42:31Z, method api):
  task `local-plans-manage-training.planninginspectorate.gov.uk` →
  page `login.microsoftonline.com/5878df98-.../oauth2/v2.0/authorize?...&x-client-SKU=msal.js.node&x-client-VER=6.0.1&x-client-OS=linux&x-client-CPU=x64&...`
- The `msal.js.node` SKU + `x-client-OS=linux` is emitted by **Node.js tooling, not a browser**
  (urlscan's own renderer would be msal.js.browser). The submitter's Node-on-Linux stack
  leaked into the submitted auth URL — script/agent-shaped access to a UK Planning
  Inspectorate training portal. Single instance; no cross-country join found.
- Result page: `https://urlscan.io/result/01a109f0-e3c2-71c7-bdc3-484faf4eebfa/`
- Other query-URLs: normal Entra/Zoho/SSO flows (msal.js.browser = human-like).

### gov.tw — CLEAN
- Query-URLs: `www.mnd.gov.tw/publishiframe.aspx?title=...&types=...` (defence ministry iframe),
  `data.moenv.gov.tw/api/v2/wr_p_35?api_key=af57253c-e838-46da-a1f5-12b43afd75f3`
  (Taiwan EPA open-data API — normal data query). No nonce grammar.

### gov.kr — LOW-VOLUME (5 results; email-tracking link, not agent)
- Near-duplicate pair, 2026-10-01 02:23:03Z and 02:23:23Z (20s apart):
  task `o80xx.r.ag.d.sendibm3.com/mk/cl/f/sh/1t6Af4OiGsEcDi1RCgWkut9vqenYpN/2C3gHo9qQu-j`
  → page `gov.kr/portal/rcvfvrSvc/dtlEx/442000000119` ("서비스 상세 | 보조금24 | 정부24").
  Brevo/Sendinblue click-tracking from an email campaign pointing at the Korean gov portal.
  Not agent nonce grammar.

### gov.sg — CLEAN of nonces; two clusters (phish-monitoring + proxy QA)
- **Phish-kit cluster:** repeated scans of `mail.pcragov.com` / `www.pcragov.com` —
  "Philippines Clearance and Revenue Agency", an IRAS (Singapore tax) clone scam kit
  (property-tax / stamp-duty pages). Scans at 2026-10-04 20:28, 22:01, 2026-10-05 01:33.
  Someone is monitoring this kit.
- **Proxy cluster:** `www-mof-gov-sg.chatcox.com` (07:22), `www-reach-gov-sg.chatcox.com`
  (06:17), `www-scamshield-gov-sg.chatcox.com` (02:44) on 2026-10-04 — all redirect to
  `chatwas.com/https://www.<site>.gov.sg/` (titles "— chatwas"). Same proxy operator's
  subdomain-per-target scheme; scans within ~5h = proxy-service QA or a researcher
  checking it. Single-country (SG).
- Only query-URL: `support-isps.bca.gov.sg/auth/v3/signin?...` (Zendesk). No nonce grammar.

### gov.my — CLEAN (operator staging QA)
- ≥5 repeated scans of `kenderaan.auth-gov.staging.digiheritage.com.my` →
  `auth.sabah.gov.my/if/flow/default-authentication-flow/?client_id=ChVzC1JMkX0F18BTGV9f02fsrqPLW97PxqaeqARp&redirect_uri=...goauthentik...&state=<per-flow random>`
  (authentik SSO for Sabah government; `state` differs per scan = normal per-login OAuth state).
  Staging operator QA-ing their SSO integration, ~Oct 3–4.
- Burst: `mds.gov.my`, `mdht.terengganu.gov.my`, `mdht.gov.my` within 5 min on Oct 3 04:50–04:55 —
  same submitter sweeping Malaysian district-council portals. Programmatic but mundane.
- Query-URL: `www.mybiodtrack.gov.my/index.html?ReturnUrl=%2Ftemplate5%2F`. No nonce grammar.

### gov.th — ZERO results in the 30-day window.

## 3. Cross-country joins: NONE FOUND
- No shared tag/nonce grammar on 3+ countries' gov domains within hours.
- No burst parallelism tied to a shared grammar.
- No exit-IP/ASN shifts mid-campaign detectable — submitters are anonymous (`{}`),
  and target-side ASN variation is just CDN edge rotation (CloudFront/Akamai).

## 4. Open leads (not cross-border)
1. **FR sondage poll tokens** — 6 × `/poll/answer/<16-char>?type=MEETING` on
   sondage.apps.education.fr, Sep 27–Oct 3. Agent-shaped drip; unresolved whether agent
   or human sharing poll links.
2. **UK msal.js.node Entra login** — Node-on-Linux submitter stack leaked in a
   planninginspectorate.gov.uk auth URL (2026-10-05). Script/agent-shaped; single instance.
3. **Not ours but noted:** JP e-tax phishing-kit cluster (drfapad.com, rivalcastmed-jp.com);
   BR `hom.igeologico.sp.gov.br` gambling-page compromise; IN `wb.gov.in` SEO-spam;
   SG pcragov.com IRAS-clone kit; SG chatwas/chatcox gov-mirror proxy service.

## 5. Methodology caveats
- 30-day unauthenticated window: June-2026 AU/IA pipeline legs are unobservable here;
  only the Sep–Oct amap leg is in-window, and it shows zero.
- `task.url`/`page.url` field+wildcard queries can 403 (one occurrence: `page.url:*mark=*`);
  plain-text queries DO return results but do not index URL query strings
  (`x-client-OS=linux`, `msal.js.node` returned 0 despite a visible instance).
- Query-bearing URLs per country were enumerated by text-find on `?` in the search
  response (cheap); full 100-result pages were not read line-by-line.

**Not pushed** (per task instructions).
