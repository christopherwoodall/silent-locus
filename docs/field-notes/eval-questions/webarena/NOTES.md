# NOTES — webarena

- Source URL: https://raw.githubusercontent.com/web-arena-x/webarena/main/config_files/test.raw.json
- Homepage: https://webarena.dev/
- Eval org: Academic (CMU)
- License: apache-2.0
- Retrieved: 2026-10-05
- Raw file: raw/test.raw.json (byte-identical)
- Banked questions: 812 / expected 812 (paper) — MATCH
- Included: yes, with caveat — task templates (instantiated `intent` + start URL) referencing self-hosted WebArena environments, not the live web; limited trace value on public web surfaces (per inventory)
- Normalization: JSON array of 812 task objects; question_id = webarena-{task_id:04d}; question = instantiated `intent` (template slots filled, e.g. 'What is the top-1 best-selling product in 2022'); topic = comma-joined `sites` list (e.g. 'shopping_admin').
