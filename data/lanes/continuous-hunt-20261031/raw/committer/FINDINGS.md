# FINDINGS — committer continuation lane, continuous hunt round 20261031

- Operator: BigSexyWarlock69. Window: November 2025 onward.
- Parent context: meta fleet committer result (REPORT.md §M2): completed lanes 90 commits
  (Copilot 30 + Claude-footer 30 + Devin 30); bot-type authors 5 of 90, all from one
  Devin integration account; committer type User on all 30 Devin rows (web-flow mediated).
  Codex, PR, and phrase lanes were UNMEASURED there. This lane measures the Codex and
  PR lanes and adds new vendor footer lanes.
- Grade basis: OBSERVED = first-hand bytes in the captures below. SECONDARY by default
  for agent identity. A co-author footer proves assisted authorship, NOT standalone
  agent authorship. Standalone agent authorship needs a Bot/App-type account in the
  author or committer field itself, acting without web-flow mediation.
- Human account handles are not named in this prose. Bot/agent account names appear
  only where the API returns them as author/committer or a footer self-declares them.
  Full raw values stay in the capture files. Signed values, tokens, and query strings
  do not appear in this file.
- No commit, no push from this lane. No Factum writes. No POST, no fresh login.
  Package repos and Docker Hub out. No Shodan.

## ALERT BAR — VERY-interesting flags: NONE

- No verified standalone agent committer was found. Every Bot-type author row in
  every lane below has a User-type committer (web-flow in all but 3 rows), so every
  bot-authored row is GitHub-App/web-flow mediated, not an independent agent commit.
- Bot-type committers: 0 of 210 commit rows in this lane. App-type authors or
  committers: 0 of 210.
- Closest signal (not a standalone commit, documented normally): a self-named
  agent bot account appears as author on one Gemini-lane commit carrying repeated
  Gemini-model footers — but its committer is web-flow, so it is mediated, same
  class as the meta fleet's Devin finding. See §2c.

## 1. Run record

- 10 searches, all read-only GET via existing gh CLI auth, 2026-10-31T18:20–18:29Z.
  Search starts 52–65 s apart (all above the 45 s floor). No rate guard fired.
  Pre-run bucket: search 30/30, core 4996/5000. Post-run: no guard event, so no
  STOPPED.txt was written; nothing is UNMEASURED by a guard in this lane.
- All captures carry `.PROVENANCE.txt` + `.sha256`; all 20 hashes verify.
- Page-1 slices only (`--limit 30`). A capped page is not a total. Counts below are
  "N of 30 rows returned", never totals.
- The 20 unswept phrases from the meta lane were NOT run here (this lane's brief is
  committer follow-up, not the phrase pass). They remain UNMEASURED unless another
  lane runs them. No zero is cited for them.

## 2. Counts table — commit lanes (author type / committer type, with denominators)

| Lane (search text) | Rows | Author Bot | Author User | Committer Bot | Committer User | Distinct authors | Distinct commits | In-window |
|---|---|---|---|---|---|---|---|---|
| Codex footer | 30 | 0 | 30 | 0 | 30 | 1 | 30 | 30/30 |
| Cursor footer | 30 | 0 | 30 | 0 | 30 | 17 | 30 | 30/30 |
| Jules footer | 30 | 0 | 30 | 0 | 30 | 10 | 30 | 30/30 |
| Gemini footer | 30 | 5 | 25 | 0 | 30 | 29 | 29 | 30/30 rows |
| Aider footer | 30 | 1 | 29 | 0 | 30 | 5 | 30 | 30/30 |
| OpenAI Codex footer | 30 | 1 | 29 | 0 | 30 | 17 | 30 | 30/30 |
| Copilot-bot author (corrected query) | 30 | 1 | 29 | 0 | 30 | 15 | 30 | 30/30 |
| **This lane, commit rows** | **210** | **8** | **202** | **0** | **210** | — | **209** | — |

- Committer detail: web-flow accounts for 177 of 180 rows in the six footer lanes
  (30 + 30 + 30 + 27 + 30 + 30) and 30 of 30 in the Copilot-bot lane. The only
  non-web-flow committers are 3 User-type committers in the Gemini lane.
