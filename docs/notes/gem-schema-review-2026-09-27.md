# Gem corpus schema review — 2026-09-27

**Question from Christopher:** "Are we matching schema?"
**Scope:** gem graph JSONL + IOC log/hits vs the FROZEN hunt's schema
(`urlquery-api-hunt`, read-only) and vs the proposed ES mapping
(`notes/gems-es-mapping.json`).
**Status at review time:** the bulk Diffend harvest agent is still running;
`data/gem-graph-*.jsonl` currently hold pilot rows (13 nodes / 11 edges) plus
`.pre-bulk` backups. `scripts/mine_gems.py` was read (not modified) to review
what the bulk run *will* emit. **Patches are proposed only — nothing was
changed.**

## Verdict

| Layer | vs hunt | Detail |
|---|---|---|
| Graph **node field contract** | ✅ MATCH | `id,label,type,subtype,description,first_seen,last_seen,source_url,confidence` — identical to hunt `graph/nodes.csv` header, field for field |
| Graph **edge field contract** | ✅ MATCH | `source,target,relation,evidence_url,notes` — identical to hunt `graph/edges.csv` header |
| Node/edge **vocabulary** (types, relations, confidence) | ⚠️ PARTIAL | Same shape, different vocab; 3 concrete renames needed (§E) |
| `first_seen`/`last_seen` population | ❌ BUG | Miner emits `null` for every Diffend-harvested gem (§E.1) — the timestamps exist in the log, they're just not read |
| IOC log + hits files vs proposed ES mapping | ❌ STALE | Mapping doc describes fields that don't exist and omits the most important record kind (§C) |
| ES layer vs hunt ES conventions | ❌ DIVERGED | Hunt ES is full ECS (`threat.indicator.*`, `@timestamp`, `event.*`, `observer.*`, `labels.hunt.*`); gem mapping is custom flat fields with no `@timestamp` (§D) |
| Index name | ✅ GOOD | `rubygems-goimport-campaign` — descriptive, provenance-clean (no "swarmtraces"), index-safe. **Keep it.** |

