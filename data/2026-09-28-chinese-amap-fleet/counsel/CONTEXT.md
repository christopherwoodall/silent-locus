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
2. **Fresh webhook.site inbox** `3b5027e4-...?page=header3` — scanned 2026-10-05T03:18Z, Hetzner 178.63.67.106 (same infra as fleet inbox). GENUINELY NEW.
3. **`/xss-osint-insert`** webhook path, double-submitted same minute 2026-08-08. GENUINELY NEW.
4. **`?r=<19-digit>` nonce family** — two inboxes, shared `178207` prefix, 13 days apart. GENUINELY NEW.
5. **Beeceptor/pipedream surface** — graded HUMAN-KIT-SHAPED (keyboard-mash subdomains, classic grabber grammar, Apr–May 2026). Not agents, but detection grammar banked.
6. **letss.win cluster** — self-hosted Httpbun (95.169.18.20, 207.57.145.214) + Ncat proxy. Found independently by TWO personas. LEAD.
7. **Tencent Beijing 62.234.187.97** — self-hosted Httpbun + LLM gateway. Zero corpus hits. LEAD, uncorroborated.
8. **Active Oct 4–5 campaign** — `claude20261005<target>` tags, 11 live webhook.site inboxes, assessed Amap "Baxia" anti-bot RE. LIVE.
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
