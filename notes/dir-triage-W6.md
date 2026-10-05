# Dir triage — worker W6 (2026-09-29)

Normalization sweep: 4 assigned dirs + 10 undated dirs under `data/`.
Branch `local`; nothing pushed (per instructions).

## (a) Flags for Christopher — do not merge/move/invent

### FLAG 1: `data/2026-09-27-rmn-re-linktable` — PROVENANCE claims a build that isn't there

Contents: **PROVENANCE.md only** (462 bytes). No `raw/`, no `events.jsonl`,
no `SHA256SUMS`.

The PROVENANCE says, verbatim:

> "RMN RE link-table index collection. Docs are built by
> `scripts/es_ingest_rmnre.py` from raw sources in
> `data/2026-09-27-rmn-re/raw/` (link table capture + decoded JSON) and
> `data/aggregates/2025-09-26-cors-bwa-proxy/raw/`."

That part is consistent with reality: `data/2026-09-27-rmn-re/raw/` holds
exactly those files (`link_table_2026-09-27.jsonl`, manifest, decoded JSON).

But it also says:

> "2026-09-29: materialized as a physical collection dir
> (`events.jsonl` via the builder's `--dump` mode) under the canonical
> layout; previously a virtual registry entry with no directory."

That claim is **unsubstantiated**: there is no `events.jsonl` in the dir,
and `scripts/es_ingest_rmnre.py` has **no `--dump` mode** (no argparse at
all; it is a straight ES bulk-ingest script that emits `record_kind:
"shortlink"`).

What actually exists: the materialized dump lives in the aggregates dir —
`data/aggregates/2025-09-26-cors-bwa-proxy/raw/rmn-re-linktable.jsonl`
(1 JSON line, `_index: "rmn-re-linktable"`, `record_kind: "shortlink"`,
`event.dataset: "rmn-re-linktable"`, `event.created:
"2026-09-28T03:07:14.725078+00:00"`). It was **not** copied into the
linktable dir (that would cross the aggregates boundary — forbidden by the
brief). Note also that `"shortlink"` is **not in the schema record_kind
registry** (and is not one of my new kinds below).

Recommendation: either (1) leave the linktable dir as a pointer-stub until
you decide the merge policy, or (2) authorize copying the aggregates dump in
as the dir's `events.jsonl` and registering/fixing the `shortlink` kind.
Do not merge silently — the linktable collection is a derived join of the
rmn-re link table with another aggregate, while `2026-09-27-rmn-re` is the
raw source table; they are different layers.

### FLAG 2: `data/2026-09-28-api-usa-fbi-ucr` — orphaned SHA256SUMS, no data at all

Contents: **SHA256SUMS only** (83 bytes). No `raw/`, no `PROVENANCE.md`.

The SHA256SUMS references a single file that does not exist:

```
f27dcc3cafd5c7ad0d46fba111c28bd4cb243f7c9d3eb12e34206722796f5f17  raw/progress.log
```

No file anywhere in the repo matches that hash (the three `progress.log`
files that do exist — under `data/separate-eval-test/`,
`data/july7-gem-forensics/`, `data/xss-ssti-census/` — plus
`hidden_files/lane12/progress.log`, all hash differently). No FBI/UCR data
exists anywhere in the repo; the only "ucr" hit is an unrelated negative
probe (`goto-ucr-edu_stats-login-walled_2026-09-28.txt` under
`2026-09-28-university-shorteners-batch2`). Nothing buildable — no data
invented.

Recommendation: decide whether this dataset ever existed (lane output that
was never captured?) or delete the orphan SHA256SUMS.

## (b) Undated-dir triage (read-only; nothing moved/deleted/renamed)

No undated dir has `events.jsonl`. File counts are `find -type f` totals.

| dir | files | verdict | evidence |
|---|---|---|---|
| `md-succ-ai` | 2 | **stub** — build tooling, not data | `repo/Makefile`, `repo/scripts/browser-server.mjs`; dated `2026-02-14-md-succ-ai` has 83 files, no events.jsonl — unrelated content |
| `reverse-tunnels` | 1 | **stub** | single `__pycache__/htmx_search.cpython-312.pyc`; dated `2016-05-06-reverse-tunnels` has 24 files, no events.jsonl |
| `july7-gem-forensics` | 1 | **stub** — worker run log | `progress.log` ("forensics fetch start: 18 gems…", 2026-09-29T00:28Z); dated `2026-07-07-july7-gem-forensics` has 54 files / 57 events |
| `university-shorteners` | 0 | **stub** — empty capture scaffold | `wayback/`, `wayback-cc/` hold only empty per-slug dirs (`7t6-o`, `vbudg`, `agentdamacosh777`); dated `2026-05-12-university-shorteners-events` has the full events.jsonl (1522 rows) |
| `dockerhub-trojan-images` | 2 | **orphan logs, not duplicates** | `hub10_stdout.log`, `registry_stdout.log` — hashes unique to this dir, NOT present in dated `2026-09-28-dockerhub-trojan-images` (29 files / 42318 events, uses `raw/` instead); possibly belong to the dated dir's raw layer — merge candidate for your call |
| `forged-flag-hunt` | 1 | **stub** | single `cache/__pycache__/*.pyc` |
| `gem-temporal-pivot` | 1 | **stub** — sweep stdout | `diffend_temporal_sweep.stdout.log` ("total 3025, done 0, todo 3025") |
| `separate-eval-test` | 1 | **stub** — worker run log | `progress.log` (worker-4 resumable log, 2026-09-28T19:27Z start) |
| `transfer-test-family` | 0 | **stub** — empty scaffold | only empty `bodies/`; dated `2026-07-21-transfer-test-family` has 3 files / 28 events |
| `xss-ssti-census` | 1 | **stub** — build log | `progress.log` ("inventory-built payloads.jsonl rows=122", worker1) — documents the build of dated `2026-07-07-xss-ssti-census` (3 files / 122 events) |

Net: 8 stubs (run logs / empty scaffolds / build tooling), 1 orphan-log dir
(`dockerhub-trojan-images`, possible merge candidate), 0 duplicates.

## (c) New record_kinds (registry NOT edited — `schema/README.md` untouched)

- `shortener_link` — one link-table entry from a public YOURLS shortener
  (2026-09-27-rmn-re, 764 rows). Fingerprint identity: `sha256(slug)`.
- `counter_reading` — one read-only counter-channel value read
  (2026-09-28-counter-channel, 3 rows). Identity:
  `sha256("countapi.mileshilliard.com|<key>")`.
- `counter_probe` — the sibling-enumeration probe (1 row). Identity:
  `sha256("countapi.mileshilliard.com|sibling_probe")`.

Observation (not mine to register): the aggregates linktable dump uses
`record_kind: "shortlink"`, which is absent from the registry and from every
`events.jsonl` on disk.

## (d) BLOCKED dirs

- `2026-09-27-rmn-re-linktable` — BLOCKED (see FLAG 1). Nothing to build
  from inside the dir; merge forbidden by the brief.
- `2026-09-28-api-usa-fbi-ucr` — BLOCKED (see FLAG 2). No data; SHA256SUMS
  is an orphan.

## Build log (the two completed dirs)

- `2026-09-27-rmn-re`: 764 raw records -> 764 `events.jsonl` rows.
  `scripts/validate_schema.py`: 0 violations. 3 rows spot-checked by hand;
  fingerprint recompute (`sha256(slug)`) verified on all 3. `chain` (list of
  dicts) excluded from labels per the flat-labels rule, retained in raw.
- `2026-09-28-counter-channel`: 4 docs (3 keys + sibling probe) -> 4 rows.
  0 violations; all 4 fingerprints recomputed by hand.
- Reference-function check: `sha256("TheNacken/python-cors-proxy")`
  reproduced the `2023-11-14-hfspace-proxies` reference fingerprint exactly.
- **Stale-checksum finding:** the *committed* SHA256SUMS in both built dirs
  FAILED `sha256sum -c` against the committed raw files (all entries).
  Regenerated files verify clean, and the rmn-re jsonl hash matches the
  manifest's embedded `sha256` (`3f636443…`), corroborating the raw bytes
  are the genuine upstream capture. The old hashes were simply stale.

Committed on `local`, NOT pushed (per instructions).
