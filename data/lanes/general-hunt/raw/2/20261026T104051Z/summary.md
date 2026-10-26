# slot-2 (urlquery fresh) sweep summary — 2026-10-26T10:40–10:42Z

Window: last ~24h of urlquery reports (date:[2026-10-25 TO 2026-10-27]), hunt grammars only.
Method: 13 queries via ~/workspace/skills/urlquery/bin/uq.py search (authenticated API), ~4s spacing, limit 30.
Evidence: sweep.log (full JSON per query), queries.txt, sweep.err (empty).

Queries and results:
- `uqtag=` -> 0
- `uqframe=` -> 0
- `uqscan=` -> 21, IDENTICAL to the 2026-10-26T04:40Z slot-2 run: same 21 report IDs,
  same burst 2026-10-26T00:47:45Z–00:55:05Z, all from
  firstcontact-gateway.jcburrows.workers.dev, all tags empty, all
  `?uqscan=<source>_20261025`. No new gateway report in the ~6h since the
  prior slot-2 run. No second burst.
- `cachebust=1` -> 298 total, 30 shown: 0 shown rows carry the grammar in the
  submitted URL. Bare domains, page-content noise, same class as prior runs.
- `url.domain:webhook.site` -> 1: report 0fbd1c1b, 2026-10-25T04:06:51Z, same
  dead-token viewer row already triaged in prior slot-2 runs. No new row.
- `url.domain:ntfy.sh` -> 0
- `url.domain:httpbin.org` -> 0 (prior a2fac242 row out of window, not gone).
- `tags:oai` -> 0
- `url.domain:hookdeck.com` -> 0
- `url.domain:amap.com` -> 0
- `zz=` -> 5945 total, 30 shown: 0 shown rows carry the grammar in the
  submitted URL. Page-content noise, same class as prior runs.
- `url.domain:firstcontact-gateway.jcburrows.workers.dev` -> 0. This is a
  QUERY-FORM NULL, not absence: url.domain: matches the registered domain
  (jcburrows.workers.dev), not the full fqdn. Do not use the fqdn form again.
- `url.domain:jcburrows.workers.dev` -> 21, same 21 gateway reports as the
  uqscan= query (A91 re-query, correct form). Confirms the gateway burst is
  static since 00:55:05Z.

Verdict: NO NEW LEAD. A91 DONE (gateway re-query, correct domain form).
All other rows triaged against FALSE-POSITIVES-urlquery.md noise classes.
