# FINDINGS — unmeasured-leftovers lane, continuous hunt 20261031

- Grade basis: OBSERVED means first-hand bytes in the captures below.
  Everything else is SECONDARY by default. No NEW claim is made here.
- Window: November 2025 onward. In-window counts are given per item
  where staged dates allow them. Pre-window rows are reported, not
  dropped, and are excluded from in-window counts.
- Counting rule, stated plainly: `gh search` returns at most the
  requested limit per call and prints no total in this output shape.
  Every count below is "N returned of 30 requested, page 1" — never a
  total. A capped page is never cited as a total.
- Rule applied throughout: a co-author footer proves assisted
  authorship, NOT standalone agent authorship. Standalone agent
  authorship needs a Bot/App-type account in the author or committer
  field itself.
- Human account handles are not named in this prose. Bot/agent account
  names appear only where the API returns them as author (Bot type).
  Full raw values stay in the capture files. No signed values, tokens,
  or query strings appear in this file.
- No Factum writes. No POST, no login, no sessions. Package repos and
  Docker Hub out. No Transluce submissions.

## VERY-interesting flags

None. No genuinely new agent or swarm behavior and no new agent
infrastructure with first-hand evidence surfaced in this lane. The
most notable measurement is the Codex concentration in section 2:
it narrows, rather than extends, what the Codex lane can support.

## 1. Recovered unmeasured set (exact)

Recovered from the sniffer-sweep meta fleet: `STOPPED.txt` and
`STATE.md` and `FINDINGS.md` §4 in
`data/lanes/sniffer-meta-20261031/raw/committer-rerun/`, plus the
query shapes in that lane's `run-rerun.sh`. All 23 items recovered
exactly, no partial recovery needed:

- 1 Codex commit lane: `gh search commits "Co-Authored-By: Codex"`,
  limit 30. Failed twice before (original sweep run and the meta
  re-run, both HTTP 403 secondary rate limit).
- 2 PR lanes with the recorded fix applied (the original failure was
  the invalid `--type pr` flag; the fix is the `type:pr` qualifier
  plus `--include-prs`):
  - `gh search issues "Generated with Claude Code type:pr"`
  - `gh search issues "agent harness type:pr"`
