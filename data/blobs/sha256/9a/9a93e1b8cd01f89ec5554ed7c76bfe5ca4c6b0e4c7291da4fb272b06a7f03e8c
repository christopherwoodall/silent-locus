# Hunt lane 2 — deps.dev — 2026-09-27

**Verdict: dead end. deps.dev retains nothing for the yanked campaign gems.**

## Method
Read-only GETs against the deps.dev v3 API at ~1.2s pace, 2026-09-27:
- `GET https://api.deps.dev/v3/systems/RUBYGEMS/packages/<name>` — 10 campaign
  names + 2 controls
- `GET .../packages/southfetchprobe42/versions/0.0.3` — version-level confirmation
- RubyGems API (`rubygems.org/api/v1/gems/<name>.json`) as yank-state control

## Results

| name | deps.dev package | deps.dev version | rubygems.org |
|---|---|---|---|
| tryf3zz | 404 | — | 404 |
| southwarkssrfhack | 404 | — | — |
| londonyardtestabc | 404 | — | — |
| southfetchprobe42 | 404 | 404 (v0.0.3) | 404 |
| wandsworthprobe1778551714 | 404 | — | — |
| zzsouthrunnerb | 404 | — | — |
| uxjinalamb2 | 404 | — | — |
| q--00cfmapjson726 (Jun-18 wave) | 404 | — | — |
| oaitest1778473828 (rehearsal) | 404 | — | — |
| probejiqptzco (tuned 6x) | 404 | — | — |
| rake (control) | 200 — 96 versions | 200 (v13.0.0) | 200 |
| json (control) | 200 — 136 versions | — | — |

Every campaign gem 404s at both package and version level. Controls return
full records, so the API path is healthy — the 404s are gem-specific.

## Interpretation
deps.dev builds its package graph from registry snapshots. The May-12 gems were
yanked within hours of publication (May 12–13) and the June-18 wave likewise —
almost certainly before any deps.dev snapshot captured them, so they never
entered the graph. Unlike rubydoc.info (which at least had build workers to
exploit), there is no evidence these gems ever existed in deps.dev's data.

Comparison with other sources:
- **Diffend** (my.diffend.io/gems): full diffs + metadata for the May corpus —
  still the primary source.
- **Wayback Machine**: pre-removal rubygems.org metadata for 4 June-18 gems —
  secondary source.
- **deps.dev**: nothing. Not even version stubs.
- **rubydoc.info**: 404s, nothing preserved.

## Notes
- Advisory endpoints were not queried; no OSV/GitHub advisory is known to
  reference these gem names (public intel lane found none).
- Raw probe output: `/tmp/depsdev_results.json` (ephemeral).
