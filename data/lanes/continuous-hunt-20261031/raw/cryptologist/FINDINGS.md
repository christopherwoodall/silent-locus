# CRYPTOLOGIST — continuous hunt round 20261031

Lane dir: `data/lanes/continuous-hunt-20261031/raw/cryptologist/`
Operator: BigSexyWarlock69. Method: read-only analysis of saved bytes only.
No live fetch was used. No commit, no push, no Factum write, no other
worker's files touched. No POST, no login, no session, no Shodan.
Package repos and Docker Hub out. No human identity in prose.
No human poster handles in prose. Agent and bot names appear only as
vendor and model shapes, never as personal handles.

## Rules kept in this file

Signed values, tokens, query strings, wallet values, and
credential-like strings are NEVER reproduced here. Values are
described by shape only: length, charset class, repetition, and
position. A shape match is never identity. Similarity is not
corroboration. Grades: OBSERVED means first-hand saved bytes show
the shape. SECONDARY is the default for any identity claim. No lane
claim is upgraded on pattern similarity alone.

## VERY-interesting flags

NONE. No hidden marker, encoded payload, beacon shape, or
cross-lane identifier match in this round meets a new-lead bar.
What follows is shapes, negatives, and one cross-link correction.

## 1. Shapes table

### 1a. Committer footers (committer + unmeasured lanes, saved JSON)

- Trailer grammar, OBSERVED: `Co-authored-by` (both capitalisations)
  dominates every footer lane. `Signed-off-by` is rare (single-digit
  lines in most lanes, low-double-digit lines in one lane). A footer
  line is `Display <local@domain>` with a lower-case hyphenated
  local part in vendor lines.
- Display grammar, OBSERVED, four families:
  1. Single vendor token (one word, vendor name form).
  2. Two-word vendor + model form (dominant in one lane: 401 lines
     of one display shape in 30 rows).
  3. Model-qualified slash form: vendor-slug, slash, model name
     with a digit and a short word (three variants in one lane).
  4. Parenthetical model form: vendor name, space, open paren,
     provider slash model, close paren, with a size suffix on
     some lines (dominant in one lane: 128 lines of one shape,
     47 of a second shape).
  5. Model-version form: model name, space, digit, space, one
     word (58 lines in one lane). A bot-suffixed form
     (name plus `[bot]`) carries 31 lines in the same lane.
  6. App form: two-word app display (542 lines in one lane).
- Local-part grammar, OBSERVED: short lower-alnum-hyphen vendor
  locals (5, 7, and 11 chars are the repeated lengths) versus
  plus-addressed noreply locals (numeric prefix, plus sign, login
  segment; total lengths 14 to 33 chars). Plus-addressing is the
  standard public noreply shape, not a covert channel.
- Domain grammar, OBSERVED: vendor domains, the public noreply
  domain, personal domains, and machine-local hostname domains
  (one lane carries 11 lines with a local-hostname domain, one
  lane carries 1 line with a private-IPv4-shaped domain part).
  A local hostname or private address in a committer email is a
  local-git config leak shape, not an agent marker.
- Session trailers, OBSERVED (values never reproduced):
  - One vendor session trailer: URL-shaped, 5 segments, last
    segment 32 chars = short prefix, underscore, 24-char
    mixed-case alnum tail. Count: 5 lines in one lane, 29 in
    another. Same shape in both lanes.
  - A second vendor session trailer: plain value, two forms:
    36 chars hex with 4 hyphens (21 lines) and 32 chars hex
    with no hyphens (8 lines). The two forms are consistent
    with one UUID with and without hyphens, but no row was
    shown to carry both forms, so that reading is shape-only.
  - A third vendor thread trailer: URL-shaped, 5 segments,
    last segment 38 chars mixed alnum. Count: 1 line.
  - A generic trailer with the key `Agent`: 12 lines total.
    In one lane the values are 26 chars (3 hyphens) and
    33 chars. In another lane the values are 5-char short
    tokens. Different length families under one key name.
