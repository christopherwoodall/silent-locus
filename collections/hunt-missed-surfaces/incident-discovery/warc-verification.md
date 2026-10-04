# WARC verification — the two biggest leads

2026-10-03. Read-only. Note on method: web.archive.org `web/` fetches returned
HTTP 429 for this VM's egress IP on all attempts (4 tries, spaced); Archive-It's
`wayback.archive-it.org` mirror shares the same limiter ("Rate limit reached",
contact Aitratelimit@archive.org). CDX (`web.archive.org/cdx`) stayed reachable
but returns null for `offset`/`filename`/`source`/`robotflags` on these records,
so direct WARC range requests were not possible. Verdicts below rest on CDX
records, the archived-URL evidence itself, and timing analysis — the WARC
request-record (user-agent) check remains unrun and is flagged where it matters.

## Lead 1: county.json Wayback burst — verdict: AGENT-DRIVEN on-demand saves, not IA crawl

**Record pulled (CDX):** `20260618201918`,
`https://www.sec.gov/files/county.json?x=0.01693224778333735`,
status 200, `application/json`, digest `VABBDDDTZS2COG3DDYVIWHVX7TDH7OYH`,
length 19424. robotflags/source/offset/filename: null (CDX limitation, not a finding).

**Timing analysis (65 Jun-18 sec.gov captures, local data):**
- 02:00 UTC: 2, 06:00: 1, 14:00: 11, 15:00: 2, 16:00: 4, 17:00: 4, 19:00: 2,
  **20:00: 39** — 39 captures in one hour, roughly one per 90 seconds.
- 61/65 share a single digest (byte-identical 200s); 4 are 404s (probing shapes:
  `?a`, `?_=true`, `?baz=zip`, `?download`, `?format=json`, `?redirect=1` etc.).
- Every nonce URL is unique: 60+ distinct `?x=0.<17-digit>` URLs, plus
  `?0.<16-digit>` and `?x=1/2/4/8` variants.

**The undiscoverability argument (core evidence):** a crawler captures only URLs
it discovers. `?x=0.01693224778333735`-style URLs are undiscoverable — nobody
links them; they exist only in the minter's head. The minter used the agent
toolkit's nonce grammar (same `?x=0.<17d>` family as the DoE/Kansas/Navy/
Illinois/CAL-ACCESS arquivo.pt captures; cousin to the `?fresh=x<epoch>.<random>`
SPN-loop saves). Therefore these are on-demand saves submitted by (or for) the
nonce-minting party — automated save requests at machine cadence, not a crawl.
Whether the endpoint was Save-Page-Now specifically vs. another on-demand
mechanism is the residual uncertainty; "save-on-demand, not crawl" is
established.

**Corroboration:** joshuadavid/wikiagentswarminvestigation documents an ~8-hour
county.json swarm burst on 2026-06-18 (wiki-revision side); our capture burst
runs 14:52–20:21 UTC the same day.

**What would close it:** the WARC request record's User-Agent for any one of the
39 20:00-hour captures (retry when the 429 lifts), or the CDX `source` field
from an unblocked network.

## Lead 2: AIHW jina-wrapped capture — verdict: AGENT-SHAPED relay fetch, archived

**Record (CDX urlkey):**
`ai,jina,r)/http:/https:/www.aihw.gov.au/getmedia/57e4c61f-213a-4b27-b2fa-3a22a2a19d27/principal-diagnosis-cube_2014-15.xlsx.aspx`
@ **20260618063135** (Jun 18, 2026, 06:31:35 UTC).

**Evidence:**
- The doubled scheme `http://https://` is preserved verbatim in the CDX urlkey —
  agent URL-construction sloppiness, baked into the archived record itself. No
  WARC needed for this point.
- The capture is of the *jina-wrapped* URL (`r.jina.ai/http://https://…`), i.e.
  someone fetched AIHW content through the r.jina.ai reader proxy (keyless in
  June 2026) and the wrapped fetch got archived — exactly the relay-ladder
  behavior the skill files teach.
- Timestamp vs. county.json burst: same calendar day (Jun 18) but 06:31 UTC vs.
  14:52–20:21 UTC — same-day cluster, not the same burst window. Sep 4–5 PBS
  dashboard/data wrapped captures form a second cluster.
- Relation to Transluce: their Sep-23 report covers AIHW via urlquery.net scans
  (Jun 20/21, pre-prod server pulls). Our Jun-18 jina-wrapped capture slightly
  *predates* their window — same incident family, new trace venue, earlier date.

**Not verified:** the wrapped response's request headers/body (429-blocked).
The urlkey + timestamp + relay-wrapping evidence stands without it.

## Bottom line
Both leads hold without the WARC bodies: the county.json burst is
machine-cadence on-demand saving of minter-only URLs (agent-driven, not crawl),
and the AIHW record is a jina-relayed fetch with agent sloppiness baked into
the archived URL. The single highest-value remaining pull: one WARC request
record from the 20:00-hour burst for the saving party's User-Agent.
