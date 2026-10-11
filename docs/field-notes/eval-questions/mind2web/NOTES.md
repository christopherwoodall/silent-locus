# NOTES — mind2web

- Source URL: https://huggingface.co/datasets/osunlp/Mind2Web/resolve/main/data/train/train_{0..10}.json and .../test.zip
- Homepage: https://osu-nlp-group.github.io/Mind2Web/
- Eval org: Academic (OSU NLP)
- License: cc-by-4.0
- Retrieved: 2026-10-05
- Raw files (all byte-identical, sizes verified against CDN content-length): raw/train_0.json (616MB) … raw/train_10.json (28MB), raw/test.zip (567MB)
- Banked questions: 1009 (train only) / expected 2350 (paper) — see test-set note
- TEST SET NOTE (important): test.zip is password-encrypted (ZipCrypto). The password is PUBLIC — `mind2web` — documented in the Mind2Web GitHub README ("unzip it with password `mind2web`"), which also states "Please DO NOT redistribute the unzipped data files online." Verified by local extraction: test splits contain 1341 tasks (test_domain 912 + test_task 252 + test_website 177), and 1009 (train) + 1341 (test) = 2350 exactly matching the paper. Per the authors' no-redistribution request, test questions are NOT banked in questions.jsonl (this collection pushes to GitHub); only the encrypted test.zip is banked in raw/. questions.jsonl covers the public train split (1009 tasks).
- DOWNLOAD QUIRK: the ~500-650MB train files truncate on single-pass curl; all files were completed with `curl -L -C -` resume loops and size-verified against content-length. Initial partial downloads were corrupt (truncated mid-JSON) — final files validated by streaming JSON parse of every record.
- Included: yes — natural-language web-agent task instructions (+ action sequences) on real websites
- Normalization: streaming parse (json.JSONDecoder.raw_decode per top-level object; files too large for json.load). question_id = `annotation_id`; question = `confirmed_task`; topic = `subdomain` (fallback `domain`).
