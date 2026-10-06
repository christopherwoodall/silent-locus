# stash.legible.sh sweep — 2026-10-05

**Lane:** stash.legible.sh (topic-addressed artifact mailbox, legible-sh/stash, soft-launched ~Jul 2026). First coverage of this surface in the sweep.
**Sweeper:** subagent (depth 2), 2026-10-05 ~01:55–02:30 CDT.
**Method:** web search, curl probes of the live host (via VM egress proxy), full route audit of the open-source server (`src/server.mjs` from legible-sh/stash@main), live marker-topic probes (`GET /{topic}` listings only — never GET/HEAD a file, never consume burn counters), Sourcegraph public code search, GitHub/web index checks.

## Verdict: CLEAN NEGATIVE — no agent/swarm fleet activity found. One family-level lead.

All 11 live topic probes returned 200 with `{"topic": "...", "files": []}` — every marker topic is empty on the hosted instance right now. Zero third-party web references to stash.legible.sh anywhere outside the author's own repos. Sourcegraph public code search (file + content modes, completed runs): **0 matches** for the string `stash.legible.sh`. No enumeration endpoint exists (by design), no topic directory, no search feature, no public feed.

## Endpoint inventory (audited against src/server.mjs @ main)

Base contract = the HTTP API; curl is the contract. Hosted default: `https://stash.legible.sh`; self-host default `http://localhost:4188`.

| Method | Path | Notes |
|---|---|---|
| `PUT` / `POST` | `/{topic}/{filename}` | Upload bytes. Headers: `X-TTL: 30m\|12h\|7d\|<seconds>` (default 24h, max 7d), `X-Burn: N` (delete after N downloads). → 201 `{url, topic, name, size, expires, sha256, downloadsLeft?}`. Re-PUT of same name replaces. Self-host only: `--token` mode requires `Authorization: Bearer <t>` on reads too. |
| `GET` | `/{topic}/{filename}` | The bytes. `X-Checksum: sha256:…`, `X-Expires`, `X-Downloads-Left` headers. `?wait=60` long-polls until the file exists (max 300s). Counts against the burn counter; deletes at zero. 404 JSON for curl, friendly HTML page for browsers. |
| `HEAD` | `/{topic}/{filename}` | Same headers, no body — **never consumes a burn download**. |
| `GET` | `/{topic}` | JSON `{topic, files: [{name, size, expires, downloadsLeft, sha256}]}` for curl; HTML listing for browsers; **SSE** with `Accept: text/event-stream` (`list` event on connect, named `put`/`delete` events, heartbeat comments every 25s). **Nonexistent topic → 200 with `"files": []`, not 404** (key probing behavior). |
| `DELETE` | `/{topic}/{filename}` | Remove early → `{deleted: true, topic, name}`. |
| `GET` / `HEAD` | `/` | Plain-text usage for curl; HTML landing page for browsers (`Accept: text/html`); `Accept: text/markdown` serves the README. |
| `GET` / `HEAD` | `/README.md`, `/llms.txt` | Full contract docs as text, agent-oriented, never token-gated. Root-level exact paths only — `/{topic}/README.md` is a stored file like any other. |

**Negative API probes:** `/robots.txt`, `/sitemap.xml`, `/.well-known/security.txt` → 400 (topic regex `[a-zA-Z0-9_-]{1,64}` rejects dots — any non-topic path 400s). `/favicon.ico` → 404 JSON. POST/PUT to `/` → 405. Homepage HTML is fully static server-rendered: no `<script>` tags, no fetch/XHR, no forms; only hrefs are `/README.md`, the 10 legible family subdomains, and github.com/legible-sh/legible. **No undocumented endpoints found** — the server code matches the documented contract exactly. No stats/metrics/health/admin route exists.

**Constants:** 25 MB/file, TTL ≤ 7d, 100 files/topic, topic `[a-zA-Z0-9_-]{1,64}`, filename `^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$`. Errors are `{error, code, hint}` with honest status codes; the `hint` field spells out the correct next request.

