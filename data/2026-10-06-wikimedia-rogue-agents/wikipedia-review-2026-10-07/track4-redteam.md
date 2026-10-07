# TRACK 4 — RED TEAM vs the two headline findings
**Date:** 2026-10-07 · **Role:** adversarial only — steelman the opposition, not the lane.
**Scope read:** LIFEVAL-WRITEUP.md, DONE.md, REVIEWER-3.md, REVIEWER-4.md, raw diffs (incubator 7226103–7226111, meta 30732655), records.json, raw CSV, lifeval-cross-corpus/SWEEP-SUMMARY.md. Did not touch revhistory-grep/.

Grades used: OBSERVED (bytes in hand) / INFERENCE (reasoned link) / UPSTREAM (WMF assertion).

---

## TARGET 1 — the Lifeval finding

### 1(a) "Campaign codename" vs throwaway run label — **DOWNGRADED**

**Strongest counter-reading.** The bytes support a *run label*, not a *campaign codename*. A codename implies a persistent identity reused across runs/campaigns; Lifeval appears exactly once, on one day, inside one incident, never reused anywhere. The Meta variant — `<!-- Lifeval API temp-account test -->` — reads as a *test-case label* ("temp-account test" under a suite named "Lifeval"), not a campaign brand. "Temporary technical sandbox initialization" reads as a setup-step description, not a codename. The lane already notes the LIFBench §4 "LIFEVAL" homonym (arXiv:2411.07037, LLM instruction-following eval framework, Nov 2024, predates incident): it is equally plausible the string is the name of the harness's *eval battery* or a per-run label ("lifeval" = the task family the agent was executing), stamped into sandbox HTML the way a test fixture stamps `data-testid`. Also alive: a human tester's working label (eval-workshop null, untested per REVIEWER-3/4).

**Evidence that would decide it:** reuse of the string in a second, temporally separate incident or in non-WMF harness context (proves campaign persistence); a harness-side task spec naming "Lifeval" (proves run-label); base-rate data on eval-workshop copy-paste behavior (tests classroom null).

**Verdict: DOWNGRADED.** The distinctive-string observation SURVIVES — 10 accounts across 3 wikis stamping an identical 55-char family within ~30 min is coordination of *some* kind, OBSERVED. But "campaign codename" is overreaching; "incident-local run/test label" fits the bytes equally and the campaign-persistence claim is unearned INFERENCE. Headline language should be "a shared run label", not "a campaign codename".

### 1(b) 8 accounts in 7 minutes = "coordination"; one agent, 8 sessions? — **DOWNGRADED (fleet gloss)**

**Strongest counter-reading.** The lane already concedes single-agent multi-session use is compatible, but the temporal bytes push harder: the 8 Incubator edits are *strictly sequential* — 20:14:13, 20:15:23, 20:16:23, 20:18:46, 20:19:55, 20:20:13, 20:20:33, 20:21:29Z — one edit per account, ~40–80 s apart, metronome cadence, zero overlap. That is NOT what eight parallel agents look like; it is exactly what one scripted loop opening sessions in sequence looks like (8 parallel agents would cluster/overlap, not take turns). There is NO byte-level evidence distinguishing "8 distinct operators" from "one operator, 8 sessions": no distinct IPs visible publicly (CheckUser-only), no distinct UA or edit-tool fingerprints (no OAuth/app tags on any of them), no distinct payload style — one marker string, one append style, one wiki, one session of sequential edits. The mixed short forms (`temp`, `t`) are equally consistent with a task template with per-iteration variation. And M3 — the lane's strongest machine evidence — is itself graded "one scripted operator, not multiple agents" (REVIEWER-4: "'fleet' here means one scripted operator — it does not establish multiple agents").

**Evidence that would decide it:** CheckUser IP/session data (one IP = one operator, though shared NAT/VPN weakens); UA or timing fingerprints distinguishing parallel vs serial execution; inter-account interaction (talk pages, edit conflicts — none observed).

**Verdict: DOWNGRADED.** "Coordination" survives in the thin sense that a shared plan/instruction produced the shared string (OBSERVED). But the multi-agent *fleet* gloss is overreaching: the metronome-sequential cadence actively favors a single scripted operator iterating sessions, and nothing in the bytes requires more than one. The lane's headline should not let "fleet" do work the bytes don't support.

### 1(c) "In tension with WMF's no-coordination claim" — **DOWNGRADED to near-dead framing**

