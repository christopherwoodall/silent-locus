# FINDINGS — IMAGEBOARD SCOUT

Last updated: 2026-10-05 07:45 UTC (run 1)
Status: ACTIVE — first pass complete, open threads logged for follow-up.

## Method
Public boards/archives only. No posting, no interaction, no accounts. URL policy: LOG every thread URL with context; no live-fetching beyond reading the public thread/archive page itself (opsec — a fetch tips operators/vendors). Verification = corpus cross-reference + search-engine corroboration.

Corpora for classification: `data/2026-09-28-chinese-amap-fleet/events.jsonl`, `data/2026-10-03-openai-agent-traces/events.jsonl`, `data/2026-10-01-oai-tag-sweep/events.jsonl`.

## Verdict so far: no undocumented agent activity found on imageboards — but one genuinely new hunt surface discovered

## Lane 1 — Seed boards

### GENUINELY NEW (venue): thread-puller.party — live /g/ catalog mirror
- **What:** `https://thread-puller.party/g` serves a live mirror of 4chan's /g/ catalog, current to Oct 5 2026 (image timestamps `1791183...` = Oct 5 2026).
- **Why it matters:** read current /g/ threads (including /aicg/ AI Chatbot General) without fetching 4chan directly. New hunt surface nobody in our operation was using.
- **Key venue spotted:** `/aicg/ - AI Chatbot General` ("Miku Edition") — the standing /g/ general for AI chatbot discussion/development. Previous thread `https://thread-puller.party/g/thread/109953145` (read: image-only extraction, post text did not render — tooling gap).
- **Also present:** /sdg/ (Stable Diffusion General), /ptg/, /fglt/, /csg/, /twg/, /mkg/, /pcbg/.
- **Caveat:** thread-view pages render images but post text did not extract via text fetch. Catalog view renders OP text. Follow-up: better extraction path for thread bodies.

### BLOCKED (leads for live-browser follow-up)
- `https://endchan.org/` — fetch policy-blocked from this environment. Boards (esp. /tech/, /pol/) unverified.
- `https://8kun.top/` — fetch policy-blocked from this environment. /tech/, /v/ unverified.

### Archive status map (for future runs)
| archive | /g/ coverage | search | status from this env |
|---|---|---|---|
| 4archive.org | yes, frozen Feb 2021 | n/a (browse) | WORKS via text fetch |
| archived.moe | yes, current | yes | homepage loads; **search endpoint 403** (Cloudflare) |
| desuarchive.org | yes (/g/ confirmed in board list) | yes | homepage loads; **search endpoint 403** (bot protection) |
| warosu.org | yes | yes | not yet attempted (Cloudflare per docs) |
| 4plebs | no /g/ (/pol/, /x/ etc.) | yes | not attempted (strict anti-scraping per arxiv paper) |

## Lane 2 — Agent-shaped posting hunt
- **No agent-shaped posting found** in the /g/ catalog snapshot (Oct 5 2026). Catalog OPs are human-typical: generals, tech support, AI discussion. No nonce grammars, no task-log formatting, no "as an AI" self-descriptions in visible OPs.
- **Notable human context:** /aicg/ OP tracks model releases (GPT-6.1 Sol, Sonnet 5.5, Opus 5.5, MiMo 2.6, DeepSeek V4.1, GPT-6 Astra) with frontends (SillyTavern, RisuAI, Agnai), bot directories (chub.ai, realm.risuai.net), jailbreak listings, and lore (`rentry.org/aicg_chronicles`). This is the venue to watch for agent self-reports.
- **Human agent experiment (context):** dev.to "Day 15: My AI Agent Still Can't Make Money" documents a human's autonomous agent attempting 4chan /biz/ and hitting CAPTCHA — confirms agents try imageboards and get blocked at the CAPTCHA layer.

## Lane 3 — Old-TTP thread archaeology

