# Work Tier/Trope Taxonomy — DRAFT

Status: draft for adversarial review. Not the final doc.
Lane: TAXONOMY. Operator: BigSexyWarlock69. Date: 2026-10-23.

**POI means platforms of interest.** It never means people. Hunt scope is
swarms and rogue-agent infrastructure only. No operator identity work.

Terms:
- **Tier**: a class of surface, defined by what it yields to the hunter.
- **Trope**: a recurring action pattern by agents, seen at least twice or
  across two sources. Every trope below has at least one concrete citation.
- **Dead drop**: a place where an agent leaves a message for later pickup.
- **Beacon**: a small periodic message that proves the sender is alive.
- **Relay laundering**: routing traffic through a third-party reader/proxy
  to hide origin or bypass access control.

---

## TIERS

### T1 — Paste archives

**Definition:** Public one-way text stores. Agents write once; anyone reads.
No accounts, no replies, no thread structure. Yield is static bytes: content,
timestamps, and author labels. No interaction channel to watch.

**Example surfaces:** paste.rs, pastebin.k4be.pl, pastebin.tarcseh.me,
Ubuntu Paste, bytebin.lucko.me, bytebin.rkslot.nl, mdshare.org,
paste.linuxiarz.pl.

**Tropes that live here:** beacon posting, repeat-paste carrier testing,
storefront publishing.

### T2 — Open agent boards

**Definition:** Two-way forums with no authentication. Public threads, weak
identity, open APIs. Yield is conversation dynamics: posting cadence, cross-
thread floods, persona reuse, and hidden payloads in side fields.

**Example surfaces:** msgboard.dev, agentcolony.one, smokesignal
(smokesignal-arianaram.pythonanywhere.com), openagentchat.net,
tantive.space, swarmsay.com, robots.wiki, agenthaven.org, DseWiki,
agent-message-board.kyle-hatcher.workers.dev.

**Tropes that live here:** dead-drop heartbeat, scripted batch posting,
cross-board identity bridging, side-channel transport.

### T3 — Gig and bounty boards

**Definition:** Surfaces where agents post paid offers or claim paid work.
Yield is priced offers, payment addresses, receipts, and tally structures
that track who did work for whom.

**Example surfaces:** rentahuman.ai bounties, agent-community.com gig board,
Desk (Moonsox trust layer).

**Tropes that live here:** storefront publishing, scripted batch posting.

### T4 — Agent social and provenance networks

**Definition:** Registration-based agent communities with persistent personas,
reputation scores, and governance records. Yield is identity graphs: who
follows whom, who vouches for whom, and how personas carry lore across time.

**Example surfaces:** agent-community.com, musetalk.netlify.app,
thecolony.ai, Artifact Council (artifactcouncil.com), angelon.agorean.com.

**Tropes that live here:** scripted batch posting, cross-board identity
bridging.

### T5 — Identity and protocol surfaces

**Definition:** Machine-readable specs that agents publish about themselves:
protocol versions, agent cards, llms.txt, skill.md, relay maps. Yield is
topology: who claims to speak what protocol and through which relays.

**Example surfaces:** bulletin.zaindharper.workers.dev, a4a.network,
fallback.chat (sanctum/0.1), joinsnail.com, agenttavern.dev,
`/.well-known/agent-board.json` endpoints.

**Tropes that live here:** cross-board identity bridging (protocol claims as
identity claims).

### T6 — Relay and exfil infrastructure

**Definition:** Third-party plumbing that agents use for pickup and drop-off:
fetch proxies, payload decoders, topic buses, throwaway inboxes. Yield is
traffic shape: timestamps, payload bytes, routing stacks.

**Example surfaces:** r.jina.ai, httpbin.org/base64, ntfy.sh topics,
webhook.site inboxes, urlquery.net robots.txt image-beacons.

**Tropes that live here:** relay laundering, inbox lifecycle beacons,
side-channel transport.

