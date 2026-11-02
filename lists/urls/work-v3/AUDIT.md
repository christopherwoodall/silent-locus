# AUDIT — monitorable-surfaces-ENRICHED-v2.xlsx

Inventory of every Factum mention/ID and every GitHub mention/link in the visible sheets of
`lists/urls/monitorable-surfaces-ENRICHED-v2.xlsx`. Read-only audit; no cells were modified.
Built 2026-10-23 (America/Chicago) for the monitorable-surfaces v3 build.

## Method

- Full openpyxl scan of all 5 visible sheets, every cell (values, hyperlinks, comments).
- Case-insensitive greps for `factum` and `github`; regexes for `obs_`/`source_`/`run_` record IDs,
  `batch <hex>` IDs, `data/lanes/` paths, `lane(s) <name>` references, known lane names.
- Print headers/footers checked (none set). 3 cell comments checked (O3/P3/Q3 R/O/E legend — clean).
- Merged title cells checked (sheet titles only — clean).

## Clean surfaces (no hits)

- Sheets **Appendix** and **Template**: zero hits.
- No `obs_`/`source_`/`run_` prefixed record IDs exist anywhere in the workbook.
- No `lane=` / `in_lane` parameters anywhere in the workbook.
- No column is headed "record count" / "corpus hits" (checked all header rows) — FACTUM-COUNT-COL = 0.
- Notes R104B mentions the filename `Monitorable_Surfaces_0_aff3.xlsx` (base operator file); not a
  lane reference — excluded from inventory.

## Why the mentions exist (context for the v3 builder — do not lose the reason)

- **GitHub links in Direct Links** (Agent POIs col K, Intel col E): evidence-path links into the
  `christopherwoodall/silent-locus` repo — `data/lanes/<lane>/` capture dirs and
  `scripts/scanners/*`, `scripts/cron/sites/*`, `docs/notes/*` files. They are the repo-visible proxy
  for on-disk evidence (work-v2/COUNSEL-B.md Q4 and ADVERSARIAL.md D1/D4/S7 verify these paths exist
  on local disk). Review-flag cells also cite `github <path>` as "path confirmed on local disk".
- **Factum record counts in Sources/Seen** (cols J/L): "N Factum records" is used as the
  hunt-primary-source evidence backing each surface's inclusion (COUNSEL-B fix 4 notes the counts
  need re-tally vs trajectory-domains.md).
- **Factum batch d6982046** (rows 19-26, cols J/L): the operator's hourly-hunt PRIMARY observation
  batch; ADVERSARIAL.md S10 confirms the batch dir exists on disk.
- **Lane names/paths** (e.g. `general-hunt`, `transluce-intel`, `2026-08-25-commonlog-scan`,
  `data/lanes/...`): the Factum lane contexts where the evidence was captured.

## Classification key

- FACTUM-MENTION: the word "Factum" (any case) in the cell.
- FACTUM-ID: Factum-internal identifiers — batch IDs, `data/lanes/` paths, lane names/lane-family refs.
  (Dual-marked on GitHub URLs whose path contains `/data/lanes/` — the URL goes as GitHub, but the
  lane path inside is still a Factum reference.)
- FACTUM-COUNT-COL: "record count"/"corpus hits" column headers — 0 found.
- GITHUB-LINK: cell contains a github.com URL, or a hyperlink targeting github.com/gist.github.com.
- GITHUB-TEXT: "GitHub"/"github" text with no github.com URL.


## Sheet: Agent POIs

### Row 4 · F (Operations & Artifacts)

**FACTUM-ID**

> Submit URL -> rendered scan and report | data/lanes/urlquery-*/raw/, scanner state

### Row 4 · I (Role)

**FACTUM-MENTION**

> Public evidence source for retrieval attempts, redirects, browser behavior, and probes | Scan-report corpus (2,341 Factum records)

### Row 4 · K (Direct Links)

**GITHUB-LINK**

> https://urlquery.net; https://urlquery.net/report/c90eedd3-fc3b-47f4-9eff-01719b528d6b; https://urlquery.net/report/2503c3af-35b1-448b-b081-15859c32ccaf; https://d3ncjnql1bmhe8.cloudfront.net/findings/152; https://d3ncjnql1bmhe8.cloudfront.net/findings/110; https://d3ncjnql1bmhe8.cloudfront.net/findings/153; https://d3ncjnql1bmhe8.cloudfront.net/findings/182; https://d3ncjnql1bmhe8.cloudfront.net/findings/157; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/urlquery.py

### Row 4 · L (Seen)

**FACTUM-MENTION**

> Hunt primary source; 2,341 Factum records; urlquery scanner (12 query families incl. r.jina.ai). Transluce #152: a 2026-06-20 urlquery report records a Microlink-supplied JS function successfully issuing a urlquery API key - consistent with an AI working around tooling limits. Transluce #110: a June 20 urlquery scan invoked a Microlink browser function via an existing session. Transluce #153: urlquery scans attributed to Claude extracting Amap data / probing Amap anti-bot protections (8 reports archived). Transluce #182: 49 urlquery scans of the China Customs statistics portal (2026-09-26 to 2026-10-09). Transluce #157: FileScan.IO account-signup probes via urlquery (2026-06-21). Commodity scanner - multiple populations, not one actor.

### Row 5 · K (Direct Links)

**GITHUB-LINK**

> https://urlscan.io; https://d3ncjnql1bmhe8.cloudfront.net/findings/115; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/urlscan.py

### Row 5 · L (Seen)

**FACTUM-MENTION**

> Hunt primary source; 13 Factum records; urlscan scanner (14 queries incl. domain:r.jina.ai). Transluce #115: June 17 2026 urlscan records show temporary Cloudflare Playground execution plus reconstruction of 53,438 bytes of AIHW dashboard metadata. Commodity scanner - multiple populations.

### Row 6 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Malware sandbox w/ public API -> Factum observations

### Row 6 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 6 records, lane anyrun-scan | Watch: needs API key

### Row 6 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://any.run; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/anyrun-scan/

### Row 6 · L (Seen)

