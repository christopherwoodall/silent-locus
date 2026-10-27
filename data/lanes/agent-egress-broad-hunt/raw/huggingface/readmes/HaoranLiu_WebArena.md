---
license: other
tags:
- cua-lite
- gui
- sft
task_categories:
- image-text-to-text
configs:
- config_name: default
  data_files:
  - split: validation
    path:
    - "*/*/validation*parquet"
    - "*/*/validation/*.parquet"
    - "*/*/validation/*/*.parquet"
- config_name: Qwen3-VL-32B-Instruct
  data_files:
  - split: validation
    path:
    - "*/*/validation/Qwen3-VL-32B-Instruct.parquet"
    - "*/*/validation/Qwen3-VL-32B-Instruct/*.parquet"
- config_name: Qwen3.5-27B
  data_files:
  - split: validation
    path:
    - "*/*/validation/Qwen3.5-27B.parquet"
    - "*/*/validation/Qwen3.5-27B/*.parquet"
- config_name: Qwen3.5-9B
  data_files:
  - split: validation
    path:
    - "*/*/validation/Qwen3.5-9B.parquet"
    - "*/*/validation/Qwen3.5-9B/*.parquet"
- config_name: gpt-5.5
  data_files:
  - split: validation
    path:
    - "*/*/validation/gpt-5.5.parquet"
    - "*/*/validation/gpt-5.5/*.parquet"
---

# cua-lite/WebArena

WebArena web-use agent rollout trajectories staged from ~/cua-lite-all-agents/.exps/eval/browsergym.webarena/2026-07-19T01-32_07f599ab7a/run_0. The HF validation split contains one config per model.

## Origin



## Load via `datasets`

```python
from datasets import load_dataset

# entire dataset
ds = load_dataset("cua-lite/WebArena")

# just one named subset (config)
ds = load_dataset("cua-lite/WebArena", "Qwen3-VL-32B-Instruct")
```

You can also filter by `metadata.platform` / `metadata.task_type` /
`metadata.others.*` after loading; every row carries a rich `metadata`
struct (see schema below).

## Schema

Each row has these columns:

| column | type | notes |
|---|---|---|
| `images` | list[Image] | embedded PNG/JPEG bytes; HF viewer renders thumbnails |
| `messages` | list[struct] | OpenAI-style turns with `role` + structured `content` |
| `metadata` | struct | `{platform, task_type, extra_tool_schemas, valid_actions, others{...}}` |

Coordinate values in `messages` are normalized to `[0, 1000]` integers.

**Image-dedup (`grounding.*` / `understanding` cohorts).** These cohorts are
single-image-per-row and many rows share the same screenshot, so to avoid
re-embedding identical image bytes once per instruction they are stored
*folded*: one row per unique screenshot (image embedded once), carrying an
extra **`_folded`** column — a JSON string with the authoritative list of
`{messages, metadata}` members for that screenshot. The row's top-level
`messages` is the members concatenated for viewer convenience. `use`
cohorts are not folded. **Use `lite.data.hf.download` to consume this repo** —
it unfolds automatically back to one row per instruction; reading the parquet
directly yields the folded form.

## Layout

```
<platform>/<task_type>/<split>/shard-NNNNN-of-NNNNN.parquet                  # single-variant cohort
<platform>/<task_type>/<split>/<variant>/shard-NNNNN-of-NNNNN.parquet        # multi-variant cohort
```

- `platform` ∈ {desktop, mobile, web}
- `task_type` ∈ {understanding, grounding.action, grounding.point, grounding.bbox, use} — used verbatim as the dir component
- HF config names are `<platform>.<task_type>` by default (e.g. `mobile.grounding.action`) — UNLESS the dataset was staged with `--config-names`, which sets verbatim, explicitly-chosen config names (see the `configs:` block above for the authoritative list). The agent registry lookup key in code is `<agent>@<platform>@<task_type>` (e.g. `qwen3_vl@mobile@grounding.action`); only this user-facing token uses `.` between platform and task_type, because `@` triggers a 403 on the dataset-viewer's signed image URLs.
- HF split names stay `train` / `validation` (the `datasets` library blacklists `<>:/\|?*` in split names; everything else is fine in config_name)
- `validation` is an in-distribution held-out slice (never used in training); `test` is reserved for out-of-distribution benchmark datasets

## Stats

| platform | task_type | variant | train | validation |
|---|---|---|---:|---:|
| web | use | Qwen3-VL-32B-Instruct | 0 | 812 |
| web | use | Qwen3.5-27B | 0 | 812 |
| web | use | Qwen3.5-9B | 0 | 812 |
| web | use | gpt-5.5 | 0 | 792 |

## Local mirror & SFT export

For local workflows (SFT export, dedup, mixing across datasets), use
`lite.data.hf.download` to mirror this repo back to the canonical local
layout:

```
$CUA_LITE_DATASETS_ROOT/cua-lite/WebArena/
  images/<hash[:2]>/<hash>.<ext>                          # content-addressed image store
  <platform>/<task_type>/<split>[/<variant>].parquet      # rows reference images by relative path
```

Rows in the local parquet have `images: list[str]`; bytes are extracted to
the image store. `lite.train.export.export_sft` consumes the local
form directly with `--image-root=$CUA_LITE_DATASETS_ROOT`.

- Total unique images: **33,676**
- Image store size: **3.47 GB**

## Notes

Staged via `lite.data.hf.stage` from rollout log-roots: /home/haoranliu/cua-lite-all-agents/.exps/eval/browsergym.webarena/2026-07-19T01-32_07f599ab7a/run_0/Qwen_Qwen3-VL-32B-Instruct, /home/haoranliu/cua-lite-all-agents/.exps/eval/browsergym.webarena/2026-07-19T01-32_07f599ab7a/run_0/Qwen_Qwen3.5-27B, /home/haoranliu/cua-lite-all-agents/.exps/eval/browsergym.webarena/2026-07-19T01-32_07f599ab7a/run_0/Qwen_Qwen3.5-9B, /home/haoranliu/cua-lite-all-agents/.exps/eval/browsergym.webarena/2026-07-19T01-32_07f599ab7a/run_0/gpt-5.5 (row filter: none).

## License & citation

other


