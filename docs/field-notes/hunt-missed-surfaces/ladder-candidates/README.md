# Ladder candidates — probe lane

Read-only curl probes of the 5 new relay/proxy candidates surfaced by the
skill-ladders lane (`../skill-ladders/REPORT.md`).

- `probe.py` — rerunnable, idempotent (`state.json`), polite (2s pacing),
  logs every request to `data/probe-log.jsonl`. No accounts, no API keys,
  no content-creating submissions. The single live proxy fetch is a
  read-only GET of a public government JSON file to verify documented
  URL grammar.
- `PROBE-REPORT.md` — per-surface verdicts.

Run: `python3 probe.py`