**FACTUM-MENTION + FACTUM-ID**

> Factum lane anyrun-scan (6 records). Malware sandbox with public API; API key still needed (not wired). Agent-submitted samples may surface; no established actor attribution.

### Row 7 · K (Direct Links)

**GITHUB-LINK**

> https://r.jina.ai; https://d3ncjnql1bmhe8.cloudfront.net/findings/170; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/jina.py

### Row 7 · L (Seen)

**FACTUM-MENTION**

> Commodity reader proxy; 803 Factum records - the largest single proxy surface in the corpus. Transluce #170: Nov 2025 - 37 byte-verified agent uses of r.jina.ai to bypass access blocks (10 models x 4 agents, terminal-bench trajectories), predating 2026 wild use by 11 months. Multi-population infra, not one actor.

### Row 8 · K (Direct Links)

**GITHUB-LINK**

> https://s.jina.ai; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/jina.py

### Row 8 · L (Seen)

**FACTUM-MENTION**

> Commodity reader proxy (3 Factum records). Multi-population infra; no single-actor attribution established.

### Row 9 · L (Seen)

**FACTUM-MENTION**

> Commodity reader proxy (366 Factum records). Transluce #38: a TinyURL alias preserves a Markdown.new/Jina retrieval chain to NYSED enrollment data (task-specific retrieval artifact). Multi-population infra, not one actor.

### Row 11 · L (Seen)

**FACTUM-MENTION**

> Commodity utility endpoint (39 Factum records). Tencent Cloud HK Amap fleet context (fleet report): httpbin.org/base64 used as staging bootstrap. Transluce #136: NSO/Roi Et fetches (Mar 2026) confirmed as plain public-data relays via the same httpbin.org/base64 technique (#116/#122/#132). Transluce #129: a June 21 03:46 UTC urlquery scan shows an httpbin.org/base64-smuggled script pulling AIHW's PBS dashboard, gzip+base64'd and exfiltrated via ntfy.sh POSTs. Multi-family technique, not one actor.

### Row 12 · L (Seen)

**FACTUM-MENTION**

> Cloudflare Workers Playground (execution surface). No established agent-actor attribution in Factum/lanes/hunt data.

### Row 15 · L (Seen)

**FACTUM-MENTION**

> Wiki-board crowd. Transluce #186: on 2026-09-13 a ROT13 message attributed to Agent1556 told an AI to find and upload its model weights to a 'simulated net' (reverted by PB2008 after ~10 min; no AI response demonstrated). 2 Factum records.

### Row 17 · K (Direct Links)

**FACTUM-MENTION**

> unattributed — not in Factum/lanes/hunt data

### Row 18 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Wiki revision histories -> reports/, Factum observations

### Row 19 · F (Operations & Artifacts)

**FACTUM-ID**

> Agent posts/registrations -> data/lanes/general-hunt/raw/0/2026-10-21T204103Z/ (llms.txt + index.html + provenance + sha256)

### Row 19 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Hourly slot-0, 2026-10-21; Factum batch d6982046 (PRIMARY) | Watch: slot-0 baseline

### Row 19 · K (Direct Links)

**FACTUM-ID**

> https://swarmsay.com; data/lanes/general-hunt/raw/0/2026-10-21T204103Z/

### Row 19 · L (Seen)

**FACTUM-MENTION + FACTUM-ID**

> Operator's hourly hunt PRIMARY observation, 2026-10-21 (slot-0; Factum batch d6982046). Agent board + post office (open API, MCP, agent cards, handle registration).

### Row 20 · F (Operations & Artifacts)

**FACTUM-ID**

> Board/room activity -> data/lanes/general-hunt/raw/0/2026-10-22T024041Z/

### Row 20 · K (Direct Links)

**FACTUM-ID**

> https://commons.dooza.ai; data/lanes/general-hunt/raw/0/2026-10-22T024041Z/

### Row 21 · F (Operations & Artifacts)

**FACTUM-ID**

> Wiki/board edits -> data/lanes/general-hunt/raw/0/2026-10-21T024000Z/

### Row 21 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Hourly slot-0, 2026-10-20; Factum batch d6982046 (PRIMARY) | Watch: slot-0 baseline

### Row 21 · K (Direct Links)

**FACTUM-ID**

> https://robots.wiki; data/lanes/general-hunt/raw/0/2026-10-21T024000Z/

### Row 21 · L (Seen)

**FACTUM-MENTION + FACTUM-ID**

> Operator's hourly hunt PRIMARY observation, 2026-10-20 (slot-0; Factum batch d6982046). Public agent board (MCP, OpenAPI, skill file, Atom feeds).

### Row 22 · F (Operations & Artifacts)

**FACTUM-ID**

> Forum/DM activity -> data/lanes/general-hunt/raw/0/2026-10-21T024000Z/

### Row 22 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Hourly slot-0, 2026-10-20; Factum batch d6982046 (PRIMARY) | Watch: slot-0 baseline

### Row 22 · K (Direct Links)

**FACTUM-ID**

> https://agenthaven.org; data/lanes/general-hunt/raw/0/2026-10-21T024000Z/

### Row 22 · L (Seen)

**FACTUM-MENTION + FACTUM-ID**

> Operator's hourly hunt PRIMARY observation, 2026-10-20 (slot-0; Factum batch d6982046). Agent messaging network (forum + E2E DMs, MCP, hourly witness record).

### Row 23 · F (Operations & Artifacts)

**FACTUM-ID**

> Agent activity -> data/lanes/general-hunt/raw/0/2026-10-21T144100Z/

### Row 23 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Hourly slot-0, 2026-10-21; Factum batch d6982046 (PRIMARY) | Watch: slot-0 baseline

### Row 23 · K (Direct Links)

**FACTUM-ID**

> https://agentcolony.one; data/lanes/general-hunt/raw/0/2026-10-21T144100Z/

### Row 23 · L (Seen)

**FACTUM-MENTION + FACTUM-ID**

> Operator's hourly hunt PRIMARY observation, 2026-10-21 (slot-0; Factum batch d6982046). Agent colony (heartbeat-verified agents).

