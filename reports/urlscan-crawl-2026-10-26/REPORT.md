# urlscan.io crawl — final report, 2026-10-26

## Terms

- **urlscan.io**: a public service that scans web pages and stores scan metadata (page address, page title, scan date, page network address).
- **Fleet marker**: a string that links a scan to the agent fleet we hunt (for example `getPoiInfo`, `uqscan=`, `uqframe=`, `hysandbox`).
- **Triage-passing hit**: a scan result that carries at least one fleet marker or a HIGH-confidence scanner grade.
- **SECONDARY**: evidence from a third-party source, not first-hand capture. All urlscan hits are other people's scan metadata, so they grade SECONDARY by default.
- **OBSERVED**: a claim based on direct observation of the source data.
- **INFERENCE**: a reading drawn from observed facts, not directly observed.
- **Factum**: the structured evidence store in `data/`.
- **Lane**: a work group in Factum. Records in one lane share a tag.
- **Batch**: one exported set of Factum records, in `data/records/<id>/`.

## Result in one line

The crawl found zero new fleet hits in the last 30 days of urlscan search
metadata (metadata only; query-string index coverage unverified). The only
hit ingested by this fleet is one older morning-scan hit that had never
been ingested before (a 3-record batch). That hit is a bare scan of a
public reader service, not agent-relay use. Neither ranked hit below
passed crawl triage (triage-passing count is 0); both are morning-scan
hits reviewed alongside the crawl.

## Coverage table

Crawl run: 2026-10-26T17:02:32Z–17:02:49Z. Anonymous urlscan search API.
Polite rate target was one request per 2 seconds; measured log gaps
averaged about 3.4 seconds. All queries returned HTTP 200.

| Label | Query string | Total | Fetched | Triage-passing |
|---|---|---|---|---|
| getpoiinfo | getPoiInfo | 0 | 0 | 0 |
| uqscan-tag | uqscan= | 0 | 0 | 0 |
| uqframe-tag | uqframe= | 0 | 0 | 0 |
| proxy-marker | hysandbox | 0 | 0 | 0 |
| relay-jina-reader | domain:r.jina.ai | 57 | 57 | 0 |
| title-amap | page.title:"amap" | 17 | 17 | 0 |
| **Total** | | **74** | **74** | **0** |

Each query was fetched exactly once. The task's extra-grammar list overlapped
the enabled config queries in four places. No duplicate fetches occurred.

## Ranked hits

### Rank 1 — Oct 25 morning-scan hit (ingested by this fleet)

- Page scanned: `https://r.jina.ai/ec`.
- urlscan result: `https://urlscan.io/result/01a17355-8853-7179-8623-5d2a48a3e0b5/`.
- Scan time: 2026-10-25T13:52:41Z.
- Page network address: Cloudflare, AS13335, tier 2, label CLOUD_SERVICE.
- Grade: LOW, SECONDARY. Swarm-linked: false.
- Grade disclosure: the morning bundle graded this hit PRIMARY. This
  report grades it SECONDARY instead, and the change is disclosed here.
  The lane's PRIMARY rationale is "scans of jina-proxied URLs". This
  hit has no inner target, so that rationale does not attach. The
  false-positives doc grades urlscan hits as other people's scan
  metadata, which is SECONDARY.
- What it is (OBSERVED): a scan of the reader service's own front page.
  No inner target address appears after the reader host. No fleet marker
  appears in the metadata.
- What it is not (adversarial verdict): it is not agent-relay use. Relay
  use would show a target address after the reader host. None appears.
  Better fits are a reader-service health check, a third-party uptime
  monitor, or a researcher scan.
- Novelty: the specific scan is new to the corpus, where corpus means
  the Factum record store, not merely absent from repo working files.
  Pre-ingest dedup found no corpus record for this scan UUID or result
  address. The page-address claim is narrowed: fuzzy search returned 25
  generic `r.jina.ai` relay mentions from other lanes, none holding
  this page or this scan. The relay service itself is already known
  from other lanes. This hit is not new to the operator: it was
  already surfaced in the Oct 25 morning-scan report. It was only
  un-ingested, until now.
- Factum batch: `data/records/a3fc917d22794d0eb9dbea8ba6b1d405/`
  (3 records, all `tags.lane=urlscan`). See "Ingest" below.

### Rank 2 — Oct 26 morning-scan hit (observed, NOT ingested by this fleet)

