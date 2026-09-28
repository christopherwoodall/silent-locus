# Gem dashboards — build log (2026-09-27)

Two Kibana dashboards backed **only** by `rubygems-goimport-campaign`.
Separate from every urlquery dashboard. No urlquery index, pattern, or saved
object was touched.

## Index state at build time

- Index: `rubygems-goimport-campaign`
- Doc count at build: **3,564** (2026-09-27 23:06 UTC; bulk ingest finished)
- Index pattern: `rubygems-goimport-campaign*`
  (`d7b5794b-0269-40cc-a465-6a3f506fa1ad`, time field `@timestamp`)
- Campaign-window harvest docs (May 11–13): 614; total harvest docs: 616;
  unique harvest gems: 560 (canonical Diffend analysis said 555/608 — the
  dashboard shows what the index actually contains)
- Hit fingerprints present: `council-domain` (629), `go-import` (476),
  `go-import-repo` (474), `go-import-vcs` (474), `r-jina-proxy` (269),
  `probe-name` (6), `zz-token` (1)

## Dashboards

1. **Gem Burst — Overview**
   `https://agent-apocalypse-f1f7ba.kb.us-east-1.aws.elastic.cloud/app/dashboards#/view/df101171-88af-4e73-a258-171d02361af3`
   (saved-object id `df101171-88af-4e73-a258-171d02361af3`, logical `gem-dash-overview`)
2. **Gem Payloads — Mechanism**
   `https://agent-apocalypse-f1f7ba.kb.us-east-1.aws.elastic.cloud/app/dashboards#/view/70ff5e82-37ac-4b29-96f8-bfd71d6cd58d`
   (saved-object id `70ff5e82-37ac-4b29-96f8-bfd71d6cd58d`, logical `gem-dash-payloads`)

## Panel validations (every query ran against ES and returned data before save)

### Dashboard 1 — Gem Burst — Overview (7 panels)

| Panel | Type | Query (KQL unless noted) | Validation result |
|---|---|---|---|
| Publications per hour — May 11–12 | histogram (date_histogram 1h) | `record_kind: "diffend_harvest"` + `@timestamp` in [2026-05-11, 2026-05-13) | 10 hourly buckets; peak bucket `2026-05-12T02:00:00.000Z` |
| Unique gems | metric (cardinality `gem`) | `record_kind: "diffend_harvest"` | buckets returned |
| Version pins | metric (count) | `record_kind: "diffend_harvest"` | buckets returned |
| Peak-hour publications | metric (count) | `record_kind: "diffend_harvest"` + `@timestamp` in [2026-05-12T02:00, 2026-05-12T03:00) — hour resolved from the validated histogram, not string surgery | 295 pubs in peak hour (index holds slightly more than the canonical 271) |
| Verified uploaders | metric (cardinality `gem`) | `record_kind: "diffend_harvest"` AND the 3 exact pairs: `londonyardtestabc-0.0.2`, `southfetchprobe42-0.0.3`, `southlondonfetchroot-0.1.0` | **3** uploader gems present |
| Gem families by name pattern | horizontal_bar (filters agg) | `record_kind: "diffend_harvest"`; filters: `gem: lamb*`, `gem: south*`, `gem: wand*`, `gem: oai*`, `gem: chatoaifetch*`, `gem: *zz*`, `gem: *hack*`, `gem: (*fossil* or *bzr* or *hg* or *svn*)` | docs: lambeth=77, south*=53, wandsworth=31, oai*=73, chatoaifetch=14, zz=158, hack=45, vcs-labelled=88 — all > 0. Families overlap by design (one gem may match several); the KQL in the panel mirrors the validated ES wildcard filters exactly |
| go-import VCS values | pie (donut) | `record_kind: "hit"` + `fingerprint: "go-import-vcs"`; terms on `matched_string` | hg=276, fossil=72, mod=49, git=37, bzr=22, svn=18 |

### Dashboard 2 — Gem Payloads — Mechanism (5 panels)

