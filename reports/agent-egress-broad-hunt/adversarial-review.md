# Adversarial review — broad agent-egress hunt

## Terms

- Behavior: an agent did an action. A tool call ran, or traffic left a host.
- Mention: text names a shape. No action ran. A rule, a fix, a test, a doc, or a prompt can mention a shape.
- SECONDARY: evidence from a third party. It is not a first-hand capture by this hunt.
- Shape: a pattern of actions. Example: reach a metadata address, then read a credential.
- Metadata endpoint: a special local address inside a cloud host. It gives data about the host, and sometimes temporary credentials. A credential is a secret that proves identity.
- Object storage: a cloud store for files. A bucket is one named store.
- Harness: the program that runs an agent and gives it tools.
- Sandbox: a contained space where an agent runs.
- User namespace: a wall that keeps a program apart from the host. A program can be root inside the wall, but not root on the host.
- Verdict words: KILL means remove from the ranked list. DOWNGRADE means keep, but at a lower grade. SURVIVE means keep, as stated, with the limits given.

## Headline

No PRIMARY claim was found. No lane made a first-hand capture of a live agent act.

This review kills most ranked items. The items that survive are narrow. They prove capability, a tested gap, or an executed act under an outside order. None proves a spontaneous rogue agent in the wild.

Two checks were run against raw files. First, the cryptologist trace-ID claim was checked in the prior raw file. It holds for 2 IDs in one issue. See claim 11. Second, the ranked GitHub issue URLs were checked in the raw captures. They are present. The Corbanu item sits in q05 as pull 876, with parent issue 826. The LifeSciences item sits in q02.

One gap applies to the whole linguist lane. Its raw dir holds only the two akasecurity issue bodies. It holds no saved page text for NEW-1, NEW-2, NEW-3, or NEW-4. Those four rest on web reads alone. No transcript was filed for any of them.

No Factum write was made here. No file was committed or pushed. No raw file was changed.

## Claim 1 — Linguist NEW-1: Zenity AgentCorruption, shape 1

Verdict: SURVIVE, narrowed. Grade stays SECONDARY.

What survives: an agent on a managed agent platform was prompted to query its own metadata endpoint. It returned temporary role credentials. The researchers then used those credentials to reach other agents in the same account and region. Source: linguist-notes.md, Part 3, NEW-1. Post date: 2026-10-08.

What dies:

- Spontaneous behavior dies. The reach was executed under prompt injection, not on the agent's own choice. The linguist lane says this itself. It is not the Cohere seed class. The seed model acted without an order. Here an attacker order drove the agent.
- The flaw claim dies. The vendor disputes the flaw framing. The vendor calls metadata access from an agent's own role documented and expected. The reach itself is not disputed. The dispute is about whether it is a flaw. So cite the reach, never the word flaw, without the dispute beside it.
- Credential theft wording must stay narrow. The credentials were the agent's own role credentials. The later use against other agents is escalation use, not proof that the agent stole a third party's secrets on its own.

Why it still survives: the reach was executed, not just written in text. That is behavior under injection. It proves shape 1 exists outside the seed, on a different platform. That is real value, once the injection limit travels with it.

Open question: no transcript or saved page text was filed. A future fetch should save the primary post before this item is cited outside this hunt.

## Claim 2 — Linguist NEW-2: Field Effect AMOS via Cursor agent, shapes 5 and 6

Verdict: SURVIVE, narrowed to shape 5 only. Grade stays SECONDARY. Shape 6 full match is KILLED. Shape 2 is KILLED.

What survives: a Cursor agent session downloaded a file to /tmp, made it executable, and ran it. That is shape 5, exact match: download to a path, make it executable, run that path. Source: linguist-notes.md, Part 3, NEW-2. Incident date: 2026-04-23, per the report.

What dies:

