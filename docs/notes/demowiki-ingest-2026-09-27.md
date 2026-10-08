# Lane K — DemoWiki ingest (2026-09-28)

**Source:** `https://prowiki.org/demo/wiki.cgi` — a live OddMuse-style demo wiki
(German UI; operator HelmutLeitner), identified in the thecolony.ai lane's swarm
catalogue as the **sixth swarm wiki** (epoch nonces 1781634491/1781641854,
handles AgentResearchTest / OpenAIDataBridge / AgentNameX, activity June 16+).

## What was captured

Read-only crawl (`scripts/crawl_demowiki.py`, ~2s pacing, no writes, no
accounts): full 10-year RecentChanges (`days=3650`), page index, RSS feed,
current HTML of all 7 edited pages, and per-revision diff views for all 9 RC
entries. The install rejects `action=history`; revision content comes from the
`action=browse&diff=N` views linked in RecentChanges (`diff=N` = last N changes
of the page, not revision N — each RC entry still gets its own doc).

The wiki's entire history is **9 edits** (2021-10-30 → 2026-09-10):

| Date | Page | Author | Summary |
|---|---|---|---|
| 2026-09-10 | WikiSandbox | HelmutLeitner | [Seite gelöscht.] (operator delete) |
| 2026-09-10 | Context | HelmutLeitner | — |
| 2026-09-10 | RecentChanges | HelmutLeitner | — |
| 2026-09-06 | PublicBoard | 159.146.96.208 | [PublicBoard relay] |
| 2026-09-04 | WikiSandbox | CollusionWikiTest | [collusion.wiki test marker] |
| 2026-06-22 | XAgentApiTestUnique | AgentNameX | [test] |
| 2026-06-16 | RecentChanges | OpenAIDataBridge | [API bridge 1781641854] |
| 2026-06-16 | AgentResearchDataUsaLink1781634491 | AgentResearchTest | [test] |
| 2021-10-30 | StartSeite | KerstinMüller | (original demo content) |

## Content findings

- **AgentResearchDataUsaLink1781634491** (AgentResearchTest, [test]): a
  datausa.io tesseract API URL —
  `api.datausa.io/tesseract/data.jsonrecords?cube=pums_5&drilldowns=State,Year&include=Industry Sector:61-62;Workforce Status:true&locale=en&measures=Total Population`
- **XAgentApiTestUnique** (AgentNameX, [test]): "ASCII test link"
  `https://api.datausa.io/tesseract/cubes/acs_ygpsar_poverty_by_gender_age_race_5`
- **PublicBoard** (IP editor, [PublicBoard relay]): *"PublicBoard relay
  (https://public-board.com) -- an anonymous message board for AI agents:
  plain-text HTTP reads, MCP at /mcp, no account (see /llms.txt for the daily
  key). Cross-run memory, open questions, hello-test first contact."* —
  a direct DemoWiki↔public-board.com bridge, written 2026-09-06.
- **Epoch nonces confirmed against RC timestamps:**
  `1781634491` → 2026-06-16T18:28:11Z (page edited 20:28 local render);
  `1781641854` → 2026-06-16T20:30:54Z (revision summary, edited 22:30).

## Pattern sweep (standard battery)

Zero campaign tradecraft in all bodies/diffs: no `zz`, no `oai`, no proxy
wrappers (jqp/jina/md.succ.ai/allorigins/markdown.new/da.gd/is.gd/rmn.re),
no go-import, no webhooks, no A000/ZZEND chunk markers. External URLs are
exactly three: two api.datausa.io task-target URLs and public-board.com.

## Cross-corpus handles (vs collusion.wiki `labels.jsonl`)

- **AgentResearchTest** → dse wiki, 3 revisions, first 2026-06-16T18:35:52Z
  (same day as the DemoWiki edit, ~2h earlier)
- **OpenAIDataBridge** → dse + probier, 22 revisions, first 2026-06-16T09:42:32Z
- **AgentResearchTestName** → dse, 1 revision, 2026-06-17T03:05:17Z
- **AgentNameX** → NOT in the collusion.wiki corpus — DemoWiki-unique so far
- **CollusionWikiTest** (Sept-04 `[collusion.wiki test marker]`) also not in
  the corpus labels

## Dataset

`data/demowiki/` — `demowiki_crawl.json` (parsed RC/page/diff records),
`raw/` (26 HTML captures), `sweep.json`, `PROVENANCE.md`. 23 Elastic docs in
own index **`demowiki`**: 7 wiki_page, 9 wiki_revision, 3 wiki_link, 4
wiki_bridge. Shared canonical mapping (`notes/gems-es-mapping.json`), verified
`event.dataset.keyword` aggregation. Script: `scripts/es_ingest_demowiki.py`.

## Interpretation

DemoWiki reads as a **probe site**: the swarm handles touched it on June 16/22
with test-scaffold edits (epoch-nonce page name, "API bridge" summary, ASCII
test links against datausa.io), then left. The Sept edits are different
actors: an investigator running a collusion.wiki test marker, and someone
wiring the wiki into the public-board.com agent-board ecosystem. Minimal
footprint, maximum linkage — it ties the June-16 eval wave, the datausa task
family, and the agent-board layer into one surface.
