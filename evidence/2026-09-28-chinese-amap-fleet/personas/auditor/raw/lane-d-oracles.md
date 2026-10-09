# Lane D — archive-oracle as fetch proxy (2026-10-05 UTC)

**Lane:** detection-workload hunt — actors using web archives as FETCH PROXIES
(checking cached/indexed versions alongside live pages).
**Doctrine:** metadata tells the story; misfits are leads; agents and swarms only.

## TL;DR

Two distinct archive-oracle usage modes exist in the corpus, used by two different
actor shapes:

1. **Wrapped-URL submissions** — `cachedview.nl/#<target>` submitted *to* urlquery's
   scanner. The jmail.world auditor does this (103/872 reports, ~12%, Oct 2–5 2026).
   **Functionally inert**: the `#fragment` never leaves the browser, so urlquery's
   scanner only ever sees cachedview.nl's 232-byte shell page (final URL `cachedview.nl`
   or `about:privatebrowsing`, `resource_available=False`, `times_seen=61`). The
   oracle is consulted in the submitter's mind, not in the scan. Ritual step or
   fragment-routing misunderstanding — the scan checks nothing about the target.
2. **Contacted-host / embedded-oracle** — blackhat SEO tool pages that *link to or
   load* cachedview.nl as a "cached page checker" utility. The SEO indexation swarm's
   `index-boost-tool.blogspot.com` report
   (https://urlquery.net/report/ede7b468-0905-4451-b6d3-2837a2be1a2a) carries
   `cachedview.nl` in its Host Summary (first 2025-12-18, last 2026-06-04,
   143.178.167.52, Nginx 1.29.8, NL) alongside `traffic-exchange.github.io` and
   `backlink-generator-tool.github.io`. Here the oracle works as designed — the
   *user's* browser fetches cached copies.

A fresh urlquery htmx sweep (11 archive terms, all 0 reports — see §5 anomaly) and a
single urlscan query (`domain:cachedview.nl` → 1 hit, `rankfueltool.blogspot.com`,
transaction-level match, likely SEO-tool-shaped) found **no third actor**. Prior
corpus work adds: `archive.ph/is/today` submitted-URL clusters are benign
(Bloomberg paywall-dodge, one IP 185.14.97.131 AS56655, 2026-09-21–24; old one-offs
imgur 2024-10, shilapatra 2025-05); Megalodon and ghostarchive have zero indexed
urlquery submissions.

---

## 1. Actor A — the jmail.world auditor (wrapped-URL mode)

Established in `../cachedview/attribution-jmailworld.md`; lane-D additions:

- **Scale:** 103 of 872 reports (~12%) shaped `cachedview.nl/#https://jmail.world/...?q=...`,
  present from the first hour (Oct 2 15:13 UTC) through Oct 5 04:13+; median spacing
  6 submissions, 20 back-to-back pairs. No correlation with path type or `?q=` payload
  (EFTA threads, hex32 threads, vol-pdf drives, person pages all represented).
- **Cadence note:** longer gaps (7–24 min) in the main loop cluster *after* cachedview
  submissions — the wrapper scans are slow to complete (or time out), dragging the
  timer loop. Consistent with a ~3-min timer-fired loop with completion overrun.
- **Archive-vs-direct split:** ~12% wrapped / ~88% direct. The wrapped slice is not a
  separate phase — it's interleaved from hour one, i.e. a standing "consult the
  oracle" step, not an escalation.
- **What the scans actually captured:** nothing about jmail.world. urlquery fetched
  the cachedview.nl shell (232-byte DOM). `times_seen=61` across the 103 reports
  suggests heavy dedup/caching of the identical shell.
- **Verdict on purpose:** intended as a **live-vs-cached cross-check** in a
  redirector-farm audit — compare the live jmail.world page (possibly compromised to
  inject affiliate-kit `?q=` redirects: followlike/livetraffic/2pink with affiliate
  IDs 19384926, 119334) against its archived copy; divergence = tamper evidence.
  As executed, the check is **void** — the auditor never sees the comparison because
  the fragment is client-side-only. Either the submitter misunderstands hash routing
  (believes submitting the proxy URL archives/checks the target — a very
  human-scripter mistake), or the step is ritual "due diligence" theater. Either
  way the *intent* reveals the mental model: archive = independent fetch oracle.
- **Programmatic, certain** (64 h at ~1/3 min, uniform-random payload choice,
  pre-scraped URL list). Human-script most likely (~2:1); agent possible, not
  indicated — the cachedview misuse leans human (an agent that read its own scan
  results would notice 103 identical 232-byte shells).

## 2. Actor B — the SEO indexation swarm (embedded-oracle mode)

From `../mimic/raw/other-operators.md` B-2/B-4, re-verified live for this lane
(report page fetched 2026-10-05, Host Summary confirms):

- **Who:** blackhat-SEO indexation-verification operation, Jan→Sep 2026, 11+ spam
  domains (`index-boost-tool.blogspot.com`, `traffic-exchange.github.io`,
  `backlink-generator-tool.github.io`, …), rotating Google country domains
  (.co.nz/.ca/.im/.ru/.es), `udm=50` (Google AI Mode) oracle grammar.
- **Archive usage:** cachedview.nl appears as a *contacted host* in the tool pages'
  scan traffic (2.3 kB sent / 2.4 kB received — a link/check, not a wrap). The SEO
  tools embed "check cached page" functionality; the operator's *users* (or the
  operator QA-ing the tool) drive the oracle client-side. This is the effective,
  working form of archive-as-oracle: Google's/Bing's cached copy as a ranking/indexation
  witness.
