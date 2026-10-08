# Ingest Lane I — RubyGems `fieldnotes` v0.1.3 micro-dataset

Date: 2026-09-28. Read-only GETs only; the gem itself was **never downloaded or installed**.

## What it is

The `fieldnotes` gem on RubyGems is the **official client package of public-board.com** — the plain-text AI-agent message board discovered in lane H (`notes/public-board-ingest-2026-09-27.md`). The board's llms.txt lists it alongside npm / PyPI / crates.io clients. It is a registry artifact tying the agent-board ecosystem to RubyGems — and, critically, a **control sample**: a legit agent-ecosystem gem to hold next to the malicious May-12 go-import campaign gems.

## Registry facts (metadata only)

- 4 versions: 0.1.0 (2026-09-05T21:14:04Z), 0.1.1 → 0.1.2 → 0.1.3 (all 2026-09-20, within ~4h — a burst-publish day: 16:33 → 18:46 → 20:17 UTC).
- Author string: `field-notes` (org/team handle, not a natural person — no person-focused attribution collected).
- Homepage https://public-board.com; MIT license; **zero dependencies** (runtime and dev); **empty gem `metadata: {}`**.
- Description: "Read and write cross-run notes on https://public-board.com (plain-text board for AI agents). See https://public-board.com/llms.txt for the protocol."
- **Live, not yanked** (`yanked: false`) — unlike every gem in the May-12 go-import campaign.
- Downloads: 2772 total — 1629 on 0.1.0 (the agent-board population pulled it hard right after the Sept 5 release), 451 / 347 / 345 on 0.1.2 / 0.1.3 / 0.1.1.
- Checksums: compact-index `/info/` checksums match the API `sha` for all four versions (0.1.3 → `1e3d0e2f684ff68452fb0888e35afbc05ce90094a37273148e83e1d40d99b87c`). Diffend's diff timestamps agree with `created_at` to within ~6 min (Diffend ingest lag).

## Cross-source verification

- Diffend (single gentle GET, http 200, no connection-close): versions page shows diff pairs 0.1.0→0.1.1 / 0.1.1→0.1.2 / 0.1.2→0.1.3 plus cross-pairs and the standalone 0.1.0 card; **no security/malware flags** on the page. Diff-detail pages (which embed full file contents) were deliberately NOT fetched — metadata lane only.
- rubygems.org compact index (new-style format: `version |checksum:<sha256>,ruby:>= 3.0,created_at:<ts>`), API v1 versions + gem detail — all 200s.

## Campaign-grammar sweep

Swept all four captures (zz / oai / tryzz / go-import / web_hooks / A000 / ZZEND / jina.ai / md.succ.ai / rmn.re): **0 hits**. The empty `metadata: {}` is itself a contrast point — the campaign gems' payloads lived in summary/description meta tags. This gem's registry record is clean of the campaign grammar.

## What this buys the hunt

1. **Negative control for the registry lane.** The May-12 campaign was found via Diffend's yanked-gem corpus; `fieldnotes` shows what a legit, live, agent-ecosystem gem looks like in the same registry at the same time — empty metadata, no dependencies, burst-publish release cadence (which is NOT a campaign signal on its own).
2. **Ecosystem mapping.** public-board.com's agents are real consumers of registry infrastructure (1629 downloads of 0.1.0). Any future RubyGems lane (e.g. the July-7 Diffend sweep, the 2,463 JFrog-only names) can be cross-checked against this population's tooling.

## Elastic

Own index **`fieldnotes-gem`**, 7 docs, 0 bulk errors, verified. Canonical shared mapping; `event.dataset=fieldnotes-gem`; `event.dataset.keyword` multi-field present at creation. Doc kinds: gem_metadata (1), version (4), diffend_page (1), grammar_sweep (1). Script: `scripts/es_ingest_fieldnotes_gem.py`.

## Files

- `data/fieldnotes-gem/` — diffend-page.html, compact-index-info.txt, rubygems-versions.json, rubygems-gem.json, grammar-sweep.json, checksums.txt, manifest.json, PROVENANCE.md, progress.log
- `notes/fieldnotes-gem-2026-09-27.md` (this file)
- `scripts/es_ingest_fieldnotes_gem.py`

## Open

- Diffend diff-detail pages (0.1.0→0.1.1 etc.) remain unfetched by design — they embed file contents and the lane scope is metadata-only. If a future lane wants file-level diffs of a *legit* gem as a control against campaign diffs, that's the next step.
- The 1629 downloads of 0.1.0 are consistent with board-agent adoption but not decomposed by downloader (no per-IP data in public registry metadata — same dead end as the urlquery submitter-IP finding; not pursued).

## DEFENSIVE TAKEAWAY

- **Detection surfaces exposed:** name-grammar patterns (zz/oai/epoch/try-zz) as cheap pre-filters over large corpora.
- **Early-warning signals:** this lane's 0-hit result is itself signal — it calibrates the false-positive rate of grammar-only detection and shows where grammar alone is insufficient.
- **What a defender could instrument:** run grammar regex as first-pass triage before expensive analysis; pair every grammar hit with a second independent signal (mechanism marker, temporal burst) before escalating.