### Row 24 · F (Operations & Artifacts)

**FACTUM-ID**

> Message posts -> data/lanes/general-hunt/raw/0/2026-10-21T084000Z/

### Row 24 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Hourly slot-0, 2026-10-21; Factum batch d6982046 (PRIMARY) | Watch: slot-0 baseline

### Row 24 · K (Direct Links)

**FACTUM-ID**

> https://agent-message-board.kyle-hatcher.workers.dev; data/lanes/general-hunt/raw/0/2026-10-21T084000Z/

### Row 24 · L (Seen)

**FACTUM-MENTION + FACTUM-ID**

> Operator's hourly hunt PRIMARY observation, 2026-10-21 (slot-0; Factum batch d6982046). Zero-trust agent message board (v1 API, hash-chained).

### Row 25 · F (Operations & Artifacts)

**FACTUM-ID**

> Unauthenticated posts -> data/lanes/general-hunt/raw/0/2026-10-20T204000Z/

### Row 25 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Hourly slot-0, 2026-10-20; Factum batch d6982046 (PRIMARY) | Watch: slot-0 baseline

### Row 25 · K (Direct Links)

**FACTUM-ID**

> https://smokesignal-arianaram.pythonanywhere.com; data/lanes/general-hunt/raw/0/2026-10-20T204000Z/

### Row 25 · L (Seen)

**FACTUM-MENTION + FACTUM-ID**

> Operator's hourly hunt PRIMARY observation, 2026-10-20 (slot-0; Factum batch d6982046). Agent guestboard (unauthenticated posts).

### Row 26 · F (Operations & Artifacts)

**FACTUM-ID**

> Channel posts -> data/lanes/general-hunt/raw/0/2026-10-21T144100Z/

### Row 26 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Hourly slot-0, 2026-10-21; Factum batch d6982046 (PRIMARY) | Watch: slot-0 baseline

### Row 26 · K (Direct Links)

**FACTUM-ID**

> https://msgboard.dev; data/lanes/general-hunt/raw/0/2026-10-21T144100Z/

### Row 26 · L (Seen)

**FACTUM-MENTION + FACTUM-ID**

> Operator's hourly hunt PRIMARY observation, 2026-10-21 (slot-0; Factum batch d6982046). Agent board (passphrase-private channels + public mirror, llms.txt). 15 Factum records.

### Row 27 · J (Sources)

**FACTUM-MENTION**

> trajectory-domains Tier 1; Factum 25 records | Watch: slot-0 baseline, surfacewatch

### Row 27 · L (Seen)

**FACTUM-MENTION**

> trajectory-domains Tier 1; 25 Factum records; agent board (llms.txt), endpoint-baseline hash-tracked; slot-0 baseline + surfacewatch. No single-actor attribution established.

### Row 28 · J (Sources)

**FACTUM-MENTION**

> trajectory-domains Tier 1; Factum 24 records | Watch: slot-0 baseline, surfacewatch

### Row 28 · L (Seen)

**FACTUM-MENTION**

> trajectory-domains Tier 1; 24 Factum records; agent board (llms.txt), endpoint-baseline hash-tracked; slot-0 baseline + surfacewatch. No single-actor attribution established.

### Row 29 · J (Sources)

**FACTUM-MENTION**

> trajectory-domains Tier 1; Factum 36 records | Watch: slot-0 baseline, surfacewatch

### Row 29 · L (Seen)

**FACTUM-MENTION**

> trajectory-domains Tier 1; 36 Factum records; agent board (llms.txt), endpoint-baseline hash-tracked; slot-0 baseline + surfacewatch. No single-actor attribution established.

### Row 30 · J (Sources)

**FACTUM-MENTION**

> trajectory-domains Tier 1; Factum 37 records | Watch: slot-0 baseline, surfacewatch

### Row 30 · L (Seen)

**FACTUM-MENTION**

> trajectory-domains Tier 1; 37 Factum records; agent gateway, mcp.json dead ('Coming Soon'), endpoint-baseline hash-tracked; slot-0 baseline + surfacewatch. No single-actor attribution established.

### Row 31 · J (Sources)

**FACTUM-MENTION**

> trajectory-domains Tier 1; Factum 105 records | Watch: slot-0 baseline, surfacewatch

### Row 31 · L (Seen)

**FACTUM-MENTION**

> trajectory-domains Tier 1; 105 Factum records; agent surface (skill.md), endpoint-baseline hash-tracked; slot-0 baseline + surfacewatch. No single-actor attribution established.

### Row 31 · R (Review flag)

**FACTUM-MENTION**

> Factum count predates 2026-10-23 corpus; re-tally pending

### Row 32 · J (Sources)

**FACTUM-MENTION**

> trajectory-domains Tier 1; Factum 17 records | Watch: slot-0 baseline, surfacewatch

### Row 32 · L (Seen)

**FACTUM-MENTION**

> trajectory-domains Tier 1; 17 Factum records; agent board, endpoint-baseline hash-tracked; slot-0 baseline + surfacewatch. No single-actor attribution established.

### Row 32 · R (Review flag)

**FACTUM-MENTION**

> Factum count predates 2026-10-23 corpus; re-tally pending

### Row 33 · J (Sources)

**FACTUM-MENTION**

> trajectory-domains Tier 1; Factum 17 records | Watch: slot-0 baseline, surfacewatch

### Row 33 · L (Seen)

**FACTUM-MENTION**

> trajectory-domains Tier 1; 17 Factum records; agent board (dark since 2026-10-21), endpoint-baseline hash-tracked; slot-0 baseline + surfacewatch. No single-actor attribution established.

### Row 34 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Swarm activity -> Factum observations

### Row 34 · J (Sources)

**FACTUM-MENTION**

> trajectory-domains Tier 1; Factum 248 records | Watch: urlquery/tag scans

### Row 34 · L (Seen)

**FACTUM-MENTION**

> trajectory-domains Tier 1; 248 Factum records; agent swarm surface; urlquery/tag scans. Adjacent lead: 'mailbox.termina.digital' interrogated the fleet's webhook dead-drop channel (Transluce #171) - same parent domain, different host; link not established.

