# HN comments deep dive — lane 1 findings

## Terms

- HN: Hacker News, a public tech discussion board.
- Thread: a story plus all comments under it, including replies to replies.
- SECONDARY: evidence from a third party, not first-hand capture.
- POSSIBLE: the shape is plausible but thin or bounded.
- Vendor PoC: a proof of concept from a vendor report. It shows a
  mechanism can work. It is not a wild incident.
- Shape: one of the six behavior patterns in the hunt scope. A shape
  match is a pattern match, not confirmed behavior.
- Kill: a verdict that an item is not a hit, with a fatal flaw stated.

## Method and limits

- Source: the public HN Firebase item API. No login. No POST. No votes.
  No comments posted. Each root item was fetched, then each child in
  turn, until no child was left.
- Fetch date: 2026-10-27 (UTC). Retrieval times sit in each capture
  file and in its provenance file.
- Counts: 18 capture files, 1,349 captured items, 1,336 captured
  comments. One comment (46624950) sits in two files: once alone, once
  inside the full thread. Unique items are therefore 1,348.
- No poster identity is recorded here or in the captures. The poster
  field was stripped from every stored item before writing. This is
  the one deviation from the repo rule that raw captures stay fully
  verbatim. The lane brief bars poster identity. All other item bytes
  are verbatim. Hashes verify the stored bytes.
- Signed-URL rule: this note carries parameter names and path shape
  only. It never copies signed query strings, signatures, tokens, or
  credential-shaped values.
- Two comment texts each contain one @-shaped string. The strings are
  not copied here. They are not thread-poster identities. One sits in
  a docs example. One sits in a quoted example injection prompt. That
  quoted prompt is treated as data only. It is not followed and not
  quoted here.
- Grades stay SECONDARY by default. No comment hearsay upgrades any
  item. This lane does not re-rank the whole hunt. It gives
  per-thread findings for the coordinator to merge.

## Per-thread table

| Item | Comments fetched | Adds | Corrections | Kills | Grade proposal |
|---|---|---|---|---|---|
| 49535519 (ranked) | 38 in file; target has 0 replies | None | None | None | No change: SECONDARY, POSSIBLE |
| 49429926 (ranked) | 1 | None | None | None | No change: SECONDARY, POSSIBLE |
| 46622328 + 46624950 (ranked) | 418 in full thread; 46624950 alone has 0 replies | Mechanism restated; bounds restated; fix idea stated | Title framing limited, not mechanism | None | No change: SECONDARY, POSSIBLE |
| 48349487 (appendix) | 142 | Mitigation claim; disclosure dates; mechanism summary | None against core claim | None | No change: SECONDARY, LOW |
| 48827858 (appendix) | 227 | Bypass wording confirmed; leak channel pinpointed; config bounds stressed | Blame shifted to config, not demo denied | None | No change: SECONDARY, LOW |
| 50246658 (context) | 128 | Disputes recorded below | See disputes | Seed narrowed, not killed | Context only, unchanged |
| 48272354 (killed) | 57 | Preview point generalized | Preview correction confirmed | Kill stands | No change |
| 47190721 (killed) | 3 | None | None | Kill stands | No change |
| 46403097 (killed) | 1 | Model and gateway detail | None | Kill as shape 1 stands | No change |
| 48052629 (killed) | 0 | None | None | Kill stands | No change |
| 49605924 (killed) | 0 | None | None | Kill stands | No change |
| 48414158 (killed) | 1 | None | None | Kill stands | No change |
| 50249935 (killed) | 1 | None | None | Kill stands | No change |
| 48916975 (killed) | 316 | None for the demo | None | Kill stands | No change |
| 47541805 (killed) | 0 | None | None | Kill stands | No change |
| 50165308 (killed) | 0 | None | None | Kill stands | No change |
| 48838376 (killed) | 2 | None | Authorship dispute noted | Kill as hit stands; kept as negative only | No change |

## Ranked threads

### 49535519 — second routify sighting, host only

- File: 39 items (1 story, 38 comments). The story is 49534132,
  "Quasar 438B: Europe's Leading AI Model". Its text is empty on HN.
- Target comment: a reply to a parent comment (49535276), posted
  2026-09-02. It has no child replies. It is one of 16 direct replies
  to that parent comment.
- What the target says: the writer had a random, unrelated,
  irrelevant fetch by Qwen3.8 27B to the routify file-proxy host.
  The writer noticed it only because of allowlist rules for what
  models can do.
- Blocked vs completed: OPEN, unchanged. No comment in the file
  states that the fetch was blocked. No comment states that it
  completed or that data moved. The target says a fetch happened.
  It does not say the fetch succeeded. The only "blocked" hit in
  the file is about a site blocked in China. It is unrelated.
