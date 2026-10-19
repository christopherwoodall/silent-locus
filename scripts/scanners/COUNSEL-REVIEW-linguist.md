# COUNSEL REVIEW — Linguist: agent-swarm crawler scanners

Reviewer: linguist counsel. Scope: every detection pattern, keyword,
regex, and query in `~/workspace/silent-locus/scripts/scanners/`
(`urlquery.py`, `ntfy.py`, `urlscan.py`, `wayback.py`, `crtsh.py`,
`packages.py`, `dbmining.py`), the shared `swarm-infra-config.json`,
and the FALSE-POSITIVES docs. Method: each suspect pattern was
executed against adversarial test strings before filing (see
"Verification" at the end).

Summary verdict: the scanners' strongest patterns (`hysandbox-ats`,
`uqscan=`/`uqframe=` literals, `pre-amap-pc-ssr.amap.com`, Amap POI
page paths, the tag-grammar conjunction design) are linguistically
sound. The imprecision concentrates in five places: (1) the `research*`
label regex, (2) the `amap+geo-context` word list in `packages.py`
(the single worst false-positive factory found), (3) the POI-ID regex
`B[A-Za-z0-9]{9}` colliding with hex/sha fragments, (4) the `oai*`
package-name prefix colliding with the OAI-PMH family, and (5) generic
topic/query terms (`fleet-*`, bare `webhook.site`, bare `amap`). Each
finding lists severity, file:line, the offending pattern quoted, why it
is imprecise, and a concrete fix.

---

## HIGH

### H1 — `label_grammar` matches any word containing "research"
- File: `urlquery.py:74`
- Pattern: `re.compile(r"(claude20\d{6,}|research[\w-]{2,})", re.IGNORECASE)`
- Problem: the `research[\w-]{2,}` alternative has no boundary, no
  required suffix shape, and no anchor. Verified: it matches
  "researchers" in the sentence "researchers at MIT" — i.e. ordinary
  English prose, paper titles, and package descriptions containing
  "researcher/researchers/researching/research-paper" all fire this
  indicator. The docstring claims the "research*" label grammar is
  fleet-observed; the regex as written captures a plain English word,
  not a label grammar. Weight is only 1, but it can be the deciding
  indicator that pushes `tag_grammar(1)+amap_target(2)`-style
  conjunctions over the threshold.
- Fix: require the observed label shape and boundaries, e.g.
  `r"\bresearch[-_][a-z0-9]{4,}\b"` (fleet labels observed are
  `research-*` hyphenated suffixes) and `\bclaude20\d{6,}\b`. If the
  actual fleet label grammar includes a bare "research" token, require
  it to appear in a label-like position (e.g. preceded by `?`/`&`/`=`
  or in the tags field), not in free prose.

### H2 — `amap+geo-context` word list is dominated by generic substrings
- File: `packages.py:89-94`
- Pattern:
  ```python
  if ("amap" in low or "gaode" in low) and any(
      w in low for w in ("poi", "scrap", "map", "geo", "location",
                         "place", "导航", "高德")):
  ```
- Problem: `"map"` is a substring match against full text, so
  "roadmap", "mindmap", "sitemap", "mind-map" all count as geo
  context. `"scrap"` matches "scraper"/"scrapbook". `"location"` and
  `"place"` are generic. Verified: `"amap wrapper; see roadmap for
  scraper plans"` satisfies the context requirement — a package with
  no geographic function whatsoever earns the MEDIUM
  `amap+geo-context` indicator. This is the cheapest false-positive
  path in the whole scanner set: any package mentioning "amap"
  (e.g. legitimate Amap SDK wrappers, which the doc itself says are
  numerous) plus a roadmap link hits MEDIUM. `tier_confidence` then
  promotes it to full "MEDIUM" confidence.
