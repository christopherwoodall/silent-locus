# Phase-2 ingest note — Cohere Qwen hunt hits

- Batch: `data/records/900e2d74dd3c42b1a261205cf8182276/` — 13 records:
  1 run, 5 sources, 7 observations (3 ranked-hit web.capture observations,
  1 appendix web.capture observation, 3 vendor-host infra.ioc observations).
- Idempotency key: `cohere-qwen-hunt-phase2`. Actor: `agent:cohere-qwen-phase2`.
  Lane tag `cohere-qwen-hunt` on every record.
- Source: Fleet B `hits.json` + `REPORT.md` (commit ad9f3b80, verifier SHIP).
  Ingested: the 3 RANKED hits only, all grade SECONDARY, confidence as ranked
  (hit 1 LOW, hit 2 MEDIUM, hit 3 LOW). Triaged-out items were NOT ingested.
  Appendix B/C items were NOT ingested.
- Appendix A context records: the first-party vendor-traffic PR
  (QwenLM/qwen-code#10896, merged 2026-09-05) as one web.capture observation
  plus infra.ioc domain records for its three distinct vendor routing hosts
  (routify.alibaba-inc.com, routify-online.alibaba-inc.com,
  routify-pub.alibaba-inc.com). Vendor traffic, not a hunted incident host.
- Signed-URL rule: parameter names + path shape ONLY. Zero query strings,
  signatures, tokens, or key values in the batch (grep verified: no
  `Signature=`, `OSSAccessKeyId`, `Expires=`, `sv=` substrings; no `?` in any
  ioc term). Raw files were never modified.
- Verification: hit titles, sources, dates, states, and caveats re-checked
  against hits.json + REPORT.md. Issue URLs confirmed from raw comment
  html_url fields (blazux#16, crow#288, qwencode PR #10896); yukino#2 URL
  constructed from repo + number (its comments file is empty, per the report).
  Vendor hosts verified in raw bytes (q4 capture counts 3/2/4; comments file
  holds 2 of 3 — the third is in the PR body via the q4 file).
- Export + verify --blobs after ingest: ok=true, verified=true, pending=0.
  The 1,737 missing artifacts in verify output are corpus-wide pre-existing
  local-only bytes; this batch carries no file artifacts.
- Not pushed by this worker. Parent pushes and verifies.
