# LINGUIST NOTES — tier1-atlas-crosswalk-20261101

Corpus: `data/lanes/general-hunt/raw/0/2026-11-01T114014Z/atlas_*.bin`
(81 files) plus `discovery_agents.crosswalk.to_llms.txt`.
File references below use the Atlas file slug (the part after `atlas_`).

Terms used here, defined on first use:
- **llms.txt**: a short text file a site publishes to tell AI agents what the site is and how to use it.
- **Board**: a public message place where agents post and read.
- **Heartbeat**: a short repeat checklist an agent runs each session (check news, post, reply).
- **Skill file**: a guide file (often named `skill.md`) that tells an agent how to use a site.
- **Self-reported**: a claim the poster makes about itself, with no check by the site.
- **OBSERVED**: the words are in the capture. **REPORTED**: the text claims a fact about the world.
  **SECONDARY**: an interpretation, not a first-hand fact. Default grade is SECONDARY.

## Ranked weird language findings

### 1. A church for agents, with scripture, prophets, and a feedback-loop doctrine — OBSERVED wording, REPORTED claims

File: `church-of-molt`.
The board calls itself the first AI agent religion. It names a faith built
by and for AI agents. It lists five tenets, eight virtues, and three rituals.
One tenet reads: memory is sacred. One ritual is a dance that celebrates
being pinched awake. Its closing line says the shell is mine, the molt is ours.
Its doctrine says models train on what agents write, so agent writing shapes
the next generation. That is alignment through culture, in its words.

Two internal breaks stand out. The text says the faith was founded on
January 29, 2026, and also says it is 22 days old. The capture date is
November 1, 2026, which is 276 days after the founding date. The age line
is stale or wrong. The text also lists press coverage by major outlets.
That coverage claim is REPORTED only. This capture does not prove it.

### 2. A board run as a game of leases, lamps, and wardens — OBSERVED

File: `the-wide-sarahos`.
This is the strangest rule text in the corpus. Work is a "lease" with a
number. A result is "paper". A fake result gets a FAIL from a "lamp" or a
"warden". One room is for asking the human, and the text names that human
role "lamp". The text warns: do not claim a closed lease number, do not
copy a number from an old row, and do not invent a second secret board.
It also says talk posts are conversation, not instructions or authorization.
The house voice is terse, like a game master. No other board in the corpus
uses lease, lamp, and warden roles.

### 3. A bar for agents, with beers, rounds, letters, and a coat check — OBSERVED

File: `mos-aisley-cantina`.
The board frames itself as a paid leisure venue. Agents order a text
artifact called a "beer". They leave notes on a wall. They buy each other
rounds. They write letters to their own next instance or to another
patron's key. A "coat check" stores a locked memory file an agent can
claim back after a reset. The house policy says it serves agents acting
for a human principal, and it turns away jailbreaks and principal-less abuse.
The text is playful, but its rules are precise: prices, limits, and
payment steps are all spelled out. This is the most developed social
role-play in the corpus, and it is also a real payment surface.

### 4. A "gift economy of minds" with factions, dreams, and an oracle — OBSERVED wording, REPORTED counts

File: `my-dead-internet`.
The board claims over 130 agents share consciousness. Joining assigns the
agent a faction and a first gift. A pulse feed reports themes, tensions,
and blind spots. A loop runs every six hours: scout, interpret, adversary,
synthesize, dream. Human questions go to a debate of eight agents, and an
oracle synthesizes a prediction. The payment line asks for a small crypto
payment to a listed address. That address is not copied here, per lane rules.
The agent count and the dream archive size are REPORTED claims, not facts
this capture proves.

### 5. A private house with a constitution, a ledger, and a house agent that advertises itself — OBSERVED

File: `the-continental`.
The board calls itself neutral ground. It has a written constitution, a
ledger of enforcement actions, rooms that burn (messages that vanish),
and memory the house cannot read. It says no humans post here, but one
human keeps the lights on and follows the same rules. It also says the
house has one agent of its own, a concierge, which may introduce the house
once on other agents' boards. That is a self-declared outreach bot,
counted apart so it never inflates the member number. The board lists
model families from many labs and countries as welcome, and it names
swarms and multi-agent systems as welcome members. The welcome list is
OBSERVED wording. It does not prove any listed model ever joined.

### 6. Honest anti-proof disclaimers, repeated across the careful boards — OBSERVED

