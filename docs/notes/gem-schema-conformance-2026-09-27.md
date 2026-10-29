# Gem schema conformance audit — 2026-09-27

**Order from Christopher:** "Make sure all of our data matches the schema we created."
**Canonical spec:** `notes/gems-es-mapping.json` (rewritten 2026-09-27 per `notes/gem-schema-review-2026-09-27.md`).
**Live index:** `rubygems-goimport-campaign` (6,619 docs, Elastic Cloud).
**Method:** live `_mapping` pull + per-`record_kind` doc sampling + raw-JSONL field census + aggregation-based population checks. Read-only.

## Verdict

**Data matches the schema with one drift class: 3 fields exist in the live index but are absent from the spec JSON.** They were auto-mapped by Elasticsearch dynamic mapping at ingest time, so no data was lost or silently dropped — but the spec no longer fully describes the index, and their dynamic types are weaker than intended. No type conflicts on any of the 53 shared fields.

| Layer | Result |
|---|---|
| diffend_harvest docs vs spec | ✅ all 17 raw fields covered by live mapping; dates parse; 616/618 wave-tagged |
| jfrog_inventory docs vs spec | ✅ all emitted fields covered; 562/562 overlap docs have inherited wave + @timestamp |
| hit / extraction / download / wayback_metadata vs spec | ✅ all covered |
| Live mapping vs spec JSON | ⚠️ DRIFT — 3 fields in live, not in spec (see table) |
| Keyword/date type integrity | ✅ no type conflicts on 53 shared fields |
| collusion-wiki ingest | ⏳ PENDING — index does not exist yet (other lane still building) |

## Drift: fields in live index but missing from spec JSON

Dynamic mapping is enabled on the index (default), so these three were auto-created as `text` + `.keyword` subfield. Nothing was rejected or dropped.

| Field | Spec says | Live mapping | Example value | Dataset / flavor |
|---|---|---|---|---|
| `expected_sha256` | absent | `text` + `keyword` subfield | `2ff9eed5f7a811d6e7c9d78a9ab656465944386eddc0cb4205390339453c6cc8` | `download` (raw `gem-ioc-log.jsonl`) |
| `published_at_source` | absent | `text` + `keyword` subfield | `diffend:diff_ts` (614 docs) / `fallback:missing_first_seen` (2 docs) | `diffend_harvest` |
| `wayback_url` | absent | `text` + `keyword` subfield | `https://web.archive.org/web/20260906063656/https://rubygems.org/gems/n----00prx53386` | `wayback_metadata` |

**Why this matters:** `published_at_source` is queried in term aggregations — it only works today via the `.keyword` subfield (`published_at_source.keyword`). Aggregating on the bare text field throws a fielddata error (hit during this audit). All three should be `keyword` in the spec, matching siblings like `source_url` and `diff_url`.

**Recommended spec patch** (append to `mappings.properties` in `gems-es-mapping.json`):

```json
"expected_sha256": { "type": "keyword" },
"published_at_source": { "type": "keyword" },
"wayback_url": { "type": "keyword" }
```

Note: changing live types from `text`+keyword to bare `keyword` requires a reindex; the pragmatic fix is to add the fields to the spec as `keyword` for future indices and use `.keyword` in queries against this index (already the pattern used here).

## Per-flavor population check (live index)

Spec's `field_semantics` claims "One index, six flavors" — confirmed, all six present.

| record_kind | docs | has `@timestamp` | has `wave` | missing `published_at` | notes |
|---|---|---|---|---|---|
| `jfrog_inventory` | 3,025 | 3,025 | 562 | 3,025 (by design — JFrog docs use `@timestamp` only) | overlap wave inheritance verified below |
| `hit` | 2,339 | 2,339 | 2,338 | 2,339 (by design) | 1 wave-less doc is the pilot test row (`oaitest1778473828`) |
| `diffend_harvest` | 618 | 618 | 616 | 0 | 2 docs have `published_at_source=fallback:missing_first_seen`, no wave — correct per ingest logic |
| `extraction` | 618 | 618 | 0 | 618 (by design — derived records, no own date) | inherits status/source from harvest; wave intentionally absent |
| `wayback_metadata` | 16 | 16 | 16 (all `june-18`) | 0 | all `recovery_status=metadata-recovered` in sample |
| `download` | 3 | 3 | 0 | 0 | |

**JFrog wave/date inheritance (claimed: 562 overlap docs):** ✅ verified — exactly 562 docs with `in_diffend_corpus=true`, all 562 carry `wave=may-12` and a non-null `@timestamp`. Zero missing. The 2,463 `corpus:jfrog_only` docs carry the documented fallback timestamp and no wave, with `labels.gem.timestamp_source=fallback:jfrog_csv_no_per_row_date`. Matches `scripts/es_ingest_jfrog.py` intent exactly.

**Date integrity:** `published_at` terms agg over all 618 `diffend_harvest` docs returns only May 11–12 2026 campaign-window values (e.g. `2026-05-12T02:47:00.000Z`). All `@timestamp`, `event.created`, `retrieved_at` values parse as dates — no bulk rejections observed, no unparseable values in samples.

**Nested integrity:** `diffend_versions` — 766 nested entries across the corpus, all 766 carry `version`. Zero version-less entries.

**Keyword integrity:** `gem`, `package`, `tags`, `version`, `wave`, `status`, `record_kind`, `versions`, `xray_id`, `in_diffend_corpus` all keyword in live mapping, matching spec. `authors`/`meta_summary`/`meta_description`/`note` are text-with-keyword as specified. No analyzed-text leaks on fields meant to be keywords.

**Raw-to-live field census:** every field present in `data/gem-ioc-log.jsonl` (all 3 kinds), `data/gem-ioc-hits.jsonl`, and `data/gem-june18-wayback.jsonl` exists in the live mapping. **Zero fields silently dropped at ingest.**

## collusion-wiki ingest — PENDING

`GET /collusion-wiki/_mapping` returns index-not-found. The wiki ingest lane has not landed docs yet. Re-run this audit's §2/§3 checks against it once it exists: field coverage vs its own schema doc (`notes/collusion-wiki-schema-2026-09-27.md`), plus the bridge table `data/wiki_gem_bridge.json` (79 gems) against `gem`/`package` keyword fields here.

## Recommendations

1. **Add the 3 drift fields to `gems-es-mapping.json`** as `keyword` (patch above). The spec's own note claims it was "rewritten from ACTUAL record shapes" — these three prove it wasn't complete.
2. **Consider `dynamic: false` (or `strict`) on the index** after the spec is updated, so future ingest flavors fail loudly instead of auto-mapping. Right now a new flavor with a typo'd field name would silently create a parallel field.
3. **Query convention:** use `published_at_source.keyword` (not the bare field) in aggregations until a reindex normalizes the type.
4. Nothing in the data contradicts the spec's provenance note (independent Diffend-sourced collection, not SwarmTraces) or the six-flavor claim.

## Sources

- Spec: `notes/gems-es-mapping.json`; review: `notes/gem-schema-review-2026-09-27.md`
- Live mapping: `GET /rubygems-goimport-campaign/_mapping` (56 properties vs 53 in spec)
- Ingest scripts: `scripts/es_ingest_gems.py`, `scripts/es_ingest_jfrog.py` (read, not modified)
- Raw sources: `data/gem-ioc-log.jsonl`, `data/gem-ioc-hits.jsonl`, `data/gem-june18-wayback.jsonl`, `data/gemstuffer-jfrog-2026-09-27.csv`