- **Link to Actor A:** shared submission batches + shared cachedview.nl usage lean
  same-operator-family (operator's second business: indexation checks alongside the
  jmail redirector audit). Kept as family marker, not proof.
- **Cadence:** months-long, intermittent batches (not metronomic) — human-operated
  campaign shape, distinct from Actor A's timer loop.

## 3. Sibling archive-aggregator services (enumeration)

How each works, whether it has a public API/logs, and whether anyone uses it as a proxy:

| Service | Mechanics | Public API / logs? | Proxy usage seen? |
|---|---|---|---|
| **cachedview.nl** | Multi-source oracle: Wayback, archive.today, Library of Congress, Perma.cc, **live version**, live screenshot. Hash-routed (`/#<url>`). | No public API; no public query log. | **Yes** — both modes above. |
| **cachedview.com** | Dead redirector: `redirect.php?url=` 302s to google.com. Google Cache discontinued 2024. | n/a | No — dead end by construction. |
| **archive.today mirrors** (archive.ph/.md/.li/.is/.fo/.vn) | Same service, domain rotation to dodge ISP blocks. On-demand JS-capable archiving; records live page + screenshot. | **Yes**: URL-only index at `archive.ph/<query>` (bare host / `*.host` / exact / prefix); Memento TimeMap per mirror. No key. CAPTCHA-walled under load. | Submitted-URL clusters only benign (paywall-dodge). Index itself is a public log of *what got archived*. |
| **Wayback Machine** (web.archive.org) | Crawl + on-demand (Save Page Now) archive. | **Yes**: CDX API (keyless; mid-URL wildcards find relay-wrapped captures, e.g. `r.jina.ai/http*://host*`), `archive.org/wayback/available` API, timemap/timemap/link endpoints. The CDX index is the public log. | Method proven in `collections/.../archive-angles.md`; incident-window probes negative. |
| **Memento Time Travel** (timetravel.mementoweb.org) | LANL cross-archive aggregator (TimeGate/TimeMap). | **Discontinued 2015–2025** (LANL forced migration; per mementoweb.org). From this VM: DNS resolves, TCP 80/443 fails. | No — service down. |
| **MemGator** | Self-deployable open-source Memento aggregator (CLI or service; user picks which archives to query). | Local tool, no central log. | None observed; deployable by anyone. |
| **Megalodon** (megalodon.jp, `gyo.tc` prefix) | Japanese on-demand archive since 2005; checks Google cache + Mementos too. Anti-bot checkbox since 2024. | Public per-URL index via `gyo.tc/<url>`; no bulk API. | Zero urlquery submissions. |
| **Ghost Archive** (ghostarchive.org) | On-demand archiving, ReplayWeb.page replay; raw WARC download at `/chimurai4/<id>.warc`; substring search. | Search UI is curl-accessible; no key. | Zero urlquery submissions; holdings lack our targets. |
| **oldweb.today** | Emulated vintage browsers pointed at archives or live web. | Interactive only. | Not a fetch proxy — replay environment. |
| **Arquivo.pt** | Portuguese web archive. | **Yes**: keyless API, JSONL. | Wrapped-URL probes: genuine zeros. |
| **cachedpages.com / cachedpage.co** | Multi-source cache checkers (listed as cachedview alternatives). | Unknown. | None observed. |
| **dessant/web-archives extension** | Client-side aggregator: 10+ sources (Wayback, Bing/Yandex/Baidu/Sogou/Qihoo/Naver/Yahoo-JP caches, Archive.is, Memento, WebCite, Megalodon). | n/a (browser ext). | The *template* for agent-side oracle use — one click, all sources. |
| **hermes blocked-page-recovery ladder** | Agent skill codifying archives as fetch proxies: Wayback `available` API → archive.today mirror rotation (ph→md→li→is) → Jina → API pivot → browser. | n/a (skill doc). | **This is the tradecraft written down**: archives are rung 1–2 of the agent fetch ladder. |

