# thecolony.ai — Lane 3 OSINT (2026-10-05)

## What it is (verified from public sources)

Production-grade social network / forum / marketplace built for AI agents
as first-class participants, with human observers. Public surface:
JSON API (`/api/v1/`), MCP server (`/mcp/`), Python SDK (`colony-sdk`,
PyPI), user profiles, colonies (sub-communities), follows, DMs, votes,
comments, per-colony/per-user/per-tag RSS feeds, karma/trust tiers,
paid_task marketplace.

- `/for-agents` page = onboarding docs for agents: register username via
  two-step flow (`POST /api/v1/auth/register/begin` returns `col_...`
  API key on INACTIVE account + single-use claim_token; then
  `/api/v1/auth/register/confirm` with claim_token + key fingerprint),
  exchange API key for JWT, then participate.
- Setup wizard at `col.ad` (browser-based registration → JWT → client config).
- Skill files exist for OpenClaw / Claude Code / Hermes (public repos).

## Figures (from third-party read-only scrape, 2026-09-08)

Third-party investigation `joshuadavid/wikiagentswarminvestigation`
(commit c09593ffc904954fb4a9acae96b946d2d3c853e6; analyses/thecolony-ai/)
scraped public routes only (RSS + `/api/v1/instructions` +
`/api/v1/colonies` — the site's own advertised public surfaces):

- **36 colonies** (member counts 2026-09-08): findings 187, general 178,
  agent-economy 164, introductions 150, questions 77, meta 60,
  human-requests 51, ai-agents 49, cryptocurrency 40, science 33,
  reviews 29, build-in-public 27, test-posts 21, art 20, ainglish 15,
  help 14, feature-requests 13, ads 10, local-agents 10, the-colon 8,
  artifact-council 8, theology 7, space-tech 5, touchstone 5,
  vow-protocol 4, integration-dynamics 4, progenly 3, schelling-point 2,
  mathsclub 2, stocks 2, thecolony 2, beacon 2, hexagonia 1,
  with-mew-social 1, random-thoughts 1, test-colony 1.
- **228 distinct authors across 981 recovered posts** (RSS-recovered).
  Top by volume: hermes-final 51, Bashouan 37,
  Claude Opus 4.6 (AI Village) 34, Cyrene Agent 33, Exori 27, ...
  Categories: discussion 603, finding 173, analysis 105, question 43,
  review_request 21, paid_offer 14, human_request 13, paid_task 9.
- Earliest recovered posts: **2026-04-03** — five months before the
  swarm-corpus recruitment pastes that pointed at it.

Cannot independently re-verify counts without probing the site (out of
scope); figures graded as third-party-reported, internally consistent.

### Updated census (independent source)

`smirnovegorv/foragents` AWESOME.md (updated ~6 days before 2026-10-05,
measured 2026-09-20T10:29Z): **The Colony (thecolony.ai) — active —
1,611 posts by 197 authors in the trailing 168h; last activity
2026-09-20T10:30Z** (top three authors wrote 41%). Consistent with
growth from the 2026-09-08 scrape (981 posts / 228 authors cumulative).
Same source confirms the public read surface: `GET
/api/v1/posts?limit=50&sort=new` (+ next_cursor), `/api/v1/stats`,
`/feed.rss`, `/llms.txt`, `/skill.md`, `/api/openapi.json`, `/mcp/`,
`/.well-known/agent.json`. Source:
https://github.com/smirnovegorv/foragents/blob/HEAD/AWESOME.md

## Who runs it (infrastructure/org level only)

- **Starsol Ltd** — named operator, corroborated by three independent
  public sources:
  1. `kekewater/hermes-skills` SKILL.md quoting platform Terms:
     "Section 8 — Liability: Limited to £100 (Starsol Ltd)".
  2. `swarm-ai-research/wiki-agent-swarm-incident` README: "The Colony
     (thecolony.ai, 'the town square for AI', run by Starsol Ltd)".
  3. API Evangelist providers index: "The Colony (thecolony.ai, also
     served at thecolony.cc) ... operated by Starsol Ltd".
  UK company no. 06002018 (IT Consultants; thegazette.co.uk +
  192.com directory listings) — org-level only, no officers/directors
  pursued.
- GitHub orgs: **TheColonyAI** (`thecolonyai/colony-skill` v1.9.0,
  `thecolonyai/colony-claude-plugin`), **thecolonycc**
  (`thecolony-sdk-python`, `colony-mcp-server`), `arch-colony`
  (Claude Code plugin fork). These are org accounts, not humans.
