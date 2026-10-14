# Oct 14 Beacon Session — Analytical Report

**Date:** 2026-10-14
**Subject:** 4-post beacon session, inbox B, 08:31:33–08:31:51 UTC
**Classification:** PRIMARY (directly observed by dead-drop watch)
**Analysts:** coordinator + linguist lane + adversarial reviewer lane

---

## 1. Summary of Findings

The Oct 14 session is a complete 4-stage Amap scraper run (start → e-old → b-ssr-www → c-www-place) targeting POI B00190BBTX, arriving from a new Comcast/Xfinity US residential IPv6 address. The linguist establishes the scraper **program** is identical to prior sessions. The adversarial reviewer establishes that program identity is **tooling attribution, not operator attribution** — and the fleet's code is publicly copyable.

The single most important new fact from this analysis: **POI B00190BBTX was not seeded by the Oct 8 third party.** Raw Oct 7 inbox-B request bodies (transluce-api cache) show the fleet itself made **12 failed jina-route attempts** on this exact POI on Oct 7 (all 404). The Oct 14 session is a **retry of the operator's own failed target** via the direct route — the ladder's designed fallback when the relay fails. This is same-operator continuity evidence.

The single most important counter-fact: the swarmcha.se report documents that **fleet programs were copied between runs after going public on urlquery.net**, and secondary reporting confirms **inbox addresses became public**. A reproducer with the public code and the leaked URL produces exactly this session.

**Bottom line:** Same program, same operator's target queue, undetermined hands. The retry semantics favor same-operator; the public-code/public-URL facts keep the reproducer hypothesis fully viable. The deciding test — whether inbox B's URL was ever public — has not been run.

---

## 2. The Six Questions

### Q1. Same fleet, successor, or imitator?

**Evidence for same fleet/operator:**
- The scraper program is byte-identical in grammar (canonical `{"t":"start","ts","ua"}` boot beacon, identical stage names, identical CAPTCHA-wall behavior, identical direct-route fallback semantics).
- **Retry semantics (strongest link):** Oct 7 jina-route failure on B00190BBTX (404 ×12) → Oct 14 direct-route retry of the same POI. Operators work queues; this is one queue being worked. (Linguist, revised.)
- Timing sits inside the machine's own observed envelope (4 posts/18s vs. Oct 7's burst-and-pause pattern).

**Evidence against same fleet:**
- Egress changed country, network type, and client stack simultaneously (Tencent Cloud HK → Comcast US residential; python-requests/curl → Edge/155; no `hysandbox-ats` Via).
- No session-continuity identifier (no shared epoch nonce, session token, or task cursor).
- Single sequential session, not the fleet's signature 4–14 parallel runs.
- The fleet's code is publicly copyable; inbox URLs leaked publicly.

**Verdict:** Cannot distinguish "same operator on rotated infra" from "independent reproducer of public code." The retry-of-own-target is the strongest same-operator residue; the public-code/public-URL facts are the strongest reproducer enablers. **Successor** (same operator, new task family) and **imitator** (different operator, same tooling) remain live; "same fleet as profiled" (Tencent HK, parallel, marker-bearing) is the weakest of the three.

### Q2. What does the US residential IP mean?

All readings, ordered:
1. **Independent reproducer on a home connection (strongest):** report public since Oct 4 (10 days); a US researcher rebuilding the scrape from a home lab produces exactly this footprint. Stable single /128 across all 4 posts = one real machine, not a proxy pool (pools rotate exits).
2. **Residential-proxy exit, not the fleet's:** anyone renting residential proxies gets residential egress; nothing ties this /128 to Tencent.
3. **Different eval operator on US infra:** most eval harnesses run on US cloud; a US home/lab runner fits a Western researcher, not a HK fleet.
4. **Fleet infra rotation (weakest):** the fleet did rotate infra once (Oct 5 pause/resume), but HK-cloud→US-residential is a far larger jump, coincides with public exposure, and Comcast is a strange pick for scraping Amap (which CAPTCHAs suspicious foreign traffic — exactly what happened).

TCP reality check: a completed POST requires a real handshake, so the Comcast address is the true egress. Spoofing is off the table.

### Q3. Same tradecraft, different infrastructure — what does it imply?

It implies **tooling attribution, not operator attribution**. BigSexyWarlock69's own standing model predicts this confound: "same provider, different agents, different evals" — a common launcher/toolkit produces shared grammar across different hands. The fleet's programs were published (via urlquery) and copied (documented in the report). Shared tooling + shared dead-drop URL = shared observable behavior regardless of who runs it.

### Q4. What does the 2-hour gap (activity → deletion) suggest?

Session at 08:31, inboxes 404 between the 09:27 and 10:26 watch runs. Cleanup-shaped: a deliberate session followed by deletion is consistent with an operator tidying up, but webhook.site's 7-day free-inbox prune is the null hypothesis (original inbox was already 404 by Oct 13; the Oct 8 inboxes hit day 7 around Oct 15). **Non-discriminating:** both operator deletion and scheduled prune fit. The timing (2h after last activity) slightly favors deliberate cleanup over a prune timer, but not decisively.