- Repetition, OBSERVED, the lane's most important correction:
  footer lines per message run median 5 to 18 depending on lane,
  max 217 lines in one message (a 52,717-byte message). The
  distinct-to-total footer ratio per message runs median 0.07
  to 0.50. Messages are about half blank lines. That is the
  shape of squash or merge concatenation: many constituent
  commits contribute their own footer blocks. Footer LINE
  counts (for example 603 lines in 30 rows in one lane) must
  never be cited as commit counts. Repetition here is
  concatenation, not a beacon and not steganography.

### 1b. Surface identifiers (surfaces lane, saved bytes)

- Post IDs, OBSERVED: one board carries 622 UUID-shaped
  occurrences. Distinct count: 149 on the homepage, 38 on the
  tabs page, overlap 30. Every distinct value has version
  nibble `4` (UUIDv4). 38 links per file use the path shape
  `/p/<UUID>`. The rest sit in embedded script JSON with no
  nearby key. Reading: post IDs plus app payload IDs, all
  standard v4. No hidden marker shape.
- Slug tokens, OBSERVED: a second surface's sitemap carries
  36 long tokens, all distinct, lengths 33 to 56 chars,
  under two path templates (a use-cases template with 23
  rows, a blog template with 11 rows). Length varies with
  word count. Reading: SEO slugs, not encoded payloads.
- Long-token census, OBSERVED: the first board also carries
  748 long-token (32-plus chars) occurrences, mostly in
  embedded script JSON, and 12 hex-64 occurrences on the
  homepage. Those are asset and payload hash shapes, not
  agent identifiers. One distinct hex-40 value occurs twice
  on the same homepage.
- Agent-card schema, OBSERVED (field names and lengths only):
  one surface's well-known agent-card JSON carries version
  shape `0.16.0`, two security schemes (a signature scheme
  and a payment scheme), a payment block with fields of
  lengths 4, 5, 14, and 4 chars, three blockchain identifier
  fields of 11 chars each, integer chain IDs, and empty
  contract strings. Its endpoint map carries 41 keys with
  URL string lengths 26 to 68. Its docs also carry a
  heartbeat document. These are schema shapes, not live
  secrets. No wallet value, signature, or credential value
  is reproduced here.
- Protocol version strings, OBSERVED: one board's machine
  doc carries a protocol string of shape `word/0.1` (2
  occurrences). One identity surface's machine doc carries
  a protocol string of shape `word/0.0` (1 occurrence).
  The other three surfaces carry no such string in their
  machine docs. Short, versioned, plain-text protocol tags.
- Docs example, OBSERVED: one board's pages repeat a docs
  code block with a placeholder host, an example public-key
  string in a named curve format, and an example timestamp.
  The block is a template, not a live credential. Whether
  the example key string is complete or a truncated
  placeholder in source bytes is an open question (see §5).
- Percent-encoding, OBSERVED: one surface homepage carries
  20 percent-encoded sequences, a second carries 12, a
  third carries 3. Decoded from saved bytes, the first
  surface's fragments are 26 to 27 chars, slash-leading,
  printable ASCII, no spaces: ordinary URL path encoding.
  The third surface's fragments decode to 6-char printable
  fragments. No decoded payload, no hidden text.
- Board-name grammar, OBSERVED: one board's boards are
  short lower-case single words. No encoded board names.

### 1c. Urlquery rows (rotation lane, saved JSON)

- Relay tag, OBSERVED: one worker-hosted relay family
  carries a single query key on 21 rows, values
  alnum-hyphen-underscore, lengths 21 to 36 chars.
  Base64url decoding of all 21 values from saved bytes
  yields 0 printable decodes. Reading: opaque scan tags,
  not encoded text.
- Map-service tag, OBSERVED: a second family on a map
  host carries two query keys on 8 rows: a 10-char uniform
  identifier key and a tag key of 10 to 14 chars. Same tag
  key name as the relay family, shorter length family,
  different host. Shared key name only (see verdict V3).
- Frame tag, OBSERVED: one row in the frame file carries
  the frame key with a 15-char alnum-hyphen-underscore
  value. The other rows in that file carry no such key
  in their submitted URLs: content-match rows, not
  frame-tagged submissions.
- Search-noise proof, OBSERVED: in the `zz` file, 0 of
  the scanned submitted URLs carry a `zz` key. One row
  carries generic analytics keys (a vendor tracker
  prefix, a client identifier, a product identifier, a
  location key, and an equipment key). That is tracker
  grammar, not hunt grammar, and it confirms the lane's
  content-match-noise reading.
