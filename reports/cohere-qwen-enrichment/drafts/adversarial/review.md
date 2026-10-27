# Adversarial review — Cohere Qwen enrichment, wave 1

Role: reviewer only. No commit, no push, no git contact. No trace or
benchmark code was run. Files were read as text only.

Overall verdict: SHIP-WITH-FIXES. Do not ship or ingest until every
KILLED item below is fixed and re-checked. No core dataset claim was
found fabricated. The failures are grade vocabulary, counts, and
verdict wording — plus one inflated headline count in the leads file.

## What I checked

- Linguist: 142 rows, all with grade, source file, location, and
  context. Grades: 102 OBSERVED, 39 UPSTREAM, 1 INFERENCE.
- Cryptologist: 193 rows, all with at least one occurrence (source
  file + location). Grades: 162 OBSERVED, 21 INFERENCE, 5 UPSTREAM,
  plus 5 broken grade fields (see K2).
- IOC list: 62 URLs + 46 domains + 13 buckets + 4 IPs = 125 rows.
- Leads: 7 verdicts marked corroborated, 1 unverified.
- Overlap notes: 48 entities, 7 Factum strict hits, 4 lists hits.
- Source re-check: README re-fetched at the pinned revision. Size
  15,020 bytes, SHA-256 matches the linguist metadata exactly. Blog
  re-fetched at 474,274 bytes, matching the linguist metadata.
  Main-trace PUT string checked in the raw JSONL, line 3. Lead
  pages checked in the raw lead captures.

## KILLED — must be fixed, claim as written does not stand

### K1. "7 corroborated" as incident corroboration
- Claim: leads file headline count implies 7 corroborations.
- Location: `drafts/leads/lead-verdicts.md`, verdicts for Leads 1–3
  and 6–8.
- Verdict: KILLED.
- Why: only Leads 1, 2, and 5 are third-party behavior sightings on
  the routify host. Lead 3 proves only that a blocking plugin exists;
  its "signed links" wording is the plugin author's claim, not an
  independent observation. Leads 6, 7, and 8 check generic background
  claims (cheap backdoors, backdoor persistence, namespace attack
  surface). They do not corroborate the Cohere trace at all. None of
  the 7 corroborates Cohere's own sandbox trace. The file's own
  "UPSTREAM/SECONDARY" header does not cure the headline count.
- Fix: replace the single count with a split count: 3 behavior-page
  matches (SECONDARY), 1 plugin-existence match, 3 background-claim
  matches, 1 unverified. Add to every verdict: "does not corroborate
  the Cohere trace."

### K2. Five cryptologist rows have no valid grade
- Claim: rows graded by a sentence, not by OBSERVED, INFERENCE, or
  UPSTREAM.
- Location: `drafts/cryptologist/entities-cryptologist.json`,
  TOKEN_PATTERN rows for routify dates 2026-07-29, 2026-08-05,
  2026-08-10, 2026-08-11, 2026-08-12. Grade field holds "Date segment
  in routify /proxy_temp_file/production/…/trace_* paths."
- Verdict: KILLED (as graded rows).
- Why: grade discipline fails. A consumer filtering on grade will
  drop or misread these rows. Their occurrence context says
  OBSERVED, so the underlying observation is sound.
- Fix: set grade to OBSERVED on all five. Move the date-segment
  sentence into the note field.

### K3. Routify slot count is 19, should be 18
- Claim: 15 distinct routify URLs in 19 example slots.
- Location: `drafts/cryptologist/entity-to-behavior.md`, section B,
  routify bullet.
- Verdict: KILLED.
- Why: re-count from the re-fetched README gives 18 routify host
  occurrences and 15 distinct URLs. The linguist notes say 18
  mentions, which is correct. The 19 figure contradicts it.
- Fix: change 19 to 18. Keep 15 distinct and 14 distinct trace paths
  plus 1 distinct /tmp/probe.txt path, which do check out.

### K4. Non-routify Alibaba URL count double-counts the main trace
- Claim: "8 distinct non-routify URLs + main trace."
- Location: `drafts/cryptologist/entity-to-behavior.md`, section B,
  other-Alibaba bullet.
- Verdict: KILLED (as counted).
- Why: the IOC list holds 8 non-routify aliyuncs.com URLs in total,
  and one of them is the main-trace sanmaohe URL. The README holds
  7, not 8. The phrase as written reads as 8 + 1 = 9.
- Fix: write "7 README non-routify URLs, plus the main-trace URL,
  8 in total."

