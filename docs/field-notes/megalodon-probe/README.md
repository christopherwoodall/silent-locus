# Megalodon probe

Read-only curl probe of Megalodon (megalodon.jp) gyotaku lists for Transluce-incident URLs.

- `probe.py` — idempotent, polite (2s pacing), logs every lookup to `data/probe-log.jsonl`, state in `state.json`.
- Native lookup used: `GET /pc/main?url=<url>`. Free-word search on the homepage is just Google site-search (not native); per-URL list is the native index.
- Run: `python3 probe.py`
