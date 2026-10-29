# PROVENANCE — 2022-03-01-jsonhero (ingested into Factum 2026-10-10 UTC)

Factum lane: lane_d2a331be589644038eee576af4e0df4b (title 2022-03-01-jsonhero).
Batch 220b933fe353409090c9080769ff68d8: 24 records tagged {"lane": "2022-03-01-jsonhero"}.
(1 source, 1 dataset.snapshot, 18 infra.ioc [jsonhero.io + 17 shared doc IDs], 3 artifacts, 1 run).
Cite the Factum record IDs in queries; legacy fingerprints are preserved in record tags.

---

# PROVENANCE — data/2022-03-01-jsonhero/

Separate dataset: recon artifacts for jsonhero.io usage by the wiki agent swarms. Kept out of `data/2026-05-17-collusion-wiki/` by design.

## Sources

| File | Source | Retrieved |
|---|---|---|
| `repo_metadata.json` | GitHub API `GET /repos/triggerdotdev/jsonhero-web` | 2026-09-28 |
| `usage_patterns.json` | Derived by grepping `data/2026-05-17-collusion-wiki/raw/*.jsonl` for `jsonhero.io` URLs (read-only) | 2026-09-28 |
| `../notes/recon-jsonhero-2026-09-27.md` | Lane F recon report | 2026-09-28 |

## Method

- Corpus URL extraction: regex `https?://jsonhero.io...` over revisions/pages/events/links dumps; doc-ID, `?path=`, and view-suffix rollups.
- Service description: one normal web read of https://jsonhero.io (homepage) + web search for the repository.
- Repo metadata: unauthenticated GitHub REST API call.

## Limitations

- Agent names in the corpus are publisher-redacted; the 4 named agents are labels, not identities.
- The 17–18 shared document IDs were NOT fetched live (deliberate; left for a follow-up decision).
- No operator identity pursued; infrastructure facts only.

## Keep-all + annotate

No records dropped. `usage_patterns.json` is a lossy rollup; the underlying URLs remain in the collusion-wiki dumps.

## Schema normalization 2026-09-29 (W2)

Built `events.jsonl` (19 rows) from `raw/repo_metadata.json` and
`raw/usage_patterns.json` on the canonical record schema
(`scripts/validate_schema.py`: 19/19 clean).
- 1 × `venue_probe` — triggerdotdev/jsonhero-web repo metadata;
  `@timestamp` = repo.created_at 2022-03-01T09:33:29Z;
  identity `jsonhero|repo|triggerdotdev/jsonhero-web`.
- 17 × `corpus_hit` — one per shared jsonhero.io doc ID with its URL
  occurrence count; no per-ID dates in the rollup, so `@timestamp` uses the
  dir-date prefix 2022-03-01T00:00:00Z with
  `labels.timestamp_source="dir_date_prefix"` (actual usage dates live in the
  collusion-wiki corpus); identity `jsonhero|corpus-doc-id|<doc_id>`.
- 1 × `artifact_observation` — usage rollup (2,398 corpus URL occurrences /
  17 doc IDs / top ?path= params / view suffixes); identity
  `jsonhero|usage-rollup`.
Fingerprint = sha256 hex of the documented identity string (verified against
the 2023-11-14-hfspace-proxies reference implementation before writing).
SHA256SUMS regenerated (events.jsonl + all raw contents); `sha256sum -c` OK.

## Rollup review 2026-09-29 (W8)

rollup: none — the usage aggregate already exists as an event row
(`artifact_observation`, identity `jsonhero|usage-rollup`: 2,398 corpus URL
occurrences / 17 doc IDs); a rollup.jsonl would duplicate it.
