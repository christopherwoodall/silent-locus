# Provenance — July-7 gem forensics (`data/july7-gem-forensics/`)

Date: 2026-09-28/29. Worker 2 of the off-task web-mechanism hunt.
Lane: July-7 gem forensics (XSS/SSTI reconstruction). Read-only throughout.

## What this dataset is

Forensic reconstruction of the July-7 RubyGems wave's third mechanism family
(XSS PoCs + SSTI probes in gem metadata). Two source tiers, kept separate:

1. **Our bytes** — `raw/` + `payload-reconstructions.jsonl`: read-only captures
   of Diffend (`my.diffend.io`) gem pages and version-diff pages for the 18
   `in_diffend=true` gems from the Lane-J sweep (`data/july7-wave/`). These are
   third-party test/security-researcher gems (NOT GemStuffer campaign gems —
   the campaign's named specimens are absent from Diffend, verified across the
   full 264-name re-sweep), but 5 carry real XSS payloads in their Diffend
   metadata bytes and all 18 are timestamped inside the July-7 window.
2. **JFrog report text** — `campaign-specimens-jfrog.jsonl`: payload
   reconstructions for the 7 named GemStuffer campaign specimens, quoted from
   the JFrog Security Research writeup
   (https://research.jfrog.com/post/gemstuffer-openai-rubygems/, fetched
   2026-09-28). Marked `source: jfrog-report-text` — these are NOT locally
   captured bytes. No campaign gem yielded bytes anywhere in our holdings
   (0 hits in `rubygems-goimport-campaign` and `july7-wave` ES for the payload
   strings and gem names).

## Method

- Fetch: `scripts/july7_forensics_fetch.py` — curl GETs to
  `https://my.diffend.io/gems/<name>` and `/gems/<name>/<version>` only,
  4s pacing, 3-attempt backoff. 50/50 captures OK. **Never executed, never
  rendered in a browser; no HTTP to exfil endpoints (oast.online,
  webhook.site); no DNS beyond normal resolution.**
- Extraction: `scripts/july7_forensics_extract.py` — HTML tags stripped,
  entities unescaped (by inspection), marker-centered line extraction.
  Full lines preserved; nothing truncated silently (lines capped at 4000
  chars in JSONL).
- Manifest: `raw-manifest.json` (per-file SHA-256 of raw captures) and
  `SHA256SUMS` (all dataset files).

## Inventory

| File | Records | Source |
|---|---|---|
| `raw/` (50 HTML captures) | 18 gems × (index + version diffs) | Diffend, 2026-09-29 |
| `payload-reconstructions.jsonl` | 50 capture records | our extraction |
| `campaign-specimens-jfrog.jsonl` | 7 specimens | JFrog report text |
| `PROVENANCE.md` | this file | — |
| `SHA256SUMS` | manifest | — |
| `raw-manifest.json` | 50 entries | — |
| `progress.log` | run log | — |

## Key facts established

- ES index `july7-wave` holds **264 docs** (verified `_count`; the task brief's
  "296" was stale — corrected 2026-09-28).
- July-7 campaign wave per JFrog: 215 packages / 333 releases,
  2026-07-07 03:03:09–18:13:42 UTC.
- Campaign XSS: stored in gem metadata (author/description/homepage), never
  reflected. Campaign SSTI: ERB + EL + pct-encoded ERB in the author field —
  **no Jinja2 `{{7*7}}` anywhere observed**.
- Author conventions: May wave = `x`, `a`, `d`, `tmp`, `oai`, `research`, `SR`;
  July campaign = `Testing <Animal>` (Testing Buffalo, Testing Wolf, Test
  Rhino per JFrog), `John Doe`, and payload-as-author.

## Constraints honored

- Agents/infrastructure only; no human/operator attribution pursued.
- No credentials reproduced. No absolute home-directory paths in docs.
- Hosted Elastic write freeze respected: this dataset is disk + git only;
  no ES ingest was performed by this worker.
