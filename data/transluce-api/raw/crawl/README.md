# raw/crawl/ — Transluce evidence-URL captures

135 evidence URLs crawled 2026-10-07 (curl; all HTTP 200), one file per URL.
Naming: `f<finding-id>_<seq>.<ext>` — e.g. `f153_012.html` is finding #153's
12th capture. **Read `MANIFEST.jsonl` first**: it maps every filename to its
source URL, retrieval time, and sha256. A few filenames carry a non-standard
suffix (e.g. `f168_126.119` for an rdap IP lookup) — the suffix mirrors the
MANIFEST `filename` field verbatim, so treat MANIFEST as the index, not the
extension. Collected with `../crawl_urls.py` (see `../PROVENANCE.md`).