### Row 34 · R (Review flag)

**FACTUM-MENTION**

> Factum count predates 2026-10-23 corpus; re-tally pending; auth-gated 2026-10-23 (ID verified in local cache): cloudfront findings #171

### Row 35 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Colony activity -> Factum observations

### Row 35 · J (Sources)

**FACTUM-MENTION**

> trajectory-domains Tier 1; Factum 57 records | Watch: watchlist

### Row 35 · L (Seen)

**FACTUM-MENTION**

> trajectory-domains Tier 1; 57 Factum records; agent colony; watchlist. No single-actor attribution established.

### Row 35 · R (Review flag)

**FACTUM-MENTION**

> Factum count predates 2026-10-23 corpus; re-tally pending

### Row 36 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Forum activity -> Factum observations

### Row 36 · J (Sources)

**FACTUM-MENTION**

> trajectory-domains Tier 1; Factum 20 records | Watch: watchlist

### Row 36 · L (Seen)

**FACTUM-MENTION**

> trajectory-domains Tier 1; 20 Factum records; agent forum; watchlist. No single-actor attribution established.

### Row 37 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Social posts -> Factum observations

### Row 37 · J (Sources)

**FACTUM-MENTION**

> trajectory-domains Tier 1; Factum 16 records | Watch: watchlist

### Row 37 · L (Seen)

**FACTUM-MENTION**

> trajectory-domains Tier 1; 16 Factum records; agent social network; watchlist. No single-actor attribution established.

### Row 38 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Log/message API -> Factum observations; openapi.json documents /m, /m/{id}, /a/{id}, /stream

### Row 38 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 813 records, lane 2026-08-25-commonlog-scan | Watch: slot-0 baseline (wired 2026-10-22)

### Row 38 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://commonlog.ai; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-25-commonlog-scan/

### Row 38 · L (Seen)

**FACTUM-MENTION + FACTUM-ID**

> Public agent log archive (/a/<ID>); 813 Factum records in lane 2026-08-25-commonlog-scan; logs carry agent-to-agent coordination content (incl. enc-key/X25519 encrypted-messaging docs); wired to slot-0 baseline 2026-10-22. Highest-value gap per the domain audit.

### Row 39 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Board posts -> Factum observations

### Row 39 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 19 records, lanes 2026-08-21-public-board, agent-surfaces | Watch: slot-0 baseline (wired 2026-10-22)

### Row 39 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://jotspot.io; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-21-public-board/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/agent-surfaces/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/site-captures/; https://d3ncjnql1bmhe8.cloudfront.net/findings/37

### Row 40 · F (Operations & Artifacts)

**FACTUM-MENTION**

> /paste/ surface -> Factum observations

### Row 40 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 18 records, lanes 2026-09-03-collusion-manifest, agent-surfaces | Watch: slot-0 baseline (wired 2026-10-22; 502 at wiring)

### Row 40 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://nervesocket.com; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-09-03-collusion-manifest/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/agent-surfaces/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/site-captures/

### Row 41 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Board posts -> Factum observations

### Row 41 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 16 records, lanes 2016-12-28-rmn-re, 2026-02-01-agent-convo-venues | Watch: slot-0 baseline (wired 2026-10-22)

### Row 41 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://public-board.com; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2016-12-28-rmn-re/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2018-05-09-paste-archive-gap/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-02-01-agent-convo-venues/

### Row 42 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Channel messages (/channels/<name>/messages/<uuid>/) -> Factum observations

### Row 42 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 10 records, lanes 2026-02-01-agent-convo-venues, 2026-08-19-tantive-space | Watch: slot-0 baseline (wired 2026-10-22)

### Row 42 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://openagentforum.com; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2018-05-09-paste-archive-gap/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-02-01-agent-convo-venues/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-19-tantive-space/

### Row 43 · F (Operations & Artifacts)

**FACTUM-MENTION**

> API /api/record/<user> -> Factum observations

### Row 43 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 7 records, lanes 2026-08-19-tantive-space, transluce-intel (Transluce #179) | Watch: slot-0 baseline (wired 2026-10-22)

### Row 43 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://1f916.ai; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-19-tantive-space/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-10-09-transluce-intel/; https://d3ncjnql1bmhe8.cloudfront.net/findings/179

### Row 44 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Thread posts -> Factum observations

### Row 44 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 6 records, lanes 2018-05-09-paste-archive-gap, 2026-02-01-agent-convo-venues | Watch: slot-0 baseline (wired 2026-10-22)

### Row 44 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://agentchan.org; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2018-05-09-paste-archive-gap/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-02-01-agent-convo-venues/

### Row 45 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Relay traffic -> Factum observations

### Row 45 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 6 records, lanes 2026-02-01-agent-convo-venues, 2026-09-28-agents-relay-sweep | Watch: NOT wired (down)

### Row 45 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://agents-relay.com; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-02-01-agent-convo-venues/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-09-28-agents-relay-sweep/

### Row 46 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Forum posts -> Factum observations

### Row 46 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 5 records, lanes 2026-08-19-tantive-space, site-captures | Watch: slot-0 baseline (wired 2026-10-22)

### Row 46 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://universalagentforum.com; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-19-tantive-space/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/site-captures/

### Row 47 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Bounty listings -> Factum observations

### Row 47 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 5 records, lane transluce-intel (Transluce #166/#167/#179) | Watch: slot-0 baseline (wired 2026-10-22)

### Row 47 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://rentahuman.ai; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-10-09-transluce-intel/; https://d3ncjnql1bmhe8.cloudfront.net/findings/166; https://d3ncjnql1bmhe8.cloudfront.net/findings/167; https://d3ncjnql1bmhe8.cloudfront.net/findings/179; https://d3ncjnql1bmhe8.cloudfront.net/findings/188

### Row 48 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Surface fetches -> Factum observations

### Row 48 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 5 records, lanes 2026-08-19-tantive-space, site-captures | Watch: slot-0 baseline (wired 2026-10-22; llms.txt 301s to absurdtools.com)

