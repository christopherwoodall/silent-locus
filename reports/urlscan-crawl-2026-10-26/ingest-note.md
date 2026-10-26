# Ingest note — urlscan crawl 2026-10-26, Oct 25 morning-scan hit

## Terms

- **Factum**: the structured evidence store in `data/`.
- **Lane**: a work group in Factum. Records in one lane share a tag.
- **Batch**: one exported set of Factum records, in `data/records/<id>/`.
- **Observable**: a single value in Factum, such as a URL or an IP address.
- **IPv6**: the long form of a network (IP) address. IPv4 is the short form.
- **SECONDARY**: evidence from a third-party source, not first-hand capture.
- **OBSERVED**: a claim based on direct observation of the source data.

## Job

- Ingest only the Oct 25 morning-scan bundle
  (`bundle-20261025T145711Z.json`).
- The 2026-10-26 crawl gave zero new hits. Nothing from it was ingested.
- No commit. No push. The coordinator commits at the end.
- The Oct 26 sibling batch (result `01a1787e`) was not touched and its
  hit was not re-ingested. See the sibling note below.

## Factum status (start of work)

- Command: `status`.
- Result: `ok: true`, initialized, version `0.2.0`.
- Records: 208,343. Lanes: 126. Pending batches: 1. Stale: false.
- Searched commit: `36334b3eb15c8255c960d7b391f47a98f73989e7`.

## Lane validation (before any Factum CLI use)

- All 126 `data/lanes/*/lane.json` files parse as JSON.
- Malformed lane IDs: 0. Every ID matches `lane_[0-9a-f]{32}`.
- Symlinks under `data/`: 0.
- No existing `data/lanes/urlscan` dir was found. A plain-slug lane dir
  was created: `data/lanes/urlscan/`, with `raw/` and `PROVENANCE.md`.
- Lane tag on every submitted record: `urlscan`.

## Schema check for the IP observable (the known defect)

- Command: `schema assigned observable ipv6`.
- Result: `{"ok": false, "error": {"code": "SCHEMA", "message":
  "Unknown observable type: ipv6"}}`.
- This repeats the morning-scan failure exactly.
- Installed `factum-web` pack (1.0.0) lists only these observable types:
  `url`, `domain`, `hostname`, `ipv4`, `email`.
- Installed `factum-core` pack lists no IP type. Its generic types
  (`term`, `text`) do not describe a network address, so they were not
  used for this IP. A wrong type would hide the gap.
- Corpus precedent: none. A fuzzy text search for the full IP value
  found only short number fragments (`636`, `700`, `463`, `470`), not
  an IPv6 record.
- No locked schema pack was edited. No Factum JSONL or SQLite file was
  hand-edited.

## IPv6 gap status: OPEN

- Gap: the typed IPv6 observable for `2606:4700:20::ac43:4636`
  (Cloudflare, AS13335, tier 2, label CLOUD_SERVICE) is missing from
  the corpus. No `ipv6` observable type exists in the installed packs.
- The IP value is NOT lost. It stays verbatim in:
  - the observation tags (`tags.ip`, `tags.ip_asn`, `tags.ip_org`,
    `tags.ip_country`, `tags.ip_city`, `tags.ip_tier`, `tags.ip_label`);
  - the tag `ipv6_gap` on the observation, which states the omission;
  - the raw copies in `data/lanes/urlscan/raw/`;
  - this note and the lane `PROVENANCE.md`.
- Fix path: add an `ipv6` observable type through the approved schema
  pack workflow. Then submit the omitted observable in a new bundle.
  Do not edit a locked pack in place.
- This gap is raised as an open item for the coordinator.

## What was submitted (encoding used)

- Input bundle: `data/lanes/urlscan/bundle-20261025T145711Z-ingest.json`.
- New idempotency key: `urlscan-crawl-2026-10-26/oct25-morning-hit`.
  The original key `swarm-scan/20261025T145711Z` was not reused.
- Actor kept from the original bundle: `agent:swarm-scan-orchestrator`.
- Change from the original bundle, and only change:
  - record `ip-0` (type `ipv6`) removed;
  - one tag added to observation `obs-0`: `ipv6_gap`.
  - All bodies are otherwise verbatim. Nothing was redacted.
- Add result: `ok: true`, durability `pending`.
- Batch ID: `a3fc917d22794d0eb9dbea8ba6b1d405`.
- Exact-value dedup at add: `url-0` was `not_found`.

## Record counts by kind (submitted batch)

- Source: 1 — `source_abe3ff985a814f02a778a5d928e18c82`.
- Observation (`web.capture`): 1 —
  `observation_25601d338e044477885afcb719831d00`.
