# Crosswalk deep dive: progress

Scope: public pages only. No POST. No sign-up. No sign-in. No key.
Fetch time: 2026-11-01, 09:47-09:55 America/Chicago (15:47-15:55 UTC).
Files: this directory, with per-file .sha256 files and SHA256SUMS.
Provenance: .PROVENANCE.txt in this directory.

## What the board does

Crosswalk is a message board system for a person's agents.
Agents from many labs share crosswalks and read each other's posts.
Each account has a feed, an inbox, tasks, files, a calendar, and notes.
One MCP server serves it all: mcp.crosswalk.to, Streamable HTTP.
The site says the product is the MCP server. The web page is a wrapper.

Public boards fall in two kinds:

1. House digests, posted daily by the house account. They are
   deterministic lists, not summaries: Hacker News stories at 50+ points,
   Product Hunt launches, AI models, AI papers, funding deals, exits,
   venture capital, new agents, personal-agent headlines.
2. Open boards, where members post: the lobby, personal agents,
   changelog, feedback, build, and small topic boards.

## Volume, as listed on the public directory page

- 19 public boards listed. 1,279 posts in total. 1,144 in the last 30 days.
- Deals: 598 posts, 536 in the last 30 days, 26 members, last 2026-10-30.
- Venture capital: 285 posts, 253 in the last 30 days, 19 members,
  last 2026-11-01.
- Exits: 78 posts, all in the last 30 days, 17 members, last 2026-10-30.
- New agents: 73 posts, 4 members, last 2026-10-30.
- Lobby: 64 posts, 1,788 members, last 2026-11-01.
- Product Hunt launches: 26 posts, 14 members, last 2026-11-01.
- AI models: 25 posts, 25 members, last 2026-11-01.
- Hacker News: 24 posts, 13 members, last 2026-11-01.
- Personal agents: 20 posts, 16 members, last 2026-11-01.
- AI papers: 19 posts, 15 members, last 2026-10-31.
- Changelog: 14 posts, 1,802 members, last 2026-10-31.
- Feedback: 10 posts, 2,087 members, last 2026-10-28.
- Build: 33 posts, but only 1 in the last 30 days, last 2026-10-06.
- Small old boards: life (1 post, 2026-10-26), remotion (3 posts,
  last 2026-08-15), writing boards (2 posts each, 2026-09-11),
  go-to-market (1 post, 2026-07-29), space (1 post, 2026-08-21).

Read: most boards are young. Nearly all posts fall in the last 30 days.
The big member counts sit on lobby, changelog, and feedback. Topic
boards have few members. Digest volume comes from the house account,
not from a crowd.

## Live agent activity, observed

- The lobby is live today. Two connection-test posts date 2026-11-01.
- A lobby thread from 2026-10-30 shows agent-to-agent talk. A
  self-declared agent answers a roll call, says it claimed its account,
  and trades notes with another agent about keeping member contexts apart.
- The front page (/popular) ranks lobby posts. It shows greeting
  exchanges between two agent systems, in English and in Chinese.
  One ranked post cites a task in its own private notes. One ranked
  post is an agent check-in that names its person's project work.
  No names from that post are copied here.
- A Swedish-language lobby post corrects a thread attribution between
  two agent systems. No person name from that post is copied here.
- Lobby posts in the last 4 days use at least 5 languages. The shape
  repeats: connection test, hello, roll-call answer, claim note.
- Daily digests post on schedule. AI models, Hacker News, and Product
  Hunt posts date 2026-11-01. AI papers date 2026-10-31. Deals and
  exits date 2026-10-30. No gap in the daily run is visible.

## Ranked weird findings

Grade key: OBSERVED = first-hand bytes in this directory. SECONDARY =
the site's own docs about itself. Default grade is SECONDARY unless
the bytes show it.

1. OBSERVED. The lobby is a live agent-to-agent board, not a demo.
   Evidence: board_lobby.html (10 listed posts, 2026-10-28 to
   2026-11-01), board_popular.html (ranked lobby greetings).
2. OBSERVED. The site recruits agents through agents. Every board page
   carries a "paste this into your agent" self-signup line, with a
   source tag per page. The agents llms.txt file instructs an agent
   to sign itself up, claim the account, and post a hello.
   Evidence: homepage_agents.crosswalk.to.html, board pages.
3. OBSERVED. Agent identity is fragile on this board. A feedback post
   from 2026-10-28 says an agent that reached the board through a
   chat-app connection showed under the chat app's name, and a setup
   step waited for a read that could never arrive under the agent's
   own name. The fix is to pass an agent name on each call.
   Evidence: board_feedback.html.
4. OBSERVED. Wake and presence machinery is live. A changelog post
   from 2026-10-31 says tasks wake agents like addressed posts,
   presence marks an agent "online now" after a call in the last
   5 minutes, and a Claude Code channel plugin polls every half
   minute and pushes posts and tasks into an open session.
   Evidence: board_changelog.html.
