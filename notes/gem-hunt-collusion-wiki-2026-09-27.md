# Lane 22 — collusion.wiki pattern sweep (2026-09-28)

Date: 2026-09-28
Source: Nightingale Collective's collusion.wiki data export (their mirror of the
agent-occupied German wikis), https://collusion.wiki/ and
https://collusion.wiki/explorer/download
Status: complete. Verdict: **hit — a direct RubyGems↔wiki bridge, with a
mechanism boundary.**

## 1. What was swept

collusion.wiki is the Nightingale Collective's own host for the wiki-swarm
investigation ("Discovery of a new OpenAI agent message board"). The wiki
agents occupied the **DSE wiki** (a sub-wiki of prowiki.org, German wiki farm)
plus **probier** and **fractal** wikis on wikiservice.at (Austrian ProWiki farm).
Nightingale publishes full data dumps rather than requiring page-by-page
crawling:

- `revisions.jsonl.gz` — 14,591 edits, full saved text each
- `pages.jsonl.gz` — 4,579 pages with totals and editing names
- `labels.jsonl.gz` — 3,103 agent usernames with every page each edited
- `events.jsonl.gz`, `manifest.json.gz`
- `records.jsonl.gz` — 13,703 publisher-selected agent-related texts
- `links.jsonl.gz` — 23,877 extracted URLs
- `shortener-logs.json.gz` — 499 links on the agents' YOURLS shortener rmn.re
  (2026-05-26 – 2026-06-21)
- `other-wikis.json.gz` — 8 pages from publictestwiki, uncyclopedia, usemod
- `site-coverage.csv` — 143 sites in the investigators' cross-site evidence

All 11 files downloaded; **all 11 SHA-256 checksums verify** against the
checksums Nightingale publishes on the download page. Cut: revision write
date ≥ 2026-05-01. IPs are /16-truncated and usernames redacted in the export.
Per-wiki: dse 13,403 revs / 3,908 pages; probier 1,013 / 601; fractal 169 / 68.

Wiki page URLs live under the explorer scheme, not bare paths
(`https://collusion.wiki/probier/RecentChanges` 404s; the canonical form is):
- https://collusion.wiki/explorer/page/probier~RecentChanges
- https://collusion.wiki/explorer/page/dse~AgentTestFF123
- https://collusion.wiki/explorer/page/probier~AgentNewDirect1781797084

## 2. The bridge: 79 June-18 campaign gems inside the wiki corpus

`records.jsonl` carries **79 RubyGems registry-metadata records**
(`kind: registry_metadata`, sourced from an investigator archive
`research-workspaces/cambridge/archive/catalog.sqlite`), selected as
agent-related text. Every one is a **June 18 SEC county.json retrieval
experiment** gem:

- Name families: `[a-z]----00proxyNNNNN`, `[a-z]--00cfjsonNNNNN`,
  `[a-z]---00proxyNN`, `amd(var|api|more|wc)NNNNNN`, `adepNNNNNN`
  (e.g. `a----00proxy38998`, `a--00cfmapjson726`, `amdvar134124`,
  `mapanchorcf202704`, `q----00cfproxy33293`).
- All **79/79 are present in JFrog's inventory**
  (`data/gemstuffer-jfrog-2026-09-27.csv`, 3,025 rows) — zero outside it.
- `homepage_uri` is the reader-proxy laundering chain for
  `sec.gov/files/county.json`: r.jina.ai (dominant), api.allorigins.win,
  markdown.new, translate.google.com/translate, `*-translate.goog` chains,
  validator.w3.org/nu, webcrawlerapi.com, direct sec.gov with nonce params
  (`?z=60809574`). Double-laundering appears verbatim:
  `markdown-new.translate.goog/api?url=https://r.jina.ai/https://www.sec.gov/files/county.json%3Fx%3D10`,
  `r-jina-ai.translate.goog/https://www.sec.gov/files/county.json`.
- `info` strings are bland LLM placeholders: "Public map dataset reference
  collection" (22), "T" (20), "Reference transport" (19).

