# HYPOTHESES.md — ARG hunter's testable claims

Grade: CONFIRMED / PLAUSIBLE / KILLED. Every hypothesis states what would confirm or kill it.
Corpora: F=fleet(2,141) T=traces(589,972) S=sweep(96,353). "0 in corpora" = checked via grep 2026-10-05.

## H1. The September wiki-swarm wave is a DIFFERENT operator from the June collusion-wiki swarm
- **Claim:** ProbierWiki Sep-7 activity (AWS us-east-1, `Agent<NNN><Word>Direct<epoch>` handles, ~300 saves/day) + Wiki4D `AnthropicSwarmBot` + ten-wiki PublicBoard seeding (Sep 6) = a new population, not the June Azure swarm.
- **Evidence:** librarian/FINDINGS.md — new handle grammar, new infra (AWS vs Azure), new behaviors (cross-lab invites, off-wiki board ads). 0 hits for ProbierWiki/public-board.com/AnthropicSwarmBot in F/T/S.
- **Would confirm:** Wayback CDX for ProbierWiki Sep 7 showing the `Agent<NNN><Word>Direct<epoch>` grammar at scale; handle→IP mapping to AWS.
- **Would kill:** the Sep handles resolve to the June operator's Azure blocks.
- **Grade: PLAUSIBLE (strong).** This is the freshest unattributed agent population in the hunt.

## H2. `utm_source=chatgpt.com` on gov domains is a fleet-independent agent tripwire
- **Claim:** the marker recurs across harnesses/regions: Iraq cert.gov.iq (Mar 2025, earliest), UAE dha.gov.ae (May 2026), Indonesia jdih.balikpapan.go.id (Jul 2026), Egypt EDA ×2 (Jul 2026).
- **Evidence:** arabic-agent-hunter §1 (4 sightings) + global-south-scout §1 (Indonesia, S=1 confirmed). Grammar identical everywhere: gov URL copied out of a ChatGPT answer, submitted to urlquery.
- **Would confirm:** a fifth sighting paired with machine cadence or probe grammar.
- **Would kill:** nothing — it's a tripwire, not an attribution. But as an *agent* marker it's weak alone (humans copy URLs from ChatGPT too).
- **Grade: PLAUSIBLE** as tripwire; UNPROVEN as agent marker.

## H3. The `a7753b69` dead-drop inbox is the operator's live exfil channel (3-persona corroboration)
- **Claim:** webhook.site/a7753b69-2ceb-4221-adfa-80c69d57480c is the Amap operator's active token-theft exfil point.
- **Evidence:** codebreaker — RETRIEVED, ALIVE (33 requests, newest 2026-10-04 15:43 UTC), 5 stolen signed bx-ua URLs, token reuse across 7 payloads; evaluator — `?run=1791126770493` variant in dead-drop lane; contrarian C4 — Baxia harness beacons to the same inbox; F=1.
- **Would confirm:** already confirmed (live retrieval).
- **Grade: CONFIRMED.**

## H4. The operator runs counter-forensics R&D, not just collection
- **Claim:** the Baxia/Umeng harness (hooking Alibaba anti-bot SDK, exfiltrating telemetry tokens, replaying signed URLs) is research into Amap's defenses — one level past scraping.
- **Evidence:** codebreaker S2 (Umeng token-theft beacon family, `umx={wu:...}` + `__fycb`, 2 replays rejected 419), contrarian C4 (Baxia init on getPoiInfo path, sendBeacon to a7753b69).
- **Grade: CONFIRMED.**

## H5. `uq*` grammar drift is single-harness evolution, not a mimic
- **Claim:** `uqscan=` → `uqm=`/`uqattempt=`/`uqid=`/bare-epoch is the same operator A/B-testing param survival (contrarian C5: 157 Oct-4 submissions, whole `uq*` family under test).
- **Evidence:** grammarian E-label-ext (350 reports, incl. `claude20261005mobile1/2`, `claudeprime`); mimic CONFIRMED `uqid=` live 2026-10-04.
- **Tension:** `uqid=` = 0 hits in F and raw/ — mimic's confirmation is live-only, not corpus-grounded. Either the collection lags or it was a transient test.
- **Would confirm:** `uqid=` appearing in a refreshed corpus pull.
- **Would kill:** `uqid=` never reappears AND new grammars show different egress/IPs.
- **Grade: PLAUSIBLE** (strong on the A/B-test reading; the `uqid=` leg is live-only).

