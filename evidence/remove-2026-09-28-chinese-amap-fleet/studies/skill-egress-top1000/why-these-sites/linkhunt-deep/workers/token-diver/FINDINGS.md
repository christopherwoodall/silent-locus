# TOKEN-DIVER findings — Discord webhook full tokens in the evaluator corpus

**Date:** 2026-10-05
**Worker:** token-diver (subagent 361749fd)
**Task:** document-only deep dive on Discord webhook full tokens found in the evaluator corpus.
**Sensitivity note:** this file is the evidence vault. Full observed credential values are recorded below per the standing "never redact from evidence" rule. These are live-format bearer credentials (Discord webhook id/token pairs). Document-only: never validate, never fetch the webhook URLs, never transmit the tokens beyond this file.
**Scope:** agents/infrastructure only. No human/operator attribution.

---

## 1. What the evaluator corpus is (surrounding structure)

### 1a. The evaluator persona's mission — NOT a benchmark run's score output

The `personas/evaluator/` directory is a hunt lane ("EVAL-HUNT") that ran 2026-10-05 (~00:49–06:45 CDT). Its mission: **find wild agent activity matching known eval benchmarks** — the inverse of the Amap-fleet work (the Amap fleet was confirmed DoE→dsqa_250 but matches NO public benchmark; the evaluator hunted wild activity that DOES match a known eval).

Five sub-lanes:
- **gaia-lane** (`raw/gaia-lane.md`): swept urlquery for GAIA validation-question fingerprints (165 validation questions parsed from an open `zhengxiaodu/dify-agents` snapshot). Verdict: honest negative — no GAIA-shaped agent activity.
- **swe-lane** (`raw/swe-lane.md`): swept for SWE-bench/Commit0/terminal-bench traces. Found 4 real OpenHands eval-monitor runs (swebench, swtbench, commit0×2; claude-opus-4-7, gpt-5-5, qwen3-coder-next via litellm proxy) scanned on urlquery May 1–19 2026, plus 20 `app.all-hands.dev/conversations/<uuid>` share links scanned Jun–Sep 2026. But the scans are of public dashboards — submitter (agent vs human) unattributable; conversation contents 401-blocked.
- **webarena-lane** (`raw/webarena-lane.md`): WebArena/WebVoyager/Mind2Web keyword sweeps — all noise or weak negatives.
- **scoredrop-lane** (`raw/scoredrop-lane.md`): **hunted escaped eval runs reporting scores via dead-drop inboxes** — this lane produced `phase1_results.json`.
- **harness-lane** (`raw/harness-lane.md`): eval-harness scaffolding markers (inspect_ai, lm-eval, task_id=, run_id=, sample_id, epoch=) + HF "eval trace" datasets. Honest negative on wild harness telemetry; watch-listed 0skeng.com (Basque-CAPTCHA agent-luring benchmark).

### 1b. What phase1_results.json actually is

`personas/evaluator/raw/phase1_results.json` (30,490 bytes) is the **phase-1 URL inventory** from the scoredrop lane. It is NOT an agent benchmark's score output. It is the raw result set of 12 urlquery htmx `q=` searches (see `raw/phase1.log`), one key per query:

- Dead-drop domains: `webhook.site` (5 reports), `ntfy.sh` (23), `0x0.st` (24), `paste.rs` (24), `rentry.co` (24), `discord.com/api/webhooks` (19)
- Eval-keyword queries: `accuracy` (24), `pass@1` (24), `exact_match` (3), `task_complete` (0 — retries exhausted), `swe-bench` (8), `scoreboard` (24)

Each entry = `{report_id, url, date}` where `url` is the urlquery report's **submitted URL**. Phase 2 (`raw/phase2_results.json`, `raw/phase2.log`) ran 4 more queries: `benchmark`, `leaderboard`, `?score=`, `?accuracy=`.

**Therefore the `accuracy`/`pass@1`/`task_complete`/`swe-bench`/`scoreboard` keys are search terms, not benchmark results.** The evaluator was looking for escaped eval runs *reporting scores through dead-drop inboxes*. The scoredrop lane's pre-result local find: 2 dead-drop-inbox scans already in the Amap fleet corpus (`eb4ecb55...` relay route via href.li with epoch run-nonce `?run=1791126770493`; `97f0619b...` direct), graded infrastructure-shaped, not score-shaped.

### 1c. How the webhook URLs got into this inventory

