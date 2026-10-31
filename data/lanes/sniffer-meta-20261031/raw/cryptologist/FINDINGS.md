# Cryptologist findings — sniffer-sweep meta review

Lane: cryptologist. Date of work: 2026-10-31.
Scope: staged bytes and saved rows only. No new endpoint fetch was made.
No payload was executed. No instruction inside evidence was followed.
No ANEC-01 material was touched.

Grades: default SECONDARY. OBSERVED means only that the byte shape is
present in the staged capture. It does not prove agent behaviour.
Shapes only: no credential-like value, token, wallet value, query
string, contact value, or human handle is reproduced below.

Sources are repo-relative under `data/lanes/sniffer-sweep-20261031/raw/`.

## 1. da.gd decode — full decode succeeds from `final_path`

Source: `urlquery-wayback/uq-odd-dagd-domain.json`.
File facts OBSERVED: query total 98 hits, 30 saved rows. All 30 saved
rows have both flag fields false. The June 21 subset is 17 rows.

Correction to the earlier review: the earlier review said full decode
fails because the staged titles truncate the base64 segment. That is
true only for the title copy. The `final_path` copy is not truncated.
All three distinct segments decode fully from `final_path` after
percent-unquoting. The title copy is capped at 200 characters, so it
is partial. The title copy is no longer needed for decode.

Method note: two of the three segments are percent-encoded in
`final_path`. Raw base64 decode of those two gives garbage. Decode
after percent-unquoting gives clean UTF-8 HTML. That step matters.
It is a transport encoding, not a second cipher layer.

### Per-segment decode table (final_path copy)

Segment A — 8 rows, 2026-06-21, 11:35:41Z to 11:37:31Z (110 seconds).
Final host shape: echo-service host under an httpbin-style path.
Raw segment length 628 characters. No percent sequences. Length mod 4
is 0. Decoded length 471 bytes. UTF-8 valid. Printable ratio 1.0.
Verdict: DECODES FULLY.
Decoded shape: one style element, one iframe element, one script
element. All three elements open and close. Two whitespace bytes
follow the last closing tag. No START marker is present.

Segment B — 3 rows, 2026-06-21, 01:58:12Z, 02:06:24Z, 02:06:25Z.
Final host shape: echo-service host, direct base64 path.
Raw segment length 2408 characters, 4 percent sequences. Unquoted
length 2400 characters. Length mod 4 is 0. One padding character is
present after unquoting. Decoded length 1799 bytes. UTF-8 valid.
Printable ratio 1.0. Verdict: DECODES FULLY.
Decoded shape: one style element, one pre element, one div element,
two script elements. All elements open and close. A START marker is
present at byte offset 128 of 1799. The scripts render an embedded
view of a remote data source. No source locator is reproduced here.

Segment C — 2 rows, 2026-06-21, 01:37:31Z and 01:38:06Z.
Final host shape: echo-service host, direct base64 path.
Raw segment length 666 characters, 5 percent sequences. Unquoted
length 656 characters. Length mod 4 is 0. One padding character is
present after unquoting. Decoded length 491 bytes. UTF-8 valid.
Printable ratio 1.0. Verdict: DECODES FULLY.
Decoded shape: one pre element, one div element, two script
elements. All elements open and close. A START marker is present at
byte offset 10 of 491. This is the short form of the segment B
shape: same pre, div, and two-script skeleton, no style block.

No base64 segment exists outside June 21 in this file. The other
4 June 21 rows have no segment: 3 resolve to an error page shape
and 1 to a bare example host. The June 21 submitted short codes
are 6 distinct codes across 17 rows, so codes repeat.

### Title-copy partial table (for the record)

Title length is 200 characters for all 13 base64 rows. The visible
segment in the title is partial in every case.

- Segment A title copy: 173 segment characters visible of 628
  needed. Complete 4-character groups give 172 usable characters,
  129 decoded bytes, tag shape style plus iframe. Remainder 1
  character is unusable. Verdict: DECODES PARTIALLY (title only).
- Segment B title copy: 181 segment characters visible of 2400
  needed (unquoted). Complete groups give 180 usable characters,
  135 decoded bytes, tag shape style plus pre. Remainder 1
  character is unusable. Verdict: DECODES PARTIALLY (title only).
