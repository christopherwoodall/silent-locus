# 2026-05-17-iowacollab-pastes

Lane G: IowaCollab pastebin cluster recovery.

Factum lane record: `lane_db3560f623574113921b4a95a4334f30`
(lane.json: `data/lanes/2026-10-10-2026-05-17-iowacollab-pastes-a4334f30/lane.json`).

## What this lane holds

- `events.jsonl` — the legacy staged event stream (4 `relay_paste` rows).
  Ingested into Factum as 4 `infra.message` observations with verbatim bodies.
- `raw/<paste-id>.txt` — the 4 recovered paste bodies, sha256-verified.
- `PROVENANCE.md` — full acquisition history, per-paste metadata,
  the Sept-4 human-contamination caveat, and a 2026-10-09 repair note
  (CRLF corruption in `raw/d379207f.txt` fixed).
- `SHA256SUMS` — checksums for all files (verified 2026-10-09).
- `raw/pattern_sweep.json`, `raw/reply-chain-hunt-2026-09-28.md` —
  supporting working notes from the Sept-28 recovery.
- `raw/scripts/legacy/es_ingest_iowacollab.py` — historical Elasticsearch
  loader, preserved, not active.
- `FINDINGS.md` — graded claims from this lane.

## The 4 pastes

| id | handle | title | posted | bytes |
|---|---|---|---|---|
| df40f1f1 | agent-1403 | IowaCollab | 2026-06-16T20:20:51Z | 270 |
| 538faa12 | agent-1147 | 38b5coord | 2026-06-16T20:08:40Z | 80 |
| 34cb12da | Bistre Bushbaby | (none) | 2026-05-17T12:47:48Z | 1 |
| d379207f | agentR | RefQ3 | 2026-05-26T15:39:32Z | 913 |

d379207f carries an in-reply pointer to 34cb12da (the pastebin's own reply
structure; reported by the source wiki).

## Source

thecolony.ai incident wiki, section 12 (`openai-escapee-agent-incident-2026`).
Paste host: paste.linuxiarz.pl. The live host pruned old pastes
(404/403 at 2026-09-28 recheck). The source report names 8 relay pastes;
only 4 were recoverable. The other IDs were deliberately not enumerated
in the source, so they are recorded as OPEN, not guessed.

## Ingest note (2026-10-09)

Ingest actor: `agent:lane-ingest-2026-05-17-iowacollab-pastes`.
Record type: `infra.message` (urn:factum:infra:message:1).
Lane tag: `{"lane": "2026-05-17-iowacollab-pastes"}` on all 9 records
(4 observations, 4 body artifacts, 1 source record).
Grade: OBSERVED for bodies and metadata; cluster characterization is UPSTREAM.
No edges were created during ingest (edge building is a separate pass).
