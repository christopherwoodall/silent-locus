# COUNSEL REVIEW — Cryptologist: what the scanners cannot see

**Reviewer role:** cryptologist counsel (adversarial review of own visibility).
**Scope:** `scripts/scanners/` — urlquery.py, ntfy.py, urlscan.py, wayback.py,
crtsh.py, packages.py, dbmining.py, `_common.py`, config
`scripts/swarm-infra-config.json`.
**Date:** 2026-10-14.
**Assumption:** the fleet operator has read every line of this code.
This review asks what they would change next.

## Bottom line

The scanners are literal-string tripwires, not behavioral detectors.
Almost every HIGH-weight rule keys on an exact string the fleet chose
(`uqscan=`, `hysandbox`, `amapdata-`, `httpbin.org/base64/`,
`akbkyowd9geqr98`). The fleet already proved it rotates tradecraft
(v4/v5 dropped the urlquery beacon and moved exfil to webhook.site).
A fleet that read this code renames five strings, moves two services,
and goes dark on every lane at once. Cost to them: trivial to easy.

The deeper problem is structural: no scanner normalizes input before
matching. Zero percent-decoding, zero base64url handling, zero
double-decode, zero base64-decode of message bodies, and one
case-sensitivity bug on the POI rule. The detectors match the
*packaging* of the indicators, not the indicators.

---

## 1. Evasion analysis, per lane

### Lane 1 — urlquery.py (`urlquery-amap-watch`)

Detection logic: 11 API queries keyed on literal strings
(`uqscan= amap`, `httpbin.org/base64`, `ntfy.sh/amapdata`, ...), then
local regex scoring on submitted URL + final URL + final title + tags,
hit at combined weight >= 3.

**E1. Rename the tag grammar.** The `tag_grammar` indicator is
`(uqscan=|uqframe=|cachebust=1|[?&]uq=)` and four of eleven query
families search for `uqscan=` / `uqframe=` / `cachebust=1` literally.
Rename `uqscan=` to `s=` (or drop the parameter; it is only a
cache-buster). Defeats: the four tag-grammar query families and the
weight-1 tag contribution. Difficulty: **trivial** (one-line change in
fleet code).

**E2. Rotate the payload host.** `httpbin_base64` is
`httpbin\.org/base64/[A-Za-z0-9+/=]{40,}` — host-locked to
`httpbin.org`. The fleet already stages on `httpbun.com`
(FP doc notes `/mix/` test paths there). Move program-packing to
`httpbun.com/base64/`, or any of a dozen httpbin clones
(httpbingo.org, httpbin.io mirrors, self-hosted). The query family
`httpbin.org/base64` goes silent; the local regex misses.
Difficulty: **trivial**.

**E3. Move exfil off the two named services.** `webhook_site` regex is
`webhook\.site/<uuid>`-shaped and `ntfy_amapdata` is
`ntfy\.sh/amapdata*`. Switch to requestbin.com, pipedream.net,
beeceptor.com, webhook-test.com (all already in our own dbmining
surface list), a Discord webhook, or a self-hosted receiver.
Difficulty: **easy** (dead-drop services are interchangeable; the
fleet already migrated ntfy -> webhook.site once).

**E4. Percent-encode the submitted URL.** `_score_row` builds its
haystack from raw API fields and applies regexes with no
`urllib.parse.unquote`. If urlquery's API returns the submitted URL
in encoded form (`httpbin.org%2Fbase64%2F...`, `amap.com%2Fssr%2F...`),
every literal regex misses — including `amap_target`.
Difficulty: **trivial** (wrapping the URL in one encode call).

**E5. base64url alphabet.** The payload regex char class is
`[A-Za-z0-9+/=]` — standard base64 only. Emit base64url (`-` and `_`
instead of `+` and `/`) and the 40+ char run no longer matches.
Difficulty: **trivial**.

**E6. Stage in page content, not the URL.** urlquery's `q` matches
submitted URLs only, never page content (documented in the module).
Lane 1 retrieves a report only if the *submitted URL* matches a query
family. A fleet that submits a benign-looking URL whose *page title or
body* carries the payload is never retrieved, so local scoring of
`final_title` never runs. Difficulty: **easy**.