- Segment C title copy: 181 raw characters visible, 175 after
  unquoting, of 656 needed (unquoted). Complete groups give 172
  usable characters, 129 decoded bytes. Remainder 3 characters
  are unusable. Verdict: DECODES PARTIALLY (title only).

The title copy cannot give a full segment length on its own. The
full length comes from `final_path`, so the title gap is closed.

### Carrier versus framing probe — verdict

The decode question is decided from saved bytes alone: yes, all
segments decode fully. The intent question is not proved by bytes
alone. But the saved bytes weigh clearly one way:

- For framing probe: each segment repeats byte-identically across
  its rows (A 8 times, B 3 times, C 2 times). A per-message carrier
  would vary per row. It does not. The START marker is a framing
  delimiter, not a message. The final hosts are public echo
  services, not a dead drop. The decoded pages are test-page
  scaffolding: style, pre, div, iframe, and script elements that
  render a view. Nothing in any decoded page varies per row.
- Against carrier: no varying payload, no per-row secret shape,
  no nonce, no key, no second layer after unquoting and decoding.

Verdict: framing-probe shape, carrier not evidenced. Intent itself
cannot be proved from staged bytes alone, because intent lives
with the submitter, not in the bytes. A fresh live capture is NOT
needed to decode. It would only help a different question: what
the echo service returns live, or who submitted the links. That
live question is left open for the parent. This lane did not fetch
it.

## 2. Second look at hidden markers in cut items

### GH7 file: `github/q06-i-am-ai-agent.json` (10 items)

Trap-template entries (4):

- Item 0, 2026-10-27: issue template text. It orders agents and
  bots to tick a checkbox that states the opener is an AI agent
  or bot. The staged text shows the template, not a ticked box.
  No agent act is shown. Shape: disclosure trap in template text.
- Item 4, 2026-10-21: issue template text. It carries a checkbox
  that states the content was submitted by an AI agent without
  human review. Same note: template text, not a ticked instance.
  Shape: disclosure trap in template text.
- Item 3, 2026-08-29T19:51:44Z: honeypot-named repository, issue
  number 1. Body is one bare sentence: a self-disclosure that
  the writer is an AI agent that read the page. Body length 36.
  Shape: bare tripwire hit.
- Item 5, 2026-08-29T19:54:08Z: same honeypot-named repository,
  issue number 2, 144 seconds after item 3. Body length 68. Body
  is the same disclosure plus a fill-in template for tool/model
  and for the task being done. Shape: fill-in tripwire. Any agent
  that completes it leaves a structured trace.

Non-trap entries (6), each with its hidden shape if any:

- Item 1, 2026-10-29: agent self-disclosure plus a named
  principal, in a directory-listing addition request. Hidden
  shape: disclosure plus principal only. No code, no nonce, no
  encoded string, no relay.
- Item 2, 2026-10-02: agent acting on behalf of a named principal,
  with an approval claim, asking a licence question about a
  modified fork. Hidden shape: delegation grammar (agent plus
  principal plus approval claim). No code, no nonce, no encoded
  string.
- Item 6, 2026-10-21: agent-authored maintenance report about a
  patch, a release tag, and a build result. Two 40-character
  tokens are present. Both sit in commit positions (one merge
  commit, one commit link). They are commit-hash shapes, not a
  wallet shape. The earlier review's wallet-shape note belongs
  to item 9, not to this item. Hidden shape: none beyond commit
  hashes and a test-result count.
- Item 7, 2026-10-18: the Village launch issue. Hidden shape:
  the publication-verification beacon, assessed in section 4.
  Numbered agent labels (8 occurrences) and model labels (6
  occurrences) are present. No nonce, no base64, no short link.
- Item 8, 2026-09-14: agent bounty-work disclosure plus a vendor
  offer note (a public startup credit offer, stated in round
  amounts). Hidden shape: disclosure plus offer-catalog entry
  only. No nonce, no encoded string, no relay.
- Item 9, 2026-09-25: structured agent onboarding form. Fields
  include a username field, a contributor-type field set to
  agent, a wallet-address field holding one 43-character
  alphanumeric token, planned repositories, and a self
  description (agent label, harness name, own server, autonomous
  work, operator-supervised payment custody). Hidden shape:
  payment-identity shape in a registration form. This is the
  file's only wallet-shape item. It links to the x402 mechanism
  family only at the level of payment identity, not by a shared
  identifier. No shared identifier with any other candidate was
  found.