- Combined with the meta fleet's completed lanes (90 commits, 5 bot-type authors):
  300 commit rows measured across both lanes, 13 bot-type author rows — but the two
  runs used different queries and page-1 slices, so the combined figure is a
  measurement sum, not a population total. Do not cite it as a rate.

### 2a. Codex footer lane — OBSERVED, assisted only

- Query text: Codex co-author footer. 30 of 30 rows, author User 30/30, Bot 0/30.
  Committer web-flow 30/30. Commit-author dates 2026-10-11 → 2026-10-31.
- Concentration caveat (page-1 slice, not a population claim): all 30 rows come
  from ONE repo and ONE distinct author. The Codex page-1 slice is a single-repo
  cluster, not a broad sample. No standalone agent account acts as committer here.
- Footer presence verified in message bytes: 30 of 30 rows carry a Codex footer
  (codex@openai.com address form).

### 2b. Cursor, Jules, Aider lanes — OBSERVED, assisted only, new vendor shapes

- Cursor footer: 30 rows, User 30/30, Bot 0/30, web-flow 30/30, 17 distinct authors,
  dates 2026-10-17 → 2026-10-31. Footer verified: 30 of 30 rows carry a cursoragent
  footer (cursor.com address form). No bot-type author or committer.
- Jules footer: 30 rows, User 30/30, Bot 0/30, web-flow 30/30, 10 distinct authors,
  dates 2026-09-26 → 2026-10-30. Search-match caveat: the query matched the token
  inside the vendor bot's account name, not a display name "Jules". Verified footer
  shape: 30 of 30 rows carry a google-labs-jules bot footer (508 footer lines
  across the lane), and 30 of 30 rows carry at least one bot-suffixed footer.
  Assisted authorship only: every author is User, every committer web-flow.
- Aider footer: 30 rows, User 29/30, Bot 1/30, web-flow 30/30, 5 distinct authors,
  dates 2026-10-03 → 2026-10-30. Footer verified: 29 of 30 rows carry an aider footer
  (aider.chat address form). Concentration caveat: 26 of 30 rows come from one repo.
  The single Bot-type author row is github-actions[bot] (2026-10-03, web-flow
  committer) — CI automation, not an agent account, and not an independent commit.

### 2c. Gemini footer lane — OBSERVED; the lane's only new agent-account names

- 30 rows, author Bot 5/30, User 25/30; committer User 30/30 (web-flow 27/30, other
  User committers 3/30). 29 distinct authors, 29 distinct commits: one commit sha
  appears twice in the 30 rows, so row counts and commit counts differ by one.
  Dates 2026-07-02 → 2026-10-31, all in window.
- Bot-type author rows (5 rows, 4 distinct accounts, all web-flow committed):
  - Copilot (2 rows, same sha — the duplicate): message is a Gemini-content fix
    carrying a copilot-swe-agent bot footer plus a User co-author footer. The row
    carries NO Gemini footer in message bytes; its search hit came from Gemini
    text elsewhere in the message. Cross-vendor assisted authorship, not a Gemini
    agent commit.
  - vitruvian-wren-agent[bot] (1 row, 2026-10-31): self-named agent bot account
    as author, message carrying repeated "Gemini 4 Argon" model footers
    (noreply@google.com form). Closest signal in this lane — but committer is
    web-flow, so it is mediated, not standalone.
  - synlynk-synlynk-pm[bot] (1 row, 2026-10-25): vendor integration bot account
    as author, message carrying repeated "Agy (Gemini)" footers (antigravity.dev
    form). No Gemini-named footer in the strict address sense; the Gemini link
    is the footer display name. Web-flow committed: mediated.
  - models-bot[bot] (1 row, 2026-10-30): bot account as author, message carrying
    Cursor and vendor-model-bot footers. No Gemini footer in message bytes; its
    search hit came from Gemini text elsewhere. Web-flow committed: mediated.
- Same API quirk as the meta Devin lane, recorded verbatim: all 5 Bot-type author
  records carry `is_bot: false` in the same record. Type and `is_bot` disagree;
  counts here use `type`, the field the brief names.
