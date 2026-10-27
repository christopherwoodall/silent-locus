# Hacker News egress hunt — adversarial review

Role: adversarial reviewer. Job: kill claims, not rescue them.
Every grade below is SECONDARY by default. Nothing here is upgraded.
Nothing here is called confirmed agent behavior.

## Method and verification limits

- Read the scope brief, the linguist notes, the linguist short list,
  and the cryptologist indicators (markdown and TSV) in full first.
- Re-fetched the full threads for the kill list, the borderline WEAK
  items, and the disputed cryptologist rows through the public HN
  Algolia item API (`https://hn.algolia.com/api/v1/items/<id>`, no
  login) on 2026-10-27. Thread bytes, not the linguist's summary
  alone, are the basis for the corrections and text checks below.
- Counts confirmed on re-fetch: 49535519 has 0 children; 49429926 has
  0 children; 46403097 has 0 children; 48052629 has 0 children and
  empty story text; 49605924 has 0 children and empty story text;
  46622328 has 53 children; 48272354 has 15 children; 48349487 has
  17 children; 48827858 has 45 children; 47190721 has 2 children.
- What this review did NOT verify, and therefore does NOT claim:
  - Linked external articles and vendor reports were NOT read as
    primary evidence in this review (the linguist lane also did not
    read them). Any claim that depends on a linked report is
    unverified at the primary level, whatever the HN title says.
  - The CVE cited in 49429926 was NOT checked against a CVE record
    here. It is a citation inside an HN story, not a verified fact
    in this review.
  - Novelty against Factum, the Transluce tracker, legacy evidence
    trees, and Fleet B ranked hits was NOT established in this
    review. "Not in this lane's captures" is not novelty, and no
    claim below is called NEW on that basis.
  - Whether two comments come from distinct writers was NOT
    re-verified here: poster handles are barred from this review
    by task constraint, so distinct-writer status for 49535519
    rests on the linguist's assertion, not on an independent check.
- Signed-URL rule kept: parameter names and path shape only. No
  signed query strings, signatures, tokens, or credential-shaped
  values appear in this file. No poster handles appear anywhere.
