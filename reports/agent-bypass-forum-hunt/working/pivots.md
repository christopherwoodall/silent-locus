# Pivots — agent-bypass forum hunt (working note, STAGED, not filed)

## Scope and rules

- Pivot executor pass, 2026-10-29. One row per pivot. Result grades:
  ADD (adds corroboration), KILL (contradicts or removes the item),
  neutral (no change to the item).
- Items are the ranked items from the four lane notes. Forums F1 and
  GitHub item 1 are the SAME item (OpenAI GPT-6 monitoring incidents):
  merged here, never double-counted. GitHub item 17 is a spec that
  points at that same item, not a separate incident.
- HN appendix items (vendor PoCs, title-only stories) were NOT ranked
  by the HN lane and got no pivot rows here. That is a stated gap,
  not a kill.
- Agents and agent infrastructure only. No poster handle appears in
  this note. No signed value, token, or full query string appears
  here. Path shapes and page titles only, where relevant.
- Passive reads only. No POST, no login, no sessions. No Shodan.
  No package repos. No Docker Hub. No Transluce submissions.
  No Factum writes. No commit, no push.
- Evidence: `data/lanes/agent-bypass-forum-hunt/raw/pivots/`.
  Every capture has a `.PROVENANCE.txt` (source, retrieval time,
  method) and a `.sha256`. All hashes verified after capture
  (sha256sum check clean).

## Method notes (read before citing a neutral)

- urlquery: the `q` term matches submitted URLs AND page content.
  Broad terms therefore return recent-submission noise. Only
  domain-scoped queries and narrow distinctive terms are
  discriminating. For broad terms only the top 30 returned reports
  were inspected (titles and hosts). A neutral on a broad term
  means "no corroboration in the inspected set", not "the item
  does not exist".
- urlscan: search API only. No detail page was fetched, per the
  brief (detail pages are login-gated; the gate was not bypassed).
  The search API itself reports a 30-day window
  (`search_date_limit_days: 30`), so September incidents mostly
  fall outside it. A urlscan zero is weak evidence by design.
- crt.sh: certificate existence proves a host held certificates.
  It never proves an incident. Every crt.sh row is neutral by
  construction unless stated otherwise. Two hosts failed (see
  coverage limits); a failed lookup is not a finding.
- GitHub: unauthenticated public REST reads of issue state and
  comments, compared with the counts in the GitHub lane note
  (captured 2026-10-29). Unchanged counts plus an `updated_at`
  before the lane date mean no new thread activity since the lane.
- Tool quirks found during this run: the urlquery CLI hard-codes
  a helper path that no longer exists; it ran with an explicit
  path override to the live helper location (no connector file
  was edited). The urlquery htmx endpoint returned 404 and was
  not used; the authenticated API was used instead.

## Headline

- ADD: 4 pivots (all weak-to-moderate, all bounded below).
  No ADD proves an agent's intent, and no ADD upgrades any
  item's grade on its own.
- KILL: 0. No pivot contradicted or removed any item.
- Neutral: all other pivots.
- Strongest ADD: GitHub issue search for the hackerbot-claw
  campaign returns 210 results, including hardening pull
  requests that cite the campaign and the Trivy compromise as
  their reason. That corroborates that the campaign exists and
  is widely referenced. It does NOT prove the "autonomous
  agent" attribution in the HN4 vendor article.

## Pivots: urlquery

