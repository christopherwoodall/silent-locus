# NOTES — google-facts-grounding

- Source URL: https://huggingface.co/datasets/google/FACTS-grounding-public/resolve/main/examples.csv
- Homepage: https://deepmind.google/discover/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models
- Eval org: Google DeepMind
- License: cc-by-4.0
- Retrieved: 2026-10-05
- Raw file: raw/examples.csv (19.7MB, byte-identical)
- Banked questions: 860 / expected 860 (datasets-server) — MATCH
- Included: yes — long-form factuality eval; the `user_request` is the question, `context_document` is the grounding doc
- Normalization: CSV needs csv.field_size_limit(sys.maxsize) (context_document fields are huge; naive wc -l shows 220534 lines due to embedded newlines, true records = 860). question_id = facts-0000..0859. topic = '' (no topic column in source).
