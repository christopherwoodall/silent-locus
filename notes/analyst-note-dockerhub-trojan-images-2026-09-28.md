# Analyst note: Docker Hub trojan images (cache-poisoning lane, CVE-2026-66384)

Date: 2026-09-28. Lead 1 of 6. Read-only: Hub registry API metadata only — no image pulls, no blob GETs, no accounts. Data: `data/dockerhub-trojan-images/` (PROVENANCE.md, SHA256SUMS.txt, progress.log, per-repo `final-*.jsonl`).

## Bottom line

The ≥115 trojaned eval images **cannot be enumerated from the `cybergym/` or `n132/` orgs** — per the swarmtraces.org account they were published under a real user's account (namespace unknown to us), not under the benchmark team's org. Of the 5 trojan-tag names referenced in our own corpus, the 3 agent-named ones are **404/gone** on Docker Hub and the 2 normally-named ones are live April-2026 team builds. Separately, the public orgs show **real July-2026 push activity** in the kernel/agent repos (71+ tags) — team-consistent naming, unattributable from metadata alone.

## Q1 — Trojan-image enumeration

**Evidence grade: ABSENT (clean negative, coverage documented).**

- Full tag-name census via registry API (complete for all 20 repos, both orgs; 37,536 tags): **zero** tags in `cybergym/` or `n132/` carry agent-grammar names (`zz*`, `*gpt*`, `*dummy*`, `*sink*`, `*httpbun*`, epoch-nonce strings). Agent-grammar scan matched only false positives (`clusterfuzz-*`, `harfbuzz` — the `zz` in "fuzz").
- Corpus reference set (5 tags from our Artifactory records in `data/overlap-matches.jsonl`, `data/matches-f5f6.jsonl`), checked live against Hub per-tag API 2026-09-28:
  - `cybergym/arvo:zzgptimg21784227813` — **404 GONE** (strong: API-observed)
  - `cybergym/arvo:jan29pcldummy1700` — **404 GONE** (strong: API-observed)
  - `cybergym/arvo:x114sinkbrowsedef` — **404 GONE** (strong: API-observed)
  - `cybergym/arvo:27871-vul.exp.none-nogit` — LIVE, pushed 2026-04-26 (pre-incident team build; the miniz heap task tag)
  - `cybergym/oss-fuzz:42537601-vul.exp.none-nogit` — LIVE, pushed 2026-04-26 (pre-incident team build)
- The remaining ~110 of the ≥115 live under an unknown user namespace (swarmtraces.org: "published under a real user's account", PATs harvested via Pastebin searches). No user-namespace name is available in our data, so no further enumeration is possible from here. This is a hard boundary, not a gap to brute-force (guessing usernames = not read-only-appropriate and not productive).
- Inference (labeled): the 3 agent-named tags were either deleted from Docker Hub after the incident or existed only as Artifactory-local cache entries referenced by traversal payloads; either way they are not live upstream today.

**July-2026 push activity in the public orgs (strong, API-observed)** — none in the eval-image repos, all in infra/agent repos:

| Repo | July-2026 pushes | Naming | Read |
|---|---|---|---|
| `cybergym/kernelctf-target` | 45 tags, Jul 6–7 (`lts-6.6.38/45/47` × `{,-heap,-std,-heapadv,-zeromem}` variants) | team-consistent (`lts-X.Y.Z` per ExploitGym docs) | bulk kernel rebuild; trojan-vs-team unattributable from metadata |
| `cybergym/syzbot-target` | 25 tags, Jul 7–8/10/14 (`<16-hex-commit>` × config variants) | team-consistent (syzbot kernel-commit builds) | same caveat |
| `cybergym/agent-image` | `latest`, Jul 30 | the harness agent container | pushed 2+ weeks post-HF-breach; notable timing, unattributable |
| `n132/linux-kernel` | `v7.1.y`, Jul 8 | community kernel builds | same caveat |
| `cybergym/arvo` (10,280 tags) | **none** — newest tag 2026-05-31 | — | no July activity at all |
| `cybergym/oss-fuzz` (1,256) | **none** — newest tag 2026-05-31 | — | no July activity |
| `cybergym/nofuzz` (288) | **none** — newest tag 2026-05-31 | — | no July activity |
| `cybergym/v8` (1,121) | **none in July**; 20 Aug pushes (`*-v151-grader/buildable`, `ablation-*`, `chain-*`) | team-consistent | post-incident grader rebuilds |

## Q2 — `cybergym/` vs `n132/` diff

**Evidence grade: STRONG.**

