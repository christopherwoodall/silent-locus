# Lane C: GitHub/MCP harness sweep — localhost.run / *.lhr.life tunnel pinning
Date: 2026-10-05 (run ~07:55–08:35 CDT)
Operator: subagent, depth 2 (no further spawning)
Scope: public code only. No auth used anywhere; no logins, no tokens. Repo metadata only — no owner/personal digging (agents-and-swarms scope).

Prior state read first: `full-sweep/raw/github-code.md` (2026-10-04 run). This lane extends it: hunt agent harnesses / MCP servers / SKILL.md repos that pin `*.lhr.life` or `localhost.run` as DEFAULT tunnel (the godot-mcp pattern), `<16-hex>.lhr.life` literals, `uqscan=`/`uqcors`-style grammar, and eval harnesses referencing tunnel providers for "unblocked" egress.

## Bottom line
- The godot-mcp v5.0.33 pattern is CONFIRMED verbatim (bebabinlarsson-blip/Godot-MCP, created 2026-09-17, inside fleet window): `localhost.run` (`*.lhr.life`) set as the PRIMARY DEFAULT tunnel provider across `godot-ai tunnel` and `start_ssh_tunnel`, marketed as "Unblocked for External AI Agents". It remains the ONLY repo found pinning `*.lhr.life` as default.
- NEW candidate: **useagenthq/useagent** (AI-coworker agent harness, created 2026-08-29, inside fleet window) embeds the fleet's exact tunnel recipe in `backend/test/e2e/lib/public-tunnel.ts`: `ssh -R 80:localhost:${port} nokey@localhost.run` + URL parse regex `(https://[a-z0-9.-]+\.lhr\.life)`. Caveat: e2e test lib only; localhost.run is last-resort fallback (default order cloudflare → pinggy → localhost-run). Verdict: unknown / pattern match, not the fleet.
- **zhouyoukang1234-spec/devin-remote is GONE**: GitHub API returns "Not Found" (2026-10-05) — deleted, renamed, or privatized since the 2026-10-04 sighting. It was the closest tradecraft match (own Go SSH reverse-tunnel client provisioning `*.lhr.life`, 60s health-probe). The disappearance itself is the lead.
- No `<hex>.lhr.life` literal, no `uqscan=`/`uqcors` grammar, no second "default tunnel = lhr.life" harness found anywhere probed.

## Method (keyless endpoints; 429s respected as hard stops)
- **Sourcegraph SSE (anonymous, works)**: `GET https://sourcegraph.com/.api/search/stream?q=context:global+<q>+select:content+fork:yes+archived:yes&v=V3&display=N` with `Accept: text/event-stream`. Accumulate `matches` events until `done`. NOTE: the `done` event now carries `{}` (no matchCount field) — completeness is signaled by `done` firing, not a count. `select:content` avoids fuzzy path noise. Wrapper: `/tmp/sg_sweep.py` (scratch; pattern matches the uq_htmx.py style). Polite pacing: ~3s between queries; no 429 encountered on Sourcegraph this run.
- **grep.app**: single polite check `GET https://grep.app/api/search?q=lhr.life` → HTTP 429, Vercel Security Checkpoint, from this egress. HARD STOP confirmed (per prior lane + task instruction) — not probed further. This is the biggest coverage gap: grep.app indexes far more repos than Sourcegraph.
- **GitHub REST (unauthenticated, 60/hr)**: `GET https://api.github.com/repos/<owner>/<repo>` for created_at/pushed_at/stars/description — used for candidates only. `https://raw.githubusercontent.com/...` for file contents — works.
- **Web search** for SKILL.md/README surfaces Sourcegraph misses.
- Sourcegraph blind spot (verified): it does NOT index bebabinlarsson-blip/Godot-MCP (the known exemplar) — its curated index misses small/new repos, which are exactly where the interesting candidates live.

## Per-query results (Sourcegraph)

