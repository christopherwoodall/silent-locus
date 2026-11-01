# Candidate sheet — cryptologist lane, Transluce audit 2026-11-01

SCOUTING ONLY. No filing was made. No contact with Transluce
was made. Filings are frozen since 2026-10-08.

Full reasoning, evidence paths, and limits are in
`findings.md` in this same directory. This sheet is the
short form only. Grades: SECONDARY is the default for any
claim about who did it or why.

## Provisional candidate (1, weak)

### C1. da.gd two-spike use-shape split

Mechanism: one public shortener carries two different use
shapes in May and June 2026. Spike A (2026-05-19, 19 rows,
16 distinct codes) resolves mostly to ordinary destinations,
largest group a public statistics API host. Spike B
(2026-06-21, 17 rows, 6 distinct codes, codes repeat)
resolves mostly to echo-service base64 test pages that
decode to fixed scaffolding with a START marker. Each
segment repeats byte-identically across rows: framing
probe, not carrier. Zero zz or oai flags in all 98 rows
of the full pull.

Evidence:
- `data/lanes/sniffer-meta-20261031/raw/uq-wayback/uq-dagd-domain-FULL.json`
- `data/lanes/sniffer-meta-20261031/raw/cryptologist/FINDINGS.md`
- `data/lanes/sniffer-meta-20261031/raw/verifier/VERIFIER.md`, X4

Novelty verdict: codes already filed (all 6 June codes
and all 16 May codes appear in the filed da-gd lane's
95 shortcut records), BUT all 22 spike-day shortcut
records carry no destination value, so the destination
shapes are not filed. Tracker findings 122 (da.gd
bootstrap) and 146 (da.gd among relay services) do not
describe the echo-test shape or the destination split.

Grade: PROVISIONAL, weak, SECONDARY for any agent link.
Single-source evidence. No archive corroboration. The
May spike looks like ordinary shortening. The June spike
looks like generic echo testing. No agent action is proved.

Transluce-care line: da.gd carries two distinct use shapes
in May to June 2026 (ordinary destinations vs echo-service
base64 framing probes), neither marked with zz or oai
markers; the tracker covers da.gd as a bootstrap and relay
service, not as this use-shape split.

Coordinator call: detection note or behavior finding?
If behavior only, drop this to watch.

## Held, NOT a candidate (1)

### H1. Circled-letter host segment in a stored o-pattern copy

Shape: a circled capital letter codepoint replaces an
ASCII letter in a host segment, systematically, in the
stored live-page copy. Origin unresolved: live page or
saved copy, unproven. No signed address is reproduced
here. Re-grade only after that one check is resolved.

Evidence:
- `data/lanes/2026-10-30-o-pattern-phase2/FULL-REPORT.md`,
  sections 4 and 6

Grade: HELD. Do not file on this shape alone.

## Killed shapes (short form)

- o-pattern reader-service relay chain (reader, archive
  citation, proxy hop): tracker finding 146 plus
  submission pack 003 already name it; family verdict
  is art, not swarm. KILLED.
- o-pattern reversal plus palindrome naming: naming
  play, not concealment, per the linguist lane. KILLED.
- o-pattern three-value run-length alphabet: 860 decode
  attempts found no text; cycle-order reading untested,
  not evidence. KILLED as a candidate.
- o-pattern tone ladder (constant ratio of three):
  a single constant ratio cannot encode a message. KILLED.
- o-pattern audio carrier tests: frame and ancillary
  routes closed; coefficient and keyed-gain layers
  untested, not evidence. KILLED as a candidate.
- o-pattern UTF-16 glyph text file: byte-order mark
  is file encoding; glyph bulk undecoded, not encoded;
  no agent term, no link, no tasking. KILLED.
- o-pattern vector image path coordinates: no anomaly
  suggests encoding; untested, not evidence. KILLED.
- o-pattern large image file: size and hash only, no
  pixel analysis, no stash claim. KILLED.
- Webhook chunked dead drop (sequenced chunks plus
  terminator, plus single liveness pings): vendor-
  documented May taxonomy, already in the corpus.
  July items are name-only. KILLED.
- Dead-drop lifecycle and beacon state machine:
  tracker findings 171 and 173 plus submission pack
  003 already cover it, including topology evolution.
  KILLED.
- Topic-name-as-signal and empty-body pings: already
  in submission pack 003 (notification-topic probe
  version) and in the May probe-ping taxonomy. KILLED.
- Beacon base64 carrier URL in an inbox: already in
  submission pack 003 and tracker finding 171. KILLED.
- Relay wrapping (outer relay plus encoded inner URL
  plus filter): known relay family per the rotation
  lane; tracker finding 146 lists relay services.
  KILLED.
- Percent-encoding chains: URL transport, not a cipher
  layer; decoding yields ordinary paths and filter
  expressions. KILLED.
- Opaque base64url tags: zero printable decodes;
  opaque scan tags, not encoded text. KILLED.
- Committer footers and session trailers: vendor
  formats and squash concatenation, not a covert
  channel. KILLED.
- Zero-width and invisible characters in the October
  31 round: honest zero across all five lanes. NEGATIVE,
  not a candidate.
- October 23 webhook inbox rows and the single 2025
  not-found inbox capture: no hunt marker, dead inbox.
  KILLED.

## Open questions (carried from findings.md)

1. Detection note or behavior finding for C1?
2. Where is the brief's 2026-10-31 amapdata-topic
   message? Not found in any accessible lane; the
   October 31 rotation lane records zero archive
   captures for that topic prefix and zero last-24-hour
   notification rows, newest row 2026-10-07.
3. Resolve H1 origin (live page vs saved copy)?
4. Run a Factum match leg for C1? Barred for this
   lane under its brief; coordinator must run it.

## Files written

- `data/lanes/transluce-candidates-20261101/work/crypto/findings.md`
- `data/lanes/transluce-candidates-20261101/work/crypto/candidates.md`

No other file was written. No commit. No push.
No Factum submission. No Transluce contact.
