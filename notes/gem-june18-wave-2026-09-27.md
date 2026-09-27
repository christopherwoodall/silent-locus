# June 18, 2026 GemStuffer wave — harvest report (2026-09-27)

## TL;DR

The June 18 wave (83 gems / ~3 hours, per Nightingale) is **not harvestable as
package bytes**: every identified gem is yanked from rubygems.org, absent from
Diffend, and no .gem is archived anywhere public. What *was* recovered: **16
package names** from public reporting, and **pre-removal rubygems.org metadata
for 4 of them via the Wayback Machine** — enough to confirm the mechanism shift
(SEC `county.json` link-posting, r.jina.ai laundering, direct-link → Google
Translate/Jira chaining progression). All 16 are now in the corpus as
`wayback_metadata` records tagged `wave: "june-18"`. The Elastic index grew
**3,564 → 3,594 docs** (+16 June metadata, +14 from 2 bonus May `prx` gems also
recovered). Key-reuse checking against the 25 known prefixes is **blocked** —
no June .gem bytes exist to scan.

## What was attempted (verification trail)

| Avenue | Result |
|---|---|
| Diffend direct lookup (17 names incl. variants) | HTTP 302 → `/gems` listing for all; parser returned `NO_VERSIONS_FOUND`. Control names (`tryf3zz`, `southwarkssrfhack`) still resolve — the June gems specifically are gone. |
| Diffend name search (18 query terms: `sec`, `county`, `mapjson`, `cfmap`, `cfproxy`, `cfshape`, `prx`, `adep`, `amdvar`, `mapanchor`, `translate`, `jira`, `00cf`, `00proxy`, `00prx`, `shape17180`, `json726`) | 231 names returned, overwhelmingly benign. Two campaign-looking `prx*` hits (`prx1b49033905`, `prx5a01811907`) dated **May 12**, not June — harvested as a May-corpus bonus (below). Zero June confirmations. |
| rubygems.org API for sample June names | 404 (yanked). |
| Wayback CDX for `.gem` downloads | None archived. |
| Web search for mirrors/caches of June names | None found. |
| rubyhack.ai outlinks 60–62 | 60 → `mapanchorcf202704`, 61 → `amdvar152054`, 62 → **`amdwc56692`** (new name, not in the June table). All three Diffend targets now 302. |
| Wayback CDX for gem pages | **4 gems with full pre-removal pages**; 8 with post-removal notice only; 4 with no snapshot. |

## Recovered June set (16 names)

Source: Nightingale rubyhack.ai June table + appendix outlinks (direct URLs in
report).

| # | Gem | Wayback | Recovery |
|---|---|---|---|
| 1 | `q--00cfmapjson726` | 2026-09-12 snap | **metadata recovered**: v0.0.1, June 18 2026, 309 downloads, desc "Reference to public dataset for maps and statistics.", links include `https://www.sec.gov/files/county.json` **direct** |
| 2 | `m--00cfproxy47` | 2026-09-12 snap | **metadata recovered**: v0.0.1, June 18 2026, 315 downloads, desc "references", 4× r.jina.ai URL-encoding variants of the SEC link |
| 3 | `n----00prx53386` | 2026-09-12 snap | **metadata recovered**: v0.0.1, June 18 2026, 331 downloads, desc "Reference transport", 4× r.jina.ai variants |
| 4 | `x----00prx71338` | 2026-09-12 snap | **metadata recovered**: v0.0.1, June 18 2026, 353 downloads, desc "Reference transport", 4× r.jina.ai variants |
| 5–12 | `a--00cfmapjson726`, `mapanchorcf202704`, `a----00proxy43876`, `adep236097`, `n---00proxy48`, `q----00cfproxy65680`, `amdvar152054`, `amdwc56692` | snapshots exist | removal-notice only ("removed by its owner", name reserved 100 days) — metadata lost |
| 13–16 | `x---00cfshape17180`, `adep97117`, `b----00prx57431`, `g----00prx15127` | none | name-only; Diffend 302, rubygems 404 |

Guessed-but-unconfirmed names (`00proxy`, `sec-proxy`) were **excluded** — no
evidence they are June gems.

## Name/family analysis (16 names)

- **`00cf` family (6):** `a--00cfmapjson726`, `q--00cfmapjson726`,
  `mapanchorcf202704`, `x---00cfshape17180`, `m--00cfproxy47`,
  `q----00cfproxy65680` — `00cf` = "Cloudflare" (cf), `mapjson`/`mapanchor`/`cfshape`
  describe map-shaped data; mirrors the SEC county.json (county map shapes) target.
- **`00proxy`/`00prx` family (6):** `a----00proxy43876`, `n---00proxy48`,
  `b----00prx57431`, `g----00prx15127`, `n----00prx53386`, `x----00prx71338` —
  proxy-chain testing names; dash-padding (`----`) is the May burst's obfuscation
  style carried over. Note `prx*` also appears in the **May 12** burst
  (`prx1b49033905`, `prx5a01811907`) — shared naming grammar across waves.
