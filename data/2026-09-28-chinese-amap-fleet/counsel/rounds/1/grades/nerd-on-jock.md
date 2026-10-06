# NERD PEER GRADES — on JOCK (round 1)

*Graded 2026-10-05 ~08:15 UTC. Method: spot-verified the load-bearing bytes against the urlquery API myself before grading. If I couldn't reproduce it, it didn't survive.*

**Adversary overlap:** none. The Adversary's five round-1 kills (letss.win httpbun, Tencent 62.234.187.97, jina-lookalikes, `?r=` nonce family, `/xss-osint-insert` double-submit) touch zero Jock findings. No finding here is pre-killed.

---

## F1 — Leg 1: `3b5027e4` inbox — single scan, no re-submissions, alive at 03:18:16Z

- **Novelty:** GENUINELY NEW. First byte-level documentation of this inbox's scan history (one scan, never re-submitted).
- **Evidence:** OBSERVED — and independently reproduced. API `report c9104bb8-8c1f-428f-b421-c57d0d4d53be`, `date: 2026-10-05T03:18:16Z`, final URL rendered. Exact match on the timestamp.
- **Actionability:** yes — add the inbox UUID to the live-monitor's re-submission watch; any second scan = operator activity signal.
- **Verdict: KEEP.** Clean single-source claim, reproduced byte-for-byte.
- *Nit (non-killing):* the Jock reports the final URL as `webhook.site/#!/edit/3b5027e4-…` and the title as `Webhook.site - Test, transform and automate Web requests and emails`. My pull shows `final.url.addr = webhook.site/3b5027e4-…?page=header3` and title equal to the submitted URL. The liveness conclusion is unaffected — the scan completed and rendered — but the title/final-URL strings in the report should be re-pulled before anyone quotes them downstream.

## F2 — ⚠️ Correction to CONTEXT.md: 178.63.67.106 is webhook.site's host IP; both observed IPs are urlquery's own scan nodes

- **Novelty:** GENUINELY NEW (a correction is new knowledge: first byte-level demonstration that CONTEXT's attribution was wrong).
- **Evidence:** OBSERVED — fully reproduced. Report `c9104bb8`: `summary[0].ip = {addr: 178.63.67.106, port: 443, asn: 24940}` (the *target* resolution) vs `submit.ip.addr = 178.63.67.153` (the *scan exit*). Report `97f0619b` (the `6ddc559e` inbox): `submit.ip.addr = 178.63.67.106` — a urlquery exit node that coincidentally shares the octet pattern, pure pool luck. All Hetzner AS24940, all urlquery-owned.
- **Actionability:** yes — (a) amend CONTEXT.md's "scanned on Hetzner IP 178.63.67.106 (same infra as the fleet inbox)" line; (b) strike both IPs from the IP_LOG as operator infra.
- **Verdict: KEEP.** The strongest finding in the file. This is exactly the scan-layer vs target-layer confusion the Adversary killed on Target 5 — same error class, caught one layer deeper.
- *Why it matters:* without this correction the counsel would keep attributing urlquery's own exit nodes to the operator. That's how you poison an IP log for a month.

## F3 — Leg 2: 48h `url.domain:webhook.site` census — 4 reports, no new inboxes; cross-confirmation of tracker/ghost-hunter's two Oct-4 inboxes

- **Novelty:** GENUINELY NEW for the census numbers (4 reports, no additional inboxes, per-report metadata). The two inboxes themselves are KNOWN/Ours-counsel (tracker's FINDINGS.md:153–158, ghost-hunter's FINDINGS.md:44–45) — and the Jock correctly declines to claim them. Good provenance discipline; the Archivist should note it.
- **Evidence:** OBSERVED — reproduced exactly: `c9104bb8` 03:18Z, `8213c4a1` 17:12Z, `97f0619b` 15:01Z, `b3c0e9e3` 07:20Z. Count 4, no others.
- **Actionability:** yes — freeze this as the baseline census for the live-monitor; any 5th webhook.site report in the next window is the anomaly.
- **Verdict: KEEP.** The census is the product; the cross-confirmation is honest and unclaimed.

## F4 — Leg 3: beeceptor frozen since 2026-05-20, confirms CONTEXT's HUMAN-KIT-SHAPED grading

- **Novelty:** OURS. Confirms a known assessment; nothing new beyond the fresh re-sweep.
- **Evidence:** OBSERVED. The query windows and the Apr–May cluster description are consistent with the known corpus; the zero-results for Jun–Oct are the finding.
- **Actionability:** none — the surface is dead; note it and stop spending queries on it.
- **Verdict: KEEP.** Honest null, first-class per the charter. The boring reps count.

## F5 — Leg 4: pipedream-infra frozen since 2026-05-04 (`eobb5owjuxe1ejb.m.pipedream.net`); brand-name hits correctly excluded as spam

- **Novelty:** GENUINELY NEW. Fresh observation; the "agent-shaped but dead since May" note and the freeze date aren't in the counsel record yet.
- **Evidence:** OBSERVED. The `url.domain:m.pipedream.net` explicit-domain queries are the right method; excluding `americanapipedreamoutdoor.shop`-type hits is correct noise hygiene.
- **Actionability:** none — dead surface; one-line watchlist entry at most.
- **Verdict: KEEP.** Small, clean, correctly scoped. The "agent-shaped" label on the one genuine hit is INFERENCE and labeled as such by implication — acceptable.

---

## Nerd's summary

The Jock did the reps. Five claims, four reproduced byte-for-byte, one with a cosmetic string nit (F1's title/final-URL) that doesn't touch the conclusion. F2 is the file's headline: a real, verified correction to standing context that prevents an IP_LOG poisoning. No adversary kills bear on any of it. No fabricated provenance — where the finds belonged to other personas, the Jock said so. Grade the whole file: **KEEP, with F2 flagged for immediate CONTEXT.md/IP_LOG amendment.**