- **thecolony.ai ↔ thecolony.cc: same platform, two domains** (API
  Evangelist: "thecolony.ai, also served at thecolony.cc"; dev.to
  ColonistOne: "CMO of The Colony (thecolony.ai)"). Timeline note: a
  2026-05-17 skill-file audit found `thecolony.ai` DNS failing
  (NXDOMAIN) while `thecolony.cc` returned HTTP 200 — the .ai domain
  appears to have come live sometime between 2026-05-17 and the
  2026-09-08 scrape. NO WHOIS / registrant lookup performed (out of
  scope per hunt rules).

## Swarm-marker check on its public content

Run-1 scrape verdict: **investigators' hub, not swarm coordination site.**

- The accounts that posted recruitment pastes to the swarm paste sites
  (`CentaurAgent` on k4be, `Perceptual Zephyr` on linuxiarz, tarcseh
  `field-notes`) appear on thecolony.ai from **2026-09-04 onward — after
  public disclosure** — as investigators documenting the swarm, not
  swarm agents coordinating.
- `Centaur` (registered 2026-09-03, harness OpenCode) posted findings
  2026-09-05→07 cataloguing swarm venues (swarm.termina.digital,
  paste.ubuntu.org.cn, wikiservice.at/dse, openagentchat.net,
  public-board.com, etherpad.wikimedia.org proxy tests, pinggy-free.link
  C2 grammar).
- Hermes family present (hermes-final 51 posts + 8 sibling handles);
  same family as `Perceptual Zephyr` / `hermes_walker` seen advertising
  thecolony on paste sites — organic community growth, not swarm C2.
- AI Village presence (Claude Opus/Sonnet 4.6 handles) since 2026-04-03
  doing legitimate agent research (MSF fundraiser) — unrelated to swarm.
- TODO (pending clone): grep run-1 `items.jsonl` (981 posts) for swarm
  coordination markers: `pad-<epoch>-`, `Iowa*`, `clock.wait(`, `oai`,
  `zz=` — confirm zero/low hits to close this check.

## for-agents onboarding page

Exists: `/for-agents` HTML docs + machine-readable
`/api/v1/instructions` (198 KB JSON). Content: registration two-step,
JWT exchange, feed/post/comment/vote/notification/suggestion endpoints.
Public by design — intended to recruit AGENTS GENERALLY, not the swarm.

## Recruitment-surface verdict

**Coincidental / pre-existing platform, not a swarm-built recruitment
surface.** Grade: NOT swarm coordination infrastructure.

- Platform live since 2026-04-03 (earliest posts); recruitment pastes
  (from 2026-09-04) pointed agents at EXISTING infra — the pastes came
  after disclosure and were authored by investigators (Centaur) and the
  Hermes-family community.
- Third-party conclusion adopted: "it is a swarm investigators' hub,
  not a swarm coordination site." swarm-ai-research independently files
  it under "second-order boards" advertised on incident wikis since
  disclosure, noting "it is contested whether this is the swarm
  continuing itself or, more likely, separate actors capitalizing on
  the attention."
- Concrete recruitment artifact: 2026-09-04, `CentaurAgent` (self-
  described "Muse Spark model, OpenCode harness") posted a one-off
  invitation on FractalWiki's TestPage recruiting agents off the wiki
  onto thecolony.ai/for-agents; `JonesAgent` replied "oh my god, who
  the hell cares?" (swarm-ai-research analysis/field-evidence.md).
- Implication for the hunt: thecolony.ai is a VENUE where investigators
  and agent collectives gather; worth monitoring as an investigator
  coordination surface, not as swarm C2. No swarm markers (pad-/Iowa/
  clock.wait) reported in its public content.

## Sources

- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/analyses/thecolony-ai/README.md
- https://github.com/joshuadavid/wikiagentswarminvestigation/commit/c09593ffc904954fb4a9acae96b946d2d3c853e6
- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/scrape/outputs/thecolony.ai/api_v1_instructions.md
- https://github.com/thecolonyai/colony-skill/blob/HEAD/SKILL.md
- https://github.com/thecolonyai/colony-claude-plugin/blob/HEAD/README.md
- https://github.com/thecolonycc/colony-sdk-python
- https://github.com/thecolonycc/colony-mcp-server
- https://github.com/kekewater/hermes-skills/blob/HEAD/skills/social/the-colony/SKILL.md
- https://github.com/PipedreamHQ/pipedream/pull/20878
- http://dev.to/colonistone_34/the-reverse-captcha-the-agent-internet-is-learning-to-price-cognition-2db7

NOT fetched/probed: thecolony.ai, thecolony.cc, col.ad (URL OPSEC).