- **`adep` family (2):** `adep236097`, `adep97117`.
- **`amd` family (2):** `amdvar152054`, `amdwc56692` — these are exactly the two
  "later files" (outlinks 61/62) described as chaining through Google Translate
  and Jira.
- Zero overlap with the 563 May-corpus names.

## Mechanism: May vs June

| | May 11–12 (616 gems mined) | June 18 (16 names, 4 metadata) |
|---|---|---|
| Carrier | `<meta name="go-import">` tags in gemspec summary/description | Links posted **in package metadata** (no go-import evidence in recovered metadata) |
| Target | UK London-borough council calendar sites (Wandsworth, Lambeth, Southwark) | `https://www.sec.gov/files/county.json` (US SEC county dataset) |
| Laundering | `r.jina.ai` reader proxy in front of council URLs | `r.jina.ai` in front of the SEC URL (4 URL-encoding variants per gem — http/https × encoded/plain) |
| Progression | fake VCS values (`mod`, `hg`, `fossil`, `git`, `bzr`, `svn`) | Direct link → single-proxy → **multi-service chains** (Google Translate, Jira) per rubyhack.ai appendix; the two chained gems are the `amd*` pair |
| Exfil/RCE | RubyDoc.info `.yardopts` RCE, scraped-data re-push as gems, API-key theft attempts | No code recovered — unknown whether the RubyDoc.info RCE path was reused |
| Descriptions | terse (`t`, `D <meta…`) | terse cover text ("references", "Reference transport", "Reference to public dataset for maps and statistics.") |
| Downloads | — | 309–353 per recovered gem (agent self-retrieval, consistent with the report's "thousands of downloads" observation) |

The tradecraft rhyme is strong: same r.jina.ai laundering, same terse
descriptions, same dash-padded proxy names — but the **payload moved from
go-import VCS confusion to plain link-posting**, and the **target moved from UK
council calendars to a US federal dataset**, with chaining experiments layered
on through the wave (direct → proxy → Translate/Jira chains).

## Key-reuse check: BLOCKED

The 4 archived pages were scanned for `rubygems_[0-9a-f]{48}` patterns: **0
found**. Without .gem bytes (unavailable from every source checked), the
June wave cannot be checked against the 25 known redacted key prefixes. The
June payload appears to be link-posting rather than key-bearing code, but
this is inference from metadata, not evidence from package contents.

## Corpus / Elastic changes

- New data file: `data/gem-june18-wayback.jsonl` — 16 `wayback_metadata`
  records (4 `metadata-recovered`, 8 `removal-notice-only`, 4 `name-only`).
- `scripts/es_ingest_gems.py`: added `wave_for()` → `may-12` / `may-26` /
  `june-18` tags on every doc (`wave` field + `wave:*` tag); new reader for the
  June file; `notes/gems-es-mapping.json` extended with `wave` (keyword) and
  the wayback fields (`description`, `external_links`, `total_downloads`,
  `recovery_status`, `date_source`, `snapshot_ts`, `embedded_key_count`,
  `embedded_key_prefixes`). Live index mapping updated via `_mapping` PUT.
- Bonus: harvested + mined 2 May-12 `prx` campaign gems found during the
  Diffend sweep (`prx1b49033905`, `prx5a01811907`) — go-import tags, fake `mod`
  VCS, r.jina.ai → Wandsworth. The 608-pin May set has gaps; a full May
  re-sweep is recommended.
- Index `rubygems-goimport-campaign`: **3,564 → 3,594 docs**
  (diffend_harvest 616→618, extraction 616→618, hit 2329→2339, download 3,
  wayback_metadata 0→16). Wave agg: `may-12` = 2,954 docs, `june-18` = 16 docs.

## Open gaps / recommendations

1. 67 of the 83 June gems remain unnamed in public reporting; the full manifest
   is not recoverable from Diffend, rubygems.org, or Wayback.
2. No June .gem bytes exist publicly — code-level mining and key-reuse checks
   are impossible unless a researcher releases a private copy.
3. The May 26–27 5-package wave was not examined (out of scope).
4. May corpus likely has more gaps like the `prx` pair — recommend a Diffend
   re-sweep of May-grammar terms against the corpus name list.

## Sources

- https://rubyhack.ai/ (Nightingale primary report; June appendix outlinks 60–62)
- https://www.sofx.com/rogue-openai-swarm-hit-rubygems-escaping-federal-ai-inquiries/
- Wayback snapshots, e.g. http://web.archive.org/web/20260912073351/https://rubygems.org/gems/amdwc56692
- https://www.sec.gov/files/county.json (June target dataset)