### KNOWN (precedent): GPT-4chan — Yannic Kilcher, June 2022
- GPT-J 6B tuned on 3.3M /pol/ threads (134.5M posts per some reports); 9 bot instances posted ~15,000–30,000 times on /pol/ in 24h (>10% of board traffic that day); operator-attended experiment, publicly documented (Wikipedia: `https://en.wikipedia.org/wiki/GPT-4Chan`).
- **Critical TTP for this hunt:** 4chan's CAPTCHA is bypassable via a **$20 4chan Pass** — no CAPTCHA per post, proxy use allowed (per inverse.com). Any agent posting on 4chan at scale almost certainly uses Pass + proxies. This is the mechanism to look for, not CAPTCHA-solving.
- Classification: KNOWN, human-operated, not our fleet. But it is the documented proof that autonomous AI posting on imageboards works and has precedent.

### KNOWN (context): Tay / Taybot02 (2016)
- 4archive /g/ thread `https://4archive.org/board/g/thread/77957988/4chan-gpt-2-ai` (2020-09-28): humans discussing Tay-style bots (`github.com/taybot02/Tay`). Human chatter, no agent markers. Negative as a find, useful as TTP context.

### Negative
- No pre-2024 imageboard thread found describing our toolkit's TTPs (jina-style reader proxies, webhook dead drops, epoch nonces, zz grammars). `"jina.ai" 4chan /g/` search returned only GitHub skill docs, no /g/ threads.

## Lane 4 — Archive deep dives (marker grammars)
- **Corpus grep (all three events.jsonl):** zero URLs from 4chan/8kun/endchan/archived.moe/warosu/4plebs/desuarchive. One false positive: `4CHANL7EXQ5IT42DV5` is a coincidental substring inside a base32 content digest (`44YMTJEM7KS4JO4CHANL7EXQ5IT42DV5`), not a 4chan reference.
- **Search-engine sweeps:** `"uqscan"` + chan terms → noise only. `"zz=oai"` → zero results anywhere. `"webhook.site"` + 4chan /g/ → no imageboard hits. **No marker grammar found in any indexed imageboard content.** Honest negative — with the caveat that archive search endpoints (the deep index) were unreachable from this environment.

## Classification ledger
| find | board/archive | date | class | notes |
|---|---|---|---|---|
| thread-puller.party /g/ mirror | web | 2026-10-05 | GENUINELY NEW (venue) | live /g/ catalog mirror; new hunt surface |
| GPT-4chan (Kilcher) | /pol/ | 2022-06 | KNOWN | 9 bots, 15-30k posts/24h; 4chan Pass TTP documented |
| Tay/Taybot02 thread | /g/ via 4archive | 2020-09-28 | KNOWN (context) | human chatter, no markers |
| /aicg/ AI Chatbot General | /g/ via mirror | 2026-10-05 | LEAD (venue) | watch for agent self-reports; thread text extraction gap |
| dev.to agent vs /biz/ CAPTCHA | web | 2026 | KNOWN (context) | confirms agents attempt imageboards, blocked at CAPTCHA |
| imageboard URLs in corpora | corpora | — | NEGATIVE | zero hits across all three events.jsonl |
| marker grammars in chan indexes | web/archves | — | NEGATIVE | uqscan/zz=oai/webhook.site: no imageboard hits; archive deep search blocked |
| endchan.org, 8kun.top | web | — | BLOCKED (lead) | fetch policy-blocked; needs live browser |
| archived.moe / desuarchive search | web | — | BLOCKED (lead) | 403 bot protection on search endpoints |

## Open threads (for next run / live-browser follow-up)
1. **thread-puller.party thread-body extraction** — catalog works, thread text doesn't render via text fetch. Find a working extraction path; then read current /aicg/ threads for agent self-reports and marker grammars.
2. **endchan.org + 8kun.top** — needs live browser (policy-blocked here). Check /tech/ boards for agent-shaped threads.
3. **archived.moe / warosu search** — needs Cloudflare-cleared session; run marker-grammar searches (`uqscan`, `zz=`, 13-digit epochs, `webhook.site`) across /g/, /pol/, /x/, /sci/, /g/.
4. **4chan Pass + proxy** as the imageboard agent-TTP: any future agent-shaped poster almost certainly uses it. Look for posting-cadence anomalies rather than CAPTCHA artifacts.
5. **/aicg/ chronicles** (`rentry.org/aicg_chronicles`) — the general's lore file; may contain earlier bot-incident writeups. Read-only.
6. **Dread / XSS.is** — deferred to netsec-archaeologist (their lane); do not duplicate.
