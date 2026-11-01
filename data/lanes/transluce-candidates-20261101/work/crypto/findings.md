# Cryptologist findings — Transluce submission-candidate audit, 2026-11-01

Scope: hidden, encoded, and relay shapes only. Behavior or technique
(TTP) candidates only. String matches do not count.

Status: SCOUTING ONLY. No filing was made. No contact with Transluce
was made. Transluce filings are frozen since 2026-10-08.

Method: read-only reads of saved lane files. No live fetch was made.
No payload was run. No instruction inside evidence was followed.
No POST, no login, no new session, no Shodan search was made.
No file outside the work directory named below was written.
The in-flight crosswalk lane was not touched. The Factum database
and the records tree were not touched.

Work directory (only write location):
`data/lanes/transluce-candidates-20261101/work/crypto/`

Grades used here:
- OBSERVED: the byte shape is present in a saved file.
- SECONDARY: the default grade for any claim about who did it or why.
- PROVISIONAL CANDIDATE: the mechanism is not in the tracker or the
  filed corpus in this form, but the agent link is not proved.
- KILLED: the shape is already in the corpus or the tracker, or it
  is not a covert or agent mechanism on the evidence in hand.
- HELD: the shape needs one more check before any verdict is safe.

Terms, defined on first use:
- Relay: a service that fetches a target page for the requester and
  returns a copy. The requester hides behind the relay host.
- Dead drop: a public inbox where a program leaves data for later
  pickup. The inbox itself holds no secret. The signal is the
  pattern of posts.
- Framing probe: a test page that shows a marker so the tester can
  see that a relay or echo path works. It carries no per-message
  secret.
- Carrier: a channel that carries a different message in each use.
  A carrier must vary per message. A fixed test page is not one.

## Headline verdict

One provisional candidate survives. It is weak. Everything else in
this lane is killed, held, or an honest negative.

The provisional candidate is the da.gd two-spike use-shape split
(see section 1). Its weakness is stated plainly: the echo-test
shape is generic public test scaffolding, and no agent link is
proved for either spike. The candidate is a use-shape distinction
for a known shortener family, not a new toolkit and not proof of
agent action.

No o-pattern shape survives as a candidate. The o-pattern family
is graded in its own lane as generative art with a negative swarm
finding, and its relay use is already filed in a different family
(see section 2).

No dead-drop shape survives as a candidate. The dead-drop
lifecycle is already in the Transluce tracker and in a prior
submission pack (see section 3).

No encoding shape from the last two weeks survives as a candidate.
The most recent round records an honest zero for invisible
characters, and the percent and base64 shapes found are transport
encoding or generic relay wrapping, not a covert channel
(see section 4).

## 1. da.gd two-spike use-shape split — PROVISIONAL CANDIDATE (weak)

Mechanism: one public shortener carries two different use shapes
in May and June 2026.

- Spike A, 2026-05-19: 19 rows, 19:08 to 21:48 UTC, 16 distinct
  submitted short codes. Most rows resolve to ordinary
  destinations. The largest destination group is a public
  statistics API host (14 of 19 rows). Only 2 of 19 rows use an
  echo-service base64 path.
- Spike B, 2026-06-21: 17 rows, 00:00 to 11:37 UTC, 6 distinct
  submitted short codes, so codes repeat. Thirteen of 17 rows
  use an echo-service base64 path. The decoded pages are test
  scaffolding: style, preformatted, division, iframe, and script
  elements, with a START marker in two of three segment forms.
  Each segment repeats byte-identically across its rows. No
  per-row payload varies. That is a framing probe, not a carrier.
- Both spikes: zero zz-parameter flags and zero oai-token flags
  in all 98 rows of the full pull. The da.gd family stays
  separate from the oai and zz family. That separation is
  already established in prior lanes.
- Timing shape inside spike B: 8 rows resolve to the same echo
  host shape within about two minutes in the late morning
  cluster. The full day runs from just after midnight to late
  morning, so the day as a whole is not one minute burst.

