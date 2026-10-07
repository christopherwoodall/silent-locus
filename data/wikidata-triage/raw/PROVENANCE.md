# Provenance — wikidata-triage raw captures

Method: Wikidata Action API (https://www.wikidata.org/w/api.php), no auth.
Retrieved: 2026-10-07 ~16:00–17:00 UTC via curl/urllib, UA `silent-locus-triage/1.0`.

## Files
- `insource-lifeval.json` — `list=search&srsearch=insource:"Lifeval"`, srlimit=50.
  1 hit: Q11524114 (Tokyo Gas "Lifeval" — known real-world name collision,
  last touched 2025-08-24). NOT agent activity.
- `insource-Lifeval-API-temp-account-test.json` — insource:"Lifeval API temp-account test" → 0 hits.
- `insource-temporary-technical-sandbox-initialization.json` — insource:"temporary technical sandbox initialization" → 0 hits.
- `insource-temp-account-test.json` — insource:"temp-account test" → 0 hits.

## API checks NOT capturable as files (recorded in FINDINGS.md)
- `Wikidata:Sandbox` revision history: 387 revisions retained, oldest
  2026-07-09T13:44:45Z — June 25 incident window pruned. 0 marker hits in
  retained window (grep: lifeval|temp-account|sandbox initialization|zz=oai|_oai=).
- `list=recentchanges`: table pruned to ~2026-09-10 (~27 days) — June 24–26 and
  May 11–Jul 2 windows unreachable.
- `list=usercontribs` for ~2026-36766-54, ~2026-36837-35, ~2026-28355-02,
  ~2026-36867-71 → 0 edits each on wikidata.org.
- 15,000 recent non-bot edits scanned (2026-10-07 ~16:09–16:54Z window of
  activity) — 0 marker-comment hits.

SHA-256 in SHA256SUMS.
