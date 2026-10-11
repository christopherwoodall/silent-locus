# Dork hunt — Google-dork matrix over the shared IOC word list

BigSexyWarlock69's idea: advanced search operators + word-list terms to find
agent traces on surfaces search engines index.

## Method
- `run_dorks.py` — curl-based runner against DuckDuckGo's html endpoint
  (BigSexyWarlock69 prefers automation). Stateful + idempotent: re-running
  resumes from `data/dork-log.jsonl` (already-logged exact query strings are
  skipped). `--fidelity` runs the 6-dork operator check; `--limit N` caps a run.
- Fidelity gate: the backend must honor `site:` / `inurl:` / quotes (verified
  2026-10-03: `inurl:county.json sec.gov` restricts to sec.gov hosts vs the
  bare query; `site:` and quotes change result sets appropriately).
- Every dork is logged: exact query string, backend, path (curl vs
  browser.search), status, hit count, top-3 examples, or honest zero.
- Fallbacks: `browser.search` for anything curl can't reach; live-browser
  (Bing/DuckDuckGo) if a backend ignores operators entirely.

## Layout
- `data/dork-log.jsonl` — one row per dork (the log of record)
- `state.json` — progress counters, backend, fidelity verdict
- `run_dorks.py` — the runner
