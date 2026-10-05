# Hunt Lane 14 — GitHub Actions / GitHub repos — 2026-09-27

**Verdict: negative.** No GitHub repos carry the campaign's name grammars, and no
operator workflow infrastructure surfaced. The Actions-logs angle needs candidate
repos; none exist.

## Method (read-only, no auth, ~11 API calls — well under the 60/hr limit)

- GitHub repo search API (`/search/repositories`) for exact campaign names:
  `tryf3zz`, `southwarkssrfhack`, `londonyardtestabc`, `southfetchprobe42`,
  `zzjina`, `yardbreaker` — **all total: 0**.
- `go-import in:name,description` — 3,019 hits, all legitimate Go tooling
  (`rsc/go-import-redirector`, `bradfitz/goimports`, godot importers). Noise.
- `builder alive in:name,description` — 25 hits, all generic builder-pattern
  projects. Noise.
- Date-boxed sweeps (May–Jun 2026): `oai in:name` (390, all legit OpenAPI/OAI
  projects), `r.jina.ai in:readme` (2,138, all legit Jina Reader usage),
  `probe in:name` May 11–13 (85, all ordinary).
- Web search `site:github.com "YARD RAN"` / `"HOOKED!!!!!!"` — zero results.
- Web search for go-import + gemspec + r.jina.ai surfaced only public
  reporting artifacts, not operator repos:
  - https://github.com/continuum-ai-corp/orca-ai-incident-archive/blob/HEAD/incidents/2026-09/2026-09-11-rubygems-gemstuffer.md
  - https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/second-swarm-trajectories-crosscheck.md
  - https://github.com/pranava0x0/vibe-coding-security/blob/HEAD/advisories/2026-09-openai-agents-rubygems-gemstuffer-campaign.md
  These are researcher writeups (useful context: 2,000+ pkgs May 11–12, 233 with
  "oai", 1,397 referencing r.jina.ai, RubyDoc.info RCE via .yardopts, SEC
  county.json June wave). Not operator infrastructure.

## Gaps / caveats

- GitHub **code search** (`/search/code`) requires authentication — literal
  content search for the beacon strings inside workflow files or run logs was
  not possible unauthenticated.
- grep.app (public code search, no auth) returned HTTP 429 to the fetch
  service; not retried per policy. That route remains open for a later pass.
- Actions workflow-run logs are only inspectable per-repo; with zero candidate
  repos there was nothing to inspect.

## Bottom line for the parent

GitHub holds no repo-level trace of the campaign under its own naming. If the
operator used GitHub Actions for compute, it was under unrelated names — the
beacon strings would be the way in, and that needs authenticated code search
or a working grep.app/Sourcegraph pass.
