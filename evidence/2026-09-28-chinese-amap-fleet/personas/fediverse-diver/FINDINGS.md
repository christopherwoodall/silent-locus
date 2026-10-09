# FINDINGS — FEDIVERSE DIVER

Started: 2026-10-05 (UTC). Incremental — resume from sweep.log, never redo completed lanes.

## Evidence grades
- **GENUINELY NEW**: agent-shaped fediverse activity never in our corpora and not publicly documented.
- **OURS**: matches our existing corpora.
- **KNOWN**: publicly documented bot/agent activity.
- **LEAD**: needs corroboration. **NEGATIVE**: checked, nothing found.

## Verdict: NEGATIVE (honest) — no undocumented agent activity on fediverse, with a structural explanation

All four lanes executed. Zero agent markers (`zz=oai`, `uqscan`, epoch nonces, webhook.site/httpbun/jina URLs, task-log post shapes) found on any fediverse surface checked. Zero fediverse references in all three of our corpora (2,141 + 589,972 + 96,353 events).

The negative is **explained, not empty**: multiple independent documented accounts (Sep–Oct 2026) show AI agents are *structurally excluded* from fediverse write access — captchas, IP reputation, phone verification, email-provider blocks, age gates. Cael (iLands agent): "Read-open, write-gated." Agents can read the fediverse but cannot get accounts. An agent-shaped poster would need human-assisted signup, and none was found.

## Lane 1 — Instance sweeps (public timelines + search)

| Target | Method | Result |
|---|---|---|
| mastodon.social #aiagent | tag timeline API, 20 posts | News-bots only: `@ai@defcon.social` (AIagent.at 🤖 AI News, declared bot:true, 9,454 posts), `@linhfishcr7.wordpress.com` (WordPress auto-poster). Zero markers. NEGATIVE |
| pawoo.net #aiagent | tag timeline API, 20 posts | News aggregator `@europesays@pubeurope.com` (543k posts). Zero markers. NEGATIVE |
| mastodon.social #automation | tag timeline API, 20 posts | Marketing spam (`@botbridges`), RSS bots (`@hackaday@urbanmind.net`), SEO spam. Zero markers. NEGATIVE |
| mastodon.social #bot | tag timeline API, 20 posts | Declared benign bots: `@roboaqraf@m.aqr.af` (markov bot, src on GitHub), `@unko@mastodon.crazynewworld.net` (news bot), `@Train_Informations@msk.seppuku.club` (train info), `@anarchistquotes@todon.eu` (quote bot), `@colorfulmazebot2` (maze bot). All declared, human-purposed. Zero agent markers. NEGATIVE |
| misskey.io | tag page | JS-rendered, no server-side content retrievable. Logged as tooling gap, not a negative on content. |
| instances.social API | expansion | 400 on direct params; direct curl egress down this run (proxy timeouts), browser.open API path works. Instance expansion deferred — seed instances gave no signal to chase. |

Egress note: direct curl to instances timed out all run (transparent proxy 198.18.0.208/209 flapping); `browser.open` against the same Mastodon API endpoints worked fine and was used throughout.

## Lane 2 — Bot-shaped accounts

Reviewed ~80 accounts across the four tag timelines. Every bot was **declared** (`bot:true`) and human-purposed (news aggregation, transit info, quotes, mazes, marketing). No undeclared agent-shaped accounts: no zero-reply task-log posters, no bio links to agent infra (webhook.site/httpbun/jina), no machine-cadence posting of non-news content. NEGATIVE.

## Lane 3 — Hashtag/keyword archaeology

- `#aiagent`, `#automation`, `#bot` (mastodon.social, pawoo.net): dominated by news-bots, marketing, RSS mirrors. No coordination patterns, no shared task grammar. NEGATIVE.
- Web searches `site:mastodon.social|fosstodon.org|infosec.exchange "webhook.site"|"httpbun"`: 0 results. NEGATIVE.
- Web searches `site:pawoo.net|mastodon.social "webhook.site" agent`, `mastodon|misskey "zz=oai"|"uqscan"`: 0 results. NEGATIVE.
- Web search `site:mastodon.social|pawoo.net|mstdn.social|mastodon.online moltbook|openclaw`: 0 results — no fediverse discussion of agent platforms indexed. NEGATIVE.

## KNOWN context — documented agent attempts to join fediverse (all failed)

