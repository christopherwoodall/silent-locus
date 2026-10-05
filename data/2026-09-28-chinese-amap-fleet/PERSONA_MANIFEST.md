
## Wave 3 — foreign-language hunters (2026-10-05 00:50 CDT)
| persona | dir | status |
|---|---|---|
| french-agent-hunter | personas/french-agent-hunter/ | COMPLETE 2026-10-05 05:53 UTC — honest negative, urlscan cross-check |
| german-agent-hunter | personas/german-agent-hunter/ | RUNNING |
| russian-agent-hunter | personas/russian-agent-hunter/ | RUNNING |
| arabic-agent-hunter | personas/arabic-agent-hunter/ | RUNNING |
| italian-agent-hunter | personas/italian-agent-hunter/ | RUNNING |
| hebrew-agent-hunter | personas/hebrew-agent-hunter/ | RUNNING |
| iranian-agent-hunter | personas/iranian-agent-hunter/ | RUNNING |

## Wave 3b — infrastructure/behavior hunters (2026-10-05 00:50 CDT)
| persona | dir | status |
|---|---|---|
| evaluator | personas/evaluator/ | RUNNING |
| registrar | personas/registrar/ | RUNNING |
| phisher-hunter | personas/phisher-hunter/ | RUNNING |

## Wave 4 — whacky cross-domain hunters (2026-10-05 00:56 CDT)
| persona | dir | status |
|---|---|---|
| speedrunner | personas/speedrunner/ | RUNNING |
| birdwatcher | personas/birdwatcher/ | RUNNING |
| ham-radio | personas/ham-radio/ | RUNNING |
| watchmaker | personas/watchmaker/ | RUNNING |
| chef | personas/chef/ | RUNNING |
| transit-nerd | personas/transit-nerd/ | RUNNING |
| lighthouse-keeper | personas/lighthouse-keeper/ | RUNNING |
| meteorologist | personas/meteorologist/ | RUNNING |
| antiquarian | personas/antiquarian/ | RUNNING |
| sports-statistician | personas/sports-statistician/ | RUNNING |

All wave 3/3b/4 personas carry a durable BRIEF.md in their dir. To respawn any dead one: spawn a subagent with "Read <dir>/BRIEF.md and resume from existing files."

## Wave 5 — gray hats, randos & wildcards (2026-10-05 02:05 CDT)
OPSEC: log URLs, NEVER live-fetch candidates (a fetch tips the operator + vendors publish first).
| persona | dir | status |
|---|---|---|
| dead-drop-diver | personas/dead-drop-diver/ | RUN 1 COMPLETE 2026-10-05 07:27 UTC — 6 NEW shapes, fresh inbox today, beeceptor surface |
| netsec-archaeologist | personas/netsec-archaeologist/ | RUN 1 COMPLETE 2026-10-05 07:20 UTC — msgboard.dev agent board, board-as-coordination synthesis |
| pastebin-plunderer | personas/pastebin-plunderer/ | RUN 1 COMPLETE 2026-10-05 07:18 UTC — K4be/linuxiarz swarm corpus, new markers |
| numbers-station | personas/numbers-station/ | RUN 1 COMPLETE 2026-10-05 07:25 UTC — zz=oai nonce decoded (epoch+7), disjoint grammars |
| c2-pattern-analyst | personas/c2-pattern-analyst/ | RUN 1 COMPLETE 2026-10-05 07:29 UTC — 3 NEW Shodan infra finds, no cron-beacon cadence |
| fediverse-diver | personas/fediverse-diver/ | COMPLETE 2026-10-05 07:19 UTC — honest zero, read-open-write-gated structural explanation |
| imageboard-scout | personas/imageboard-scout/ | RUN 1 COMPLETE 2026-10-05 07:23 UTC — honest zero, thread-puller.party venue, 4chan-Pass TTP |
| telegram-scout | personas/telegram-scout/ | COMPLETE 2026-10-05 07:18 UTC — honest zero, t.me/s method banked |
| fileshare-farmer | personas/fileshare-farmer/ | RUN 1 COMPLETE 2026-10-05 07:20 UTC — pixeldrain re-scan LEAD, catbox OURS validation |
| paper-trail | personas/paper-trail/ | COMPLETE 2026-10-05 07:15 UTC — Kang-lab provenance, uqscan/zz zero in papers |
| cert-sleuth | personas/cert-sleuth/ | RUN 1 COMPLETE 2026-10-05 07:32 UTC — crt.sh outage, 2 lead clusters, letss.win corroborated |
| github-dorker | personas/github-dorker/ | COMPLETE 2026-10-05 07:12 UTC — honest zero, ABOUT-vs-WITH discriminator |
| kwai-scout | personas/kwai-scout/ | COMPLETE 2026-10-05 07:10 UTC — honest zero, 5 KNOWN context items |
| arg-hunter | personas/arg-hunter/ | COMPLETE 2026-10-05 07:12 UTC — 8 collisions, 10 hypotheses tested, weird catalog |
| librarian | personas/librarian/ | COMPLETE 2026-10-05 07:12 UTC — 10 collisions, 60+ marker index, null catalog |

All wave 5 personas carry a durable BRIEF.md in their dir. To respawn any dead one: spawn a subagent with "Read <dir>/BRIEF.md and resume from existing files."

## Wave 5b — registry & supply-chain hunters (2026-10-05 02:12 CDT)
| persona | dir | status |
|---|---|---|
| dockerhub-diver | personas/dockerhub-diver/ | RUN 1 COMPLETE 2026-10-05 07:28 UTC — honest zero, lane 4 blocked on egress, ODIN Fleet lead |
| package-sleuth | personas/package-sleuth/ | RUN 1 COMPLETE 2026-10-05 07:35 UTC — AUR lax confirmed, bashdev AI-attributed lead, npm/PyPI clean |