| Panel | Type | Query | Validation result |
|---|---|---|---|
| Target domains | horizontal_bar (terms on `matched_string`, 15) | `record_kind: "hit"` + `fingerprint: "council-domain"` | 15 domains returned |
| Proxy laundering of go-import URLs | pie (donut, filters agg) | `record_kind: "hit"` + `fingerprint: "go-import"`; filters: `matched_string: "*r.jina.ai*"` / `"*s.jina.ai*"` / `not "*jina.ai*"` | r.jina.ai=266, s.jina.ai=15, direct=195 |
| go-import tag presence among campaign pins | **Vega donut** (Pattern B: custom `body.query`, no top-level `%context%`/`%timefield%`/`%timefilter%`; static campaign-window scope) | Embedded ES query: `record_kind: "diffend_harvest"` + May 11–13 range; aggs `present` = `terms(gem, [431 validated go-import gem names])`, `absent` = `must_not terms(...)` | present=445 pins, absent=169 pins (614 in window). Spec parses under Vega 5 and was rendered headlessly to SVG against the real ES response. The 431-name list is a build-time snapshot, documented here |
| Notable gems — uploaders & log carriers | table (terms `gem` → terms `version`) | `gem: ("londonyardtestabc" or "southfetchprobe42" or "southlondonfetchroot" or "southnewsprobe1778550995")` | 4 gems; nested rows include all 5 required versions: `londonyardtestabc-0.0.2`, `southfetchprobe42-0.0.3`, `southlondonfetchroot-0.1.0`, `southfetchprobe42-0.0.2`, `southnewsprobe1778550995-0.0.3` (plus their 0.0.1 rows, which are real campaign data) |
| Dead-drop beacon strings | markdown | **none — static evidence panel** (see below) | n/a |

### Static (non-query) panel

- **Dead-drop beacon strings** (markdown, Dashboard 2): static evidence panel, no ES
  query. Records the uploader dead-drop strings: `"builder alive\nstatus=<code>\n"`
  (`southfetchprobe42-0.0.3` `lib/out.rb`, baked into 0.0.4's README),
  `"builder alive but fetch fail <err>"`, `#exfil 2026-05-12 04:17:55 +0200` /
  `YARD RAN` (`southnewsprobe1778550995-0.0.3` build log = 02:17:55 UTC, inside
  the peak hour), `# get any modern gov page to prove` (`southfetchprobe42-0.0.3`).

## Dropped / failed panels

**None.** Every requested panel validated and was saved. Corrections applied
during the build (per the pre-build review):

- Overview stat tile is **Verified uploaders** (3 exact gem-version pairs), not IOC hits.
- "Top packages" was replaced by the **gem-family bar chart** (8 name-pattern
  families, each count validated; overlap disclosed).
- "go-import tags by package" was replaced by **tag presence** (Vega donut,
  present vs absent pins — the join KQL cannot express).
- Notable-gems table uses nested `gem` → `version` buckets so both
  `southfetchprobe42` versions appear as rows.
- No fingerprints were assumed: all fingerprint-gated panels derive from the
  live `fingerprint` terms agg.

## Stack quirks found during the build

- On this Elastic Cloud Serverless stack, `PUT /api/saved_objects/{type}/{id}`
  returns **404 for new objects** ("Saved object [type/id] not found") — PUT only
  updates. Creation must use **POST** (idempotent via find-by-title + reuse).
- Classic `filters`-agg ES responses return buckets as a **dict**, not a list —
  validation code must normalize.
- The Vega presence spec follows Pattern B (custom `body.query`, absolute time
  range, no dashboard placeholders) — the only placeholder-safe pattern for a
  static-scope panel.

## Verification status

- API/ES/query validation: **complete** — every panel's backing query was run
  against the live index and returned data before the visualization was saved;
  both dashboards' `panelsJSON` + references were re-read and every panel
  resolves to its saved visualization with the expected query.
- **Pixel health in the real Kibana UI is NOT yet confirmed** — API/headless
  checks are necessary but not sufficient. Needs visible inspection via browser
  delegation before the dashboards are declared healthy.

## Builder

`/tmp/build_gem_dashboards.py` (ephemeral; raw build log at
`/tmp/gem-dashboards-build.log`). Re-running is idempotent: existing saved
objects are found by title and reused.
