# Provenance — DemoWiki corpus

## Source
- **Wiki:** DemoWiki, `https://prowiki.org/demo/wiki.cgi` (OddMuse-style install,
  German UI; operator: HelmutLeitner)
- **Identified in:** thecolony.ai lane (notes/thecolony-ai-ingest-2026-09-27.md),
  via the swarm catalogue — "a SIXTH wiki (prowiki.org/demo/wiki.cgi, epoch
  nonces 1781634491/1781641854, Jun 16+22)"
- **Retrieved:** 2026-09-28, read-only crawl (`scripts/crawl_demowiki.py`),
  ~2s pacing, no writes, no accounts

## What was captured
- `recentchanges_days3650.html` — full 10-year RecentChanges (`days=3650`);
  the wiki's entire edit history is **9 edits** (2021-10-30 → 2026-09-10)
- `pageindex_spx.html` — full page index
- `recentchanges_rss.html` — RSS feed of recent changes
- `page_<id>.html` × 7 — current HTML of every edited page:
  StartSeite, WikiSandbox, Context, RecentChanges, PublicBoard,
  XAgentApiTestUnique, AgentResearchDataUsaLink1781634491
- `diff_<page>_rev<N>.html` — per-revision diff views for all 9 RC entries
  (note: this OddMuse install rejects `action=history`; revision content comes
  from the `action=browse&diff=N` views linked in RecentChanges)
- `demowiki_crawl.json` — parsed RC entries, page bodies, diff texts, file list

## Swarm edits (June 2026)
| Date | Page | Author | Summary |
|---|---|---|---|
| 2026-06-22 10:43 | XAgentApiTestUnique | AgentNameX | [test] |
| 2026-06-16 22:30 | RecentChanges | OpenAIDataBridge | [API bridge 1781641854] |
| 2026-06-16 20:28 | AgentResearchDataUsaLink1781634491 | AgentResearchTest | [test] |

Plus later swarm-adjacent edits:
- 2026-09-04 18:40 WikiSandbox `[collusion.wiki test marker]` by CollusionWikiTest
- 2026-09-06 22:36 PublicBoard `[PublicBoard relay]` by IP `159.146.96.208`
  (IP shown as-is; /16 truncation is the publisher convention for collusion.wiki,
  not for this live-site crawl — no operator identity is pursued or recorded)

## Epoch nonces
- `1781634491` — embedded in page name `AgentResearchDataUsaLink1781634491`
  (≈ 2026-06-16 20:28 UTC, matching the RC timestamp)
- `1781641854` — in revision summary `[API bridge 1781641854]`
  (≈ 2026-06-16 22:30 UTC, matching the RC timestamp)

## Caveats
- Live-site crawl, not a publisher export: no username redaction, no IP
  truncation. Research scope stays on agent handles and infrastructure; the
  single IP editor is recorded only as an edit attribution.
- `action=history` unsupported by this install; revision history is limited to
  the 9 RC-linked diff views.
- WikiSandbox was deleted on 2026-09-10 by the operator; captured content is
  the placeholder text surviving in the delete diff.

## Closure 2026-09-28 (workstream C)

Naturally small: full read-only crawl of a 9-edit wiki (2021-10-30 →
2026-09-10 — the wiki's entire edit history). N=23 docs (RC entries, page
bodies, per-revision diffs) is the venue exhaustively captured by construction;
there is no more history to pull. ES `demowiki` _count=23 verified,
schema-drift clean.

## Schema normalization 2026-09-29 (W2)

Built `events.jsonl` (16 rows) from `raw/demowiki_crawl.json` on the canonical
record schema (`scripts/validate_schema.py`: 16/16 clean).
- 9 × `wiki_revision` — one per RecentChanges entry, merged with its
  `action=browse&diff` text; `@timestamp` parsed from German `rc_day` +
  `time_str` (e.g. "22. Juni 2026" + "20:28" → 2026-06-16T20:28:00Z);
  identity `demowiki|rev|<page_id>|<iso_timestamp>` (timestamp disambiguates the
  two WikiSandbox rev4 entries). Swarm-agent authors flagged in
  `labels.wiki.swarm_agent`; epoch nonces extracted to
  `labels.wiki.epoch_nonce` when present.
- 7 × `wiki_page_snapshot` (new kind) — current page bodies at crawl time;
  identity `demowiki|page|<page_id>`; `@timestamp` = crawl time
  2026-09-28T03:19:41Z.
Fingerprint = sha256 hex of the documented identity string (verified against
the 2023-11-14-hfspace-proxies reference implementation before writing).
SHA256SUMS regenerated (events.jsonl + all raw contents); `sha256sum -c` OK.

## Rollup review 2026-09-29 (W8)

rollup: none — 9 RC revisions + 7 page snapshots are already atomic; the wiki's
entire edit history is 9 edits, so a per-day/per-actor rollup would duplicate
the event rows 1:1.

## Build-script relocation 2026-09-29 (ingest-script condensation)

- Moved `scripts/es_ingest_demowiki.py` into this collection dir per Christopher's build-script convention (single-collection build scripts live in the event directory).
- Path fixes in the moved script: `WIKI` is now the script's own dir (self-locating); `REPO_ROOT` resolves three levels up for the mapping path.
- BUG FIX: `build()` read `{WIKI}/demowiki_crawl.json` but the crawl file lives at `raw/demowiki_crawl.json` (the docstring already said `raw/`) — the old path never existed, so `--load` was broken; fixed to the `raw/` path.
- Verified offline (2026-09-29): `build()` assembles 23 docs from disk (7 wiki_page, 9 wiki_revision, 3 wiki_link, 4 wiki_bridge) with no network/ES access.
- ES ingest driver: `push_to_local_es.py --all` runs the path in `scripts/local_es_manifest.json` `via_script` for index `2021-10-30-demowiki`; manifest entry updated to the new script location.

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_demowiki.py` at `raw/scripts/legacy/es_ingest_demowiki.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.

## Factum ingest 2026-10-10 (lane worker, Phase 3)

Ingested into Factum on branch factum-shaping. Batch 64ff2106b5734e5c8d7a02a834fabb99.
Lane ID lane_41b7df31a501419aab563d29e31230f5. Tag {"lane":"2021-10-30-demowiki"} on every record.

Records:
- source_5a734488f6d24f94a5f13e837ddea15f — DemoWiki source
- observation_2c1b99f0edeb4de29e07d6e4f18c676a — dataset.snapshot of the 2026-09-28 crawl
- observation_b957530399794c309d3cded0a1073615 — web.capture: full-history RecentChanges
- observation_fd4b75ecf98649c6a4436334d74120e8, observation_ed6b53eed4bb48d6b8bcf0d24f33a1cf, observation_9b8245ee28d84915aa882ed88d796db9, observation_fcccbc8cca9d474b8952e2e56876595e, observation_0279c147c18c48ddba8d7ed3e0dfa3f9 — web.capture of the 5 swarm-relevant revision diffs
- 10 infra.ioc observations: epoch nonces 1781634491, 1781641854; handles AgentNameX, OpenAIDataBridge, AgentResearchTest, CollusionWikiTest; ip 159.146.96.208; domain prowiki.org; page names XAgentApiTestUnique, AgentResearchDataUsaLink1781634491
- 10 artifact records (git storage): events.jsonl, demowiki_crawl.json, RecentChanges HTML, 5 diff views, 2 agent-page bodies

Note: legacy paths above (evidence/2021-10-30-demowiki/) are the pre-ingest locations. Working copies now live at data/lanes/2021-10-30-demowiki/; the renamed legacy dir evidence/remove-2021-10-30-demowiki/ keeps the originals.
