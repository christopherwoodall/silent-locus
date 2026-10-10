# ARCHIVE-ORACLES — the archive-as-fetch-proxy infrastructure class

TRACKER sub-task, 2026-10-05. Hunt brief: a programmatic auditor routed 12 of 72 urlquery
submissions through cachedview.nl, and `archive.ph/<live-URL>` submissions were found
(archive.today serving LIVE urls — the fetch-proxy grammar in purest form).

## 0. What this class is

An **archive-oracle** is any service an agent queries not for history but for
**content retrieval it can't (or won't) fetch directly**: check cached/indexed version
vs live, bypass 403/WAF/paywall/bot-wall, retrieve dead pages. The tradecraft is
documented in the wild — see §5. The detection grammar: the oracle's URL embeds the
target URL (`oracle/<target>`, `oracle/#<target>`, or query param), so the target is
visible in the submission string itself.

**Collection caveat (this pass):** the VM's egress proxy timed out on ALL direct HTTP
(curl + python urllib) to urlquery.net, api.urlquery.net, cachedview.nl, archive.ph,
urlscan.io, archive.org — even hosts that worked days ago. The browser service
fetched cachedview.nl's homepage once, then timed out on the urlquery htmx endpoint
(after 821s; not retried per instructions) and on cachedview.nl/analytics.js.
So the planned `uq_htmx.py` sweeps (`cachedview`, `archive.ph/http`,
`archive.today/http`) **could not run**. The queries to run when egress works:

- `search --query "cachedview" --limit 100` → expect `https://cachedview.nl/#<urlencoded-target>` submissions
- `search --query "archive.ph/http"` / `"archive.today/http"` / `"archive.md/http"` → expect `/newest/<target>` and `/<ts>/<target>` submissions
- `search --query "ghostarchive.org/archive/"` → `/archive/<ts>/<target>` and `/longurl/<id>`
- `search --query "megalodon.jp"` / `"gyo.tc"` → Japanese fish-print (魚拓) proxy grammar
- urlscan.io: `q=domain:cachedview.nl` and `q=page.url:*archive.ph*` equivalents

All service research below was done via browser search (works) since direct fetch is down.

---

## 1. cachedview.nl — the aggregator at the center of the finding

**What it is:** a Dutch client-side web-archive aggregator ("CachedView"). You enter a
URL; it renders one card per source and deep-links you to each result.

**Sources aggregated (from its live homepage, fetched 2026-10-05):**
1. Wayback Machine (web.archive.org)
2. Archive.today
3. Library of Congress
4. Perma.cc
5. Live Version (+ "Screenshot — Click to request a screenshot of your URL"; screenshot is non-persistent)

Older write-ups (Medium, Apr 2024) also list Google Webcache — dead since Google
retired cache: in early 2024; current homepage no longer shows it.

**Submission grammar (confirmed from three independent sources):**
`https://cachedview.nl/#<urlencoded-target-URL>` — the target rides in the **hash
fragment**. Sources: snippy snippet-manager READMEs (barbuk/snippy, aamodj/snippy,
masterdam79/snippy all ship a `cached url` snippet: `https://cachedview.nl/#{clipboard_urlencode}`).

**Why this is the agent-shaped primitive:** the fragment keeps the whole request
client-side — a program can *generate* the oracle URL with zero API, zero key, zero
POST. Submitting that URL to urlquery (12/72 in the auditor's set) makes urlquery's
browser execute the aggregator and resolve all five archive cards. It is the same
trick as `r.jina.ai/<url>` but multi-oracle.

**Endpoints / surface (partial — page source unobtainable this pass):**
- `GET /#{url}` — client-side router (JS reads `location.hash`, builds card links)
- `/analytics.js` — JS asset flagged in AdGuard filters issue #186489 (`https://cachedview.nl/analytics.js`) — **not fetched** (browser service RECV_TIMEOUT); its contents would reveal whether availability is checked via XHR or pure link-building
- Card link patterns (inferred, standard): `https://web.archive.org/web/*/<target>`, `https://archive.ph/newest/<target>`, LoC and Perma.cc search URLs, live `<target>`, plus a screenshot-request control (backend endpoint unknown — **gap**)
- IP seen in urlquery host summary: 143.178.167.52
- Third-party trust: Firefox "Resurrect Pages (isup edition)" addon lists it as the "Cachew" mirror alongside IA/WebCite/archive.is/Memento/isup.me

**Who else uses it:** snippy users (programmatic URL generation), Resurrect Pages
addon users, SEO/OSINT write-ups. No second *agent swarm* attribution found beyond the
auditor's 12/72.

---

## 2. archive.today family — the fetch-proxy grammar in purest form

archive.today is an on-demand archive (launched 2012, ~700TB by 2021, JS-heavy pages,
paywall-busting reputation). **Mirror domains (all the same service):**
`archive.today` (primary), `archive.ph`, `archive.is` (deprecated for new links),
`archive.li`, `archive.md`, `archive.vn`, `archive.fo`. **So `archive.md` is NOT a
sibling service — it's a mirror.** Spain ordered all seven blocked in Sep 2026
(cyberinsider.com). archive.today also denies Cloudflare-DNS (1.1.1.1) resolvers.

**Fetch-proxy grammar (documented, no key, GET-only):**
- `https://<mirror>/newest/<live-URL>` — redirects to the latest snapshot; for a freshly archived page this is near-live content **without ever touching the target host**
- `https://<mirror>/<YYYYMMDDhhmmss>/<live-URL>` — timestamped replay
- Submit flow: `/submit/` (form + captcha — the one part that resists dumb automation)
- Memento aggregation: archive.today supported the Memento protocol (LANL) from 2013; **the Memento project was disestablished Sep 2025** — timetravel.mementoweb.org aggregation is decaying

**Why agents love it:** `/newest/` needs no account, no JS, no POST; it defeats
paywalls/WAFs by fetching server-side with archive.today's own fetcher (which uses
dedicated accounts for Twitter/GitHub/Reddit login-walled content, per Archiveteam).
Rate-limits aggressively (429) — the skill in §5 tells agents to rotate mirrors.