- 20 phrases, GitHub issue search, page 1, limit 30, in planned order:
  1. `I am GPT` — 2. `I am Codex` — 3. `I am Gemini` —
  4. `function_call` — 5. `system_capability` — 6. `browser_rules` —
  7. `coding_rules` — 8. `MCP server` — 9. `claude mcp add` —
  10. `custom_tool_call` — 11. `server_side_tool_usage_details` —
  12. `BOOTSTRAP.md` — 13. `Claude Code` —
  14. `ignore previous instructions` —
  15. `ThinkingBlock/ToolUseBlock/ToolResultBlock` —
  16. `spawn_agent` — 17. `wait_agent` — 18. `send_message` —
  19. `tool_call.arguments` — 20. `zz oai epoch` (space-separated
  tokens, as written in the meta lane's script; see its §4 note).

## 2. Codex commit lane — MEASURED (OBSERVED)

- Query: `gh search commits "Co-Authored-By: Codex" --limit 30`.
- Capture: `gh-commits-codex.json` (30/30 rows requested).
- Author type: User 30/30, Bot 0/30. Author `is_bot`: false 30/30.
- Committer type: User 30/30, Bot 0/30.
- Codex co-author footer present: 30/30 messages (lowercase footer
  form; a case-sensitive first check missed it and is corrected
  here — method note, not a data change).
- Commit-author dates: 2026-10-11 → 2026-10-31. In-window: 30/30.
- Concentration, the lane's key limit: all 30 rows come from ONE
  repository, ONE distinct commit-author name, ONE distinct GitHub
  author account, and ONE distinct committer account (committer
  differs from author on all 30 rows). This is a single-actor,
  single-repo cluster, NOT a cross-repo sample.
- Grading: assisted authorship only. Zero Bot/App-type authors and
  zero Bot-type committers, so this lane shows NO standalone agent
  account acting as committer or author. The Codex footers are
  self-declared assistant markers inside one actor's commits.
- Consequence for combined counts: completed commit lanes now cover
  120 commits (Copilot 30 + Claude-footer 30 + Devin 30 + Codex 30),
  bot-type authors 5/120, all 5 from the single Devin integration
  account reported by the meta lane. Any "5 of 120" citation must
  carry "completed lanes only; the Codex lane is a single-repo,
  single-author cluster, not a cross-repo sample" in the same
  sentence. The meta report's B7 qualifier for commits is now
  retired and replaced by this narrower qualifier.

## 3. PR lanes — MEASURED, with a shape caveat (OBSERVED counts)

The `type:pr` qualifier fix works against the live API: both calls
returned rc=0 with rows. Caveat that travels with both lanes: the
staged row shape carries NO pull-request discriminator field (keys
are author, title, url, repository, createdAt, plus body for the
first lane only). From staged bytes alone, a row cannot be
re-verified as a pull request rather than an issue; the PR status
rests on the query qualifier, not on a staged field. Report these
as "returned rows under the type:pr qualifier," not as
independently verified PRs.

### 3a. PR lane, Claude-code footer

- Query: `gh search issues "Generated with Claude Code type:pr"
  --include-prs --limit 30` (body fetched).
- Capture: `gh-prs-claudecode.json` (30/30 rows requested).
- Distinct repositories: 28. Created dates: 2025-08-27 → 2026-10-31.
  In-window: 29/30 (one pre-window row).
- Author type: User 29/30, Bot 1/30. The single Bot-type author row
  is `real-robin-ai[bot]`.
- Match-location screen (staged fields only): phrase in title 6/30,
  phrase in body 5/30. Most rows' matches live outside the staged
  title/body fields (search also matches other fields, which were
  not fetched). Do not cite these 30 rows as 30 title- or
  body-verified footer hits.
- Lists check: the Bot-type author name above returns zero hits in
  `lists/` (grep, 2026-10-31). That is a lists-only check, not a
  novelty verdict, and no NEW claim is made for this single row.
- Grading: search-return counts only. One Bot-type author row is a
  pattern match, not agent-behavior evidence on its own.

### 3b. PR lane, agent harness

- Query: `gh search issues "agent harness type:pr" --include-prs
  --limit 30` (no body fetched).
- Capture: `gh-prs-agent-harness.json` (30/30 rows requested).
- Distinct repositories: 30. Created dates: 2026-09-18 → 2026-10-31.
  In-window: 30/30.
- Author type: User 29/30, Bot 1/30. The single Bot-type author row
  is `autter-dev[bot]`.
- Match-location screen (staged fields only): phrase in title
  14/30. The other 16 rows' matches live outside the staged title
  field (body was not fetched). Do not cite these 30 rows as 30
  title-verified hits.
- Lists check: the Bot-type author name above returns zero hits in
  `lists/` (grep, 2026-10-31). Lists-only check, not a novelty
  verdict; no NEW claim is made for this single row.
- Grading: search-return counts only. One Bot-type author row is a
  pattern match, not agent-behavior evidence on its own.

## 4. Phrase pass — MEASURED, 19 of 20 with rows, 1 honest null

Issue search, page 1, limit 30 per phrase. "Rows" is returned rows
of 30 requested. "In-window" counts rows with createdAt on or after
2025-11-01. "Title-match" counts rows whose staged title contains
the phrase (case-insensitive); the phrase search matches title
plus other fields, and body was NOT fetched for this pass, so a
title-match of 0 does NOT mean the phrase is absent from the row —
it means the match lives outside the staged title field. Phrase
counts below are search-return counts, not verified phrase-in-text
counts, except where title-match is high.

| # | Phrase | Rows | In-window | Repos | Title-match | Bot-type authors |
|---|--------|------|-----------|-------|-------------|------------------|
| 1 | I am GPT | 30 | 23 | 23 | 0 | 1 |
| 2 | I am Codex | 30 | 28 | 23 | 0 | 0 |
| 3 | I am Gemini | 30 | 30 | 23 | 3 | 1 |
| 4 | function_call | 30 | 30 | 28 | 17 | 0 |
| 5 | system_capability | 11 | 9 | 10 | 0 | 0 |
| 6 | browser_rules | 8 | 6 | 4 | 0 | 0 |
| 7 | coding_rules | 30 | 30 | 4 | 1 | 28 |
| 8 | MCP server | 30 | 30 | 25 | 30 | 1 |
| 9 | claude mcp add | 30 | 30 | 29 | 9 | 0 |
| 10 | custom_tool_call | 30 | 30 | 27 | 10 | 0 |
| 11 | server_side_tool_usage_details | 14 | 14 | 10 | 1 | 5 |
| 12 | BOOTSTRAP.md | 30 | 30 | 29 | 15 | 2 |
| 13 | Claude Code | 30 | 30 | 21 | 26 | 1 |
| 14 | ignore previous instructions | 30 | 29 | 7 | 6 | 24 |
| 15 | ThinkingBlock/ToolUseBlock/ToolResultBlock | 30 | 30 | 27 | 0 | 0 |
| 16 | spawn_agent | 30 | 30 | 25 | 21 | 0 |
| 17 | wait_agent | 30 | 30 | 19 | 13 | 0 |
| 18 | send_message | 30 | 30 | 26 | 21 | 0 |
| 19 | tool_call.arguments | 30 | 27 | 28 | 4 | 1 |
| 20 | zz oai epoch | 0 | 0 | 0 | 0 | 0 |

Notes on the table:

- Phrases 1, 2, 3 (self-disclosure shapes): title-match 0, 0, and 3
  respectively. These rows are search hits, not title-verified
  self-disclosure statements. No self-disclosure finding is made
  from this pass; body text would be needed, and it was not fetched.
- Phrase 7 (coding_rules): 28 of 30 rows are Bot-type authors, but
  the Bot-type author set is a single account, and that account is
  the platform's own automation bot, not an agent account. Repo
  spread is only 4 repositories. This reads as automation-generated
  issue text, not agent behavior. Graded as automation noise, not
  a finding.
- Phrase 14 (ignore previous instructions): 24 of 30 rows are
  Bot-type authors, again a single platform-automation account,
  across only 7 repositories. Same grading: automation noise, not
  a finding.
- Phrase 11: 5 Bot-type rows across 2 bot accounts, both platform
  automation accounts. Same grading.
- Phrases 5, 6, 11 returned under the 30 limit (11, 8, 14 rows).
  Those are the returned counts for page 1 under those queries;
  no total is asserted for them.
- Phrase 8 (MCP server): title-match 30/30, all in-window. This is
  the phrase pass's cleanest title-verified set, but the phrase is
  generic product vocabulary, so it is a vocabulary count, not
  agent-behavior evidence.
- Phrase 20 (zz oai epoch): 0 rows on the issue search. Per the
  brief, one narrower second pass was run before closing it as a
  null: a code-surface search with the same token string
  (`gh search code "zz oai epoch"`, limit 30) also returned 0 rows
  (capture `phrase-20b-code.json`). Honest null on two query
  shapes (issue + code). It is NOT a zero for every zz/oai/epoch
  form — only for this token combination on these two surfaces.

## 5. Measured vs unmeasured table

| Item | Status | Evidence |
|------|--------|----------|
| Codex commit lane | MEASURED, 30/30 rows | `gh-commits-codex.json` |
| PR lane, Claude-code footer (type:pr fix) | MEASURED, 30/30 rows, shape caveat §3 | `gh-prs-claudecode.json` |
| PR lane, agent harness (type:pr fix) | MEASURED, 30/30 rows, shape caveat §3 | `gh-prs-agent-harness.json` |
| Phrases 1–19 | MEASURED, counts in §4 table | `phrase-01-*.json` … `phrase-19-*.json` |
| Phrase 20 (zz oai epoch) | MEASURED as honest null, 0 rows on 2 shapes | `phrase-20-zz-oai-epoch.json`, `phrase-20b-code.json` |
| (none remaining) | UNMEASURED: none. All 23 recovered items are measured. | — |

## 6. Rate-guard record

- No guard fired in this run. All 23 planned calls returned rc=0,
  plus the 1 second-pass call (rc=0).
- Run window: 2026-10-31T18:19:37Z–18:41:51Z (13:19:37–13:41:51 CDT).
  Starts paced 55 s sleep plus call duration, about 59 s between
  starts — longer than the 30 s minimum in the brief and longer
  than the meta re-run's ~30–33 s spacing, which failed at call 3.
- Pre-run bucket: search 30/30 remaining, core 4997/5000
  (2026-10-31T18:19:17Z). The previous guard fired
  2026-10-31T16:11:32Z, about 2 hours earlier.
- INFERENCE, not established: the Codex query succeeding here after
  failing twice under fleet traffic is consistent with the earlier
  failures being shared-bucket pressure rather than the query
  itself. One quiet-window success does not prove the mechanism.
- No `STOPPED.txt` was written in this lane (nothing stopped); the
  run log records the full run instead.

## 7. Failures

- None on the GitHub calls. All 24 calls (23 planned + 1 second
  pass) returned rc=0 with captures, provenance files, and hashes.
- One self-caught analysis error, corrected before writing this
  file: a case-sensitive footer check first reported 0 Codex
  footers; a lowercase check shows 30/30 messages carry a
  co-author footer, 30/30 of them naming Codex. The corrected
  count is the one reported in §2. The analysis scripts are kept
  in this lane so the correction is auditable.

## 8. Evidence paths (this lane only; no commit, no push)

- `data/lanes/continuous-hunt-20261031/raw/unmeasured/run-leftovers.sh`
- `data/lanes/continuous-hunt-20261031/raw/unmeasured/run.log`
- `data/lanes/continuous-hunt-20261031/raw/unmeasured/phrase-map.tsv`
- `data/lanes/continuous-hunt-20261031/raw/unmeasured/gh-commits-codex.json` (+ `.PROVENANCE.txt`, `.sha256`, `err-codex.txt` + `.sha256`)
- `data/lanes/continuous-hunt-20261031/raw/unmeasured/gh-prs-claudecode.json` (+ `.PROVENANCE.txt`, `.sha256`, `err-prs-claudecode.txt` + `.sha256`)
- `data/lanes/continuous-hunt-20261031/raw/unmeasured/gh-prs-agent-harness.json` (+ `.PROVENANCE.txt`, `.sha256`, `err-prs-agent-harness.txt` + `.sha256`)
- `data/lanes/continuous-hunt-20261031/raw/unmeasured/phrase-*.json` (20 files, each + `.PROVENANCE.txt`, `.sha256`, `.err.txt` + `.sha256`)
- `data/lanes/continuous-hunt-20261031/raw/unmeasured/phrase-20b-code.json` (second pass, + `.PROVENANCE.txt`, `.sha256`, `.err.txt` + `.sha256`)
- `data/lanes/continuous-hunt-20261031/raw/unmeasured/analyze.py`, `analyze2.py`, `analysis.txt`, `analysis2.txt`
- `data/lanes/continuous-hunt-20261031/raw/unmeasured/STATE.md`
- `data/lanes/continuous-hunt-20261031/raw/unmeasured/FINDINGS.md` (this file)

## 9. Open questions

1. Does the PR-lane row shape carry a PR discriminator anywhere
   outside the fetched fields (for example via a follow-up fetch
   of one row's record)? Until then, §3 rows stay "returned under
   the type:pr qualifier," not verified PRs.
2. Do the phrase-pass rows with title-match 0 (notably phrases 1,
   2, 5, 6, 15) match in body text or elsewhere? Body fetch would
   answer it, but that is a new call set for the coordinator, not
   this lane.
3. Is the Codex single-repo cluster's co-authorship pattern shared
   anywhere else (a second repo with the same shape)? One cluster
   does not generalize; a cross-repo check would be needed before
   any wider Codex claim.
4. Novelty legs not run here, stated plainly: no Factum exact/fuzzy
   check was run (the lane brief forbids touching
   `data/.local/factum.db`), and no Transluce snapshot check was
   run. No NEW claim is made, so no novelty leg is asserted. The
   only novelty-adjacent checks run were the `lists/` greps in §3
   (zero hits for both PR-lane bot names).
