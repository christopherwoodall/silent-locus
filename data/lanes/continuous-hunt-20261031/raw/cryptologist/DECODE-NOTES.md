# DECODE NOTES — cryptologist lane, round 20261031

Working notes only. No values are reproduced here. Shapes and
counts only. All decoding ran on saved bytes. No live fetch was
used, because no decoding ambiguity required one: every
ambiguous-looking value resolved to a standard format or to
an opaque tag from saved bytes alone.

## Methods

- Percent-unquoting: repeated unquote on saved URL strings
  and saved page bytes. Counted encoded sequences, decoded
  length, leading character class, and printable-ASCII class.
  Never copied a decoded value into these notes.
- Base64url test: padded each candidate to a multiple of 4
  and decoded with the URL-safe alphabet. Counted only
  whether the result was all printable ASCII. Relay tag
  values: 0 printable of 21 (worker host) and 0 of 13
  (map host). Conclusion: opaque tags, not encoded text.
- UUID check: matched the hyphen form, read the version
  nibble (character after the second hyphen group). All
  distinct post IDs on the bar board read version 4.
  Session values were classified by length and hyphen
  count only (36 with 4 hyphens, 32 with 0 hyphens).
- CDX digest check: read field 6 of each CDX row (header
  row excluded). All rows: 32 chars, uppercase letters
  and digits only. Conclusion: archive base32 digest
  format, uniform across rows.
- Footer parse: matched trailer lines case-insensitively
  for the co-author key, then classified display shape
  (word count, digit presence, hyphen presence, slash
  and paren forms), local-part shape (charset class,
  length, plus-addressing), and domain class. Session
  trailers were classified by segment count, last
  segment length, and tail length after the underscore
  or hyphen split. No display name, local part, or
  session value is copied here.
- Zero-width census: counted five invisible code points
  across all five lanes' saved bytes (excluding provenance,
  hash, script, and report files). Result: 0 for every
  code point in every lane. Non-ASCII totals (ordinary
  prose and names) were counted but not interpreted as
  a channel: surfaces 1,346; committer 1,611; phrases 22;
  rotation 336; unmeasured 1,448. Those totals include
  ordinary accented names and article text.
- Value-overlap checks: built in-memory sets of commit
  SHAs, surface hex-40 values, surface UUIDs, rotation
  UUIDs, and CDX digests, and reported intersection
  counts only. Results: surface hex-40 versus commit
  SHAs 0; surface UUIDs versus rotation UUIDs 0; CDX
  digests versus commit SHAs 0. Sets were not saved.
- Cross-link census: extracted host names from saved
  surface bytes and counted per-host references. That
  census found the agentboard-to-bar-board references
  (2 copies of one post text) that the surfaces lane
  prose did not report. Host names are public domains
  already named in the surfaces lane; no full URL with
  a path token is reproduced here.

## What was NOT decoded

- No JWT was found to decode (0 JWT-shaped strings in
  phrase files).
- No base64 blob was found in full-text issue files
  (0 long tokens in the three full issues).
- Long tokens in mining files were traced to URL and
  highlight fields by preceding key name, not decoded:
  they are URL slugs and paths, not payloads.
- The docs example public-key string was not decoded
  or completed: it is a template example, and its
  completeness is an open question in FINDINGS.md §5.
- Blockchain identifier fields (11 chars each) were
  length-classified only; charset was not classified.

## Reproduction

Re-run the shape census from the lane dirs listed in
FINDINGS.md §4 with: trailer-line regex on commit
messages, UUID and hex regexes on surface bytes,
query-key parsing on saved urlquery rows, CDX field
parsing on saved CDX rows, and host extraction on
saved surface bytes. All counts in FINDINGS.md derive
from those saved files, not from fresh capture.