- Other verified footer shapes in this lane (message bytes): gemini-code-assist
  bot footer on 8 of 30 rows; "Gemini 4 Argon" model footer on 2 of 30 rows;
  any bot-suffixed footer on 9 of 30 rows. Only 12 of 30 rows carry a literal
  "Co-Authored-By: Gemini" string — GitHub tokenizes the query, so the search
  hit is NOT proof of that exact footer shape. Footer presence above is verified
  from message bytes, not assumed from the hit.
- Novelty status for the three new bot account names: they do not appear in the
  meta committer lane captures or in the local lists/ checks (§5). A direct
  Factum check was NOT done by this lane (no-touch constraint, §5), so they are
  reported as "not seen in checked sources", not as established NEW.

### 2d. OpenAI Codex footer lane — OBSERVED, assisted only, new model footer shapes

- 30 rows, User 29/30, Bot 1/30, web-flow 30/30, 17 distinct authors,
  dates 2026-09-19 → 2026-10-29.
- The single Bot-type author row is dependabot[bot] (2026-10-13, web-flow
  committer) — dependency automation, not an agent account, not an independent
  commit.
- Footer verified: 30 of 30 rows carry a Codex-named footer. Two address forms:
  codex@openai.com (17 of 30 rows) and noreply@openai.com with Codex-named display
  forms (the remaining rows). New model-qualified footer shapes in message bytes:
  "OpenAI Codex" (dominant form) plus openai-codex model variants (gpt-6-luna,
  gpt-6-sol, gpt-6.1-sol forms). Model identity is self-declared in footers:
  SECONDARY, not independently verified.

### 2e. Copilot-bot author lane — OBSERVED, with a query caveat

- First attempt (qualifier-only query) was REJECTED by the API as invalid:
  qualifier-only commit searches are not allowed. This was a query error, not a
  rate guard, and not a null. No retry in a loop; one corrected second pass was
  run with search text added (see provenance file for the exact corrected query).
- Corrected query: 30 rows, author Bot 1/30, User 29/30; committer web-flow 30/30;
  15 distinct authors; dates 2026-10-25 → 2026-10-30; 30 distinct commits.
- Query caveat, stated plainly: the author qualifier did NOT restrict the result
  set to the bot account (29 of 30 rows are User-authored). The observed set is
  therefore a "Copilot"-text match slice, not a bot-author census. Do not cite
  1/30 as a Copilot authorship rate.
- The single Bot-type author row is Copilot (2026-10-30, web-flow committer),
  carrying repeated "Copilot App" footers plus a User co-author footer. Mediated
  by web-flow: not a standalone agent commit. Only 2 of 30 rows in this slice
  carry a copilot-swe-agent bot footer.

## 3. Counts table — PR lanes (fixed flag, first live test)

| Lane (search text) | Rows | Author Bot | Author User | Distinct authors | In-window |
|---|---|---|---|---|---|
| Claude Code PRs | 30 | 1 | 29 | 28 | 29/30 |
| Agent harness PRs | 30 | 1 | 29 | 28 | 30/30 |

- The fixed flag works: both PR queries returned rows live. The meta lane's
  original failure (invalid flag) is resolved by the qualifier + include-prs form.
- PR caveat: a PR has no committer field, so a bot-type PR author is NOT a
  committer finding. PR author type must never be cited as committer evidence.
- Claude Code PR lane: the single Bot-type author row is real-robin-ai[bot],
  dated 2025-08-27 — OUTSIDE the window. In-window bot-type PR authors: 0 of 29.
  Text-match caveat: only 8 of 30 rows carry the marker in title or body
  (6 title, 5 body, overlap 3); the rest matched on other searched text
  (GitHub issue search also matches comments). This lane is a text-match slice,
  not a footer-verified lane.
- Agent harness PR lane: the single Bot-type author row is utter-dev[bot]
  (2026-10-28, in-window), on a dependency-update title ("Update .../Harness-Agent").
  Title shape indicates dependency automation, not agent authorship. The other
  29 rows are harness-catalog/addition PR titles (harness listings, presets, and
  evals), i.e. PRs ABOUT harnesses, not PRs BY agents. No agent-author signal
  beyond the one dependency-bot row.

## 4. What did NOT change vs the meta result