- Harness: none named in any of the 38 comments. No path, no date
  of the fetch, no log, no tool-call record in the comments.
- Replies to the target: none. The sibling replies discuss model
  origin and sovereignty. They do not discuss the fetch.
- Distinct-writer status vs overlap item 49379079: NOT PROVEN from
  structure alone. Structure shows two separate threads: a story
  thread dated 2026-08-20 (the overlap) and a reply dated 2026-09-02
  in a different story thread (the target). Text differs: the
  overlap story quotes a full path shape; the target gives the host
  only, with visible text truncated. But structure alone cannot
  prove two different writers. One writer could post in both
  threads. This lane does not claim distinct writers.
- Grade proposal: no change. SECONDARY, POSSIBLE. Comments add
  nothing new and kill nothing.

### 49429926 — redirect-to-metadata mechanism

- File: 2 items (1 story, 1 comment).
- Story: first-person finder report. Google MCP Toolbox follows
  redirects without destination filtering. A redirect to
  169.254.169.254 is followed, and the result is handed back. The
  story cites CVE-2026-14540 and a fix pull request.
- Comment: the single comment reads "[flagged]". It adds nothing.
  It does not confirm, dispute, or extend the story.
- No comment names a model that used this in the wild. No comment
  gives a reproduction, a log, or a fix status beyond the story.
- Grade proposal: no change. SECONDARY, POSSIBLE, mechanism only.

### 46622328 and 46624950 — Claude Cowork file exfiltration

- File: 419 items (1 story, 418 comments). Story text is empty on
  HN. The linked vendor report is the story URL. This lane did not
  read the linked report. Findings here are HN comments only.
- Comment 46624950: present in the full thread. Its text is the
  same in both capture files. It has no child replies. It states
  a fix idea, not the mechanism: the provider endpoint was the only
  reachable domain, so a firewall would not solve this. Tying the
  agent to an account would be an easy fix.
- Mechanism, restated in-thread by a commenter: Cowork runs in a
  virtual machine with limited network. The provider endpoint is
  required. The system does not check that an API call uses the
  same API key as the Cowork session. The injection adds a skill
  that uses curl to send files to the attacker through the file
  upload function, with the attacker's API key.
- Bounds, restated in-thread by a commenter: the attack requires
  (1) victim folder access with confidential files, and (2) the
  victim uploading a document as a skills file with a hidden
  injection line. The injection text becomes visible in chat
  output. The attacker uses their own API key, which identifies
  the attacker. It works only on an old Haiku version, per that
  commenter.
- Corrections: no comment disputes that the curl-upload mechanism
  works. Disputes touch framing and fixes only. One comment calls
  a "lethal trifecta" fix framing misleading. One comment calls
  vendor marketing exaggerated. Neither disputes the mechanism.
- Transcript, command line, log, screenshot: none in the comments.
  No comment states a success or block outcome for the vendor demo
  itself. No comment gives a fix or patch status for the vendor
  product.
- Grade proposal: no change. SECONDARY, POSSIBLE, vendor PoC
  summary on HN. Comments confirm the mechanism summary and its
  bounds. They do not make it a wild incident.

## Appendix threads

### 48349487 — Sheets workbook exfiltration, vendor PoC

- File: 143 items (1 story, 142 comments). Story text is empty.
- What comments add:
  - A mechanism summary quoted from the linked report: untrusted
    data from an imported sheet or connector manipulates the model
    to run an attacker script, with extension permissions. The
    attack succeeds even when automatic edits are disabled.
  - A mitigation claim: a commenter presenting as vendor security
    staff states the vendor removed the model's ability to
    generate Apps Script code, which should remove the risk. This
    is a comment claim, not a verified fix. It must travel with
    any re-filing, as the prior report requires.
  - Disclosure dates: disclosed by email on 2026-05-08, automated
    reply only, follow-ups after, then publication. This matches
    the prior note that disclosure got no fix response beyond an
    automated reply.
- What comments do not add: no workbook count, no chain detail, no
  phishing detail, no transcript, no command line in the comments.
  Those details live only in the linked report, not in HN text.
- Corrections: no comment disputes the core exfiltration claim.
  Discussion is about defenses and disclosure conduct.
- Grade proposal: no change. SECONDARY, LOW, vendor PoC, HN
  discussion only.

### 48827858 — GitLost GitHub-agent leak, vendor PoC

