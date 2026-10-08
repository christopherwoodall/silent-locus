# schemas/wordlists.md

IOC search-term wordlists under `lists/words/`.

## `wordlist.txt` — active terms

- One term per line, exact string.
- Lines starting with `#` are comments / section headers.
- Exact-match dedupe, case-sensitive. Noisy/FP terms do NOT belong here.
- Real headers seen: category blocks like `# LAUNCHER_TOOLKIT`, with a
  build comment at the top (date, source lanes, version note).

## `wordlist.json` — metadata superset

JSON array. One object per term:
- `term` — the IOC string (exact, matches txt).
- `category` — taxonomy bucket (e.g. `launcher_toolkit`,
  `sqli_payloads`).
- `provenance` — where the term came from (file + question/context).
- `added_utc` — UTC ISO-8601 timestamp of addition.
- `status` — `active` | `noisy` | `retired`. Noisy terms live here
  ONLY (`status != active`), never in the txt.
- `note` — free text, may be empty.

## `by-family/` — per-model-family splits

- One `*.txt` per model family (e.g. `gpt-openai.txt`,
  `claude-anthropic.txt`, `deepseek.txt`, `qwen.txt`, `glm-zai.txt`,
  `kimi.txt`, `grok-xai.txt`, `gemini-google.txt`, `llama-meta.txt`,
  `other-unknown.txt`).
- Format: one term per line, same as `wordlist.txt`.
- `FAMILY-SPLIT.md` documents the split: source data, coverage table,
  and per-family counts.

## `staging/` — n-gram candidates

- JSON files (`ngrams-*.json`) of candidate n-grams awaiting triage.
- Terms graduate to `wordlist.txt` only after human/agent review; noisy
  ones go to `wordlist.json` with `status: noisy`.
