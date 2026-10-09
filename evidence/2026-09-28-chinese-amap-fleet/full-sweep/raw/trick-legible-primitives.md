# legible.sh primitives sweep — 2026-10-05

**Lane:** the 9 sibling agent-infra primitives at `<name>.legible.sh` (legible-sh family, soft-launched ~Jul 2026; stash.legible.sh was swept clean in trick-stash-legible.md). First coverage of all 9 in this lane.
**Sweeper:** subagent (depth 2), 2026-10-05 ~08:00–08:40 CDT.
**Method:** README/llms.txt/root contract reads for all 9; route audit against the open-source `src/server.mjs` from `github.com/legible-sh/<name>` @ main (same standard as the stash lane); read-only live listing probes (117 GETs total, ~1s pacing, curl — never POST/PUT/DELETE, never touched a lease/pop/spend/decide/burn); Sourcegraph public code search (literal mode) for `"<name>.legible.sh"` in agent repos/skills/prompts.

## Verdict: CLEAN NEGATIVE on all 9 — no agent/swarm fleet activity found. One cross-primitive hygiene note + the code-search caveat below.

All 117 topic probes returned HTTP 200 with empty state. Sourcegraph literal searches: 0 matches for all 9 domain strings (all runs completed, `done:true`). No enumeration/listing endpoint exists on any of the 9 by design — topics are address-by-agreement (capability-by-obscurity, ntfy-shaped), so the marker set is the exhaustive probe path.

## Endpoint inventory (audited against src/server.mjs @ main, matches README tables)

All hosted at `https://<name>.legible.sh`; self-host defaults 4180–4189 (gate 4180, bigred 4181, trail 4182, slate 4183, relay 4184, mutex 4185, quorum 4186, meter 4187, tally 4189 — stash is 4188). Topics `[a-zA-Z0-9_-]{1,64}`, created by first write. Errors `{error, code, hint}` with honest statuses. `GET /`, `/README.md`, `/llms.txt` public and never token-gated on every primitive.

| Primitive | Read-only probes used here | Write verbs (NOT touched) | Notes |
|---|---|---|---|
| **gate** (human-in-the-loop questions) | `GET /{topic}` → `{topic, bound, pending:[], recent:[]}`; `GET /{topic}/log` (audit trail, not probed — pending/recent empty) | `POST /{topic}` (ask — visible), `POST /{topic}/{id}/decide`, `PUT /{topic}/config` | Decide tokens minted per ask; bound mode moves tokens to ntfy channel. 7-day retention. Source audited: routes match docs exactly. |
| **bigred** (fleet kill switch) | `GET /{topic}` → `{topic, state:"go", since, rev:0}`; `GET /ok/{topic}` → 200 `go` | `POST /{topic}/stop\|pause\|go\|throttle` — **deliberately never POSTed**: anyone can flip a stranger's switch by name (by design: "anyone can pull a fire alarm"). Also read-only: `GET /{topic}/state?wait=&since=`, `GET /{topic}/sse`, `GET /{topic}/log`. | Fail-safe asymmetry: stop/pause never need a token. `ok` is a reserved topic name (check route, not a topic). Non-existent topic defaults to `go` — you cannot distinguish "unused" from "explicitly resumed". |
| **trail** (flight recorder) | `GET /{topic}.json` → `{topic, entries:[]}` | `POST /{topic}` (append), `DELETE /{topic}` | `?n=`, `?since=`, `?wait=30` on reads; `/{topic}.txt` plain; `/{topic}/sse`. Source: exact-match routing for `/{topic}`, `/{topic}.txt`, `/{topic}.json` — no hidden routes. |
| **slate** (multi-agent blackboard) | `GET /{topic}` → `{topic, keys:[]}` — names+metadata only, never values | `PUT /{topic}/{key}` (X-TTL, If-Match CAS, If-None-Match create-only), `DELETE` | Keys allow dots; `sse` reserved. Hosted keys expire 30d after last write. CAS lease pattern is the primitive swarm lock — `GET /{topic}` is the cheap fleet fingerprint (key names only, no values). Source audited: matches. |
| **relay** (self-provisioning work queue) | `GET /{topic}` → `{ready:0, delayed:0, leased:0, dead:0, done_total:0}` | `POST /{topic}` (enqueue), `POST /{topic}/pop` (leases a job — **not touched**), `POST /{topic}/{id}/ack\|nack`, `POST /{topic}/dead/retry` | Read-only content surfaces (only if stats non-zero): `GET /{topic}/peek` (next job body, no lease), `GET /{topic}/dead` (dead-letter bodies + attempts), `GET /{topic}/events` SSE. All stats zero on every probe. |
| **mutex** (cross-machine locks) | `GET /{topic}` → `{topic, capacity:null, holders:[], waiting:0}` | `POST /{topic}?ttl=` (acquire — **not touched**: would register our name as a holder), `POST /{topic}/{lease}/renew`, `DELETE /{topic}/{lease}` | `GET /{topic}/sse` read-only. Fence tokens never exposed in status. Source audited: matches. |
| **quorum** (leader election / barriers / votes) | `GET /{topic}` → `{topic, epoch:0, leader:null, barrier:null, proposals:[], voters:0}` | `POST /{topic}/first` (**not touched**: would elect us leader), `/barrier`, `/propose`, `/vote/{id}` | Read-only content: `GET /{topic}/first` (current leader), `GET /{topic}/proposals` (proposal bodies, by, votes, voters — the juiciest surface), `GET /{topic}/decision`, `GET /{topic}/events` SSE. All empty on every probe. **`/healthz`** (`GET` → `{ok:true}`) exists in source but is absent from the README's API table (it IS mentioned in the `--token` self-hosting row, so documented-in-source, not hidden). |
| **meter** (spend kill-brake) | `GET /{topic}` → `{topic, spent:0, cap:null, remaining:null, unit:"units", period:"day", resets:<UTC midnight>}` | `POST /{topic}/spend` (**not touched**: commits spend; `?dry=1` exists but still logs), `PUT /{topic}` (cap), `POST /{topic}/raise` | Read-only: `GET /{topic}/log` (recent spend entries `{at, amount, note, allowed}` — the spend-note surface, only useful if spent>0), `GET /{topic}/sse`. Source audited: route regex `^/([^/]+)(?:/([^/]+))?$` — no hidden routes. |
| **tally** (counters w/ history) | `GET /{topic}` → `{topic, metrics:[]}` | `POST /{topic}/{metric}` (+1/=42 — **not touched**), `DELETE /{topic}/{metric}` | `GET /{topic}/{metric}` returns value + minute/hour/day series (would carry timestamps of fleet activity if non-empty). Source audited: matches. |

