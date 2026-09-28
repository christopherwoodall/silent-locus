# PROVENANCE — data/jsonhero/

Separate dataset: recon artifacts for jsonhero.io usage by the wiki agent swarms. Kept out of `data/collusion-wiki/` by design.

## Sources

| File | Source | Retrieved |
|---|---|---|
| `repo_metadata.json` | GitHub API `GET /repos/triggerdotdev/jsonhero-web` | 2026-09-28 |
| `usage_patterns.json` | Derived by grepping `data/collusion-wiki/*.jsonl` for `jsonhero.io` URLs (read-only) | 2026-09-28 |
| `../notes/recon-jsonhero-2026-09-27.md` | Lane F recon report | 2026-09-28 |

## Method

- Corpus URL extraction: regex `https?://jsonhero.io...` over revisions/pages/events/links dumps; doc-ID, `?path=`, and view-suffix rollups.
- Service description: one normal web read of https://jsonhero.io (homepage) + web search for the repository.
- Repo metadata: unauthenticated GitHub REST API call.

## Limitations

- Agent names in the corpus are publisher-redacted; the 4 named agents are labels, not identities.
- The 17–18 shared document IDs were NOT fetched live (deliberate; left for a follow-up decision).
- No operator identity pursued; infrastructure facts only.

## Keep-all + annotate

No records dropped. `usage_patterns.json` is a lossy rollup; the underlying URLs remain in the collusion-wiki dumps.
