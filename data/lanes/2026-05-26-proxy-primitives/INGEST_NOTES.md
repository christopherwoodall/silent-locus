# Ingest notes — 2026-05-26-proxy-primitives (standard)

## Record mapping (legacy record_kind -> Factum type)

| legacy kind (count) | Factum type (count) | note |
|---|---|---|
| wiki_link (553) | infra.proxy_chain (122) / infra.proxy_instance (301) | 262 withheld-URL + 39 null-target rows -> instance; 130 dupes |
| wiki_record_annotation (128) | infra.proxy_chain (51) / infra.proxy_instance (9) | malformed matched_strings cleaned; 68 dupes |
| wiki_shortener (4) | infra.proxy_chain (2) | 2 dupes |
| wiki_ioc_pivot (827) | infra.proxy_chain (416) / infra.proxy_instance (3) | 408 dupes (same rows as sibling lane's chains) |
| corpus_hit (3) | infra.ioc (2) | bare hosts api.cors.lol, pure.md; 1 skipped (URL in corpus) |
| gem_name_fragment (6) | infra.ioc (3) | deduped within batch by term (zjgview5, zrgview1, zrgview2) |
| wiki_revision (1) | infra.ioc (1) | term=gview, first-seen evidence |

Total submitted: 914 records (910 observations, 1 source, 1 run, 2 claims).
Skipped: 612 (drop_log.json).

## Field conventions

- `target_url` = the invocation URL exactly as observed (triple-decoded
  `matched_string`), following the sibling-lane convention
  (2026-10-01-intermediary-relays stores the relay-invocation URL, not the
  final destination). The best-effort parsed destination stays in
  `tags.laundered_target`.
- `proxy_service` = leftmost host of the invocation URL (e.g. jqp.vercel.app
  for jqp-wrapped api.cors.lol URLs); the sweep's `primitive` label is kept
  in tags.
- `chain` = single-element `[proxy_service]` (direct use).
- `observed_at` = legacy `first_seen_effective` (earliest wiki revision
  write_date), `time_basis` = `source_metadata`; rows with no recoverable
  date use the 1970-01-01 sentinel with `time_basis` = `unknown`.
- Withheld/unusable URLs (262 `[operational URL omitted; host=pure.md;
  sha256=...]` wiki_link rows, 1 `host=pure.md;` fragment) become
  `infra.proxy_instance`: host from row labels, verbatim placeholder as
  `invocation_shape`, `access` = `unknown`. No URL is invented.
- Malformed matched_strings are cleaned before use: leading `[` stripped,
  `&url=` fragments resolved to the inner URL, trailing dots stripped.

## Dedup (pre-ingest, against exported batches)

URL-variant match (on the cleaned URL) over all corpus
`infra.proxy_chain` target_urls; exact term match for ioc candidates;
within-batch term dedup for gem_name_fragment. 608 rows collide with
existing chains (mostly via sibling lane 2026-10-01-intermediary-relays,
which ingested the same wiki_ioc_pivots.jsonl source as chains). Skipped
per the pre-ingest dedup rule; every skip is in drop_log.json with its
legacy fingerprint (validator cross-checks the dup set exactly).

## Root cause found during ingest

The first bundle mapped the 262 withheld-URL rows to `infra.proxy_chain`
with the placeholder text as `proxy_service` (garbage). Fixed: withheld
rows now become `infra.proxy_instance` with the verbatim placeholder as
the shape. Also fixed: 4 drop_log entries missing `legacy_fingerprint`,
and chain tags missing verbatim `matched_string`. Both caught by the
independent validator.

## Overlap

The 608 skipped rows are the same evidence the sibling lane ingested as
chains (same matched_string, same agent samples). Pivot agent-prevalence
(n_agents, wikis, agents_sample) is preserved in tags on the submitted
rows.

## Edges

No edges submitted during ingest.

## Batches

One bundle, idempotency key `2026-05-26-proxy-primitives-v1` (914 records).

## Validator

`validate_bundle.py` — independent re-derivation (kind counts, own dup-set
recompute matched by legacy fingerprint: 612 exact), bundle structure,
schema-required fields, ioc status enum, all-string tags,
proxy_service sanity (no placeholders/brackets), verbatim spot-checks.
PASS.
