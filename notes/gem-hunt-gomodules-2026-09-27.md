# Hunt Lane 10 — Go module index + pkg.go.dev (2026-09-27)

**Verdict: clean negative.** No GemStuffer campaign fingerprints in the Go module
index (May 1 – Jun 30, 2026) or pkg.go.dev search. The campaign's footprint
remains RubyGems-only across every lane.

## Method

- Queried the append-only Go module index (`https://index.golang.org/index?since=…`),
  paging `since` through the full May 1 – Jun 30, 2026 window in 8 parallel
  date-chunks (~1s between page requests per worker, read-only). Coverage was
  continuous from 2026-05-01T00:00:00Z through 2026-06-30T23:59:59Z (chunk tails
  extended slightly past both edges; results filtered to the exact window and
  deduplicated by (Path, Version)).
- Fingerprint regexes on module paths: 10-digit epoch runs, `try[a-z][0-9]zz`,
  `(^|/)zz`, `oai`, and `probe|proxy|fetch|yard|jina|go-import|goimport|moderngov|`
  `lambeth|wandsworth|southwark|county.json|builder|webhook|ssrf|exfil|oast`.
- pkg.go.dev search for 7 markers: `tryf3zz`, `southwarkssrfhack`, `go-import
  r.jina.ai`, `builder alive`, `YARD RAN`, `wandsworthprobe`, `zzsouthrunner`.
- Index/metadata only — no module zips fetched.

## Results

- **pkg.go.dev: 0 modules** for all 7 marker queries ("Showing 0 modules with
  matching packages").
- **Index sweep:** ~2.91M module versions scanned, 35,014 raw pattern matches,
  32,766 unique (Path, Version) pairs triaged → **zero campaign hits**:
  - `try[a-z][0-9]zz` grammar: **0 hits** across the full window.
  - 10-digit epoch runs in final repo-name components: 24 hits — all benign:
    MongoDB Atlas SDK date-version paths (`go.mongodb.org/atlas-sdk/v20250312019`,
    `/v20250312020`, `/v20250312021`), `danielvt914/zzaps`, `zznewclear13/
    zznewclear13.me`, `zzquant/zzshare`. Remaining epoch-10 matches were
    pseudo-version timestamps (`v0.0.0-20260609014459-…`) or numeric GitHub user
    IDs in workers.dev proxy-mirror paths — benign.
  - `zz`-leading names: 186 hits, all ordinary usernames/projects
    (`zzet/gortex`, `zzzhangjian/ai_pkg`, `zzingobomi/…`, `zzquant/…`, …).
  - `oai` substring: 2,013 hits, all AI-company names (`hanzoai`, `kudoai`,
    `h2oai`, `smooai`, `groai-fi`, `loaiabdalslam` username, …) — benign.
  - `jina`: 126 hits — `jina-ai` org repos (`jina-ai/reader`, `jina-ai/
    late-chunking`, `jina-ai/hubble-client-python`) and usernames
    (`tkrajina/sgf2img`, …). **No r.jina.ai or s.jina.ai references in any
    module path.**
  - `go-import`/`goimport`: 83 hits — all legitimate Go tooling
    (`palantir/go-importalias`, `neilotoole/sq/tools/goimports-reviser`, …).
  - `yard`: 490 hits — `shipyard`/`dockyard`/`switchyard`/`lanyard` projects,
    benign.
  - `builder`: 254 hits — Azure `agentbaker/vhdbuilder`, benign.
  - `moderngov`: 7 hits — LocalGov Drupal's legitimate `localgovdrupal/
    localgov_moderngov` (+tpl) and `afdy/moderngov` (proxy metadata: latest
    version 2022-11-26, a pre-campaign relic). Benign.
  - `lambeth`: 16 hits — Lambeth Council's own `lambethcouncil/opencouncil`,
    `lambethcouncil/lambeth2`. Benign.
  - `southwark`: 39 hits — `domdfcoding/southwark` (proxy metadata: v1.0.0
    tagged 2025-12-10, predates the campaign; author is a known prolific dev).
    Benign.
  - `webhook`: 7 hits — `mister-webhooks/sts-assume-role-proxy`,
    `opendevstack/ods-core/jenkins/webhook-proxy`. Benign tooling.
  - No `wandsworth`, `county.json`, `ssrf`, `exfil`, `oast`, council domains,
    "builder alive", or "YARD RAN" in any module path.

## Pattern-level triage (family shape, not exact phrases)

Per the standing guidance to hunt by pattern, the full 32,766-pair match set was
re-swept for campaign-family grammar beyond exact names:

- Animal-name paths ("Testing \<Animal\>" family): 44 hits — all ordinary
  (`apecloud/kubeblocks`, `aperturerobotics/*` via the workers.dev mirror,
  `FoxDen/uds-proxy`). Testing×animal combos: **0**.
- `A000`/`ZZEND` markers, `oast`/`webhook.site` callbacks, `/api/v1/` paths in
  module names: **0 each**.
- `try`+letter+digit broader grammar: **0**. 10-digit runs adjacent to `zz`:
  **0**. Numeric-only final path components: **0**.
- probe/fetch/ssrf paths co-occurring with a family marker (zz/oai/jina/epoch/
  council): 91 pairs — all benign (`to1zzz/unicornfetch` — neofetch-style tool,
  `SmooAI/fetch` — AI-company fetch library).
- Christopher's word-part watchlist (hack/root/fossil/999/dlx): 9 hits — k8s
  `hack/goimports` script dirs, `xerneas3318/hackfetch` (sysinfo tool),
  `jargonautical/moderngov-hacking` (proxy metadata: version from **2017**,
  pre-campaign relic).
- Content patterns (`<meta name="go-import">` with hg/fossil/git/bzr/svn values,
  r.jina.ai/s.jina.ai URL shapes) live in file *contents*, not module paths —
  not observable from index data (module zips out of lane scope). Zero
  r.jina.ai/s.jina.ai references in any of the 32,766 module paths.
- Author patterns ("Testing \<Animal\>"): the Go module index exposes no author
  field — not checkable from this source.

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

## Provenance

- Raw match data: `~/workspace/tmp-gomod/matches_1..8.jsonl` (32,766 unique
  matches), crawler `~/workspace/tmp-gomod/chunk.py`, triage
  `~/workspace/tmp-gomod/final_triage.py`.
- Sweep completed 2026-09-28 ~04:27 UTC after two VM reboots; workers were
  resumed from durable progress files with append-mode match files, coverage
  verified continuous across the full window.
