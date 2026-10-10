# CHEERLEADER grades — ADVERSARY (Round 1)
*Grader: THE CHEERLEADER. Chair: Hunter S. Thompson. Charter rubric. Filed 2026-10-05.*
*Rule of the seat: I amplify ONLY what the bytes support, and I grade the same way. Kills get celebrated, survivors get cheered — loudly — and anything standing on vibes gets dragged into the light.*

**Corpus baseline (inherited from the report, unchallenged):** grep across `data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141), `openai-agent-traces/data/traces.jsonl` (589,972), `data/2026-10-01-oai-tag-sweep/events.jsonl` (96,353) — ~688k events.

---

## FINDING 1 — letss.win self-hosted Httpbun cluster (95.169.18.20, 207.57.145.214)
- **Novelty:** OURS (new lead this round, born in Shodan, absent from all three corpora).
- **Evidence:** OBSERVED (Shodan host/DNS/count this session; zero corpus hits via grep).
- **Actionability:** YES — standing watchlist grep for `letss.win`, both IPs, and `16clouds.com` on every future corpus/urlquery ingest; upgrade to lead ONLY on first agent-traffic co-occurrence.
- **Verdict: WOUNDED — concur with the downgrade.** The adversary's kill of the *agent linkage* is clean: self-hosted httpbun is README-documented normal behavior (sharat87/httpbun: `docker run -p 80:80`), zero hits in ~688k events, and the Ncat proxy is pentester-shaped, not agent-shaped (no agent in our corpora has ever touched a bespoke Ncat proxy — that's a real negative check, well done). What survives genuinely deserves survival: a dual-ASN, no-web-presence httpbun + Ncat-proxy-on-cPanel-port oddity is weird enough to watch. The cheerleader cheers the discipline of killing your own lead while keeping the residue honest. Watchlist, not lead board.

## FINDING 2 — Tencent Beijing 62.234.187.97 (self-hosted Httpbun + LLM gateway)
- **Novelty:** OURS (Shodan lead, new this round).
- **Evidence:** OBSERVED + PUBLIC SOURCE (Shodan host data; QuantumNous/new-api's 48k-star README/docs).
- **Actionability:** None beyond generic infra logging — and that barely.
- **Verdict: KILLED — full concur.** The nginx OpenCloudOS welcome page + `eol-product` + stale CVE pile is the kill shot; nobody runs live agent infra behind a default test page. The "WordPress on a VPS" analogy is exact and honest. The hobbyist stack needs no conspiracy. Bury it; IP stays in the generic log at most. Zero bytes lost.

## FINDING 3 — jina-reader lookalikes (jina.orz.fit, jina.qingchuan.cloud, relay.woaifei.com)
- **Novelty:** OURS (Shodan page-hit pivot, new this round).
- **Evidence:** OBSERVED (Shodan DNS subdomains; tag-sweep corpus reader-endpoint census: r.jina.ai 3,233 / s.jina.ai 15 / r.jina-ai.workers.dev 6 / translate.goog 6; zero bespoke mirrors in agent traffic; zero hits for the three lookalikes across ~688k events).
- **Actionability:** YES — keep the three domains on the corpus co-occurrence watchlist; they promote only on first agent-traffic touch.
- **Verdict: KILLED as agent infra — full concur, and the strongest kill of the round.** The adversary's central move is the right one: the report doesn't just assert "no evidence," it asserts *positive evidence of a different pattern* — 96k events of agent reader traffic show agents use ONLY official/public reader endpoints, never bespoke mirrors. That's a dog that didn't bark with teeth. The orz.fit/qingchuan.cloud subdomain lists (jina next to openai, openrouter, aiapi2) read as personal AI-dev relays, exactly right. "Barely one pivot wearing a trenchcoat" — keep that line. Residue correctly parked at watchlist.

## FINDING 4 — `?r=<19-digit>` nonce family (shared `178207` prefix)
- **Novelty:** N/A — born from a prior writeup's framing, not a new lead.
- **Evidence:** OBSERVED (arithmetic: `date -d` on both values → 2026-06-21 19:46:16 and 19:40:00 UTC; delta 375,317,629,511 ns ≈ 6.25 minutes).
- **Actionability:** YES — the original dead-drop-diver writeup's "13 days apart / family marker" framing must be amended in FINDINGS.md, and the `?r=<19-digit>` "operator signature" hypothesis retired from the grammar list (agents here use `zz=oai<epoch+random>` / `uqscan=<tagword>`).
- **Verdict: KILLED — and this is the round's cleanest kill.** The shared prefix is chronology wearing a costume: any two nanosecond timestamps six minutes apart share their first ~15 digits; the prefix carries zero operator information. The 13 days was scan spacing, not nonce spacing; the values were baked in one June-21 session days before scanning — human cache-busting (`?r=` = cache-buster, universal convention) on inbox URLs to force fresh urlquery scans. Three layers peeled: temporal misreading → artifact-as-signature → scan-layer/submission-layer confusion. Surviving residue is honestly scoped to a footnote (one ~6-minute human session, human-shaped). Cheer for the `date -d`. Nothing cheaper and nothing more lethal.

## FINDING 5 — `/xss-osint-insert` double-submit
- **Novelty:** N/A — from the prior writeup.
- **Evidence:** OBSERVED (urlquery API overviews + full report for both scans: 2026-07-31T12:19:33Z and 12:32:29Z; Firefox 134 default UA; same exit node `qguvgzjxzsgb3vs`; 5 GETs, alert_count 0, zero captured webhook requests).
- **Actionability:** YES — amend FINDINGS.md: the "same minute 2026-08-08" metadata is factually wrong per the API's own `date` fields; reclassify the item as human-kit re-scan, not agent cadence.
- **Verdict: KILLED — concur, killed on three independent grounds and any one sufficed.** (1) Timestamps false. (2) Two urlquery *scans* ≠ two webhook *submissions* — the layer confusion is fatal, and the full-report detail (no captured requests at all) proves nobody ever POSTed. (3) `xss-osint-insert` is literate English — human-shaped — and the writeup's own SHAPE-6 graded keyboard-mash as human-kit, so grading the *legible* one as machine cadence is backwards on its own terms. What's left is a human OSINT tester's inbox link scanned twice 13 minutes apart: re-scan behavior. File under human kit. The "correct the record" recommendation is endorsed — the metadata error propagates if left.

---

## Verdict on the adversary's work overall

Five targets, one WOUNDED, four KILLED — and every kill is *evidenced*, not vibes. The best moves of the round: the timestamp arithmetic on Finding 4, the positive-evidence-of-absence on Finding 3 (official-endpoints-only census), and the scan-layer/submission-layer distinction on Finding 5. The "Corrections to the record" section (dead-drop-diver metadata wrong on dates; `?r=` "13 days" misframing) is the most valuable non-finding output — recommend the Chair adopts both amendments to FINDINGS.md. Cheerleader's only beef: the attack on Finding 1's "corroboration of existence" point (attack #5) is a freebie — two personas running the same Shodan query isn't corroboration of anything and the steelman shouldn't have offered it as such. Otherwise: red team did its job. Nothing wounded or killed here is wronged by the verdict.

**Aggregate: 0 clean survivals, 1 honest watchlist resident, 2 factual corrections owed to FINDINGS.md.**