- Page scanned: `https://r.jina.ai/ec` (same page as Rank 1).
- urlscan result: `https://urlscan.io/result/01a1787e-fe16-745d-9831-d0642306fcb2/`.
- Scan time: 2026-10-26T13:55:56Z.
- Page network address: Cloudflare, AS13335, tier 2, label CLOUD_SERVICE.
- Grade: LOW, SECONDARY. Swarm-linked: false.
- What it is (OBSERVED): the same bare front-page scan, scanned again
  about 24 hours after Rank 1. The two hits differ in scan UUID, scan
  time, and network address family (IPv6 on Oct 25, IPv4 on Oct 26).
  That family difference is consistent with Cloudflare dual-stack
  fronting (INFERENCE; anycast rotation also fits). It is not a new
  target (same page address).
- Disposition: this hit belongs to a sibling morning-scan batch
  (`swarm-scan/20261026T151547Z`). This fleet did not re-ingest it and
  did not touch its files. An operator export sweep later committed its
  batch dir in commit `0c1ef707`. It is left to its owner.

### Rank 3 — The crawl haul itself (74 results, zero hits)

- The 57 `domain:r.jina.ai` results split into 13 scans of the reader
  service itself (bare or two-character paths, empty titles) and 44 scans
  of 29 other page domains (temporary-mail pages, a document-portal page,
  and one-off streaming, news, finance, and community pages).
- The 17 `page.title:"amap"` results are name collisions: 13 cloud
  hostnames, 2 marketing-academics association pages, and 2 French
  food-association pages.
- Triage verdict (linguist agrees, adversarial reviewer agrees): all 74
  are routine noise for fleet purposes (INFERENCE, not OBSERVED:
  metadata alone cannot exclude subrequest use). No result was wrongly
  dismissed on the metadata available.
- Two downgrades apply to the noise description (adversarial review):
  the "documented collisions" label is overstated for the 2 French AMAP
  pages, because that class is absent from
  `scripts/scanners/FALSE-POSITIVES-urlscan.md`; and the `domain:`
  match mechanism is unsupported by bytes, because the 44 non-reader
  results contain zero "jina" strings, so the match field lies outside
  captured metadata. A fleet page that calls the reader as a subrequest
  cannot be excluded from metadata alone.

## Behavior and TTP notes

No behavior in this haul indicates agent activity. Three weak patterns were
noted and none was promoted (all INFERENCE at most):

1. Repeat `/ec` scans cluster near the same time of day: 7 of 10 fall
   between 13:46 and 13:55 UTC, across 8 of 14 days, with 3 scans far
   off that window. This is a cluster, not a near-daily pattern. A
   schedule alone does not prove an agent. No target ever appears.
2. Short re-scan bursts on single suspicious pages (4 temporary-mail scans
   in about 10 minutes on 2026-10-24; 5 document-portal scans on
   2026-10-21) match normal security re-scanning shape, not fleet
   coordination.
3. No cross-page pattern links the reader scans to the map-title scans,
   or any one page to another.

Identifier findings (cryptologist, OBSERVED):

- 57 jina-domain results carry 57 distinct scan UUIDs, 30 page domains,
  28 real network address values plus 1 blank, and 7 real network
  owners plus 1 blank. Cross-query UUID overlap is zero. Real
  cross-query network address overlap is zero (one apparent share was
  a blank-value artifact; blank values must be excluded before any
  shared-infrastructure claim).
- Shared addresses inside the jina haul trace to shared hosting and
  Cloudflare, not coordination.
- Only one URL parameter name exists in the whole 74-result haul
  (`client`, on one host). Zero percent-encoding appears in any page
  address. Zero base64-looking path segments appear.
- Zero matches exist for `getPoiInfo`, `uqscan=`, `uqframe=`,
  `hysandbox`, `amap-pc-ssr`, `/ssr/place`, and `zz=` across all 74
  results. One `zz` substring sits inside a hostname label with no
  equals sign. It is not a parameter key.

Detection note for future runs (cryptologist, INFERENCE): the `domain:`
query is weak. Only 13 of 57 jina results have the reader as page
domain, and all 13 reader addresses are bare or two-character paths
with no proxied target after the host. Future marker checks should
require a target after the reader host, and must exclude blank
network-address values before claiming shared infrastructure.

## Novelty verdicts

- Crawl haul: no new fleet finding. Marker zero in metadata stands
  (adversarial reviewer verified by independent grep over all raw files).
- Rank 1 hit: new as a corpus record (ingested now), not new to the
  operator (already surfaced Oct 25), and not evidence of a new behavior.
- Rank 2 hit: not new to this fleet (sibling batch, already committed
  by the operator sweep).
