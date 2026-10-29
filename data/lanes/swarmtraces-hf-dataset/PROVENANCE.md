# PROVENANCE — swarmtraces-hf-dataset lane

## Source

- **Dataset**: SwarmTraces "OpenAI agents hacked Hugging Face" (July 2026
  incident) redacted release.
- **Locator**: `https://swarmtraces.org/data/final/redacted.jsonl.gz`
- **Local copy**: `evidence/raw/redacted.jsonl.gz` (shared raw storage;
  NOT renamed — it is shared, not a lane dir).
- **sha256**: `7b66ab21674de52fcd3f557652f68b1801170c998e2f266862124e6edf283488`
- **Retrieval date**: 2026-09-27 (per
  `evidence/raw/swarmtraces_provenance.json`).
- **Size**: 15 MB compressed; 189,579 JSONL records.

## Record layout (verified from bytes)

Uniform 7-field records: `id` (R0000001–R0189579, zero gaps), `cite`
(R-id + 8-hex token), `kind` (payload 91,037 / recovered_text 75,534 /
response 23,008), `parent_id` (null on all payloads; 61,125 non-null),
`time_utc` (null on all 189,579 records — no timestamps anywhere),
`tags` (empty string), `text` (redacted payload/response content).

## Method

Giant-lane aggregation (no 1:1 ingest of 189,579 records):

1. `build_bundle.py` — single streaming pass over the gzip. Extracts
   literal (non-redacted) URLs with exact-match semantics: any URL
   containing `[`, `REDACTED`, `CREDENTIAL`, or `SERVICE` is discarded, so
   counted values are complete observed strings, never redaction-truncated
   prefixes. Counts are per-record (records containing the value).
   Chain depth by parent-link walk. Redaction-slot token cardinality via
   set accumulation.
2. `validate_bundle.py` — independent re-derivation from bytes with its
   own regexes. Checks envelope, tag-string rule, claim shape, every IOC
   count, chain stats, slot cardinalities, snapshot fields, verbatim
   spot-checks. All checks passed.
3. Dedup: file-level grep over all committed `data/records/*/records.jsonl`
   for every candidate term, plus `match --text --mode fuzzy` spot queries.
   Related-but-distinct records noted in provenance/tags (edge-building
   pass can link them later).

## Dedup decisions

Submitted (genuinely new literal values):

- 6 domain IOCs, 20 URL-prefix IOCs, 8 tailscale build URLs, 10 zz-marker
  Artifactory full URLs, 1 IP IOC (169.254.169.254).
- 1 source (dataset URL), 1 run, 1 dataset.snapshot, 5 OBSERVED claims.

Skipped (already in corpus):

- Corpus record counts, field stats, redaction-marker occurrence counts,
  parentage topology counts, cite-token semantics — all claimed in lane
  `2026-09-27-swarmtraces-verification` (5 claims). Not re-submitted.
- Redaction-slot placeholder tokens (`[SERVICE N URL M]` etc.) as IOCs —
  not concrete values (taxonomy precedent: indicator names are not IOCs).
  Their distinct-token cardinality is claimed instead (new dimension).
- `github-remote-cache/zz` and `artifactory/github-remote/...` fragment
  IOCs exist (lanes `2026-10-01-intermediary-relays`,
  `2026-09-28-ace-research-ct`); the full-URL forms submitted here are
  distinct values, cross-referenced in tags.
- `https://swarmtraces.org/` source exists (lane
  `2026-09-28-pastebin-pivot`); the dataset-URL source submitted here is a
  different locator.

## Key findings

- The Artifactory board host `packages.hub.ace-research.openai.org`
  appears in 1,983 records across 760 distinct literal URLs, with 629
  distinct zz-prefixed path terms — the zz grammar marker family is
  present in the HF incident corpus.
- 5 recovered_text records contain AWS IMDSv2 token-request code against
  `http://169.254.169.254/latest`.
- Parent chains are flat: all 61,125 parented records at depth 1, zero
  multi-hop chains, 26,248 distinct parents, zero dangling references.
