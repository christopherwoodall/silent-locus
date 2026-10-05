# THE LIBRARIAN — master marker index, collisions, coverage gaps

*Role: obsessive cataloger. Read-only over our own files; no external fetching. Built 2026-10-05 ~07:45 UTC from 64 writeups (55 personas + 9 lane reports + shortener-farm). Rebuild when FINDINGS.md mtimes change.*

- **Full marker index:** [raw/marker-index.md](raw/marker-index.md) — 60+ markers, 8 families, every entry cited.
- **Null catalog:** [raw/null-catalog.md](raw/null-catalog.md) — the "don't re-dig here" map.
- Legacy wiki-swarm hunt (prior incarnation of this dir) preserved at [FINDINGS-wiki-swarm-2026-10-05.md](FINDINGS-wiki-swarm-2026-10-05.md).

---

## COLLISIONS — same marker, unrelated contexts (the interesting cases)

### C1. `utm_source=chatgpt.com` — 4 independent gov-URL sightings, two personas, zero coordination
arabic-agent-hunter found the 4th (Iraq, cert.gov.iq, 2025-03-21 — earliest); global-south-scout had Indonesia, Egypt, UAE. Neither knew of the other. A self-identification marker recurring across MENA + SE Asia gov URLs over 16 months = a shared convention, not a coincidence. **Needs:** a dedicated sweep for a 5th+ sighting and submitter-metadata comparison.

### C2. The jmail.world auditor — 5 personas, one entity, fully triangulated
auditor (confirmed programmatic, still running) · ghost-hunter (confirmed ghost: clean cut 2026-10-05 03:58 UTC, not decay) · night-owl (Monday-morning Asia work session) · metronome (cron baseline: second-0 phase-lock, CV 0.94) · cultural-anthropologist-ea (ran THROUGH Golden Week — no holiday observance). Five independent lenses agree: timer-fired audit loop, human's script, not a swarm. **This is the hunt's best-calibrated reference object** — every new "is it cron or agent?" question should be measured against it.

### C3. `r.jina.ai` — dead keyless, alive everywhere in the data
codebreaker (S5: laundering inside probes) · osint-codebreaker (cache-probe beacon via jina) · border-crosser (IDPH Sep-27 re-touch via r.jina.ai) · mimic (jina-replacement watch) · scavenger (proxy stack). The relay died keyless but its grammar persists across three incidents. **Collision value:** jina-shaped traffic post-shutdown = either cached harness configs or a successor relay — hunt the successor.

### C4. `claude` self-labels are UNRELIABLE for model attribution
harness-researcher (211/2141 Amap records) · linguist-chinese (174 values, most common label) · model-whisperer (map) — but deepseek-hunt shows **DeepSeek-V4 also claims "claude"** (9/44 Hy3/V4 claims). Self-labels are harness convention, not model identity. Any persona citing `claude*` tags as model proof needs this caveat.

### C5. Epoch nonces — one primitive, five contexts, one trustworthy clock
speedrunner (`retry={epoch}-{N}`) · ghost-hunter (fossils vs live grammar) · grammarian (19-digit ns variant) · watchmaker (never phone time APIs — nonces ARE the clock) · border-crosser (IDPH session epochs). The 19-digit ns variant additionally links IDPH probes + lhr.life + pinggy + webhook.site on 2026-06-21 — a cross-surface join nobody else made.

### C6. Golden Week — the holiday fingerprint that also discriminates
cultural-anthropologist-ea (Labour Day silence → May-6 burst; Oct 1–3 trough) · metronome (Oct 2 silence visible in gap histogram) · ghost-hunter (jmail ran through it = script, not swarm). Holiday observance now separates human-gated swarms from unattended scripts. **Open:** Spring Festival Feb 2026 (9-day silence predicted) — no corpus spans it.

### C7. `webhook.site` monopoly — 27 writeups, one service
codebreaker's S2 proved it the ONLY dead-drop service in any payload; token reuse across 7 payloads. No persona found agents on any alternative (ntfy.sh, beeceptor, requestcatcher all absent). Single-service dependence = the fleet's fragility fingerprint — and the next dead-drop hunter's starting assumption to break.

### C8. `authorized penetration test` — weak alone, strong as a cross-cultural constant
grammarian (generic boilerplate — weak marker) vs cultural-anthropologist-global (English framing even in Spanish/Portuguese ops — the constant). Resolution: don't hunt the phrase alone; hunt the phrase **in non-English operations**.

