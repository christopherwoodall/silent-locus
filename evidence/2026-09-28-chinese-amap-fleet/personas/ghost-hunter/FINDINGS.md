# GHOST HUNTER — abandoned-agent findings

Persona: hunt ABANDONED agents — crons still running, webhooks still receiving, tunnels still open after their agent died or moved on. A ghost tells you where an agent USED to be; ghosts cluster, so one dead agent means a live sibling nearby.

Status: IN PROGRESS. Three child sweeps running: `tunnels.md`, `deaddrops.md`, `stopped-bursts.md`.

## Confirmed ghost: jmail.world auditor (cut clean at 2026-10-05 03:58 UTC)

- 72 reports, 2026-10-04 23:54 → 2026-10-05 03:58 UTC, median gap exactly 3.0 min, max gap 24 min.
- Death shape: **clean cut, NOT a decay**. Last-10 gaps: 6,2,4,2,3,5,3,6,3,3 min — metronome steady to the end. No lengthening intervals = not a dying cron. Either the task finished or the worker was killed.
- Night Owl context: in UTC+8 that's Mon 07:54–11:58 — a Monday-morning Asia work session. Scheduled audit that completed, or terminated worker.
- Ghost verdict: CONFIRMED GHOST (no activity after 03:58 UTC as of local corpus snapshot; live re-check blocked — egress down during this sweep, retry pending).
- Sibling hunt: an auditor with this workload shape likely has siblings auditing other farms. `stopped-bursts.md` child is mining for them.

## Probe fossils in the Amap corpus (known operator's abandoned tests)

Not ghosts of dead agents — ghosts of dead EXPERIMENTS by the live operator:
- `uqscan=2026092701` — 2 reports, 2026-09-30 18:33, never used again. Date-stamped label, single test.
- `uqscan=20261001yor` — 2 reports, 2026-09-30 21:04, never used again. Same shape.
- Note: `uqscan=1<epoch>` (e.g. `uqscan=179111225301`) is the LIVE epoch-nonce grammar, not a fossil — do not confuse.

These date-stamped one-offs (Sep 30) are harness-test fossils: someone tried a `<word><date>` label variant, abandoned it within hours. They mark the operator's R&D cadence — tests die same-day when they don't stick.

## Corpus-wide fossil sweep (known operator, 1,970 true-submission-date reports)

- 1,107 tag families; only 3 pre-Oct-4 fossils with n≥2 (the two above + 1 duplicate).
- 1,056 families (1,916 reports) still alive at collection end. The known operator is NOT a ghost — alive through Oct 5.

## Egress outage (2026-10-05 ~04:40 UTC)

urlquery htmx, urlscan.io API, google.com, urlquery.net all unreachable from this VM during the sweep (curl timeouts). Live liveness re-checks (jmail.world resumption, tunnel probes, webhook inbox reads) are PENDING retry. Local-corpus analysis above is unaffected.

## Open questions for child sweeps

## Tunnel graveyard (child 3/3 — CANCELLED before finishing, INCOMPLETE)

The tunnel-liveness sweep was cancelled before producing results. Treat as incomplete, not "nothing found". The work is fully egress-dependent (DNS + HTTP probes of `*.lhr.life` subdomains from the corpus), and egress was down for its entire window. **Re-dispatch when egress returns**: extract `*.lhr.life` (plus trycloudflare/ngrok/bore/zrok) subdomains from events.jsonl, classify ALIVE/ZOMBIE/DEAD, check the four OTX-known subdomains (`5ede92286ebdfd`, `820eea12fec476`, `98a8e091083f27`, `c2679a7c8e852b`).
- stopped-bursts: other clean-cut or decaying metronomes on urlquery (cron/heartbeat/healthcheck grammars); tronzap burst death shape.

## Dead-drop graveyard (child 2/3 complete, 2026-10-05 05:02 UTC)

Full tables: `deaddrops.md`. Ready-to-run probe script: `recheck_deaddrops.sh` (run when egress returns).

- **3 fleet dead-drops (2026-10-04)**: `6ddc559e-…` (urlquery `97f0619b`), `0a947514-…` (`8213c4a1`), `a7753b69-…` (`eb4ecb55`, href.li-wrapped). ~14h old at sweep time — likely still alive; ghost check = revisit after 2026-10-12.
- **Gap: 14 fleet inboxes uncollected.** Lane analysis confirms they existed (visible via webhook.site public API in report `97f0619b`, created from Tencent Cloud via `python-requests/2.32.5`, 13/14 on AS132203) but UUIDs were never saved. Highest-value ghost targets; unrecoverable from local corpus. Recovery lead: shared view token `webhook.site/#!/view/e691f66e-73c7-44ff-9d90-a79521173811` — needs a JS/live browser (delegated to parent).
- **9 legacy operator inboxes (Jun–Aug 2026 lhr.life stack)**: 6 likely long expired (35–106d old vs ~7d free expiry — any still existing = still-firing cron); 3 excluded as non-agent noise.
- All ghost verdicts PENDING — no live inbox reads possible during egress outage; nothing fabricated.

## Needs from parent (delegated upward)

1. Run `recheck_deaddrops.sh` when egress returns; compare newest-request timestamps vs `deaddrops.md` last-seen table.
2. urlquery htmx sweep `--query webhook.site` + per-UUID queries — egress-blocked.
3. Open `webhook.site/#!/view/e691f66e-73c7-44ff-9d90-a79521173811` in a live JS browser to recover the 14 missing fleet inbox UUIDs.
