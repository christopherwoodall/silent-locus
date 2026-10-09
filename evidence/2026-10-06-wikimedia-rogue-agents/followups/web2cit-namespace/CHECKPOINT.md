# CHECKPOINT — Web2Cit namespace enumeration lane (b)
Lane: wiki-surgeon follow-up, phase 2 of 2026-10-06 Wikimedia rogue-agent hunt.
Started: 2026-10-06 ~12:54 CDT (17:54 UTC).
Branch: wikimedia-rogue-agents-followups-2026-10-06.
Read-only MediaWiki API queries against meta.wikimedia.org, curl, ≤1 req / 5s.

## Status: LANE COMPLETE (2026-10-06 ~14:05 CDT)

All planned work done. Verdicts in FINDINGS.md §9. Files committed on branch
wikimedia-rogue-agents-followups-2026-10-06 (web2cit-namespace/ only).
Pre-existing cron-file modifications in data/2026-09-28-chinese-amap-fleet/ untouched.

Key results:
- 867 pages enumerated (848 live + 19 redirects), 562 unique domains, zero
  non-bibliographic targets (flaglist empty).
- 5 deletions by Pppery 01:39:44–01:40:18Z 2026-10-06 (4 incident configs + agent
  sandbox); comments empty; oldids 30732696–30732700 still unverifiable.
- Agent ~2026-36867-71's complete creation footprint: 5 pages, 10-min burst
  2026-06-25 20:28–20:38Z. No hidden pages. No temp-account editors/owners anywhere live.
- Lead: Diegodlh's own "Temporary raw response passthrough for GIS lookup" sandbox
  (2026-07-20) on geodata.hawaii.gov — developer-known fetch-oracle pattern.

## Done (full log)
- 2026-10-06 ~12:56 CDT: read HUNT-SUMMARY.md background; verified git branch; created lane dir.
- 2026-10-06 ~13:05 CDT: allpages enumeration complete — 867 pages (513 templates.json,
  289 tests.json, ~65 patterns.json + 2 oddballs). Raw: raw/ap_page{1,2}.json, raw/titles.txt,
  raw/batch_NN.txt (25 × 35 titles).
- 2026-10-06 ~13:15 CDT: deletion-log cross-check — 5 pages deleted by Pppery
  2026-10-06 01:39:44–01:40:18Z (4 incident configs' templates.json leaves + the agent's
  sandbox template-temp-5123). Logged in FINDINGS §2.
- 2026-10-06 ~13:20 CDT: user-namespace sandbox sweep — 211 live pages, 20 named owners,
  ZERO temp-account owners. Logged in FINDINGS §3. raw/user-sandbox-titles.txt saved.
- 2026-10-06 ~13:25 CDT: revision+content batch fetch — first loop FAILED: all 25 batches hit
  curl exit 52 "Empty reply from server" (~13:07–13:10 CDT window), yet trivial API queries
  worked in the same window and the identical batch request succeeded minutes later.
  Diagnosis: transient egress/proxy or endpoint blip, not a query-shape problem.
  Retry loop: 8s pacing, ≤3 attempts per batch, jq-validated outputs, skips already-OK files.
  Second run launched ~13:33 CDT (backgrounded, auto-delivers).

## Schema note (2026-10-06 ~13:10 CDT, from Web2Cit/Docs/Storage, Meta-Wiki — UPSTREAM)
- Config = JSON wiki pages, up to 3 per domain: templates.json (translation templates),
  patterns.json (URL path patterns), tests.json (translation tests).
- Location grammar: Web2Cit/data/<reversed hostname labels>/ — e.g. meta.wikimedia.org
  → Web2Cit/data/org/wikimedia/meta/. Target domain is derivable from the page title itself.
- Sandbox storage under User:<name>/Web2Cit/data/ (matches the deleted incident sandbox page
  User:~2026-36867-71/Web2Cit/data/com/arcgis/geocode/templates-temp-5123).

## Next
- Enumerate list=allpages&apprefix=Web2Cit/data/ (paginate with aplimit=max, continue).
- For each page: latest revision (user, timestamp) via prop=revisions (batch titles in ≤50s).
- For each page: content via prop=revisions&rvprop=content (batch ≤50s), extract target domains from JSON ("domains" fields, URL patterns).
- Flag non-bibliographic targets (geocoding, geodata, weather, IP/geolocation, shorteners, pastebins, webhooks, API-shaped).
- Cross-check against 4 known incident configs (deleted; expect absent):
  Web2Cit/data/com/arcgis, Web2Cit/data/com/arcgis/services,
  Web2Cit/data/com/arcgis/use1-geocode, Web2Cit/data/gov/hawaii/geodata.
- Write FINDINGS.md; commit web2cit-namespace/ only.

## Resume commands
API base: https://meta.wikimedia.org/w/api.php
Allpages: curl -sS --max-time 60 "https://meta.wikimedia.org/w/api.php?action=query&list=allpages&apprefix=Web2Cit%2Fdata%2F&aplimit=500&format=json&formatversion=2" | jq .
Continue with &apcontinue=<token>.
Revisions: ...&prop=revisions&rvprop=user|timestamp&titles=T1|T2...
Content:    ...&prop=revisions&rvprop=content|user|timestamp&titles=T1|T2...
