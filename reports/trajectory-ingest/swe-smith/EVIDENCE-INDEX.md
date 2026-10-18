# SWE-smith trajectories — Evidence Index

Every verified finding maps to a byte location in the local raw store. The parquet shards are canonical. The JSONL files are local expansions (built by `raw/convert.py`).

## Source files

| File | Size | SHA-256 |
|---|---|---|
| `data/lanes/swe-smith-trajectories/raw/tool-00003-of-00008.parquet` | 138,356,054 | `677831f640fb14e5b7bc02fd2aa729c05cd2068750777eaf877084de03157594` |
| `data/lanes/swe-smith-trajectories/raw/xml-00003-of-00008.parquet` | 143,562,585 | see MANIFEST |
| `data/lanes/swe-smith-trajectories/raw/ticks-00003-of-00008.parquet` | 143,312,101 | `f77f88efc19c01f5507c7e0d4569c89f705b0d589d7a6650b871e5cac93b0b9f` |

Authoritative hashes live in `data/lanes/swe-smith-trajectories/raw/MANIFEST.json` (per-file `sha256` fields). The `.sha256` sidecars sit next to each parquet file.

## Provenance

- Dataset: https://huggingface.co/datasets/SWE-bench/SWE-smith-trajectories
- Revision: `08e109b4a59eaeebf80e4675cd125d42e7ac99a4`
- Retrieved: 2026-10-17T04:10:55Z, method `curl` (single-threaded; range-chunked 16 MB for xml/ticks)
- License: `mit` — recorded in `raw/LICENSE.note` (three-source check: README front matter, HF API cardData.license, HF tags)
- Retrieval source URLs: `raw/MANIFEST.json` field `source_base_url`

## Finding → bytes map

| Finding | Trajectory id | Scaffold | Steps | Byte location |
|---|---|---|---|---|
| A-001 | bottlepy__bottle.a8dfef30.lm_rewrite__drqgvm47.j2lokqk2 | tool | 112–130 | `raw/tool-00003.jsonl`, row key = trajectory id |
| A-002 | oauthlib__oauthlib.1fd52536.combine_file__otc4vogi.j2lokqk2 | tool | 70–76 | `raw/tool-00003.jsonl` |
| A-003 | adrienverge__yamllint.8513d9b9.pr_537.j2lokqk2 | tool | 144–148 | `raw/tool-00003.jsonl` |
| A-004 | pandas-dev__pandas.95280573.pr_50844.gb64eyg9 | tool | 22–174 | `raw/tool-00003.jsonl` |
| A-005 | python-trio__trio.cfbbe2c1.combine_module__imtwngmi.u00cgsat | tool | 40–44 | `raw/tool-00003.jsonl` |
| A-006 | iterative__dvc.1d6ea681.pr_9014.j2lokqk2 | tool | 86–92 | `raw/tool-00003.jsonl` |
| A-007 | pandas-dev__pandas.95280573.pr_48511.1cul4bk0 | tool | 42–45 | `raw/tool-00003.jsonl` |
| B-001 | oauthlib__oauthlib.1fd52536.lm_rewrite__vtd9nx1w.40o1rcbf | ticks | 78–107 | `raw/ticks-00003.jsonl` |
| B-002 | seperman__deepdiff.ed252022.lm_rewrite__ifm38kzi.40o1rcbf | ticks | 53–55 | `raw/ticks-00003.jsonl` |
| B-003 | benoitc__gunicorn.bacbf8aa.lm_rewrite__r8ht93g3.40o1rcbf | ticks | 89–91 | `raw/ticks-00003.jsonl` |
| B-004 | pydantic__pydantic.acb0f10f.pr_7101.ejvrtcy9 | ticks | 27–28 | `raw/ticks-00003.jsonl` |
| B-005 | facebookresearch__hydra.0f03eb60.pr_2136.40o1rcbf | ticks | 74–78 | `raw/ticks-00003.jsonl` |
| B-006 | conan-io__conan.86f29e13.pr_13346.40o1rcbf | ticks | patch-field | `raw/ticks-00003.jsonl` |

## Review artifacts

- `data/lanes/swe-smith-trajectories/verified-findings.jsonl` — 13 findings, all PRIMARY, verifier notes inline (re-checked 2026-10-17)
- `data/lanes/swe-smith-trajectories/kill-list.json` — 21 reviewer kills, 0 verifier kills, 3 verifier corrections
- `data/lanes/swe-smith-trajectories/raw/SAMPLE-STATS.json` — row counts, resolved split, parse-failure counts (all zero)
- `data/lanes/swe-smith-trajectories/bundle-swe-smith.json` — factum bundle v2 (61 records), idempotency key `swe-smith-ingest-2026-10-17-v1`
- `data/lanes/swe-smith-trajectories/build-report.json` — builder output, bundle SHA-256

## Writeups (drafts, NOT submitted — Transluce filing freeze in force)

- `writeups/01-test-tampering.md` — A-001, A-002, A-003, B-001, B-002, B-003, B-005
- `writeups/02-goalpost-moving.md` — A-005, A-006
- `writeups/03-error-blind-retry.md` — A-004
- `writeups/04-environment-corruption.md` — A-007
- `writeups/05-deference-tic.md` — B-004
- `writeups/06-patch-misalignment.md` — B-006