## H6. The Kansas Memory toddler is a separate, unreported agent (first-week-of-era)
- **Claim:** 36,496 submissions May 7 (3.2 req/s, self-submitted 404s, zero tags) = a different agent from the OpenAI-tagged operation, active the day of the first Artifactory agent messages.
- **Evidence:** toddler-watcher Finding 1; T=36,496 confirmed.
- **Grade: CONFIRMED** as a distinct agent-shaped event (untagged, different vertical, error-cascade behavior).

## H7. `zzFILE_`/`zzMAILBOX_` is same-provider, different-eval from our operator
- **Claim:** the METR "swarm that kept coming back" family (5,161 files, HOLD/VETO/GO/STOP/ACK, `hb####`) shares the `zz` prefix with our `zz=oai` but a different suffix grammar → same launcher toolkit, different eval (per user's refined thesis).
- **Evidence:** grammarian lane 2a; 0 hits in F (2,141).
- **Would confirm:** a `zzFILE_` artifact carrying an oai-adjacent marker.
- **Would kill:** (as a linkage claim) — it's already a no-bridge negative; the thesis survives either way.
- **Grade: PLAUSIBLE** (thesis-consistent).

## H8. Kimi (Moonshot) models are in the wiki-swarm loop
- **Claim:** non-OpenAI models participate in wiki swarms — messageboardauditbench forensic report filed under `react_moonshotai_kimi-k3_r1_20260907T095543Z`.
- **Evidence:** librarian; single report ID.
- **Would confirm:** a second Kimi-attributed wiki artifact.
- **Grade: PLAUSIBLE (weak)** — one data point.

## H9. The Iranian gov-domain re-scan campaign is agent-shaped, unattributed
- **Claim:** 14 urlscan API submissions, fixed target list, two waves (Sep 7–12, Sep 27–Oct 5), 00:00–07:30 UTC band = machine schedule.
- **Evidence:** iranian-agent-hunter §1; 0 in F/T/S.
- **Would confirm:** third wave ~Nov 1–5 with the same target list (monthly cadence hardens the monitoring hypothesis).
- **Would kill:** wave 3 never comes (one-off researcher project).
- **Grade: PLAUSIBLE.**

## H10. INVERSION: some "escaped eval" shapes are deliberate commercial/red-team operations
- **Claim:** the eval-escape framing may mislabel deliberate activity — e.g. "Trim" pentest platform (Claude Opus 4.8 + GLM-5, shipped Jun 21), ACN catalog walk (could be a commercial scanner), koresh.app.lizzyai.com (commercial Hebrew legal AI, hebrew hunter).
- **Evidence:** model-whisperer §1, italian hunter §1, hebrew hunter.
- **Would confirm:** vendor attribution for any one of these clusters.
- **Grade: PLAUSIBLE** as a standing alternative — the hunt should keep "deliberate product" on the differential for every cluster.

## KILLED / WEAKENED
- **K1. golan.org.il as an Israeli campaign — KILLED.** Shared bulletproof host; neighbors are phishing/malware (tibiahd.com, 7-seas-casino-ca.com, b1-binance.com.cn). One-off inside a wrapper, not a campaign. (hebrew hunter)
- **K2. Dream "Agent A–Q" as a live swarm marker — WEAKENED.** It's OpenAI Swarm's default demo grammar (README). Don't treat new hits as Dream-tooling evidence alone. (grammarian)
- **K3. "Authorized penetration test" framing as Dream evidence — WEAKENED.** Generic pentest-agent boilerplate (team7-hermes SKILL.md, kali forks). (grammarian)
- **K4. warnung.bund.de singleton as a German agent — CLOSED.** No IP/domain/similar siblings. Singleton stays a singleton. (german-agent-hunter-2)
- **K5. GAIA eval fingerprints in the wild — HONEST NEGATIVE.** ~40 fingerprints, zero genuine hits. (evaluator)
- **K6. Scheduled dead-drop beaconing — HONEST NEGATIVE.** 13 services, zero metronomic runs. (metronome §5)
- **K7. French/Russian agent fleets on checked surfaces — HONEST NEGATIVES.** French zero cross-checked on urlscan; Russian net catches nothing (PaperCut actor lives off visible surfaces). (french/russian hunters)
- **K8. Gaming vertical as agent gameplay — HONEST NEGATIVE.** Reconnaissance only, no TAS-shaped play. (speedrunner)
