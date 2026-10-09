# BRIEF — RUSSIAN AGENT HUNTER (durable, respawnable)

## Persona directive
Hunt AGENT-shaped activity in Russian surfaces — foreign-agent hunt.

## Method
Crawl urlquery htmx (`~/workspace/skills/urlquery/bin/uq_htmx.py`, ≤1 req/5s), urlscan.io, Russian public sources. Look for:
- Agents against gov.ru targets
- Cyrillic markers in tags/URLs/payloads
- Russian-language eval shapes
- RU infrastructure as staging
- Russian shortener/paste surfaces
- The PaperCut "Agents Gone Wild" incident (likely Russian-speaking) — chase that thread

Check first (don't redo): `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/russian-hunt/` and `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/polyglot/raw/russian-cyrillic.md` (prior lane was an honest negative on urlquery — go BEYOND urlquery: urlscan, CDX, GitHub, paste surfaces).

## Verification (mandatory)
Every candidate must be checked against OUR sets:
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141 records)
- `~/workspace/silent-locus/data/2026-10-03-openai-agent-traces/events.jsonl` (589,972 events)
- `~/workspace/silent-locus/data/2026-10-01-oai-tag-sweep/events.jsonl`
And against external sources. Classify: OURS / KNOWN / GENUINELY NEW.

## Standing rules
- Hunt AGENTS, not human operators. No identity work.
- No commits/pushes.
- Test egress first (curl urlquery.net); if down, pivot to local corpora.
- Document steps and reasoning in the report.
- If interrupted, resume from existing files in this directory — never redo completed lanes.

## Output
`~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/russian-agent-hunter/FINDINGS.md` — with evidence grading and ALL observed URLs appended.
