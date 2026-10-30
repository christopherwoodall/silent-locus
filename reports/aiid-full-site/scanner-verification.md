# AIID scanner verification — scanner-verification.md

- Module: `scripts/scanners/aiid.py` (25,670 bytes, unchanged by this lane)
- Draft cron body: `reports/aiid-full-site/aiid-scanner-cron-body-DRAFT.md`
- Verified: 2026-10-30 (America/Chicago) by the SCANNER-VERIFICATION lane
- No cron job was created (parent owns creation). Nothing was committed or pushed.

## Verdict: SHIP-WITH-FIXES (do NOT enable live until F1 + F2 are fixed)

The module is safe to hold in its current disabled state: it refuses any
live run today (no `aiid` block exists in `scripts/swarm-infra-config.json`),
and its dry-run performs zero network and zero state writes. But two
structural defects (F1, F2 below) corrupt the hit payload / first-run
behaviour, so the operator must NOT add `"aiid": {"enabled": true}` until
they are fixed. F1 and F2 are logic changes, not mechanical fixes, so this
lane left the module untouched per its brief.

## Per-check table

| # | Check | Result |
|---|-------|--------|
| 1 | `py_compile` passes | PASS — `python3 -m py_compile scripts/scanners/aiid.py` → OK |
| 2 | `--help` works | PASS — shows `--dry-run`, `--since-hours` (default 24), `--json` |
| 3 | `--dry-run` performs zero network / zero state writes | PASS — output is the three `[dry-run]` lines + `[dry-run] would return 0 hits` + `[]`, exit 0; afterwards no `scripts/scanners/state/aiid*` file exists and no error-log write was made by the dry-run path (dry-run returns before `load_config`, before any `_report`) |
| 4 | Live run refuses while disabled | PASS — `python3 scripts/scanners/aiid.py --since-hours 168 --json` prints `[aiid] disabled … refusing live scan` and `[]`, exit 0, no state file created |
| 5 | Disabled-by-default gate honoured (sibling pattern) | PASS — live scan requires `scripts/swarm-infra-config.json` → `"aiid": {"enabled": true}`; config today has NO `aiid` key (verified by parsing the file). Matches the `surfacewatch`/`cairnwatch` pattern (`cfg.get("<lane>", {}).get("enabled", False)`, fail-closed on missing/unreadable config) |
| 6 | State write uses no shared fixed `.tmp` name | PASS — `_save_state` uses `STATE_PATH + f".tmp.{pid}.{uuid4 hex[:8]}"` + atomic `os.rename`. This is the repo lesson applied correctly. NOTE (inherited, not this module): `_common.report_error` still uses a fixed `error-log.jsonl.tmp` name — out of this lane's scope, do not edit `_common.py` from this ticket |
| 7 | State load is safe on corruption | PASS — schema/version/shape checked; on failure the file is quarantined to `aiid_state.json.corrupt-<ts>` and the run re-baselines with zero hits |
| 8 | No login / session / POST / cookie / auth code paths | PASS — opener is built from `ProxyHandler, UnknownHandler, HTTPHandler, HTTPDefaultErrorHandler, _NoRedirect, HTTPErrorProcessor` only: no `HTTPCookieProcessor`, no auth handler. The only request is a bare `urllib.request.Request(SNAPSHOTS_URL)` (GET by default, no body). No `--url` override exists; `SNAPSHOTS_URL` is hardcoded and `ALLOWED` is a frozenset of that one URL. Grep for POST/login/session/cookie/auth hits only docstrings/comments stating the prohibition. The login-gated incidents list page is never referenced as a fetch target |
| 9 | Polite rate respected | PASS — exactly one GET per run; 2.0 s spacing, 30 s timeout, max 1 retry on transport errors only, HTTP 429 = hard stop for the run, redirects NOT chased (3xx / final-URL mismatch = degraded, state listing untouched), 2 MB streaming cap. Matches the sibling `surfacewatch`/`cairnwatch` contract (2 s / 30 s / 1 retry / 2 MB) |
| 10 | Snapshot URL handling matches the real snapshots page | PARTIAL — see F1. URL itself is correct (`https://incidentdatabase.ai/research/snapshots/`), the weekly cadence is confirmed, and the `.tar.bz2` / `.xlsx` extensions are both in `_SNAPSHOT_HREF_RE`. But the date-keyed parse collapses the tarball and the Excel export for the same date into one entry (F1) |
| 11 | New/changed detection logic is sound (pure diffs) | PASS for the pure functions, FAIL in live wiring — see F1 (key collision) and F2 (degraded first run). `diff_snapshots` (new / changed-URL / vanished) and `diff_incidents` (new / changed-hash) were unit-exercised: new + changed + vanished/incident cases all return correctly. Vanished snapshot dates are correctly logged-only, never hits. Name-like columns are correctly excluded from `_row_hash` (verified: changing only `submitter` leaves the hash unchanged) |
| 12 | `parse_snapshot_rows` formats | PASS for JSON / JSONL / CSV (exercised: JSON list → `{id: hash}`). LIMIT: it cannot parse `.xlsx` binary (decodes as UTF-8-replace, then falls through to `{}`) — the ingest worker, not this module, must extract rows from the Excel export or the tarball before calling `scan(snapshot_incidents=…)` |
| 13 | `_common.py` contract compliance | PASS — `scan(since_hours, seen_ids, dry_run)` signature, `make_hit` (lane `aiid`, grade SECONDARY, MEDIUM new / LOW incident-changed), `emit`, `parse_args`, `redact_secrets` on all hit/state/error paths, shared `USER_AGENT`. Minor note: `ALLOWED` is defined but never referenced by the fetch code (the fetch uses `SNAPSHOTS_URL` directly) — dead variable, harmless, left untouched |
| 14 | Draft cron body: schedule | PASS with correction — see F3. Weekly, Mondays 09:00 America/Chicago, `--since-hours 168`. Weekly (not daily) is right for a weekly source |
| 15 | Draft cron body: paths and command | PASS — `cd ~/workspace/silent-locus && python3 scripts/scanners/aiid.py --since-hours 168 --json` is correct: repo root, module path, and both flags exist. Dry-run command in the draft is also correct |
| 16 | Draft cron body: no session / login | PASS — draft states the never-list explicitly and correctly forbids adding the enable block without an explicit operator order |
| 17 | Draft cron body: delivery rule | PASS — silent on zero hits; surfaces only new/changed snapshots, new/changed incidents (when a parsed map is supplied), and run failures/quota blocks, via the main agent as the single surface point. Matches the pipeline rule |
| 18 | Draft cron body: state description | PASS — state path, contents (IDs + hashes only, no titles/names), corrupt-quarantine file, and error-log path all match the module code |

