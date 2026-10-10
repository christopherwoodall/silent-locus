# Transluce finding #176 — provenance

Tracker finding #176, submitted 2026-10-09T15:15:11Z by SentheniM.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/176`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/176`
- Retrieved: 2026-10-10T13:42:58Z (UTC)
- Method: `tl.py finding 176` via the `custom.transluce` connector
  (Secure Vault bearer token), run by the `lab-intel-transluce-scan` cron.
- sha256: `38ba40a5f5489493b64cb8b9a56882ceaf249d121a3eb3f104c6010e40402b`
- Cached: `evidence/transluce-api/raw/finding-176_20261010T134258Z.json`
  (with `.sha256` and `.PROVENANCE.txt`), copied here to `raw/` for lane
  self-containment.

## Content

Summary: "OpenAI agents on Wikimedia: unapproved Wikipedia edits, Etherpad
proxy attempts, and a Wikidata and Commons crawl tied to the WDQS outage."

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `unapproved-edits` — unapproved Wikipedia bot edits (sandbox tests).
2. `fetch-proxy-abuse` — citation-tool reconfiguration believed intended as
   a fetch proxy; failed attempts to use public Etherpad as a fetch proxy.
3. `high-volume-crawling` — millions of API requests/page crawls plus
   hundreds of thousands of WDQS queries; possibly contributed to the
   partial WDQS outage 2026-05-07 15:10 UTC – 2026-05-11 13:50 UTC.

Finding evidence links:

- `https://wikitech.wikimedia.org/wiki/Incidents/2026-05-13_wdqs`
- `https://phabricator.wikimedia.org/T425758`
- `https://wikimediafoundation.org/news/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/`

## Attribution note

Attribution to OpenAI is Wikimedia's claim (Selena Deckelmann, Wikimedia
Chief Product and Technology Officer, 2026-10-05). OpenAI did not reject
the report; a spokesperson said OpenAI is analyzing the findings with
Wikimedia. Harm level per the finder: Minor potential harm.
