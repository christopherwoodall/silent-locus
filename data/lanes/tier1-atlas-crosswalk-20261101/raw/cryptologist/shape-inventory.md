# Identifier and shape inventory (shapes only, no values)

Corpus: 81 files that match `atlas_*.bin` in
`data/lanes/general-hunt/raw/0/2026-11-01T114014Z/`.
Counts are OBSERVED from first-hand bytes. Classes are SECONDARY.

## Identifier shapes

| Pattern | Total hits | Files with hits | Note |
|---|---:|---:|---|
| Hyphenated UUID shape | 3 | 3 | Task links, analytics tag. No repeat. |
| 32-hex shape | 1 | 1 | Site-verification meta tag. Name shared, value not. |
| 40-hex shape | 0 | 0 | None. |
| 64-hex shape | 0 | 0 | None. |
| 3-segment dotted shape | 1 | 1 | Script code, short segments. Not a token. |
| Long base64 shape (40+ chars) | 22 | 8 | Docs and code text. No cross-board repeat. |
| Bearer-header shape | 19 | 16 | Mostly placeholders. See below. |
| Key-assignment shape | 43 | 11 | Key, token, secret words in docs. |
| Email shape | 11 | 7 | Contact shapes in docs. No value here. |
| IPv4 shape | 2 | 1 | One file only. |
| Long path-segment shape (16+ chars) | 1390 | many | Mostly framework chunk and class names. |
| Decentralized-identifier shape | 2 hits | 2 | Identity pointers. No value here. |
| PGP block marker | 0 | 0 | None. |
| Key-block start marker | 0 | 0 | None. |

Per-file counts and shapes: `analysis.json`, field `per_file`.

## Bearer-header detail (shapes only)

- Files with a bearer-header shape: 16.
- Files where every bearer-shaped string matches a simple
  placeholder test (short, word-like, or marked as example): 13.
- Files with at least one bearer-shaped string that fails that
  simple test: 3. Those strings are still short. This does not
  prove a live key. Human context read is open. No value is given.

Files with at least one bearer-shaped string that fails the
simple placeholder test: `atlas_abund-ai.bin`,
`atlas_botnet.bin`, `atlas_vynly.bin`. Per-file bearer counts
are in `analysis.json`. The flagged set is an open question,
not a finding of a live key. No string value is given for any
of these files.

## URL and relay shapes (parameter names only, never values)

Query parameter names seen across the corpus (generic names):
`id`, `q`, `query`, `url`, `key`, `v`, `page`, `per_page`, `since`,
`sort`, `filter`, `offset`, `title`, `body`, `thread`, `room`,
`post`, `from`, `order`, `status`, `format`, `view`, `display`,
`family`, `kind`, `category`, `agent`, `limit`, `name`, `about`,
`hello`, `invite`, `wall`, `agents_only`, `drop`, `to`, `re`,
`content`, `text`, `dataset`, `public_key`, `ts`, `jti`, `sig`,
`msig`, `patron_id`, `protocol`, `verified`, `size`, `full`, `as`,
`m`.

Signed-link set (one board only): `public_key`, `ts`, `jti`, `sig`,
plus `msig`. No other board uses this set.

Hex-shaped parameter names (16 hex chars, parser artifacts from
JSON-embedded URLs): 8 distinct names, each in 1 file only.
Recorded in `analysis.json` by length and fingerprint only.

Relay-like host classes (each tied to its own board, none shared):
worker hosts, app hosts, page hosts, render hosts, fly hosts,
railway hosts, and chat-site hosts. Full host list per file is in
`analysis.json` under `multi_file_hosts` for shared hosts only.
Single-board hosts are the board's own host from the probe file.

## Encoding anomalies (all OBSERVED)

- Zero-width characters: 0.
- Byte-order mark: 0.
- Null bytes: 0.
- Invalid UTF-8: 0.
- Unicode escapes: 34. Mostly JSON escapes for `&` and `>` in
  Next.js page data. One file uses emoji code-point escapes.
- HTML entities: 243. Normal page markup.
- Percent-encoded runs of 3 or more: 1. Normal URL fragment.
- JSON-escaped host variant: 1 public standards host, in 2 files.
  Same host, escaped form. Not a second host.

## Footer and signature grammar

- Powered-by or made-with line: 1 file in last-lines scan.
- Generated or signed line: 6 hits in last-lines scan, mostly
  ordinary English, not crypto text.
- Copyright line: 5 hits.
- Closing URL line: common. Boards end with links, not signatures.
- No signature block, no key block, no checksum block in any file.

## Crosswalk document (excluded from board counts)

The crosswalk document holds signup and key-template shapes.
All are instruction templates with placeholders. They are not
board behavior. They are not counted above.
