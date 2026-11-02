# fleet-fresh-scan-2026-10-14

**Charter.** Check whether the Chinese Amap agent fleet is still active on
urlquery.net on 2026-10-13/14. The swarmcha.se report window ends 2026-10-08,
but our dead-drop watch logged a live beacon session 2026-10-14 08:31 UTC
(4 POSTs, 18s window, new POI B00190BBTX, new Comcast source IP), then all
three inboxes went 404 by ~10:26 UTC. If the fleet still burns urlquery as a
remote code runner, fresh scans will carry the fleet signature.

**Method.** Read-only query of urlquery.net's public HTMX search endpoint,
using the documented fix: `HX-Current-URL` header flips
`/api/htmx/search/` from 204 to 200 + rows (HX-Request alone does not).
Query syntax per hunt doctrine: `q` matches submitted URLs;
`url.domain:`, `tags:`, `date:[YYYY-MM-DD TO YYYY-MM-DD]` scoping.

**Queries** (`check.py`):
- `url.domain:amap.com date:[2026-10-13 TO 2026-10-14]` — fresh Amap submissions
- `url.domain:gaode.com date:[2026-10-13 TO 2026-10-14]` — fresh Gaode submissions
- `uqscan= date:[2026-10-13 TO 2026-10-14]` — fleet tag grammar, any domain

**What to extract from a hit.** Report UUID, submitted URL (check the
`uqscan=`/`uq=`/`uqframe=` tag grammar), scan timestamp, and whether the URL
matches the known fleet routes (relay: jina/ai-launder; carrier: httpbin
base64; direct: amap-pc-ssr.amap.com/ssr/place/<POI>).

**Status (2026-10-14 ~16:45 UTC).** Prepared in the proactivity research
stage; execution blocked — background egress to urlquery.net is denied
(tunnel 403). Run `check.py` from a context with live egress (main chat or
a worker). 5s pacing between queries.

**Scope.** Agents and agent infrastructure only. Do not pursue
human/operator identity, registrant details, or social profiles.
