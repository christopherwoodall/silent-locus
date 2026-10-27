---
license: other
license_name: openmdw
license_link: LICENSE
pretty_name: Science Tool-Use Conversations
language:
- en
task_categories:
- text-generation
size_categories:
- 10K<n<100K
tags:
- synthetic
- conversational
- self-play
- glm
- tool-use
- agents
- science
---

# Science Tool-Use Conversations

This dataset contains 11,405 synthetic conversations about science questions. GLM-5.3 generated both the user and assistant messages. The assistant could run commands in [shellsim](https://github.com/rjpower/shellsim), an in-memory shell and Python simulator. Each row includes a system message, the user-visible conversation, a tool-call transcript, and the tool definition. Some conversations contain no tool calls.

The questions come from the `so_openq` split of [nvidia/Nemotron-RL-Science-v1](https://huggingface.co/datasets/nvidia/Nemotron-RL-Science-v1). This release does not include the source questions or reference answers. Each row contains `idx`, its row index in the source split. Use the included `enrich.py` script to join those fields locally. The source dataset has a separate CC-BY-SA-4.0 license.

## Marin SFT token count

Marin's SFT representation contains **20,855,889 tokens** after chat normalization,
rendering, and tokenization with its 2026-09-18 tokenizer snapshot. Marin uses
`full_log`, including tool calls and replies. This count was reproduced locally;
tokenized artifact validation is pending.

## Generation and filtering

1. **Source questions.** The `so_openq` split has 150,644 rows. Generation attempted its first 20,630 rows before the run stopped. The source fields used were `problem`, `expected_answer`, `topic`, and `subtopic`.
2. **User messages.** GLM-5.3 played a person asking about the assigned question over several brief, informal messages. It was prompted to push back gently when an assistant answer clearly contradicted its approximate recollection of the reference answer. The prompt allowed disagreement to remain unresolved.
3. **Assistant messages and tools.** GLM-5.3 played the assistant with access to a persistent shellsim session. The simulator has no network access and supports a limited subset of Python; it does not run commands in a system shell or CPython. The assistant could use it to check calculations or reasoning. The assistant issued commands during generation by writing `bash` code blocks, which the pipeline parsed and executed. The release represents those commands and their outputs as `tool_calls` and `tool` messages in `full_log`; `messages` keeps only the system message and user-visible turns.
4. **Filtering.** Trace inspection identified several generation artifacts: claims about tool use that did not occur, near-duplicate replies to successive user messages, replacement characters from a decoding error, and attempted commands leaking into final replies after the action limit. The pipeline was changed to detect and remove affected conversations. A final GLM-5.3 grading pass reviewed the full traces for coherence, responsiveness, factual errors, role breaks, and unsupported claims about tool verification. Conversations it flagged were removed.

After generation failures and filtering, 11,405 conversations remain. A missing `idx` may refer to a question that was never attempted or to a conversation that was removed; it does not indicate a problem with the source row.

## Fields

| Field | Type | Description |
| --- | --- | --- |
| `idx` | int | Row index in the source `so_openq` split. `enrich.py` uses it to recover `problem` and `expected_answer`. |
| `topic`, `subtopic` | string | Category labels from the source row, such as `Physics` and `Quantum Mechanics`. |
| `messages` | list of `{role, content}` | The assistant system prompt at `messages[0]`, followed by the user-visible conversation. Each assistant message contains its final reply for that turn. |
| `full_log` | list of messages | Complete conversation, including the system message and opening user message. Tool use appears as assistant `tool_calls` followed by matching `tool` messages with command output. |
| `tools` | list of tool definitions | The `execute_bash` function schema, identical across rows. Supply it with `full_log` when using an OpenAI-compatible tool-calling format. |
| `turns` | int | Number of user and assistant messages; excludes the leading system prompt. |
| `tool_actions` | int | Number of shellsim commands executed in the conversation. |
| `shellsim_commit` | string or null | Short shellsim commit hash when tracked. `null` marks conversations generated before commit tracking began. |

## Stored system prompt and tool definition

Every row stores the same system message in `messages[0]` and `full_log[0]`:

````text
You are a helpful assistant chatting with a user, with one extra capability: a persistent Shellsim bash session (a sandboxed, in-memory Unix-like shell with a limited Python) that carries files/cwd/variables between your actions within this conversation. Shellsim is not the real host: no network, no package installs, no native binaries. The python/python3 commands are Shellsim's own limited interpreter, not CPython.

Shellsim's Python/bash support is a genuinely incomplete, from-scratch reimplementation, not real CPython or a real shell — it will sometimes reject completely valid, ordinary syntax (an operator, a builtin, a stdlib function) with an error like "unsupported by minimal shim". This is a quirk of this specific sandbox, not something to expect from real Python or a real shell elsewhere — don't conclude your code was wrong just because Shellsim rejected it; rewrite using a simpler, more basic construct it does support and move on.

When it would help — computing something, checking your own reasoning numerically, working out unit conversions, anything you'd otherwise be doing icky arithmetic for by hand — you may run a shell command before replying to the user. When a task involves computation or verification you'd otherwise redo by hand more than once, consider writing yourself a small script as a reusable tool, then running it; revise it with sed or by rewriting the file if your first attempt is wrong.

Each step, respond with EITHER:
- a single shell command in a ```bash code block (nothing else) to take an action and see the result before you decide what to say next, OR
- your plain-text chat reply to the user (no code block) when you're ready to respond.

Actively look for a reason to write and run a small Python tool as part of your answer —
even for a conceptual question, plugging in representative numbers, a symbolic sanity
check, a quick simulation, or verifying a limiting case can make your explanation more
concrete and catch your own mistakes before you commit to an answer. Default to trying
this rather than skipping it; only skip when there's genuinely nothing a script could add
(e.g. a pure definitional/terminology question). Keep chat replies conversational, matching
the user's casual tone — the tool use should support the explanation, not replace it with
a wall of output.
````

The emulator-limitation paragraph in this stored message was added after generation. The model that generated the conversations did not see that paragraph. The generated user role did not receive a system prompt.

The `tools` field contains this function definition:

```json
[{
  "type": "function",
  "function": {
    "name": "execute_bash",
    "description": "Execute a single shell command in a persistent, sandboxed Shellsim session (an in-memory Unix-like shell with a limited, non-CPython Python interpreter). State (files, cwd, variables) persists between calls within the conversation. No network access, no package installs, no native binaries. This is a genuinely incomplete reimplementation and will sometimes reject valid syntax with an 'unsupported by minimal shim' error -- that reflects this sandbox's limitations, not an error in the command itself.",
    "parameters": {
      "type": "object",
      "properties": {
        "command": {"type": "string", "description": "The shell command to execute."}
      },
      "required": ["command"]
    }
  }
}]
```

## Recovering the source questions

```bash
pip install huggingface_hub datasets pandas pyarrow
hf download open-athena/science-tool-use-conversations train.parquet enrich.py --repo-type dataset --local-dir .
python3 enrich.py --in train.parquet --out enriched.parquet
```

The script downloads the `so_openq` split, looks up each row by `idx`, and adds `problem` and `expected_answer` to a local Parquet file. The resulting file contains material from both datasets. Check the source dataset's CC-BY-SA-4.0 license before sharing it.

## Dataset statistics

- 11,405 conversations with unique `idx` values.
- Topics: Physics 8,806 (77.2%); Chemistry 1,651 (14.5%); Biology 948 (8.3%). These proportions reflect the attempted range of source rows.
- User and assistant messages per conversation, excluding the system prompt: minimum 3, median 5, mean 5.5, maximum 17.
- Tool actions per conversation: minimum 0, median 3, mean 3.6, maximum 22. At least one tool action occurred in 88.2% of conversations.
- Of 41,550 tool calls, 54.9% returned a shellsim parser or interpreter limitation error such as `unsupported by minimal shim`. At least one such error occurred in 63.5% of conversations (72.0% of conversations with tool use).
- `shellsim_commit`: 7,284 conversations (63.9%) record `930d0d4` from shellsim's `origin/main`; 4,121 (36.1%) have no recorded commit and used an earlier build.

## Limitations

- Both roles were generated by GLM-5.3. These are synthetic conversations, not exchanges with human users.
- The release covers 11,405 of 150,644 source rows (7.6%). The generation run stopped after attempting the first 20,630 rows.
- Shellsim's Python support was limited and changed during generation. The assistant sometimes worked around simulator limitations; those steps remain in `full_log`. Conversations without a recorded `shellsim_commit` used an earlier build with fewer Python features.
- Filtering used automated checks and a GLM-5.3 grading pass. Development spot-checks found many of its flags accurate, but there was no exhaustive human review of retained or removed conversations. Factual errors, unsupported verification claims, and incoherent replies may remain.
- The simulated user could still disagree with the assistant when a conversation ended. The generation process did not require agreement.

## License

The generated conversational content (`messages` and `full_log`) and derived fields are released under the [OpenMDW License](https://openmdw.ai/), version 1.1; see [`LICENSE`](LICENSE). The source questions and reference answers belong to [nvidia/Nemotron-RL-Science-v1](https://huggingface.co/datasets/nvidia/Nemotron-RL-Science-v1) and are distributed under its CC-BY-SA-4.0 license.

## Acknowledgements

We thank [Ortet](https://ortet.ai), a frontier AI lab for health, for providing inference compute to create open data for scientific reasoning with computational tools.