## Live-page ground truth (checked 2026-10-30)

Text fetch of `https://incidentdatabase.ai/research/snapshots/` (crawled
2026-10-30 11:51 UTC) confirms:

- "Snapshot Downloads — Weekly point-in-time dumps … in JSON, MongoDB
  archive, and CSV formats." Latest entry 2026-10-26 10:15 AM,
  121.49 MB, `backup-20261026101519.tar.bz2` (hosted on
  `pub-72b2b2fc36ec423189843747af98f80e.r2.dev`). Prior Mondays
  2026-10-19, 2026-10-12, 2026-10-05 follow the same shape.
  2026-10-26, 2026-10-19 were confirmed Mondays (America/Chicago).
- "Excel Export — An Excel file, updated weekly … updated every
  Monday." Latest entry 2026-10-26, 2.60 MB,
  `AIID_Excel_Export-20261026.xlsx`, same R2 host.
- So the Monday cadence in the draft is now CONFIRMED (the draft's own
  caveat that "the weekday of publication is not confirmed" is stale),
  and the next snapshot is due Monday 2026-11-02.
- The tarball (~121 MB) correctly exceeds the module's 2 MB cap, so the
  module's decision to never download archives itself is correct.

## Fixes applied

NONE. No mechanical defects (typos, wrong paths, missing flags) were
found in the module or the draft's command. The module file is byte-
identical to its as-received state (25,670 bytes, still untracked in
git). The draft cron body was not edited: this lane's write scope is
this report plus mechanical corrections to the module only.

