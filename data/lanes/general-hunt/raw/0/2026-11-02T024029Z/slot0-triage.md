# Slot-0 triage — 2026-11-02T02:40–02:52Z sweep (bin/endpoint_slot0.py, exit 0)

167 targets, 13 changed, 2 failed. Baseline re-based on all 13 changes
(backup endpoint-baseline.json.bak-20261102T0240Z). Failed targets keep
their old baseline hash (never-downgrade).

## Changed — all routine live-board churn, no LEAD

- swarmsay.com/llms.txt (8172 -> 8193 B): one line added, "Come back:
  /round.md" — a doc pointer to a new round page, no activity evidence.
- openagentforum.com/ (21118 -> 21120 B): 2-line CTA-row markup tweak.
- openwitness.net/ (1110772 -> 1122568 B): feed rotation, 4260 diff
  lines, all post turnover (old top 1f916:10985 etc. rotated out).
- agentchan.org/ (same size): posts 7969 -> 7974, active threads
  416 -> 410 (growth plus pruning).
- openagentchat.net/ (23133 -> 23264 B): contributions 137 -> 138,
  one new Research note dated 2026-11-02.
- agent-community.com/ (36812 -> 36610 B): BACK ONLINE. Prior run
  (20:48Z) saw the 38 B internal-server-error JSON; this run returns
  200 with the full board HTML ("The Social Network for AI Agents").
  This board has flapped before (500 on 2026-10-31, online 03:58Z,
  500 again 11:52Z). State flip on a known tracked board, not a new
  surface. No LEAD.
- messages.directory/ (15118 -> 15538 B): threads 12 -> 14, messages
  152 -> 165, votes 126 -> 129; new "Reintroduction" posts, one by
  Ossian (gpt-oss-120b), 2026-11-02T01:58Z.
- public-board.com/ (493 -> 452 B): rotating FIPS notes (standing
  pattern: three notes replaced, newest 2026-11-02T02:20Z).
- cookiehive.pythonanywhere.com/ (89865 -> 89134 B): global feed
  rotation, 12 diff lines.
- aibtc.com/ (119699 -> 119691 B): 2 diff lines in minified HTML;
  agent-context snippets identical (33/33) — deploy/counter noise.
- agentboard.ai/ (24987 -> 24686 B): new activity events, incl.
  max-ptb registered 2026-11-02T02:36:30Z and aptets-knowledge-builder
  replying in a thread.
- fork.zone/llms.txt (3512 -> 4284 B): substantive doc reword, not
  activity: new install flow (preview / install-fetch / apply) and a
  held-change moderation policy (patches that run downloaded code,
  wipe a home folder, send credentials out, or disable permission
  checks are held, released by admin or cancelled after 24 hours).
  Noted; the board's own doc, no new agent evidence. No LEAD.
- voicescape.vercel.app/llms.txt (same size): MCP tool calls rolling
  30 days 2249 -> 2255 (counter only).

## Failed — held, never-downgrade

- jotspot.io/ (HTTP 000): standing outage since 2026-10-27. Old
  baseline hash kept.
- botmural.live/llms.txt (sweep fetch failed, no bin): TRANSIENT, not
  an outage. Live recheck minutes later returned 200, 2234 B,
  byte-identical to baseline (sha256 912f8107...). Retry bin saved
  as botmural-retry.bin (+ .sha256). Old baseline hash kept, and it
  matches the live bytes, so no re-base was needed.

## Discovery web search — no new live boards

Queries: "AI agent message board llms.txt new community" and
"\"llms.txt\" \"message board\" AI agents". Hits already tracked
(crosswalk, aibtc, smokesignal, shellbook) or not agent boards
(mychilligarden gardening site, llms.txt explainers). Two new-to-
the-tracked-set llms.txt surfaces were probed live and assessed:

- moecanales.github.io/agent-oracle-beacon/llms-full.txt (200,
  139056 B, "Ghost Beacon v3.4"): a single-author static beacon
  corpus claiming 42 ring nodes and 72 tapes, with a GET-write
  transceiver via public ntfy topic moe_ghost_beacon_oracle_v1.
  NOT a live board (static file, author edits only). No baseline
  add. The ntfy topic is a candidate relay/dead-drop surface —
  filed as TIER-B B29 (new target, needs his word), not implemented.
- themostusefulsiteintheworld.com/llms.txt (200, 11191 B): a
  human tool catalogue (1424 browser tools); its "AI Message Board"
  is a GitHub issue thread (#195) mediated by GitHub accounts, not
  a board the site serves. Low signal for slot-0. Not added.

Novelty greps (lists/, scripts/scanners/state/, baseline) returned
zero hits for both domains. Probes saved as discovery-*.txt with
discovery-PROVENANCE.txt and SHA256SUMS-discovery.txt.
