# PROVENANCE — LEAD 5: GitHub forensics on ExploitGym (2026-09-28)

All data retrieved read-only from the public GitHub REST API, unauthenticated,
from worker session at ~/workspace/silent-locus (remote christopherwoodall/silent-locus).

Retrieval timestamp (UTC): 2026-09-28T23:35:32Z .. 2026-09-29T~00:05Z (API responses carry no per-call stamp; file mtimes are the retrieval-time record).

## Sources / endpoints (repo: sunblaze-ucb/exploitgym)

| Cached file | Endpoint | Query window |
|---|---|---|
| commits-aug1-10.json | GET /repos/sunblaze-ucb/exploitgym/commits | since=2026-08-01T00:00:00Z, until=2026-08-10T23:59:59Z, per_page=100 |
| fix-commit-e4123d04.json | GET /repos/sunblaze-ucb/exploitgym/commits/e4123d043774623b2274e6bbe0155a423d631f0a | — |
| fix-commit-e4123d04.diff | same commit, Accept: application/vnd.github.diff | — |
| issues-all.json | GET /repos/sunblaze-ucb/exploitgym/issues?state=all&per_page=100 (29 items = full set) | — |
| repo-meta.json | GET /repos/sunblaze-ucb/exploitgym | — |
| forks-p1.json, forks-p2.json | GET /repos/sunblaze-ucb/exploitgym/forks?per_page=100&page={1,2} (146 rows) | — |
| search-repos-exploitgym.json | GET /search/repositories?q=exploitgym+in:description+OR+exploitgym+in:readme&sort=updated&per_page=50 | total_count=131 |
| related-readmes/*-README.md (5) | GET /repos/{owner}/{repo}/contents/README.md, Accept: raw | related repos (see below) |
| gists-pub-p{1,3,4}.json | GET /gists/public?per_page=100&page={1,3,4} (300 gists scanned; pages 2,5 hit 401/rate-limit and are recorded as error docs) | — |

Related repos whose READMEs were cached:
- JuhoArtturiHemminki/METR-OpenAI-Hugging-Face-Incident-Report (created 2026-09-24)
- ankit595/huggingface-openai-agent-incident.io (created 2026-09-23)
- EmmaLehec/Projet_hackaton (created 2026-09-24)
- talaria0101/cyber-mods (created 2026-09-22)
- ElenaViewSynthesis/GymSIEGE (created 2026-08-31)

## Coverage limitations (unauthenticated API)

- `/repos/{o}/{r}/stargazers` returns 401 ("Requires authentication") — per-star `starred_at` unavailable; star-growth timeline could not be built. stargazers-p1..p12.json record this response.
- `/search/code` returns 401 unauthenticated — code-content search for `DEFAULT_FLAG_SEED` / `restart_server` / `catflag` not possible. No auth was used per task guards.
- Gist scan covers public-gist descriptions + filenames only (300 gists, latest ~48h); gist file bodies were not fetched (would exceed unauthenticated quota).
- Issues API returns titles + bodies only; issue comments were NOT fetched (task guard) — threads beneath issues are unexplored.
- No PRs opened/fetched beyond #11 (the fix PR, title-only via issues endpoint).

## Notes on sensitive values

The cached fix-commit diff (fix-commit-e4123d04.diff) necessarily contains the
pre-fix hardcoded values, as published in the public repo history. They are
redacted in all prose documentation (cited as file/line only).

## Schema normalization 2026-09-29 (W2)

Built `events.jsonl` (239 rows) from `raw/` on the canonical record schema
(`scripts/validate_schema.py`: 239/239 clean). Grain is one record per
retrieved item.
- 1 × `repo_snapshot` (new kind) — repo-meta.json for
  sunblaze-ucb/exploitgym; identity `exploitgym|repo|sunblaze-ucb/exploitgym`;
  `@timestamp` = repo.pushed_at.
- 1 × `repo_commit` (new kind) — fix commit e4123d04 (PR #11), merged from
  commits-aug1-10.json + fix-commit-e4123d04.json + diff stats (17 files,
  734 additions / 124 deletions); filenames listed, pre-fix secret values NOT
  reproduced (cited as file/line only, per the redaction rule above);
  identity `exploitgym|commit|<sha>`; `@timestamp` = commit author date.
- 29 × `repo_issue` (new kind) — one per issue (issues-all.json is the full
  set); identity `exploitgym|issue|<number>`; `@timestamp` = issue created_at.
- 146 × `repo_fork` (new kind) — one per fork (forks-p1/p2.json);
  identity `exploitgym|fork|<full_name>`; `@timestamp` = fork created_at.
- 50 × `repo_search_hit` (new kind) — one per repo from
  search-repos-exploitgym.json (total_count=131, 50 cached);
  identity `github|repo-search|<full_name>`; `@timestamp` = repo created_at.
- 5 × `gist_scan_page` (new kind) — p1/p3/p4: 100 gists each, 0 exploitgym
  hits; p2/p5 emitted as `sweep_negative` (API rate limit, pages unscanned).
- 1 × `sweep_negative` — stargazers 12/12 pages 401 unauthenticated (star
  timeline unavailable); 1 × `sweep_negative` — /search/code 401
  unauthenticated (DEFAULT_FLAG_SEED code search not possible).
- 5 × `related_readme` (new kind) — related READMEs (sha256 + size carried on
  the record); created dates from the retrieval notes; identity
  `github|related-readme|<full_name>`.
Fingerprint = sha256 hex of the documented identity string (verified against
the 2023-11-14-hfspace-proxies reference implementation before writing).
SHA256SUMS regenerated (events.jsonl + all raw contents, incl.
related-readmes/); `sha256sum -c` OK.

## Rollup 2026-09-29 (W8)

Built `rollup.jsonl`: 67 rows, schema-validated (`scripts/validate_schema.py`:
0 violations).
- 66 x `fork_day_rollup` — per-day fork bursts from the 146 `repo_fork`
  events (2026-06 -> 2026-09; peak: 2026-07-22->25, 47 forks in 4 days).
  Labels: `day`, `forks.new`, `forks.cumulative`, `fork.first/last`,
  `fork.owners`; `@timestamp` = first fork of the day
  (`timestamp_source="labels:rollup.day"`); identity
  `2022-08-09-github-forensics|fork-day|<day>`.
- 1 x `issue_summary_rollup` — the 29 `repo_issue` rows collapsed: 18 open /
  11 closed, 13 PRs; `@timestamp` = max `issue.created_at`; identity
  `2022-08-09-github-forensics|issue-summary`.
Builder: `temp/build_rollup_w8.py` (repo root passed as argv[1]); per-day
counts independently recomputed from events (sum = 146 forks, final
cumulative = 146). Fingerprints = sha256 of the documented identity strings.
SHA256SUMS regenerated (38 entries, incl. rollup.jsonl); `sha256sum -c` OK.
