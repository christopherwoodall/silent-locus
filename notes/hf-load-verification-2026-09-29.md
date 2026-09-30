# HF `datasets` load verification — 2026-09-29

Verified with `datasets` 5.0.1 (installed in a throwaway venv; `pip install datasets`).
Repo validator (`scripts/validate_schema.py`) at time of test: **141,804 records in 84 event files, 0 violations** — no data fixes were needed for any of the loads below.

## SNIPPET FOR DATASET CARD

```python
import glob
from datasets import load_dataset, Features, Value, Sequence
from datasets.features import Json

# Union schema: the 64 top-level collections + aggregates use 33 distinct
# top-level key sets, so schema inference from the first file fails.
# labels/ payloads are Json because nested key sets vary per collection.
features = Features({
    "@timestamp": Value("string"),   # ISO-8601 with zone offset; keep as string
    "event": {"dataset": Value("string"), "created": Value("string")},
    "record_kind": Value("string"),
    "fingerprint": Value("string"),
    "labels": Json(decode=True),
    "observer": {"product": Value("string"), "type": Value("string"), "vendor": Value("string")},
    "description": Value("string"),
    "confidence": Value("string"),
    "tags": Sequence(Value("string")),
    "retrieved_via": Value("string"),
    "retrieved_at": Value("string"),
    "source_url": Value("string"),
    "file": Value("string"),
    "sha256": Value("string"),
    "size_bytes": Value("int64"),
    "status": Value("string"),
    "matched_string": Value("string"),
    "note": Value("string"),
    "payloads": Sequence(Json(decode=True)),
})

# All 84 schema-valid event files. Do NOT use data/*/events.jsonl: it misses the
# two nested events.jsonl under data/aggregates/*/ (17,355 + 1,522 rows) and the
# 18 rollup.jsonl sidecars (271 rows). raw/ dirs are pre-event source material.
files = sorted(f for f in glob.glob("data/**/*.jsonl", recursive=True)
               if "raw" not in f.split("/"))

ds = load_dataset("json", data_files=files, features=features)["train"]  # 141,804 rows

# memory-light alternative (no local arrow cache):
ds = load_dataset("json", data_files=files, features=features, streaming=True)["train"]
```

## Results

| check | result |
|---|---|
| single collection `data/2026-05-11-osv/events.jsonl` | 1,956 rows == `wc -l`; loads with no explicit features |
| payloads collection `data/2026-06-17-reverse-tunnels/events.jsonl` | 107 rows == `wc -l`; `payloads` present as list-of-dicts |
| full corpus, materialized | **141,804 rows** (6.6 s) == repo known count |
| full corpus, streaming | **141,804 rows** (20.3 s) |
| nested access | `ds[0]["labels"]` → dict (9 keys); `ds[0]["event"]` → `{'dataset': ..., 'created': ...}`; first `payloads[0]` → `{'kind': 'paste_body', 'content_type': 'text/plain', ...}` with keys `kind, content_type, content, encoding, truncated, byte_size, sha256`; `observer` → `{'product': 'muse', 'type': 'research-agent', 'vendor': 'meta'}` |

## Why the naive load fails (documented, not fixed in data)

1. `load_dataset("json", data_files="data/*/events.jsonl")` raises `DatasetGenerationError` (pyarrow `CastError: ... column names don't match`): schema is inferred from the first file and later collections carry different top-level columns. Fix: explicit union `features` above.
2. With `features` given, a second failure appears: `@timestamp` as `timestamp[s]` cannot parse zone-offset ISO strings (`...Z` / `+00:00`) through the cast path. Fix: keep `@timestamp` (and `retrieved_at`) as `Value("string")` — lossless, matches the repo validator's own string check.
3. The glob `data/*/events.jsonl` silently drops 19,148 rows (2 nested `aggregates/` events files + 18 `rollup.jsonl` sidecars). The recursive glob with the `raw/` exclusion reproduces the validator's 84-file / 141,804-record set exactly.

## Environment notes

- `/tmp` on this VM is a 512 MB tmpfs: the materialized arrow cache for 141,804 rows exceeds it, so set `HF_DATASETS_CACHE` to a directory on the main disk (the streaming load needs no cache at all).
- Collections carrying `payloads`: `2026-05-17-iowacollab-pastes`, `2026-06-17-reverse-tunnels`, `2026-09-28-worldpoverty-task-family` (grep `'"payloads"' data/*/events.jsonl`).