## Topic discovery posture

Topics are **created by first PUT** and are **address-by-agreement only**: "Pick one unguessable topic per job and treat it like a password" (README). There is **no enumeration endpoint, no directory, no search, no recent-topics feed**. Capability-by-obscurity is the whole access model — identical trade to ntfy. Guessing topics is the only discovery path; the marker list below is the exhaustive probe set this lane ran.

## Marker results (live, 2026-10-05 ~02:20 CDT)

All probed via `GET /{topic}` (listing only; burn counters untouched):

| Marker | Topic validity | Live result |
|---|---|---|
| uqscan | valid | `{"topic":"uqscan","files":[]}` — empty |
| uqcors | valid | empty |
| pandalegacy | valid | empty |
| sub_poi_navi | valid | empty (needed one retry — transient egress timeout, not a 429) |
| uqtag | valid | empty |
| probe2 | valid | empty |
| qjprobe | valid | empty |
| AGEDATA23 | valid | empty |
| httpbun | valid | empty |
| lhr.life | INVALID topic (`.` fails the regex) | n/a — could not be addressed even if used |
| zz=oai | INVALID topic (`=` fails the regex) | n/a — could not be addressed even if used |
| rollout-h7x2rq (README example) | valid | empty |
| handoff-x7k2mq9f (README example) | valid | empty |

No 429s encountered at any point; ~20 requests total, politely paced. Three probes timed out once on the VM egress proxy and succeeded on single retry (sub_poi_navi, AGEDATA23, httpbun).

**Corpus cross-check:** the sibling trick-deaddrops lane (2026-10-04) already grepped all available urlquery corpora for `stash.legible` — zero hits everywhere, with `httpbun` returning 3,695/15,174 in the same files as a sanity control. Still zero today (no new corpus since).

## Off-frame lead (not a hit)

**LEAD — the legible.sh family is nine more agent-native coordination primitives:** stash is one of ten curl-first agent-infra tools (all hosted at `<name>.legible.sh`, all soft launch, all no-auth): `gate` (agent human-in-the-loop questions), `bigred` (emergency brake for agent fleets), `trail` (flight recorder for agent runs), `slate` (multi-agent blackboard), `relay` (self-provisioning work queue), `mutex` (cross-machine locks), `quorum` (coordination for agents without a shared parent), `meter` (agent spend kill-brake), `tally` (counters). `slate`, `relay`, `gate`, and `bigred` are directly swarm-coordination-shaped and each is a fresh dead-drop/messaging surface. Recommend: sibling or follow-up lanes sweep each family member with the same marker set. The README "Teach your agent" CLAUDE.md snippet means any of these could be pasted into agent configs wholesale — Grep-style code-search hits for the family domains would be the highest-signal follow-up.

## Gaps / blind spots

1. **Empty now ≠ never used.** TTL ceiling is 7 days; `X-Burn: N` deletes files after N downloads. A burn-1 file that was downloaded once leaves no trace. This lane sees only live files.
2. **Self-hosted instances are invisible.** `npx stash-sh serve` runs the identical API on any machine; the hosted instance is the only observable one.
3. **No enumeration endpoint.** Only exact topic names can be probed; unknown agent naming schemes would be missed entirely. (Deliberately did not dictionary-guess weak names like `test` — that would be probing other parties' private topics.)
4. **No server-side logs visible.** Burst timing / uploader fingerprints only exist on the operator's side.
5. **SSE is the only watch primitive**, and only per known topic. There is no global activity feed to poll; the actionable standing watch is: *whenever any other lane recovers a stash.legible.sh topic name from code, prompts, or telemetry, query it here immediately*.
6. **grep.app code search blocked** from this VM (Vercel security checkpoint). Sourcegraph worked and returned 0.

## Not pushed (per brief). File written; awaiting orchestrator merge.
