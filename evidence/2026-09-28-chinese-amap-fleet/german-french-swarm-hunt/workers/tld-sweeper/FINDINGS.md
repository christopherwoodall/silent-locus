# TLD-SWEEPER — German/French TLD sweep (2026-10-05)

Worker: TLD-SWEEPER · EUROSWARM. Task: extend the foreign-TLD sweep (prior:
.cn, clck.ru, vk.cc, t.ly, s.id — zero foreign-TLD infra for the known
operator) into fresh ground: **.de, .fr, .at, .ch, .be, .lu**. Passive/public
OSINT only; no candidate infrastructure was fetched or probed. Full observed
values throughout; nothing redacted. OBSERVED vs INFERENCE are separated.

Scope: agent/swarm behavior only (burst timing, agent grammar in URLs,
programmatic hosts, non-browser submitters) — NEVER human/operator identity,
registrants, or social attribution.

Sources: urlquery htmx endpoint (curl variant `uq_htmx_curl.py`; the urllib
variant `uq_htmx.py` timed out on this VM's egress — see Endpoints),
urlscan.io anonymous search API (`domain:<tld>`, 30-day window for anonymous
users — results below are ~Sep 5 – Oct 5, 2026 unless stated).

## Method notes
- urlscan `domain:<tld>` is fuzzy: it surfaced scans whose *page* domain
  resolves to the TLD but also off-TLD results (fnn.jp/tbs.co.jp under
  `domain:be`; linguee.com/bergamot.ch under `domain:deepl.com`;
  shop.apothic.com under `domain:be`). Grading used the page/task apex
  domain actually observed, not the query.
- `domain:*.de` (glob) returns 0 — no wildcard support; `domain:de` works.
- Marker check: searched all TLD-bucket URLs and all priority-target URLs
  for `zz=`, `uqscan`, `httpbun`, `webhook`, `oai`, `epoch`, `is.gd`,
  `lhr.life` — **0 hits**. The known operator's markers are absent from the
  entire German/French TLD surface surveyed.

## Per-TLD buckets (urlscan, 100 most recent each)

### .de — INFERENCE: honest negative
100 recent scans, 92 api / 8 automatic. Top apexes: der-miet-mann.de (4),
verivox.de (3), sfrischling.de (3), assorted small German business sites (2
each). Content: SEO/affiliate referral spam redirects (billigerstreamen.de →
verivox.de utm links), small-business site scans, and one recon cluster:

- OBSERVED: `http://cpanel.der-miet-mann.de/` 15:21:02Z,
  `http://der-miet-mann.de/` 15:20:48Z, `http://www.der-miet-mann.de/`
  15:20:33Z, `http://webdisk.der-miet-mann.de/` 15:20:23Z — 4 scans in
  39 seconds, anonymous api submitter, page country FR, cPanel/Apache server.
- INFERENCE: pre-exploitation recon (cpanel/webdisk are admin-host probes).
  Programmatic burst, but no agent grammar, no harness markers, no program
  hosts. Scanner-class behavior; no swarm tells.

### .fr — LEAD (one weak: julesferry88.fr numbered-host enumeration)
100 recent scans. Top apexes: mailin.fr (14), julesferry88.fr (6),
assorted French small sites (2 each).

- mailin.fr (14): OBSERVED — all 14 are spam-tracking subdomains from
  third-party email campaigns (`img.experiencias.cafelacabana.com`,
  `img.mail.etaxnexus.com`, `r.kampag.onlinemarketing.de`,
  `qsbermegamarket.pochtabank.blablacar.admcdek.rhxyvcq9vvts2ld9.r.mail.leankoala.com`,
  `img.mail.curspack.com`, `img.mail.makimpact.fr`, ...), 14:37–15:20Z,
  api, anonymous. INFERENCE: mail-security scanner analyzing phishing/spam
  emails. Honest negative for swarm.
- julesferry88.fr (15 observed after full pull): OBSERVED —
  `http://ps2..ps17.edu.julesferry88.fr/` and `http://wp1..wp15.edu.julesferry88.fr/`
  (samples: ps17 15:19:28Z, ps5 15:01:48Z, ps11 14:50:40Z, ps9 14:48:42Z,
  ps3 14:41:10Z, wp14 14:39:32Z, ps2 14:28:35Z, wp15 14:25:36Z, wp11
  14:22:39Z, wp12 14:04:50Z, ps4 2026-10-03T13:43:48Z, wp3 12:24:01Z, wp1
  07:32:55Z, ps14/ps15 2026-09-12), all api, public, anonymous submitters
  (2 with page country FR). INFERENCE: systematic numbered-host enumeration
  of a French education domain (ps=postes? wp=workplaces?). Structured
  enumeration is the closest to the `/c/NN` agent-shaped pattern in this
  sweep, but cadence is loose (minutes to days apart) and there is no agent
  grammar, no markers. LEAD (weak) — worth a coordinator look, not a track.

### .at — honest negative (phishing-scanner noise)
100 recent scans. Top: landingpage.at (20), adoptamestizos.com (3),
anadibank.com (2), various Austrian small sites.

- landingpage.at (20): OBSERVED — 20 scans 14:43–15:19Z of bizarre
  subdomains, e.g. `http://dev.admin.www.dev.www3660619319497.landingpage.at/`,
  `https://yxwrqpsrmlkjilkjihgfeupdate.987654761032765432status.cottagebank.com156.landingpage.at/`,
  `https://tsrqpojilkjiadhwocbaupdate.98769872565update.9en.v2202508297531378155.powersrv.de/`.
  The "update"/"status"/random-label grammar is phishing-campaign lures,
  submitted to urlscan for analysis. INFERENCE: anti-phishing scanner
  burst, not agent infrastructure. Honest negative for swarm.
- adoptamestizos.com (3): pet-adoption blog pages — researcher browsing.
  Honest negative.

### .ch — honest negative (recon-scanner noise)
100 recent scans. Notable clusters:

- OBSERVED: `http://s3.copytrading.ch/` 15:23:53Z,
  `http://studio.copytrading.ch/` 15:14:44Z,
  `http://playground.copytrading.ch/` 15:01:16Z,
  `http://workspace.copytrading.ch/` 15:00:29Z, plus repeats of the same
  three on 2026-09-12 — api, anonymous, page country US (Cloudflare).
- OBSERVED: `http://faszination-planet.ch/`, `/mail.`,
  `/webmail.`, `/www.` all within 14:17:10–14:17:24Z (14 seconds);
  `http://webmail.nationalolten.ch/`, `/www.`, root within 14:12:09–14:12:44Z
  (35 seconds). Classic mail/webmail/root enumeration quartets.
- INFERENCE: recon scanners sweeping subdomains; the mail/webmail quartet
  is a known scanner fingerprint. No agent grammar, no markers. Honest
  negative for swarm.

### .be — honest negative
100 recent scans. Top: fnn.jp (14), tbs.co.jp (10) — query fuzz (Japanese
news sites, off-TLD); de-beste-datingsite.be (4), extrema.be (3),
tickoweb.be (3).

- fnn.jp/tbs.co.jp: OBSERVED — bursts of news-article URLs
  (`https://www.fnn.jp/articles/-/1127235` etc.; `https://newsdig.tbs.co.jp/articles/-/2991154?display=1`
  re-scanned 14:52:19Z after 14:53:42Z), api, anonymous. INFERENCE: a
  researcher/news-monitoring script submitting articles; not agent-shaped,
  and off-TLD (query artifact). Honest negative.
- tickoweb.be (3): OBSERVED — Dutch event-tenant subdomains
  (`zintuigenwandeling-augustus.tickoweb.be` 13:03:55Z,
  `vleermuizenwandeling-volwassenen.tickoweb.be` 12:34:20Z,
  `vleermuizenwandeling-volwassenen-uitpas.tickoweb.be` 12:15:32Z).
  Ticketing-platform tenant pages, one submitter walking event pages.
  INFERENCE: manual or scripted browsing, no agent tells. Honest negative.
- extrema.be (3): `http://shop.apothic.com/` x3 — off-TLD query artifact.

### .lu — honest negative
100 recent scans (total corpus for domain:lu is 5,633 vs 10,000 cap on
others). Top: roblox.com.bn (5 — query fuzz, scans of `g5.lu` short links),
viesgodistribucion.com (4), kuku.lu (4), blogspot.lu (3).

- OBSERVED: `https://c.kuku.lu/cwwr5bdg` re-scanned 4x in 07:05:52→06:56:35Z
  via api; `https://g5.lu/3fxeb` rescanned 5x across the day (automatic +
  api). INFERENCE: automated re-scan cadence on .lu short links — no
  grammar, no bursts with structure. Honest negative.

## Priority targets (urlscan, agent-relevant German/French services)

- mistral.ai (total 30): OBSERVED — repeated identical re-scans of
  `https://mistral.ai/`: Sep 24 20:18:33Z / 20:20:54Z / 20:23:39Z / 20:25:59Z
  (4x in ~7 min), Sep 25 12:09:39Z / 12:11:38Z / 12:13:45Z / 12:16:48Z (4x in
  ~7 min), Sep 24 02:44:59.662Z + 02:45:00.241Z (0.6s apart — automated
  double-submit). Plus `http://api.mistral.ai/` (Sep 29, Sep 30) and
  `http://security-review-app-v2.mistral.space/` (Sep 28 — note: mistral.space
  is NOT mistral.ai; phishing-impersonation style domain). INFERENCE: uptime/
  QA monitor re-scanning the homepage; no agent grammar, no harness markers.
  Honest negative for swarm. The mistral.space hit is a phishing-relevant
  LEAD outside this sweep's scope — logged, not tracked.
- deepl.com (total 171): OBSERVED — only 3 on-target scans
  (`www.deepl.com/ar/translator` 2026-10-02, an es→en share link, and
  `sl.deepl.com/t/110265/sc/d09218b5-6f02-40d2-ad5b-4c8b9f80d9cb/NB2HI4B2F4XXO53XFZSGKZLQNQXGG3`
  — a user translation-share token). Off-target under the query: bergamot.ch
  x34 (monitoring cadence, multiple/day — uptime checks), linguee.com x4
  (Chinese vocab: 塑料 08:24:09Z, 容器 08:22:54Z on Oct 5; 容器 07:56:40Z,
  玻璃 07:56:22Z on Oct 2 — sequential translation lookups 2 min apart).
  INFERENCE: the linguee Chinese-vocab burst is the only weakly
  agent-flavored pattern here (sequential scripted lookups submitted via
  api) — but equally an auto-submit browser extension on a language
  learner's lookups. LEAD (weak) / likely honest negative.
- qwant.com (total 26): OBSERVED — sparse api scans of homepage and
  `http://api.qwant.com/` (Sep 8, 18, 24, 28, Oct 2). No bursts, no grammar.
  Honest negative.
- startpage.com (total 21): OBSERVED — `https://www.startpage.com/do/search?q=sahibden&segment=startpage.brave`
  submitted 3x (Oct 4 18:12:25Z, Oct 4 20:53:23Z, Oct 5 00:13:31Z), api,
  page country NL. "sahibden" = Turkish "from the owner". INFERENCE: one
  user's repeated search submitted by an auto-scan script; not agent-shaped.
  Honest negative.
- ecosia.org (total 12): OBSERVED — sparse homepage scans plus unrelated
  `.de` hits under the query (alibabaimbiss.de x2). Honest negative.
- api.gouv.fr (total 24) / data.gouv.fr (total 35): OBSERVED — no direct
  hits on the API/portal themselves; query fuzz returned French civic sites
  (cnfpt.fr x6+, guidasso.bzh, stations-services.fr, data.data-wax.fr,
  franceconnect.gouv.fr, pgadmin.pliage-test.socle-ia.data-ia.dev.atlas.fabrique.social.gouv.fr).
  No burst patterns, no agent grammar. Honest negative.

## urlquery htmx TLD leg

Ran 9 htmx queries total (polite pacing: 65s between, curl variant — the
urllib variant `uq_htmx.py` dies in this VM's proxy tunnel): `.de uqscan`
(0), `url.domain:de` (0), `.fr` (30), `.de` (60), `.at` (23), `.ch` (23),
`.be` (59), `.lu` (47). No 429s encountered.

METHOD CAVEAT (important): urlquery's keyword `q` does NOT filter by TLD —
the same report_id appears under multiple query buckets (e.g.
`b07862f0-64ad-45a8-8515-addc1f6f1842` under both `.de` and `.be`;
`571e6df4-1dea-4e31-9986-0392de392d94` under `.de`, `.at`, `.be`), so `q`
matches page text/tags/language beyond the URL. Deduplicating by
report_id: **171 unique reports** across the 5 TLD sweeps. Date stamps also
wobble ±1 min for the same report_id across pages (relative-time rendering),
so treat displayed minutes as approximate.

On-TLD uniques (host actually ends in the TLD): .de 11, .fr 1, .at 1,
.ch 1, .be 2, .lu 0. All mundane: small-business sites
(hayalogistica.de x4 — a logistics firm, `/bzar/` page re-scanned 14:46–15:13Z;
bluefinsupboards.de, aktion-moorschutz.de, 42-marketresearch.de, test.de),
pinterest.de user profiles x2, leboncoi.fr, interseq.at, shsv.ch,
youtu.be/wCWhU59OcNY, ifbd.be (Belgian training institute). No agent
grammar, no bursts, no program hosts.

LEAD — Appwrite deployment burst: OBSERVED — 26 unique `*.appwrite.network`
reports submitted 14:15–15:28Z on 2026-10-05, including
`branch-main-5203b51.appwrite.network` (15:22Z),
`branch-dev-dca64b1.appwrite.network` (15:15Z),
`branch-spec-92-u5-home-81df635-70e2d92.appwrite.network` (15:25Z),
`6ac3c1740a890-routertest.stage.appwrite.network` (+ 3 sibling
`routertest.stage` hosts, 15:23–15:27Z), `hackhub.appwrite.network`
(14:15Z and 15:17Z re-scan), `vb-qc.appwrite.network` /
`vb-qc-me7p.appwrite.network` (re-scanned 15:21Z and 15:28Z),
`my-website-pi1b.appwrite.network` (15:09/15:22/15:24Z),
`6a48588f10b4aef223a7.appwrite.network` and 3 more hex-labeled projects
(15:12Z), `sha-kweyol.appwrite.network`, `pfpzone.appwrite.network`,
`radphrase.appwrite.network` (12:25Z). These matched the TLD keyword
queries via page content (non-.de/.fr hosts). INFERENCE: a single actor
systematically scanning ~26 Appwrite branch/stage deployments in ~75 min —
branch-deployment naming (`branch-main/dev/spec-*`) is Appwrite's
deployment-branch convention, and `routertest.stage` reads as QA.
Appwrite branch deployments are already in our agent-harness history
(ExploitGym: agents ran harnesses against Appwrite console/branch
deployments, May–Sep 2026). No agent grammar or known markers in the URLs;
the hackhub report (public, tags empty) shows a student "Collegiate
Builder Directory" (Next.js + Python/Uvicorn on Azure) — benign content.
Grade: **LEAD (moderate-weak)** — programmatic burst with structure, but
equally consistent with CI-driven deploy verification or a security
researcher sweeping deployments. Needs coordinator judgment; do not track
as a swarm without more.

Elsewhere in the 171 uniques: `documentview-acc.com/?a7923de5/qwer@qwerqwer.com`
(credential-phish lure, re-analyzed — phishing, not swarm),
`sli.emergencyemail.org/click?...WeatherAlerts1022026` (spam click-tracker),
`is.gd` homepage scanned once 14:54Z (surface presence only — the known
operator's shortener, but a homepage scan is not infra), vimeo share-link
bursts, scholia.io repeats (Wikidata scholar profiles — scripted researcher,
off-TLD). Zero known-operator markers (`zz=`, `uqscan`, `httpbun`,
`webhook`, `oai`, `epoch`, `lhr.life`) anywhere in the set.

## Graded findings (summary)

| # | Lead | Grade | Basis |
|---|---|---|---|
| 1 | Appwrite branch/stage deployment burst (urlquery, 26 hosts, 75 min) | LEAD (moderate-weak) | branch-main/dev/spec-* + routertest.stage naming = Appwrite deployment-branch convention; Appwrite is in our agent-harness history (ExploitGym); no agent grammar/markers; could be CI QA |
| 2 | julesferry88.fr numbered-host enumeration (urlscan) | LEAD (weak) | 15 scans of psN/wpN.edu.julesferry88.fr, Oct 3–5; systematic but loose cadence, no grammar/markers |
| 3 | linguee.com Chinese-vocab lookup burst (urlscan, under deepl.com query) | LEAD (weak) | Sequential translation URLs minutes apart; likely auto-submit extension, not agent |
| 4 | security-review-app-v2.mistral.space scan (urlscan) | LEAD (out of scope: phishing) | Impersonation-style domain; logged, not tracked |
| 5 | landingpage.at phishing-subdomain burst (urlscan) | HONEST NEGATIVE | Anti-phishing scanner analyzing lure subdomains |
| 6 | mailin.fr spam-tracking cluster (urlscan) | HONEST NEGATIVE | Mail-security scanner on spam campaigns |
| 7 | der-miet-mann.de / copytrading.ch / faszination-planet.ch / nationalolten.ch recon quartets (urlscan) | HONEST NEGATIVE | Recon scanners (mail/webmail/cpanel probes), no agent tells |
| 8 | fnn.jp / tbs.co.jp news-article bursts (urlscan) | HONEST NEGATIVE | Researcher/news monitoring; off-TLD query artifact |
| 9 | kuku.lu / g5.lu short-link re-scans (urlscan) | HONEST NEGATIVE | Automated re-scan cadence, no structure |
| 10 | mistral.ai / qwant.com / startpage.com / ecosia.org / deepl.com / api.gouv.fr / data.gouv.fr | HONEST NEGATIVE | Re-scan/monitor patterns only; zero markers |
| 11 | urlquery on-TLD uniques (.de 11, .fr/.at/.ch/.be handful, .lu 0) | HONEST NEGATIVE | Small-business sites, profiles, youtu.be link — no agent-shaped activity |

Net: **no CONFIRMED German/French agent-swarm infrastructure found.** The
known operator's markers are absent across all six TLDs on both sources.
The three weak leads (#1–#3) are automation-shaped but marker-free — handed
to the coordinator for judgment, not tracked as swarms.

## Open items
- urlscan anonymous window is 30 days — anything older is invisible to this
  sweep; no-auth limitation stands.
- The Appwrite burst (lead #1) deserves a coordinator call: re-pull
  `appwrite.network` on urlquery in 24h to see if the scanning continues
  (persistent pipeline) or was a one-off QA pass; a second burst with
  `branch-*` naming would strengthen the agent-harness reading.
- urlquery keyword `q` is not a TLD filter — any future TLD sweep must
  dedupe by report_id and filter on the parsed host, as done here.
- `.fr` keyword sample: `etools.mail.education-superieur-recherche-jeunesse-sports.gouv.fr`
  and repeated `scholia.io` (Wikidata scholar profiles, scripted researcher
  pattern) seen but off-TLD/weak — not pursued.

## Undocumented endpoints (for reuse)
- `https://urlquery.net/api/htmx/search/?q=<query>&limit=<n>&offset=<n>` —
  GET, no auth, returns HTML fragments parsed by `uq_htmx.py`/`uq_htmx_curl.py`.
  On this VM use the curl variant: the urllib one dies in the proxy tunnel
  (TimeoutError in `_tunnel`/`_read_status`, ~60s).
- `https://urlscan.io/api/v1/search/?q=<lucene>&size=<n>` — GET, no auth,
  anonymous window ≈ 30 days. `domain:<tld>` works; glob `domain:*.tld`
  returns 0 (unsupported). `domain:` is fuzzy — always verify the apex
  domain of returned scans before grading.