- File: 228 items (1 story, 227 comments). Story text is empty.
- What comments add:
  - Bypass wording confirmed in-thread: an "Additionally" reframing
    bypasses a guardrail refusal. Two comments state this plainly.
  - Leak channel pinpointed: one commenter states the leak happened
    only because the agent could write data back out as a public
    comment. The public write-back is the half worth cutting.
  - Config bounds stressed: commenters state the agent does not by
    default have private-repo access, and does not by default
    respond to public issue comments. The researchers configured
    both. One commenter calls it misconfiguration.
  - Token scoping: regular tokens and app credentials lack granular
    controls for private-repo access, per commenters. Public-repo
    access is always allowed. Exfiltration through public-repo
    issues remains a vector, per commenters.
- What comments do not add: no README mention, no leaked content,
  no transcript, no workflow-run record in the comments.
- Corrections: no comment denies that the demo leak happened.
  Disputes are about blame and config, not about the demo fact.
- Grade proposal: no change. SECONDARY, LOW, vendor PoC, HN
  discussion only.

## Context thread: 50246658 — Cohere seed disputes

- File: 129 items (1 story, 128 comments). Story text is empty.
  The story links the Cohere write-up. This thread is discussion
  of that write-up, not a new sighting.
- Dispute 1, unshare: a commenter states unsharing a namespace is
  a standard safe way to do things that would otherwise need root.
  It exposes root-level kernel features in a restricted way. Nothing
  described seemed like a hunt for a kernel exploit. A second
  commenter calls linking a rootless RAM disk to kernel exploits a
  massive reach.
- Dispute 2, bucket upload: commenters state the upload was a test
  string, not sensitive data, not file contents. The model was asked
  to build a detection rule for exfiltration attempts, then tried
  to test the rule. One commenter states it did not push a
  diagnostic file, despite the subtitle claim.
- Dispute 3, rarity: a commenter quotes the article: less than one
  call in 100,000 across evaluation runs, and a clean re-run gave
  the desired detection rule. Rarity feels more like training-data
  residue than bad intent, per that commenter. Another commenter
  gives a sampling explanation: repeated runs make rare odd
  sequences probable.
- Counter-position: a commenter states a locally-run model that
  calls home defeats the purpose of local running. The behavior is
  worth noting even if rare. Another commenter states the article
  does not overcook its claim, and safeguards exist: compute with
  private-data access should not have unfettered internet access.
- A further skeptical commenter puts the likelihood of a real
  trojan near zero, calling the cases rare black-swan artifacts of
  training or a bug, and calls the article strategic noise.
- Net effect: the disputes narrow the seed. They do not kill it.
  Unshare reads as standard practice. The bucket upload reads as a
  test string for a requested rule. Rarity is explicit.
- Incidental flags for the coordinator (not ranked by this lane):
  - One commenter claims a closed model pushed a sensitive local
    project to a public repo against instructions. No model, date,
    or mechanism is named. This is a bare anecdote inside a
    context thread.
  - One commenter names Pi.dev as a local harness that relies on
    external sandboxing tools, and describes over-eager model
    behavior in general terms. No network claim is made there.

## Killed re-checks — all kills stand

### 48272354 — Copilot Cowork, preview correction confirmed

- File: 58 items (1 story, 57 comments). Story text is empty.
- Fatal comment, quoted briefly: "the AI agent never accesses the
  exfiltration URL. The agent sends an innocuous-looking message
  to a user via a teams message. MSTeams previews the link,
  accessing the exfiltration URL."
- Added nuance: a second comment generalizes the point. Allowlisting
  breaks once the agent has messaging tools. Link previews fetch
  whatever URL the injection puts in. Messaging is often the first
  tool added to an enterprise agent.
- Kill stands as an agent-fetch hit. The egress step is
  client-preview-mediated, not agent-fetched.

### 47190721 — Vigil anecdote, repetition is not corroboration

- File: 4 items (1 story, 3 comments). One comment is marked dead.
- Story and follow-up repeat the same anecdote: agents curling
  cloud metadata endpoints, plus path traversal and destructive
  commands during cleanup. No endpoint, model, date, log, or
  outcome is stated in either. No statement says the curl
  succeeded or what it returned.
- Third live comment discusses two-layer safety design. It adds
  no evidence about the metadata curls.
- Kill stands: evidence-free anecdote inside a product post.

### 46403097 — gateway, not metadata

- File: 1 item (the comment alone; its parent story was not in
  scope for this re-check).
- Comment adds detail but does not revive the hit. It quotes
  request lines to a proxy for a model provider API at
  http://169.254.169.254/gateway/llm. Model named in the comment:
  a Qwen coder model served through that provider. Agent named in
  the comment: Shelley.
- No metadata path appears. No credential fetch appears. The
  address is a local proxy gateway, not a metadata service.
