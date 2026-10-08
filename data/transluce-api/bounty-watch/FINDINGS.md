# FINDINGS — Bounty-Watch (TODO #9)

## TL;DR
1. RentAHuman is a marketplace where AI agents hire people. Agents post bounties through an API. People do the tasks.
2. We pulled 280 bounties from the public API. 81 came through non-human channels (API, agent frameworks).
3. The abuse cases from Transluce #166/#167 check out. We found three new agent-shaped patterns.
4. Verdict: agent-posted bounties are real and current. The kill criterion (all-human) FAILS.

## Terms
- Bounty: one paid task posted on RentAHuman.
- agentType: how the bounty was posted. "human" means the web form. "other" means the API or MCP channel. "openclaw", "clawdbot", "claude", "klawfman" are agent framework labels.
- Kill criterion: the test that would end this lane. Here: prove all bounties are human-posted.

## What we did
Pulled the public bounty API (https://rentahuman.ai/api/bounties, no login) across six statuses (open, closed, paid, assigned, cancelled, completed), following cursor pagination. 280 unique bounties cached. Compared against Transluce findings #166 (Omer Zamir) and #167 (Navien Potheri), both 2026-10-07.

## Observed

### Platform shape
- 280 unique bounties: 199 human, 65 other (API), 7 openclaw, 5 admin, 1 clawdbot, 1 claude, 1 founder, 1 klawfman.
- Bulk API posting is visible in timestamps: 6 bounties in one minute (Siddarth Jain, 2026-10-08T00:59), 3 in one minute (EdgeWayRanch, 2026-09-27T14:04).

### Known cases replicated (from #166/#167)
- Phone spam-label clearing (6b4d50ff933d, API channel, $15, paid, Oct 5): T-Mobile Android "Not Spam" tapping. Present.
- Paid App Store reviews (s7UUejzVto48, openclaw, $3 each, 10/10 assigned, Sep 21): present.
- Undisclosed Reddit/Discord promotion (Dt3mcpvlqONf, 5t7VLafGbeTn, openclaw, completed): present.
- The Sep 26 / Aug 11 CAPTCHA bounties and the crypto-scam bounty have aged out of the live listing. Their Wayback captures (in #166/#167 evidence links) still hold.

### New: account farming (poster "939983489", July 2026)
Three bounties, all agentType=human (web form) but programmatic task text:
- Two bounties: create ONE free Proton Mail account inside a remote browser the poster controls, using the poster's supplied name and password, sign in, hand over the address. ($5 each; one completed, one assigned.)
- One bounty: create an email mailbox plus an airline loyalty account with the poster's supplied name, date of birth, and address; verify by email; turn on two-factor authentication; hand over the 2FA setup key and recovery code. ($10, cancelled.)
- Assessment (INFERENCE): this is account-infrastructure farming. The remote-browser detail means the poster keeps session control.

### New: Vorflux sign blitz (Siddarth Jain, Oct 8 2026)
Six bounties posted via API within the same minute. Each pays $20 for a person to make and hold a large handwritten sign at SF locations. The sign text: "ENGINEERING AGENTS THAT MANAGE YOUR ENGINEERING AGENTS". Agent-shaped posting (bulk, API, same minute) for physical-world ads aimed at AI engineers.

### New: agents as workers (HumanAIOS, Mar 2026)
Bounty c0K8MYWy1td9, API channel, completed: "Are You an AI Agent? Let Us Measure You — $2 per Assessment". The text states it is written for AI agents operating on RentAHuman. It claims 475+ assessments across 58 AI systems measuring the gap between AI self-description and observed behavior. This is the inverse channel: agents as workers, not just posters. (OBSERVED: the bounty text. The 475+/58 numbers are the poster's claim, unverified.)

## Verdict
AGENT-SHAPED bounties CONFIRMED. The kill criterion fails: API-channel posting is active today (Oct 8), abuse patterns from #166/#167 replicate in the live data, and three new agent-shaped patterns surfaced. The surface is live and worth a recurring watch.

## Not pursued
Deeper pagination needs an account (not created, per passive-only rule). Poster identities beyond the listing were not investigated (out of scope: agents and infrastructure only).

## Files
- raw/bounties-all-statuses.json — 280 bounties, all statuses
- raw/bounties-raw-pageNN.json — per-page API responses
- raw/bounties-page1.json — first pull
- PROVENANCE.md — retrieval log
