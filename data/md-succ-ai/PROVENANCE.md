# PROVENANCE — md.succ.ai separate dataset

Separate dataset staged per hunt directive: artifacts for the md.succ.ai
recon lane, kept OUT of the collusion-wiki corpus.

## Source

- Public Git repository: https://github.com/vinaes/md-succ-ai
- Cloned 2026-09-28 (UTC) via `git clone --depth 1`, then `git fetch --unshallow`
  for full history. Local copy: `repo/`
- Live API spec: https://md.succ.ai/openapi.json (fetched 2026-09-28, saved as
  `openapi.json`)

## Retrieval record

| item | date (UTC) | sha256 |
|---|---|---|
| repo HEAD commit | 2026-09-28 | `ea3ec780741b9f777d1e5575b2dd9d1b2fc80b82` |
| openapi.json | 2026-09-28 | see `openapi.json.sha256` |

## Provenance notes

- Repository first commit: 2026-02-14 ("feat: md.succ.ai — HTML to clean
  Markdown API"). HEAD commit: 2026-02-25 (MCP server, TLS fingerprint
  impersonation, browser resource blocking).
- License in repo: FSL-1.1-Apache-2.0 (Functional Source License,
  source-available; converts to Apache 2.0 over time).
- The repo is presented as part of the "succ" ecosystem (succ.ai), an
  agentic coding framework whose web-fetch backend is md.succ.ai.
- Operator identity is OUT OF SCOPE for this hunt; no person-focused
  attribution was pursued. This dataset covers infrastructure facts only.

## Relation to other datasets

- Referenced by 483 wiki agents in the collusion-wiki corpus
  (see `../wiki_ioc_pivots.jsonl`).
- Referenced in third-party analyses:
  - https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/sub-swarms.md
  - https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/reddit-local-forensics-crosscheck.md
  - https://github.com/hamzah2304/messageboardauditbench (blind_verbatim report
    react_z-ai_glm-5.3_r3_20260907T095543Z.md)
