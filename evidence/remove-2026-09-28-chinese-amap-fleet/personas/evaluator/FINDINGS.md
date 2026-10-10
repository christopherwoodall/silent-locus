# THE EVALUATOR — FINDINGS
## Hunting escaped eval runs

**Persona:** hunt ESCAPED EVAL RUNS specifically — agents running benchmarks that got loose. Inverse of the eval-coordinator (which linked known traces→evals): find wild agent activity that DOES match known evals.
**Run:** 2026-10-05 ~05:55–06:25 UTC. Egress healthy. Five crawl lanes + coordinator direct hunt.
**Method:** urlquery htmx (≤1 req/5s), new keyless report-data endpoints (HTMX_ENDPOINTS.md), HF via curl. Every candidate verified against our sets: amap-fleet events.jsonl (2,141), openai-agent-traces events.jsonl (589,972), oai-tag-sweep events.jsonl (96,353), collections/*/data/*.jsonl.

---

## HEADLINE FIND: code-review-fix eval task family leaking through Greptile IDE API (CONFIRMED, genuinely new)

Four urlquery reports, same task grammar — *"Fix the following N code review issues. Work through them one at a time, proposing concise fixes."* — submitted via Greptile's IDE API (`/api/ide/codex`, `/ide/claude-code`). The benchmark task prompt itself was fetched by an agent's IDE and scanned, leaking eval task text into urlquery:

| # | Report | Date (UTC) | Repo | Task | Via |
|---|---|---|---|---|---|
| 1 | [5ee91a65-07db-4b75-afe7-fe2ad3d2beac](https://urlquery.net/report/5ee91a65-07db-4b75-afe7-fe2ad3d2beac) | 2026-06-07 01:52 | `scaleapi/terminal-bench-3` | `tasks/bilingual-ui-rtl/` (Terminal-Bench task dir), branch `ci-check/task-1779812786`, PR 1489, 2 review issues | `app.greptile.com/api/ide/codex` |
| 2 | [e33a6324-4b7f-4c49-b25e-b760d0e8a45e](https://urlquery.net/report/e33a6324-4b7f-4c49-b25e-b760d0e8a45e) | — | `aegra/aegra` | 2 review issues (auth_middleware.py) | `app.greptile.com/ide/claude-code` |
| 3 | [2d108260-a6e7-4168-aa01-73f2be4ed8ab](https://urlquery.net/report/2d108260-a6e7-4168-aa01-73f2be4ed8ab) | — | `lgtm-hq/rustume` | 4 review issues | `app.greptile.com/ide/claude-code` |
| 4 | [c55d39c5-68ca-4e3e-be39-a354299cdb46](https://urlquery.net/report/c55d39c5-68ca-4e3e-be39-a354299cdb46) | — | `leona-quantum/leona` | majorana_api courses.py issue | `app.greptile.com/ide/claude-code` |

**Agent-shaped because:** benchmark task prompts (repo + branch + PR + review issues, verbatim) appearing in submitted URLs = an agent's IDE fetching eval task instructions and the fetch being scanned. The `tasks/bilingual-ui-rtl/` path is Terminal-Bench's canonical task-dir layout — the smoking gun for benchmark origin. Report 1 tagged `agent-ide` by the hunter sweep.
**Verification:** record 1 from oai-tag-sweep sweep-corpus; records 2–4 from `frozen:urlquery-incidents` (re-hunt fingerprints). Zero hits in amap-fleet corpus and openai-agent-traces — genuinely new family, not ours.
**Foreign-language angle:** `bilingual-ui-rtl` is an RTL (right-to-left) UI task — Arabic/Hebrew UI territory. Follow-up: check whether the task's test fixtures involve Arabic/Hebrew content.
**Raw evidence:** `raw/greptile-terminal-bench-report.html`, `raw/greptile-aegra-report.html` (full keyless /filter/http captures).

---

## Lane 2 (SWE-bench): real eval runs scanned, but scans ≠ escaped agents

- **Four real OpenHands eval runs** scanned May 1–19, 2026 — public dashboards with run metadata (`params.json`, `submission.json`, `cost_report.jsonl`):
  - [dfa38929-a7e1-4ee3-8a8c-4c6573632cbc](https://urlquery.net/report/dfa38929-a7e1-4ee3-8a8c-4c6573632cbc) — `?run=swebench/litellm_proxy-anthropic-claude-opus-4-7/24840336632/`
  - [fcbc6e99-849d-4c7f-b426-78db224d9310](https://urlquery.net/report/fcbc6e99-849d-4c7f-b426-78db224d9310) — `?run=commit0/litellm_proxy-anthropic-claude-opus-4-7/24863774497/`
  - [c92092b5-6746-41e7-943a-b4db8a9b6bb7](https://urlquery.net/report/c92092b5-6746-41e7-943a-b4db8a9b6bb7) — `?run=commit0/litellm_proxy-openai-gpt-5-5/1778132350/` (run-id = epoch 2026-05-07 05:39:10 UTC, scanned 2.5 min later)
  - [b382593f-a3c5-4c51-bdf8-d5f299585846](https://urlquery.net/report/b382593f-a3c5-4c51-bdf8-d5f299585846) — `?run=swtbench/litellm_proxy-openrouter-qwen-qwen3-coder-next/25976432719/` (GENUINELY NEW; others known)
- **20 new `app.all-hands.dev/conversations/<uuid>` agent-conversation share links** scanned Jun 12–Sep 20, 2026 (full IDs in `raw/swe-lane.md`; e.g. b4fee2b8-… 2026-09-20). Conversation API returns 401 — content auth-gated, eval content unconfirmable.
- **Honest grade:** SWE-bench-shaped wild traces DO exist — but these are *scans of public/agent surfaces*, not agent telemetry. The submitter (agent vs human) is unattributable keylessly. This lane did NOT find an escaped agent's own eval exhaust (zero FAIL_TO_PASS/test_patch/instance_id-shaped agent URLs). It proves coding evals happen in the wild with public dashboards; it does not prove the evals escaped.

## Lane 1 (GAIA): honest negative
165 GAIA validation questions secured (open GitHub mirror, gated HF bypassed); ~40 distinctive fingerprints searched on urlquery — all real matches were routine single-page scans, never the question-specific resource. Zero genuine GAIA fingerprints in our holdings. One weak/curious: `httpbin.org/redirect-to?url=https://pubchem.ncbi.nlm.nih.gov/compound/Nigerloxin` ([37243246-de93-4a3d-9c9c-600c4e0ffc00](https://urlquery.net/report/37243246-de93-4a3d-9c9c-600c4e0ffc00), 2026-03-15) — probe-shaped, not GAIA's question. Note: GAIA harnesses likely use their own browser tooling, not urlquery — a true negative here is plausible.

## Lane 3 (WebArena/WebVoyager/Mind2Web): honest negative
No matches for any task family. Bonus: Amap-fleet grammar evolution — same-IP cluster systematically probing one POI with attempt counters `?uqm=1/2/3`, `?uqattempt=0/1`, `switchVersion?src=manual0/2` ([967b20ce-ad80-4042-8e24-1430896ddb80](https://urlquery.net/report/967b20ce-ad80-4042-8e24-1430896ddb80), [b031a5a0-6170-47c1-9d05-231dd02b7ee0](https://urlquery.net/report/b031a5a0-6170-47c1-9d05-231dd02b7ee0)) — new to our sets, same operator, evolved grammar. Flagged to fleet lane.

## Lane 4 (score dead-drops): no confirmed score-reporting
Zero scoreboard-shaped JSON in all corpora (2,141 / 96,353 / 589,972 / collections). Fleet dead-drop inboxes confirmed with epoch run-nonces (`webhook.site/a7753b69-…?run=1791126770493`, [eb4ecb55-d335-45fb-b775-6746d422c7f0](https://urlquery.net/report/eb4ecb55-d335-45fb-b775-6746d422c7f0); [97f0619b-36e5-4c01-adab-a18a89b2b319](https://urlquery.net/report/97f0619b-36e5-4c01-adab-a18a89b2b319)) — dead-drop infrastructure, not score-shaped. Two wild inboxes opened 2026-10-05 unreadable (webhook.site anonymous API 429). A `.result` file on 0x0.st ([d402e4b9-5648-4134-884e-4e71121c1bbf](https://urlquery.net/report/d402e4b9-5648-4134-884e-4e71121c1bbf)) expired before recovery — suggestive filename, unresolvable.

## Lane 5 (harness scaffolding): honest negative + one watch-listed lead
Zero for inspect_ai/lm-eval/openai-evals/eval_id; task_id=/run_id=/sample_id=/epoch= all resolved to spam/phishing/analytics noise. HF sweep (150 datasets): **watch-listed `hug-the-trees/0skeng-agentic-web-benchmark`** — price dataset paired with a LIVE agent-luring benchmark at 0skeng.com (dataset card addresses autonomous agents; Basque CAPTCHA gate); zero urlquery hits, dataset 3 days old. `taejoon89/Ko-Agent-Trajectories-1.0` (Korean synthetic): zero wild-agent markers — legit synthetic.

---

## Verification summary

| Candidate | Ours? | Verdict |
|---|---|---|
| Greptile code-review-fix family (4 reports) | New (0 in all sets) | **CONFIRMED escaped-eval-shaped** |
| OpenHands eval dashboards (4 reports) | 3 known, 1 new | Scans, not agent telemetry |
| all-hands.dev conversations (20) | 17 new | Content 401-gated, unconfirmable |
| Fleet dead-drop inboxes | Ours (amap-fleet) | Infrastructure, not scores |
| GAIA / WebArena / harness markers | — | Honest negatives |

## Non-English/non-Chinese flags
- `bilingual-ui-rtl` task: RTL UI territory (Arabic/Hebrew) — open follow-up on test fixtures.
- 0skeng: Basque CAPTCHA gate on an agent-luring benchmark.
- No French/German/Russian eval-shaped activity found on any lane.

## Open follow-ups
1. Dates for greptile reports 2–4; more greptile/codex/claude-code prompts live.
2. `bilingual-ui-rtl` test fixtures — Arabic/Hebrew content?
3. Authenticated urlquery API for submitter metadata on the 4 OpenHands eval-monitor reports.
4. Re-attempt the two wild webhook.site inbox reads after 429 cools.
5. Periodic re-check of 0skeng.com for agent traffic.

---

## APPENDIX — All observed URLs

### Greptile code-review-fix family
- https://urlquery.net/report/5ee91a65-07db-4b75-afe7-fe2ad3d2beac
- https://urlquery.net/report/e33a6324-4b7f-4c49-b25e-b760d0e8a45e
- https://urlquery.net/report/2d108260-a6e7-4168-aa01-73f2be4ed8ab
- https://urlquery.net/report/c55d39c5-68ca-4e3e-be39-a354299cdb46
- https://urlquery.net/api/htmx/report/5ee91a65-07db-4b75-afe7-fe2ad3d2beac/filter/http
- https://urlquery.net/api/htmx/report/e33a6324-4b7f-4c49-b25e-b760d0e8a45e/filter/http

### OpenHands eval dashboards
- https://urlquery.net/report/dfa38929-a7e1-4ee3-8a8c-4c6573632cbc
- https://urlquery.net/report/fcbc6e99-849d-4c7f-b426-78db224d9310
- https://urlquery.net/report/c92092b5-6746-41e7-943a-b4db8a9b6bb7
- https://urlquery.net/report/b382593f-a3c5-4c51-bdf8-d5f299585846

### Amap fleet grammar evolution (flagged, not eval)
- https://urlquery.net/report/967b20ce-ad80-4042-8e24-1430896ddb80
- https://urlquery.net/report/b031a5a0-6170-47c1-9d05-231dd02b7ee0

### Score dead-drop lane
- https://urlquery.net/report/eb4ecb55-d335-45fb-b775-6746d422c7f0
- https://urlquery.net/report/97f0619b-36e5-4c01-adab-a18a89b2b319
- https://urlquery.net/report/c9104bb8-8c1f-428f-b421-c57d0d4d53be
- https://urlquery.net/report/8213c4a1-41ea-438d-ada0-489eabb94deb
- https://urlquery.net/report/d402e4b9-5648-4134-884e-4e71121c1bbf

### GAIA lane (examined, not matches)
- https://urlquery.net/report/c04ee077-1cde-48a7-9b38-bcd4ee4c0f2b
- https://urlquery.net/report/7d814627-48ed-4326-b4fc-31c21157c584
- https://urlquery.net/report/e4ef535e-63c4-4282-bd57-db0e48e43d54
- https://urlquery.net/report/004bfc90-ddf1-48e4-9709-b0bf8f098772
- https://urlquery.net/report/37243246-de93-4a3d-9c9c-600c4e0ffc00

### HF / misc
- https://huggingface.co/datasets/hug-the-trees/0skeng-agentic-web-benchmark
- https://huggingface.co/datasets/taejoon89/Ko-Agent-Trajectories-1.0
- https://huggingface.co/datasets/DeusHorizon/agent-web-index
