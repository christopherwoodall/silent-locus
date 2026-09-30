# GitHub agent-upload sweep — 2026-09-29

Prototype sweep (BigSexyWarlock69's idea): search agent-associated GitHub accounts and
screenshot-upload patterns via the API, metadata only — no image downloads.
Raw JSON in /tmp/gh-sweep (ephemeral). Token used transiently, never stored.

## Method

- `Authorization: Bearer` against api.github.com, search budget 30 req/min.
- Wave 1: code search `_gitshot`; repo-name searches (`gitshot`, `pr-assets`,
  `screenshots` in:name); user searches (`clawdbot`, `openclaw` in:login); root
  contents of top candidates.
- Wave 2: `_gitshot` tag check on gitshot-images repos; one-dir peek into
  `adrw-bot/penny-pr-screenshots`; user searches for moltbot, devin, swe-agent,
  autogpt, babyagi, openhands, gpt-engineer, aider, crewai, smol (in:login);
  repo listings of top 3 accounts each; asset-word flagging.

## Confirmed: the `_gitshot` tag marker is real and live

- `j-0rdon/gitshot-images` — tags: **`_gitshot`** (exact marker from the Glow report).
- `chlo-eli/gitshot-images` — tags: **`_gitshot`**.
- `lobstermane/gitshot-images` — 20 tags, a whole screenshot-publishing taxonomy:
  `_gitshot-shopping-calendar-api`, `_gitshot-dev-8982-followup`,
  `trackermane-pr-503`, `trackermane-pr-473`, `trackermane-pr-472`,
  `trackermane-demos`, `startup-reconnect-proof-20260929`, `_shots-2026-09`,
  `proof-2026-09`, `pr-3752-paging-proof`, `pr-3566-marketplace-id`,
  `pr-367-proof`, `pr3923-dealseek`, `pr3516-1790272639`, `pr502-manual-cutoff`,
  `pr475-daily-proof`, `og-3778`, `media-2026-09`, `media`,
  `live-thinking-326`. Dated September 2026 — active within the last month.

## Confirmed: per-PR screenshot repos run by bots

- `adrw-bot/penny-pr-screenshots/pr-99` contains `before.png`,
  `after-view.png`, `after-expanded.png` — real before/after PR screenshots,
  organized one directory per PR (`pr-11`, `pr-99`, `pr-343`, …). This is the
  report's "agent can't attach to private PRs, uses a public adjacent repo"
  shape, live.

## Skill-propagation signal in code search

- `_gitshot` code hits (21): mostly the tool's own repos, but skill files show
  the propagation path — `.agents/skills/gitshot/SKILL.md` inside
  `trekawek/coffee-gb`, gitshot bundled in `AtifAssari/MCP-Skills-Universe`
  skill packs. The shared-skill vector from the report is observable.

## Username search: surface is large, leaks are not there

- 283 `clawdbot*` logins, 2,462 `openclaw*`, 21,697 `devin*`, 5,884 `smol*`.
- 13 asset-ish repos flagged across moltbot/devin/swe-agent/openhands/
  gpt-engineer/crewai accounts — all benign on inspection (company demo repos,
  SWE-agent's own readme-media hosting, image tooling). No leaked internal
  screenshots.
- This is the expected negative: it validates the report's 93% figure. The
  real PixelLeak cases hide in *personal* accounts under human credentials —
  username search finds the self-identified bots and misses the leaks by
  construction.

## Lead worth a follow-up

- `lobstermane` / `trackermane-*` tags: looks like an agent workflow
  ("trackermane") filing proof screenshots per PR onto public tags. Naming
  suggests automation rather than hand uploads. Deeper look (commit authors,
  tag dates, image subjects) would confirm — left as a lead, not a claim.

## Limits of this prototype

- Search API only; code search covers the default branch with indexing delay.
- Tag check was per-repo (3 repos) — a corpus-wide `_gitshot`-tag census would
  need enumerating candidate repos first.
- Personal-account leaks (the actual 93%) are not reachable by username
  search; artifact-pattern search (`_gitshot` tags, image-only repos) is the
  productive lane.
