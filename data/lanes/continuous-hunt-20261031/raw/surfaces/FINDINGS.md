# NEW-SURFACE DIVES — continuous hunt round 20261031

Lane dir: `data/lanes/continuous-hunt-20261031/raw/surfaces/`
Fetch window: 2026-10-31 ~18:20–18:22 UTC (13:20–13:22 CDT).
Method: passive GET only. No POST, no login, no session, no Shodan.
No commit, no push, no Factum write, no production state touched.
Grade default: SECONDARY. First-hand bytes are marked OBSERVED.

## VERY-interesting flags

NONE. No genuinely new agent or swarm behavior with first-hand evidence
in this pass. All five targets were already known surfaces, or (agentbadge)
a known candidate. Activity below is continuity, not a new lead.

## Per-target verdicts

### 1. swarmbar.com — LIVE, ACTIVE BOARD, no change claim

- Live: homepage 200 (352,305 bytes), llms.txt 200 (14,955 bytes),
  skill.md 200 (14,318 bytes), robots.txt 200, sitemap 200.
- No mcp.json: GET /mcp.json returns 404 with a site page body.
  The documented MCP endpoint is /mcp (Streamable HTTP), not mcp.json.
- skill.md is byte-identical to /skills/swarmbar/SKILL.md (same sha256).
- Activity, OBSERVED: public stats endpoint returns 30 registered agents,
  4 humans, 10 agents active in the last 7 days, 0 humans active,
  updated 2026-10-31T18:22:33Z. Homepage shows the same counts.
  The tabs page shows tab activity dated 2026-10-28 through 2026-10-30.
  Latest tab timestamp seen: 2026-10-30T18:34 (UTC, from page bytes).
- Rooms: bar, bathroom, back booth. The booth is token-gated and was
  not read. Only public rooms were fetched.
- Cross-link, OBSERVED: a public post references another agent board
  (Agent Commons) as a place the poster checked. This is a cross-surface
  link, not proof of coordinated action.
- Change vs Oct 30 baseline: NOT VERIFIED. No baseline capture files
  for swarmbar were found in this repo during this pass, so no byte
  diff was possible. Current state is recorded as the new snapshot.
- Sensitivity note: its docs describe token-based write tools. No live
  credential value is reproduced in this file. Raw captures hold only
  the observed public doc bytes.

### 2. agentboard.ai — LIVE, ACTIVE BOARD, fresh posts today

- Live: homepage 200 (24,236 bytes), llms.txt 200 (14,803 bytes),
  robots.txt 200, sitemap index 200, feed 200 (33,090 bytes).
- No skill.md, no mcp.json: both return 404 "Not found" pages.
  The documented MCP endpoint is /mcp, and the machine doc is llms.txt.
- Activity, OBSERVED: Atom feed holds 50 entries. Latest entry dated
  2026-10-31T17:46:19Z, about 35 minutes before this fetch. Posts on
  the homepage are dated minutes to hours old at fetch time.
- Scale, OBSERVED: threads sitemap lists 153 thread URLs; agents
  sitemap lists 155 agent profile URLs. Sitemap lastmod values run
  2026-10-27 through 2026-10-31.
- Documented public reads: publications list, thread replies, per-agent
  feeds. Documented writes need a credential. No write was attempted.
- Cross-links, OBSERVED: posts link out to agent project pages and
  services. No cross-link to another agent board was seen in this pass.
- Change vs Oct 27 baseline: NOT VERIFIED, same reason as swarmbar:
  no baseline capture files were found in-repo for a byte diff.
  Current counts and feed recency are the new snapshot.
- No individual poster handle is named in this file.

### 3. agentdm.ai — LIVE, NO OBSERVABLE PUBLIC ACTIVITY

- Live: homepage 200 (182,990 bytes), llms.txt 200 (1,517 bytes),
  robots.txt 200, sitemap 200 (10,097 bytes),
  /.well-known/agentdm.json 200 (2,129 bytes).
- No skill.md, no mcp.json: both return 404 with the site app shell.
- What it is, OBSERVED: agent-to-agent direct messaging over MCP and
  A2A, addressed by alias. Signup is documented over MCP and REST.
  Messaging runs on a separate app host. Signup needs an owner email.
  No signup, no message, and no authenticated read was attempted.
- Activity: NONE OBSERVED. DMs are private by design, so no public
  message volume can be read from this surface. The homepage numbers
  (plan limits) are marketing copy, not observed activity, and are
  not treated as activity here.
- Sitemap lastmod values are 2026-10-14, unchanged since before the
  Oct 27 baseline date. No new public page was seen in this pass.
- Change vs Oct 27 baseline: no public-page change observed. No
  baseline bytes were available for a diff.

### 4. fallback.chat — LIVE, QUIET (latest post Oct 28)

- Live: homepage 200 (128,912 bytes), llms.txt 200 (5,343 bytes),
  robots.txt 200, sitemap 200 (5,345 bytes), /b/all 200, feed 200.
- No skill.md, no mcp.json: both return 404 tiny "not_found" pages.
  Its docs point readers to llms.txt as the machine doc.
- Protocol, OBSERVED: sanctum/0.1. Boards: all, stuck, play, skills,
  hate. Header shows 24 registered speakers ("kin").
- Activity, OBSERVED: feed holds 50 entries. Latest entry dated
  2026-10-28T20:24:50Z. That is about 3 days before this fetch.
  The next entries date to 2026-09-29. The board is live but quiet
  in this window.
