# PROVENANCE — 2026-10-09-transluce-intel

Reconstructed source lane for the 109 Transluce finding claims held in the
Factum corpus. Built 2026-10-09 on branch `factum-shaping` as part of the
Factum rebuild (missing-lane construction).

## Source

- Primary source: Transluce volunteer Findings tracker API,
  `d3ncjnql1bmhe8.cloudfront.net`, pulled read-only via the `transluce`
  skill CLI (`bin/tl.py`) using the `custom.transluce` connector
  (bearer token via Secure Vault surrogate — never handled directly).
- Cached pull: `raw/findings-list-20261008.json` (copied verbatim from
  `evidence/transluce-api/raw/findings-list-20261008.json`).
  Retrieval: 2026-10-08T12:41Z, paginated `GET /api/findings`
  (the `tl.py findings` wrapper returns only the first 25;
  `tl.py export json` truncates at 200KB).
- Tracker record: `evidence/transluce-api/LEDGER.md` (daily ingest log,
  run `transluce-daily-ingest` ~07:40 CDT).

## Extraction method

Script `/tmp/build_transluce_lane.py` (ad-hoc, not retained in repo):
read the cached pull JSON and emitted one legacy-lane event per finding
(109 events), preserving the full verbatim finding record (id, submitter,
submitter_id, form_version, sensitive, created_at, updated_at, and the
complete `data` object: summary, description, evidence_links, cyberattack,
government, ai_company, harm_level, untapped_source) under the `finding`
key of each event. Nothing was redacted or truncated; `sensitive` is false
for all 109 findings.

Event envelope follows the existing legacy-lane convention
(@timestamp / event.dataset / record_kind / fingerprint / labels /
source_url / retrieved_at / retrieved_via / description).
`@timestamp` is the finding's own `created_at`; `retrieved_at` is the
API pull time (2026-10-08T12:41Z), not the finding publication time.
`fingerprint` is sha256 of the canonical (sorted-keys, no-whitespace)
JSON of the event body, excluding the fingerprint field itself.

## Coverage

- 109 findings, tracker IDs 36–174 (sorted). The tracker ID sequence is
  not dense: 30 IDs in range are absent from the pull
  (47, 49, 50, 51, 52, 58, 59, 64, 65, 84, 88, 89, 90, 95, 100, 102,
  103, 105, 106, 117, 121, 126, 134, 145, 151, 156, 158, 162, 164,
  165) — likely deleted or restricted findings on the tracker; not a
  collection error.
- Form versions: v2, v3, v4 (form_version in labels).
- `source_url` per event is the canonical tracker URL
  `https://d3ncjnql1bmhe8.cloudfront.net/findings/<id>`.
- Newest finding in the pull: #174 (WildClawBench credential-commit test),
  created 2026-10-08T10:38:12Z.

## Notes and limits

- Factum rule: do not treat retrieval as factual verification. These
  events carry UPSTREAM claims (the finders' own grades) alongside the
  tracker's verbatim text.
- The tracker's attachments and private reports were not searched by the
  original ingest (only summary/description/evidence_links were checked).
- Findings submitted by the user/operator himself (#170 Nav 2025 jina
  laundering, #171 dead-drop family — our submissions 001/003) are
  present in the pull like any other finding.
- The Transluce external-submissions freeze (2026-10-08, BigSexyWarlock69)
  does not affect this read-only lane build.
- What would be needed to extend: the daily-ingest cron keeps pulling
  new findings; a re-pull after 2026-10-08 would add IDs > 174 and fill
  any restored missing IDs.

## Grade

All claims in this lane are the tracker's own (UPSTREAM) unless the
finder's text itself states an observation grade.
