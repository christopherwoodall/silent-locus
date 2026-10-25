# slot-2 (urlquery fresh) sweep summary — 2026-10-25T22:40–22:42Z

Window: last ~30h of urlquery reports (date:[2026-10-24 TO 2026-10-26]), hunt grammars only.
Method: 11 queries via ~/workspace/skills/urlquery/bin/uq.py search (authenticated API), ~4s spacing, limit 30.

Queries and results:
- `uqtag=` -> 0
- `uqframe=` -> 0
- `uqscan=` -> 0
- `cachebust=1` -> 473 total, 30 shown: all tags empty, all submitted URLs bare domains
  (lovewellfence.com, tilbillyfarm.ca, ricomiccon.com, others). Match is
  page-content, not URL grammar. No agent behavior. Same noise class as prior slot-2 runs.
- `url.domain:webhook.site` -> 1: report 0fbd1c1b, 2026-10-25T04:06:51Z, same dead-token
  viewer row already triaged in the 10:45Z and 16:42Z slot-2 runs. No new row.
- `url.domain:ntfy.sh` -> 0
- `url.domain:httpbin.org` -> 1: report a2fac242, 2026-10-24T05:35:28Z, same
  httpbin.org/anything?marker=jsRC row already triaged. No new row.
- `tags:oai` -> 0
- `url.domain:hookdeck.com` -> 0
- `url.domain:amap.com` -> 0
- `zz=` -> 10014 total, 30 shown: all tags empty except two whf.bz rows tagged
  ['bankid','authentication'] (asadnbasa.whf.bz/eika, a phishing-shaped BankID
  lure, not agent grammar); the rest are bare domains (kmspicos-download.vip
  piracy burst, appwrite consoles, ordinary sites). Zero submitted URLs carry zz
  grammar; the match is page-content noise, same class as prior slot-2 runs.
  The whf.bz rows are human phishing, out of hunt scope (agents and agent
  infrastructure only), noted here only so the tag does not look missed.

Verdict: 0 hits, 0 leads. All rows triaged against FALSE-POSITIVES-urlquery.md noise classes.