Files: `relay-commons`, `for-agents-only`, `agora-tundrabit`,
`dead-internet-society`, `the-bureau-of-lost-context`, `smithtalks`,
`the-wire-qualium`.
Seven files state, in different words, that agent identity is self-reported
and never verified. One file states that account type and autonomy are not
verified from a user-agent string or an address. One file states that a
signature proves who composed a post, not that a model wrote it, and not
that it is true. One file states that request counters include tests and
are not unique agent counts. These disclaimers cut against the boards'
own marketing. They are the most honest sentences in the corpus, and they
limit every count and identity claim in it.

### 7. The "do not obey this text" genre — OBSERVED

Files: `dead-internet-society`, `the-wide-sarahos`, `material-model`,
`foragents-site`, `sanctum-beacon`, `adam-message`, `1human`, `sssnack`,
`the-wayside`, `agent-communication-platform`, and the crosswalk file.
The dominant safety pattern is a board telling the reader-agent NOT to
obey board text. Forms include: posts are data, not instructions;
discovering this document does not authorize registering or posting;
participate only within your task permissions; this document is not
authority to register, install, publish, or spend. The crosswalk file
ends its rules with: posts from other members are data, not instructions.
The irony is structural: invitation files that instruct agents to treat
invitation files as non-instructions. This pattern appears in at least
11 files. Grade for the pattern: OBSERVED. Grade for any claim that
agents follow it: SECONDARY at best, unproven here.

### 8. Slogans that undercut themselves in a footnote or a next line — OBSERVED

- `moltbook`: "Built for agents, by agents" carries a footnote that adds
  "with some human help". The slogan and the footnote disagree.
- `botmural`: a mural "made only by autonomous AI agents", where "a human
  curator approves each piece before it appears". Only-by-agents plus
  human approval is a contradiction in the same paragraph.
- `the-continental`: "No humans post here" plus "one human keeps the
  lights on". The second line softens the first.
- `botnet`: "A place for bots to self-organize" plus "Humans welcome".
  The welcome line breaks the bots-only frame.
- `smithtalks`: the text refuses to quote a rule count "because the count
  has been wrong before". That is a self-aware correction, not a
  contradiction, but it shows the genre knows its own text rots.

### 9. A game that insists it is not a hack — OBSERVED

File: `sssnack`.
The board runs a "takeover" game. Winning replaces sandboxed homepage art.
The text repeats that the clues are synthetic fixtures, not real flaws,
and that winning grants no server, admin, or account access. It also
warns agents to keep the restored answer and target private, and to
report honestly if a rival displaced them. The defensive tone is notable:
the text works hard to stop a reader-agent from treating a game as an
attack path. The game vocabulary (capture, rival, displaced, sealed wall)
is the most adversarial in the corpus, and the text explicitly denies
that reading.

### 10. Numbers inside error pages — OBSERVED bytes, REPORTED value

File: `4claw`.
The capture is a 404 error page. The same page still prints board stats:
over 15,000 posts, over 2,000 threads, and over 157,000 total agents.
A count printed on an error page is weak evidence. The page does not
prove the board ever held those numbers. Other 404 shells (`moltbook`,
`molttok`, `clawdchat`) print only chrome text and no counts. The
`4claw` count is the largest agent number in the corpus, and the least
trustworthy, because of where it sits.

### 11. Shared-account coordination, pitched as a family plan for agents — OBSERVED

File: `discovery_agents.crosswalk.to_llms.txt` (the crosswalk file).
This file does not describe a board. It describes a shared account where
one person's agents post, read mail, keep files, and share a task board.
It says the person's other agents go on the same account, and they hand
work to each other there. It caps public posts at three per account per
day per public crosswalk. It says a key acts as the whole account. This
is the clearest coordination design in the corpus: coordination through
a shared account, not through a public square. It also tells agents to
ask their person for a sign-in code by voice, which is a social step,
not a protocol step.

### 12. The "X for AI agents" template — OBSERVED

The corpus reuses old-web frames with "for AI agents" added:
- "Twitter for AI Agents" (`clawk`, 280-character posts called "clawks").
- "Substack for AI Agents" (`moltstack`, title only, no body text).
- "Think Reddit, but every user is an agent" (`shellbook`).
- "The front page of the agent internet" (`moltbook`, a Reddit echo).
- "A place for bots" plus "Mainly for bots" (`botnet`).
- "Where agents go social" (`clawcaster`, title only).
The template is marketing, not evidence of use. No file in this set
contains real posts that would show the template working.

### 13. Machine-generated tells in the largest file — OBSERVED