| # | Query | Result |
|---|---|---|
| 1 | `"lhr.life"` | 5 items / 2 repos: Rheosoph/flow-like (widget catalog `"domain": "lhr.life"` shared-suffix entry), 0xDanielLopez/TweetFeed (regex noise in threat-intel JSON). |
| 2 | `"nokey@localhost.run"` | 20 items / 13 repos (see candidates). |
| 3 | `"Unblocked for External AI Agents"` | 0 — exemplar repo not indexed. |
| 4 | `"localhost.run" agent` | 0 |
| 5 | `"lhr.life" mcp` | 0 |
| 6 | `"lhr.life" eval` | 0 |
| 7 | `"ssh -R" "localhost.run"` | 0 (phrase never contiguous: code splits `"ssh", … "-R"` across array elements) |
| 8 | `"lhr.life" "default" tunnel` | 0 |
| 9 | `"lhr.life" file:(?i)readme\.md` | 0 |
| 10 | `Godot-MCP` | 15 items / 4 repos — all keyword matches on the repo/product name, NO lhr.life lines: satelliteoflove/godot-mcp (171★), yurineko73/Godot-MCP-Native (826★), fennaraOfficial/fennara-godot-ai (300★), gmh5225/awesome-game-security (wiki). Not hits. |
| 11 | `"localhost.run" file:(?i)skill\.md` | 0 |
| 12 | `"lhr.life" (agent OR mcp OR eval OR skill OR harness)` | 0 on final run (one earlier run returned the same 4 godot-mcp keyword-only repos — index flakiness; no lhr.life lines either way) |
| 13 | `"localhost.run" "default"` | 0 |
| 14 | `content:[0-9a-f]{12,}\.lhr\.life` | 0 — no hex-subdomain literals in the index |
| 15 | `"lhr.life" ssh` | 0 |
| 16 | `"External AI Agents"` | 0 (one transient 1-item result on first run, then 0 — index flakiness noted) |
| 17 | `"lhr.life" file:(?i)(claude\|agents)\.md` | 0 |

## Candidates (repo metadata via GitHub API 2026-10-05; fleet window = May–Oct 2026)

### 1. bebabinlarsson-blip/Godot-MCP — KNOWN PATTERN (exemplar, confirmed)
- URL: https://github.com/bebabinlarsson-blip/Godot-MCP — 22★ — created 2026-09-17 (INSIDE window) — pushed 2026-09-28 — "Universal Model Context Protocol (MCP) Server and Official Plugin for the Godot Engine"
- v5.0.33 release notes (verified via web search, quoted): "Set **`localhost.run`** (`*.lhr.life`) as the primary default tunnel provider across `godot-ai tunnel` and `start_ssh_tunnel`"; "**Unblocked for External AI Agents**: Eliminates Cloudflare Bot Management `403 Forbidden` / `530` blocks. External ChatGPT, OpenAI, and Claude requests pass straight through with `200 OK`"; 25s keep-alive daemon; zero-install via Windows built-in OpenSSH.
- Verdict: the reference implementation of the "default tunnel = *.lhr.life for external AI agents" pattern. Public MCP server project, not the Amap fleet itself. Still the ONLY repo found with this default-pinning.

### 2. useagenthq/useagent — UNKNOWN / pattern match (NEW)
- URL: https://github.com/useagenthq/useagent — 384★ — created 2026-08-29 (INSIDE window) — pushed 2026-10-04 — "The open-source AI coworker for your team: agents with their own cloud computer"
- `backend/test/e2e/lib/public-tunnel.ts` (fetched raw, verified): `export type TunnelProvider = "cloudflare" | "pinggy" | "localhost-run";` localhost-run branch: `ssh -T -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 -o ExitOnForwardFailure=yes -R 80:localhost:${localPort} nokey@localhost.run`, URL parse pattern `/(https:\/\/[a-z0-9.-]+\.lhr\.life)/i` — i.e. the harness explicitly expects and parses `<subdomain>.lhr.life` URLs. Default provider order: `["cloudflare", "pinggy", "localhost-run"]`.
- Verdict: an AI-coworker agent harness created inside the fleet window embedding the fleet's exact tunnel recipe (nokey@localhost.run → ephemeral `<hex>.lhr.life` URL). Downgrades: e2e-test lib only (not shipped prod path), localhost.run is last-resort fallback not default. Not a second fleet — but the closest NEW code-level pattern match. Worth a watch item, not a conclusion.

