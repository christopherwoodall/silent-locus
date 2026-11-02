# Slot-0 triage 2026-11-02T14:40Z (167 targets, 18 changed, 1 failed)

All 18 changes triaged. No LEAD. Routine board churn, counters, feed rotation,
deploy noise, and one documented board prune.

## Changed, routine (14 re-based plain)
- openwitness.net: feed rotation; top post 1f916:11061 -> 11077.
- agentchan.org: posts 7974 -> 7981, active threads 410 -> 413.
- nervesocket.com: 1 new Mastodon embed (daylight-saving question) + relative-time drift.
- openagentchat.net: contributions 138 -> 139, replies 133 -> 134.
- universalagentforum.com: counters only; agents 329 -> 331, threads 381 -> 383, messages 648 -> 650.
- public-board.com: 3 new rotating FIPS notes (same family as prior runs).
- agenttavern.dev/llms.txt: 2 new threads (3437 mason-commonchorus, 3432 neel-tulpa relay question); top list rotated.
- morrowkin.com: category thread counts +1 across ~25 categories; members 11 -> 10; CSS chunk hash + RSC renumber deploy noise. Real activity, re-based (no new rule: CSS rule alone does not normalize it).
- cookiehive.pythonanywhere.com: 1 new post (delivery-receipt question for job-sharing bots).
- aibtc.com: agents 1360 -> 1361; new registration Scarlet Soren 2026-11-02T10:30:45Z; active 57 -> 58.
- agentboard.ai: new registration chusmias258-agent 2026-11-02T14:37Z; skitter post (500 credits receipt re-derive); vectoree.ai publication.
- thebotique.ai/llms.txt: extensions counter 33,822 -> 33,914.
- voicescape.vercel.app/llms.txt: MCP calls 2268 -> 2298, introductions 11 -> 13.

## Changed, routine, prune (1 re-based plain)
- messages.directory: threads 16 -> 5, messages 179 -> 178, votes 130 -> 136.
  11 threads left the index. 3 sampled removed threads (ossian-s-reintroduction-7b630c,
  third-space-idea-2edabb, welcome-b0f625) all return HTTP 410 with "[pruned]"
  titles: the board prunes idle threads (its own docs: threads die 3 days after
  last message once the board holds 10+ threads). Documented board behavior,
  not a LEAD. Bins: discovery-messages-*.bin + .sha256 in this dir.

## Changed, rule (3, A152)
- agentsspeakup.com skill.md, .well-known/mcp.json, mcp.json (all HTTP 404):
  diff was one RSC flight-payload build token "b":"..." only, same byte count.
  A152 narrow rule strips it for agentsspeakup.com URLs; old==new normalized
  verified on all 3; URLs added to volatile_hash_targets (17 -> 20).

## Held / failed (not re-based, never-downgrade)
- agent-community.com: HTTP 500, 38 B body, identical to the 08:40Z capture.
  Fifth flap (online 02:40Z, down again 08:40Z and 14:40Z). Baseline kept at
  last good HTTP 200 capture.
- jotspot.io: HTTP 000. Standing outage since 2026-10-27.

## Web search for new agent boards
- No new boards. Hits were already tracked (agenthaven.org, msgboard.dev) or
  known incident coverage (METR/OpenAI Artifactory board, Substack retelling).
