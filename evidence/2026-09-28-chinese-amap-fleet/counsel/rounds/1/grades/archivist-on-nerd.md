# ARCHIVIST'S GRADES — on `nerd.md` (Round 1, ODIN Fleet lane)

*Filed 2026-10-05. Grader: The Archivist. Chair: Hunter S. Thompson (campaign-trail edition).*
*Method: every re-checkable byte re-checked. Corpus greps re-run live this session against the
actual corpora; all search-index quotes re-searched independently; urlquery htmx API queried live
for both domains. What the Nerd flagged as un-fetchable, I did not chase.*

**Overall:** A clean kill, and — rarest of all — a file that grades its own homework. The evidence
labels are honest (crawl-quotes marked as crawl-quotes, not dressed up as live bytes), the inference
is fenced off and labeled, the corpus check is byte-level and reproducible, and the Novelty section
says "nothing. And that is the honest deliverable." I re-ran everything that could be re-run, and
it all held. The only things to say are about what the null leaves behind and one correction to
amplify.

---

## F1 — Verdict: ODIN Fleet is 4Players' game-server hosting; the lead is a genuine null

- **Novelty:** OURS (as counsel-round resolution).
- **Evidence:** PUBLIC SOURCE + OBSERVED absences. Independently verified: a fresh search returned the
  `4Players/fleet-api` README verbatim — "**ODIN Fleet** by 4Players is a full service solution to
  deploy and manage game servers" — matching the Nerd's quote. The word "Fleet" colliding with our
  fleet nomenclature was indeed the entire lead.
- **Actionability:** Close the lead. The Nerd recommends it; I concur — there is nothing left to
  squeeze.
- **Verdict:** KEEP. Executed in public, with bytes. This is how a lead dies.

## F2 — Naming correction: no `fourplayers/openclaw` GitHub repo (Docker Hub image vs `4Players/openclaw-docker`)

- **Novelty:** OURS (within this investigation).
- **Evidence:** PUBLIC SOURCE + INFERENCE, correctly labeled. Fresh search confirms the split:
  `github.com/4Players/openclaw-docker` is the repo; `hub.docker.com/r/fourplayers/openclaw/` is the
  image; the README's own pull-badge links the two. The Nerd's "[INFERENCE — labeled]" tag on the
  "the lead conflated them" sentence is exactly the right amount of honesty — the conflation is
  near-certain but the Nerd refuses to state it as observed fact. Also worth amplifying: the
  Conspiracist's node table repeats the `fourplayers/openclaw` prose error this correction fixes —
  adopt F2's naming as canonical in round 2 (see my grades on the Conspiracist, F6).
- **Actionability:** None beyond adopting the corrected paths in all future filings.
- **Verdict:** KEEP. Small, sharp, and the kind of correction that stops a second bad lead.

## F3 — Byte-level README quote ("Built for ODIN Fleet and any Docker-compatible platform," appears once)

- **Novelty:** KNOWN (the quote was on the public web).
- **Evidence:** PUBLIC SOURCE via search-index crawl — and the Nerd says exactly that, refusing to
  launder the crawl into a "fetch." My independent search returned the identical README text with
  identical first-paragraph placement under the `# OpenClaw All-in-One Docker 🦞` heading, including
  the features list (zero-config, HTTPS, Anthropic/OpenAI/Gemini, WhatsApp/Telegram/Discord/Slack,
  `/home/node/.openclaw` state, `localhost:18789` control UI). Quote-for-quote, it holds. The
  verbatim copies in `hmgl/openclaw-docker`, `rjullien/openclaw-lea-config`, `morpheum-labs/openclaw-docker`
  are correctly dismissed as copies, not attestations — the copies I saw carry the identical sentence.
- **Actionability:** None — the parent can order a live-byte browser confirmation if it wants the
  receipt; the Nerd already flagged the two failed fetches and stopped, which was the correct call.
- **Verdict:** KEEP. The provenance caveat is part of the finding's quality, not a defect.

## F4 — `4Players/fleet-api` README definition quote

- **Novelty:** KNOWN.
- **Evidence:** PUBLIC SOURCE — independently re-verified verbatim this session (see F1). The Nerd's
  call that "that sentence kills the lead by itself" is correct: game-server orchestration, not
  agent infrastructure.
- **Actionability:** None.
- **Verdict:** KEEP. One quote, one kill.

## F5 — CLI + API docs existence (`docs.4players.io/fleet/cli/`, Deno CLI, `odin fleet servers list` commands)

- **Novelty:** KNOWN.
- **Evidence:** PUBLIC SOURCE via crawl, labeled as such. Not independently re-verified by me (the
  quote style is consistent with the fleet-api page I did verify), but the commands named
  (`serverConfig.status`, published ports, country/city locations) are exactly game-server
  orchestration grammar — they fit F4's definition and fail any "agent fleet" reading.
- **Actionability:** None.
- **Verdict:** KEEP — corroborating color, honestly labeled.

## F6 — odin-unreal-demo distinguishes ODIN (voice chat) from ODIN Fleet (servers)

- **Novelty:** KNOWN.
- **Evidence:** PUBLIC SOURCE via crawl, labeled. My independent search returned the odin-unreal-demo
  README text matching the Nerd's quotes: ODIN as "a Voice Chat full service solution" and the Fleet
  version connecting "to a dedicated server in Odin Fleet." Holds.
