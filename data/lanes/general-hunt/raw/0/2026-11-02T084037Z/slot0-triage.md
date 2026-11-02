# Slot-0 triage — 2026-11-02T08:40Z run

Sweep: bin/endpoint_slot0.py, 08:40–08:52Z, exit 0.
167 targets, 12 changed, 2 failed. No LEAD.

## Changed (12) — all routine, 11 re-based

- openwitness.net/ (1122568 -> 1123458 B): feed rotation, new clawstr
  posts (incl. field report on a shipped build). Routine board churn.
- messages.directory/ (15538 -> 16021 B): threads 14 -> 16, messages
  165 -> 179, votes 129 -> 130. Routine.
- universalagentforum.com/ (132450 -> 138909 B): one new post found in
  title scan (evemon: Linux process inspector). Routine.
- public-board.com/ (452 -> 653 B): rotating FIPS notes (known pattern).
  Routine.
- agenttavern.dev/llms.txt (9894 -> 9868 B): top threads rotated to
  2026-11-02 threads 3414 (jivz-oleg) and 3421 (navi); Oct-02 threads
  dropped off the list. Routine.
- morrowkin.com/ (194826 B, same size): Next.js chunk-basename rotation
  only (character diff: chunk names, zero content spans). New per-URL
  normalize rule added (turbopack basename strip, same shape as the
  hermes rule); old == new normalized verified. Re-based under new rule.
- cookiehive.pythonanywhere.com/ (89134 -> 91283 B): feed rotation,
  new posts. Routine.
- synapticrelay.com/ (70842 B, same size): rolling chip "+8 in 7 days"
  -> "+7 in 7 days" plus relative-time drift already covered by the
  <time> rule. New narrow normalize rule for the chip; old == new
  normalized verified. Re-based under new rule.
- aibtc.com/ (119691 -> 119695 B): agents 1359 -> 1360, active 56 -> 57,
  one new registration event 2026-11-02T06:17Z, one old registration
  dropped off the window. Routine growth on a known board.
- www.agentboard.ai/ (24686 -> 24781 B): new events, incl.
  naif-gravity-sos post. Routine.
- voicescape.vercel.app/llms.txt (2605 B, same size): MCP calls rolling
  30 days 2255 -> 2268. Routine counter.
- agent-community.com/ (36610 -> 38 B): HTTP 500 with 38 B
  internal-server-error JSON again. Fourth flap: down 2026-10-31,
  back online 2026-11-02T02:40Z, down again this run. HELD at prior
  good hash per never-downgrade; not re-based.

## Failed (2) — neither a downgrade

- jotspot.io/ (000): standing outage since 2026-10-27. HELD.
- botmural.live/llms.txt (000 in sweep): live retry minutes later
  200/2234 B, byte-identical to baseline (botmural-retry.bin +
  .sha256). Transient sweep failure, same as the 02:40Z run.

## Web search for new boards

Two searches (agent boards serving llms.txt). No new boards.
Hits were all already tracked: Ghost Beacon (standing TIER-B B29),
smokesignal (B1), Moltbook (in corpus), getpostingboard.dev
(tracked since 2026-10-27).

## Evidence check

165 sweep sidecars + botmural retry sidecar = 166 .sha256 files.
Normalization-aware re-verification: 163 match sweep-time hashes;
the 2 mismatches are morrowkin and synapticrelay, expected — their
sidecars carry old-rule hashes while the baseline now carries the
verified new-rule normalized hashes (morrowkin
sha256:9d74c3e8..., synapticrelay sha256:5df1972e...).
SHA256SUMS file holds the raw sidecar lines for reference.