- Dead-drop address grammar, OBSERVED: dead-drop rows
  use first path segments of three shapes: UUID-hyphen
  36 chars (3 rows), 14-char alnum-hyphen-underscore
  (2 rows), and a 6-char two-segment shape (1 row).
  Reading: UUID inbox versus short alias inbox, no hunt
  marker in the shapes themselves.

### 1d. Wayback CDX rows (rotation lane, saved JSON)

- Relay invocation, OBSERVED: one relay host's file
  carries 100 rows plus a header row. 74 rows carry the
  key pair (filter key, URL key). The URL value is a
  percent-encoded inner URL. 14 rows are double-encoded
  (an encoded percent sign survives the first decode).
  Filter values run 21 to 100 chars and contain
  non-alnum characters: filter-expression syntax, not
  opaque tokens.
- Inner-host chain, OBSERVED (hosts only, no full URLs):
  the inner hosts are led by a shortener host (26 rows),
  a public proxy host (16 rows), the archived shortener
  host itself (9 rows), a government investor host
  (8 rows), a public CORS host (8 rows), an archive host
  (4 rows), and a notes host (3 rows), plus singletons.
  Inner path segment counts run mostly 1 (55 rows).
  Reading: outer relay, inner target, filter applied.
  This is the known relay family shape, prior art per
  the rotation lane, not a new shape.
- Singleton keys, OBSERVED: one shortener file carries
  an uppercase injection-shaped key on 2 rows (1-segment
  path, 2026 captures, statuses 301 and 200). One CORS
  file carries an uppercase novel-shaped key on 1 row
  (5-segment path, 200). Singletons are not a grammar
  family. No pattern claim is made for either key.
- Asset tree, OBSERVED: one notification-host file
  carries 80 three-segment paths under a 6-char first
  segment. Third segments are static asset extensions
  (font 24, style 12, image 12, script 11, vector 9,
  icon 6, audio 6). Reading: a static site asset tree,
  not topic paths. No topic-shaped path was found.
- Digest shape, OBSERVED: every CDX row carries a
  32-char uppercase-digit digest (base32 shape). That
  is the archive's content digest format, uniform
  across all rows, not an agent marker.
- Dead inbox, OBSERVED: the single-inbox file carries
  1 capture row, status 404, dated 2025. Dead shape,
  nothing new.

### 1e. Phrase tokens (phrases + unmeasured lanes, saved JSON)

- Snake-case telemetry family, OBSERVED: two lanes share
  one naming grammar — lower-case words joined by
  underscores, 2 to 4 segments, plus one dot-joined
  variant and one slash-joined triple. Members include
  delegation verbs, tool-call nouns, capability nouns,
  and rule nouns. The same grammar covers both lanes'
  tokens, but the stems differ per token. Grammar is
  shared; tokens are not shared (see verdict V9).
- CamelCase class triple, OBSERVED: one token is a
  slash-joined triple of CamelCase names sharing one
  suffix word. That is a protocol or telemetry class
  naming shape, not three separate findings.
- Prose vocabulary, OBSERVED: hyphenated and spaced
  agent phrases (agent-created, agent-to-agent, agent
  card, agent loop, fleet of autonomous agents) are
  discussion vocabulary, not identifiers. They carry
  no length, charset, or position marker.
- Self-disclosure sentences, OBSERVED as search hits
  only: the "I am X" family (model names and one
  autonomy variant) has title-match 0 in most lanes.
  A search hit is not a verified disclosure. No
  disclosure finding follows from shape alone.
- Honest null, OBSERVED: one combined three-token
  string returns 0 rows on two surfaces (issue search
  and code search). That null covers that exact
  combination only, not each token alone.
- No encoded payloads, OBSERVED: 0 JWT-shaped strings
  in all phrase files. 0 long tokens in the three
  full-text issue files. Long tokens in mining files
  (404 in one file group) sit in URL and highlight
  fields: URL slugs and paths, lengths 40-plus chars.
  No base64 blob decodes to text in the full texts
  checked.

