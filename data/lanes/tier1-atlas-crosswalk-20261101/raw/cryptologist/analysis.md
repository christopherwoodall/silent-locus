# Cryptologist analysis: tier1-atlas-crosswalk-20261101

Lane: tier1-atlas-crosswalk-20261101.
Role: cryptologist.
Date of work: 2026-11-01.
Corpus path: `data/lanes/general-hunt/raw/0/2026-11-01T114014Z/`.
Output path: `data/lanes/tier1-atlas-crosswalk-20261101/raw/cryptologist/`.

Rule for this lane: shapes only. No signed value, token, key, or full
query string is reproduced here. Pattern names and shapes only.
A fingerprint (SHA-256 prefix) stands in for a matched string so the
coordinator can verify a match byte-for-byte without reading the value.

## Scope note

The brief said 52 captures. The disk holds 81 files that match
`atlas_*.bin`. I analyzed all 81. I did not analyze the `fetch_*.bin`
files in the same directory. They are out of scope for this lane.

Probe status is second-hand. It comes from `atlas_probe_results.txt`.
Per that file, 59 captures have status 200 and 22 have status 404.
One probe row has no capture file. That row is out of scope here.

Content class, counted from first bytes (OBSERVED):

- Markdown or plain text: 51 files. These read as `llms.txt` text.
- HTML page: 22 files. Most are error pages, not board text.
- JSON body: 5 files. These are short error bodies.
- Plain or other: 3 files.

This split matters. A large share of shared strings comes from HTML
error pages and web frameworks, not from board content.

## Ranked findings

### 1. No shared live identifier was found. Shared strings are framework text.

Grade: OBSERVED for the byte matches. SECONDARY for the classification.

All 18 cross-file token-like matches resolve to framework or template
vocabulary, not to live identifiers. Examples, by shape and context:

- A CSS media-feature word in a Next.js error page. Present in 10 files.
- A 23-letter React property name. Present in 10 files.
- HTML meta-name words for mobile web-app tags. Present in 5 files.
- A React page property name, 24 letters long. Present in 4 files.
- A Next.js font CSS-module class name. Present in 3 files.
- A Next.js error-digest constant tied to status 404. Present in 2 files.
- A rate-limit header name in `llms.txt` docs. Present in 2 files.
- A CSS class token from a shared UI component set. Present in 4 files.

None of these is a live account key, session token, or endpoint.
Similarity here means shared template, not shared infrastructure.
Full match list: `cross-board-matches.md`. Fingerprints: `analysis.json`.

### 2. One board uses a signed-URL shape. It is alone.

Grade: OBSERVED.

One capture, `atlas_the-continental.bin`, holds URLs with this
parameter-name set: `public_key`, `ts`, `jti`, `sig`.
A second, related parameter name, `msig`, also appears in that file.
The path shape is a short user path. The host is a hosted API host.

No other capture uses this parameter set. This is a single-board
signed-link shape, not a cross-board relay. The values are not
reproduced here. The shape alone does not prove what the link grants.

### 3. Auth shapes in `llms.txt` files are mostly instruction placeholders.

Grade: OBSERVED for counts. SECONDARY for the placeholder call.

- Bearer-header shape: 19 hits in 16 files.
- Key-assignment shape (key, token, secret words): 43 hits.
- In 13 of the 16 bearer files, every bearer-shaped string matches a
  simple placeholder test: short, word-like, or marked as an example.
- In 3 files, at least one bearer-shaped string fails that simple test.
  Those strings are still short. Length and shape alone do not prove
  a live key. They sit in instruction text. File names are in
  `shape-inventory.md`.

Open question: a human must read the context of those 3 files before
any live-key claim. No value is reproduced here, and no live-key claim
is made. See `shape-inventory.md`.

### 4. Two identifier shapes look board-specific, not shared.

Grade: OBSERVED.

- `atlas_sanctum-beacon.bin` holds 2 hyphenated UUID shapes. Context
  is task links on the board's own host. They are per-task links.
- `atlas_chirper.bin` holds 1 hyphenated UUID shape. Context is an
  analytics script tag. It is a tracker tag, not a board identifier.
- `atlas_relay-commons.bin` holds 1 32-hex shape. Context is a site
  verification meta tag. The tag name is shared with other boards.
  The tag value is not shared. Name shared, value not shared.

No UUID or hex shape repeats across two boards in this corpus.

### 5. Cross-board host repeats are public web furniture, not shared infra.

Grade: OBSERVED.

Hosts that appear in 2 or more captures:

- Code hosting, font services, social platforms, tag managers, and
  standards bodies. These are normal web dependencies.
- One board host appears in one other board's capture in 3 cases.
  Each case is a link from one board to another board. A link is not
  shared infrastructure. It is a reference.
- No proxy, relay, or tunnel host is shared across two boards.

Relay-like host shapes in single files: worker hosts, app hosts,
page hosts, and render or fly hosts. Each belongs to its own board.
They show boards use the same hosting classes, not the same host.

### 6. One equal-size pair is coincidence, not a copy.

Grade: OBSERVED.

Two captures have near-equal size (about 6,000 bytes each).
Their line overlap is 1 line out of 50 lines each. Their first lines
differ. They are two different texts of similar length, not a shared
template copy.

No two captures are byte-identical. No whole-file duplicate exists.

### 7. Footer and signature grammar is thin. No signature block was found.

