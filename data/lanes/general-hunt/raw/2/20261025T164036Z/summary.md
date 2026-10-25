# slot-2 (urlquery fresh) sweep summary — 2026-10-25T16:40–16:42Z

Window: last 24h of urlquery reports (date:[2026-10-24 TO 2026-10-25]), hunt grammars only.
Method: 11 queries via ~/workspace/skills/urlquery/bin/uq.py search (authenticated API), ~4s spacing, limit 30.

Queries and results:
- `uqtag=` -> 0
- `uqframe=` -> 0
- `uqscan=` -> 0
- `cachebust=1` -> 396 total, 30 shown: all tags empty, all submitted URLs bare domains
  (sterkrade-nord.de, merrillanderson.com, genspark.ai, forbes.cz, others). Match is
  page-content, not URL grammar. No agent behavior. Same noise class as prior slot-2 runs.
- `url.domain:webhook.site` -> 1: report 0fbd1c1b, 2026-10-25T04:06:51Z, same dead-token
  viewer row already triaged in the 10:45Z slot-2 run. No new row.
- `url.domain:ntfy.sh` -> 0
- `url.domain:httpbin.org` -> 1: report a2fac242, 2026-10-24T05:35:28Z, same
  httpbin.org/anything?marker=jsRC row already triaged. No new row.
- `tags:oai` -> 0
- `url.domain:hookdeck.com` -> 0
- `url.domain:amap.com` -> 0
- `zz=` -> 8795 total, 30 shown: all tags empty, all submitted URLs bare domains
  (kmspico-piracy, appwrite.io consoles, ordinary sites). Zero titles carry zz grammar;
  the match is page-content noise, same class as prior slot-2 runs.

Verdict: 0 hits, 0 leads. All rows triaged against FALSE-POSITIVES-urlquery.md noise classes.
