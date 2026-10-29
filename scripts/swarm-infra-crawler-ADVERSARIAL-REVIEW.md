# Adversarial Review — Swarm Infrastructure Crawler (creator-IP method)

**Reviewer role:** adversarial counsel. **Date:** 2026-10-14.
**Scope:** `swarm-infra-crawler.py` (v2), `ip_classifier.py`,
`swarm-infra-config.json`, `swarm-infra-watch-README.md`,
`swarm-infra-watch-CRON-PROPOSAL.md`.

**Bottom line up front:** The code reads the right endpoint and does not
confuse creator IPs with poster IPs — that part is clean. But the
*attribution chain* built on top of it rests on three load-bearing
assumptions that are asserted, not proven: (1) the `ip` field means
"creator IP" (one undocumented observation; the kill-shot control was
never run), (2) tier-1/2 classifications mean "swarm" (SECONDARY report
IPs, an *inferred* /16, and report-fitted ASN flags), and (3) the watch
can actually see a resurgence (it only fires if the fleet repeats the
exact opsec failure, on webhook.site, captured by urlquery, living longer
than the poll gap). No fatal flaw in the extraction code path. Several
HIGH issues that would corrupt the evidence base if left in. Ship this as
a tripwire for repeat opsec failure, not as attribution infrastructure.

---

## A. The extraction method — is `ip` really the creator IP?

### A1. The verification is a single undocumented observation — HIGH

**Description.** The entire creator-IP interpretation rests on "verified
2026-10-14 via test token." No file records the procedure: what the test
token's UUID was, what IP created it, what IP read it back, the raw JSON,
or timestamps. If creation and read-back shared one egress IP (the
likely case on this VM), the observation is consistent with *both*
"creator IP" and "last-accessor IP" / "last-viewer IP." The control that
kills the alternative hypothesis — create from IP-A, read from IP-B, and
confirm the field still says A — was never run, or never recorded.

**Evidence.**
- `extract_creator()` docstring and `provenance.extraction_verified`
  both cite "2026-10-14 via test token" with no pointer to a procedure
  note, raw capture, or UUID.
- Counter-evidence *for* the creator reading exists but is second-hand:
  the open-source webhook.site codebase (per DeepWiki docs of
  `webhooksite/webhook.site`) models the Token entity with `ip` =
  "IP address of the creator" and `user_agent` = "User agent of the
  creator's browser," while per-request IP/UA live on the separate
  Request entity; `TokenController.update()` only touches content,
  status, content-type, timeout, and CORS — not `ip`. But DeepWiki is
  AI-generated secondary documentation, not the pinned primary source,
  and the deployed webhook.site may differ from the public repo.

**Fix (concrete).**
1. Run the two-IP control: create a token from IP-A (this VM's egress),
   read `GET /token/<uuid>` from IP-B (a VPN/proxy exit or second
   network), confirm `ip` still equals A and `user_agent` still equals
   A's UA. Then have a third IP view it and re-read. All three reads
   must return A.
2. Pin the primary source: quote `TokenController::create()` from
   `github.com/webhooksite/webhook.site` at a specific commit, showing
   `ip`/`user_agent` set at creation and never rewritten on read/update.
3. Write the procedure and full raw JSON into a dated provenance note
   (full values, per the never-redact rule). Until then, downgrade every
   "verified" claim to "single observation, control pending."

### A2. Chain-of-trust and grade vocabulary — MEDIUM

**Description.** What we directly observed is webhook.site's API
*output*. The IP value itself is webhook.site's server-side claim about
who created the inbox. Fabrication risk is low (token creation requires
receiving the UUID, so blind source-IP spoofing is impractical), but the
attribution step adds two unexamined assumptions: the creator was not
behind a VPN/proxy/Tor (the fleet already uses proxies on the poster
side), and webhook.site logs the true client IP rather than an edge /
`X-Forwarded-For` value. Separately, records carry `"grade": "PRIMARY"`,
which is not in Factum's registered grade vocabulary
(OBSERVED / INFERENCE / UPSTREAM per the repo AGENTS.md) — the lane-ingest
worker may reject or misgrade these.

**Evidence.** `build_factum_records()` sets `"grade": "PRIMARY"` on an
observation record whose `data.creator_ip` is a third-party server's
claim. Repo AGENTS.md: "Grade every claim: OBSERVED, INFERENCE, or
UPSTREAM."

**Fix.** Keep the API-output records as observations (OBSERVED) *of
webhook.site's claim*; record tier conclusions and `swarm_linked` as
INFERENCE in a separate claim or clearly-labeled field. Align the grade
vocabulary with the installed schema pack before the lane-ingest worker
runs — verify what it accepts, don't assume.

### A3. Code-path check: creator vs poster — CLEAN (verified)

**Description.** Attacked specifically because this is the #1 poisoning
risk. The code is clean: `extract_creator()` only ever requests
`GET /token/<uuid>` and reads the top-level `ip` / `user_agent` fields.
It never touches `/token/<uuid>/requests` and never reads per-request
source IPs. The README's comparison table matches the implementation.

**Residual nit.** If a harvested UUID is a *request* UUID rather than a
token UUID (the regex grabs any UUID-shaped string after
`webhook.site/`), `/token/<uuid>` 404s and the UUID is marked "gone."
That is noise, not confusion — but see A4/B-pipeline on UUID quality.

---

## B. Classification attacks

### B1. Tier-1 CIDR 43.162.0.0/16 is a /16 treated as certainty — HIGH

**Description.** 65,536 addresses of Tencent Cloud HK are classified
KNOWN_SWARM, "highest signal, immediate alert." The config's own
provenance says "~half fleet inferred in 43.162.0.0/16" — *inferred*,
not observed. Any Tencent HK tenant in that /16 (game servers, VPN
exits, unrelated customers) trips a tier-1 alert. The 18 exact IPs are
SECONDARY (report-derived); if the report misattributed even one —
e.g., a researcher's own view IP recorded under the method's own
ambiguity (A1) — tier-1 becomes a self-fulfilling loop that re-finds the
report's assumptions.

**Evidence.** `swarm-infra-config.json`: `known_swarm_cidrs` =
`["43.162.0.0/16"]`, provenance "swarmcha.se report SECONDARY (~half
fleet inferred in 43.162.0.0/16)"; `classify_ip()` returns tier 1 on any
CIDR hit with detail "Within known swarm CIDR."