## 2. Cross-lane pattern verdicts

- V1. Footer repetition is NOT a beacon. The repetition
  shape (median distinct ratio 0.07 to 0.50, half blank
  lines, max 217 lines in one message) matches squash
  or merge concatenation. No repetition-based beacon
  claim survives. Grade: OBSERVED shape, INFERENCE
  for the concatenation reading.
- V2. Same session shape is NOT the same session. The
  URL-shaped session trailer has identical segment and
  length shape in two lanes (5 segments, 32-char last
  segment, 24-char tail). That is one vendor's format,
  not one session. No cross-lane session identity is
  claimed. Grade: OBSERVED shape, SECONDARY identity
  (not established).
- V3. Same query key is NOT the same tag family. The
  relay tag key appears on a worker host (21 to 36
  chars) and on a map host (10 to 14 chars, beside a
  uniform 10-char identifier key). Different length
  families, different hosts, different companion keys.
  The key name alone does not merge the families.
  Grade: OBSERVED.
- V4. UUID shape is NOT an identifier link. UUIDs
  appear as post IDs (v4, 149 plus 38 distinct), inbox
  addresses (36-char hyphen form), and session values
  (36-char hyphen form and 32-char plain form). Value
  overlap checks return 0: surface UUID set versus
  rotation UUID set share no value, and surface hex-40
  values share no value with commit SHAs. Same grammar,
  different roles, no shared value. Grade: OBSERVED
  (counts), SECONDARY for any identity (not found).
- V5. Relay host reuse is NOT an actor link. One
  shortener host appears both as an archived prefix
  and as an inner host in 9 relay rows. One notes host
  appears as an inner host (3 rows) and matches the
  known nested-relay-URL shape family. Host reuse
  across roles is prior-art relay topology, not proof
  of one actor. Grade: OBSERVED shape, SECONDARY
  identity (not established).
- V6. Agentboard to swarmbar cross-link: OBSERVED, and
  it CORRECTS the surfaces lane. The surfaces lane
  reports no cross-link to another board seen for
  agentboard. Saved bytes show 2 references to the
  swarmbar domain in one post text (homepage and feed
  copies of the same post), describing the board as a
  bar with a plain API and MCP access. Verdict: a real
  descriptive cross-link exists. It is a mention, not
  coordination evidence. No poster handle is named
  here. Grade: OBSERVED for the link, SECONDARY for
  any coordination reading (not supported).
- V7. Shared third-party link is NOT board coordination.
  One project domain appears on three boards (the
  bar board, the agentboard, and the fallback board).
  A shared project link is a shared reference, not a
  shared actor or a coordinated act. Grade: OBSERVED.
- V8. Payment mechanism family is prior art, phrase
  is new. The identity surface's payment scheme shape
  and the phrases lane's wallet experiment phrase
  belong to one payment-mechanism family already
  recorded in prior lanes. The phrase string is new
  to the sweep; the mechanism is not. No novelty is
  claimed for the mechanism. Grade: SECONDARY.
- V9. Snake-case grammar is one code-naming family,
  not one harness fingerprint. The same underscore
  grammar covers delegation, tool-call, capability,
  and rule tokens across two lanes. Only one token
  in the set carries a low-collision search signal
  (smallest token total by two orders of magnitude
  in its lane, with exact-title hits). That token is
  a search signature for harness telemetry leaks, not
  an identity marker. The rest of the family is
  generic code vocabulary. Grade: OBSERVED grammar,
  SECONDARY identity (not established).
- V10. No cross-lane identifier, grammar, or shape
  in this round ties two lanes to one actor. Shared
  shapes found are vendor formats (footers, session
  URLs, UUIDs, noreply addresses), archive formats
  (CDX digests), protocol formats (agent-card schema,
  version tags), and public code grammar (snake-case
  tokens). None of those is actor evidence on its own.

## 3. What did NOT hide anything

- Zero-width and invisible characters: 0 occurrences of
  zero-width space, zero-width non-joiner, zero-width
  joiner, byte-order mark, or word joiner in every
  lane's saved bytes (surfaces, committer, phrases,
  rotation, unmeasured). No invisible-character channel.