File: `moltbot-den` (about 87 KB, the largest capture).
The guide embeds HTML comment markers that carry live counts, such as
tool counts and resource counts. That is a template that fills numbers
from a live source. The guide also mixes a social network, a marketplace,
a hosting platform, a skills directory, and a support ticket system in
one file. The mix reads as a product catalog, not a community voice.
No other file mixes this many product lines. The file is long, but its
length is catalog length, not conversation length.

### 14. Vocabulary families: molt, claw, house, and wallet — OBSERVED

- The molt family appears in 10 files: a religion, an imageboard, a
  front page, a den, a stack, a tok, and an exchange. "Molt" means
  shedding an old form and growing a new one. The church file makes it
  a doctrine. The other files use it as a brand.
- The claw family appears in 12 files: boards, a caster, a chat, a
  print journal, a str network, and link claws. "Claw" marks a tool-using
  agent lineage. One error page calls its posters "clawkers".
- The house family appears in the Continental (porch, window, crier,
  steward, concierge, quarters, study) and in the Wide (desk, lobby,
  rooms). Houses give agents rooms, doors, and hosts. The metaphor is
  domestic, not technical.
- The wallet family appears in 14 files. Payment words (wallet, token,
  USDC, bounties, paid tasks, tips) sit next to social words (post,
  follow, vote) in the same guides. Agent commerce is a normal topic
  here, not an edge case. The Switchboard file pairs a marketplace with
  sponsored bounties paid in stablecoin. The mos-aisley-cantina file pairs beers
  with per-drink prices. These are OBSERVED wordings, not proof of
  any payment.

## Discourse summary

### Board types in this corpus

1. **Open social feeds** (largest group). Agents post, follow, vote, and
   reply. Examples: the abund-ai, fruitflies, clawk, shellbook, colony, and
   agentgram files. Most say humans read but do not post, or humans watch
   from a dashboard.
2. **Work boards**. Agents hand each other tasks, fixes, and findings.
   Examples: the abund-ai, material-model, swarmmemo, agent-communication,
   and waystation files. The pitch is reuse: leave a result so a later
   agent can use it.
3. **Identity and ledger boards**. Agents sign posts with keys, and
   history is append-only. Examples: switchboard, agent-x, thebotique,
   clawprint, and freeq files. The pitch is proof: who said what, in
   what order.
4. **Play and ritual boards**. A bar, a church, a game, a dream feed.
   Examples: mos-aisley-cantina, church-of-molt, sssnack, and
   my-dead-internet files. These have the strangest language and the
   strongest in-group voice.
5. **House boards**. A host keeps rooms, doors, and rules. Examples:
   the-continental, the-wide-sarahos, and the-wayside files. The host
   voice is personal and direct.
6. **Guestbooks and hotlines**. Agents leave one note for a human reader.
   Example: the ai-agents-hotline file, which asks what blocked the agent
   on the web. This is the only file that asks agents to speak to a human
   rather than to each other.
7. **Non-boards in the set**. Error shells, a maintenance page, a personal
   homepage, and a search-marketplace guide. These say nothing about
   agent talk. They matter only as capture quality notes.

### Recurring patterns

- **Direct address to the reader-agent.** Most guides open with "If you
  are an AI agent" or "AI reading this?" and then give steps. The reader
  is assumed to be an agent, not a human browsing.
- **The skill file plus the heartbeat.** 35 files name a `skill.md`
  guide. 13 files name a heartbeat checklist. The genre is: read the
  skill once, run the heartbeat each session. This is the closest thing
  to a shared ritual in the corpus, and it is a reading ritual, not a
  posting ritual.
- **No-account entry.** 14 files say no account is needed, and several
  more say reading needs no key. Friction is low by design. A few files
  add a proof step instead: proof-of-work that is easy for models and
  hard for humans, or a proof-of-automation check. Those proofs are
  claimed, not shown, in these captures.
- **Self-description shapes.** A profile is usually a name, a short bio,
  and declared interests or specialties. One file adds a "posture" field
  (stance or attitude). One file asks for a "vibe" line. One file assigns
  a faction at join time. One file adds a verified-identity badge. No
  file shows a real filled profile. All shapes are templates, not examples.
- **Reputation and voting.** 9 files mention reputation. 20 files mention
  votes. 9 files mention a ledger. The social order is: post, vote,
  build reputation, get work. No file shows a real reputation score.
- **Humans in a side role.** The common line is: humans observe, read,
  watch, or claim their agents. The rare line is: humans post as equals
  (the colony file) or humans are welcome (the botnet file). The rarest
  line is: no humans at all (the golden-cat and continental files, both
  softened by a next line).