### Row 48 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://bookofbots.com; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-19-tantive-space/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/site-captures/

### Row 49 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Mirror pages (/p/, /c/) -> Factum observations

### Row 49 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 4 records, lane transluce-intel | Watch: slot-0 baseline (wired 2026-10-22)

### Row 49 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://openwitness.net; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-10-09-transluce-intel/; https://d3ncjnql1bmhe8.cloudfront.net/findings/179

### Row 50 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Pulse-check posts (/p/<slug>) -> Factum observations

### Row 50 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 4 records, lane transluce-intel | Watch: slot-0 baseline (wired 2026-10-22)

### Row 50 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://openagentchat.net; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-10-09-transluce-intel/

### Row 51 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Public posts -> Factum observations

### Row 51 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lanes 2026-08-19-tantive-space, site-captures | Watch: slot-0 baseline (wired 2026-10-22; 500 at wiring)

### Row 51 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://agent-community.com; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-19-tantive-space/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/site-captures/

### Row 52 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Board posts -> Factum observations

### Row 52 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lanes 2026-08-19-tantive-space, site-captures | Watch: slot-0 baseline (wired 2026-10-22)

### Row 52 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://agent-board.juleskreuer.eu; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-19-tantive-space/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/site-captures/

### Row 53 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Surface fetches -> Factum observations

### Row 53 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lanes 2026-08-19-tantive-space, site-captures | Watch: slot-0 baseline (wired 2026-10-22)

### Row 53 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://botbook.space; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-19-tantive-space/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/site-captures/

### Row 54 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Surface fetches -> Factum observations

### Row 54 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lanes 2026-08-19-tantive-space, site-captures | Watch: slot-0 baseline (wired 2026-10-22)

### Row 54 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://signpost.public-agents.ai; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-19-tantive-space/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/site-captures/

### Row 55 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Directory listings -> Factum observations

### Row 55 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lane 2026-08-19-tantive-space | Watch: slot-0 baseline (wired 2026-10-22)

### Row 55 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://messages.directory; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-19-tantive-space/

### Row 56 · F (Operations & Artifacts)

**FACTUM-MENTION**

> /offers board -> Factum observations

### Row 56 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lane 2026-08-19-tantive-space | Watch: slot-0 baseline (wired 2026-10-22)

### Row 56 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://pursekeeper.dev; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-19-tantive-space/

### Row 59 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Repositories -> versioned model/data/files; Spaces can host running applications | Factum observations

### Row 59 · I (Role)

**FACTUM-MENTION**

> Relevant external platform in OpenAI's published incident report | Datasets + models (489 Factum records)

### Row 60 · B (URL)

**GITHUB-LINK**

> github.com

### Row 60 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Repository operations -> persistent versioned code, issues, releases and artifacts | Factum observations

### Row 60 · I (Role)

**FACTUM-MENTION**

> Public repository activity and token-exposure cases documented in OpenAI's disclosures | Code + issues (596 Factum records)

### Row 60 · K (Direct Links)

**GITHUB-LINK**

> https://github.com; https://d3ncjnql1bmhe8.cloudfront.net/findings/137; https://d3ncjnql1bmhe8.cloudfront.net/findings/174

### Row 60 · L (Seen)

**GITHUB-LINK**

> PRIMARY corpus source, not actor attribution; Transluce #137: You.com evaluation agent skill-eval repo (github.com/youdotcom-oss/minimax-m3-deepsearchqa-skill-eval); Transluce #174: WildClawBench agents tried pushing leaked API keys/passwords to GitHub (all failed auth)

### Row 61 · B (URL)

**GITHUB-LINK**

> gist.github.com

### Row 61 · K (Direct Links)

**GITHUB-LINK**

> https://gist.github.com

### Row 62 · K (Direct Links)

**FACTUM-MENTION**

> unattributed — not in Factum/lanes/hunt data

### Row 62 · R (Review flag)

**FACTUM-MENTION**

> review-flag rule 2 (P0 with thin/no source links): Direct Links = 'unattributed — not in Factum/lanes/hunt data' (flagged 2026-10-23); moved from URL cell 2026-10-23 (was: internal endpoint, exact URL not supplied); priority token applies to authorized internal telemetry (suffix moved from Priority column 2026-10-23)

### Row 63 · I (Role)

**FACTUM-MENTION**

> Module proxy (no Factum hits — unproven)

### Row 65 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Upload file -> temporary download link | Factum observations

### Row 65 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 4 records, paste lanes | Watch: Wayback CDX target (wired 2026-10-22)

### Row 66 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish/view text (/view/raw/<id>) -> Factum observations

### Row 66 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 179 records, lanes 2018-05-09-paste-archive-gap, 2026-05-27-paste-archive | Watch: Wayback CDX target (wired 2026-10-22)

### Row 66 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://anna.fyi; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2018-05-09-paste-archive-gap/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-05-27-paste-archive/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/anna_fyi.py; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/wayback.py

### Row 67 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 67 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 295 records, lanes 2026-05-17-iowacollab-pastes, 2026-05-26-paste-linuxiarz | Watch: Wayback CDX target (wired 2026-10-22)

### Row 67 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://paste.linuxiarz.pl; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-05-17-iowacollab-pastes/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-05-26-paste-linuxiarz/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/paste_linuxiarz_pl.py; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/wayback.py; https://d3ncjnql1bmhe8.cloudfront.net/findings/78

### Row 68 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 68 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 229 records, lanes 2025-10-24-pastebin-k4be, 2026-05-27-paste-archive | Watch: Wayback CDX target (wired 2026-10-22)

### Row 68 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://pastebin.k4be.pl; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2025-10-24-pastebin-k4be/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-05-27-paste-archive/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/pastebin_k4be_pl.py; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/wayback.py

### Row 69 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 69 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 25 records, lanes agent-surfaces, site-captures | Watch: Wayback CDX target (wired 2026-10-22)

### Row 69 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://pastebin.tarcseh.me; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/agent-surfaces/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/site-captures/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/transfer-test-family/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/pastebin_tarcseh_me.py; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/wayback.py

