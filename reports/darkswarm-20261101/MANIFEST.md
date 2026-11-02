# DarkSwarm ingest — manifest

- Source: https://github.com/SauersML/DarkSwarm, branch main,
  HEAD be21462916e9f94ee7ff2ad48eb6c82b92d1617e.
- Lane: data/lanes/darkswarm-20261101/ (raw + work).
- Factum batch: data/records/8b87915d91ce4e7284fbbfdb1ad60f60/
  (91 records: 88 claims + 1 source + 1 observation + 1 artifact).
- Lane tag: darkswarm-20261101 on all 91 records (tag-only grouping).
- Claims: 94 graded (7 OBSERVED, 81 REPORTED, 6 INFERENCE).
- Adversarial: KILL 6, DOWNGRADE 81, STAND 7. Top 20: 0 STAND.
- Verification: 41 assessed — VERIFIED 3, PARTIAL 8, CONTRADICTED 0,
  UNCHECKABLE 30.
- Novelty: 10 subjects — NEW 6, OVERLAP 4 (surface only), PENDING 0.
- SHA256SUMS check: 4 of 4 OK (run 2026-11-02, before commit).
- This manifest does not cover the lane raw/work files or the Factum
  batch. Those carry their own sidecars (raw: .PROVENANCE.txt + .sha256
  per file, 51 of 51 verified; batch: manifest.json + records.jsonl).

## Files and SHA-256

- REPORT.md: 62b690ff4292fe341b6d1ad74eee76e8b59fac5fb834a08c656210c5e47d9818
- hits.json: 76d76b53f5e6c59b3f8fd1377786246735db794f1774ed9de8bacedf55fea55a
- adversarial-review.md: f9f6b785e2c1a40a61703f1662affbb2af67730167e5c2366a78d41cae69eebf
- verifier-review.md: d84f2e355694610a84050378434e8e8a132ede37adb87d8c787ad8bf07cfe101
