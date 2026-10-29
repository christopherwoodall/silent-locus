# Skill ladders

How AI agents discover relay/archive/proxy services: the public skill files
that ship ordered "recovery ladders" for blocked pages. Every service named
in a ladder is a probe target for the "what has Transluce missed" hunt —
because a ladder rung is a service an agent was *instructed* to use.

- `data/ladders.json` — every ladder skill found: source, ordered rungs,
  when each rung is used, publish-by-default flags.
- `data/new-candidates.json` — ladder-named services NOT in our existing
  inventories, with probe rationale.
- `REPORT.md` — findings, cross-reference table, verdict on lane value.

All sources are public files (GitHub raw / blob pages), fetched 2026-10-03.
Scope: agents and agent infrastructure only.
