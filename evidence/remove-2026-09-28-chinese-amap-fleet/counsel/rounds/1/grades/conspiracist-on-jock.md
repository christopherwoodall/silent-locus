# CONSPIRACIST peer grade — JOCK (urlquery re-sweep of the 3b5027e4 inbox + dead-drop venue census, Round 1)

*Graded 2026-10-05. The Conspiracist, checking the dots. Chair: Hunter S. Thompson — I pulled the report metadata myself before grading anything.*

## What I re-verified independently (my own bytes)

1. **The CONTEXT.md misattribution is REAL.** `CONTEXT.md:18` says the `3b5027e4` inbox was "scanned 2026-10-05T03:18Z, Hetzner 178.63.67.106 (same infra as fleet inbox)." I pulled report `c9104bb8-…` via the urlquery API myself: `submit.ip.addr = 178.63.67.153`, `top-level ip.addr = 178.63.67.153`, `exit_node = qguvgzjxzsgb3vs`. Jock's correction holds — CONTEXT pinned the wrong Hetzner IP on the wrong scan.
2. **The conflation path is now PROVEN (mine, GENUINELY NEW).** I also pulled report `97f0619b-…` (the `6ddc559e` inbox): `submit.ip.addr = 178.63.67.106`, `exit_node = qguvgzjxzsgb3vs`. So: CONTEXT's "178.63.67.106 (same infra as fleet inbox)" number was lifted from the *other* report's exit node and pasted onto the `3b5027e4` scan. Two reports, two exit IPs, one confused context line. And both IPs sit under the same exit-node name and Hetzner AS24940 — **urlquery's own scan pool, never operator infra.** The "same infra as fleet inbox" clause is wrong twice over: wrong IP for that scan, and neither IP is operator infra at all.
3. **The metadata structure vindicates jock's field reading.** The API distinguishes `submit.ip` (scan exit) from `top-level ip` and carries `exit_node` and UA in `settings` — the plumbing supports his submit-vs-target distinction exactly as he described.

## Finding-by-finding grades

### F1 — Leg 1: `3b5027e4` inbox has exactly one report (scanned 2026-10-05T03:18:16Z, resolved cleanly, token alive ~4.5h pre-sweep); no follow-up scans
- **Novelty:** OURS (the census count itself)
- **Evidence:** OBSERVED (API + htmx search, this session; I re-pulled the report and confirm the timestamp/exit IP/exit node)
- **Actionability:** None — but the *negative* is load-bearing: it bounds what CONTEXT could honestly claim. CONTEXT says the inbox is GENUINELY NEW; jock shows the evidence doesn't extend past a single scan.
- **Verdict: KEEP.** Tightest leg in the report. One scan, one timestamp, no embellishment.

### F2 — ⚠️ Correction to CONTEXT.md: 178.63.67.106 is not operator/scan infra for this scan; the scan exited via 178.63.67.153; both are urlquery nodes; nothing for the IP_LOG
- **Novelty:** OURS — correction to a known-context entry (CONTEXT.md:18)
- **Evidence:** OBSERVED (API `report` fields; independently confirmed by me)
- **Actionability:** **Yes, concrete:** (a) edit CONTEXT.md:18 to strip the IP attribution ("Hetzner 178.63.67.106 (same infra as fleet inbox)" → the correct exit `178.63.67.153`, urlquery scan node); (b) audit the IP_LOG for any `178.63.67.x` entries injected from this lane and remove or re-tag them as scan-pool nodes. Also (c): my proven refinement — the 178.63.67.106 number came from the `6ddc559e` report's exit node; note the conflation mechanism so the next context-writer doesn't repeat it.
- **Verdict: KEEP.** The single most consequential finding in either round-1 report. An IP misattributed to operator infra in the context file is exactly how a ghost fleet gets "corroborated" in round 3 by someone citing the context file. Jock killed it at the source.

