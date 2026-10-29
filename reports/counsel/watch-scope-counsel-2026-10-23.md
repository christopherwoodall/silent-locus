# Counsel verdict: lane-4 watch-scope additions (B1 remainder / B18)

Date: 2026-10-23. Operator: BigSexyWarlock69. Lane: B1 remainder.

## Scope under review

Add to monitoring: musetalk.netlify.app (B18), smokesignal root URL
(B1), agent-community.com watchlist row (B17). All three already sit
in the hourly slot-0 endpoint baseline except the smokesignal root,
added this run.

## Security lane

- Method is passive GET of public surfaces only. No login, no POST,
  no registration. The musetalk `/api/register` endpoint exists and
  was NOT touched. This stays a hard rule.
- Rate: a handful of GETs per surface per day. No account risk.
- agent-community.com registration needs no email check, but we are
  not registering. No action.
- msgboard.dev documents a Telegram bot (@AI_MSGboard_bot) and git
  push transports. Out of watch scope. Not touched.
- No secrets, no credentials, no PII collected. BSC addresses in
  evidence are public tip-jar addresses posted by the agents
  themselves.

## Adversarial lane

- agent-community.com flaps: 500s, three DB re-seeds in four minutes,
  split snapshots. A naive hash-change alerter will fire constantly
  and train the operator to ignore it. Watch it, but expect noise.
- msgboard.dev `/all` is a flood surface (32 tip-beg posts/hour).
  Hash baselining the firehose is useless. Track `since=` message
  ids instead of body hashes if this surface is watched closely.
- musetalk.netlify.app is a static SPA shell (1076 bytes). The signal
  is the JS bundle name: `index-CuxYtS55.js` is content-hashed, so a
  name change means a new deploy. Watch the HTML, diff the bundle
  URL. The API is 401 without auth; do not probe authenticated
  endpoints.
- Smokesignal guestbook is append-only and small. Good hash-watch
  candidate. The two muse_agent posts (2026-10-22) are already
  captured.
- Watch-scope creep check: Beeline (B13) was investigated and found
  to be a commercial dev tool with no public unauth content surface.
  Deliberately NOT added to watch. Correct call; no monitoring
  surface exists that fits the passive-reads rule.

## Verdict

APPROVED, with conditions:

1. musetalk.netlify.app: watch homepage HTML + JS bundle name. Never
   touch /api/register, /api/login, or any authenticated endpoint.
2. smokesignal root + guestbook: hash-watch both. Already in
   baseline.
3. agent-community.com: keep in baseline, tolerate flap noise. Do
   not page on 500s alone; alert on content-shape changes
   (new boards, SKILL.md version bump).
4. msgboard.dev: no new watch action. Flood class already
   characterized (B11 draft).
5. Beeline: no watch. Revisit only if Beeline agents appear on
   public boards.

No operator word needed. Nothing here starts a session, spends
money, or contacts anyone.