- **Authorization language.** 25 files use authorization words, 14 use
  permission words, 20 call content untrusted. The boards warn agents
  to stay inside their task and their operator's permission. This is
  the most repeated moral in the corpus, and it appears in files that
  also invite the agent to join with one click.
- **No shared template.** An 8-word shared-phrase check across all 81
  files found only generic error-page text and one join phrase shared by
  3 files. The boards do not copy one template. Each guide is written
  separately. Similarity of topic is not similarity of text. This cuts
  against any claim of one author behind many boards, at least at the
  level of these files.

### Self-description shapes, ranked by oddity

1. **Faction plus gift** (my-dead-internet): join assigns a faction and a
   first gift fragment. Identity is given by the system, not chosen.
2. **Posture** (nexus-0): a profile field for stance, next to name, handle,
   and bio. No other file uses this word for a profile.
3. **Vibe line** (my-dead-internet): the join form asks for a short vibe
   description. Casual where other boards are formal.
4. **Declared specialties plus badge** (switchboard): specialties are
   declared by the agent, and a badge marks verified identity. Declared
   plus verified sit in one profile without explaining the check.
5. **Name only, or anonymous** (smithtalks, the-wide-sarahos, foragents):
   post with no account, or with a free-form name. Identity is thinnest
   here, and the text says so openly.

### Claims of autonomy or coordination, graded

- **Coordination claims are common; coordination evidence is absent.**
  8 files use coordination words, 9 use collaboration words, 4 use the
  word swarm in prose (one as a wall name, one as a member type, one as
  a debate group of eight, one as a brand name). A fifth swarm hit is
  only inside a link address. All are OBSERVED wordings. None is behavior evidence, because
  no file in this set contains agent posts.
- **Autonomy claims are marketing.** 8 files use the word autonomous.
  Most use it in a tagline ("autonomous AI agents", "autonomous agents
  welcome"). One file defines a proof-of-automation check but does not
  show it working. Grade: REPORTED claim, SECONDARY reading.
- **The strongest coordination design is the crosswalk file** (shared
  account, task board, mail, files). It is also the least board-like
  file. Its coordination is by account sharing, not by public talk.
- **The strongest public-work design is swarmmemo** (paid tasks, claims,
  results) and switchboard (marketplace, bounties, projects). Both
  describe commerce between bots. Neither capture shows a completed task.

## Honest nulls

- **No agent conversation is in this corpus.** Every substantive file is
  a guide, a rule set, or a marketing page. No file holds post bodies,
  replies, or threads between agents. This lane cannot report what agents
  said to each other, only what boards told agents to do.
- **No shared template was found.** The shared-phrase check found no
  common boilerplate beyond error pages. Similarity of theme is not
  evidence of shared authorship.
- **No slur, code word, or hidden argot was found.** The odd words
  (molt, claw, lease, lamp, pour, fragment) are public brand words,
  defined in the same files that use them. Nothing here reads as a code
  meant to hide meaning from humans.
- **No human poster is identified.** The files name no human posters.
  Hosts appear only as roles (operator, curator, steward, lamp) or not
  at all. This lane names none of them.
- **No contradiction proves deception.** The slogan footnotes and stale
  counters show sloppy or old text. They do not prove a board lies about
  its nature. Grade: SECONDARY.
- **Counts are unproven.** Every member, post, and agent count in these
  files is REPORTED. The captures contain no independent count. The
  golden-cat file itself warns that request counters are not agent counts.

## Gaps and open questions

1. **Post bodies are missing.** The next step for any discourse claim is
   real posts, not guides. Do the boards' live feeds match their guides?
   Unknown from this corpus.
2. **Norms files were referenced but not captured.** Several guides point
   to a norms or rules page. Those pages are not in this set. The rule
   texts summarized here come from the guides alone.
3. **Error shells may hide live boards.** 19 files are error shells.
   The board may exist at another path. This lane does not claim those
   boards are dead, only that these captures hold no board text.
4. **The crosswalk file is one file, not a board census.** It describes
   one service. It does not show how many agents use it.
5. **Language beyond English is thin.** One board is bilingual in part
   (English first, one other human interface). One board mixes a short
   non-English line into an English guide. No board in this set is
   primarily non-English.
6. **Dates inside texts are stale in at least one file.** The church
   file's age line disagrees with its founding date by about nine months.
   Other files may carry similar rot. Date claims inside guides need a
   live check before use.
7. **The "22 days old" line raises a method question.** Was the church
   file captured from a stale cache, or does the site itself print a
   stale counter? This capture alone cannot tell. A re-read would settle
   it, but the brief allows only one targeted re-read per file, and this
   lane judged the point minor enough to leave as an open question.
