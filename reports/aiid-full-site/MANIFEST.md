# AIID full-site fleet — manifest

Scope: all 1,777 snapshot incidents (2026-10-26 snapshot) from incidentdatabase.ai.
Operator calls: ingest all 1,782 (site count 2026-10-29); push the FULL raw set
(2026-10-30). Reconciled: 1,777 in snapshot + 5 post-snapshot (unknown IDs,
never fetched) = 1,782 site count. Fetch scope was the snapshot.

## Batches (Factum, lane aiid-full-site, lane object lane_ad9dd8e545bc47bf8007615750bff4ff)

- Incident batch fc09b8bfbd7b4d719e070fed0d5c4d49: 5,379 records
  (1,775 sources + 1,829 observations + 1,775 claims). records.jsonl 5,558,810
  bytes. Manifest SHA-256:
  20133579136fe746dfc65af953cf13782e73facf3c61dc9883555b02a034400a
- IOC batch 32bb59c709f6423a8e043c640f5b80a3: 10,595 records
  (1 source + 10,594 infra.ioc). records.jsonl 10,502,848 bytes. Manifest
  SHA-256: 202d71d040e3de398624f1276ba5691e3575275a3ee429173850e20216af72db
- Corpus: 208,745 → 214,124 → 224,719. Both batches verify --blobs ok,
  pending 0. Both under the 80 MB local-only threshold: commit-eligible.
- Excluded overlaps (already ingested, batch 756a273f, lane
  incident-7050-antigravity): incidents 1152, 1433. Zero records for them
  in either batch.

## Reports (this directory; SHA-256 in SHA256SUMS)

INGEST-REPORT.md, IOC-REPORT.md, TOOL-UPDATES.md, HUNT-INDEX.json,
iocs.json, ioc-bundle.json, build-ioc-bundle.py, scanner-verification.md,
scanner-fix-note.md, aiid-scanner-cron-body-DRAFT.md, adversarial-review.md,
verifier-report.md, MANIFEST.md, SHA256SUMS.

## Evidence lane (data/lanes/aiid-full-site/)

- raw/snapshot/: 2026-10-26 tarball + Excel export + inventories +
  extracted CSVs. Tarball split (see raw/snapshot/SPLIT.txt): original
  121,490,067 bytes, SHA-256
  bc8c01b15417785d3753f95052d0c20816b57e9f41a954175e6aabf9f8eead07,
  kept on disk local-only (lane .gitignore); 3 parts committed, reassembly
  verified byte-identical. No other file in the lane exceeds 100 MB.
- raw/fetch/: f1-1-450, f2-451-900, f3-901-1350, f4-1351-1788.
  Lane total 3.2 GB, 27,338 files at commit time (includes split parts
  and extracted JSONs; per-file .sha256 sidecars throughout).
- extracted/: e1-1-900 (889 JSON), e2-901-1788 (886 JSON),
  novelty-verdicts.json (1,767 NEW / 2 OVERLAP / 8 PARTIAL).
- Gaps: 5 report pages HTTP 404 (3447, 2587, 3205, 3875, 3916);
  5 post-snapshot incidents (unknown IDs); zero 403/429.

## Scanner + tools

- scripts/scanners/aiid.py (fixed: F1 date|kind keys, STATE_VERSION 2;
  F2 no baseline on degraded fetch; dry-run + disabled gate verified).
  Cron draft only — parent creates the cron; enable needs operator word.
- lists/words/wordlist.json + wordlist.txt (+96 entries, append-only).
- scripts/swarm-infra-config.json (otx 23→52, prcomment queries 10→11;
  diff: 149 insertions + 3 deletions, confined to iocfeeds/prcomment).
- TIER-B list (not implemented): see TOOL-UPDATES.md.

## Grading

All AIID-derived records SECONDARY. Press articles were not fetched, so
nothing is OBSERVED from press. Low-confidence IOCs stay candidate/low.