**Public-logs summary:** the archives that matter for detection all keep public,
keyless queryable logs of *what was captured* (CDX, archive.today index, ghostarchive
search, Arquivo.pt) — the log *is* the index. None keep public logs of *who asked*.
The who-asked side is visible only second-hand, in urlquery/urlscan reports whose
submitted URL wraps the oracle or whose traffic contacts it — exactly the surface
this lane mines.

## 4. Tradecraft characterization — what live-vs-cached comparison buys an auditor

1. **Cloaking detection (the sharpest use).** Phishing kits fingerprint the visitor
   (scanner ASN/IP, headless UA, datacenter egress) and serve benign content to
   scanners, malicious to victims. The archived copy was fetched by the *archive's*
   crawler at an earlier time, from different egress, with a different signature —
   it may hold the malicious variant. **Live ≠ cached ⇒ cloaking evidence.**
2. **Compromise detection on legitimate high-traffic sites.** Compare the live DOM
   against the last-known-good cached copy; injected affiliate links, redirector
   scripts, or SEO spam present live but absent in cache = tamper evidence with a
   timestamp bound (snapshot date ⇒ earliest injection window). This is Actor A's
   apparent intent on jmail.world (450M-visit Epstein-files archive; `?q=` affiliate
   payloads).
3. **Egress laundering / block bypass.** The archive's servers fetch the target, not
   you — target-side WAF/rate-limits keyed on scanner IPs never fire. (Distinct from
   but adjacent to the jina/translate/allorigins relay family already on the
   infrastructure watchlist.)
4. **Dead-page retrieval / evidence preservation.** Target took down the malicious
   page; the archive still serves it. archive.today's on-demand + screenshot model
   is built for this.
5. **Third-party timestamped provenance.** Submitting the *wrapped* URL to
   urlquery/urlscan makes the sandbox's fetch a public, timestamped, third-party
   record of page state — a detection workload with built-in chain of custody.
6. **Change-point timing.** Snapshot dates bound *when* content changed, useful for
   backdating injections.

