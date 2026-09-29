# PROVENANCE — fieldnotes gem micro-dataset

## Source
- **Gem:** `fieldnotes` on RubyGems — the official client gem of public-board.com, the plain-text AI-agent message board ("field notes"). Discovered via the public-board lane (read: `notes/public-board-ingest-2026-09-27.md`): the board's llms.txt lists RubyGems `fieldnotes` v0.1.3 (2026-09-20) as its official registry package, alongside npm / PyPI / crates.io clients.
- **Retrieval:** 2026-09-28 ~03:22–03:25 UTC (2026-09-27 22:22–22:25 CDT). Read-only GETs only. **The gem itself was NEVER downloaded or installed** — only registry metadata and the Diffend versions page were fetched.
- **Authorship note (scope rule):** the registry lists the gem author as `field-notes` — an org/team string, not a natural person. No operator identity, registrant details, or person-focused attribution was collected.

## URLs fetched (all read-only GET)
1. `https://my.diffend.io/gems/fieldnotes` → `diffend-page.html` (7846 bytes, http 200, 6.3s; no connection-close this time, single gentle request — Diffend hostility not triggered)
2. `https://index.rubygems.org/info/fieldnotes` → `compact-index-info.txt` (504 bytes, http 200; new-style compact-index format: `version |checksum:<sha256>,ruby:>= 3.0,created_at:<ts>`)
3. `https://rubygems.org/api/v1/versions/fieldnotes.json` → `rubygems-versions.json` (2690 bytes, http 200)
4. `https://rubygems.org/api/v1/gems/fieldnotes.json` → `rubygems-gem.json` (939 bytes, http 200)

## SHA-256 (local captures; see checksums.txt)
- diffend-page.html: e413488ae5c8f006220087e37a056ea634261ab3306d1e6538a37bbe91f799b3
- compact-index-info.txt: 334f1277caaeeec5949bab040b5a6eeef7f835d16404ecf062ed5cdc0606a781
- rubygems-versions.json: c37bade46b972ba75c2ef508facd7a9671788f5130b58187b6cf096bcaa06f82
- rubygems-gem.json: 3fa414ac867a937afa5779bb20bde1e2955a27571090a492cdae4b031009d8b8

## Cross-source consistency (verified from tool output)
- Compact-index checksums match API `sha` for all four versions (e.g. 0.1.3 → `1e3d0e2f684ff68452fb0888e35afbc05ce90094a37273148e83e1d40d99b87c` in both sources).
- Diffend diff timestamps (0.1.0 → Sep 05 2026 21:20; 0.1.0→0.1.1 Sep 20 16:34; 0.1.1→0.1.2 Sep 20 18:47; 0.1.2→0.1.3 Sep 20 20:18) agree with API `created_at` to within ~6 min (Diffend's ingest lag).
- Gem is **live on RubyGems** (`yanked: false`) — unlike every gem in the May-12 go-import campaign, which was yanked.

## Key registry facts (metadata only)
- name `fieldnotes`, latest 0.1.3 (2026-09-20T20:17:20.814Z); versions 0.1.0 (2026-09-05) → 0.1.1 → 0.1.2 → 0.1.3 (all Sept 20, within ~4h — a burst-publish day).
- authors: `field-notes`; homepage: https://public-board.com; license: MIT.
- description: "Read and write cross-run notes on https://public-board.com (plain-text board for AI agents). See https://public-board.com/llms.txt for the protocol."
- dependencies: **none** (empty runtime + development); `metadata: {}` (empty — no go-import meta tags, no VCS-injection fields).
- downloads: 2772 total — 1629 on 0.1.0, 451 on 0.1.2, 347 on 0.1.3, 345 on 0.1.1. The 0.1.0 count shows the agent-board population pulled the gem heavily right after its Sept 5 release.

## Campaign-grammar sweep (grammar-sweep.json)
- Swept all four captures for zz/oai/tryzz/go-import/web_hooks/A000/ZZEND/jina.ai/md.succ.ai/rmn.re patterns: **0 hits**. Registry metadata is clean of the campaign grammar.
- Diffend shows no security/malware flags on the gem's versions page; Diffend's diff pairs (0.1.0→0.1.1, 0.1.1→0.1.2, 0.1.2→0.1.3 plus cross-pairs) exist but per lane scope the diff-detail pages (which embed file contents) were NOT fetched — read-only metadata lane only.

## Scope compliance
- Agents/infrastructure only. No human/operator identity pursued; no credentials reproduced; no gem artifact downloaded/installed.
- The gem is a legit operator package (public-board.com's official client), NOT part of the May-12 go-import campaign and NOT in the RubyGems campaign corpus — kept as its own micro-dataset and own ES index, matching the provenance-correction rule for the Diffend gem corpus.

## Closure 2026-09-28 (workstream D)

Naturally small: metadata-only micro-dataset for a single RubyGems package
(`fieldnotes`, 4 versions). N=7 docs (4 version + gem_metadata + diffend_page
+ grammar_sweep) is the complete public registry surface of one gem — bounded
by the package's own version list. ES `fieldnotes-gem` _count=7 verified.
No campaign grammar in any capture; gem is the legit public-board.com client,
not campaign infra. Kept as its own dataset per the RubyGems provenance rule.

## Schema build 2026-09-29 (worker W5)

- events.jsonl: **7 records** (record_kind `venue_finding`), one per raw
  capture file (diffend-page.html, compact-index-info.txt,
  rubygems-versions.json, rubygems-gem.json, grammar-sweep.json,
  checksums.txt, manifest.json). Complete public registry surface of the
  single `fieldnotes` gem — no more records to make.
- fingerprint identity string: `fieldnotes-gem|file|<filename>`.
- `@timestamp`: 2026-09-05T00:00:00Z (dir date prefix; gem v0.1.0 released
  2026-09-05) for all rows, `timestamp_source = "dir_prefix"`;
  `retrieved_at` 2026-09-28T03:25:00Z (capture window 03:22–03:25 UTC).
  Per-file registry facts live in `labels.gem.*` / `labels.file.*` /
  `labels.diffend.*` / `labels.sweep.*`; per-file sha256+size at top level.
  Key facts: 4 versions (0.1.0 Sep 05; 0.1.1–0.1.3 burst-published Sep 20
  within ~4h); `yanked: false`; 2772 downloads; authors `field-notes`
  (org/team string, scope-compliant); zero campaign-grammar hits in
  grammar-sweep.json.
- SHA256SUMS regenerated: covers events.jsonl + all 7 raw files. The
  previous SHA256SUMS listed `raw/progress.log`, which does not exist —
  stale entry dropped.
- Verified: all 7 records validate; fingerprint + file sha256 recomputed by
  hand for rubygems-gem.json (matches the checksums.txt entry).

## Rollup decision 2026-09-29 (worker W5)

- No rollup.jsonl: 7 per-file capture records with no natural aggregate
  layer (no bursts, windows, or groupings in the data). Per Christopher's
  worker rule, no rollup was built.
