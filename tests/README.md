# tests — offline regression suite

Pure-unittest regression checks; no network, no live services. Run from the
repo root.

## Coverage

| File | What it checks |
|---|---|
| `test_canonical_ingest.py` | Registry-driven staged ingest produces canonical event records |
| `test_corpus_loader.py` | Strict registered-corpus ingestion (schema, rejection of unregistered corpora) |
| `test_script_layout.py` | Preserved build-script layout (collection scripts live in their event dir, multi-event parsers in `scripts/`) |
| `test_shortener_event_fingerprints.py` | Fingerprint invariants for the canonical shortener event slice (hashes stable across rebuilds) |
| `test_swarmtraces_ingest.py` | SwarmTraces source validation and Elastic response handling |
