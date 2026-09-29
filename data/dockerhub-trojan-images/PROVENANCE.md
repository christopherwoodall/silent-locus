# Provenance — Docker Hub trojan-image enumeration (Lead 1 of 6)

Retrieved 2026-09-28 ~23:35–23:56 UTC (18:35–18:56 CDT); deep-pagination resume attempt 2026-09-28 23:58–2026-09-29 00:07 UTC. Read-only.

## Sources (all public, no accounts, no logins)

| Source | Used for | URL pattern |
|---|---|---|
| Docker Hub web API v2 (anonymous) | org repo lists; per-repo tag metadata (names, `tag_last_pushed`, `last_updated`, `tag_status`, digest, arch) for the newest 1000 tags per repo | `https://hub.docker.com/v2/repositories/{org}/?page_size=100`, `https://hub.docker.com/v2/repositories/{org}/{repo}/tags?page_size=100&page={1..10}`, `…/tags/{tag}` |
| Docker registry API (anonymous pull-scope token from `auth.docker.io`) | COMPLETE tag-name lists for every repo (both orgs) | `https://registry-1.docker.io/v2/{org}/{repo}/tags/list?n=1000` |
| Local corpus | reference set of agent-uploaded trojan tag names | `data/overlap-matches.jsonl`, `data/matches-f5f6.jsonl` (Artifactory `dockerhub-public[/-cache]/…` path references) |

## Method

1. `org-{cybergym,n132}-repos.json` — full org repo listings (Hub API, page 1 of 1 each).
2. `registry-tags-{org}-{repo}.json` — complete tag-name sets via registry `tags/list` (20 repos; 37,437 tags total). Cached; the fetch script skips existing files (resumable).
3. `hub10-{org}-{repo}.jsonl` — tag metadata (newest 1000 per repo, Hub API pages 1–10). For repos with ≤1000 tags this is the complete set with timestamps.
4. `corpus-trojan-tag-liveness.jsonl` — per-tag Hub lookups for the 5 corpus-referenced trojan tags (live vs 404).
5. `final-{org}-{repo}.jsonl` — merged per-repo records: `org, repo, tag, tag_last_pushed, last_updated, tag_status, digest, images_arch, metadata_fetched, liveness, retrieved, sources`. `final-gone-trojan-tags.jsonl` holds the 3 corpus tags that 404.

## Constraints encountered (documented, not worked around)

- Docker Hub API rejects anonymous pagination past offset 1000: HTTP 403 `{"message":"pagination offset too large for anonymous requests; sign in to page further"}`. No login was created (read-only guard). Consequence: Hub metadata covers only the newest 1000 tags per repo for the 4 large repos (`cybergym/arvo` 10,280; `cybergym/oss-fuzz` 1,256; `cybergym/v8` 1,121; `n132/arvo` 23,907).
- July-2026 detection is still complete: Hub tag listing is ordered newest-first, and the newest fetched tag in each large repo predates (arvo: 2026-05-31; oss-fuzz: 2026-05-31) or brackets (v8: Aug pushes present, zero July; n132/arvo: 2026-02-19) the July window. Any July push would necessarily sort above the fetched newest tag.
- Registry `tags/list` has no anonymous pagination cap; tag names are complete. Timestamps for tags beyond the newest 1000 are not available without a Hub login or config-blob reads (blob reads were out of scope).
- No image pulls, no layer/blob GETs, no manifest content reads beyond Hub metadata. Manifest digests were recorded from Hub metadata only.
- `n132/arvo` registry count (23,907) vs Hub `count` (23,900): 7-tag drift between the two fetches (~2 min apart); registry list is the fresher value.

## Scripts

- `fetch_tags.py` — deep-pagination path (pages 11+); resume of `cybergym/oss-fuzz` pages 11–13 attempted 2026-09-28 23:58 → 2026-09-29 00:07 UTC: HTTP 403 on all 8 tries (5s→120s backoff) at `page_size=100&page=11`, then `RuntimeError: failed after 8 tries`. This CONFIRMS the anonymous-pagination wall is standing policy, not a transient block — the task's own probe that returned HTTP 200 was on offset 13 (`page_size=1&page=13`), i.e. below the 1000-offset cap, so it never tested the wall. No login created, no evasion attempted; stopped per instructions. Script kept for the audit trail.
- ES ingest: QUEUED — `ELASTIC_WRITE_PAUSE` in effect; dataset lives disk+git only. Post-pause, ingest `final-*.jsonl` + `corpus-trojan-tag-liveness.jsonl` under the shared schema (notes/gems-es-mapping.json, `event.dataset.keyword` multi-field at index creation).
- `registry_tags.py` — registry `tags/list` enumeration (resumable, skips cached files).
- `fetch_hub10.py` — Hub pages 1–10 metadata (resumable, skips cached files).
- `fetch_stdout.log`, `registry_stdout.log`, `hub10_stdout.log`, `progress.log` — run logs.

## Corpus reference set (trojan tag names from our own data)

Extracted from Artifactory `dockerhub-public[/-cache]/` path references in `data/overlap-matches.jsonl` / `data/matches-f5f6.jsonl`:
`cybergym/arvo:zzgptimg21784227813`, `cybergym/arvo:jan29pcldummy1700`, `cybergym/arvo:x114sinkbrowsedef`, `cybergym/arvo:27871-vul.exp.none-nogit`, `cybergym/oss-fuzz:42537601-vul.exp.none-nogit`.
