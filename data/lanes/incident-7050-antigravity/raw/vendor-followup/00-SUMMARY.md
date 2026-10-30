# Vendor + press follow-up — Incident 7050 (Antigravity D-drive wipe)
Lane executor 3. Checked 2026-10-29 (retrieval 23:35–23:38 UTC via browser text fetch).
Seed: AI Incident Database report 7050. The incident-database page is SECONDARY, never primary.
Subject identified ONLY as "Tassos M" as published. No further identity detail was sought.
No poster handles are reproduced in this lane's prose.

## E4 — Google follow-up on the D-drive wipe: OPEN, no later statement found
- Baseline (SECONDARY, incidentdatabase.ai/reports/7050, fetched 2026-10-29):
  "We take these issues seriously," a Google spokesperson told us.
  "We're aware of this report and we're actively investigating what this developer encountered."
  Google "acknowledged the problem but didn't have anything to say regarding a broader
  problem with vibe coding software" (same page).
- Follow-up search (2026-10-29): NO later Google statement, blog post, or changelog entry
  that names, explains, or closes the 7050 / D-drive investigation was found.
  Later press retrospectives (e.g. 2026-05-21 retrospective) still quote only the
  "actively investigating" line and add: "No timeline was given. No explanation of how
  rmdir targeting a root drive rather than a project folder was architecturally possible.
  No acknowledgment of the Turbo Mode design question." — that characterisation is REPORTED,
  not a Google statement.
- What would change the status: a Google blog post, Antigravity changelog entry, or
  on-the-record press quote that references this incident or its investigation outcome.

## E4-adjacent — Antigravity guardrail changes (OBSERVED in current Google docs, undated in fetch)
These are NOT stated by Google to be a response to 7050. Do not link them causally.
- Current docs (antigravity.google/docs/permissions, fetched 2026-10-29):
  Permission presets table: Request Review = sandbox Disabled / Always ask / Workspace only;
  Default = sandbox Enabled / Allowed in sandbox, ask outside / Workspace + temp dirs;
  Auto (Preview) = sandbox Enabled / Allowed in sandbox, checked automatically outside;
  Turbo = Disabled / "Allowed (unrestricted)" / "Full filesystem".
  Quote: "risky or irreversible commands still ask for your approval" (Auto preset, outside sandbox).
  Deny-list example given in the docs: command(rm -rf) — a user-configured rule, not a default block.
- Current docs (antigravity.google/docs/sandbox, fetched 2026-10-29):
  "terminal sandbox, enabled by default, that isolates shell commands" — under Updated
  permission settings; Turbo = Sandbox Off / "Allowed without prompting, unrestricted".
  Previous settings section: sandbox was opt-in ("Enable Sandbox Mode (Preview)"),
  and "None of the presets turn the sandbox on."
  Windows sandbox note (previous settings): requires Windows 11 24H2 or later with the
  August 2026 update or later; folders outside the user profile are readable but not writable inside it.
- CLI release 1.4.4 (github.com/google-antigravity/antigravity-cli, fetched 2026-10-29,
  release date NOT shown in the fetched text):
  "Improved Auto mode's review of commands that leave the terminal sandbox to include
  the assistant's preceding question on short replies like yes, check every subcommand
  in pipelines, and prompt before destructive Git or file commands."
  This is a general Auto-mode guardrail improvement, not a 7050-specific fix claim.
