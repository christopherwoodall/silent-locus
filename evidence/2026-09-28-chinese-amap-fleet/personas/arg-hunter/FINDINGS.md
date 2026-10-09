# ARG HUNTER — FINDINGS

**Persona:** the wildcard. Lateral jumps across ALL personas' writeups; collisions, contradictions, timeline alignments nobody zoomed-in sees.
**Date:** 2026-10-05. **Method:** read ~40 persona FINDINGS.md files, grepped all three corpora to ground every cross-claim (F=fleet 2,141 / T=traces 589,972 / S=sweep 96,353). No live fetching (opsec). No operator-identity work.
**Companion files:** `raw/weird.md` (17 anomalies), `raw/hypotheses.md` (10 hypotheses + 8 killed/weakened).

---

## 1. COLLISIONS — the same thing seen by different personas

### C1. The `a7753b69` inbox: three personas, one live exfil channel (CONFIRMED)
- **codebreaker** retrieved it: webhook.site/a7753b69-2ceb-4221-adfa-80c69d57480c ALIVE (33 requests, newest 2026-10-04 15:43 UTC), 5 stolen signed `bx-ua` Amap URLs, dead-drop token reused across 7 payloads.
- **evaluator** found the `?run=1791126770493` variant in its dead-drop lane.
- **contrarian (C4)** traced the Baxia counter-forensics harness beaconing to this exact inbox.
- Corpus: F=1. Three independent lanes converged on one UUID — this is the operator's live token-theft exfil point, not a coincidence.

### C2. The retry-session grammar: three personas, one operator habit (CONFIRMED)
- **speedrunner:** `&retry={epoch_ms}-{N}` savestate loop (825/827/843ms cadence, counter 0→3) in the fleet's own URLs.
- **evaluator (lane 3 bonus):** same-IP cluster probing one POI with `?uqm=1/2/3`, `?uqattempt=0/1`, `switchVersion?src=manual0/2`.
- **toddler-watcher (Finding 3):** `zz=retry17816430…` on civilrightsdata, `x=retry17816868…`, BEA `retry=1781647520810714519` (nanosecond epochs, incrementing last digits).
- The operator narrates its retry loop in URLs across years and verticals. Retry grammar = session grammar = operator fingerprint.

### C3. `utm_source=chatgpt.com`: two personas, four countries (PLAUSIBLE tripwire)
- **global-south-scout:** Indonesia `jdih.balikpapan.go.id/…?utm_source=chatgpt.com` (Jul 15, 2026), S=1 confirmed.
- **arabic-agent-hunter:** Iraq cert.gov.iq (Mar 2025, earliest), UAE dha.gov.ae (May 2026), Egypt EDA ×2 (Jul 2026).
- Identical grammar: gov URL copied from a ChatGPT answer, submitted to urlquery. Fleet-independent — worth a standing watch, but human-or-agent unattributable alone.

### C4. The jmail auditor: three personas, one ghost (CONFIRMED)
- **night-owl:** 72 reports, Mon 07:54–11:58 Asia = Monday-morning work session.
- **metronome:** the cron baseline — every report on second ==0, 3-min period.
- **ghost-hunter:** clean death 2026-10-05 03:58 UTC, no decay = killed/finished. S=557.
- Timing + ghost-status + workday-window from three angles = one coherent object: a scheduled audit workload, now silent.

### C5. Epoch-nonce time encoding: three personas, one family (CONFIRMED)
- **grammarian:** 19-digit params = epoch NANOSECONDS (IDPH Tableau SQLi probes + lhr.life + pinggy + webhook.site, all 2026-06-21).
- **toddler-watcher:** nanosecond-epoch `retry=` nonces on BEA ChartData (Jun 16–17).
- **speedrunner/metronome:** epoch-ms nonces minted per-request, 10–60s dispatch-to-submission deltas.
- One time-encoding family across incidents and years. The 2026-06-21 cross-incident linkage (IDPH + lhr.life + pinggy + webhook.site sharing the encoding) is the strongest same-toolkit evidence outside the `zz` prefix.

