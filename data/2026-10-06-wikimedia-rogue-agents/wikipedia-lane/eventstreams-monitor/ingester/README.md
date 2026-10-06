# eventstreams-monitor / ingester

Offline-built SSE ingestion component. **BUILD ONLY — never executed against
the live stream during development; no network on import, no cron/systemd.**

## Design decisions (made without DESIGN.md; adjust if it says otherwise)

- **Transport split:** `curl -N -s <stream-url> | python3 process.py`.
  Python HTTP stacks break on this VM's egress proxy (TOOLS.md); curl works.
  `process.py` reads stdin only — provably network-free (tests import it).
- **Rotation by event time, not wall clock:** hour files derive from the
  event's own `timestamp`/`meta.dt`, so replays land in the correct hour.
- **No redaction:** raw event JSON stored verbatim (standing rule).
- **Graceful shutdown:** trap kills curl; the processor's `finally` block
  flushes/closes the current hour file before exit. No partial-line risk —
  curl emits complete lines and the processor only writes whole JSON lines.
- **Backoff:** 2s × 2, capped at 300s, no jitter (operator's problem).

## Files

| file | role |
|---|---|
| `ingest.sh` | entry point; `--dry-run` validates config, prints plan, touches no network |
| `process.py` | stdin SSE line processor; import-safe, unit-tested |
| `config.example.yaml` | copy to `config.yaml`; every knob commented |
| `tests/test_process.py` | offline fixture tests (`python3 tests/test_process.py`) |
| `tests/fixtures/*.sse` | hand-written fixtures (labeled; NOT real stream data) |

## Usage (operator only)

```bash
cp config.example.yaml config.yaml   # edit
./ingest.sh --dry-run                # validate, no network
./ingest.sh                          # connect (NEVER during build)
```

Output: `<out_dir>/raw/YYYY-MM-DD/HH.jsonl` (UTC), one JSON event per line.
