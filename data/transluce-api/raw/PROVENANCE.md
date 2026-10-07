# PROVENANCE — Transluce findings API pull

- Source: https://d3ncjnql1bmhe8.cloudfront.net (Transluce volunteer "Findings tracker")
- Access: bearer API key shared via volunteer Discord (used transiently, never stored)
- Retrieved: 2026-10-07, via curl (Authorization: Bearer)
- Files:
  - raw/schema-v3.json — GET /api/schema (schema version 3)
  - raw/findings-list.json — GET /api/findings (25 findings)
- Note: /api/schema, /api/findings return 401 without the key. No llms.txt found
  at any probed path. Signup is passkey-gated (Discord-shared passkey).
