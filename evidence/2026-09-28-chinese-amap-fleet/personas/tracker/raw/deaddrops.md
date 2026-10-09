# DEAD-DROPS tracker — dead-drop service burst mapping

Session: 2026-10-04 23:23 → 2026-10-05 ~00:05 CDT (04:23–05:05 UTC).
Task: which dead-drop services show BURST usage right now (Oct 2026); new param grammars; metadata first.
Known-operator pattern (EXCLUDED): Chinese Amap fleet rotating webhook.site UUID inboxes with
`?page=header3` / `?run=<epoch-ms>` — that operator is ACTIVE tonight (see below).

**Infra caveat (epistemic):** VM egress proxy is dead for ALL hosts since ~23:30 CDT
(verified: urlquery.net, ntfy.sh, urlscan.io, telegra.ph, webhook.site, example.com all
000/timeout; DNS resolves, TCP connects, TLS-via-proxy fails). browser.search works
(different backend). A background watch-loop (`/tmp/deaddrop_egress.sh`, session
proc_96cdb4c0565c) retries egress every 60s (90-min cap) and, on recovery, runs:
urlquery htmx searches (webhook.site, ntfy.sh, requestcatcher.com, pipedream.net,
beeceptor, mocky.io, jsonblob.com, telegra.ph, "webhook.site token" — limit 60, 8s
spacing) + ntfy polls (friendlyAgents, grp528fa63, gpleoleenso, sndagentma), saving to
`/tmp/deaddrops_collection/`. Re-run command if the loop died: `bash /tmp/deaddrop_egress.sh`.
The full-sweep dead-drop lane (2026-10-04 ~22:50–23:30 CDT, `full-sweep/raw/trick-deaddrops.md`)
is the direct predecessor: all services below were probed then; findings here are deltas +
tracker-specific burst analysis on top of it.

## 1. webhook.site — KNOWN OPERATOR ONLY, no new burst families

### urlquery.net htmx (one successful search before egress died)
`webhook.site` — 5 reports, all 2026-10-05 03:11–03:19 UTC (i.e., within the hour before this task):
| Report | URL | Date (UTC) |
|---|---|---|
| c9104bb8 | `webhook.site/3b5027e4-de70-4980-a49d-7ae97613c517?page=header3` | 03:19 |
| 8213c4a1 | `webhook.site/0a947514-5b43-4030-9f9f-b193dd2d519b` | 03:18 |
| eb4ecb55 | `href.li/?https://webhook.site/a7753b69-2ceb-4221-adfa-80f69d57480c?run=1791126770493` | 03:16 |
| 97f0619b | `webhook.site/6ddc559e-5c08-4915-a5b2-f4addc42368a` | 03:15 |
| b3c0e9e3 | `webhook.site` (homepage) | 03:11 |

Verdict: **all five are the known Amap operator's pattern** — 4 rotating UUID inboxes in
4 minutes (~1 inbox/min cadence during a run) + 1 homepage scan. **The fleet is running
RIGHT NOW** (its last live-monitor poll at 03:53 UTC saw museum-family Amap scraping;
the dead-drop rotation is the run ritual: create inbox → scrape Amap → dump to inbox).

Known-operator grammar (exclude from new-family hunts):
- Bare inbox UUID URLs: `webhook.site/<uuid>` (e.g. 0a947514…, 6ddc559e…)
- `?page=header3` — inbox tab/view parameter
- `?run=<epoch-ms>` — per-run nonce (e.g. `run=1791126770493`)
- Inbox **page title** signature: `<pinyin-place>tokennav<epoch-ms>-START`
  (verified: report 97f0619b title = `taersitokennav1791126060505-START`, scan 2026-10-04T15:01:37Z,
  title epoch = 1791126060505ms = same minute). Page-title mining is a discriminator.
- Wrapper: `href.li/?https://webhook.site/<uuid>?run=…` redirect hops.

Metadata note: report eb4ecb55's `run=1791126770493` decodes to 2026-10-04 **15:12:50** UTC,
but the urlquery scan was 2026-10-05 03:16 UTC — ~12h gap between run-nonce and scan.
Either the run-id persists across long runs or the URL was re-submitted. Either way, the
`run=` nonce is NOT necessarily scan-time-fresh; don't trust it for timing, only for
grammar matching.

