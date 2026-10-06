# Hunt methodology (distilled)

This is the onboarding-friendly distillation of the full hunt manual:
[`../data/2026-09-28-chinese-amap-fleet/METHODOLOGY.md`](../data/2026-09-28-chinese-amap-fleet/METHODOLOGY.md).
The manual is the authority; this page is the map. Section numbers (§)
below refer to the manual.

## Principles

1. **The metadata tells the story.** Timestamps, burst timing, submitter
   user agents, tag grammars, tunnel subdomains, infrastructure metadata
   carry the signal; content is secondary.
2. **Agent shape is more than language.** Time and action are agent shape
   too — cadence, nonce grammars, retry patterns, enumeration order.
3. **A finding that doesn't fit the frame is a lead, never a negative.**
   Misfits get their own investigation.
4. **Honest zeros are first-class.** A documented clean negative with
   stated coverage beats a vague maybe.
5. **Keep all, annotate, never silently dedupe.** Records stay; overlap
   goes in annotation sidecars.
6. **No API key is not a stop.** Read the page source, find the
   frontend's undocumented XHR endpoints, query them directly — and
   document every endpoint found for reuse.
7. **Grade everything.** OBSERVED vs INFERENCE vs upstream assertion, on
   every claim.
8. **Hunt agents and swarms, never human operators.**
9. **Log, don't touch.** Record candidate URLs; never live-fetch them.
10. **Automate with curl.** (On the hunt VM, curl handles the egress
    proxy; Python HTTP stacks do not. Adapt to your own environment.)
11. **A failed check is not a verdict.** "Could not check" ≠ zero. Zeros
    require a working query path.
12. **Write it down as you go.** Steps, rationale, evidence, caveats —
    incrementally, in the durable file.
13. **Direct the hunt, don't just execute it.** (§8) The coordinator
    decides *what* to investigate; workers execute. Every lane brief
    carries objective, approach, success criteria, and a stop condition —
    and stopping a lane is a verdict, not a failure.
14. **Evidence is a graph, not a list.** (§9) Typed nodes (account, IP,
    domain, ASN, marker) joined by typed, graded, provenance-carrying
    edges — flat IOC lists plus `nodes.jsonl`/`edges.jsonl` per event.

## Detection techniques (the working set)

- **Timing discriminators.** Cron-shaped (phase-locked to second 0) vs
  fleet-shaped (uniform seconds, same-second parallel volleys) vs
  interactive sessions. Death-shape: clean cut (finished/killed) vs decay
  (dying cron). Epoch nonces decode to session wall-clock.
- **Grammar census.** Catalog every nonce/tag/param family before hunting
  (`zz=oai<digits>`, `uqscan=<word><date><letter>`, `retry={epoch_ms}-{N}`,
  19-digit epoch-ns). New grammar = lead. Grammars evolve — track lineage.
- **Probe-grammar hunts.** Query the terms an agent would emit, per
  language/domain. Hyphenated probe-name patterns cut hex-substring noise.
- **Cert + ASN pivots.** crt.sh for cert subjects, then Shodan: same cert
  + same ASN + same banner = cluster. Infra claims need ≥2 pivots.
- **Dead-drop tradecraft recognition.** webhook.site inbox view-tokens,
  httpbun `/anything/` endpoints, chunked sendBeacon exfil grammars.
  Decode carrier payloads as text evidence only — never execute, never
  fetch onward.
- **Cross-corpus collision / disjointness.** Same marker in two unrelated
  contexts = investigate. Near-perfectly disjoint grammars across corpora
  = different evals/families (supports the same-provider/different-evals
  framing).
- **Shodan harness-grammar dorking.** Exposed agent surfaces via indexed
  HTML (`.codex/sessions`, `.claude/projects`, `.openclaw/agents`, …)
  across a country/hosting-provider matrix; re-run weekly.
- **Rescan-campaign detection.** Same URLs re-scanned on machine intervals
  = campaign, not coincidence.
- **Enumeration-order analysis.** Serial ID walks, numbered-file walks,
  alphabetical target lists — machine order is agent-shaped.
- **Referrer-laundering route checks.** `href.li`-laundered fetches mark
  the sensitive subset; bank the multi-hop exfil-chain grammar.
- **Platform-default UA as fingerprint.** ~99% of observed reports use
  the scanner's stock UA; zero organic custom agent UAs. The *absence* of
  customization is itself the fingerprint.

