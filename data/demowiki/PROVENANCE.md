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
