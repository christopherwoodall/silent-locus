# NOTES — openai-mle-bench

- Source URL: https://github.com/openai/mle-bench (git clone --depth 1, commit 507f92e1138bb6e40dac5c6ee7a6758e6424bf97, 2026-04-24)
- Homepage: https://github.com/openai/mle-bench
- Eval org: OpenAI
- License: MIT
- Retrieved: 2026-10-05
- Raw: raw/mle-bench/ (full repo clone)
- Banked questions: 82 / expected 75 (paper) — repo has MORE than the paper count
- Note: 84 dirs under mlebench/competitions/, of which 82 contain description.md (the other two entries are __init__.py and utils.py, not competitions). Paper reports 75 Kaggle tasks; the repo snapshot ships 82 task descriptions. Each task's `description.md` is the competition brief; `description_obfuscated.md` is the contamination-resistant variant actually shown to agents. Banked the plain description.md (question = full brief text, whitespace-normalized). Agent traces for these would hit kaggle.com competition pages.
- Included: yes — ML-engineering agent tasks (wrong-shape for web-search traces but in-scope per brief)
- Normalization: question_id = competition dirname (e.g. 'aerial-cactus-identification'); topic = ''.
