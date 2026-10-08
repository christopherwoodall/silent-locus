# schemas/farm-reports.md

Farm-level writeups under `data/hf-trajectories/`.

## Farm run reports (e.g. `URL-KEYWORD-FARM.md`, `url-farm/*.md`)

- One writeup per farm run. Required sections:
  - Coverage table (rows/files scanned per dataset).
  - Tiered URL inventory (counts per laundering tier).
  - Keyword hit counts (per term/category).
  - Ranked leads, with exact OBSERVED counts.
- No sampling silently hidden: state what was scanned and what was not.
- Keep the raw per-group JSONs beside the writeup
  (`group-A.json`, `group-B.compact.json`, …) and the rollups
  (`merged.json`, `lead-candidates.json`, `hosts-deduped.json`).

## `TARGET.md` — agent targeting profile

- What the agents were pointed at, how they accessed it, how they
  exfiltrated — built from farm output + dead-drop evidence.
- Starts with a 10-line executive summary, then per-persona sections
  (kept in `personas/` as `fbi-behavioral.md`, `red-team.md`,
  `army-intel.md`, `cryptographer.md`, `blue-team.md`).
- Every claim graded OBSERVED / INFERENCE. No ungraded verdicts.

## `FRESH.md` / `NOVELTY.md` — hunt result + novelty audit

- `FRESH.md`: new infrastructure finds, ranked; each with evidence
  (agent usage OBSERVED vs live-but-unseen), raw lane JSONs referenced.
- `NOVELTY.md`: per-find verdict NOVEL / REPORTED (with citation) /
  ADJACENT (reported class, our angle new). Scoreboard at the top.
  Research sources listed (web, social, Transluce DB, internal corpus).
  Falls get `[AUDIT: …]` annotations back in `FRESH.md`.
