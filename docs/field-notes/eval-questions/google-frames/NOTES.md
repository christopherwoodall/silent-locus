# NOTES — google-frames

- Source URL: https://huggingface.co/datasets/google/frames-benchmark/resolve/main/test.tsv
- Homepage: https://huggingface.co/datasets/google/frames-benchmark
- Eval org: Google
- License: apache-2.0
- Retrieved: 2026-10-05
- Raw file: raw/test.tsv (byte-identical)
- Banked questions: 824 / expected 824 (paper) — MATCH
- Included: yes — multi-hop questions (2–15 constraints), iterative-search RAG eval
- Normalization: TSV parsed with csv.DictReader(delimiter='\t'). question_id = frames-0000..0823. topic = reasoning_types column. question = Prompt column, whitespace-normalized.