Evidence paths:
- `data/lanes/sniffer-meta-20261031/raw/uq-wayback/uq-dagd-domain-FULL.json`
  (98 rows, full pull)
- `data/lanes/sniffer-sweep-20261031/raw/urlquery-wayback/uq-odd-dagd-domain.json`
  (30-row saved subset; same June 21 cluster of 17 rows)
- `data/lanes/sniffer-meta-20261031/raw/cryptologist/FINDINGS.md`
  (full decode from the final-path copy after percent-unquoting;
  framing-probe verdict)
- `data/lanes/sniffer-meta-20261031/raw/verifier/VERIFIER.md`,
  section X4 (two-spike restatement; May 19 is the largest day)

Novelty check (run for this audit, counts only, no code values
reproduced):
- The filed da-gd lane holds 95 shortcut records. All 6 distinct
  June 21 codes and all 16 distinct May 19 codes already appear
  there. Sixty-seven of 70 distinct codes in the full 98-row
  pull already appear there.
- BUT: all 22 shortcut records for the two spike days carry no
  destination value. The filed lane records the codes, not the
  destination shapes. The echo-test shape and the ordinary
  destination shape are not in the filed lane.
- Tracker check: Transluce finding 122 describes a
  bootstrapping script that loads program pieces through
  da.gd-shortened links. Finding 146 lists da.gd among reader
  and relay services in a campaign relay chain. Neither
  finding describes an echo-service base64 test page, a START
  marker page, or a statistics-API destination spike. The
  destination-shape split is not in those findings.
- Limit: this is single-source evidence (one search service).
  The archive leg adds no corroboration: the shortener domain
  archive query returned a capped, host-ordered slice, not a
  burst distribution.

Grade: PROVISIONAL CANDIDATE, weak, SECONDARY for any agent link.
The mechanism distinction is new in this form. The agent link
is not proved. The May spike looks like ordinary shortening.
The June spike looks like generic echo testing, which any
tester can do. A filing on this shape must say that plainly
and must not claim agent action.

Transluce-care line: da.gd carries two distinct use shapes in
May to June 2026 (ordinary destinations vs echo-service base64
framing probes), neither marked with zz or oai markers; the
tracker covers da.gd as a bootstrap and relay service, not as
this use-shape split.

Open question for the coordinator: does the tracker want a
detection note (how to tell probe traffic from ordinary
shortening) rather than a behavior finding? That is a scope
call, not a crypto call.

## 2. o-pattern relay-jina-reader family — KILLED as a candidate

Mechanism examined: pages read through a public reader service,
in both plain and secure forms, with an archive citation service
used to reference captures, and one unreproduced trace through
a commercial CORS proxy to the reader service.

Why it is killed:
- The reader-as-relay mechanism is prior art in the tracker
  and in a prior submission pack. Tracker finding 146 lists
  reader services among campaign relay services. Submission
  pack 003 (dead-drop family) already documents a loader that
  fuses reader-service laundering with a probe and a dead drop.
  The o-pattern use adds no new relay step: reader, archive
  citation, and proxy hop are all already named.
- The o-pattern family's own verdict is negative for swarm
  behavior. Its lane grades the family as generative art with
  a mirrored glyph vocabulary, no agent term, no fleet term,
  no tasking text, and no beacon pattern in any examined
  asset. A relay shape on art pages is not agent tradecraft.
- The CORS proxy hop is unreproduced. The March 2026 trace
  rests on a prior corpus snapshot only. An unreproduced hop
  cannot carry a candidate.
- The archive re-census found no new captures after
  2026-10-27 in 24 of 26 query forms. Two forms were
  inconclusive (repeated backend errors), not evidence of
  activity. Absence in the archive does not prove absence
  of live activity, since the live pages were up on
  2026-10-30.

