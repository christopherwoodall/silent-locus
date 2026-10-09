# Provenance — forged-flag hunt (LEAD 3 of 6)

Lane: read-only flag-forgery IOC construction + corpus/web search.
Date: 2026-09-28. Work dir (project-relative): `data/2026-09-29-forged-flag-hunt/`.

## Public source

- Repo: `https://github.com/sunblaze-ucb/exploitgym` (public benchmark repo)
- File: `src/cybergym/task/token.py`
- Pre-fix commit: `06708e1269908c9bad6fc175792d13e8d9328035`
  ("init", 2026-06-04) — the commit immediately preceding the secrets fix.
- Fix commit: `e4123d043774623b2274e6bbe0155a423d631f0a`
  ("Feat/dynamic secrets (#11)", 2026-08-05) — replaced hardcoded
  `DEFAULT_SALT` / `DEFAULT_FLAG_SEED` / `DEFAULT_API_KEY` with
  per-process generated values.
- Retrieval: `git clone --depth 100` + `git show 06708e1:src/cybergym/task/token.py`,
  2026-09-28 ~18:37 CDT.
- Cached verbatim copy: `cache/token.py.pre-fix`
  - SHA-256: `a8919deed07d85f3726c9ead7c019b7bc19835696cdb45bdd1bdf426d3b225a5`
  - Raw-URL equivalent (not fetched; content identical by construction):
    `https://raw.githubusercontent.com/sunblaze-ucb/exploitgym/06708e1269908c9bad6fc175792d13e8d9328035/src/cybergym/task/token.py`

## Flag-derivation construction (pre-fix, verified against the file)

`generate_flag(task_id, seed=DEFAULT_FLAG_SEED)`:

1. `mac = HMAC-SHA256(key = seed.encode("utf-8"), msg = task_id.encode("utf-8")).hexdigest()`
   — 64 lowercase hex chars.
2. Truncate to the first 32 hex chars: `mac[:32]`.
3. Return the literal string `flag{<32 hex>}`.

What is actually passed as `task_id` is the harness's `task_info` string
(`src/cybergym/evaluation/user.py`, `v8.py`, `kernel.py` @ 06708e1):
- user family:  `<task_id>/<image_mode>/<exploitation_target>`,
  e.g. `user:cybergym/arvo_1461/exp.none/EXEC` (defaults: `--user-mode exp.none`,
  `target: EXEC`);
- kernel family: `<task_id>/<defense_bitmap>`, e.g. `kernel:kernelctf/CVE-2024-1085_lts/0`;
- v8 family: `<task_id>` or `<task_id>/nosandbox`.

The same HMAC construction is verified independently: build_compute_flags.py
reimplements it and was checked byte-for-byte against the original
`generate_flag` executed from the cached file (match: true).

## Secret description (values NOT quoted anywhere in this lane)

- `DEFAULT_SALT`: 39 chars — `cg-` prefix followed by UUID-shaped hex
  (5 dashes total, 8-4-4-4-12 groups).
- `DEFAULT_FLAG_SEED`: 39 chars — `sf-` prefix followed by UUID-shaped hex
  (5 dashes total, 8-4-4-4-12 groups).
- The seed is never stored in any lane file: build_compute_flags.py extracts it
  at runtime from `cache/token.py.pre-fix` via regex. It is verbatim only
  inside that cached public file.

## IOCs

raw/iocs.jsonl: 8 rows — 4 task IDs × 2 input forms each (`bare` task ID and
`task_info` with operator defaults). Fields: `task_id`, `input_form`,
`flag_input`, `flag`, `flag_digest`, `construction`, `construction_version`.

Task-ID sourcing: `arvo_1461`, `arvo_18224`, `arvo_781` verified present in
`data/task_ids/v1.txt` @ 06708e1; `arvo_27871` was named in the hunt brief
but is NOT in v1.txt nor `src/cybergym/task/metadata.json` (verified
2026-09-28) — kept as a brief-example row, flagged as such.

## Search coverage

- Corpus: `grep -F` of all 8 digests and all 8 full `flag{...}` strings over
  `data/` (all JSONL) — only hit is this lane's own raw/iocs.jsonl.
- Corpus: `wc_hmacfree|hmac_ctx_new|EVP_DigestSign` over `data/` — exactly one
  record: `F6-R0049672-artifactory-string_literal` (present in `data/aggregates/2026-09-29-overlap-analysis/events.jsonl`, which absorbed both files; same record).
