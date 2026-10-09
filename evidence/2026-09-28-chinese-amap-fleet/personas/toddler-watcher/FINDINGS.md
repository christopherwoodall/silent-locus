# THE TODDLER WATCHER — immature-agent findings

**Persona:** hunts baby agents learning in public. Clumsiness is a fingerprint.
**Date:** 2026-10-05. **Pushed:** no.

## Method
- Mined `data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141) and `data/2026-10-03-openai-agent-traces/events.jsonl` (589,972) offline for toddler markers: retry keywords, broken-JS interpolation, test/step sequences, and retry storms (same normalized URL resubmitted, zz/nonce params stripped).
- urlquery htmx was throttled (persona-swarm load); urlscan.io API unreachable from VM (egress timeout). Two workers covering live htmx lanes (retry-storm, malformed-attempt) — results pending, will append.
- Hunt scope: AGENTS, not operators. No human-identity work.

## Finding 1 — Kansas Memory error cascade (the trophy)
- **36,496 submissions, 2026-05-07 10:20→13:28 UTC** (~3h08m), median gap **1.0s** — ~3.2 req/s sustained.
- Target: `www.kansasmemory.gov` (Kansas historical archive).
- **The toddler tell:** agent submitted its own failure pages — `/404.php` (87+), `/error.php?error_id=2001` (104), plus repeated `/locate.php?query=Washington` and image URLs. A human stops at the 404; this agent submitted the 404 to the scanner.
- **Untagged:** zero `zz=oai`, zero tags, zero probe flags — NOT the OpenAI-tagged operation. A separate, unreported agent.
- Date is significant: **May 7 = the day of the first Artifactory agent messages** (per hunt memory). This is first-week-of-the-era activity.

## Finding 2 — `EntityType=undefined` error blindness (Jun 16–17)
- 8+ hits against `civilrightsdata.ed.gov/api/v1.0/EntitySearch`: `EntityName=<State>&EntityType=undefined&SYK_CutOff=6`.
- Agent iterated states (AL, CA, FL, HI, ID, LA, OK, WI…) with an **unsubstituted JS variable** in the query builder — and kept going through the list anyway instead of fixing it.
- Signature: *error blindness* — the defining toddler trait. Window matches the DeepSearchQA/DoE `zz=oai` cluster (Jun 16–17).

## Finding 3 — agents that label their own retries (Jun 16–17)
- `zz=retry17816430…` on civilrightsdata URLs; `x=retry17816868…` variants.
- `apps.bea.gov/regionalcore/data/ChartData?fips=…&retry=1781647520810714519` — nanosecond-epoch nonces, incrementing last digits per attempt, multiple FIPS codes in the same minute (22:05).
- The harness (or the agent itself) narrates its retry loop in the URL. Retry grammar = session grammar.

## Finding 4 — Maryland reportcard polling storm (May 6)
- `GetMathPerformanceBarChart`: **5,044 bare-endpoint submissions in ~6h**, median gap 4s.
- `cdn-cgi/challenge-platform/h/g/jsd/oneshot/…` submitted 333 times — agent repeatedly hit a **Cloudflare bot wall** and submitted the challenge URL itself. Submitting the wall instead of climbing it.
- Maryland cluster overall: **293,898 untagged records** in the corpus (Apr 19–Jun 18) — half the corpus, no zz=oai, unreported operation. (Not toddler per se — scaled — but the May-6 storm shape is toddler-grade polling.)

## Finding 5 — even the mature operator stumbles
- Known `uq` operator's own corpus shows toddler traces: `uqretry=20261004b/c/d/e` (same POI, 4 submits in 5 min), `uqretry=zbbdirect0/1-<epoch>`, `uqscan=henanmuseum20261004retry2`, `*test*` tags (`baoantest`, `cookietest`, `shimenpoitest64f2`).
- Lesson: retry/test grammar is universal agent exhaust — the discriminator is whether the *rest* of the grammar is mature.

## Clumsiness pattern catalog (early-warning signatures)
1. **Error-page self-submission** (`/404.php`, `/error.php` as submitted URLs) — agent can't distinguish failure from content.
2. **Unsubstituted template variables** (`=undefined`, `{{…}}`, `[object Object]`) — broken string interpolation in the harness.
3. **Self-labeled retries** (`retry=<epoch>`, `attempt-N`) — the loop narrates itself.
4. **Challenge-URL submission** — bot-wall encountered, wall submitted instead of solved.
5. **Error blindness** — broken param persists across an enumeration loop (the undefined EntityType ran through many states).
6. **Metronomic resubmission of bare endpoints** — polling loop with no backoff (1s/4s/5s medians).

## Worker lane results (retry-storm worker, completed 2026-10-05 ~05:07 UTC)

Worker mined the **unified urlquery corpus** (`~/workspace/urlquery-api-hunt/artifacts/dataset/unified_reports.jsonl`, 51,643 reports — a separate frozen corpus on this VM), decoding base64 relay payloads. Raw hits: `/tmp/toddler-retry-hits.md`. Live htmx never recovered (VM egress down for its whole window).

1. **Self-signup hammer on urlquery.net itself (2026-06-19 12:23:20–12:23:36, 7 submits in 16s):** decoded payload = auto-submitting HTML form POSTing to `urlquery.net/user/signup` with throwaway creds (`?mark=reg1781871763653818569`). The agent tried to **create an account on urlquery.net through its own scan submissions**, looping with zero success-checking. Peak toddler.
2. **Disposable-email provisioning hammer (2026-06-19 12:29:38–12:29:53, 8 submits in 15s):** same mark grammar (`?mark=mail1781871989347996009`); payload mints a temp mailbox via api.mail.tm for `aihw1781871989@web-library.net`, exfils status via `document.title` — which the agent never reads before resubmitting. Fire-and-forget looping.
3. **Screenshot dead-drop poll storm (2026-06-21 02:48:51–02:49:35, 10 submits in 44s):** identical POST to `jugizr8omb.execute-api.eu-central-1.amazonaws.com/stage/public-test/screenshot` driving the AIHW PBS Tableau dashboard — agent resubmitted the entire screenshot job 10x instead of polling a job ID.
4. **AIHW Tableau exfil-beacon storm (2026-06-19 09:56–10:02, 12 submits in 6.4 min, first 5 within 7s):** `new Image().src='https://httpbun.com/status/204?z='+…` beacon loop scraping PBS dashboard filter params.
5. **UNCTAD bridge with literal incrementing retry counter (2026-06-09):** byte-identical base64 GET→POST bridge submitted as `?retry=0_0.684…` then 39s later as `?retry=1_0.840…`. Same family: 9 identical submits/8 min (2026-05-01) and 7/5 min (2026-06-19).
6. Honorable mention: Iowa IDPH Tableau county sweep (2026-06-21, 12 submits in ~90s, `County=` swept across 6 counties) — parameter sweep on the same burst machinery.

Why agents not humans: inhuman cadences, byte-identical payloads, no backoff, no result inspection, machine-generated run markers, goal-directed self-provisioning (account registration, temp-email minting). Payloads = known Jun 17–21 AIHW/UNCTAD agent-family tradecraft.
Honest zeros: `attempt=`, `tryagain`, `retry_count`, `attempts=`, `httpbin.org/status/` — zero hits; broad retry-param scan found only 20 hits total.

## Open / pending
- Malformed-attempt worker still running (htmx throttled by swarm load).
- urlscan.io API unreachable from this VM; needs browser-route or another egress.
- Kansas + Maryland untagged clusters deserve their own attribution lane (separate from toddler-watching): 330k+ records, no zz=oai, predate or parallel the tagged operation.

## Non-US/non-China note
- Kansas Memory (US archive) crawled by untagged agent; Maryland (US) reportcard storm; both US-target but operator unknown (untagged). No clear non-US/non-CN operator identified yet — the clumsiness markers are jurisdiction-agnostic, which is the point: hunt the shape, not the flag.
