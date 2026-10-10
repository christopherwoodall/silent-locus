# Provenance — collusion.wiki corpus

## Source
- **Publisher:** Nightingale Collective (https://rubyhack.ai/)
- **Download page:** https://collusion.wiki/explorer/download
- **Retrieved:** 2026-09-28 (re-download; lane 22's 2026-09-27 copies were lost
  with /tmp on a VM rebuild — the files below are bit-identical re-downloads,
  all 11 SHA-256 checksums re-verified against the publisher's published list)

## What the export is
Publisher-selected **"agent-related text"** from five wikis where agent swarms
were active (dse, probier, fractal on wikiservice.at/prowiki.org, plus dorfwiki
and three external wikis). This is **not a full wiki census**:
- IPs are **/16-truncated** (e.g. `172.184`) — host-level attribution is
  impossible by design.
- Usernames are **redacted**; agent identities appear as labels (e.g.
  `DataResearcherAlpha`, `AgentNewDirect1781797084`).
- Deleted pages are unrecoverable; selection basis per record is
  `publisher_selected_plus_task_or_exchange_signal` (see `records.jsonl`).
- Revision write-date cut: `>= 2026-05-01` (per `manifest.json`).

## Keep-all + annotate policy
No records were dropped in this ingest. External overlap is annotated in
document metadata (`tags`, `labels.bridge.*`), never a deletion ground.
Derived annotations added at ingest (name-grammar tags `grammar:zz`,
`grammar:epoch10`, `grammar:oai`, `grammar:999`; proxy-family tags
`proxy:jina`, `proxy:translate`, `proxy:hf-space`, `proxy:other`) are marked
`labels.annotated_by=es_ingest_wiki` and are reversible.

## Files (all SHA-256 verified, 2026-09-28)

```
92b296170b496b836cdf5ef783bed9465d2d75db7e1a0becec1c36c8b7c42cfd  pages.jsonl
60df4a515178230aa952d9f64f6215aea4bd95ab2f05e31e484cf9b887e3f793  revisions.jsonl
588584295f1c4a7c3d90b04075ab151504f165ff069534d935cda08853ec28b1  events.jsonl
d94aecd84baecda46344f5b8726a95a9c81e7e41a1c0969fc89a90c8906f0388  labels.jsonl
b6d53e16b5d9a6a0a98d4577238835ee7a574d7d10a8f1312330b4e626c6ba2b  manifest.json
130d34ef80b591f49d123793d39dcd9d94ee5598b962803ee231047eea22e03a  other-wikis.json
40b49e3e7e223dd349aa8a465aa7dabd9db8515b7f0533f047c8e1087d5ef01d  shortener-logs.json
f41af25fa0b16f88522ba9924f175400eeb9461332568eaca39a34010bb746ed  records.jsonl
9ef4c6771d37e94aa7e8448f8f2ce9fe78915729e2ef70cae6fcfbce58ef44d9  links.jsonl
1091014ca713391dd68d9c658550b2a00e15cee83e53513aa07f9b1862efda01  site-coverage.csv
1f9f80864910d4c49e8ff24a35b1931b87eaeae9d1282c3efa3d6d7b0ee279dd  coverage-gaps.csv
```

(`sha256sum -c SHA256SUMS` passed on all 11 files at ingest time.)

## Derived / bridge files
- `../../wiki_gem_bridge.json` — 79 June-18 campaign gems found as
  `registry_metadata` records inside `records.jsonl` (all 79 present in JFrog's
  inventory; zero outside it). Generated 2026-09-28 by lane 22.
- `../../collusion-manifest/` — earlier copy of SHA256SUMS + manifest +
  coverage-gaps (superseded by this directory; kept for history).

## Scope note
Agents and agent infrastructure only. Per the standing hunt scope, no
operator identity is pursued; the /16 truncation and username redaction in the
source export make that impossible anyway.

## Raw layer 2026-09-29
Moved the five upstream wiki dump captures into `data/2026-05-17-collusion-wiki/raw/`,
keeping their upstream names (raw layer is exempt from the event schema):

- `data/collusion-wiki/pages.jsonl` -> `data/2026-05-17-collusion-wiki/raw/pages.jsonl`
- `data/collusion-wiki/links.jsonl` -> `data/2026-05-17-collusion-wiki/raw/links.jsonl`
- `data/collusion-wiki/records.jsonl` -> `data/2026-05-17-collusion-wiki/raw/records.jsonl`
- `data/collusion-wiki/revisions.jsonl` -> `data/2026-05-17-collusion-wiki/raw/revisions.jsonl`
- `data/2026-05-17-collusion-wiki/labels.jsonl` -> `data/2026-05-17-collusion-wiki/raw/labels.jsonl`

Rationale: these are upstream captures / script-consumed transform inputs
(consumed by `scripts/extract_wiki_proxy_urls.py` and
`scripts/es_ingest_powerbi.py`; `pages.jsonl` and `labels.jsonl` are upstream
captures with no current script consumer). Companion `.jsonl.gz` files were
left in place pending the centralized reference patch.

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_wiki.py` at `raw/scripts/legacy/es_ingest_wiki.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.

## Factum aggregation ingest (2026-10-10)

Per operator approval of aggregation (no 1:1 ingest of the 19,913 wiki
events), the lane was aggregated into Factum as lane `collusion-wiki`.

Method:
1. Read docs/taxonomy (TTP taxonomy + behavior categories) before shaping
   records.
2. Computed full aggregates from
   `evidence/2026-05-17-collusion-wiki/events.jsonl` (19,913 rows, sha256
   136efac16eb4a40f6d87395bc261af7b5cfefa3ec5dfcf8ea6ab28a53cdfec62,
   verified against SHA256SUMS above):
   - event_type distribution (probe / save / delete / revert)
   - request_action distribution (only the 5,322 probe + delete events
     carry request_action; save events carry none)
   - param_family distribution (only the 101 probe events carry
     param_family)
   - success_observed true / false / absent counts (absent = save events)
   - unique ip16 count (50 non-null; 14,591 save events carry no ip16)
   - temporal range from labels.time; time_grade distribution
   - actor_label and relation_type distributions
3. Pre-ingest dedup: searched committed Factum batches for
   "collusion-wiki", the XSS payload term, and "OpenAIResearchHelper".
   No existing aggregate of this events.jsonl. Matches found are
   incidental cross-references in other lanes only; the 5,217 delete
   events were previously aggregated as a dataset.snapshot in lane
   `2026-06-04-admin-deletions` (annotated as overlap in the source
   record). The XSS payload term had no prior infra.ioc.
4. Submitted one bundle: 1 source record (lane locator + raw/ contents
   note + overlap annotation), 1 dataset.snapshot observation (row
   count, sha256 revision), 10 OBSERVED-grade aggregate claims, and 1
   infra.ioc for the single XSS probe payload
   (`<script>alert('XSS')</script>`, 2026-06-29, attacklog_raw_dse_2606,
   ip16 52.159). No 20k event ingest.
5. Exported, verified (verify --blobs), committed explicit pathspecs,
   pushed.
6. Retained bytes copied to `data/lanes/collusion-wiki/` (PROVENANCE.md,
   SHA256SUMS, events.jsonl, raw/). Legacy directory renamed to
   `evidence/remove-2026-05-17-collusion-wiki/`.

Aggregation script: deterministic re-derivation from events.jsonl; every
count above was recomputed from the raw rows, not carried from
summaries.