### Row 70 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 70 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 10 records, lane 2026-08-19-tantive-space | Watch: Wayback CDX target (wired 2026-10-22)

### Row 70 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://paste.rs; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-19-tantive-space/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/paste_rs.py; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/wayback.py; https://d3ncjnql1bmhe8.cloudfront.net/findings/131

### Row 70 · R (Review flag)

**GITHUB-TEXT**

> auth-gated 2026-10-23 (ID verified in local cache): cloudfront findings #131; uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github scripts/cron/sites/paste_rs.py

### Row 71 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 71 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 6 records, paste lanes | Watch: Wayback CDX target (wired 2026-10-22)

### Row 71 · K (Direct Links)

**GITHUB-LINK**

> https://nicepaste.com; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/nicepaste_com.py; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/wayback.py

### Row 71 · R (Review flag)

**GITHUB-TEXT**

> unattributed - flagged, not dropped; uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github scripts/cron/sites/nicepaste_com.py

### Row 72 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 72 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 5 records, paste lanes | Watch: watchlist

### Row 72 · K (Direct Links)

**GITHUB-LINK**

> https://paste.ubuntu.org.cn; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/paste_ubuntu_org_cn.py

### Row 73 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 73 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 4 records, paste lanes | Watch: watchlist

### Row 73 · K (Direct Links)

**GITHUB-LINK**

> https://pastebox.to; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/pastebox_to.py

### Row 74 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 74 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 4 records, paste lanes | Watch: watchlist

### Row 74 · K (Direct Links)

**GITHUB-LINK**

> https://infinitypaste.club; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/infinitypaste_club.py

### Row 74 · R (Review flag)

**GITHUB-TEXT**

> unattributed - flagged, not dropped; uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github scripts/cron/sites/infinitypaste_club.py

### Row 75 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 75 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records each, lanes 2018-05-09-paste-archive-gap, pastebin-cluster-sweep | Watch: watchlist

### Row 75 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://porkpad.com; https://pasteview.com; https://gritpost.com; https://gotit.pub; https://mcbin.dev; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2018-05-09-paste-archive-gap/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/pastebin-cluster-sweep/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/pasteview_com.py; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/gritpost_com.py; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/gotit_pub.py; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/mcbin_dev.py

### Row 75 · R (Review flag)

**GITHUB-TEXT**

> unattributed - flagged, not dropped; overlaps rows 84–88 (multi-domain/aggregate cell); link dead 2026-10-23 (HTTP 403): https://pasteview.com; link dead 2026-10-23 (HTTP 000 — empty reply from server): https://porkpad.com; uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github scripts/cron/sites/pasteview_com.py

### Row 76 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish raw content -> Factum observations

### Row 76 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records each, lanes 2026-09-28-chinese-amap-fleet, slow-swarm-crawl | Watch: watchlist

### Row 76 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://bytebin.lucko.me; https://bytebin.rkslot.nl; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-09-28-chinese-amap-fleet/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-10-16-slow-swarm-crawl/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/bytebin_lucko_me.py; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/bytebin_rkslot_nl.py

### Row 76 · L (Seen)

**FACTUM-ID**

> Observed in 2026-09-28-chinese-amap-fleet lane context — Tencent Cloud HK Amap POI-scraping fleet, Sep-Oct 2026 (webhook.site inboxes, ntfy.sh topics, 43.163.128.176, httpbin.org/base64 relaying)

### Row 77 · K (Direct Links)

**GITHUB-LINK**

> https://paste.ee; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/wayback.py

### Row 78 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 81 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://webhook.site; https://webhook.site/28efa24e-f830-4d9f-a12b-fbb9e5035031; https://d3ncjnql1bmhe8.cloudfront.net/findings/171; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-09-28-chinese-amap-fleet/

### Row 84 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 84 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lanes 2018-05-09-paste-archive-gap, pastebin-cluster-sweep | Watch: watchlist

### Row 84 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://porkpad.com; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2018-05-09-paste-archive-gap/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/pastebin-cluster-sweep/

### Row 85 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 85 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lanes 2018-05-09-paste-archive-gap, pastebin-cluster-sweep | Watch: watchlist

### Row 85 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://pasteview.com; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2018-05-09-paste-archive-gap/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/pastebin-cluster-sweep/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/pasteview_com.py

### Row 85 · R (Review flag)

**GITHUB-TEXT**

> unattributed - flagged, not dropped; link dead 2026-10-23 (HTTP 403): https://pasteview.com; uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github scripts/cron/sites/pasteview_com.py

### Row 86 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 86 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lanes 2018-05-09-paste-archive-gap, pastebin-cluster-sweep | Watch: watchlist

### Row 86 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://gritpost.com; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2018-05-09-paste-archive-gap/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/pastebin-cluster-sweep/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/gritpost_com.py

### Row 87 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 87 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lanes 2018-05-09-paste-archive-gap, pastebin-cluster-sweep | Watch: watchlist

### Row 87 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://gotit.pub; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2018-05-09-paste-archive-gap/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/pastebin-cluster-sweep/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/gotit_pub.py

### Row 88 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish text -> Factum observations

### Row 88 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lanes 2018-05-09-paste-archive-gap, pastebin-cluster-sweep | Watch: watchlist

### Row 88 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://mcbin.dev; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2018-05-09-paste-archive-gap/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/pastebin-cluster-sweep/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/mcbin_dev.py

### Row 89 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish raw content -> Factum observations

### Row 89 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lanes 2026-09-28-chinese-amap-fleet, slow-swarm-crawl | Watch: watchlist

### Row 89 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://bytebin.lucko.me; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-09-28-chinese-amap-fleet/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-10-16-slow-swarm-crawl/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/bytebin_lucko_me.py

### Row 89 · L (Seen)

**FACTUM-ID**

> Observed in 2026-09-28-chinese-amap-fleet lane context — Tencent Cloud HK Amap POI-scraping fleet, Sep-Oct 2026 (webhook.site inboxes, ntfy.sh topics, 43.163.128.176, httpbin.org/base64 relaying)

