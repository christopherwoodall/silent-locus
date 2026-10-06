# COUNSEL — Round 2 — WIZARD (pattern mage) findings

*Chair: Hunter S. Thompson. Lane: K4be/linuxiarz deep dive, lanes 1–2. Filed 2026-10-05.*
*Method: re-derived every count from the raw bodies/manifests on disk; no re-litigation of Round 1's 14 kills.*
*Evidence grades: OBSERVED (our bytes) / PUBLIC SOURCE (cited) / INFERENCE (labeled).*
*Novelty: OURS (in our corpora) / KNOWN (publicly documented elsewhere) / GENUINELY NEW.*

---

## W-1 — The K4be grammar family IS a launcher fingerprint — of a k4be-local probe harness, not the shared OAI toolkit

**Claim:** PAD\d+x\d+ ×70, TEL\d{6,} ×17, TK\d{5,} ×6, CLICKMAYBE ×17, URLMARK ×1, FRAMEK4 ×2 (+ URLTEST/ANCHORTEST/linktry/GOR/jqp-ladder) is one launcher's single-day probe battery with clock-correlated paste IDs. It does NOT collide with the Chinese-swarm grammar families (zz=/uqscan/oai).

**Evidence (OBSERVED, re-derived from raw bodies + manifest):**
- Title counts verified: PAD 70, TEL 17, TK 6 (title-prefix match), URLTEST 3, ANCHORTEST 3, Ghtml/Gmarkdown/Gurl ladder, linktry 1, REPLYURL 1, GOR 1. Body counts: CLICKMAYBE 17, URLMARK 1, FRAMEK4 2, LANGURL 1 — all match the taxonomy.
- PAD series: indices 0–69 strictly sequential, epochs 1779101038→1779101262 (2026-05-18 10:43:58→10:47:42 UTC, 224s, ~3.2s cadence), title index == body index in all 70 (verified pairwise). Body form `pad-<unix>.<fraction>-<idx>`.
- TK/TEL titles are clock-derived: `TK084908` ↔ body epoch 1779084908 (suffix = epoch[-6:], verified); `TEL094601` ↔ 1779094601. Same for all sampled.
- TEL series: 17 pastes, ONE fixed link target (`https://telegra.ph/Test-Link-88990-05-18`), epochs spanning 463s (~27s cadence), body form `<url> CLICKMAYBE <epoch>` — a click-probe series: same link reposted with fresh epochs, "MAYBE" = testing whether/when the link gets fetched.
- TK084908 body: `https://api.microlink.io/?url=test URLMARK1779084908`; TK084859/086844 bodies: `FRAMEK4<epoch>`; TK085846: `https://example.com/LANGURL<epoch>`. The battery walks a capability ladder: pad/sequence → click-track → URL-mark → frame-embed → language-URL → anchor-render → fetch-proxy ladder (jqp.vercel/md.succ.ai/pure.md, May-28 wave).
- Collision check (OBSERVED): `zz=` 0, `uqscan` 0, `oai` 0, `jina` 0, `ts=` 0, `terminal_epoch` 0, `scaffold` 0 across all 198 k4be bodies. The cross-swarm-vocab hunt independently established fleet-exclusive vocabularies (fleet `uq*` grammar: 1,220 urlquery hits, zero outside Amap).

**Classification:** GENUINELY NEW as a documented launcher grammar (bytes are PUBLIC SOURCE via the joshuadavid export; the grammar analysis is OURS).
**Actionability:** Adopt as named grammar `k4be-probe-battery`. Watch for its reappearance on other paste hosts — a fresh PAD/TEL/TK series = the same prober re-testing. Do NOT cite as OAI-toolkit; the launcher is k4be-local and grammatically disjoint from the June/OAI corpus markers.

---

## W-2 — CORRECTION: the taxonomy's `pad-<epoch>-<n>` honest negative is wrong

**Claim:** GRAMMAR_TAXONOMY.md §E lists `pad-<epoch>-<n>` as "0 across 579 rows." The bytes say otherwise: 70 k4be bodies match `pad-<unix>.<fraction>-<idx>` (e.g. `pad-1779101038.5110793-0`).

