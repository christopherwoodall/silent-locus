# Transluce Filing Draft — DO NOT SUBMIT (freeze in effect)

## Filing 1: Post-Report Beacon Activity Matching Chinese Amap Fleet Tradecraft
### summary (≤280 chars)
On 2026-10-14, six days after the published observation window closed, our dead-drop watch logged a 4-request beacon session matching the Chinese Amap fleet's scraper state machine. New POI, new source IP. Fleet continuation, successor, or imitator — unconfirmed.

### description
**What we observed (PRIMARY):**

On 2026-10-14 at 08:31:33–08:31:51 UTC, our dead-drop watch (`deaddrop-family-watch`, 6h cadence) logged 4 new POST requests in webhook.site inbox B (count 35→39). The 18-second session followed the known Amap scraper state machine exactly:

1. `{"t":"start"}` boot beacon
2. `e-old` — ditu.amap.com/detail/B00190BBTX (hit slider CAPTCHA)
3. `b-ssr-www` — amap.com/ssr/place (19.4k chars)
4. `c-www-place` — amap.com/place (7.7k chars)

New indicators in this session:
- POI `B00190BBTX` (Mochou Lake Park) — first *fleet-scraper beacon post* referencing this POI in inbox B. Note: the same POI string appeared in inbox B on Oct 8 in a third-party message from mailbox.termina.digital (the researchers' honeypot), not a fleet post.
- Source IPv6 `2601:644:8100:23e0:ac6e:9b2a:7712:4b9f` (Comcast/Xfinity range), Edge/155 UA — not previously seen in inbox B. Prior B sources: 195.64.118.152 (dominant), 36.95.1.159, 173.239.236.28, 96.76.222.193.
- No zz=/oai*/epoch grammar markers; no interrogator-style free text.

Approximately two hours later (10:26 UTC run), all three monitored inboxes returned 404 (inbox B had been live at 09:27 UTC). Counts frozen at last-seen: A=42, B=39, original=47.

**Why this matters (SECONDARY context):**

The swarmcha.se full report (https://swarmcha.se/posts/chinese-agent-fleet-full-report) documents the Tencent Cloud Amap fleet's activity between Sept 28 and Oct 8, 2026, with 2,600+ extraction attempts. Our session occurred **six days after their window closed**.

**Three hypotheses, none confirmed:**

1. **Fleet continuation** — the same operation was still running. Supports: exact state-machine match, same inbox infrastructure.
2. **Successor task** — a new eval or task family reusing the tradecraft. Supports: new POI, new source IP.
3. **Imitator or researcher** — someone else running the same pipeline. Supports: the Comcast/Xfinity US residential IP does *not* match the fleet's Tencent Cloud HK egress profile. This is the strongest counter-indicator.

**What we cannot claim:**

- We cannot attribute this session to the original Tencent fleet. The source IP geolocation (US residential) contradicts the fleet's established infrastructure (Tencent Cloud Hong Kong, AS132203).
- Four requests is a minimal sample. We describe the pattern match, not a confirmed operation.
- The 404 may be webhook.site's 7-day free-inbox prune (inbox B was created ~Oct 7), not operator deletion.

**Confidence:** Medium that the *tradecraft* matches; Low on *attribution* to the original fleet.

### Evidence and provenance
- PRIMARY: `~/workspace/goals/urlquery-agent-activity-hunt/hidden_files/deaddrop-watch-state.json` (inbox B: count 39, newest_ts "2026-10-14 08:31:51", status 404_inbox_gone as of 2026-10-14T10:26Z run)
- PRIMARY: `~/memory/2026-10-14.md` (beacon session details, pattern, IP, POI)
- SECONDARY: swarmcha.se report §Technical Overview (Sept 28–Oct 8 window, 2,600+ attempts); §How we found the fleet (inbox census, hysandbox-ats proxy)

### Proposed field values
- **summary:** (above, 276 chars)
- **untapped_source:** No — the inboxes are deleted; this specific channel is cold.
- **cyberattack:** None (checked)
- **harm_level:** No/negligible harm
- **government:** No
- **ai_company:** Unknown (agents claimed Claude/Anthropic per the report, but identity is unverified — do not assert)

### Adversarial notes (for reviewer)
- Weakest claim: fleet continuation. The US residential IP is a serious attribution problem.
- The POI "novelty" was initially overstated — corrected: the string appeared Oct 8 via a third party.
- Filing value: documents post-window tradecraft reuse regardless of attribution. The pattern match itself is the finding.

---