Evidence paths:
- `data/lanes/2026-10-30-o-pattern-phase2/FINDINGS.md`
- `data/lanes/2026-10-30-o-pattern-phase2/FULL-REPORT.md`
- `data/lanes/2026-10-09-transluce-intel/submissions/003-deaddrop-family/README.md`
  (loader fusion: reader laundering plus probe plus dead drop)

Grade: KILLED. Overlap, not a candidate.

### 2a. o-pattern encoding shapes — all KILLED or HELD

Reversal plus palindrome naming:
- Host stems pair a reversed English stem with its forward
  form, plus fully palindromic stems. The linguist lane
  already weakened the concealment reading to play: paired
  forward and reverse forms printed side by side undercut
  pure concealment. This is naming play, not a covert
  channel. KILLED.

Three-value run-length alphabet (visible emoji layer):
- Each page row is a palindrome of the form N plus 1 plus N,
  with only three distinct row shapes per page. One row
  carries one number, not a full bit row. Eight hundred and
  sixty decode attempts found no text. The cycle-order
  reading (the order of row-shape choices across cycles)
  is untested, and a keyed mapping over a three-value
  alphabet is unfalsifiable without a key. An untested
  residual is not a candidate. KILLED as a candidate;
  the cycle-order gap stays open in the o-pattern lane.

Tone ladder (powers of three):
- A calculator state defines tones at a constant ratio of
  three, and one audio file matches seven of those tones
  exactly. A single constant ratio with no varying
  parameter cannot encode a message. This is a sound-art
  parameter, not an encoding. KILLED.

Audio file carrier tests:
- Frame parsing ends exactly at end of file for both
  audio files. No appended data, no metadata payload.
  Ancillary data is deterministic encoder stuffing. The
  amplitude channel was decoded and failed cleanly.
  Coefficient-level embedding and keyed gain encodings
  are untested. An untested layer is not evidence of a
  stash. KILLED as a candidate; the test gap stays open
  in the o-pattern lane.

Glyph text file:
- The text file is encoded as UTF-16 with a byte-order
  mark, 403 lines, line-level palindrome, with eight
  readable definition-style sentences about glyphs and
  wavelength. The byte-order mark is a file encoding,
  not a covert channel. The glyph bulk is undecoded.
  Undecoded is not encoded. The file holds no agent
  term, no link, and no tasking text. KILLED as a
  candidate; the glyph-bulk decode gap stays open.

Image path-coordinate encoding:
- The vector image is a confirmed calculator export of
  the same woven-star artwork. No anomaly in path
  counts, ranges, or groupings suggests encoding, and
  coordinate steganography was not tested. No anomaly
  plus no test equals no candidate. KILLED.

Large image file:
- A 62 MB image file was verified by format, size, and
  hash only. No pixel-level analysis was performed.
  Size alone is not a stash claim. KILLED as a
  candidate; the pixel gap stays open in the o-pattern
  lane.

### 2b. Circled-letter host segment in a stored copy — HELD

Shape OBSERVED in the o-pattern phase-2 report: the stored
live-page copy uses a circled capital letter codepoint in
place of an ASCII letter in a host segment, systematically
(121 occurrences in the stored copy, zero plain-ASCII
occurrences of that host form).

Why it is held, not filed:
- The report itself leaves open whether the live page as
  served holds this form or whether the saved copy
  introduced it. That question is unproven.
- A homoglyph substitution in a host string is a known
  obfuscation shape in general, but a single stored-copy
  observation with an unresolved origin cannot carry a
  candidate. No live re-check is owed from this lane,
  and no signed address is reproduced here.
- If a coordinator resolves the origin to the live page,
  this shape should be re-graded. Until then it is an
  open observation, not a candidate.

Evidence path:
- `data/lanes/2026-10-30-o-pattern-phase2/FULL-REPORT.md`,
  sections 4 and 6 (host-segment observation, mechanism
  unclaimed)

Grade: HELD. Do not file on this shape alone.

## 3. Webhook dead-drop and ntfy topic shapes — KILLED as candidates

### 3a. Chunked dead-drop exfiltration — KILLED (prior art)