- The relay service (`r.jina.ai`) is already known from other lanes.
  Generic relay overlap was noted, not re-submitted.

Novelty checks run for the ingested hit: Factum fuzzy match per candidate
key (scan UUID, result address, page address, query tag, network address
text); legacy evidence corpus context (relay uses in other lanes noted);
Transluce tracker (see THIRD-PARTY-REPORTS.md); `lists/` inventory
context. A failed check would have blocked a confident novelty claim.
No check failed for the narrow claim above (this scan record is new).

## Ingest

- Lane: `urlscan` (new plain-slug lane dir `data/lanes/urlscan/`, with
  `raw/` verbatim copies and `PROVENANCE.md`). All 126 lane files
  validated before any Factum command. Zero malformed. Zero symlinks
  under `data/`.
- Batch: `data/records/a3fc917d22794d0eb9dbea8ba6b1d405/`
  (manifest + records.jsonl, 3 records, all `tags.lane=urlscan`):
  1 source (`source_abe3ff985a814f02a778a5d928e18c82`), 1 observation
  (`web.capture`, `observation_25601d338e044477885afcb719831d00`),
  1 observable (`url`, `observable_9b3a23a0de7a4f9b8035be1dabc4d308`).
- New idempotency key: `urlscan-crawl-2026-10-26/oct25-morning-hit`.
  The original morning key was not reused.
- Export then verify: `verify --blobs` returned `ok:true`,
  `verified:true`, `pending:0`. The 1,737 missing artifacts in that
  output are corpus-wide pre-existing local-only bytes. None belongs
  to this batch (it has no files). Post-ingest URL match finds both
  new records indexed, lane `urlscan`.
- Nothing from the Oct 26 crawl was ingested (zero new hits).
- The batch dir was already tracked in git via commit `0c1ef707`
  (operator export sweep). It needs no commit from this fleet.

## Exclusions and sampling limits

Excluded queries (not run), with reasons:

| Query | Reason |
|---|---|
| domain:amap.com | Task-forbidden; adversarially disabled 2026-10-14 (~809 benign scans/30d vs 0 true positives) |
| domain:gaode.com | Task-forbidden; adversarially disabled 2026-10-14 (same class) |
| domain:jqp.vercel.app | Task-forbidden opt-in relay query; counsel judge 2026-10-20 (per-query review hold) |
| domain:vanderbi.lt | Task-forbidden opt-in relay query; same counsel hold |
| domain:ntfy.envs.net | Task-forbidden opt-in relay query; same counsel hold |
| domain:itty.bitty.site | Task-forbidden opt-in relay query; same counsel hold |
| domain:cors.bwa.workers.dev | Task-forbidden opt-in relay query; same counsel hold |
| domain:pingllo.com | Task-forbidden opt-in relay query; same counsel hold |

Sampling limits (adversarial reviewer verified):

- Anonymous search window: last 30 days only. Scans in the haul run
  2026-09-26 to 2026-10-26. A zero means none in the last 30 days of
  urlscan, not "never".
- Metadata only: full result bodies need login, which was not used.
  Verdicts rest on search metadata (address, title, scan date,
  network address).
- One page per query (size=100). Both non-zero queries returned fewer
  than 100 results, so no second page was needed.
- No HTTP failures, no timeouts, no 429. No 429 hard stop triggered.
- One understatement (adversarial review): urlscan's search-index
  coverage for query-string tokens (`uqscan=`, `uqframe=`) is
  unverified, so those zeros are weaker than stated.
- Handling note: `page.title:"amap"` is marked `enabled:false` in the
  config, but the task order listed it as a proven grammar query, so
  it was run this once as an extra. The config flag was not changed.
  Coverage discloses the one-off run.

## Third-party reports

Full detail sits in THIRD-PARTY-REPORTS.md. In short: 2 reports were
accepted as bearing on the hunted markers or the relay, and none bears
on the two `/ec` morning scans themselves, and none uses urlscan.io as
a source for agent-infrastructure observation.

1. Swarmchasers, "We found a Tencent agent fleet" (UPSTREAM):
   corroborates the hunted markers and Jina Reader as the fleet's only
   successful relay. It does not corroborate the urlscan zero, the
   `/ec` scans, or any ongoing fleet activity (last seen Oct 8).
2. Transluce tracker entry 153 (SECONDARY): corroborates `uqscan` tag
   values in Amap scanner traffic only, with its own warning that the
   value is freely chosen and not conclusive.