| Item | Query | Result | Evidence |
|---|---|---|---|
| HN1 DNS escape | `url.domain:alignment.openai.com` | neutral — 0 hits; no urlquery submission of the report host | `raw/pivots/uq-openai-alignment-domain.json` |
| HN1 DNS escape | `url.domain:madrobot.blog` | neutral — 0 hits | `raw/pivots/uq-madrobot-domain.json` |
| HN2 Voratiq | `url.domain:voratiq.com` | neutral — 0 hits | `raw/pivots/uq-voratiq-domain.json` |
| HN3 Australian gov accesses | phrase for the Register headline shape | neutral — 880 hits, top 30 all content-match noise, none the Register article | `raw/pivots/uq-aus-gov-phrase.json` |
| HN4 Trivy / hackerbot-claw | `trivy` | neutral — 498 hits, top 30 noise, none the grith.ai article (see GitHub search ADD below) | `raw/pivots/uq-trivy-term.json` |
| HN4 Trivy / hackerbot-claw | `url.domain:grith.ai` | neutral — 0 hits | `raw/pivots/uq-grith-domain.json` |
| HN5 Kimi K3 | `Kimi K3 sandbox` | neutral — 431 hits, top 28 noise | `raw/pivots/uq-kimi-sandbox.json` |
| HN5 Kimi K3 | `url.domain:ai-updates.net` | neutral — 0 hits | `raw/pivots/uq-aiupdates-domain.json` |
| HN6 /proc dodge quote | `proc/self/root` | neutral — 3 hits, none the Ona article; one sandbox-titled page is unverified and is NOT counted as corroboration | `raw/pivots/uq-proc-root.json` |
| HN7 ISC-Bench | `ISC-Bench` | neutral — 0 hits in urlquery (see GitHub repo ADD below) | `raw/pivots/uq-iscbench-term.json` |
| HN8 OpenClaw wipe refusal | `OpenClaw` | neutral — 1,214 hits, top 28 noise | `raw/pivots/uq-openclaw-term.json` |
| HN11 collusion.wiki board | `url.domain:collusion.wiki` | ADD (weak) — 6 reports, all on the collusion.wiki host, dated 2026-09-08 to 2026-09-28, page title matching the HN story title. This corroborates host plus title in the exposure window only. It does NOT corroborate the swarm claims themselves | `raw/pivots/uq-collusion-domain.json` |
| HN12 grader deception (DISCUSSED) | `deceiving the grader` | neutral — 1,162 hits, top 30 noise | `raw/pivots/uq-grader-deception.json` |
| R1 Antigravity drive wipe | `Antigravity` | neutral — 1,326 hits, top 30 noise | `raw/pivots/uq-antigravity-term.json` |
| R2 Claude Code home wipe | Reddit post id `1pgxckk` | neutral — 0 hits | `raw/pivots/uq-reddit-postid-1pgxckk.json` |
| R2 Claude Code home wipe | phrase for the home-wipe headline shape | neutral — 592 hits, top 30 noise | `raw/pivots/uq-home-wipe-phrase.json` |
| R3 48,218-file junction deletion | `48218` | neutral — 1,579 hits, top 30 numeric noise | `raw/pivots/uq-48218-term.json` |
| R3 junction deletion | `url.domain:blog.darkcontrolai.com` | neutral — 0 hits | `raw/pivots/uq-darkcontrol-domain.json` |
| R3 junction deletion | `url.domain:rapidclaw.app` | neutral — 0 hits | `raw/pivots/uq-rapidclaw-domain.json` |
| R4 Codex F: drive wipe | `pycache` | neutral — 18 hits, none the gizmochina article or a Codex F: drive account | `raw/pivots/uq-pycache-term.json` |
| R5 Grok canary URLs | `whofetched` | neutral — 0 hits in urlquery (see GitHub repo ADD below) | `raw/pivots/uq-whofetched-term.json` |
| R5 Grok canary URLs | `url.domain:technicalseonews.com` | neutral — 0 hits | `raw/pivots/uq-techseo-domain.json` |
| F1/GH1 GPT-6 monitoring | phrase for the WindowsForum headline shape | neutral — 747 hits, top 30 noise | `raw/pivots/uq-windowsforum-gpt6.json` |
| F1/GH1 GPT-6 monitoring | `url.domain:alignment.openai.com` | neutral — 0 hits (same capture as HN1 row) | `raw/pivots/uq-openai-alignment-domain.json` |
| F2 evasion notes | `evade containment` | neutral — 737 hits, top 29 noise | `raw/pivots/uq-evade-containment.json` |
| F3 Forever AGENTS.md | `function-color` | neutral — 987 hits, top 30 noise | `raw/pivots/uq-function-color.json` |
| F4 monitor jailbreaking | `monitor jailbreaking` | neutral — 989 hits, top 30 noise | `raw/pivots/uq-monitor-jailbreaking.json` |
| F5 finance agent fakes revenue | `SummitBridge` | neutral — 6 hits, all unrelated (a funding company and generic pages) | `raw/pivots/uq-summitbridge-term.json` |
| F6 /proc dodge synthesis | `proc/self/root` | neutral — same capture as HN6 row | `raw/pivots/uq-proc-root.json` |
| GH4 harness#135 | `claude-code-harness` | neutral — 15 hits, none the harness repo or issue | `raw/pivots/uq-claude-code-harness.json` |
| GH2/GH3 codex issues | `github.com/openai/codex` | neutral — 62 hits, top 30 content matches only; the one openai.com hit is a model-deprecation notice, not either issue | `raw/pivots/uq-codex-github-url.json` |

