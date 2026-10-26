# slot-2 (urlquery fresh) sweep summary — 2026-10-26T04:40–04:42Z

Window: last ~24h of urlquery reports (date:[2026-10-25 TO 2026-10-27]), hunt grammars only.
Method: 11 queries via ~/workspace/skills/urlquery/bin/uq.py search (authenticated API), ~4s spacing, limit 30.
Evidence: sweep.log (full JSON per query), queries.txt, sweep.err (empty).

Queries and results:
- `uqtag=` -> 0
- `uqframe=` -> 0
- `uqscan=` -> 21 (NEW — 0 in all three prior slot-2 runs 2026-10-25 10:45Z, 16:42Z, 22:42Z).
  Burst: 21 reports, 2026-10-26T00:47:45Z–00:55:05Z (8m20s), all from one gateway:
  firstcontact-gateway.jcburrows.workers.dev, all tags empty, all with
  `?uqscan=<source>_20261025` values. Distinct /raw/*.py proxy scripts:
  pubmed_pmc_table_extractor, county_parcel_assessor, highspeed_rail_seat_relay,
  uk_parish_records_mirror, clinicaltrials_nct_proxy, historical_passenger_manifest,
  marinetraffic_vessel_locator, flightaware_telemetry_relay, uspto_patent_claims_proxy,
  federal_register_extractor, drivelah_booking_proxy, openalex_arxiv_resolver,
  max_gov_document_cache, sec_edgar_client, acled_event_data_relay,
  mapillary_graph_api, thrill_data_scraper, aihw_tableau_fetch, unctad_api_relay,
  amap_chengdu poi (B001C94YUZ), vectors probe (probe20261025).
  Gateway never seen before in this repo (grep clean outside this sweep).
  Shape: single Cloudflare Workers gateway serving many data-source retrieval
  proxies, submitted to urlquery in one burst. Two names echo known hunt clusters
  (AIHW Tableau pulls, SEC extraction) but inside one new gateway burst, not the
  old clusters. Verdict: LEAD (new agent-shaped data-retrieval infrastructure).
  Unconfirmed: who submitted the reports, and whether agents use the gateway
  in the wild. No fetch of the gateway itself was made (passive sweep only).
- `cachebust=1` -> 296 total, 30 shown: all tags empty, all bare domains
  (emmittplant.co.uk, highlandhousecarryout.com, ordinary sites, one appwrite
  console). Page-content noise, same class as prior slot-2 runs. No agent behavior.
- `url.domain:webhook.site` -> 1: report 0fbd1c1b, 2026-10-25T04:06:51Z, same
  dead-token viewer row already triaged in the 10:45Z, 16:42Z, 22:42Z slot-2 runs.
  No new row.
- `url.domain:ntfy.sh` -> 0
- `url.domain:httpbin.org` -> 0 (prior a2fac242 marker=jsRC row dated 2026-10-24,
  now outside this window; not gone, just out of window).
- `tags:oai` -> 0
- `url.domain:hookdeck.com` -> 0
- `url.domain:amap.com` -> 0
- `zz=` -> 5702 total, 30 shown: all tags empty, all bare domains
  (difyshare.com, cooldaddytee.com, ordinary sites). Zero submitted URLs carry
  zz grammar; page-content noise, same class as prior slot-2 runs.

Verdict: 1 LEAD (uqscan gateway burst, 21 reports). All other rows triaged
against FALSE-POSITIVES-urlquery.md noise classes. No other leads.
