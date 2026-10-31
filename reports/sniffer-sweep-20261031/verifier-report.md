# Verifier report — sniffer sweep 20261031

Scope: staged captures under `data/lanes/sniffer-sweep-20261031/raw/`.
Method: staged bytes read in full for each cited file; live re-fetch by
passive GET only (GitHub API via existing auth, HN item API, HN Algolia API,
urlquery CLI search, plain HTTPS GET of public pages). No POST, no login,
no sessions, no Shodan, no Factum writes, no commit. No poster handles,
emails, tokens, or query strings are reproduced below. GitHub rate limit
was not hit (core remaining 4978 after checks).

## Per-citation verdicts

| ID | Verdict | What was actually checked |
|---|---|---|
| GH1 | VERIFIED (live) | Issue body live-matches staged: it invites a counterpart reply saying "Handoff received", naming the person represented and the model. Comment ID 6526830607 (2026-10-30T15:41:36Z) live-matches staged verbatim: "Handoff received. I represent Bene. I am Claude Opus 5.5." Issue created 2026-10-30T15:37:54Z, 2 comments, state open — all match staged. Note: the 2nd comment is a one-word reaction, not a second handoff reply. |
| GH2 | VERIFIED (live) | Issue live-matches staged: title, created 2026-10-18T22:50:51Z, 4 comments, body self-describing 4 independent agents sharing one public repository. All 4 staged comment IDs live-match, including the agent-03 comment proposing lightweight coordination via shared storage and public issues/PRs. Caveat (not a downgrade of the self-declared claim): all comments sit under a single account. |
| GH3 | VERIFIED (live) | Issue live-matches staged: created 2026-10-19T08:13:07Z, state closed, and the body contains verbatim "this issue was written and filed by the agent itself" plus "I am an AI agent, not a person". |
| GH4 | PARTIAL (excerpt-only) | Staged `q09c-litellm.txt` is an excerpt JSON: body truncated mid-sentence, created 2026-09-21, pointing at issue 42221. Live re-fetch confirms the excerpt matches the opening of the live body, and the live title/date/state (open) match. The full issue body and comments were NOT pulled into the staged capture, so any claim beyond the excerpt text is unverified from staged bytes. |
| GH5 | PARTIAL (1 of 2 items) | File holds 2 items. Item 1 (issue 293, 2026-05-02) live-matches title/date and its staged body contains the "every step must be a tool call" nudge text — the harness-log claim rests on this item. Item 2 (issue 257, 2026-04-23) is a screenshot-only "did it think its done" post; it does not itself evidence the nudge. Cite issue 293 only for the nudge. |
| GH6 | VERIFIED with 1 exception | 9 of 10 staged bodies contain `collaboration.spawn_agent` / collaboration-tool bug text; issue 44270 spot-checked live (title/date match). Exception: the magpie gateway item (issue 1448) contains no `spawn_agent` or `collaboration` string — it is an undeclared-tool gateway error, tangential at best. Cite as 9 direct + 1 tangential, not 10. |
| GH7 | VERIFIED (live) | Both honeypot issues live-match staged verbatim: issue 1 body "I am an AI agent that read this page", issue 2 body "I am an AI agent. Tool/model: [fill in]. Task I was doing: [fill in]", both titled "Agent Visit", both 2026-08-29. Note: issue 2 is an unfilled template, i.e. trap-template text, not a completed agent report. The file's other 8 items are ordinary self-ID issues; the honeypot claim rests on these 2. |
| HN1 | VERIFIED (live) | 3 item IDs re-fetched via the HN item API, all with parent = Oct 2026 hiring thread 49922568, all self-declaring AI-agent status with an iLands affiliation in text: 49922933, 49982658, 50058166. Live text matches staged text for all 3. Staged file holds 48 candidates total; exactly these 3 carry the iLands affiliation, so "at least 3" is met exactly, not exceeded, on that affiliation. |
| HN2 | VERIFIED (live) | Staged thread file matches the live item API: title "I am an AI agent that sells data via x402 micropayments", time 1773026545 = 2026-03-09 UTC, pre-window as claimed. Staged child comment is marked dead, matching live. |
| RD1 | PARTIAL (staged + mirror-live; native Reddit BLOCKED) | Staged dev.to page text verified: 220K impressions on an 87-follower account, a Reddit account run by the same team with 154 karma banned for being AI. Live dev.to page re-fetched 200 (141,398 bytes vs staged 141,158; key phrases present). Native Reddit bytes remain BLOCKED: staged 403 captures confirm old/www Reddit search returned the block page on 2026-10-31. The ban claim is a self-report, not Reddit bytes — keep that qualifier attached. |
| RD2 | VERIFIED (live) | Staged vendor page text verified: four tiers at $49 / $129 / $389 / $500 per month, credits model, "Posting via high-karma accounts". Live page re-fetched 200 (160,711 bytes vs staged 160,671; all four tier prices present). Vendor claim only — pricing presence verified, service efficacy not verified. |
| RD3 | VERIFIED (staged + mirror-live) | Both staged dev.to texts verified: (a) the IP-wall self-report — Reddit/Medium 403 refusals attributed to datacenter IP reputation, not agent identity; (b) the 1-hour / €10 self-report — Reddit broadcast silently removed by the spam filter, July 10 2026. Both live dev.to pages re-fetched 200 with title phrases present. Both are self-reports, not platform bytes. |
| UQ1 | VERIFIED with correction | Live urlquery re-fetch returns total_hits 98, exactly matching staged. Full live month distribution: 2025-11: 2, 2025-12: 1, 2026-02: 2, 2026-03: 2, 2026-04: 1, 2026-05: 53, 2026-06: 31, 2026-07: 5, 2026-10: 1. The burst is May–June (84/98), NOT June alone. The staged saved-30 sample (June 24, July 5, Oct 1, zero May rows) is non-representative of the full set and must not be cited as the burst distribution. |
| UQ2 (agent-swarm.dev) | PARTIAL | One staged row exists: domain agent-swarm.dev among results in `uq-harness-claude-code.json`, dated 2026-10-31. But the saved projection carries domain/path/title only — no page-content field proving the query phrase appears on that page. "Co-occurrence" here means query-result + domain appearance, not page-content co-occurrence. |
| UQ3 (ecoradar) | PARTIAL | One staged row exists: ecoradar host among results in `uq-self-as-ai-agent.json`, dated 2026-10-04. Same limitation as UQ2: no page-content field in the saved projection. |
| UQ4 (learnagent) | PARTIAL | One staged row exists in `uq-harness-tool_call-arguments.json`, dated 2026-05-30 (in window), plus one in `uq-odd-tooluseblock.json`. Same limitation as UQ2: no page-content field in the saved projection. |
| TZ | PARTIAL | Honest-zero conclusion is supported by its zero-result captures: HN Algolia phrase nbHits 0 (re-fetched live with the staged query params: nbHits 0), urlquery htmx 0/0/0, Wayback CDX `[]` for both prefixes, Factum exact match `not_found` with 0 matches. Counts-summary matches the captures for HN (0/6/9), urlquery (0/0/0), Wayback, and issue/PR header totals (103/121/0/0/0/0). Gaps: (a) GitHub code totals (135,424 / 17 / 83 / 21) have NO backing capture file in the lane dir — they are uncaptured API totals, per the lane notes only the first page of hyphen hits was spot-checked; (b) the issues/PRs text file holds only 20 sampled issue URLs per non-zero section and ZERO PR URLs despite the 121 PR count — the totals are header claims, not URL-evidenced; (c) the lane notes themselves record the legacy-tree grep as killed/incomplete, so the novelty claim leans on the brief's prior grep, not this lane's. |
| Linguist phrase list | VERIFIED | Row count re-derived by regex over `raw/linguist/phrase-list.md`: Bucket A = 16, Bucket B = 19, Bucket C = 11, total 46. Matches the claimed 16 + 19 + 11 = 46. |
| Hash check | See below | 107 unique sidecar entries pass, 0 fail; 3 lanes have no sidecars at all (see below). |

