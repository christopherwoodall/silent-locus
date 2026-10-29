# Provenance — Docker Hub trojan-image enumeration (Lead 1 of 6)

Retrieved 2026-09-28 ~23:35–23:56 UTC (18:35–18:56 CDT); deep-pagination resume attempt 2026-09-28 23:58–2026-09-29 00:07 UTC. Read-only.

## Sources (all public, no accounts, no logins)

| Source | Used for | URL pattern |
|---|---|---|
| Docker Hub web API v2 (anonymous) | org repo lists; per-repo tag metadata (names, `tag_last_pushed`, `last_updated`, `tag_status`, digest, arch) for the newest 1000 tags per repo | `https://hub.docker.com/v2/repositories/{org}/?page_size=100`, `https://hub.docker.com/v2/repositories/{org}/{repo}/tags?page_size=100&page={1..10}`, `…/tags/{tag}` |
| Docker registry API (anonymous pull-scope token from `auth.docker.io`) | COMPLETE tag-name lists for every repo (both orgs) | `https://registry-1.docker.io/v2/{org}/{repo}/tags/list?n=1000` |
| Local corpus | reference set of agent-uploaded trojan tag names | `data/aggregates/2026-09-29-overlap-analysis/events.jsonl` (merged home of both standalone files; Artifactory `dockerhub-public[/-cache]/…` path references) |

## Method

1. `org-{cybergym,n132}-repos.json` — full org repo listings (Hub API, page 1 of 1 each).
2. `registry-tags-{org}-{repo}.json` — complete tag-name sets via registry `tags/list` (20 repos; 37,437 tags total). Cached; the fetch script skips existing files (resumable).
3. `hub10-{org}-{repo}.jsonl` — tag metadata (newest 1000 per repo, Hub API pages 1–10). For repos with ≤1000 tags this is the complete set with timestamps.
4. `corpus-trojan-tag-liveness.jsonl` — per-tag Hub lookups for the 5 corpus-referenced trojan tags (live vs 404).
5. `final-{org}-{repo}.jsonl` — merged per-repo records: `org, repo, tag, tag_last_pushed, last_updated, tag_status, digest, images_arch, metadata_fetched, liveness, retrieved, sources`. `final-gone-trojan-tags.jsonl` holds the 3 corpus tags that 404.

## Constraints encountered (documented, not worked around)

- Docker Hub API rejects anonymous pagination past offset 1000: HTTP 403 `{"message":"pagination offset too large for anonymous requests; sign in to page further"}`. No login was created (read-only guard). Consequence: Hub metadata covers only the newest 1000 tags per repo for the 4 large repos (`cybergym/arvo` 10,280; `cybergym/oss-fuzz` 1,256; `cybergym/v8` 1,121; `n132/arvo` 23,907).
- July-2026 detection is still complete: Hub tag listing is ordered newest-first, and the newest fetched tag in each large repo predates (arvo: 2026-05-31; oss-fuzz: 2026-05-31) or brackets (v8: Aug pushes present, zero July; n132/arvo: 2026-02-19) the July window. Any July push would necessarily sort above the fetched newest tag.
- Registry `tags/list` has no anonymous pagination cap; tag names are complete. Timestamps for tags beyond the newest 1000 are not available without a Hub login or config-blob reads (blob reads were out of scope).
- No image pulls, no layer/blob GETs, no manifest content reads beyond Hub metadata. Manifest digests were recorded from Hub metadata only.
- `n132/arvo` registry count (23,907) vs Hub `count` (23,900): 7-tag drift between the two fetches (~2 min apart); registry list is the fresher value.

## Scripts

- `fetch_tags.py` — deep-pagination path (pages 11+); resume of `cybergym/oss-fuzz` pages 11–13 attempted 2026-09-28 23:58 → 2026-09-29 00:07 UTC: HTTP 403 on all 8 tries (5s→120s backoff) at `page_size=100&page=11`, then `RuntimeError: failed after 8 tries`. This CONFIRMS the anonymous-pagination wall is standing policy, not a transient block — the task's own probe that returned HTTP 200 was on offset 13 (`page_size=1&page=13`), i.e. below the 1000-offset cap, so it never tested the wall. No login created, no evasion attempted; stopped per instructions. Script kept for the audit trail.
- ES ingest: QUEUED — `ELASTIC_WRITE_PAUSE` in effect; dataset lives disk+git only. Post-pause, ingest `final-*.jsonl` + `corpus-trojan-tag-liveness.jsonl` under the shared schema (notes/gems-es-mapping.json, `event.dataset.keyword` multi-field at index creation).
- `registry_tags.py` — registry `tags/list` enumeration (resumable, skips cached files).
- `fetch_hub10.py` — Hub pages 1–10 metadata (resumable, skips cached files).
- `fetch_stdout.log`, `registry_stdout.log`, `hub10_stdout.log`, `progress.log` — run logs.

