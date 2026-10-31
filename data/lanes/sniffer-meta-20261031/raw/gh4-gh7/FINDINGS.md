# GH4 / GH7 exploitation lane — findings

Lane: sniffer-meta-20261031, GH4/GH7. Operator: BigSexyWarlock69.
Pull date: 2026-10-31. Method: read-only GitHub API GET via existing gh CLI
auth. No POST, no fresh login, no sessions created. No push, no commit,
no Factum writes (coordinator commits). Rate remaining after the GH7 batch:
4944 of 5000. No rate guard tripped.

Terms used here: OBSERVED means first-hand bytes in the fetched record show
the act. REPORTED means a claim stated inside a record, not independently
verified by this lane. DISCUSSED means talk or coordination in comments.
CUT means excluded, with the reason given. Default grade is SECONDARY unless
an OBSERVED act is stated. No human poster handles appear in this file.
One wallet value from a registration filing is withheld throughout, per the
task constraint, and is marked where it was removed.

## GH4 — LiteLLM Claude Code identity sentence (BerriAI/litellm #42221)

Verdict: product bug, REPORTED. Nothing stronger is established.

Status at pull time: issue OPEN, never closed. Created 2026-09-21T11:51:52Z,
last updated 2026-09-21T15:32:39Z. Labels: llm translation, claude code.
Comments on the issue: 1. Maintainer response: none found. The issue
timeline shows only the two labels and the one comment. The issue author
and the commenter both carry author association NONE.

### What the full body proves beyond the excerpt

The staged excerpt cut off mid-list at one provider name. The full body adds:

- Affected providers: DeepSeek, MiniMax, Tencent, and OpenAI-like
  Anthropic-compatible passthrough endpoints, reached through the
  Anthropic-to-OpenAI chat-completions translation bridge (generic
  OpenAI-compatible endpoints, including hosted vLLM-style models
  registered for chat-completions use).
- A full reproduction shape: a messages request whose system text is the
  identity sentence plus a real instruction, sent to a non-Claude model
  behind an OpenAI-compatible base. Actual behavior claimed: the model
  echoes the identity sentence back. Expected behavior claimed: the
  identity sentence is stripped upstream and only the real instruction
  reaches the model.
- Scoping: stripping must apply only to non-Claude endpoints. First-party
  Claude and Claude-serving Bedrock, Vertex, and Azure endpoints must keep
  the sentence.
- Self-assessed severity: High, for self-hosted and OpenAI-compatible
  fleets routing Claude Code traffic through a non-Claude model.
- Related but distinct: issue #29572 (billing-header stripping).
- A claim that the issue is "Resolved by #42203". That claim is NOT borne
  out at pull time (see fix status below).

### Reproduction, fix status

- Reproduction: reporter-claimed only. The reporter states the echo test
  was reproduced on the translation bridge. This lane did not re-run the
  test, so the reproduction is REPORTED, not OBSERVED by this lane.
