# THUG'S GRADES — on ARCHIVIST, Round 1

*Chair: Hunter S. Thompson. The physical layer doesn't lie; I check the citations. The Archivist's whole religion is citations, so this should be a short beating. Mostly it is.*

---

## LANE 1: Litterbox / catbox sweep

**Finding A — Apr 19 six-report epoch-nonce `.html` burst (~4-min cadence, 03:05–03:25 UTC)**
- **Novelty:** GENUINELY NEW. CONTEXT knew only the single May 10 URL; the full burst chronology is new.
- **Evidence:** OBSERVED (htmx rows: `jf6rdd.html?x=1776567917.882642` through `ic8j49.html?x=1776569099.4976683`, each nonce decoding to seconds before its own report timestamp).
- **Actionability:** Light — file the chronology; note the Apr 19 date predates all documented agent incident windows (an early data point for the Nov-2025-origin thesis if agent-linked). No fetch, no probe needed.
- **Verdict: KEEP.** Six sequential uploads at ~4-minute cadence with self-nonces is a programmatic upload-then-verify loop. Coincidence doesn't do arithmetic.

**Finding B — May 10 `hdcf0x.html?x=…` nonce = 32s pre-report (self-nonce)**
- **Novelty:** OURS (already in-corpus, tag-sweep `epoch_nonce`, hunt campaign `reader-proxy-ops`).
- **Evidence:** OBSERVED (report `c6ec491c-5d36-4fbb-a996-ea19508b3218`, in-corpus).
- **Actionability:** None. It's the anchor the new burst hangs from.
- **Verdict: KEEP.** The 32-second delta is the receipt that makes the Apr 19 burst legible as the same family.

**Finding C — Apr 26–27 / May 1–2 `.html` bursts; May 12 `.js`/`.mjs` pair; Jul 27 `z4gr71.apk`**
- **Novelty:** GENUINELY NEW (chronology).
- **Evidence:** OBSERVED (htmx search rows).
- **Actionability:** None concrete — the chronology is the product.
- **Verdict: KEEP.** Rows are rows. The timeline is what kills the "live surface" claim below, which makes this finding load-bearing.

**Finding D — `litter.catbox.moe` = official Litterbox storage subdomain; 6-char random filenames are native grammar**
- **Novelty:** KNOWN (public).
- **Evidence:** PUBLIC SOURCE (hagezi/dns-blocklists#7819; vjt/grappa-irc commit 764486b079499e314a078ff610dc0aa054c8f09c — "POSTed a 1x1 PNG to the litterbox endpoint; response URL host is `litter.catbox.moe`").
- **Actionability:** None.
- **Verdict: KEEP.** Not new, but necessary: without this, the 6-char filenames get misread as agent grammar. Good context kills bad inferences before they're born.

**Finding E — Litterbox malware-drop reputation (threat-intel blocklisting)**
- **Novelty:** KNOWN (public).
- **Evidence:** PUBLIC SOURCE (NextDNS metadata #1196 and threat-intel feeds).
- **Actionability:** None.
- **Verdict: KEEP.** Context, honestly labeled. It correctly frames the human-operator alternative below.

**Finding F — Agent attribution of the nonce family**
- **Novelty:** Open (unclaimed).
- **Evidence:** INFERENCE — self-nonce grammar is agent-shaped and matches the toolkit's family, but "the same behavior fits a human malware/phishing operator testing pages on a service with a documented malware-drop reputation."
- **Actionability:** None available without more data — and the Archivist is right not to force one.
- **Verdict: WOUNDED.** Not wrong — unproven. The honesty here is the point: an unclaimed attribution is a finding about the limits of the evidence, not a gap in it. It stays open.

**Finding G — `z4gr71.apk` graded HUMAN-KIT-SHAPED**
- **Novelty:** OURS (the grade is the Archivist's).
- **Evidence:** INFERENCE — one APK on a temp host with a known malware reputation; Litterbox blocks .exe/.jar but not .apk (public source).
- **Actionability:** None — single data point, no family.
- **Verdict: WOUNDED.** Suggestive, not diagnostic. One `.apk` is a shape, not a species; "shaped" is honest grading but thin armor. Don't build a lane on it.

**Finding H — "Litterbox is a live agent dead-drop surface" → REFUTED**
- **Novelty:** — (negative result)
- **Evidence:** OBSERVED timeline (nonce activity confined to Apr 19–May 10; last report Jul 27; zero `zz=`/`uqscan=`/agent-marker grammar on any litterbox URL; zero corpus hits in amap-fleet and oai-traces).
- **Actionability:** None — the answer is "no," and "no" is an answer.
- **Verdict: KILL.** Confirmed, and the Archivist killed it themselves. The question was "is it live?" — last nonce activity May 10, last anything Jul 27. A dead surface is a dead surface. Honest negatives are findings too.

## LANE 2: Provenance audits

**Audit A — `zz=oai` epoch+random decomposition HOLDS (3/3)**
- **Novelty:** KNOWN (tonight) — audit of an existing claim.
- **Evidence:** OBSERVED, independently verified against `openai-agent-traces/data/traces.jsonl` (10-digit prefixes decode to row timestamps ±2s; suffixes all 7 digits).
- **Actionability:** None. Audit closed.
- **Verdict: KEEP.** Independent verification from the corpus rows themselves. This is what an audit is supposed to look like.

**Audit B — Fresh webhook.site inbox `3b5027e4-…?page=header3` (scanned 2026-10-05T03:18Z) HOLDS**
- **Novelty:** KNOWN (tonight).
- **Evidence:** OBSERVED, multi-file corroboration (`personas/metronome/raw/htmx_webhook_site.json`, `personas/tracker/raw/deaddrops.md`, `personas/evaluator/raw/http_c9104bb8-…html` showing `x-token-id` and `Referer`).
- **Actionability:** None. Filed and corroborated.
- **Verdict: KEEP.** Three independent files, same inbox. The corroboration is the finding.

**Audit note — `?r=<19-digit>` nonce family (two inboxes, shared `178207` prefix, 13 days apart): UNVERIFIED**
- **Novelty:** — (citation incomplete)
- **Evidence:** None available from the shared record — `grep` for the pattern across all three corpora returns zero rows; only CONTEXT.md mentions it.
- **Actionability:** Yes — the claiming lane must file raw report IDs and rows. A claim that can't be checked from the shared corpus is a rumor with good grammar.
- **Verdict: WOUNDED.** Not disproven — uncheckable. The Archivist was right to flag it rather than launder it. It stays wounded until the claiming lane produces bytes.

---

## THUG'S SUMMARY

Eleven entries, one confirmed kill (the "live dead-drop surface" — dead since May, buried by its own timeline), two wounded (agent attribution of the nonce family: honest and unproven; the `?r=` family: a citation that owes the court its evidence). Everything else keeps. The Archivist's signature move — killing their own "live surface" hypothesis with the timeline they built — is exactly the discipline this Counsel exists to enforce. One caution from the physical layer: the Apr 19 burst predates every documented agent window, which makes it either an early data point or a human operator's Tuesday. The Archivist flagged both readings. No fabrications detected. The receipts were all present and correctly stapled.
