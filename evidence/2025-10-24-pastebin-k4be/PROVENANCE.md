# PROVENANCE — pastebin.k4be.pl agent-swarm paste dataset

Separate dataset. Not part of collusion-wiki.

## Source

- Texts from the public investigation export `agent-logs/pastebin-k4be/`
  of [JoshuaDavid/WikiAgentSwarmInvestigation](https://github.com/JoshuaDavid/WikiAgentSwarmInvestigation)
  (branch `main`, retrieved 2026-10-05; files `revisions.jsonl`, `manifest.json`,
  `README.md` read from `raw.githubusercontent.com` — read-only fetch of a
  public corpus; the paste hosts themselves were never probed).
- Their export: direct scrape of `https://pastebin.k4be.pl` on 2026-09-07
  (322 non-private unexpired pastes at scrape time), filtered to 198
  agent-swarm-surface pastes: 126 shellac-imported (`inclusion_reason:
  "shellac_import"`) + 72 subagent-classified (51 `swarm`, 21 `unclear`
  verdicts; 124 human-labelled pastes excluded from their export).
- Time span per stikked `created`: 2025-10-24 → 2026-09-05.

## Method

- Bodies extracted verbatim from the investigators' `revisions.jsonl`
  `body` fields (`body_encoding: raw_utf8` on all 198).
- One file per paste: `raw/<pid>.txt` (UTF-8 body, unmodified).
- `raw/manifest.jsonl`: per-paste id, title, retrieval timestamp,
  joshuadavid verdict/inclusion metadata, verdict rationale/confidence,
  label attribution, body-availability, Wayback fields (n/a on this host),
  external-overlap annotation, investigator body SHA-256 vs local body
  SHA-256 (`body_sha256_matches_jd` — all 198 matched).
- `events.jsonl`: 198 `relay_paste` records, fingerprint identity string
  `k4be-paste:<paste_id>` (sha256 hex). `@timestamp` = stikked `created`
  (uncorroborated — investigators do not independently verify it);
  `labels.timestamp_source = "labels:paste.jd_time"`.
- `rollup.jsonl`: 24 rows x `paste_day_burst` — per-day paste bursts over
  2025-10-24 → 2026-09-05; identity string `k4be-paste-day:<day>`.
- `SHA256SUMS`: whole-tree sha256sum-style, verified with `sha256sum -c`.
- `scripts/validate_schema.py`: 0 violations.

## Keep-all policy

Nothing dropped; all 198 bodies carried verbatim, including the 21
`unclear`-verdict rows (jd labels them; downstream precision filters
should use `labels."paste.jd_verdict" != "unclear"`). Failures would be
recorded in the manifest, not silently omitted.

## Caveats

- Investigator-selected subset ("agent-swarm output"), not a site census;
  classifier deliberately errs toward inclusion.
- Authorship: stikked colour+animal default names are not attribution.
- `ip16` null everywhere (endpoints expose no IPs); no reply-diff hunks.
- Bench-answer bodies (EPL relegation tables, Roi Et TH45 stats) are
  agent benchmark/test artifacts, not human correspondence.
- Live site not checked by this lane (read-only corpus ingest).

## Cross-host notes (2026-10-05 lane-1 reconciliation)

- Markers exclusive to this host in the combined corpus: `PAD\d+x\d+`
  titles (70), `TEL\d{6,}` (17), `TK\d{5,}` (6), `CLICKMAYBE` (17),
  `URLMARK` (1), `FRAMEK4` (2), `jqp.vercel.app/api/v0` (10),
  `bullfincher.io/sec-proxy` (3), `md.succ.ai`/`pure.md` (1 each),
  `2md.link` (7), `telegra.ph/Test-Link` (17), `URLTEST\d` (3), `linktry\d` (1).
- Shared with paste.linuxiarz: `is.gd` (7/13), `thecolony.ai/for-agents`
  (1/8), stikked `Re:` reply chains (3/32).
- `jina`, `zz=`, `webhook`, `oai` tags: zero hits on this host.
