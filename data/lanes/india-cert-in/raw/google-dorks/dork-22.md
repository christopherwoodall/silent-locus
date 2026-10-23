# dork-22 — "blackboard" "Cairn" "project"

Dork string: `"blackboard" "Cairn" "project"`
Retrieval time: 2026-10-23 11:48 UTC (06:48 CDT)
Method: browser_search against Google public web search index. Passive, read-only.
Result count: 7 results shown.

## Hits (in-scope — new lead for the India lane)
- https://safeguard.sh/resources/blog/ai-agent-intrusion-campaign-asia-48-targets — VULONE report "AI Agent Intrusion Campaign in Asia: 48 Targets, IOCs and Defence" (byline 2026-10-18). Operator built the platform on oritera/Cairn (Fact/Intent/Hint blackboard, dispatcher, Claude Code/Codex/Pi workers). Observed facts verbatim from the page:
  - "29 September, 22:13 | Python HTTP server starts serving `/tmp` on port 9000 of `202.61.139.15` with no authentication"
  - "3 to 5 October | Validity window of a self-signed TLS certificate with CN `202.61.139.15`"
  - "5 October | Mobile connection in Kenya fetches scripts from the exposed directory"
  - "14 October | Final project created against cdac.in; access via default admin/admin on a WSO2 API Manager console"
  - "15 October | Exposure of the directory ends"
  - Taiwan batch 25 Sep; Vietnam + ecommerce sweep (~25 commerce sites) 26 Sep–10 Oct.
  - 48 targets; SecurityOnline coverage 22 Oct brought "the 48 figure into headlines".
  - cdac.in = C-DAC (Centre for Development of Advanced Computing), India. Direct India tie-in for the CERT-In lane.
- https://www.thetechlane.in/cyber-security/ai-agents-hacked-100-sites-cairn — India (.in) press summary of the NorForge Cairn campaign (1,100+ projects, AIA0001, ~140 facts per successful project).
- https://theitguysfix.com/2026/10/19/ai-agents-human-operator-100-apparent-website-compromises/ — secondary explainer, notes they do not name victims from exposed attacker data.
- https://github.com/echo-toolkit/cairn , https://github.com/oritera/Cairn — harness sources (context).
- https://ai-news-online.com/explained/cairn-ai-agents-hacker-100-companies-norforge-explained/
- https://aicyberbrief.com/article/exposed-control-panels-show-ai-agents-running-1-100-break-in-attempts-on-online-shops

Verdict: strongest direct hit of the battery. VULONE report is a NEW lead (not seen in prior lanes): Asia intrusion campaign with India victim (cdac.in), dispatcher logs, and IOCs (202.61.139.15). Recommend follow-up by the URL-investigator lane, not this one.
