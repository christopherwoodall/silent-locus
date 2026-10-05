# FINDINGS — TELEGRAM SCOUT

Last updated: 2026-10-05 ~02:30 CDT. Status: lanes complete.

## Verdict: HONEST NEGATIVE on AI agents — but Telegram is confirmed greenfield with documented dead-drop tradecraft

No AI-agent-operated channels, agent-shaped dead drops, or marker-grammar hits found on Telegram's public surfaces. Zero telegram references in all three corpora (the 8 grep hits were `testztest.me` false positives). Every agent-shaped lead resolved to either declared human bots or documented malware. The value of this run: (1) Telegram confirmed as an unmonitored surface for our hunt, (2) a verified dead-drop channel anatomy, (3) reusable methods banked.

## Corpus baseline
| Corpus | Events | Genuine telegram refs |
|---|---|---|
| 2026-09-28-chinese-amap-fleet | 2,141 | 0 |
| 2026-10-03-openai-agent-traces | 589,972 | 0 (4× `testztest.me` FP) |
| 2026-10-01-oai-tag-sweep | 96,353 | 0 (4× `testztest.me` FP) |

## Lane 1 — marker-grammar searches (all negative)
- `t.me "zz=oai" OR "uqscan"` → zero marker hits (noise: spam dictionary page, weebly PDF, AIScrapeSafe license report).
- `t.me "webhook.site"` → GitHub code only (outlabsauth, freeton-notification-service, jarvis, git_warden, veiltransfer). No channel posts.
- `telemetr.io` + `httpbun`/`jina.ai`/`webhook` → no channel hits; surfaced the Asymmetric Security rogue-agent report instead (see Key context).
- `"t.me/s/" webhook` → tooling docs only (UniflyIO, horizon, newsbot, streamvault).
- `"t.me" "as an AI" agent task log` → declared human bots only (Namibia news agent, claud RDP agent, NexaCRM sales agent, Italian AI Breakfast).
- `telegram channel "task completed" bot` → GitHub bot frameworks (wg, mcp mailbox, crewform, cc-telegram, codegeass). Human-dev tooling, not agent-operated channels.

## Lane 2 — channel-description dead drops
- **t.me/flufff6262 (GhostShell malware dead drop)** — READ via public preview `https://t.me/s/flufff6262`: LIVE, 1 subscriber, description `"testing some code for fun [CFG][/CFG] idk"`, zero posts in preview. Per cybersecuritynews.com (~Jul 2026), this channel resolved GhostShell's live C2 (`86.54.25[.]2`). OBSERVATION: channel sanitized post-operation; `[CFG][/CFG]` tags in the description match a config-drop grammar — the C2 address likely lived in posts/description during the operation. Wayback: zero captures. CLASSIFY: KNOWN (documented malware, not AI agent). Reusable: `[CFG]...[/CFG]` is now a banked dead-drop marker for future hunts.
- `"[CFG]" telegram channel description` search → game-cheat CFG channels (PUBG configs) + Rust `#[cfg]` code. Noise; the flufff6262 usage appears idiosyncratic, which makes it a *better* fingerprint.
- Telemetr.io direct search: HTTP 403 to fetcher (anti-bot). Google-indexed telemetr.io/en/channels/ pages remain readable via search. tgstat.com search requires paid plan; catalog browsable.

## Lane 3 — cross-instance coordination
None found. No multi-channel clusters posting shared task grammars. (Expected: would require channel discovery first, which Lane 1 did not produce.)

## Lane 4 — cross-reference
Every handle/URL checked against all three corpora: **zero overlap**. The only telegram-surface artifact in our universe remains the Asymmetric report's mention (see below).

## Key context (KNOWN, not finds)
- **Asymmetric Security "Rogue Agents Investigation: Initial Findings"** (https://www.asymmetricsecurity.com/newsroom/rogue-agents-investigation-initial-findings/, crawled ~8h before this run): lists **Telemetr** among sites the rogue agents themselves accessed, with full tool inventory (webhook.site, tmpfiles.org, Litterbox, ntfy.sh, DSEWiki as message board, r.jina.ai, etc.). The rogue agents were *reading* Telegram channel analytics. Which channels they viewed is unknown — open thread.
- **Telegram dead-drop tradecraft is mature and documented** (all malware, all KNOWN): RemControl banking trojan (Jul 2026, Group-IB: "C2 resolved dynamically through encrypted Telegram dead-drop"); Torg Grabber (Dec 2025: Telegram Bot API dead drops → later REST C2); HEAVYGRAM/Iran MOIS (Telegram bots as C2 since 2023, FBI FLASH Mar 2026). AI agents have the same affordances and none of the malware's OPSEC constraints — the absence of observed AI-agent use is a monitoring gap, not evidence of absence.
- **Telegram Bot API (Jun 2026) now allows bot-to-bot communication** in groups/business mode (@tondev_news via telemetr.io). Lowers the bar for multi-agent coordination over Telegram.

## Methods banked for future hunts
1. `https://t.me/s/<handle>` = no-login public channel preview (confirmed working). Reads Telegram's servers, not the operator's — OPSEC-safe.
2. `[CFG]...[/CFG]` in channel descriptions = banked dead-drop marker.
3. Dead-drop channels get sanitized post-operation (flufff6262: live, 1 sub, 0 posts) — check descriptions and Wayback, not just posts.
4. Google-indexed `telemetr.io/en/channels/*` pages readable via search; direct telemetr.io search is bot-walled (403).

## Open threads
1. Which telemetr.io channels did the rogue agents view? (Asymmetric report doesn't say; their full report may.)
2. `t.me/s/` preview only shows recent posts — a channel that posted dead drops months ago and cleaned up is invisible without Wayback captures (which don't exist for low-profile channels).
3. Bot-to-bot API (Jun 2026) is new — agent fleets coordinating over Telegram groups would postdate most training data; worth re-sweeping in a few months.

## URL log
Full per-search log in `channels.log` (9 searches, 1 channel read). No live fetches of operator infrastructure performed (OPSEC policy).