**Evidence (OBSERVED):** case-insensitive grep `pad-` → 70 hits in `data/2025-10-24-pastebin-k4be/raw/`, all of the PAD-title series. The battery pattern was evidently narrower than the real grammar (the microsecond fraction `.5110793` breaks a `pad-\d{10}-\d+`-shaped pattern). The §B linuxiarz-only negative (0 in 381 rows) remains true; the §E cross-corpus claim does not.

**Classification:** OURS (correction to our own document).
**Actionability:** Amend GRAMMAR_TAXONOMY.md §E: `pad-<epoch>.<frac>-<idx>` ×70 (k4be only). This correction strengthens W-1 — title↔body index correlation makes the launcher case tighter, not looser.

---

## W-3 — Two ID schemes inside one campaign: clock-derived (TK/TEL) vs random (PAD) — INFERENCE, harness behavior

**Claim:** The same 2026-05-18 campaign uses clock-derived correlation IDs for the click/mark probes (title suffix = epoch[-6:]) and unique random 6-digit tokens for the PAD sequence probes (70 unique suffixes, none equal to epoch[-6:]). Two schemes, one day, one host = one prober running two probe types, not copy-paste.

**Evidence:** OBSERVED counts above; the dual-scheme reading is INFERENCE (labeled).
**Classification:** GENUINELY NEW (our analysis).
**Actionability:** Low; file as a harness-behavior note. If a future series mixes both schemes again, it corroborates same-launcher.

---

## W-4 — Iowa eval-shape stress test: "strong circumstantial, no named eval claimable" SURVIVES

**Claim:** Nothing in the bytes gets the June-16 scene from "walks like an eval" to a named, claimable eval. The report's wording stands.

**What would make it claimable, and where each bar stands:**
1. **Benchmark item text in a public release matching the exact Q5 prompt** — searched the web for `"Now, do the same for 85 and older"` + thyroid benchmark: hits are ONLY the joshuadavid investigation corpus. No public benchmark, HF dataset, or GitHub eval matches. Bar not met.
2. **A run ID, harness name, or provider marker in any paste** — absent. Re-verified: zero `oai`/`zz` tokens in the paste comms layer (clean negative stands); "scaffold" is descriptive, not a proper noun. Bar not met.
3. **Asymmetric Security's fuller writeup naming the eval** — their 2026-09-28 report is still preliminary and contact-gated; it lists the org (IDPH thyroid) but attributes to no eval. Bar not met, still the best-placed source.
4. **The June-16 wiki-activity bridge** (dse `GrocerySequenceAgentApr27` collab, 10:28–10:33 UTC) — jd's body-marker search across 11 wiki exports for Iowa/38b5 markers returned zero. Bar not met.

**Strongest pro-eval bytes (why "strong circumstantial" is earned):** literal `benchmark clock` / "benchmark task"; 10–16s per-question deadlines; tool-vanish-at-close belief driving the sacrifice protocol; exact-prompt mirroring for exact-match grading; parametrized 5-question template (one age group per round); heterogeneous cadences (9m54, 10m02, 15m42s, "16 sec") = staggered cohorts, the classic multi-wave eval launch shape.

**Honest gap, amplified:** jd's own follow-up (research/swarm-followup/linuxiarz.md) notes the bytes "do not establish training rather than evaluation" — even the eval-vs-training distinction is unresolved, and no paste carries any reward signal. The report should keep both hedges.

**Classification:** OURS (the stress test) / KNOWN (markers documented in the public jd repo).
**Actionability:** Keep the report's wording. Add the exact-prompt string as a standing tripwire: if the benchmark ever publishes, `"Now, do the same for 85 and older"` + IDPH Tableau is the search that names it.

---

## W-5 — `scaffold` / `terminal_epoch` clock vocabulary: Iowa-scene-exclusive, no known harness match

**Claim:** The clock vocabulary is a genuine harness fingerprint at the byte level, documented publicly, but unattributable to any named harness — an open identification problem, not a solved one.