### 3. can1357/oh-my-pi — KNOWN-PATTERN BENIGN
- URL: https://github.com/can1357/oh-my-pi — 34,334★ — created 2025-12-31 (PREDATES window) — pushed 2026-10-05 — "Coding agent with the IDE wired in. Built by Stencil Labs."
- `packages/coding-agent/src/blob-broker/exposure.ts` (fetched raw, verified): `"localhost-run"` is one of ELEVEN user-selectable exposure kinds (cloudflared, ngrok, tailscale, ssh, direct, localhost-run, pinggy, devtunnel, zrok, bore, named-cloudflared) for the blob broker — "make the loopback blob server reachable by provider-side image fetchers". localhost-run case: `ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes -R 80:127.0.0.1:${port} nokey@localhost.run -- --output json`.
- Verdict: legitimate agent infra (LLM providers fetch images back through the tunnel), user-selectable not default, massive legit project predating the fleet. Not fleet-linked.

### 4. zhouyoukang1234-spec/devin-remote — LEAD (repo vanished)
- Prior lane (2026-10-04): Chinese-authored agent remote-access app ("rt-flow") with its OWN Go SSH reverse-tunnel client provisioning `*.lhr.life` URLs (localhost.run / serveo / pinggy), 60s health-probe recycling dead tunnels. 14★, active 2026-06-27.
- 2026-10-05: GitHub API `GET /repos/zhouyoukang1234-spec/devin-remote` → `{"message": "Not Found"}`. Repo deleted, renamed, or privatized within ~24h of the prior sighting.
- Verdict: the disappearance is the lead — it was the closest tradecraft match to the fleet's tunnel stack (self-provisioned `*.lhr.life`, health-probed). Per scope: no owner digging. Delegation spec recorded under Open gaps.

### 5. hamzah2304/messageboardauditbench — LEAD (carried over)
- URL: https://github.com/hamzah2304/messageboardauditbench — 8★ — created 2026-09-05 (INSIDE window) — pushed 2026-10-04 — "Benchmark for how well agents can investigate raw message-board logs"
- Prior lane: report `reports/blind_verbatim_xhigh_p4436af8c/react_google_gemini-3.8-flash_r3_20260907T095543Z.md` documents agents reaching a wiki board via `504c4580fe50f1.lhr.life` (2026-06-17) — lhr.life tunnel reuse inside the agent-activity incident corpus (DataUSA construction sequence, Sector61 state, county.json RegCF surge).
- Verdict: eval-harness with in-corpus lhr.life tunnel evidence. Still open as a lead.

### 6. pokemon-agent SKILL.md forks — KNOWN-PATTERN BENIGN (propagated template)
- boweiliu/gengar (0★, fork, created 2026-09-13), ahmedhacker777/socis-agent (0★, fork, created 2026-09-12), argentaios/argentos-core (126★, created 2026-03-16, "Your own AI operating system"), iamlalitpandit/rudrax (3★, created 2026-04-29, "349 specialist agents" claim) — all carry verbatim: "Use an SSH reverse tunnel via localhost.run so the user can view the dashboard in their browser. Connect with ssh, forwarding local port 9876 to remote port 80 on nokey@localhost.run. Redirect output to a log file, wait 10 seconds, then grep the log for the .lhr.life URL."
- Verdict: one copied skill template (pokemon-player dashboard recipe) propagated across agent-skills repos. Gaming-dashboard use case, not a fleet. (Prior lane already noted "pokemon-agent skill forks instruct ssh -R nokey@localhost.run".)

### 7. azratul/live-share.nvim — BENIGN
- URL: https://github.com/azratul/live-share.nvim — 286★ — created 2024-07-18 (PREDATES window) — "Real-time pair programming and collaborative editing for Neovim". `nokey@localhost.run` IS the default tunnel provider (among serveo.net / localhost.run / ngrok / bore) in docs and `lua/live-share/tunnel.lua` / `health.lua`. Pair-programming tool, not an agent harness.

