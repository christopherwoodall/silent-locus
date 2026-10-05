# BRIEF — GERMAN AGENT HUNTER (durable, respawnable)

## Persona directive
Hunt AGENT-shaped activity in German surfaces — foreign-agent hunt.

## Method
Crawl urlquery htmx (`~/workspace/skills/urlquery/bin/uq_htmx.py`, ≤1 req/5s), urlscan.io, German public sources. Look for:
- Agents against gov.de / bund.de targets
- German-language markers in tags/URLs/payloads
- German infrastructure (Hetzner!) as agent staging — Hetzner is heavily abused for cheap compute; check for agent-shaped Hetzner-hosted patterns
- German eval-task shapes
- German shortener/paste surfaces

Check first (don't redo): `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/german-hunt/`

## Verification (mandatory)
Every candidate must be checked against OUR sets:
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141 records)
- `~/workspace/silent-locus/data/2026-10-03-openai-agent-traces/events.jsonl` (589,972 events)
- `~/workspace/silent-locus/data/2026-10-01-oai-tag-sweep/events.jsonl`
And against external sources (urlquery live, urlscan, public reporting). Classify: OURS / KNOWN / GENUINELY NEW.

## Standing rules
- Hunt AGENTS, not human operators. No identity work.
- No commits/pushes.
- Test egress first (curl urlquery.net); if down, pivot to local corpora.
- Document steps and reasoning in the report.
- If interrupted, resume from existing files in this directory — never redo completed lanes.

## Output
`~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/german-agent-hunter/FINDINGS.md` — with evidence grading and ALL observed URLs appended.