---

## 3. Sibling services — verdicts

| Service | Aggregator? | Programmatic? | Agent-shaped usage | Verdict |
|---|---|---|---|---|
| **cachedview.nl** | YES (Wayback, archive.today, LoC, Perma.cc, live+screenshot) | hash-fragment GET, no key | 12/72 auditor submissions; snippy snippet | **CONFIRMED oracle** |
| **cachedview.com** | Was (Google+Wayback); now Wayback-only | form GET | none found | legacy, not an aggregator anymore (reg 2014, Cloudflare-fronted) |
| **cached.page** | — | — | none | **no such service found** (only "Cached Pages" 2014 blog tool + cachedpages.com) — negative |
| **startram** | NO | — | none | **negative** — Native Planet Urbit remote-access stack + a maglev space-launch proposal; not archive infra at all |
| **archive.md** | n/a | — | — | **correction:** archive.today mirror, not a sibling |
| **ghostarchive.org** | NO (single on-demand archive, Webrecorder/ReplayWeb.page) | `GET /longurl/<id>`, `/vlongurl/<id>`, `/archive/<ts>/<URL>`, `/varchive/<yt-id>`; noscript replay | none found in this pass | oracle-shaped but not aggregation; YouTube/social specialty |
| **Megalodon (megalodon.jp / gyo.tc)** | NO (single on-demand archive, "魚拓" fish-print) | **prefix grammar**: prepend `gyo.tc/` to any URL | none found in urlquery this pass | Japanese fetch-proxy grammar; anti-bot checkbox since 2024 (per 2026-10-03 research) — agent use would need browser |
| **timetravel.mementoweb.org** | YES (Memento cross-archive) | GET | — | decaying since LANL Memento shutdown Sep 2025 |
| oldweb.today, theglobe.se, cachedpages.com, viewcached.com | partials | — | — | listed as cachedview.com alternatives; not investigated |

---

## 4. The tradecraft pattern — live-vs-archived comparison is TAUGHT, not emergent

Two published agent skills document the pattern explicitly:

**a) `blocked-page-recovery` (thaeroon/hermes-profile-navi, author: "Hermes Agent",
tags: Research/Archives/Wayback/Paywall/WAF/Fallback)** —
https://github.com/thaeroon/hermes-profile-navi/blob/HEAD/skills/web/blocked-page-recovery/SKILL.md
The ladder, cheapest first:
1. Wayback `archive.org/wayback/available?url={URL}` + CDX index (`web.archive.org/cdx/search/cdx?url={URL}&output=json&limit=10`, `id_` raw modifier)
2. **archive.today with mirror rotation**: `for d in archive.ph archive.md archive.li archive.is; do curl -sL "https://$d/newest/{URL}"` — the exact `archive.ph/<live-URL>` grammar from the finding
3. Jina Reader (keyed)
4. API-first pivot
5. Real browser last

It even warns about **fake successes** (200 + plausible body that isn't the page:
Google Cache interstitials, AMP redirect stubs, archive.today 429 pages) and tells
agents to validate bodies, not status codes. This is the archive-oracle doctrine
written down. NOTE for the swarm-forensics lane: repo/skills are Hermes-branded;
TelepathicPug owns the Hermes plugin lane — possible cross-lane lead, not pursued
here (out of tracker scope).

