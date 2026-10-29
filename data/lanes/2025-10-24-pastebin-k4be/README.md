# 2025-10-24-pastebin-k4be

Pastebin.k4be.pl agent-swarm paste dataset.

## Source

Public investigation export `agent-logs/pastebin-k4be/` of
[JoshuaDavid/WikiAgentSwarmInvestigation](https://github.com/JoshuaDavid/WikiAgentSwarmInvestigation)
(branch `main`, read 2026-10-05). Their export: direct scrape of
`https://pastebin.k4be.pl` on 2026-09-07, filtered to 198 agent-swarm-surface
pastes. The paste hosts were never probed.

## Factum records

- 178 `infra.message` observations: one per paste, body verbatim from
  `raw/<paste_id>.txt` (all 198 manifest SHA-256 checks passed; 12 bodies keep
  CRLF line endings).
- 1 `source` record for the investigators' export.
- Tag: `{"lane": "2025-10-24-pastebin-k4be"}` on every record.
- 20 of 198 pastes were already in the corpus as `infra.message` observations
  from lane `2026-05-27-paste-archive` (same paste IDs, live-get copies).
  True duplicates. Skipped, not re-submitted. IDs:
  11e9447e, 1d6736e9, 1fad07cb, 21c68f36, 52400bf5, 57492617, 5c15bef1,
  5d1004ff, 64d1bc5e, 6a9925f1, 6db42cfc, 8812970e, 8c3a5621, 98ad943e,
  9e4ecc8b, ad00ad72, bd25603e, cbf4b460, d826348b, e3657127.

## Time span

Stikked `created` field: 2025-10-24 to 2026-09-05. Uncorroborated.
`paste.jd_time` kept per record; `posted_at` uses it with grade
`api_paste_created_field (uncorroborated)`.

## Verdicts (investigator labels)

- 126 shellac-imported rows (no verdict), 51 `swarm`, 21 `unclear`.
- Keep-all policy: all rows ingested, including `unclear` rows. Downstream
  precision filters should use `tags."paste.jd_verdict" != "unclear"`.

## Artifacts

- `raw/<paste_id>.txt`: verbatim paste bodies (199 files: 198 pastes +
  `manifest.jsonl`).
- `events.jsonl`: legacy `relay_paste` records (198).
- `rollup.jsonl`: 24 per-day burst rows, kept as legacy.
- `PROVENANCE.md`: full acquisition history.
