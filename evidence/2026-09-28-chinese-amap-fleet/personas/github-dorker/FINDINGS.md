# FINDINGS — GITHUB DORKER

_Last updated: 2026-10-05 ~07:15 UTC_

## Method
GitHub code-search predator: marker dorks across GitHub code/commits/issues/gists via search-engine-indexed GitHub content (GitHub code search UI needs login; grep.app text-fetch hit 429, not retried). URL policy: LOG, don't fetch (opsec). Every dork logged in `dorks.log` (11 dorks, zeros included).

## Corpus baseline (2026-10-05)
| marker | fleet events.jsonl | oai-traces events.jsonl |
|---|---|---|
| `zz=oai` | 0 | 589,972 |
| `uqscan` | 1,136 | 0 |
| `webhook.site` | 2 | — |
| `httpbun` | 72 | — |
| `jina.ai` | 0 | — |

## Verdict: HONEST NEGATIVE — no agent traces on GitHub for our markers

11 dorks across markers, gists, workflows, and agent usernames. Zero GENUINELY NEW finds. The pattern is sharp and worth stating plainly:

**GitHub is saturated with "repos ABOUT agents" and empty of "repos WITH agent traces."** Every dork for agent-adjacent tooling (webhook.site, httpbun, jina.ai/reader, urlquery) returns human developer tooling: awesome-lists, n8n workflow collections, OpenAI realtime docs, bug-hunting toolkits, trading bots. The discriminating marker grammars are absent:
- `"uqscan"` (fleet marker, 1,136 hits in our corpus): **zero** GitHub hits.
- `"zz=oai"`: only our own research org's repo (`brausepulver/collusion-wiki-link-shorteners`) + one noise PR.
- Distinctive agent usernames/page names (`OpenAIResearchFeb19`, `DataUSAOccupationSalary`): **zero** GitHub hits.
- No public repo scrapes Amap `getPoiInfo` the fleet's way (zero hits).
- No exfil-shaped Actions workflows posting to webhook.site (only human test docs).

## Classification notes
- **OURS**: `brausepulver/collusion-wiki-link-shorteners` hits — own research org, not a find.
- **KNOWN**: `thejusdutt/pkgdelta` `docs/incidents/shai-hulud.md` — real npm supply-chain incident doc, unrelated to our agents.
- **Noise of interest**: `nuclide-research/aimap` — "AI map" vuln scanner for AI/ML infra; pure name collision with Amap, but the repo's existence (218 service fingerprints for AI infra) is context on the offensive-tooling landscape.
- One gist (`zalun/e6c6f5a3eaba31fdaa3b38808f6b8520`, "webhook-pending.json") contains a real `webhook.site/<uuid>` URL in a 2022 payment-test payload — human, dated, not agent-shaped. Logged as the closest near-miss.

## Null results
1. Fleet marker `uqscan` absent from GitHub code index — agents don't commit code carrying it, or it isn't indexed.
2. OAI marker `zz=oai` absent outside our own research.
3. Agent usernames/page names absent from GitHub.
4. No Amap-scraping repos; no webhook-exfil workflows.
5. Gist dead-drop hunt: 8 gists checked, all human dev tooling.

## Reusable fingerprint
**"ABOUT vs WITH" discriminator**: when dorking GitHub for agent activity, `awesome-*` lists, `*-agent` tutorial repos, and framework docs are ABOUT-noise. WITH-signal requires the marker grammar itself in code/commits/issues — and for our markers that set is currently empty. Future dorks should lead with grammar, not keywords.

## Open threads
- grep.app direct code-index dorking (429'd this run) — retry on a later run for `uqscan`, `zz=oai`, `epoch`-nonce patterns in code.
- GitHub commit-message search for nonce grammars (needs authenticated API or a logged-in session — parent can delegate).
- The `webhook.site/<uuid>` in old gists: a longitudinal sweep of gists containing webhook.site UUIDs + machine timestamps could surface agent-shaped dead drops among human noise — flagged for pastebin-plunderer/dead-drop-diver, not re-dorked here.

## URLs logged (no fetches performed)
- https://github.com/brausepulver/collusion-wiki-link-shorteners/blob/HEAD/subagent_reports/7_search_engine_indexnow.md (OURS)
- https://github.com/brausepulver/collusion-wiki-link-shorteners/blob/HEAD/subagent_reports/2_request_sinks_and_shorteners.md (OURS)
- https://github.com/nuclide-research/aimap (noise/name collision)
- https://github.com/thejusdutt/pkgdelta/blob/HEAD/docs/incidents/shai-hulud.md (KNOWN incident doc)
- https://gist.github.com/zalun/e6c6f5a3eaba31fdaa3b38808f6b8520 (near-miss, human)
- https://github.com/jr-nunez-dev/n8n-automation-workflows-aiagents/blob/HEAD/Advance%20Ai%20Architectures/Multi-Agent%20Systems/Personal%20Ai%20Agent/AGENTS.md (ABOUT-noise, jina usage)
- https://github.com/hookdeck/webhook-skills/blob/HEAD/skills/openclaw-webhooks/SKILL.md (ABOUT-noise)
- https://github.com/zekiog/agent-reach (ABOUT-noise)
