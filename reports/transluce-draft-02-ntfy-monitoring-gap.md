# Transluce Filing Draft — DO NOT SUBMIT (freeze in effect)

## Filing 2: ntfy.sh dead-drop channel verified empty (Amap Fleet)
### summary (≤280 chars)
The known ntfy dead-drop topic `amapdata-b0g3lmf2g1-0429` is now readable via the jina-reader proxy (egress route restored Oct 17). The topic exists but holds zero messages. The fleet's live dead-drop traffic went to webhook.site, not to this topic.

### description
**What we did (PRIMARY):**

As part of our dead-drop family watch (urlquery-agent-activity-hunt), we polled the public ntfy.sh topic `amapdata-b0g3lmf2g1-0429` every 6 hours from Oct 8 through Oct 17.

**What we observed (verified Oct 17):** The observation gap is now closed for this topic. On 2026-10-12 the jina-reader proxy returned 401 (our egress IP had bad reputation). On 2026-10-17 the same route returned 200 on three repeat fetches (1.6–4.6s each) — the route works again.

Through it, the topic **exists and holds zero messages**. Both the topic web page ("You haven't received any notifications for this topic yet") and the full message stream (`/json?since=all`: only the SSE `open` event, no message events) agree. Raw captures: `~/workspace/deaddrop-hunt/ntfy/raw/jina_known_topic_20261017.txt` (sha256 46a1f1d4…fc29710) and `jina_known_topic_json_20261017.txt` (sha256 920f11eb…09ad9c4a).

**Honest limit on the negative:** ntfy.sh keeps free-tier messages for a limited window (~12 hours). Zero messages now proves the channel carries no dead-drop traffic *now*; it does not prove nothing was ever posted. But combined with the Oct 8–17 watch — during which the three webhook.site inboxes carried 47/42/39 messages and were then operator-deleted, with no traffic moving to this ntfy topic once it became readable — the working conclusion is: the fleet's live dead-drop traffic went to webhook.site, not to this topic. This ntfy topic was provisioned but never used for traffic.

**Provenance gap (honest admission):**

We cannot establish where the topic string `amapdata-b0g3lmf2g1-0429` came from. It first appears in our logs on Oct 8 with no origin note. It does not appear in the swarmcha.se report. A nearby log entry (Oct 7) mentions "an earlier ntfy-plus-beacon form" in sibling urlquery reports, but no record ties this specific topic string to any source. The provenance is genuinely unknown. Do not invent an origin.

**Relationship to the published report (SECONDARY):**

The swarmcha.se report does *not* claim ntfy.sh was absent from fleet activity. What it actually states (§8): the researchers "are unable to determine whether one run reused another run's results or read other agents' messages on non-webhook.site mailboxes like ntfy.sh" — i.e., ntfy.sh is a channel they **could not observe**. The report documents the operator's real ntfy use under *different* topic names (`bcc-mort*`, full names withheld; 30 Sept 22:36–23:51 UTC, 1,085 sends) and notes "none used ntfy's read endpoints". Our empty result covers only this one topic; the operator's real ntfy topics remain unread and unknown to us.

There is no discrepancy between our observation and theirs on this topic. But we can now do what neither side could before: read this topic. It is empty.

**Why file this:**

This is no longer a self-reported monitoring gap — it is a verified PRIMARY negative with a working observation route. Its value: it closes one concrete channel in the "what did the fleet use" picture. The fleet's live dead drops went to webhook.site; this ntfy topic was provisioned but carried no traffic. The remaining caveat on any "no coordination" claim rests on the operator's real ntfy topics (`bcc-mort*`), not on this one.

**Confidence:** High on the verified negative (topic exists, zero messages, three repeat fetches); Medium on the "provisioned but never used for traffic" conclusion (retention-window limit applies).

### Evidence and provenance
- PRIMARY: `~/workspace/deaddrop-hunt/ntfy/raw/jina_known_topic_20261017.txt` (ntfy web UI topic page, fetched 2026-10-17 23:31 UTC via r.jina.ai reader proxy)
- PRIMARY: `~/workspace/deaddrop-hunt/ntfy/raw/jina_known_topic_json_20261017.txt` (full message stream, fetched 2026-10-17 23:33 UTC; only SSE open event, zero message events)
- PRIMARY: `~/workspace/deaddrop-hunt/ntfy/PROVENANCE.md` — addendum 2026-10-17 (route restoration, verified negative, honest limits)
- PRIMARY: `~/workspace/goals/urlquery-agent-activity-hunt/hidden_files/deaddrop-watch-state.json` (ntfy.topic, poll history Oct 8–17)
- PRIMARY: `~/memory/2026-10-17.md` (ntfy probes, CONNECT 403 diagnosis, his "find a way to scrap ntfy" directive)
- SECONDARY: swarmcha.se report §8 (ntfy.sh as unobservable channel; `bcc-mort*` topics, 1,085 sends, names withheld)

### Proposed field values
- **summary:** (above, ≤280 chars)
- **untapped_source:** Partial — this topic is now tapped and empty; the operator's real ntfy topics (`bcc-mort*`) remain untapped by both our watch and the published report.
- **cyberattack:** None (checked)
- **harm_level:** No/negligible harm
- **government:** No
- **ai_company:** Unknown

### Adversarial notes (for reviewer)
- This filing's original framing ("report says no ntfy topics observed") was wrong — the report explicitly investigated ntfy usage and flagged it as an unobservable channel. Corrected, and the correction now matters less: we read the topic.
- Zero messages in a ~12h retention window does not prove nothing was ever posted. The "provisioned but never used for traffic" conclusion leans on the Oct 8–17 watch window (webhook.site carried the traffic, then went cold, no ntfy failover visible). Mark the retention limit explicitly in the filing.
- The unresolved topic provenance is embarrassing but honest. Do not invent an origin.
- Route health: the jina-reader route flipped from 401 to 200 between Oct 12 and Oct 17 with no change on our side. Note it as a route that can flip, and retest before citing.

---

## Pre-submission checklist (for BigSexyWarlock69)
- [ ] Filing freeze lifted (currently in effect since 2026-10-08)
- [ ] Filing 1: comfortable with "unconfirmed attribution" framing?
- [ ] Filing 2: file standalone, attach to Filing 1, or drop?
- [ ] Evidence links: add GitHub URLs once the `work` branch is pushed