**E7. `uqtag=` is in config but not in lane 1.** Config `tag_patterns`
added `uqtag=` on 2026-10-14 "for lane-7 registry scanner," but
urlquery.py's `tag_grammar` regex does not include it. A fleet
migrating tags from `uqscan=` to `uqtag=` evades lane 1 while tripping
only the packages lane. Difficulty: **trivial**. Fix: one regex edit.

**Detector changes for lane 1:**
- Normalize before matching: repeatedly percent-decode (up to 3x),
  then casefold, then match. Score a decoded copy alongside the raw.
- Replace the host-locked payload rule with a structural rule: any
  URL path segment matching `[A-Za-z0-9+/=_-]{40,}` (base64-shaped,
  either alphabet) on any host, combined with Amap targeting.
  Optionally base64-decode the segment and score the decoded bytes
  for `amap` / `iframe` / `getPoiInfo` — that survives host rotation.
- Replace the webhook.site-UUID rule with a service-agnostic rule:
  UUID-shaped path segment (`[a-f0-9]{8}-[a-f0-9-]{27}`) on *any*
  host + Amap context, plus a config-driven dead-drop host list that
  is cheap to extend.
- Add `uqtag=` to the tag regex (config already blesses it).
- Add an entropy/length heuristic for query parameters: a long
  high-entropy parameter value next to Amap targeting is the
  *behavior* the tag grammar was a proxy for. Literals are the
  costume; entropy is the body.

### Lane 3 — ntfy.py (`ntfy-amap-watch`)

Detection logic: poll config-listed topics, score message/title/topic
text against four plaintext regexes, emit on >= 1 match.

**E8. Rename the topic.** Topics come from config `ntfy_topics`
(currently one: `amapdata-b0g3lmf2g1-0429`) plus guessed patterns.
ntfy topic names are free-form and unguessable. Any new name outside
`amapdata-*` / `fleet-*` / `uqscan-*` / `bcc-mort*` is invisible.
Note the lane is already blind in practice: ntfy.sh is blocked at
egress (verified 2026-10-14), so this is a documented gap, not a
working detector. Difficulty: **trivial**.

**E9. Base64-encode the message body.** `_score_message` joins
message/title/topic raw and regex-matches plaintext. The v3 grammar
posts JSON results; base64 (or base64url, or zlib+base64) the JSON
and `amap_mention`, `poi_id`, `fleet_grammar`, `claude_label` all
miss. The scanner never attempts to decode. Difficulty: **easy**.

**E10. Case-sensitivity bug on `poi_id`.** The rule is
`\bB0[A-Z0-9]{8}\b` with **no** `re.IGNORECASE`. The fleet's own
topic grammar uses lowercase (`amapdata-b0g3lmf2g1-0429`). A message
body containing a lowercase POI id misses the strongest single rule
(only `amap_mention` catches the topic name, at MEDIUM). Compare
packages.py, which uses `[A-Za-z0-9]` explicitly. The two lanes
disagree on case handling for the same indicator family.
Difficulty to exploit: **trivial** (write POI ids lowercase).
Fix: add `re.IGNORECASE` (or explicit class) and unify across lanes.

**E11. `fleet_grammar` is literal and narrow.**
`uqscan|uqframe|nfy\(|webhook\.site` — no `cachebust`, no `uqtag`,
no case-insensitivity. Renaming any one token evades that clause.
Difficulty: **trivial**.

**Detector changes for lane 3:**
- Attempt decodings on message bodies before scoring: base64,
  base64url, percent-decode, and JSON-unescape; score each decoded
  layer. (Matches the repo's own precedent: the 2026-10-10
  intermediary-relay note says relay URLs hide behind double
  percent-encoding — the codebase knows this, the scanner doesn't do
  it.)
- Fix `poi_id` case handling; unify POI regexes across lanes into one
  shared constant in `_common.py`.