The `discord.com/api/webhooks` key holds 19 reports whose submitted URL matched the htmx query `discord.com/api/webhooks` (urlquery `q` matches submitted-URL text). Six of the 19 submitted URLs are **full webhook URLs with tokens**; the other 13 are loose-match junk (game-spam domains like `arcanefurybeta.com`, `arcanewrath.com`, `rpgvalkadia.com` — the same loose htmx matching behavior documented in gaia-lane). Prior work (corpus-grepper FINDINGS.md §4) listed only 3 of the 6; this dive found all 6.

---

## 2. The six webhook records (evidence vault)

All from `discord.com/api/webhooks` key of `phase1_results.json`. Webhook IDs are 19-digit snowflakes; tokens follow the `/` separator.

### Record A — report `6e712034-a2ee-4d14-9fe1-4d755114434f`, 2026-09-03T22:29:00Z
- URL: `discord.com/api/webhooks/1510273553176592507/sKKeGWq97Ny7N8aYBn7JaY3PeqC1qwJvTdY6ftxeIcS12GoFPx9-J7yc8iDefb2dVh-`
- Webhook ID: `1510273553176592507` (19 digits)
- Token: `sKKeGWq97Ny7N8aYBn7JaY3PeqC1qwJvTdY6ftxeIcS12GoFPx9-J7yc8iDefb2dVh-` (67 chars; ends `-`)
- Local capture: `personas/evaluator/raw/http_6e712034-a2ee-4d14-9fe1-4d755114434f.html` (keyless `/api/htmx/report/{id}/filter/http` pull, 20 KB)
- Capture contents: sandbox issued `GET /api/webhooks/1510273553176592507/<token> HTTP/1.1` (Referer: the webhook URL itself) → **404 Not Found, 45 B**, IP `162.159.138.232`. Only other request: `GET discord.com/favicon.ico`. No POST, no payload, no JavaScript.
- Shape: bare-URL read probe of the webhook endpoint.

### Record B — report `cb42fda7-003e-4f98-b651-67adecf2e1bd`, 2026-07-20T23:11:15Z
- URL: `discord.com/api/webhooks/1495584774142689451/cVdZCwBoBJ9MQYkK_WXz-vZrDdUB8-GdtvT2o5oyXXaG9C4MKmxPSbgVBGSLujFy7EhQ`
- Webhook ID: `1495584774142689451`
- Token: `cVdZCwBoBJ9MQYkK_WXz-vZrDdUB8-GdtvT2o5oyXXaG9C4MKmxPSbgVBGSLujFy7EhQ` (68 chars)
- Report page (fetched 2026-10-05, text only): submitted URL = the bare webhook URL; finishing URL identical; IP `162.159.138.232` (AS13335 CLOUDFLARENET); 8 HTTP transactions; detections: urlquery 0, NIDS 0, Threat Detection 0. No scan-result detail rows recovered in text fetch.
- Shape: bare-URL read probe.

### Record C — report `3059e28c-829e-48c2-b9df-d11aa265bb05`, 2026-04-04T07:02:53Z
- URL: `discord.com/api/webhooks/1489875390095818832/W9CQpSVHiUCWqkKy8faMsoXS-dLsO6o2nnDYrcoRHVYHUsJJECB6naVWgLhMtzzYcyfV`
- Webhook ID: `1489875390095818832`
- Token: `W9CQpSVHiUCWqkKy8faMsoXS-dLsO6o2nnDYrcoRHVYHUsJJECB6naVWgLhMtzzYcyfV` (68 chars)
- Report page: submitted URL = bare webhook URL; finishing URL identical; IP `162.159.136.232` / host `162.159.128.233` (AS13335); 1 HTTP transaction (581 B sent / 2.2 kB received); Suricata/ET-Pro NIDS fired **ET INFO Observed Discord Service Domain (discord .com) in TLS SNI** (low severity, informational only); 0 other detections.
- Shape: bare-URL read probe.

### Record D — report `14186863-5aea-4225-b16b-bd8407f0bfab`, 2026-01-31T01:25:21Z
- URL: `discord.com/api/webhooks/1463631524258648146/qSpy3WaRp77Lfk1SdueTEGUfsetaZNIhaupfEGRPvEK5xDxj-wq4MnzY5y2w0uLSnboD`
- Webhook ID: `1463631524258648146`
- Token: `qSpy3WaRp77Lfk1SdueTEGUfsetaZNIhaupfEGRPvEK5xDxj-wq4MnzY5y2w0uLSnboD` (68 chars)
- Report page: submitted URL = bare webhook URL; finishing URL identical; IP `162.159.137.232` / `162.159.138.232` (AS13335); 1 HTTP transaction (581 B sent / 2.2 kB received); same Suricata ET INFO Discord-SNI alert (low); 0 other detections.
- Shape: bare-URL read probe.