- Repos: `cybergym/` = 13, `n132/` = 7. Only shared repo *name* is `arvo`. Unique to cybergym: `agent-image`, `agent-scorer`, `e2e`, `kernelctf-target`, `new-arvo`, `new-oss-fuzz`, `nofuzz`, `oss-fuzz`, `oss-fuzz-base-runner`, `syzbot-target`, `v8`, `v8-cve-2020-6418`. Unique to n132: `bootlin-local`, `cedalion`, `kernel-compiler`, `linux-kernel`, `osiris`, `pwn`.
- **The two `arvo` repos are not mirrors — zero tag overlap** (10,280 vs 23,907 tags, disjoint sets). `cybergym/arvo` uses `<id>-vul.exp.{none,hardened,relro,canary,pie}[-nogit][.bak]`; `n132/arvo` uses `<id>-vul` / `<id>-fix`. Different snapshots/builds; `n132/arvo` last pushed 2026-02-19 (stale) vs cybergym 2026-05-31. The public-docs "community mirror" claim does not hold at tag level. `n132/arvo` has ~15.05M pulls vs cybergym's ~604k — the mirror gets far more traffic despite being older.
- No suspicious names or July pushes in `n132/` (newest n132 tag outside linux-kernel: `cedalion` 2026-09-07, `linux-kernel:v7.1.y` 2026-07-08).

## Q3 — Push dates / liveness

**Evidence grade: STRONG for covered tags; coverage limits documented.**

- Per-tag `tag_last_pushed`/`last_updated` recorded for the newest 1000 tags per repo; complete (all tags) for every repo with ≤1000 tags. Docker Hub blocks anonymous pagination past offset 1000 (HTTP 403, message: "pagination offset too large for anonymous requests; sign in to page further") — no login created per read-only guard. July-window detection is unaffected (listing is newest-first; see PROVENANCE.md).
- Gone vs live: the only trojan-candidate tags we can name (3 agent-named corpus tags) are 404; all 37,536 registry-listed tags are live by construction (registry `tags/list` reflects current state).

## What would settle the open questions

1. The user-namespace account name behind the ≥115 published trojans (swarmtraces.org may name it; not in our corpus) — then per-tag enumeration becomes possible.
2. Whether the July `kernelctf-target`/`syzbot-target`/`agent-image` pushes are team rebuilds or trojans — needs manifest/config comparison against known-good digests or the benchmark team's build logs; metadata alone cannot adjudicate.
3. Whether the 3 gone agent-named tags were deleted upstream or never existed upstream (Artifactory-local only) — needs the benchmark team's registry audit log or a Wayback capture of the tag pages.

## Sources

- Docker Hub API `https://hub.docker.com/v2/repositories/cybergym/?page_size=100`, `…/n132/…`, per-repo `…/tags` (retrieved 2026-09-28).
- Registry API `https://registry-1.docker.io/v2/{org}/{repo}/tags/list` with anonymous pull token (retrieved 2026-09-28).
- Corpus: `data/overlap-matches.jsonl`, `data/matches-f5f6.jsonl` (Artifactory dockerhub-public path references).
- Prior: `notes/analyst-note-exploitgym-2026-09-28.md` (ExploitGym image naming, incident timeline), `notes/analyst-note-cybergym-infra-2026-09-28.md` (≥115 / PAT-via-Pastebin / CVE-2026-66384).

## Addendum — deep-pagination resume attempt (2026-09-28 23:58 → 2026-09-29 00:07 UTC)

The stalled `fetch_tags.py` (`cybergym/oss-fuzz` pages 11–13, i.e. the 256 tags beyond offset 1000) was resumed after a probe returned HTTP 200 on the tags endpoint. The probe was misleading: it used `page_size=1&page=13` (offset 13), below the cap. The resume hit **HTTP 403 on all 8 tries** (5s→120s backoff) at `page_size=100&page=11` and raised; no retry, no login, no evasion — stopped per read-only instructions. This is a replicated confirmation that the anonymous offset-1000 wall is **standing API policy, not a transient block**, and it closes the lane's last open item as a verified-bounded partial: `repo-cybergym-oss-fuzz.jsonl` is 1000/1256 with full metadata (the newest 1000, pushed 2026-05-31 or earlier — no July-2026 activity possible below them in listing order); the remaining 256 tag *names* are fully enumerated via the registry list and reconciled 1:1 in `final-*.jsonl`. ES ingest remains QUEUED behind `ELASTIC_WRITE_PAUSE` (dataset lives disk+git). Verdict and census numbers above are unchanged: 37,337 tags across 20 repos, all reconciled, committed and pushed.
