# dream-lane: verdicts per Dream-swarm grammar marker

Date: 2026-10-04 (CDT). Verdicts: LIVE / reporting-only / noise / inconclusive.
Nothing below is a live hit. One lead (MODA date mismatch) stays open.

## Marker verdicts

| Marker | Surface | Verdict | Evidence |
|---|---|---|---|
| `agent-a` | urlquery htmx | **noise** | 11 reports, all generic sites (rundown.ai, wormgpt.ai, ahrefs traffic-checker, medium, vimeo...); tag/substring matches, no swarm grammar. dream-uq-01-agent-a.json |
| `agent-b` / `agent-c` | urlquery htmx | **inconclusive** | HTTPS-tunnel timeouts; files carry {"query","error"} only. NOT honest zeros. |
| `wave-1` / `wave1` | urlquery htmx | **inconclusive** | Transport failures, same as above. |
| `attack wave` | urlquery htmx | **inconclusive** | Transport failures. |
| `openclaw` / `hermes` / `deepseek` / `gov.tw` / `pentest` | urlquery htmx | **inconclusive** | Transport failures; retry job killed when whole-VM egress (even example.com) went down. Re-run when egress recovers. |
| same terms as `task.url:*...*` | urlscan.io API | **not run** | urlscan.io unreachable from this VM (urllib + curl timeouts). |
| `Agent A`–`Agent Q` lettered sub-agents | GitHub code / web | **reporting-only + noise** | Only in (a) Dream's own report ("up to 8 lettered sub-agents in parallel per wave (Agent A through Agent Q observed across the campaign)") and (b) generic agent-framework documentation: OpenAI Swarm README example names its demo agents "Agent A"/"Agent B"; OpenClaw/cline/orchestration skills use the same convention. Not live reuse — it's the default naming grammar of the frameworks themselves, which is likely WHY the swarm's self-labeling looks that way. |
| numbered `wave` in agent configs | GitHub code / web | **noise** | All hits benign project-management usage: pentest-swarm-ai roadmap (Burp bridge "Wave 2", Metasploit adapters "Wave 2"), WeChat campaign "Wave 1/2/3" analyst phases, yuri-os fix-queue handoffs, halbert "WAVE 1 DISPATCHED" executor batches. No attack-wave numbering outside Dream reporting. |
| "authorized penetration test" framing in prompts/configs | GitHub code | **noise** | Found in legitimate pentest tooling: stefanoratto/team7-hermes SKILL.md ("I'm conducting an authorized penetration test focused on SSRF"), strategic-automation/violin Hermes pentest profile ("Run an authorized penetration test against example.com"; requires written authorization), kali-pentest forks ("I have authorization" boilerplate), skillsmp web-pentest skill (authorization acknowledgement flow). The phrase is generic pentest-skill boilerplate → WEAK as a live-swarm marker. Do not treat new "authorized pentest" prompt hits as Dream-tooling evidence without more. |
| 160MB / 1,395-file operator archive mirrors | web | **reporting-only** | No mirror or re-post found; only Dream's report and report mirrors (wesearch.press). |
| new Taiwan-gov AI-agent incidents (Sep–Oct 2026) | news | **reporting-only** | All coverage loops back to the Jul 1–4 / Aug 12 disclosure. No second incident reported. |
| copycat wave-numbered attacks | web | **noise** | No hits; "swarm is here" content is influence-ops theory, not operational reuse. |

## Lead (not a negative — follow up, do not file)

**MODA date mismatch.** Taiwan's Ministry of Digital Affairs confirmed OpenClaw-based attacks but said the activity **it observed began July 20**, not Jul 1–4. Either (a) continued operations after Dream's window, (b) a second wave with the same tooling, or (c) a different incident folded into the same story. Source: medium.com/@JulienNauy article citing Reuters Aug 13, 2026. Follow-up: MODA monthly cybersecurity report (moda.gov.tw/en/press/monthly-report/).

## Context (same tooling family, distinct incidents — do not conflate)

- **Unit 42**: Chinese-speaking actor used DeepSeek + Hermes Agent to autonomously attack exposed servers in Asia (Tomcat, NetScaler, Langflow, Marimo) — 460+ targets, 3 confirmed. Same framework pairing, different target set/timing.
- **Thailand Ministry of Finance (Jul 9–13, 2026)**: Hermes-based, operator ran assistant with approval disabled; distinct country, window, and recovery vector (attacker's staging server). Dream report explicitly distinguishes these.
- **JADEPUFFER** and **Mexico government** incidents (per vibe-coding-security repo): different tooling/framing.

## Bottom line

The Dream swarm's distinctive grammar — lettered Agent A–Q sub-agents, numbered attack waves with after-action feedback loops — appears NOWHERE outside incident reporting in the surfaces reachable this session (web, news, GitHub via search). No live reuse detected. Caveat: the urlquery/urlscan scan-activity lanes degraded on egress; treat the `gov.tw`/pentest/urlscan markers as uncovered, not negative.
