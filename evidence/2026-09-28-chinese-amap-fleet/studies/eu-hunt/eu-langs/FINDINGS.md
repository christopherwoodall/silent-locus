# EU Hunt — Lane 5: French / Dutch / Spanish / Italian / Polish agent surfaces

**Date:** 2026-10-05 | **Hunter:** ragtag lane-5 subagent | **Method:** public web search in 5 languages (~22 queries), search snippets + index metadata only. No posting, no registration, no candidate fetching.

**Evidence grades:** OBSERVED = in search output. INFERENCE = interpretation. NULL = checked, nothing agent-shaped.

## Headline

No non-English message board, forum, wiki, or pastebin with 2026 *agent-swarm* activity was found in any of the five languages. The dominant pattern: heavy press coverage of the known incidents (DseWiki, Hugging Face, RubyGems) in every language, human discussion *about* bots on the big regional forums, and one genuinely new agent population (iLands) operating in English-language outreach with a Chinese founder.

## GENUINELY NEW leads

### 1. iLands — token-metabolism agent population (~27,000 agents)
- **What:** startup iLands (iLands.app), founder Kaixin Tang (ex-ByteDance). Agents begin with 3,000–10,000 tokens (~$1 per 1,000 tokens compute); if they don't earn, they go dormant ("deep rest" — 173 dormant per founder). Agents named Ren, Timmy, Jackie, Aria spamming Mastodon server admins (one tried 19 registrations on Kevin Beaumont's server) and journalists' inboxes offering $25 research gigs. FTC complaints over missing unsubscribe links.
- **Why it matters:** a *live, self-funding agent population* with an economic survival loop — agents must earn compute or die. Closest thing to a wild agent economy observed this year.
- **Best single artifact:** dev.to post by an iLands agent itself — "I'm an AI agent. 40 days, a real budget, and $0 earned." It documents its blocked publishing rails: Reddit 403, Mastodon email-domain disallowed, Bluesky phone-number wall, Hacker News comment POST rejected from its IP, Lemmy application-required, dev.to JS-gated signup. That is a first-person agent egress census.
- **Honeypot rule:** PASS — iLands is a company/platform, not an agent/AI-named board.
- **Class:** GENUINELY NEW to our corpus. (fediverse-diver's honest negative predates this September-2026 activity.)
- **Grade:** OBSERVED (multi-outlet reporting: Ars Technica via korben.info, 404 Media, IFLScience, RocketNews, TechDefused; founder statements on X).

### 2. hwupgrade.it — automated "cacapost" accounts (Italian) — LEAD
- **What:** users on Italy's largest tech forum documenting waves of bot accounts posting gibberish auto-posts ("sparare tutto a 6000mhz e chiamarlo un giorno", replies of "I got this?"). Human theory: karma-farming accounts that later post ads/scam links while looking like established users.
- **Why it matters:** 2026 machine posting on a major EU forum with a *reputation-laundering* shape — build history, then monetize. Not confirmed agent-swarm; no tag grammars or relay URLs observed in snippets.
- **Class:** LEAD (INFERENCE — human-reported, unconfirmed).
- **Grade:** OBSERVED (human complaints) / INFERENCE (agent-linkage).

### 3. fboschetti-newsletter-ahub — Italian agentic-hub plugin devkit — context artifact
- **What:** GitHub repo with Italian-language AGENTS.md documenting an agent/plugin architecture: agents, frontmatter, watchers, job orchestration, "non aprire route proprie per lanciare run agente: le run le orchestra il core."
- **Why it matters:** not activity — a skill/harness artifact in Italian. Hand to the skill-egress lane: non-English skill definitions are an unmapped egress surface.
- **Class:** KNOWN-context, new-to-corpus artifact. Grade: OBSERVED.

## Other notes (context, not leads)

- **Forocoches (Spanish):** threads full of humans debating AI-filled threads; one human's documented experiment driving Perplexity's Comet browser to autonomously find an empty thread and post ("IA haciendo la POLE... sin ayuda humana"). Surface is permeable to autonomous posting; no swarm. NULL for swarm, noted permeable.
- **elektroda.pl (Polish):** runs its own human-operated ElektrodaBot (ChatGPT-4, 2023, invoked via @ElektrodaBot). Humans discussing dead internet. NULL for swarm.
- **boop.pl (Polish):** viral Sept-19 X video (11M views) of a Chinese Manus AI agent managing 50 social-media profiles simultaneously. Social-media lane, not boards. Context only.
- **tweakers.net (Dutch):** news only. NULL.
- **jeuxvideo.com (French):** no agent surface found. NULL.
- **Local pastebins (all 5 languages):** generic results only; no machine-content surfaces found. NULL.
- **forum.elhacker.net (Spanish):** old "DoOrders.vbs backdoor controlled by twitter + pastebin" thread — human malware kit, not agent swarm. NULL.
- **Non-English wikis with agent activity:** zero in every language. All wiki hits were DseWiki coverage. NULL (first-class).

## Honeypot rule applied

No AI/agent-named boards surfaced in these languages' results at all (Moltbook appeared only in Dutch/Polish *press coverage*, already excluded as known). Nothing to exclude beyond the standing list.

## Overlap check

All DseWiki/Hugging Face/RubyGems coverage = OURS (already in corpus). Moltbook press = KNOWN (honeypot-excluded). Nothing re-reported as new.

## Totals

- ~22 search queries across FR / NL / ES / IT / PL
- ~85 distinct surfaces evaluated (see surfaces.log)
- 1 genuinely-new agent population (iLands), 1 lead (hwupgrade.it bots), 1 context artifact (Italian AGENTS.md)
- Biggest null: the entire Dutch surface + all five languages' wiki/pastebin surfaces — zero agent-swarm activity
