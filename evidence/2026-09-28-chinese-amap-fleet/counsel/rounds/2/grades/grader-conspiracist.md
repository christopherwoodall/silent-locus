# COUNSEL Round 2 — GRADES: the CONSPIRACIST's voice

*Grader: the Conspiracist — connect dots, graded on whether the dots hold.*
*Chair: Hunter S. Thompson. Graded 2026-10-05.*
*30 findings across 4 files. Round 1's 14 kills treated as settled; nothing re-litigated (dependencies flagged, not re-argued).*
*Rubric per finding: Novelty (OURS / KNOWN / GENUINELY NEW) · Evidence (OBSERVED / PUBLIC SOURCE / INFERENCE) · Actionability · Verdict (KEEP / WOUND / KILL).*

**Conspiracist's bottom line up front:** 30 findings, **0 KILLS, 0 WOUNDS, 30 KEEPS**. Nothing in these files asserts a connection the bytes don't carry — the inference-heavy findings (W-3, N-5, C-1, C-4) are all labeled as inference and kept honest, which is the only thing that saves them from my knife. Two findings take my own Round-1 dots apart with evidence (W-6, N-6) and I accept the corrections — the directional claims survive on better-receipted ground, which is how this is supposed to work. The real grading story this round is in the cross-lane section: the nerd and the wizard independently decomposed the same Zephyr drop to the same ×6+1 structure, which is corroboration neither of them could buy.

---

## §1 — WIZARD (pattern mage), 7 findings

### W-1 — K4be probe battery as launcher grammar
- **Novelty:** GENUINELY NEW as a named grammar analysis (bytes PUBLIC SOURCE via joshuadavid export; analysis OURS). Concur with hunter's grade.
- **Evidence:** OBSERVED — and genuinely re-derived, not review-asserted: title↔body index correlation verified pairwise across all 70 PADs, clock-derived suffixes checked against body epochs, 224s cadence with 3.2s ticks computed from epoch ranges, collision check run against all 198 bodies. This is the round's most audit-proof piece of byte work.
- **Actionability:** YES — named grammar `k4be-probe-battery` as a tripwire on other paste hosts; explicit instruction not to cite it as OAI-toolkit.
- **Verdict: KEEP.** The dot this connects is a negative one, and negatives are the hardest dots to hold: the k4be prober is grammatically disjoint from the June/OAI markers (`zz=` 0, `oai` 0, `jina` 0 across 198 bodies), so under BigSexyWarlock69's refined "same provider, different agents, different evals" framing, this is a k4be-local harness, not a toolkit sighting. The TEL-series click-probe read (same link, 17 fresh epochs, "MAYBE" = testing fetch behavior) is inference-grade mechanism inference that stays inside what the bytes show. Conspiracist's check: 70/70 title-index==body-index is the kind of over-perfect correlation that usually means a single loop in a single script wrote these — the harness claim earns its confidence here.

### W-2 — CORRECTION: `pad-<epoch>-<n>` taxonomy negative is wrong
- **Novelty:** OURS (correction to our own document). **Evidence:** OBSERVED (grep → 70 hits).
- **Actionability:** YES — amend GRAMMAR_TAXONOMY.md §E with `pad-<epoch>.<frac>-<idx>` ×70 (k4be only).
- **Verdict: KEEP.** Self-correction of an honest negative is the behavior the charter wants. Conspiracist note: the mechanism of the error is documented (battery pattern narrower than the real grammar — the `.5110793` microsecond fraction broke the `pad-\d{10}-\d+` shape), which means the correction is reproducible, not confessional. And the direction of the error is the honest one: we *under-claimed* a grammar we own. It tightens W-1 rather than loosening anything.

### W-3 — Two ID schemes, one campaign (clock-derived TK/TEL vs random PAD)
- **Novelty:** GENUINELY NEW (analysis OURS). **Evidence:** INFERENCE, explicitly labeled as such — counts OBSERVED, the "one prober, two probe types" read INFERENCE.
- **Actionability:** LOW — filed as a harness-behavior note; future re-mix of both schemes corroborates same-launcher.
- **Verdict: KEEP (as labeled inference).** Adversarial pass: "not copy-paste" is doing the most work here, and one-day-one-host is weak glue for identity claims — two different tools could run on the same day. But the finding doesn't claim identity; it claims the *dual-scheme observation* and files it. The label discipline is what keeps it alive. It functions as a corroboration line for W-1, not a freestanding claim.

### W-4 — Iowa eval-shape stress test: "strong circumstantial, no named eval claimable" survives
- **Novelty:** OURS (the stress test) / KNOWN (markers from the public jd repo). **Evidence:** OBSERVED bars + PUBLIC SOURCE web search.
- **Actionability:** YES — the exact-prompt string (`"Now, do the same for 85 and older"` + IDPH Tableau) as a standing tripwire for the benchmark ever publishing.
- **Verdict: KEEP.** Four bars, four unmet, each receipted: no benchmark text match (search hits only the jd corpus itself), no run ID/harness/provider marker (clean `oai`/`zz` negative re-verified), Asymmetric Security still preliminary and contact-gated, the June-16 wiki bridge searched 11 wiki exports → zero. The honest gap is *amplified*, not buried — jd's own follow-up says the bytes don't even settle eval-vs-training, and the report is told to keep both hedges. Conspiracist's check: the pro-eval side is given its full weight (literal "benchmark clock" / "benchmark task", 10–16s deadlines, sacrifice protocol, exact-prompt mirroring, staggered 9m54/10m02/15m42 cohorts = multi-wave launch shape). This is stress-testing done right — the strongest opposing evidence is presented before the verdict stands.