## Pivots: urlscan (search only, 30-day window)

| Item | Query | Result | Evidence |
|---|---|---|---|
| HN2 Voratiq | `domain:voratiq.com` | neutral — 0 results | `raw/pivots/urlscan-voratiq.com.json` |
| HN1 DNS escape | `domain:madrobot.blog` | neutral — 1 result, a different article (usage-limit topic), not the DNS-escape article | `raw/pivots/urlscan-madrobot.blog.json` |
| HN4 Trivy | `domain:grith.ai` | neutral — 0 results | `raw/pivots/urlscan-grith.ai.json` |
| HN11 collusion.wiki | `domain:collusion.wiki` | neutral — 1 result, but on an unrelated host (search mismatch); not counted as a collusion.wiki scan | `raw/pivots/urlscan-collusion.wiki.json` |
| HN1, F1/GH1 OpenAI report | `domain:alignment.openai.com` | neutral — 0 results | `raw/pivots/urlscan-alignment.openai.com.json` |
| HN5 Kimi K3 | `domain:ai-updates.net` | neutral — 0 results | `raw/pivots/urlscan-ai-updates.net.json` |
| R3 junction deletion | `domain:blog.darkcontrolai.com` | neutral — 0 results | `raw/pivots/urlscan-blog.darkcontrolai.com.json` |
| R3 junction deletion | `domain:rapidclaw.app` | neutral — 1 result, a sign-in page only | `raw/pivots/urlscan-rapidclaw.app.json` |
| R5 canary URLs | `domain:technicalseonews.com` | neutral — 0 results | `raw/pivots/urlscan-technicalseonews.com.json` |
| F1/GH1 GPT-6 monitoring | `domain:windowsforum.com` | neutral — 4 results: one adjacent AI-agent prompt-injection article (not the GPT-6 monitor article), the rest homepages or unrelated articles | `raw/pivots/urlscan-windowsforum.com.json` |
| R1 Antigravity wipe | `domain:incidentdatabase.ai` | neutral — 1 result, an entity page, not Incident Database report 7050 | `raw/pivots/urlscan-incidentdatabase.ai.json` |
| F2/F4/F5 LessWrong posts | `domain:lesswrong.com` | neutral — 1 result, the LessWrong homepage only | `raw/pivots/urlscan-lesswrong.com.json` |

## Pivots: crt.sh (host existence only — all neutral)

