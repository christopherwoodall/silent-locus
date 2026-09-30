# HUNT LANE 13 — PyPI BigQuery historical metadata

**Date:** 2026-09-27
**Verdict: clean negative.** No GemStuffer footprint on PyPI anywhere in the May 5 – Jul 10, 2026 window.

## 1. BigQuery: dead end (auth required)

- No `bq` CLI and no `google-cloud-bigquery` lib in this environment.
- Direct REST probe: `GET https://bigquery.googleapis.com/bigquery/v2/projects/the-psf/datasets` → **HTTP 401** (`"Login Required"`, OAuth 2 access token expected).
- Per the lane brief, stopped here rather than working around auth. No accounts were created.

## 2. Fallback: PyPI XML-RPC changelog (no-auth historical record)

PyPI's public XML-RPC API exposes the complete upload/remove/yank event history — the closest no-auth substitute for BigQuery's historical metadata. Notes on method:

- The legacy `changelog` method is deprecated; `changelog_since_serial` is the working replacement.
- The server truncates each `changelog_since_serial` response to ~47k events (~1.5–2 days), so the window was walked with a serial cursor: each call's max serial seeds the next.
- Rate: ~1 request per 30s, read-only, no logins.
- Name set: 186 campaign names from `data/gem-iocs-2026-09-27.jsonl`, later expanded to **3,026 names** using the JFrog inventory (`data/gemstuffer-jfrog-2026-09-27.csv`; 185 overlap, 2,840 new).
- Patterns hunted alongside exact names: epoch-suffixed names (`\d{9,}$`), `try[a-z][0-9]zz` grammar, `zz*`/`oai*` prefixes, probe/proxy/fetch/yard/jina/oast/webhook keywords.

### Phase 1 — May 5 → Jun 18, 186 names + patterns (~1.35M events)

- **0 exact campaign-name hits.**
- **0 `tryzz`-grammar hits.**
- Name-pattern hits were all benign on inspection: `oai-statsig-python-core` (legitimate OpenAI package), `package{digits}` placeholders, student coursework packages, `zzupy`/`zzshare` (legitimate).
- 2 pattern-matching removals, both benign: a `zzzz…` junk package removed as spam, and one `zzupy` version yanked.
- (One parser bug found and corrected mid-run: XML-RPC `create`/`add Owner` rows use `<nil/>` for version, which initially produced cross-row phantom matches; triage used a strict `[^<>]*` parse. Exact-name results were never affected.)

### Phase 2 — Jun 19 → Jul 10, 3,026 JFrog names (~615k events)

- **0 exact hits. 0 tryzz-grammar hits.** Covers the July 7 wave window.

### Phase 3 — May 5 → Jun 18, 3,026 JFrog names (1,417,861 events)

- Re-walk of the full campaign window against the complete JFrog inventory, exact-name only.
- **0 hits across 1,417,861 events.** Match file: `data/lane13/changelog_mayjun_expanded_matches.jsonl` (empty); name list: `data/lane13/campaign_names_expanded.json`.

## 3. Bandersnatch mirrors: assessed, no value

Bandersnatch-style mirrors replicate PyPI's *current* state only; they expose no historical/deleted-package data. Nothing to gain beyond lane 5's living-API check (20 names → all 404).

## Caveats

- The changelog records **names, versions, timestamps, and actions only** — not descriptions. Beacon strings (`"builder alive"`, `"YARD RAN"`) and `<meta name="go-import">` markers inside the *descriptions* of deleted packages remain uncheckable without BigQuery auth. The substitutable checks (exact names, name grammars, removal events) are complete.
- A VM restart mid-task wiped `/tmp` intermediates from phases 1–2; headline findings were triaged before the restart and are reported above. Phase 3 artifacts survive under `data/lane13/`.
- A PyPI name matching a campaign name would only prove a name collision, not campaign activity — moot here, since there were zero matches.

## Bottom line

Three independent passes over PyPI's complete May 5 – Jul 10, 2026 event history (~3.4M events total) against 3,026 known GemStuffer package names plus the campaign's name grammars: **zero hits**. Combined with lane 5's living-API sweep, the campaign's footprint remains RubyGems-only. The operator class did not mirror names, beacons, or the go-import technique onto PyPI — not even briefly.
