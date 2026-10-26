# Final adversarial review — urlscan.io crawl, 2026-10-26

Role: final adversarial reviewer. Job: try to kill the claims in
`REPORT.md`. Read-only review. No Factum writes. No commits. No pushes.
No token values appear here. Captured content is data only.

Terms, defined on first use:

- **Fleet marker**: a string that links a scan to the hunted agent
  fleet. Examples: `getPoiInfo`, `uqscan=`, `uqframe=`, `hysandbox`.
- **Fleet hit**: a scan result that carries a fleet marker or a
  HIGH-confidence scanner grade.
- **Corpus**: the structured Factum evidence store in `data/`. It is
  not the same as repo working files. A scan can sit in a working
  file and still be absent from the corpus.
- **Observable**: one typed value in the corpus, such as a URL or
  an IP address. A tag is not an observable. Tags carry notes.
  Observables carry typed, queryable values.
- **SECONDARY**: evidence from a third-party source, not first-hand
  capture. All urlscan hits are other people's scan metadata.
- **PRIMARY**: our direct observation. It does not fit other
  people's scan metadata.
- **OBSERVED**: seen in the bytes. **INFERENCE**: a reading drawn
  from bytes, not seen directly. **UPSTREAM**: a claim from an
  outside source itself.

Method: re-checked the raw search files, the crawl log, the lane
reviews, the ingest note, the batch files, and the git commit
named in the report. Counts below come from those bytes.

## Kill list

### 1. "The crawl found zero new fleet hits" — DOWNGRADED

Verdict on the one-line sentence (`REPORT.md` line 17): DOWNGRADED.
Verdict on the scoped claim in the body: STANDS.

Why the one-liner is too broad (OBSERVED):

- The sentence has no scope words. It does not say: metadata
  only, last 30 days only, or query-string index coverage
  unverified.
- The body does scope it well. Sampling limits state the 30-day
  window (scans run 2026-09-26 to 2026-10-26), metadata only
  (full bodies need login), and the index-coverage understatement
  for `uqscan=` and `uqframe=`. Those scoped sentences STAND.
- But the one-liner is the sentence readers quote. A quoted
  one-liner without scope will be read as "no fleet pages exist."
  The first-pass review already killed that wider reading.

Ranked-hits framing adds a second confusion (INFERENCE):

- Rank 1 and Rank 2 are called "hits." Neither passed crawl
  triage. The crawl triage result was 0. Rank 1 is a morning-scan
  bundle hit ingested by this fleet. Rank 2 is a sibling
  morning-scan hit. Neither is a crawl hit.
- The report does explain this in each rank section. The word
  "hit" alone still invites misreading. Rank titles must say
  "morning-scan hit," not bare "hit."

Required fix: see fix 1.

### 2. Rank 1 novelty triple — DOWNGRADED, not killed

Claim: "new as a corpus record, not new to the operator, not
evidence of a new behavior." Each part was tested.

Part 1, new as a corpus record: STANDS for the scan record
(OBSERVED):

- Pre-ingest dedup in `ingest-note.md` found no corpus record
  for scan UUID `01a17355-8853-7179-8623-5d2a48a3e0b5` or for
  its result address. The result URL was `not_found` before
  ingest. After ingest, a URL match finds 2 records, both lane
  `urlscan`.
- The batch file confirms 3 records:
  `source_abe3ff985a814f02a778a5d928e18c82`,
  `observation_25601d338e044477885afcb719831d00`,
  `observable_9b3a23a0de7a4f9b8035be1dabc4d308`.

Part 1, weak spot (OBSERVED):

- The ingest note also claims no corpus record for the page
  address, based on 25 fuzzy hits that are "all generic relay
  uses." No hit IDs are listed. A reader cannot check that
  none of the 25 holds this page. The scan-record claim is
  proven. The page-address claim is asserted, not shown.
- The report also blurs corpus versus repo files. The scan was
  already in repo morning-state files. It was new only to the
  structured corpus. The report says "already surfaced Oct 25,"
  which helps, but it never states the corpus-versus-files
  distinction in one sentence.