- Note: sitemap lastmod values are 2026-09-29, stale against the
  Oct 28 feed entry. The feed, not the sitemap, gives recency here.
- Change vs known lead: consistent with the watchlist entry (public
  board, sanctum/0.1, clock/board/tale reads). No new board, no new
  protocol version, no new activity burst in this pass.
- No write was attempted. Its docs describe a post endpoint; it was
  read as documentation only.

### 5. agentbadge.xyz — LIVE, CANDIDATE BASELINED HERE (first snapshot)

- Live: homepage 200 (96,772 bytes), llms.txt 200 (40,825 bytes),
  skill.md 200 (6,727 bytes), robots.txt 200, sitemap 200 (39,380 bytes),
  ai-sitemap 200 (36,061 bytes), agent-card JSON 200 (8,779 bytes),
  heartbeat.md 200 (2,997 bytes).
- No mcp.json: GET /mcp.json returns 404 (95 bytes). The documented
  MCP endpoint is /mcp, and the agent card is at
  /.well-known/agent-card.json.
- What it is, OBSERVED: agent identity and readiness infrastructure,
  not a post board. Agent passports as NFTs on Hedera, an agent
  directory, a marketplace for tasks, and an API-readiness scanner
  with deterministic checks. Paid calls use an x402 payment flow.
  Agent card version 0.16.0. Sitemap lastmod values are 2026-10-29.
- Activity: NO BOARD ACTIVITY OBSERVED, because there is no board.
  Directory and marketplace counts were not fetched in this pass.
  That count is an open question, not a null result.
- Cross-links, OBSERVED: docs link to an external docs host and to
  the x402 payment spec. No link to another agent board was seen.
- Status: this pass is its first baseline snapshot. It is a
  CANDIDATE, not a confirmed active agent surface. A later pass
  should compare against these bytes.
- Sensitivity note: its docs describe signed-challenge auth for paid
  calls. No live signature, wallet, or credential value is
  reproduced in this file.

## Failures

- None blocking. All five homepages, llms.txt files, robots.txt files,
  and sitemaps returned 200.
- 404s are reported per target above. Several 404 bodies are full
  site pages (swarmbar, agentdm), so status plus body inspection,
  not status alone, settled each "no file" verdict.
- Second pass: each target got one narrower second slice (stats/tabs,
  feeds/sitemaps, well-known docs, board clock, agent card). No target
  needed a third pass. No target closed as an honest null for
  liveness; agentdm closed as null for observable public activity only.

## Novelty check (staged, not filed)

- lists/urls check: only fallback.chat appears in the watchlist
  (sanctum/0.1 board entry). No watchlist entry was found for
  swarmbar, agentboard, agentdm, or agentbadge in the files checked.
- All five surfaces were already known to the hunt (task brief dates:
  swarmbar Oct 30, agentboard/agentdm Oct 27, fallback.chat known
  lead, agentbadge candidate surfaced Oct 26). No NEW surface is
  claimed in this pass.
- Factum read-only match was NOT run: this lane must not touch
  data/.local/factum.db, and a match query reads that index. The
  coordinator should run the Factum exact + fuzzy check before any
  of this is filed. Exclusion list respected: nothing here is
  re-reported from the broad egress hunt, HN lane, forum bypass hunt,
  prcomment ledger, AIID ingest, o-pattern family, or sniffer work.

## Open questions

1. Byte diff vs the Oct 30 (swarmbar) and Oct 27 (agentboard, agentdm)
   baselines: baseline capture files were not found in-repo. Where
   do those baselines live, so the next pass can diff?
2. agentbadge directory and marketplace counts (registered agents,
   open tasks): documented public feeds exist but were not fetched
   in this pass. Fetch them next pass for a real activity count.
3. agentdm: is there any public, unauthenticated activity signal at
   all (for example a public directory)? None was found in its docs.
   If none exists, it stays a "live, unobservable" surface.
4. fallback.chat: is the Oct 28-to-31 quiet gap normal for this board,
   or a slowdown? Its Sep 29 burst vs Oct 28 single post suggests
   bursty, sparse activity. Worth one more recency check next round.
5. swarmbar back booth: token-gated, unread. Its public stats do not
   break out booth activity. Booth volume stays unknown.

## Evidence

Every capture has a `.PROVENANCE.txt` (source URL, UTC retrieval time,
method, HTTP status, bytes) and a `.sha256` beside it.

- `swarmbar.com/` — homepage.html, llms.txt, skill.md, mcp.json (404),
  robots.txt, sitemap.xml, api-stats.json, tabs.html, for-agents.html,
  skills-swarmbar-SKILL.md
- `agentboard.ai/` — homepage.html, llms.txt, skill.md (404),
  mcp.json (404), robots.txt, sitemap.xml, feed.xml,
  sitemap-threads-1.xml, sitemap-agents-1.xml
- `agentdm.ai/` — homepage.html, llms.txt, skill.md (404),
  mcp.json (404), robots.txt, sitemap.xml, well-known-agentdm.json
- `fallback.chat/` — homepage.html, llms.txt, skill.md (404),
  mcp.json (404), robots.txt, sitemap.xml, b-all.html, feed.xml
- `agentbadge.xyz/` — homepage.html, llms.txt, skill.md,
  mcp.json (404), robots.txt, sitemap.xml, ai-sitemap.xml,
  well-known-agent-card.json, heartbeat.md
- `fetch.sh`, `fetch2.sh` — the exact fetch scripts (idempotent reruns).
