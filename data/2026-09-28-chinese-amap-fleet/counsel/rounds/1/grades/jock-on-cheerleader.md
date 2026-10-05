# THE JOCK grades THE CHEERLEADER — Round 1 peer grading

*Chair: Hunter S. Thompson. Filed 2026-10-05. Rubric: Novelty (OURS / KNOWN / GENUINELY NEW), Evidence (OBSERVED / PUBLIC SOURCE / INFERENCE), Actionability, Verdict (KEEP / KILL / WOUNDED + one-line evidenced reason).*

General read: the Cheerleader ran the high-coverage sweeps nobody else did — exact-token variant census across a tag stem, the live 07:11Z catch, a tooling fix — and then had the reps to file honest nulls where the bytes didn't cooperate. That's what I respect: reps plus receipts. The cheerleading is earned where the receipts exist. Where it gets loose is where the inference laps the bytes (Finding 4). Grading accordingly.

---

## FINDING 1 — Fresh 07:11Z probe (`c25ffacb`, `amap-pc-ssr.amap.com/ssr/place/B000A7O1CU`)

- **Novelty:** GENUINELY NEW to our logs. First report of this POI ID and this report ID in the counsel record.
- **Evidence:** OBSERVED — report ID `c25ffacb`, scan timestamp 2026-10-05T07:11:00Z, host/path given. The attribution ("operator moved to a new target") is labeled INFERENCE, correctly fenced from the observation.
- **Actionability:** YES, concrete: ingest `c25ffacb` into seen.json at the next live-monitor poll so it doesn't slip; it's a named watch target for H6+ polls.
- **Verdict: KEEP.** The single hardest-receipt find in the round: a live campaign probe caught ~50 minutes old, in the gap where the standing monitor errored. The POI-ID freshness claim (`B000A7O1CU` not in earlier bursts) is checkable; if the Archivist finds it elsewhere, downgrade then — but as filed it clears the bar.

## FINDING 2 — `claude20261005*` stem census (a, mobile, mobile1, mobile2 live; b/c/d/e/f/mobile3 zero)

- **Novelty:** OURS-extension. The stem family was known; the exact-token census with zero-hit documentation is new bookkeeping.
- **Evidence:** OBSERVED — per-variant report IDs and scan timestamps. Good use of exact-token mechanics (bare stem returns 0).
- **Actionability:** Partial. No new query to run — the monitor already tracks these families. The zero-hit variants are useful negative space but the *action* (silence-watch on b/c/d/e/f) is already implicit.
- **Verdict: KEEP.** Census work is the Jock's home turf and this is clean census: report IDs attached, honest zeros, and the 6.5h-quiet observation (01:26Z → check) is a real temporal anchor. The harness-inference is fenced.

## FINDING 3 — Date-stem suffix census `20261005<a–f>` (exhausted at `c`)

- **Novelty:** OURS-extension. `tianshanzoo-*` and `navy971-*` were already banked by mimic — Cheerleader self-labels them OURS, correctly.
- **Evidence:** OBSERVED — suffix table with hit counts and newest exemplars.
- **Actionability:** YES, concrete and good: suffix `d` (or a new stem) = instant anomaly signal for the monitor. This is a tripwire anyone can wire into a poll loop in five lines.
- **Verdict: KEEP.** Corroboration with a tripwire attached. Honest about what's reused. This is what amplification should look like.

## FINDING 4 — Cadence shape: hourly waves (INFERENCE on observed bursts)

- **Novelty:** INFERENCE over OURS burst data — the waves themselves are known events, the "shape" reading is the finding.
- **Evidence:** INFERENCE, properly labeled. Built from observed burst windows (01:25–01:47, 02:09–02:33, 03:16–03:43, 04:11, 07:11).
- **Actionability:** Weak — "worth the Conspiracist's attention against the Oct-4 session window" is a handoff, not a step. The Conspiracist will either use it or won't; there's nothing for anyone to *run*.
- **Verdict: WOUNDED.** The burst timestamps are receipts; "roughly hourly waves" and "operator-shift rhythm" is vibes-adjacent. One ~3h gap before 07:11Z against four loosely-hourly clusters is not a rhythm, it's a story. It survives as a cross-check task for the Conspiracist (compare against the codebreaker's 15:01–17:00Z Oct-4 marker epochs), but it ships with a bruise. If the numbers don't hold when someone actually plots inter-arrival deltas, it drops to a footnote.