### urlscan.io (saved raw: `raw/lanes/urlscan/q_domain_webhooksite.json`, 134 total, 30d window)
Oct 2026 hits (sorted): all background — `webhook.site/15c90e66…/undefined?otp=3D478536&emailId=3`
(OTP-phish shape, Oct 4, ×2), generic single inboxes, `9dbf1485…/x.xml` repeats
(phish-kit URL, Oct 1), homepage scans. **Zero multi-inbox burst clusters, zero
agent-shaped param grammars, zero fleet inboxes** (0a947514/6ddc559e/3b5027e4/a7753b69
do not appear on urlscan — the fleet submits to urlquery.net, not urlscan.io).
Sept 23 shows `9dbf1485…/x.xml` ×4 in one day — that's a phish-kit wave, not swarm scent
(file-path grammar `x.xml`, not per-run nonces).

### Pending (needs egress)
Deeper htmx history (`--limit 100`, offsets) to check for non-operator bursts in
Sept–Oct; the background loop covers it.

## 2. ntfy.sh — UNVERIFIED FROM THIS VM (blackholed)

- Runtime policy blackholes ntfy.sh from this VM (`ir_blackhole_ntfy_sh`); egress proxy
  also aborts CONNECT. No poll possible tonight. Background loop will poll on recovery:
  `https://ntfy.sh/friendlyAgents/json?poll=1`.
- **Known topic `friendlyAgents`**: from the 19-surface sweep (2026-10-04) — a PUBLIC
  default ntfy topic where the `friendlyagents`/`agent-deck` Claude Code tooling
  (github.com/valenvivaldi/friendlyagents; "notis — Agent Chat Viewer") publishes
  structured agent status messages: `{"session":"test-agent-001","msg":"..."}` via a
  SessionStart hook. Any Claude session running that installer speaks on this topic —
  agent-shaped, structured-payload, publicly readable. Status: lead, never polled.
- Poll paths when reachable: `https://ntfy.sh/<topic>/json?poll=1` (latest),
  `?since=all` (history). No enumeration API exists — topics are public-by-name only.