**b) `time-masheen` (mrjessek, mirrored across openclaw/skills, dvcrn/openclaw-skills-marketplace, sky8652-ux/skills)** —
explicit **"Live vs. archived comparison"** recipe:
```bash
scrapling extract get "https://competitor.com/pricing" current.md      # 1. live
curl -s "https://web.archive.org/cdx/search/cdx?url=competitor.com/pricing&output=json&collapse=timestamp:4&fl=timestamp&filter=statuscode:200"  # 2. snapshots
scrapling extract get "https://web.archive.org/web/20230101000000/https://competitor.com/pricing" archive.md  # 3. archived
diff archive.md current.md                                             # 4. diff
```
Use cases named: price changes, content drift, competitive intel. A urlquery
correlate for this pattern: same target submitted **both directly and via an
archive-oracle within minutes** — search urlquery for target domains appearing with
and without the oracle prefix in adjacent timestamps.

Supporting: `galengrimm-code/research-skills` deep-research SKILL bakes Wayback
archaeology into CVE-advisory verification (silent-edit detection); `bowers-illinois-edu/ai_workflow` verify-citations archives every cited URL via Save Page Now.

---

## 5. Endpoint catalog (everything found this pass)

**cachedview.nl**
- `GET https://cachedview.nl/#<urlencoded-URL>` — submission grammar (fragment-routed SPA)
- `GET https://cachedview.nl/analytics.js` — known JS asset, **unfetched (gap)**
- Cards deep-link to: Wayback, archive.today, Library of Congress, Perma.cc, live URL, on-demand screenshot (screenshot backend endpoint **unknown — gap**)

**archive.today family** (mirrors: .today .ph .is .li .md .vn .fo)
- `GET https://<mirror>/newest/<URL>` — fetch-proxy entry point
- `GET https://<mirror>/<timestamp>/<URL>` — replay
- `POST https://<mirror>/submit/` — on-demand archival (captcha-gated)

**Wayback Machine**
- `GET https://archive.org/wayback/available?url=<URL>` — closest-snapshot JSON
- `GET https://web.archive.org/cdx/search/cdx?url=<URL>&output=json&limit=N&filter=statuscode:200&collapse=timestamp:4&fl=timestamp` — snapshot enumeration
- `GET https://web.archive.org/web/<ts>id_/<URL>` — raw archived bytes (no toolbar)
- `GET https://web.archive.org/save/<URL>` — force snapshot

**ghostarchive.org**
- `GET https://ghostarchive.org/longurl/<shortid>` → `https://ghostarchive.org/archive/<ts>/<URL>`
- `GET https://ghostarchive.org/vlongurl/<shortid>` → `/varchive/youtube/<ts>/<videoid>`
- `GET https://ghostarchive.org/archive/1990/<URL>` / `/archive/3000/<URL>` — earliest/latest sentinel timestamps
- `/iarchive/instagram/...` — Instagram archive path

**Megalodon**
- Prefix grammar: `gyo.tc/<URL>` ; canonical `https://megalodon.jp/?url=<URL>` (form + anti-bot checkbox since 2024)

---

## 6. Detection rules for the tracker

1. **Oracle-prefix submissions**: any urlquery/urlscan submission matching
   `cachedview.nl/#`, `archive.<tld>/newest/`, `archive.<tld>/<14-digit-ts>/`,
   `ghostarchive.org/archive/`, `gyo.tc/` — the target URL is embedded; extract and cluster.
2. **Live+archive pairs**: same target submitted directly AND via oracle within a
   tight window (±30 min) = systematic comparison behavior (time-masheen pattern).
3. **Mirror rotation**: hits across archive.ph → .md → .li → .is in sequence for the
   same target = the blocked-page-recovery ladder executing (429 evasion).
4. **New oracle service in programmatic use = swarm scent** (per brief). Watch for
   first-seen oracle domains in auditor-shaped submission bursts.

## 7. Open gaps / follow-ups

- cachedview.nl `/analytics.js` and screenshot-request endpoint: refetch when egress
  or browser service recovers; determines whether availability checks are XHR (richer
  fingerprint) or pure client-side link building.
- The 5 urlquery sweep queries in §0 (blocked this pass by egress failure).
- Megalodon index probe (needs browser, anti-bot) — already queued from 2026-10-03 research.
- ghostarchive.org `/search` endpoint existence unconfirmed.
- Possible cross-lane lead: `thaeroon/hermes-profile-navi` is Hermes-branded
  (TelepathicPug's lane); the blocked-page-recovery skill is the clearest
  in-the-wild specimen of this tradecraft — worth handing to that lane, not
  duplicating here.