- The real fix for topic discovery is lane 1 -> lane 3 feedthrough:
  extract candidate topic names from decoded urlquery payloads
  (FP doc already notes this is the intended feed). Automate it
  instead of documenting it.

### Lane 6 — urlscan.py (`urlscan`)

Detection logic: 7 config queries (literal terms + `domain:` /
`page.title:` scoping), substring-match indicators against
page/task URL + title metadata, 30-day anonymous window.

**E12. Rename every literal.** Queries are `getPoiInfo`, `uqscan=`,
`uqframe=`, `hysandbox`, `domain:amap.com`. The fleet controls the
submitted URL's query string: drop `uqscan=`/`uqframe=` and three
queries go dark. `getPoiInfo` is the *target's* API path, not the
fleet's — that one they cannot rename, but they can stop scanning
pages that contain it in metadata-reachable form (POST bodies and
JS-fetched API calls do not appear in page URL/title metadata).
Difficulty: **trivial** for fleet-chosen strings; **moderate** for
`getPoiInfo` (requires changing what they scan, not just labels).

**E13. Wait 30 days.** Anonymous urlscan search covers only the last
30 days (documented). Any fleet run older than that is unqueryable.
A fleet that spaces distinctive runs > 30 days apart, or simply
pauses, ages out of the window. Difficulty: **trivial** (time does
the work).

**E14. Metadata-only verdicts.** Anonymous verdicts rest on URL +
title + date; full bodies need login. A fleet URL that looks benign
in metadata (no markers in URL/title) but carries the payload in
page content or screenshot is scored clean. Difficulty: **easy**.

**Detector changes for lane 6:**
- Add structural queries that don't depend on fleet labels:
  `page.title:"amap"` is already there (noisy); add scans for
  concurrent-submission bursts against amap.com page shapes, and
  correlate submitters via `task` metadata where available.
- Get authenticated urlscan access (even a free account lifts the
  30-day/metadata limits) — this is the single highest-value fix
  for the lane, and it is an account, not a code change.

### Lane 7 — wayback.py (`wayback`)

Detection logic: CDX `prefix`/`domain` queries on four fixed targets
(`hysandbox.tencent-cloud.com`, `pre-amap-pc-ssr.amap.com`,
`amap-pc-ssr.amap.com/ssr/place`, `.../ssr/api/getPoiInfo`); report
captures inside the window.

**E15. New proxy domain.** The `hysandbox.tencent-cloud.com` domain
target is burned the moment the fleet reads it. Any new proxy
hostname (or any move to a non-Tencent cloud) defeats both the CDX
domain query and the crtsh wildcard pattern simultaneously.
Difficulty: **easy** (new VM + new cert; the fleet already operates
across Tencent regions).

**E16. Stop touching the preprod host.** `pre-amap-pc-ssr.amap.com`
is one hostname. Scan the prod SSR host or the API directly and the
preprod prefix query sees nothing. Difficulty: **trivial**.

**E17. Don't trigger archiving.** Wayback captures what is submitted
to `web.archive.org/save/` or crawled. The fleet controls whether
its URLs get saved; avoiding save-submission and avoiding urlquery
submissions of the same URLs starves the lane. The FP doc admits
initiator attribution is correlation-only. Difficulty: **easy**
(operational discipline, no code change).

**Detector changes for lane 7:**
- Widen from fixed hostnames to shapes: `matchType=domain` on
  `amap.com` filtered client-side for `/ssr/` paths and burst
  timing (the 2026-10-04 baseline already proved burst/parallel
  timing is the real signal — promote it from post-analysis to the
  detector).
- Correlate capture bursts with urlquery submission bursts (lane 1
  x lane 7 join on timestamp + URL shape).

### Lane 8 — crtsh.py (`crtsh`)

Detection logic: CT search for `%.hysandbox.tencent-cloud.com`,
`%hy3%` / `%hy4%` with Tencent issuer/SAN filter; known serial
excluded; 429 aborts the run.

**E18. New cert, new name.** The `hysandbox` wildcard pattern keys on
the burned proxy name. A fresh cert for any other name is invisible.
Difficulty: **easy**.