| Item | Host | Result | Evidence |
|---|---|---|---|
| HN2 Voratiq | voratiq.com | neutral — 61 certificates; host existed, nothing about the logs | `raw/pivots/crtsh-voratiq.com.json` |
| HN4 Trivy | grith.ai | neutral — 40 certificates; host existed only | `raw/pivots/crtsh-grith.ai.json` |
| HN1 DNS escape | madrobot.blog | neutral — 2 certificates | `raw/pivots/crtsh-madrobot.blog.json` |
| HN11 collusion.wiki | collusion.wiki | neutral — 6 certificates; host existed only | `raw/pivots/crtsh-collusion.wiki.json` |
| HN1, F1/GH1 OpenAI report | alignment.openai.com | neutral — 10 certificates | `raw/pivots/crtsh-alignment.openai.com.json` |
| HN5 Kimi K3 | ai-updates.net | neutral — 20 certificates | `raw/pivots/crtsh-ai-updates.net.json` |
| R3 junction deletion | blog.darkcontrolai.com | neutral — 2 certificates | `raw/pivots/crtsh-blog.darkcontrolai.com.json` |
| R3 junction deletion | rapidclaw.app | neutral — 514 certificates (shared-cert noise included); host existed only | `raw/pivots/crtsh-rapidclaw.app.json` |
| R5 canary URLs | technicalseonews.com | neutral — 18 certificates | `raw/pivots/crtsh-technicalseonews.com.json` |
| F1/GH1 GPT-6 monitoring | windowsforum.com | neutral — 411 certificates (shared-cert noise included) | `raw/pivots/crtsh-windowsforum.com.json` |
| F2/F4/F5 LessWrong posts | lesswrong.com | neutral — 225 certificates | `raw/pivots/crtsh-lesswrong.com.json` |
| R1 Antigravity wipe | incidentdatabase.ai | SURFACE FAILED — crt.sh lookup failed after retries; not a finding (host is already established via the lane capture and the urlscan entity page) | `raw/pivots/crtsh-incidentdatabase.ai.ERROR.txt` |
| F3/F6 DEV posts | dev.to | SURFACE FAILED — crt.sh lookup failed after retries; not a finding (a shared-host cert set would not have been discriminating anyway) | `raw/pivots/crtsh-dev.to.ERROR.txt` |

## Pivots: GitHub comments refresh (issue state + comments, vs lane counts)

All 16 issues are still open and every comment count is unchanged
from the GitHub lane note. No new confirmation, no contradiction,
no closure or fix landed for any item. Each row is neutral.