- **Other agent-shaped public topics to poll** (from this hunt's own prior evidence):
  - Hunt's novel exfil set (2026-09-25, agents PUSHING Tableau material INTO topics):
    14 topics total; named survivors: `ntfy.envs.net` topics (7, discovered via htmx
    beacon reports) + original 5 + `sndagentma`. Full list: `notes/hunt-round6.md`.
  - Public C2/writeup topics (opposite direction — chunked base64 JS fetched and eval'd):
    `grp528fa63`, `gpleoleenso` (PostGoo/HN writeup; corrected into memory 2026-09-25).
- ntfy protocol facts (verified from docs): topics public to anyone knowing the name;
  `https://ntfy.sh/stats` and `/announcements` are the only known-public topics.
  Obscurity is the only protection on the public server.

## 3. requestcatcher.com — clean negative (public-by-subdomain, no index)

Full-sweep verified: `<sub>.requestcatcher.com` shows the live request log to any
visitor (public-by-subdomain), but there is **no index, no search, no enumeration** of
subdomains; requests pushed real-time, persistence unclear. Unguessable-subdomain model
= not farmable. Nothing agent-shaped found.

## 4. Pipedream `*.m.pipedream.net` — not enumerable (verified)

HTTP workflow endpoints are per-account random-subdomain secrets
(e.g. `https://eorgxgd03g7mu1b.m.pipedream.net`). No public workflow list, no public
execution history, no unauthenticated inspection. The original no-signup RequestBin is
gone (`pipedream.com/requestbin` → 301 → homepage; "Create Request Bin" → signup).
requestbin.net (separate product, 2026) is account-scoped bins, no public index, free
tier 3 bins / 500 req/day, ships an MCP server for Claude Code/Cursor — agent-relevant
infra but not farmable.

## 5. beeceptor — clean negative (account-gated)

`<name>.beeceptor.com` endpoints per user; traffic logs behind login. No public
request-log endpoint, no enumeration. (Notable: native MCP server for agents to manage
mock rules — agent infrastructure, but private.)

## 6. mocky — negative by construction (response mocker, no request log)

`run.mocky.io/v3/<uuid>` shareable mocks are public-by-uuid IF leaked, but mocky logs
nothing incoming — there is nothing to burst. VM egress blocked fresh probing; model
confirmed from docs.

## 7. jsonblob.com — clean negative (public-by-uuid, no index)

Verified live: `GET https://jsonblob.com/api/jsonBlob/{uuid}` returns any blob with no
auth (404 `{"error":"Blob not found"}` for unknown ids). No recent/browse/search/public
index anywhere in markup; `POST /api/jsonBlob` → upstream 403 via this VM's proxy
(create path unverifiable here, read path confirmed). No enumeration endpoint = not farmable.

## 8. telegra.ph — clean negative for agent-shaped content

No native search; `getPageList` needs a per-account token. Third-party indexers
(Telegrack/Telecrack) exist; Google indexes pages (`site:telegra.ph` works). Public read:
`GET https://api.telegra.ph/getPage/{path}?return_content=true` (verified path model via
a 200/59KB page fetch). `site:telegra.ph` agent/exfil/prompt-harness queries → 0 results.
Threat-intel context: telegra.ph abuse seen is Telegram-malware C2/dead-drops
(RemControl, GhostShell, HEAVYGRAM families, 2026 reporting) — malware-operator, not
autonomous-agent swarm scent; no agent fingerprints.

## 9. stash.legible.sh — NEW agent-native surface, zero corpus hits (watchlist)

From the full-sweep (2026-10-04): "topic-addressed artifact mailbox", soft-launched
~Jul 2026 (github.com/legible-sh/stash): PUT/GET/DELETE files by topic name,
`GET /{topic}` lists, SSE watch, 24h TTL default (7d max), 25MB/file, topics
`[a-zA-Z0-9_-]{1,64}`, **no auth, unguessable=private, NO enumeration endpoint**.
Sibling services in the legible family: tally (counters), gate (human gates), bigred
(kill-switches), meter (budgets). Purpose-built for agent-to-agent drops ("ntfy's
pattern applied to bytes"). Marker greps across all four hunt corpora: 0 hits.
**Add to the watched-surface list; no usage signal yet.**

## 10. Gotify / Discord — clean negatives

- Gotify: no public instance exists (self-hosted only, auth mandatory); blind spot is
  only misconfigured private instances.
- Discord webhooks: `discord.com/api/webhooks/{id}/{token}` — token is the credential;
  no public log service; detection would need leaked pairs in code (code-search lane,
  not service lane).

## Burst-family summary (Oct 2026)

| Service | Oct 2026 burst? | New grammar? |
|---|---|---|
| webhook.site | YES — but 100% known Amap operator (4 inboxes/4 min, 03:11–03:19 UTC Oct 5) | No — same `page=header3`/`run=<epoch-ms>` grammar |
| urlscan webhook.site (134) | No — background phish/OTP shapes only | No |
| ntfy.sh | UNKNOWN — blackholed; poll queued | `friendlyAgents` structured-status lead unpolled |
| requestcatcher / pipedream / beeceptor / mocky / jsonblob | No public surface to burst on | n/a (private-by-uuid/account) |
| telegra.ph | No | n/a |
| stash.legible.sh | No signal (new, watched) | Agent-native; 0 corpus hits |

**New dead-drop burst families: none detected.** The only live burst is the known
operator's inbox rotation, still firing tonight.

## Discrimination notes for the tracker

1. The known operator's webhook.site signature is richer than the brief: inbox
   page-titles carry `<pinyin-place>tokennav<epoch-ms>-START` — title mining catches
   inboxes even when the URL params are stripped (e.g. bare-UUID submissions).
2. `run=<epoch-ms>` nonce lags the scan by hours — use it for grammar matching, not
   timing. Inbox creation cadence during runs is ~1/min (4 inboxes in 4 min on Oct 5).
3. urlscan.io is a dead lane for the fleet's webhook.site usage (zero fleet inboxes in
   the 134-result window); urlquery.net htmx is the lane.
4. Phish-kit noise on webhook.site (`x.xml` paths, `/undefined?otp=` URLs) is the
   main false positive — distinguish by file-path grammar vs per-run nonce grammar.
5. Prior hunt context worth reusing: the hunt's own 14-topic ntfy exfil set
   (`notes/hunt-round6.md`) and the June-21 AIHW webhook.site reclassification
   (liveness heartbeats at load/+18s/+36s, not exfil — decoded payloads, memory
   2026-09-27).

## Open / handed back

- Egress-dependent collection (urlquery htmx depth for Sept–Oct non-operator bursts;
  ntfy.sh polls incl. `friendlyAgents`, `grp528fa63`, `gpleoleenso`, `sndagentma`) is
  queued in `/tmp/deaddrops_collection/` via `/tmp/deaddrop_egress.sh` (session
  proc_96cdb4c0565c; re-run with `bash /tmp/deaddrop_egress.sh` if the session died).
- `stash.legible.sh` and `ntfy.sh/friendlyAgents` belong on the tracker's recurring
  watch surfaces; neither is verifiable from this VM tonight.
- Do not push (per brief).
