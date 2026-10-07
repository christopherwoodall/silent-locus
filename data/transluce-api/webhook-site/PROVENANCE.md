# PROVENANCE — webhook.site dead-drop history

- Target: token UUID `9b8517a8-c3b4-4035-81c0-e7844881055e`
  (from COMBO-INIT urlquery report f153_012, finding #153; documented in
  `data/transluce-api/urlquery-reports/FINDINGS.md`)
- Access method: `GET https://webhook.site/token/<uuid>/requests` — the token
  UUID in the path IS the read credential; no other auth required. Read-only;
  nothing was submitted to the inbox.
- Retrieved: 2026-10-07 (UTC), via curl. HTTP 200, 312,520 bytes.
- Files:
  - `raw/requests.json` — full request history (47 requests), sha256 below.
- Sensitivity note (annotated, not redacted): payloads contain the operator's
  dead-drop UUID (already public via the urlquery report) and source IPs of
  the beaconing hosts. Values kept verbatim per the no-redact rule.

SHA-256 of raw/requests.json:
  e9130654d6e71f2a6e839d6e6e7d9082640cc8ae7cb48c5aa91d45b2caa6da09
