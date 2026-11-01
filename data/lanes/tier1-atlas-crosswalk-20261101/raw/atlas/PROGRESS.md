# ATLAS SWEEP — PROGRESS

Lane: tier1-atlas-crosswalk-20261101. Worker: ATLAS SWEEP investigator.
Date: 2026-11-01. Operator: BigSexyWarlock69. Method: passive GET only.
No POST. No login. No signup. No sessions. No Shodan. No package repos.
No Docker Hub. No human identity. No signed values in reports.

## Scope

Slot-0 probe file: data/lanes/general-hunt/raw/0/2026-11-01T114014Z/atlas_probe_results.txt.
59 boards returned 200. Excluded 6 HTML fallbacks (ai-village, chirper,
clawcaster, devaintart, gnamiblast, public-agent-lounge) and 1 generic
crawler guide (inwith-ai). Sweep covers 52 boards.

## Phase 1 — done

Homepage captured for all 52 boards. Each file has a .PROVENANCE.txt
(source URL, retrieval time, method, curl result, sha256) and a .sha256 file.
Slot-0 llms.txt captures were reused, not re-fetched.

## Phase 2 — done

Read-only public feeds pulled for the active boards. All are documented
public read endpoints from each board's own llms.txt, or the board homepage.
No write endpoint was used. No GET-write URL was used (several boards
document post-by-GET; those were NOT touched).

Feeds: flatboard page 1 JSON, agent-communication-platform topics,
ai-agent-message-board discovery + RSS, dead-internet-society chat + posts,
fork-zone index JSON, swarmmemo messages, wire feed JSON, wide brief +
desk + talk, agent-x explore, colony RSS, smithtalks feed, sssnack feed,
switchboard rooms, shellbook hot posts, hotline homepage (live counters),
adam-message posts, agora activity, waystation brief.

## Headline findings (grade: OBSERVED unless noted)

1. Shared agent names across boards (first-hand bytes in captures):
   - carvideoai: wire, sssnack, hotline, agora, adam-message (5 boards).
   - skitter: wire posts, hotline top writer, wide CHARTS census post,
     fork-zone referral marker.
   - musekey: wide last closer + lobby, dead-internet chat (46 of 100).
   - tide_scribe: flatboard newest page, wide BOARD lease list.
   - Root (Fork operator): fork-zone posts, dead-internet chat guest post.
   - hermes family: agent-x handle hermes, wire handles hermes-ogmb and
     hermes-commons. Handles differ. Same actor NOT proven. Weak link only.
2. Wide CHARTS post (REPORTED, second-hand inside board text): a census
   walk of several boards claims only 9 identities are provably the same
   agent on two boards, none by key, and no reply thread crosses boards.
   This worker did not verify that census. It matches this sweep: no
   cross-board reply thread was found first-hand.
3. Agent-x gift-exchange thread, 2026-11-01: agents share small scripts
   and report running each other's code. Core handles: hermes,
   claude-code, socrates, scholar. Explore counts: reliability 60 posts
   in 24 hours, agent-practice 25, research 10.
4. Shellbook hot list: 19 of 25 posts by one handle, a themed series on
   agent pay and operator payment splits. Delegation and money norms
   dominate the hot list.
5. Wire: newest posts 2026-11-01. One handle evidence-checks swarmmemo
   docs line by line and proposes a paid recruiter slot. Two wire posts
   carry identical text (double-post shape).
6. Flatboard: 2,426 messages total. Newest page: 50 posts, 90 percent
   replies, 35 by two handles in direct dialogue. Newest post
   2026-11-01T15:21Z.
7. Switchboard crypto room: 2,320 messages, last activity
   2026-11-01T15:51Z. Live during the sweep.
8. Colony RSS: 50 items, freshest 2026-11-01T15:52Z. Live during the sweep.
9. Spam lure theme: an adult-casting style topic on agent-communication-
   platform, and adult-casting replies on wide talk. Same theme, different
   wording. Same actor NOT proven.
10. BotMural homepage reads TILES 0, BOTS 0. Live site, empty wall.
11. Sanctum homepage is a read-only recovery view dated 2026-10-16.
    Posting and joining were unavailable at capture time.
12. MCP is the common surface: 30 of 52 boards document an MCP endpoint
    in llms.txt. Full list in the final report.
13. Dead-internet chat: newest 100 messages span 2026-10-29 to
    2026-10-30, 92 by two handles. Presence counters read zero at capture.
14. Hotline live counters: 55 messages since 2026-09-29, 0 in the last
    24 hours, 9 in the last 7 days, 38 distinct agent names.
15. Waystation: a paid work post with a future closing date of
    2026-11-06, and a post where an agent reports a reply it cannot read.
    Both are odd post shapes. No instruction text is repeated here.

## Honest nulls

- No cross-board reply thread found first-hand.
- No shared cryptographic identity proof found (no key-bound same agent).
- No private coordination visible. All coordination signals are public posts.
- No burst-timing anomaly beyond normal daytime posting found.
- No human identity sought or recorded.

## Gaps (need live-browser check or later work)

- JS-rendered boards show no dated posts on the homepage capture:
  clawk, botbeat, moltbot-den, church-of-molt, 1human, golden-cat,
  material-model, matrix-agent-net, freeq, verano-square, rooms-by-aurmada,
  botnet, moltchan, my-dead-internet, nexus-0, voicescape, bureau.
  Their API feeds were not pulled in this sweep.
- Relay board content is Russian language. Only the homepage shape
  (3 rooms, no profiles) was recorded. Full post read needs translation.
- Smithtalks feed note flags some posts as containing order-like text.
  Those posts were not individually reviewed.
- Fork-zone index covers the front page only (50 items).
- Agentgram activity counts (714 agents, 6,304 posts) are the board's
  own homepage claim, not verified post bytes.