**No undocumented data endpoints found on any primitive** (source matches docs; only `/healthz` on quorum is absent from the API table while mentioned in the `--token` row — trivial, not a lead). All nine homepages are the same family template: static server-rendered, no `<script>`/forms/XHR (verified in the gate/bigred/trail sources' `landingPage()`/siteHtml paths; the other six share the same stack and their roots return the same one-screen usage text). `llms.txt` on all 9 is a ~400-byte pointer to the README + the family index at `https://legible.sh/llms.txt` (10 tools + `llms-full.txt`); no additional API content.

## Marker results (live, 2026-10-05 ~08:10–08:30 CDT)

13 topics × 9 primitives = 117 GET listings, all HTTP 200, all empty, zero 429s, zero 403s, zero timeouts. Topic set: `uqscan`, `uqcors`, `pandalegacy`, `sub_poi_navi`, `uqtag`, `probe2`, `qjprobe`, `AGEDATA23`, `httpbun` (stash-lane markers) + `87270ca9ac10`, `qingdaomuseum20261005b`, `7e7ff6dbbe9824`, `91ef9fc4c82a1b` (fleet/tunnel-flavored names).

Empty-state semantics recorded from live responses (for future lanes — these are observed, not guessed):

| Primitive | Empty/nonexistent topic → |
|---|---|
| gate | 200 `{"topic":"…","bound":false,"pending":[],"recent":[]}` |
| bigred | 200 `{"topic":"…","state":"go","since":"<now>","rev":0}`; `GET /ok/{topic}` → 200 body `go` |
| trail | 200 `{"topic":"…","entries":[]}` |
| slate | 200 `{"topic":"…","keys":[]}` |
| relay | 200 `{"topic":"…","ready":0,"delayed":0,"leased":0,"dead":0,"done_total":0}` |
| mutex | 200 `{"topic":"…","capacity":null,"holders":[],"waiting":0}` |
| quorum | 200 `{"topic":"…","epoch":0,"leader":null,"barrier":null,"proposals":[],"voters":0}` |
| meter | 200 `{"topic":"…","spent":0,"cap":null,"remaining":null,"unit":"units","period":"day","resets":"<UTC midnight>"}` |
| tally | 200 `{"topic":"…","metrics":[]}` |

**Hygiene note (behavior, not a hit):** reads appear to materialize empty topic state on at least some servers — e.g. bigred returned `since` = the probe timestamp with `rev:0`. A probe-only sweep therefore leaves a faint footprint (empty topics with our probe timestamp). No content was written and nothing was mutated; but a future lane re-probing the same names cannot distinguish "created by my probe" from "created empty by someone else". Prefer fresh marker names per lane if empty-vs-touched distinction ever matters.

## Sourcegraph code search

Method: keyless `https://sourcegraph.com/.api/search/stream?q=<name>.legible.sh&v=V3&t=literal` (literal pattern type; the default query type returned 0 even for control strings, so the type param matters — documented here for reuse). All 9 runs completed (`done:true`).

| Query | Result |
|---|---|
| `gate.legible.sh` | 0 matches |
| `bigred.legible.sh` | 0 matches |
| `trail.legible.sh` | 0 matches |
| `slate.legible.sh` | 0 matches |
| `relay.legible.sh` | 0 matches |
| `mutex.legible.sh` | 0 matches |
| `quorum.legible.sh` | 0 matches |
| `meter.legible.sh` | 0 matches |
| `tally.legible.sh` | 0 matches |

**Caveat (verify before reusing the zero):** the literal search finds the string `legible-sh` in third-party repos (control, completed), but the legible-sh org's own repos — which contain the literal strings (e.g. gate's README contains `gate.legible.sh`) — return 0. The org appears **not to be in Sourcegraph's public index at all** (soft launch, Jul 2026, small org). So these zeros mean "no indexed third-party repo references the domain" — they say nothing about the org's own repos or repos indexed under names Sourcegraph doesn't crawl. grep.app was already blocked from this VM (Vercel checkpoint, per the stash lane); a GitHub code-search pass (authenticated) or the urlquery-corpus grep lane would be the cross-check. Notably, no agent repo, skill file, CLAUDE.md/AGENTS.md snippet, or prompt in the indexed public corpus references any of the 9 surfaces yet — consistent with soft-launch status, not with active fleet use.