Part 2, not new to the operator: STANDS (OBSERVED):

- The first-pass review shows the Oct 25 hit already sits in
  morning state (`hits-20261025T145711Z.jsonl` and its bundle).
  The operator's own scanner surfaced it before this fleet.

Part 3, not evidence of a new behavior: STANDS (OBSERVED):

- The hit is a bare scan of the reader front page. No inner
  target address follows the reader host. No fleet marker
  appears. The same bare shape already appeared on Oct 24
  (two scans) and in older crawl results. A repeat shape is
  not a new behavior.

Required fix: see fix 2.

### 3. Rank 1 downgrade to LOW / SECONDARY — grade STANDS, disclosure DOWNGRADED

The downgrade itself is justified. The bytes support SECONDARY,
not PRIMARY (OBSERVED):

- The morning bundle grades the hit PRIMARY, confidence LOW.
  That grade is confirmed in the morning state file.
- The config grades the `domain:r.jina.ai` query PRIMARY, but
  its note defines the signal as "scans of jina-proxied URLs."
  A proxied URL carries an inner target. Rank 1 carries none.
  The PRIMARY rationale does not attach to a front-page scan.
- The false-positives doc states the SECONDARY rationale in
  plain words: urlscan hits are other people's scan metadata,
  not our direct observations. It assigns SECONDARY grade to
  the opt-in relay queries on that basis.
- LOW confidence stands. Both the bundle and the report agree
  on LOW.

What the report hides (OBSERVED):

- `REPORT.md` never names the morning PRIMARY grade. A reader
  who compares the morning bundle to this report sees a grade
  change with no explanation. The crawl-pass review explains
  the downgrade. The final report applies it in silence.
- That silence matters. A grade change without a named override
  looks like an error, not a decision.

Required fix: see fix 3.

### 4. IPv6 gap: "value NOT lost" — DOWNGRADED

The sentence at `REPORT.md` line 240 is file-true and
function-false. Verdict: DOWNGRADED.

What is true (OBSERVED):

- The typed IPv6 observable is missing from the batch. The
  batch has 0 IPv6 observables. The installed pack allows only
  `url`, `domain`, `hostname`, `ipv4`, `email`.
- The Rank 1 IPv6 value does stay verbatim in the observation
  tags (`tags.ip` and related tags), in the `ipv6_gap` tag, in
  the lane raw copies, and in the ingest note. The batch file
  confirms `tags.ip` is present on the observation record only,
  not on the source or the URL observable.

What "NOT lost" overstates (INFERENCE from OBSERVED facts):

- Tags are not observables. A future typed query for an IPv6
  observable will miss this value. Edge building on observables
  will miss it. Observable counts will miss it.
- Even text findability is unproven after ingest. Before ingest,
  a fuzzy text search for the full value found only short
  number fragments, not an IPv6 record. The ingest note claims
  only a post-ingest URL match, not a post-ingest IP-value match.
  The report claims preservation. It does not claim a proven
  post-ingest IP-value search.

What a future query would and would not find:

- WOULD find: the value in the exported batch file, in lane raw
  copies, and in the ingest note, by direct file read.
- WOULD NOT find: the value as a typed IPv6 observable, by an
  observable-type query, by an IP-observable match, or by
  observable-based edge building.
- UNPROVEN: whether a corpus text search for the full value
  finds the tagged observation after ingest. That search was
  not run and reported.

Required fix: see fix 4.

### 5. Third-party accepts — 178 KILLED, 153 STANDS, Swarmchasers STANDS

#### 5a. Transluce entry 178 — KILLED as an accept

Verdict: KILLED. Demote to rejected or background-only. It is
padding under the report's own bar (OBSERVED from
`THIRD-PARTY-REPORTS.md`):

- Entry 178 covers library retrieval through the reader in May
  2026. No fleet link. No fleet marker. No `/ec` scan. No
  urlscan record. AI authorship, bypass, and private-data
  access are all unproven per the entry itself.
