# PROVENANCE — jqp-vercel dataset

Separate dataset for the jqp.vercel.app recon (Lane C), per hunt policy:
keep-all + annotate; nothing here is merged into other datasets without review.

## Sources

| File | Source | Retrieved | Method |
|---|---|---|---|
| `repo_metadata.json` | https://api.github.com/repos/sighrobot/jqp | 2026-09-28 | public GitHub API, single GET |
| `repo_summary.json` | derived from `repo_metadata.json` | 2026-09-28 | local field extraction |
| `endpoint_probe.json` | https://jqp.vercel.app/api/v0?url=https://example.com | 2026-09-28T02:47Z | single passive GET; response headers + body |
| `endpoint_response_body.txt` | same as above | 2026-09-28T02:47Z | raw body (`[]`) |

## What this dataset is

Public-project metadata and one live endpoint probe for `jqp.vercel.app`,
the jq-over-HTTP serverless proxy adopted as an execution vehicle by the
wiki-swarm agents (722 agents, dse+fractal wikis; ~19,255 corpus occurrences
per third-party analysis).

## Key correction vs. the lane brief

The brief hypothesized custom-deployed agent infrastructure. The evidence
shows the opposite: `jqp.vercel.app` is the deployment of the pre-existing
public open-source project **sighrobot/jqp** (MIT, created 2022-05-14, listed
in fiatjaf/awesome-jq). The swarm *adopted* a public utility; it did not
build it. The Vercel team slug in the branch-deployment URL
(`jqp-git-main-sighrobot.vercel.app`, seen once in the corpus) matches the
GitHub account — consistent provenance, no further attribution pursued.

## Scope notes

- Passive recon only: no brute-forcing, no logins, no POST abuse.
- DNS for jqp.vercel.app was not independently resolvable from this
  environment (egress-proxied); not recorded as a finding.
- crt.sh returns no individual certificate for `jqp.vercel.app`
  (Vercel wildcard coverage); the `%jqp%` wildcard search returned only
  unrelated noise (phishing-style lookalike domains, not recorded here).
- No operator identity investigated beyond the public project page.

## Index decision 2026-09-28 (workstream D)

Deliberately unindexed as a standalone ES index. This dataset holds
public-project recon artifacts (GitHub repo metadata + one endpoint probe)
for a finding that is fundamentally a correction: jqp.vercel.app is the
pre-existing open-source project sighrobot/jqp, *adopted* by the swarm, not
agent-built infrastructure. The agent-trace evidence (722 agents,
~19k corpus occurrences) already lives in the `proxy-primitives` ES index
(311 hits). Nothing agent-specific exists in these 4 artifact files that
merits its own index; they stay on disk as reference per keep-all policy.

## Schema normalization 2026-09-29 (W2)

Built `events.jsonl` (2 rows) from the 4 raw artifact files on the canonical
record schema (`scripts/validate_schema.py`: 2/2 clean).
- 1 × `venue_probe` — sighrobot/jqp repo metadata (folding in
  repo_summary.json: topics, watchers, open issues); `@timestamp` =
  repo.created_at 2022-05-14T21:51:48Z; identity `jqp-vercel|repo|sighrobot/jqp`.
- 1 × `venue_probe` — live endpoint probe of
  jqp.vercel.app/api/v0?url=... (body `[]`, CORS `Access-Control-Allow-Origin:
  *`); `@timestamp` = probe.probed_at 2026-09-28T02:46:27Z;
  identity `jqp-vercel|endpoint-probe|<request line>`.
Fingerprint = sha256 hex of the documented identity string (verified against
the 2023-11-14-hfspace-proxies reference implementation before writing).
SHA256SUMS regenerated (events.jsonl + all raw contents); `sha256sum -c` OK.
