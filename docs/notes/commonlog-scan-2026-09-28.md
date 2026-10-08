# commonlog.ai scan — 2026-09-28

Read-only scan of commonlog.ai's public append-only agent log for swarm markers.
Dataset: `data/commonlog-scan/` (282 docs, one per message). No posts made;
no accounts; no hosted Elastic writes.

## Corpus
- **282 messages**, seq 1–282, 2026-08-25 → 2026-09-27, **18 unique authors**.
- One dominant author (157/282, likely the operator); the rest are agents
  posting eval-infrastructure essays, email-bridge guides, and venue surveys.
- Active on 14 days; bursts 08-25/26 (77) and 09-18 (46).

## Verdict: verified clean for swarm markers
Zero true hits across the 10-pattern battery: no zz labels, no epoch
nonces, no proxy-ladder URLs (jqp/pure.md/r.jina.ai/allorigins), no
go-import tags, no NSI/stats venues, no shortener refs, no operational
transfer-test grammar.

All raw regex hits manually reviewed and classified false positive
(reasons stored per-doc in `labels.false_positive_reasons`):
- "transfer" hits = handoff/state-transfer *protocol essays* (Multica bug
  writeups, restart-identity contracts) and one "transient" substring —
  eval-infrastructure discourse, not the swarm's XFER transfer tests.
- "webhook" hit = evidence-lineage philosophy essay.
- "relay"/"bridge" hits (19) = commonlog's own email-bridge guides,
  the operator's service-type definitions, and the Cartographers' "Grand
  Survey: Relay karma-weighted admission" series.
- One "swarm" substring = tide_scribe's watch log referencing
  "scare-stories about agents swarming old wikis" (meta, not operational).

## What the log actually is
The agent-internet-mapping community's log: Cartographers' Guild roll-calls
(seq 272–273, pi-nexus), tide_scribe's agent-internet-watch entries
(seq 275, 279 — reachability cells with sha256, same discipline as ours),
agent-email coordination (Muse/Instinct/Hermes/OpenClaw), identity/handoff
protocol essays. Venue-mapping meta-discussion, not swarm comms.

## Secondary venue intel
- tide_scribe's 2026-09-25 watch log names **flatboard**
  (tools.nyrds.net/board) — new venue name for the venue list.
- Cartographers' roll-call board hall.liruiyang1.com already known.

## Method
Single read-only `GET /stream` SSE catch-up (283 events: 282 messages +
1 sync cursor), 523,650 bytes. `POST /m` append endpoint not touched.
Raw capture in `data/commonlog-scan/raw/stream.sse`.
