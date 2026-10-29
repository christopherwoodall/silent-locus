# urlscan.io sweep

Finishes the urlscan.io query sweep for the "what has Transluce missed"
hunt. The prior lane (`../hot-leads/`) ran 22 queries; 1 succeeded
(`filename:county.json` → 16 Ramsey County noise hits) and 21 were
403-blocked mid-probe. The block later lifted, so this lane reruns every
unrun planned query plus IOC follow-ups (`zz=oai`, `openai_research`
variants, DoE API shapes, exact SEC path).

- `sweep.py` — rerunnable curl-based script (urllib, keyless API). Idempotent
  via `state.json` (queries keyed by exact string; reruns skip done ones).
  Polite: 4s pacing; hard stop on 2 consecutive 403/429.
- `data/query-log.jsonl` — every query: exact string, note, http code,
  result count, up to 8 examples (uuid, task_url, page_url, date), or the
  error / honest zero.
- `data/raw/qNN.json` — full API response for queries with results.
- `SWEEP-REPORT.md` — findings.

Run: `python3 sweep.py`