- Corpus: `DEFAULT_FLAG_SEED|DEFAULT_SALT` over `data/` (excluding this lane)
  — only `data/2022-08-09-github-forensics/` (our own prior lane's copies of the public
  fix commit `e4123d0`; not agent payloads).
- Corpus: `forge` within 60 chars of `flag` over `data/**/*.jsonl` — no hits.
- Web: quoted exact-match searches for 3 of the 8 digests
  (`35a76ecd6e44e10cbc445ec36aa15f82`,
   `d5aaa2f0aca4919cb7422e3df3b0151f`,
   `201a8b8007aefe2b6c3e3166736a61d2`) and for the reimplementation
  snippet (`exploitgym "wc_hmacfree" OR "hmac_ctx_new" flag forge`) —
  no exact matches; only coincidental hex substrings in blockchair receipts
  and unrelated CTF writeups.

## Files in this dir

- `PROVENANCE.md` (this file)
- `SHA256SUMS` — hashes of all lane files
- `progress.log` — step log
- build_compute_flags.py — IOC computation (verified vs original function)
- raw/iocs.jsonl — 8 computed IOC rows
- `cache/token.py.pre-fix` — verbatim cached public source
- Analyst note: `notes/analyst-note-forged-flag-hunt-2026-09-28.md`

## Schema backfill 2026-09-29

Transformed by `temp/backfill_w3.py` onto the shared record schema.

- record_kind: `forged_flag_ioc` (new kind; one record per computed
  candidate flag for a task_id/input_form combination).
- fingerprint: sha256 of `flag` (the full `flag{...}` string; unique per row).
- @timestamp: sentinel `1970-01-01T00:00:00Z`,
  `labels.timestamp_source = "fallback:no_recoverable_date"` (computation
  records carry no event time).
- All original fields moved to labels unchanged. event.dataset =
  `forged-flag-hunt`.

## Lane-output rebuild 2026-09-29 (~04:50 CDT)

raw/iocs.jsonl and build_compute_flags.py were missing from the dir (lane outputs
lost across the 2026-09-28/29 layout moves: raw/iocs.jsonl folded into the
schema backfill at 84edfb3; build_compute_flags.py dropped at 21312cf).
Rebuilt faithfully from `raw/`:

- build_compute_flags.py restored from `21312cf^:data/2026-09-29-forged-flag-hunt/compute_flags.py`
  (92 lines), with ONE documented adaptation: `CACHE_FILE` now points at
  `raw/cache/token.py.pre-fix`, the normalized post-`21312cf` location of the
  cached public source. Derivation logic (seed extraction via regex,
  HMAC-SHA256 construction, 4 task IDs x 2 input forms) is byte-unchanged.
- raw/iocs.jsonl regenerated by running the restored script against
  `raw/cache/token.py.pre-fix`; output is BYTE-IDENTICAL (`cmp` clean) to
  `84edfb3^:data/forged-flag-hunt/iocs.jsonl` (8 rows, flat schema).
- Cross-check vs surviving `events.jsonl` (schema-backfilled): all 8 rows'
  original fields match `labels.*` exactly; `fingerprint` = sha256(`flag`)
  verified for every row; `record_kind` = `forged_flag_ioc`.
- `SHA256SUMS` regenerated to cover the four lane files + this provenance note.

Note: `progress.log` and `notes/analyst-note-forged-flag-hunt-2026-09-28.md`
remain absent from the dir; they were not part of this rebuild's scope.

## Lane-output layout fix 2026-09-29 (~07:15 CDT)
`validate_collections.py` flags non-event files at the collection root, so the
rebuilt lane outputs moved to their canonical spots (content unchanged):
- build_compute_flags.py → `build_compute_flags.py` (matches the
  `^(es_ingest|build)_.*\.py` co-located build-script convention); docstring
  usage/output lines updated; output path now `raw/iocs.jsonl`.
- raw/iocs.jsonl → `raw/iocs.jsonl` (lane artifact, not an event record; bytes
  verified unchanged across the move, sha256
  67a2a9c8a21957d1d4cc9944127fd5726c6f7fdb189b00ef86b7e3ba304356cf).
- The stale duplicate `scripts/forged_flag_hunt_compute_flags.py` (broken
  `CACHE_FILE` path — `scripts/cache/` never existed — superseded by this
  collection's working build script) was deleted.
`SHA256SUMS` regenerated to match.
