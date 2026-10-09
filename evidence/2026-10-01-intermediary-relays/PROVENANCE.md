# PROVENANCE — data/2026-10-01-intermediary-relays/

Lane 3 of 4 (2026-10-01): markdown.new + intermediary conversion services.
Collection worker for the Transluce us-canada-gov pivot. Read-only /
observational; no invented IDs; agents/infrastructure only.

## What was collected

- `WRITEUP.md` — service-class writeup: per-relay keyless status, public
  logs, URL scheme, graded agent-use evidence; full-indicator census;
  relay scores by co-occurring indicator count; burst-timing join keys.
- `sweep_v3.py` — the sweep (kept; v1/v2 retained per keep-all, superseded).
- `sweep_indicators.py`, `sweep_v2.py` — superseded iterations (v1 killed
  by a service restart mid-run; v2 hit Python-regex blowup on long lines).
- `sweep_results.json` — census (lines/files per indicator), relay_scores
  (distinct indicators, line matches, per-indicator co-occurrence),
  ts_samples (≤40 @timestamp samples per relay).
- `sweep_samples.jsonl` — ≤3000 evidence samples (≤600 chars each).
- `sweep_summary.txt` — stdout JSON summary of the final run.
- `sweep_stderr.txt` — run log (includes EXIT code).

## Sources (all read-only)

- Live fetches 2026-10-01 ~20:18–20:30 UTC: https://markdown.new/
  (homepage), https://markdown.new/https://example.com (benign test
  conversion #1), https://markdown.new/https://example.com?format=json
  (benign test conversion #2), https://markdown.new/crawl,
  https://pure.md/ (homepage). No other submissions; ≤2–3 benign
  conversions as briefed.
- On-disk corpora under `~/workspace/silent-locus/data/` (pre-existing;
  sibling `data/2026-10-01-*` lanes excluded from the census).
- Read-only reads of the frozen archive
  `~/workspace/muse-home/projects/swarmtraces-hf-corpus/elastic-exports/urlquery-incidents-20260928T022324Z.jsonl.gz`
  (11 markdown.new reports extracted with submission timestamps).
- Prior notes: transluce-us-canada-gov-2026-10-01.md,
  cors-bwa-proxy-2026-09-28.md, proxy-primitives-2026-09-27.md,
  nsi-venue-sweep-2026-09-28.md, gem-hunt-wiki-ioc-pivots-2026-09-27.md.

## Method notes

- Stage 1 (ripgrep): per-indicator matching-line and file counts over
  text files (`*.jsonl`, `*.jsonl.gz`, `*.txt`, `*.csv`, `*.md`,
  `*.json`, `*.html`, `*.log`), `-z` for gz. Stage 2 (Python): only
  relay-mentioning lines scored for co-occurring indicators; lines
  truncated to 20KB before regex to avoid blowup (full lines remain in
  sources; noted in WRITEUP).
- Known census blind spot: the `double_slash` lookbehind pattern is not
  supported by ripgrep's default engine → 0 lines in the rg census; the
  Python pass (which supports lookbehind) found the hits; verified
  separately with zgrep (124× `//www.sec.gov//files//county.json` etc.).
- `1970-01-01` timestamps in samples are `dir_date_prefix` placeholders,
  not real events.
- Keep-all + annotate: no records dropped; superseded scripts kept;
  sibling-lane exclusion documented above rather than silently applied.

## Gaps

- r.jina.ai live keyless status not re-verified (sandbox fetch policy
  blocked the probe; do not retry per runtime instruction).
- md.succ.ai keyless status not live-probed (deployment-dependent;
  self-hostable open-source).
- The 17–18 jsonhero.io doc IDs remain unfetched (prior deliberate
  deferral, unchanged).
