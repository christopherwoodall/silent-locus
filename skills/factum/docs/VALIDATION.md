# Deployment validation

## Status

**READY for the first synthetic-validated research-agent deployment.**
The complete external-host loop passed. This is not a production-scale or
cross-platform certification.

## Code and environment

- Base: `08183d4da30958cc056fffe649fe80aaff7f4643` (`dogfood`).
- Fixes, tests, examples, and documentation are local/uncommitted.
- Toolkit `0.2.0`; corpus format `2`; pack/lock format `1`.
- Ubuntu/WSL2, Linux `6.6.114.1-microsoft-standard-WSL2`.
- Git `2.43.0`; uv `0.10.4`.
- Isolated test Python `3.12.3`, SQLite `3.45.1`.
- filelock `3.32.7`, jsonschema `4.26.0`, referencing `0.37.0`,
  rapidfuzz `3.14.6`, pytest `9.1.1`, build `1.6.1`.

Dependencies and disposable hosts are under `/home/chris/factum-validation/`,
not the toolkit checkout or a real corpus.

## Executed checks

From `/mnt/c/Users/chris/Desktop/projects/factum`:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/chris/factum-validation/venv/bin/python \
  -m pytest -q -p no:cacheprovider \
  --basetemp /home/chris/factum-validation/pytest

PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 tools/smoke_test.py \
  --workspace /home/chris/factum-validation/smoke-first \
  > /home/chris/factum-validation/smoke-first-output.json

PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 tools/smoke_test.py \
  --workspace /home/chris/factum-validation/smoke-refreshed \
  > /home/chris/factum-validation/smoke-refreshed-output.json

PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 tools/smoke_test.py \
  --workspace /home/chris/factum-validation/smoke-final \
  > /home/chris/factum-validation/smoke-final-output.json
```

The final full suite had **130 passed in 94.80s**.
All three full installation smoke runs passed. Each exercised actual nested clones,
two-site synchronization through a local bare remote, exact bytes and strings,
custom schemas, pending recovery, concurrent retries, historical views,
submodules, wheel/sdist builds, and clean console installation. The refreshed
run also exercised isolated `uv tool install`. The final run checked real help
for 25 public command/action combinations, exercised note/query/template/lanes,
and proved historical catalogs exclude later schema additions. Both sites
converged to **35 records** and the same logical state digest.

Final runtime identity (SHA-256 over the sorted file-hash map for `scripts/`
and `pyproject.toml`):

```text
7ff5ba78b46981bef66234b76f4324d003722cd1c77a9c0efd2f011aa0834ff3
```

The full source inventory and archive checksum are in the release sidecar.
The source files, not the base commit alone, identify these uncommitted fixes.

All 17 Python source/test/tool files parsed successfully. `git diff --check`
passed; Git noted CRLF-to-LF warnings for toolkit source files. Installed corpus
pack bytes are separately protected by the tested `-text` rule.

Earlier regression runs intentionally failed: 59 passed/14 failed, then
29 passed/4 failed. One later full-suite collection failed due to an introduced
indentation error, which was corrected before the 127-pass run. No failed check
is counted as passing.

## Fixed defects

1. Schema inspection treated property names and example/default/constant data
   as schema keywords. It now visits only subschema locations.
2. Unsupported reference annotations under dependency/property-name and other
   unimplemented traversals were silently accepted. They now fail.
3. Managed directory symlinks could redirect writes before a later rejection.
   Ancestors and targets are checked before managed access.
4. Appending host Git rules normalized unrelated existing CRLF content.
   Appends now preserve original bytes.
5. Git normalized hash-pinned CRLF pack files, breaking clone/historical
   validation. Installed packs now receive `-text`.
6. Historical dispatch incorrectly required current corpus metadata.
7. Unknown search types returned `not_found` instead of failing.
8. Graph depth exhaustion could omit edges without truncation disclosure.
9. Receipts did not validate all returned record IDs.
10. Blob verification skipped inconsistent sizes on later same-hash
    acquisitions.
11. New parent directory entries were not consistently synced before durable
    publication. Atomic writes now sync newly created ancestors.
12. JSON Schema errors could echo raw submitted values. Diagnostics now retain
    schema paths and failed rules without those values.
13. The unused path helper imported a nonexistent error helper and had a stale
    asset path.
14. Architecture links and seed-asset paths disagreed with the actual layout.

Portable format, seed-pack content/IDs, fingerprints, and historical type
assignments are unchanged.

## Limitations and untested scenarios

- Synthetic small corpora only; no production-scale memory/latency benchmark.
- Full in-memory loading and SQLite rebuilds remain intentional.
- General ingestion checks locator structure, not every quote/selector.
- Fuzzy retrieval is heuristic, not an exhaustive absence test.
- Local-only bytes do not synchronize through Git. Missing bytes are disclosed.
- Format migration, pack replacement/uninstall, automatic source acquisition,
  and automatic Git publication are not implemented.
- Injected disk/permission/SQLite failures are deterministic tests, not
  physical power-loss or real disk-full experiments.
- Native Windows, macOS, network filesystems, and hostile concurrent filesystem
  replacement are untested. External Git changes must be serialized.
- Functional acceptance used Python 3.12.3. Python 3.11 and 3.14 were not
  functionally validated; 3.14 was used only for reconnaissance/help.
- The manual CI workflow requires a preconfigured Linux self-hosted runner;
  no GitHub CI run was performed.
- Public branch publication was not performed. A public clone URL cannot
  deliver the uncommitted fixes.

The source archive checksum and complete inventory belong in the release
sidecar, avoiding a checksum embedded in the archive it identifies.