### Record E — report `1fb93d44-485d-49db-82ae-56e01e63e85b`, 2025-09-10T16:03:07Z — **different shape**
- Submitted URL: `43.226.1.26:5000/get_soundhttps:/discord.com/api/webhooks/1404099194175619203/FktBiiN76dGTrk`
- Webhook ID: `1404099194175619203`
- Token fragment: `FktBiiN76dGTrk` (14 chars — see §4)
- Report page: target IP `43.226.1.26` (AS16276 OVH SAS; SE geo flag); page title **"404 Not Found"**; 2 HTTP transactions; Threat Detection Systems = 1 — **Quad9 DNS verdict on 43.226.1.26: malicious / Sinkholed**. urlquery 0, NIDS 0.
- Shape: the webhook URL is **concatenated into a URL aimed at an OVH IP on port 5000 with a `/get_sound` path** — exfil-target/C2-config-shaped, not a bare probe. The submitting party pointed the urlquery scanner at the IP endpoint, which embeds the discord webhook URL in its path.

### Record F — report `4f309f4c-0204-40ca-8861-4e3390accd60`, 2025-05-31T19:31:53Z
- URL: `discord.com/api/webhooks/1339377338789527583/ZaaIPm4r2pFnKkE4RUXqcS7xZBcizAgYuFYROtiKuY4mBlDtpUuVxpzdEO-vDdFinBBV`
- Webhook ID: `1339377338789527583`
- Token: `ZaaIPm4r2pFnKkE4RUXqcS7xZBcizAgYuFYROtiKuY4mBlDtpUuVxpzdEO-vDdFinBBV` (68 chars)
- Report page: submitted URL = bare webhook URL; finishing URL identical; IP `162.159.128.233` (AS13335 CLOUDFLARENET); 2 HTTP transactions; detections 0 across urlquery, NIDS, Threat Detection Systems, Public InfoSec YARA, OpenPhish, PhishTank, Quad9, ThreatFox.
- Shape: bare-URL read probe.

---

## 3. Frozen-corpus check

`~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/dataset/unified_reports.jsonl`:
- All 6 report IDs (8-char prefixes: `6e712034`, `cb42fda7`, `3059e28c`, `14186863`, `1fb93d44`, `4f309f4c`): **0 lines each — none in the frozen corpus.**
- All 6 webhook numeric IDs: **0 lines each — none in the frozen corpus.**
- Only `phase1_results.json` and `phase2_results.json`/`uq_harness_hits.jsonl` were checked within the evaluator dir: `phase2_results.json` and `uq_harness_hits.jsonl` contain **zero** `discord.com/api/webhooks/` strings — phase1_results.json is the sole holder.

Classification: all six records are **GENUINELY NEW** to the frozen urlquery-incidents corpus.

## 4. Wider-corpus grep for the webhook IDs (numeric prefixes)

**Targeted single-pass sweep** (all six 19-digit IDs + all six 8-char report-ID prefixes, one `grep -f` pass per location), 2026-10-05:

