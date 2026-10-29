# factum-behavior/1.0.0 — usage examples

Pack purpose: first-class `model` and `harness` observable nodes plus a
derived-layer profile container (`intel.behavioral_profile`) with mandatory
derivation provenance, for behavioral edges between models.

Type names: `model`, `harness` (observables); `intel.behavioral_profile`
(observation). No new predicates; reuse core `related_to`, `derived_from`,
`sighting`, `ngram`/`term`.

## Pattern: per-(model, harness) command-histogram profile

1. Submit a `source` record and a `model` observable (byte-exact string,
   e.g. `claude-opus-4-6@anthropic`) and a `harness` observable (e.g.
   `claude-code`).
2. Submit an `intel.behavioral_profile` observation with `profile_kind`,
   `markers` (marker → count), and the mandatory `derivation` block.
   `eval_only: true` marks benchmark/eval sources — never incident evidence.
   `scaffold_stripped: true` records that harness boilerplate was removed
   before profiling.
3. Attach each marker as a `ngram`/`term` observable with a `sighting`
   on the profile. Sighting locators MUST reference an artifact attached
   to the profile observation's `files` array (`files: [{"artifact": ...}]`),
   or submit fails with "Sighting artifact is not attached to the
   observation". Sighting `locator` is an object like
   `{"artifact": "@file", "whole": true}` — a bare string fails validation.
4. Write explicit `related_to` edges: `model` → profile, `harness` →
   profile. `graph` traverses ONLY edge records — sightings alone do NOT
   make model→profile graph-reachable.
5. Behavioral edges between models: `related_to` edge profile↔profile
   (basis + cites required on interpretive edges), giving
   modelA → profileA → profileB → modelB traversal.

## Example (disposable-corpus test, 2026-10-11)

```json
{"kind": "observable", "body": {"type": "model", "value": "claude-opus-4-6@anthropic"}, "tags": {"lane": "behavioral-schema-test"}}
{"kind": "observable", "body": {"type": "harness", "value": "claude-code"}, "tags": {"lane": "behavioral-schema-test"}}
{"kind": "observation", "body": {
  "type": "intel.behavioral_profile", "source": "@src", "files": [{"artifact": "@file"}],
  "observed_at": "2025-12-09T07:18:54Z", "time_basis": "source_metadata",
  "data": {"profile_kind": "command_histogram", "model": "claude-opus-4-6@anthropic", "harness": "claude-code",
    "markers": {"cat": 8586, "cd": 8309, "python3": 6536, "apt-get": 2189},
    "derivation": {"dataset_uri": "https://huggingface.co/datasets/yoonholee/terminalbench-trajectories",
      "dataset_locator": "train-00000-of-00002.parquet rows 0-2999",
      "extraction_method": "first-token histogram over steps[].tools[].cmd",
      "model_version_window": "claude-opus-4-6@anthropic, 2025-12 runs",
      "expires_after": "2027-01-11", "eval_only": true, "scaffold_stripped": true},
    "provenance": "synthetic test slice"}},
 "tags": {"lane": "behavioral-schema-test"}}
```

Test result: 14-record bundle accepted; `graph <modelA> --depth 4` →
5 nodes / 4 edges reaching a second model through the shared-marker
profile chain. Negative test: profile without `derivation` rejected
(`urn:factum:behavior:profile:1/: validation failed (required)`).
