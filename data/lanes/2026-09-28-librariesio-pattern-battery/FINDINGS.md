# Findings

Grade claims OBSERVED, UPSTREAM, or INFERENCE.
Terms: libraries.io = the RubyGems mirror site; go-import payload = a
`<meta name="go-import">` tag in a gem description that points a Go tool at a
VCS URL; echo rig = test gems pointed at HTTP echo services to check the fetch fires.

All claims below are UPSTREAM (observed by the 2026-09-28 battery note, not by
this ingest). Factum record IDs are cited in README.md.

1. 2,698 names were checked. 1,609 pages were live. 1,191 live pages carried
   go-import payloads. libraries.io is a partial but verbatim mirror of the campaign.
2. The July-7 wave was fully mirrored: 55 gems atom-dated 2026-07-07 03:30–06:15 UTC
   (XSS/SSRF/tar/YAML red-team plus cross-tenant probes).
   `apexblack-evidence-1783394610` says: "Proof-of-impact: pushed via
   scope-escalated legacy API key."
3. The oai echo-rig family: 123 gems dated 2026-05-11 09:50–10:35 UTC. Their
   go-import tags pointed at echo services (httpbin.org, postman-echo.com,
   httpbingo.org, eu.httpbin.org) to check the fetch fires.
   `oaihx7579061` pointed at `https://webhook.site/token?foo=1` — the webhook
   dead-drop technique starts on May 11, not in July.
4. The timeline starts earlier than thought: May 8 (Google Drive targets),
   May 9 (XSS+go-import hybrid), May 11 (echo-rig rehearsal), May 12 (main
   burst; remote exfil and image-tag beacons), June 18 (link-posting),
   July 7 (red-team).
5. The June-18 wave was mirrored: 55 gems (`00proxy`/`00prx`/`-00` families)
   with bland descriptions. No sec.gov/county.json targets in descriptions.
6. The tryzz namespace was closed: 0 of 231 unseen `try[a-z][0-9]zz` combos found.
7. libraries.io shows no author field in HTML, versions.atom, or the public API.
   The July "Testing <Animal>" author format cannot be checked here. 45
   "Testing …" description markers were found.
8. Zero hits for `web_hooks`, `oast.online`, `A000`, `ZZEND` across 1,912
   descriptions. The southpxdatapp6pi zlib+base64 dead-drop lives in gem
   metadata URL paths — it is a Diffend-bytes-only technique.
