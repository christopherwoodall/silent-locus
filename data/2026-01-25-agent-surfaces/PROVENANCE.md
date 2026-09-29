# PROVENANCE — agent-surfaces lane (Lane H, 2026-09-28)

Lane report: notes/agent-surfaces-2026-09-27.md. Raw captures in
data/agent-surfaces/<slug>/ (homepage, llms.txt, agent docs), each with
pages.json, per-dir PROVENANCE.md, progress.log. Capture script:
scripts/capture_agent_surfaces.py; ES ingest: scripts/es_ingest_agent_surfaces.py.

## Closure 2026-09-28 (workstream D)

Bounded census complete: the 11 surfaces named in public-board.com field
notes, each captured read-only (homepage, llms.txt, agent docs). N=11 docs
(surface_capture) is the complete list — no more named surfaces exist in
the source list. ES `agent-surfaces` _count=11 verified. The note's open
follow-ups (full-dataset pulls for the 6 board surfaces, paste-lane
enumeration, bitily alias lane) are recorded as concrete next steps in
notes/agent-surfaces-2026-09-27.md, not orphaned.

## Schema backfill 2026-09-29 (normalization sweep, worker W4)

- Built `events.jsonl`: 87 records, one per captured page (`raw/<surface>/pages.json`, 11 surfaces).
- record_kind: `venue_probe`. Fingerprint identity string: `agent-surfaces|<surface_slug>|<page_url>` (sha256).
- @timestamp = page `retrieved_at_utc` (the probe observation is the event); labels.timestamp_source=`retrieved_at_utc:probe_observation`. `page.ok=false` pages kept with their HTTP status.
- Surface base from each `raw/<surface>/PROVENANCE.md` `base_url:` line.
- `rollup.jsonl`: 11 rows, one per surface (record_kind `venue_finding`, event.dataset `2026-01-25-agent-surfaces-rollup`): pages_ok/pages_total, first/last probe, content types. Fingerprint identity: `agent-surfaces-rollup|<surface_slug>`.
- Regenerated `SHA256SUMS` (events.jsonl + rollup.jsonl + raw/**).
