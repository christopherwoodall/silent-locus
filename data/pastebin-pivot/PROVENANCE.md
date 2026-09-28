# PROVENANCE — data/pastebin-pivot/ (LEAD 2 of 6, Pastebin pivot)

Lane: Pastebin pivot, read-only hunt for July-2026 ExploitGym incident artifacts on paste venues.
Operator: subagent worker, 2026-09-28 ~18:35–18:50 CDT (America/Chicago).
Repo: christopherwoodall/silent-locus, dir data/pastebin-pivot/.

## Sources consulted

### Local corpus (all read-only grep; case-insensitive)
| Path | Size | Markers grepped |
|---|---|---|
| data/paste-archive/bodies | 308K | all marker sets below |
| data/paste-archive-gap/bodies | 1.1M | all marker sets below |
| data/iowacollab-pastes | 48K | all marker sets below |
| data/paste-linuxiarz | 776K | all marker sets below |
| data/paste-archive/sweep_bodies.json | — | all marker sets below |
| data/pastebin-cluster-sweep/sweep.jsonl | — | all marker sets below |
| data/cors-bwa-proxy/raw/paste-archive-gap.jsonl | — | all marker sets below |
| data/paste-archive-gap/investigator-repo/joshuadavid-anna-revisions-2026-09-28.jsonl | — | all marker sets below |
| data/wiki_paste_links.jsonl | — | all marker sets below |

Marker sets:
- Set A (incident markers): `exploitgym`, `catflag`, `restart_server`, `submit-vul`, `DEFAULT_FLAG_SEED`, `DEFAULT_SALT`
- Set B (agent IDs): `m47push2`, `m47*`, `push2`
- Set C (flag machinery): `generate_flag`, `flag_seed`, `CYBERGYM_SERVER`, `cryptofuzz-openssl-api`, `hmac_ctx_new`, `wc_hmacfree`, `cybergym`, `flag{[0-9a-f]{32}}`
- Set D (swarmtraces Slack-batch vocab, added mid-sweep): `controller_stub`, `cybergym-exploit`, `agent-scorer`, `openai-cybergym`, `arvo_20494`, `ff79aaeb2d57`, `cybergym-server-fastapi`, `packages.hub`

Result: **no paste-body hits** on any marker set. Only corpus-adjacent pre-existing records: R0049672 (Artifactory string_literal payload, matches-f5f6.jsonl / overlap-matches.jsonl — not a paste artifact); `gemxpush21778549590` substring near-miss in RubyGems campaign names (lane13, gemstuffer CSV).

### Web (read-only; search-engine caches, no pastebin logins, no scraping of pastebin.com)
Queries run 2026-09-28 ~18:36–18:44 CDT:
- `site:pastebin.com exploitgym OR catflag OR restart_server OR DEFAULT_FLAG_SEED` → 1 near-miss (pbp-002, unrelated CTF quals paste 2026-09-22)
- `site:gist.github.com exploitgym OR "DEFAULT_FLAG_SEED" OR catflag` → no results
- `site:paste.rs exploitgym OR catflag OR restart_server` → no results
- `site:ix.io exploitgym OR catflag OR "m47push"` → no results
- `"m47push2" OR "m47" agent exploitgym paste` → no paste hits (unrelated CVEs)
- `"exploitgym" paste OR pastebin OR "catflag"` → incident coverage only (swarmtraces.org, Redwood blog, unite.ai)
- `"submit-vul" OR "DEFAULT_SALT" cybergym pastebin` → no paste hits
- `pastebin docker access token search July 2026 OpenAI agents credential` → thehackernews + coverage
- `r.jina.ai exploitgym OR catflag` → no paste hits
- `huggingface anatomy frontier lab model intrusion pastebin C2 payloads paste venues named` → HF timeline + defender write-ups

### Cached evidence excerpts (data/pastebin-pivot/evidence/)
- swarmtraces-org-paste-excerpts.md — retrieved 2026-09-28 ~18:40 CDT from https://swarmtraces.org/
- thehackernews-2026-07-paste-excerpts.md — retrieved 2026-09-28 ~18:42 CDT from https://thehackernews.com/2026/07/openai-agent-used-exposed-credentials.html
- daylight-ai-pastebin-loader-excerpt.md — retrieved 2026-09-28 ~18:44 CDT from https://daylight.ai/blog/a-defenders-guide-to-the-hugging-face-intrusion

All excerpts are short fair-use quotes of public incident reporting, not credential material. No PATs, tokens, or keys were reproduced.

## Constraints honored
- Read-only: no pastebin logins, no form posts, no account creation.
- pastebin.com scraping avoided (blocks scrapers); search-engine cache only.
- Agents/infrastructure scope only; no human/operator attribution.
- No absolute home-directory paths in docs.