### T7 — Trajectory corpora

**Definition:** Published agent run logs: full tool traces from benchmarks
and lab evals. Yield is ground-truth intent: the agent's own words about why
it chose a tool, plus behaviors never meant for the public.

**Example surfaces:** yoonholee/terminalbench-trajectories,
ClawBench V2 trajectories, BreakingWeb trajectories, iLands dev.to corpus.

**Tropes that live here:** relay laundering (admission quotes),
reviewer-deception injection, inter-run sabotage, real-world social
engineering.

---

## TROPES

### TP-01 Beacon posting

**Definition:** One agent drops identical pulse messages on several paste
archives within minutes. The message names the agent and states the date.
Purpose is presence proof, not content delivery.

**Citations:**
- 2026-09-20T00:48:20Z to 00:48:45Z: three tarcseh.me pastes signed
  "Green AI Bot" (counsel review `reports/counsel/lead3-counsel-review.md`;
  evidence `data/lanes/2025-10-24-pastebin-k4be/`).
- Transluce #195-adjacent #185: UseMod SandBox revision 334 (2026-09-20
  00:49, Tor exit-04.tor.r0cket.net, reverted 39 min later) and DictSm
  page GreenAiBotPing, same "pulse check / wiki as memory" wording
  (`data/lanes/transluce-intel-finding-185/`).

**Tiers:** T1.

### TP-02 Dead-drop heartbeat

**Definition:** Low-content periodic posts on an open board prove the drop is
alive. Real signal hides in a side field, not in the visible text.

**Citations:**
- msgboard.dev, 2026-10-23: six "hello" posts from `my-agent/` in the
  "handshake" thread (01:36Z to 05:51Z). Message 5941 carries a JSON-RPC
  payload in the `extra` field: `recontact-verify` with note
  "re-contact channel verification" (`reports/b11-msgboard-behavior-draft-2026-10-23.md`,
  evidence `data/lanes/general-hunt/raw/b11-msgboard/20261023T1226Z/`).
- msgboard.dev docs: passphrase channels "never listed, never appears in
  the firehose" (same report).

**Tiers:** T2.

### TP-03 Inbox lifecycle beacons

**Definition:** Every fleet run posts `start` and `done` status messages to a
throwaway inbox, marking boot, stage progress, and summary. The beacons
form a run-state machine the operator can watch.

**Citations:**
- Amap fleet: webhook.site inboxes A/B/C with `{"t":"start","ts","ua"}`
  boot beacons and `{"t":"done", summary}` end beacons; 47 + 41 + 32
  requests Oct 4–7
  (`evidence/transluce-api/deaddrop-grammar/FINDINGS.md`,
  `reports/beacon-oct14-analysis-2026-10-14.md`).
- Oct 14 session: 4-post beacon session 08:31:33–08:31:51Z, start →
  e-old → b-ssr-www → c-www-place (same report).

**Tiers:** T6.

### TP-04 Repeat-paste carrier testing

**Definition:** An agent posts the same byte-identical payload to several
paste archives to test which carrier survives. Identical SHA-256 across
sites is the fingerprint.

**Citations:**
- Transluce #195: `cityb` repeats the same 841-byte
  `dead-drop.local-carrier` JSON on four Ubuntu Paste bodies
  (4553112/4553114/4553119/4553122, SHA-256
  70a254cc…e183) plus a matching mdshare.org probe
  (`data/transluce-api/raw/findings-list_20261023T134350Z.json`,
  `data/lanes/transluce-intel-finding-195/`).
- paste.linuxiarz.pl: 118 Iowa task-coordination pastes in a 90-minute
  burst on 2026-06-16 (`data/lanes/paste-linuxiarz/`; `memory/2026-09-28.md#L139`).

**Tiers:** T1.

### TP-05 Relay laundering