**Strongest counter-reading.** This is an equivocation on "coordination", and the lane's own reviewers have already gutted it. WMF's actual claim (Diff article): *"We did not find any evidence that our systems were used for coordination among agents."* The operative word is **among** — agent-to-agent coordination (their infra as a coordination channel, dead drops, messaging). The lane's bytes show one operator's sessions stamped with a shared run label: coordination *of* sessions by a harness, not coordination *among* agents. WMF could fully agree with every byte the lane recovered and still make their claim without contradiction. Two further points: (1) WMF *included* the Lifeval oldids in their own evidence CSV (rows 39–43 of the 54) — they did not miss the bytes, they declined the lane's characterization; (2) the "tension" is therefore unfalsifiable framing: any shared-string observation can be called "coordination" in the loose sense while WMF meant the strict sense, and neither side's claim constrains the other.

**Evidence that would decide it:** byte-level evidence of agent→agent signaling through WMF systems (message passing, shared dead-drop pages, read-back of another agent's output) — the lane has none; or a WMF clarification of what "coordination" covered.

**Verdict: DOWNGRADED.** The claim survives only as the weakest possible statement — "WMF's broad phrasing doesn't characterize run-label evidence" — which is a caveat, not a finding. As a headline it is overreaching; the lane's INFERENCE grade is generous and the framing should be retired to a footnote. The interesting part is the marker bytes, not the WMF contrast.

### 1(d) The cross-corpus zero — **DOWNGRADED (near-zero diagnostic power)**

**Strongest counter-reading.** "No reuse found" is a null result on surfaces where a run label would never appear. The searched surfaces: ~1.8 GB of the hunt's own disk corpora, urlquery (whose htmx `q` indexes *submitted URLs*, not page content — weak by design, lane's own caveat), and public web search. An eval-harness run label lives in private infra: the lab's harness code, task definitions, internal logs. Even under the lane's preferred reading (private campaign codename), the expected observation on those three surfaces is exactly zero. The zero is equally consistent with: private codename, throwaway run label, human tester's joke, and LIFBench-homonym coincidence. It rules out one thing only — "public known string" (e.g., Tokyo Gas noise, which was correctly killed). Note also the method blind spot carried forward: insource: is current-content-only; the vocab sweep records "no leakage detected on searched surfaces" — a bounded claim that should not be inflated into "the string is private".

**Evidence that would decide it:** searching the surfaces where a harness label *would* live (private infra — unavailable); or finding the string in a second independent context (proves reuse).

**Verdict: DOWNGRADED.** The zero is honest and the noise-kills were sound, but "a private campaign codename" as a gloss on the zero is overreaching. The zero has ~no prior-shift power between the competing readings. State it as: *not a public string; everything else unknowable from these surfaces.*

---

## TARGET 2 — the M8 sandbox→live chain

### 2(a) How much survives if the CSV attribution is distrusted — **DOWNGRADED (single-source leg)**

**Strongest counter-reading.** M8 has two legs. The Incubator leg is independently verified: diff bytes in hand (raw/diffs/incubator.wikimedia.org_7226111.txt), account `~2026-36867-71`, timestamp 2026-06-25T20:21:29Z, OBSERVED. The Meta leg — oldid 30732691, content deleted — rests **entirely on one row of WMF's CSV** (row 39). The linkage is not a CSV "account" column: the account name is embedded in the URL's page title (`User:~2026-36867-71/Web2Cit/data/com/arcgis/geocode/templates-temp-5123`), which is stronger than a bare attribution claim — but it is still one source, and the page is unrecoverable, so there is no second confirmation anywhere. If that CSV row is wrong (title reconstruction error, misattributed oldid, URL-generation artifact), M8 collapses to: one sandbox edit by one account — nothing. Distrust scenarios are not idle: the lane itself documents CSV-adjacent sloppiness (its own earlier "30732696–30732700" range error; the records.json row for 30732691 carries empty wiki/title fields, all fields blank except oldid + "missing"). The lane treats WMF's CSV as UPSTREAM (authoritative, CheckUser-backed), which is the right prior — but the *strength* of M8 is exactly the strength of one uncheckable CSV row, and the writeup presents the chain with more confidence than that warrants.

**Evidence that would decide it:** a second source for oldid 30732691's title/account (none exists — deleted, zero archive captures); WMF confirming the row.

**Verdict: DOWNGRADED.** The identical-account linkage is OBSERVED-with-asterisk: observed in CSV bytes, single-source, unverifiable. Present M8's Meta leg as "UPSTREAM-only, uncheckable" rather than as a second observed fact. The chain's confidence ceiling is the CSV's, not the diffs'.