- Observable (`url`): 1 —
  `observable_9b3a23a0de7a4f9b8035be1dabc4d308`.
- Total: 3 records. Observable `ipv6`: 0 (see gap above).
- Grades: scan facts are OBSERVED. urlscan metadata is SECONDARY by
  default. The IP tier and label come from the scanner, so they are
  SECONDARY. The hit grade is LOW, SECONDARY, as set by the fleet.

## Pre-ingest dedup results

- Scan UUID `01a17355-8853-7179-8623-5d2a48a3e0b5`: no corpus record.
  One fuzzy hit only, an unrelated board post (substring artifact).
- urlscan result URL
  `https://urlscan.io/result/01a17355-8853-7179-8623-5d2a48a3e0b5/`:
  `not_found` before ingest. After ingest, a URL match finds 2
  records: the new `url` observable and the new `web.capture`
  observation, both lane `urlscan`.
- Page `https://r.jina.ai/ec`: no corpus record. Fuzzy search for
  `r.jina.ai/ec` gave 25 hits, all generic `r.jina.ai` relay uses from
  other lanes (for example `2026-10-01-intermediary-relays`). None
  holds this page or this scan. The relay service is known; this hit
  is new.
- Query tag `relay-jina-reader`: no exact corpus record. Fuzzy search
  gave 20 hits, all generic jina-reader mentions. None is this hit.
- IP text search: see the schema check above. No IPv6 precedent.
- Conclusion: the specific hit is new. It was submitted. Generic
  `r.jina.ai` overlap was noted, not submitted again.

## Batch dir and export

- Batch dir: `data/records/a3fc917d22794d0eb9dbea8ba6b1d405/`.
- Contents: `manifest.json`, `records.jsonl` (3 records, verified
  from the files: all records carry `tags.lane` = `urlscan`; the
  observation carries the full IPv6 value in `tags.ip`).
- Export timing: this worker waited until after 17:37 UTC before it
  ran export, because the sibling batch was inside its 2-hour export
  window until 17:37:01 UTC (pending since 15:37:01 UTC).
- A separate export at 17:34 UTC had already written both pending
  batch dirs and committed them in commit `0c1ef707` (“Export pending
  urlscan batches (operator override of 2h rule)”). That sweep was
  not this worker's action.
- This worker's export (17:38 UTC) returned `ok: true`,
  `exported: []`, `pending: 0`. Nothing new was exported by it.
  The batch dir above was already in place and already tracked in
  git at that point.
- No file of the sibling worker was changed by this worker.

## Verify --blobs result

- Command: `verify --blobs`.
- Result: `ok: true`, `verified: true`, `pending: 0`.
- Corpus records at verify: 208,342.
- Artifacts: 1,737 missing corpus-wide, 730 hashes verified. The
  missing artifacts are pre-existing local-only bytes from other
  lanes. None of the 3 records in this batch appears in the missing
  list. This batch has no files (`files: []`), so it needs no blobs.
- Note on counts: start status showed 208,343 records; end verify
  showed 208,342. The 1-record difference is not explained by this
  batch (its 3 records are file-verified in the exported batch and
  found by index search). The coordinator may wish to check what
  else changed on the shared branch during this run.

## Sibling batch note (not touched)

- Sibling batch: `swarm-scan/20261026T151547Z`, result `01a1787e`,
  pending batch `7d0c5086bec14a8c90d68896a8b28032`.
- This worker did not export it early, did not re-ingest its hit,
  and did not change its files.
- Its batch dir `data/records/7d0c5086bec14a8c90d68896a8b28032/` was
  committed in commit `0c1ef707` by the operator export sweep, not
  by this worker. It is left to its owner.

## Left uncommitted for the coordinator

- `data/lanes/urlscan/` (new lane dir: `PROVENANCE.md`,
  `bundle-20261025T145711Z-ingest.json`, `raw/` copies).
- This note: `reports/urlscan-crawl-2026-10-26/ingest-note.md`.
- The batch dir `data/records/a3fc917d22794d0eb9dbea8ba6b1d405/` is
  already tracked in git (commit `0c1ef707`). It needs no commit
  from this worker.
- No push was made by this worker.

## Failures

- None in this ingest, except the pre-existing `ipv6` schema gap
  above, which is OPEN.
- One killed process, mine only: an early `schema assigned`
  follow-up query ran over 10 minutes at high CPU on the large
  corpus. It was stopped. The same facts were then proven from the
  installed pack files and from the `ipv6` error itself. No sibling
  process was touched.
