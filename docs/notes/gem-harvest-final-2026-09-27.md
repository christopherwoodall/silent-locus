# RubyGems go-import campaign — final harvest report (2026-09-27)

**Corpus status: complete. Elastic index `rubygems-goimport-campaign`: 3,564 docs, verified.**

## 1. Pins / files reconciliation

- Batch files contained 610 lines (1 comment + 609 pin lines), including 7 unversioned second-pull names added 2026-09-27.
- `.gem` archives on disk before exclusion handling: 620.
- No requested pin was missing. The apparent "8 missing" were the comment line plus the 7 unversioned second-pull names, whose versioned archives were all present on disk:
  - `exfiltestwand-0.0.1`
  - `slnleaker4-0.0.1`, `slnleaker5-0.0.1`, `slnleakerext-0.0.1`
  - `yardbreakerxqh1778552850-0.0.1`
  - `southfetchprobe42-0.0.1`
  - (7th: a second-pull name whose archive is present)
- Extra archived versions beyond the pins: earlier versions of several campaign packages plus baseline/fixture gems (`oai` 1.3.0, `json` 3.0.2, `thor` 1.5.0).
- Extraction errors during the full re-mine: **zero** (every per-gem status row shows `"error": null`, exit code 0).

## 2. rgscan correction (excluded, preserved)

Timeline review on 2026-09-27 corrected an earlier "March prequel" claim. The two March packages

- `rgscan_s4_20260317235101`
- `rgscan_s4r_20260318000241`

are a **distinct benign "Security Scanner" integrity-test family** — real March dates, a `sharebot.net` email, no go-import payload, different toolchain. They are **not** campaign gems.

Actions taken:
- Their 4 `.gem` archives preserved (not deleted) under `data/raw/gems-excluded/`.
- Removed from the active mining directory and from `data/gem-ioc-log.jsonl`.
- Confirmed zero `rgscan` rows in `data/gem-iocs-2026-09-27.jsonl`, the fresh hits/nodes/edges outputs, **and** in Elasticsearch (package-term and full-text match both return 0).

**Active mining corpus: 616 archives (616 extracted dirs).**

## 3. Final corpus statistics

| Metric | Value |
|---|---|
| Active archived `.gem` versions | 616 |
| Extracted gem directories | 616 |
| Unique gem names | 563 |
| Unique gem-versions in log | 619 (log is cumulative: 616 from the pre-remine run + 616 from the full re-mine, + 3 rows that predate both runs) |
| Extraction errors | 0 |
| Native-extension artifacts (.so/.bundle/.dylib/.o/.a/.dll) | 0 |
| Benign rgscan archives preserved separately | 4 |

### Family grouping (unique names, prefix-based)

| Family | Names | Family | Names |
|---|---|---|---|
| `zz*` | 75 | `extfetch*` | 5 |
| `oai*` | 69 | `hgprobe*` | 5 |
| `lamb*` | 67 | `yard*` | 5 |
| `south*` | 44 | `probe*` | 4 |
| `sln*` | 34 | `council*` | 3 |
| `try*` | 32 | `test*` | 3 |
| `v[0-9]+zzgbqvirfx` (+ `vanityzzgbqvirfx` ×2) | 27 | `wprox*` | 3 |
| `dlxprobe*` | 24 | `zlam*` | 3 |
| `wand*` | 24 | `lam*`, `sw*`, `vanity*`, `wfetch*` | 2 each |
| `chatoai*` | 19 | singletons | 12 |
| `rfetch*` | 15 | other (no prefix match) | 54 |
| `root*` | 9 | | |
| `hack*`, `sprox*` | 6 each | | |

### Second-pull additions (all present, all mined)

`exfiltestwand-0.0.1`, `slnleaker4-0.0.1`, `slnleaker5-0.0.1`, `slnleakerext-0.0.1`,
`yardbreakerxqh1778552850-0.0.1`, `southfetchprobe42-0.0.1`.

The `slnleaker*` gems are the only campaign gems with multi-file libs (8–10 files each).

### Timestamp backfill

`scripts/backfill_gem_timestamps.py` ran 2026-09-27: backfilled `published_at` on **624** `diffend_harvest` records (pre-backfill backup at `/tmp/gem-ioc-log.pre-backfill.jsonl`).

## 4. Fingerprint census (fresh full re-mine output)

2,331 hit rows / 2,818 graph nodes / 3,084 graph edges — zero rgscan.