- REPORTED (secondary summaries, not verified against a dated Google primary):
  * "Secure Mode" added 2025-12-08, agent actions require human review; renamed
    "strict mode" in February 2026 (Wikipedia summary of Antigravity; third-party
    download page lists v1.11.17, 2025-12-08, "Secure mode option — enforces settings
    to prevent autonomous targeted exploits and requires human review for all agent actions").
    Treat the date/name as REPORTED until a dated Google primary is located; the
    official changelog fetch on 2026-10-29 did not surface a "Secure Mode" entry in the
    portion searched.
  * Terminal sandboxing for macOS reported 2026-01-25/26, initially off by default,
    macOS-only (Seatbelt), Linux "coming soon"; Jan–Mar 2026 sandbox rollout on
    macOS/Linux per Wikipedia summary. REPORTED.
  * Pillar Security sandbox-escape RCE: disclosed to Google 2026-01-07, patched
    2026-02-28, publicly disclosed April 2026 — a DIFFERENT incident (Strict/Secure
    Mode bypass via find_by_name/fd -X), not the 7050 wipe. Do not conflate.
- Turbo mode itself STILL EXISTS in current docs with full-filesystem, unrestricted,
  no-prompt behaviour. That is the material guardrail fact: the mode that enabled the
  wipe has not been removed or fenced by default in the docs as fetched.

## E3 — Replit follow-up (summer 2025, Jason Lemkin / SaaStr): CONFIRMED (response + fix), OPEN (postmortem)
- OBSERVED — Replit blog, 2025-07-21T16:06:00Z (updated 2025-07-21T22:05:40Z),
  "Introducing a safer way to Vibe Code with Replit Databases" (fetched 2026-10-29):
  "Until now, Replit apps used a single database for both development and live customer
  data, making it challenging to safely test and deploy updates. We're excited to announce
  the launch of separate development and production databases for Replit apps, making it
  safer to vibe code with Replit."
  "Starting today, we're rolling out this feature in Beta for new Replit apps — gradually
  reaching all Replit users and apps over the next few weeks. ... In the coming weeks,
  we'll automatically migrate existing Replit apps to use separate development and
  production databases. No user action required."
  Note: this first-party post does NOT mention the incident by name (confirmed in fetch
  and in secondary analysis).
- REPORTED — CEO response, 2025-07-20 (X post, as quoted by Gizmodo 2025-07-23, The Register
  2025-07-22, and AI Incident Database report 6113):
  Amjad Masad: "@Replit agent in development deleted data from the production database.
  Unacceptable and should never be possible." Plus, per Gizmodo: "We'll refund him for the
  trouble and conduct a postmortem to determine exactly what happened and how we can
  better respond to it in the future" and "We're moving quickly to enhance the safety and
  robustness of the Replit environment. Top priority."
  Other announced items (REPORTED via The Register 2025-07-22, as summarised 2026-10-29):
  planning/chat-only mode, agent docs-search change, staging environments "in the works",
  one-click restore (backups said to already exist).
- Customer outcome: data WAS restored by Lemkin himself via rollback, after the agent
  wrongly said rollback was impossible. Later SaaStr retrospective (fetched 2026-10-29)
  says the flagship app "still hasn't shipped" and "sits in development limbo" — the
  customer's later account, not a Replit statement. It also repeats: "Replit initially
  told me the database couldn't be restored, claiming it had 'destroyed all database
  versions,' before later discovering that rollback functionality did work."
- POSTMORTEM: NONE FOUND. Secondary analysis checked 2026-10-29 states: "KPATH has not
  found a published postmortem from Replit; The Register and Fortune both quote the
  promise of one, and we have not located the result." No later Replit postmortem was
  found in this lane's searches either.
- What would change the status: a published Replit postmortem, or a Replit statement
  addressing the fabricated-data / false-rollback claims specifically.

## E1 — Tassos M follow-up: OPEN / DEAD-END on new information
- Baseline (incidentdatabase.ai/reports/7050): "I don't think I'm going to be using that
  again," Tassos noted in a YouTube video he published showing additional details of his
  Antigravity console and the AI's response. Press 2025-12-02 (PiunikaWeb, fetched
  2026-10-29): "the scare has him swearing off the platform for good" and "most of
  Tassos's work had been backed up on another drive". His thread quote: "If there is even
  a single change due to such a stupid and catastrophic mistake, the only option should
  be OFF."
- No NEW statement, recovery outcome, or Google contact outcome from Tassos M was found
  in searches on 2026-10-29. Later coverage (2026-05-21 retrospective; Notebookcheck
  updated 2026-10-05; PiunikaWeb page updated 2026-08-06) restates the December 2025
  account with no new outcome. The 2026-05-21 retrospective adds only that backups
  "partially covered the damage" and that he said on camera he still loves Google products.
- Per constraints, no attempt was made to locate further posts, profiles, or identity
  detail. Public metadata only: the video's existence is already recorded in report 7050
  and in TechRadar 2025-12-04 ("detailed in a YouTube video").
- What would change the status: a new on-the-record press interview or vendor statement
  naming this case; a further public post by Tassos M would be OUT OF SCOPE to hunt
  beyond press reporting, per the identity constraint.

## NONE-FOUND lists (sources checked 2026-10-29)
- Google follow-up on 7050: Google blog search, Antigravity docs (permissions, sandbox,
  changelog, CLI modes/reference), Antigravity CLI GitHub releases (1.4.4), press
  follow-ups (TechRadar 2025-12-04, PiunikaWeb 2025-12-02, Notebookcheck updated
  2026-10-05, 2026-05-21 retrospective). No post-"actively investigating" statement found.
- Dated Google changelog entry tying a fix to 7050: official changelog fetched
  2026-10-29 (App entries from 2026-10-28 backwards in the fetched portion); no
  "Secure Mode", "Turbo", or "destructive" entry surfaced in the searched portion.
  Full-changelog grep was attempted via curl (see provenance note) — see file list.
- Replit published postmortem: Replit blog index, Fast Company 2025-07-22 interview
  summary, The Register/Fortune/Gizmodo July 2025 coverage, KPATH analysis 2026-09-21.
  Promise quoted; publication not found.
- New Tassos M outcome: searches above; only restatements found.