**Fix.** Demote the /16 to a watchlist ("CIDR of interest"), not
KNOWN_SWARM. Keep exact-IP matches at tier 1 but tag them
SECONDARY-sourced with the report citation. Require a second independent
signal (fleet UA, tag-grammar context, Amap targeting) before any
"immediate alert."

### B2. Tier-2 "cloud = signal" has no measured base rate — HIGH

**Description.** Tencent Cloud HK hosts millions of tenants. AS132203
gets `swarm_linked: true` while AS45090 (also Tencent Cloud) gets
`false` — the *only* basis for the distinction is that the report's 18
IPs landed on the former. That is report-fitting, not AS-level evidence.
A tier-2 alert on Tencent HK is nearly content-free without a
denominator: how many ordinary webhook.site creators sit on Tencent HK?

**Evidence.** Config `cloud_asns`: AS132203 "Tencent Cloud / HK /
swarm_linked true" vs AS45090 "Tencent Cloud / BJ / swarm_linked false";
provenance: "Mixed: AS132203/AS45090 from report; others from our lane
IP_LOG.md."

**Fix.** Measure the base rate before alerting: run the harvester for two
weeks, count tier-2 Tencent HK hits among fleet-indicator inboxes *and*
among a control sample of random webhook.site inboxes. Only alert on
tier-2 when paired with a second signal. Document the AS132203/AS45090
asymmetry as report-derived, not intrinsic — the code currently presents
it as ground truth.

### B3. The python-requests/2.32.5 "fleet marker" is brittle and weak — MEDIUM

**Description.** Version-pinned UA matching breaks silently the day the
fleet (or the library) moves to 2.32.6. Worse, `python-requests` is the
default scripting client for thousands of legitimate webhook.site API
users — as a *creator* UA (creators are often scripts, unlike browser
posters) it has a high legitimate-use base rate. It is corroboration at
best, never a primary signal.

**Evidence.** `has_fleet_ua = "python-requests/2.32.5" in (ua or "")`;
tier-1 confidence is granted on `tier == 1 or has_fleet_ua`.

**Fix.** Match the `python-requests` family, not the exact version; track
version drift across runs; never let the UA alone raise confidence —
and note that a HIGH on `has_fleet_ua` + tier-2 is really "a script on a
big cloud," which describes half of webhook.site's API users.

### B4. The researcher-contamination mitigation is fictional — MEDIUM

**Description.** The config carries `known_researcher_ids` (e.g.
`"akbkyowd9geqr98"`) — the obvious defense against classifying *our own
side's* test inboxes as swarm infrastructure. Nothing reads it. If a
researcher creates a test inbox on Tencent HK and it gets harvested, the
crawler will file a tier-1/2 "swarm" record on a friendly IP.

**Evidence.** `grep` for `known_researcher_ids` across `scripts/*.py`:
zero hits. The RULES block lists "Researchers creating inboxes to study
the fleet" as an FP source with mitigations that do not include the
researcher-ID filter.

