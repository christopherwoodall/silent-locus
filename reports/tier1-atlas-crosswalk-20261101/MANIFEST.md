# MANIFEST — tier1-atlas-crosswalk-20261101

Report dir: `reports/tier1-atlas-crosswalk-20261101/`
Raw lanes: `data/lanes/tier1-atlas-crosswalk-20261101/raw/`
  (ingest, crosswalk, atlas, linguist, cryptologist, behavioral,
  adversarial, verifier — each with PROGRESS.md and per-file
  provenance + sha256 sidecars)
Ingest batch: `data/records/b50b4847b64045f59906e7facdfb4fb4/`
Blobs: `data/blobs/sha256/` (117 files, listed in
  `raw/ingest/BLOB_PATHS.txt`)
Slot-0 source: `data/lanes/general-hunt/raw/0/2026-11-01T114014Z/`

Deliverable files in this dir (hashes in SHA256SUMS):
- REPORT.md
- hits.json
- MANIFEST.md
- adversarial-review.md (copy of raw/adversarial/adversarial-review.md)
- verifier-report.md (copy of raw/verifier/verifier-report.md)

Reviews: adversarial 0 KILL / 8 DOWNGRADE / 3 STAND.
Verifier: SHIP-WITH-FIXES (fixes applied in REPORT.md).
Ingest: batch b50b4847b64045f59906e7facdfb4fb4, 351 records,
  verify --blobs ok.
Commit: unpushed. Push needs the operator's word.