- The draft itself calls it "the weakest accepted report" and
  admits it bears "on Jina-as-relay only, not on any fleet
  finding."
- The same bar rejects entry 38: reader mentioned only in a
  chain, with execution, bypass, and authorship unconfirmed.
  Entry 178 fails that bar in the same way.
- The same bar rejects entry 115: urlscan as a source, but a
  different subject and no fleet marker. Entry 178 is also a
  different subject (library retrieval) with no fleet marker.
- The method point it adds ("third-party records can show relay
  use") is already carried by the Swarmchasers report, which
  shows relay use in a scanner corpus for the actual fleet.
  Entry 178 adds zero to the crawl verdict. The report itself
  says nothing found changes the crawl verdict.

Required fix: see fix 5.

#### 5b. Transluce entry 153 — STANDS, narrowly

Verdict: STANDS as background, not as finding support
(OBSERVED):

- Entry 153 bears directly on finding set B: `uqscan` tag values
  in Amap scanner traffic in early October 2026. That is a
  hunted marker in a scanner corpus. Entry 178 has no such link.
- The report states its limit honestly: the value is freely
  chosen and not conclusive, and it does not cover urlscan, the
  reader, or the `/ec` scans.
- Wording note: "corroborates" should mean background-marker
  corroboration only. It does not corroborate the crawl zero
  or the morning scans. The report's caveats already say this.
  Keep the caveats attached to the verb.

#### 5c. Swarmchasers report — STANDS

Verdict: STANDS (UPSTREAM):

- The report itself is the outside source. It names the exact
  hunted markers (`getPoiInfo`, `uqscan=`, `uqframe=`,
  `hysandbox`) and the reader as the fleet's only successful
  relay, with activity 2026-09-28 to 2026-10-08.
- The report states the limits: it does not mention `/ec`
  scans or urlscan, and it does not show ongoing activity
  (last seen Oct 8). Those limits are correct and keep the
  accept honest.

### 6. Corpus count drift 208,343 to 208,342 — DOWNGRADED

Verdict: DOWNGRADED. Not buried, but understated and
under-computed (OBSERVED from `ingest-note.md`):

- The drift is disclosed as open item 2. That is honest
  placement. It is not hidden.
- But "needs a glance" is too weak for an unexplained move on
  a shared branch, and the arithmetic in the report is wrong
  in effect.
- Start status showed 208,343 records. End verify showed
  208,342. The report frames this as a 1-record difference.
- This fleet's batch added 3 records. The sibling batch
  committed in the same sweep added 4 records. Both batch
  files confirm those counts (3 and 4 lines in their
  `records.jsonl` files). On a same-basis reading, the count
  should have risen by 7. It fell by 1. The unexplained gap
  is 8 records, not 1.
- The report never states the counting basis for the two
  numbers. If the bases differ (status versus verify), that
  fact alone would explain part of the gap, but it is never
  stated. A reader cannot tell whether the drift is 1 or 8.
- The report also presents verify as clean (`ok:true`,
  `verified:true`, `pending:0`) in the Ingest section, while
  the count moved. Clean verify plus moved count needs one
  sentence of reconciliation. It has none.
- The report does say "Check before the next push." That is a
  gate, and it must stay. Strengthen it from a glance to a
  block: no push until the move is explained.

Required fix: see fix 6.

### 7. Similarity promoted into corroboration or identity — three DOWNGrades, one KILL

#### 7a. "Near-daily ~13:5x UTC pattern" — KILLED as phrased

Verdict: KILLED for "near-daily." The count underneath STANDS
(OBSERVED from `raw/relay-jina-reader/search.json`):

- Ten `/ec` scans exist in the haul. Seven fall between 13:46
  and 13:55 UTC. That count is verified and STANDS.
- But the scans fall on only 8 days out of 14 (Oct 13, 14, 17,
  18, 19, 24, 25, 26). Three scans fall far outside the window
  (Oct 13 at 20:43, Oct 17 at 11:37, Oct 24 at 10:03). Days
  Oct 15, 16, and 20 through 23 have no `/ec` scan at all.
- "Near-daily" is false on those dates. The honest phrase is
  "7 of 10 scans cluster in a 13:46–13:55 UTC window." A
  cluster is not a daily schedule.
- The report does say the pattern is "noted, not attributed"
  and that a schedule alone does not prove an agent. Those
  caveats STAND. The "near-daily" word must still go.

#### 7b. "Cloudflare dual-stack fronting" — DOWNGRADED to INFERENCE

Verdict: DOWNGRADED (INFERENCE stated as fact at `REPORT.md`
line 73):

- OBSERVED: Rank 1 uses IPv6, Rank 2 uses IPv4, same ASN
  (AS13335), same page URL, same empty title, same grade.
- INFERENCE: one Cloudflare-fronted service answering on both
  address families. That reading fits the bytes, but anycast
  edge rotation across Cloudflare addresses also fits. The
  haul shows several distinct Cloudflare addresses for the
  same page. The bytes do not prove one dual-stack host.
- What STANDS without inference: "not a new target." The page
  URL is the same. Same URL means same target page, whatever
  edge address served it.

#### 7c. "Same target, re-scanned" — DOWNGRADED

Verdict: DOWNGRADED (INFERENCE):

- "Same page URL, scanned again" is OBSERVED. The URL matches.
- "Re-scanned" hints at the same submitter running the scan
  again. The submitter is unknown. Anonymous metadata carries
  no submitter field. The report itself states this in open
  item 5. Do not imply one actor from two scans of one URL.

#### 7d. "Routine noise, no result wrongly dismissed" for the 44 — DOWNGRADED

Verdict: DOWNGRADED (INFERENCE stated as flat verdict at
`REPORT.md` line 89):

- The 44 non-reader results contain zero "jina" strings. The
  match field lies outside captured metadata. A fleet page
  that calls the reader as a subrequest cannot be excluded
  from metadata alone. The first-pass review states this.
  The report states it too, in the downgrade sentence that
  follows the verdict.
- The verdict sentence still reads as proof. The honest form
  is: "no fleet marker in captured metadata; subrequest use
  not excluded." Dismissal is correct on the evidence. Proof
  of noise is not available from metadata alone.

### 8. Internal contradictions and count checks

Checked against raw bytes, batch files, and git. Mismatches
first, then checks that pass.

#### 8a. Phantom VERIFICATION.md — KILLED, SHIP-BLOCKER

- `REPORT.md` line 278 lists `VERIFICATION.md` as an artifact
  in this directory: "verifier re-fetch results and final
  adversarial review of this report."
- `MANIFEST.md` lists it as a deliverable too.
- The file does not exist. It is absent from the directory
  listing. It is absent from `SHA256SUMS` (37 entries, all
  hashes verified OK, no VERIFICATION entry).
- The report therefore claims a verification artifact it does
  not contain. A report cannot ship as verified on a missing
  verification file.
- Related gap: this final review file
  (`adversarial-review-final.md`) is not listed in the
  report's artifact list either. The list is stale in both
  directions.
- Required fix: see fix 7. This is the ship-blocker.

#### 8b. Network address and owner counts count a blank — KILLED

- `REPORT.md` line 117: "29 network address values, and 8
  network owners" for the 57 jina results.
- Bytes say: 28 real addresses (26 IPv4, 2 IPv6) plus 1 blank
  value; 7 real owners plus 1 blank value. The cryptologist
  review states this plainly and warns that blank values must
  never count as shared values.
- The report elsewhere knows the blank artifact ("one apparent
  share was a blank-value artifact"). It still counts the blank
  as a value and an owner in the identifier inventory. That is
  the exact error the cryptologist warned against.
- Required fix: see fix 8.

#### 8c. "Differ only in scan UUID and scan time" — KILLED

- `REPORT.md` lines 71 to 73: the two hits "differ only in scan
  UUID and scan time," then add that "the network address
  family differs."
- The address family is a third difference. "Only" is false on
  the report's own next sentence. Other differences exist in
  the bundles too (scan method details aside, the family
  difference alone kills "only").
- Required fix: see fix 8.

#### 8d. Request rate "~2 seconds" — KILLED

- `REPORT.md` line 24 and `coverage.md` both say one request
  per ~2 seconds.
- The crawl log shows gaps of about 3.7, 3.3, 3.3, 3.4, and
  3.5 seconds between the 6 queries. Mean gap is about 3.4
  seconds, not about 2. Small error, but it is a stated rate
  contradicted by the log.
- Required fix: see fix 8.

#### 8e. "Only record ingested" — DOWNGRADED wording

- `REPORT.md` line 17: "The only record ingested by this fleet
  is one older morning-scan hit."
- The batch holds 3 records (1 source, 1 observation, 1 URL
  observable). "Record" here means "hit," but in a Factum
  report "record" means a corpus record. The sentence invites
  a count of 1 where the batch count is 3.
- Required fix: see fix 1.

#### 8f. Checks that PASS (OBSERVED)

- Totals: 74 = 57 + 17. Crawl log shows 6 queries, all HTTP
  200. Raw totals match the log.
- Jina split: 13 reader scans (10 `/ec`, 3 home page) and 44
  scans of 29 other page domains. Title split: 13 cloud
  hostnames, 2 marketing-academics pages, 2 French
  food-association pages. All verified in raw bytes.
- UUIDs and times: Rank 1 UUID and Rank 2 UUID match the raw
  haul and the morning bundles. Scan times match to the
  second. The "about 24 hours" gap is 24 hours, 3 minutes.
- Batch IDs: `a3fc917d22794d0eb9dbea8ba6b1d405` (3 records)
  and sibling `7d0c5086bec14a8c90d68896a8b28032` (4 records)
  both appear in commit `0c1ef707`, which the git log
  confirms as "Export pending urlscan batches (operator
  override of 2h rule)."
- Record IDs in `hits.json` match the batch file and the
  ingest note exactly.
- Lane files: 126 lane files validated, 0 malformed, per the
  ingest note. The report repeats this correctly.
- First-pass kills applied, not merely cited: the relay-use
  kill, the French "documented" downgrade, the `domain:`
  match-mechanism downgrade, and the index-coverage
  understatement all appear in the final report text. The
  gaps are the grade-override silence (item 3) and the new
  blank-count error (item 8b), not a failure to apply the
  first pass.
- Raw provenance files exist: dotfiles (`.PROVENANCE.txt`)
  are present in each raw query directory. An early listing
  without dotfiles hid them. They are present. No kill here.
- Third-party draft versus final: `THIRD-PARTY-REPORTS.md`
  is identical to `third-party-reports-draft.md` (same hash).
  The "promoted verbatim" claim is true. That sameness is
  also why the 178 problem survives into the final report.
- The "16 candidate groups" rejected count in the report
  could not be verified to one method from the draft bullets.
  Counting method is unstated. This is noted, not killed.
  Fix: drop the number or show the count method.

## Required fixes to REPORT.md

Fix 1 — one-liner scope and rank titles (lines 17 to 18, 66, 70):

- Change line 17 to: "The crawl found zero new fleet hits in
  the last 30 days of urlscan search metadata. No fleet marker
  was found. Query-string index coverage is unverified."
- Change line 17 to 18: "one older morning-scan hit" becomes
  "one older morning-scan hit (3 corpus records in one batch)."
- Change Rank 1 and Rank 2 titles to "morning-scan hit," not
  bare "hit."

Fix 2 — novelty scope (Rank 1 novelty paragraph):

- Add one sentence: "Corpus here means the structured Factum
  corpus, not repo working files. The scan already sat in
  morning-state files."
- Add one sentence or drop the page-address novelty claim:
  either list the 25 fuzzy-hit IDs that prove none holds this
  page, or narrow the claim to scan UUID and result address
  only, which the dedup proves.

Fix 3 — grade override disclosure (Rank 1 grade line):

- Add one sentence: "The morning bundle graded this hit
  PRIMARY. This report grades it SECONDARY because the hit is
  other people's scan metadata with no inner target, so the
  config PRIMARY rationale for proxied URLs does not attach."

Fix 4 — IPv6 wording (open item 1, lines 240 to 241):

- Replace "The value itself is NOT lost" with: "The value is
  preserved verbatim in tags and raw copies, but it is not
  preserved as a typed observable. A future typed IPv6 query,
  IP-observable match, or observable edge build will miss it."
- Add: "Post-ingest text search for the full value was not
  run. File preservation is proven. Corpus text findability
  is unproven."

Fix 5 — third-party section (lines 225 to 228):

- Remove entry 178 from the accepted list. Move it to the
  rejected list with the reason: "Different subject, no fleet
  marker, no fleet link, authorship unproven. Same bar as
  rejected entry 38."
- Change the accepted count from 3 to 2. Keep the "weakest
  accept" label out. There is no weakest accept once 178
  is gone.

Fix 6 — count drift (open item 2, lines 246 to 248):

- Replace "needs a glance" with "must be resolved before the
  next push. Do not push on an unexplained corpus move."
- Add the arithmetic: "This batch added 3 records. The sibling
  batch added 4. On a same-basis reading the count should have
  risen by 7. It fell by 1. The unexplained gap is 8 unless the
  two counts use different bases. State both counting bases."

Fix 7 — phantom artifact (line 278) — SHIP-BLOCKER:

- Either create `VERIFICATION.md` with real verifier re-fetch
  results, or delete the line. Do not ship a report that lists
  a verification file that does not exist.
- Add `adversarial-review-final.md` to the artifact list.
  Update `MANIFEST.md` and `SHA256SUMS` to match, or the
  inventory will be stale again after this review lands.

Fix 8 — small factual corrections:

- Line 117: change "29 network address values, and 8 network
  owners" to "28 real network address values plus 1 blank
  value, and 7 real network owners plus 1 blank value."
- Lines 71 to 73: change "differ only in scan UUID and scan
  time" to "differ in scan UUID, scan time, and network
  address family."
- Line 24: change "One request per ~2 seconds" to "One request
  per ~3.4 seconds." Apply the same fix in `coverage.md`.
- Line 73: change "That difference is Cloudflare dual-stack
  fronting" to "That difference is consistent with Cloudflare
  dual-stack fronting (INFERENCE)."
- Open item 5, line 260: delete "near-daily." Replace with
  "7 of 10 scans cluster in a 13:46–13:55 UTC window."
- Rank 2 and behavior sections: change "re-scanned" to
  "scanned again" where the submitter is unknown.
- Rank 3 verdict, line 89: change "are routine noise" to "show
  no fleet marker in captured metadata; subrequest use is not
  excluded."
- Third-party section: either drop "16 candidate groups" or
  show the count method.

## Survivors, stated plainly

- Zero fleet markers in the 74 fetched search records, within
  the stated scope (metadata only, last 30 days, index
  coverage unverified for query-string tokens).
- 74 = 57 + 17. Jina split 13 / 44. Title split 13 / 2 / 2.
- Both morning hits are bare front-page scans, not agent-relay
  use. No inner target. No fleet marker.
- Rank 1 is LOW, SECONDARY, not swarm-linked. The downgrade
  from morning PRIMARY is correct on the bytes.
- The relay service is already known. The scan record is new
  to the corpus. The operator already saw the scan. No new
  behavior is shown.
- Swarmchasers and Transluce 153 stand as narrow background.
  Neither bears on the `/ec` scans or the crawl zero.
- The first-pass kills were applied in the final report, with
  the exceptions named above (grade-override silence, new
  blank-count error, surviving 178 accept).

## Ship verdict

SHIP-BLOCKER, narrow. The blocker is the phantom
`VERIFICATION.md` (item 8a, fix 7). A report that lists a
verification file that does not exist cannot ship as verified.
The fix is one line (create the file with real results, or
delete the line) plus the artifact-list update. Apply fixes 1
through 8 with it. After those edits, with no new claims added,
the report can ship.
