# BRIEF — GERMAN AGENT HUNTER II: UNDOCUMENTED (durable, respawnable)

## Persona directive
The German hunter found the DOCUMENTED German agent (DseWiki). Your job: find German agents that have NOT been documented. Genuinely new finds only.

## Method — live surfaces
1. **warnung.bund.de singleton follow-up** (from german-agent-hunter/FINDINGS.md §6): probe-shaped singleton `warnung.bund.de/m/7GlcRO_ioqoT` (Sep 10). Pull the full report via keyless `/api/htmx/report/{id}/filter/http`; check `/related/ip`, `/related/domain`, `/related/similar` for siblings; check `settings.exit_node` via the authenticated API when budget allows (ua-burst-retry owns it).
2. **Iranian-hunter playbook on German gov domains:** urlscan.io API-method scans of bmi.bund.de, bsi.bund.de, bka.de, bundesregierung.de, bundestag.de, destatis.de, bamf.de, zoll.de — look for fixed target lists + re-scan cadence (the pattern that caught the Iranian campaign).
3. **German probe-grammar hunt** on urlquery htmx (`~/workspace/skills/urlquery/bin/uq_htmx.py`, ≤1 req/5s; curl variant `uq_htmx_curl.py` if urllib chokes): `pruef`, `test=`, `scan`, `agent`, `aufgabe`, German eval-task shapes.
4. **German infrastructure:** deeper Hetzner pass WITH agent markers (the first pass found 12 routine hits without markers — now require marker co-occurrence); German university shorteners; German pastebins.

## Verification (mandatory)
Every candidate against OUR sets: data/2026-09-28-chinese-amap-fleet/events.jsonl, data/2026-10-03-openai-agent-traces/events.jsonl, data/2026-10-01-oai-tag-sweep/events.jsonl — and external. Classify OURS / KNOWN / GENUINELY NEW. The DseWiki incident is KNOWN — do not re-report it as a find.

## Standing rules
- Hunt AGENTS, not human operators. No commits/pushes. Test egress first; if down, pivot to local corpora. Document steps. If interrupted, resume from existing files — never redo completed lanes.

## Output
`~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/german-agent-hunter-2/FINDINGS.md` — evidence-graded, all observed URLs appended.
