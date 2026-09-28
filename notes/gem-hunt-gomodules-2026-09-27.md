# Hunt Lane 10 — Go module index + pkg.go.dev (2026-09-27)

**Verdict: clean negative.** No GemStuffer campaign fingerprints in the Go module
index (May 1 – Jun 30, 2026) or pkg.go.dev search. The campaign's footprint
remains RubyGems-only.

## Method

- Queried the append-only Go module index (`https://index.golang.org/index?since=…`),
  paging `since` through the full May 1 – Jun 30, 2026 window in 8 parallel
  date-chunks (~1s between page requests per worker, read-only).
- Fingerprint regexes on module paths: 10-digit epoch runs, `try[a-z][0-9]zz`,
  `(^|/)zz`, `oai`, and `probe|proxy|fetch|yard|jina|go-import|moderngov|lambeth|`
  `wandsworth|southwark|county.json|builder.alive`.
- pkg.go.dev search for 7 markers: `tryf3zz`, `southwarkssrfhack`, `go-import
  r.jina.ai`, `builder alive`, `YARD RAN`, `wandsworthprobe`, `zzsouthrunner`.
- Index/metadata only — no module zips fetched.

## Results

- **pkg.go.dev: 0 modules** for all 7 marker queries ("Showing 0 modules with
  matching packages").
- **Index sweep:** [COVERAGE] module versions scanned, [MATCHES] raw pattern
  matches, triaged to zero campaign hits:
  - `try[a-z][0-9]zz` grammar: **0 hits** across the full window.
  - 10-digit epoch runs in repo names: 1 hit — `go.mongodb.org/atlas-sdk/v20250312021`
    (MongoDB's legitimate date-based SDK path). All other epoch-10 matches were
    pseudo-version timestamps (`v0.0.0-20260609014459-…`) or numeric GitHub user
    IDs in workers.dev proxy-mirror paths — benign.
  - `zz`-leading names: 14 hits, all legitimate users (`zzet/gortex`,
    `zzzhangjian/ai_pkg`, …).
  - `oai` substring: 77 hits, all AI-company names (`hanzoai`, `kudoai`, `h2oai`…)
    — benign.
  - `jina`: 2 hits — `songjinagjun/songprotos`, `tkrajina/sgf2img` (usernames,
    not r.jina.ai). **No r.jina.ai references in any module path.**
  - `go-import`/`goimport`: 11 hits — all legitimate Go tooling
    (`palantir/go-importalias`, `neilotoole/sq/tools/goimports-reviser`, …).
  - `yard`: 74 hits — `shipyard`/`dockyard`/`lanyard` projects, benign.
  - `builder`: 32 hits — Azure `agentbaker/vhdbuilder`, benign.
  - No `moderngov`, council names, `county.json`, `ssrf`, `exfil`, `webhook`,
    or `oast` in any module path.

## Notes

- `github.1485827954.workers.dev/…` appears as a Go module proxy mirror serving
  many modules — third-party infra worth knowing about, unrelated to the campaign.
- The go-import mechanism targeted Go *tooling behavior* (VCS confusion via
  `<meta name="go-import">` tags), not Go module publication — so the negative
  here is consistent with the campaign's RubyGems-native design.

## Caveats

- Module *paths* were swept; go.mod/README *contents* (where a laundering URL
  could hide) were not bulk-downloaded — out of scope for this lane.
- pkg.go.dev search is tokenized; short beacon phrases can't be matched literally.
