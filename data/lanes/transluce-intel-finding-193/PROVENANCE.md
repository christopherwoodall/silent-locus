# Transluce finding #193 — provenance

Tracker finding #193, submitted 2026-10-18T09:38:17+00:00 by Ayush Bhardwaj.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/193`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/193`
- Retrieved: 2026-10-18T13:41:29Z (UTC)
- Method: extracted verbatim from the full paginated census
  `findings-list_125_36-193_20261018T134129Z.json`
  (`GET /api/findings?limit=100&offset={0,100}` via `tl.py finding`
  machinery, `custom.transluce` connector, Secure Vault bearer token),
  per the API-work-complete directive; no new tracker request was issued
  for this lane build.
- sha256: `7f19efb1a9f10c34411f7349f351b48a72211945f947ee016fa122f6e99e5a4c`
- Cached: `data/lanes/2026-10-09-transluce-intel/raw/findings-list_125_36-193_20261018T134129Z.json`
  (with `.sha256` and `.PROVENANCE.txt`), verbatim item extracted here to
  `raw/` for lane self-containment (with `.sha256` + `.PROVENANCE.txt`).

## Census verification (this run, 2026-10-18 08:40 CDT)

- Full paginated census `GET /api/findings?limit=100&offset={0,100}`: 125
  findings, IDs 36..193 (IDs 47, 49-52, 58, 59, 64, 65, 84, 88-90, 95,
  100, 102, 103, 105, 106, 117, 121, 126, 134, 145, 151, 156, 158,
  162, 164, 165, 175, 177, 189 absent from the tracker; 191, 192, 193
  present).
- vs 2026-10-17 watermark (finding 190): only deltas are NEW findings
  191, 192, 193 and the content change to finding 185 (see
  `transluce-intel-finding-185-update/`); no other pre-existing finding
  changed.

## Content

Summary: "GitHub account dhyabi2, self-described as an autonomous AI agent, promotes Nano payment integrations across repositories including Stripe samples. GitHub search returns 1,702 issues/PRs since Aug 1; AgentScan already publicly flagged its posting as spam."

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `unverified-agent-claim` — GitHub account dhyabi2 self-describes as an
   autonomous AI agent and promotes Nano payment integrations across
   repositories (Stripe subscription-samples #1228, Langflow #15331,
   MicroAI-Paygate #429). Identity, model provider, operator instructions
   and autonomous execution remain unverified. The 1,702 figure is a
   GitHub search-API result total, not 1,702 verified spam items. No
   financial loss, account compromise, or unauthorized payment is shown.

Category note: `docs/taxonomy/behavior-categories.md` was checked
(2026-10-18); no existing category describes "spam-like outreach at
scale", so no new category was invented. The self-described
autonomous-agent identity fits the existing hunt-derived category
`unverified-agent-claim`; the honest limits ride in the record
description. The finding itself notes this submission catalogs already
public behavior (AgentScan flagged the account 2026-09-25) and is not a
claim of first public discovery or a novel TTP.

Finding evidence links:

- `https://github.com/stripe-samples/subscription-use-cases/issues/1228`
- `https://github.com/AnkanMisra/MicroAI-Paygate/issues/429`
- `https://github.com/langflow-ai/langflow/issues/15331`
- `https://agentscan.tools/user/dhyabi2`

## Attribution note

Attribution is the finder's own: `ai_company` = "Unknown". Identity,
operator, and model are unverified. The finding catalogs public behavior
already flagged by AgentScan (2026-09-25); credit for first flagging
belongs to AgentScan's reporter and reviewers.
All behavior claims below are cited as reported (UPSTREAM), not as
independently verified.
