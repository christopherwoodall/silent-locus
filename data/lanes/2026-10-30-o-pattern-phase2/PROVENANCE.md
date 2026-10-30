# Provenance — o-pattern relay-jina-reader, phase 2

Lane: `2026-10-30-o-pattern-phase2` (lane id `lane_2483c3b5db0d471db67f6654d61f18c2`).
Actor for all submissions: `agent:o-pattern-phase2`.
Tags on every record: `{"lane": "2026-10-30-o-pattern-phase2"}`.
Method: passive GET only on openly public surfaces. No accounts, no
logins, no sessions. No POST to any operator, forum, or host
infrastructure. No 429 retried within a run.

## File-backed captures (4 batches, 12 records, all ok:true, seen_before empty)

- TXT: batch `089033e65f174697a065728771dcb718`.
  artifact_d68593caf0e340eaaaceddacbb70f22c,
  source_e9bd20392afe4e6fa226be4733fcb257,
  observation_45fee6f3d5e946a98695d068067788ca.
  URL: forum.fractalfuture.net short-url TXT (gyo ref 2026-0604-0033-06).
  Observed 2026-10-30T03:15:01Z (collector_clock). File: 189,356 bytes,
  sha256 9c0459c2a39ff397d4df59ee1b78709173db27a54e3fe99c8e78276bf0b3e3e3.
- ww MP3: batch `5f754586ab4b457f9c6e545f76ca58e2`.
  artifact_039bffd20f5b46dcb4a81db597bd1c54,
  source_245af6d745254882be7aa69c803cea79,
  observation_9ad883229886433d8fbcead45fd06b0c.
  URL: Wayback 20261020014219id_ replay of the forum ww MP3.
  Observed 2026-10-30T05:02:25Z (received_by_factum). File: 10,126,848
  bytes, sha256 355d706fe36e73a45fdbe30c7ea36a325dc941c9f55abe8bca29a35346154cde.
  Note: 20261020014219 is NOT an exact CDX timestamp (nearest
  20261020014241/42, warc/revisit to a 2025-08-13 original). Served
  capture identity is unconfirmed.
- mUr MP3: batch `fc87df125ee4488a913909c9c897f595`.
  artifact_45fb4fcf234a45a08933fff5,
  source_52c1ac3a4dcd43d29020345e9e374ad2,
  observation_8507abf71bc740bfb7335687fb4eb43a.
  URL: Wayback 20261019071014id_ replay of the forum mUr MP3 (exact CDX
  entry, gyo ref 2026-1019-1618-09). Observed 2026-10-30T05:12:04Z
  (received_by_factum). File: 3,378,240 bytes,
  sha256 20d09d309f03c5aea6fc9411678e99fec8b5ee2179d75a42f160aad3a70792f8.
- WEBP: batch `7b347f8fce8f4be683e9fbc3bd36e788`.
  artifact_58208cbd89d84e77a4ec9ec4de69f521,
  source_c88f2b108c224f52a94208c739177f27,
  observation_2066139ee96a497683b6d44201d5c6b0.
  URL: Wayback 20230216011350im_ replay of iili.io/HGHQml9.webp.
  Observed 2026-10-30T05:16:58Z (received_by_factum). File: 62,243,550
  bytes, sha256 66a713ce8d11889a3c79cfd4664b1902a3f3665eb224aa7d69ba450659f14f8d.
  Capture script: workspace `o-pattern-followup/phase2/run_captures.sh`.
  Log: `capture-log.txt` in this lane directory.

## IOC + claims bundle (32 records)

Batch id: `53e548eedcf04f4db36492a827b6f14f` (32 records: 3 sources,
11 observables, 14 observations, 4 claims; durability pending at
submit; seen_before: all 11 url observables `not_found`).
Bundle file: workspace `o-pattern-followup/phase2/bundle-ioc-claims.json`.
Idempotency key: `o-pattern-phase2/ioc-claims-bundle`.
Contents: 3 bundle-local sources (live pages, Desmos/Ghost Archive,
SVG capture), 11 `url` observables (live pages, forum files, Desmos
calculator, Ghost Archive parent + WARC, freeimage viewer + file,
archived WEBP), 14 `infra.ioc` observations (8 hosts category `domain`,
5 filenames + Desmos id category `other`, all status `active`), 4
claims (TXT verdict, Desmos tone match, MP3 carrier assessment,
freeimage classification) citing the capture observations above.

Dedup (exact mode, before submit): all 11 URLs and all 14 terms checked.
9 URLs not found; 2 URLs (TXT forum URL, archived WEBP URL) matched only
the submitter's own pending capture observation + source records, not a
`url` observable — submitted as new by type+value, overlap noted.
13 terms not found; `web.archive.org` matched 50 other-kind records but
zero `infra.ioc` term records (verified by direct corpus query) —
submitted as a new term, overlap noted. Within-batch dedup by key field
done. No `infra.ioc` term duplicates the termina-digital marker terms.

## Lane raw files (this directory, raw/)

- SVG bytes + local render PNG (416,706 bytes,
  sha256 d8660ed21a49b058e88a00db800bee627a6b9b123ce6bc2110d5780a42546d96;
  render 253,870 bytes,
  sha256 319d8a6d4f8a6985acaa2fa05feef59b1d0da533094918f8d7d7081ca8c0dec9).
- Desmos state JSON (sha256
  779703e551f8b1475520e3dee36dd752473e59919030777080534a94c189b6d6).
- TXT decoded copy (UTF-8, 241,728 bytes).
- 26 CDX re-census responses (24 exactly `[]`, 2 11,832-byte 503 pages).

## Deliberately NOT captured, with reasons

- Desmos state JSON: extracted from a Ghost Archive WARC, not downloaded
  from a URL. Lane raw file + description instead. No capture record.
- SVG: its original URL carries a credential-like token. Token-bearing
  URLs are forbidden in every file, report, and message. Lane raw file
  (retrieved via the stored live-page link, which is never printed) +
  description instead. No capture record. The fetch script prints counts,
  hosts, HTTP status, size, and hash only, never the link.

## Token rule

No token value and no token-bearing URL appears in any phase-2 file,
this lane, or the report. The four phase-1 raw infra files DO contain
token values (see FULL-REPORT.md section 8, C3). They are excluded
from this push. If the operator ever wants them in the repo, that is a
separate secrets decision.

## Review

Independent adversarial review: workspace
`o-pattern-followup/phase2/adversarial-review-FINDINGS.md`.
3 kills + 8 weakens + 3 minors, all applied to FULL-REPORT.md before
finalizing (one wording corrected: the review's evidence-map item 13
stated the 503 directory holds "the 2 persistently failed forms plus 2
forms that succeeded"; the directory actually holds 4 worker-run 503
pages, of which only neo-jina-https stayed failed in the completion
pass — the report carries the corrected accounting).
