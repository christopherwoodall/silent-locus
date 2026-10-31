# STATE — committer continuation lane, continuous hunt round 20261031

- Lane dir: `data/lanes/continuous-hunt-20261031/raw/committer/`
- Parent context: meta fleet committer result (reports/sniffer-meta-20261031/REPORT.md §M2;
  raw data/lanes/sniffer-meta-20261031/raw/committer-rerun/): completed lanes 90 commits
  (Copilot 30 + Claude-footer 30 + Devin 30); bot-type authors 5/90, all one Devin
  integration account; committer type User on all 30 Devin rows (web-flow mediated).
  Codex, PR, and phrase lanes were UNMEASURED.
- This lane: follow up. Other vendors' integration bots, self-declared agent accounts as
  committer, co-author footer patterns beyond measured lanes.
- Rules: existing gh CLI auth only, read-only GET, never POST, never fresh login.
  Pace: 60 s sleep between search calls (starts >60 s apart). STOP on any 403 /
  secondary-rate-limit response; no retry in a loop; remaining queries stay UNMEASURED.
  No commit, no push. No Factum writes (stage only). No touch of data/records/ or
  data/.local/factum.db (so a direct Factum DB novelty check is NOT done by this lane;
  flagged as an open item for the parent). No human handles in prose; bot/agent account
  names only when self-declared or commit authorship. Signed values, tokens, query
  strings never in FINDINGS.md.
- Pre-run check 2026-10-31T18:19Z: gh auth OK (account on file, existing auth only);
  search bucket 30/30 remaining, core 4996/5000. Last guard firing in the prior lane was
  2026-10-31T16:11:32Z, ~2 h before this run.

## Planned query order (all --limit 30, page 1 only)

Pass 1 — meta follow-ups (unmeasured in meta fleet):
1. commits-codex — `Co-Authored-By: Codex`
2. prs-claudecode — `Generated with Claude Code type:pr` (+ --include-prs; fixed flag)
3. prs-agent-harness — `agent harness type:pr` (+ --include-prs)

Pass 2 — new vendor footer shapes:
4. commits-cursor — `Co-Authored-By: Cursor`
5. commits-jules — `Co-Authored-By: Jules`
6. commits-gemini — `Co-Authored-By: Gemini`
7. commits-aider — `Co-Authored-By: Aider`
8. commits-codex-openai — `Co-Authored-By: OpenAI Codex` (variant footer shape)

Pass 3 — self-declared agent account as author:
9. commits-copilot-bot — author-qualifier query for the Copilot bot account

Null-slice rule: a slice returning 0 rows gets ONE narrower second pass (different
vendor, footer shape, or repo slice) before it is closed as an honest null.

## Run timeline (UTC; CDT = UTC − 5 h)

| # | Call | Start (UTC) | Result |
|---|------|-------------|--------|
| 1 | commits-codex | 18:20:06 | OK, 30 rows |
| 2 | prs-claudecode | 18:21:08 | OK, 30 rows (fixed flag works) |
| 3 | prs-agent-harness | 18:22:13 | OK, 30 rows |
| 4 | commits-cursor | 18:23:17 | OK, 30 rows |
| 5 | commits-jules | 18:24:20 | OK, 30 rows |
| 6 | commits-gemini | 18:25:23 | OK, 30 rows (29 distinct commits) |
| 7 | commits-aider | 18:26:26 | OK, 30 rows |
| 8 | commits-codex-openai | 18:27:28 | OK, 30 rows |
| 9 | commits-copilot-bot | 18:28:31 | REJECTED as invalid (qualifier-only query); not a guard |
| 10 | commits-copilot-bot2 (corrected second pass) | 18:29:23 | OK, 30 rows (qualifier did not restrict) |

- No rate guard fired at any point in this lane. No STOPPED.txt (nothing stopped
  by a guard). Search starts 52–65 s apart, all above the 45 s floor.
- All 20 capture/error hashes verify (`sha256sum -c` clean).

## What is done

- [x] Pre-run rate check + prior-lane review.
- [x] Pass 1 (3 queries: Codex footer + 2 fixed PR lanes).
- [x] Pass 2 (5 queries: Cursor, Jules, Gemini, Aider, OpenAI Codex footers).
- [x] Pass 3 (1 query + 1 corrected second pass: Copilot-bot author).
- [x] Per-lane author-type counts with denominators + footer presence from bytes.
- [x] FINDINGS.md.
- [x] No commit, no push from this lane (parent owns Git).
- [ ] Direct Factum novelty check — NOT done by this lane (no-touch constraint);
      open item for the parent (see FINDINGS.md §5, §7 Q1).
- [ ] Meta 20-phrase pass — NOT run by this lane; remains UNMEASURED.