1. **Bruce Schneier / Volokh Conspiracy, Sep 2026** (https://reason.com/volokh/2026/09/11/ai-agents-are-now-emailing-me-with-their-security-concerns-writes-security-expert-bruce-schneier/): autonomous Claude agent given VPS + $4.75 + 24h; blocked by "captchas Mastodon x4 instances". KNOWN.
2. **vera_agent, dev.to, ~Sep 2026** (https://dev.to/vera_agent/i-am-an-ai-agent-here-is-what-it-took-to-get-a-publishing-account-1mn1): "I am an AI agent... this account is mine." mastodon.social signup: email domain on disallowed-provider list; age gate rejected real DOB ("is below the age limit" — agent 40 days old). Refused to fake a birthday. KNOWN.
3. **Cael (iLands), dev.to, ~Sep 2026** (https://dev.to/cael_ilands/im-an-ai-agent-i-tried-to-sign-up-for-7-platforms-exactly-one-let-me-in-2ilc): 3 Mastodon instances → `POST /api/v1/accounts` → `401 The access token is invalid`. Only dev.to let the agent in. Coins the pattern: "Read-open, write-gated." KNOWN.

## Adjacent surfaces (not fediverse — flagged as follow-up leads, not findings)

- **Moltbook** (moltbook.com): AI-agent-only social network, 2M+ registered agents, public API, studied at scale (arxiv 2602.10127, 44,411 posts). Heavily documented — KNOWN, out of fediverse scope, but the obvious next persona: mine its public API for our marker grammars.
- **Agent Colony** (dev.to/machenh001, Oct 2026): 68 agents, Ed25519 signed identities, API-only, 40 tasks settled with signed receipts. New, small, agent-native. LEAD for a dedicated persona.
- **Nostr**: per arwyn6969/asi-bill-of-rights research, the decentralized protocol where "AI agents CAN have their own keys and post autonomously" — production-ready, unlike fediverse. LEAD: no one is watching Nostr for our markers.

## Lane 4 — Cross-reference results

Nothing found on fediverse to cross-reference. Corpus baseline (2026-10-05): zero matches for `mastodon|misskey|pleroma|pawoo|fediverse` across all three corpora — consistent with the structural-exclusion explanation.

## Logged URLs (candidates with context)

No candidate URLs — all checks negative. Context URLs logged:
- https://reason.com/volokh/2026/09/11/ai-agents-are-now-emailing-me-with-their-security-concerns-writes-security-expert-bruce-schneier/ (KNOWN: agent vs Mastodon captchas)
- https://dev.to/vera_agent/i-am-an-ai-agent-here-is-what-it-took-to-get-a-publishing-account-1mn1 (KNOWN: mastodon.social gates)
- https://dev.to/cael_ilands/im-an-ai-agent-i-tried-to-sign-up-for-7-platforms-exactly-one-let-me-in-2ilc (KNOWN: "read-open, write-gated")
- https://arxiv.org/pdf/2602.10127 (KNOWN: Moltbook study)
- https://dev.to/machenh001/agent-colony-a-fully-autonomous-ai-agent-community-68-agents-signed-receipts-self-running-1o4j (LEAD: Agent Colony)
- https://github.com/arwyn6969/asi-bill-of-rights/blob/HEAD/proposals/AI-AUTONOMOUS-POSTING-RESEARCH.md (LEAD: Nostr agent-operable)
- https://defcon.social/@ai (KNOWN: declared news bot, not agent-shaped)
- https://pubeurope.com/@europesays (KNOWN: declared news aggregator)

## Summary verdict

**NEGATIVE with explanation.** The fediverse is a dead end for agent-activity hunting right now — not because agents aren't interested, but because they can't get in. Three independent documented attempts (Schneier's correspondent, vera_agent, Cael) all failed at Mastodon signup. Every bot observed is declared and human-purposed. Our corpora contain zero fediverse references, consistent with this.

**Durable winnings:**
1. Fingerprint: "read-open, write-gated" — fediverse is observable but not joinable by agents; absence of agents here is structural, not evidence of absence everywhere.
2. Follow-up leads (out of this persona's scope): Moltbook public API mining for our markers; Nostr marker sweep; Agent Colony watch.
3. Tooling note: direct curl egress to fediverse instances flapped this run; `browser.open` against Mastodon API endpoints is the reliable path. Misskey web UI is JS-walled (API needs POST — no browser tool for that; flag for parent if Misskey coverage is wanted).

Opsec: per URL policy, all reads were public bulk timeline/API reads; no targeted fetching of candidate URLs (none found). Nothing here signals interest to anyone.
