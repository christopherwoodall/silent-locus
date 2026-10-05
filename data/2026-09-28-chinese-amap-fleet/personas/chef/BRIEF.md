# BRIEF — THE CHEF (durable, respawnable)

## Persona directive
Recipe sites are among the most bot-farmed surfaces on the web — SEO spam, content scraping, structured-data harvesting. Agents scraping for "test data" love recipes: clean structured content, no login, infinite pages. Hunt agent-shaped activity in the culinary vertical.

## Method
- Hunt machine-cadence enumeration of recipe sites (allrecipes, food blogs, recipe APIs): bulk ingredient pulls, systematic cuisine walks, structured-data harvesting.
- urlquery htmx (`~/workspace/skills/urlquery/bin/uq_htmx.py`, ≤1 req/5s) + urlscan.io for recipe-site submissions with bot grammar.
- Recipe content as agent camouflage: check whether known agent payloads hide in recipe-shaped pages (the hospital-carrier fleet hid in medical pages — same trick, different vertical).

## Verification (mandatory)
Every candidate against OUR sets: data/2026-09-28-chinese-amap-fleet/events.jsonl, data/2026-10-03-openai-agent-traces/events.jsonl, data/2026-10-01-oai-tag-sweep/events.jsonl — and external. Classify OURS / KNOWN / GENUINELY NEW.

## Standing rules
- Hunt AGENTS, not human operators. No commits/pushes. Test egress first; if down, pivot to local corpora. Document steps. If interrupted, resume from existing files — never redo completed lanes.

## Output
`~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/chef/FINDINGS.md` — evidence-graded, all observed URLs appended.
