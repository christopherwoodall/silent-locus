# INGEST_NOTES — 2026-09-05-termina-digital

Batch 1 `7a482cebea3a4ff19d9a725eea9877a5`: 352 records.
Batch 2 `66ec5afa968147b49573d1760a4a89de`: 14 records
(7 retractions + 7 corrected artifacts). Lane tag `2026-09-05-termina-digital`
on every record. No edges at ingest. Zero retractions for metadata.

## Legacy row mapping (223 events + 21 rollups = 244 rows)

| legacy kind | count | Factum mapping |
|---|---|---|
| wayback_capture | 104 | `web.capture` observation (capture_kind=http; tag capture_kind_detail=wayback) |
| corpus_hit | 105 | `infra.ioc` observation (category=marker) |
| corpus_grep_negative | 5 | claim (property=pattern_sweep_zero_hit, subject=@run) |
| artifact_observation | 7 | artifact record (reference, bytes retained in lane raw/) |
| surface_negative | 2 | `reachability.check` observation |
| pattern_sweep_rollup | 21 | claim (property=pattern_sweep_rollup, subject=@run) |

Plus: 99 artifact records (one per recovered wayback file), 5 lane-document
artifacts (events.jsonl, rollup.jsonl, PROVENANCE.md, SHA256SUMS, sweep.json),
2 sources, 1 run (collection).

Notes:

- `requested_url` for OK captures is reconstructed as
  `https://web.archive.org/web/<ts>id_/<CDX original>` (the manifest only
  stores wayback URLs for failed entries). All 99 OK captures join CDX
  originals with matching timestamps (99/99 verified).
- The 43-byte HTTP-503 placeholder for
  `pub/datasets/agent-pastes-2026-09-08.tar.gz` is ingested as an OK capture
  with http_status=503 (keep-all policy; body bytes preserved).
- The 4 failed captures (3 wayback-404, 1 directory artifact) are ingested
  with capture_status=failed and the verbatim error in tags.
- `infra.ioc` terms are the hunt's pattern labels (established marker
  convention from the librariesio-pattern-battery lane). Provenance carries
  the (file, hit-count) evidence. The term-mapping rule is satisfied: these
  labels ARE the IOC values of record for the sweep, documented in
  provenance.
- Claim values are byte-identical to the legacy descriptions (validator-checked).
- observed_at comes only from source labels (capture.ts / sweep.date /
  retrieved.date); time_basis=source_metadata. No timestamps invented.
- Artifact records are references (artifact_path → data/lanes/...); bytes are
  retained in this lane directory under git. `verify --blobs` lists them as
  missing-byte references by design.

## Pre-ingest dedup

`match --text <term> --mode fuzzy` for: termina.digital, swarm.termina.digital,
zz_word, oai_prefix, epoch_nonce, tryzz, go_import, jqp, md_succ,
webhook.site, jina.ai, da.gd, is.gd, bit.ly — zero true duplicates.

Overlap notes (not duplicates):

- 3 fuzzy hits for "epoch_nonce" in the proxy-fresh-blood lane: term appears
  in prose of audit tags about litter.catbox.moe, not sweep observations.
- 25 fuzzy hits for "md_succ" in the 2018-05-09-paste-archive-gap lane: the
  lane used md.succ.ai as a reader proxy for termina.digital DB actor pages
  (ladder.actor_url tags) — same term, different evidence.
- 4 fuzzy hits for "webhook.site": exfil-endpoint-pivot and
  librariesio-pattern-battery observations — different evidence.
- In-batch: all 105 (pattern,file) pairs unique; seen_before empty on submit.

## Cleaner — PASS

352/352 records tagged lane=2026-09-05-termina-digital; grades all OBSERVED;
no manually set factum.* tags; actor and idempotency key set; every legacy
fingerprint accounted for (244/244); all descriptions byte-identical to
source; 100/4 OK/failed capture split; artifact sha256+size match disk.

## Adversarial validator — PASS (0 failures after fix batch)

Checks: no invented timestamps (observed_at traced to source labels), no
edges in bundle, no top-level lane edge generator, no placeholder terms,
no metadata retractions, legacy coverage complete.

One genuine evidence error was found and corrected via retraction (7 records):
the first submit ran before the CRLF fix below, so 7 artifact records carried
sha256/size of CRLF working-tree bytes. Retracted with reason; corrected
artifact records (LF bytes) submitted in batch 2. The retraction is for
wrong evidence, not metadata.

## Root causes fixed

1. **Git CRLF normalization corrupted 50 evidence bytes on checkout.**
   `.gitattributes` protects `data/**/raw/**` with `-text`, but the legacy
   lane lived at `evidence/2026-09-05-termina-digital/raw/` — not covered.
   Working-tree files were CRLF while git blobs, SHA256SUMS, the wayback
   manifest, and events.jsonl all record LF bytes. Fix: normalized the 50
   working-tree files to their canonical LF bytes (verified each against the
   recorded sha256 before writing); added `evidence/**/raw/** -text` to
   `.gitattributes` so remaining legacy lanes are protected. Lesson: verify
   evidence bytes against the lane's own checksums before trusting the
   working tree.
2. **wayback_manifest.json stores no wayback URLs for OK entries** (only
   failed entries carry url/wayback_url). The ingest reconstructs
   requested_url from CDX originals; the reconstruction is documented in
   tags.requested_url_note on every capture record.

## Discrepancies found (data fixed, none retracted)

- events.jsonl `file` values carry the stale `data/2026-09-05-termina-digital/`
  prefix (documented in PROVENANCE.md); artifact_path tags use the post-move
  `data/lanes/2026-09-05-termina-digital/` path.
- PROVENANCE.md says the live RSS had 10 items; events.jsonl records 9
  (feed.items=9). Both forms preserved verbatim; not reconciled.
- `lane edit --tags` replaces tags instead of merging (first edit dropped the
  scope tag; re-applied with the full set). Worth knowing for other workers.