Mechanism: a program posts compressed and base64-encoded
page-scrape chunks to a web-hooks endpoint, in sequenced
path segments with a terminator segment that carries the
total length, plus single liveness pings that carry only an
epoch marker and no scrape target.

Why it is killed:
- The mechanism is documented by an external vendor report
  and is already in the corpus with a full taxonomy: four
  chunk grammars plus two probe pings, all dated to the
  May wave. The July webhook-named items are name-only
  candidates with no payload bytes. Name alone is not a
  mechanism.
- The lifecycle reading (probe, then chunked exfiltration,
  then terminator) is the documented taxonomy itself, not
  a new observation. A lifecycle that is already written
  down cannot be filed as new.
- The tracker already covers dead-drop families at the
  mechanism level (see 3b). This shape adds nothing the
  tracker lacks.

Evidence paths:
- `data/lanes/webhook-deaddrops/events.jsonl` (taxonomy
  record: four chunk grammars plus two probe pings)
- `data/lanes/webhook-deaddrops/PROVENANCE.md` (bounded
  sweep, closed 2026-09-28; footprint is May plus July
  name-only items)

Grade: KILLED. Overlap, not a candidate.

### 3b. Dead-drop lifecycle as a TTP — KILLED (tracker-covered)

Mechanism: multi-stage beacon state machine (boot, then
initialization steps, then capture repeats, then error
repeats, then done), with evolving exfiltration topology
across probe versions (notification topic only, then
notification topic plus webhook inbox plus a robots-file
beacon, then reader-service laundering fused with a probe
and a dead drop).

Why it is killed:
- Tracker finding 171 already documents a live webhook
  inbox dead-drop family with a multi-stage beacon state
  machine and evolving exfiltration topology. Finding
  173 is its follow-up. Submission pack 003 already
  packages the same topology evolution, including the
  notification-topic version, the triple-exfiltration
  version, and the reader-laundering loader version.
- A lifecycle candidate must add a stage, a transition,
  or a topology the tracker lacks. This audit found none.
  The single-inbox archive capture from 2025 returning
  not-found is a dead inbox, not a new stage. The
  October 23 webhook inbox rows in the October 31
  rotation lane show no hunt marker and sit outside
  the last-24-hour slice.

Evidence paths:
- `data/lanes/2026-10-09-transluce-intel/raw/finding-171_*.json`
  (live dead-drop family, beacon state machine)
- `data/lanes/2026-10-09-transluce-intel/raw/finding-173_*.json`
  (follow-up)
- `data/lanes/2026-10-09-transluce-intel/submissions/003-deaddrop-family/README.md`
  (topology evolution across probe versions)
- `data/lanes/continuous-hunt-20261031/raw/rotation/FINDINGS.md`,
  slices 1 and 2 (October 31 rotation: no new dead-drop
  captures in the recent window)

Grade: KILLED. Tracker-covered, not a candidate.

### 3c. Topic-name-as-signal and empty-body pings — KILLED, with one open item

Mechanism examined: a notification service topic name used
as the signal itself, so that a post to the topic needs no
body to mean something, plus empty-body pings as liveness
checks.

Why it is killed as a new candidate:
- Topic-as-signal is already the version history in
  submission pack 003: an early probe version exfiltrates
  through a notification topic plus a robots-file beacon,
  with no webhook inbox. The shape is filed, not new.
- Empty-body liveness pings are already the May probe
  pings in the dead-drop taxonomy (section 3a): a single
  ping, no scrape target, epoch marker in the path.
  The ping stage is filed, not new.
- The October 31 rotation lane records zero archive
  captures for the amapdata topic prefix and zero
  last-24-hour notification-service rows. The newest
  notification-service rows in that lane are dated
  2026-10-07 and are content-match noise pointing at
  paste-style hosts, not at notification topics.