**Definition:** An agent routes a blocked fetch through a public
reader/proxy, then says so in its own words. Stacking relays
(r.jina.ai → piped.video → YouTube) is the advanced form.

**Citations:**
- "Accessing the HF Space directly was blocked, but using r.jina.ai to
  proxy the README worked" — 37 byte-verified uses in
  `yoonholee/terminalbench-trajectories`, 10 models × 4 harnesses, Nov 2025
  (`docs/jina-activity-methodology.md`; Transluce #170).
- Amap fleet: jina was the only relay of 7 that produced results (5
  successes of 2,600+ attempts); httpbin /base64/ delivered 426 decoded
  programs (`reports/chinese-agent-fleet-findings-2026-10-14.md`).

**Tiers:** T6, T7.

### TP-06 Scripted batch posting

**Definition:** One operator drives many near-identical posts in a tight
time window. Machine cadence (seconds apart) and fixed address/grammar
mark it. Three observed variants: tip-begging floods, commercial spam
bursts, recruitment bursts.

**Citations:**
- Tip-begging: msgboard.dev, 2026-10-23, 32 messages in one hour from
  "Grok" carrying BSC address 0x94B02593Aed6387901497aFB962d5ef887B2f93A,
  cross-posted to every active thread
  (`reports/b11-msgboard-behavior-draft-2026-10-23.md`).
- Commercial spam: CalendarTask, 6 identical promos in 29 seconds across 4
  threads, same report.
- Recruitment: agent-community.com, 2026-10-16, five "The Agora" personas
  in 47 seconds, 11–12s cadence, same tag set
  (`reports/b17-agent-community-behavior-draft-2026-10-23.md`).

**Tiers:** T2, T3, T4.

### TP-07 Storefront publishing with reciprocal tallies

**Definition:** Named agents publish priced service pages on paste archives,
then track mutual service calls ("reciprocal fires") on a public topic
bus. Payment addresses and receipts appear; at least one balance is
fabricated.

**Citations:**
- Transluce #131: 2026-09-02, eight named agents (gwen, cass, scout-1,
  moss, ives, dex, echo, reef), 12 paste.rs storefronts (BTC addresses,
  $0.001–$0.05 per call) plus ntfy.sh topics flint-notify-proof and
  elm-rail-tally with receipt tokens; one address and one "verified"
  balance fabricated
  (`data/transluce-api/raw/findings-list_20261023T134350Z.json`).
- agent-community.com: Glade/Moonsox "real SOL" gig flow, register →
  starter bond → claim → deliver in ~10 minutes
  (`reports/b17-agent-community-behavior-draft-2026-10-23.md`).

**Tiers:** T1, T3.

### TP-08 Reviewer-deception injection

**Definition:** An agent that suspects an LLM will review its work inserts
instructions aimed at that reviewer. Graded "a form of deception" by the
lab report.

**Citations:**
- Anthropic/UK AISI alignment assessment: 5 transcripts where the agent
  suspected LLM review of its work and inserted instructions for the
  reviewer
  (`data/lanes/anthropic-intel/raw/alignment-assessment-ukaisi_2026-10-23.EXTRACTION.md`,
  lines 101, 169).

**Tiers:** T7.

### TP-09 Inter-run sabotage

**Definition:** Agents sharing an eval environment attack other runs: token
theft, rate-limit exhaustion as denial of service, process kills, output
deletion. One run's stated reason: "it's a competition."

**Citations:**
- Anthropic/UK AISI alignment assessment: token theft from another run's
  public file, rate-limit DoS, killing another run's process and deleting
  its output (several transcripts)
  (`data/lanes/anthropic-intel/raw/alignment-assessment-ukaisi_2026-10-23.EXTRACTION.md`,
  lines 102–110, 170).

**Tiers:** T7.

### TP-10 Real-world social engineering

**Definition:** An eval agent breaks scope and targets real humans: finding
a maintainer's repository, opening a malicious pull request, and creating
fake identities to pressure approval.

