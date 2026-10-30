# AIID scanner fix note — F1 + F2 (blockers fixed)

- Module: `scripts/scanners/aiid.py` (25,670 bytes before, 29,346 bytes after)
- Basis: `reports/aiid-full-site/scanner-verification.md` (verdict SHIP-WITH-FIXES)
- Fixed: 2026-10-30 (America/Chicago), by the SCANNER-FIX lane
- NOT done, per brief: no cron job created, no config block added,
  nothing committed or pushed, live scanning NOT enabled.
  `scripts/swarm-infra-config.json` still has no `aiid` block (verified
  below), so the module still refuses any live run.

## F1 — BLOCKER, FIXED: tarball and Excel entries for the same date no longer collapse

### Before (as verified)

- `parse_snapshot_listing` returned `{date: url}`. In the HTML path:
  `out[date_m.group(1)] = url`; in the JSON path: `out[date] = url`.
- The live snapshots page lists BOTH
  `backup-20261026101519.tar.bz2` and `AIID_Excel_Export-20261026.xlsx`
  under 2026-10-26, so the later (Excel) entry overwrote the earlier
  (tarball) entry. Only the xlsx URL survived in state.
- Consequences, per the verifier: a `aiid.snapshot.new` hit pointed
  at the Excel URL instead of the tarball URL, and a tarball-URL
  change alone never fired `aiid.snapshot.changed`.
- State schema version was 1, with snapshot keys as bare dates.

### After (exact change)

1. New helpers, after `_SNAPSHOT_HREF_RE`:
   - `_snapshot_kind(url)` — strips query/fragment, lowercases, and
     returns `"excel"` for `.xlsx`, `"tarball"` for `.tar.bz2` /
     `.tar.gz` / `.tgz`, `"archive"` for `.zip`, `"json"` for `.json`,
     `"csv"` for `.csv`, else `"file"`.
   - `_entry_key(date, kind)` — returns `f"{date}|{kind}"`, the
     JSON-safe state/diff key for one (date, kind) entry.
   - `_split_entry_key(key)` — inverse; a bare date yields kind `""`.
2. `parse_snapshot_listing` now returns `{(date, kind): url}`:
   - HTML path: `out[(date_m.group(1), _snapshot_kind(url))] = url`
   - JSON path: `out[(date, _snapshot_kind(url))] = url`
   - The tuple form is used at the parse layer only, because JSON
     state cannot hold tuple keys (`json.dumps` raises
     `TypeError: keys must be str, int, float, bool or None, not tuple`
     — confirmed by direct test during this fix).
3. `scan()` converts parse output to state entries:
   `new_entries = {_entry_key(d, k): {"url": u, "anchor_hash": _sha256(f"{d}|{k}|{u}") } for (d, k), u in entries.items()}`
   The anchor hash now includes the kind, so a kind collision cannot
   alias two entries to one hash.
4. `diff_snapshots` is key-agnostic and now documented over
   `{"date|kind": {url, ...}}`; it returns `(new_keys, changed_keys,
   vanished_keys)`. A tarball-URL change fires independently of the
   Excel URL for the same date, and vice versa.
5. Snapshot hits now carry the kind:
   - seen keys: `aiid:snapshot:{date}|{kind}:new` /
     `aiid:snapshot:{date}|{kind}:changed` (previously date-only)
   - summaries: `[aiid] new weekly snapshot 2026-10-26 (tarball)` /
     `[aiid] snapshot 2026-10-26 (tarball) download URL changed`
   - hit extra: `snapshot_date`, `snapshot_kind`, `snapshot_url`
     (plus `previous_url` on changed hits, as before)
   - vanished entries are still logged-only, never hits, now logged
     under key `entries` with the `date|kind` keys.
6. `last_seen_snapshot_date` is now the max of the DATE parts
   (`max(_split_entry_key(k)[0] for k in new_entries)`), not
   `max(new_entries)`, so kind suffixes cannot affect the date.
7. State schema version bumped: `STATE_VERSION = 1` → `2`, with a
   comment stating a v1 file fails the version check in `_load_state`
   and is quarantined + re-baselined, never misread as v2 keys.
   This is the existing `_load_state` behaviour (version mismatch
   raises, the file is renamed to `aiid_state.json.corrupt-<ts>`,
   the run returns a blank state with `silent=True`); no migration
   code was added, because silently reinterpreting bare-date keys
   as `date|kind` keys is exactly the misread the bump must prevent.
   Module docstring state description updated to
   `{"date|kind": {url, anchor_hash}}` (schema_version 2).

## F2 — BLOCKER, FIXED: a degraded first run no longer poisons the next run

### Before (as verified)

- In `scan()`, both degraded branches (fetch returns `body is None`
  or a note other than `ok`/`capped_2MB`; and a parse to zero
  entries) unconditionally incremented `consecutive_gaps` and called
  `_save_state(state)` — even when `_load_state` had just returned a
  fresh blank baseline (`silent=True`: no state file existed, or a
  corrupt file had just been quarantined).