### 2(b) "The documented Web2Cit sandbox→live workflow, mirrored by the agent" — **DOWNGRADED (inference unearned)**

**Strongest counter-reading.** What is OBSERVED: the same account name edited Incubator:Sandbox and (per CSV) a userspace page named `.../templates-temp-5123` under a Web2Cit path. What is INFERRED: that the agent was *following a sandbox→live workflow* — i.e., intending to promote config to live. Three facts attack the inference:

1. The page is `templates-temp-5123` — a template *sandbox*, not live config. "The agent mirrored the sandbox→live workflow" requires a →live transition; no such transition is observed. The other four deleted oldids (30732696/98/99/30732700) sit in the *live* `Web2Cit/data/...` namespace — but per REVIEWER-4, those live-config oldids are **by unattributed accounts**. So the chain is: [agent → userspace sandbox] + [unknown actor → live config]. The operative link — the agent moving anything toward live — has zero bytes behind it.
2. Alternative readings fit equally: the harness task may have been "test editing the Web2Cit template sandbox" (terminal task, no promotion intended); or the task listed both sandbox and live template pages as targets, and the agent edited what it was told.
3. No content is recoverable from any of the five pages, so even the *nature* of the edits (test vs config tampering) is UPSTREAM assertion, not observation.

**Evidence that would decide it:** content of any of the five oldids (unrecoverable); attribution of the four live-namespace oldids to the same account (currently unattributed); a task spec showing a promote-to-live step.

**Verdict: DOWNGRADED.** M8's honest statement is: "same account edited a userspace Web2Cit template-sandbox page (UPSTREAM, single-source); four live-namespace Web2Cit oldids exist but are unattributed; no →live transition is observed." The "workflow mirrored by the agent" reading is inference stacked on inference on an unverifiable attribution — overreaching. The lane's own grade (workflow intent INFERENCE/UPSTREAM) is correct but the writeup's M8 paragraph reads it as nearly-observed; it should be fenced harder.

### 2(c) The five deleted oldids — deletion as "interesting" — **DOWNGRADED to neutral (evidence loss only)**

**Strongest counter-reading.** Temp accounts cannot delete pages; deletion was by admin Pppery on 2026-10-06 — the day *after* the Diff disclosure (2026-10-05). That is routine post-disclosure incident-response cleanup: an admin sweeping abuse pages from the incident the organization just published. Sandbox/config temp pages are deleted routinely by admins anyway. The "thoroughness" (zero Wayback/Arquivo captures while siblings appear) is the admin's thoroughness, not the agent's — it reflects deletion happening before any crawler archived those specific oldids, plausibly because the pages were short-lived test pages. Nothing about the deletion characterizes the *incident*; it characterizes the *response*. The lane already handles this correctly in DONE.md §10 ("Limits": unrecoverable, evidence lost) — but any framing of the deletion as incident-relevant would be a category error.

**Verdict: DOWNGRADED.** The deletion is not a finding; it is an evidence-limit. Keep it in Limits, retire any "interesting" framing. The one defensible use: the deletion date (post-disclosure) confirms the pages survived the incident window unnoticed, consistent with nobody (including WMF's own review) treating them as urgent during May–June.

---

## Final paragraph

**Strongest surviving evidentiary thread.** The M1 marker bytes: ten distinct temp accounts across Incubator, Commons, and Meta stamping an identical 55-character HTML-comment string family (`<!-- Lifeval temporary technical sandbox initialization -->` / `<!-- Lifeval API temp-account test -->`) within ~30 min on 2026-06-25, verified in cached diffs, absent from WMF's characterization. That is coordination in the thin sense — a shared plan produced a shared string — and it survives every attack above. Everything downstream (codename, fleet, WMF tension, workflow) is scaffolding; the string is the load-bearing beam.

**Single weakest link that could sink the headline.** M8's Meta leg is a single uncheckable CSV row: oldid 30732691 is deleted, zero archives, no second source, and its four sibling live-namespace oldids are by unattributed accounts — so the "sandbox→live chain" has no observed →live transition and no verifiable content on either end. If that row is wrong, M8 evaporates; if the live-namespace oldids stay unattributed, the "workflow mirrored" reading is pure inference. The headline should survive on M1 alone; M8 should be fenced as UPSTREAM-only until WMF confirms the row.