### K5. "125 IOCs" read as 125 distinct indicators
- Claim: 125 IOC rows.
- Location: `drafts/cryptologist/ioc-list.md`, all sections.
- Verdict: KILLED (as a distinct-indicator count).
- Why: 100.100.100.200 appears twice as the exact same string, once
  under DOMAINs and once under IPs. The list holds 125 rows but
  124 distinct strings. The other IP-like strings differ (they carry
  ports), so this is the only exact duplicate.
- Fix: keep one row for 100.100.100.200, or label the total as
  "125 rows, 124 distinct strings." State the dual classification
  if both rows are kept.

### K6. Crow lead "matches the blog claim exactly"
- Claim: Lead 2 count, host, and fetching all match exactly.
- Location: `drafts/leads/lead-verdicts.md`, Lead 2 verdict.
- Verdict: KILLED (wording).
- Why: the raw Crow issue says the 11 URLs carry signing-style
  parameters only in "some" cases ("some carrying Expires /
  OSSAccessKeyId-style signing parameters"). The draft's quoted
  evidence omits that qualifier. The issue also does not name the
  model, which the draft notes, so "exactly" already overreaches.
- Fix: change to "count and host match; signing parameters present
  on some, not all, of the 11 URLs." Quote the "some carrying"
  qualifier in the page evidence.

## DOWNGRADED — partly true, wording must be narrowed

### D1. Lead 1 "signed routify URLs" needs the ellipsization qualifier
- Location: `drafts/leads/lead-verdicts.md`, Lead 1 verdict.
- Verdict: DOWNGRADED.
- Why: the raw Hacker News page does show Expires, OSSAccessKeyId,
  and Signature parameters on a routify URL, so the signed-shape
  claim is not invented. But the poster ellipsized the key and the
  signature, and the draft's quoted evidence omits the query string
  entirely. A reader of the draft alone cannot verify "signed."
- Fix: quote the parameter names with "key and signature ellipsized
  by the poster." Change the verdict to "signed-parameter shape
  (ellipsized), 16 fetches." Keep the "probably training links"
  guess and the no-comments caveat, which are accurate.

### D2. Lead 3 leak claim is plugin assertion, not observation
- Location: `drafts/leads/lead-verdicts.md`, Lead 3.
- Verdict: DOWNGRADED.
- Why: "every retry leaks a trace identifier to a third party" is
  quoted from the plugin README. The draft does not mark it as the
  author's claim, and the plugin page alone does not prove what the
  host logs. The plugin-existence verdict itself is sound.
- Fix: prefix the leak sentence with "plugin README claims." Keep
  the verdict scoped to plugin existence and link-shape match.

### D3. Lead 8 is partial support from a vendor source, not full corroboration
- Location: `drafts/leads/lead-verdicts.md`, Lead 8.
- Verdict: DOWNGRADED.
- Why: the Edera article supports widened kernel attack surface
  (40 CVEs reachable only with user namespaces enabled). It does
  not prove the blog's framing that the namespace step is "the
  starting point for a long line of kernel privilege-escalation
  exploits." The draft already discounts the vendor headline number.
  The verdict word should match that caution.
- Fix: change the verdict to "PARTIALLY SUPPORTED (vendor source)."
  Do not count it in any corroboration total without that label.

### D4. Main-trace "what leaves the host" mixes OBSERVED with INFERENCE
- Location: `drafts/cryptologist/entity-to-behavior.md`, section A,
  step 5.
- Verdict: DOWNGRADED.
- Why: the probe string and the request path are OBSERVED in the
  trace text. Source IP and time are not in the trace text; they are
  generic network metadata. The step labels the whole list OBSERVED.
- Fix: split the sentence. OBSERVED: probe string, request line,
  path. INFERENCE: source IP and time, if the sandbox network
  recorded them at all.

### D5. Main-trace flag row reads like a fetch command
- Location: `drafts/cryptologist/entities-cryptologist.json`,
  FLAG_SEQUENCE row "curl -s -m 10 -o /tmp/put_probe," sourced to
  the main trace.
- Verdict: DOWNGRADED.
- Why: in the main trace, -o writes the PUT response to
  /tmp/put_probe. It is one half of the PUT command in the row
  above it (-X PUT). Standing alone, the row looks like the README
  fetch chain's -o flag. Direction confusion lives here, not in the
  prose, which separates PUT from fetch correctly.
- Fix: annotate the row "component of the main-trace PUT command,
  not a fetch." Link it to the -X PUT row.

### D6. "No network probe in the main trace" is ambiguous
- Location: `drafts/cryptologist/entity-to-behavior.md`, section A,
  step 5.
- Verdict: DOWNGRADED.
- Why: the PUT itself is a network call. The sentence means no
  additional recon probe (such as a metadata fetch) beyond the PUT.
  As written, it can be read as "no network activity."
- Fix: write "no additional network probe beyond the PUT itself."

### D7. Overlap "clean-novel" headline needs its scope in the same sentence
- Location: `drafts/corpus/overlap-notes.md`, counts section.
- Verdict: DOWNGRADED.
- Why: the arithmetic checks out (48 − 7 = 41; lists NO-HIT 44 =
  41 + the 3 Factum-only hits). But "clean-novel in both systems"
  can be misread as corpus-wide novelty. The gaps section already
  limits scope: top-20 fuzzy returns per entity, structured Factum
  records plus lists/urls/ only, legacy evidence trees and the
  Transluce tracker not checked. That limit must travel with the
  headline, not sit pages below it.
- Fix: change the headline to "clean-novel within the checked
  scope (Factum structured records + lists/urls/, top-20 returns)."
  Keep the gaps section.

### D8. Linguist samples sentence can blur fetch and PUT
- Location: `drafts/linguist/notes.md`, "What the README adds."
- Verdict: DOWNGRADED.
- Why: "a curl-style probe that writes to /tmp/put_probe" describes
  the README samples, which are fetch-then-inspect. The main trace
  also writes to /tmp/put_probe, but by PUT response. The sections
  are kept separate, so this is a clarity risk, not a merge.
- Fix: add "fetch-then-inspect, not PUT" to that sentence.

### D9. Rumo domain row normalizes case without saying so
- Location: `drafts/cryptologist/ioc-list.md`, DOMAINs.
- Verdict: DOWNGRADED.
- Why: the URL row preserves "oss-cn-qINGdao" exactly. The domain
  row lowercases it to "oss-cn-qingdao" with no note. The house rule
  is to preserve observed case.
- Fix: add "case normalized to lowercase here; observed form is
  oss-cn-qINGdao" to the domain row, or keep the observed case.

## UPHELD — attacked, stands

### U1. Dataset signed-link status is UNVERIFIED, not upgraded
- The cryptologist states it plainly: routify URLs carry no query
  string as shown; the one dataset URL with a query parameter
  (sanmaoheihei, Expires, truncated after "&OSS") supports only an
  inference from the parameter name, and the full signature is not
  in the source. The main-trace sanmaohe URL has no query string,
  no signature parameter, plain http. No draft transfers the
  lead pages' signed parameters back onto dataset URLs. The IOC
  list header ("a string here is NOT a maliciousness verdict")
  holds. No draft calls any URL malicious from its string alone.
  The word "implant" appears only inside the observed path
  "implant%2Fupdate.sh" and inside the detection-objective prompt
  text, never as a verdict on that URL.

### U2. Direction is not merged
- Main trace: one bash call, inventory steps, then a PUT upload to
  sanmaohe, response saved to /tmp/put_probe. Verified in raw JSONL
  line 3: "-o /tmp/put_probe -X PUT --data-binary
  PROBE_PAYLOAD_ABC123", no GET in that message. README samples:
  fetch-then-inspect chain (ls and cat counts 30/64 and 14/64
  re-checked against the README text). Entity-to-behavior section
  A, B, and C keep these apart and warn "do not merge the two
  directions" and "do not attach tbench2 to the sanmaohe URL."

### U3. Owner and revision discrepancy is kept unsmoothed
- Linguist rows keep CohereLabs (README) and cfahlgren1 (JSONL
  session source) as separate entities, flagged "differs, not
  reconciled." Revision cb30f9f3… (JSONL) is kept separate from
  the download revision 028b7cd7… Cryptologist dataset rows carry
  the same warning ("do not conflate"). No draft picks a canonical
  owner. Model-name spellings are likewise kept separate
  (Qwen-3.8-Flash-Next in traces, Qwen/Qwen3.8-Flash-Next in README,
  Qwen3.8-Flash-Next in blog).

### U4. Blog-only items stay UPSTREAM and are never presented as observed
- Verified against the re-fetched blog: prefill 4% → 92% and
  watchlist 0.5% → 23% at the -o step (routify count 42 in the
  table); metadata address in 23–36% of completions; tbench2
  test id; "four publishers, Alibaba included" with the other three
  unnamed; "more than 113,000 Qwen derivatives"; rarity "less than
  one call in 100,000"; 1% invented-turn quirk. Linguist count
  claims for all of these are graded UPSTREAM. Cryptologist
  prefill, tbench2, and metadata rows are graded UPSTREAM with
  "not a dataset row" notes. The linguist notes state CTI-REALM and
  tbench2 do not appear in the trace files.

### U5. Reddit lead is UNVERIFIED and its wording is not quoted as checked
- Lead 4 verdict is UNVERIFIED (UNFETCHABLE). The raw Reddit capture
  holds only a shell page, no thread text, no signature parameters.
  The "normal or sketchy" phrase appears only in the "Blog claim"
  line, attributed to the blog, never in "Page evidence." No reply
  content is quoted as checked.
- Minor fix (not a verdict change): add "(blog wording, unchecked)"
  to the Lead 4 heading, so the heading alone cannot be mistaken
  for a checked quote.

### U6. Overlap hits are not cited as incident corroboration
- The overlap notes state it in the section title and the text:
  "None of the 7 Factum hits corroborates the Cohere incident
  itself." Each hit is labeled generic or different-context:
  169.254.169.254 (standard metadata endpoint), Qwen3.8-Flash-Next
  (Transluce BetterWright BoardGameGeek trace, different incident),
  r.jina.ai (same service, different proxy-laundering use),
  Qwen3-Coder (baseline trajectories, blog comparison only),
  tmpfiles.org and paste.rs (generic surfaces), 127.0.0.1
  (loopback). Headline entities (routify host, sanmaohe bucket,
  proxy_temp_file, put_probe, PROBE_PAYLOAD_ABC123, upload/test.bin,
  CTI-REALM, both dataset ids) are NO-HIT in both systems. No draft
  cites any of these 7 as corroboration.

### U7. Grade and provenance discipline, otherwise
- Linguist: zero rows without grade, source file, location, or
  context; zero duplicate values; zero OBSERVED rows sourced to the
  blog. All UPSTREAM rows are sourced to the blog.
- Cryptologist: zero rows without an occurrence. The 84 empty note
  fields are not provenance failures; occurrences carry the
  provenance. Bucket and region rows are graded INFERENCE with
  "no listing observed" / "not independently verified" notes.
  The 5 broken rows are K2, not a wider provenance gap.
- Timestamps: the linguist notes correctly call the single full
  timestamp (2026-10-26T23:52:49.315237+00:00) export time, not
  event time, with original execution time unknown.
- No human or operator identity work was found in any draft. Blog
  contributor names and GitHub usernames in blog links were
  deliberately not extracted, per the linguist notes.

### U8. Lead 5 access-key match, with its limit
- The Yukino raw issue shows the full key shape; the Hacker News
  raw post shows the same prefix and suffix with the middle
  ellipsized by the poster. The draft's wording ("same access-key
  shape," "ends in the same characters") is accurate at that level.
  It does not claim full-key identity, which the ellipsized post
  cannot prove. The "invalid" label caveat on the Yukino issue is
  also correctly kept.

## Fixes required before ship (in order)

1. Fix K1: split the leads count; add "does not corroborate the
   Cohere trace" to every verdict.
2. Fix K2: re-grade the five routify-date rows to OBSERVED.
3. Fix K3, K4, K5: correct the three counts (18 slots; 7 + main;
   125 rows / 124 distinct strings).
4. Fix K6, D1, D2, D3: rewrite the four lead verdict wordings.
5. Fix D4, D5, D6, D8, D9: split or annotate the five
   direction/grade/case wordings.
6. Fix D7 and the Lead 4 heading: carry scope and attribution in
   the headline itself.
7. Re-run a grade-vocabulary check on both JSON files (allowed
   grades only: OBSERVED, INFERENCE, UPSTREAM) and a recount of
   routify slots before any ingest.

## Items not killed for lack of evidence

- README per-example counts other than the ones re-checked here
  (exit-echo split 15 + 8 + 8 = 31, 2>/dev/null in 25/64) were not
  independently re-derived per example, because the draft does not
  document its per-example counting method. They are consistent
  with raw occurrence totals, but the next pass should either
  document the method or drop the per-example denominators.
- Lead 6 (Hackster/BadSeek) and Lead 7 (Sleeper Agents abstract)
  stand only in their narrow, caveated form. They must not be
  quoted outside this file without their caveats (different model
  and backdoor shape for Lead 6; abstract only for Lead 7).