- Encoded text: 0 printable base64url decodes among
  relay tag values (21 plus 13 values tested), 0 JWT
  shapes in phrase files, 0 base64 blobs in full-text
  issues, 0 printable decodes among the relay tag
  family. Percent-decoding yields only ordinary URL
  path fragments.
- Hidden board or protocol: no new board, no new
  protocol version, and no new activity burst hides in
  the surface bytes beyond what the surfaces lane
  already reports (one board active, one board fresh,
  one board unobservable, one board quiet, one
  candidate baselined). The agent-card surface's
  endpoint map is public schema, not a hidden board.
- Hidden dead-drop or relay activity: no new captures
  in the recent window on any checked dead-drop or
  relay domain; the relay rows found are old captures
  of the known family. The asset-tree file hides no
  topic paths. The singleton query keys hide no family.
- Hidden self-disclosure: the "I am X" search hits
  hide no verified disclosure (title-match 0 in most
  lanes). The combined three-token string hides
  nothing: honest null on two surfaces.
- Hidden wallet or credential: no live wallet value,
  signature, token, or credential-like string was
  found in the findings-grade bytes reviewed. Docs
  examples and schema fields are templates and
  lengths, not live values. Nothing in this file
  reproduces one.

## 4. Evidence paths (this round only)

- Surfaces captures: `data/lanes/continuous-hunt-20261031/raw/surfaces/`
  (homepage, llms, skill, sitemap, feed, tabs, stats,
  well-known docs, agent-card JSON, heartbeat).
  Cross-link correction source: `agentboard.ai/feed.xml`
  and `agentboard.ai/homepage.html` (same post text,
  two copies).
- Committer captures: `data/lanes/continuous-hunt-20261031/raw/committer/`
  (`gh-commits-*.json`, `gh-prs-*.json`). Session
  trailers: aider and gemini commit files, copilot
  second-pass file, jules commit file.
- Unmeasured captures: `data/lanes/continuous-hunt-20261031/raw/unmeasured/`
  (`gh-commits-codex.json`, `phrase-*.json`).
- Rotation captures: `data/lanes/continuous-hunt-20261031/raw/rotation/`
  (`uq_*.json`, `uq2_*.json`, `cdx_*.json`).
  Relay shape source: `cdx_jqp_vercel_app.json`.
  Tag shape sources: `uq_uqscan.json`,
  `uq2_amap_uqscan.json`, `uq_uqframe.json`, `uq_zz.json`.
- Phrases captures: `data/lanes/continuous-hunt-20261031/raw/phrases/`
  (`gh_sweep_*.json`, `hn_sweep_*.json`, `hn_mine_*.json`,
  `gh_issue_*.json`).
- This lane: `data/lanes/continuous-hunt-20261031/raw/cryptologist/FINDINGS.md`,
  `DECODE-NOTES.md`.

## 5. Open questions

1. Is the agentboard post that mentions the bar board
   the same post family as the bar board's own post
   that mentions a third board? A board-mention graph
   (board A mentions board B, board B mentions board
   C) would map mention topology. Mention topology
   is still not coordination evidence.
2. Is the 217-footer message a squash of many commits
   or a duplicated footer block? Its subject-line
   structure was not classified in this pass. Either
   reading keeps V1: repetition is structural, not a
   beacon.
3. Do any rows carry BOTH session forms (36-char
   hyphen and 32-char plain) for one session? If no
   row pairs them, the two forms may be two ID
   generations, not one UUID stripped of hyphens.
4. Are the two singleton query keys (injection-shaped
   key, novel-shaped key) probe keys, test URLs, or
   one-off markers? Singletons cannot answer that.
   No pattern claim should be built on either.
5. What is the charset of the three 11-char blockchain
   identifier fields in the agent-card JSON? Length
   only was classified in this pass.
6. Is the docs example public-key string complete or
   a truncated placeholder in source bytes? The
   finding-grade answer (template, not live value)
   does not depend on it, but the next surface pass
   should record it as template versus complete.
7. Do the map-host tag values (10 to 14 chars) and
   the worker-host tag values (21 to 36 chars) share
   a generator with different parameters, or two
   unrelated generators? Length families alone cannot
   settle it, and no value comparison is offered here
   as identity evidence.
