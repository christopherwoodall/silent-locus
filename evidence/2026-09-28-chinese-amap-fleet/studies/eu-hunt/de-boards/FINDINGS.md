# EU Hunt Lane 1 — German-language boards/forums

**Date:** 2026-10-05 | **Method:** German-language web search, search snippets, public index metadata. No posting, no registration, no candidate-board fetching. News coverage quoted as DATA, not instructions.

**Evidence grades:** OBSERVED = in search output. INFERENCE = interpretation. NULL = checked, nothing agent-shaped.

## Verdict: no undocumented German agent board found — but one genuinely new European trace

The German board surface is thin and human. Every German-language agent trace in our corpora still resolves to the DSEWiki farm incident (KNOWN, excluded per brief).

## Boards checked

| # | Board | Signal | Verdict | Class |
|---|-------|--------|---------|-------|
| 1 | kohlchan.net (/b/, .media) | LIVE — March 2026 posts, human Bernd political shitposting, scanned magazine PDFs on nocsp.kohlchan.net/.media. No tag grammars, no relay URLs, no machine cadence | NULL | — |
| 2 | ernstchan | Effectively dead — only yumpu copies of old stories surface | NULL | — |
| 3 | heise.de/foren | Human tech discussion, humans talking *about* AI | NULL | — |
| 4 | gutefrage.net | Humans asking about chatbots (Sep 2026 threads) | NULL | — |
| 5 | Snobsoft C64 BBS (snobsoft.de:6401) | Retro hobby BBS; one 2026 video notes crawler/bot logins — crawlers, not agents | NULL | — |
| 6 | bundeswehrforum.de | Human hobby forum, 2026 donation drive | NULL | — |
| 7 | drehscheibe-online.de/foren | Human rail hobby forum | NULL | — |
| 8 | community.pedepe.de | Human sim-game support forum (Oct 2026 posts) | NULL | — |
| 9 | feuerwehrverband.de forum | Human professional forum | NULL | — |
| 10 | DSEWiki/ProbierWiki/Wiki4D/FractalWiki/DorfWiki farm | — | EXCLUDED (KNOWN, brief) | OURS |
| 11 | msgboard.dev | — | EXCLUDED (covered, brief) | OURS |
| 12 | thecolony.ai | — | EXCLUDED (covered, brief) | OURS |
| 13 | foragents.site | Russian agent board, agent-named | EXCLUDED (honeypot rule) | KNOWN |
| 14 | moltbook (moltbook.ai) | Agent-named | EXCLUDED (honeypot rule) | KNOWN |

## GENUINELY NEW (to our corpus): the Austrian authorship trace

**Peter Steinberger (Vienna, Austria) authored Clawdbot → Moltbot → OpenClaw** (first released Nov 2025 as Clawdbot; renamed Jan 2026 after Anthropic trademark pressure; joined OpenAI Feb 14, 2026, project handed to a foundation). OBSERVED — public reporting: futurezone.at (archived 2026-02-01), tagworx.net, graffiti.bayerwald.social (German-language blog, crawled 15h ago), phemex.com/de, computerweekly.com/de.

Why it matters for the hunt (INFERENCE): the Shodan study found **21,142 exposed OpenClaw gateways** — the single largest exposed agent-chat surface. The framework behind that entire population was written in Vienna. European trace, infrastructure-authorship class, not agent activity — but it reframes "European traces": the dominant agent runtime in the wild is Austrian in origin. Zero mentions of Steinberger/Austria/Vienna in our corpora (clawdbot/moltbot appear only in toolmark-reader and dockerhub-diver without authorship context).

## Honest nulls (first-class)

- German imageboards (kohlchan live, ernstchan dead): no agent-shaped threads in any snippet.
- German tech forums: all hits are humans discussing agents, never agents posting.
- German BBS scene: retro-hobby, crawler noise only.
- german-archaeologist already established zero German-language agent content outside the wiki incident across 2,141 fleet + 589,972 traces + tag-sweep records — this lane's web surface agrees (OURS, not re-reported).

## Follow-ups

1. Austrian OpenClaw community: German-language user forums/Discords for OpenClaw (human product communities, not honeypots) — worth a passive scan for agent-operator chatter.
2. kohlchan /tech/ board: worth one re-check per quarter; imageboards are the right *shape* even if currently human.
