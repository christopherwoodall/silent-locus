# Hunt lane 7 — other doc build pipelines — 2026-09-27

**Question:** GemStuffer got RCE on RubyDoc.info's YARD build workers via crafted
`.yardopts`. Did the same exploit class get worked against other doc pipelines
(docs.rs, pkg.go.dev, readthedocs.org), and do their traces sit there?

**Method:** read-only searches, ~1/s pace, no logins. crates.io API (backs the
docs.rs index), pkg.go.dev search, readthedocs.org API v3 search. Patterns:
campaign voice phrases (`"builder alive"`, `"YARD RAN"`, `"yard exploit"`),
payload markers (`go-import`, `r.jina.ai`), target markers (`modern.gov`,
`sec.gov/files/county.json` → `county.json`), and name grammars
(`tryf3zz`, `zzjina*`).

## docs.rs / crates.io

| query | result |
|---|---|
| `go-import` | 1 hit: `use-go-import` — **checked, negative**. Legitimate crate ("Go import metadata primitives for RustUse"), published 2026-05-24 by long-standing GitHub user `CloudBranch` (Joshua Whalen, account since 2016). docs.rs page shows clean validated-import-path library code. Timing (12 days post-burst) is coincidence. https://docs.rs/use-go-import / https://crates.io/crates/use-go-import |
| `r.jina.ai` | 1 hit: `nab` — **negative**. Legitimate "token-optimized HTTP client for LLMs" (github.com/MikkoParkkola/nab); the reader-proxy mention is docs context, not a payload. |
| `"builder alive"` | 589 tokenized results, all noise (embassy-supervisor, talk-rs, etc.) — crates.io does not do exact-phrase matching; no campaign trace. |
| `"YARD RAN"` | 8 results, all token noise (switchyard, yardlet, zshrs…) — negative. |
| `"yard exploit"` | 0 results. |
| `modern.gov` | 0 results. |
| `county.json` | 0 results. |
| `tryf3zz` | 0 results. |
| `zzjina` | 0 results. |

docs.rs builds docs for yanked crates too, so the name searches cover the
yanked-but-documented case — nothing matching the campaign grammars exists.

## pkg.go.dev

| query | result |
|---|---|
| `go-import` | 25 modules, all legitimate vanity-import tooling (searKing/golang go-import vanity server, importgen, goimportgraph, govanityurls…) — negative. |
| `"builder alive"` | 0 modules. |
| `"YARD RAN"` | 0 modules. |
| `r.jina.ai` | 0 modules. |

## readthedocs.org (API v3 search)

| query | result |
|---|---|
| `go-import` | 0 projects. |
| `"builder alive"` | 0 projects. |
| `"YARD RAN"` | 0 projects. |
| `r.jina.ai` | 0 projects. |

## Verdict

**No GemStuffer-class traces found on docs.rs, pkg.go.dev, or readthedocs.org.**
The two near-misses (`use-go-import`, `nab`) were both investigated and are
legitimate projects with established authors. The operator's doc-pipeline
exploitation appears confined to RubyDoc.info — consistent with the campaign's
RubyGems-native design (YARD is the Ruby documentation toolchain; the other
pipelines serve different ecosystems the campaign never touched).

## Caveats

- crates.io search is tokenized, not exact-phrase: short voice phrases
  (`"builder alive"`) cannot be matched literally; the distinctive markers
  (`go-import`, `r.jina.ai`, `modern.gov`, `county.json`, `yard exploit`) and
  name grammars are the reliable signals, and all returned zero.
- A crate/module whose payload lives only in build scripts or non-indexed
  README text would not surface in these searches. Content-level sweeps would
  require bulk downloads, out of scope for this lane.
- docs.rs `use-go-import` (2026-05-24) is worth one line in the timeline as a
  coincidence, not a lead.