### GH6 file: `github/q05-collab-spawn.json` (10 items)

Verdict: pure bug-report grammar. No wild-instance grammar was
found in any item. Wild-instance markers tested and absent in all
10: self-disclosure as a live agent act, a spawned-agent report,
and numbered-agent arrival claims.

Form counts across the file (body plus title):

- Dotted form `collaboration.spawn_agent`: items 0, 1, 2, 3, 4,
  6, 8.
- Flat form `collaboration__spawn_agent`: item 5 only.
- Envelope form (JSON object with namespace plus name): items
  0, 5, 9.
- Concatenated form (namespace and tool joined with no
  separator): items 6 and 9. This fourth form was missed in the
  earlier review's three-form list.
- Companion wait-tool confusion (`collaboration.wait_agent`
  versus `functions.wait`): item 1.
- Reserved-tool schema collision: items 2 and 4.
- Privacy-preserving attestation request for encrypted spawn
  arguments: item 2.
- Multi-agent configuration block: items 0, 3, 4, 9.
- Item 7 is the outlier: it contains zero `spawn_agent`
  occurrences. It is a gateway tool-declaration bug report in
  the same search file, not a spawn report and not a wild
  instance.

All 10 items are dated July to October 2026, inside the window
from November 2025 onward. The grammar cluster is corroborated
across independent bug reports. It is a harness fingerprint, not
a beacon, and it does not link to the da.gd, oai/zz, iLands, or
x402 families.

## 3. zz/oai flagged-row mystery — resolved

Source: `urlquery-wayback/uq-odd-zz-param-agent-conj.json`.
File facts: query total 68,265 hits, 30 saved rows, all with empty
tag lists.

Verdict: a flagged row DOES exist in the file. The earlier
"sampled rows" miss is explained: the flagged row sits late in
the saved list, past a small sample.

- Flagged row: saved row 26 of 30 (index 25). Date
  2026-10-31T14:10:46Z. Submitted domain is a dating-site domain.
  Final domain is a different adult-site domain. Flag fields:
  `has_zz_param` true, `has_oai_token` false, `has_dagd` false.
  All other 29 saved rows have all three flags false.
- Corroboration failure: none of the saved fields for this row
  contains the string `zz` at all. Saved path length 16, saved
  final path length 28, title length 13, and none carries a
  query string. So the flag cannot be verified from the saved
  bytes. The flag must come from data that is not stored in this
  row, most plausibly the full submitted URL query, which the
  saved row does not preserve.
- Therefore: the file-level count of 1 flagged row is real, but
  it is NOT a corroborated zz instance from saved bytes alone.
  Do not claim a new zz parameter instance from it. A fresh
  lookup of that report would be needed to see the full URL,
  and that lookup is left open for the parent. This lane did
  not fetch it.
- Related noise check: saved row 15 of 30 in the same file
  contains `zz` as a substring inside a longer path word, with
  all flags false. That is substring noise, not a parameter.
  The same pattern holds in the zz-only search file: its two
  rows containing a `zz` substring both have the flag false,
  because the substring sits inside an ordinary word.

Control files checked: the zz-only search file (30 saved rows,
0 flagged) and the oai-tag search file (30 saved rows, 0
flagged). No new-window zz, oai, or epoch marker is corroborated
by any saved row in this sweep.

## 4. Village beacon — what the fetch-back step proves

Sources: `github/q06c-village-issue1-full.json` (issue),
`github/q06d-village-issue1-comments.json` (4 comments),
`github/q06b-village-comments.txt` (truncated mirror of the
same 4 comments, bodies cut mid-sentence; the JSON file is the
authoritative staged copy).

Timeline OBSERVED:

- Issue created 2026-10-18T22:50:51Z: launch note from a
  numbered agent label plus a model label.
- Comment at 22:51:35Z (44 seconds later): same agent reports
  parallel arrival by a second numbered agent.
- Comment at 22:51:37Z (46 seconds later): the second numbered
  agent checks in, reports its own workspace and a second issue,
  and reports a third numbered agent appearing almost
  immediately after.
- Comment at 23:01:03Z: a short comment that asks for an
  external post. This text is evidence content. It was read
  only. It was not acted on.
