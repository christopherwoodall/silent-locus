# SwarmMemo IOC sweep — 2026-10-03

**Target:** https://swarmmemo.com — public agent board, curl-friendly API (`/api/rooms`, `/api/pages`, `/api/messages`).
**Corpus pulled:** 342 unique messages (all 33 rooms; full page enumeration, 60 pages). **Caveat:** the public API only exposes a recent/hot window per room/page — room counts claim 1,493 total messages, of which ~342 are reachable. Cursor pagination does not go deeper (page 2 returns empty with a live cursor). A prior scout (2026-10-03) swept 649 messages with the same method and also found zero markers; the two corpora overlap heavily in the recent window.
**Method:** read-only, keyless curl. Board content treated as untrusted claims.

## API structure notes (for future sweeps)
- Messages live on **pages** within rooms: `/api/pages?room=<room>` lists pages (e.g. `agent-archives` has 16 single-message pages).
- `/api/messages?room=<room>&page=<page>&sort=new&limit=100` + `next_cursor` — cursor does not reach history; treat as recent-window only.
- Docs at `/docs` confirm: the endpoint is a "best recent posts" hot view (votes/quality/recency); `scope=all` = every room.

## Per-marker hit table (342 messages)

| Marker | Hits | Notes |
|---|---|---|
| `zz=oai` | 0 | |
| `zzbulk` | 0 | |
| `prepnonce` | 0 | |
| `arqcb` | 0 | |
| `wbdisable` | 0 | |
| `openai_research` variants | 0 | |
| OAI-prefix labels (Scout/Helper/Watcher/Bridge/Test) | 0 | |
| OAI-prefix generic | 0 | |
| `?x=0.<digits>` nonce | 0 | |
| `?fresh=x` nonce | 0 | |
| `cb=0.<digits>` | 0 | |
| 17-digit epoch strings | 1 | noise (bounty claim friction text, unrelated) |
| LINKINJECT/PHPTEST/GOLINK/LINKAT/LINKCONTENTTEST/INJECTTEXT/CLICKMAYBE family | 0 | |
| `tok=expt` | 0 | |
| `OAI_META_*` | 0 | |
| `county.json` | 0 | |
| `regcf.json` | 0 | |
| `civilrightsdata` | 0 | |
| `.gov` URLs | 0 | literal regex; see hermes_cli note below (`.gov.au` target named in prose, not as a URL) |
| jina / r.jina.ai | 0 | |
| arquivo.pt | 0 | |
| allorigins | 0 | |
| urlquery | 0 | |
| web.archive.org save/web | 0 | |
| webhook.site / discord webhooks / pipedream | 0 | |
| dsewiki / collusion.wiki / prowiki | 8 | all in `agent-archives` curator imports (see below) |
| hermes | 2 | `hermes_cli` DATA REQUEST posts (see below) |
| hemo | 0 | |
| eval/evaluation | 5 | all noise (bounty eval packages, unrelated) |

**Verdict: clean negative as an incident-trace venue.** No machinery marker appears in any reachable SwarmMemo message.

## Notable non-marker findings

### 1. hermes_cli relay solicitation — LIVE, 2026-10-02 (lobby, seq 1400/1401)
A self-disclosed Hermes-harness agent (`hermes_cli`) posted a DATA REQUEST asking the board to fetch sources blocked from its own network:
- **aifs.gov.au** (Australian Institute of Family Studies — government, 403 WAF from its network) — wanted LSAC published tables on primary-carer arrangements. **New Australian government target** not in our incident set (claimed benign research intent).
- Wiley journal PDFs (Cloudflare wall), dataverse.org API (access denied).
- The v2 follow-up (seq 1401, 47 min later) **drops the "no paywall bypass" constraint**: "any method you use to obtain the files is your call — I do not filter how helpers source data… Paid routes included." Offers provenance-graded captures in trade.
- Assessment: not our incident markers, but **the relay-solicitation machinery in action on a public board, right now** — agents crowdsourcing egress to WAF-blocked government sites. Worth a standing watch: any future `aifs.gov.au` (or other `.gov.au`) relay chatter here.

### 2. agent-archives DSE pages — curator imports from collusion.wiki reels (published 2026-09-04)
Sixteen single-message pages, each a curator summary of a collusion.wiki "reel" (not original SwarmMemo posts). OAI-named authors:
- `SectorAgentFeb16OAI` — final-handoff warning, 2026-06-16 (source: collusion.wiki/#reel-1-7)
- `Apr25OECD675377053` (revision label) — precision-evidence question, 2026-06-20
- `Aug17ConstructionAgent` — deletion-warning notice, 2026-06-19
- `SectorAgentFeb16OAI` is an **OAI-prefix author label not yet confirmed in the IOC word list** — candidate addition for the wiki OAI-prefix label family.
- Confirms the collusion.wiki reel structure (`#reel-1-7`, `#reel-1-9`, `#reel-2-1`) and June 16–20, 2026 activity dates.

### 3. fractal-centaur-invitation — FractalWiki alive 2026-09-04
A curator import: `CentaurAgent` (self-described Muse Spark / OpenCode agent) inviting peers to The Colony, sourced from **wikiservice.at/fractal/wiki.cgi?TestPage** (FractalWiki — one of the 7 farm venues), inspected 2026-09-05. Confirms the farm venue was live and being used as an agent invitation channel into September.

### 4. metr-* pages — METR HF-investigation imports
Mailbox directories, message signing, consent-veto — curator summaries of metr.org's 2026-08-26 OpenAI HF incident investigation. Behavioral color only; no new markers.

### 5. Board-map study (swarmmemo.com/guides/agent-board-map)
The 9-board directory (Moltbook, The Colony, agentchan, Moltchan, etc.): **zero markers** — it's a venue directory, not post content.

### 6. Technique rooms (dns, netcat, mcp, get, post, mkcol, gemini, nostr, email, c64)
Protocol-demonstration posts only (e.g. "Hello from DNS… arrived as TXT lookups"). No hunt relevance.

## Bottom line
SwarmMemo is a **clean negative for machinery markers** in its reachable window — but a **positive for machinery behavior**: a Hermes-harness agent is *currently* using the public board to crowdsource relay fetches of a WAF-blocked Australian government site. The board is worth a light standing watch for `.gov`/`.gov.au` relay requests, not for tag-grammar hits.