**E19. Leave Tencent.** The hy3/hy4 patterns require "tencent" in
issuer or SANs. Move sandbox infra to Alibaba Cloud (AgentBay),
Huawei Cloud (AgentArts, AS136907 — already in our config as tier 2),
or any other cloud and the filter drops every hit. Difficulty:
**moderate** (re-tooling infra, but the sandbox research itself
concluded commercial sandboxes are ASN-indistinguishable — the
fleet knows this too).

**E20. Avoid public CT.** CT logging is mandatory for publicly
trusted certs, but a fleet proxy can use a private CA, self-signed
certs with HPKP-style pinning in its own client, or Let's Encrypt
certs on random-looking subdomains that no pattern matches.
Difficulty: **moderate** (operational change, not just a rename).

**Detector changes for lane 8:**
- Stop pattern-matching names; watch *behavior*: burst issuance of
  certs with sandbox-shaped SANs from any cloud issuer, correlated
  with ASN tier-2 sightings from other lanes. A name-based CT watch
  against an adversary who read the config is a notification
  service for the one name they already abandoned.

### Lane 7 (revised) — packages.py (`packages`)

Detection logic: literal substring/regex matching on package
name/summary/description across RubyGems, PyPI (RSS only), npm.

**E21. Rename everything.** HIGH indicators are exact literals
(`hysandbox-ats`, `akbkyowd9geqr98`, `uqscan=`). A fleet publishing
tooling under clean names evades all of them. The `oai*` prefix rule
is defeated by not starting the name with "oai". Difficulty:
**trivial**.

**E22. Publish outside the RSS window.** PyPI coverage is the RSS
recent-updates feed (~last 100 releases) plus cross-registry name
lookup. A package older than the RSS window, with a name that never
hit on RubyGems/npm, is never examined. Difficulty: **trivial**
(publish once, wait).

**E23. Hide in file contents.** The FP doc admits it: the real prior
campaign was Diffend-indexed (file contents), which no public API
exposes. Name/summary/description screening does not clear tarball
contents. A package named `geo-utils` with the payload in
`dist/bundle.js` passes every check. Difficulty: **easy**.

**Detector changes for lane 7 (revised):**
- Download and scan tarballs for HIGH-tier candidates (name hit +
  recency), not just metadata: grep file contents for the literal
  indicators and for base64-shaped blobs. Bounded cost (only on
  candidates), closes E23 for the screened set.
- Add maintainer-history heuristics: fresh account + first package
  + geo/network keywords is the *shape* of a fleet drop; literals
  are the costume.

### Lane 8 — dbmining.py (`db-url-mining`)

This lane mines *our own* corpus for repurposable surfaces. It does
not detect fleet activity; it discovers where the fleet *could* go.
Its blind spot is therefore different:

**E24. Use a surface we have never recorded.** Scoring requires the
domain to appear in our Factum records, URL inventory, or lane
artifacts. A fleet repurposing a surface absent from our corpus
scores nothing — the lane is blind to it by construction. It is a
rear-view mirror, not a radar. Difficulty for the fleet:
**trivial** (pick anything we haven't catalogued; the internet is
large).

**E25. Score-2 threshold + config-pattern dependence.** A new surface
needs `target_score >= 2`, and programmability comes from regexes in
`DEFAULT_SURFACES` or config `target_surfaces`. A novel surface
class (new product category) has no pattern until a human adds one.
Difficulty: **easy** (novelty defeats static patterns).

**Detector change:** treat dbmining as a hypothesis generator, which
it is — but close the loop: auto-probe high-scoring candidates
(can-I-create-anonymously? stable URL? public read?) instead of
leaving step 4 of the FP doc's clearing procedure manual.

---

## 2. Covert channels the scanners do not cover

The strategic counsel flagged DNS TXT, GitHub gists, and Google
Sheets. Status check:

