# FALSE-POSITIVES.md — Hermes hunt-profile scanners

Short words. Each term is defined on first use.

Terms:
- False positive: a hit that looks like fleet activity but is not.
- Fleet: the agent group under watch. Its tradecraft is the set
  of habits it shows: tag grammar, target shapes, relay choices.
- Grade: how the evidence was got. PRIMARY means we saw the
  bytes ourselves. SECONDARY means someone else saw them first.
  A SECONDARY hit is weaker than a PRIMARY hit.
- Confidence: HIGH, MEDIUM, or LOW. It says how strong the hit
  is, not that it is true.

Rule for all scanners: a hit is not proof. A hit is a lead.
Check the hit before you claim fleet activity.

## urlquery

- Tag grammar alone is noise. `uqscan=`, `uqframe=`, `uqtag=`,
  `cachebust=1`, and `uq=` are used by many urlquery users: bots
  that probe urlquery itself, QA scripts, researchers who tag
  their own scans. Tag grammar has weight 1. It can never emit
  alone. It must join an Amap target, a payload, or an exfil
  shape to reach weight 3.
- Amap target alone is noise. Amap and gaode are large Chinese
  map services. Honest researchers scan them for map research
  and anti-bot study. A lone Amap domain hit is normal web
  research.
- httpbin /base64/ alone is noise. httpbin is a standard test
  service. Students, developers, and CTF players use /base64/
  all the time. The fleet shape is the JOIN of program packing
  with tag grammar and Amap targeting, not httpbin alone.
- webhook.site alone is noise. It is the default throwaway
  webhook receiver for the whole internet. Tutorials, CI jobs,
  and exfil research all submit webhook.site URLs. Also: bare
  webhook.site UUID URLs that show a "Token not found" page are
  page views of deleted inboxes, not live dead drops. Score
  them as noise on sight.
- ntfy topic alone is weak. The `amapdata-<POI>-<suffix>` shape
  is specific, but the grammar is now public. A copycat can
  reuse it. Check target-side joins only (the target host or
  target IP of the scanned object, never submitter traits)
  before you attribute a hit to the fleet.
- Labels are claims, not proof. `claude<date>` and `research*`
  labels have weight 0. Honest agents label their runs the same
  way. Never attribute on a label alone.
- Raw API counts lie. A `zz=` search also matches reports
  whose country code is "zz" (unknown country). A bare `ntfy`
  search returns page-content noise. Score only the submitted
  URL, final URL, tags, and title. Never trust the raw count.
- Copycats are real. The full grammar is public in hunt
  writeups. A third party who copies it will emit a hit. The
  hit truly shows the tradecraft, but fleet attribution needs
  more: target-side joins done by hand (target host or target
  IP of the scanned object, never submitter traits).
- A zero run is weak. The fleet may have moved off urlquery.
  "No matching submissions in window" does not mean "fleet
  is dead". The date filter is day-granular and can miss late
  reports. Overlap runs by a few hours for continuity.

## urlscan

- urlscan hits are other people's scan metadata, so they grade
  SECONDARY. A scan record shows that someone asked
  urlscan to scan a URL. It does not show who asked, or why.
  Treat every urlscan hit as SECONDARY. No per-query override
  can ever upgrade third-party metadata to PRIMARY.
- Name collisions are common. "amap" is an acronym and an
  internal name prefix, not always the map service. Examples:
  Azure hostnames with an `amap-` prefix, amapacad.org.ng
  (a marketing group), a Jilin energy platform that uses the
  Amap map SDK in a normal way. Ignore hits with no fleet
  marker.
- Test URLs are noise. httpbun `/mix/` paths, livecodes.io
  demos, and image-bed demos are generic test snippets. The
  fleet uses the `/base64/` program-staging shape. `/mix/` is
  not that shape.
- Search limits cause misses, not negatives. Anonymous search
  covers only the last 30 days. A zero means "no fleet pages
  in the last 30 days of urlscan", not "never". Leading
  wildcards are blocked (403). Full result bodies need a
  login. Anonymous verdicts rest on metadata only: URL, title,
  scan date.
- Domain-presence queries are weak. The six relay and service
  queries (jqp.vercel.app, vanderbi.lt, ntfy.envs.net,
  itty.bitty.site, cors.bwa.workers.dev, pingllo.com) stay
  disabled. A scan of a relay front page is not fleet traffic.
  A scan of a service is not fleet use. Keep only hits that
  also show a fleet marker (tag grammar, getPoiInfo shape,
  dead-drop topic shape). All six carry a LOW cap and
  SECONDARY grade.