- No lane shows a Bot/App-type committer (0 of 210 commit rows here; 0 in the
  meta completed lanes' committer fields as reported).
- No lane shows a standalone agent commit: every bot-authored row is web-flow
  committed (207 of 210 rows web-flow overall; the 3 exceptions are User
  committers in the Gemini lane, on User-authored rows).
- Co-author footers remain the dominant signal class: vendor/model footers
  (Cursor, Jules, Aider, Codex, Gemini variants) appear on User-authored,
  web-flow-committed rows. That is assisted authorship, same as the meta lanes.
- The Devin single-vendor pattern generalizes in one respect: bot-type authors
  are rare (8 of 210 rows here) and each lane's bot rows trace to automation or
  integration accounts (CI, dependency, vendor integration, model-assist bots),
  not to independent agent accounts acting as committer.

## 5. Novelty checks performed (and the one not performed)

- Checked: meta committer lane captures + FINDINGS (no Cursor/Jules/Gemini/Aider/
  OpenAI-Codex footer lanes, no vitruvian/synlynk/models-bot author rows);
  local lists/ greps for the candidate names (only unrelated hits: "Cursor" as a
  wordlist term from an unrelated source, "jules" as an unrelated agent-board
  domain). Exclusion list respected: nothing here re-reports the broad egress
  hunt, HN lane, deep-dive, forum bypass hunt, prcomment ledger, AIID ingest,
  o-pattern family, or sniffer sweep + meta findings as new; the meta findings
  are cited above as prior art only.
- NOT performed by this lane: direct Factum exact + fuzzy check. The brief
  forbids this lane from touching data/records/ and data/.local/factum.db, so
  that check is an open item for the parent, not a skipped step silently
  absorbed. Consequence: no candidate in this file is claimed as established
  NEW. Transluce snapshot check likewise not run by this lane (no Transluce
  submissions were made, per constraints).

## 6. Failures

- Qualifier-only author query rejected as invalid (API error, not a guard).
  Corrected with one second pass; the corrected query did not restrict as
  expected (§2e). Neither failure is a rate-guard event.
- Repository field note (method, for the next lane): `gh search commits --json`
  returns the repo under `repository.fullName`, not `nameWithOwner`. Repo
  distributions in this file use `fullName`. The earlier per-lane repo counts
  derived from `nameWithOwner` were null and are not cited.
- No other failures. No guard fired at any point in this lane.

## 7. Open questions (for the parent)

1. Factum exact + fuzzy check for vitruvian-wren-agent[bot],
   synlynk-synlynk-pm[bot], models-bot[bot], and the new footer shapes
   (google-labs-jules bot footer, gemini-code-assist bot footer, "Gemini 4
   Argon", "Agy (Gemini)", openai-codex model variants) — pending parent-side
   check before any NEW claim.
2. Do the 20 unswept meta phrases get a lane, or stay UNMEASURED? This lane did
   not run them.
3. Is a bot-authored, web-flow-committed row (e.g. the vitruvian row) worth a
   deeper per-account pull (its other commits, its app/installation shape), or
   does the web-flow mediation close it? This lane takes no position beyond
   reporting the mediation.
4. The author-qualifier behavior (§2e): does GitHub commit search restrict on
   git-author rather than the linked GitHub user, or did the CLI drop the
   qualifier? A single probe with a known bot author + distinct search text
   could settle it, but it was out of this lane's query budget shape.
5. Codex page-1 concentration (1 repo / 1 author): is a second Codex page
   (offset) worth pulling to test whether the concentration is a ranking
   artifact? Page 1 alone cannot answer it.

## Evidence

- Captures (each with `.PROVENANCE.txt` + `.sha256`, all hashes verify):
  gh-commits-codex.json, gh-prs-claudecode.json, gh-prs-agent-harness.json,
  gh-commits-cursor.json, gh-commits-jules.json, gh-commits-gemini.json,
  gh-commits-aider.json, gh-commits-codex-openai.json,
  gh-commits-copilot-bot.json (0 bytes, rejected query + error file),
  gh-commits-copilot-bot2.json (corrected second pass).
- Run script + log: run-continuation.sh, run.log. State: STATE.md.
- All files in data/lanes/continuous-hunt-20261031/raw/committer/.