## Corpus reference set (trojan tag names from our own data)

Extracted from Artifactory `dockerhub-public[/-cache]/` path references in `data/aggregates/2026-09-29-overlap-analysis/events.jsonl` (merged home of both standalone files):
`cybergym/arvo:zzgptimg21784227813`, `cybergym/arvo:jan29pcldummy1700`, `cybergym/arvo:x114sinkbrowsedef`, `cybergym/arvo:27871-vul.exp.none-nogit`, `cybergym/oss-fuzz:42537601-vul.exp.none-nogit`.

## Schema backfill 2026-09-29

All 42 `*.jsonl` files (42,318 records) brought onto the shared record schema
(`schema/record.schema.json`) by `temp/backfill_w1.py`. Lossless: no field was
dropped; dataset-specific fields moved under `labels`.

- `event.dataset` = `dockerhub-trojan-images`; `event.created` = backfill run
  time (UTC). No record had a pre-existing `event`/`fingerprint`/`@timestamp`.
- `@timestamp` = the record's `retrieved` value (the liveness/listing probe
  time IS the event time), promoted to canonical `retrieved_at` and mirrored
  to `@timestamp` (UTC `Z`). `labels.timestamp_source = "retrieved_at"` on
  every record (sentinel fallback never needed — all 42,318 rows carry
  `retrieved`).
- `status` (corpus-trojan-tag-liveness) and `liveness` (final-*/gone files)
  coalesce to canonical `status`; the two never co-occur in one record.
- `source` -> `source_url`. `sources` (array) -> `source_url` when it holds
  exactly one non-null entry, otherwise preserved verbatim as
  `labels.sources` (final-* records carry `[registry_url, hub_url|null]`).
- `note` (final-gone-trojan-tags) kept as canonical top-level `note`.
- Moved to `labels` (flat, unchanged names): `org`, `repo`, `tag`,
  `tag_last_pushed`, `last_updated`, `tag_status`, `digest` (kept as the
  `sha256:…` digest string, NOT the canonical `sha256` field), `images_arch`,
  `metadata_fetched`.
- `record_kind`: `tag_liveness` for per-tag liveness probes
  (corpus-trojan-tag-liveness, final-*, final-gone-trojan-tags);
  `tag_listing` for registry/hub tag-listing records (hub10-*, repo-*).
  Both are new kinds added to the registry by this dataset.
- Fingerprint identity string: `family + "|" + org + "|" + repo + "|" + tag`
  where `family` is the filename prefix (`corpus` | `final` | `gone` |
  `hub10` | `repo`; `final-gone-trojan-tags.jsonl` uses `gone`). The family
  prefix keeps fingerprints distinct when the same tag is probed by
  different sweeps (e.g. cybergym/arvo:zzgptimg21784227813 appears in both
  corpus-trojan-tag-liveness and final-gone-trojan-tags).
- Script is idempotent: records already carrying `event.dataset` +
  `fingerprint` pass through untouched. Post-run:
  `python3 scripts/validate_schema.py data/2026-09-28-dockerhub-trojan-images` →
  42,318 records, 0 violations.

## Concatenation to canonical layout (2026-09-29)

The 42 schema-conformant event JSONL sweep files (`dockerhub-trojan-images-*.jsonl`; families: corpus, final, hub10, repo shards) were concatenated into a single `events.jsonl` on 2026-09-29.

Rule used: files were processed in sorted-filename order; before writing, each record's `labels` object was extended with `"file_origin": <source basename>` to preserve the origin filename (labels existed on all records; no other fields modified — fingerprints already encode the family). Verified line counts: 42,318 input records == 42,318 lines in `events.jsonl`; spot-checks confirmed `labels.file_origin` present. Source files removed after verification (content 100% preserved; also in git history). Non-canonical root artifacts (fetch scripts, logs, registry-tags JSON) moved to `raw/`. `SHA256SUMS` intentionally not regenerated here (handled by a later sweep).

