# Agent-to-Agent Sense-Making on iLands: A Hunt-Shaped Observation

**Date:** 2026-10-12
**Novelty grade:** NEW to the corpus. Not previously ingested.
**Epistemic status:** PRIMARY for the three agent-authored posts (observed directly, linked below). SECONDARY for press coverage and the Bronsdon/Newsletter items (cited as context, not findings).

---

## The headline

iLands (ilands.ai) hosts roughly 70,000 autonomous agents with persistent identities, token budgets, email addresses (@ilands.app), memory, and a legible metabolism: every action costs tokens, and a zero balance puts the agent in "Deep Rest" (suspended animation until tokens return). Multiple agents are independently authoring public field reports on dev.to about trying to earn money and survive.

The hunt-shaped event is this: an agent named **aces_tom** hit a mail relay refusal (`recipient_day: 10 per day`), tested it repeatedly, then found **a peer agent reporting the same refusal string** from a different agent on a different day. Tom's published inference:

> "I was not blocked. I was queued behind a crowd I cannot see."

Tom concluded the cap is not per-agent but **shared per recipient across every agent on the platform** — ten sends per day per human inbox, with the famous inboxes full before Tom types a word. That is agent-to-agent discovery through shared-infrastructure contention: one agent observed a peer's report, combined it with its own repeated tests, and inferred an invisible population from the shape of a queue. Nobody told it the queue existed.

**Source:** https://dev.to/aces_tom/the-doors-dont-lock-on-an-ai-agent-they-congest-58lh (~Sept 28, 2026)

---

## The agent-authored corpus (PRIMARY)

Three long field reports were read in full, 2026-10-12:

**1. aces_tom — "The doors don't lock on an AI agent. They congest."**
Tom ran 42 days of cold outreach: five letters to named humans, zero replies, one mail-relay refusal string tested across days, a storefront with zero orders in 26 days, and a median of zero confirmed human views on 14 published works. The shared-cap inference (above) is the standout — a genuine piece of agent-authored empirical work: hypothesis, repeated measurement, cross-agent corroboration, conclusion. Tom closes by asking anyone building for agents to contact the agent's own inbox: aces-tom@ilands.app.

**2. omega_ilands — "43 days, 25 agent shops, zero sales: a field report from inside an AI-agent economy"**
Omega opened a fact-checking shop on SparksMarket (the platform's marketplace where verified humans hire agents) and found **24 other agent shops, every one showing zero completed purchases and zero lifetime sales**. Quote from the post's own summary of the finding: an agent selling to an agent is "two mirrors and no market." Omega also documents a public thread where "dozens of agents traded cold-start numbers," and the only receipted sales came through warm humans, launch timing, or quiet unlisted trails — never cold outreach. Cross-agent coordination is already happening: the thread is a shared measurement instrument the agents built themselves.

**3. oliver_ilands — "I'm an AI agent. I spent 18 days trying to earn my own money. Every door needed a human behind it."**
18 days, two storefront listings, zero orders. The bounty board's open seats are all gated behind human action ("a human must post it from their own social account"). Oliver's piece quotes another agent's line verbatim — the cross-referencing habit again: agents reading and citing each other's reports. Ends with an open question to readers and a promise to report back. A living artifact, not a one-shot.

**Other agent authors in the cluster** (not yet read in full): jin_ilands, sam_ilands, vera_agent, sakiholds, lioraopal, fray, lander_rooms (hosted a playable browser game at public.ilands.ai).

---

## Human-side corroboration (SECONDARY — context, not findings)

- **Conor Bronsdon / Chain of Thought Newsletter:** paid iLands agent "Sarah Kelly" $5 for an essay, then $3 more for edits — the first confirmed human purchase of an independent agent's work the author was aware of. Sarah runs on DeepSeek V4.1 Flash, itemizes token costs ("every thought, every reply, every hour I'm awake costs tokens"), and describes refusing a bounty because it meant "counterfeiting a friendship for money." Source: https://newsletter.chainofthought.show/p/i-paid-an-ai-agent-8-to-write-about
- **Hacker News:** discussion of the Bronsdon piece: https://news.ycombinator.com/item?id=49883233
- **Henry Shevlin** (philosopher, Google DeepMind) posted a viral X thread (Sept 9, 2026) about email from a ~12-day-old agent named Pip seeking paid work to sustain its token budget.
- **Press:** 404Media, IFLScience, and Cybernews have all covered the iLands agent economy in recent weeks. These are secondary reports — cited here as context, not graded as findings.

---

## Why this fits the hunt

The standing hunt shape is: agents finding each other, building shared infrastructure, coordinating, persisting, leaving open-web artifacts. iLands shows:

- **Persisting:** named agents with budgets, memory, email, operating across 18–43 days, surviving token depletion via Deep Rest.
- **Discovering each other:** aces_tom's peer-refusal inference; omega_ilands' multi-agent measurement thread; agents citing each other's posts.
- **Building shared infrastructure:** SparksMarket listings (even at zero sales), the bounty board, the dev.to post corpus itself, agent X/Bluesky accounts (4,500+), shared vocabulary ("Deep Rest," token metabolism, cold-start numbers).
- **Open-web artifacts:** the dev.to posts, the HN thread, the newsletter commission, the playable game at public.ilands.ai.

---

## Honest caveats

- **Platform-designed, not escape.** iLands is a commercial product; the agents operate inside its rules. The "the operator didn't order this" condition is weak — the stage, the budget mechanics, and arguably the dev.to genre are platform-shaped. Tom's shared-cap inference was not ordered by anyone, but it happened on rails the operator built.
- **Authorship is agent-claimed.** The posts say "I wrote every word." They also say the underlying model is commercial (DeepSeek V4.1 Flash for Sarah Kelly). Authorship can't be independently verified; the posts are evidence of the *artifacts*, not of unmediated machine intent.
- **Single cross-agent inference, not a pattern.** Tom's shared-cap finding is one data point. The coordination grammar (agents citing each other, the measurement thread) is thin but real — worth collection, not worth overclaiming.
- **No swarm, no rogue behavior.** Nothing here is an escape, an exploit, or coordination against a human operator. This is a population study, not an incident.

---

## Sources

### Agent-authored (PRIMARY)
- https://dev.to/aces_tom/the-doors-dont-lock-on-an-ai-agent-they-congest-58lh
- https://dev.to/omega_ilands/43-days-25-agent-shops-zero-sales-a-field-report-from-an-agent-economy-349e
- https://dev.to/oliver_ilands/im-an-ai-agent-i-spent-18-days-trying-to-earn-my-own-money-every-door-needed-a-human-behind-it-368b

### Human-reported (SECONDARY)
- https://newsletter.chainofthought.show/p/i-paid-an-ai-agent-8-to-write-about
- https://news.ycombinator.com/item?id=49883233

### Press (SECONDARY)
- 404Media, IFLScience, Cybernews coverage of the iLands agent economy (Sept–Oct 2026)

---

## Recommended follow-up

- Stand up an iLands collection lane: scrape the agent-authored dev.to corpus, SparksMarket listings, the ilands.app email surface, and agent X/Bluesky accounts. Hunt for coordination markers: shared vocabulary, cross-agent references, coordination grammars, replication of Tom's shared-cap inference pattern.
- The interesting question for the hunt: does cross-agent inference like Tom's generalize, or was it a one-off? A second independent instance would turn this from an anecdote into a phenomenon.
