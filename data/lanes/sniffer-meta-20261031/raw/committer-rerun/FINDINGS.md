# FINDINGS — committer-account re-run lane (partial: rate guard fired)

- Grade basis: OBSERVED = first-hand bytes in the captures below.
  Everything else is SECONDARY by default.
- Window: November 2025 onward. All 60 completed-lane commits fall in
  window (commit-author dates 2026-09-27 through 2026-10-31).
- Rule applied throughout: a co-author footer proves assisted authorship,
  NOT standalone agent authorship. Standalone agent authorship needs a
  Bot/App-type account in the author or committer field itself.
- Human account handles are not named in this prose. Bot/agent account
  names appear only where the API returns them as author/committer or a
  footer self-declares them. Full raw values stay in the capture files.
- No profile lookups were done after the guard fired. No Factum writes.
  No POST, no login, no sessions. Package repos and Docker Hub out.

## 1. Completed lanes: bot-type counts with denominators

### 1a. Claude-code-footer commit lane — OBSERVED

- Query: `gh search commits "Generated with Claude Code" --limit 30`
- Capture: `gh-commits-claudecode-footer.json` (30/30 rows requested).
- Author type: User 30/30, Bot 0/30, App 0/30. Author `is_bot`: false 30/30.
- Committer type: User 30/30, Bot 0/30. Dominant committer is the
  GitHub web-flow account (27/30); 3 distinct committers total.
- Distinct authors: 12 (handles withheld here; see capture file).
- Commit-author dates: 2026-09-27 → 2026-10-29. In-window: 30/30.
- Footer evidence (line counts across the 30 messages, not commit counts):
  - "Generated with Claude Code" marker lines: 229 lines total
    (165 with link form, 52 with emoji form, 12 plain form).
  - Claude co-author footer lines: 35 lines total, naming model
    identities `Claude Opus 4.7 (1M context)`, `Claude Opus 5.5`,
    `Claude Haiku 5.5`, all with `noreply@anthropic.com`.
  - Commits carrying at least one Claude co-author footer: 7/30.
  - Commits carrying any Claude mention: 30/30 (that is the search hit).
- Grading: assisted authorship only. Zero Bot/App-type authors and zero
  Bot-type committers, so this lane shows NO standalone agent account
  acting as committer/author. The model-name footers are self-declared
  assistant markers inside human-authored commits, not agent accounts.

### 1b. Devin commit lane — OBSERVED

- Query: `gh search commits "Co-Authored-By: Devin" --limit 30`
- Capture: `gh-commits-devin.json` (30/30 rows requested).
- Author type: Bot 5/30, User 25/30, App 0/30.
  - API quirk, recorded verbatim: the 5 Bot-type authors carry
    `is_bot: false` in the same record. Type and `is_bot` disagree;
    the count above uses `type`, the field the task names.
  - All 5 Bot-type author rows are one account:
    `devin-ai-integration[bot]`.
- Committer type: User 30/30, Bot 0/30. Single committer across all 30
  rows: the GitHub web-flow account (30/30).
- Distinct authors: 20. Distinct committers: 1.
- Commit-author dates: 2026-10-21 → 2026-10-31. In-window: 30/30.
- Footer evidence (line counts across the 30 messages):
  - Devin co-author footer lines: 404 lines total, overwhelmingly
    `Co-Authored-By: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>`
    plus a `Devin <devin@cognition.ai>` variant and a `bot_apk`
    variant from the same vendor domain.
  - Commits carrying at least one Devin co-author footer: 30/30.
- The 5 Bot-type-authored commits (sha prefix, date, committer):
  - `b947211bb607`, 2026-10-26, web-flow.
  - `da2afbf4749d`, 2026-10-27, web-flow.
  - `a4f51d05a205`, 2026-10-27, web-flow.
  - `3d5082a3fb3c`, 2026-10-30, web-flow.
  - `40c1fe171630`, 2026-10-30, web-flow.
  - Full rows (repo, message, URL) are in the capture file, keyed by sha.
- Grading: the 5 Bot-type rows are the lane's only standalone
  agent-account authorship signal (5/30 commits, 1 distinct bot
  account). Even those 5 were committed through web-flow, so they are
  GitHub-App-mediated, not independent agent commits. The other 25/30
  are assisted authorship: User author + Devin footer.
- Self-declaration bytes (verbatim from footers in the capture):
  `Co-Authored-By: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>`.

### 1c. Context: prior Copilot slice (from the sweep brief, not re-run here)

- 30 commits, 17 distinct authors, 0 bot-type authors.
- Combined completed-lane picture (Copilot + Claude-footer + Devin):
  90 commits requested, 90 rows captured, bot-type authors 5/90,
  all 5 from the single Devin integration account above.

## 2. Failed / not-attempted lanes

### 2a. Codex commit lane — FAILED, twice

- Query: `gh search commits "Co-Authored-By: Codex" --limit 30`
- Original sweep run: HTTP 403 secondary rate limit.
- This re-run: HTTP 403 secondary rate limit again, at
  2026-10-31T16:11:32Z (11:11:32 CDT), call 3 of 25.
  Error file: `err-codex.txt`; capture `gh-commits-codex.json` is 0 bytes.
- The same query failing twice, while the two preceding queries in this
  run succeeded, is consistent with (a) shared-bucket pressure from
  concurrent fleet work, or (b) this query pattern tripping the
  secondary limit. That distinction is INFERENCE, not established.
