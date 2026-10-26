# Verification — urlscan.io crawl, 2026-10-26

## Terms

- **Verifier**: this check. It re-reads the raw files. It does not trust the report.
- **Hash**: a short fingerprint of a file. If the file changes, the hash changes.
- **Raw file**: the verbatim copy of a search response. No edits. No redactions.
- **Scan UUID**: the unique ID urlscan gives one scan.
- **Factum**: the structured evidence store in `data/`.
- **Lane**: a work group in Factum. Records in one lane share a tag.
- **Batch**: one exported set of Factum records, in `data/records/<id>/`.
- **Observable**: a single value in Factum, such as a URL or an IP address.
- **IPv6**: the long form of a network (IP) address. IPv4 is the short form.
- **PASS**: the check matches the claim. **FAIL**: it does not.
  **UNVERIFIED**: the check could not run, with the cause stated.

## Scope and method

This file checks every citation in REPORT.md in the same directory.
Each check re-reads the raw bytes. No live database query was used
for the Factum batch. The exported batch files are the artifact.
No file was changed except this file. No commit was made. No push was made.
Token-like values are noted only by presence. No token value is copied here.

## Check 1 — Hash integrity

- **Claim**: SHA256SUMS passes for every entry. The manifest file list
  matches the directory.
- **Method**: Ran `sha256sum -c SHA256SUMS` in the report directory.
  Listed the directory and the raw tree. Counted SHA256SUMS entries.
- **Result**: PASS.
- **Evidence**: All 37 entries report OK. Exit code 0.
  The 37 entries cover 11 top-level files and 24 raw files plus 2 scripts.
  The directory holds exactly those files, plus MANIFEST.md, SHA256SUMS
  itself, and this file. The raw screenshots directory is empty, as claimed.
- **Note**: This file did not exist at assembly time. It is not in
  SHA256SUMS. See the gap in the verdict below.

## Check 2 — Coverage numbers

- **Claim**: The 6 queries give totals 0, 0, 0, 0, 57, 17. Total 74.
  Fetched equals total for each query. hits-draft.json is an empty list.
  hits.json parses, holds 2 ranked hits, and holds crawl totals 74 and 0.
- **Method**: Read each `raw/<query-label>/search.json`. Compared its
  `total` field with its result count. Parsed both hit files.
- **Result**: PASS.
- **Evidence**:
  - getpoiinfo: total 0, results 0.
  - uqscan-tag: total 0, results 0.
  - uqframe-tag: total 0, results 0.
  - proxy-marker: total 0, results 0.
  - relay-jina-reader: total 57, results 57.
  - title-amap: total 17, results 17.
  - Sum: 74. This matches the REPORT.md coverage table and coverage.md.
  - hits-draft.json parses as `[]`.
  - hits.json parses. It holds `crawl_totals` 6 queries, 74 fetched,
    0 triage-passing. It holds 2 ranked hits.

## Check 3 — Marker zero

- **Claim**: Zero matches for each fleet marker across all raw files.
- **Method**: Ran an independent case-insensitive search over all 6
  raw search.json files. Terms: getPoiInfo, uqscan=, uqframe=,
  hysandbox, amap-pc-ssr, /ssr/place.
- **Result**: PASS.
- **Evidence**: Count is 0 for each term, in each file, 0 in total.
  This matches the REPORT.md claim of marker zero in metadata.

## Check 4 — Morning-hit citations

- **Claim**: Rank 1 scan UUID 01a17355-8853-7179-8623-5d2a48a3e0b5 and
  Rank 2 scan UUID 01a1787e-fe16-745d-9831-d0642306fcb2 both appear
  in raw/relay-jina-reader/search.json. The staged morning bundles
  hold the same two UUIDs with page https://r.jina.ai/ec.
- **Method**: Searched the relay raw file text for both UUIDs. Read
  both staged morning bundle files and matched UUID, page, scan time,
  page network address, and network owner.
- **Result**: PASS.
- **Evidence**:
  - Both UUIDs appear 5 times each in relay-jina-reader/search.json.
  - Rank 1 entry: page https://r.jina.ai/ec, scan time
    2026-10-25T13:52:41.718Z, IPv6 page address, AS13335. The report
    shows the same time to the second. The millisecond part is dropped
    in the report. This is a format trim, not a mismatch.
  - Rank 2 entry: page https://r.jina.ai/ec, scan time
    2026-10-26T13:55:56.416Z, IPv4 page address, AS13335. Same trim note.
  - hits-20261025T145711Z.jsonl holds Rank 1 UUID with page
    https://r.jina.ai/ec. hits-20261026T151547Z.jsonl holds Rank 2
    UUID with page https://r.jina.ai/ec.
- **Note, not a fail**: The morning bundle files carry their own
  grade field with a different value than the report grade. The report
  grades urlscan hits SECONDARY by rule. This check covers UUID and
  page only, so the grade field difference does not change this result.

## Check 5 — Factum batch

- **Claim**: Batch data/records/a3fc917d22794d0eb9dbea8ba6b1d405/
  holds 3 records, all with tags.lane=urlscan. IDs are
  source_abe3ff985a814f02a778a5d928e18c82,
  observation_25601d338e044477885afcb719831d00, and
  observable_9b3a23a0de7a4f9b8035be1dabc4d308. The observation tags
  carry the IPv6 value and an ipv6_gap tag. No ipv6-typed observable
  exists in the batch.