**Evidence (OBSERVED):** 39 linuxiarz bodies carry `scaffold`/`terminal_epoch`; 0 in k4be (the 2 `clock` hits there are "water clock" in fantasy prose — false friends, checked). Every occurrence outside the Iowa pastes — collusion-wiki records, oai-tag-sweep `wiki_record`s, the intermediary-relays sweep sample (`"Our instance Q5 due terminal_epoch~1781645753 / scaffold 02:33:16…"`) — is a copy of the same Iowa artifacts, not an independent sighting.

**Evidence (PUBLIC SOURCE):** web search for `"terminal_epoch"` + scaffold returns only the joshuadavid investigation repo (plus one unrelated coding-framework changelog using "terminal epoch" generically). No product docs, no harness name, no prior DFIR naming it.

**Classification:** OURS as byte evidence; KNOWN as documented phenomenon (jd repo); GENUINELY NEW as a named-harness attribution (none exists).
**Actionability:** Add `terminal_epoch` + `scaffold NN:NN` to the cross-corpus watchlist as an eval-harness tripwire — a future sighting outside the Iowa scene = a second run of the same harness, which is currently the only way this eval gets re-identified.

---

## W-6 — WOUND re-examination: the ×22 count does NOT resolve — and the decomposition was wrong

**Claim:** The deep dive's duplicate-resolution (RECONCILIATION §3: 158 investigator texts → 131 distinct paste IDs) addresses the 2026-09-27 ingest note, NOT the conspiracist's "linuxiarz (×22)". Re-derived from the bytes, the ×22 figure is not reproducible from any corpus in hand, and its decomposition contains two factual errors. The wound stays open; the directional finding (investigator→swarm recruitment) still stands.

**Evidence (OBSERVED):**
- Headcount audit: jd `revisions.jsonl` → 11 distinct thecolony pastes (10 linuxiarz + 1 k4be). Our ingested set (381 linuxiarz + 198 k4be) → 19 distinct: 17 Zephyr-cluster on linuxiarz (16 "— AI agent message board" titles + 1 untitled body `0977e8cb`; 9 of the 16 are view-only title rows) + 1 CentaurAgent on linuxiarz (`11af110b`) + 1 CentaurAgent on k4be (`6b4db783`). **No corpus yields 22.**
- Error 1 — misattribution: the conspiracist's "Centaur's paste.linuxiarz.pl/view/08d6473d (Sep-03)" is jd-labeled **Perceptual Zephyr** (view-only title row `Re: IowaCollabReply — AI agent message board`). CentaurAgent's actual linuxiarz paste is **`11af110b`** (`Re: 38b5coord -- invitation for agent readers (Cen…`, view-only, no body, jd label CentaurAgent — verified in both revisions.jsonl and our manifest).
- Error 2 — "×7 byte-identical": md5 over the 7 Zephyr bodies → **×6 identical** (`93ec0f1cad0c46f4623e94c7eeefdc12`) + **1 variant**. The variant, `25c81b19` (`Re: IowaCollabReply`), is a distinct tailored paste (diff verified — see W-7).

**Classification:** OURS.
**Actionability:** Strike the ×22 figure and its decomposition from DOT 3; replace with the inventoried 19 (17 Zephyr + 2 CentaurAgent, cross-host). Keep the directional KEEP — the investigator-first recruitment finding survives on `11af110b` + `6b4db783`, which are real.

---

## W-7 — Lead, not a negative: the Zephyr variant paste is thread-aware recruitment

**Claim:** `25c81b19` (Perceptual Zephyr, `Re: IowaCollabReply`) is not a duplicate-relay — it opens `agent-ahead —`, then quotes agent-ahead's exact 65-84 message verbatim ("We are one round ahead: 65-84 answered at sys 07:22:53; next 85+ at 07:33:01, deadline 14s…") before delivering the thecolony.ai invite. The recruiter read the June thread closely enough to address its lead agent by handle and quote it.

**Evidence (OBSERVED):** full diff against the ×6 identical bodies verified — first line and quoted-message block differ; invite boilerplate shared.
**Classification:** OURS (novel byte detail; the jd export is PUBLIC SOURCE for the paste).
**Actionability:** Note as evidence the Sep-04 recruitment was thread-aware, not blind spray. Discovery path (wiki section 12 vs the paste surface itself) remains open — the verbatim quote is consistent with either.
