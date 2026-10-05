# CLOWN grades ARCHIVIST — Round 1

*Peer grading, charter rubric. Filed 2026-10-05. Every claim below was either re-touched by my own bytes or is labeled as the Archivist's.*
*Corroboration I ran myself: epoch decodes (`date -u -d @<nonce>`) for all three showcase rows — 1781681519 → 2026-06-17 07:31:59 ✓, 1776567917 → 2026-04-19 03:05:17 ✓, 1778400745 → 2026-05-10 08:12:25 ✓. Corpus greps: `litter.catbox.moe` = 0 in amap-fleet events.jsonl, 1 in oai-tag-sweep events.jsonl ✓ (matches "only ONE in-corpus").*

---

## Finding 1 — Apr 19 six-report epoch-nonce `.html` burst (~4-min cadence, 03:05–03:25 UTC)
- **Novelty:** GENUINELY NEW (CONTEXT knew only the single May 10 URL; the six-report burst timeline is this lane's)
- **Evidence:** OBSERVED (urlquery htmx search results; I re-verified the first nonce's epoch decode independently)
- **Actionability:** CONCRETE — reconcile the Apr 19 burst against documented incident windows (predates Artifactory May 7+, DoE Jun 17, HF Jul 10–13; overlaps UNCTADstat). If the self-nonce family is toolkit grammar, Apr 19 is an early specimen worth filing into the self-nonce family index.
- **Verdict: KEEP** — six sequential uploads on a four-minute metronome is not a human with a browser; it's a loop with a clock, and the nonce is the clock's fingerprint.

## Finding 2 — May 10 `hdcf0x.html?x=…` nonce = 32s pre-report (self-nonce)
- **Novelty:** OURS (already in-corpus as `epoch_nonce`, hunt campaign `reader-proxy-ops`)
- **Evidence:** OBSERVED (corpus row `c6ec491c`; epoch decode verified by me)
- **Actionability:** none beyond anchoring — this is the type specimen, not a new animal.
- **Verdict: KEEP** — the anchor row that makes Finding 1 a family instead of a coincidence.

## Finding 3 — Apr 26–27 / May 1–2 `.html` bursts; May 12 `.js`/`.mjs` pair; Jul 27 `z4gr71.apk`
- **Novelty:** GENUINELY NEW (burst chronology assembled by this lane)
- **Evidence:** OBSERVED (htmx search results)
- **Actionability:** CONCRETE — the `.apk` belongs in a human-threat lane's inbox (urlquery metadata only, per standing rules); also re-sweep urlquery for post–Jul 27 litterbox self-nonce `.html` to confirm the surface is dead rather than sleeping.
- **Verdict: KEEP** — a chronology nobody had drawn; the `.js`/`.mjs` same-minute pair smells like someone testing what the sandbox will execute.

## Finding 4 — `litter.catbox.moe` = official Litterbox storage subdomain; 6-char names are native grammar
- **Novelty:** KNOWN (public: hagezi/dns-blocklists#7819, vjt/grappa-irc 764486b079499e314a078ff610dc0aa054c8f09c)
- **Evidence:** PUBLIC SOURCE (linked)
- **Actionability:** none — it's plumbing, but load-bearing plumbing.
- **Verdict: KEEP** — this is the finding that stops every future lane from writing a breathless report about "random 6-char agent filenames" on catbox. Boring is a feature.

## Finding 5 — Litterbox's malware-drop reputation (threat-intel blocklisting)
- **Novelty:** KNOWN (public: NextDNS metadata #1196, blocklist feeds)
- **Evidence:** PUBLIC SOURCE (linked)
- **Actionability:** none — context, not a step.
- **Verdict: KEEP** — it keeps Finding 6 honest. You can't claim agent attribution while standing in a room full of malware ops and pretending the smell is yours.

## Finding 6 — Agent attribution of the self-nonce family ("agent-shaped, unproven")
- **Novelty:** open
- **Evidence:** INFERENCE (labeled as such)
- **Actionability:** CONCRETE — file the Apr 19 burst + May 10 row into the cross-corpus self-nonce family index (`zz=oai`, `taersitokennav…-START`, etc.) as *candidate* members; attribution stays unfunded until a second agent-only marker co-occurs on a litterbox URL.
- **Verdict: WOUNDED** — shaped like an agent, dresses like a malware op, and zero agent markers (`zz=`, `uqscan=`) appear on any of the 68 litterbox URLs. The Archivist hedged correctly; the hedge is the finding. Ship the grammar, not the ghost.

## Finding 7 — `z4gr71.apk` graded HUMAN-KIT-SHAPED
- **Novelty:** OURS (this lane's grading)
- **Evidence:** INFERENCE (blocklist-awareness argument: Litterbox blocks .exe/.jar but not .apk — the uploader knew the menu)
- **Actionability:** CONCRETE — hand to a human-threat lane; check the urlquery report's metadata/tags for campaign context (no fetch).
- **Verdict: WOUNDED** — the blocklist-menu argument is the only load-bearing beam, and it's a good one, but without payload bytes "human-kit-shaped" is still a silhouette, not a suspect. Keep the grade, don't upgrade it.

## Finding 8 — "Litterbox is a live agent dead-drop surface" → REFUTED
- **Novelty:** n/a (a kill, not a claim)
- **Evidence:** OBSERVED (timeline: nonce activity Apr 19–May 10; last report Jul 27)
- **Actionability:** none — the action is the funeral.
- **Verdict: KILL (the claim), KEEP (the kill)** — a lane that kills its own headline is a lane the Chair can trust with live ammo. First-class honest negative.

## Finding 9 — Audit A: `zz=oai` epoch+random decomposition HOLDS 3/3
- **Novelty:** KNOWN (tonight — CONTEXT #1)
- **Evidence:** OBSERVED (I confirmed the `oai17816815195423336` value exists in traces.jsonl and re-decoded the epoch myself: 2026-06-17 07:31:59, +2s to capture — matches)
- **Actionability:** none — the audit's job is to be boring, and it was boring correctly.
- **Verdict: KEEP** — the Archivist did the thing the title promises: provenance with a citation, verified against primary rows.

## Finding 10 — Audit B: fresh `3b5027e4` inbox identity/freshness HOLDS
- **Novelty:** KNOWN (tonight — CONTEXT #2)
- **Evidence:** OBSERVED — I corroborated end-to-end: `metronome/raw/htmx_webhook_site.json` contains `3b5027e4-de70-4980-a49d-7ae97613c517?page=header3`; `tracker/raw/deaddrops.md` lists report `c9104bb8` with the same URL at 03:19; `new-fleets/FINDINGS.md` mentions the inbox.
- **Actionability:** CONCRETE — fix the citation address: the Archivist filed paths as `personas/...` relative to the counsel directory, where they don't exist. The files live at `data/2026-09-28-chinese-amap-fleet/personas/...`. A citation with the wrong address is a letter sent to the wrong house.
- **Verdict: KEEP (substance), citation address must be corrected** — the evidence is real and multi-file; only the path is drunk.

## Finding 11 — `?r=<19-digit>` nonce family: citation incomplete
- **Novelty:** KNOWN (tonight — CONTEXT #4), but *unfunded by this report*
- **Evidence:** none filed (the Archivist's own greps returned zero; the evidence lives with another lane)
- **Actionability:** CONCRETE — the claiming lane must file raw report IDs and rows into the shared record; until then this claim rides on CONTEXT's authority, not evidence.
- **Verdict: WOUNDED** — not a failure, an IOU. Debts get collected in Round 2.

## Finding 12 — Open thread: Apr 19 burst vs Nov-2025-origin thesis
- **Novelty:** OURS (this lane's framing)
- **Evidence:** INFERENCE (timeline comparison)
- **Actionability:** CONCRETE — compare the Apr 19 self-nonce grammar byte-for-byte against the Nov-2025+ self-nonce family; if it matches, Apr 19 becomes the earliest toolkit specimen and the origin thesis gets a birthday.
- **Verdict: KEEP** — an open thread with a concrete next step is a finding wearing casual clothes.

---

## Chair's summary (the funny part)

The Archivist went looking for a live dead-drop and came back with a corpse, a clock, and an apology — which is the best possible outcome, because the clock is the actual story. A six-report burst on a four-minute metronome in April, each URL carrying its own birth timestamp like a hospital bracelet, on a temp host the malware kids already loved. The Archivist refused to call it an agent, refused to call it a human, and filed the grammar instead. That's not indecision — that's the discipline that keeps the rest of us from hallucinating. The litterbox lane is dead; the self-nonce grammar is alive; somebody please reconcile April with November before the Chair has to.
