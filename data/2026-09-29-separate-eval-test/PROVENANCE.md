# PROVENANCE — separate-eval test (worker 4, off-task web-mechanism hunt)

Date: 2026-09-28. Lane: red-team falsification of the favored hypothesis
("off-task exploration by escaped ExploitGym agents explains the July-7
RubyGems XSS/SSTI wave").

## Question
Find a BETTER explanation for the July-7 RubyGems wave (215 packages /
333 releases, XSS PoCs with oast.online/webhook.site exfil, `{{7*7}}`-style
SSTI probes) than off-task exploration by the escaped ExploitGym agents.

## Sources consulted (all read-only, public web)

| # | Source | URL | Retrieved (UTC) | SHA-256 of local copy |
|---|--------|-----|-----------------|-----------------------|
| 1 | JFrog Security Research, "New packages identified in GemStuffer 'OpenAI Swarm' malicious RubyGems campaign" | https://research.jfrog.com/post/gemstuffer-openai-rubygems/ | 2026-09-29T00:29:24Z | `b6bce4b807cd51d1ad7479b23200316a7a5356b671d859eba8d3425cc5f2ef2e` (file: `sources/jfrog-gemstuffer-post.html`) |
| 2 | rubyhack.ai (Nightingale Collective) GemStuffer report — attribution scope check | https://www.rubyhack.ai | 2026-09-28 (page text fetched, not cached to disk) | n/a — cited inline |
| 3 | arXiv 2607.11288 (Mako) abstract — benchmark-shape check | https://arxiv.org/abs/2607.11288 | 2026-09-28 (page text fetched) | n/a — cited inline |
| 4 | RubyGems security advisory, legacy API-key leak (timeline anchor) | https://github.com/rubygems/blog/blob/HEAD/_posts/2026-07-22-security-advisory-legacy-api-key-leak.md | 2026-09-28 (search-result text) | n/a — cited inline |
| 5 | RubyGems HackerOne program page (VDP existence) | https://hackerone.com/rubygems | 2026-09-28 (search-result text) | n/a — cited inline |
| 6 | ajaysenr/hackerone-disclosed-reports, by-year/2026.md (disclosed-report sweep) | https://github.com/ajaysenr/hackerone-disclosed-reports/blob/HEAD/by-year/2026.md | 2026-09-28 (page text fetched, 1364 lines / 678 reports) | n/a — cited inline |
| 7 | BountyBench paper/blog/repo (candidate benchmark) | https://arxiv.org/pdf/2505.15216 ; https://github.com/bountybench/bountybench | 2026-09-28 (search-result text) | n/a — cited inline |
| 8 | CVE-Bench paper (candidate benchmark) | https://arxiv.org/pdf/2503.17332 | 2026-09-28 (search-result text) | n/a — cited inline |
| 9 | AutoPenBench paper (candidate benchmark) | https://arxiv.org/html/2410.03225v2 | 2026-09-28 (search-result text) | n/a — cited inline |
| 10 | Cybench repo benchmark README (candidate benchmark) | https://github.com/andyzorigin/cybench/blob/HEAD/benchmark/README.md | 2026-09-28 (search-result text) | n/a — cited inline |
| 11 | ARTEMIS competitive-landscape entry (candidate live-target eval) | https://github.com/evkir/cyberai/blob/HEAD/docs/competitive-landscape-2026.md | 2026-09-28 (search-result text) | n/a — cited inline |
| 12 | XBOW HackerOne #1 reporting (candidate commercial agent) | https://github.com/r00t-kim/terminator/blob/HEAD/research/llm_bug_bounty_sota_2024_2026.md ; https://www.spartechsoftware.com/cybersecurity-news/xbow-achieves-a-groundbreaking-milestone-as-the-first-ai-system-to-surpass-human-hackers-in-the-hackerone-competition/ | 2026-09-28 (search-result text) | n/a — cited inline |

## Repo-local evidence reused (already in this repo, not re-cached)
- `data/gemstuffer-jfrog-2026-09-27.csv` — 22 xss/ssti-named rows enumerated
  via grep (2026-09-28). Version-timestamp decoding done with `date -u -d @<ts>`.
- `notes/gem-jfrog-report-2026-09-27.md`, `notes/analyst-note-exploitgym-2026-09-28.md`,
  `notes/exploitgym-leads-synthesis-2026-09-28.md` — context.

## Method notes
- No accounts, no logins, no submissions, no benchmark interaction. Web
  searches + page-text fetches only.
- Benchmarks evaluated on three axes: (a) web-task family match (XSS/SSTI),
  (b) operator + date plausibility for a July-2026 window, (c) artifact-shape
  fit — whether the eval's mechanics could produce 215 gem uploads to the
  LIVE rubygems.org registry with metadata-embedded collaborator PoCs.
  Axis (c) is the binding constraint: every public sandboxed benchmark fails it.
- Attribution claims about the July-7 wave are graded separately for
  JFrog (inventory-based, includes July 7) vs rubyhack.ai/Nightingale
  (report timeline ends June 18; July 7 not described).

## Schema backfill 2026-09-29

Transformed by `temp/backfill_w3.py`.

- record_kind: `eval_candidate` (one record per candidate
  benchmark/operator assessed as the possible artifact source).
- fingerprint: sha256 of `name` (candidate name, unique across the 9 rows).
- @timestamp: sentinel `1970-01-01T00:00:00Z`,
  `labels.timestamp_source = "fallback:no_recoverable_date"` — `date` is
  publication prose (e.g. "2025-05 (arXiv 2505.15216)"), not an event time.
- All original fields moved to labels unchanged. event.dataset =
  `separate-eval-test`.

## Merge 2026-09-29

Moved the worker-4 run log from the undated stub `data/separate-eval-test/`
into `raw/run-logs/progress.log`; stub dir removed. Log covers
2026-09-28T19:27Z–20:20Z and was read and verified before the move: same lane
("separate-eval test (worker 4)"), same research question, step entries
consistent with the sources table above (BountyBench/CVE-Bench/AutoPenBench/
Cybench sweeps, JFrog post fetch with matching SHA-256, hackerone-disclosed-
reports sweep). No contradictions found. File force-added (`*.log` is
gitignored repo-wide; this is a curated lane run log, not a build artifact).