Before/after log: no before/after — nothing changed.

## Open fix list (do NOT enable live until F1 + F2 are fixed)

### F1 — BLOCKER: tarball and Excel entries for the same date collapse into one state entry

- Location: `parse_snapshot_listing` (HTML path), `out[date] = url`.
- Evidence: the live page lists BOTH `backup-20261026101519.tar.bz2`
  and `AIID_Excel_Export-20261026.xlsx` under date 2026-10-26 (and the
  same for every Monday). The parser keys by date alone, so the later
  section (Excel) overwrites the earlier (tarball). Reproduced with a
  synthetic listing: tarball + xlsx for 2026-10-26 → only the xlsx URL
  survives.
- Consequences: (a) a `aiid.snapshot.new` hit reports the Excel URL,
  not the tarball URL, so an ingest worker following the hit fetches
  the wrong artifact; (b) a tarball-URL change alone never fires
  `aiid.snapshot.changed` if the Excel URL is unchanged (and vice
  versa); (c) the two artifacts are different products and must not
  share one state slot.
- Required fix (structural, left to the parent): key snapshot entries
  by (date, kind) — e.g. separate `tarball` and `excel` slots — or
  keep two URLs per date, and emit distinct hit types/fields per kind.
  State schema version must bump with the change. Verify against the
  live page after fixing: 2026-10-26 must yield both URLs.

### F2 — BLOCKER: a degraded first run poisons the next run into a false-positive flood

- Location: `scan()` degraded-fetch branches (`body is None` /
  zero-entries parse).
- Evidence (code reading): on a degraded fetch the branch increments
  `consecutive_gaps` and calls `_save_state(state)` — even when the
  loaded state was a fresh blank baseline (no state file existed).
  The next successful run then loads a real state file, so
  `silent` is False, and EVERY historical snapshot date in the
  listing (200+ entries back to 2021) is reported as
  `aiid.snapshot.new` in one run.
- Required fix (structural, left to the parent): on a degraded fetch,
  do not persist a blank/first-run baseline — either skip the save
  when the run was a fresh baseline, or persist a marker that forces
  the next successful run to re-baseline with zero hits. Same
  consideration applies after a corrupt-state quarantine followed by
  a degraded fetch.

### F3 — Cron schedule: move Monday 09:00 to Monday afternoon America/Chicago

- Evidence: snapshots publish Mondays around 10:10–10:16 AM (page
  timestamps; timezone of the page clock is not stated). A 09:00
  Chicago run risks landing before that Monday's snapshot appears,
  delaying detection by a full week (not a loss — the state diff
  still catches it next week — but a needless week's delay).
- Required fix (parent, at cron creation): schedule Monday afternoon
  Chicago time (e.g. 15:00) instead of 09:00, and update the draft's
  stale "weekday not confirmed" caveat to "Monday confirmed
  2026-10-30 from the live snapshots page".

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

## Dry-run evidence (verbatim, 2026-10-30)

```
$ python3 -m py_compile scripts/scanners/aiid.py   → OK (no output)
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
```

Post-run state check: no `scripts/scanners/state/aiid*` file exists
after either run. Pure-function spot checks passed: listing parse
(tarball + xlsx), snapshot diff (new/changed), incident diff
(new/changed), name-insensitive row hash, JSON row parse.

## What the parent still owns

1. Fix F1 + F2 in `scripts/scanners/aiid.py` (structural; not done here).
2. Create the cron with the F3 schedule (Monday afternoon Chicago),
   weekly, using the draft's verified command.
3. Do NOT add `"aiid": {"enabled": true}` to
   `scripts/swarm-infra-config.json` until F1 + F2 are fixed and the
   operator has ordered the scanner live.
4. On the first live run, confirm: entry count is sane (not zero),
   first run baselines with zero hits, and 2026-10-26 yields both the
   tarball and Excel URLs after F1.