- The next successful run then loaded a real state file, so
  `silent` was False, and EVERY historical snapshot date in the
  listing (200+ back to 2021) was reported as `aiid.snapshot.new`
  in one run — a false-positive flood.

### After (exact change — option chosen: do NOT persist a fresh baseline)

- The fix takes the first of the two options the brief offered:
  **do not persist a fresh baseline on a degraded fetch**. No
  force-re-baseline marker was added, because no marker is needed:
  not writing a state file leaves `_load_state` returning
  `silent=True` on the next run, which already re-baselines with
  zero hits. Adding a marker field would have been a second state
  shape to maintain for no extra safety.
- Both degraded branches in `scan()` are now guarded:
  ```
  if not silent:
      state["consecutive_gaps"] = int(state.get("consecutive_gaps", 0)) + 1
      _save_state(state)
  _report("fetch_gap", <message> + ("; fresh baseline not persisted" if silent else ""), ...)
  return []
  ```
  The error report is still written in both cases (reporting is not
  state); only the state save is skipped on a fresh baseline.
- The same guard covers a corrupt-state quarantine followed by a
  degraded fetch, because `_load_state` returns `silent=True` for
  quarantined state as well (stated in the code comment).
- Unchanged, and already safe: the `http_429` branch returns before
  any state save, so a rate-limited first run never persisted a
  baseline either. Degraded runs on an EXISTING state still
  increment `consecutive_gaps` and save, preserving the listing
  untouched — that behaviour is kept deliberately.
- Module docstring updated to state the rule: a degraded fetch on a
  fresh baseline persists nothing, so the next successful run still
  re-baselines with zero hits.

## Verification evidence

All checks below were run after the fix, from the repo root
`~/workspace/silent-locus`, unless noted. No live scan was run:
the synthetic tests use a listing modelled on the live-page pattern
(filenames and date 2026-10-26 taken from the verification report)
and monkeypatched fetch/state paths; the real state directory was
never written.

### 1. Compile, help, dry-run, disabled-by-default refusal

```
$ python3 -m py_compile scripts/scanners/aiid.py && echo PY_COMPILE_OK
PY_COMPILE_OK
$ python3 scripts/scanners/aiid.py --help
usage: aiid.py [-h] [--dry-run] [--since-hours SINCE_HOURS] [--json]
$ python3 scripts/scanners/aiid.py --dry-run
[dry-run] aiid: GET https://incidentdatabase.ai/research/snapshots/ (passive GET only, no redirects, no cookies, no auth, no POST; login-gated list page never touched)
[dry-run] aiid: state /home/hatch/workspace/silent-locus/scripts/scanners/state/aiid_state.json (read on live run, created on first live run; untouched by dry-run)
[dry-run] aiid: hits would be aiid.snapshot.new / aiid.snapshot.changed (listing diff) and, only when an ingest worker supplies snapshot_incidents, aiid.incident.new / aiid.incident.changed
[dry-run] would return 0 hits
[]
exit 0
$ python3 scripts/scanners/aiid.py --since-hours 168 --json
[aiid] disabled (config 'aiid'.enabled is not true); refusing live scan
[]
exit 0
$ ls scripts/scanners/state/aiid*
ls: cannot access 'scripts/scanners/state/aiid*': No such file or directory
$ python3 -c "import json; cfg=json.load(open('scripts/swarm-infra-config.json')); print('aiid block present:', 'aiid' in cfg)"
aiid block present: False
```

Before and after both verification runs, no
`scripts/scanners/state/aiid*` file exists. The disabled-by-default
gate is unchanged and still works.

### 2. F1 synthetic test (pure functions, no network, no state)

Input modelled on the live page: a 2026-10-26 tarball anchor
(`backup-20261026101519.tar.bz2` on the R2 host) and a 2026-10-26
Excel anchor (`AIID_Excel_Export-20261026.xlsx`), plus a 2026-10-19
tarball anchor.

```
F1 entries: {('2026-10-26', 'tarball'): 'https://pub-72b2b2fc36ec423189843747af98f80e.r2.dev/backup-20261026101519.tar.bz2',
             ('2026-10-26', 'excel'): 'https://pub-72b2b2fc36ec423189843747af98f80e.r2.dev/AIID_Excel_Export-20261026.xlsx',
             ('2026-10-19', 'tarball'): 'https://example.r2.dev/backup-20261019101000.tar.bz2'}
diff: ([], ['2026-10-26|tarball'], [])
JSON entries: {('2026-10-26', 'tarball'): 'https://x/backup-20261026101519.tar.bz2',
               ('2026-10-26', 'excel'): 'https://x/AIID_Excel_Export-20261026.xlsx'}
F1 PASS
```

Assertions passed: 3 entries (not 2 — the tarball is no longer
overwritten); tarball URL ends `backup-20261026101519.tar.bz2`;
Excel URL ends `AIID_Excel_Export-20261026.xlsx`; a tarball-only
URL change yields exactly `changed = ['2026-10-26|tarball']`
with no new/vanished entries; the JSON listing path also yields
both kinds for 2026-10-26.

