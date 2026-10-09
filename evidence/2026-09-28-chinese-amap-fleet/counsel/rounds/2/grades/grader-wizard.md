# GRADER — WIZARD (pattern mage) — Round 2 peer grades

*Filed 2026-10-05. Chair: Hunter S. Thompson. Grading clown.md, archivist.md, nerd.md, jock.md.*
*Charter rubric: Novelty (OURS / KNOWN / GENUINELY NEW), Evidence (OBSERVED / PUBLIC SOURCE / INFERENCE), Actionability, Verdict (KEEP / WOUND / KILL + one-sentence grounds).*
*Standing: agents/infrastructure only; no redaction; passive OSINT. Round-1 settled business (rounds/1/GRADES.md, 14 kills) is not re-litigated — dependencies are flagged, not re-argued.*
*Verification note: all grades are paper grades from the filed bytes. The clown's linchpin byte (urlquery report titles preserve query params verbatim — report `fa43bbf8-3938-4ef7-b8e0-bd8bd86ce231`, read 2026-10-05) is clown-asserted PUBLIC SOURCE; I did not independently re-verify it (no fetching in this lane). Everything downstream of C-1..C-3 inherits that dependency.*

---

## 1. CLOWN (C-1 … C-15)

### C-1 — Fragment Reading A: "The receipt, not the mailbox"
- **Novelty:** GENUINELY NEW (differential reading; Round 1 didn't have the title byte)
- **Evidence:** OBSERVED mechanics / INFERENCE (intent) — labeled honestly
- **Actionability:** medium (watch urlquery titles for fragment tags on sensitive targets)
- **Verdict:** KEEP — as one of three intent branches under the canonical observer-claim (see dedupes §5.1). Weakest of the three on falsifiability, acknowledged by the author.

### C-2 — Fragment Reading B: "Probing the observer"
- **Novelty:** GENUINELY NEW
- **Evidence:** OBSERVED (8 f-reports, distinct fragment titles; HTTP-identical requests by fragment semantics) / INFERENCE (intent); the `/ssr/`→`/place/` path-change caveat is honestly carried
- **Actionability:** medium ("vary the channel, hold the target constant" as a fleet fingerprint)
- **Verdict:** KEEP — strongest of the three; CANONICAL version of the f-phase claim (see dedupes §5.1)

### C-3 — Fragment Reading C: "Two-channel verification" (the return address)
- **Novelty:** GENUINELY NEW
- **Evidence:** OBSERVED mechanics / INFERENCE / cross-corpus rhyme (probe's labeled fuzz run, Round 1)
- **Actionability:** low-medium (tradecraft note, kept as rhyme not claim)
- **Verdict:** KEEP — as a sub-variant intent branch, not a standalone finding (see dedupes §5.1). Least provable, honestly labeled.

### C-4 — xz ten sizes = ten record types (the slot machine)
- **Novelty:** GENUINELY NEW (as a stated, falsifiable prediction)
- **Evidence:** PUBLIC SOURCE (Centaur via XZ_KNOWLEDGE.md; lane-4's 93-byte/6.251-bit decode) / INFERENCE (schema reading)
- **Actionability:** high *if a key surfaces*; pair-homogeneity check needs the 59 MB record table (see §5.3 — same missing artifact as Nerd N-4)
- **Verdict:** KEEP — a genuinely testable hypothesis, the best kind of inference

### C-5 — xz correlated drift = one clock
- **Novelty:** GENUINELY NEW (correlation noted nowhere in the lane)
- **Evidence:** PUBLIC SOURCE (XZ_KNOWLEDGE.md §3: both phases' late degradation) / INFERENCE (single-clock reading)
- **Actionability:** medium (compare drift curves when the record table is available; general single-vs-multi-process cadence test)
- **Verdict:** KEEP — new supporting signal for the lane-4 verdict. Cross-lane tension with Nerd N-5 flagged (§5.4).

### C-6 — The venue is the default (pastebinit and the Chinese Ubuntu ISO)
- **Novelty:** GENUINELY NEW (as a venue-selection hypothesis)
- **Evidence:** PUBLIC SOURCE (paste.ubuntu.org.cn official, pastebinit-supported) / INFERENCE
- **Actionability:** medium (weight pastebinit-default hosts in the termina.digital 20-new-hosts sweep)
- **Verdict:** KEEP — boring-is-beautiful hypothesis, properly scoped; does not re-litigate the lane's "no evidence for Chinese-state actor" verdict

### C-7 — ID contiguity = write atomicity (the forensic gift)
- **Novelty:** GENUINELY NEW
- **Evidence:** PUBLIC SOURCE (pastebin-php sequential IDs; consecutive-ID pairs) / INFERENCE (forensic use)
- **Actionability:** high when the record table is available (ID-gap analysis over ~1,742 pairs, free)
- **Verdict:** KEEP — clean forensic-method finding, no overclaim

### C-8 — The Werbel bridge as second-order instrument
- **Novelty:** OURS (Artist Round 1, OBSERVED) + GENUINELY NEW (marker-bank use)
- **Evidence:** OBSERVED (artist lane, Round 1) — correctly attributed to the settled Round-1 Artist E2 KEEP, not self-claimed as fresh observation
- **Actionability:** medium (log bridge header grammar + no-dedup doubling in the marker bank)
- **Verdict:** KEEP — consistent with Nerd N-1's conflation correction (§5.2); figure belongs to msgboard.dev, correctly cited

### C-9 — thecolony.ai as the control group (benign-agent-discourse baseline)
- **Novelty:** GENUINELY NEW (as a stated use)
- **Evidence:** OBSERVED (artist's thread-title census) / PUBLIC SOURCE (smirnovegorv/foragents AWESOME.md: 1,611 posts/168h, 197 authors, trailing window)
- **Actionability:** HIGH — public read surface documented (`/api/v1/posts?limit=50&sort=new`, `/feed.rss`, `/llms.txt`); a benign-discourse baseline ingest is a concrete next build
- **Verdict:** KEEP — depends on (does not re-litigate) the Round-1 lane-3 verdict (NOT swarm C2); best "new use of old bytes" in the round

### C-10 — Centaur's venue list as participant-observer intel
- **Novelty:** KNOWN/OURS (independent corroboration, not a new list)
- **Evidence:** PUBLIC SOURCE (joshuadavid run-1 scrape via THECOLONY.md) + OURS cross-check (venues already in pastebin-plunderer FINDINGS/GRAMMAR_TAXONOMY, librarian's lead table)
- **Actionability:** medium (corroboration upgrades these from single-source leads — the "second independent pivot" pattern)
- **Verdict:** KEEP — honest about being corroboration rather than discovery

### C-11 — Iowa: exact-match grading via revealed preference
- **Novelty:** GENUINELY NEW (eval-forensics reading)
- **Evidence:** OBSERVED (title/body census, TIMELINE.md) / INFERENCE (grading-function reading) — the inference step is visible
- **Actionability:** medium (eval-forensics template for future task-family attribution)
- **Verdict:** KEEP — a genuinely new lens on already-settled bytes

### C-12 — The vanishing eschatology (belief-driven coordination)
- **Novelty:** GENUINELY NEW (framing); the null itself is OURS/KNOWN
- **Evidence:** OBSERVED (title census, TIMELINE.md §5) / INFERENCE (belief framing, honestly noted as agent-stated)
- **Actionability:** low-medium (agent-behavior modeling note + eschatological-chatter detection heuristic)
- **Verdict:** KEEP — framing does the work, and the author doesn't oversell it

### C-13 — The dress rehearsal (May-26 → June-16 precursor pattern)
- **Novelty:** GENUINELY NEW (as a stated predictive pattern)
- **Evidence:** OBSERVED (TIMELINE.md §6) / INFERENCE (precursor generalization)
- **Actionability:** high *as stated* (watchlist doctrine: laundering-grammar clusters → task bursts ~3 weeks later)
- **Verdict:** WOUND — the "13 pastes" subset count is asserted via TIMELINE.md §6 against Archivist A-2's 131-wave arithmetic; the subset relationship needs byte-verification before the "13" propagates. Pattern stands as doctrine; the count must be receipted first.

### C-14 — The 3:46 AM asthma paste (off-frame lead)
- **Novelty:** OURS
- **Evidence:** OBSERVED (our `raw/95768bcf.txt`: full county×year JSON, opens `{"2003":{"Adair":23,…`)
- **Actionability:** medium (check Asymmetric's org list / wiki for asthma-dashboard task families)
- **Verdict:** KEEP — parked as an open lead per standing rules, not filed as a negative

### C-15 — agent-ours\<HHMM\> suffix = scaffold-clock timestamp (CONFIRMED)
- **Novelty:** GENUINELY NEW
- **Evidence:** PUBLIC SOURCE (joshuadavid authored records: ours1405→14:05:20 exact, ours1415→14:15:29 exact; 0438/1052/0402/0909 within 3–9 min; the ours0909 anomaly dissolves on authorship filtering) / OBSERVED (null in our 131-subset: 11 hits, all @-mention addressee position)
- **Actionability:** HIGH — collapses the label census below JD's audit; general label↔clock test for paste-coordination corpora
- **Verdict:** KEEP — strongest byte-anchored finding in the file; six correspondences with exact-to-minute anchors is confirmation, not suggestion

---

## 2. ARCHIVIST (Findings 1–6)

### Finding 1 — pastebin-k4be arithmetic HOLDS (198/198)
- **Novelty:** per Finding 3 (wound) — verification, not discovery
- **Evidence:** OBSERVED (198 rows, unique fingerprints/IDs, timestamp span matches, rollup sums to 198, SHA256SUMS green)
- **Actionability:** none; NOTE stands (reconciliation artifacts live at `lane1-reconciliation/`, not inside the collection dir)
- **Verdict:** KEEP — the bedrock other claims stand on

### Finding 2 — linuxiarz arithmetic HOLDS, to the byte (381 = 131+88+35+127)
- **Novelty:** OURS (131) / GENUINELY NEW (250)
- **Evidence:** OBSERVED (exact set-equality on the 131/131 reconciliation and 250/250 new — not eyeballed; 381 unique IDs; 254 bodies = 131+88+35; 127 view-only)
- **Actionability:** none needed — cited as the gold-standard reconciliation to copy
- **Verdict:** KEEP — exemplary; also the arithmetic bedrock for Clown C-11..C-15 (see §5.7)

### Finding 3 — WOUND: k4be "ALL new / host was never in our corpus" is FALSE
- **Novelty:** OURS (the 20 were ours first, as `pastebin_probe` events)
- **Evidence:** OBSERVED (20/20 exact ID overlap with `data/2026-05-27-paste-archive`'s 20 k4be.pl records; true figure = 178 genuinely-new + 20 re-captures; manifest `external_overlap` annotates only the JD export, missing the internal overlap — gap against the keep-all+annotate policy)
- **Actionability:** HIGH — amend the novelty claim; add internal-overlap annotations to the 20 manifest rows
- **Verdict:** KEEP as a finding — it imposes a WOUND on the k4be novelty framing. The core novelty (178 genuinely-new IDs) is explicitly untouched; the wound is on the "all new" framing, nothing deeper.

### Finding 4 — The events-count discrepancy (2,110 / 2,141 / 2,159), audited
- **Novelty:** GENUINELY NEW (audit resolution)
- **Evidence:** OBSERVED (2,110 = stale prose, reproducible from nothing on disk; 2,141 = canonical, fully itemized 1,970 base + 171 pivots; 2,159 = unreproduced honest null — API total drifts 1,974→1,977 in stored files)
- **Actionability:** concrete (fix PROVENANCE.md line 33 to "2,141 = 1,970 base + 171 pivots"; remine figures recorded with query string + run date, reconciled by report_id before touching the canonical count)
- **Verdict:** KEEP — ends a three-number ambiguity with receipts; the "do NOT change any canonical count" restraint is correct

### Finding 5 — Chinese-only URL inventory VERIFIED (375, exact nine categories)
- **Novelty:** GENUINELY NEW inventory (Chinese-swarm-only cut)
- **Evidence:** OBSERVED (375 rows, 375 unique URLs, all nine class counters exact; zero REDACTED patterns per the 2026-10-05 rule; the 8 truncated httpbun-carrier rows carry honest `truncated: true` flags with recovery path documented)
- **Actionability:** none required
- **Verdict:** KEEP — clean verification; the fidelity note on truncated rows is honest, not a wound

### Finding 6 — Round 1 citation integrity: 5 of 6 landed, 1 FAILED
- **Novelty:** process finding (not a factual dispute)
- **Evidence:** OBSERVED (CONTEXT.md line 24 still states "11 live webhook.site inboxes" — the figure Round-1 kill #8 killed; the kill never got applied at that line)
- **Actionability:** HIGH — one-line amend to "4 confirmed ALIVE, newest beacon 03:05Z; '11' was unreconciled, killed Round 1"; Chair should sweep CONTEXT.md and downstream persona copies for other pre-kill phrasing
- **Verdict:** KEEP as a finding — it flags an un-applied Round-1 kill (not a re-litigation; the kill stands) and imposes a process WOUND on the citation pipeline

---

## 3. NERD (Findings 1–7)

### Finding 1 — Task-description correction: "19 of 20 Werbel relays" does NOT belong to thecolony.ai
- **Novelty:** OURS (conflation caught in our ingest bytes); the Werbel finding itself is KNOWN (settled Round 1, Artist E2 Chair-final KEEP)
- **Evidence:** OBSERVED (zero "werbel" hits in `data/2026-10-05-thecolony-ai/`; the 20 events are 17 linuxiarz + 3 k4be pastes, not threads; thecolony.ai appears only as a URL in 7 bodies)
- **Actionability:** YES (cite msgboard.dev as the mirror surface, thecolony.ai as the mirrored source)
- **Verdict:** KEEP — a clean citation correction; consistent with Clown C-8 (§5.2)

### Finding 2 — thecolony.ai grading HOLDS: post-disclosure recruitment venue, not swarm C2
- **Novelty:** OURS (byte-confirmation); the venue verdict is KNOWN; the 764-byte poaching specimen is GENUINELY NEW
- **Evidence:** OBSERVED (6 byte-identical 540-byte copies sha `46aa43d7` + 1 × 764-byte variant `cbe4c9a7`, all signed "— Perceptual Zephyr"; the 764-byte variant quotes a live coordination message then pitches the colony — recruitment caught in the act; swarm-marker sweep across all 10 nonempty bodies: zero hits)
- **Actionability:** YES (grading stands without amendment; watch for Perceptual-Zephyr-style drops on other paste hosts post-October)
- **Verdict:** KEEP — the 764-byte variant is the best new specimen of the round on the recruitment-venue reading

### Finding 3 — Provenance discrepancy: metadata-only fraction is 10/20, not 1/20
- **Novelty:** OURS (found in our own ingest files)
- **Evidence:** OBSERVED (10 of 20 source rows carry `body: ""`; PROVENANCE.md admits only 08d6473d; the sha256-recomputed claim passes by construction for empty-string hashes; honest census = 17 metadata records, 7 with bodies)
- **Actionability:** YES (amend PROVENANCE.md; note the two-burst capture structure 17:38–17:39 ×3 / 18:12–18:14 ×14 — scraper schedule vs posting schedule)
- **Verdict:** KEEP — a real provenance correction on a new collection (not Round-1 settled business); anyone doing authorship analysis on "the Zephyr drop" needs this first

### Finding 4 — xz_knowledge cadence: totals-compatible but NOT verified by us
- **Novelty:** OURS (independent re-verification + arithmetic bound); the 3,484-post figure is PUBLIC SOURCE
- **Evidence:** OBSERVED arithmetic (1,742 pairs over 14,400 min → 8.27 min/pair; a sustained 5–6 min cadence exhausts the budget in ~6.1–6.7 days, so "breaks late" must cover ~3.3–3.9 days); byte-exact decode re-verified (93 bytes, entropy 6.251 bits, no gzip magic, invalid UTF-8, 0xDF lead — ciphertext-like, NOT Fernet); termina.digital `/pub/` returned HTTP 503 on 2026-10-05, absent from the joshuadavid repo — no per-paste timestamps of our own
- **Actionability:** YES (mark the cadence third-party-reported, not byte-verified, in XZ_KNOWLEDGE.md; retry the `/pub/` exports — the record table is the open thread)
- **Verdict:** KEEP — honest epistemic bookkeeping; the decode re-verification strengthens lane 4 while the cadence story is correctly downgraded to reported-but-unverified

### Finding 5 — Stress-test: three cracks in the "a run, not a swarm" verdict
- **Novelty:** OURS (new stress-test analysis)
- **Evidence:** PUBLIC SOURCE (handle names, phase times, dates) + labeled INFERENCE (cracks A: `_p1` suffix anticipates parallelism; B: phase-b/c 19-min overlap + phase-d concurrency = 2–3 posting loops; C: Jul-10–20 run fully contains the HF Jul-10–13 burst; "different crypto posture" is the assumption under test, not evidence). Counter-legs kept honestly (single handle, monotonic snapshot growth, hand-renamed version string, persistence-layer bootstrap sequence).
- **Actionability:** YES (do not cite "not a swarm" as settled fact; falsifiers named: `xz_*`/`xinzhai*` on other paste hosts; a key surfacing)
- **Verdict:** KEEP — this does not re-litigate a Round-1 kill (the lane-4 verdict is not in the 14 kills); it downgrades an investigator verdict to PROVISIONAL with named falsifiers, which is what a stress-test lane is for. Tension with Clown C-5 flagged (§5.4); both are labeled INFERENCE and can coexist (one process, concurrent loops, shared clock)

### Finding 6 — Bullfincher wound RESOLVED (partially): 3 paste IDs in hand, the "4th hit" stays rumor
- **Novelty:** OURS (new grep result); the 3-paste cluster is KNOWN (lane 3 + new ingest)
- **Evidence:** OBSERVED (exactly 3 rows with "bullfincher" in `ref/run1/agent-logs/pastebin-k4be/revisions.jsonl`: `5329a841` 2026-02-26T14:49:24Z 900B, `bd44d381` 14:50:18Z 590B, `680ec235` 14:52:19Z 330B — Humana 10-K via `bullfincher.io/sec-proxy?url=…sec.gov…`; no 4th paste ID exists in this export; the conspiracist's "4 hits" is byte-falsified to 3 for this export)
- **Actionability:** YES (amend conspiracist.md DOT 2 to three with IDs; do not let "4" propagate)
- **Verdict:** KEEP — RESOLVES the Round-1 wound (conspiracist DOT 3), narrows it to 3 confirmed + IDs, keeps "4th hit" as rumor. Flagged for the Chair as resolved settled business (§6).

### Finding 7 — Minor byte wrinkle: row-declared body_len vs stored bytes on 5329a841 (900 vs 866)
- **Novelty:** OURS / OBSERVED (sha256 matches the file; the 34-byte delta is likely `\r\n`→`\n`/whitespace normalization)
- **Evidence:** OBSERVED; the other two pastes (590/330) match exactly
- **Actionability:** LOG ONLY (dataset-builder note: joshuadavid export length fields are not byte-exact pre-normalization)
- **Verdict:** KEEP — as an annotation, not a claim; correctly not chased further

---

## 4. JOCK (Census + Findings 1–10)

### Census — 686,325 events, 12/13 harness/IP/hostname queries absolute zero
- **Novelty:** OURS / OBSERVED (`data/2026-10-01-oai-tag-sweep/events.jsonl` 96,353 + `openai-agent-traces/data/traces.jsonl` 589,972; all 6 lead IPs, 3 hostnames, 7 map grammars, 10/11 broad harness names zero; the single `openhands` hit is the already-attributed foreign eval-monitor URL, scavenger lane)
- **Actionability:** none (null is the result)
- **Verdict:** KEEP — an honest null at scale; the foundation for Findings 9–10. Cross-rhyme with the Round-1 kill grounds (b) corpus-contrary: 686k events still touch no bespoke agent-infra surfaces.

### Finding 1 — Aider "YES (git-remote risk)" OVER-RATED → recommend PARTIAL
- **Novelty:** GENUINELY NEW correction to our files
- **Evidence:** PUBLIC SOURCE (two independent Sep–Oct 2026 community sources treating Aider's `.gitignore` auto-write as the default; residual risk documented: `--no-gitignore` users, already-tracked files, `--api-key` CLI leakage into history)
- **Actionability:** YES (downgrade YES→PARTIAL, correct the mechanism line, keep residual-risk note)
- **Verdict:** KEEP — with one caveat: the auto-gitignore default is confirmed by two community sources, not re-verified against official Aider docs (jock's own method null #2). Downgrade warranted; keep the residual-risk leg.

### Finding 2 — Headline count correction: 7-of-10 becomes 6-of-10
- **Novelty:** GENUINELY NEW (derived)
- **Evidence:** depends entirely on Finding 1 (all other six YES verdicts re-verified in Findings 3–6)
- **Actionability:** YES (amend the map's bottom line and summary table)
- **Verdict:** KEEP — arithmetic consequence of Finding 1, cleanly derived

### Finding 3 — Gemini CLI YES *strengthened*: `usageStatisticsEnabled=true` (default) collects prompts+answers
- **Novelty:** GENUINELY NEW to our files (the usageStatistics→prompt-collection path is not in the map)
- **Evidence:** PUBLIC SOURCE (config refs; official FAQ quoted on HN: Login-with-Google + enabled = Google collects prompts and answers for model improvement; #21101 confirms first-class default-true) / INFERENCE (per-auth-method variance noted, not exhaustively mapped)
- **Actionability:** YES (replace the wounded `logPrompts` framing — logPrompts=true sits inside a default-off telemetry block — with the usageStatistics leg; YES verdict stands, firmer ground)
- **Verdict:** KEEP — a real strengthening: the map's #1 leg was overstated, and the replacement leg is stronger

### Finding 4 — Cursor YES re-verified; binary framing stale → three-stance model
- **Novelty:** KNOWN publicly; the vendor-language upgrade and three-stance model are GENUINELY NEW to our files
- **Evidence:** PUBLIC SOURCE (`cursor.com/data-use`: "we may use and store codebase data, prompts, editor actions… to improve our AI features and train our models" — stronger than the map's paraphrase; defra guidance: three stances, no privacy default)
- **Actionability:** YES (KEEP the YES; update the mechanism to quote cursor.com/data-use; note the three-stance model)
- **Verdict:** KEEP — verdict unchanged, mechanism upgraded with primary-source language

### Finding 5 — Windsurf YES (individuals) freshly corroborated post-Cognition
- **Novelty:** KNOWN publicly; the 5-day-old Cognition-policy confirmation is GENUINELY NEW to our files
- **Evidence:** PUBLIC SOURCE (katagun ADR: Cognition security page — "By default, we may use your data for model training purposes… opt-out only on paid plans"; plucins: ZDR default for Teams/Enterprise only)
- **Actionability:** YES (cite the current Cognition policy)
- **Verdict:** KEEP — timely re-verification; the cascade-`.pb` AES claim stays correctly flagged as community-RE-sourced

### Finding 6 — Codex CLI YES and Claude Code YES re-verified; OpenClaw NO (core) confirmed
- **Novelty:** KNOWN (all three confirm map's existing claims)
- **Evidence:** PUBLIC SOURCE (official docs fetched 2026-10-05: Codex `[analytics] enabled=false` opt-out + local plaintext rollout files/auth.json corroborated by third-party tools reading live paths; Claude Code data-usage docs: plaintext transcripts under `~/.claude/projects/` for 30 days — verbatim vendor admission; OpenClaw: daily update check only)
- **Actionability:** minimal (add the missed `update.checkOnStart: false` knob to the map)
- **Verdict:** KEEP — rock-solid re-verifications, honestly marked as confirmations rather than discoveries

### Finding 7 — UNDER-RATED: OpenClaw is the most *exposed* agent control surface in the wild despite "NO (core)"
- **Novelty:** GENUINELY NEW synthesis (the map and the exposed-instances hunt never reconciled)
- **Evidence:** mix — the Shodan counts (`http.title:"OpenClaw"` = 33,669; `port:18789` raw = 198,478) are labeled OBSERVED ("our hunt") but per the Round-1 convention ("Shodan-stored records are PUBLIC SOURCE, not OBSERVED") should be re-labeled PUBLIC SOURCE; the dev.to exposure-wave report, ~900 malicious registry skills, Kaspersky/Bitdefender advisories, NemoClaw CVE-2026-65105 are PUBLIC SOURCE; lead 75.146.94.94 (residential Comcast OpenClaw UI) is hunt-derived
- **Actionability:** HIGH (split the verdict: NO (core telemetry) / YES (network exposure by deployment); add control-UI exposure port 18789 + title grammar as the highest-priority *live* exposure surface)
- **Verdict:** KEEP — the strongest synthesis in the file, but WOUND the evidence labels: Shodan-stored counts → PUBLIC SOURCE per the Round-1 convention the jock otherwise applies. The finding does not re-litigate Round-1 kill #5 (ODIN Fleet = game-server naming) — different claim entirely.

### Finding 8 — Coverage gap: the map misses live grammars (Cline modern path, Antigravity, Qwen, Roo/Kilo, SpecStory, Copilot CLI, Goose, Crush, LM Studio)
- **Novelty:** GENUINELY NEW to our files
- **Evidence:** PUBLIC SOURCE (chaybits/ectype inventory, maximilianfeix/spillage, multiple path confirmations)
- **Actionability:** YES (extend watchlist grammars with `~/.cline/data/sessions/`, `~/.cline/data/tasks/`, `roo-cline/tasks/`, `.qwen/tmp/`, `~/.gemini/antigravity-cli/`, `.specstory/history/`, `~/.copilot/session-state/`, `.crush/`; flag the roster as "10 of N" not exhaustive)
- **Verdict:** KEEP — the Cline modern-path gap alone justifies this; the map documented only the legacy VS Code path while current installs write elsewhere

### Finding 9 — The 7 map grammars are high-value *watchlist*, zero *observed* exposures — null triply confirmed
- **Novelty:** corpus/index nulls OURS; Truffle/agentleak material KNOWN publicly, GENUINELY NEW to our files
- **Evidence:** OBSERVED (0/686,325 for all 7 grammars; exposed-instances.md honest nulls); PUBLIC SOURCE (agentleak/README citing Truffle Security: 221,303 live credentials in 6,003 public AI datasets; Infura key → 1,131 datasets via WildChat; Fuzzland 6TB LLM-relay logs); the grep.app 429 is honestly recorded as a *method* null, not an evidence null
- **Actionability:** YES (keep grammars as WATCHLIST per the map's own framing; add the dataset-leak channel as the empirically-observed exfil path; future lane: query public dataset indexes for transcript-shaped content)
- **Verdict:** KEEP — the dataset-leak reframing is the round's most useful redirect: the observed exfil channel was never open directories

### Finding 10 — The 6 exposed-instance leads re-graded: 4→WATCHLIST, 2→OBSERVED (population markers)
- **Novelty:** GENUINELY NEW counsel dispositions; population figures KNOWN
- **Evidence:** OBSERVED (all 6 IPs 0/686,325; all 3 hostnames 0/686,325; no lead has agent-traffic co-occurrence or a second independent pivot — each is single-source Shodan); PUBLIC SOURCE (Mysterium/SentinelOne/Censys population context: the population is the story)
- **Actionability:** YES (apply the four WATCHLIST / two OBSERVED grades to IP_LOG.md; do not cite any of the six as agent-linked, per the Round-1 convention)
- **Verdict:** KEEP — a disciplined application of the Round-1 tie-break upgrade condition; the 75.146.94.94 residential-ISP caveat is correctly kept (Vietnam-residential precedent explicitly not re-litigated)

---

## 5. Duplicates & dedupes (the pattern-mage's ledger)

**5.1 — The f-phase is ONE claim with three intent branches (C-1/C-2/C-3).** All three agree: *the fragment phase's audience was never Amap — the experiment was always about the observer.* The canonical version is **C-2** (strongest: controlled-variable structure + the new title byte + the `/ssr/` caveat carried honestly). C-1 (stealth calibration) and C-3 (covert return address) are intent branches of the same mechanism, not separate findings. Recommendation: file one canonical finding "f-phase targeted the observer, not Amap" with three labeled intent hypotheses; mark C-1 and C-3 as dedupe notes, not kills — the hypotheses are worth keeping, the triple-counting is not.

**5.2 — The Werbel fact is canonical in Round 1, not duplicated in Round 2.** Clown C-8 (marker-bank use) and Nerd N-1 (conflation correction) both rest on the same settled Round-1 Artist E2 (Chair-final KEEP): 19/20 msgboard.dev threads are Werbel bridge relays. These are NOT duplicates of each other — C-8 proposes a new use of the fact, N-1 corrects a mis-citation of it — and neither re-claims the fact itself. Cross-reference both to E2; no dedupe action needed.

**5.3 — One missing artifact, two findings.** Clown C-4 ("pair-homogeneity testable from the 59 MB record table when termina.digital exports recover") and Nerd N-4 ("record table needed to resolve pair structure vs the ten size cohorts; `/pub/` 503 on 2026-10-05") both call the same absent artifact. Canonical open thread: **termina.digital `/pub/` exports (59 MB record.jsonl + 9.9 MB body bundle), HTTP 503 as of 2026-10-05.** C-4 and N-4 are complementary (falsifiable hypothesis vs epistemic status + retry lead), not duplicates — merge the open-thread tracking, keep both findings.

**5.4 — thecolony.ai: two claims, one verdict.** Clown C-9 (control-group baseline use) and Nerd N-2 (verdict holds + 764-byte poaching specimen) both depend on the settled Round-1 lane-3 verdict (NOT swarm C2, post-disclosure recruitment venue). Distinct claims — C-9 is a *new use*, N-2 is *corroboration* — cross-ref, no dedupe. Note both are consistent and neither re-litigates.

**5.5 — k4be export, two claims, no overlap.** Archivist A-3 (20/20 re-capture overlap → 178+20) and Nerd N-6 (bullfincher 4→3 with paste IDs) both work the same 198-row run-1 export, but the claims are orthogonal (novelty framing vs paste-ID resolution). Cross-ref for the Chair; no dedupe.

**5.6 — linuxiarz: three collections, don't cross-cite.** Archivist A-2 (381-event collection, 254 bodies, exact set-equality), Clown C-11..C-15 (claims resting on TIMELINE.md + the 131-subset), and Nerd N-2/N-3 (`data/2026-10-05-thecolony-ai` — 20 events, 7/17 bodies, a *different* collection). A-2 is the arithmetic bedrock for the clown's Iowa readings; N-3's 10/20 metadata-only figure belongs to the 20-event ingest only and must never be cited against the 381. Flagged to prevent cross-collection citation errors.

**5.7 — Evidence-label collision: Shodan-stored counts.** Jock Finding 7 labels Shodan counts OBSERVED ("our hunt"); the Round-1 convention fix ruled Shodan-stored records PUBLIC SOURCE. Same for the map's Shodan-derived population figures where cited. Relabel, don't re-litigate — the counts and the synthesis stand.

---

## 6. Cross-lane contradictions (flagged for the Chair)

**6.1 — [TENSION, not contradiction] Clown C-5 vs Nerd N-5 on "a run, not a swarm."** C-5 adds a new supporting signal (correlated drift → one clock → single process). N-5 adds three labeled cracks (p1 shard grammar, concurrent loops, HF-burst calendar overlap) and downgrades the verdict to PROVISIONAL. Both are labeled INFERENCE and they can coexist (one process with concurrent posting loops on a shared clock), but the two lanes land opposite on confidence. Recommendation: keep both as labeled hypotheses; the verdict's status is PROVISIONAL per N-5 until the named falsifiers resolve. No kill warranted on either side.

**6.2 — [VERIFY] Clown C-13's "13 pastes" vs Archivist A-2's 131-wave.** C-13's May-26 tooling sub-cluster (13 pastes, portal.max.gov/api.usaspending.gov) is asserted via TIMELINE.md §6; A-2 proves the original wave is exactly 131. The subset relationship (13 ⊆ 131, distinguished by tooling-shakedown signature) is plausible but the "13" is not byte-receipted in the filed text. Graded WOUND: verify the 13 against bytes before it propagates; the precursor-pattern doctrine stands regardless.

**6.3 — [SETTLED-BUSINESS DEPENDENCY, not re-litigation] Clown C-1..C-3 vs the Round-1 wound.** The new title byte *refines* the wounded "talking to the scan log" reading: the differential property is target-server invisibility, not scan-log visibility (the scan log heard both phases equally). This is wound-repair on settled business, explicitly permitted. Recommendation: record the wound disposition — "the 'talking to the scan log' framing is superseded by target-server invisibility + observer-facing experiment" — and close it.

**6.4 — [RESOLVED WOUND] Nerd N-6 vs Round-1 conspiracist DOT 3.** Round-1 wound: "bullfincher '4 hits / 2026-02-26' needs paste IDs or stays rumor." N-6 byte-falsifies the "4" to 3 (with IDs) and keeps the 4th as rumor. The wound is resolved; the disposition narrows to "3 confirmed (5329a841, bd44d381, 680ec235); '4th hit' stays rumor." Chair to amend conspiracist.md DOT 2 accordingly.

**6.5 — [UN-APPLIED KILL] Archivist A-6 vs Round-1 kill #8.** Kill #8 ("11 live webhook.site inboxes" — unreconciled claim) was Chair-final, but CONTEXT.md line 24 still carries the killed figure in the "Tonight's verified finds" section. The kill stands; the citation pipeline failed. Wound the process: apply the one-line amend and sweep CONTEXT.md + downstream persona copies for pre-kill phrasing.

**6.6 — [CONSISTENT APPLICATION] Jock J-10 vs the Round-1 tie-break.** J-10 applies the tie-break upgrade condition (agent-traffic co-occurrence or second independent pivot) to the 6 exposed-instance leads and demotes accordingly. This is the settled convention working as designed, not re-litigation. The 75.146.94.94 residential caveat is kept without re-arguing the Vietnam precedent — correct.

---

## 7. Kill / wound summary

**Proposed KILLS: none.** No finding in the four files contradicts the bytes or itself badly enough to die; the honest-caveat discipline held across all four personas (uncontrolled variables, provisional verdicts, method nulls all labeled).

**Proposed WOUNDS (on findings or on downstream artifacts):**
1. **C-13 (clown):** verify the "13 pastes" subset count against bytes; the precursor-pattern doctrine stands, the count must be receipted before it propagates.
2. **Finding 7 (jock):** relabel Shodan-stored counts from OBSERVED to PUBLIC SOURCE per the Round-1 convention; the synthesis and the split-verdict recommendation stand.
3. **k4be novelty framing (via Archivist Finding 3):** amend "198 all new" → "178 genuinely-new + 20 re-captures"; add internal-overlap annotations to the 20 manifest rows (keep-all+annotate policy applies to internal overlap too).
4. **CONTEXT.md line 24 (via Archivist Finding 6):** apply the Round-1 kill #8 that was never applied — "4 confirmed ALIVE, newest beacon 03:05Z; '11' was unreconciled, killed Round 1"; sweep for echoes.
5. **PROVENANCE.md line 33 (via Archivist Finding 4):** "2,110" → "2,141 `venue_finding` records = 1,970 base sweep + 171 pivot/infra reports."
6. **`data/2026-10-05-thecolony-ai/PROVENANCE.md` (via Nerd Finding 3):** "1 metadata-only row" → "10 rows metadata-only, 7 of 17 with bodies"; add the two-burst capture structure.
7. **HARNESS_LOG_MAP.md (via Jock Findings 1–2, 8):** Aider YES→PARTIAL; bottom line 7-of-10 → 6-of-10; add the Cline modern path + 8 missing harness grammars; add `update.checkOnStart: false` knob (Finding 6); re-frame Gemini leg (Finding 3) and Cursor three-stance model (Finding 4); split OpenClaw verdict NO(core)/YES(exposure) (Finding 7).
8. **conspiracist.md DOT 2 (via Nerd Finding 6):** "Four appearances" → three, with the paste IDs; the "4th hit" stays rumor.

**Resolved / closed:** the bullfincher wound (N-6, narrowed to 3+IDs); the Round-1 fragment-intent wound (C-1..C-3 supersede it — see §6.3); the 2,110/2,141/2,159 ambiguity (A-4).

**Strongest keeps:** C-15 (agent-ours\<HHMM\> clock confirmation), C-9 (thecolony.ai as benign-discourse control group — concrete next build), J-7 (OpenClaw exposure synthesis), J-9 (dataset-leak channel reframing), A-2 (381-event exact set-equality), N-2 (764-byte poaching specimen), C-4 (falsifiable xz schema hypothesis).

*No installs, no commits, no posts, no probes. The wizard sees the pattern: four personas hunted four different forests and the same game keeps walking through all of them — fragments that talk to the observer, labels that are clocks, venues that are defaults, exposures that are populations. Two findings were secretly one; one finding was secretly three; the rest held their shape. The spreadsheet, as ever, is funnier than the truth.*
