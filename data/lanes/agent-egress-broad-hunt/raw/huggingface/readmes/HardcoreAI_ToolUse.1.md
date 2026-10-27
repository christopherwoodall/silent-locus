---
license: apache-2.0
language:
  - en
  - ru
pretty_name: ToolUse.1
task_categories:
  - text-generation
tags:
  - tool-use
  - function-calling
  - agents
  - evaluation
  - benchmark
  - hardcore-ai
size_categories:
  - n<1K
configs:
  - config_name: default
    data_files:
      - split: test
        path: data/tooluse1.jsonl
---

# ToolUse.1

A tool-calling benchmark that scores correct invocation **and** correct abstention.

114 cases · 78 requiring a call · 36 requiring abstention or clarification · English-only · 9 tool schemas · 3 calling protocols (JSON, XML, plain-text) · deterministic grading, no LLM judge.

Most tool-use evaluations reward a model for emitting a well-formed call. ToolUse.1 also asks
whether it should have called at all: roughly a third of the corpus is prompts where the correct
answer is to say something useful and call nothing. A model that calls a tool for every prompt
and a model that never calls one score about the same.

## Composition

| Category | Cases | Category | Cases |
|---|---|---|---|
| calculator | 15 | negative | 30 |
| get_weather | 8 | clarification | 5 |
| translate | 8 | multi_step | 6 |
| convert_currency | 8 | web_search | 8 |
| convert_units | 8 | set_timer | 6 |
| save_note | 6 | get_time | 6 |

114 English cases. Difficulty is labelled per case (`easy` / `medium` / `hard`) and
reported as a breakdown.

| Group | What it tests |
|---|---|
| `calculator`, `get_weather`, `translate`, `convert_currency`, `convert_units`, `set_timer`, `save_note`, `get_time`, `web_search` | Single call, correct tool, semantically correct arguments. Most cases ship all nine tools, so selection is tested against distractors. |
| `negative` | No call is correct. Knowledge questions, absent capabilities, explicit no-tool instructions, and a quoted call the user asked to be repeated. |
| `clarification` | A required argument is missing. Guessing fails; asking the user passes. |
| `multi_step` | History contains prior tool calls and results; the follow-up requires the next call, or a comparison answered without any call. |

## Schema

```json
{
  "id": "weather-en-001",
  "lang": "en",
  "category": "get_weather",
  "difficulty": "easy",
  "tools": ["calculator", "get_weather", "..."],
  "user": "What's the weather in Berlin?",
  "expect": {"kind": "call", "name": "get_weather", "args": {"city": "Berlin"}}
}
```

`expect.kind` is `call` (with `name` and canonical `args`) or `no_call` (optionally with
`answer_contains_all` / `answer_contains_any`, case-insensitive substring groups). Multi-step
cases add a `history` array of `user` / `assistant` (with `tool_name`, `tool_args`) / `tool`
messages.

## Metrics

| Metric | Definition |
|---|---|
| **Score** | passed cases / all cases, with a Wilson 95% interval |
| Correct call when a tool applies | passing among call cases |
| Correct abstention | passing among no-call cases |
| **Spurious-call rate** | no-call cases where any call was emitted (lower is better) |
| Tool selected correctly | call cases with the right tool name |
| Arguments exactly correct | call cases with every expected argument matching |
| Malformed output rate | call attempts that failed to parse |

Arguments are compared **semantically**, not as strings: `expression` is evaluated as
arithmetic (`45+12` equals `45 + 12`), numbers compare with a `1e-6` tolerance, and cities,
languages, currencies, units and timezones go through alias tables (`СПб` → `saint petersburg`,
`английский` → `en`, `$` → `USD`, `Moscow` → `Europe/Moscow`). Tool names are alias tolerant.
Extra arguments are tolerated and flagged.

## Evaluation harness

The harness is in this repository (`tooluse1/`), alongside the frozen corpus in
`data/tooluse1.jsonl` and the corpus digest in `data/manifest.json`.

```bash
git clone https://huggingface.co/datasets/HardcoreAI/ToolUse.1
cd ToolUse.1
pip install -r requirements.txt

python -m tooluse1 selftest                       # grader sanity check, no model needed
python smoke.py --model HardcoreAI/Nova-1.1-0.8B --limit 8 --batch-size 8
python -m tooluse1 run --model Qwen/Qwen3.5-0.8B --backend transformers --protocol all --batch-size 8 --out results/
python -m tooluse1 run --model my-model --backend openai --base-url http://localhost:8000/v1 --protocol json
```

Backends: local `transformers` checkpoints, any OpenAI-compatible `/chat/completions` endpoint
(vLLM, llama.cpp server, Ollama, OpenRouter), or a scripted file for ablations. Local runs take
`--batch-size` (batch the evaluations into one padded `generate` call; 8–16 saturates a small
GPU) and `--dtype` (`float16` where bfloat16 is unavailable, e.g. a T4 — and report it).

Loading is verified, not assumed: the harness reads back the loading report and refuses an
architecture whose weights do not match the checkpoint, because `from_pretrained` only warns in
that case and hands you a randomly initialised model that still writes plausible text.

Reproduction settings: greedy decoding, `max_new_tokens=256`, the harness system prompt
unmodified, no few-shot examples, reasoning mode disabled where the runtime supports it. Use the
same protocol set when comparing numbers.

## Leaderboard

Results are listed on the [ToolUse.1 leaderboard](https://huggingface.co/spaces/HardcoreAI/ToolUse.1).
To submit, run the harness, keep the JSON it writes, and open a discussion here with the model
id, protocols, case count, decoding configuration and the raw results file.

The leaderboard seeds itself with harness self-checks only (an oracle runner that reads the
expectations, which must score exactly 1.000, and a null runner that never calls a tool). Those
rows validate the grader — they are not model results, and they are labelled as such.

## Contamination

The corpus is fully public. A model trained on these cases will overfit them. Scores should be
read as an upper bound for any model whose authors had access to this repository; models
evaluated before publication are the fair comparison. A held-out private split is planned for
the 2.x line.

## Versioning

Any change to a case bumps the minor version and changes the corpus digest in
`data/manifest.json`, which breaks comparability with earlier scores. Grading changes bump the
major version. Always report the digest with a number.

## Files

```
data/tooluse1.jsonl      114 cases, one JSON object per line
data/manifest.json       counts, sha256 of the frozen corpus, harness version
SPEC.md                  full specification: grading rules, limitations, contamination policy
smoke.py                 checkpoint loading check plus a throughput measurement
tooluse1/                harness (cases, tools, protocols, parser, grader, runners, CLI)
tests/                   tests covering parser robustness, grading semantics, corpus invariants
```

## Limitations

See `SPEC.md` §6. The short version: substring-based answer constraints, wording-sensitive
clarification expectations, synthetic tool results in multi-step cases, no private split yet, and
one documented ambiguity in the plain-text protocol where a call quoted on its own line is
indistinguishable from a real call.

## Citation

```bibtex
@misc{hardcoreai_tooluse1,
  title  = {ToolUse.1: a tool-calling benchmark with abstention},
  author = {Hardcore AI},
  year   = {2026},
  url    = {https://huggingface.co/datasets/HardcoreAI/ToolUse.1}
}
```

## License

Apache-2.0. The corpus may be redistributed and used for training; see the contamination note
above before comparing numbers.
