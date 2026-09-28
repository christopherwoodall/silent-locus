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