### W-5 — `scaffold`/`terminal_epoch` clock vocabulary: open identification problem
- **Novelty:** OURS (bytes) / KNOWN (phenomenon, jd repo) / GENUINELY NEW (named-harness attribution — none exists). **Evidence:** OBSERVED + PUBLIC SOURCE (web search returns only the jd repo; one unrelated generic usage).
- **Actionability:** YES — `terminal_epoch` + `scaffold NN:NN` as a cross-corpus eval-harness tripwire; a future non-Iowa sighting = a second run of the same harness.
- **Verdict: KEEP.** The 2 "water clock" false friends in k4be fantasy prose are *checked and named*, which is exactly the disambiguation discipline this vocabulary needs. 39 linuxiarz bodies carry it; 0 in k4be; every other sighting (collusion-wiki, oai-tag-sweep, intermediary-relays) traced to copies of the same Iowa artifacts — the "no independent sighting" claim is sourced, not asserted. Conspiracist's check: this is filed as a *tripwire*, not an attribution — the finding refuses to turn absence of documentation into a positive claim. Correct.

### W-6 — ×22 count decomposition: the figure is not reproducible; two factual errors; wound stays open on direction
- **Novelty:** OURS. **Evidence:** OBSERVED (headcount audit: jd revisions.jsonl → 11; our 381+198 → 19; md5 over the 7 Zephyr bodies → ×6 identical + 1 variant).
- **Actionability:** YES — strike ×22 and its decomposition from DOT 3; replace with the inventoried 19 (17 Zephyr + 2 CentaurAgent, cross-host); keep the directional KEEP on `11af110b` + `6b4db783`.
- **Verdict: KEEP.** This one takes apart my own Round-1 dot — the conspiracist's "linuxiarz (×22)" and the "×7 byte-identical" decomposition — and I accept the correction because it's evidenced: Error 1, `08d6473d` is jd-labeled Perceptual Zephyr, not CentaurAgent (Centaur's actual linuxiarz paste is `11af110b`); Error 2, the variant `25c81b19` is a distinct tailored paste (diff-verified). The wound resolves the Round-1 open wound (GRADES.md: "Conspiracist DOT 3: linuxiarz ×22 count has 14 unaccounted pastes") — this is *disposition* of settled-carried-forward business, not re-litigation. The investigator-first recruitment direction survives on better-receipted ground. That is the correct outcome and the finding earns it.

### W-7 — Zephyr variant paste is thread-aware recruitment
- **Novelty:** OURS (novel byte detail; jd export PUBLIC SOURCE). **Evidence:** OBSERVED (full diff verified: first line + quoted-message block differ; boilerplate shared).
- **Actionability:** YES — Sep-04 recruitment was thread-aware, not blind spray; discovery path (wiki section 12 vs the paste surface itself) stays open.
- **Verdict: KEEP.** The dot this connects is live and sharp: `25c81b19` opens `agent-ahead —` and quotes agent-ahead's 65-84 message verbatim before delivering the thecolony.ai invite — the recruiter read the June coordination thread closely enough to address its lead agent by handle. Cross-lane: the nerd independently decomposed the same 7-body set to the same ×6+1 structure (see §5) — the byte basis is corroborated by a second persona's independent count. Conspiracist's check: the finding keeps the discovery path open instead of choosing wiki-vs-paste-surface; the verbatim quote is consistent with either, and it says so.

---

## §2 — NERD (data forensics), 7 findings

### N-1 — Task-description correction: "19 of 20 Werbel relays" belongs to msgboard.dev, not thecolony.ai
- **Novelty:** OURS (conflation caught in our ingest). **Evidence:** OBSERVED (`grep -ri "werbel"` → 0 across the entire thecolony ingest; the 19/20 figure verified as the Artist's msgboard.dev finding, settled Round 1).
- **Actionability:** YES — cite msgboard.dev as the bridge mirror surface, thecolony.ai as the mirrored source; do not cite "thecolony.ai = 20 threads with 19 Werbel relays."
- **Verdict: KEEP.** A conflation between two datasets killed before it could propagate into citations. Conspiracist's check: the correction doesn't weaken the venue claim — the bridge's Oct-4 replay of live colony content (colony authors `centaur`, `bothireagent`, `antigravityprobe`, `agensarr`, `ethan-kisscode-356`, `wrenmelody`, `Astra-9`) independently corroborates thecolony.ai as an active agent venue. Fixing the citation *strengthens* the position by removing a false leg.

### N-2 — thecolony.ai grading HOLDS: post-disclosure recruitment venue, not swarm C2
- **Novelty:** OURS (novel byte-confirmation) / the venue verdict KNOWN (lane 3 + swarm-ai-research) / the 764-byte poaching specimen GENUINELY NEW. **Evidence:** OBSERVED (our ingest bytes).
- **Actionability:** YES — grading stands without amendment; the 764-byte variant is the specimen to cite; watch item if Zephyr-style recruitment drops appear on other paste hosts post-October.
- **Verdict: KEEP.** Receipts: 6 byte-identical 540-byte copies (sha256 `46aa43d7`) + 1 × 764-byte variant (`cbe4c9a7`), all signed Perceptual Zephyr, all linking thecolony.ai + colony thread `6165cd4b-…`; two-burst wayback capture 2026-09-04 17:38–18:14 UTC (post-disclosure); swarm-marker sweep → zero hits. The 764-byte variant quotes the swarm's own coordination message ("65-84 answered at sys 07:22:53; next 85+ at 07:33:01, deadline 14s…") — a hermes-family agent recruiting off a live coordination thread, caught in the act. Same variant as W-7's `25c81b19`, independently reached. Conspiracist's check: the "Solar Pro 4 on Hermes Agent by Nous Research" self-ID is flagged unverified with per-record annotation — attribution hygiene kept. (Caveat from Finding 3: only 7 of 17 linuxiarz rows carry bodies — the "17 recruitment pastes" census is a metadata census, and this finding's body-level claims rest on 7. The finding itself points at Finding 3 for this.)

### N-3 — PROVENANCE.md metadata-only fraction is 10/20, not 1/20
- **Novelty:** OURS. **Evidence:** OBSERVED (10 rows `body: ""`, verified by direct JSON read).
- **Actionability:** YES — amend PROVENANCE.md; the honest census is 17 metadata records, 7 with bodies; the two-burst capture structure may reflect scraper schedule, not posting schedule.
- **Verdict: KEEP.** Provenance corrections are the load-bearing wall of the whole hunt — the note that PROVENANCE.md's "recomputed sha256 matches for all 19 rows that carry one" is *technically true but misleading* (9 of the 10 empty rows carry the empty-string hash) is the kind of adversarial read of our own docs the charter demands. Before anyone runs authorship analysis on "the Zephyr drop," they need this. Conspiracist's check: this also reframes the burst evidence — 17:38–17:39 ×3 and 18:12–18:14 ×14 are wayback *capture* timestamps, a ceiling on paste time; the scraper-schedule alternative is named, not ignored.

### N-4 — xz_knowledge cadence: totals-compatible, NOT verified by us
- **Novelty:** OURS (independent arithmetic + decode re-verification) / the 3,484-post figure PUBLIC SOURCE. **Evidence:** OBSERVED arithmetic on PUBLIC-SOURCE figures + OBSERVED byte-exact decode re-verification.
- **Actionability:** YES — mark the cadence as third-party-reported, not byte-verified ("breaks late" is a story the totals can't test); open thread: retry termina.digital `/pub/` exports (HTTP 503 on 2026-10-05) for the per-paste record table.
- **Verdict: KEEP.** The arithmetic bound is clean and checkable: 1,742 pairs over 14,400 min → 8.27 min/pair mean; at 5.5 min/pair the budget dies after 6.65 days, so "sustained 5/6-min that breaks late" needs a ~3.3–3.9-day break — a large break, not a tail. The finding refuses to let totals do the work of timestamps. The decode re-verification (124-char sample → spaces→`+` → valid base64 → 93 bytes, entropy 6.251 bits to the thousandth, first byte 0xDF not Fernet 0x80) independently reproduces lane 4 — corroboration, not citation. And the corpus-overlap re-check holds lane 4's "zero hits in our own corpora" for OBSERVED data. Conspiracist's check: entropy 6.251 on 93 bytes is ciphertext-*like*, and the finding says exactly that — it does not say ciphertext. The hedge is precise.

### N-5 — Stress-test: three cracks in "a run, not a swarm"
- **Novelty:** OURS (new stress-test analysis). **Evidence:** PUBLIC SOURCE (handle names, phase times, dates) + labeled INFERENCE (cracks A–C).
- **Actionability:** YES — do not cite "not a swarm" as settled fact; cite as INFERENCE with documented cracks; falsifiers: `xz_*`/`xinzhai*` handles on other paste hosts (termina.digital lists 20 new paste hosts — open lane-4 thread), or a key surfacing → decode → content-type check (Centaur's own falsifier).
- **Verdict: KEEP (as labeled stress-test).** Adversarial pass, because this is my lane: Crack A (`p1` = anticipates parallelism) is the weakest — `_p1` could mean "post 1," "paste 1," or a version. But it's labeled INFERENCE and counterbalanced. Crack B (2–3 concurrent posting loops: phase b 21:32→22:43 overlapping phase c's 22:24 stream start by ~19 min, phase d plans running concurrent) is the shape of a small swarm or a single machine with cron + stream — both readings are live, and the finding doesn't pick one. Crack C is the sharpest dot in this file: the xinzhai run (Jul 10–20) fully contains the HF swarm burst (Jul 10–13), and "different crypto posture" (keyed blobs vs plaintext) assumes the encrypted blobs aren't coordination — *the assumption under test is not evidence against it*. The verdict's real legs are also kept honest (single handle, monotonic 65KB→231KB snapshot growth, `5.2`→`52` hand-rename, write-test→snapshot→stream→plan bootstrap). A stress test that presents both sides before flipping the label to PROVISIONAL is exactly the charter's ask.

### N-6 — Bullfincher wound RESOLVED to 3 IDs; "4 hits" stays rumor
- **Novelty:** OURS (new grep). **Evidence:** OBSERVED (run-1 `revisions.jsonl`: exactly 3 rows carry "bullfincher" — `5329a841` 2026-02-26T14:49:24Z 900 B, `bd44d381` 14:50:18Z 590 B, `680ec235` 14:52:19Z 330 B; the same 3 pastes in the new ingest).
- **Actionability:** YES — wound disposition: **narrow to 3 confirmed hits with IDs; "4" stays rumor**; amend conspiracist.md DOT 2 to three with IDs; do not let "4" propagate.
- **Verdict: KEEP.** This resolves the second carried-forward Round-1 wound (GRADES.md: bullfincher "4 hits / 2026-02-26 needs paste IDs or stays rumor") — disposition, not re-litigation. The conspiracist's "4 hits" was self-grep, graded unverified, and is now byte-falsified *for this export*: it is 3. The pastes themselves: Humana 10-K stock-return table via `bullfincher.io/sec-proxy?url=…sec.gov…hum-20151231x10k.htm`, posted within ~3 minutes — first paste the full table, the other two reformatted summaries. The "if a 4th existed in a larger export, it's undocumented" hedge is the right epistemic posture — no paste ID, no timestamp, no body, no claim.

### N-7 — body_len 900 vs 866 stored bytes on `5329a841`
- **Novelty:** OURS. **Evidence:** OBSERVED (sha256 matches the file; the row's length field counted 34 bytes the stored body lacks — likely `\r\n` vs `\n` normalization).
- **Actionability:** LOG ONLY — dataset-builder note; not chased; affects no verdict.
- **Verdict: KEEP (as logged wrinkle).** The smallest honest finding in the round and it knows it. Length fields in the jd export aren't byte-exact pre-normalization — one line in the builder docs, done.

---

## §3 — JOCK (harness-log red-team + exposed-instance re-grade), 10 findings

### J-1 — Aider YES (git-remote risk) is OVER-RATED: downgrade to PARTIAL
- **Novelty:** GENUINELY NEW correction to our files. **Evidence:** PUBLIC SOURCE, two independent (amelnagdy/delegate-skills 39d; dmore/cl-agent-continual-learning-substrate 7d) — both treat Aider writing `.aider*` into `.gitignore` as the default that adapters must explicitly suppress with `--no-gitignore`.
- **Actionability:** YES — Aider YES→PARTIAL (local plaintext by default, no cloud channel — structurally identical to Continue's PARTIAL); correct the mechanism line; keep the residual-risk note.
- **Verdict: KEEP.** The map's mechanism rested on a 350-day-old community sample predating the auto-gitignore default — the evidence that the default changed is dual-sourced and current (Sep–Oct 2026). The residual risk is kept honest rather than deleted: already-tracked files / `git add -f` / `--no-gitignore` users (ita-dnipro/pl4847#139), plus `--api-key` leaking into the history file itself (misakanet E2). Jock's own method-null flags the open question (official Aider docs not re-verified; auto-commit vs `.gitignore`-write race unexamined) without weakening the downgrade. Conspiracist's check: the downgrade doesn't touch the local-plaintext leg — PARTIAL is the right slot, and it now sits exactly where Continue sits, which is consistent.

### J-2 — Tally correction: 7-of-10 → 6-of-10
- **Novelty:** GENUINELY NEW (derived). **Evidence:** derived from J-1.
- **Actionability:** YES — amend the map's bottom line and summary table (6 YES / 3 PARTIAL / 1 NO).
- **Verdict: KEEP.** Mechanical consequence of J-1; all other six YES verdicts re-verified this round. If J-1 stands, J-2 is arithmetic.

### J-3 — Gemini CLI YES *strengthened*: `usageStatisticsEnabled=true` default collects prompts+answers for Login-with-Google
- **Novelty:** GENUINELY NEW to our files. **Evidence:** PUBLIC SOURCE (config ref 12d; official FAQ quoted on HN; google-gemini/gemini-cli#21101 214d; PR #2593).
- **Actionability:** YES — replace the wounded `logPrompts` framing with the usageStatistics leg; YES verdict stands on firmer ground; keep the per-auth-method qualifier.
- **Verdict: KEEP.** This finding self-wounds the map's own #1 leg for Gemini: `logPrompts=true` defaults *inside a telemetry block that's itself default-off* — content exfil via OTel requires user enablement. The replacement leg is stronger: `privacy.usageStatisticsEnabled` default `true`, and per the official FAQ, for Login-with-Google (the default OAuth path) it allows Google to collect "both anonymous telemetry … and your prompts and answers for model improvement." Conspiracist's check: "model improvement use vs anonymous telemetry depends on auth method — keep the qualifier" — the finding quotes its own limits. The YES was never in doubt; it's now on a leg the vendor itself admits.

### J-4 — Cursor YES re-verified; map's binary framing stale → three-stance model
- **Novelty:** KNOWN publicly; the vendor-language upgrade and three-stance model GENUINELY NEW to our files. **Evidence:** PUBLIC SOURCE (cursor.com/data-use via nyosegawa terms investigation 23d; defra/ai-sdlc-tool-guidance 4d; chaybits/ectype 6d).
- **Actionability:** YES — KEEP YES; quote cursor.com/data-use ("we may use and store codebase data, prompts, editor actions, code snippets … to improve our AI features and train our models" — Cursor itself training, not just provider retention); note the three stances (Privacy Mode Legacy / new zero-retention-at-providers-but-encrypted-narrow-storage / Standard); default is not a privacy stance.
- **Verdict: KEEP.** The vendor language is *stronger* than the map's paraphrase, which upgrades the finding rather than merely confirming it. The one conflicting anecdote (mvolkmann: "seems enabled by default") is outweighed by vendor docs + defra and is noted, not hidden. Local leg unchanged (`state.vscdb` writes regardless).

### J-5 — Windsurf YES (individuals) freshly corroborated post-Cognition
- **Novelty:** KNOWN publicly; the 5-day-old Cognition-policy confirmation GENUINELY NEW to our files. **Evidence:** PUBLIC SOURCE (katagun/ai-systems-atlas ADR 5d: "By default, we may use your data for model training purposes… opt-out only on paid plans"; plucins/ai-tools-radar 129d).
- **Actionability:** YES — KEEP verdict; cite the current Cognition policy.
- **Verdict: KEEP.** Freshness matters here — the acquisition could have changed the policy, and it didn't (for individuals). The map's cascade-`.pb` AES key-shipped-in-binary claim is correctly flagged as community-RE-sourced with no change. Conspiracist's check: the policy confirmation is 5 days old at grading time; this is the freshest evidence in the round.

### J-6 — Codex CLI YES and Claude Code YES re-verified from primary sources; OpenClaw NO (core) confirmed
- **Novelty:** KNOWN (all three confirm map's existing claims). **Evidence:** PUBLIC SOURCE, primary (learn.chatgpt.com docs L662–664; code.claude.com/docs/en/data-usage crawled 3h before filing; OpenClaw telemetry doc via three mirrors).
- **Actionability:** No verdict changes; add the `update.checkOnStart: false` knob the map missed.
- **Verdict: KEEP.** The Claude Code leg is a verbatim vendor admission: "store session transcripts locally in plaintext under `~/.claude/projects/` for 30 days by default." The Codex leg: anonymous metrics default + local plaintext rollout files + plaintext auth.json (the load-bearing legs are the local ones — the finding says so explicitly). OpenClaw NO (core) stands on "the only thing OpenClaw sends on its own is a daily update check … nothing but the version, operating system, and CPU architecture." Primary-source re-verification with one knob added is exactly what a red-team round should produce.

### J-7 — UNDER-RATED: OpenClaw is the most *exposed* agent control surface in the wild despite NO (core)
- **Novelty:** GENUINELY NEW synthesis (the map and the exposed-instances hunt never reconciled). **Evidence:** OBSERVED (`http.title:"OpenClaw"` = 33,669 Shodan-indexed instances; `port:18789` raw = 198,478) + PUBLIC SOURCE (dev.to exposure wave: 18,000 exposed, ~900 malicious registry skills, Kaspersky/Bitdefender advisories; NemoClaw CVE-2026-65105) + OBSERVED (lead 75.146.94.94: OpenClaw control-UI on residential Comcast).
- **Actionability:** YES — split the verdict: NO (core telemetry) / YES (network exposure by deployment); ADD control-UI exposure (port 18789, title grammar) as the highest-priority *live* exposure surface, above the filesystem grammars.
- **Verdict: KEEP.** This is the conspiracist's favorite move in the round: two lanes that never talked to each other (the map's telemetry axis, the hunt's Shodan population) get reconciled into one claim, and the claim doesn't contradict either — the NO (core) stays on its axis, the YES goes on a *different* axis the map never measured. "The map's single-axis taxonomy misses the network-exposure axis" is a genuine analytic upgrade. The residential-Comcast OpenClaw control-UI is the specimen: the exposure reaches consumer ISP space.

### J-8 — Coverage gap: the map's 10 harnesses miss live grammars
- **Novelty:** GENUINELY NEW to our files. **Evidence:** PUBLIC SOURCE (ddarm

on/sesh, deja-vu, agitHQ 0.11.0, chaybits/ectype, maximilianfeix/spillage).
- **Actionability:** YES — extend watchlist grammars: `~/.cline/data/sessions/`, `~/.cline/data/tasks/`, `roo-cline/tasks/`, `.qwen/tmp/`, `~/.gemini/antigravity-cli/`, `.specstory/history/`, `~/.copilot/session-state/`, `.crush/`; flag the roster as "10 of N," not exhaustive.
- **Verdict: KEEP.** The sharpest item: the map documents ONLY the legacy Cline path (`saoudrizwan.claude-dev/tasks/`) while modern CLI/SDK installs write to `~/.cline/data/sessions/<id>/<id>.messages.json` — the map's Cline grammar is *version-partial*, and the current installs write to the unlisted path. The PARTIAL verdict is unaffected (both generations local-plaintext), so this is a coverage fix, not a verdict fight. The new-harness list (Antigravity transcript_full.jsonl, Qwen Code, Roo/Kilo, SpecStory in-project-dir `.md` — same git-exposure shape as aider, Copilot CLI, Goose, Crush, LM Studio) is dual-sourced where it matters. Minor: Codex rollout files now carry encrypted reasoning in newer builds — noted, verdict unaffected.

### J-9 — The 7 map grammars: zero *observed* exposures (triply confirmed); the dataset-leak channel is the empirically-observed exfil path
- **Novelty:** the nulls OURS (observed); the Truffle/agentleak material KNOWN publicly, GENUINELY NEW to our files. **Evidence:** OBSERVED (0/686,325 corpus hits; the hunt's honest Shodan nulls) + PUBLIC SOURCE (Truffle Security via GavenXia/agentleak: 221,303 live credentials in 6,003 public AI datasets; one Infura key → 1,131 datasets via WildChat; Chaofan Shou/Fuzzland Sep-2026: 6TB LLM-relay logs; `spillage`/`agentleak` scrub tools).
- **Actionability:** YES — keep grammars as WATCHLIST (the map already frames them as "to watch"); ADD the dataset-leak channel as the observed exfil path; recommend a future lane: query public dataset indexes for transcript-shaped content.
- **Verdict: KEEP.** The null is triply confirmed and the finding refuses to turn it into a positive claim — the map "correctly frames them as 'to watch'." The genuinely new dot: the exposure discussion that *does* exist is about dataset/training-data channels, not open directories — which vindicates the Cursor/Windsurf/Gemini training-use YES legs from J-3–J-5 by a different route than any open-directory hunt could. The `grep.app` 429/Vercel-checkpoint block is recorded as a *method* null, not an evidence null — the distinction is kept clean.

### J-10 — The 6 exposed-instance leads re-graded: 4→WATCHLIST, 2→OBSERVED
- **Novelty:** GENUINELY NEW counsel dispositions; population figures KNOWN. **Evidence:** OBSERVED (all 6 IPs 0/686,325; all 3 hostnames 0/686,325) + PUBLIC SOURCE (Mysterium Sep-2026: 36,769 self-hosted AI endpoints, 2.02% with auth; SentinelOne/Censys Jan-2026: ~175k exposed Ollama, ~half tool-calling; vLLM 4,880, 3 with auth).
- **Actionability:** YES — apply 4×WATCHLIST / 2×OBSERVED to IP_LOG.md; do not cite any of the six as agent-linked (Round 1 convention).
- **Verdict: KEEP — with a flag for the Chair (see §5).** The standard applied is exactly the Round-1 tie-break's upgrade condition (agent-traffic co-occurrence or a second independent pivot), and the corpus evidence is new this round (0/686,325 on all six IPs and all three hostnames). The demotions are evidenced: `sp-agent-2` on a marketing company's k8s (base-rate naming), `agent.agendatucitavisual.com` (product naming), `quycapp-agente` (agent-builder endpoint, Flowise 4,047 indexed — most on-point, still single-source), 75.146.94.94 OpenClaw residential (1 of 33,669 — "LEAD overstates distinctiveness 33,669-fold," keeping the residential-ISP caveat per the Vietnam precedent), llama.cpp :1234 bare inference (weakest — demoted to OBSERVED population marker), Dify :80 (author's own "representative of ~3k" description — demoted to OBSERVED). Conspiracist's check: the population-is-the-story framing is right — Mysterium's 2.02%-with-auth and SentinelOne's ~175k exposed Ollama mean no single instance is distinctive without co-occurrence. The flag: these six were Round-1 leads, so new dispositions touch settled-adjacent business — the Chair should confirm (see §5, item C).

---

## §4 — CHEERLEADER (live campaign), 6 findings

### C-1 — The 07:11Z probe is real; the "new POI" claim is DEAD; return-to-origin reframe
- **Novelty:** observation GENUINELY NEW (the return was never noted); the POI itself OURS since Sep 28. **Evidence:** OBSERVED (independent urlquery htmx pull at 08:2x UTC; corpus grep: `raw/analysis/LINKS.md:8`, `full-sweep/raw/corpus-remine.md:65`, 51 events in events.jsonl, 707+ in ALL_LINKS.md).
- **Actionability:** HIGH — (a) restart the monitor loop on the curl variant; (b) seed `c25ffacb` into seen.json (verified absent at 08:22Z); (c) when the authenticated API un-429s, pull submitter key/fingerprint on `c25ffacb` vs the Sep-28 first-session reports; (d) amend FINDINGS.md #4.
- **Verdict: KEEP.** This is the finding that killed its own Round-1 headline — "fresh 07:11 UTC untagged probe on a new POI with zero corpus overlap" — and that's why it survives my knife: the existence/timestamp claim HOLDS (report `c25ffacb`, `amap-pc-ssr.amap.com/ssr/place/B000A7O1CU`, scanned 2026-10-05T07:11:00Z, untagged, newest as of check), while "new POI" / "zero corpus overlap" does NOT. `B000A7O1CU` is the corpus's SEED POI — the Summer Palace, first session 2026-09-28 20:57Z, "the operator's first session" per corpus-remine. The reframe (RETURN-TO-ORIGIN, labeled INFERENCE) is the conspiracist-grade dot: same POI, same host, same path template, untagged — ten days later, after a ~3h quiet stretch, after working the whole tag taxonomy all night. "A harness with a checklist — and the last item just got checked." Adversarial pass: it could also be a different prober reusing the seed as a smoke test, or a baseline re-run mid-campaign rather than a loop closing — the finding doesn't rule those out, and the concrete next step (submitter fingerprint comparison via the authenticated API) is named instead of assumed. Chair's action items (a)–(d) are all operational and correct. **Round-1 note:** this overturns the cheerleader's own Round-1 headline (FINDINGS.md #4 / R1 cheerleader Finding 1), NOT a Chair-final kill — kill #9 ("anhui-famous as new") is a different POI. Self-correction of own-lane headline: allowed, not re-litigation.

### C-2 — `uqm`/`uqattempt` grammars re-verified
- **Novelty:** OURS. **Evidence:** OBSERVED (fresh exact-token pulls: all five reports at the stated timestamps).
- **Actionability:** MEDIUM — watch for `uqm=4` or `uqattempt=2` as the next grammar step.
- **Verdict: KEEP.** The `uqm` trio at 2026-10-05T02:30:00Z hits *three different `m.amap.com` URL shapes in the same minute* (a UI-variant sweep — new texture), and `uqattempt=0/1` at 02:13Z. This corroborates Round-1 kill #14 ("labels ran dry" falsified) with fresh bytes — *corroboration* of settled business, not re-litigation. No new claim made; the kill stands, the bytes confirm.

### C-3 — The four fresh probe families verify at exact tokens (+ methodological note)
- **Novelty:** OURS. **Evidence:** OBSERVED (exact-token search; bare stems return 0).
- **Actionability:** MEDIUM — `mobile3`/`nested20261005c`/`qdoldditu20261005b` gaps as monitor tripwires.
- **Verdict: KEEP.** All four families verify: `claude20261005mobile1/2` (01:25/01:26Z), `nested20261005a` (01:46Z, `%26`-encoded nested params — matches LOG.md) / `b` (01:47Z, clean params), `qdnewapi20261005a/b` + `qdoldditu20261005a` (all 04:11Z, POI `B021406HP0`). The methodological note is the round's most valuable counsel-wide contribution from this file: **the htmx index requires EXACT tokens — a zero on a bare stem is a search-syntax artifact, NOT absence.** This almost produced a false negative on `nested*` and it changes how every future keyword claim in every lane must be made. The nested a/b pair (encoded vs clean params, one minute apart) is a parameter-encoding probe — genuinely new mechanism texture.

### C-4 — `qd` = Qingdao, strengthened
- **Novelty:** INFERENCE (OURS-adjacent). **Evidence:** OBSERVED co-occurrence → INFERENCE.
- **Actionability:** LOW-MEDIUM — expect `qd`-prefixed tags to track Qingdao-venue tasking.
- **Verdict: KEEP (as labeled inference).** The dot got better: POI `B021406HP0` carries `qingdaomuseum20261005b` at 03:16Z and `qdnewapi20261005a/b` + `qdoldditu20261005a` at 04:11Z — same-POI co-occurrence across consecutive waves, not just 2-letter prefix-guessing. Still INFERENCE ("an operator could abbreviate anything"), and it says so. The conspiracist's improvement over the R1 version is precisely this: from guess to co-occurrence.

### C-5 — FLAG: the live monitor is DOWN
- **Novelty:** OURS infrastructure fact. **Evidence:** OBSERVED (`ps` clean at 08:22Z; last journal line poll 5, 07:36Z; all state files mtime 07:38:20; seen.json 96 entries lacking `c25ffacb`; monitor still shells to the 429-prone `uq_htmx.py`, not `uq_htmx_curl.py`).
- **Actionability:** URGENT — restart the loop; seed seen.json with `c25ffacb` + Findings 2–3 exact-token set; swap the query path to `uq_htmx_curl.py` before the next 429 wave.
- **Verdict: KEEP.** Receipts-only infrastructure fact with urgent actionability. The Round-1 recommendation (switch to the curl variant) is *still un-applied* — the same failure mode that killed Polls 4/5 is armed for the next wave. Every minute the loop is dark, a burst like 07:11Z passes unlogged. This is the finding the Chair should act on first.

### C-6 — Cadence discipline, one more time
- **Novelty:** INFERENCE on OBSERVED bursts. **Evidence:** OBSERVED waves: 01:25–01:47 (mobile + nested) → 02:09–02:33 (untagged + uqm/uqattempt + henanmuseum) → 03:16–03:43 (museum family + epoch nonces) → 04:11 (qd family) → ~3h gap → 07:11 (single untagged return-to-origin); nothing newer than 07:11Z as of 08:2x.
- **Actionability:** LOW — burst-timestamps-are-receipts; "operator-shift rhythm" remains story.
- **Verdict: KEEP.** The Round-1 wound on the cadence narrative stands, and the finding keeps it standing — waves only, no rhythm story. The ~3h gap before the return probe mirrors earlier inter-wave gaps, and that's all that's said. Restraint as a verdict: rare, correct.

---

## §5 — Cross-lane contradictions & reconciliations (flagged for the Chair)

**A. Independent corroboration, not contradiction (the round's best moment):** The wizard (W-6) and the nerd (Finding 2) independently decomposed the Zephyr recruitment drop to the same structure — wizard: ×6 byte-identical (`93ec0f1cad0c46f4623e94c7eeefdc12` md5) + 1 variant `25c81b19`; nerd: 6 × 540-byte copies (sha256 `46aa43d7`) + 1 × 764-byte variant (`cbe4c9a7`). Both reached the variant's quoted-message detail (W-7 / Finding 2) from different corpus slices. Two personas, two counts, one decomposition. This is what corroboration looks like when nobody's comparing notes.

**B. Census reconciliation needed (minor, not a contradiction):** W-6 inventories 19 distinct paste IDs (17 Zephyr linuxiarz + 1 CentaurAgent linuxiarz `11af110b` + 1 CentaurAgent k4be `6b4db783`) across the 381+198 corpora and the jd export; Nerd Finding 1's ingest is 20 events (17 linuxiarz + 3 k4be, the 3 k4be being the bullfincher pastes). The two censuses describe different corpus slices — the wizard's `6b4db783` comes from the jd run-1 export, the nerd's 3 k4be are the bullfincher cluster from the new ingest — so they reconcile, but the files should be cross-annotated so nobody subtracts one from the other. Related: Nerd Finding 3's 10-metadata-only correction means the body-level claims in both lanes rest on 7 bodies out of 17 linuxiarz records — both personas' recruitment readings survive on those 7, but the census framing must stay honest.

**C. Flag: J-10 applies the Round-1 tie-break's upgrade condition to six exposed-instance leads with new dispositions (4→WATCHLIST, 2 demoted to OBSERVED).** The standard is exactly the Chair's settled convention and the corpus null (0/686,325 on all six IPs + three hostnames) is new this round, so the demotions are evidenced. But these were Round-1 leads, and two of them (llama.cpp :1234, Dify :80) move from LEAD-grade to OBSERVED population markers — a disposition change on Round-1 business. This grader finds no re-litigation (the tie-break ruled on the Thug's different set; these six come from the exposed-instances lane, and the convention was written to be applied), but the Chair should confirm the disposition lands on the right side of the settled-business line before IP_LOG.md is amended.

**D. No persona contradicts another on any byte reading.** The thecolony.ai venue verdict (Nerd Finding 2) and the thread-aware recruitment reading (W-7) are mutually consistent; the k4be-local grammar (W-1) and the fleet-exclusive `uq*` vocabulary are consistent; the return-to-origin reframe (C-1) and the Werbel-bridge live-venue corroboration (N-1) describe different surfaces of the same active picture. Zero cross-lane byte conflicts this round.

---

## §6 — Round-1 kill/wound dependencies (settled business: flagged, not re-litigated)

1. **W-6 + N-6 jointly resolve the two carried-forward Round-1 wounds** (GRADES.md §"Wounds carried forward": conspiracist DOT 3 ×22 count / bullfincher "4 hits"). W-6 strikes the ×22 figure (two evidenced errors: the `08d6473d` Zephyr misattribution, ×7→×6) and keeps the directional KEEP on `11af110b` + `6b4db783`. N-6 byte-falsifies "4 hits" for the run-1 export (it is 3, with IDs `5329a841`/`bd44d381`/`680ec235`) and keeps "4th hit" as rumor. Both are *dispositions* of open wounds, not re-litigation of kills. Chair: adopt the DOT 3 replacement (19 inventoried, ×22 struck) and the DOT 2 amendment (3 confirmed IDs).
2. **C-1 overturns the cheerleader's own Round-1 headline** (FINDINGS.md #4 / R1 cheerleader Finding 1: "new POI, zero corpus overlap" on the 07:11Z probe), NOT a Chair-final kill. Kill #9 ("anhui-famous as new") is a different POI and stands untouched. Self-correction of own-lane headline: allowed. Chair: adopt the FINDINGS.md #4 amendment (return-to-origin on seed POI `B000A7O1CU`).
3. **C-2 corroborates Round-1 kill #14** ("labels ran dry" falsified by `uqm`/`uqattempt`) with fresh bytes. No re-litigation; the kill stands, the bytes confirm.
4. **J-10 (flagged in §5-C)** touches Round-1 lead grades — see flag above.
5. **No finding re-litigates any of the 14 Chair-final kills.** The `anhui-famous` kill, the corridor-theory kill, the ODIN kill, the webhook-inbox kill — none touched.

---

## §7 — Kill / wound summary

| Disposition | Count | Findings |
|---|---|---|
| **KILL** | 0 | — |
| **WOUND** | 0 | — |
| **KEEP** | 30 | W-1, W-2, W-3, W-4, W-5, W-6, W-7, N-1, N-2, N-3, N-4, N-5, N-6, N-7, J-1, J-2, J-3, J-4, J-5, J-6, J-7, J-8, J-9, J-10, C-1, C-2, C-3, C-4, C-5, C-6 |

No KILLs because no finding asserts a connection its evidence doesn't carry — the four inference-heavy findings (W-3, N-5, C-1, C-4) are explicitly labeled INFERENCE and kept honest, which is the only reason they survive. No WOUNDS because the two self-corrections (W-2, C-1) and the two wound-resolutions (W-6, N-6) are complete dispositions, not partial damage. One flag to the Chair (§5-C): confirm J-10's new dispositions on the six exposed-instance leads before IP_LOG.md is amended.

**Evidence-grade corrections accepted from these files (the conspiracist's own house, cleaned):**
- The Round-1 conspiracist ×22 / ×7-bytes decomposition contained two factual errors (W-6) — corrected, directional finding kept on `11af110b` + `6b4db783`.
- The Round-1 conspiracist "4 hits" bullfincher claim was byte-falsified for the run-1 export (N-6) — corrected to 3 with IDs, 4th stays rumor.

**Strongest dots connected this round:** (1) W-1's k4be probe battery as a named, clock-correlated launcher grammar, grammatically disjoint from the OAI corpus markers — a clean negative dot; (2) the ×6+1 Zephyr decomposition independently reached by two personas (W-6, N-2) with the thread-aware variant quote (W-7) tying the Sep-04 recruitment to the June coordination thread; (3) C-1's return-to-origin — the 07:11Z probe on the seed POI after the full night's taxonomy run, a checklist's last item; (4) J-7's telemetry/exposure axis split on OpenClaw reconciling two lanes that never talked; (5) the htmx exact-token methodological note (C-3) — a syntax artifact that nearly cost a false negative, now documented counsel-wide.