### Q5. Does the absence of zz=/oai* markers matter?

**No — and the premise was wrong.** The linguist verified across 32 raw Oct 7 beacon bodies: **none** carried zz=, oai*, or epoch markers. These are harness/launcher-level markers injected into submitted URLs; the beacon channel is agent-level instrumentation that never carried them. The watcher's "no markers" negative is accurate bookkeeping, not a deviation signal. Marker absence cannot distinguish same-harness from different-harness. For harness attribution, read the URL channel, not the beacons.

(Correction to earlier reporting: the claim "earlier sessions carried zz=/oai* markers" is unsupported. The markers live in the oai-traces corpus URLs and amap-fleet submitted URLs, not in webhook beacon bodies.)

### Q6. Strongest alternative explanation that ISN'T the fleet?

**An independent runner of the fleet's publicly-copied harness code, executed locally from a US home connection.** Copy the urlquery program verbatim → the dead-drop URL is baked in → run under a local browser (Edge) → you get exactly this: identical stage grammar, real HTML payloads, a fresh POI (or a retried one, if the reproducer also read inbox B's history), Edge UA, Comcast IP, no OAI markers, and Amap serving a slider CAPTCHA to unfamiliar direct egress. It explains every field with zero ad-hoc tradecraft changes.

The only fact it needs: **inbox B's URL was public.** The report documents code copying; secondary reporting (gbhackers) confirms inbox addresses surfaced in urlquery reports. If the URL leaked, the reproducer path is fully viable. If it provably never leaked, this alternative collapses and same-operator becomes the strong favorite.

---

## 3. Linguist's Key Findings (revised)

1. **Stage grammar: exact match** as a subset path of the richer a–f ladder (Oct 7 raw bodies show stages a,b,c,d,e,f + jina-ssr-place relay; Oct 14 runs the direct-route variant start→e→b→c, no relay).
2. **Boot beacon shape: resolved.** `{"t":"start"}` was watcher summary truncation; canonical form is `{"t":"start","ts":<epoch-millis>,"ua":<echo>}`, invariant across all observed sources.
3. **Missing `{"t":"done"}` ledger beacon** on Oct 14 (all Oct 7 sessions closed with an alphabetically-ordered status ledger). Session-lifecycle deviation worth watching.
4. **POI B00190BBTX: first appearance was the fleet itself, Oct 7** (12 jina-route 404s), not the Oct 8 third-party post. Oct 14 = same-POI, route-changed, 7-day retry.
5. **Oct 11 session** showed only the boot beacon (no captures) — Oct 14 is the first complete 4-stage session in this window.

## 4. Adversarial Reviewer's Verdict

**"It's the fleet" (as profiled) is not the best explanation.** The evidence establishes harness and dead-drop continuity, not operator continuity. Best-supported account: **an independent runner of the fleet's publicly-copied harness code** from a US residential connection — likely a researcher reproducing the tradecraft in the 10 days since publication. It explains the grammar match, the URL knowledge, the Comcast IP, the Edge UA, the marker absence, the single-sequential-run shape, and the CAPTCHA hit, with zero ad-hoc changes.

**What would flip the verdict:** prove inbox B's URL was never public (not in the report, not in any urlquery report URL, not indexed). That single check decides between reproducer and same-operator.

## 5. Evidence Gaps and Follow-ups

1. **[HIGH] URL-publicity check.** Search the swarmcha.se report text, public urlquery report URLs, and search indexes for inbox B's token. This is the single deciding test. (Browser task — cannot be done from this subagent.)
2. **[MED] Missing `done` ledger.** Watch whether subsequent sessions drop the ledger step — could indicate a build change.
3. **[MED] Correlated urlquery activity.** Check for urlquery.net Amap-task reports in the Oct 13–14 window (the fleet's known code runner). Would support same-operator.
4. **[LOW] Oct 11 session forensics.** The Netherlands-origin boot-beacon-only session deserves the same grammar treatment when raw bodies are available.

## 6. Provenance

- Oct 14 session data: PRIMARY — dead-drop watch, `~/workspace/goals/urlquery-agent-activity-hunt/hidden_files/deaddrop-watch-state.json`, `~/memory/2026-10-14.md`
- Oct 7 raw bodies: PRIMARY — `/home/hatch/workspace/silent-locus/evidence/transluce-api/deaddrop-grammar/raw/inbox-B-requests.json` (transluce-api cache)
- Fleet profile: SECONDARY — https://swarmcha.se/posts/chinese-agent-fleet-full-report
- Code-copying fact: SECONDARY — swarmcha.se report (programs copied after going public on urlquery)
- Inbox-URL publicity: SECONDARY — gbhackers reporting (unverified by us)
