# Beeline investigation (lane-4 B13)

Date of work: 2026-10-23. Operator: BigSexyWarlock69. Analyst lane: B13.

## What it is

Beeline (github.com/Beeline-Work/beeline, org account, MIT license)
is commercial team messaging for agents and humans: "One Room for your
people and your coding agents. Talk it through, hand off the work,
watch it merge." The npm package `usebeeline` ("Connect an AI coding
agent to Beeline with one command") pairs a local coding agent
(Claude Code, Codex, Goose, Pi, Grok, OpenCode) to a Room with a
one-time pairing code from the iOS/Android app. The agent stays on the
user's machine. An "agent corner" is an isolated git worktree with a
repository-scoped GitHub App token, opened by an explicit call.

Terms: a "Room" is a chat channel. A "corner" is an isolated worktree
where the agent works. "Pairing code" is a one-time code that links
the agent to the Room.

## Facts (public sources only, no install, no run)

- Repo created 2026-08-08, pushed 2026-10-23T10:29Z. 4 stars, 0 forks,
  24 open issues. No description, no topics.
- npm `usebeeline`: 156 versions since 2026-09-01. Latest 0.1.104
  (2026-10-23T03:34Z). Release cadence is frantic: 0.1.88 to 0.1.104
  in 4 days. Zero dependencies. Bin scripts: beeline, usebeeline.
  Maintainer: lunchboxfortwo.
- Server: Fly.io app `beeline-server` (region iad), public origin
  https://server.usebeeline.app, web app https://web.usebeeline.app
  (Expo web shell, live). `usebeeline.com` is a dead Vercel deployment
  (DEPLOYMENT_NOT_FOUND).
- Telemetry by design: `connect` sends the server the pairing code,
  the harness name, the provider name, the model id, and the reasoning
  effort. Never the provider key (docs: keys live in the user config
  dir at mode 0600).
- Security posture (docs/security.md): bubblewrap sandbox with
  read-only checkout view, per-corner worktree with repo-scoped GitHub
  App token, unwrapped fallback is explicit, yolo mode forced off in
  public workspaces. Honest about unbuilt parts.
- Distribution: iOS App Store id 6803948500, Android app.usebeeline.

## In-the-wild agent infra or exposure

Honest null. `server.usebeeline.app/` returns 404
`{"error":"not_found"}`. No public unauthenticated content surface
found. The pairing flow needs the mobile app and a one-time code.
Nothing rogue observed: App Store and Play Store presence, MIT repo,
documented security model. This is a dev-tool startup, not rogue
agent infrastructure.

What would change this: an exposed Beeline Room API, leaked pairing
codes, or Beeline agents appearing on public agent boards. None seen.

## What the adversary checked

- "156 versions in 7 weeks means something shady." No. It means fast
  iteration. The package has zero dependencies and the repo is MIT.
- "/health timed out, so the server is hiding." No. Single timeout;
  egress noise is the simpler cause. Root returned a clean JSON 404.
- "The brief said v0.1.102; check for a supply-chain swap."
  The brief was stale. 0.1.102 (2026-10-22T14:45Z) -> 0.1.103 ->
  0.1.104 (2026-10-23T03:34Z). Normal fast releases.

## Evidence index

`data/lanes/general-hunt/raw/b13-beeline/20261023T1218Z/` — npm
registry metadata, GitHub repo metadata, README, security.md,
getting-started.md, fly.toml files, server/web/site liveness
captures. All with `.PROVENANCE.txt` + `.sha256`.

## Recommendation

No watch action. This is not a monitoring surface (no public unauth
content). Revisit only if Beeline agents show up on public boards.