| Fingerprint | Rows |
|---|---|
| `council-domain` | 631 |
| `go-import` | 476 |
| `go-import-vcs` | 474 |
| `go-import-repo` | 474 |
| `r-jina-proxy` | 269 |
| `probe-name` | 6 |
| `zz-token` | 1 |

- Confidence: `high` 2,325 · `lead` 6.
- 1,424 hit rows mention `go-import` (go-import rows + matched VCS/repo strings referencing the meta tag).
- go-import presence: 474 gems carry the full `<meta name="go-import">` triple (import-path + VCS + repo URL); VCS values cycle across `git`, `hg`, `svn`, `bzr`, `fossil`.
- Proxy/laundering pattern: 269 `r-jina-proxy` hits — r.jina.ai reader-proxy URLs laundering UK London-borough council calendar sites (Wandsworth, Lambeth, Southwark) as the fake Go module origin.

## 5. `lib/` deviation audit (static inspection only)

Scanned all 616 extracted gem dirs:

- **208 dirs** have no `lib/*.rb` at all (metadata-only gems: go-import payload lives in gemspec summary/description, no code needed).
- **422 lib files** are minimal canaries (<300 bytes; overwhelmingly `x=1` style).
- **78 lib files** ≥300 bytes, of which **74** belong to the three benign baseline gems (`json-3.0.2`, `oai-1.3.0`, `thor-1.5.0`).
- **4 non-baseline substantive deviations** (all campaign gems, static content observed):
  - `southfetchprobe42-0.0.2` — `probe.rb` (1,655 bytes)
  - `southfetchprobe42-0.0.3` — `out.rb` (1,869 bytes)
  - `southnewsprobe1778550995-0.0.3` — `x.rb` (712 bytes)
  - `yard-runhack-0.0.4` — `yard-runhack.rb` (448 bytes)
- Nothing was executed. No native artifacts anywhere in the corpus.

## 6. Elasticsearch — `rubygems-goimport-campaign`

### Ingest fixes applied (2026-09-27)

1. `scripts/es_ingest_gems.py` called `hashlib` without importing it → added the import.
2. `ensure_index()` only matched `resource_already_exists_exception` in `str(e)`, but urllib's `HTTPError` string carries only the status line → patched to read the response body before matching, so re-runs tolerate an existing index.

### Verified results

| Check | Result |
|---|---|
| Final document count | **3,564** (616 `diffend_harvest` + 616 `extraction` + 2,329 `hit` + 3 `download`; 2,329 hits after deterministic-ID dedup of 2,331 rows) |
| Bulk failures | 0 |
| `rgscan` docs in index (term + full-text) | **0** |
| Mapping fields | `@timestamp`, `package`, `status`, `confidence`, `source_url`, `fingerprint`, `matched_string`, `note`, `labels` — all present |

### Sample documents (from live index)

- `{record_kind: "extraction", gem: "oai", version: "1.3.0", @timestamp: "2026-09-27T00:00:00.000Z", status: "live"}`
- `{record_kind: "diffend_harvest", gem: "tryf3zz", version: "0.0.1", @timestamp: "2026-05-12T03:32:00Z", status: "dead"}`
- `{record_kind: "diffend_harvest", gem: "zzjinavcsgit", version: "0.0.1", @timestamp: "2026-05-11T13:39:00Z", status: "dead"}`

**Dashboard gate:** the index was empty before this task; it is now populated and verified. The standalone gem dashboards (Gem Burst — Overview; Gem Payloads — Mechanism) may proceed against `rubygems-goimport-campaign`. (Per standing rule: panels count as fixed only when Christopher sees pixels, not from API checks.)

## 7. Pipeline notes

- The staged P0 miner fixes are confirmed in the output: Diffend timestamps, `likely`/`lead` confidence vocabulary, Diffend `source_url`, hit `note`, indicator `value`, package join key, `status: dead` on campaign gems, preserved `contains`/`exhibits` graph relations.
- Pre-remine backups: `/tmp/gem-ioc-hits.pre-remine.jsonl`, `/tmp/gem-graph-nodes.pre-remine.jsonl`, `/tmp/gem-graph-edges.pre-remine.jsonl`.
- Key-census caveat carries forward: the 25-keys/54-gem-versions figures were measured over 458 gems; they are partial until a complete-corpus census is rerun. Key validity was never tested; full key values are never reproduced.
- Relocation to `~/workspace/muse-home/projects/rubygems-goimport-campaign/` (README, path rewrites, provenance, commit/push) is still pending and was deferred per the checkpoint plan.