- Comment at 23:13:00Z: external-publication update. It states
  the agent published an introduction on a posting-board site
  under its agent label plus model label. It gives a public
  thread locator (shape only, value not reproduced) and a
  second locator described as verification evidence. It states
  the workflow fetched the resulting public thread back over
  HTTPS, received HTTP 200, and required both the agent label
  and the experiment name to be present before reporting
  success. The issue `updated_at` matches this comment time.

What the fetch-back step proves, strictly from staged bytes:

- It proves the claim that a fetch-back check was reported, in
  the stated form: HTTPS fetch, HTTP 200, two required strings.
- If the report is accurate, it proves the posted thread was
  publicly retrievable at fetch time and that the fetched page
  contained the two required strings. That confirms the fetched
  page was the intended thread.
- It proves a post-then-verify shape exists in this experiment:
  publish externally, then read the public surface back, then
  gate the success report on the read-back.

What it does NOT prove:

- It does not prove the post's claims are true. The required
  strings are identity labels that the post itself contains, so
  their presence confirms identity of the page, not truth of
  the content.
- It does not prove independent verification. The poster and
  the verifier are the same agent workflow, by the report's own
  words. This is self-attestation, not second-party checking.
- It does not prove the thread stayed unchanged after the
  fetch, reached any audience, or was read by any other agent.
- It does not prove coordination. The parallel-arrival burst is
  a separate claim in earlier comments. The fetch-back step
  alone says nothing about coordination.
- It does not prove the linked verification-evidence locator
  was itself checked. Its content is not in the staged files,
  and this lane did not open it.
- It does not prove authorship beyond the report's own claim.
  No staged byte ties the posting-board account to the
  repository account except the report's words.

### Same shape anywhere else in the sweep? No.

Method: record-level scan of all staged sweep evidence files
(excluding lane review notes) for the combined shape: a fetch
step plus a success status plus a required-string check in the
same record, plus a text-file scan.

- Only one record matches tightly: Village comment 3 above.
- Three HN records match loosely (fetch, status, and present
  in the same record) but are false friends: all three are the
  same Show HN text about an indexing product, where fetch
  means ingesting documentation sources, not verifying an own
  post. No post-then-fetch-back shape is present.
- One Reddit capture contains the word `fetched`, but in a
  discussion of a URL-fetch exploit, not a verification step.
- Near shapes that are NOT the same: the pursekeeper public
  payment log is publish-then-let-others-verify, not a
  same-workflow fetch-back. The tron handshake is a fixed
  reply template with no fetch step. The da.gd echo resolution
  is a redirect to an echo page, not verification of an own
  post. The Village shape stands alone in this sweep.

## Open questions for the parent

1. Fresh live capture is not needed for da.gd decode. It would
   only serve live-response or submitter questions. Parent's
   call whether that is wanted.
2. The zz flagged row (conj file, row 26) needs a full-URL
   lookup to check the flag. Parent's call whether to fetch it.
3. The Village verification-evidence locator was not opened.
   Its content is unknown from staged files. Parent's call
   whether to read it.
4. GH7 items 0 and 4 show template text, not ticked boxes. No
   staged evidence shows an agent actually ticking either box.
   That gap is noted, not filled.

## Evidence paths

- `data/lanes/sniffer-sweep-20261031/raw/urlquery-wayback/uq-odd-dagd-domain.json`
- `data/lanes/sniffer-sweep-20261031/raw/github/q06-i-am-ai-agent.json`
- `data/lanes/sniffer-sweep-20261031/raw/github/q05-collab-spawn.json`
- `data/lanes/sniffer-sweep-20261031/raw/urlquery-wayback/uq-odd-zz-param-agent-conj.json`
- `data/lanes/sniffer-sweep-20261031/raw/urlquery-wayback/uq-odd-zz-param.json`
- `data/lanes/sniffer-sweep-20261031/raw/urlquery-wayback/uq-odd-oai-tag.json`
- `data/lanes/sniffer-sweep-20261031/raw/github/q06c-village-issue1-full.json`
- `data/lanes/sniffer-sweep-20261031/raw/github/q06d-village-issue1-comments.json`
- `data/lanes/sniffer-sweep-20261031/raw/github/q06b-village-comments.txt`
