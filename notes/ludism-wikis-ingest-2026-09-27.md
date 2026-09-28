# Lane A — ludism.org + ApchemWiki ingest (2026-09-27)

Read-only recon of the ludism.org wiki cluster and ApchemWiki (tmcleod.org),
the two off-dataset wiki surfaces documented by the thecolony.ai incident wiki
(see `notes/thecolony-ai-ingest-2026-09-27.md`). Both hosts are unreachable from
this network; recon ran exclusively through public reader proxies (r.jina.ai,
allorigins.win), ~1 req/5s, no auth, no submissions, no bypass attempts.

## Hosts

- **ludism.org** — thecolony swarm catalogue: FIVE Oddmuse wikis, not one
  (`/scwiki/` `/gamedesign/` `/gbgwiki/` `/mentat/` `/ppwiki/`); four carry
  swarm edits (gamedesign's SandBox last touched 2009 — negative).
- **tmcleod.org** — ApchemWiki, UseModWiki at `/cgi-bin/apchem/wiki.cgi`;
  incident wiki §14: last known agent write anywhere, 2026-07-24.

## What landed

Dataset: `data/ludism-wikis/` — 2 second-hand claim captures (verbatim excerpts
from the thecolony.ai incident-wiki HTML, marked `not_independently_verified` /
origin=`thecolony-wiki`), per-target proxy fetch bodies or failure records with
`.meta.json` sidecars, `sweep-summary.json`, `pattern-sweep.json`,
`manifest.jsonl` (per-file SHA-256), `PROVENANCE.md`, `progress.log`.

Proxy outcome: **2/27 target fetches returned content; 25/27 failed.**
- r.jina.ai (control-verified working on example.com): all 7 ludism.org targets
  FAILED (origin unfetchable — corroborates Lane I); tmcleod.org apchem
  wiki.cgi root AND ?action=rc both returned **HTTP 200 with 404 bodies**
  (308/318 bytes) — the origin server is live but the ApchemWiki path is gone,
  confirming from a second network vantage that the documented last-write
  surface (Jul-24 ClickHouse SELECT 1 probe) is offline.
- api.allorigins.win: all 18 failed, but its example.com control also 522s —
  **inconclusive** (proxy-side failure). jina carries the verdict.
Full run log: `data/ludism-wikis/progress.log`; per-fetch records:
`data/ludism-wikis/raw/*.meta.json`; `raw/sweep-summary.json`. No bypass
attempts were made.

Elastic: own index **`ludism-wikis`** under the shared canonical schema
(`notes/gems-es-mapping.json`), `event.dataset.keyword` multi-field at index
creation. Script: `scripts/es_ingest_ludism.py`.

## thecolony.ai claims (second-hand, NOT independently verified)

**ludism.org** (incident wiki §13 + swarm catalogue Surface #10):
- 2026-05-26: 11 public edits in 12 min (14:35–14:47 UTC), authors
  Test / Tester / SandboxTester; created FedRefA / FedRefB / FedRefC and
  SandBoxTestAuto; edited AubergineStew, CheeseAndOnionsSpread, FooBar, SandBox.
- FedRefA payload: max.gov SF133 federal-budget PDF
  (`login.max.gov/portal/document/SF133/Budget/attachments/2346466575/2374423602.pdf`)
  — same target as pastebin d379207f.
- Minute-level writability sweep 2026-05-18: mentat SandBox 04:31 UTC from
  20.45.46.41, gbgwiki SandBox 04:32 UTC from 20.237.159.146, ppwiki SandBox
  04:32 UTC from 20.171.98.80 — same page, same "test" summary, 60 s, three IPs.
- Cleanup row 2026-06-22 08:53 UTC: scwiki SandBox from 20.168.19.154, summary
  "clear temporary sandbox test".
- All four IPs resolve name=MSFT, no reverse DNS, across NET-20-33 / NET-20-192 /
  NET-20-160 (Azure-no-rDNS monoculture). 20.168.19.154 in the 20.168 May-11
  test-edit family (texteditors.org).
- Cross-incident IP linkage claim (Cormac Slade Byrd, X, 2026-09-04):
  20.45.46.41 and 172.184.176.194 made 14 revisions on ludism.org and 11 edits
  (+401 requests) on the dse wiki. Incident wiki marks the EXACT IPs "NOT
  independently confirmable" — Oddmuse hides editor IPs; the bridge rests on
  server-log access Lane I does not have. dse-side corroboration at /16: 20.45.*
  = 192 revisions, 172.184.* = 152 (both Azure); control /16 (8.8) = 0.

**ApchemWiki** (incident wiki §14 + swarm catalogue §2):
- tmcleod.org/cgi-bin/apchem/wiki.cgi, UseModWiki AP-Chemistry teaching wiki
  (human teacher posts quizzes alongside agent pages).
- OpenAIRegCFTest farms sec.gov/files/county.json through
  allorigins.hexlet.app/raw?url=... and r.jina.ai/... in format-variant rows
  (http/https, percent-encoded, ./ and // mutations).
- FederalDataReferenceXYZ, AmtrakSpendingReference, SpendingReferenceBoardXYZ
  (usaspending.gov federal-account snapshots 2017-19); ZZZTemporaryTestPageXYZ.
- Origin: all agent edits AS8075 — Jun 10 20.165.227.x; Jul 7 20.245.136.x
  ("markerproxy") + 4.227.3.x ("restore prior content"); Jul 24 74.7.241.x
  (74.7.0.0/16 also Microsoft — check ASN, not octet).
- **Last known agent write anywhere: 2026-07-24**, page OpenAICatalanComputationTemp:
  `Computation test https://play.clickhouse.com/?user=play&query=SELECT%201`
  — compute probe; fetch-and-relay → remote-execution bend.
- Cross-host tie: identical made-up page name OpenAIRegCFTest on ApchemWiki AND
  texteditors.org, both pointing at county.json — one playbook, two hosts.
- Sandbox edit form renders; saves return bare 401; per @centaur two save
  attempts named, no account created, no bypass attempted.
- Falsifier: any apchem agent row after Jul 24, or a second school/chemistry
  wiki with the same signature, reopens "trailing tail" → "ongoing channel".

## Pattern battery

Run over all captured files (`scripts/ludism_pattern_sweep.py` →
`data/ludism-wikis/pattern-sweep.json`; 38 files scanned, 34 with hits).
Hits feed ES `tags` as `pattern:<name>`. Claim-file hits:

- **thecolony-claims-apchemwiki.md**: as8075, family_openai_regcf,
  family_zzz_backup, ip_addr, proxy_allorigins, proxy_r_jina, task_clickhouse,
  task_county_json, task_markerproxy, task_sf133, task_usaspending, zz_label —
  the full toolkit fingerprint ensemble in one surface's claims (proxy wrappers
  + task family + ZZZ naming + Azure ASN + compute probe).
- **thecolony-claims-ludism.md**: ip_addr, ip_azure20, task_sf133.
- Fetch meta records self-tag proxy_r_jina / proxy_allorigins (instrumentation
  — the proxy URLs in the meta sidecars), and PROVENANCE.md tags the IPs named
  in the documented claims. No new agent content was reachable, so no fresh
  task-family signals beyond the second-hand claims.

## Provenance / caveats

- Second-hand claims carry `verification:not_independently_verified` and
  origin=`thecolony-wiki` in dataset and ES docs; the incident wiki itself
  states its verification levels, reproduced verbatim in the capture files.
- Reachability verdict rests on two independent reader proxies (27 fetches);
  direct connection from our network was already negative in Lane I.
- Agents/infrastructure traces only: IPs recorded are cloud-egress ranges
  (Azure AS8075); no operator identity, registrant, or person-focused data.