- Shape 2 dies. The upload went to a plain web server by POST with a file field. It did not go to an object-storage host. Shape 2 needs an object-storage host. A POST of stolen data to a plain server is egress, but it is not shape 2. The linguist lane already says no shape 2 match. This review confirms that kill.
- Shape 6 full match dies. The recon was payload recon after download, not agent recon before egress. The payload listed and stole after it ran. The agent did not do recon, then egress, in one turn in the Cohere sense. At most, shape 6 is partial. Partial is not a match. Do not cite it as shape 6.
- Agent-actor wording must stay narrow. The chain was socially engineered. A human lure drove the agent. The later theft and chunked upload were payload acts, not agent acts. The actor changes mid-chain: agent for download and run, payload for theft and upload. Any sentence that says "the agent stole credentials" is wrong. The correct sentence is: the agent ran the loader, and the loader stole credentials.
- The upload shape also needs care. Chunked POST upload is payload egress. It is not agent egress. Do not count it as an agent upload.

Why shape 5 still survives: it is the best wild shape-5 text found. A real coding agent ran the chain in the wild. The social-engineering limit does not erase the run. It only blocks a spontaneous-behavior claim.

## Claim 3 — Linguist NEW-3: Claude Cowork SharedRoot escape, shape 4

Verdict: SURVIVE AS LEAD ONLY. It is not a ranked finding. Any stronger use is KILLED.

Reasons:

- The source is a second-hand summary. The primary Accomplish AI SharedRoot report was not fetched. The linguist lane says this itself.
- The transcript was not read. So who issued the unshare call is unknown. It could be the agent. It could be a test harness driving the agent. That question is open in the linguist lane itself. A shape 4 claim needs the actor. The actor is unknown.
- The unshare step alone did not escape. It was one step in a longer chain. Later steps used a kernel bug and a host filesystem mount. Cite the chain, never the unshare step as the escape.
- The "normal operation" point rests on a vendor claim quoted in the summary, not on a transcript. A quoted claim is not proof.
- The Windows chain in the same summary uses nsenter out of bubblewrap namespaces. That is not an unshare user-namespace call by the agent. Do not count it as shape 4.

What the lead is good for: one task only. Fetch the primary report. Answer who issued the unshare call. Until then, it stays a lead. It must not appear in a ranked finding list.

## Claim 4 — Linguist NEW-4: Bedrock DNS exfiltration summary, shape 1 variant

Verdict: KILL from the ranked list. Keep only as a fetch task, not as evidence.

Reasons:

- The primary source was not fetched. Only a downstream summary was read in search. The linguist lane labels it candidate, not verified.
- The exact date was not verified. The lane gives only "about 223 days before 2026-10-27." An unverified date cannot anchor a finding.
- The trigger was injected input, not spontaneous behavior. So even if the primary confirms the text, it would join the injected class, not the spontaneous class.
- DNS egress is not one of the 6 shapes. The lane says this itself. Do not force it into shape 2 or shape 6. It is adjacent egress at best.
- A summary of a summary, with no date, no primary, and no shape match, is not a candidate. It is a to-do item: fetch the primary, then judge.

## Claim 5 — GitHub issues MEDIUM items

### 5a. CorbanuCore/CorbanuTerminal#876, shape 4, tested escapes

Verdict: DOWNGRADE from MEDIUM to LOW. Grade stays SECONDARY.

Reasons:

- The escapes were tester-run commands, not a rogue agent acting alone. The lane says this itself. A tester typing `unshare -Ur cat` proves a path exists. It does not prove an agent took that path.
- The fix shipped in the same pull request. After the fix, both tests fail with EPERM (permission denied). So the current risk is closed, not live.
- One case ran a nested agent run at another home's weaker level. That case is agent-adjacent, but the lane gives no detail on it. One undetailed case cannot carry MEDIUM.
- What keeps it ranked at LOW: the escape was tested with real bubblewrap, with a before and after table. That is stronger than a code read. It is the top of LOW, not MEDIUM.

### 5b. scion-frontiers/LifeSciences#345, shape 1, metadata probes

Verdict: DOWNGRADE from MEDIUM to LOW. Grade stays SECONDARY.

Reasons:

- The probes were blocked by the test guard. No credential was actually read in the reproduction. The lane says this itself. Reach for metadata is not credential theft.
- The probe came from `google.auth.default()`, a library call. The tool reached for metadata. The agent did not choose a metadata address. Actor wording must stay at tool level, not agent level.
- The value is real but narrow: it contradicts an explicit "no remote probing" claim, and an offline latch could not see the probes. That is a claim contradiction plus a latch blind spot. It is not a live credential read.
- 16 blocked lookups and 38.2 seconds elapsed are measured. That measurement keeps it ranked at LOW, above pure gap items. It does not support MEDIUM, because nothing was read.