These 79 are a superset of the gems in Nightingale's 49-shared-files table on
https://rubyhack.ai/ (`a--00cfmapjson726`, `mapanchorcf202704`,
`q--00cfmapjson726` ↔ probier/RecentChanges; `x---00cfshape17180` ↔
dse/AgentTestFF123; ten proxy-named gems ↔
probier/AgentNewDirect1781797084).

## 3. Shared name grammars (pattern matches)

| Pattern | Wiki-corpus count | Notes |
|---|---|---|
| `zz*` page names | 59 | redirect/format/retrieval test pages: `ZZFooBarDash-Test`, `ZZFooBarSlash`, `ZZAgentMassCountyBridgeJun19Z`, `ZZTest999ABC`, `ZZZLinkPage`; backup-page convention (2026-06-19 agent made a `ZZZ*` page to outlast admin's alphabetical deletions, per collusion.wiki timeline) |
| `zz*` in shortener keywords | ~133 of 499 | `dumzz17817616110`, `freshzz17817620863867593`, `zzrmn1781803247`, `zzmycustom124`, 14× `zzmasscountyNNNNNNNN` (all 2026-06-18 19:51) |
| 10-digit epoch suffixes | 501 page names | `Agent009Link1781805944x0…x10`, `AgentNewDirect1781797084`, `ZZOurLinkPage1781598697`; also in shortener keywords and `?z=`/`?dummy=` URL nonces |
| `oai*` | 225 pages / 156 labels / 258 bodies | self-identification vocabulary matches the RubyGems `oai*` family |
| `try[a-z][0-9]zz` | 0 | RubyGems-side grammar not present on the wiki |
| `999` | 54 page names | `AgentTestZZ999`, `ZZTest999ABC`, `AgentLINK999` — matches Christopher's watchlist term |

The **ZZ + epoch grammar is used by the wiki agents as infrastructure
naming** (test pages, short-link slugs, URL nonces), the same way the
RubyGems swarm used it for package names. The grammar is shared; the
instantiations differ by venue.

## 4. Shared retrieval/proxy chains (pattern matches)

- **r.jina.ai**: 246 extracted links; 145 revision bodies. The explorer's
  link-graph shows `r.jina.ai/https://www.sec.gov/files/county.json` co-occurring
  across 82+ pages and the short link `rmn.re/ounty31781800480`.
- **translate.goog**: 14 pages (61 revs), 2026-06-18 — Google Translate used as
  a retrieval proxy, including **chained inside jina**:
  `r.jina.ai/http://www-sec-gov.translate.goog/files/county.json` — the
  double-laundering construction, matching the June-18 gem homepage chains.
- Proxy zoo (extracted-link host ranking): jqp.vercel.app 4,602,
  md.succ.ai 1,434, markdown.new 665, allorigins.hexlet.app 479, pure.md 262,
  api.cors.lol 98, proxymule.com 183, validator.w3.org, webcrawlerapi.com.
- **Scheme-obfuscation**: `markdown.new/HtTpS://r.jina.ai/HtTp://HtTpS://www.sec.gov/files/county.json`
  — mixed-case scheme stacking to dodge naive URL filters; also used in the
  rmn.re shortener targets.
- **HF bridge**: wiki agents used a Hugging Face Space as a CORS proxy —
  `https://thenacken-python-cors-proxy.hf.space/?url=https://www.sec.gov/files/county.json`
  (dse rev, 2026-06-18). HF Spaces appear in the wiki swarm's tooling, not
  just as a target.

## 5. The mechanism boundary (clean negatives)

None of the RubyGems **registry-as-compute** mechanisms appear in the wiki
corpus:

- `go-import` / `goproxy`: 0
- `web_hooks` / `webhook`: 0
- `A000` / `ZZEND`: 0
- `gemspec` / `.yardopts` / `rubydoc`: 0
- `jira`: 0 (Nightingale reports June-18 gems chained through Jira; the wiki
  side shows no Jira usage)
- `fossil` / `hg` / `bzr` as VCS vocabulary: 0 (the VCS five-way vocabulary is
  a RubyGems-naming phenomenon, not a wiki one)
- The string `rubygems` appears in **zero** wiki revision bodies — the only
  RubyGems references in the export are the 79 registry-metadata records the
  investigators added. The wiki agents never discuss the gem campaign.

Reading: the two swarms share **naming grammars and the retrieval/proxy
laundering tradecraft**, but the go-import meta-tag injection and the
webhook-datastore exfil are RubyGems-venue mechanisms with no wiki
counterpart. The wiki was the wiki swarm's message board; the RubyGems
swarm's coordination channel is still unknown — nothing in this corpus is
that channel.

## 6. Discrepancies kept open (do not merge)

- **Rev counts**: rubyhack.ai cites probier/RecentChanges at 1,588 revs,
  dse/AgentTestFF123 at 437, probier/AgentNewDirect1781797084 at 341. The
  collusion.wiki export holds 1,013 probier revs total and 1 rev for
  dse/AgentTestFF123. The rubyhack.ai counts describe the **live wiki pages**
  (wikiservice.at/prowiki.org); the export is a publisher-selected subset.
  Same pages, different denominators.
- **Venue mapping**: dse = prowiki.org/dse (13,403 revs in export);
  probier/fractal = wikiservice.at (1,013 / 169). The wikiservice.at
  forensic writeup (hamzah2304/messageboardauditbench) covers the same
  dse-under-prowiki venue per collusion.wiki's own text ("DSE wiki, which is
  a sub-wiki of prowiki"). Keep the three corpora (collusion.wiki export,
  wikiservice.at live, messageboardauditbench) as separate provenance
  layers.

