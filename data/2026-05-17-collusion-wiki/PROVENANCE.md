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