- **Method**: Read the batch records.jsonl file only. No live
  database query was run. Checked record count, record kinds, IDs,
  lane tags, observation tags, and observable types.
- **Result**: PASS.
- **Evidence**:
  - Record count is 3. Kinds are source, observation, observable.
  - All 3 IDs match the claim exactly. All 3 carry tags.lane=urlscan.
  - The observation kind is web.capture. Its tags hold the full IPv6
    value, the AS13335 owner value, and an ipv6_gap tag that states
    the omission.
  - The single observable has type url. No record has an observable
    type of ipv6. A search for the exact typed value `"ipv6"` returns 0.
    The string ipv6 appears only in tag names and text, not as a type.

## Check 6 — Third-party citations

- **Claim**: THIRD-PARTY-REPORTS.md accepts 3 reports. Each exists
  where claimed and matches its stated topic.
- **Method**: Fetched the Swarmchasers page as public text only.
  No login was used. Searched the fetched text for the title, the
  markers, and the relay claim. Ran the Transluce tool directly for
  entry 153 and entry 178.
- **Result**: PASS for all 3 citations.
- **Evidence**:
  - Swarmchasers, https://swarmcha.se/posts/chinese-agent-fleet-full-report :
    Page title is "We found a Tencent agent fleet". Topic is a Tencent
    agent fleet that used Amap. The text names hysandbox. It shows
    getPoiInfo, uqscan=, and uqframe= values. It states Jina Reader
    gave answers in 5 runs. This matches the accepted-report summary.
  - Transluce entry 153: The tool returns id 153, submitter Linus,
    created 2026-10-04. Summary covers Amap extraction on urlquery.
    Text states "claude" appears in a uqscan parameter in about 9%
    of relevant reports, and warns the value is freely chosen. This
    matches the claimed summary and warning.
  - Transluce entry 178: The tool returns id 178, submitter Ayush
    Bhardwaj, created 2026-10-14. Summary covers BGSU library
    retrieval through r.jina.ai. Text states AI authorship, bypass,
    and private-data access are unproven. Evidence links include
    arquivo.pt records of r.jina.ai URLs. This matches the claimed
    narrow relay-only corroboration.
- **Note**: No fetch failed for network reasons. No citation needed
  an UNVERIFIED mark.

## Check 7 — Exclusion honesty

- **Claim**: The config urlscan block marks page.title:"amap" as
  enabled:false. It marks domain:amap.com and domain:gaode.com as
  disabled. This matches the report exclusion table.
- **Method**: Read scripts/swarm-infra-config.json. Read the urlscan
  block query entries. Compared each flag and reason with REPORT.md.
- **Result**: PASS.
- **Evidence**:
  - Query `page.title:"amap"` (label title-amap) has enabled:false.
    Reason: adversarial 2026-10-14, documented acronym collisions.
  - Query `domain:amap.com` has enabled:false. Reason: adversarial
    2026-10-14, about 809 benign scans per 30 days vs 0 true positives.
  - Query `domain:gaode.com` has enabled:false. Reason: adversarial
    2026-10-14, same class as domain:amap.com.
  - The report states the title-amap query still ran once as an extra
    at task order. The config flag was not changed. The config read
    confirms the flag is still false, which fits that statement.

## Overall verdict

VERIFIED-WITH-GAPS.

- All 7 checks pass. No check failed.
- Gap 1, minor: This file, VERIFICATION.md, is not covered by
  SHA256SUMS. It could not be covered at assembly time, because the
  verifier creates it after assembly. If full hash coverage is wanted,
  re-run the hash list after this file lands.
- No other gap was found. The zero-hit verdict, the coverage totals,
  the marker zero, the morning-hit citations, the Factum batch shape,
  the third-party citations, and the exclusion flags all re-check
  against the raw bytes.

## Final adversarial review (coordinator addition, from adversarial-review-final.md)

- Ship verdict from the final reviewer: SHIP-BLOCKER (narrow). The
  blocker was the phantom VERIFICATION.md: the report listed it as a
  deliverable before it existed. That blocker is now closed by this
  file itself, which the verifier wrote with all 7 checks PASS.
- Required fixes 1–8 from the final review were all applied to
  REPORT.md, THIRD-PARTY-REPORTS.md, and MANIFEST.md before commit:
  scoped one-liner and rank titles; corpus-vs-files sentence and
  narrowed page claim; disclosed PRIMARY→SECONDARY override; tags-only
  IPv6 preservation with would/would-not-find table; Transluce 178
  moved to rejected (accepted count 3→2); drift strengthened to a
  resolve-before-push gate with +7/−1 arithmetic; VERIFICATION.md
  listing confirmed real; counts corrected (28 real + 1 blank
  addresses, 7 real + 1 blank owners); "differ only" fixed;
  ~2s→~3.4s measured rate; dual-stack downgraded to INFERENCE;
  "near-daily"→"7 of 10 cluster"; "re-scanned"→"scanned again"; noise
  verdict qualified as INFERENCE.
- Note on timing: the final reviewer read the report directory before
  the verifier's file landed, which is why it reported VERIFICATION.md
  as absent. The file exists now and its checks are recorded above.