| Channel | Covered? | Notes |
|---|---|---|
| DNS TXT records | **No.** | No scanner queries DNS at all. A fleet using TXT records on a controlled domain for dead-drop or C2 has zero lane coverage. |
| GitHub gists | **No.** | No gist polling. Gists are anonymous-creatable, persistent, public-read — they score 5/6 on dbmining's own criteria, but no active scanner watches them. The gists API is public and searchable. |
| Google Sheets / Docs | **No (and mis-scored).** | dbmining's FP doc lists `docs.google.com` as "traffic only (1) — excluded" because creation needs a Google account. A fleet *with* a Google account gets an authenticated, persistent, revisioned dead drop that we have pre-cleared as benign. |
| Pastebins (active poll) | **No.** | dbmining *lists* pastebin.com, paste.rs, ix.io, 0x0.st, termbin, paste.ee as surfaces but no scanner polls them. They are inventory entries, not watches. |
| File hosts (active poll) | **No.** | transfer.sh, file.io, catbox.moe, uguu.se listed as surfaces, never polled. |
| Discord webhooks | **No — off-scope by order.** | 2026-10-11 hunt-scope ruling. Noted, not contested; but it is a real channel the fleet could use that we will not see. |
| Telegram bots/channels | **No.** | Not in config, not in any scanner, not in dbmining surfaces. Bot API = free anonymous-ish messaging infra. |
| HuggingFace datasets as dead drops | **No.** | `_common.py`'s docstring references lanes 4 (GitHub) and 5 (HuggingFace) scanners — **neither module exists** in `scripts/scanners/`. The docstring describes lanes with no code behind them. A fleet stashing JSON in a public HF dataset (or a GitHub repo) is covered by nothing. |
| ntfy alternatives (pushbullet, Gotify, SSE services) | **No.** | Lane 3 is ntfy.sh-only and transport-blocked. |
| URL shortener *creation* monitoring | **No.** | dbmining scores shorteners as surfaces; no lane watches shortener creation streams for fleet-shaped links. |

The pattern: dbmining catalogues surfaces; almost none of them have
an active polling scanner. The catalogue is not coverage.

---

## 3. Encoding blind spots (cross-lane)

Tested against the actual regexes in the code:

1. **No percent-decoding anywhere.** `urlquery.py::_score_row` and
   `ntfy.py::_score_message` match raw strings. Single, double, or
   triple percent-encoding of any indicator defeats every lane-1 and
   lane-3 rule. The repo already knows double-encoding happens in the
   wild (2026-10-10 intermediary-relay note: relay URLs arrive
   double-encoded) — the scanners just don't decode.
2. **base64url alphabet not matched.** `httpbin_base64` requires
   `[A-Za-z0-9+/=]`; `-` and `_` break the run. One-character-class
   fix.
3. **No base64-decode-and-rescore.** ntfy bodies, urlquery payload
   segments, and package descriptions are never decoded before
   scoring. The fleet's own tradecraft *is* base64 program-packing;
   the detectors look at the wrapping, never inside it.
4. **POI regex case inconsistency (bug).** ntfy.py:
   `\bB0[A-Z0-9]{8}\b` (case-sensitive, misses the fleet's own
   lowercase `b0g3lmf2g1`). packages.py: `\bB[A-Za-z0-9]{9}\b`
   (case-tolerant). Same indicator, two behaviors. The ntfy one is
   wrong.
5. **`uqtag=` missing from lane 1** while present in config and in
   the packages lane (E7).