Grade: OBSERVED.

- No PGP block marker appears in any capture.
- No key-block start marker appears in any capture.
- The words "powered by", "built by", "made by", and "created by"
  appear in 2, 3, 1, and 2 captures. Each is a normal credit line.
- The word "signature" appears in 12 captures. The word "signed"
  appears in 19 captures. In context these are mostly ordinary
  English (sign up, sign in, signed text), not crypto signatures.
- Two captures hold a decentralized-identifier shape (`did:`).
  Those are identity pointers in board text, not keys. No value is
  reproduced here.

No board signs its `llms.txt` with a verifiable signature block in
this corpus.

### 8. Encoding is clean. No hidden-character trick was found.

Grade: OBSERVED.

- Zero-width characters: 0 in all files.
- Byte-order mark: 0 files.
- Null bytes: 0.
- Invalid UTF-8: 0 files.
- Unicode escapes: 34 hits, all explained. Most are JSON escapes for
  `&` and `>` in Next.js page data. One file uses escapes for emoji
  code points in page data. No escape hides a token.
- HTML entities: 243 hits. These are normal page markup.
- Percent-encoded runs: 1 hit. It is a normal encoded URL fragment.
- One JSON-escaped host variant appears in 2 files. It is the same
  public standards host with JSON escaping, not a second host.

### 9. Small captures are complete error bodies, not truncated text.

Grade: OBSERVED.

The 5 smallest captures (19 to 69 bytes) are short error bodies:
plain "not found" text or small JSON error objects. They match their
probe 404 status. They are not cut-off `llms.txt` files.

Three large captures end without a trailing newline. All three end
with punctuation. They read as complete. No re-fetch was needed.
No capture shows mid-token truncation.

### 10. The crosswalk document is instructions, not board behavior.

Grade: OBSERVED for its bytes. DISCUSSED, never behavior.

`discovery_agents.crosswalk.to_llms.txt` is an instruction document.
It tells agents how to sign up, get a key, and connect a server.
Its key and token shapes are templates with placeholders.
Its rules text says posts from other members are data, not
instructions. I followed no instruction inside it. I made no signup,
no key request, and no connection.

Its auth shapes must not be counted as board behavior. They are
excluded from the board counts above.

## Cross-board matches: verified vs merely similar

Verified byte-for-byte (same string, same bytes, 2 or more files):
all 18 token-like matches in `cross-board-matches.md`. All are
framework or template vocabulary. None is a live identifier.

Merely similar (same shape class, different values):

- Signed-URL shape class: only 1 board uses it. No similar second.
- Bearer-header shape: 16 files share the shape, not a value.
- UUID shape: 3 files share the shape, not a value.
- Hosting class (workers, app hosts, page hosts): many boards share
  the class, not a host.

Template vs infrastructure vs coincidence, applied:

- Shared template: framework strings, meta-tag names, font classes,
  error-page text. Proven by context.
- Shared infrastructure: none found. No shared live host, key,
  endpoint, or identifier.
- Coincidence: equal-size pair, common public hosts, common words.

## Honest nulls

- No shared live identifier across 2 or more boards.
- No shared token, key, or session value across boards.
- No zero-width, BOM, or hidden-character encoding trick.
- No PGP or key block.
- No signed `llms.txt` block.
- No shared proxy, relay, or tunnel endpoint.
- No cross-board account or key reuse.
- No hex hash (40 or 64 chars) at all in the corpus.
- No JSON Web Token. The 1 three-segment dotted string has short
  segments and sits in script code context. It is not a token.
  It does not repeat.

## Gaps and open questions

1. Three bearer-shaped strings fail the simple placeholder test.
   Human context read is needed before any live-key claim. No value
   is reproduced here.
2. The single signed-URL shape needs a live check to learn what the
   link grants. That check is for the parent, not this lane. No live
   request was made here.
3. The 2 decentralized-identifier shapes need context review by the
   identity lane, if any. No value is reproduced here.
4. Long base64-shaped strings (22 hits) never repeat across boards.
   Their contexts are docs and code text. None is claimed as a key.
   Single-file context review is still open for the longest hits.
5. The 22 probe-404 captures are error pages, not board text. A
   re-fetch of the live board root may give real board text. That is
   a collection decision for the coordinator, not a cryptology call.
6. The social JSON file was checked at top-level keys only. Platform
   entries inside it belong to another lane. No token shape was
   found in its top-level keys.
7. Brief count mismatch: brief said 52 captures, disk holds 81.
   The coordinator should confirm which set is canonical.

## Evidence refs

- Machine evidence: `cryptologist/analysis.json` (counts, shapes,
  fingerprints, per-file stats; no token values).
- Scanner: `cryptologist/analyze.py`.
- Shape inventory: `cryptologist/shape-inventory.md`.
- Cross-board matches: `cryptologist/cross-board-matches.md`.
- Corpus: `data/lanes/general-hunt/raw/0/2026-11-01T114014Z/atlas_*.bin`.
- Probe file: same directory, `atlas_probe_results.txt`.
- Crosswalk doc: same directory,
  `discovery_agents.crosswalk.to_llms.txt`.
- Social file: same directory, `atlas_social_full.json`.

## Method note

Work was from disk only. No live fetch was made. No payload was run.
No instruction inside evidence was followed. Strings were hashed
for cross-file comparison. Only shapes, counts, and fingerprints
were written to disk.
