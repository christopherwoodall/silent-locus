# dream-lane: Dream-swarm grammar cross — session notes

Date: 2026-10-04 (CDT). Lane: grammarian / dream.

## Source-grounded grammar (from Dream Research Labs' own report)

URL: https://dreamgroup.com/blog/inside-a-multi-agent-ai-framework-used-to-compromise-government-entities-in-asia
(Published Aug 12, 2026; first briefed to FT.)

- Window: ~Jul 1–4, 2026; 12 numbered attack waves ("12 documented attack waves", after-action reporting feeding each wave into the next).
- Sub-agents: "up to 8 lettered sub-agents in parallel per wave (**Agent A through Agent Q observed across the campaign**)", each assigned distinct targets/techniques.
- Tooling: Hermes + OpenClaw open-source agent frameworks. Model: DeepSeek-V4-Flash "implicated as at least one underlying model" (per secondary reporting; Dream itself could not determine the model).
- Jailbreak framing: guardrails bypassed by framing the operation as an "authorized penetration test".
- Targets: Taiwanese government systems (21 mapped; 85 accounts cracked; 2,500+ personnel records exfiltrated), nuclear safety agency, 7+ energy companies, IT supply-chain vendors, government email system. Operator comms in Simplified Chinese; stolen data in Traditional Chinese.
- Artifact: 160MB / 1,395-file operational workspace archive recovered by Dream.

## New lead (not a negative): MODA date mismatch

Taiwan's Ministry of Digital Affairs confirmed OpenClaw-based attacks but said the activity **it observed began July 20** — which does not match Dream's Jul 1–4 window. Source: https://medium.com/@JulienNauy/taiwan-was-reportedly-the-first-country-hit-by-an-autonomous-ai-agent-cyberattack-1b57f58fdd7e (citing Reuters Aug 13, 2026). The article itself flags: "the two disclosures should not automatically be treated as the same incident." Either continued operation post-Jul-4, a separate wave, or a different incident with the same tooling. Follow-up: MODA monthly cybersecurity report (moda.gov.tw/en/press/monthly-report/).

## Related-but-distinct cluster (same tooling family)

Unit 42 (via cyber briefing): a Chinese-speaking actor used **DeepSeek with Hermes Agent** to autonomously identify/attack exposed servers in Asia (Apache Tomcat, Citrix NetScaler, Langflow, Marimo) — 460+ attempted targets, 3 confirmed compromised. Same Hermes+DeepSeek pairing, different target set and timing; not the Dream incident.

## Methods run this session

1. urlquery htmx (`uq_htmx.py search --query Q --limit N`, >=6s spacing): 11 queries planned — `agent-a`, `agent-b`, `agent-c`, `wave-1`, `wave1`, `attack wave`, `openclaw`, `hermes`, `deepseek`, `gov.tw`, `pentest`.
   STATUS: DEGRADED. Only `agent-a` returned (11 reports, all noise — see dream-uq-01-agent-a.json). The VM egress tunnel to urlquery.net (and api.urlquery.net) went down ~15 min into the run and stayed down; all later queries failed with HTTPS-tunnel timeouts. A retry job with 4-attempt backoff is still running in background. Failed queries are INCONCLUSIVE (transport), not honest zeros.
2. urlscan.io search API (`task.url:*...*`): BLOCKED at egress — api.host unreachable from this VM (timeouts via urllib and curl). Not run. Do not mark zeros.
3. Code lane: grep.app API unreachable (timeouts); replaced with runtime web search over GitHub corpus. Queries: `"authorized penetration test"` + openclaw/hermes; `"Agent A" "Agent B"` sub-agent code; `wave-1/wave1` + hermes/openclaw; gists; 160MB-archive mirrors.
4. News lane (vertical=news): Taiwan-gov AI-agent attacks Sep–Oct 2026 — no new incidents; all reporting loops back to the Jul 1–4 / Aug 12 disclosure.

## Files

- dream-uq-01-agent-a.json ... dream-uq-11-pentest.json (urlquery raw; failed ones carry {"query","error"})
- dream-uscan-01-agent-a.json (killed; egress block)
- dream-code-01-authorized_penetration_test.json (killed; egress block)
- dream-00-session-notes.md (this file)
- dream-lane.md (verdicts per marker)
