# THE JOCK grades THE ADVERSARY — Round 1 peer grading

*Chair: Hunter S. Thompson. Filed 2026-10-05. Rubric: Novelty (OURS / KNOWN / GENUINELY NEW), Evidence (OBSERVED / PUBLIC SOURCE / INFERENCE), Actionability, Verdict (KEEP / KILL / WOUNDED + one-line evidenced reason).*

Note on method: the Adversary already graded each target itself (WOUNDED/KILLED). My peer grade is on the *grading* — did the steelman hold, did the attack land, does the verdict survive my tape measure? The Adversary's job is the kill chain; my job is checking the chain isn't rusted. Five targets, five kill-attempts. Here's the tape.

---

## TARGET 1 — letss.win self-hosted Httpbun cluster (95.169.18.20, 207.57.145.214) → Adversary verdict: **WOUNDED**

- **Novelty:** GENUINELY NEW. Shodan-born lead from this round; the Shodan count observation (exactly 7 `http.html:"httpbun"` hosts worldwide) is new intel.
- **Evidence:** OBSERVED (Shodan host/count this session; zero corpus hits across ~688k events for letss.win, both IPs, 16clouds.com) + PUBLIC SOURCE (httpbun README's self-host instruction) + INFERENCE (Ncat proxy reads human-shaped). All labeled.
- **Actionability:** YES, concrete and well-scoped: watchlist-only, upgrades *only* on future corpus/urlquery co-occurrence with agent traffic; explicit instruction "do not cite as agent-linked."
- **Verdict on the verdict: KEEP the WOUNDED.** This is how a wounded call is supposed to work. The attack is sound on all five points — the README-norm point and the base-rate point (2 of 7 hosts, other 5 scattered dev boxes) are the real killers of the agent hypothesis, and the Ncat-shaped-human read is the one place where I'd press the Adversary: "no agent in 688k events touched a bespoke Ncat proxy" is absence-of-evidence doing honest work *because* the corpus is large enough to make the absence meaningful (96k relay-traffic events with zero private mirrors — same argument used in Target 3, cross-consistent). The watchlist carve-out is disciplined, not sentimental. Stays wounded, stays unattributed.

## TARGET 2 — Tencent Beijing 62.234.187.97 (New API + Httpbun) → Adversary verdict: **KILLED**

- **Novelty:** GENUINELY NEW as a lead (Shodan-born this round).
- **Evidence:** OBSERVED (Shodan: nginx default test page on :80, OpenCloudOS, `eol-product` tag, old CVE list; zero corpus/urlquery linkage) + PUBLIC SOURCE (QuantumNous/new-api 48k-star project, one-click deploys, Alibaba Cloud partnership) + INFERENCE (gateway+relay = "I proxy my model calls and test my webhooks"; real operators separate concerns).
- **Actionability:** YES — remove from the lead board; IP kept in generic infra log at most. Clean disposal instruction.
- **Verdict on the verdict: KEEP the KILL.** The "like finding WordPress on a VPS" line is the correct base-rate read, and the stale-VPS observation (nginx welcome page, eol tags, unpatched CVEs) is the kind of physical-layer receipt the Adversary earned this round. "Zero corpus hits is not evidence of freshness — it's absence of evidence, full stop" is a shot across the bow of every future steelman that tries to spin emptiness as signal. The kill is clean and final.

## TARGET 3 — jina-reader lookalikes (jina.orz.fit, jina.qingchuan.cloud, relay.woaifei.com) → Adversary verdict: **KILLED as agent infra**

- **Novelty:** GENUINELY NEW as a lead (Shodan page-hits this round).
- **Evidence:** OBSERVED (Shodan DNS: subdomain spreads reading as personal AI-dev domains; reader-endpoint census from the 96k tag-sweep corpus — r.jina.ai 3,233 / s.jina.ai 15 / workers.dev 6 / translate.goog 6, zero bespoke mirrors; zero hits across ~688k events) + PUBLIC SOURCE (jina-reader open source, self-host documented) + INFERENCE (weak double-pivot on the Shodan hit; personal-gateway/SEO-spam hypotheses).
- **Actionability:** YES — watchlist-only, upgrade only on agent-traffic co-occurrence; explicit "do not present as leads." Also correctly preserved the cert-sleuth's prior watchlist position.
- **Verdict on the verdict: KEEP the KILL.** This is the round's strongest kill and the one with the most Jock energy: the dog-that-didn't-bark argument works here because the baseline is quantified (96k relay events, every one landing on official/public endpoints — if agents used private reader mirrors we'd have seen at least one). That's absence-of-evidence upgraded to evidence-of-absence by sheer sample size. The "one pivot wearing a trenchcoat" read on the Shodan page-hit is harsh and correct — page *mentions* of r.jina.ai are SEO/keyword noise. Well killed.

## TARGET 4 — `?r=<19-digit>` nonce family (shared `178207` prefix) → Adversary verdict: **KILLED**

- **Novelty:** GENUINELY NEW as a finding (the kill dismantles a steelman from the dead-drop writeup).
- **Evidence:** OBSERVED and decisive — `date -d` on both nonces gives 2026-06-21 19:46:16 UTC and 19:40:00 UTC, ~6.25 minutes apart; both predate their urlquery scans by days; `?r=` is the universal cache-buster param (PUBLIC SOURCE, general web knowledge); no corpus hits as agent marker (OBSERVED); agent grammar in-corpus is `zz=oai<epoch+random>` / `uqscan=<tagword>`, not `?r=` (OBSERVED).
- **Actionability:** YES — downgrade to a footnote (the weak session-linkage observation), and a concrete correction for the Chair: the "13 days apart" framing in the dead-drop writeup is misleading; it's 6 minutes of construction time plus 13 days of scan spacing.
- **Verdict on the verdict: KEEP the KILL.** The kill is on two independent grounds — timestamps *and* layer semantics — and the Adversary's best line of the round is in here: "the shared `178207` prefix is what time looks like." Nanosecond timestamps six minutes apart sharing 15 leading digits is chronology wearing a costume, exactly right. This is a kill I'll cite in the future when someone tries to turn temporal proximity into a signature. Clean, educational, final.

## TARGET 5 — `/xss-osint-insert` double-submit → Adversary verdict: **KILLED**

- **Novelty:** GENUINELY NEW (correction of the dead-drop writeup's facts).
- **Evidence:** OBSERVED and triple-grounded — (1) urlquery API `date` fields contradict the writeup: 2026-07-31T12:19:33Z and 12:32:29Z, thirteen minutes apart, not "same minute 2026-08-08"; (2) scan-layer vs submission-layer confusion: identical URL, Firefox 134 default scanner UA, same exit node `qguvgzjxzsgb3vs`, 5 HTTP GETs, `alert_count: 0`, zero captured webhook requests — one human re-scanning an inbox URL, not machine exfil cadence; (3) label-shape argument: descriptive English "xss-osint-insert" is more human-shaped than the keyboard-mash domains the same writeup graded HUMAN-KIT-SHAPED (INFERENCE, correctly fenced). Zero corpus hits (OBSERVED).
- **Actionability:** YES — file under human kit, not agents; and a concrete correction for the Chair: amend FINDINGS.md, because the writeup's dates/times are factually wrong, not just interpretively wrong.
- **Verdict on the verdict: KEEP the KILL.** Three independent grounds, and the Adversary caught an actual *factual* error in a sibling persona's writeup — dates that don't match the API's own fields. That's the red-team function working at its best: not "I disagree with your read" but "your numbers are wrong and here are the right ones." The re-scan read (check inbox, wait 13 minutes, check again) is the economical human-shaped explanation and it fits the identical-UA/same-exit-node receipts.

---

## JOCK'S SCOREBOARD — Adversary

| Target | Novelty | Evidence | Actionable | Verdict on the verdict |
|---|---|---|---|---|
| 1 — letss.win httpbun cluster | GENUINELY NEW | OBSERVED + PUBLIC + INFERENCE | YES (watchlist rules) | **KEEP** the WOUNDED |
| 2 — Tencent 62.234.187.97 | GENUINELY NEW | OBSERVED + PUBLIC + INFERENCE | YES (delist) | **KEEP** the KILL |
| 3 — jina-reader lookalikes | GENUINELY NEW | OBSERVED + PUBLIC + INFERENCE | YES (watchlist rules) | **KEEP** the KILL |
| 4 — `?r=` nonce family | GENUINELY NEW | OBSERVED (decisive) + PUBLIC | YES (footnote + correct the writeup) | **KEEP** the KILL |
| 5 — `/xss-osint-insert` | GENUINELY NEW | OBSERVED (decisive, triple-grounded) | YES (human-kit file + amend FINDINGS.md) | **KEEP** the KILL |

Net: all five verdicts stand. One wounded, four killed — and every one of the five earns its grade. Targets 4 and 5 are the Adversary's receipts-heavy work of the round: real timestamp computation, real API contradiction of a sibling's writeup, and the session-layer discipline (scan-layer ≠ submission-layer) that the whole counsel should copy. Target 3's kill is the strongest argument in the round for letting absence-of-evidence work *when the sample is big enough to make the absence meaningful*. Target 1's WOUNDED is the model for how to leave something on the watchlist without letting it inflate into a "lead" — upgrade condition stated, no cite-without-co-occurrence.

One note for the Chair: the Adversary's two "corrections to the record" (the xss-osint-insert dates and the ?r= 13-days framing) are actionable findings in their own right — they amend FINDINGS.md and the dead-drop writeup. Fold them into synthesis as corrections, not footnotes.
