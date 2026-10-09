# Hunt lane 4 — RubyGems API yanked-version residue — 2026-09-27

Question: the campaign gems were yanked, but does RubyGems' API still serve
any residue of them?

Method: read-only GETs at ~1/s, 10 campaign names probed
(`tryf3zz`, `southwarkssrfhack`, `londonyardtestabc`, `southfetchprobe42`,
`wandsworthprobe1778551714`, `zzsouthrunnerb`, `uxjinalamb2`, `slnleaker4`,
`yardbreakerxqh1778552850`, `q--00cfmapjson726`).

## Findings

| Endpoint | Yanked name | Never-existed name | Live control |
|---|---|---|---|
| `/api/v1/gems/<name>.json` | 404 "This rubygem could not be found." (10/10) | — | 200 + full metadata |
| `/api/v1/versions/<name>.json` | 404, same body (10/10) | — | 200 + version list |
| `/info/<name>` (compact index) | **200, empty YAML doc** (`---\n\n`, 4 bytes) | 404 "This gem could not be found" | 200 + full version data (~7 KB) |
| `/gems/<name>` (HTML page) | 200, "not currently hosted" notice | — | 200 + full page |

### The residue that survives

1. **Name reservation is visible via `/info/`.** A yanked name returns HTTP 200
   with an empty document, while a never-existed name returns 404. So the
   compact-index info endpoint distinguishes three states: live (data),
   yanked (empty 200), nonexistent (404). The names remain reserved —
   nobody can re-register them, and the reservation itself is detectable.

2. **The gem HTML page still renders** (`/gems/tryf3zz` → 200, ~34 KB) with the
   notice "This gem is not currently hosted on RubyGems.org. Yanked versions
   of this gem may already exist." It also still links the gem **owner's
   profile page** (handle observed; not visited — operator identity is out of
   scope).

3. **No metadata survives.** Descriptions, version lists, download counts,
   yanked flags, dependency data — all gone from every API endpoint. The old
   `/api/v1/dependencies` endpoint is deprecated entirely (404 + deprecation
   notice for live gems too).

## Verdict

RubyGems serves **no content residue** of yanked gems — no descriptions, no
versions, no metadata through any API surface. What remains is purely
structural: the reserved name (detectable via the `/info/` 200-vs-404
discriminator) and the owner profile link on the stub HTML page. For data
recovery purposes this lane is a dead end; Diffend and the Wayback Machine
remain the only sources of the yanked bytes/metadata.

Raw probe captures: `/tmp/rgapi/` (ephemeral).