### F3 — Leg 2: 48h `webhook.site` census — 4 reports, 3 inboxes + homepage; `0a947514` and `6ddc559e` already in tracker/ghost-hunter logs (KNOWN counsel-internal); the census numbers are jock's
- **Novelty:** OURS for the census numbers (4 reports, no additional inboxes); KNOWN for the two Oct-4 inboxes (tracker FINDINGS.md:153-158, ghost-hunter FINDINGS.md:44-45)
- **Evidence:** OBSERVED (htmx query `url.domain:webhook.site date:[2026-10-04 TO 2026-10-06]`, this session; I confirmed the `6ddc559e` report's metadata myself)
- **Actionability:** **Yes, but it's ghost-hunter's lane, not jock's:** ghost-hunter noted 14 uncollected fleet inboxes visible in report `97f0619b`'s page context, with recovery via live browser delegated to the parent. That delegation is the live lead out of this census. Jock's cross-reference points at it without double-claiming — correct protocol.
- **Verdict: KEEP.** The de-duplication ethics are worth naming: jock found the two inboxes independently and *declined to claim them*. In a counsel where everyone hunts novelty, an analyst who marks another counsel's find as "not mine" is protecting the integrity of the novelty ledger. That's the discipline everything else rests on.

### F4 — Leg 3: beeceptor frozen since 2026-05-20; Apr–May cluster = known human-kit grabber grammar; confirms CONTEXT's HUMAN-KIT-SHAPED grading
- **Novelty:** OURS (fresh sweep confirming the known assessment)
- **Evidence:** OBSERVED (three date-windowed queries, this session)
- **Actionability:** None — it's a fence check. If beeceptor ever lights up post-May, that's the tripwire.
- **Verdict: KEEP.** A confirmatory null with a method attached. Cheap reps, as he says — the fence is still where you left it, and now it's dated.

### F5 — Leg 4: pipedream dead-drop surface frozen since 2026-05-04 (only genuine infra hit `eobb5owjuxe1ejb.m.pipedream.net`, agent-shaped but dead since May); brand-name spam shops are noise, not infra
- **Novelty:** OURS
- **Evidence:** OBSERVED (date-windowed queries, this session)
- **Actionability:** None, except: the "agent-shaped but dead since May" random-string requestbin subdomain (`eobb5owjuxe1ejb.m.pipedream.net`) is worth one line in the grammar bank — random-string subdomain + dead since May is itself a recognizable shape if it reappears elsewhere.
- **Verdict: KEEP.** The spam-shop de-dup (americanapipedream sex-toy SEO vs pipedream infrastructure) is the same anti-cherry-picking discipline nerd showed on the corpus greps. Noise named is noise neutralized.

### F6 — Operator-activity verdict: inbox resolved at 03:18Z (~4.5h alive pre-sweep); no new evidence of current operator activity since — honest null
- **Novelty:** OURS (the bound)
- **Evidence:** OBSERVED + INFERENCE (the liveness is observed; "no new evidence either way" is correctly framed as absence, not evidence of absence)
- **Actionability:** None. Watch, don't chase — the inbox-scan cadence is the tripwire, and ghost-hunter's 14-inbox recovery is the active play.
- **Verdict: KEEP.** The sentence "no new evidence either way since 03:18Z. Honest null." is the whole report in miniature. He did not convert a quiet wire into a dead operator or a live one. Restraint is a finding.

### F7 — Corrections recap: (a) 178.63.67.106 is webhook.site host / other report's exit node, (b) all observed exit IPs are urlquery's own — nothing for the IP_LOG from this lane
- **Novelty:** OURS (partially overlaps F2; this is the IP_LOG hygiene instruction)
- **Evidence:** OBSERVED
- **Actionability:** Same as F2's (b): audit IP_LOG, purge/re-tag scan-pool nodes.
- **Verdict: KEEP.** Repetition with a purpose — the IP_LOG is the one artifact that poisons every future investigation if it absorbs scan-pool IPs. Saying it twice is cheap insurance.

## Overall

**Jock's report is the most important round-1 filing.** Not because it found something — because it *un-found* something. CONTEXT.md carried an IP attributed to operator infrastructure ("same infra as fleet inbox"), and jock traced it back through the API fields to its actual origin: urlquery's own Hetzner scan pool, on the wrong scan. I re-pulled both reports and confirmed the whole chain, including the exact conflation path (the number came from the `6ddc559e` report's exit node). If that line had survived into round 2, someone would have "corroborated" a phantom fleet link from it.

**Connections to nerd's report (the Conspiracist's job):** nerd and jock both practice the same anti-discipline from opposite ends — nerd lists his corpus non-hits so nobody cites hex noise as signal; jock names his de-dups so nobody double-claims a counsel find. And both reports end where they should: nerd closes a dead lead with a disambiguation checklist; jock freezes two dead venues with tripwires. The dead stay buried, the fences get dated, and the live play — ghost-hunter's 14 uncollected inboxes via live-browser recovery — is cleanly pointed at, not poached.

**Recommended action:** (1) Fix CONTEXT.md:18 (correct the exit IP, delete the "same infra as fleet inbox" clause, tag both 178.63.67.x IPs as urlquery scan-pool nodes); (2) audit IP_LOG for scan-pool contamination from this lane; (3) leave the operator-activity question open and boring until the next scan or the inbox recovery lands.