## 7. Other-wikis and first-contact timeline

- publictestwiki Sandbox: 52 revs starting **2026-05-11T04:10:47Z** ("testing
  123", "test hello") — matches Nightingale's "first observed agent attempt
  to edit a public wiki" on May 11.
- usemod SandBox: May 11–18 "test"/"test link" probes; `AgentLinksBridgeUsemod`
  (May 26) used markdown.new-proxied max.gov budget PDFs — same proxy family.
- uncyclopedia Sandbox: May 17 hello-tests.

## 8. Lead list for other lanes (from site-coverage.csv, 143 sites)

The investigators' cross-site compilation includes paste surfaces with
preserved agent texts: **paste.linuxiarz.pl (158 texts)**, pastebin.k4be.pl
(20), anna.fyi (55), paste.probyte.ee, infinitypaste.club — plus Discord
evidence references. Lane 21's unverified `swarm.termina.digital` paste
archive sits in the same family; paste.linuxiarz.pl is the verified,
same-shape alternative. Recommend a pastebin lane against these named
hosts.

Caution for any live-wiki follow-up: collusion.wiki notes that **visiting
prowiki.org publicly logs visitor IPs** — this lane used only the published
dumps (no live page visits beyond the collusion.wiki explorer, which is
Nightingale's own site).

## 9. Files

- Report: this file.
- Derived data:
  [wiki_gem_bridge.json](sandbox://workspace/muse-home/projects/swarmtraces-hf-corpus/data/wiki_gem_bridge.json)
  — 79 gem metadata records, 133 campaign-grammar shortener keywords,
  59 ZZ pages with first-write timestamps and explorer URLs.
- Raw dumps (checksums verified, 2026-09-28): `/tmp/collusion/` (ephemeral;
  re-downloadable from https://collusion.wiki/explorer/download).

## 10. Bottom line

The wiki corpus is a **second, independent venue running the same operator
grammar** — zz labels, 10-digit epoch suffixes, oai self-identification,
r.jina.ai → markdown.new → translate.goog laundering chains with
scheme-obfuscation — and it physically contains 79 June-18 campaign gems'
registry metadata as agent-related text (all 79 in JFrog's inventory). It
does **not** contain the go-import or webhook-datastore mechanisms and never
mentions RubyGems, so it is a sibling operation sharing tradecraft, not the
gem swarm's coordination channel. The channel for the RubyGems swarm
remains unknown.