## Collection methods (highlights)

- **Endpoint discovery (the htmx pattern).** No API key → read page source
  → find XHR endpoints → query directly with curl. Document every endpoint
  found for reuse.
- **Pacing.** ≤1 request per 5–10s on keyless endpoints; separate
  throttles per endpoint. Authenticated endpoints are 429-prone — retry
  with backoff, one attempt per cycle.
- **Timestamp hygiene.** Use the report's own submission-time field, not
  normalization timestamps. Verify a surface's timezone basis before
  interpreting times. Collection-window bias is not a fleet property.
- **Corpus building.** Canonical `events.jsonl` + `raw/` captures;
  per-report annotation sidecars for external overlap; dataset-level
  provenance records. Counts are canonical — reconcile differences
  explicitly, never silently.
- **Archive status map before deep-diving.** Map an archive's coverage
  window, search reachability, and bot protection before spending a lane
  on it.
- **Cross-archive slug presence sweep** (`slug-hunt.py`). Per marker slug,
  check urlquery search API + urlscan search API (`page.url:"…"`) + Wayback
  CDX in one pass. Hit counts screen for *presence*, not content — a zero
  is a weak negative, never a clean zero.
- **Cross-dataset joins.** Join corpus fingerprint sets (URLs, domains,
  UUIDs, tokens, phrases) against third-party agent-activity datasets,
  restricted to pre-incident windows; date the recreation window from
  incident markers first.
- **Gated downloads.** For gated datasets, use the documented credential
  flow and pin revisions; pull the file manifest before planning.

## Verification protocol

1. **Two pivots minimum** for any infrastructure claim (e.g. cert + ASN,
   or index hit + archived capture).
2. **Positive-control recall check** before filing an archive negative:
   prove the surface can find a known-positive first.
3. **Transport health check** before filing any negative: a failed query
   path yields "could not check". Only a healthy transport + empty result
   = confirmed negative.
4. **Corroborate operator quirks.** Search operators drop records
   (`url.domain:` vs plain keyword); re-run zeros with a second query
   form before trusting them.
5. **Timestamp recovery.** `zz=oai` nonces embed epoch seconds — recover
   collection time ±2s from any logged URL, including third-party logs.
6. **Grade the linkage, not just the fact.** OBSERVED (bytes present) vs
   INFERENCE (reasoned link) vs upstream assertion (someone else's claim)
   — and a strength grade on top (see
   [`evidence-rules.md`](evidence-rules.md)).

## Anti-patterns (mistakes already made, don't repeat)

- **Treating a failed check as a zero.** Network failure, egress outage,
  login-gated API — all yield "could not check".
- **Trusting one search-operator form.** Operators silently drop records;
  corroborate zeros with a plain-keyword search.
- **Claiming cadence from tiny n.** Two submissions 12 minutes apart is a
  behavior note, not a cadence.
- **Confusing ABOUT with WITH.** GitHub is full of repos *about* agents
  and empty of repos *with* agent traces. Dork marker grammars in code,
  not keywords.
- **Reading collection bias as fleet behavior.** Day-of-week over a burst,
  htmx's recent-window bias, pull-vs-count fluctuation — all collection
  artifacts until proven otherwise.
- **Word-boundary failures on short fingerprints.** Short acronyms collide
  (`WHO` the org vs `who` the word). Use word boundaries and minimum
  token lengths for short fingerprints.
- **Assuming the archive covers the target.** Check collection policy and
  domain-level crawl coverage before mining; a structurally wrong corpus
  makes a whole lane moot.
- **Forgetting the observer is in the data.** Rescans, auto-submissions,
  and investigator artifacts look like activity. Attribute the *observer*
  layer before the operator layer.
- **Structural noise mistaken for signal.** Map high-count repeated
  strings to schema fields (doc `_id`s, report IDs, cache-busters) before
  treating them as agent signal.

## OPSEC

- Passive/public OSINT only. No probing suspicious infrastructure: no
  live-fetching candidate URLs, no submitting to scanners, no webhooks,
  no inboxes, no bot APIs, no tunnel endpoints. Use public indexes and
  stored observations.
- Decode carrier payloads as text evidence only — never execute payloads,
  never follow them onward.
- Log candidate URLs with context instead of fetching them.
- When a surface is bot-walled or login-gated, document the endpoints and
  delegate to a browser-capable route — don't force egress.