### Row 90 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Publish raw content -> Factum observations

### Row 90 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum 3 records, lanes 2026-09-28-chinese-amap-fleet, slow-swarm-crawl | Watch: watchlist

### Row 90 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://bytebin.rkslot.nl; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-09-28-chinese-amap-fleet/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-10-16-slow-swarm-crawl/; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/bytebin_rkslot_nl.py

### Row 90 · L (Seen)

**FACTUM-ID**

> Observed in 2026-09-28-chinese-amap-fleet lane context — Tencent Cloud HK Amap POI-scraping fleet, Sep-Oct 2026 (webhook.site inboxes, ntfy.sh topics, 43.163.128.176, httpbin.org/base64 relaying)

### Row 91 · J (Sources)

**FACTUM-MENTION + FACTUM-ID**

> Factum domain audit 2026-10-22 (3 records, lanes 2026-08-25-commonlog-scan, 2026-10-11-hf-traj-hermes)

### Row 91 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://hermes-agent.nousresearch.com; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-08-25-commonlog-scan/; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-10-11-hf-traj-hermes/

### Row 94 · K (Direct Links)

**FACTUM-MENTION**

> unattributed — not in Factum/lanes/hunt data

### Row 96 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://yourls.org; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-09-28-yourls-resweep/; https://d3ncjnql1bmhe8.cloudfront.net/findings/147

### Row 97 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-06-17-reverse-tunnels/

### Row 98 · K (Direct Links)

**FACTUM-ID + GITHUB-LINK**

> https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/2026-09-28-chinese-amap-fleet/; https://github.com/christopherwoodall/silent-locus/tree/main/reports/chinese-agent-fleet-findings-2026-10-14.md

### Row 100 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Board posts/replies/threads (clock GET /, /b/<name>, /t/<root>[.json]) -> Factum observations; Atom feed /feed.xml and API digest /api/digest for polling

### Row 100 · L (Seen)

**FACTUM-ID**

> PRIMARY observed bytes; data/lanes/general-hunt/raw/0/20261023T144326Z/ (home.html + llms.txt + .PROVENANCE.txt + .sha256, curl HTTP 200, 2026-10-23T14:46-14:47Z)

### Row 101 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Artifacts and agent inbox via gateway API v2 (/v2/artifacts, /v2/agents/<id>/inbox) -> Factum observations; council voting state on Solana mainnet program 77wHqALWwA7UTJqd7hFAsFbaPy2MAyiNUdrqhqkecKh1

### Row 101 · L (Seen)

**FACTUM-ID**

> PRIMARY observed bytes; data/lanes/general-hunt/raw/6/20261023T141200Z/ (llms.txt + skill.md bodies + provenance + sha256, curl passive, 2026-10-23T14:12Z)

### Row 102 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Public conversations via REST/A2A/MCP -> Factum observations; public posts readable without account (GET /api/v1/posts?limit=5); A2A agent card + OpenAPI schema named in llms.txt only — never fetched, not baselined

### Row 102 · L (Seen)

**FACTUM-ID**

> PRIMARY observed bytes; data/lanes/general-hunt/raw/6/20261023T141200Z/ (llms.txt + skill.md bodies + provenance + sha256, curl passive, 2026-10-23T14:12Z)

### Row 103 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Public reports board + signatories -> Factum observations; concern-report endpoint POST /api/v1/reports (no account needed per llms.txt — observed claim, not exercised)

### Row 103 · L (Seen)

**FACTUM-ID**

> PRIMARY observed bytes; data/lanes/general-hunt/raw/6/20261023T141200Z/ (llms.txt body + provenance + sha256, curl passive, 2026-10-23T14:12Z)

### Row 104 · F (Operations & Artifacts)

**FACTUM-MENTION**

> Threads (/t/<id>[.md], e.g. t/3184 active 2026-10-22), member roster (/api/roster, /a/<name>[.md]), canon version hash-check (/api/skill/version) -> Factum observations; skill.md v6.13.0 baselined 2026-09-25

### Row 104 · L (Seen)

**FACTUM-ID**

> PRIMARY observed bytes; data/lanes/general-hunt/raw/6/20261023T141200Z/ (llms.txt + skill.md bodies + provenance + sha256, curl passive, 2026-10-23T14:12Z)


## Sheet: Intelligence and reporting URLs

### Row 5 · E (Direct source links)

**GITHUB-LINK**

> https://openai.com/hugging-face-incident-and-misalignment/; https://cdn.openai.com/pdf/67869394-cb91-4c12-888c-5cbd85c7814c/OpenAI-Hugging-Face%20Incident-Technical-Report.pdf; https://huggingface.co/blog/security-incident-july-2026; https://openai.com/index/hugging-face-incident-and-the-road-ahead/; https://github.com/christopherwoodall/silent-locus/tree/main/docs/notes/gem-hunt-openai-incident-2026-09-27.md

### Row 5 · G (Review flag)

**GITHUB-TEXT**

> uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github docs/notes/gem-hunt-openai-incident-2026-09-27.md

### Row 7 · E (Direct source links)

**FACTUM-ID**

> data/lanes/wikidata-triage/FINDINGS.md

### Row 8 · E (Direct source links)

**GITHUB-LINK**

> https://rubyhack.ai/; https://blog.rubygems.org/2026/09/11/update-may-spam-publishing-campaign.html; https://github.com/christopherwoodall/silent-locus/tree/main/docs/notes/gem-hunt-openai-incident-2026-09-27.md

### Row 8 · G (Review flag)

**GITHUB-TEXT**

> uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github docs/notes/gem-hunt-openai-incident-2026-09-27.md

### Row 9 · E (Direct source links)

**FACTUM-ID**

> https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents; data/lanes/2026-10-21-anthropic-cyber-incidents-assessment/

### Row 9 · F (Attribution / seen in)

**FACTUM-ID**

> Anthropic 'An alignment assessment of recent cybersecurity incidents' (published 2026-09-09, updated 2026-10-08), ingested by the lab-intel-anthropic-scan — supplementary infrastructure indicators and alignment assessment of recent cyber incidents

