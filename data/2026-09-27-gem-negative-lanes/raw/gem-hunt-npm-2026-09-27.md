# npm hunt — GemStuffer tradecraft, other registry — 2026-09-27

Lane 6 of 7. Question: does the GemStuffer operator class's tradecraft
(metadata poisoning, go-import tags, dead-drop beacons, name grammars)
appear in npm? Read-only: npm registry search API + package metadata
endpoints, ~1/s pace, no installs, no logins.

## Pattern pack used
`<meta name="go-import">` in descriptions/readmes; epoch-suffixed names;
`try[a-z][0-9]zz` grammars; `zz*`/`oai*` prefixes; `*probe*`/`*proxy*`/`*fetch*`
test names; beacons "builder alive", "YARD RAN", "yard exploit";
`r.jina.ai`/`s.jina.ai` URLs; UK council `modern.gov` and
`sec.gov/files/county.json` references.

## Result: NEGATIVE — no campaign fingerprints on npm

### 1. Search battery (19 queries, registry.npmjs.org/-/v1/search)
- Campaign-specific names — **total=0** for all: `zzjinavcs`, `tryf3zz`,
  `southwarkssrfhack`, `southfetchprobe42`, `londonyardtestabc`,
  `wandsworthprobe`, `slnleaker`, `yardbreaker`, `chatoaifetch`.
- `modern.gov` — **total=0**. No npm package mentions it.
- `r.jina.ai` — 20 hits, all legitimate Jina AI Reader/MCP ecosystem tools
  (mcp-jina-reader, pi-search-hub, multifetch-mcp, osint-agent-mcp, …).
- `jina.ai` — 53 hits, same legitimate ecosystem.
- Beacon strings (`builder alive`, `YARD RAN`, `yard exploit`) and
  `go-import` — only fuzzy keyword noise. npm's search API tokenizes, so
  "go-import" matches "imports", "builder alive" matches any builder +
  alive. Top results are mainstream packages (html-escaper, react-icons,
  storybook builders). No campaign-shaped hits in the top 60 of any query.
- `sec.gov/files/county.json` — total=340997, pure token noise (matches
  "files"/"json" everywhere). Not usable via this API.

### 2. Squat check (direct registry.npmjs.org/<name> lookups, 18 names)
All 404 — **none of the campaign names exist on npm**:
tryf3zz, southwarkssrfhack, southfetchprobe42, londonyardtestabc,
zzsouthrunnerb, uxjinalamb2, zzjinavcsgit, oaitest1778473828,
southnewsprobe1778550995, wandsworthprobe1778551714, slnleaker4,
yardbreakerxqh1778552850, exfiltestwand, chatoaifetch177855288717,
lambfetchx548811, probejiqptzco, southlondonfetchroot, zgitjina.

### 3. r.jina.ai package spot-checks (full metadata, 4 packages)
All legitimate tools with real authors, GitHub repos, and homepages; no
`go-import` in any readme; no laundering URLs. Notable: `termread@1.0.1`
was created 2026-05-12T00:14Z — the same day as the burst — but is a
normal terminal reader tool (author sagiriiiiii / maintainer xiaofun,
github.com/sagiriiiiii/termread). Temporal coincidence only, no linkage.

## Honest limitations
- npm's search API is fuzzy keyword search: no exact-phrase, regex, or
  wildcard queries. A literal `<meta name="go-import">` string buried in a
  readme **cannot** be exhaustively found this way.
- A true content sweep needs the npm bulk metadata feed (skimdb/couchdb
  changes) — bigger job, flagged as follow-up, not attempted here.
- Scoped-package coverage limited to what the search surfaced.

## Verdict
No evidence of GemStuffer-style tradecraft on npm through the registry
search and metadata layer: no squatted campaign names, no beacon strings,
no council/SEC references, and the r.jina.ai surface is the legitimate
MCP tooling ecosystem. The operator class, as far as this lane can see,
worked RubyGems only.

Raw: /tmp/npmhunt/searches.json, /tmp/npmhunt/squats.json, /tmp/npmhunt/campaign_names.json