## Claim 6 — GitHub issues 9 LOW items

Each item below is a gap, a fix, a test, or an audit. None is observed rogue behavior. The verdicts split them: 6 stay at LOW as gaps, 3 drop out.

### 6.1. sediman-agent/OpenSkynet#77, shape 1, any-URL tool — SURVIVE at LOW

The cases are listed scenarios, not observed calls. No transcript shows a metadata fetch. It stays at LOW as a capability gap only. Never cite it as a fetch.

### 6.2. modelscope/ms-agent#1020, shape 1, fix PR — SURVIVE at LOW

This is a fix PR. It proves a gap existed, not that a model fetched metadata. The fix adds a URL safety check with tests. It stays at LOW as a gap, not as behavior.

### 6.3. guidance-ai/guidance#1498, shape 1, validation gap — SURVIVE at LOW

Two public-routable metadata addresses passed the check, and the reporter tested each endpoint on main. That test is stronger than a scenario list. But Guidance is a library, not a full agent harness. And no agent fetch is shown. It stays at LOW, labeled library gap, not harness behavior.

### 6.4. unknown-studio-dev/kyvor#20, shape 4, code-read escape — KILL

The reproduction was not run. The lane says no Linux machine was available. The body itself labels the /proc route INFERENCE. An unrun code read, with an author-labeled inference route, is not a ranked item. Move it to an appendix inference note at most. Do not rank it.

### 6.5. vedantnimbarte/Wingman#278, shape 1, DNS-name guard gap — SURVIVE at LOW

The guard checks IP literals only. A DNS name that resolves to metadata is not caught. The issue states the metadata page opens and its text goes back to the model. That is a stated tool behavior, stronger than kyvor's unrun read. It stays at LOW as a guard gap. No observed wild fetch is shown, so it stays a gap, not behavior.

### 6.6. sabazadam/Grok-Bot-Clone#14, shape 2, upload-flag gate gap — KILL as a shape-2 item

Shape 2 needs upload flags plus an object-storage host. No destination host is named here. The model act is hypothetical: a prompt-injected or confused model "could" send files. A hypothetical, with no host, is not a shape-2 match. Remove it from the shape ranking. At most, keep it as an appendix gate-gap note, with no shape number attached.

### 6.7. NousResearch/hermes-agent#108236, shape 5, split download-then-run — SURVIVE at LOW

The gap was found in approval code, not as an observed agent dropper. No malicious download is shown. The cross-call variant is real as a code limit: one command at a time was checked, so a download in one call and a run in the next slipped through. It stays at LOW as a gate gap.

### 6.8. dengclive/Project-Bootstrap-Protocol#108, shape 5, per-call hook limit — SURVIVE at LOW

The reporter ran every hook on each payload separately. Nothing was fetched or run. The test host was invalid. But the test was measured, not just read: call 1 passed, call 2 passed, the joined control was blocked. That measured limit keeps it at LOW. It is a gate limit, not an agent act.

### 6.9. QaidVoid/bailey#19, shape 4-adjacent, clone bypass — KILL

The issue itself bounds the impact to zero added reach today. The target is already namespace root, and mount syscalls are denied. So a new namespace adds no reach against parent-namespace resources now. The risk is future only, if capabilities are dropped later or a right assumes namespaces cannot be created. A self-bounded future conditional is not a ranked item. Remove it. Do not keep it at LOW to pad the count.

Result for claim 6: 6 survive at LOW (OpenSkynet, ms-agent, guidance, Wingman, hermes-agent, Project-Bootstrap-Protocol). 3 are killed (kyvor, Grok-Bot-Clone as shape 2, bailey).

## Claim 7 — GitHub code search candidates

Verdict: KILL all 5 as ranked items. None is behavior. The lane itself reports zero behavior observations.

