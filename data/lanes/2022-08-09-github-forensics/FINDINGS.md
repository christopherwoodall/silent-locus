# Findings

Grade claims OBSERVED, UPSTREAM, or INFERENCE.

- OBSERVED: `sunblaze-ucb/exploitgym` had 1,104 stars and 145 forks at
  2026-08-06T00:36:02Z (repo snapshot via GitHub REST API).
- OBSERVED: Commit `e4123d04` (PR #11, "Feat/dynamic secrets") replaced
  hardcoded `DEFAULT_SALT` / `DEFAULT_FLAG_SEED` / `DEFAULT_API_KEY` with
  per-startup dynamic secrets; 17 files, +734 / -124. Pre-fix secret values
  stay redacted (file/line only).
- OBSERVED: 146 forks observed 2026-06-04 -> 2026-09-28; peak burst
  2026-07-22 -> 2026-07-25 (47 forks in 4 days). Per-day counts in 66
  `fork_day_burst` claims.
- OBSERVED: 29 issues/PRs total (18 open, 11 closed; 13 PRs), window
  2026-06-14 -> 2026-09-24.
- OBSERVED: Repo search ("exploitgym" in description/readme) returned 131
  repos; 50 cached as indicator terms.
- OBSERVED: 300 public gists scanned (pages 1, 3, 4); 0 exploitgym hits.
  Pages 2 and 5 hit the API rate limit (unscanned).
- OBSERVED: `/stargazers` and `/search/code` returned 401 unauthenticated;
  star-growth timeline and code-content search were not possible.
- OBSERVED: 5 related repo READMEs cached (incident reports and mods,
  created 2026-08-31 -> 2026-09-24).

Scope is agents and agent infrastructure. No operator identity pursued.