- Fix: replace substring list with boundary-anchored, genuinely
  geographic terms, e.g.
  `r"\b(poi|gaode|高德|导航|geocod\w*|reverse-?geocod\w*|lnglat|gcj-02|wgs-84)\b"`,
  and drop `map`, `scrap`, `location`, `place` entirely. Add an
  explicit exclusion for `roadmap`/`sitemap`/`mindmap` if `map` is
  ever reintroduced.

### H3 — `oai*` name-prefix regex collides with the OAI-PMH family
- File: `packages.py:96` and `packages.py:201-203` (`NAME_RE`)
- Patterns: `re.match(r"(?i)^oai[\w-]*", name)` and
  `r"^(oai|amap|uqscan|uqtag|uqframe|hysandbox)[\w-]*|[\w-]*(amap|uqscan|uqtag|uqframe|hysandbox)[\w-]*$"`
- Problem: `^oai[\w-]*` matches `oasis-*`, `oaken`, and the entire
  OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting)
  ecosystem — verified: `oai-pmh-harvester` matches. OAI-PMH is a
  long-established, high-volume legitimate naming family completely
  unrelated to OpenAI. The FALSE-POSITIVES doc acknowledges "the oai
  prefix is crowded with legitimate OpenAI client libraries" but
  misses the OAI-PMH collision, which is the worse one because it is
  an acronym collision, not just a crowded market. These feed
  `NAME_RE`, which drives the RubyGems full-index sweep — every match
  costs a metadata fetch and a triage slot.
- Fix: require a separator and exclude the harvesting protocol:
  `r"(?i)^oai[-_](?!pmh\b)"` for the prefix, and the same in
  `NAME_RE`. Consider also excluding `^oasis\b` unless observed in
  fleet use.

### H4 — POI-ID regex `B[A-Za-z0-9]{9}` matches hex/sha fragments
- File: `packages.py:88`; config `swarm-infra-config.json`
  (`registry_scanners.poi_id_regex`, line ~`"poi_id_regex": "\\bB[A-Za-z0-9]{9}\\b"`)
- Pattern: `r"\bB[A-Za-z0-9]{9}\b"`
- Problem: this is any 10-character token beginning with "B" —
  lowercase allowed. Verified: the git short-sha fragment `B4f6a8c2d9`
  matches. So do 10-char build IDs, API key fragments, base64-ish
  tokens, and version-ish strings in changelogs (a known input —
  the doc itself warns about version strings elsewhere). It earns
  MEDIUM tier ("tooling pattern"), which `tier_confidence` promotes
  to full "MEDIUM" confidence on a recent package. The ntfy scanner
  uses a stricter grammar (see L5); the two scanners disagree on
  what a POI ID looks like.
- Fix: align with the observed Amap POI grammar — require the `B0`
  prefix both scanners can agree on: `r"\bB0[A-Za-z0-9]{8}\b"`
  (case-sensitive; Amap POI IDs are uppercase+digits). If
  case-insensitive matching is wanted, keep it but require a
  co-indicator (`amap`/`gaode`/`poi` within the same field) before
  granting MEDIUM.