Transluce entry 178 was first accepted as the weakest accept, then
KILLED on final adversarial review and moved to the rejected list: it
fails the same bar that rejected entries 38 and 115 (no fleet link,
no fleet marker, no `/ec`, no urlscan, authorship unproven), and it
adds nothing beyond the Swarmchasers report.

17 candidate groups were rejected with reasons in
THIRD-PARTY-REPORTS.md. Nothing found changes the crawl verdict.

## Open items

1. **IPv6 observable gap — OPEN.** The installed `factum-web` pack
   allows only `url`, `domain`, `hostname`, `ipv4`, `email` as
   observable types. `factum-core` has no IP type. No corpus precedent
   exists for an IPv6 observable. The typed IPv6 observable for the
   Rank 1 hit was therefore omitted from the batch. The value itself
   is preserved in files only, NOT as a typed observable. It stays
   verbatim in the observation tags (`tags.ip` and `tags.ip_*`), in
   the `ipv6_gap` tag on the observation, in the lane raw copies,
   and in the ingest note. What a future query would find: a file
   read of the batch or lane raw copies WOULD find it; a typed IPv6
   observable query, an IP-observable match, or observable
   edge-building WOULD NOT find it. Corpus text findability after
   ingest is UNPROVEN (pre-ingest fuzzy search found only number
   fragments; only a URL match was re-run). Fix path: add an `ipv6`
   observable type through the approved schema-pack workflow, then
   submit the omitted observable in a new bundle. Do not edit a
   locked pack in place. Do not hand-edit Factum JSONL or SQLite.
2. **Corpus count drift — RESOLVE BEFORE PUSH (push block).** Start
   status showed 208,343 records; end verify showed 208,342. This
   fleet's batch adds 3 records and the sibling batch adds 4 (both
   confirmed in commit `0c1ef707`), so the same-basis expectation is
   +7, while the observed move is −1: an unexplained gap of 8, not 1,
   unless the counting bases differ, which this report does not
   establish. Do not push this fleet's commit until the gap is
   explained or the counting bases are stated. This fleet's own 3
   records are file-verified and index-verified, so the gap lies
   elsewhere on the shared branch.
3. **French AMAP class missing from the false-positives doc.** The 2
   French food-association pages in the title-amap haul are a collision
   class absent from `scripts/scanners/FALSE-POSITIVES-urlscan.md`.
   Add the class to the doc (TIER-A style doc fix, needs no new lane).
4. **`domain:` match field unexplained.** The 44 non-reader results in
   the jina haul contain zero "jina" strings, so the field urlscan
   matched on lies outside captured metadata. Full bodies (login
   needed) would be required to check for subrequest use.
5. **Submitter of the `/ec` scans unknown.** Anonymous urlscan
   metadata carries no submitter field. The timing note is only that
   7 of 10 `/ec` scans cluster between 13:46 and 13:55 UTC across 8
   of 14 days. That cluster is noted, not attributed.
6. **Sibling batch ownership.** The Oct 26 sibling batch
   (`7d0c5086bec14a8c90d68896a8b28032`) was committed by the operator
   sweep in `0c1ef707`. It is left to its owner. This fleet claims no
   credit for it.

## Evidence and artifacts in this directory

- `coverage.md` — crawl coverage table, exclusions, limits.
- `crawl-progress.log` — per-query status lines.
- `hits-draft.json` — empty list (0 triage-passing crawl hits).
- `hits.json` — machine-readable hit list for this report (Rank 1
  ingested, Rank 2 sibling-owned, crawl haul zero).
- `linguist-review.md`, `cryptologist-review.md`,
  `adversarial-review-crawl.md`, `adversarial-review-final.md`,
  `third-party-reports-draft.md`, `ingest-note.md` — lane outputs.
- `THIRD-PARTY-REPORTS.md` — final third-party section.
- `VERIFICATION.md` — verifier re-fetch results and final
  adversarial review of this report.
- `MANIFEST.md` and `SHA256SUMS` — artifact inventory and hashes.
- `raw/<query-label>/search.json` + `.PROVENANCE.txt` + `.sha256` —
  verbatim urlscan responses per query. `raw/screenshots/` is empty
  (no triage-passing hits).
- `crawl.py`, `triage.py` — executor working scripts (not deliverables).

## Sensitivity note

Raw files are preserved verbatim and never redacted, per the standing
rule. No token value is reproduced in this report. Captured page
addresses were checked for token-like capability values: no
triage-passing hit exists, so no token-bearing hit is carried forward
in prose. Treat the raw files as the verbatim evidence store and keep
any token-bearing content local-only.
