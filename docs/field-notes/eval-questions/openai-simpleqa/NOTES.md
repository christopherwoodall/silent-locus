# NOTES — openai-simpleqa

- Source URL: https://openaipublic.blob.core.windows.net/simple-evals/simple_qa_test_set.csv
- Homepage: https://openai.com/index/introducing-simpleqa/
- Eval org: OpenAI
- License: MIT (simple-evals repo)
- Retrieved: 2026-10-05
- Raw file: raw/simple_qa_test_set.csv (byte-identical download)
- Banked questions: 4326 / expected 4326 (paper) — MATCH
- Included: yes — short factoid questions with per-question `urls` in metadata (trace gold for urlquery/urlscan hunting)
- Normalization: CSV parsed with Python csv module (handles multiline quoted fields; naive wc -l shows 4332 lines but true record count is 4326). question_id = simpleqa-00000..04325. topic = metadata['topic'] (e.g. 'Science and technology'). question = problem column, whitespace-normalized.