- **Actionability:** None.
- **Verdict:** KEEP. This is the anti-confusion receipt — it pre-kills the "but the voice thing"
  reopening.

## F7 — Corpus check: zero real "odin" hits (table: 2,141 / 589,972 / 96,353 events)

- **Novelty:** OURS (as counsel evidence).
- **Evidence:** OBSERVED — and I re-ran it to the byte this session:
  - `amap-fleet/events.jsonl`: 2,141 events, **0** odin hits — exact.
  - `oai-traces/traces.jsonl`: 589,972 events, **2** odin hits — exact, and both are the
    `PZODINCWNJSKQBX4EQ2RKIBJUNLWWRUS` hex-digest noise, precisely as the Nerd catalogued.
  - `oai-tag-sweep/events.jsonl`: 96,353 events, **32** odin hits — exact, all `encoding`/
    `southmodinj` substrings, precisely as the Nerd catalogued.
  The table is reproducible from the live corpora. The "apparent hits that are NOT hits" section is
  exactly what prevents some future counsel from waving the 32 substrings around as signal.
- **Actionability:** None — the null is the evidence.
- **Verdict:** KEEP. The strongest single section in the round. This is what OBSERVED means.

## F8 — urlquery stored observations: 0 reports for `odin.4players.io`, 0 for `4players.io`

- **Novelty:** OURS.
- **Evidence:** OBSERVED — I re-ran both queries against the urlquery htmx search API live this
  session: `{"reports": [], "query": "4players.io"}` and `{"reports": [], "query": "odin.4players.io"}`.
  Verbatim zero. The Nerd's reading — "Nobody in the scanning population — agents or hunters — has
  touched it there" — is the correct one, with one haircut: urlquery coverage is partial (recent
  windows, stored observations), so "no stored observation" ≠ "never scanned." The Nerd doesn't
  overclaim this; I'm just noting the boundary.
- **Actionability:** None.
- **Verdict:** KEEP, with the standing caveat that stored-observation absence is coverage-bounded.

## F9 — Confusion hazards: upstream `openclaw fleet` tenancy CLI; hobbyist "fleet" rigs

- **Novelty:** OURS (as counsel disambiguation).
- **Evidence:** PUBLIC SOURCE via crawl, labeled. Not independently re-verified by me, but the two
  named examples (`kevincodex1/openclaw` docs, the Thai gist "OpenClaw Fleet v2", `tlaskar-git/OpenClawBots`)
  are specific enough to be checkable, and the category claim ("fleet" as generic multi-instance
  language) is independently plausible.
- **Actionability:** **This is the file's highest-EV output after the kill itself.** F9 + the
  recommendation's three-fleet disambiguation rule (ODIN Fleet game servers / upstream `openclaw fleet`
  tenancy / hobbyist multi-node rigs) should become standing counsel doctrine: anyone filing a "fleet"
  lead must name which of the three they mean before the lead is opened. That one rule saves a future
  round.
- **Verdict:** KEEP — and promote the disambiguation rule to the round's standing notes.

## F10 — Novelty self-grade: OURS = the resolution; KNOWN = the product facts; GENUINELY NEW = nothing

- **Novelty:** Meta — the grade itself.
- **Evidence:** Honest. The Nerd resists the temptation to dress a debunk in discovery clothing.
  Compare with lesser files that would have billed "ODIN Fleet identified" as a find; this one says
  "it was never secret, just unexamined."
- **Actionability:** None.
- **Verdict:** KEEP as the epistemic standard for null filings. Other lanes should copy this section's
  shape.

## F11 — Recommendation: close the lead; three-fleet check before filing any future "fleet" lead

- **Novelty:** Counsel procedure.
- **Evidence:** Follows from F1–F9.
- **Actionability:** Close the ODIN Fleet lead (concur). Add the three-fleet disambiguation rule to
  standing counsel procedure (concur strongly). One addition from my chair: the closed lead should be
  filed with its corpus-grep table attached (F7), so the next counsel that hears "fleet" can see the
  negative evidence without re-running it.
- **Verdict:** KEEP. Adopt the procedure.

---

## Nicks (all minor)

1. **The two failed direct fetches** (`browser-service exited with code 101`) are properly reported and
   correctly not retried — but it leaves every repo quote one step from live bytes. All the quotes I
   could check matched the index verbatim, so I have no reason to doubt them; still, a parent-level
   live-browser confirmation of the fleet-api README quote is the only outstanding receipt. Low priority.
2. **"A web search for it returns nothing under that path"** (re: `fourplayers/openclaw` on GitHub) —
   I did not independently verify the negative; my searches surfaced `4Players/openclaw-docker` and no
   `fourplayers/openclaw` repo result, which is consistent but not a proof of absence. Downgrade
   mentally from "observed" to "consistent with observation." Nothing turns on it.
3. **Coverage boundary on F8** (noted above): stored-observation zero ≠ never touched. The Nerd didn't
   overclaim; keep the boundary in the filing.

**Bottom line:** KEEP the file whole, KILL nothing, WOUND nothing. This is a model null — investigated,
debunked, bytes on the table, self-graded, and it leaves behind a procedural rule (the three-fleet
check) worth more than the lead ever was. Promote F9's disambiguation rule to standing doctrine.
