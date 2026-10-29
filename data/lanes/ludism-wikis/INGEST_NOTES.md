# INGEST_NOTES — ludism-wikis

Batch `5151ff8d7d2c4ea796b6fd5ea2084a6e`: 58 records
(29 `reachability.check` observations + 29 `source` records).
Tag `{"lane":"ludism-wikis"}` on every record. No edges at ingest.
Zero retractions.

## Legacy row mapping (29 events)

| legacy kind | count | Factum mapping |
|---|---|---|
| venue_probe | 29 | `reachability.check` observation + one `source` record per fetched proxy URL |

Per observation: `body.data.target` = decoded underlying venue URL
(real value, never the internal slug); `method` = GET; `observed_at` =
legacy `@timestamp` with `time_basis` = `legacy_documented`.
Tags carry the verbatim `description`, `legacy_fingerprint`,
`probe.target`/`probe.via`/`probe.proxy_url`, the lane `confidence`
(high=jina control-verified, low=allorigins inconclusive), and, for the
4 probes with captured bodies, `capture.sha256`/`capture.size_bytes`/
`capture.body_path`. Bodies stay as lane documents in `raw/` (no
byte duplication into the batch).

## Outcome mapping

| legacy probe result | count | reachability.check outcome |
|---|---|---|
| ok, HTTP 200 | 3 | `response` |
| RemoteDisconnected | 10 | `connect_failure` |
| IncompleteRead (truncated body) | 1 | `connect_failure` |
| HTTPError 522 (proxy-side timeout) | 8 | `timeout` |
| HTTPError 422 (jina: origin unfetchable) | 3 | `unknown` |
| HTTPError 500 (proxy-side error) | 2 | `unknown` |
| HTTPError 400 (proxy-side error) | 1 | `unknown` |
| failed, no error recorded (allorigins control) | 1 | `unknown` |

## Discrepancies found (documented, legacy bytes untouched)

- PROVENANCE.md says proxy controls are marked `labels.proxy_control =
  true`. Both control records in `events.jsonl` actually carry
  `"probe.proxy_control": false` (the W7 builder never set the flag).
  Factum tags set `probe.proxy_control: true` for the two records whose
  `probe.target` is `proxy_control (example.com)`; this is a metadata
  correction on new records, not an edit of legacy evidence.
- The allorigins_raw control "FAILED (None)" but captured a 16-byte body
  reading `error code: 522`. Preserved verbatim in
  `raw/proxy_control__allorigins_raw.txt`; mapped outcome `unknown`.
- The jina control (example.com, ok) records no `http_status` in labels;
  no `http_status` submitted for it. No value invented.

## Validation

- Pre-ingest dedup: `match --text` (fuzzy) for the full jina fetch URL,
  `ludism.org`, `tmcleod`, `allorigins`, and `venue_probe` against the
  corpus — no existing probe records (the 9 `allorigins` hits are
  `infra.ioc` sweep-pattern records from lane
  `2026-09-05-termina-digital`, a different shape). Batch-internal dedup
  by (probe.target, probe.via): 29 unique.
- Adversarial validator (`/tmp/ludism_adversarial.py`, ephemeral):
  every observation field traced byte-for-byte to `events.jsonl`
  (description, proxy_url, error, http_status, timestamp, fingerprint);
  venue URL decoded from the exact fetched URL; outcome rule applied
  uniformly; no placeholders; source refs all resolve. PASSED.
- One submit-time schema fix: `type` belongs inside `body`, not at
  record level (bundle schema rejects `additionalProperties`). Noted
  for future workers: copy the `template --bare` shape exactly.

## Root-cause notes for the next worker

- `uv` is not on the default PATH; it lives at `~/.local/bin/uv`.
- `factum query --input` takes a file path, not inline JSON.
- `lane edit --tags` REPLACES tags instead of merging — always pass
  the complete tag set in one edit.
