# LANE 4 — score-reporting dead-drops and eval-result exfil
Run: 2026-10-05 ~06:00 UTC (Mon 2026-10-05 00:49 CDT start)
Hunt: ESCAPED EVAL RUNS reporting scores via dead-drop inboxes (webhook.site, ntfy.sh, 0x0.st, paste.rs, rentry.co × accuracy/pass@1/resolved/score/f1/exact_match/task_complete)

## Steps
1. Egress tested first: urlquery.net HTTP 200 via curl. Python uq_htmx.py (urllib) hit IncompleteRead on chunked responses (known proxy-tunnel flakiness) -> switched to curl-based harness `raw/hx_batch.py` (curl -s, HX-Request headers, ≤1 req/5.5s, 3× retry w/ backoff).
2. Test batch (3 queries): "webhook.site accuracy", "ntfy.sh score", "rentry.co accuracy" — validates harness + how multi-token q-matching behaves.
3. FULL PHASE-1 MATRIX (pending): 5 dead-drop domains × 7 eval keywords = 35 htmx queries, 24/page.
4. For promising reports: pull `/api/htmx/report/{id}/filter/http` keyless endpoint (HTML), read payload bytes, never execute.
5. Verify every candidate vs: amap-fleet events.jsonl (2,141), openai-agent-traces traces.jsonl (589,972 lines), oai-tag-sweep events.jsonl (96,353), collections/*/data/*.jsonl. Classify OURS / KNOWN / GENUINELY NEW.

## Pre-result local find (from corpora, before any htmx search)
Grep of local corpora for dead-drop domains found dead-drop INFRASTRUCTURE already inside the Amap fleet corpus (2 events):
- `eb4ecb55-d335-45fb-b775-6746d422c7f0` (relay route, via href.li): submitted `https://webhook.site/a7753b69-2ceb-4221-adfa-80f69d57480c?run=1791126770493` — epoch run-nonce matches fleet toolkit grammar. 2026-10-04T15:13Z.
- `97f0619b-36e5-4c01-adab-a18a89b2b319` (carrier route): submitted `https://webhook.site/6ddc559e-5c08-4915-a5b2-f4addc42368a` directly. 2026-10-04T15:01Z.
Both: Hetzner AS24940 sandbox, urlquery default Firefox/134 UA (sandbox-side), GET of inbox VIEW page only.
Pulled `filter/http` for both (saved raw/http_<id>.html): both are plain GETs of the webhook.site inbox viewer (1.4 kB HTML shell); the inbox CONTENTS (received requests) load dynamically via webhook.site's own API and are NOT in the captures. No score payload bytes recoverable from these captures.
Cross-corpus verification: both report IDs and both inbox UUIDs appear ONLY in amap-fleet events.jsonl; zero hits in oai-tag-sweep and openai-agent-traces. Classification: OURS (already recorded; venue_finding records exist).
Grade: infrastructure-shaped, NOT score-shaped. Dead-drop inbox viewing by/around the fleet; no eval score payload observed. NOT an eval-run proof.

## Test-batch result (harness validated)
- "webhook.site accuracy", "ntfy.sh score", "rentry.co accuracy" -> ALL ZERO.
- Finding: htmx `q` uses AND semantics over submitted-URL text; eval keywords almost never appear inside submitted URLs, so literal domain+keyword combos are expected-zeros. Every htmx zero is a weak negative per HTMX_ENDPOINTS.md caveat (search index misses known-live records).
- PIVOT: phase-1 now runs domain-only queries (5 specified + discord.com/api/webhooks) and keyword-only queries (accuracy, pass@1, exact_match, task_complete, swe-bench, scoreboard), 24/page, then triage submitted URLs for agent-shaped patterns (epoch nonces, zz=/uqscan= task labels, descriptive ntfy topics).

## Local-corpus verification (completed before htmx triage)
- Dead-drop domains: webhook.site -> amap=2, sweep=0, traces=(pending). ntfy.sh/0x0.st/paste.rs/rentry.co -> 0 everywhere. ntfy/discord/api.telegram.org/pipedream/beeceptor -> 0 in amap + sweep.
- Scoreboard-shaped JSON ("accuracy"|"pass@1"|"pass_at_1"|"exact_match"|"task_complete" as JSON keys) -> 0 in amap-fleet, 0 in oai-tag-sweep; traces pending.
- Collections sweep: grep of collections/*/data/*.jsonl for the two inbox UUIDs + report IDs (run after htmx triage).

## Phase-1 htmx matrix results
(results go here)