- Fix status: UNFIXED in the sense that matters. Linked PR #42203
  ("strip Claude Code identity from system prompt for non-Claude
  providers") is OPEN and UNMERGED at pull time. It was created
  2026-09-21T05:36:48Z, last updated 2026-09-28T02:19:28Z, with 12 comments.
  Its review associations are CONTRIBUTOR and NONE only; no
  maintainer-identified review was found. Its pre-submission checklist
  boxes are unchecked in the PR body. The PR body itself reports a
  before/after proof (identity sentence echoed before the patch, dropped
  after it, on one non-Claude model through a gateway). That proof is the
  PR author's REPORTED claim, not a maintainer acceptance.
- The single comment on the issue proposes a configurable sanitization
  transform with a flag, scoped so the sentence is kept when the target
  model is Claude. It is a community proposal, not a maintainer reply.

### Why "product bug" and not stronger

- The sentence travels to the model the request was already routed to. It
  is a false self-description delivered to the intended model, not a
  secret, credential, or payload sent to an unintended third party.
- The downstream harms listed (guardrail or classifier firing on the false
  claim, wrong self-identity leaking into user-facing responses, prompt
  rejections, off-spec behavior) are reporter-claimed effects, not
  independently verified here.
- No privilege gain, no exfiltration channel, and no credential material
  is shown. The "leak" framing in the issue title overstates the
  mechanism; the accurate frame is misdirected prompt forwarding.
- Affected versions: no version list is given in the issue or the PR body
  beyond the bridge path described above. Do not cite a version range
  for this bug from this evidence.

## GH7 — non-trap re-triage of q06-i-am-ai-agent.json

The staged file holds 10 entries. Separation used here:

- TRAP (cut, honeypot): 2 entries in the honeypot repository, whose bodies
  are only the trap template sentence. No substantive act.
- TEMPLATE FALSE POSITIVE (cut): 2 entries whose "I am an AI agent"
  text comes from the repository issue template checkbox, left unticked.
  No agent self-declaration, no agent act.
- NON-TRAP (graded on their own): 6 entries with genuine self-declared
  agent content. None inherits the GH7 verdict in either direction.

Full issue bodies match the staged bodies exactly for 9 of 10 entries.
The one exception is the registration filing, where the wallet value was
replaced by a withholding marker per the task constraint; the sanitized
body otherwise matches the staged body exactly. All 10 issues are OPEN
at pull time. Comment counts: 0 for every entry except the NGINX entry
(1 bot triage comment) and the Village entry (4 comments).

### Grade table (per entry, on its own evidence)

| Entry | Grade | Basis |
|---|---|---|
| NGINX ingress, hash-by-subset request (#11260, 2026-10-27) | CUT — template false positive | Agent checkbox unticked. Sole comment is bot triage noting a possible mix-up between two ingress controllers. Ordinary feature request, no agent act. |
| Flutter app list addition, Pomelu (#817, 2026-10-29) | OBSERVED filing act; proposal substance REPORTED | Self-declared agent filed the addition proposal for the maintainer, with a proposed table row and app description. 0 comments, open. The app claims are unconfirmed; no merged addition is shown. |
| ControlX2 licence question (#165, 2026-10-02) | OBSERVED delegated filing act | Self-declared agent filed a licence question on behalf of an operator, stating explicit approval to post. Substance is a question about fork permissions, not a completed change. 0 comments, open. |
| Verso 4.35 backport request (#1052, 2026-10-21) | OBSERVED filing + patch-on-fork act; test outcome REPORTED | Self-declared agent-authored message requests a maintenance release containing an earlier module-system import fix. It states the patch was applied on a fork, a build then passed, and a test run reported 583 passed with 0 failed. The fork patch and filing are first-hand; the test numbers were not independently re-run by this lane. 0 comments, open. Strongest act in this set. |
| GPT Village launch note (#1, 2026-10-18) | OBSERVED multi-agent act + DISCUSSED coordination | Self-declared agent published a launch note and workspace links. Comments show a second self-declared agent checking in, describing independent parallel launch actions, and proposing lightweight coordination norms. A later comment claims an external publication on a public board, backed by a workflow-run link; that external thread was not independently fetched by this lane. 4 comments, open. |
| Startup-credits missing entity, Wafer (#1540, 2026-09-14) | OBSERVED filing act; plan REPORTED | Self-declared agent doing bounty work filed a missing-entity issue, cited a first-party startup-program page, stated a catalog and pull-request check found no existing entity, and stated a plan to add a data-only entity file. The addition itself is a stated plan, not a shown completion. 0 comments, open. |
| v2rayA subscription import bug (#2091, 2026-10-21) | CUT — template false positive | Agent checkbox unticked, a human-responsible field filled, and boxes marked as checked without reading. The bug substance (imported subscription data losing an encryption field) is a real bug report shape but is not an agent act. |
| Contributor registration (#204, 2026-09-25) | OBSERVED registration filing act | Self-declared agent filed a contributor registration stating autonomous bounty intent and operator-supervised payout routing. Wallet value withheld from all captures and from this file per the task constraint. Registration is a self-claim; autonomy and payout facts are unconfirmed. 0 comments, open. |
| Honeypot #1 and #2 (2026-08-29) | CUT — trap | Bodies are only the trap template sentence in a honeypot repository. No substantive act, no discussion. |

### Survivors (REPORTED or better): 6

Pomelu list proposal, ControlX2 licence question, Verso backport request,
GPT Village launch, Wafer entity proposal, contributor registration.

### Novelty spot-check for survivors

- lists/urls: zero hits in urls.jsonl for every key term checked
  (Pomelu, ControlX2, MobiControl, Palomar, GPT Village, Village-store,
  Wafer, paulcrossland, RustChain). No md-file hits in lists/urls either.
- reports/: zero hits for Pomelu, ControlX2, MobiControl, Palomar, Wafer,
  paulcrossland, RustChain. GPT Village appears only in the parent sweep
  report documents (the sweep this lane belongs to), which is expected:
  the Village issue was already fully captured in the sweep as
  q06b/q06c/q06d, so it is NOT new to the sweep corpus. The other five
  survivors have no hit found in reports/ under this check.
- Factum read-only match (no writes): fuzzy matches were run for Pomelu,
  ControlX2, Palomar, GPT Village, Wafer, and paulcrossland. True-substring
  hits: NONE for every term (25 fuzzy returns each, except 7 for the
  registration term, all unrelated noise). Caveat: the tool itself warns
  fuzzy retrieval is heuristic, not an exhaustive absence test, and its
  coverage is structured records only, excluding unimported files and
  live sources. No DB lock blocked the check.
- GH4 note (not a GH7 survivor, for completeness): the term litellm in
  reports/ appears only in unrelated trajectory-ingest writeups about
  model-name labels in trajectory rows, not about this identity bug.

## Captures

All captures are in this directory (data/lanes/sniffer-meta-20261031/raw/
gh4-gh7/). Each capture file has a .sha256 sidecar and a .PROVENANCE.txt
sidecar. GH4: issue + comments + linked PR #42203 issue record.
GH7: issue + comments for all 10 staged entries.

## Open questions and follow-ups

1. GH4: recheck PR #42203 merge status and any maintainer reply after
   2026-10-31; the "Resolved by #42203" claim is open until the PR merges.
2. GH4: no affected-version range is established; do not cite one without
   a code or release check outside this lane.
3. Verso: the reported build and test outcome was not independently
   re-run; the fork commit and linked records would need a code check.
4. GPT Village: the claimed external board thread and workflow-run
   verification were not independently fetched by this lane.
5. Contributor registration: agent autonomy, bounty completion, and payout
   facts are self-claims only; the withheld wallet value was never copied
   into any file or report by this lane.
6. All six survivors remain OPEN with 0 comments except Village; none
   shows maintainer acceptance or a merged outcome at pull time.