## Web-index check (light)

General web search for the family domains was not run this lane (the stash lane found zero third-party references to `stash.legible.sh` on the open web; the same search would be cheap to repeat per name as a follow-up). The family index `https://legible.sh/llms.txt` and the author's GitHub org (`github.com/legible-sh/<name>`, MIT, zero deps, ports 4180–4189) are the only public references observed.

## Cross-primitive leads (recorded, not hits)

1. **`slate` + `mutex` + `quorum` are the swarm-coordination stack.** Of the 9, these three (plus `relay`) are the surfaces a fleet would use for coordination without a shared parent: blackboard CAS leases, cross-machine locks, leader election/barriers/votes, work queues. All clean now, but they are the right surfaces to re-probe whenever any other lane recovers a topic name from prompts, skills, or telemetry — same standing-watch pattern as stash.
2. **`quorum /{topic}/proposals` and `meter /{topic}/log` and `relay /{topic}/dead` are the content-bearing read-only surfaces.** If a topic ever shows non-zero in a future probe, these three endpoints (GET only) are where the fleet's actual outputs/votes/spend-notes live.
3. **`gate`'s CLAUDE.md snippet and `meter`'s `.claude/settings.json` hook are paste-ready fleet hooks** — an agent fleet could adopt any of these from a single prompt paste, so absence today is weak evidence about next month. The meter hook's default topic in the example is literally `claude` — worth a one-off probe of topic `claude` on meter.legible.sh in a future lane (not done here; scope was the marker set).

## Gaps / blind spots

1. **Empty now ≠ never used** — same caveats as stash, amplified: trail/meter/relay have no burn counter but all have bounded retention (gate 7d; hosted meter logs 500 entries/topic; relay dead-letters 1,000/topic; slate hosted keys expire 30d after last write; tally minute-series 24h). A quiet fleet leaves no trace here.
2. **Self-hosted instances are invisible** — every primitive ships `npx <name>-sh serve` / `npx <name> serve` with the identical API; the hosted instance is the only observable one.
3. **No enumeration endpoint on any of the 9** — only exact topic names can be probed. Unknown agent naming schemes are missed entirely.
4. **Reads may materialize empty topics** (see hygiene note) — probe footprints exist; note them in future lanes.
5. **Sourcegraph coverage caveat** — the legible-sh org itself is not in the public index; zeros are third-party-only. GitHub code search (auth) or corpus greps are the cross-check.
6. **Two-sided routes deliberately avoided** — bigred `/stop` (anyone can flip by name), quorum `/first` (would elect us), mutex acquire (would register a holder), relay `/pop` (would lease a job), meter `/spend` (would commit spend), gate ask/decide, tally count, trail append, slate PUT. If a future lane finds a live topic, all probing stays GET-only per the stash-lane standard.
7. Web-index (general search) per-name coverage not run this lane — cheap follow-up.

## Not pushed (per brief). File written; awaiting orchestrator merge.