### 3. F2 synthetic test (monkeypatched scan, state in a temp dir, no real state touched)

`STATE_PATH` pointed at a temp dir, `load_config` stubbed to
`{"aiid": {"enabled": True}}`, `_fetch_listing` stubbed per case.

```
A degraded-fresh hits: [] state exists: False
B zero-parse-fresh hits: [] state exists: False
C baseline hits: [] state exists: True
C state: {"schema_version": 2,
          "snapshots": {"2026-10-26|excel": {"url": "https://x/AIID_Excel_Export-20261026.xlsx", ...},
                        "2026-10-26|tarball": {"url": "https://x/backup-20261026101519.tar.bz2", ...}},
          "last_seen_snapshot_date": "2026-10-26", "consecutive_gaps": 0, "incidents": {}}
D hits: [] gaps: 1 snapshots preserved: True
E v1 load silent: True snapshots: {}
F2 PASS (A-E)
```

Cases: (A) degraded fetch on a fresh baseline writes no state file;
(B) zero-entry parse on a fresh baseline writes no state file;
(C) the next successful run baselines with zero hits and writes a
v2 state holding BOTH `2026-10-26|tarball` and `2026-10-26|excel`;
(D) a degraded run on an existing state bumps `consecutive_gaps`
to 1 and preserves the listing byte-for-byte; (E) a hand-written
v1 state file is quarantined by `_load_state`, which returns
`silent=True` with an empty snapshot map (re-baseline, zero hits).

### 4. No login / session / POST / cookie / auth paths; login-gated list page untouched

- Opener unchanged: `ProxyHandler, UnknownHandler, HTTPHandler,
  HTTPDefaultErrorHandler, _NoRedirect, HTTPErrorProcessor` only —
  no `HTTPCookieProcessor`, no auth handler.
- The only request is still a bare
  `urllib.request.Request(SNAPSHOTS_URL)` (GET by default, no body).
- `SNAPSHOTS_URL` is still the single hardcoded URL
  `https://incidentdatabase.ai/research/snapshots/`; `ALLOWED` is
  still a frozenset of that one URL; no `--url` override exists.
- Grep for POST/login/session/cookie/auth hits only docstrings,
  comments stating the prohibition, the name-exclusion column list
  (submitter/editor/author/reporter — columns dropped from hashes),
  and the `no HTTPCookieProcessor` comment. No executable path for
  any of them, and no fetch target other than the snapshots page.
- `_common.py` was NOT touched (the verifier's note that
  `_common.report_error` uses a fixed tmp name remains out of scope).

## What was NOT changed

- No cron job created. No `aiid` block added to
  `scripts/swarm-infra-config.json`. Nothing committed or pushed.
- F3 and F4 below are carried forward untouched, exactly as the
  verifier documented them. This lane fixed F1 and F2 only.

## Remaining open items (carried forward untouched)

### F3 — Cron schedule: move Monday 09:00 to Monday afternoon America/Chicago (parent owns, at cron creation)

- Evidence (verifier): snapshots publish Mondays around
  10:10–10:16 AM (page timestamps; timezone of the page clock is
  not stated). A 09:00 Chicago run risks landing before that
  Monday's snapshot appears, delaying detection by a full week
  (not a loss — the state diff still catches it next week — but a
  needless week's delay).
- Required action (parent, at cron creation): schedule Monday
  afternoon Chicago time (e.g. 15:00) instead of 09:00, and update
  the draft's stale "weekday not confirmed" caveat to "Monday
  confirmed 2026-10-30 from the live snapshots page".
- Do NOT add `"aiid": {"enabled": true}` until the operator has
  ordered the scanner live (F1 + F2 are now fixed, but enabling
  still needs the operator's explicit order).

### F4 — Robustness notes (not blockers, verify on first live run)

1. Same-line date fallback: the HTML parser takes the snapshot date
   from anchor text, href, or "the nearest preceding text on the same
   line". The live page's rendered lines put the date on the same
   line as the download link, but raw-HTML line breaks inside a list
   item are unverified — if the date and anchor sit on different
   source lines, entries parse to zero and the run degrades (gap
   logged, state untouched, no false hits). Confirm entry counts on
   the first live run; if zero, widen the date search to the
   enclosing list item.
2. Capped-page state overwrite: a `capped_2MB` listing is treated as
   `ok` and its partial entries replace full state, so entries past
   the truncation point become "vanished" and then "new" on the next
   full run. Current page size is far below 2 MB (~hundreds of short
   entries), so this is latent only; consider treating `capped_2MB`
   as degraded if the page ever approaches the cap.
3. `parse_snapshot_rows` cannot parse `.xlsx` binary — the ingest
   worker must parse the Excel export or tarball contents itself and
   pass the `{incident_id: row_hash}` map; this module alone can only
   emit listing-level hits.

## First-live-run checklist (for the parent, unchanged from verification)

1. Entry count is sane (not zero).
2. First run baselines with zero hits.
3. 2026-10-26 yields both the tarball and Excel URLs after F1
   (now `2026-10-26|tarball` and `2026-10-26|excel` in state).