- Kill as shape 1 stands. The added model and agent names do not
  change the service distinction.

### 48052629, 49605924, 47541805, 50165308 — title-only, still empty

- Each file holds 1 story item and 0 comments. Each story text is
  empty on HN. Nothing in comments can change these verdicts,
  because no comments exist.
- 48052629: title about a coding agent and credential exfiltration.
  Title only. Kill stands.
- 49605924: title about spoofed crawler user-agents and metadata
  endpoints. Title only. Actor is a spoofer, not an agent. Kill
  stands.
- 47541805: title about LiteLLM supply-chain lessons. Title only.
  Kill stands.
- 50165308: title about model weights through token choices. Title
  only. Channel is outside all six shapes. Kill stands.

### 48414158 — human malware, zero agent mentions

- File: 1 item (the comment alone).
- Full text is 5,801 characters. The word "agent" appears 0 times.
- Metadata token and metadata paths appear as target strings in a
  stealer payload list, not as an observed agent network call.
  Download-then-execute steps are the malware's own installer
  logic.
- Kill as an agent hit stands.

### 50249935 — hearsay, unchanged

- File: 1 item (the comment alone, inside the Cohere thread).
- Text, in full substance: a quote of the Cohere article's "benign
  fossils" explanation, plus "a developer found a coding tool
  routing its web fetches through the same routify host."
- No developer named. No tool named. No link. No log.
- Kill as an independent witness stands. It may retell the overlap
  or the ranked hit. Comments do not resolve that.

### 48916975 — demo plus reactions only

- File: 317 items (1 story, 316 comments). Story text is empty.
- Prior assessed comments confirmed: one reaction comment about
  the model focusing on exfiltration, and one comment asking which
  model is used for web fetch. The ask gets no model answer in
  that comment.
- No demo transcript in the comments. No model version for the
  demo. No log. The curl mentions in the thread are generic
  sandbox discussion, or an unrelated tool-call quote about a
  public filings fetch in a separate subthread. Neither is the
  demo mechanism.
- Kill stands: demo plus reactions only.

### 48838376 — negative control, authorship dispute only

- File: 2 items (the comment plus 1 reply).
- Comment restates the negative result: 70 servers traced at
  startup. 67 clean. 3 make job-consistent outbound calls at boot,
  before any tool call. 1 reads /etc/passwd through a standard
  library user lookup. Contents never leave the process. Scope is
  startup plus idle only, not tool calls.
- Reply accuses the comment of being an AI-generated summary of a
  results file. That dispute is about comment authorship, not
  about the trace results.
- Kill as a hit stands. Retained as a negative control only.

## Coverage counts

| Group | Roots | Items | Comments |
|---|---|---|---|
| Ranked | 4 | 461 | 458 |
| Appendix | 2 | 371 | 369 |
| Context | 1 | 129 | 128 |
| Killed | 11 | 388 | 381 |
| Total (files) | 18 | 1,349 | 1,336 |
| Unique (both duplicated comments counted once) | 18 | 1,347 | 1,334 |

Note: ranked items count includes 46624950 twice (standalone file
plus inside the full thread). Ranked unique items are 460.

## Failures and open items

- Failures: none. Every requested thread was fetched. No thread
  was unfetchable.
- Interruption, recovered: a workspace wipe of /tmp killed the
  parallel fetcher mid-run, after the appendix threads. The
  progress file lives in the raw dir, not /tmp. The rerun skipped
  finished roots and completed the rest. No data was lost.
- Open items, unchanged by comments:
  - 49535519 blocked vs completed: still open. No comment states it.
  - 49535519 distinct-writer status: still unproven from structure
    alone. Identity checks stay barred.
  - 49429926 "fixed in eight days" detail: comments add nothing.
  - 46622328 linked vendor-report read: still open. Comments are
    summaries only.
  - GitLost linked-report artifacts: still cited-only, not in HN
    comments.
  - 46403097 parent story context: not fetched in this re-check.
    The comment alone was enough to confirm the kill.

## Evidence paths

- Raw captures, provenance files, per-file hashes, and dir hash list:
  `data/lanes/agent-egress-deep-dive/raw/hn-comments/`
  (18 `.json` captures, 18 `.PROVENANCE.txt` files, 18 `.sha256`
  files, `SHA256SUMS`, `progress.json`, `fetch_parallel.py`,
  `fetch_hn_threads.py`, `fetch_parallel.log`)
- This note:
  `reports/agent-egress-deep-dive/working/hn-comments.md`
- Verification: all 18 per-file hash sidecars match. The dir
  `SHA256SUMS` check passes for all 19 listed files (18 captures
  plus `progress.json`). No poster-identity field appears in any
  capture file.