**Fix.** Implement it or delete it: skip (or flag) inboxes whose creator
IP matches a researcher list, and log skips. Fictional mitigations are
worse than none — they suppress the paranoia that would catch the real
event.

### B5. Asymmetric failure mode is undocumented — MEDIUM

**Description.** The classifier's threat model only prices false
positives. The false-*negative* direction is unpriced: a creator behind
a commercial VPN, Tor, or bulletproof proxy lands in tier 3/4 and the
fleet is missed entirely. The method detects *repeat of the observed
opsec failure*, not fleet resurgence by a competent operator. ipinfo.io
data is also cached forever with no TTL; org strings are free text that
the keyword heuristics already guess at.

**Evidence.** `asn_lookup()` caches on success with no expiry;
`classify_ip()` tier-3 keyword lists (`"hosting"`, `"vpn"`, …).

**Fix.** State the asymmetry in the README: this watch detects opsec
failures, it cannot detect opsec-competent operators. Add cache TTL or
ASN-change detection. Never treat tier-3/4 as "not fleet" — treat it as
"uninformative."

---

## C. Pipeline attacks

### C1. Transient failures are permanently burned — HIGH

**Description.** Any non-extracted status — HTTP 429, 500, DNS blip,
timeout — is appended to `seen_inbox_uuids` and never retried. One
rate-limit event or network hiccup permanently deletes those inboxes
from the watch. The comment says "don't retry dead inboxes," but the
branch covers *all* failures, not just 404/410.

**Evidence.** `module_creator_ips()`: the `status != "extracted"`
branch appends to `seen_inbox_uuids` unconditionally, including
`"http_error"` and `"error"` statuses.

**Fix.** Only mark seen on 404/410 and the API's explicit not-found
(`success: false`). Leave transient failures unmarked so the next run
retries them; add a bounded retry counter (e.g. 3 strikes, then park
with a `retry_exhausted` flag rather than silent burial).

### C2. The watch fails silent — HIGH

**Description.** If the fleet stops using webhook.site, changes exfil,
or simply stops being submitted to urlquery, the crawler reports "0 new
inboxes" forever — indistinguishable from "fleet dormant." There is no
denominator metric, no harvester health check, no negative control.
Separately, each query is `limit=24`; on a high-volume day the endpoint
returns the newest 24 and older matches age out of the 7-day window
unprocessed, silently, every run.

**Evidence.** `uq_htmx_search(query, limit=24)`; 7 queries per run; no
per-rule yield logging; no control query; the cron only reports on hits.

**Fix.** Log per-run denominators: reports scanned per rule, inboxes
found per rule. Alert on harvester anomalies (a rule that historically
returns hits suddenly returning zero). Paginate or raise the limit.
Add a control query (a few random webhook.site inboxes) so "extraction
path alive" is proven each run, not assumed.

### C3. Feeder/extraction mismatch is unmeasured — MEDIUM

**Description.** `extract_inbox_uuids()` scans only `report["url"]`.
The tag-grammar feeder matches on *tags* (`uqscan=`, `uqframe=`); if
those tags ride on reports whose URLs are Amap targets rather than
inbox URLs, the feeder yields zero inboxes *by construction*. Per-rule
yield is never measured, so nobody would know which feeder actually
feeds and which is decoration.

**Evidence.** `module_harvest_inboxes()`: UUID extraction only over
`r.get("url")`; tag values are never scanned for embedded UUIDs.

**Fix.** Log inboxes-per-rule every run. If tag-grammar yields zero over
N runs, fix it (scan tag values for UUIDs) or drop it. Also scan
`tags` for embedded UUIDs — the grammar may carry the inbox reference
outside the URL.

### C4. Inbox-lifetime story contradicts itself; cadence may miss everything — MEDIUM

**Description.** The README baseline concludes "7-day expiry" from 25
inboxes that were 16 days old and all 404. The CRON-PROPOSAL, in the
same directory, notes the Oct 14 session had "inboxes gone in 2h."
Both cannot be the general rule, and the code cannot tell them apart:
404 and 410 collapse into `"gone"` without recording which. If the real
lifetime is ~2h (operator deletion after use), a 6h poll misses entire
inbox lifecycles, and the watch only ever sees what urlquery happened
to capture.

**Evidence.** README "Baseline (2026-10-14)": "The 7-day webhook.site
free-tier expiry wiped the fleet's inboxes." CRON-PROPOSAL: "inboxes
gone in 2h." `extract_creator()`: 404 and 410 both → `"gone"`.

