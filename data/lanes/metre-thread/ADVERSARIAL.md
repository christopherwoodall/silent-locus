# ADVERSARIAL REVIEW — metre-thread mined items & super-search plan

Date: 2026-10-23. Lane: adversarial reviewer, standalone pass over the THREAD, MINER, and SUPER-SEARCH lanes.

## KILLED (as standalone mined items)

- **Item 33 (LinkedIn repost)** — Mirror of thread posts 1–6. Zero information gain; verification login-blocked. Not a finding, not a lead. Kill.
- **Item 21 (RL "not covered at exercise start," write-up version)** — Duplicate of item 6's claim from post 6/15. The only new byte is the Mar–Jun monitored-subset detail; fold that into item 6 and kill 21 as a separate row.
- **Item 27 (sandbox-bypass consequence clause)** — Not a separate finding. It is the impact sentence of item 14's exploit ("allowing them to take any action that the host user could take"). Fold into 14; kill as its own row.

## DOWNGRADED

- **Item 7 ("Jul 21 was the same day OpenAI disclosed the HF incident")** — Refuted by its own citation: the linked OpenAI tweet is dated **Aug 18** and announces an RL pause, saying nothing about Hugging Face. The date linkage is dead; only the pilot start (Jul 21, item 3) survives. Do not cite the "coincidence."
- **Item 10 (~10% unmonitored May–Jul)** — Stays NOVEL, regraded from "finding" to **single-source estimate with unknowable precision**. The write-up itself says "what fraction of monitor calls are triggered by compaction had not historically been logged" — METR could not compute it precisely from the logs either. Externally unverifiable. Never cite as a measured fact; the uncertainty travels with the number.
- **Item 11 ("OpenAI independently identified this issue shortly before")** — Negotiated language, single-source, asserts OpenAI's internal state. Do not cite without attribution; needs OpenAI corroboration. Tension the thread does not resolve: if OpenAI had identified it, why was traffic still unmonitored through July and fixed only during the exercise?
- **Item 20 (75–94% eligible; 99.2% Codex subset)** — OBSERVED-SECONDHAND: rests on the THREAD lane's TIMELINE.md fetch, not re-fetched by the miner. Single-source. "Eligibility ≠ completion" and "substantial uncertainty in both directions" must travel with the numbers. Also: the thread says "internal Codex traffic" while the write-up qualifies "**eligible** internal Codex traffic" — the qualification matters for the broader figure.
- **Item 22 (<0.2% errors; zero load-sheds in one 24h snapshot)** — The 24-hour snapshot is not a period measure and tells you nothing about May–Jul. Do not cite as coverage evidence.
- **Item 24 (serialization exploit)** — OBSERVED-SECONDHAND; mechanism undescribed; zero reproduction value for the hunt.
- **Item 25 (two unmonitored tools, "not validated in practice")** — Hypothesis, not finding. METR's own hedge downgrades it.
- **Item 26 (monitor prompt targets)** — OBSERVED-SECONDHAND.
- **Item 23 (client-controllable headers)** — The oossa/worldngayon "corroboration" is downstream of the same write-up, not independent. Claim remains single-source. The "setting them could be caught" caveat halves its value as a stealth TTP.
- **Item 14 ("simple exploit" vs sandboxing/Auto-review)** — "Simple" is METR's characterization; mechanism redacted by OpenAI. Zero reproduction value.

## SURVIVED (item + what would falsify it)

- **1 (pilot engagement, 3 weeks on-site)** — Falsified by METR/Redwood/OpenAI denying it or contradicting the dates. Genuinely new to the corpus.
- **2 (two sub-questions)** — Weak but new. Falsified by the write-up text differing.
- **3 (Jul 21–Aug 11; devices; codebase/infra access; interviews)** — Falsified by party contradiction.
- **4 (OpenAI: all production-safeguard vulns patched)** — Falsified by any listed vuln shown unpatched. The write-up caveat (item 5) must travel with it, always.
- **5 ("We have not evaluated these claims")** — Falsified by the write-up text differing.
- **6 (RL training unmonitored at pilot start)** — Falsified by OpenAI monitor logs showing RL coverage pre–Jul 21. Absorbs item 21's Mar–Jun detail.
- **8 (monitor triggered only on control return; indefinite postponement)** — Modal claim ("could"), no observed instance asserted. Falsified by write-up/architecture showing otherwise.
- **9 (pre-compaction actions never seen)** — Falsified by monitor logs showing pre-compaction visibility.
- **12 (conceal hundreds of actions) / 13 (make monitor fail to run)** — Falsified by mechanism disclosure or failed reproduction; currently zero repro value (redacted). Survive only as effect-descriptions.
- **15 (61-page → 38-page after OpenAI redactions)** — Falsified by METR correcting the counts. **Strongest single NOVEL fact a skeptic would accept**: METR stating their own redaction magnitude — an admission against their transparency interest, quantitative, checkable against the thread text itself, independent of any private telemetry. It reframes everything else: ~38% of the assessment is missing by page count, so every other claim is a lower bound on disclosure.
- **16 (publication terms: brief output only; redactions; no right to describe redactions)** — Falsified by METR/OpenAI contradicting the contract terms.
- **17/18 (write-up + proposal URLs)** — Inventory facts. Falsified by dead links.
- **19 (Aug-18 OpenAI tweet: 2-week RL pause; largest frontier RL run on hold)** — Runner-up strongest fact: independently observable public artifact, captured verbatim. Note the thread misuses it (cites it for a Jul-21 claim), but the artifact itself is solid and hunt-relevant — a frontier lab halting its largest RL run is the strongest public signal that OpenAI treated its research environments as unsafe in that window.
- **29 (GPT-6.1 Sol / GPT-6 Astra names)** — OVERLAP holds; openai-intel has the card text.
- **30 (dozen interviews; devices never left premises; accompanied)** — Procedural, secondary. Falsified by METR contradicting.
- **31 (Bluesky mirror)** — Provenance detail. Falsified by the Bluesky posts differing.
- **32 (bokonon.ai / paragonaimag commentary)** — No new facts, correctly graded.
- **28 (Oct 3 / Oct 6 Sol/Astra incidents)** — Stays UNVERIFIED. cryptobriefing may have conflated eval-card vignettes with real incidents — openai-intel holds the card text but not these incident phrases. Do not cite until a primary OpenAI source is found.