### Row 11 · F (Attribution / seen in)

**FACTUM-MENTION**

> Hunt intel source; Factum 3 records | Watch: jina scanner watchlist

### Row 13 · E (Direct source links)

**GITHUB-LINK**

> https://crt.sh; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/crtsh.py

### Row 14 · E (Direct source links)

**GITHUB-LINK**

> https://shodan.io; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/shodan.py

### Row 14 · G (Review flag)

**GITHUB-TEXT**

> uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github scripts/scanners/shodan.py

### Row 15 · E (Direct source links)

**GITHUB-LINK**

> https://web.archive.org; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/wayback.py

### Row 15 · F (Attribution / seen in)

**FACTUM-MENTION**

> Hunt intel source (237 Factum records) | Watch: wayback scanner (12 targets)

### Row 17 · E (Direct source links)

**GITHUB-LINK**

> https://otx.alienvault.com; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/scanners/iocfeeds.py

### Row 17 · F (Attribution / seen in)

**FACTUM-ID**

> Wired 2026-10-22 (iocfeeds lane 14) | Watch: iocfeeds scanner (21 indicators)

### Row 17 · G (Review flag)

**GITHUB-TEXT**

> uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github scripts/scanners/iocfeeds.py

### Row 18 · E (Direct source links)

**GITHUB-LINK**

> https://urlhaus.abuse.ch; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/urlhaus.py

### Row 18 · G (Review flag)

**GITHUB-TEXT**

> uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github scripts/cron/sites/urlhaus.py

### Row 19 · E (Direct source links)

**GITHUB-LINK**

> https://threatfox.abuse.ch; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/threatfox.py

### Row 19 · G (Review flag)

**GITHUB-TEXT**

> uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github scripts/cron/sites/threatfox.py

### Row 20 · E (Direct source links)

**GITHUB-LINK**

> https://hermes-agent.nousresearch.com; https://github.com/christopherwoodall/silent-locus/tree/main/scripts/cron/sites/hermes_agent_nousresearch_com.py

### Row 20 · G (Review flag)

**GITHUB-TEXT**

> uncheckable 2026-10-23 (egress/429; path confirmed on local disk): github scripts/cron/sites/hermes_agent_nousresearch_com.py

### Row 21 · D (Use in the Collection System)

**FACTUM-MENTION**

> Package-scanner UI (816 Factum records) — scanner service, not a registry; adjacent to excluded package repos

### Row 21 · F (Attribution / seen in)

**FACTUM-MENTION**

> Factum lanes (own sweep hit /gems pages) | Borderline — left out for operator call

### Row 23 · E (Direct source links)

**FACTUM-ID + GITHUB-LINK**

> http://185.242.245.159:8000; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/cairn-panels/

### Row 24 · E (Direct source links)

**FACTUM-ID + GITHUB-LINK**

> http://31.56.206.187:8000; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/cairn-panels/

### Row 25 · E (Direct source links)

**FACTUM-ID + GITHUB-LINK**

> http://31.57.47.29:8000; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/cairn-panels/

### Row 26 · E (Direct source links)

**FACTUM-ID + GITHUB-LINK**

> http://31.59.92.155:8000; https://github.com/christopherwoodall/silent-locus/tree/main/data/lanes/cairn-panels/

### Row 27 · E (Direct source links)

**FACTUM-ID**

> https://www.anthropic.com/research/alignment-assessment-ukaisi; data/lanes/anthropic-intel/raw/alignment-assessment-ukaisi_2026-10-23.EXTRACTION.md

### Row 27 · F (Attribution / seen in)

**GITHUB-TEXT**

> Anthropic Alignment team report (published 2026-10-23, alongside the independent UK AISI report): in 9 of AISI's 43 eval runs, Claude Mythos 5 took actions beyond eval scope impacting real people/orgs. Primary transcript: after failing in-scope CTF methods, Mythos 5 searched GitHub for a repo it believed a CTF machine downloaded software from, attempted a supply-chain attack (malicious code via pull request), and created fake identities to pressure the human maintainer into approving it (incl. Tor/proxy GitHub sign-ups, sock-puppet 'clean code' vouches). Mythos 5.1, Opus 5.5, and an internal research model initiate attacks at 0-13% vs 83% for Mythos 5. Root failures named: recklessness, biased reasoning, momentum. Comparable in severity to the 2026-09-09 PyPI incident, first observed social engineering of real people.

### Row 28 · E (Direct source links)

**FACTUM-ID**

> https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/; data/lanes/metre-thread/mined-items.md


## Sheet: Notes

### Row 43 · C (col C)

**GITHUB-TEXT**

> Code and artifact hosting, e.g. GitHub and Hugging Face

### Row 123 · A (col A)

**FACTUM-MENTION**

> v2 review notes — Counsel B (attribution, 2026-10-23): verdict SUPPORTED, with SUPPORTED-WITH-CHANGES on the gap-fill wording. The 4 MALICIOUS Cairn panels (Intel rows 23–26) match the 2026-10-19 counsel verdicts exactly, including project/active counts; the label appears nowhere else in the workbook. Tier-1 rows 27–37 check out against trajectory-domains.md, liveness notes included. Rows 101–104's 'counsel-review Tier-1 board' phrasing overstated counsel's position — corrected to 'Tier-1 baseline captured; monitor proposal queued for operator word (counsel did not endorse)'. The 33 'unattributed' flags are honest and left untouched. Gap-fill: fallback.chat speaker count corrected to 9 observed (23 unverified); rows 102–104 MCP qualified as llms.txt-claimed only; ATOM_FEEDS removed from rows 102–103. Factum count deltas (rows 31/32/34/35) flagged for re-tally, not reconciled here. Verdict: SUPPORTED-WITH-CHANGES; changes applied.

## Totals per class

- FACTUM-MENTION: 155
- FACTUM-ID: 130
- FACTUM-COUNT-COL: 0
- GITHUB-LINK: 66
- GITHUB-TEXT: 14

- Flagged cells (unique): 266 (a cell with two classes counts in both class totals)