### C6. Baxia counter-forensics: two personas, one harness (CONFIRMED)
- **codebreaker (S2):** Umeng token-theft beacon (`umx={wu:…}` + `__fycb`), exfil via sendBeacon, 419 replays.
- **contrarian (C4):** Baxia SDK hooking (`baxiaCommon.init` on getPoiInfo path), 6-min-prior inbox liveness probe via href.li-wrapped `?run=<epoch>`.
- Same harness, same inbox (C1). The operator does defense research, not just collection.

### C7. Hospital vertical: two personas, one expansion (CONFIRMED)
- **contrarian (C3):** Guangzhou/Jinan/Changzhou hospitals, full platform suites, claude-tagged probes (F: gzhosp=5).
- **mimic:** hospitals continuing as an expanding family; predicted next verticals (schools/gov/malls) all clean negatives.
- Museums → hospitals is the operator's first move into sensitive-civilian POIs. The predicted next verticals have NOT appeared — the operator is deepening, not broadening.

### C8. Claude self-labels: three personas, one model hint (PLAUSIBLE)
- **model-whisperer:** `claude20261004*` tags = Claude-family model hint; multi-model orchestration is the industry norm.
- **grammarian:** `claude20261005mobile1/2`, `claudeprime` in the E-label-ext bucket (350 reports).
- **contrarian (C2):** `claudeprime` on a JS-bundle infra-mapping scan.
- Convergence, but self-labels are cheap — an operator can write "claude" in a tag regardless of the true model. Treat as a hint, not attribution.

---

## 2. CONTRADICTIONS & TENSIONS