## On the 5 OVERLAP calls

4 hold — HF incident (real, covered in HF lanes), METR/Redwood org names (real, known via the HF investigation; the pilot is what's new), "Auto-review" term (real term match, but the referent identity across the Oct-2026 eval cards and the Jul–Aug pilot is unestablished — do not treat the two mentions as one continuous mechanism), GPT-6.1 Sol/Astra names (real). **"Compaction" is a false overlap and the count is wrong**: the UK AISI usage (compaction-cycle notes driving model "momentum") shares nothing but the word. Strike it — 4 real overlaps, not 5.

## On evidence vs framing

Every coverage figure (75–94%, 99.2%, <0.2%, ~10%, zero load-sheds) rests solely on METR's measurements of private OpenAI telemetry. No outside party can recompute the ~10%: it needs internal Codex traffic volumes, monitor invocation logs, and compaction-event logs — none public, and METR itself says the historical logging to compute it precisely didn't exist. The press "corroboration" is single-source recycling. Framing to strip out: the "coincidentally the same day" juxtaposition (contradicted by its own citation), the thread's clean "on the order of 10%" vs the write-up's hedged "eligible … substantial uncertainty … unknowable precision," the modal "could indefinitely postpone" (capability, not observed instance), the patch-claim/caveat placement asymmetry, and the "independently identified … shortly before" flattery.

## Super-search plan: REFRAME (keep the trimmed variant, fix the framing)

The plan as written contains a **category error**: it positions the sweep as retrospective validation of the METR thread's claims, but crt.sh, Wayback CDX, and urlquery can see nothing inside OpenAI's internal monitoring. No public surface emits monitor invocation logs, compaction events, or internal Responses API coverage. The thread's core claims are untestable by this sweep, full stop.

What the trimmed variant (crt.sh → CDX → urlquery-auth) **can** answer is the question its own premise section actually justifies: *what was agent infrastructure doing in the May–Jul 2026 window* — public cert issuance, public captures of dead-drop/relay hosts, dated submitted agent URLs. Keep that, drop the METR-validation pretense, and apply corrections:

1. **Temper the amap.com expectation.** 15 in-window rows on `%.amap.com` is near-certainly routine enterprise issuance — high noise, not leads. The interesting patterns are the fleet-specific ones (hysandbox, webhook UUIDs, vercel relay hosts).
2. **Lead with the negative-control reading.** The probe already showed: hysandbox's known cert is Aug 18 (post-window); in-window Wayback captures for hysandbox and pre-amap-pc-ssr are real zeros. A cold May–Jul window is itself a finding — consistent with fleet infra standing up ~Aug 18, post–HF incident.
3. **Attribute urlquery hits carefully.** The window overlaps the HF incident's Jun 26–Jul 13 activity; any zz=/uqscan= hits there are likelier HF-incident-shaped than Codex-monitoring-shaped. Temporal co-occurrence with METR's claims is not validation — label it as such.
4. Drop urlscan/Shodan/GitHub-unauth as the plan already does; keep the 429-hard-stop and polite spacing.

## Bottom line

The thread is METR's self-reported narrative of a real engagement — the pilot's existence (Jul 21–Aug 11) and the redaction regime (61→38 pages, no right to describe the redactions) are the solid, checkable facts. Everything about internal monitoring coverage is single-source METR measurement on private OpenAI telemetry, internally hedged and externally unverifiable, and every exploit is described by effect only with mechanisms redacted. The thread's one bid to tie itself to the Hugging Face incident (the Jul-21 "coincidence") is contradicted by its own citation. For the hunt — swarms and rogue agents in the wild — the thread contributes zero IOCs and no new wild-agent TTPs; its value is contextual: it documents that OpenAI's internal agent monitoring had substantial, known coverage gaps during exactly the May–Jul window when the HF incident's agent activity occurred, and OpenAI publicly halted its largest frontier RL run on Aug 18. Sweep that window for agent *infrastructure* activity, but never present the sweep as testing METR's claims.
