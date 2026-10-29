# PROVENANCE — Transluce findings API pull

- Source: https://d3ncjnql1bmhe8.cloudfront.net (Transluce volunteer "Findings tracker")
- Access: bearer API key shared via volunteer Discord (used transiently, never stored)
- Retrieved: 2026-10-07, via curl (Authorization: Bearer)
- Files:
  - raw/schema-v3.json — GET /api/schema (schema version 3)
  - raw/findings-list.json — GET /api/findings (25 findings)
- Note: /api/schema, /api/findings return 401 without the key. No llms.txt found
  at any probed path. Signup is passkey-gated (Discord-shared passkey).

## Crawl of finding evidence URLs (2026-10-07)
- Inventory: data/transluce-api/url-inventory.jsonl (139 URLs; 135 NEW, 4 HAVE)
- Method: data/transluce-api/crawl_urls.py — curl-based, priority urlquery
  reports → web.archive.org (http://, port 80) → rest; ~2 req/sec per host,
  backoff on 429/503. No logins, no submissions.
- Output: raw/crawl/ (raw bytes, f<finding_id>_<seq>.<ext>) + raw/crawl/MANIFEST.jsonl
  (url, finding_id, filename, retrieved_at_utc, method, http_code, sha256, size_bytes, error)
- Result: 126/135 fetched OK (15,454,310 bytes); 9 failed with honest HTTP errors
  (1x404, 1x405, 7x403 anti-bot on live sites). No content redacted.

## Findings list pull (2026-10-08)

- File: raw/findings-list-20261008.json — paginated GET /api/findings?limit=100&offset=N
  via curl + Secure Vault surrogate (custom.transluce); tl.py CLI only returns
  the first 25 and its export truncates at 200KB, so pagination was required.
- Retrieved: 2026-10-08 ~12:41Z (07:40 CDT run).
- sha256: 65681e8cf8815011c86a973e4edf708761f7ace18583588c9260f04053fc4ab2
- Result: 109 findings total (25 covered by the 2026-10-07 file; 84 seen via
  pagination for the first time; 5 genuinely new by created_at, ids 170-174).
- New findings logged in ../LEDGER.md; 15 new evidence URLs appended to
  ../url-inventory.jsonl (139 -> 154 rows).