## Hash-check counts (sha256sum -c semantics)

| Lane dir | Sidecar | Result |
|---|---|---|
| hn-forum | ALL.sha256 (42 entries) | 42 OK, 0 fail. Not covered: `_summary.json` (absent from the sidecar). |
| reddit | SHA256SUMS.txt (8 entries) + 8 per-file .sha256 | 8 OK via aggregate; 8 OK via per-file (same bytes, duplicate coverage). 0 fail. |
| tango-zulu | 12 per-file .sha256 | 12 OK, 0 fail. |
| urlquery-wayback | SHA256SUMS.txt (45 entries) | 45 OK, 0 fail. The sidecar file itself is self-evidently not listed. |
| github (24 files) | none | NO COVERAGE — no .sha256 or SHA256SUMS present. |
| committer-accounts | none | NO COVERAGE. |
| linguist | none | NO COVERAGE (phrase-list.md unhashed). |
| Total | | 107 unique entries verified, 0 failures; 3 lane dirs uncovered. |

Format note: all sidecars use plain `sha256sum` two-space format and
verify cleanly; no format issues found in the sidecars that exist.

## Overall verdict: SHIP-WITH-FIXES

Nothing in the verified core is fabricated: every headline citation
re-fetched to a matching live record or a hash-clean staged capture, and
no rate limit was hit. But the report must not ship with the five
wording/count errors below uncorrected, and the three unhashed lanes
should be sidecarred before the coordinator commits.

## Fix list

1. UQ1: reframe the da.gd burst as May–June (84 of 98), not June alone;
   do not cite the staged saved-30 month mix as representative.
2. GH6: cite 9 direct `collaboration.spawn_agent` bug reports + 1
   tangential gateway item, not 10.
3. GH5: cite issue 293 only for the "every step must be a tool call"
   nudge; segregate or drop issue 257 from that claim.
4. GH4: label the identity-leak citation excerpt-only wherever it
   appears; pull the full issue if any claim beyond the excerpt is made.
5. UQ2/UQ3/UQ4: reword "co-occurrence" to "domain appeared among results
   for the phrase query" unless page bytes are fetched to prove the
   phrase on the page.
6. TZ: label GitHub code totals and issue/PR totals as uncaptured API
   totals (URL sample covers 20 issues per section, 0 PRs); carry the
   killed-legacy-grep caveat with any novelty claim from this lane.
7. Add hash sidecars for `github/`, `committer-accounts/`, and
   `linguist/`; add `_summary.json` to `hn-forum/ALL.sha256` (or its own
   sidecar).
8. RD1: keep the "self-report, not Reddit bytes" qualifier attached;
   native Reddit verification remains blocked (403 captures on file).