Bottom line: the graph JSONL was clearly built against the hunt's contract and
it shows — that layer joins cleanly. The breakage is (1) a timestamp bug in the
miner, (2) a confidence-vocab drift (`medium`/`low` aren't hunt words), and
(3) an ES mapping doc that no longer describes the records. All fixable without
re-running the harvest.

---

## A. Graph schema vs hunt — field-by-field

Hunt reference: `artifacts/graph/nodes.csv` (1,275 rows), `artifacts/graph/edges.csv`
(1,870 rows), headers verified with Python csv parsing.

### Nodes

| # | Hunt `nodes.csv` field | Gem `gem-graph-nodes.jsonl` field | Match? |
|---|---|---|---|
| 1 | `id` | `id` | ✅ |
| 2 | `label` | `label` | ✅ |
| 3 | `type` | `type` | ✅ (vocab differs, §A.1) |
| 4 | `subtype` | `subtype` | ✅ (vocab differs, §A.1) |
| 5 | `description` | `description` | ✅ |
| 6 | `first_seen` | `first_seen` | ✅ shape / ❌ population (§E.1) |
| 7 | `last_seen` | `last_seen` | ✅ shape / ❌ population (§E.1) |
| 8 | `source_url` | `source_url` | ✅ |
| 9 | `confidence` | `confidence` | ✅ shape / ⚠️ vocab (§A.2) |

### Edges

| # | Hunt `edges.csv` field | Gem `gem-graph-edges.jsonl` field | Match? |
|---|---|---|---|
| 1 | `source` | `source` | ✅ |
| 2 | `target` | `target` | ✅ |
| 3 | `relation` | `relation` | ✅ (vocab differs, §A.3) |
| 4 | `evidence_url` | `evidence_url` | ✅ |
| 5 | `notes` | `notes` | ✅ |

### A.1 Node type/subtype vocabulary

Hunt node types (12): `indicator` (1024), `enhancement`, `target`, `technique`,
`campaign`, `evidence`, `infrastructure`, `tactic`, `hop`, `agent_label`,
`observation`, `incident`.
Gem node types (3): `gem`, `indicator`, `file`.

- `indicator` exists in both. ✅
- `gem` is new. Notably the hunt already has a **`gem-package` indicator
  subtype** (7 nodes) for RubyGems package names — the concept exists in the
  hunt's taxonomy. Recommendation: keep native `type=gem` on gem nodes, and in
  any ECS translation emit them as `threat.indicator.type=[software]` with
  `labels.gem.node_type=gem` — exactly how the hunt's own `gem-package →
  software` mapping works (`notes/schema/ecs-mapping.md` §3.1).
- `file` is new (gem-internal file nodes, subtype `text:.rb` / `binary:.so`).
  No hunt equivalent. Recommendation: keep, park as entity docs with
  `labels.gem.node_type=file` in ECS translation. Do not force into
  `indicator`.
- Gem indicator subtypes (`go-import`, `go-import-vcs`, `go-import-repo`,
  `r-jina-proxy`, `council-domain`, plus miner fingerprints like `epoch-nonce`,
  `zz-token`) are campaign-specific — same pattern as the hunt's
  campaign-specific subtypes (`yourls-slug`, `tableau-endpoint`). No conflict;
  native values are preserved per the hunt's keep-all rule.

### A.2 Confidence vocabulary

Hunt graph confidence values: `lead` (681), `confirmed` (428), `likely` (158),
`high` (8).
Gem miner emits: `confirmed`, `high`, **`medium`**, **`low`** (see
`FINGERPRINTS`/`METADATA_FINGERPRINTS` in `scripts/mine_gems.py`).

`medium` and `low` are **not hunt words** — concrete mismatch. The hunt's ECS
doc (§3.2) already defines the full scale: `confirmed`/`high` → High,
`likely` → Medium, `lead` → Low. **Patch: rename `medium`→`likely`,
`low`→`lead` in the miner** (§E.2). After that, gem confidence is a strict
subset of hunt vocabulary and the existing STIX-scale mapping covers it.

### A.3 Edge relation vocabulary

Hunt relations (30 verbs, top: `lists` 574, `redirects_to` 567, `used_in` 264,
`attributed_to` 102, `laundered_via` 85, `targets` 68 …).
Gem relations (2): `exhibits` (gem→indicator, file→indicator), `contains`
(gem→file).

Neither verb is in the hunt's 30. Closest hunt analogues: `exhibits` ≈
`demonstrates` (12 uses); `contains` ≈ inverse of `part_of` (23 uses).
Recommendation: **keep both verbs** and add them to the shared relation-vocab
doc — the hunt's own vocab grew organically to 30 verbs, there is no closed
enum to conform to, and renaming would break the miner's already-emitted
output. Document the crosswalk (`exhibits`≈`demonstrates`,
`contains`≈`part_of`⁻¹) for dashboard faceting.

### A.4 Node ID scheme

Hunt: `ioc-<slug>`, `camp-<slug>`, … Gem: `gem-<name>-<version>`,
`ioc-<fingerprint>-<sha8>`, `file-<sha8>`. Same prefixed-slug convention,
no collision risk (`gem-`/`file-` prefixes are new). One join consideration:
hunt `gem-package` nodes are **name-only** while gem-corpus gem nodes are
**name+version**. Patch: add a `package` field (bare gem name) on gem nodes and
hit records already carry `gem`+`version` separately — the join key then exists
on both sides (§E.6).

### A.5 Labels

Hunt `label` = raw IOC value. Gem indicator nodes use `label = val[:120]` —
**silent truncation**, full value retained only in `gem-ioc-hits.jsonl`
(`matched_string`). Patch: add a `value` field with the full string on
indicator nodes and mark truncation (§E.5). Display-vs-data: dashboards should
facet on the full value, not the 120-char label.

---

## B. IOC log / hits vs hunt `iocs.csv`

Hunt `iocs.csv` (359 rows): `ioc,type,first_seen,last_seen,report_count,source_link,context,status`.

| Hunt field | Gem equivalent | Location | Notes |
|---|---|---|---|
| `ioc` | `matched_string` | `gem-ioc-hits.jsonl` | Full IOC value; node `label` is the truncated form |
| `type` | `fingerprint` | `gem-ioc-hits.jsonl` | e.g. `go-import`, `council-domain`, `zz-token` |
| `first_seen` / `last_seen` | `published_at` (download recs) / parsed `diff_ts` | `gem-ioc-log.jsonl` | `diffend_harvest` records have **no** `published_at` — parse from `diffend_versions[].diff_ts` (§E.1) |
| `report_count` | exhibiting-gem count (derivable) | — | Analog: number of version pins exhibiting the IOC (608 pins / 555 gems); or `ioc_distinct_values` per gem on extraction records |
| `source_link` | `diff_url` | `gem-ioc-log.jsonl` (`diffend_harvest`) | Canonical provenance URL; see §C on URL field-name drift |
| `context` | `note` | `gem-ioc-hits.jsonl` | Present on metadata hits; **missing on file-content hits** (§E.4) |
| `status` | *(absent)* | — | **Add it:** every burst gem was yanked from rubygems.org → `status=dead`, matching the hunt's `dead` semantics (`ecs-mapping.md` §3.3). Recommend emitting `status: "dead"` on gem nodes / `labels.gem.status` in ES |

Record-shape note: the hunt keeps IOCs in one CSV; the gem pipeline splits
across `gem-ioc-log.jsonl` (3 record kinds) + `gem-ioc-hits.jsonl`. That's fine
as long as the ES ingest treats hits as a 4th document flavor (§F, P0-4).

---

## C. Proposed ES mapping vs actual records — the mapping is stale

`notes/gems-es-mapping.json` (index `rubygems-goimport-campaign`) was drafted
before the Diffend pivot. It no longer describes the records.

### C.1 `record_kind` fiction

Mapping doc says: `record_kind = download | extraction | hit — one index, three
record shapes`.
Actual `gem-ioc-log.jsonl` (377 lines): `diffend_harvest` (359), `extraction`
(15), `download` (3). **No `hit` records exist in the log** — hits live in the
separate `gem-ioc-hits.jsonl`. And `diffend_harvest` — the record kind carrying
the entire campaign payload — is absent from the mapping entirely.

### C.2 Field-name mismatches (mapping → actual)

| Mapping field | Actual field | Status |
|---|---|---|
| `ioc_fingerprint` | `fingerprint` | ❌ rename (mapping is wrong) |
| `ioc_value` | `matched_string` | ❌ rename (mapping is wrong) |
| `ioc_value_text` | *(nothing)* | ❌ fictional — drop, or make it a multi-field on `matched_string` |
| `evidence` (text) | `note` (text) | ❌ rename — no record emits `evidence` |
| `retrieved_at` (date) | *(absent on `diffend_harvest`)* | ⚠️ only `download` records have it; 359/377 records lack it |
| `published_at` (date) | *(absent on `diffend_harvest`)* | ⚠️ only `download` records have it; backfill from `diff_ts` (§E.1) |
| `authors` | `authors` (download) / `meta_authors` (harvest) | ⚠️ two names for one concept |

### C.3 Fields the mapping omits (all present in real records)

`diffend_harvest`: `meta_summary`, `meta_description`, `meta_authors`,
`meta_homepage`, `meta_licenses`, `diff_url`, `diffend_versions[]`
(`{version, diff_ts}`), `retrieved_via`, `note`, `error?`
`extraction`: `extracted_at`, `extracted_to`, `file_count`, `files[]`
(`{path, sha256, …}`), `ioc_distinct_values`, `native_artifacts?`, `error?`
`download`: `expected_sha256`
Hits file: `scan_truncated`

The omitted `meta_summary` / `meta_description` are **where the go-import
payloads live**. A strict template built from this mapping would drop or
dynamically map the campaign's core evidence. The mapping must be rewritten
from the actual record shapes (§F, P0-1).

### C.4 Missing ES fundamentals

- **No `@timestamp`.** The hunt's ES docs require it (ECS base field); Kibana
  time-series panels need it. Gem docs currently have no single canonical
  event time.
- **No provenance block.** Hunt docs carry `observer.{product,vendor,type}`,
  `event.{module,provider,created,dataset}`, `tags`, `labels.hunt.*`. Gem
  mapping has none of this.
- **Provenance URL has three names**: `download_url` (download),
  `diff_url` (harvest), `retrieved_via` (harvest, free text). Standardize on
  canonical `source_url` (§F, P0-5).

---

## D. ES layer vs hunt ECS conventions

The hunt's ES design (`notes/schema/ecs-mapping.md`, verified against the
actually-ingested `artifacts/dataset/elastic/*-2026-09-25-v1.ndjson`):

- **Schema:** ECS throughout. Indicators → `threat.indicator.*`
  (`name`, `type[]` from the STIX 2.0 SCO enum, `confidence` on the STIX 2.1
  None/Low/Medium/High scale, `first_seen`/`last_seen`, `description`,
  `reference`, `sightings`, `url.*`/`ip` decomposition, `related.hosts`/`related.ip`
  pivots). Entities → `event.kind=event` docs. Edges → event docs with the
  triple in flat `labels.hunt.edge_source/target/relation` (+ `message`).
- **Flavors:** one index, three document flavors (`urlquery-hunt.ioc`,
  `urlquery-hunt.graph-indicator`/`graph-node`, `urlquery-hunt.graph-edge`).
- **Timestamps:** `@timestamp` required; `event.start`/`event.end` =
  first/last seen; explicit empty-date fallback rule (fixed constant +
  `labels.hunt.timestamp_source` / `labels.hunt.date_precision` flags).
- **Dotted label namespaces:** `labels.hunt.*` (never nested objects).

The gem proposal is custom flat fields with no ECS, no `@timestamp`, no
flavors, no provenance block. **Decision needed** (§F): either

1. **(Recommended for cross-dataset dashboards)** translate gem docs into the
   hunt's ECS flavors at ingest (translation table in §F, P1-8), keeping native
   gem fields under `labels.gem.*`; or
2. keep a separate custom mapping for `rubygems-goimport-campaign` and accept
   that hunt dashboards can't query it without per-index clauses.

Either way the mapping must first be rewritten to match actual records (§C).

---

## E. Miner emit bugs found (read-only review — not fixed)

### E.1 🔴 `first_seen`/`last_seen` are null for every Diffend gem

`scripts/mine_gems.py` sets `pub = dl.get("published_at")` where `dl` is the
`download`-kind log record. Diffend-harvested gems have **no** download record
(`dl = {}`), so `pub = None` → every node the bulk run emits gets
`"first_seen": null, "last_seen": null` — exactly the pilot's state (13/13
null), and worse than the hunt (104/1275 null, with an explicit fallback rule).

The timestamps exist: `diffend_harvest.diffend_versions[]` carries
`diff_ts` like `"May 12, 2026 07:56"` (UTC per the rescan).

**Patch (in `mine_gems.py`, ~line 306):**
```python
pub = dl.get("published_at") or _diff_ts(dh)  # parse "%b %d, %Y %H:%M" → UTC ISO
```
where `_diff_ts` picks the `diff_ts` matching the pin's version, else the max.
If still absent: fall back to the documented constant
`2026-09-27T00:00:00.000Z` (harvest date — never "now") and flag it the way
the hunt does (`timestamp_source: "fallback:missing_first_seen"`,
`date_precision: "none"`). Also backfill `published_at` onto
`diffend_harvest` log records from the same parse — the ES mapping expects it.

### E.2 🟡 Confidence `medium`/`low` aren't hunt vocabulary

`FINGERPRINTS` uses `"medium"` (paste-url, httpbun-url, series-64H) and
`"low"` (probe-name). Hunt vocab is `lead/likely/confirmed/high`.
**Patch:** `"medium"`→`"likely"`, `"low"`→`"lead"` in both fingerprint tables.
ECS mapping then follows the hunt's existing §3.2 table with no new work.

### E.3 🟡 File-node `source_url` points at 404 rubygems.org URLs

File nodes use `gem_page = "https://rubygems.org/gems/<name>/versions/<ver>"`,
but burst gems are yanked — those URLs 404. The Diffend page
(`evidence_url`/`diff_url`) is the working provenance link.
**Patch:** use `evidence_url` for file nodes' `source_url` (keep `gem_page`
only when there's no Diffend record).

### E.4 🟡 Hit record shape is inconsistent

Metadata hits include `note`; file-content hits don't (no `note` key at all).
**Patch:** always emit `note` (empty string when none) so the hits file has
one shape.

### E.5 🟢 Indicator node labels are silently truncated

`label = val[:120]` with no marker; full value only in the hits file.
**Patch:** add `"value": <full string>` on indicator nodes (and a
`"label_truncated": true` flag when cut). Dashboards facet on `value`.

### E.6 🟢 No bare package-name join key

Gem node ids are `gem-<name>-<version>`; the hunt's `gem-package` nodes are
name-only. **Patch:** add `"package": <name>` on gem nodes (hit records
already split `gem`/`version`). Enables cross-corpus joins without parsing ids.

---

## F. Normalization patch plan (ordered, none applied)

### P0 — before the `rubygems-goimport-campaign` ingest

1. **Rewrite `notes/gems-es-mapping.json` from actual record shapes.**
   Proposed property list (keyword unless noted):
   `@timestamp` date; `record_kind` keyword
   (`download|extraction|diffend_harvest|hit`); `event.dataset`,
   `event.created` date, `observer.product|vendor|type`; `gem` keyword
   (+`gem.text`); `version` keyword; `published_at`, `retrieved_at`,
   `extracted_at` date; `authors`/`meta_authors` text+keyword;
   `meta_summary`/`meta_description` text (+keyword raw, `ignore_above:256`);
   `meta_homepage`, `meta_licenses` keyword; `source_url`, `download_url`,
   `diff_url`, `retrieved_via` keyword; `diffend_versions` nested
   `{version keyword, diff_ts date, diff_ts_raw keyword}`;
   `sha256`, `expected_sha256` keyword; `sha_mismatch` boolean;
   `size_bytes` long; `file` keyword; `files` nested `{path keyword,
   sha256 keyword}`; `file_count` integer; `ioc_distinct_values` integer;
   `extracted_to` keyword; `fingerprint` keyword; `matched_string` keyword
   (+`matched_string.text`); `line_no` integer; `confidence` keyword;
   `scan_truncated` boolean; `note` text; `error` keyword; `status` keyword;
   `labels.gem.*` flattened for native extras.
2. **Apply miner patches E.1–E.6**, then re-run the graph/hits emit (no
   re-harvest needed — the tarballs and log already exist).
3. **Ingest hits as a 4th record flavor** (`record_kind=hit`) into the same
   index — mirrors the hunt's one-index-flavors pattern; keeps IOC values
   queryable alongside their provenance records.
4. **Standardize on `note`** (drop fictional `evidence`); on `fingerprint` /
   `matched_string` (drop fictional `ioc_fingerprint` / `ioc_value` /
   `ioc_value_text` — mapping follows the actual files, not vice versa).
5. **Canonical provenance URL = `source_url`** on every record kind
   (keep `download_url`/`diff_url` as ingested aliases, don't delete).
6. **Emit `status: "dead"`** for all burst gems (yanked from rubygems.org) —
   matches hunt `status` semantics (`live|dead|unknown|…`); surfaces in ES as
   `labels.gem.status` + `tags: ["status:dead"]` per the hunt's §3.3 pattern.
7. **`@timestamp` rule** (mirror hunt `ecs-mapping.md` §2 with gem constants):
   `@timestamp` = `first_seen` (parsed `diff_ts`, UTC); empty →
   `2026-09-27T00:00:00.000Z` flagged
   `labels.gem.timestamp_source="fallback:missing_first_seen"`,
   `labels.gem.date_precision="none"` (`day` when parsed).

### P1 — cross-dataset join readiness (after ingest)

8. **ECS translation spec** for dashboards that query hunt + gem indices
   together (`event.dataset = rubygems-goimport-campaign.{ioc,graph-node,graph-edge}`,
   `observer.product="diffend-gem-harvest"`, native fields under `labels.gem.*`):

   | Gem artifact | ECS translation |
   |---|---|
   | indicator: `go-import`, `go-import-repo`, `r-jina-proxy` | Flavor A, `threat.indicator.type=[url]`, `url.original`=value; `related.hosts` += domain |
   | indicator: `council-domain` | Flavor A, `type=[domain-name]`, `related.hosts` += value |
   | indicator: `go-import-vcs`, `epoch-nonce`, `zz-token`, `tableau-marker`, `controller-stem`, `series-64H`, `probe-name` | Flavor A, `type=[artifact]` |
   | indicator: `ntfy-topic`, `webhook-inbox`, `filebin-url`, `paste-url`, `shortener-url`, `httpbun-url` | Flavor A, `type=[url]` (matches hunt §3.1 precedent) |
   | gem node | Flavor A, `type=[software]` (hunt's own `gem-package`→`software` precedent), `threat.indicator.name`=package name |
   | file node | Flavor B entity, `labels.gem.node_type=file` |
   | edge | Flavor C: flat `labels.gem.edge_source/target/relation` + `message` |
   | confidence | hunt §3.2 table (confirmed/high→High, likely→Medium, lead→Low) |
   | status | `labels.gem.status`, `tags+=["status:dead"]` |
9. **Relation crosswalk doc**: `exhibits`≈hunt `demonstrates`,
   `contains`≈inverse of hunt `part_of`; add both verbs to the shared vocab.
10. **Backfill window**: when E.1 is fixed, regenerate nodes/edges/hits from
    the already-harvested tarballs — no re-download needed.

---

## G. Name assessment: `rubygems-goimport-campaign`

**Good — keep it.** It names the source (RubyGems), the technique
(go-import meta-tag injection), and the shape (a campaign, not a feed).
Provenance-clean (no "swarmtraces"), index-safe (lowercase, hyphens,
no dates needed — the campaign is a fixed May-2026 event). Recommended
`event.dataset` values: `rubygems-goimport-campaign.ioc`,
`.graph-node`, `.graph-edge`. Do not rename toward anything containing
"swarmtraces" — Christopher corrected that provenance explicitly on 2026-09-27.

---

*Review artifacts read (all read-only): `data/gem-graph-nodes.jsonl`,
`data/gem-graph-edges.jsonl`, `data/gem-ioc-log.jsonl`,
`data/gem-ioc-hits.jsonl`, `notes/gem-pipeline-test.md`,
`notes/gems-es-mapping.json`, `scripts/mine_gems.py` (emit section),
hunt `artifacts/graph/nodes.csv`, `artifacts/graph/edges.csv`,
`artifacts/dataset/iocs.csv`, `artifacts/dataset/elastic/*-2026-09-25-v1.ndjson`,
hunt `notes/schema/ecs-mapping.md`. Frozen hunt not modified.*
