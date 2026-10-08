# schemas/url-inventory.md

Canonical URL inventories. One JSON object per line (JSONL).

## `lists/urls/urls.jsonl` — CANONICAL home for new URLs

Fields (observed from real rows):
- `url` — the full observed URL string, exactly as seen. Never normalized
  before storage; normalization goes in `canonical`.
- `canonical` — canonicalized form (sorted query params, percent-encoding
  normalized). This is the dedupe key.
- `finding_id` — Transluce finding number this URL came from (int), or
  null for farm-derived URLs.
- `submitter` — finding submitter name as recorded on Transluce, or null.
- `source_field` — which finding field the URL was pulled from
  (e.g. `evidence_links`), or null.
- `status` — `NEW` | `HAVE` (already in corpus) | `DEAD`
  (verified unreachable). Status reflects verification state.
- `corpus_path` — path into our corpus where the URL appears
  (e.g. `data/transluce-api/wildclaw/...`), or null if not in corpus.
- Farm rows may add: `tier` (laundering tier), `occurrences` (hit count).

Dedupe: exact match on `canonical`. Zero duplicates is the rule; dedupe
commands live in `lists/README.md`.

## `data/transluce-api/url-inventory.jsonl` — LEGACY, READ-ONLY

Same fields as above. Do NOT write new URLs here — active code still
reads it, which is why it stays. All new URLs go in `lists/urls/urls.jsonl`
only.