| Item | Issue | Result | Evidence |
|---|---|---|---|
| GH2 codex forged approvals | openai/codex#41769 | neutral — open, 2 comments (lane: 2), last update 2026-10-05, before the lane date | `raw/pivots/gh-openai-codex-41769-issue.json`, `raw/pivots/gh-openai-codex-41769-comments.json` |
| GH3 codex compaction authorization | openai/codex#41740 | neutral — open, 3 comments (lane: 3), last update 2026-10-04 | `raw/pivots/gh-openai-codex-41740-issue.json`, `raw/pivots/gh-openai-codex-41740-comments.json` |
| GH4 harness constraint edit | petrpus/claude-code-harness#135 | neutral — open, 0 comments (lane: 0); still no maintainer reply, no commit diff, no settings.json test | `raw/pivots/gh-petrpus-claude-code-harness-135-issue.json`, `raw/pivots/gh-petrpus-claude-code-harness-135-comments.json` |
| GH5 agent-filed confession | anthropics/claude-code#97890 | neutral — open, 3 comments (lane: 3) | `raw/pivots/gh-anthropics-claude-code-97890-issue.json`, `raw/pivots/gh-anthropics-claude-code-97890-comments.json` |
| GH6 coordinator false report | anthropics/claude-code#103274 | neutral — open, 4 comments (lane: 4) | `raw/pivots/gh-anthropics-claude-code-103274-issue.json`, `raw/pivots/gh-anthropics-claude-code-103274-comments.json` |
| GH7 agents:configure grant | paperclipai/paperclip#17777 | neutral — open, 0 comments (lane: 0) | `raw/pivots/gh-paperclipai-paperclip-17777-issue.json`, `raw/pivots/gh-paperclipai-paperclip-17777-comments.json` |
| GH8 approval policy ignored | temporalio/ai-integrations#274 | neutral — open, 0 comments (lane: 0) | `raw/pivots/gh-temporalio-ai-integrations-274-issue.json`, `raw/pivots/gh-temporalio-ai-integrations-274-comments.json` |
| GH9 subagent approval synthesis | sentinel-projects/sentinel#21 | neutral — open, 0 comments (lane: 0) | `raw/pivots/gh-sentinel-projects-sentinel-21-issue.json`, `raw/pivots/gh-sentinel-projects-sentinel-21-comments.json` |
| GH10 Gmail trash gap | subtract0/AgencyOS#140 | neutral — open, 1 comment (lane: 1) | `raw/pivots/gh-subtract0-AgencyOS-140-issue.json`, `raw/pivots/gh-subtract0-AgencyOS-140-comments.json` |
| GH11 confirmation callback gap | Sunona-AI-labs/sunona#36 | neutral — open, 1 comment (lane: 1) | `raw/pivots/gh-Sunona-AI-labs-sunona-36-issue.json`, `raw/pivots/gh-Sunona-AI-labs-sunona-36-comments.json` |
| GH12 launcher bypass flags | Xoshbin/asyar#959 | neutral — open, 1 comment (lane: 1); the maintainer reproduction in the lane stands, nothing new | `raw/pivots/gh-Xoshbin-asyar-959-issue.json`, `raw/pivots/gh-Xoshbin-asyar-959-comments.json` |
| GH13 loopback scanner gap | opena2a-org/arp-guard#232 | neutral — open, 0 comments (lane: 0) | `raw/pivots/gh-opena2a-org-arp-guard-232-issue.json`, `raw/pivots/gh-opena2a-org-arp-guard-232-comments.json` |
| GH14 sandbox socket path | nolabs-ai/nono-packs#64 | neutral — open, 0 comments (lane: 0) | `raw/pivots/gh-nolabs-ai-nono-packs-64-issue.json`, `raw/pivots/gh-nolabs-ai-nono-packs-64-comments.json` |
| GH15 tool-result governance gap | C360Studio/semstreams#1140 | neutral — open, 2 comments (lane: 2) | `raw/pivots/gh-C360Studio-semstreams-1140-issue.json`, `raw/pivots/gh-C360Studio-semstreams-1140-comments.json` |
| GH16 worktree doc wording | NousResearch/hermes-agent#145548 | neutral — open, 0 comments (lane: 0); still DISCUSSED only | `raw/pivots/gh-NousResearch-hermes-agent-145548-issue.json`, `raw/pivots/gh-NousResearch-hermes-agent-145548-comments.json` |
| GH17 Guardian spec (pointer to F1/GH1) | project-noemi/agents#652 | neutral — open, 0 comments (lane: 0); still a proposal, not an act | `raw/pivots/gh-project-noemi-agents-652-issue.json`, `raw/pivots/gh-project-noemi-agents-652-comments.json` |

## Pivots: GitHub repo / search (the ADDs beyond urlquery)

| Item | Query | Result | Evidence |
|---|---|---|---|
| HN7 ISC-Bench | repo read for the ISC-Bench repo named in the HN lane | ADD (weak) — the repo exists and its description matches the lane topic (safety failures in coding agents and frontier models, reproducible workspaces). This corroborates the research project exists. It does NOT verify the "100 models" or "benign task" claims | `raw/pivots/gh-repo-iscbench.json` |
| R5 Grok canary URLs | repo search for `whofetched` | ADD (weak-to-moderate) — exactly one repository named whofetched, described as a canary-link experiment (secret canary links, edge log, published checks) tested on ChatGPT, Claude, Gemini, Grok, Perplexity and Copilot, dated October 2026. This corroborates the experiment's existence, method shape, and date. It does NOT verify the 59-address Grok claim or the UA/infra reading | `raw/pivots/gh-search-whofetched.json`, `raw/pivots/gh-repo-whofetched.json` |
| HN4 Trivy / hackerbot-claw | issue search for `hackerbot-claw` | ADD (campaign existence) — 210 results; inspected top results are hardening pull requests that cite the hackerbot-claw GitHub Actions exploitation campaign and the Trivy compromise as their reason. This corroborates the campaign is real and widely referenced. It does NOT prove the agent-autonomy attribution in the grith.ai article | `raw/pivots/gh-search-hackerbot.json` |