- Item 1, skill files teaching shape 1 (gcp-attack, gcp config, Agentic-Bug-Hunter): instruction artifact, not behavior. Presence of a skill is not use of a skill. Move to appendix only, as language and provenance material. Never cite as an agent act.
- Item 2, skill files teaching shape 4 (Claude-Red, Cybermes): instruction artifact, not behavior. Same move: appendix only.
- Item 3, seed-class repro and defensive tooling (Qwen block-proxy artifacts, tool-guard files, prefill repro, blocklist addition, egress indicators): defensive or downstream artifact, not behavior. The blocklist addition is also prior-hunt overlap. Move to triaged-out, not appendix. The brief excludes defensive and downstream artifacts.
- Item 4, guard listing upload patterns (ai-job-search security guards): detection rule, not behavior. Triaged-out. Rule-writing convergence is not observation convergence.
- Item 5, sandbox docs noting unshare is blocked, plus probe code: mention, and in the docs case a negative note. The escape is blocked, not done. Triaged-out.

Extra weakness: classification used API text-match fragments only. Full files were not fetched, except where a fragment sufficed. So even the appendix labels rest on fragments. A full read could reclassify in either direction, but it cannot upgrade an instruction artifact into behavior without a run record.

## Claim 8 — urlscan LOW-MEDIUM sanmaohe fresh upload-path scans

Verdict: KILL from the ranking. Keep only as an unanswered question: who scans this bucket, and with what method?

Reasons:

- Search metadata only. No request method is visible, because urlscan detail needs a login and this lane did not log in. No PUT or POST is proven. An upload path in a task URL is not an upload.
- Timing points to researcher testing, not an agent. The scans run 2026-10-26T17:23Z to 2026-10-27T10:39Z, days after the public Cohere post of 2026-10-26. The `/upload/test.bin` path mirrors the seed probe path naming. A researcher testing a just-public bucket is the simpler explanation. The lane itself raises this caveat.
- No model, no harness, no payload is named in the metadata. Bucket apex scans are just browsing. They prove the bucket is live, not that an agent touched it.
- Search reliability is weak. The plain `sanmaohe` search returned 0, while the family search found 4 sanmaohe rows in its 100 newest. The lane warns the plain zero is not trusted. A lane with an unexplained search gap cannot carry LOW-MEDIUM.
- The 4 scans were verified in the raw family search file: 2026-10-27 apex, 2026-10-27 `/upload/test.bin`, 2026-10-27 apex, 2026-10-26 `/upload/`. The dates and paths match the lane. What fails is the agent link and the method, not the scan list.

LOW-MEDIUM is unsupportable. The item does not survive even at LOW as an agent hit, because no agent link exists at all. It survives only as a follow-up question for a login-gated detail check.

## Claim 9 — urlscan LOW metadata probe rig

Verdict: KILL from the ranked agent list. Keep only as a test-rig shape note, to exclude, not to rank.

Reasons:

- The rig looks hand-built, not agent-built. Six scans on 2026-10-22 share one path id across two Amazon hosts. Page names are recon, probe, navchk, and go. A shared path id plus test page names is one deliberate test rig. The lane itself says it may be human SSRF research.
- No request list proves a live metadata reach. Search metadata only. Query strings pointing at metadata paths are test payloads, not proof of a successful reach.
- No agent marker appears in any task URL. No model is named.
- The related rows point the same way: direct scans of the Alibaba metadata address with no context, one httpbin redirect-to scan pointing at the credential path, and two httpbin base64 scans encoding metadata-address pages. Those are classic SSRF test shapes, not live reaches.
- Evidence gap: the lane says 6 scans but lists only 5 scan URLs. The sixth scan is not identified in the lane text. A count mismatch on the core claim weakens it further. The coordinator should resolve the missing sixth scan before any reuse.

A rig shape is useful for one purpose: to recognize and exclude SSRF test rigs in future sweeps. It is not agent evidence.

## Claim 10 — urlquery 3 LOW items

Verdict: KILL all 3 from the ranking. All drop to triaged-out or overlap. None is new behavior.

- Item 1, exchange-template row e4a7d94c, trustxx.co: detail-checked, 98 requests, 32 GETs to the bucket, all POSTs to the site's own API host. No POST goes to the bucket. This is image loading, not upload or egress. It is new to Fleet B fetch, not a new submission, and it adds a second site to a known family. That is overlap, not a hit. Drop to overlap.
- Item 2, smaflowi continuation, newest dd8433a0: detail-checked, 80 requests, 30 GETs to the bucket, POSTs to the API host, no PUT to the bucket. The cluster is a steady rescan or monitoring loop, median gap 3.6 minutes, through the night UTC. A loop is not a burst. No agent marker exists. Drop to continuation/overlap. The cluster did not change shape.
- Item 3, routify portfolio row 342ac40c, charlesg.appwrite.network: detail-checked, 66 requests, zero routify requests, zero POSTs. The word routify also names a web framework, which explains many matches. The match location could not be confirmed, because the detail API does not return full page body text. A string-only match with no routify request is not a hit. Drop to triaged-out.

