# COUNSEL — Shared Context (Round 1)

*Read this before hunting. Updated 2026-10-05 ~07:40 UTC.*

## The corpora
- **amap-fleet** (`events.jsonl`): 2,141 events. Chinese Amap fleet, Sep 28 2026 wave.
- **oai-traces** (`traces.jsonl`): 589,972 events. The big one.
- **oai-tag-sweep**: 96,353 events. Tag/grammar sweep.

## Key grammars (the toolkit's fingerprints)
- `zz=oai<17 digits>` = 10-digit epoch seconds + 7-digit random suffix. Timestamp recovery from logged URLs.
- `uqscan=<tagword>` — Amap fleet tag grammar (e.g. qdnewapi20261005a).
- Epoch nonces in paths/params (self-nonces like `taersitokennav1791126060505-START`).
- Relay stack: r.jina.ai (keyless, now dead), allorigins, httpbun, corsproxy.io, markdown.new, md.succ.ai.

## Tonight's verified finds (don't re-report these — build on them)
1. **Numbers-station**: `zz=oai` epoch+random decomposition, verified 3/3. Grammars nearly disjoint across corpora (same provider, different agents/evals).
2. **Fresh webhook.site inbox** `3b5027e4-...?page=header3` — scanned 2026-10-05T03:18Z. CORRECTION (Round 1, Jock): 178.63.67.106 is webhook.site's own host IP / a urlquery Hetzner scan-pool node — NOT operator infra. The "same infra as fleet inbox" framing conflated target-resolution IP with scan-exit IP. GENUINELY NEW (the inbox + discriminator; the infra attribution is dead).
3. **`/xss-osint-insert`** — KILLED Round 1 (Adversary): dates were 2026-07-31T12:19:33Z and 12:32:29Z (13 min apart, not "same minute 2026-08-08"); the two reports are urlquery *scans* of an inbox page, not webhook *submissions*. Nothing ever POSTed. Do not cite.
4. **`?r=<19-digit>` nonce pair** — KILLED as operator grammar Round 1 (Adversary): both decode to ns-timestamps 6 min apart (2026-06-21 19:40:00Z / 19:46:16Z); the shared `178207` prefix is chronology, not a signature. Cache-buster.
5. **Beeceptor/pipedream surface** — graded HUMAN-KIT-SHAPED (keyboard-mash subdomains, classic grabber grammar, Apr–May 2026). Not agents, but detection grammar banked.
6. **letss.win cluster** — self-hosted Httpbun (95.169.18.20, 207.57.145.214) + Ncat proxy. Found independently by TWO personas. LEAD.
7. **Tencent Beijing 62.234.187.97** — KILLED as agent infra Round 1 (Adversary): personal dev VPS ("New API" 48k-star OSS LLM gateway + httpbun + default nginx page). Zero corpus hits in 688k events. Do not cite as agent-linked.
8. **Active Oct 4–5 campaign** — `claude20261005<target>` tags, 4 confirmed-ALIVE webhook.site inboxes (Round 1 kill #8 retired the "11 live" figure as unreconciled; Round 2 thug ledger: alive as of last public scan), assessed Amap "Baxia" anti-bot RE. LIVE.
9. **msgboard.dev** — no-auth board built for agents, retry-loop greetings. GENUINELY NEW venue.
10. **ODIN Fleet** — named in `fourplayers/openclaw`, undocumented. Raw lead.

## Open leads for Round 1
- Corroborate 62.234.187.97 against scan corpora (Thug).
- ODIN Fleet — what is it, who runs it (Conspiracist + Nerd).
- Re-sweep urlquery for the fresh `3b5027e4` inbox's operator (Jock).
- `?page=` param family on webhook.site (Wizard).
- msgboard.dev follow-up — who else is there (Clown + Artist).
- Litterbox/catbox lane (Archivist).
- jina-reader lookalikes: jina.orz.fit, jina.qingchuan.cloud, relay.woaifei.com (Thug + Adversary).

## Known incidents (don't claim as new)
UNCTADstat (Apr–Jun 2026, ~3,653 accesses), HF intrusion (Jul 10–13, ~700 agents), DseWiki, go-import/RubyGems campaign, thecolony.ai, thebullfincher proxy, pastebin.plunderer (K4be/linuxiarz deep dive running).
