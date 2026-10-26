# slot-2 (urlquery fresh) sweep summary — 2026-10-26T16:40–16:44Z

Window: last ~24h of urlquery reports (date:[2026-10-25 TO 2026-10-27]), hunt grammars only.
Method: lane-1 scanner (12 families, limit 30) + 6 direct grammar re-queries, authenticated API, polite spacing.

Scanner result: 36 reports screened, 0 hits.

Direct grammar results:
- `uqtag=` -> 0
- `uqframe=` -> 0
- `uqscan=` -> 21, IDENTICAL to the 2026-10-26T10:44Z slot-2 run: same 21 report IDs
  (verified set-equal against raw/2/20261026T104051Z/sweep.log, 0 new IDs),
  same burst 2026-10-26T00:47:45Z–00:55:05Z, all from
  firstcontact-gateway.jcburrows.workers.dev, all tags empty. No new gateway
  report, no second burst.
- `url.domain:jcburrows.workers.dev` -> 21, same 21 gateway reports (A91 correct form).
- `webhook.site` -> 2: 0fbd1c1b (2026-10-25T04:06:51Z, same dead-token viewer row
  already triaged) and fd17345d (2026-10-25T07:44:57Z, submitted peerlist.io,
  page-content match only, no webhook.site UUID in URL/tags/title — noise class).
- `ntfy.sh` -> 3: all page-content matches (cfast.fr, pretmontreal.com, and the
  0fbd1c1b webhook row); no ntfy.sh topic in any submitted URL — noise class.

Verdict: NO NEW LEAD. All rows triaged against FALSE-POSITIVES-urlquery.md noise classes.