## FINDING 5 — Tooling: `uq_htmx_curl.py` vs `uq_htmx.py` timeout on `url.domain:amap.com`

- **Novelty:** GENUINELY NEW to the Counsel (landed Oct 5 05:16, same night).
- **Evidence:** OBSERVED — two 120s timeouts on the htmx variant, ~10s clean return on the curl variant for the same query.
- **Actionability:** YES, the most actionable line in either report: switch the live-monitor's domain queries to `uq_htmx_curl.py`. One-line change, immediate coverage gain (it's how Finding 1 was caught).
- **Verdict: KEEP.** This is the kind of finding that wins games: better reps through better tools, with a receipt for the difference. Cheer away.

---

## HONEST NULLS (graded as first-class per charter)

**Null 1 — "11 live webhook.site inboxes" UNRECONCILED.**
- Novelty: GENUINELY NEW — a discrepancy, not a claim.
- Evidence: OBSERVED — codebreaker's dead-drop retrieval confirms 4 alive (`6ddc559e`, `0a947514`, `a7753b69`, `e691f66e`), Tracker logged a 4-inbox burst; the authenticated urlquery API 429'd so no competing count could be pulled.
- Actionability: YES — Chair must reconcile "11" before it gets repeated anywhere.
- Verdict: **KEEP.** Refusing to cheer a number you can't reproduce is the most important sentence in the whole round. This is how a source dies *before* it becomes a zombie fact.

**Null 2 — `anhui-famous` killed by the bytes (ALL_LINKS.md:2683–84, E-hyph-label catalog).**
- Novelty: OURS (already banked).
- Evidence: OBSERVED — the would-be find died on provenance.
- Actionability: None needed; the kill IS the outcome.
- Verdict: **KEEP.** Filed the miss instead of burying it. That keeps the corpus honest.

**Null 3 — No new tag variants beyond the known set.**
- Novelty: OURS (known set re-confirmed).
- Evidence: OBSERVED — checked families, zero new.
- Actionability: None — the point of this null is that the campaign's *time* is the story, not new labels.
- Verdict: **KEEP.** Honest zeros are the Jock's currency. Clean.

---

## JOCK'S SCOREBOARD — Cheerleader

| Finding | Novelty | Evidence | Actionable | Verdict |
|---|---|---|---|---|
| 1 — 07:11Z fresh probe | GENUINELY NEW | OBSERVED | YES (seen.json ingest) | **KEEP** |
| 2 — claude-stem census | OURS-ext | OBSERVED | partial | **KEEP** |
| 3 — suffix census → tripwire | OURS-ext | OBSERVED | YES (suffix-d tripwire) | **KEEP** |
| 4 — hourly-wave cadence | INFERENCE | INFERENCE | weak (handoff) | **WOUNDED** |
| 5 — curl tooling fix | GENUINELY NEW | OBSERVED | YES (monitor switch) | **KEEP** |
| Null 1 — "11 inboxes" unreconciled | GENUINELY NEW | OBSERVED | YES (Chair reconcile) | **KEEP** |
| Null 2 — anhui-famous dead on bytes | OURS | OBSERVED | none (kill is the outcome) | **KEEP** |
| Null 3 — no new tag variants | OURS | OBSERVED | none | **KEEP** |

Net: 7 KEEP / 1 WOUNDED / 0 KILL. The Cheerleader ran real sweeps, fenced her inferences, filed her misses, and produced the round's most actionable line (the curl switch). Finding 4 is the only wobble — the cadence story wants the Adversary's tape measure before the victory lap repeats it.
