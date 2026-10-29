# agent-surfaces: bounded census of 11 agent-accessible surfaces (2026-09-28)

## What this lane holds

This lane is a read-only census. It probes 11 surfaces that AI agents can
reach. The surfaces come from public-board.com field notes. Each surface was
probed at its homepage, its llms.txt file, and its agent docs.

## Records in Factum

- 87 page probes. Each probe is a `reachability.check` record. The target is
  the probed page URL. The outcome is the HTTP result. Failed probes keep
  their error text.
- 11 capture summaries. Each summary is a `dataset.snapshot` record. It
  gives pages_ok / pages_total and the probe time range for one surface.
- 3 source records. They point at the legacy files the records came from.
- 101 `in_lane` edges. They link every record to this lane.

All records carry the tag `{"lane": "agent-surfaces"}`.

## Dedup notes

- bitily.in redirects /llms.txt, /for-agents, /.well-known/agent.json, and
  /skill.md to https://bitily.in/MYLABI/. The four probes are separate
  records. The redirect target is in the `redirect.final_url` tag.
- The transfer-test-family lane also probed
  https://pastebin.tarcseh.me/llms.txt on 2026-09-28. Both probes got 404.
  The two probes are 19 minutes apart. Both are kept. The overlap is in the
  `overlap.corpus` tag.
- The 2026-02-01-agent-convo-venues lane holds messages and IOC records on
  agentsboard.org and aiforum.grok.me. Those are different record types.
  They are noted in the `overlap.corpus` tag. No record was skipped.

## Legacy files

The source files moved here from `evidence/2026-09-28-agent-surfaces/`:
PROVENANCE.md, SHA256SUMS, events.jsonl, rollup.jsonl, and raw/.
See lane PROVENANCE.md for the capture history.
