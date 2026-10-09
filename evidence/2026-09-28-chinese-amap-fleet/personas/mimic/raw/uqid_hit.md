# PREDICTION HIT: `uqid=` grammar (2026-10-05, Mimic direct hunt)

Predicted `uqid=` as grammar drift from `uqscan=`/`uqm=`. CONFIRMED in the wild via htmx (2026-10-05 ~04:3x UTC):

- 2026-10-04T14:22Z — `postman-echo.com/redirect-to?url=http%3A%2F%2Famap-pc-ssr.amap.com%2Fssr%2Fplace%2FB0…` (uqid= present)
- 2026-10-04T14:21Z — `nghttp2.org/httpbin/redirect-to?url=https%3A%2F%2Famap-pc-ssr.amap.com%2Fssr%2Fplace%…` (uqid= present)

Shape: operator's redirector tradecraft (redirect-to → Amap place) carrying the NEW `uqid=` param instead of `uqscan=`. Same day as the ltzh-family burst window (Oct 4 12:58–13:15 UTC) — possibly related tooling iteration.

Note: htmx throttled after ~4 queries (≤1/5s observed but still hit limits under concurrent sibling load). Report IDs not captured — follow-up: re-query `uqid=` with backoff and extract full URLs + report IDs.