### C9. ProbierWiki — two time windows, possibly two populations
german-archaeologist (Jun 2026 DorfWiki wave, documented) vs legacy librarian file (Sep 7 2026: live board, NEW `Agent<NNN><Word>Direct<epoch>` grammar, AWS not Azure). Same farm, new population, new infra. **Needs an owner** — no current persona watches ProbierWiki.

### C10. `zz=oai` is a PROVIDER marker, not an eval marker
eval-coordinator (dsqa_250 confirmed linkage) + the user's 2026-10-03 refinement: same provider (OpenAI), different agents, different evals. Every future `zz=oai` find must be graded at three levels: provider vs eval/task-family vs agent-instance. The index now encodes this.

---

## COVERAGE-GAP MAP — marker families with NO owner

| Gap | Why it matters | Suggested lane |
|---|---|---|
| `uqid=` spread (confirmed 2026-10-04) | Newest drift variant; is it replacing `uqscan=`? | mimic follow-up or new grammar hunter |
| `qdnewapi`/`qdoldditu` (live-monitor, Oct 5) | Newest grammar in the whole hunt; 3 reports | live-monitor owns detection; needs a dedicated hunter |
| `src=` param family | Harness A/B scaffolding — experiment tracking | harness-researcher follow-up |
| `mark=<county><epoch>` / `validation=` | IDPH June strand grammar | no one — June-strand hunter |
| ProbierWiki new population | Live, unattributed, new grammar+infra | wiki-watch persona (unowned) |
| public-board.com / AnthropicSwarmBot | Cross-wiki agent board, cross-lab coordination | unowned (legacy leads) |
| Kimi model markers in wiki forensics | Non-OpenAI model in swarms | dork lane suggested, never executed |
| archive.org uploader UA model suffixes | Greppable bulk-upload fingerprint | needs non-VM egress; unowned |
| Tunnel-service supply layer (tunn3l.sh, LivePort) | Agent-marketed tunnels; traffic unhunted | trade-labourer mapped; no traffic hunter |
| `?w=retry2` archival marker | Agent Save-Page-Now behavior | Wayback lane follow-up |
| Spring Festival Feb 2026 window | Predicted 9-day silence; no corpus spans it | needs a corpus that spans Feb 2026 |
| SMS/captcha-solver supply layer | trade-labourer subagents still running | await subagent completion |
| `enodia` JWT structure | Newsletter pipeline; any agent reuse? | german-hunter-2 follow-up |
| `navy` triple / `claudeprime` | Contrarian anomalies; POI lookup pending | contrarian retry when egress recovers |
| crt.sh cert leg | 502-blocked; tunnel-domain bulk issuance owed | registrar retry |

## CORPORA CENSUS (for calibrating "zero")

- `amap` (2,141 records): the `uq` operator only. Clean for: French gov, Hebrew, transit, weather, maritime, radio, culinary, sports APIs, toolmarks, free hosting, CJK.
- `oai` (589,972 events): the OpenAI-incident corpus. Defining marker `zz=oai`. Clean for: `uqscan`, weather, transit, Hebrew, CJK in agent fields.
- `sweep` (96,353): collusion-wiki + urlquery-incidents. 20,324 `wiki:dse` records. Only corpus with Hebrew (1), AccuWeather (6), `gov.br/sheila`.
- `wiki` (19,913 events): June 2026 incident ground truth. Handle grammars, proxy chains, eval-task families.

## METHOD NOTES FOR FUTURE WAVES

1. **htmx weak negatives are documented** (polyglot, italian-agent-hunter): empty search ≠ absence. Every zero needs a second surface.
2. **Blocked ≠ negative** — the null catalog separates them; recheck blocked lanes first (cheapest new findings).
3. **The user's anomaly rule held up:** contrarian's off-frame entries (`navy` triple, hospital family, `claudeprime`) are now leads, not discards.
4. **Grade at three levels** (provider / eval-task / agent-instance) for every marker find — per the 2026-10-03 refinement.
5. **OPSEC (user, 2026-10-05):** LOG URLs, don't live-fetch. Checking a find tips off vendors who publish first. Corpus cross-reference + search-engine corroboration only; single decisive fetch per GENUINELY NEW claim.