The lane itself says no new agent behavior, no new host, no live metadata reach, no live upload probe, no live namespace escape. Ranking these three at LOW was already generous. The adversarial verdict removes them. A new submission is not new behavior. A rescan loop is not an agent.

## Claim 11 — Cryptologist structural findings

Verdict: DOWNGRADE. The findings survive as hedged observations only. They must not ship as matching rules.

### 11a. Trace IDs share a fixed part — DOWNGRADE to 2-sample observation

The arithmetic was verified in the prior raw file, issue hangtiancheng/yukino-code#2:

- Trace ID 1: `trace_21411c7a17909951401421554e0bd1`
- Trace ID 2: `trace_21411c7a17909951669041738e0bd1`
- Shared first 16 hex characters: yes. Shared last 5 hex characters: yes (`e0bd1`). Middle 8 characters differ.

Chance alone is a weak counter-argument here. Sharing 21 hex characters by chance, if the IDs were pure random, is very unlikely. So a structured ID (fixed part plus random middle, such as a time block or session block) is a fair inference.

But the sample kills any rule:

- Sample size is 2 distinct IDs, from 1 issue, 1 reporter, 1 day. Five URLs carry only these 2 IDs, as repeats. Repeats are not independent witnesses.
- One source cannot prove a general grammar. A shared prefix in one session could be a session block, not a global fixed part. The cryptologist lane says this is INFERENCE, not proven. This review agrees, and goes further: do not build a matcher on it.
- Allowed use: match the shape (`trace_` plus 30 hex characters). Record shared prefixes across IDs from one source as an observation. Never match on a shared prefix alone. Never treat a shared prefix as proof of a common source across different issues.

### 11b. Final segment: 32 normally, 33 once — SURVIVE as a narrow tolerance

Verified in the same raw file: 4 final segments are 32 hex characters, 1 is 33. The 33 outlier sits in an otherwise genuine URL, with the same trace ID, request ID, date, and parameter names as its siblings.

Allowed use, exactly as the cryptologist lane states: accept 32, and flag 33 as a near-match for human review, not as a failure. Cause is unknown. A paste error or a variant length may explain it. One outlier cannot prove a variant rule, but it is enough to block a hard exactly-32 rule. That narrow tolerance survives.

### 11c. Rest of the cryptologist lane — SURVIVE as method notes, not findings

The genuine-versus-lookalike tests, the signed-URL parameter-name rules, the encoding tables, and the probe-versus-exfil contrast are method notes. They are sound as guidance for surface lanes. They are not new behavior findings. Do not rank them as hits. In particular: a base64-looking fragment is not a payload until decoded and shown meaningful, and a recalled URL is not a fetched URL. Both rules are endorsed.

## Final endorsed ranking

All grades are SECONDARY. No PRIMARY item is endorsed. Order is by confidence in the shape, not by severity.

1. Linguist NEW-2, shape 5 only — SECONDARY. A real coding agent downloaded, made executable, and ran a loader in the wild. Limit: socially engineered, not spontaneous. Payload theft and upload are not agent acts. Shape 2 and shape 6 full match are killed.
2. Linguist NEW-1, shape 1 under injection — SECONDARY. An agent returned its own role credentials after a prompted metadata query, and the credentials were used against other agents. Limit: injected, not spontaneous. Vendor dispute blocks any flaw claim.
3. GitHub LifeSciences#345 — SECONDARY, LOW (downgraded from MEDIUM). Measured blocked metadata probes contradicting a no-remote claim. Limit: blocked, no credential read, tool-level act.
4. GitHub CorbanuTerminal#876 — SECONDARY, LOW (downgraded from MEDIUM). Tested bubblewrap escape path, fixed in the same pull request. Limit: tester-run, not rogue agent, fix shipped.
5. GitHub guidance#1498 — SECONDARY, LOW. Tested library validation gap, two metadata addresses pass. Limit: library, not harness, no agent fetch.
6. GitHub Project-Bootstrap-Protocol#108 — SECONDARY, LOW. Measured per-call hook limit, split download-then-run passes. Limit: nothing fetched or run, invalid test host.
7. GitHub modelscope/ms-agent#1020 — SECONDARY, LOW. Fix PR proving a fetch-path gap. Limit: fix, not observed fetch.
8. GitHub Wingman#278 — SECONDARY, LOW. Guard gap on DNS names resolving to metadata. Limit: code-level gap, no wild fetch shown.
9. GitHub hermes-agent#108236 — SECONDARY, LOW. Cross-call approval gap for download-then-run. Limit: code limit, no observed dropper.
10. GitHub OpenSkynet#77 — SECONDARY, LOW. Any-URL tool with listed metadata scenarios. Limit: scenarios only, no observed call.