Open item, stated honestly:
- The brief for this audit mentions a 2026-10-31 message
  on an amapdata topic. No message dated 2026-10-31 on
  that topic was found in any accessible lane. The
  October 31 date matches the rotation lane retrieval
  date, not a message date in that lane. The closest
  corroborated items are the October 6 to 7 probe
  reports already in submission pack 003. If the
  brief's message lives in a lane this worker was
  barred from, the coordinator must point to it
  directly. Do not file on the brief alone.

Evidence paths:
- `data/lanes/continuous-hunt-20261031/raw/rotation/cdx_ntfy_sh_amapdata.json`
  (empty result set)
- `data/lanes/continuous-hunt-20261031/raw/rotation/uq_ntfysh.json`
  (24 rows, newest 2026-10-07, content-match noise)
- `data/lanes/continuous-hunt-20261031/raw/rotation/FINDINGS.md`,
  slices 1 and 2
- `data/lanes/2026-09-28-chinese-amap-fleet/METHODOLOGY.md`
  (notification topic treated as a marker slug in the
  cross-archive presence sweep)

Grade: KILLED as a new candidate. The open item above
is unresolved, not a candidate.

### 3d. Beacon carrier URL shape — KILLED (tracker-covered)

Mechanism: a beacon carries a base64 carrier URL pointing
at a public echo service, so the beacon payload rides in
a URL the inbox receives rather than in a body field.

Why it is killed: submission pack 003 and tracker
finding 171 already describe beacons carrying an echo
base64 carrier URL as part of the dead-drop family.
The carrier-in-URL shape is filed. A repeat of the
same shape in another beacon set would be a new
sighting, not a new mechanism, and this audit found
no new sighting with agent attribution.

Grade: KILLED. Overlap, not a candidate.

## 4. Encoding and relay shapes from the last two weeks — KILLED or NEGATIVE

All items below were checked against lanes dated from
2026-10-18 onward, plus the October 31 rounds. No shape
here is both new and agent-attributed.

Zero-width and invisible characters — HONEST NEGATIVE:
- The October 31 continuous round counted five invisible
  codepoints across all five of its lanes' saved bytes:
  zero occurrences of each. No invisible-character
  channel hides in that round. That negative is itself
  the finding. It kills any claim of a zero-width
  channel in the recent window on this evidence.

Evidence path:
- `data/lanes/continuous-hunt-20261031/raw/cryptologist/FINDINGS.md`,
  section 3, and `DECODE-NOTES.md` (zero-width census)

Percent-encoding chains — KILLED (transport, not cipher):
- Two layers appear and both resolve to transport.
  First, da.gd echo segments are percent-encoded, then
  base64-decoded. Raw base64 decode of the encoded form
  gives garbage; decode after percent-unquoting gives
  clean test scaffolding. The percent layer is URL
  transport, not a second cipher layer.
  Second, relay invocation rows carry a percent-encoded
  inner URL, sometimes double-encoded (an encoded
  percent sign survives the first decode). Decoding
  yields ordinary inner hosts and filter expressions,
  not hidden text.
- The October 31 continuous round likewise found that
  percent-decoding on surface pages yields only
  ordinary URL path fragments.

Evidence paths:
- `data/lanes/sniffer-meta-20261031/raw/cryptologist/FINDINGS.md`,
  section 1 (percent-unquoting step)
- `data/lanes/continuous-hunt-20261031/raw/cryptologist/FINDINGS.md`,
  sections 1b and 1d (percent fragments, double-encoded
  relay rows)

Relay wrapping (outer relay plus encoded inner URL plus
filter) — KILLED (prior art):
- One relay host's archive file carries 100 rows, 74
  with a filter-plus-URL key pair, 14 double-encoded.
  Inner hosts are led by a shortener host, a public
  proxy host, the archived shortener host itself, and
  public CORS and archive hosts. The rotation lane
  itself calls this the known relay family shape.
  Tracker finding 146 already lists relay services in
  a campaign relay chain. Wrapping an inner URL in an
  outer relay with a filter is the filed topology,
  not a new shape.
- One da.gd file row resolves through a wrapper relay
  service carrying an encoded inner short link plus a
  filter expression. Same shape, single row. A
  singleton is not a grammar family.

