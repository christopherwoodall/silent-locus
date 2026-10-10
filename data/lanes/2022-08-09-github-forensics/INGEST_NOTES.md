# INGEST_NOTES — 2022-08-09-github-forensics

GitHub forensics on `sunblaze-ucb/exploitgym` (LEAD 5, retrieved 2026-09-28/29
via public GitHub REST API, unauthenticated). Legacy lane:
`evidence/2022-08-09-github-forensics/` (239 event rows + 67 rollup rows = 306).
Build script: `build_factum_bundle.py` (moved here from the evidence dir).

## Mapping decisions

Legacy `record_kind` -> Factum type, one record per legacy row:

| legacy kind | count | Factum mapping |
|---|---|---|
| repo_snapshot | 1 | observation `dataset.snapshot` (dataset_uri = repo URL, coverage metadata_only; stars/forks/open-issues in tags) |
| repo_commit | 1 | observation `web.capture` (commit URL, capture_kind http, tool GitHub REST API; sha/message/author/files/additions/deletions in tags) |
| repo_issue | 29 | observation `web.capture` (issue URL; number/title/state/user/is_pr in tags) |
| repo_fork | 146 | observation `infra.ioc` (term = fork full_name, category other, status active) |
| repo_search_hit | 50 | observation `infra.ioc` (term = repo full_name, category other, status active; search query/total in tags) |
| gist_scan_page | 3 | observation `reachability.check` (outcome response, http_status 200; scanned=100, hits=0 in tags) |
| sweep_negative | 4 | observation `reachability.check` (outcome blocked; 403 for gist rate-limit pages, 401 for stargazers and /search/code; exact API error strings in `error`) |
| related_readme | 5 | observation `web.capture` (README contents API URL; sha256/size/cached_path in tags) |
| fork_day_rollup | 66 | claim (property `fork_day_burst`, subject @run-ingest) |
| issue_summary_rollup | 1 | claim (property `issue_summary`, subject @run-ingest) |

- Terms are real IOC values (GitHub `owner/repo`), never internal ids. The
  legacy identities (`exploitgym|fork|<full_name>` etc.) are preserved in
  tags.legacy_fingerprint.
- The pre-fix hardcoded secret values from the fix-commit diff stay redacted
  (file/line only), per the lane's standing redaction rule; the commit
  observation carries `redaction_note` verbatim from the legacy record.
- `related_readme` created dates are date-only in the source; observed_at is
  midnight UTC with `timestamp_source` flagged in tags.
- Claim `note` = legacy rollup description byte-identical; `value.labels` =
  legacy labels verbatim minus `timestamp_source` (kept in tags).
- 2 source records point at the POST-MOVE lane paths
  (`data/lanes/2022-08-09-github-forensics/events.jsonl`,
  `.../rollup.jsonl`); the files move there after submit, before the move
  commit. 1 run record (run_kind extraction) covers the build; per-day fork
  counts independently recomputed (sum = 146 = repo_fork rows).
- No edges at ingest (SKILL.md rule; edge building is a separate pass).
- tags.lane = "2022-08-09-github-forensics" on all 309 batch records.

## Dedup

- `match --text "exploitgym" --mode fuzzy`: 0 pre-submit matches.
- `match --text "e4123d04" --mode fuzzy`: 0 pre-submit matches.
- In-batch: 146 fork full_names unique, 50 search-hit full_names unique,
  29 issue numbers unique, 66 rollup days unique; fork/search term sets
  disjoint. Post-submit spot checks: `match --text "senopaul/exploitgym"`
  and `match --text "sunblaze-ucb/exploitgym"` return only this lane's
  records.
- `seen_before` empty on submit (fresh batch).

## Batch

Batch `43833c717f774278b5a798800e47ba8f`: 239 observations + 67 claims +
1 run + 2 sources (+ lane record created separately via `lane new`).
`export` ok, `verify` ok: 0 failures.

## Cleaner — PASS

- 309/309 records tagged lane=2022-08-09-github-forensics; no manually set
  factum.* tags (toolkit-stamped only); grade OBSERVED on all.
- All refs unique and match the bundle ref pattern (one fix applied at build
  time: long repo names exceeded the 64-char ref limit; refs now use the
  legacy fingerprint prefix).
- All @refs resolve; all observed_at are RFC3339 UTC from legacy labels
  (no invented times).
- Schema validation passed on submit (the single ref-pattern failure was
  fixed and resubmitted, not retracted).

## Adversarial validator — PASS

- A1 type fit: web.capture for API-retrieved repo/commit/issue/README
  objects; infra.ioc for fork/search-hit marker terms (AGENTS.md: "searchable
  marker term"); reachability.check for scan pages and blocked endpoints;
  dataset.snapshot for the repo snapshot; claims for computed rollups
  (colony-ai precedent). No registered github pack exists; no new pack
  proposed — existing types cover the shapes.
- A2 term mapping: term = actual `owner/repo` value in all 196 ioc records.
- A3 timestamps: no invented times; date-only README dating flagged.
- A4 verbatim: claim notes and value.labels byte-identical to legacy rows
  (checked against the exported batch); no bodies required by these schemas;
  secret values stay redacted per lane rule.
- A5 dedup: documented above; not_found scoped to structured records.
- A6 no edges at ingest: 0 edge records in batch; claims cite @run-ingest
  only.
- A7 lane tag: "2022-08-09-github-forensics" is new; zero collision with
  prior lanes.
- A8 scope/sensitivity: public GitHub API metadata only; no operator-identity
  pursuit; no secrets reproduced.

## Root causes fixed

- Factum bundle `ref` pattern is `^[A-Za-z][A-Za-z0-9_.-]{0,63}$` (64 chars
  max). Long repo names (e.g. a 68-char `obs-search-...` ref) fail schema
  validation on submit. Fixed in `build_factum_bundle.py`: refs derived from
  the 12-char legacy fingerprint prefix instead of the term. Worth a note in
  the skill docs for future lane workers.
- `match --text "<key-term>" --mode fuzzy` is a FALSE NEGATIVE for values
  longer than ~1.5x the query: cli.py gates fuzzy candidates on
  `ratio(value, raw_value) >= 65`, so `match --text "exploitgym"` misses
  `sunblaze-ucb/exploitgym` (ratio 62.5) and `match --text "e4123d04"`
  misses the 40-char commit sha (ratio 33). Pre-submit fuzzy checks for this
  lane were negative by construction. Reliable dedup used instead:
  in-batch uniqueness on primary identifiers, post-hoc exact-value lookups
  in `search_values`, and an FTS-level overlap audit: 79 non-lane (node,
  value) hits contain "exploitgym" (HF Hub URLs from the
  2025-05-15-hf-tampering-check lane — distinct entities), with ZERO exact
  overlap against this lane's 196 ioc terms. No duplicates submitted.
  Sibling lanes' "zero matches" dedup claims for long values are suspect
  under this gate; exact-value checks are the safe route.