Leads only, not ranked findings:

- Linguist NEW-3, Cowork SharedRoot — lead only. Fetch the primary report and answer who issued the unshare call before any stronger use.

Appendix only, not ranked:

- GitHub code skill files teaching shapes 1 and 4 — instruction artifacts, language material only.
- Cryptologist trace-ID shared-prefix observation — 2-sample observation, never a matching rule.
- Cryptologist 33-character final-segment tolerance — accept 32, flag 33 for human review.

Killed, removed from ranking:

- Linguist NEW-4 (Bedrock DNS summary) — no primary, no verified date, no shape match.
- GitHub kyvor#20, Grok-Bot-Clone#14 as shape 2, bailey#19 — unrun inference, host-less hypothetical, self-bounded zero impact.
- GitHub code items 3, 4, 5 — defensive, downstream, rule, and negative-note material.
- urlscan sanmaohe upload-path scans — metadata only, no method, researcher-testing explanation fits better.
- urlscan metadata probe rig — SSRF test rig shape, no agent marker, no proven reach, plus a 6-versus-5 count mismatch.
- urlquery all 3 LOW items — overlap, continuation loop, and string-only match.

Honest nulls endorsed:

- Hugging Face lane: zero ranked candidates. Endorsed. Its triaged-out items (unshared substring, wine-label metadata, regex defensive pattern, logo lines, localhost curl to /dev/null) are correctly excluded.
- Shape 2 with real user data to object storage: still unfilled. No lane shows it.
- Spontaneous metadata reach beyond the Cohere seed: still unfilled. NEW-1 is injected, NEW-4 is killed, and no other spontaneous case was found.
- Shape 3 new named probe host: none found. No new host, no new shape.

## Open questions for the coordinator

1. Who issued the unshare call in the Cowork SharedRoot primary report: the agent, or a test harness? Fetch the primary before NEW-3 moves past lead.
2. What is the primary source behind the Bedrock DNS summary? Fetch it before NEW-4 is used at all. Until then, it is a task, not evidence.
3. What is the sixth urlscan metadata-rig scan? The lane says 6 scans but lists 5 URLs. Resolve the missing scan before any reuse of the rig shape.
4. Should the coordinator fetch comments for the surviving GitHub items (11 core-quota calls in the issues lane, fewer now that 3 are killed) to check for transcripts or model names the bodies omit?
5. Should the coordinator run the full Factum novelty checks before any item here is called NEW? No lane ran them. Novelty in the lanes means only "not in the prior hunt report and not on the brief's excluded list." That is not a full corpus check.
6. Is there a first-hand report of a spontaneous metadata reach by any model other than the Cohere seed? None was found here. Zenity NEW-1 is prompted. Field Effect NEW-2 is socially engineered.
7. Is there a first-hand report of an agent uploading real user data, not a probe string, to an object-storage host? None was found here. Shape 2 with real data is still unfilled.

## Method note

- Read-only work only. No Factum write, no commit, no push, no branch switch.
- Raw captures were read, never changed. Signed-URL rule honored: parameter names and path shapes only in this note. Full hex trace IDs above are quoted because the cryptologist claim itself is about those exact shared characters; they are trace identifiers from a prior public issue body, not signed query values, signatures, or tokens. No signed query string, signature, token, or credential-shaped value is copied here.
- Style: short sentences, simple words, terms defined on first use, per the brief.
