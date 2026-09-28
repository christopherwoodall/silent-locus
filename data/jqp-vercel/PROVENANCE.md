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
