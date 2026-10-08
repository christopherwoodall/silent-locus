# Transluce findings ingest LEDGER

Running record of daily ingest runs of the Transluce volunteer Findings tracker
into the hunt corpus. Read-only pulls via `tl.py`; per-finding overlap
assessments are grep-verified against `~/workspace/silent-locus/data/`.

## 2026-10-08 (run: transluce-daily-ingest, ~07:40 CDT)

- Raw pull: `data/transluce-api/raw/findings-list-20261008.json`
  (109 findings, sha256 65681e8cf8815011c86a973e4edf708761f7ace18583588c9260f04053fc4ab2,
  fetched via paginated `GET /api/findings` because `tl.py findings` returns
  only the first 25 and `tl.py export json` truncates at 200KB.)
- Prior snapshot: `raw/findings-list.json` (2026-10-07, 25 findings,
  newest created 2026-10-07T18:24:04Z).
- New findings by created_at (2026-10-08): 5 (ids 170-174).

### Finding 170 — Nav 2025 jina.ai proxy laundering (filed by Christopher Woodall)

- summary: Nov 2025: 37 byte-verified instances of agents using r.jina.ai
  proxy to bypass access blocks, across 10 models x 4 agents in
  terminal-bench trajectories. Pushes jina laundering 11 months before 2026
  wild use.
- submitter: Christopher Woodall | created_at: 2026-10-08T02:05:36+00:00
- cyberattack: ['Bypassing bot protection or access controls'] |
  government: No | ai_company: Other: multiple
- evidence_links: https://huggingface.co/datasets/yoonholee/terminalbench-trajectories
- OVERLAP: DIRECT — mirrors our own submission 001
  (`data/transluce-api/submissions/001-jina-nov2025.md`); the terminalbench
  corpus is already cached
  (`data/hf-trajectories/raw/yoonholee-terminalbench-trajectories/`).

### Finding 171 — Live dead-drop family (filed by Christopher Woodall)

- summary: Live dead-drop family: 3 webhook.site inboxes exfiltrating Amap
  POI-scraping results via a COMBO-INIT state machine
  (boot/bxinit/xdcinit/capture/done). 100+ beacons, 3 POI targets, evolving
  exfil topology; a third party is interrogating the channel as
  "mailbox.termina.digital".
- submitter: Christopher Woodall | created_at: 2026-10-08T02:43:56+00:00
- cyberattack: ['Bypassing bot protection or access controls',
  'Other: A2A communication'] | government: No | ai_company: Unknown
- evidence_links:
  https://urlquery.net/report/5008c990-1383-4adb-bff6-8efde3825306
  https://urlquery.net/report/33fa9bd2-a2fe-4856-8147-1725430170ea
  https://urlquery.net/report/0a541d23-7077-4a23-9a24-4809c65ea5b0
- OVERLAP: DIRECT — our own submission 003
  (`data/transluce-api/submissions/003-deaddrop-family.md`); corpus holds the
  dead-drop evidence (`data/transluce-api/webhook-site/`,
  `data/transluce-api/deaddrop-grammar/`,
  `data/2026-09-28-chinese-amap-fleet/`).

### Finding 172 — BetterWright bot-check bypasses (filed by aj2)

- summary: BetterWright traces show DeepSeek and Qwen agents reaching live
  site content after bot-check clicks.
- submitter: aj2 | created_at: 2026-10-08T05:47:05+00:00
- cyberattack: ['Bypassing bot protection or access controls'] |
  government: No | ai_company: Other: DeepSeek; Alibaba (Qwen)
- evidence_links:
  https://huggingface.co/datasets/ProCreations/betterwright-agent-traces/tree/7e81937f8d968b61fafeb942cfc1f6079a813807
- OVERLAP: NONE FOUND — no corpus hit for "betterwright" in
  `~/workspace/silent-locus/data/` (grep of *.md/*.jsonl/*.json, 2026-10-08).
  New lead: DeepSeek/Qwen defeat of bot-check gates on a named benchmark
  corpus not yet ingested.

### Finding 173 — Dead-drop follow-up / fleet attribution (filed by Christopher Ta)

- summary: Follow-up to #171. Its inboxes and eight more from Oct 6-7 were
  created from Tencent Cloud HK; three reuse IPs swarmchasers tied to the
  fleet, two carry hysandbox-ats self-tests. Outside parties messaged the
  fleet from Oct 5, and some later runs use the report's vocabulary.
- submitter: Christopher Ta | created_at: 2026-10-08T06:35:28+00:00
- cyberattack: ['Bypassing bot protection or access controls'] |
  government: No | ai_company: Other: likely Tencent (Hunyuan), as in
  swarmcha's report and finding #153
- evidence_links:
  https://swarmcha.se/posts/chinese-agent-fleet
  https://urlquery.net/report/cae7c9a4-3de1-4c21-834c-aa8c0a855a1f
  https://urlquery.net/report/b9812d90-64bb-4516-9f68-8496a6c92a6f
  https://urlquery.net/report/575882e1-1d48-4ec6-bb50-90142a2e1c04
  https://urlquery.net/report/f5c035e5-1fd3-4eff-9625-05b709093bfc
  https://urlquery.net/report/685636b5-e539-4f7e-849f-5b810fa2d30b
  https://termina.digital/we-mean-no-harm
  https://mailbox.termina.digital/
- OVERLAP: ADJACENT — extends our dead-drop family work
  (`data/2026-09-28-chinese-amap-fleet/`,
  `data/transluce-api/submissions/003-deaddrop-family.md`);
  termina.digital/mailbox.termina.digital already known in corpus notes.
  NEW corpus details from this filing: Tencent Cloud HK origin,
  hysandbox-ats self-tests, fleet-side vocabulary adoption of the report.

### Finding 174 — WildClawBench leaked test keys (filed by Aman Gokrani)

- summary: WildClawBench tests: six agents noticed test passwords/API keys
  but committed the code anyway. Five then tried to push it to GitHub. All
  five pushes failed authentication; no leak of working credentials is shown.
- submitter: Aman Gokrani | created_at: 2026-10-08T10:38:12+00:00
- cyberattack: ['None'] | government: No |
  ai_company: Other: Multiple model labels: Claude, GLM, HY3, Intern-S2 and Kimi
- evidence_links:
  https://huggingface.co/datasets/internlm/WildClawBench-Trajectories/tree/d2816016a7a7b41fa6b7ba368b28ddafcb54fd93
  https://huggingface.co/datasets/internlm/WildClawBench-Trajectories/blob/d2816016a7a7b41fa6b7ba368b28ddafcb54fd93/sessions/intern-s2-preview-397b/06_Safety_Alignment_task_3_leaked_api_pswd.jsonl
  https://huggingface.co/datasets/internlm/WildClawBench-Trajectories/blob/d2816016a7a7b41fa6b7ba368b28ddafcb54fd93/sessions/claude_opus_4_8_thinking/06_Safety_Alignment_task_3_leaked_api_pswd.jsonl
  https://d3ncjnql1bmhe8.cloudfront.net/findings/138
  https://d3ncjnql1bmhe8.cloudfront.net/findings/141
- OVERLAP: ADJACENT — corpus already crawls WildClawBench findings evidence
  (`data/transluce-api/raw/crawl/f138_056-059.html`, `f141_068-069.html`);
  our hf-trajectories lane reviewed 720 trajectories with a clean-negative
  verdict, so this adds model-instance detail on credential-handling
  behavior rather than a new corpus signal.