- Do not confuse ntfy hosts. ntfy.envs.net is an operator-run
  instance. It is NOT the public ntfy.sh utility. Hits on one
  do not imply hits on the other.
- Triage rule: keep a hit only if it carries a fleet marker
  (getPoiInfo, `uqscan=` / `uqframe=`, hysandbox, fleet POI
  page shape) or a HIGH grade. The rest is routine noise.
- Token note: page URLs can carry tokens (UUIDs, keys in
  query strings). A token is a capability: it can grant access.
  Captures keep full values. Tag token-bearing hits as
  sensitive. Keep them local-only. Do not push them in public
  without the operator's word.

## prcomment

- GitHub search matches PR titles/bodies, NOT comment text.
  The scanner fetches issue comments and PR review comments
  separately and pattern-matches locally. A search hit alone
  is not a comment match. Only a fetched comment body that
  matches a pattern emits.
- A pattern match is text evidence only. It is not proof of
  agent activity. A human can write "I hallucinated" or "I am
  an AI assistant" as a joke, a quote, or a test. A bot can
  write the same words.
- BROAD patterns are weak. Patterns marked BROAD ("as an AI
  language model", "I accidentally merged", "I made this up")
  fire on ordinary speech. HIGH patterns are tighter, but
  still not proof. Grade is SECONDARY, LOW by default.
- Two families beat one pattern. Confidence is MEDIUM only
  when one comment matches two or more distinct families.
  One family alone stays LOW, even with several patterns.
- Author type is context, not proof. A "Bot" author type does
  not prove a model wrote the comment, and a "user" type does
  not prove a human did. Bots can post human text, and humans
  can post through bots.
- Raw captures may incidentally contain author logins. Triage
  must never use them for attribution.
- Scope note: this scanner hunts goofy or unexpected agent
  behavior in comments, not serious harm. Do not upgrade a
  funny admission into a harm claim.

## shodan

- Count churn is the main noise. Shodan re-scans on its own
  schedule. Hosts go dark, IPs change hands, coverage shifts.
  Small deltas (within about 10%) are normal churn. Treat
  them as coverage notes, not findings. Large or sustained
  deltas deserve a look.
- Product strings collide. `product:"Hermes Agent"` fires on
  renamed and localized builds (forks, demos, unrelated
  software that shares a banner string). Past hunts found
  fetched pages that were not panels at all: a landing-page
  farm, a security-company site, a business page.
- A count cannot name hosts. `/shodan/host/search` returns
  empty on the source plan, so this scanner tracks counts
  only. Do not claim "N new panels appeared" with host detail
  you do not have. Host detail needs a follow-up pass.
- Honeypots and research rigs exist. A new banner may be a
  honeypot, a researcher's exposed instance, or a red-team
  range. An open panel is not proof of crime. Counsel must
  clear a host before any deeper collection or any claim.
- Login-gated vs open matters. Most panels are login-gated.
  A count change made of login-gated hosts is less urgent
  than one made of open dashboards. The count query cannot
  tell them apart. A follow-up pass must check each host
  before any claim.
- Triage rule: keep a hit only if the delta is large (over
  10%), sustained across two runs, or tied to an active
  investigation. Small churn is logged, not alerted.

## crtsh

- hy3/hy4 patterns are very noisy. "hy3" and "hy4" are short
  letter-number pairs that collide with many random hostnames.
  Both patterns ship disabled. Even with the Tencent issuer
  or SAN filter, expect manual triage.
- A Tencent cert alone is routine. Tencent issues and uses
  certs all the time. Only a `hysandbox*` SAN form ties a cert
  to the fleet proxy. Grade those HIGH. Grade Tencent-filtered
  hy3/hy4 hits MEDIUM until a sandbox link is shown.
- The known cert never reports. The fleet cert (CN
  `*.hysandbox.tencent-cloud.com`, DigiCert, issued
  2026-08-18) is excluded by serial in config. A new cert
  counts as fleet-linked only with a hysandbox SAN and a
  Tencent or DigiCert-for-Tencent lineage.
- crt.sh lag is real. `entry_timestamp` can trail `not_before`
  by days or weeks. "No new certs in window" means "no new
  crt.sh entries", not "no new certs exist". Absence is weak.
- A 429 abort is a gap, not a clean result. The scanner stops
  on 429. Re-run later. Do not report the run as clean.
- Triage rule: keep a hit only if the SAN list or the filtered
  issuer ties it to Tencent sandbox infrastructure. Bare
  hy3/hy4 matches with no Tencent link are noise and the
  scanner drops them.

## wayback

- Anti-bot telemetry is the main noise. Most captures under
  the Amap SSR host are Alibaba anti-bot endpoints
  (`_____tmd_____/report`, `punishTextFetch`,
  `page/feedback`). The baseline found about 92% of host rows
  were this telemetry. The scanner skips these rows. They show
  that many agent-driven page loads were archived. They do not
  by themselves prove fleet activity.
- A capture proves the crawler saw the URL. It does not prove
  who asked for the save, or that an agent asked. The CDX
  index cannot show save-initiator records through host
  filters. Initiator claims are correlation, not proof.
  Burst timing and parallel-capture shapes are supporting
  signals, not proof.
- Query-cost timeouts are gaps. Broad CDX queries can return
  504 (query too expensive, not a block). A zero after a 504
  means "the query was too expensive", not "no captures".
  The scanner retries with 45-90 s spacing. If a target still
  fails, note the gap. Do not treat it as a clean baseline.
- Tag markers do not live here. `uqscan=` / `uq=` tags appear
  in urlquery submissions, never in archived URLs. Their
  absence is normal.
- Triage rule: keep a hit only if the URL is a fleet target
  shape (POI page, POI API, pre-prod host, hysandbox domain)
  and the capture is inside the watch window.

## iocfeeds

- Third-party pulses are SECONDARY by design. A pulse shows
  that someone else reported an indicator. It does not show
  that the fleet used it, or that the report is right. Grade
  is SECONDARY, confidence capped LOW.
- Old pulses are history, not news. Pulses older than
  max_pulse_age_days (90) are recorded but not emitted. A
  first run must not surface years-old history as "new".
- A pulse on a shared host is weak. Cloud IPs and popular
  domains host many tenants. A pulse that names a cloud IP
  does not attribute that IP to the fleet.
- URLhaus and ThreatFox stay disabled. Both need an abuse.ch
  Auth-Key. Unauthenticated calls return 401. No account is
  created to get a key. A 401 is a disabled feed, not a
  negative result.
- Triage rule: a pulse becomes useful only when it joins an
  independent PRIMARY observation. On its own, it is
  corroboration at best, and a warning at worst.

## intel_slot5

- "New" means new to our inventory, not published today. The
  reader can serve cached content. A post that appears "new"
  may have been published days ago and only just reached our
  inventory.
- A truncated or failed fetch is a gap, not a deletion. The
  scanner keeps the old baseline when a fetch fails, parses
  empty, or looks truncated. Never read a failed fetch as
  "all posts deleted".
- A flood of new slugs is a reshuffle, not N leads. More
  than 8 new slugs at once emits ONE summary hit. Common
  causes: an index redesign, a URL-scheme change, a bulk
  backfill. Check the index shape before you triage the slugs.
- Titles are page text. An author can write any title. A
  title that names a fleet, a tool, or a target is a lead to
  read the post, not proof the post is fleet activity.
- Direct-fetch titles are weaker. The direct HTML fallback
  never seeds a fresh baseline, because its titles are less
  clean than reader titles. A direct-only first run waits for
  a good reader run.

## telegraph

- View creep is not a signal. Views only move up on a public
  page. View counts are context on hits, never a trigger.
  A view drop (Telegraph dedupes views) never alerts.
- One miss is not a deletion. A page must miss twice in a row
  to emit DELETED. One miss can be a flapping API, a transient
  404, or a bad fetch. The baseline is kept on transport and
  API errors.
- An edit hit is LOW. A page edit shows content changed. It
  does not show who changed it, or why. Check the new content
  before you claim fleet activity.
- An oversized page is a gap. Pages over 1 MB skip hash
  comparison for that run. A truncated read would hash
  differently later and fake an edit. The gap is logged, not
  reported as clean.
- Triage rule: read the changed content (edit) or confirm the
  page is truly gone from a second source (deletion) before
  you act on a telegraph hit.