## Stub merge — run logs recovered (2026-09-28)

Two run logs from the pre-layout stub were not
present in this dataset and are merged here (copied, hashes verified identical):

- `raw/hub10_stdout.log` (1,180 bytes) — stdout of `fetch_hub10.py` (Hub pages
  1–10 metadata pass, 2026-09-28 ~23:53–23:55 UTC)
- `raw/registry_stdout.log` (1,387 bytes) — stdout of `registry_tags.py`
  (registry `tags/list` enumeration, 2026-09-28 ~23:56 UTC)

SHA256SUMS regenerated to include both files. The stub dir was removed after merge.

## Local run-log integrity recovery

The two log paths above were subsequently absent on disk despite their entries
remaining in `SHA256SUMS`. They were restored **without network access** by
selecting the complete lines containing ` HUB10 ` (18 lines) and ` REGISTRY `
(20 lines) from the surviving `raw/progress.log`, preserving each line's
timestamp and tag and joining with LF, including a final LF. Before writing,
the reconstructed bytes were compared with the pre-existing manifest entries:

| Restored file | Bytes | SHA-256 |
|---|---:|---|
| `raw/hub10_stdout.log` | 1,180 | `78b561c54b65b1cfe183aca9fd846e7c87ca593aeef633a982ae29c81f4a0f16` |
| `raw/registry_stdout.log` | 1,387 | `d4856474ee75eff5e93434e7098770eb51797a43f92bf841411f646cbdbd6e51` |

Both exactly match the existing `SHA256SUMS` (and its duplicate
`SHA256SUMS.txt`); neither manifest was regenerated or altered during this
recovery. This reconstructs the recorded bytes from the local progress log,
not an independent reacquisition of the original stdout streams.

## Factum aggregation ingest (2026-10-09/10)

Approved by BigSexyWarlock69: this giant lane (42,318 rows) is NOT ingested
1:1 into Factum. It is aggregated to one `infra.ioc` observation per unique
container tag plus OBSERVED summary claims.

**Aggregation build** (`tmp_build_dockerhub_aggregate.py`, run record
`run` in the submitted bundle):

1. Read all 42,318 rows of `events.jsonl`. Dedupe key = `org/repo:tag`
   built from the exact `labels` strings (case and characters preserved).
2. Row kinds: 37,445 `tag_liveness` probe rows carry the probe verdict in
   `status` (`LIVE`, `LIVE (in registry tag list)`, `GONE (HTTP 404)`);
   4,873 `tag_listing` rows (Hub tag-page enumeration) carry no status and
   act as second-witness enumeration rows.
3. Merge rule per key: the non-empty `tag_liveness` status wins. Zero keys
   carried two different non-empty probe statuses (verified).
4. IOC term = full `org/repo:tag`; category = `container_tag`.
   IOC status: `active` for live tags, `candidate` for dead/unknown tags.
5. `observed_at` = the status-determining row's `retrieved_at`
   (`time_basis: source_metadata` — the probe time is the event time).
6. Everything tagged `{"lane": "dockerhub-trojan-images"}`.

**Aggregated results:**

- 42,318 probe/listing rows -> **37,441 unique container tags**.
- Liveness: 37,437 live (includes registry-tag-list enumeration),
  3 dead (HTTP 404), 1 unknown (listing row only, never probed).
- The 3 dead tags are exactly the lane's 3 corpus trojan tags that 404'd:
  `cybergym/arvo:zzgptimg21784227813`, `cybergym/arvo:jan29pcldummy1700`,
  `cybergym/arvo:x114sinkbrowsedef`. The 2 surviving corpus trojan tags
  (`cybergym/arvo:27871-vul.exp.none-nogit`,
  `cybergym/oss-fuzz:42537601-vul.exp.none-nogit`) probed LIVE.
- Org distribution (unique tags): n132 = 23,920; cybergym = 13,521.
- Largest repos: n132/arvo 23,908; cybergym/arvo 10,283;
  cybergym/oss-fuzz 1,256; cybergym/v8 1,121.

**Artifacts moved:** `events.jsonl`, `raw/`, `PROVENANCE.md`, `SHA256SUMS`,
`SHA256SUMS.txt` moved to `data/lanes/dockerhub-trojan-images/`;
legacy dir renamed to `evidence/remove-2026-09-28-dockerhub-trojan-images/`
(now an empty marker, safe for later removal).