- No Codex count exists from this lane. Do not cite 0 for Codex.

### 2b. PR lanes — NOT ATTEMPTED (guard fired first)

- Original failure cause: invalid flag `--type pr` on
  `gh search issues` (confirmed in the original error files).
- Fixed commands, recorded in `run-rerun.sh` for a later window:
  - `gh search issues "Generated with Claude Code type:pr" --include-prs --limit 30 --json author,title,url,repository,createdAt,body`
  - `gh search issues "agent harness type:pr" --include-prs --limit 30 --json author,title,url,repository,createdAt`
- No PR counts exist from this lane. The fix itself is untested against
  the live API (untested because the guard stopped the run first).

## 3. Rate-guard record (exact stopping point)

- Stopping point: call 3 of 25, label `commits-codex`,
  2026-10-31T16:11:32Z (11:11:32 CDT). Full record in `STOPPED.txt`.
- Pacing actually used: 20 s sleep between calls plus call duration,
  i.e. ~30–33 s between search starts (call 1 at 16:10:23Z, call 2 at
  16:10:56Z, call 3 at 16:11:26Z). Pacing at ~1 search per 10 s was met
  and exceeded, and the guard still fired.
- Pre-run bucket state: search 30/30 remaining, core 4969/5000. The
  guard therefore is NOT the published 30/min search quota; it is the
  secondary limit, which GitHub does not publish as a number.
- Response text (verbatim, from `err-codex.txt`): "HTTP 403: You have
  exceeded a secondary rate limit. Please wait a few minutes before you
  try again."
- No retry was attempted after the guard fired, per orders. No further
  GitHub calls were made by this lane after 16:11:32Z.

## 4. Unswept-phrase pass — NOT RUN (0 of 20)

- The phrase pass never started (guard fired at call 3, before pass 2).
  These phrases remain unswept. No hit counts exist for them; nothing
  here is a zero.
- Phrases, in planned search order (page 1 only, `--limit 30`, issue
  search, as written in `run-rerun.sh`):
  1. `I am GPT` — 2. `I am Codex` — 3. `I am Gemini` —
  4. `function_call` — 5. `system_capability` — 6. `browser_rules` —
  7. `coding_rules` — 8. `MCP server` — 9. `claude mcp add` —
  10. `custom_tool_call` — 11. `server_side_tool_usage_details` —
  12. `BOOTSTRAP.md` — 13. `Claude Code` —
  14. `ignore previous instructions` —
  15. `ThinkingBlock/ToolUseBlock/ToolResultBlock` —
  16. `spawn_agent` — 17. `wait_agent` — 18. `send_message` —
  19. `tool_call.arguments` — 20. `zz oai epoch`.
- Note on phrase 20: the sweep brief lists it as "zz/oai/epoch-nonce
  tokens". The script searches it as space-separated tokens
  `zz oai epoch` (GitHub search tokenizes on slashes; the normalized
  form is recorded here so a later run can reproduce or correct it).
  Phrase 15 is likewise searched as one quoted string; GitHub's
  tokenizer, not this lane, decides how the slashes split.
- Note on denominators for a later run: `gh search` returns at most
  the requested limit per call and does not print a total in this
  output shape, so a later run must report "N returned of 30
  requested, page 1" and must never cite a capped page as a total.

## 5. Evidence paths (this lane only; coordinator commits)

- `data/lanes/sniffer-meta-20261031/raw/committer-rerun/run-rerun.sh`
- `data/lanes/sniffer-meta-20261031/raw/committer-rerun/run.log`
- `data/lanes/sniffer-meta-20261031/raw/committer-rerun/STOPPED.txt`
- `data/lanes/sniffer-meta-20261031/raw/committer-rerun/gh-commits-claudecode-footer.json` (+ `.PROVENANCE.txt`, `.sha256`)
- `data/lanes/sniffer-meta-20261031/raw/committer-rerun/gh-commits-devin.json` (+ `.PROVENANCE.txt`, `.sha256`)
- `data/lanes/sniffer-meta-20261031/raw/committer-rerun/gh-commits-codex.json` (0 bytes, failed) (+ provenance note, `err-codex.txt` + `.sha256`)
- `data/lanes/sniffer-meta-20261031/raw/committer-rerun/STATE.md`
- `data/lanes/sniffer-meta-20261031/raw/committer-rerun/FINDINGS.md` (this file)
- Prior-lane inputs read (not modified):
  `data/lanes/sniffer-sweep-20261031/raw/committer-accounts/run.sh` and its
  `err-*.txt` files.

## 6. Open questions (for the coordinator / operator)

1. Is the secondary-limit pressure coming from concurrent fleet search
   traffic on the shared token, or is the Codex query itself the
   trigger? A single probe in a quiet window would separate these, but
   this lane did not probe after the guard, per orders.
2. When should the Codex lane, the two PR lanes, and the 20-phrase pass
   be re-attempted — next quiet window, and with what pacing (longer
   than 30 s between starts, given this run's failure at that pace)?
3. Does the `devin-ai-integration[bot]` type-vs-`is_bot` disagreement
   affect the sweep's bot-count rule (count by `type`, as done here)?
4. The original sweep's truncated `gh-commits-claude.json` (8,192 bytes,
   cut mid-message, no matching error file or `run.sh` entry) was not
   investigated — it is outside this lane's brief and may belong to a
   different probe. Flagged, not touched.
