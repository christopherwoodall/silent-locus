# Script inventory

Run only the maintained entrypoints at `scripts/`: `push_to_local_es.py`,
`es_ingest_swarmtraces.py`, `validate_schema.py`, `validate_collections.py`,
`verify_checksums.py`, and `gen_dataset_card_table.py`.
`local_es_manifest.json` is loader configuration; the canonical ingest test
is maintained with the test suite. The three historical dataset-specific
loaders (`es_ingest_wiki.py`, `es_ingest_jsonhero.py`,
`es_ingest_powerbi.py`) now live under their owning collections'
`raw/scripts/legacy/` directories, not at this root.
The historical cross-collection
`archive/es/es_ingest_university_shorteners_consolidated.py` implements a
**consolidated** index and must not be mistaken for the canonical
explicit-events loader. Its `--retire` path deletes an index.
Any ES ingest is a write operation: inspect the target before running.

`builders/build_timeline_anchors.py` and
`builders/gem83_reconciliation_build.py` derive outputs from multiple
collections. Their repository-root resolution was updated for this location.
`maintenance/audit_collections.py` is a historical read-only audit.
`maintenance/checksum_sweep.py` **rewrites collection manifests on import**;
it is not the verification command. Use `make verify-checksums` to inspect
integrity without rewriting recorded hashes.

The ten historical single-collection builders formerly staged in `builders/legacy/`
are now co-located with their collections. This is a preservation move, not
a rebuild: **do not run these historical scripts** against canonical collections;
most can overwrite existing outputs or raw evidence. The university-shorteners
explicit-events builder is an exception only in that it rejects the canonical
events file and existing output paths. Each collection’s `PROVENANCE.md`
documents its relocated builder and historical limitations.

See `archive/README.md` for the historical collector lanes, migrations,
ES/Kibana tooling, and execution warnings. Nothing in the archive is part of
the maintained workflow.