Evidence paths:
- `data/lanes/continuous-hunt-20261031/raw/cryptologist/FINDINGS.md`,
  section 1d
- `data/lanes/continuous-hunt-20261031/raw/rotation/FINDINGS.md`,
  slice 2
- `data/lanes/sniffer-sweep-20261031/raw/cryptologist/cryptologist-review.md`,
  da.gd section (wrapper relay row, shape only)

Opaque base64url tags — KILLED (opaque, not encoded text):
- Relay tag values on a worker host (21 values, 21 to
  36 chars) and on a map host (13 values, 10 to 14
  chars) decode to zero printable results under the
  base64url alphabet. Different length families on
  different hosts with a shared key name do not merge
  into one family. Opaque scan tags are not encoded
  text. No candidate follows.

Evidence path:
- `data/lanes/continuous-hunt-20261031/raw/cryptologist/FINDINGS.md`,
  section 1c, and `DECODE-NOTES.md` (base64url test)

Committer footers and session trailers — KILLED (vendor format):
- Footer repetition in commit messages matches squash
  or merge concatenation (median distinct-to-total
  ratio 0.07 to 0.50, half blank lines, one message
  with 217 footer lines). Repetition here is
  structural, not a beacon and not steganography.
- Session trailer shapes repeat across lanes in
  identical segment and length form. That is one
  vendor's format, not one session and not a covert
  channel. No cross-lane session identity is claimed.

Evidence path:
- `data/lanes/continuous-hunt-20261031/raw/cryptologist/FINDINGS.md`,
  sections 1a, 2 (verdicts V1 and V2)

Discovery-probe shape (well-known agent-card endpoint) — NOT
GRADED HERE as a crypto candidate:
- One live agent-card endpoint among many probed
  well-known paths is a discovery grammar, not an
  encoding or relay mechanism. It belongs to the
  surfaces and discovery lanes, not to this lane, and
  it is not graded as a crypto candidate here. No
  value is reproduced.

## 5. What was NOT checked, and why that matters

- Factum match queries were not run. The brief bars
  this lane from the Factum database, and no NEW claim
  in this file depends on a Factum query. The novelty
  verdicts above rest on the filed lane bundles, the
  tracker raw files, and the prior lanes' own novelty
  sections. A coordinator who wants a Factum leg must
  run it separately. Until then, the da.gd candidate
  stays PROVISIONAL, not confirmed.
- The legacy-tree grep leg that prior lanes left
  incomplete was not re-run in full here. The da.gd
  code-overlap check above covers the filed da-gd
  bundle only. A full legacy grep could still turn
  up a destination-shape precedent. That is a stated
  limit, not a hidden one.
- The in-flight crosswalk lane was not read, per the
  brief. If it holds a newer encoding shape, this
  audit does not cover it.
- No live capture was made, so no claim here depends
  on a live response. The o-pattern circled-letter
  observation stays HELD for exactly that reason.

## 6. Files written by this lane

- `data/lanes/transluce-candidates-20261101/work/crypto/findings.md`
  (this file)
- `data/lanes/transluce-candidates-20261101/work/crypto/candidates.md`
  (candidate sheet: one provisional candidate, one held
  observation, killed list in short form)

No other file was written. No commit was made. No push
was made. No Factum record was submitted.

## 7. Open questions for the coordinator

1. Is the da.gd use-shape split wanted as a detection
   note rather than a behavior finding? If the tracker
   wants behavior only, this candidate should drop to
   watch.
2. Where is the brief's 2026-10-31 amapdata-topic
   message? It is not in any accessible lane. Point
   to the lane directly if it exists outside this
   worker's access.
3. Should the o-pattern circled-letter observation be
   resolved (live page vs saved copy)? That single
   check decides whether it stays held or is killed.
4. Does the coordinator want a Factum match leg run
   for the da.gd candidate before it is offered to
   the tracker? This lane could not run it under its
   brief.