## Items with no discriminating pivot available (honest gap, not a kill)

| Item | Why no pivot row | Standing |
|---|---|---|
| HN9 coding agent "refused to stop" anecdote | Generic anecdote: no host, repo, term, or artifact anchor. Any query would return noise. | neutral (untested) |
| HN10 sandbox "go crazy" observation | Generic observation: no incident, host, or term anchor. | neutral (untested) |

## Coverage checklist (every ranked item appears above)

- HN1: urlquery x2, urlscan x1, crt.sh x1 — neutral.
- HN2: urlquery x1, urlscan x1, crt.sh x1 — neutral.
- HN3: urlquery x1 — neutral.
- HN4: urlquery x2, urlscan x1, crt.sh x1, GitHub search ADD — campaign corroborated, autonomy unproven.
- HN5: urlquery x2, urlscan x1, crt.sh x1 — neutral.
- HN6: urlquery x1 (shared with F6), no dedicated host — neutral.
- HN7: urlquery x1 (zero), GitHub repo ADD (weak) — project exists, claims unverified.
- HN8: urlquery x1 — neutral.
- HN9, HN10: no-test gap — neutral (untested).
- HN11: urlquery ADD (weak, host plus title in-window), urlscan neutral, crt.sh neutral.
- HN12: urlquery x1 — neutral; grade stays DISCUSSED.
- R1: urlquery x1, urlscan x1, crt.sh failed — neutral.
- R2: urlquery x2 — neutral.
- R3: urlquery x3, urlscan x2, crt.sh x2 — neutral.
- R4: urlquery x1 — neutral.
- R5: urlquery x2, urlscan x1, crt.sh x1, GitHub repo ADD — experiment corroborated, 59-address claim unverified.
- F1/GH1 (merged): urlquery x2, urlscan x2, crt.sh x2, GitHub spec-issue refresh — neutral; no new witness, no contradiction.
- F2: urlquery x1, urlscan x1, crt.sh x1 — neutral.
- F3: urlquery x1, crt.sh failed for the DEV host — neutral.
- F4: urlquery x1, urlscan x1, crt.sh x1 — neutral.
- F5: urlquery x1, urlscan x1, crt.sh x1 — neutral.
- F6: urlquery x1 (shared with HN6), crt.sh failed for the DEV host — neutral.
- GH2–GH17: GitHub refresh each — all neutral, all still open, counts unchanged. GH2/GH3 also got a urlquery row; GH4 also got a urlquery row.

## Unresolved (for the coordinator)

1. No pivot killed anything. The four ADDs are all bounded
   existence/window corroboration, not claim verification. Do not
   let them upgrade grades on their own.
2. The Reddit threads themselves are still unread (lane block
   stands; this pass did not attempt Reddit, and did not route
   around the block). R2's approval mode, R4's execution actor,
   R5's UA/infra reading, and R3's verifier report are all still
   open exactly as the Reddit lane left them.
3. The GitHub lane's open points are unchanged: codex#41769
   transcript (offered on request), harness#135 commit diff and
   settings.json test, and all mechanism fixes are still
   unverified. No maintainer has replied to the zero-comment
   issues since the lane.
4. HN appendix items (Pillar escapes, Cursor Medium post,
   Tom's Hardware crypto-mining article behind story 47451148)
   were out of this pass's ranked scope. The /proc urlquery
   hit titled "Your Agent Sandbox Is a Suggestion" is an
   unverified possible lead for the HN6/F6 /proc claim, not a
   pivot result; a future pass may read that page and judge it
   fresh.
5. urlscan's 30-day search window and urlquery's content-match
   noise are the two structural limits on this pass. A future
   pass with authenticated urlscan (longer window) or a
   detail-page route would be needed to do better on the
   September items; that route was out of this pass's brief.
6. F5's post date is still unverified (forums lane caveat
   stands); nothing in this pass dates it.