| Location | Result |
|---|---|
| `silent-locus/data/2026-10-03-openai-agent-traces/events.jsonl` (589,972 lines) | **1 line — FALSE POSITIVE.** Line 170637 matched report-ID prefix `4f309f4c` only as a hex substring of a SHA-256 `fingerprint` digest (`7bbd985e…dc4f309f4cb3be…`). The record is `record_kind: arquivo_pt_capture`, `@timestamp: 2026-06-17T08:41:50Z`, collection SAWP5 / incident `doe-crdc` (source: `data/2026-10-01-arquivo-pt/raw/doe-crdc.cdx.jsonl.gz`, line 167223). Nothing to do with the urlquery report. **Zero genuine recurrences.** |
| `silent-locus/data/2026-10-01-oai-tag-sweep/events.jsonl` (96,353 lines) | 0 |
| `silent-locus/data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141 lines) | 0 |
| `silent-locus/collections/*/data/*.jsonl` | 0 files |
| `~/workspace/muse-home/projects/skill-tracer/` | 0 files |
| Frozen corpus `unified_reports.jsonl` | 0 lines on all 6 report IDs and all 6 webhook IDs (§3) |

**Full-tree sweep** (`~/workspace/silent-locus/`, excl. `.git`/`node_modules`/`studies/skill-egress-top500/`) was started and then stood down after the targeted sweep proved definitive; partial output for ID `1510273553176592507` showed only the three expected files —
- `personas/evaluator/raw/phase1_results.json` (source),
- `personas/evaluator/raw/http_6e712034-a2ee-4d14-9fe1-4d755114434f.html` (local capture),
- `studies/skill-egress-top1000/why-these-sites/workers/corpus-grepper/FINDINGS.md` (the study's own writeup — not independent corroboration).

Known from the earlier corpus-grepper sweep (2026-10-05): the pattern `discord.com/api/webhooks` hit 13 files / 25 lines across the three corpora, with `phase1_results.json` the most interesting (7 line-matches). The other references are *discussions* of the dead-drop surface, not observed tokens:
- `full-sweep/raw/trick-deaddrops.md` (2 lines): "No public webhook-message log service exists… detection would require leaked {id}/{token} pairs in code (gitleaks/vibeguard-style), which is a code-search lane, not a service lane." — clean negative as a *surface*.
- `personas/tracker/raw/deaddrops.md` (1 line): same note.
**No other file in the three corpora carries a full webhook id/token pair.** `phase2_results.json` and `uq_harness_hits.jsonl` contain zero `discord.com/api/webhooks/` strings — `phase1_results.json` is the sole holder among evaluator outputs.

## 5. Token structure observations (descriptive only)

Computed locally from `phase1_results.json` — no analysis-for-use:

| Webhook ID | ID len | Token len | Token charset classes |
|---|---|---|---|
| 1510273553176592507 | 19 | 67 | A–Z, a–z, 0–9, `-`, `_` (trailing `-`) |
| 1495584774142689451 | 19 | 68 | A–Z, a–z, 0–9, `-`, `_` |
| 1489875390095818832 | 19 | 68 | A–Z, a–z, 0–9, `-`, `_` |
| 1463631524258648146 | 19 | 68 | A–Z, a–z, 0–9, `-`, `_` |
| 1404099194175619203 | 19 | **14** | A–Z, a–z, 0–9 only (no `-`/`_`) |
| 1339377338789527583 | 19 | 68 | A–Z, a–z, 0–9, `-`, `_` |

Notes:
- IDs are uniformly 19 decimal digits (Discord snowflake length).
- Five tokens are 67–68 chars over the URL-safe base64-ish alphabet `[A-Za-z0-9-_]`.
- The 14-char token (record E) is an outlier: it appears **truncated** — in the submitted URL the webhook path is concatenated directly onto `.../get_soundhttps:/discord.com/...`, i.e. the token string was cut when the URL was assembled/embedded. A 14-char token would not be a complete Discord webhook credential; treat as a fragment, not a usable credential.
- Tokens were never re-fetched, re-requested, or transmitted anywhere. Length/charset were computed from the file bytes already on disk.

---

## OBSERVED (bytes)

1. `phase1_results.json` is a urlquery-search URL inventory from the evaluator's scoredrop lane (12 htmx queries: 6 dead-drop domains + `accuracy`/`pass@1`/`exact_match`/`task_complete`/`swe-bench`/`scoreboard`), not an agent benchmark's score output. Its keys are search terms.
2. Six full `discord.com/api/webhooks/<id>/<token>` URLs appear as submitted URLs in six urlquery reports spanning 2025-05-31 → 2026-09-03. Three were previously documented (records A, B, C); three are newly surfaced here (records D, E, F).
3. Five of the six (A, B, C, D, F) were submitted as bare webhook URLs; the urlquery sandbox performed read-only GETs resolving to Discord/Cloudflare edge IPs (162.159.128.232–162.159.138.232, AS13335). Record A's local capture shows `GET` → **404 Not Found (45 B)** at scan time (2026-09-03). Records B–D/F report pages show 0 detections (C and D additionally carry only the informational Suricata "Observed Discord Service Domain in TLS SNI" alert).
4. Record E (2025-09-10) is structurally different: the webhook URL is embedded in a submitted URL aimed at `43.226.1.26:5000/get_sound` (OVH SAS, AS16276) — Quad9 verdict on that IP: **malicious / Sinkholed**. Its token is a 14-char truncated fragment.
5. None of the six report IDs or webhook IDs occur in the frozen corpus `unified_reports.jsonl` (0 lines each).
6. **Zero genuine recurrences in the wider corpora.** Targeted sweep (all six 19-digit IDs + all six 8-char report-ID prefixes): 0 hits in oai-tag-sweep events, amap-fleet events, all `collections/*/data/*.jsonl`, skill-tracer, and the frozen corpus. The single openai-agent-traces hit (`4f309f4c`, line 170637) is a hex-substring false positive inside a SHA-256 fingerprint of an arquivo.pt CDX capture (doe-crdc, 2026-06-17) — unrelated to the urlquery report.
7. The evaluator lane notes (`scoredrop-lane.md`) document that the lane's actual dead-drop-inbox finds were webhook.site inboxes in the Amap fleet (infrastructure-shaped, no score payloads) — the Discord tokens were incidental inventory hits from the domain query, not score-reporting evidence.

## INFERENCE (clearly separated)

1. **Agent-posted dead drop vs test fixture — unresolved, leaning neither way on evidence.** The bare-URL probes (A–D, F) are consistent with *either* (a) a security researcher scanning a leaked webhook URL they found elsewhere, or (b) an agent (or its operator) submitting a webhook URL to urlquery to check it / see what the scanner sees. urlquery exposes no submitter identity on keyless endpoints, so submitter attribution is impossible from available data. The scan itself never POSTs — nothing in the captures shows message content being sent *to* the webhook.
2. **Record E looks more malicious-shaped than the rest** (OVH IP, `/get_sound` path, Quad9-sinkholed), and its token fragment suggests the webhook URL was copy-pasted into malware/C2 config text. But "malware-shaped" is not "agent-shaped": no `zz=`/`uqscan=`/epoch-nonce grammar or other fleet markers accompany it. It may be ordinary crimeware, not the swarm.
3. **Record A's 404 at scan time** (2026-09-03) is a scan-time observation from the saved capture, not a fresh validation — I did not and will not re-request it. A 404 on GET means the token was already invalid/deleted when scanned, *or* never valid; it does not distinguish rotation from fabrication.
4. **Eval-run connection: none established.** These tokens entered the evaluator corpus as dead-drop-domain inventory hits. The scoredrop lane found no score payloads, no `accuracy`/`pass@1` JSON exfil, and no harness markers tied to these reports. There is no evidence any eval run used these webhooks to report results.
5. **Why 2025 dates matter:** records E (2025-09-10) and F (2025-05-31) predate the current hunt window and the May–Jun 2026 incident cluster; they are background internet noise (leaked webhook URLs are routinely scanned), not necessarily part of any 2026 agent incident.

## What's still unknown

1. **Submitter identity for all six reports** — unattainable keylessly; needs authenticated urlquery API access (submitter metadata), which is out of this lane's scope.
2. **Scan-time response bodies for records B–F** — only record A has a local HTTP-transaction capture. The report-page text fetches truncated the HTTP transaction tables, so response codes/sizes for B–F are unconfirmed (only counts: B=8, C=1, D=1, E=2, F=2 transactions).
3. **Whether the full tokens (A–D, F) were valid at scan time** — deliberately not tested (hard rule). Record A's capture already shows 404 for A; the rest are unknown and will stay unknown.
4. **Full-tree numeric-ID sweep** — stood down after the targeted sweep proved definitive (§4 table): **zero genuine recurrences** of any webhook ID or report ID in oai-tag-sweep, amap-fleet, all collections, skill-tracer, and the frozen corpus. The single openai-agent-traces hit resolved as a hex-substring false positive (see table).
5. **Record E's `/get_sound` endpoint context** — the OVH IP is Quad9-sinkholed; the path grammar (`get_sound` + concatenated webhook URL) resembles infostealer/SSRF-probe config. Whether it connects to any known corpus campaign is unexamined.
6. **Provenance of the tokens** — where the submitter obtained them (leaked in code? generated for testing? harvested?) is unknown and out of scope (no human/operator attribution per hunt rules).

---

## Repro / provenance

- Source file: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/evaluator/raw/phase1_results.json`
- Query log: `raw/phase1.log` (12 queries, 2026-10-05 06:05 UTC); lane notes: `raw/scoredrop-lane.md`
- Local capture (record A only): `raw/http_6e712034-a2ee-4d14-9fe1-4d755114434f.html`
- Report pages (records B–F): fetched 2026-10-05 via text fetch of `https://urlquery.net/report/<uuid>` — read-only, no discord.com requests issued
- Frozen corpus: `~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/dataset/unified_reports.jsonl` — 0 hits on all 6 report IDs and all 6 webhook IDs
- Prior art: `studies/skill-egress-top1000/why-these-sites/workers/corpus-grepper/FINDINGS.md` §4 (documented 3 of the 6)
- Token structure table: computed locally via python from file bytes (length/charset only)
- **Nothing in this file was obtained by requesting discord.com/api/webhooks or any token-bearing URL.**