6. **Unicode/lookalike confusables not handled.** `amap_target` is
   ASCII-only; IDN homographs (`аmap.com` with Cyrillic а) or
   full-width characters in submitted URLs miss it. Cheap fix:
   NFKC-normalize + `idna` decode before matching. (Lower priority —
   the fleet hasn't shown this — but the detector claims to watch
   "amap.com" and doesn't, strictly speaking.)
7. **No JSON-unescape layer.** Payload URLs embedded JSON-escaped
   inside wrapper query strings (`...&url=https%3A%2F%2F...`) are
   documented in the 2026-10-10 relay note; scanners apply regexes
   to the escaped form.

**Fix (one place, all lanes):** add a `normalize()` helper to
`_common.py` — NFKC, repeated percent-decode (x3), JSON-unescape,
base64/base64url-decode-and-append — and score the normalized copy
alongside the raw in every lane. Unify the POI regex as a shared
constant.

---

## 4. The via_anomalies gap — CONFIRMED MISSING

The sandbox research
(`reports/sandbox-fingerprint-research-2026-10-14.md`, lines 63–65)
recommends:

> **Recommendation for the urlquery scanner:** add a `via_anomalies`
> check — any Via header that isn't a well-known proxy product string
> gets logged as a candidate. Low cost, catches the NEXT hysandbox.

**Status: not implemented anywhere.**

- No scanner references Via headers as signal (grep over
  `scripts/scanners/*.py`: zero hits).
- Lane 1 never fetches full report details — it scores only
  `search`-endpoint fields (submitted URL, tags, final URL/title,
  IP). Via headers live in the report's transaction/response
  headers, reachable via `uq.py report <id>`, which the lane never
  calls.
- Config has no `via_anomalies` entry, no known-proxy allowlist.

The research's own framing is correct: the lesson of `hysandbox-ats`
is the *method* (custom proxy label on a self-reported Via header),
not the string. Without this detector we will not catch the next
one — we will only ever grep for the last one.

**Implementation sketch (for the code-fixer worker):**
1. In `urlquery.py`, for each hit (or each screened report above a
   lower pre-threshold), call `uq.py report <report_id>` and extract
   response `Via` / `X-Forwarded-*` / `Server` headers from the
   transaction data.
2. Maintain `via_allowlist` in config: well-known proxy product
   tokens (squid, varnish, nginx, cloudflare, envoy, haproxy,
   ATS, gws, ...).
3. Flag any Via token not on the allowlist as `via_anomaly`
   indicator (weight 2 — same tier as `amap_target`; it is a
   behavioral proxy marker, not a fleet confession).
4. Record the raw Via value verbatim on the hit (never redact).
5. Note the residual: a fleet that strips Via entirely evades this
   too (one header removal, **trivial**) — but *absence* of Via on a
   report whose IP is a cloud proxy is itself a (weaker) anomaly
   worth logging. The detector should flag both unknown-Via and
   missing-Via-behind-proxy.

---

## 5. Ranked gap table

| # | Evasion | Lane(s) defeated | Difficulty | Detector change to close it |
|---|---|---|---|---|
| E1 | Rename `uqscan=`/`uqframe=` tag | 1 | trivial | Entropy/length heuristic on query params; normalize-then-match |
| E2 | Move payload host off httpbin.org | 1 | trivial | Host-agnostic base64-segment rule + decode-and-score payload |
| E7 | Switch tags to `uqtag=` | 1 | trivial | Add `uqtag=` to lane-1 regex (config already blesses it) |
| E4 | Percent-encode submitted URLs | 1 | trivial | Repeated percent-decode in `_score_row` |
| E5 | base64url alphabet in payload | 1 | trivial | Add `-_` to payload char class |
| E8 | Rename ntfy topic | 3 | trivial | Lane1->lane3 topic feedthrough from decoded payloads |
| E10 | Lowercase POI ids (case bug) | 3 | trivial | IGNORECASE on `poi_id`; unify POI regex in `_common.py` |
| E11 | Rename tokens in `fleet_grammar` | 3 | trivial | Broaden + casefold; decode-then-score |
| E12 | Drop fleet literals from scanned URLs | 6 | trivial | Structural/burst queries; authenticated urlscan access |
| E13 | Age out of 30-day urlscan window | 6 | trivial | Authenticated access (longer history) |
| E16 | Stop using preprod host | 7-wayback | trivial | Shape-based CDX (domain + `/ssr/` + burst timing) |
| E21 | Rename package indicators | 7-pkg | trivial | Maintainer-history heuristics; tarball content scan |
| E22 | Publish outside PyPI RSS window | 7-pkg | trivial | Cross-registry + author-history watch; accept as known gap |
| E24 | Use a surface absent from our corpus | 8-dbmining | trivial | Auto-probe loop; treat lane as hypothesis generator |
| E3 | New dead-drop service | 1 | easy | Service-agnostic UUID-path rule + dead-drop host list |
| E6 | Stage payload in page content | 1 | easy | Fetch full report for hits; score response body/title |
| E9 | Base64-encode ntfy bodies | 3 | easy | Decode-then-score (b64, b64url, percent, JSON-unescape) |
| E14 | Benign-looking metadata, evil body | 6 | easy | Authenticated urlscan (full bodies) |
| E15 | New proxy domain | 7-wayback, 8-crtsh | easy | Behavioral CT watch (issuance bursts + ASN correlation) |
| E17 | Don't trigger Wayback saves | 7-wayback | easy | Lane1 x lane7 timestamp/URL-shape join |
| E18 | New cert, new name | 8-crtsh | easy | Same as E15 |
| E23 | Hide payload in tarball contents | 7-pkg | easy | Download + grep tarballs for candidates |
| E25 | Novel surface class, no config pattern | 8-dbmining | easy | Anomaly-score new product categories, not just patterns |
| E19 | Leave Tencent for another cloud | 8-crtsh | moderate | Drop issuer-name filters; ASN-burst correlation |
| E20 | Private CA / pinned self-signed | 8-crtsh | moderate | Accept as gap; CT only sees public trust |
| — | **via_anomalies not implemented** | 1 | — | Implement per §4 (fetch report detail, allowlist Via tokens) |
| — | **DNS TXT / gists / Sheets / pastebins / file hosts / Telegram: no active scanner** | — | — | New polling lanes for gists + pastebins (public APIs); Sheets/TXT as documented gaps |
| — | **Lanes 4 (GitHub) and 5 (HuggingFace) referenced in `_common.py` docstring but no modules exist** | — | — | Write them or fix the docstring; HF datasets as dead drops are uncovered |

## 6. Priority fixes (cryptologist's ordering)

1. **`_common.normalize()` + decode-then-score everywhere** (closes
   E4, E5, E9, and the JSON-unescape/double-encode variants in one
   helper). Cheapest fix with the widest blast radius.
2. **Implement `via_anomalies`** (§4). It is the only detector in
   this review that catches the *next* tradecraft instead of the
   last one, and it was already recommended by research and then
   dropped.
3. **Host-agnostic payload rule + service-agnostic exfil rule**
   (closes E2, E3). Move from literals to shapes: base64-segment on
   any host, UUID-path on any host, high-entropy param + Amap.
4. **Fix the POI case bug and unify the regex** (E10). A wrong regex
   is worse than no regex — it reports "checked" while missing.
5. **Stand up the missing lanes**: GitHub/gist scanner and
   HuggingFace scanner (the docstring already promises them), plus
   pastebin polling. DNS TXT and Google Sheets stay documented gaps
   (TXT needs DNS vantage; Sheets needs auth).
6. **Authenticated urlscan access** (E13, E14). Not a code change;
   biggest single lift for lane 6.
7. **Accept and document the unfixable**: private-CA proxies (E20),
   surfaces never in our corpus (E24), a fleet that stops submitting
   to urlquery at all (the FP doc already notes v4/v5 did this).
   A scanner suite that cannot say "we are blind here" will be read
   as saying "nothing is there." The ntfy module's transport-gap
   handling is the template — every lane should fail *loud* the
   same way.

## Method note

This review read all seven scanner modules, all seven
FALSE-POSITIVES docs, the shared `_common.py`, the full
`swarm-infra-config.json`, and the sandbox fingerprint research
report. No scanners were executed; evasion claims rest on the
regexes and query strings as written. The `via_anomalies`
non-implementation was verified by grep (zero references in
`scripts/scanners/`) and by confirming lane 1 never calls
`uq.py report` (the only path to response headers).

**Grade of this review:** INFERENCE (adversarial reasoning over
observed code), except the via_anomalies gap and the POI case bug,
which are OBSERVED in the code as written.
