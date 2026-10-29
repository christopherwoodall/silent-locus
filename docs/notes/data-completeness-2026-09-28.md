# Data-completeness audit — 2026-09-28 (post-migration)

Independent verification that the repo migration (2026-09-28) lost nothing, and that the
lane12 BASE-path bug (workers wrote to the old repo 19:08–22:46 UTC, fixed in 42c691f) left
no stranded worker output.

Repos: NEW = `silent-locus` (canonical, remote christopherwoodall/silent-locus);
OLD = `muse-home/projects/swarmtraces-hf-corpus` (untouched archive).

## Verdict: COMPLETE — no gaps

## 1. Old repo is a clean archive

- `git status --short`: clean.
- `git log --oneline -3`: newest is `06a12ce` "Watch 13:56 CDT: pre-migration checkpoint" —
  no commits since the move.
- `hidden_files/lane12/` is git-tracked; working tree matches HEAD (the 22:54 UTC mtimes
  on those files come from the watch worker's git-restore to pristine, content identical).

## 2. Directory inventory

- OLD `data/`: 113 dirs. NEW `data/`: 120 dirs.
- Old-only dirs: **1** — `sec-county-json`, which is **empty** (0 files, untracked placeholder).
  No data.
- New-only dirs: **8**, all post-migration work — `agent-convo-venues`, `agents-relay-sweep`,
  `commonlog-scan`, `gem-temporal-pivot`, `nsi-venue-sweep`, `pastebin-cluster-sweep`,
  `transfer-test-family`, `yourls-resweep-2026-09-28`.
- `notes/`, `scripts/`, `schema/`: every old entry present in new; all additions are
  post-migration files (analyst notes, schema package, backfill scripts).

## 3. File-level comparison (OLD → NEW)

- 2,644 files checked across all OLD `data/` dirs.
- Missing files in NEW: **0**.
- Smaller files in NEW: **1** — `data/collusion-manifest/SHA256SUMS` (893 B → 168 B).
  Explained, not a gap: the OLD manifest was stale — it lists 11 files but only 3 exist on
  disk in the OLD repo. The NEW manifest covers exactly the 3 on-disk files, and their
  hashes match the old copies (`coverage-gaps.csv` 1f9f8086…, `manifest.json` b6d53e16…).

## 4. Bug-window recovery (wb_sweep state)

- OLD `hidden_files/lane12/state_wb.json`: 180 done entries.
- NEW `hidden_files/lane12/state_wb.json`: 300 done entries.
- Set check: OLD ⊆ NEW — **0 of the 180 old entries missing** in the new state. Continuity holds.
- OLD `wb_sweep-v3.log` (38 bytes) contains no HITs and no results — just a Wayback
  cool-down message. The NEW log carries the lane's HIT
  (`rubygems.org/gems/zztargettest18587`). No worker output stranded in the old repo.

## 5. Checksum manifests (NEW repo, spot check)

`sha256sum -c` VERIFIED on all three:
- `data/gem-temporal-pivot/SHA256SUMS`
- `data/paste-archive-gap/SHA256SUMS`
- `data/university-shorteners/SHA256SUMS`

## Caveats

- Comparison is file-count + size + hash-manifest based, not a byte-diff of all 2,644 files;
  the SHA256SUMS manifests (verified on 3 datasets) are the byte-level backstop.
- `sec-county-json` (empty dir) was not carried over — intentional or oversight is unknown,
  but it contained nothing.