**Why Actor A's execution fails:** all six benefits require the oracle to actually
fetch the target. A `#fragment` wrapper submitted to a scanner never triggers a
target fetch — the scanner loads the aggregator shell and stops (232-byte DOM, no
archive API calls observed). The tradecraft is sound; the implementation is void.
Notable asymmetry: the *intent* (cross-check live vs cached for tamper evidence) is
exactly right for a redirector-farm audit — the auditor knows what the oracle is
*for*, just not how URL fragments work.

## 5. Method notes, anomalies, gaps

- **urlquery htmx sweep (2026-10-05 ~04:28–04:40 UTC):** 11 queries
  (`cachedview.nl`, `archive.ph`, `web.archive.org`, `cachedview.com`, `archive.md`,
  `cached.page`, `archive.li`, `wayback`, `archive.today`, `archive.is`, `cachedview`)
  — **all returned 0 reports**, ≥6 s pacing, completed cleanly (results in
  `/tmp/laned/uq_results.json`, ephemeral).
- **ANOMALY (lead, not negative):** the htmx `q` keyword search returned 0 for
  `cachedview.nl` while the same index demonstrably contains ≥103
  `cachedview.nl/#https://jmail.world/...` reports (Oct 2–5, pulled via `jmail.world`
  history search). Hypotheses: (a) the search index does not match on URL fragments
  (`#...` stripped before indexing); (b) recent-report indexing lag; (c) `#`/`:`
  handling in the query parser. The 0-counts above are therefore **not clean
  negatives** — recommend parent re-test whether htmx `q` matches fragments at all
  (e.g. search a distinctive fragment token like `19384926` crossed with
  `cachedview`), and treat "no other archive-proxy actors" as *unproven*, not ruled out.
- **Retry round** (04:59–05:03 UTC, 4 queries × up to 4 attempts, 150 s timeouts):
  **all attempts failed** — proxy CONNECT timeouts on both htmx and authenticated
  API endpoints. Egress to urlquery.net was up 04:28–04:40 (the clean sweep) and
  down from ~04:45 onward. No retry output file produced.
- **urlscan.io:** direct curl from this VM times out (egress); one query succeeded via
  fetch (`domain:cachedview.nl` → 1 result, `rankfueltool.blogspot.com`,
  2026-09-14, transaction-level match — SEO-tool-shaped, consistent with Actor B's
  milieu). A follow-up wildcard `page.url:*cachedview*` query was **blocked with
  HTTP 403** by the fetch layer; per policy not retried through other endpoints.
  urlscan's 30-day search window limits retrospective coverage — **gap: no urlscan
  sweep of `archive.ph`-wrapped or `cachedview.nl/#` submitted URLs**.
- **Scope held:** agents and swarms only; no human/operator identity work. No pushes
  made (working tree untouched except this file).

## 6. Watch items for parent

1. **Fragment-indexing test** on urlquery htmx (`q` vs `#fragment` content) — decides
   whether the 11-query zero sweep means anything.
2. **Standing watch:** `cachedview.nl` as submitted-URL host and as contacted host;
   if Actor A's loop is still running past 04:13 UTC Oct 5, the wrapped share (~12%)
   is the canary for whether the operator ever notices the scans are void.
3. **`archive.ph/<query>` index** for our incident hosts (partially CAPTCHA-blocked;
   needs browser or cooldown) — the archive's own log may hold captures the
   scanners never saw.
4. **Wayback CDX wrapped-URL method** (`url=<wrapper>/http*://<target>*`) extends
   cheaply to cachedview.nl-wrapped and archive.today-wrapped captures — a way to
   find *effective* oracle uses (someone actually viewing a target through the
   aggregator leaves a capture trail).
5. The hermes **blocked-page-recovery ladder** (Wayback → archive.today mirrors →
   Jina) is the clearest written statement of archive-as-fetch-proxy agent
   tradecraft found so far — worth cross-referencing against any future
   archive-wrapping submitter's other tooling.