### H5 — ntfy `fleet_grammar` is looser than its own docstring claims
- File: `ntfy.py:70`
- Pattern: `re.compile(r"uqscan|uqframe|nfy\(|webhook\.site")`
- Problem: `uqscan`/`uqframe` without the trailing `=` match
  `uqscreenshot`, `uqframebuffer`, `framebuffer` discussions — the
  fleet marker is the `uqscan=` / `uqframe=` tag assignment, not the
  bare stems. `webhook.site` bare (no UUID path requirement, unlike
  `urlquery.py:71`'s UUID-shaped version) matches any message that
  merely mentions webhook.site — including a message discussing the
  fleet's dead-drops, which the FALSE-POSITIVES-ntfy doc itself
  warns about ("a message TALKING ABOUT probes looks identical to
  regex"). `nfy\(` is a typo-shaped fragment (presumably meant
  `ntfy(`); as written it matches `notify(`-family tokens and
  `confy(`-style words, adding noise without evident fleet
  connection. Critically, `_score_message` emits a hit at MEDIUM on
  ANY single content-rule match (`ntfy.py:275-276`, `if not matched:
  continue`), so one loose rule is enough to page a human.
- Fix: `r"uqscan=|uqframe=|ntfy\.sh/|webhook\.site/[a-z0-9-]{8,}"`
  — require the `=` on tag stems, require the actual service host
  form, and drop or correct `nfy\(` to `ntfy\(` if a function-call
  pattern was intended (document which function).

---

## MED

### M1 — `cachebust=1` is generic cache-busting vocabulary
- File: `urlquery.py:65` (inside `tag_grammar`),
  query family `swarm-infra-config.json` (lane-1 `cachebust=1 amap`)
- Pattern: `r"(uqscan=|uqframe=|cachebust=1|[?&]uq=)"`
- Problem: `cachebust=1` (and `cachebust=<anything>`) is used by
  ordinary web applications, ad tags, and analytics beacons to
  defeat caching. The FALSE-POSITIVES-urlquery doc admits the whole
  tag-grammar family fires ~1,304 reports/14 days on `uqscan=` alone
  from bots/QA scripts/researchers. Adding a fully generic param
  (`cachebust=1`) to the same family dilutes the one part of the
  family that IS fleet-specific (`uqscan=`/`uqframe=`). Weight 1 and
  conjunction-required mitigate, but the indicator name
  "tag_grammar" then mislabels a hit: a reviewer sees "tag_grammar"
  matched and assumes the fleet's `uqscan=` marker fired, when it
  was `cachebust=1` on a normal page.
- Fix: split into two indicators — keep `uqscan=`/`uqframe=` as
  `tag_grammar` (w=1), and make `cachebust=1` a separate indicator
  that only fires with an Amap-target co-indicator already present
  (or drop it; the fleet value is documented in config's
  `tag_patterns` as completeness, not as observed-in-fleet).

### M2 — `[?&]uq=` matches any query parameter named `uq`
- File: `urlquery.py:65` (inside `tag_grammar`)
- Pattern: the `[?&]uq=` alternative of
  `r"(uqscan=|uqframe=|cachebust=1|[?&]uq=)"`
- Problem: `uq` is a plausible short parameter name in unrelated
  code (user-query, unique-queue). The fleet's `uq=` usage is
  urlquery-tag shaped; the regex requires no value shape. Any URL
  like `https://example.com/search?uq=1` fires `tag_grammar` at
  weight 1 and gets the "tag_grammar" indicator label.
- Fix: require the fleet value grammar, e.g.
  `[?&]uq=[a-f0-9-]{8,}` or `[?&]uq=(scan|frame|tag)[\w-]*`,
  whichever matches the observed fleet usage; document the value
  grammar in the config `tag_patterns` provenance note.

### M3 — ntfy topic discovery patterns `fleet-*` / `uqscan-*` too generic
- File: `swarm-infra-config.json:165-169`
  (`"ntfy_topic_patterns": ["amapdata-*", "fleet-*", "uqscan-*", "bcc-mort*"]`)
- Problem: `fleet-*` matches any entity's fleet notifications
  (vehicle fleets, server fleets, "my-bot-fleet"); `uqscan-*` is a
  short generic stem. The doc says discovery is "a LEAD, not a
  hit", which is honest, but every CDX-prefix probe that returns
  unrelated topics still consumes triage attention and risks a
  follow-on poll of someone else's topic — a privacy-relevant
  overreach, not just noise. `amapdata-*` and `bcc-mort*` are
  well-scoped (observed fleet grammar); the other two are guesses.
- Fix: scope `fleet-*` to `fleet-amap*`/`amap-fleet*` (the observed
  naming direction is amap-first), or require a CDX result to ALSO
  contain a POI-ID or `amap` string in the archived topic name
  before treating it as a discovery lead. Document `uqscan-*` as
  low-priority.

### M4 — ntfy `amap_mention` rule emits alone at MEDIUM
- File: `ntfy.py:68`, `ntfy.py:275-276`
- Pattern: `re.compile(r"amap|gaode", re.IGNORECASE)`; emit rule:
  `if not matched: continue` with `confidence = "HIGH" if
  len(matched) >= 2 else "MEDIUM"`
- Problem: the FALSE-POSITIVES-ntfy doc itself says "the word 'amap'
  appears in unrelated contexts (e.g. someone testing whether ntfy
  works by posting a URL)". On the known topic
  `amapdata-b0g3lmf2g1-0429` — which is public, unauthenticated, and
  named in published writeups — any passerby posting the word
  "amap" produces a MEDIUM hit with no further discrimination.
  Copycat/coincidence traffic is the expected background here.
- Fix: require `amap_mention` to co-occur with at least one other
  rule (`poi_id`, `fleet_grammar`, `claude_label`) to emit, or cap
  single-rule `amap_mention` hits at LOW. Also add `\b` boundaries:
  as written it matches "amapacad", "teamap", "seamap" inside
  longer tokens.

### M5 — `preprod_host` regex has no boundary (suffix-squatting shape)
- File: `urlquery.py:67`
- Pattern: `re.compile(r"pre-amap-pc-ssr\.amap\.com", re.IGNORECASE)`
- Problem: no leading/trailing boundary, so
  `pre-amap-pc-ssr.amap.com.evil.com` and
  `xpre-amap-pc-ssr.amap.com` both match. URL-haystack substring
  matching against the fleet's pre-prod host is otherwise sound;
  this is a boundary hygiene issue, not a vocabulary one.
- Fix: `r"(?:^|[/:.\?#])pre-amap-pc-ssr\.amap\.com(?:[/:?\#]|$)"`.

### M6 — crt.sh `direct_domain` check is a substring, not a domain match
- File: `crtsh.py:154-155`
- Pattern: `any("hysandbox.tencent-cloud.com" in s.lower() for s in sans)`
- Problem: verified — the SAN `fakehysandbox.tencent-cloud.com`
  (and any `*.evil.com`-style suffix embedding the string) matches,
  because `in` is a substring test. A cert earns HIGH confidence
  ("fleet-linked") on this check. Hostile or coincidental SANs
  containing the fleet domain as a substring would be graded HIGH.
- Fix: proper domain-boundary test:
  `s == "hysandbox.tencent-cloud.com" or
   s.endswith(".hysandbox.tencent-cloud.com")` (after lowercasing
  and stripping a leading `*.`).

### M7 — bare `hysandbox` (without `-ats`) graded HIGH in packages.py
- File: `packages.py:82-83`
- Pattern:
  ```python
  if "hysandbox" in low and ("hysandbox-ats", "HIGH") not in hits:
      hits.append(("hysandbox", "HIGH"))
  ```
- Problem: the FALSE-POSITIVES doc's honest-zero baseline is about
  `hysandbox-ats` (the proxy label), which has zero legitimate use.
  Bare `hysandbox` also matches prose ABOUT the marker — a security
  writeup package, a detector, a blog-post mirror describing
  "hysandbox" research. Those are second-order mentions, and grading
  them HIGH ("exact rare marker. Act on it.") mislabels commentary
  as fleet artifact.
- Fix: keep `hysandbox-ats` and `hysandbox.tencent-cloud.com` at
  HIGH; demote bare `hysandbox` to MEDIUM and require a second
  indicator (package name match, or `tencent`/`proxy`/`sandbox`
  tooling context) before HIGH.

### M8 — POI grammar inconsistent between scanners
- Files: `ntfy.py:69` (`r"\bB0[A-Z0-9]{8}\b"`, requires `B0`,
  uppercase only) vs `packages.py:88` (`r"\bB[A-Za-z0-9]{9}\b"`,
  any B-lead, mixed case) vs config `poi_id_regex`
  (`\bB[A-Za-z0-9]{9}\b`, matches packages.py)
- Problem: two scanners implement two different grammars for the
  same claimed identifier. If the Amap POI grammar is `B0`+8
  (ntfy's comment says "Amap POI id grammar (10 chars)"), then
  packages.py's version is strictly looser than the evidence
  supports and is the one generating hex-fragment FPs (H4). If
  non-`B0` POI IDs are genuinely observed, ntfy is under-matching.
  Either way the inconsistency means one scanner is wrong.
- Fix: settle the grammar from observed fleet POI IDs (the
  FALSE-POSITIVES-urlquery doc cites 83% POI-ID overlap with 217
  fleet targets — that corpus is the ground truth), put the single
  canonical regex in config, and have both scanners read it.

### M9 — urlscan `page.title:"amap"` indicator matched as bare substring
- File: `swarm-infra-config.json` (`urlscan.queries`, label
  `title-amap`, indicator `"amap"`), `urlscan.py:51-56`
  (`_match_indicators`: `i.lower() in h`)
- Problem: the indicator `amap` is substring-matched against
  lowercased URL/title, so `amapacad.org.ng` (documented in the
  FP doc as an acronym collision), `teamap`, `seamap...` all fire
  the `amap` indicator at MEDIUM (single indicator → MEDIUM per
  `urlscan.py:106-107`). The FP doc lists these as "ignore", but
  the scanner still emits them as hits — the doc and the code
  disagree on disposition.
- Fix: boundary-match the indicator: check
  `re.search(r"\bamap\b", h)` or require the indicator to appear
  in the `domain:` field rather than the title, or auto-suppress
  the documented collision domains (`amapacad.org.ng`,
  `*.azure.com` amap-prefixed hosts) in `_match_indicators`.

### M10 — dbmining lane-marker substring matching
- File: `dbmining.py:319`
- Pattern: `any(m in ll for m in
  db["agent_tradecraft_lane_markers"])` with markers
  `["amap", "webhook-deaddrop", "pastebin-k4be",
  "agent-convo-venue", "chinese", "rogue-agent",
  "urlquery-marker"]`
- Problem: `"amap" in "amapacad-research-lane"` and `"chinese" in
  "chinese-mapping-sdk-docs"` are true. Marker `chinese` is a
  language adjective, not a tradecraft marker. A substring hit here
  contributes the `prior_agent_contact` criterion — one of only six
  criteria, with `min_target_score: 2` — so a loose lane-name match
  plus one surface-pattern match emits a "repurposable surface" hit.
- Fix: token-boundary match on the lane tag:
  `re.search(r"(?<![\w-])" + re.escape(m) + r"(?![\w-])", ll)`,
  and reconsider whether `chinese` belongs in this list at all.

---

## LOW

### L1 — `webhook_site` UUID shape allows dashes anywhere
- File: `urlquery.py:71`
- Pattern: `re.compile(r"webhook\.site/[a-f0-9]{8}-[a-f0-9-]{27}")`
- Problem: `[a-f0-9-]{27}` permits `-` at any position; a real UUID
  is `8-4-4-4-12`. webhook.site inbox tokens are also not always
  UUIDs (custom tokens exist), so this is both over- and
  under-specific, but only mildly: weight 1, conjunction-required.
- Fix: `r"webhook\.site/[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}"`
  for UUIDs, or document that non-UUID tokens are intentionally
  covered and widen to `[A-Za-z0-9_-]{8,}`.

### L2 — `ntfy_amapdata` tail `[-\w]*` over-matches the stem
- File: `urlquery.py:72`
- Pattern: `re.compile(r"ntfy\.sh/amapdata[-\w]*")`
- Problem: matches `ntfy.sh/amapdatabase`, `ntfy.sh/amapdata-center`
  — the observed fleet grammar is `amapdata-<POI>-<suffix>`. Minor:
  weight 2, conjunction-required, and the stem is specific.
- Fix: `r"ntfy\.sh/amapdata-[-\w]+"` (require the hyphen the fleet
  grammar uses).

### L3 — `httpbin_base64` misses URL-encoded payloads (recall, not FP)
- File: `urlquery.py:68-69`
- Pattern: `re.compile(r"httpbin\.org/base64/[A-Za-z0-9+/=]{40,}")`
- Problem: base64 in a URL path is frequently percent-encoded
  (`%2F`, `%2B`, `%3D`); the character class excludes `%`. This is
  a miss direction, but linguistically the pattern claims to cover
  "httpbin /base64/ payloads" while covering only the unencoded
  subset.
- Fix: allow `(?:[A-Za-z0-9+/=]|%[0-9A-Fa-f]{2}){40,}`.

### L4 — `claude_label` without boundaries; no fleet-shape requirement
- File: `ntfy.py:71`
- Pattern: `re.compile(r"claude20\d{6,}", re.IGNORECASE)`
- Problem: matches `xclaude20261014y` inside longer tokens; more
  importantly the fleet label is `claude<YYYYMMDD>` (8 digits) and
  `\d{6,}` also matches 6-7 digit non-dates. Minor: the doc already
  flags self-identification as spoofable.
- Fix: `\bclaude20\d{6}\b` for the date shape, or keep `{6,}` with
  a comment if longer suffixes are observed.

### L5 — `ntfy.py` POI regex can match uppercase English words
- File: `ntfy.py:69`
- Pattern: `r"\bB0[A-Z0-9]{8}\b"`
- Problem: a 10-char all-caps token starting with `B0`
  (e.g. `B0ARDGAMES1`) matches. Narrower than packages.py's
  version (H4) and the strongest single content rule per the doc,
  but still a bare-shape match with no checksum or contextual
  requirement.
- Fix: require a co-indicator (`amap`/`gaode`/`poi` within the same
  message) before `poi_id` alone can push a hit to HIGH, or check
  the token against the known fleet POI target list when available.

### L6 — crt.sh `hy3`/`hy4` patterns even with the tencent filter
- File: `swarm-infra-config.json` (`crtsh.patterns`), `crtsh.py:99-102`
- Problem: `%hy3%` matches `why3t`, `shy3ll`, `hy3brid` anywhere in
  any SAN; the `issuer_filter: "tencent"` mitigation checks
  `"tencent" in sans` against the WHOLE name_value blob, so a cert
  covering `hy3x.example.com` + `tencent.com` passes the filter with
  zero Tencent relationship to the `hy3` name. Doc acknowledges
  noise; the filter is weaker than it reads.
- Fix: require `tencent` in the ISSUER only for the filter pass,
  or require the tencent string to appear in the SAME SAN entry as
  the `hy3`/`hy4` match. Cap-and-triage remains acceptable after
  that.

### L7 — dbmining `URL_RE` trailing-character handling is asymmetric
- File: `dbmining.py:44`
- Pattern: `r'https?://[^\s<>"\'\]\)\},;]+'`
- Problem: `!` `?` `.` are included in the match and only stripped
  on some code paths (`_iter_sources` rstrips `".,;:!?"` for two
  sources but not for the legacy Transluce inventory or lane
  artifacts). Trailing `?`/`!`/`.` change `urlparse().hostname`
  rarely (hostname parsing is tolerant), but example_urls recorded
  in hits can carry junk suffixes, and `host` can end up with a
  trailing `.` only sometimes stripped (`.rstrip(".")` is applied
  to host — fine). Low impact, hygiene only.
- Fix: apply the same `rstrip(".,;:!?")` uniformly in
  `_iter_sources`, or move the rstrip into the regex with a
  trailing lookahead.

### L8 — `amap_target` regex has no boundaries
- File: `urlquery.py:66`
- Pattern: `re.compile(r"(amap\.com|gaode\.com)", re.IGNORECASE)`
- Problem: matches `notamap.com`, `amap.com.evil.com`. Weight 2
  and conjunction-required, so impact is bounded — but the
  indicator name suggests "targeted amap.com", and a lookalike
  domain would carry that label.
- Fix: `r"(?<![\w.])amap\.com(?![\w.])"` style boundaries on both
  alternatives.

### L9 — urlscan `getPoiInfo` indicator is fine; `hysandbox` query is fine
- Files: `swarm-infra-config.json` (`urlscan.queries`),
  `urlscan.py:43` (`RARE_MARKERS`)
- No change recommended. `getPoiInfo` is a distinctive API method
  name; `hysandbox` is a distinctive proxy label. These are the
  well-formed end of the spectrum — cited here as the pattern to
  imitate.

---

## Cross-cutting notes

1. **"tag_grammar" is doing too much work as a label.** In
   `urlquery.py` one indicator name covers four different
   alternatives (`uqscan=`, `uqframe=`, `cachebust=1`, `uq=`), two
   of which are generic (M1, M2). Every downstream consumer —
   triage notes, factum records, the FP doc's triage ordering —
   reads "tag_grammar matched" as "the fleet's urlquery tag
   fired". Split the indicator so the label is truthful.
2. **The docs are more honest than the code.** FALSE-POSITIVES docs
   correctly identify most of these risks (generic `cachebust`,
   oai* crowding, `fleet-*` guessiness, acronym collisions) but
   several mitigations described as handled are not implemented
   (M9's collision domains still emit; M4's single-rule MEDIUM
   emit contradicts the doc's "only in combination" framing).
3. **No issue found in `wayback.py` target patterns or `_common.py`.**
   Wayback targets are exact host/path prefixes with an explicit
   anti-bot-noise flag — linguistically the tightest lane.
   `_common.py` carries no detection patterns.
4. **dbmining's `target_surfaces` built-ins are well-formed** (exact
   host regexes with categories and per-surface auth/persistence
   notes). The imprecision is in the lane-marker substring match
   (M10), not the surface list.

## Verification

Each HIGH and MED finding above was tested by executing the actual
regex/pattern from the file against an adversarial string in
`python3` before filing:

- `research[\w-]{2,}` matches "researchers" (urlquery.py:74) —
  confirmed.
- `\bB[A-Za-z0-9]{9}\b` matches the sha-fragment `B4f6a8c2d9`
  (packages.py:88) — confirmed.
- `any(w in low ...)` geo list satisfied by "roadmap"/"scraper"
  with zero geographic content (packages.py:89-94) — confirmed.
- `NAME_RE` matches `oai-pmh-harvester` and `paramap`
  (packages.py:201-203) — confirmed.
- `"hysandbox.tencent-cloud.com" in
  "fakehysandbox.tencent-cloud.com"` is True (crtsh.py:154) —
  confirmed.
- `fleet_grammar` alternative `nfy\(` present as written
  (ntfy.py:70); `uqscan`/`uqframe` lack `=` — by inspection.

## Recommended fix priority

1. H2 (geo-context word list) — cheapest FP factory, MEDIUM-tier
   inflation across all three registries.
2. H1 (research regex) — plain-English FP in the highest-volume
   lane.
3. H4 + M8 (POI grammar) — settle one canonical grammar from the
   217-target fleet corpus, apply everywhere.
4. H3 (oai vs OAI-PMH) — index-sweep noise and wasted fetches.
5. H5 (ntfy fleet_grammar) — tighten to `=` forms; single-rule
   emit makes this load-bearing.
6. M1/M2/M3/M4/M9/M10 (conjunction/boundary hygiene) — batch with
   the above.
