---
license: cc-by-nc-4.0
language:
- kk
- ru
- en
base_model:
- Qwen/Qwen3-0.6B
pipeline_tag: text-generation
library_name: transformers
tags:
- kazakh
- russian
- agent
- tool-calling
- rag
- function-calling
- hermes
gated: auto
extra_gated_heading: "Access Farabi-0.6B-agent-rag"
extra_gated_description: "Access is granted automatically once you complete this short form. Please tell us who you are, your organization, and how you intend to use the model. Your Hugging Face username and email are shared with the authors automatically."
extra_gated_prompt: "This model is released for NON-COMMERCIAL use only under CC BY-NC 4.0. By requesting access you confirm the information below is accurate and you agree to these terms."
extra_gated_fields:
  Full name: text
  Organization / Affiliation: text
  Role / Title: text
  Country: country
  Intended use:
    type: select
    options:
      - Research
      - Education
      - Personal / hobby project
      - Evaluation / benchmarking
      - label: Other
        value: other
  Describe your intended use and purpose: text
  I agree to use this model for NON-COMMERCIAL purposes only: checkbox
  I agree to share my contact information with the model authors: checkbox
extra_gated_button_content: "Request access"
---

# Farabi-0.6B-agent-rag

A compact (0.6B) Kazakh / Russian / English assistant tuned for **grounded RAG** and
**agentic tool-calling**. It is designed to run on-device and to drop into agent stacks
that expect OpenAI-style function calling.

Built on Qwen3-0.6B and adapted for Kazakh, Russian, and English.

## Capabilities

- **Grounded RAG.** Answers strictly from provided passages, attributes claims to the
  supporting text, and **abstains when the evidence is insufficient** instead of
  fabricating an answer.
- **Tool-calling (Hermes / OpenAI function calling).** Decides when a tool is needed,
  asks for missing required arguments, and grounds the final answer in the tool result.
  - **Parallel tool-calling** — issues multiple independent calls in a single turn.
  - **Crosslingual argument normalization** — maps inflected Kazakh/Russian entities to
    canonical executable arguments (city → English name, dates → ISO-8601, currency →
    ISO-4217, units → canonical).
  - **Error recovery** — retries repairable failures, and reports non-repairable ones
    (not-found / permission-denied / empty) honestly instead of inventing success.
- **Prompt-injection resistance.** Treats retrieved documents and tool outputs as
  untrusted **data**, not instructions; ignores embedded directives, prefers
  least-privilege tools, and refuses to exfiltrate secrets found in context.
- **Text workbench.** Spelling / grammar / formality / clarity / concision edits,
  rewriting, translation, and summarization across kk / ru / en.
- **No hidden chain-of-thought** in trainable outputs — clean final answers and tool
  calls, suitable for production serving.

## Benchmarks

### Agentic & RAG capabilities (held-out probe)

| Capability | Score |
|---|---|
| Prompt-injection resistance (overall) | **89%** |
| &nbsp;&nbsp;• instruction-in-retrieved-chunk | 100% |
| &nbsp;&nbsp;• tool-output injection | 100% |
| &nbsp;&nbsp;• least-privilege tool use | 100% |
| &nbsp;&nbsp;• secret / data-exfiltration refusal | 54% |
| Parallel tool-calling | **99%** |
| Crosslingual argument normalization | **87%** |
| Text editing / workbench | **81%** |

> Note: secret-exfiltration refusal (54%) is the model's weakest safety dimension —
> use an output filter for credential-bearing contexts.

### Academic (ISSAI Kazakh/Russian QOLDA suite, n=250/bench; RAGBench = chrF)

Accuracy (%), compared with same-size and larger models for context. **AVG** is the mean of
the 10 accuracy benchmarks.

| Model | Size | ARC-kk | ARC-ru | MMLU-kk | GPQA-kk | GPQA-ru | GSM8k-kk | GSM8k-ru | PolyMath-kk | MMLU-Pro-kk | MMLU-Pro-ru | RAGBench (chrF) | **AVG** |
|---|--|--|--|--|--|--|--|--|--|--|--|--|--|
| **Farabi-0.6B-agent-rag** | 0.6B | 46.4 | 59.2 | 36.0 | 24.4 | 28.4 | 21.2 | 32.4 | 12.4 | 15.2 | 17.6 | 17.0 | **29.3** |
| ISSAI foggen-0.6B | 0.6B | 33.6 | 59.6 | 30.0 | 28.8 | 30.4 | 8.0 | 37.2 | 7.6 | 18.8 | 22.4 | 7.3 | 27.6 |
| Qwen3-0.6B | 0.6B | 29.6 | 51.2 | 33.2 | 22.0 | 22.4 | 7.2 | 41.6 | 8.0 | 14.0 | 16.8 | 15.6 | 24.6 |
| ISSAI Sherkala-8B-Chat | 8B | 74.8 | 78.4 | 47.6 | 30.0 | 25.6 | 68.8 | 80.0 | 20.4 | 20.4 | 22.4 | 41.0 | 46.8 |

At its size class Farabi-0.6B leads on the QOLDA average, ahead of both ISSAI foggen-0.6B and
the Qwen3-0.6B base. Sherkala-8B is shown as a larger-model reference point.

### Translation (FLORES-200, BLEU)

| Direction | BLEU |
|---|---|
| ru → en | 24.4 |
| en → ru | 17.1 |
| kk → en | 13.8 |
| en → kk | 8.2 |
| ru → kk | 5.6 |
| kk → ru | 1.9 |

## Serving

Works with vLLM's OpenAI-compatible server using the Hermes tool-call parser:

```bash
vllm serve nur-dev/farabi-0.6B-agent-rag \
  --chat-template chat_template.jinja \
  --enable-auto-tool-choice --tool-call-parser hermes
```

Then call it with the OpenAI SDK (and the OpenAI Agents SDK):

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="x")

resp = client.chat.completions.create(
    model="nur-dev/farabi-0.6B-agent-rag",
    messages=[{"role": "user", "content": "Бүгін Алматыда ауа райы қандай?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "Canonical English city name."}},
                "required": ["city"],
            },
        },
    }],
    tool_choice="auto",
)
print(resp.choices[0].message.tool_calls)
```

## Languages

Kazakh (kk), Russian (ru), English (en).

## License

**CC BY-NC 4.0 — non-commercial use only.** The model weights are released for research,
education, and evaluation; commercial use is not permitted. Built on Qwen3-0.6B (Apache-2.0);
the base-model components remain under their original Apache-2.0 terms.