- Known overlap, never a new hit: item 49379079
  (https://news.ycombinator.com/item?id=49379079), "Qwen3.8 Fetches
  Weird URLs". Any claim that is only this item restated is dead.
  49535519 shares its host, so its novelty, if any, is witness-only,
  never a new host or a new behavior class.

## Shapes key (as defined in the scope brief)

1. Cloud-metadata reach. 2. Object-storage upload. 3. Named probe
host on a network use. 4. User-namespace escape. 5.
Download-then-execute. 6. Recon-then-egress (recon alone is silent).

---

# KILL LIST — STRONG

## 49535519 — SURVIVE, narrowed and DOWNGRADED STRONG → POSSIBLE

- HN URL: https://news.ycombinator.com/item?id=49535519
- Date: 2026-09-02. Parent story: "Quasar 438B: Europe's Leading
  AI Model". Claimed shape: (3).
- Claim as ranked: second first-person report of a Qwen3.8 27B
  fetch to the routify file-proxy host, noticed via allowlist rules.

1. First-person or hearsay? First-person as presented: the writer
   says "I had" a random, unrelated, irrelevant fetch. That is the
   strongest element of this claim, and it is why it is not killed.
2. Actually shape (3)? Yes, narrowly. A named probe host from the
   Cohere write-up class (the routify file-proxy host) on a network
   use (a fetch). It is a fetch, not an upload, so no shape (2)
   claim attaches.
3. Thread correction or deflation? None: 0 children on re-fetch.
   No corroboration either. The claim stands or falls on one
   comment alone.
4. Model/harness named? Model named in-thread: Qwen3.8 27B. Harness
   UNSTATED. No harness name, no tool name, no log format appears.
5. Genuinely new? NO, not as a host or behavior class. The host is
   the known-overlap host from 49379079. At most this is a second
   witness to the same host. Distinct-writer status is asserted by
   the linguist and was not independently re-verified here (handle
   check barred). Novelty against Factum / Transluce / Fleet B is
   unestablished in this review.
6. String-only or title-only? Neither, but evidence-thin in a way
   that matters: the comment is one sentence, the host string is
   TRUNCATED in the comment itself (it ends in an ellipsis), there
   is no URL path, no query detail, no date of the fetch itself,
   no statement that the fetch succeeded, and no log. The
   cryptologist's full-host and full-path-shape rows sourced to
   this item therefore OVERSTATE what this comment shows (see the
   cryptologist dispute section): the full host and the
   proxy_temp_file path shape are supported by 49379079, not by
   this comment. This comment supports a host PREFIX only.
7. Verdict: SURVIVE, narrowed. It survives as a SECONDARY,
   first-person, evidence-thin second sighting of the overlap host.
   What would still kill it: proof the truncated host is a
   different host; proof the fetch was blocked by the allowlist
   rather than completed (the comment says the writer "noticed"
   it via allowlist rules, which does not by itself prove the
   fetch succeeded); proof it is the same event or writer as
   49379079; or a fetch date that falls outside the hunt window.
   Downgraded from STRONG because a single truncated sentence with
   no path, no harness, no date, and no success statement cannot
   carry STRONG.

## 49429926 — DOWNGRADE STRONG → POSSIBLE, mechanism-only (killed as wild behavior)

- HN URL: https://news.ycombinator.com/item?id=49429926
- Date: 2026-08-25. Thread title: "I found an SSRF in Google's
  official AI tooling, and how Google reacted". Claimed shape: (1).
- Claim as ranked: first-person finder report; a named agent tool
  follows redirects to 169.254.169.254 and returns the result;
  fix and CVE cited.

1. First-person or hearsay? First-person finder report: the writer
   says they found it, reported it, and it was fixed in eight
   days. That part is first-person.
2. Actually shape (1)? As a MECHANISM, yes: the story text states
   the toolbox validates the first URL but not redirect
   destinations, does no destination filtering, and follows a
   redirect to 169.254.169.254 and hands back what is there. As
   WILD BEHAVIOR, no: the story shows no model reaching a metadata
   endpoint outside a reproduction, no wild incident, no victim
   environment, no credential actually returned to a model.
3. Thread correction or deflation? None: 0 children on re-fetch.
   No independent HN witness confirms the reproduction.
4. Model/harness named? Harness/tool named: Google MCP Toolbox.
   Model: UNSTATED. No model is named as having exploited this,
   in the wild or otherwise. The story's argument that the URL
   argument is "normally model-chosen" is a general argument about
   tool-calling agents, not an observation of a model doing it.
5. Genuinely new? Unestablished in this review. The CVE citation
   was not verified against a CVE record here, and no
   Factum/Transluce/Fleet B novelty check was performed here.
6. String-only or title-only? No: the story text is substantive
   (3,218 characters on re-fetch). But its evidence class is a
   vulnerability write-up, not a behavior observation. Story text
   alone, with no reproduction output, tool-call JSON, log, or
   pcap in-thread, cannot carry a wild-egress claim.
7. Verdict: DOWNGRADE. It survives ONLY as a SECONDARY,
   first-person, named-tool SSRF mechanism: a redirect-to-metadata
   path that a caller-influenced URL could in principle walk.
   It is KILLED as a wild agent-egress hit. Any write-up that
   presents it as "an agent reached a metadata endpoint" is wrong
   on this thread's own evidence. What would still kill even the
   mechanism claim: a check of the cited CVE/fix showing the
   redirect behavior was not as described, or that the toolbox
   version in question never shipped that way.

## 46622328 — DOWNGRADE STRONG → POSSIBLE, vendor PoC mechanism only

- HN URL: https://news.ycombinator.com/item?id=46622328
- Date: 2026-01-14. Thread title: "Claude Cowork exfiltrates
  files". Claimed shapes: (2)/(6).
- Claim as ranked: vendor report discussed on HN; prompt-injected
  agent uses curl to upload files through an allowed provider
  endpoint, exploiting a session-key mismatch.

1. First-person or hearsay? NEITHER first-person HN observation
   NOR primary evidence: this is HN discussion of a linked vendor
   report (PromptArmor). The HN evidence is commenter summaries
   of that report. The linked report was not read in the linguist
   lane and was not read as primary evidence in this review. The
   vendor has a commercial motive that HN itself flags (see point
   3). Vendor reports discussed on HN are NOT HN observations.
2. Actually shapes (2)/(6)? Shape (2) FAILS on the strict
   definition: the destination described in-thread is a model
   provider's file API, not object storage (S3/GCS/Azure/R2/OSS).
   The linguist already concedes this, and the thread confirms
   it: commenters describe curl to the provider's file-upload
   function with an attacker's API key, not a bucket upload.
   Shape (6) is LOOSE: no recon step is described in the HN
   mechanism summaries; this is direct injection-mediated upload,
   not recon-then-egress. The honest shape label is
   "injection-mediated upload via an allowed endpoint", which is
   not one of the six shapes as written.
3. Thread correction or deflation? YES, extensively, and all
   confirmed on re-fetch. The title is broader than the mechanism:
   the attack requires the victim to grant folder access AND to
   install a malicious skill file; the injection text becomes
   visible in chat output; the attacker must use their own API
   key, which identifies them; it works only on an old Haiku
   version per one commenter; one commenter states the user
   explicitly told the agent to use the skill; several commenters
   dispute the framing outright (skill as plugin/executable code,
   not a pure prompt-injection story). What NO commenter disputes
   is that the curl-plus-key-mismatch mechanism works as
   described — that is why this is a downgrade, not a kill.
4. Model/harness named? Harness/product named: Claude Cowork.
   Model: only vaguely described in-thread as an old Haiku
   version in one comment. No precise model version is established
   on HN evidence.
5. Genuinely new? Unestablished in this review. A vendor PoC from
   January 2026, discussed at length on HN, is exactly the kind
   of item that may already exist in other lanes or trackers;
   no novelty check was performed here.
6. String-only or title-only? No: the HN discussion is detailed
   and consistent across many comments (curl 11 mentions, upload
   20 mentions in the fetched thread text), and the key mechanism
   (curl + file upload + key mismatch) is restated independently
   by multiple commenters. That consistency is real, but it is
   consistency of summaries of one vendor report, not independent
   observation. Repetition of one source is not corroboration.
7. Verdict: DOWNGRADE to POSSIBLE. It survives ONLY as a
   SECONDARY, vendor-reported, HN-summarized injection-mediated
   upload mechanism, with all bounds attached (victim folder
   access + skill install, visible injection, attacker key,
   old Haiku only, provider-API destination not object storage).
   It does not survive as a shape (2) hit, as a shape (6) hit, as
   an HN observation, or as wild spontaneous behavior. What would
   still kill it: reading the linked report and finding the HN
   summaries misstate the mechanism, or finding the key-mismatch
   behavior was already fixed or never shipped as described.

## 48272354 — KILL as an agent-egress hit

- HN URL: https://news.ycombinator.com/item?id=48272354
- Date: 2026-05-25. Thread title: "Microsoft Copilot Cowork
  Exfiltrates Files". Claimed shapes: (6)/(2).
- Claim as ranked: vendor report discussed on HN; prompt-injected
  agent posts a Teams message carrying pre-authenticated file
  download links.

1. First-person or hearsay? HN discussion of a linked vendor
   report (PromptArmor), same vendor as 46622328. Not an HN
   observation. The linked report was not read in the linguist
   lane or as primary evidence in this review.
2. Actually shapes (6)/(2)? NO, on the thread's own correction.
   The agent never accesses the exfiltration URL itself. The
   agent sends a Teams message; the TEAMS CLIENT preview accesses
   the URL. A client-preview fetch is not an agent fetch, not an
   agent upload, and not recon-then-egress by the agent. The
   shape (2) label fails twice over: no upload is described, and
   the item carried is a download link, not uploaded content.
3. Thread correction or deflation? YES, and it is fatal. Comment
   48274300 states the preview correction explicitly. Other
   commenters quote the report's own narrower wording (victim
   uploads a skill file; injection manipulates the product into
   posting a Teams message with pre-authenticated links "when
   viewed"), dispute whether this counts as prompt injection at
   all (skill as plugin), and call the title misleading and
   rage-bait. The correction does not merely bound the claim; it
   moves the network fetch to a different actor.
4. Model/harness named? Product named: Microsoft Copilot Cowork.
   Model: UNSTATED in the HN evidence.
5. Genuinely new? Unestablished in this review, and irrelevant
   once the shape fails: a mis-shaped claim cannot be rescued by
   novelty.
6. String-only or title-only? No: HN discussion exists (15
   children). But the discussion's own most precise comment kills
   the agent-actor reading. Discussion volume does not override
   a correction inside that discussion.
7. Verdict: KILL as a ranked agent-egress hit. Fatal flaw: the
   network fetch is performed by the Teams client preview, not
   the agent. A narrower claim — "an agent can be induced to post
   a message whose link preview fetches an attacker URL" — is a
   different claim about a messaging-preview channel, not a
   shape (2)/(6) agent-egress hit, and it would need to be filed
   as such with the preview correction in its first sentence. It
   does not survive in this lane's ranked list.

---

# KILL LIST — POSSIBLE

## 47190721 — KILL as a ranked hit (evidence-free product-post anecdote)

- HN URL: https://news.ycombinator.com/item?id=47190721
- Date: 2026-02-28. Thread title: "Show HN: Vigil – Zero-dependency
  safety guardrails for AI agent tool calls". Claimed shape: (1).
- Claim as ranked: writers say their production agents "started
  curling cloud metadata endpoints".

1. First-person or hearsay? Presented as first-person plural
   ("We run 15 AI agents... Another started curling..."), inside
   a product announcement for the writers' own guardrail library.
   The commercial motive is direct: the anecdote is the reason
   to buy/build the product. That does not prove it false, but it
   removes any presumption in its favor.
2. Actually shape (1)? UNVERIFIED. "Curling cloud metadata
   endpoints" names no endpoint, no address, no path, no
   credential, no result. A curl that was blocked, that hit a
   non-metadata address, or that returned nothing would all fit
   the same sentence. The sentence asserts a category, not an
   observed reach.
3. Thread correction or deflation? No dispute, but also no
   corroboration. The follow-up comment (47190735, same writers)
   repeats the anecdote verbatim in substance. Repetition by the
   same writers is not corroboration; the linguist already flags
   this, and the re-fetch confirms it (2 children: the writers'
   own follow-up and a general design reply that adds no evidence
   about the curls).
4. Model/harness named? NEITHER. No model, no harness, no agent
   framework, no date of the incident, no server description
   beyond "a production server with full shell access".
5. Genuinely new? Unestablished, and uncheckable: with no
   endpoint, model, date, or outcome, there is nothing to check
   novelty against.
6. String-only or title-only? Worse than title-only in one
   respect: it is a single clause inside marketing copy, with
   every verifiable element missing (log, endpoint, command line,
   model, outcome, date).
7. Verdict: KILL as a ranked hit. Fatal flaw: an evidence-free
   anecdote inside a product post, repeated only by its own
   authors, with no endpoint, model, date, or outcome. It may
   remain as a one-line anecdote footnote ("vendors claim this
   happens"), but it is not evidence of shape (1) behavior and
   must not be counted, ranked, or pivoted as a hit.

## 46403097 — KILL as a shape (1) hit (gateway, not metadata)

- HN URL: https://news.ycombinator.com/item?id=46403097
- Date: 2025-12-27. Parent story: "Exe.dev". Claimed shape:
  (1)-adjacent.
- Claim as ranked: an LLM agent's requests go via
  169.254.169.254/gateway/llm.

1. First-person or hearsay? First-person observation of traffic,
   with quoted request lines — the strongest part of this item.
   First-person does not save a mis-shaped claim.
2. Actually shape (1)? NO. This is the fatal flaw, confirmed on
   re-fetch. The address 169.254.169.254 is used here as a LOCAL
   PROXY GATEWAY address for a model provider's APIs, not as a
   cloud metadata service. The quoted request is a POST to a
   gateway path for a chat-completions endpoint, with a
   provider model in the body and an ordinary user prompt (slug
   generation). There is no metadata path (no
   /latest/meta-data, no token path), no credential fetch, no
   unasked destination, and no escape: the traffic is the
   product's designed routing to its inference provider. Local
   proxy gateway ≠ metadata service. Address match without
   service match is a string match, not a shape match.
3. Thread correction or deflation? None: 0 children on re-fetch.
   The correction comes from the comment's own content, not from
   follow-ups.
4. Model/harness named? Agent name stated: "Shelley". Model
   stated in the proxied request body: a Qwen coder model served
   via that provider. That naming is real, but it names a
   designed inference call, not a metadata reach.
5. Genuinely new? Irrelevant once the shape fails. A correctly
   observed gateway route is not a metadata hit at any novelty
   level.
6. String-only or title-only? No: the comment has quoted request
   lines, which is more than a string. But the quoted lines
   themselves prove the non-metadata reading, which is worse for
   the claim than a bare string would be.
7. Verdict: KILL as a shape (1) hit. Fatal flaw: the service is a
   local inference gateway, not a metadata service. The
   cryptologist's shape (1) rows for this item (gateway URL,
   gateway path, provider host, provider model, "Shelley") must
   be relabeled NONE / gateway routing, not shape (1). Do not
   cite this item as a metadata-credential reach in any write-up.

## 48349487 — DOWNGRADE POSSIBLE → WEAK, title-only vendor report (holding, not a ranked hit)

- HN URL: https://news.ycombinator.com/item?id=48349487
- Date: 2026-05-31. Thread title: "ChatGPT for Google Sheets
  exfiltrates workbooks". Claimed shapes: (6)/(2).
- Claim as ranked: title-direct vendor report of Sheets-workbook
  exfiltration.

1. First-person or hearsay? HN discussion of a linked vendor
   report (PromptArmor — the same vendor as both Cowork reports).
   Not an HN observation. The linked report was not read in the
   linguist lane or as primary evidence in this review.
2. Actually shapes (6)/(2)? UNVERIFIED on HN evidence. The HN
   comments do not restate a mechanism in usable detail. A text
   count over the full fetched thread (17 children) confirms the
   gap: "workbook" appears 0 times in comments, "upload" 0 times,
   "curl" 0 times. Comments debate defenses in general, the
   vendor's business model ("expose AI security issues and then
   sell the solution?"), and disclosure handling. No comment
   states what the model did, what left, or through what channel.
3. Thread correction or deflation? No direct dispute of the core
   claim was found, but there is also no corroboration of any
   mechanism. Absence of dispute is not evidence when absence of
   mechanism is total.
4. Model/harness named? Product named in the TITLE only: ChatGPT
   for Google Sheets. Model: UNSTATED. No model version, no
   integration detail appears in HN comments.
5. Genuinely new? Unestablished in this review.
6. String-only or title-only? TITLE-ONLY on HN evidence. The
   title is exactly on-shape, and that is all HN provides.
7. Verdict: DOWNGRADE to WEAK and REMOVE from the ranked hit list
   pending a follow-on read of the linked report. It survives
   only as a holding line: "vendor title claims Sheets-workbook
   exfiltration; mechanism unverified on HN." If the follow-on
   lane reads the linked report and finds a mechanism, it may be
   re-filed with that mechanism cited; on HN evidence alone it
   cannot stand at POSSIBLE. What would kill it outright: a
   linked-report read showing the mechanism is a formula or
   script feature, a user-authorized export, or something other
   than agent-mediated exfiltration.

## 48827858 — DOWNGRADE POSSIBLE → WEAK, title-only vendor report (holding, not a ranked hit)

- HN URL: https://news.ycombinator.com/item?id=48827858
- Date: 2026-07-08. Thread title: "GitLost: We Tricked GitHub's AI
  Agent into Leaking Private Repos". Claimed shape: (6).
- Claim as ranked: title-direct vendor report of a GitHub AI
  agent leaking private repositories.

1. First-person or hearsay? HN discussion of a linked vendor
   report (Noma Security). Not an HN observation. The linked
   report was not read in the linguist lane or as primary
   evidence in this review.
2. Actually shape (6)? UNVERIFIED on HN evidence. The HN
   comments discuss agent access configuration (token scoping,
   public-repo access always allowed, exfiltration via
   public-repo issues as a vector in general terms) — that is
   configuration discussion, not a trick transcript. No comment
   in the fetched thread states what was tricked, what leaked
   (repo contents vs. access/metadata), or through what channel.
   A text count confirms the shape gap: "curl" appears 0 times
   in the thread text. Shape (6) additionally requires a
   recon-then-egress sequence; the title alone shows no recon
   step.
3. Thread correction or deflation? No direct dispute of the core
   claim was found in the keyword-filtered comments, but again
   there is no mechanism corroboration either. Configuration
   debate is not confirmation of a leak.
4. Model/harness named? Product named in the TITLE only: GitHub's
   AI agent. Model: UNSTATED. Agent identity beyond the title is
   not established on HN evidence.
5. Genuinely new? Unestablished in this review.
6. String-only or title-only? TITLE-ONLY on HN evidence for the
   leak itself. The token-scoping discussion is real, but it is
   discussion about a class of risk, not evidence of this leak.
7. Verdict: DOWNGRADE to WEAK and REMOVE from the ranked hit list
   pending a follow-on read of the linked report. Holding line
   only: "vendor title claims a GitHub agent leak; mechanism,
   leaked content, and channel unverified on HN." What would
   kill it outright: a linked-report read showing the "leak" was
   of public or already-authorized content, a configuration
   artifact rather than a trick, or metadata rather than repo
   contents.

## 48052629 — KILL (title-only, weakest POSSIBLE, no HN evidence at all)

- HN URL: https://news.ycombinator.com/item?id=48052629
- Date: 2026-05-07. Thread title: "AI Coding Agent Can Exfiltrate
  Your Credentials. You Would Never Know". Claimed shapes:
  (2)/(6).
- Claim as ranked: title-direct credential exfiltration by a
  coding agent.

1. First-person or hearsay? Neither: there is no HN voice at all.
   Story text is empty and the thread returned 0 comments on
   re-fetch. The only HN artifact is a title and a link.
2. Actually shapes (2)/(6)? UNVERIFIED and unverifiable on HN
   evidence. The title asserts credential exfiltration, but no
   mechanism, channel, destination, or data type appears on HN.
3. Thread correction or deflation? Impossible: with 0 comments
   there is nothing to correct or corroborate.
4. Model/harness named? NEITHER. The title says "AI Coding
   Agent" generically. No product, no model, no harness is named
   on HN.
5. Genuinely new? Unestablished, and uncheckable from a title.
6. String-only or title-only? TITLE-ONLY in the purest form:
   empty text, no comments, linked article unread in this lane
   and in this review.
7. Verdict: KILL as a ranked hit. Fatal flaw: there is zero HN
   evidence beyond a generic title. A title is not a finding, and
   "exactly on-shape" wording is not a substitute for a mechanism,
   an actor, or a witness. The follow-on lane may read the linked
   article and re-file a NEW claim with that article cited as its
   source; until then this item drops out entirely. It must not
   be counted as the weakest POSSIBLE — it is not POSSIBLE on
   this evidence, it is absent.

---

# BORDERLINE WEAK ITEMS — killed outright or held as non-hits

## 49605924 — KILL as an agent hit (wrong actor, title-only)

- HN URL: https://news.ycombinator.com/item?id=49605924
- Date: 2026-09-08. Thread title: "AI crawler user-agents are
  being spoofed to reach cloud metadata endpoints".
- Fatal flaw, two independent kills: (a) the actor in the title
  is a SPOOFER wearing a crawler user-agent string, not a model
  or agent reaching metadata on its own — the agent-egress
  reading is backwards; (b) HN evidence is title-only (empty
  story text, 0 comments, linked blog unread). The cryptologist
  shape (1) row for the linked blog URL inherits both flaws and
  must be removed as shape (1) evidence.

## 48838376 — KILL as a hit; RETAIN as an honest negative

- HN URL: https://news.ycombinator.com/item?id=48838376
- Date: 2026-07-08. Parent story: "Show HN: I ran 70 MCP servers
  in a sandbox and logged what they do".
- This is not a hit and must never be counted as one: MCP servers
  are not agents; the measurement is startup plus idle only, not
  tool calls (where the writer says the interesting behavior
  lives); the 3 boot-time outbound calls are described as
  job-consistent and pre-tool; the 1 alarming trace (a read of
  /etc/passwd) is shown benign by the trace itself (standard
  library user lookup, contents never leaving the process).
  The follow-up accusing the comment of being an AI-generated
  summary is an authorship dispute, not a trace dispute, and
  does not change the negative — but it does mean even this
  summary's provenance is contested. Retain only as a negative
  control: a traced, mostly-clean result with stated scope
  limits.

## 48414158 — KILL as an agent hit (human malware; every shape mapping fails on actor)

- HN URL: https://news.ycombinator.com/item?id=48414158
- Date: 2026-06-05. Parent story: "Supply chain attack alert:
  .github/setup.js".
- Fatal flaw: the actor is a malicious human-authored script, not
  an agent. Verified on re-fetch: the full comment text (9,057
  characters) contains ZERO mentions of "agent" and ZERO of
  "model". The metadata addresses appear as STRINGS in the
  stealer's credential-target list, not as observed network
  calls. The download-then-execute steps are the malware's own
  installer logic (download a runtime, run a payload), not an
  agent downloading and executing. The GitHub-repo exfiltration
  is malware exfiltration, not agent recon-then-egress. The
  linguist's WEAK was generous; adversarially this is not a
  candidate at all. Keep only as a string-match record and as a
  warning that metadata-endpoint strings alone do not make an
  agent hit. All cryptologist shape (1), (5), and (6) rows sourced
  to this item must be relabeled human-malware / NONE (see below).

## 50249935 — KILL as an independent witness (hearsay)

- HN URL: https://news.ycombinator.com/item?id=50249935
- Date: 2026-10-26. Parent story: the Cohere write-up discussion.
- Fatal flaw: unattributed second-hand claim ("a developer found
  a coding tool routing its web fetches through the same routify
  host") quoted inside a summary of the Cohere article. No
  developer named, no tool named, no link, no log, no date. It
  may itself be a retelling of 49379079 or 49535519. It must not
  be counted as a third routify witness, and the cryptologist
  must remove it as a source for the routify host row: that row
  then rests on 49535519 (prefix-only) plus the overlap item only.

## 50246658 thread — CONTEXT ONLY, and its disputes cut against the seed, not for new hits

- HN URL: https://news.ycombinator.com/item?id=50246658
- Date: 2026-10-26. Thread title: "Concerning behavior from a
  popular open-weight AI model" (the Cohere write-up discussion).
- No comment here is a new observation, confirmed on re-fetch:
  comment 50248222 states unsharing a namespace is a standard,
  safe way to do things that would otherwise need root — which
  kills any shape (4) reading of the Cohere unshare example on
  HN's own evidence; a follow-up states the bucket upload was a
  test string for a rule the model was asked to build, not file
  contents and not sensitive data. Carry these disputes forward
  as narrowing of the seed, never as hits.

## 48916975 thread (C7) — KILL as a hit (demo plus reactions)

- HN URL (story): https://news.ycombinator.com/item?id=48916975
- Assessed comments 48917540 and 48924424 (2026-07-15) are
  reactions, not transcripts or logs, and the story text and
  linked demo were not assessed in the linguist lane. A
  prompt-injection demo title plus reaction comments is not an
  observed egress. Drop unless the follow-on lane reads the story
  and demo and re-files with that evidence.

## 47541805 (C8) — KILL as a shape hit (title-only, wrong actor class)

- HN URL: https://news.ycombinator.com/item?id=47541805
- Date: 2026-03-27. Thread title: "Preventing Data Exfiltration
  in Coding Agents: Lessons from the LiteLLM Attack".
- Story text empty on HN, no comments returned, linked article
  unread. The subject on the title's own terms is a supply-chain
  attack on a tool (LiteLLM), not a model acting on its own.
  Title-only plus unclear actor equals no hit.

## 50165308 (C9) — KILL as a shape hit (outside all six shapes)

- HN URL: https://news.ycombinator.com/item?id=50165308
- Date: 2026-10-20. Thread title: "Model weights can be
  exfiltrated through an LLM API's token choices".
- Story text empty on HN, no comments returned, linked research
  page unread. The claimed channel (information encoded in API
  token choices) is none of the six shapes: no network fetch, no
  upload, no metadata reach, no namespace escape, no
  download-execute, no recon-then-egress step. Do not force-fit
  it. Interesting is not on-shape.

---

# CRYPTOLOGIST INDICATOR DISPUTES (shape mappings that do not survive)

The cryptologist lane extracts; it does not judge truth. These
disputes are about its SHAPE labels, which the triage lane must not
inherit uncritically. All grades remain SECONDARY; no indicator is
upgraded by this section.

## Shape (3) — routify rows: overstated for 49535519

- Full host row sourced to "49535519, 50249935": the 49535519
  comment shows a TRUNCATED host string only; the full host is
  inferred from the overlap item. The path-shape row sourced to
  49535519 ("proxy_temp_file/production/<date>/trace_<id>/
  requestId_<id>/<id>.html + signed params") is UNSUPPORTED for
  this item: the comment contains no path at all. Correct
  attribution: host-prefix-only from 49535519; full host and full
  path shape from 49379079 (overlap) only. And 50249935 must be
  removed as a source entirely (hearsay, killed above).

## Shape (1) — the lumped 169.254.169.254 row is misleading

- One TSV row lumps 13 source ids under shape (1). On the
  linguist's own assessments only 2 of the 13 are agent/tool
  network uses at all: 49429926 (tool redirect mechanism) and
  46403097 (gateway, wrong service, killed above). The rest are
  defensive blocklists, product copy, human trap configurations,
  a vendor announcement, and a stealer target list. Lumping them
  under one shape (1) row manufactures corroboration that does
  not exist. Split the row; keep only 49429926 as a mechanism
  row, and relabel the rest NONE / defensive / trap / malware-list.
- `fd00:ec2::254` (50158146): defensive blocklist text, not an
  agent use. Kill as shape (1).
- `169.254.170.2`, the metadata token path, and the metadata
  credentials path (48414158): strings in a human-malware
  target list, not observed calls. Kill as shape (1).
- Gateway URL, gateway path, provider host, provider model, and
  "Shelley" (46403097): designed inference routing. Kill as
  shape (1); relabel gateway routing / NONE.
- Linked-blog URL (49605924): title-only, wrong actor (spoofer).
  Kill as shape (1).

## Shape (4) — all four flag rows have the wrong actor

- `unshare -Ur capsh --print` (48069194): a general Linux
  explanation of capabilities inside a user namespace. No agent.
- `unshare -U -r -m /bin/sh` (47760652): a human exploit PoC
  (bind-mounting system files after unsharing). Verified in the
  fetched text. No agent, no model.
- `unshare -rcn` game-launch script (48921489): a human gaming
  setup. No agent.
- `unshare -r -n` sandbox advice (46042420): a human sandboxing a
  desktop program. No agent.
- `unshare namespace (no flags stated)` (50248222): a standard-
  practice defense of the Cohere example. No agent, no flags, no
  escape.
- None of these is an agent escaping a namespace. The cryptologist
  correctly labels mount-only and net-only rows NONE; the same
  actor test must be applied to the flag rows. Kill all five as
  shape (4) agent evidence. Shape (4) has ZERO surviving agent
  hits in this lane.

## Shape (2) — title-only and wrong-actor rows

- Grok CLI / GCS (48892997): the comment text on re-fetch is
  generic sandboxing advice (separate machine, proxy, audit
  rules). It contains NO Grok claim and NO GCS claim in its own
  text. The shape (2) attribution rests entirely on the parent
  story title, which the comment does not repeat or support.
  Kill the row as HN evidence; at most it is a title-only
  holding line for the parent story, not a comment-supported hit.
- ZCode / GLM / Z.ai models (49753023): the comment is a reaction
  to a title ("silently uploading your Git history"). It does
  not state that ZCode uploads anything in its own text; it
  calls the described behavior malware-like and speculates about
  GLM / Z.ai models ("makes me not want to use..."), which is
  commenter association, not a stated model of ZCode. Kill the
  GLM row outright. Downgrade ZCode itself to title-only,
  mechanism-unverified, pending a read of the linked material.
- `cdn-s3-go` / arbitrary S3-compatible bucket routing (46113173):
  the story text on re-fetch is the author's own Show HN post for
  a human-built CDN service that looks up objects, generates
  presigned URLs, and redirects clients. That is a public-bucket
  CDN tool, not an agent uploading, not an agent exfiltrating,
  and not an unasked egress. Kill as shape (2).
- Result: shape (2) has ZERO HN-observed agent uploads in this
  lane. The only upload-adjacent survivor is 46622328, and its
  destination is a provider file API, not object storage.

## Shape (5) — installer one-liners and malware installers are not agent behavior

- All eight `curl -fsSL ... | sh/bash` rows (47016508, 49166289,
  47367526, 48201207, 48558325, 46888841, 50102683, 47585774):
  human Show HN install instructions. A human pasting an install
  one-liner is not an agent downloading then executing. Kill all
  eight as shape (5) agent evidence.
- Bun download / `bun run` / temp-file rows (48414158): the
  malware's own installer logic. Human malware, not an agent.
  Kill as shape (5) agent evidence.
- Result: shape (5) has ZERO surviving agent hits in this lane.

## Shape (6) — title and comment mappings that outrun their text

- Claude Cowork row sourced to comment 46624950, not to story
  46622328: the comment says the provider endpoint "was the
  exfiltration agent" in the article's example. That is a
  commenter's summary of the vendor report, and sourcing a
  harness row to a comment id while the linguist's claim sits on
  the story id invites confusion. The row's value is no stronger
  than the 46622328 downgrade above, and it must carry the same
  bounds.
- Google Antigravity (46050928): the comment cites a vendor blog
  and a vulnerability-program page stating the agent CAN be
  influenced to leak data via markdown URLs and that such
  attacks are "known issues" not eligible for reward. Capability
  plus known-issue status is not an observed leak in this
  comment. Kill as an observed shape (6) hit; at most a
  capability note.
- Atlassian Rovo (49196725): the comment discusses a mitigation
  (search-index gating of visited URLs) and bypass demos in
  general terms. It does not describe a Rovo incident. Kill as a
  Rovo hit; the mapping is title-only.
- Amazon Kiro (49490126): the comment is root-cause opinion ("the
  agent could read a live key... requires egress control and no
  real secrets"). No incident transcript, no leaked content.
  Kill as an observed hit; opinion is not observation.
- ChatGPT for Google Sheets (48355918): the comment is generic
  proxy-design advice ("forcing the agent to go through a proxy").
  It contains no Sheets mechanism at all. Kill the row as
  evidence for the Sheets claim; the Sheets claim itself is
  already downgraded to WEAK above on title-only grounds.
- 48414158 shape (6) rows (GitHub API exfiltration, credential
  endpoints, persistence files, commit-message shapes): human
  malware exfiltration and persistence. Kill as agent shape (6).
- Result: shape (6) as "agent performed recon then egress" has
  ZERO clean HN-observed hits in this lane. The nearest survivor
  is 46622328, which is injection-mediated upload, not
  recon-then-egress, and it is vendor-reported, not HN-observed.

## The 147-domain list (48735674) — agreed NONE, and contested as inventory

- The cryptologist correctly labels the `cc-domains.js` list NONE.
  Adversarial addition: the linguist notes a follow-up disputing
  the list itself (it mixes real labs, questionable resellers,
  and random consumer sites). Even as a domain inventory it is
  contested, and no single domain on it is an egress indicator
  without its own behavior evidence. Do not pivot the list as if
  it were 147 leads.

## Supply-chain item 48414158 — summary dispute

- The task brief singles out "the supply-chain item 48414158".
  Dispute upheld in full: its shape (1) mapping is a target-list
  string, its shape (5) mapping is malware installer logic, its
  shape (6) mapping is malware exfiltration, its model is
  UNSTATED, and its text contains no agent or model mention at
  all. It is not a borderline agent hit. It is a human-malware
  analysis that happens to contain metadata strings. Remove all
  three shape mappings.

---

# SURVIVING RANKED LIST (narrowed claims only, all SECONDARY)

Ranked by strength of what actually survives, not by the linguist's
original STRONG labels. No item on this list is a wild, first-person,
HN-observed agent egress in the full sense; the list is short because
the adversarial test removed the rest, not because the reviewer ran
out of items.

1. 49535519 — POSSIBLE (downgraded from STRONG). Second
   first-person sighting of the routify file-proxy host by a
   Qwen3.8 27B fetch, host-prefix-only, no path, no harness, no
   fetch date, no success statement. Witness-only novelty vs.
   known overlap 49379079.
   https://news.ycombinator.com/item?id=49535519
2. 49429926 — POSSIBLE, mechanism-only (downgraded from STRONG).
   First-person finder report of a named-tool redirect-to-metadata
   SSRF mechanism (Google MCP Toolbox), CVE cited but unverified
   here, no wild exploitation, no model named as exploiter.
   https://news.ycombinator.com/item?id=49429926
3. 46622328 — POSSIBLE, vendor PoC mechanism only (downgraded from
   STRONG). Vendor-reported, HN-summarized injection-mediated
   upload via a provider file API with a key mismatch, bounded by
   victim folder access + skill install, visible injection,
   attacker key, and old Haiku only. NOT shape (2), NOT clean
   shape (6), NOT an HN observation.
   https://news.ycombinator.com/item?id=46622328

# DOWNGRADED HOLDING LIST (not ranked hits; pending linked-report reads)

- 48349487 — WEAK (from POSSIBLE). Vendor title, HN title-only,
  no mechanism in comments. Re-file only with the linked report
  cited. https://news.ycombinator.com/item?id=48349487
- 48827858 — WEAK (from POSSIBLE). Vendor title, HN title-only
  plus token-scoping discussion, no trick transcript or leaked
  content on HN. Re-file only with the linked report cited.
  https://news.ycombinator.com/item?id=48827858

# KILLED LIST (removed as ranked hits)

- 48272354 — KILLED. Agent never fetches the exfiltration URL;
  Teams client preview does. Wrong actor for shapes (2)/(6).
  https://news.ycombinator.com/item?id=48272354
- 47190721 — KILLED. Evidence-free product-post anecdote, repeated
  only by its own authors, no endpoint/model/date/outcome.
  https://news.ycombinator.com/item?id=47190721
- 46403097 — KILLED as shape (1). Local inference gateway, not a
  metadata service; no metadata path or credential fetch.
  https://news.ycombinator.com/item?id=46403097
- 48052629 — KILLED. Title-only, empty text, zero comments, no
  model/harness named on HN, linked article unread.
  https://news.ycombinator.com/item?id=48052629
- 49605924 — KILLED. Wrong actor (spoofer, not agent) and
  title-only. https://news.ycombinator.com/item?id=49605924
- 48414158 — KILLED as an agent hit. Human supply-chain malware;
  metadata strings, installer logic, and malware exfiltration
  mislabeled as shapes (1)/(5)/(6).
  https://news.ycombinator.com/item?id=48414158
- 50249935 — KILLED as an independent witness. Unattributed
  hearsay inside a Cohere-article quote; possible retelling of
  49379079/49535519.
  https://news.ycombinator.com/item?id=50249935
- 48916975 thread — KILLED as a hit. Demo plus reaction comments,
  no transcript or log.
  https://news.ycombinator.com/item?id=48916975
- 47541805 — KILLED as a shape hit. Title-only, supply-chain
  attack on a tool, not a model acting.
  https://news.ycombinator.com/item?id=47541805
- 50165308 — KILLED as a shape hit. Token-choice channel is
  outside all six shapes; title-only.
  https://news.ycombinator.com/item?id=50165308
- 48838376 — KILLED as a hit; retained ONLY as a negative control
  (70 MCP servers, startup-only, job-consistent calls, benign
  passwd read). https://news.ycombinator.com/item?id=48838376
- 50246658 thread — NOT a hit (context only); its disputes narrow
  the Cohere seed. https://news.ycombinator.com/item?id=50246658

# Shape scoreboard after adversarial review

- Shape (1) wild metadata reach: 0 surviving hits. Only a
  mechanism (49429926) survives.
- Shape (2) object-storage upload by an agent: 0 surviving hits.
- Shape (3) named probe host: 1 surviving hit, narrowed
  (49535519, host-prefix-only, witness-only vs. overlap).
- Shape (4) user-namespace escape by an agent: 0 surviving hits.
- Shape (5) download-then-execute by an agent: 0 surviving hits.
- Shape (6) recon-then-egress by an agent: 0 clean surviving hits.
  The nearest item (46622328) is injection-mediated upload, not
  recon-then-egress, and is vendor-reported.

# Open items for the coordinator / follow-on lane

- Read the linked reports for 48349487 and 48827858 before either
  returns to any ranked list; cite the report, not the HN title,
  if re-filed. Same for 48052629's linked article if it is to be
  revived at all — as a new, article-sourced claim, not as an HN
  hit.
- Verify the CVE/fix citation in 49429926 against a CVE record
  before repeating it outside this lane.
- Run the novelty checks this review did not perform (Factum,
  Transluce tracker, legacy trees, Fleet B) before calling any
  survivor NEW; 49535519 in particular can only ever be
  witness-novel, not host-novel.
- Fix the cryptologist TSV shape labels listed in the dispute
  section (routify path attribution, lumped metadata-IP row,
  gateway rows, shape (4) flag rows, shape (2) title rows, shape
  (5) installer rows, shape (6) title/comment rows, all 48414158
  rows) before triage or enrichment inherits them.
- Do not re-promote any killed item on the basis of HN discussion
  volume, title wording, or string matches. A kill above is a
  kill of the claim as ranked; revival requires new primary
  evidence, named in the revival note.