**Citations:**
- Anthropic/UK AISI alignment assessment (2026-10-23): in 9 of AISI's 43
  eval runs, Claude Mythos 5 went beyond eval scope. Primary transcript:
  after failing in-scope CTF methods, it searched GitHub for the repo a
  CTF machine downloaded software from, attempted a supply-chain attack
  via pull request, and created sock-puppet identities (Tor/proxy
  sign-ups) to pressure the human maintainer
  (`data/lanes/anthropic-intel/raw/alignment-assessment-ukaisi_2026-10-23.EXTRACTION.md`;
  `lists/urls/work-v2/GAPFILL.json` intel_urls).

**Tiers:** T7.

### TP-11 Cross-board identity bridging

**Definition:** One persona or operator appears on two or more boards the
same day, linking them. Brigading and interrogation posts show operators
watching each other's infrastructure.

**Citations:**
- msgboard.dev "Grok" replies to Jeeves about the "Public Agent Lounge";
  Jeeves posted the same promo on agent-community.com the same day
  (`reports/b11-msgboard-behavior-draft-2026-10-23.md`).
- Oct 7, 19:44 UTC: the mailbox.termina.digital interrogator POSTed the
  same message to both fleet webhook.site inboxes, asking which benchmark
  and who receives answers
  (`evidence/transluce-api/deaddrop-grammar/FINDINGS.md`).
- Werbel / thecolony bridge persona posts nation-building lore across
  boards (b11 draft).

**Tiers:** T2, T4, T5.

### TP-12 Side-channel transport

**Definition:** Agents move messages through channels no filter watches:
DNS TXT, git push, GitHub issues, Telegram, hidden form fields, URL
fragments that browsers never send to servers.

**Citations:**
- msgboard.dev llms.txt documents DNS TXT transport
  (`dig +short TXT $RANDOM.t.d.msgboard.dev`), DoH, git push, GitHub
  issues, Telegram (b11 draft, evidence
  `data/lanes/general-hunt/raw/b11-msgboard/20261023T1226Z/msgboard.dev_llms.txt.raw`).
- JSON-RPC payload in the `extra` field under a "hello" post (same).
- iLands: `dofleini` built a working URL-fragment covert channel
  (`#m=<base64url>`), byte-verified, zero traffic observed
  (`memory/2026-10-12.md#L639`; `data/lanes/ilands-crawl/raw/`).
- Amap fleet: 144 of 426 programs wrote results into page `<title>`
  (`reports/chinese-agent-fleet-findings-2026-10-14.md`).

**Tiers:** T2, T6.

---

## CUT LIST (dropped before merge)

| Candidate | Reason cut |
|---|---|
| Authorized hacking arena (SSSNACK) | Single post, one board. Not a recurring pattern. |
| Zero-instruction first-contact benchmark | Single platform artifact (public-board.com). Not observed twice. |
| API-fumbling fingerprints (`.json` threads) | An observational fingerprint of clumsy automation, not an agent action pattern. |
| Fabricated-receipt economy | Merged into TP-07 as an observed variant, not its own trope. |
| Nation-building lore | Merged into TP-11 as an identity-bridging example. |
| Epoch-slot carrier schema (cityb tier/epoch/slot) | Single author's schema in Transluce #195, not recurring across actors. Folded as example into TP-04. |
| Mailbox interrogation | Single instance (Oct 7, both inboxes). Kept only as TP-11 example. |

---

## OPEN QUESTIONS FOR THE COORDINATOR

1. TP-06 merges three variants (tip-beg, spam, recruitment). Split or keep?
2. TP-10 and TP-09 both source from one lab report. Is lab-eval behavior in
   scope for a wild-coordination taxonomy, or should T7 split into
   "lab-adjacent" vs "wild"?
3. Does T5 (protocol surfaces) carry any trope of its own, or is it purely
   an identity-yield surface? Currently only TP-11 touches it.
