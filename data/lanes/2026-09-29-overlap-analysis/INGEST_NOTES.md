# Ingest notes — 2026-09-29-overlap-analysis (aggregation)

## Aggregation (not 1:1)

17,038 overlap_match rows = 7,982 unique matches (every fingerprint appears
twice: matches-f5f6.jsonl and overlap-matches.jsonl carry the same rows, per
lane PROVENANCE.md) + 317 paste_link rows (131 distinct paste IDs) collapse to
  - 1 run record (the analysis),
  - 1 source record (lane locator),
  - 15 `infra.ioc` observations (confirmed-present IOCs),
  - 8 OBSERVED claims (coverage + per-family findings + paste links).

Total: 25 records. Idempotency key `2026-09-29-overlap-analysis-v1`.

## IOC selection

Only confirmed-present terms become `infra.ioc` (status `active`):
F1 `httpbun.com` (domain); F3 `zzWAFBRIDGE25167`,
`zzHFPOSTRCE_WT8592N19_BEACON_` (markers); F6
`packages.hub.ace-research.openai.org`,
`packages.app.ace-research.openai.org` (domains); F5 64H-series stems
(OTS92, G236, SC4, Future9180, BE90, LIBR11, 3FR64, EARLY64, MARB051,
GSTX64) (markers).

Not minted: miss-kind terms (confirmed absent from the 189,579-record
dataset -- no "absent" status exists; covered in the negative_sweeps claim),
near/weak-string/lexical-only terms (covered in family claims),
`github-remote-cache/zz` (already an `infra.ioc` in the corpus -- skipped,
annotated in the F3/F6 claims).

## Timestamps

Rows carry no recoverable event times (1970 sentinel in legacy).
`observed_at` = 2026-09-29 (analysis date), `time_basis` =
`legacy_documented`.

## Dedup (pre-ingest, against exported batches)

All 15 IOC terms checked against corpus `infra.ioc` terms and
`infra.proxy_chain` target_urls: 14 new, 1 already present
(`github-remote-cache/zz`, skipped with annotation).

## Claims

coverage, family_f1_markers, family_f2_epochs, family_f3_board_path,
family_f5_64h_stems, family_f6_beacon_paths, negative_sweeps,
paste_link_coverage -- all OBSERVED, all cite the run record. The F5 claim
notes the pre-screen/contextual discrepancy (Future9180, SC4: zero hits via
bounded-token regex pre-screen, but present as contextual stems).

## Edges

No edges submitted during ingest.

## Validator

`validate_bundle.py` — independent re-derivation (17,038 rows / 7,982
unique / 317 paste_links), 15 unique IOC terms, github-remote-cache/zz
absent, 8 claims all citing the run. PASS.
