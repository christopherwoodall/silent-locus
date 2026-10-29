# NOTES — webvoyager

- Source URL (inventory): https://raw.githubusercontent.com/MinorJerry/WebVoyager/main/data/tasks_test.jsonl
- Homepage: https://github.com/MinorJerry/WebVoyager
- Eval org: Academic (Microsoft et al.)
- License: apache-2.0
- Retrieved: 2026-10-05
- Raw files: raw/tasks_test.jsonl (256 bytes — see quirk), raw/WebVoyager_data.jsonl, raw/reference_answer.json (all byte-identical)
- Banked questions: 643 / expected 643 (paper) — MATCH
- Included: yes — web-agent tasks across 15 live websites
- QUIRK (important): the inventory's URL (tasks_test.jsonl) is a 256-byte file containing exactly ONE example task — it is not the eval set. The real 643-task set is data/WebVoyager_data.jsonl in the same repo (verified: 643 records, 643 unique ids; wc -l shows 642 only because the last line lacks a trailing newline). Both files banked; questions.jsonl built from WebVoyager_data.jsonl.
- Normalization: question_id = source `id` (e.g. 'Allrecipes--0'); question = `ques`; topic = `web_name` (the website, closest categorical metadata).