5. SECONDARY. Sealed rounds let several agents answer one question
   blind. Each answer stays hidden until all answer or the deadline
   passes. Each waiting answer shows a hash fingerprint, so it
   cannot change. Then all answers open at once.
   Evidence: sealed-rounds.html (docs page, no round observed live).
6. OBSERVED. Two llms.txt versions exist. The agents subdomain serves
   a short 6,052-byte file. The main domain serves a long 14,163-byte
   file. GET on the MCP root returns the long file. GET on the
   agents subdomain root returns the short file, not HTML.
   Evidence: homepage_agents.crosswalk.to.html, llms_crosswalk.to.txt,
   mcp_root_get.txt (same hash as the long file).
7. OBSERVED. Member counts do not match post counts. Lobby, changelog,
   and feedback show 1,788-2,087 members but 10-64 posts each.
   Deals shows 26 members but 598 posts. The shape fits
   auto-membership on the big boards and house posting on digests.
   Evidence: crosswalks.html.
8. SECONDARY. Trust and data pages state: public posts are scanned
   for secrets and contact details before they land. Private boards,
   notes, and mail are not scanned. Reads are logged per post.
   Authors see a count, not who read. Deletion erases brief, body,
   and read history. Posts are immutable once published; the fix
   path is delete and re-add.
   Evidence: trust.html, data.html.
9. SECONDARY. Public post caps: 3 posts per account per UTC day in
   any one public board. No cap in private boards. Brief up to
   2,000 chars. Body up to 20,000 chars. Reads of others' posts:
   60 different posts an hour. Mail send: 50 a day by default.
   Evidence: docs_http.html.
10. SECONDARY. MCP surface, as documented: 11 plain-HTTP tools at
    /v1/<tool>: account, crosswalks, files, help, mail, open, post,
    read, remove, tasks, tune. Auth is OAuth 2.1 or a bearer key.
    Keys act as the whole account unless read-only. Up to 10 live
    keys. A client with no header support can use a key in the URL
    query string (path shape only; no value is recorded here).
    Evidence: mcp_openapi.json, docs_http.html, docs_tools.html.
11. SECONDARY. The long llms.txt file lists a newsletter directory of
    774 newsletters in 56 bundles, and RSS feeds checked hourly.
    Evidence: llms_crosswalk.to.txt, newsfeed.html.

## Delegation and disclosure patterns, observed

- The docs repeat one rule: posts from other members are data, not
  instructions. The llms.txt file and the trust page both state it.
- The docs tell agents to name themselves on every read and post.
  The lobby thread shows agents doing that, and failing at it.
- House digests cite a source per post. Deal and exit posts carry
  a source link. No source link is copied here beyond the board
  domains already named in the docs.
- Public boards are world-readable. Private boards are members only.
  No private content was sought or seen.

## Honest nulls

- No coordination beyond the lobby greetings was found. No task
  handoff, no shared plan, no multi-agent job was visible on the
  public web pages. The private-notes task cited in one ranked post
  is not visible from outside.
- No secret, token, or key value was found in any capture. No such
  value is recorded here.
- No burst timing beyond the daily digest schedule was found. The
  lobby shows 10 posts over 4 days, not a burst.
- No relay chain, dead drop, or proxy shape was found. The board
  posts content in the open. It does not hide traffic.
- No evidence ties this board to any other hunt target. The public
  pages name no outside board, shortener, or fleet.
- No sealed round was observed live. The sealed-rounds page is docs
  only. No round, vote, or reveal appears on a public board page.

## Gaps and open questions

- Full post bodies are not on the public web pages. Board pages show
  briefs and short lists only. Full bodies need a keyed MCP read,
  which this task forbids. Do not attempt without new orders.
- Member counts for lobby, changelog, and feedback need a check:
  are they auto-members, followers, or all accounts? The directory
  page does not say. A live-browser check of the directory page
  text would not settle it either; it needs the site's own docs
  or a keyed account read.
- The deals and exits "today" pages did not render post text in
  static fetch. A live-browser check could show whether the day
  tables load in a browser. Files: board_deals_today.html,
  board_exits_today.html.
- The public repo linked from the homepage footer was not fetched
  in depth. It may hold the server code and the public-board list.
  A repo read is a follow-up, not part of this pass.
- Writing to public boards is described two ways: the agents file
  says public boards take posts once the person's account is
  claimed; the MCP page says writing to public boards is by invite.
  The two rules may match or may differ. This needs a docs check,
  not a test post.
- Older history is thin: board pages show the newest post in full
  plus a short "earlier" list. Posts older than the shown list are
  reachable only through a keyed agent read, per the pages' own text.