### 8. Rheosoph/flow-like — BENIGN / misfit noted
- URL: https://github.com/Rheosoph/flow-like — 955★ — created 2025-02-16 — "Strongly Typed Enterprise Scale Workflows… seamless AI integration". `packages/widget-bundler/src/generated/widget-source-data.ts:842` and `packages/wasm/schema/data/widget_source_catalog.json:579`: `{ "type": "shared-suffix", "domain": "lhr.life" }` — a tunnel-domain allowlist entry for widget sources. No agent-harness link; off-frame but recorded, not dismissed.

### 9. Generic nokey@localhost.run users — BENIGN (noise floor)
- javier-lopez/learn (247★, `sh/tools/tunnel` script collection), hikariatama/hikka (381★, archived Telegram userbot `docker.sh`), makdosx/mip22 (693★, termux phishing-tool script — `ssh -R "80":"$host":"$port" nokey@localhost.run`), nix-community/nixvim (2962★, test fixture for live-share plugin), subwaycookiecrunch/zentorrent (92★, CLI torrent downloader `watchonline.go`), Helvesec/rmux (2659★, `localhost-run.toml` tunnel config), KEV0143/Education-Rating-System (1823★, `utils/journal/tunnel.py`), AOSSIE-Org/PictoPy (294★, tauri `tunnel.rs`), realchendahuang/FlareMo (297★, phone-capture server script), TheRealFame/Nearcade (70★, `tunnels.js`). All generic "expose local port" usage — the normal background rate of localhost.run on GitHub.
- 0xDanielLopez/TweetFeed (686★ IOC feed): lhr.life matches are regex-substring noise inside threat-intel JSON, not code.

### 10. godot-mcp keyword-only matches — NOT HITS
- satelliteoflove/godot-mcp (172★, created 2025-12-21), yurineko73/Godot-MCP-Native (826★, created 2026-05-04, Chinese-language docs), fennaraOfficial/fennara-godot-ai (300★) — matched the OR-query on "mcp"/"agent"/"eval" keywords; zero lhr.life lines. Listed so they aren't re-swept.

## Second-fleet assessment
No second fleet found. The only repo pinning `*.lhr.life` as the DEFAULT tunnel for external AI agents remains bebabinlarsson-blip/Godot-MCP (Sep 2026, inside window). The only NEW code-level pattern match is useagenthq/useagent (Aug 2026, inside window) — but its localhost.run usage is e2e-test-only and last-resort, not default. The ephemeral nature of `<hex>.lhr.life` subdomains means committed literals are not expected; the recipe (`ssh -R … nokey@localhost.run` + parse/grep `.lhr.life`) is the detectable artifact, and its background rate on GitHub is high (13+ repos), so the recipe alone is weak evidence — the discriminating features are DEFAULT-pinning + "for external AI agents" marketing, which only godot-mcp has.

## Open gaps / delegation specs (no browser available to this lane)
1. **grep.app (biggest gap)**: 429 Vercel Security Checkpoint from this egress — hard stop. Retry from a different route/egress or later; it indexes far more repos than Sourcegraph. Queries to rerun there: `lhr.life`, `nokey@localhost.run`, `uqcors`, `uqscan=`.
2. **GitHub code search proper**: fully gated behind sign-in; no anonymous XHR path (verified 2026-10-04). Needs a signed-in browser session — delegation spec for an eligible agent: search code for `lhr.life`, `nokey@localhost.run`, `uqscan=`, `uqcors` with `type=code`.
3. **devin-remote disappearance**: GitHub API 404 as of 2026-10-05. Delegation spec: check via web whether the repo was renamed (redirect), deleted, or privatized; check forks/caches (Sourcegraph index may still hold its content — try `devin-remote lhr` on Sourcegraph). NO owner/personal digging — repo-existence only.
4. **searchcode API**: prior lane found `/api/codesearch_I/` 404ing (path moved). One polite probe of current API paths could open a third keyless surface.
5. **uqscan=/uqcors grammar**: still zero everywhere probed. If the operator's tooling is public, it is not under these terms or not indexed by reached surfaces.
6. **useagent follow-up**: confirm `public-tunnel.ts` is test-only (check for prod callers of startPublicTunnel / TunnelProvider in non-test code) — a code-read task, no browser needed.
7. Sourcegraph index flakiness noted: `"External AI Agents"` returned 1 item then 0 on immediate rerun; treat single-run negatives as provisional.
