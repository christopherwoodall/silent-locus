# SCHEMA.md — CDX row → openai-agent-traces record

Source CDX JSONL rows (Arquivo.pt): fields `urlkey`, `timestamp`, `url`,
`mime`, `status`, `digest`, `length`, `offset`, `filename`, `collection`,
`source`, `source-coll`.

Every record also conforms to the shared `schema/record.schema.json` required
fields: `@timestamp`, `event`, `record_kind`, `fingerprint`, `labels`.
(`fingerprint` and `labels` are required there, so we populate them; see below.)

## Field mapping

| corpus field | CDX source | notes |
|---|---|---|
| `_id` | computed | = `trace_id`; the loader (`scripts/push_to_local_es.py`) uses the doc's own `_id` → deterministic ES ids, idempotent reruns |
| `trace_id` | computed | `sha256("arquivo-pt\|<incident>\|<timestamp>\|<url>")` — deterministic; re-runs never duplicate |
| `@timestamp` | `timestamp` | CDX `YYYYMMDDhhmmss` → `YYYY-MM-DDTHH:MM:SSZ` (UTC). Null only if the CDX stamp is malformed (none observed) |
| `record_kind` | fixed | `"arquivo_pt_capture"` |
| `event.dataset` | fixed | `"openai-agent-traces"` — the ES index name |
| `event.created` | computed | mapper run time (UTC ISO). Not a source property; changes between runs |
| `fingerprint` | computed | `sha256` of canonical JSON `{trace_id, url, timestamp, status, digest}` — content-derived, run-independent |
| `labels.incident` | computed | incident slug from the source filename prefix (e.g. `doe-crdc`) |
| `labels.source_system` | fixed | `"arquivo-pt"` |
| `labels.source_pull` | fixed | `"2026-10-01 pull (collections/arquivo-pt)"` |
| `labels.source_file` | computed | repo-relative source gz path |
| `labels.source_line` | computed | 1-based line number of the kept row in the source gz (first-seen row wins dedup) |
| `labels.cdx_timestamp` | `timestamp` | raw CDX stamp, preserved verbatim |
| `labels.collection` | `collection` | CDX collection (e.g. `SAWP5`) |
| `labels.source_coll` | `source-coll` | CDX source collection (e.g. `$root`) |
| `labels.warc_filename` | `filename` | WARC file holding the capture |
| `labels.warc_offset` | `offset` | byte offset in the WARC |
| `labels.warc_length` | `length` | record length |
| `source_url` | `url` | captured original URL, verbatim |
| `status` | `status` | HTTP status as string |
| `mime` | `mime` | CDX mime |
| `digest` | `digest` | CDX digest (base32 sha1) |
| `size_bytes` | `length` | int; null if non-numeric |
| `file` | computed | repo-relative source artifact (same as `labels.source_file`) — satisfies the schema's "row's source artifact exists on disk" promise |
| `tags` | computed | `["oai-tagged"]` when `zz=oai<digits>` present in the URL, else `[]` |
| `features.query_param_names` | `url` | ordered unique query-param names from the captured URL |
| `features.probe_flags` | `url` | conservative markers, incident-specific (see below) |
| `notable_query_params.zz` | `url` | the `oai<digits>` tag value when present; object is `{}` when absent |

### Divergences from the shared schema / CDX source

1. **CDX `urlkey` is dropped.** It is a SURT-canonicalized key, fully derivable
   from `url`; keeping `source_url` verbatim preserves the bytes.
2. **`source` (CDX) is not mapped.** It is always `$root:SAWP5.cdxj` — a
   constant of this pull; superseded by `labels.source_system`/`source_pull`.
3. **Attribution fields are ours, not the source's:** `attribution.provider`,
   `attribution.eval_family`, `attribution.agent_instance`, each with
   `attribution.note` documenting the evidence rule. See below.
4. **`event.created` is mapper-run time**, unlike source-derived fields — the
   one field expected to differ across re-runs (state.json timestamps are the
   other).
5. **No payload bodies.** The CDX pull carries only capture metadata; request
   bodies / response content are in WARC files we do not hold.

## Attribution rules (three levels)

| level | field | rule |
|---|---|---|
| provider | `attribution.provider` | `"openai"` **only** when the captured URL carries a `zz=oai<digits>` param (the OpenAI-attributed SQLi/fuzz cluster); else `null` |
| eval family | `attribution.eval_family` | `"deepsearchqa/dsqa_250"` **only** for `doe-crdc` rows with provider=`openai` (the confirmed dsqa_250 incident traffic); else `null`. Other incidents' eval attributions are open |
| agent instance | `attribution.agent_instance` | always `null` — no row-level evidence ties captures to specific agent instances. The 14,449 distinct `zz=oai<digits>` values are *candidate session labels*, recorded in `notable_query_params.zz`, not attribution |

Scope guard: agents and agent infrastructure only. No human/operator identity
is pursued or recorded anywhere in this corpus.

## Probe flags (`features.probe_flags`)

Conservative substring heuristics over the captured URL only — they describe
what the URL bytes look like, not intent:

- `doe-crdc`: `sqli_probe` (`State_Id` + ` OR ` / encoded-or), `fuzz_ladder`
  (comma/number fuzzing of `State_Id`), `crdc_measure_params`
  (`survey_Year_Key`/`Measure_Id` present).
- `lac-collectionsearch`: `sqli_probe`, `xss_probe`, `integer_overflow_probe`
  (`2147483648`), `fuzz_probe` (`?output=`/`?raw=`/`?url=`/`debug=1`) — the 13
  documented payloads.
- All other slugs: `[]` (no flag rules defined).

## Loader mechanism (documented per task)

The repo loader auto-discovers `data/YYYY-MM-DD-<slug>/events.jsonl`. The
corpus canonical file is `openai-agent-traces/data/traces.jsonl`; the loader
entry point `data/2026-10-03-openai-agent-traces/events.jsonl` is a **relative
symlink** to it (not a copy — a copy would drift). `SHA256SUMS` in the
collection dir records the dereferenced content hash. Records carry
`event.dataset = "openai-agent-traces"` (registered as `dataset_override` in
`schema/collections.json`), so the index is `openai-agent-traces`.

Ingest: `python3 scripts/push_to_local_es.py --index openai-agent-traces`
(local ES only; hosted ES is frozen).