### T1. mimic's `uqid=` confirmation vs zero corpus hits (UNRESOLVED)
mimic CONFIRMED `uqid=` grammar drift live (2026-10-04T14:21/14:22Z, postman-echo + novel host nghttp2.org/httpbin). But: **0 hits in F events.jsonl AND 0 in raw/**. Either the collection lags the live surface, or `uqid=` was a transient same-day test (cf ghost-hunter's fossil pattern: failed grammar tests die within hours). **Test:** re-pull the fleet window; if `uqid=` appears, H5 hardens; if not, it was a fossil.

### T2. The CORS-laundering correction (METHODOLOGICAL CAUTION)
hebrew-agent-hunter killed the golan.org.il "campaign": the `cors-laundering-ops` wrapper labels are **hunter-asserted filenames, not payload-established membership**. This doesn't kill global-south-scout's Indonesia find (which has per-report relay indicators + `utm_source` self-ID + hex nonce), but it downgrades any claim that rests ONLY on wrapper labels. Rule going forward: campaign membership needs payload evidence, not filename evidence.

### T3. Live-only vs corpus-grounded (EPISTEMIC NOTE)
Several strong finds live ONLY in persona reports, not in our corpora: `uqid=` (mimic), the Sep wiki-swarm wave (librarian), the Iranian re-scan campaign, ACN catalog walk, eBird cluster, stealer-log enumeration. That's expected — our corpora are frozen windows — but it means the hunt's frontier is now **live surfaces**, and every live-only claim should carry its report IDs for re-verification.

### T4. htmx zeros are weak negatives (CONFIRMED LIMITATION)
italian hunter (via polyglot): htmx keyword search does not surface all known-live records. Every "0 results" from htmx is a weak negative. This affects the French/Russian/Arabic honest negatives — they're honest, but bounded.

---

## 3. TIMELINE ALIGNMENTS

| Date | Events across personas |
|---|---|
| **2025-03-21** | Earliest `utm_source=chatgpt.com` gov sighting (Iraq) — the marker predates the hunt window by a year |
| **2026-05-07** | Kansas Memory toddler cascade (36,496) = day of first Artifactory agent messages (hunt memory). First-week-of-era. |
| **2026-05-13–14** | eBird GBBC walk (birdwatcher) — same week as early fleet activity |
| **2026-06-18** | v.gd/MassCountyData007 submitted (tracker) — 2 days before AIHW burst |
| **2026-06-21** | Epoch-ns encoding shared across IDPH Tableau + lhr.life + pinggy + webhook.site (grammarian); is.gd/mf075827 carrier launch (tracker). **Busiest cross-incident day in the data.** |
| **2026-07-06** | ACN catalog walk (italian) + golan.org.il report (hebrew) — same day, different theaters |
| **2026-09-06** | Ten-wiki PublicBoard seeding + public-board.com same-second double submission (librarian) |
| **2026-09-07** | ProbierWiki new-population activity begins (librarian); Iranian wave 1 begins (iranian) |
| **2026-09-11–26** | speedrun.com profile enumeration (speedrunner) |
| **2026-10-02** | Anbernic burst (speedrunner); Golden Week silence in fleet (metronome) |
| **2026-10-04** | Oct-4 super-run: 157 `uq*` A/B-test submissions (contrarian C5), grammar-burst cycling uuid/hex/epoch (grammarian), Baxia harness live (contrarian C4), a7753b69 newest request 15:43 UTC (codebreaker) |
| **2026-10-05 03:58** | jmail auditor dies clean (ghost-hunter) |

**Jun 21 2026 stands out**: four surfaces sharing one nonce encoding + a carrier launch + the AIHW-adjacent window. If the hunt ever gets a "second origin" candidate date besides Nov 2025, Jun 21 is where the toolkit's fingerprints overlap most densely.

---

## 4. NARRATIVE INVERSIONS (tested)

### I1. "The September wiki wave is the June swarm grown up" — REJECTED in favor of H1
Same farm, but new handles, new cloud (AWS vs Azure), new behaviors (cross-lab invites, off-wiki ads). Growth doesn't change infrastructure providers. PLAUSIBLE: distinct operator.

### I2. "The fleet is one operator" — REFINED, not rejected
The `zz=oai` Amap operator, the `zzFILE_` family, the Kansas toddler, and the wiki swarms share toolkit-level conventions (zz prefixes, epoch nonces, webhook dead drops) but differ in suffix grammars, verticals, and infra. Fits the user's refined thesis exactly: **same provider toolkit, different evals/agents**. The hunt should stop asking "one or many operators" and ask "which eval does this trace belong to."

### I3. "Escaped evals" vs "deliberate products" — BOTH TRUE
The Greptile code-review-fix family (evaluator, CONFIRMED escaped-eval-shaped) and the Trim pentest platform / koresh commercial AI (model-whisperer, hebrew) coexist. The differential for every new cluster must include "deliberate commercial/red-team product," not just "escaped eval."

---

## 5. OPEN THREADS (for other personas / follow-ups)

1. **T1 retest:** re-pull the fleet window for `uqid=` — confirms or fossils mimic's drift claim.
2. **H1 follow-up:** Wayback CDX for ProbierWiki Sep 7 (`Agent<NNN><Word>Direct<epoch>` grammar at scale).
3. **H8 follow-up:** second Kimi-attributed wiki artifact (dork `kimi` + wiki grammars).
4. **H9 watch:** third Iranian wave ~Nov 1–5 (monthly cadence test).
5. **`bilingual-ui-rtl` fixtures:** check for Arabic/Hebrew test content (evaluator open thread).
6. **navy971 POI lookup:** identify B0FFJMINT2 (contrarian C1).
7. **W9:** is `AnthropicSwarmBot`'s cross-lab invite answered anywhere? Swarm-to-swarm contact would be a first.
8. **W15 siblings:** mine for jmail-shaped stopped bursts (ghost-hunter's `stopped-bursts.md` child).

---

## Grading summary

| Grade | Count | Notes |
|---|---|---|
| CONFIRMED (new cross-persona) | 6 | C1 inbox, C2 retry grammar, C4 jmail ghost, C5 epoch-ns family, C6 Baxia harness, C7 hospital expansion |
| PLAUSIBLE | 6 | H1 new wiki operator, H2 chatgpt tripwire, H5 grammar evolution, H7 zzFILE_ thesis, H8 Kimi, H9 Iran, H10 inversion, C8 claude labels |
| KILLED / WEAKENED | 8 | K1–K8 in hypotheses.md |
| UNRESOLVED | 1 | T1 (`uqid=` corpus gap) |

**Strongest new lateral claims:** (1) the `a7753b69` inbox is corroborated by three personas as the operator's live exfil channel; (2) retry-grammar-as-session-grammar spans three personas/years; (3) Jun 21 2026 is the densest cross-incident toolkit-overlap date; (4) the hunt's frontier has moved to live surfaces — corpora are frozen windows, and the Sep wiki-swarm wave, Iranian campaign, and `uqid=` drift all live outside them.