**Fix.** Record exact status codes and response bodies. Run the TTL
control: create a test inbox, poll daily untouched (measures true
expiry) vs manually delete one (measures the deletion signature).
Set the poll cadence from the measured lifetime — or explicitly document
"urlquery-captured inboxes only" as the coverage boundary.

### C5. End-to-end has never fired on live data — MEDIUM

**Description.** The all-404 baseline means harvest → extract →
classify has never completed on a real fleet inbox. Extraction is
verified on a synthetic token; the classification tiers have never
fired on live data. The first real alert will also be the first live
test of the whole chain — including the factum submission path.

**Evidence.** Baseline: 25/25 `"gone"`; zero `"extracted"` findings in
any output under `data/lanes/swarm-infra-watch/`.

**Fix.** Live-fire drill before production: run the full chain against
a researcher-created inbox (or a known-live third-party inbox) through
to factum-record construction, and document the drill output. Do not
let the first tier-1 alert be the integration test.

### C6. Dead code and doc drift — LOW (but diagnostic)

**Description.** Individually trivial; collectively evidence the code
has not been reviewed line-by-line:
- `known_researcher_ids`: never read (see B4).
- `state["processed_creators"]`: written, never read — yet the README
  claims "The crawler checks `processed_creators` in state before
  re-extracting." False.
- Docstring: "Check factum for existing records (dedup)" — the code
  never touches factum.
- `seen_report_ids`, and the `load_cache()` call at the top of
  `module_creator_ips`, are unused.
- The second "direct-submission" harvest block is unreachable in
  effect — the first loop already captured those UUIDs.
- Output is `.json`; the docstring promises "factum-ready JSONL."
- Output dir `data/lanes/swarm-infra-watch/` ignores the repo's
  date-prefixed lane-dir convention.

**Fix.** Implement or delete each: wire the researcher filter, wire or
drop `processed_creators`, correct the factum-dedup docstring (or
implement the pre-ingest `match` check the repo mandates), remove dead
state, fix the JSONL claim, align the lane dir.

---

## D. Baseline analysis — the all-404 result

The 25/25 404 baseline validates *deletion detection*, not the method.
It is consistent with at least four stories — 7-day free-tier expiry,
operator deletion, webhook.site abuse purges, UUIDs that were never
valid tokens (extracted from request bodies, not inbox URLs) — and the
data cannot distinguish them. "7-day expiry" is therefore inference
wearing observation's clothes, and it is in tension with the
cron proposal's own "inboxes gone in 2h" note (C4). The baseline
establishes exactly one thing: the watch targets *new* inboxes, because
the old ones are unrecoverable. It neither validates nor invalidates the
extraction method — it is a null result with an overconfident gloss.
Recommendation: restate the baseline as "25/25 unrecoverable as of
2026-10-14; cause undetermined, TTL experiment pending" and stop citing
it as confirmation of anything else.

---

## E. Factum integration

- The observation-record shape (observed API output + provenance noting
  creator-vs-poster) is honest as far as it goes. The problem is the
  grade: `"PRIMARY"` is not a Factum grade (A2). The swarm-linkage
  conclusions (`classification_tier`, `swarm_linked`) are INFERENCE and
  must be labeled as such — currently they ride inside an observation
  record where a downstream consumer will read them as observed fact.
- The repo's pre-ingest dedup rule (manual `match` check per candidate)
  is not implemented anywhere in the crawler or its docs; the docstring
  claims a factum check that does not exist (C6).
- Tension to resolve: the cron proposal says "never publishes inbox
  UUIDs," but factum records embed the full UUID and creator IP. If the
  factum corpus is ever exported/shared, that rule is violated silently.
  Either keep UUIDs workspace-local per the proposal, or get explicit
  approval for factum storage and note it.

---

## Verdict

No fatal flaw in the extraction code path — the right endpoint is read,
and creator/poster confusion is correctly avoided. The method stands as
a **tripwire for repeat of the exact observed opsec failure** (fleet
creates webhook.site inboxes from bare Tencent HK IPs, inboxes get
submitted to urlquery, inboxes live longer than the poll gap). It does
not stand as general fleet-resurgence detection or as attribution
infrastructure. The fixes that must land before the cron goes live:
the two-IP control + pinned source (A1), transient-failure retry (C1),
base-rate measurement before tier-2 alerts (B2), /16 demotion (B1),
lifetime/TTL experiment (C4), grade-vocabulary alignment (A2/E), and the
denominator logging that makes silent failure loud (C2). Everything else
is hygiene. If A1's control ever comes back showing the field follows
the *viewer*, the method is dead and every record built on it gets a
retraction — say that out loud now, while it is cheap.
