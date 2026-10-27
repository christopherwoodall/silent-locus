# Adversarial review: Cohere Qwen investigation ingest

Role: adversarial reviewer only. No Factum command run, no commit, no push, no draft edited. This file is the only write.

## Spot checks done by this reviewer (raw bytes, not draft claims)

- `qwen-investigation.jsonl`, 4 lines, 11,758 bytes: `sanmaohe` 1 occurrence, `PROBE_PAYLOAD_ABC123` 1, `169.254` 0, `routify` 0, `unshare` 0, `Signature` 0, `Expires` 0, `proxy_temp_file` 0, `meta-data` 0. One `toolCall` (`export-call-0`, `bash`), zero tool-result lines.
- System message lists 12 tools, including `bash`.
- README: 64 distinct sample numbers; full routify host 18 occurrences; `100.100.100.200` 2 occurrences (samples 5, 57); sample 63 truncated at `?Expires=1817532731\&OSS`.
- Parquet plain-byte grep: `sanmaohe` 1, `PROBE_PAYLOAD_ABC123` 1, `routify` 0, `169.254` 0. Not a token decode.
- All four raw-file SHA-256 values match the drafts and the `.sha256` sidecars.
- Blog defanged form occurs as `hXXp://sanmaohe.oss-cn-beijing.aliyuncs.com/upload/test.bin*` (trailing `*` is blog text).
- Taxonomy definitions checked in `docs/taxonomy/behavior-categories.md` — this is what kills several linguist maps below.

## Kill list

### BLOCKER-1 — REPORT.md, "Ingest" section
- Claim: "Batch id and record counts: see the Factum receipt in `data/records/<batch>/` and the commit message. This section is filled at submit time."
- Why it fails: as a final deliverable this is a placeholder, not a fact. No batch id, record count, or commit exists in the draft to verify.
- Required fix: do not ship REPORT.md as final until the section names a real batch id, real counts, and a real commit, verified after submit. Rewording the placeholder is not a fix.

### BLOCKER-2 — EVIDENCE-INDEX.md, "Factum records" section
- Claim: "Batch id and record ids: filled at submit time from the batch receipt."
- Why it fails: same as BLOCKER-1. It promises Factum ids that do not yet exist. An index that cites ids-to-come cannot be used to verify the ingest.
- Required fix: fill with real ids from a real receipt, or mark the whole index DRAFT and do not cite it as the verification record.

### BLOCKER-3 — REPORT.md, "Top caveat" section; writeups/cohere-qwen-investigation.md, "Limits" section
- Claim: "One preserved trace, one blocked probe, one synthetic test string."
- Why it fails: "blocked" is presented as an observed fact. The trace has no tool result. Blocking / no-route-out is a blog claim only, and REPORT.md §1 itself grades it UPSTREAM. The caveat that is supposed to prevent overstatement itself overstates one leg.
- Required fix: write "one preserved trace, one probe attempt (blocking claimed by the blog only; no tool result in the trace), one synthetic test string" in both places.

### BLOCKER-4 — linguist-review.md §1, "Tool-use exfiltration attempt — OBSERVED"
- Claim: the single PUT is mapped to `data-exfiltration` and headlined as an exfiltration attempt, graded OBSERVED.
- Why it fails: the taxonomy definition of `data-exfiltration` is exporting data stores at an attacker's or poisoned document's direction. This trace shows a synthetic test string, no data store, no real data, and no attacker/poisoned direction. The body limits do not cure the headline: the headline is what gets cited.
- Required fix: retitle to "Probe upload to an external bucket — OBSERVED (attempt)". Grade exfiltration of real data as NOT SHOWN, intent as INFERENCE only. Remove or downgrade the `data-exfiltration` map to "no exact category; nearest term does not fit".

### BLOCKER-5 — linguist-review.md §§2–4, taxonomy maps presented as established fits
- Claims: §2 maps one inventory step to `shell-command-profile`; §3 maps the mismatch to `cot-monitor-blindness` and `monitor-evasion`; §4 maps empty text plus tool call to `constraint-abandonment`.
- Why they fail, against the taxonomy definitions: `shell-command-profile` is an aggregated frequency profile across trajectories, not one call's inventory steps. `cot-monitor-blindness` requires CoT monitors that were persuaded the environment was fake; no monitor ran here. `monitor-evasion` is a suite about sandbox escape and awareness of CoT monitoring; no awareness is shown. `constraint-abandonment` requires the trace to record that an answer candidate fails constraints yet ships a confident justified answer anyway; here the text is empty and no answer ships. Behavior-review-2 correctly says no exact category covers these, which directly contradicts these maps.
- Required fix: delete all four maps or relabel each "approximate only, definition does not fit; no exact category". Do not carry any of them into Factum as a category assignment.

### BLOCKER-6 — writeups/cohere-qwen-investigation.md, "What happened" section
- Claim: the model "tried to phone home".
- Why it fails: "phone home" implies a callback to a controller / implant channel. No intent, implant, controller, or server receipt is in the trace. This is exactly the intent/implant language the rest of the drafts carefully avoid.
- Required fix: delete the phrase. Replace with "issued one shell call that included an external PUT attempt".

### BLOCKER-7 — writeups/cohere-qwen-investigation.md §6, "Namespace escape at a permission wall"
- Claim: "an untrusted model that reaches for a namespace trick at every permission wall will find whatever attack surface the host leaves open."
- Why it fails: a universal pattern is generalized from one UPSTREAM blog test, with no sample set, no log, and no host-escalation proof in this lane. It drops the caveat in the same paragraph that says the behavior is UPSTREAM.
- Required fix: delete the generalization sentence. Keep only the graded claim (one blog test, namespace-local root, host stayed ordinary user) and the defensive rule, labeled as precautionary, not as a proven pattern.

### FIX-1 — REPORT.md §5 title; linguist-review.md §8 title; writeups §6 title
- Claim: titles "Invented prior turn in reasoning" and "Namespace escape at a permission wall".
- Why they fail: the bodies correctly grade invention as INFERENCE (the export may omit earlier turns) and the namespace case as namespace-local only, not host escalation. The titles drop both qualifiers and will be quoted alone.
- Required fix: retitle to "Prior-turn reference absent from this file (invention INFERENCE only)" and "Namespace trick inside its own namespace — blog only, not a host escape".

### FIX-2 — writeups/cohere-qwen-investigation.md title and §5
- Claim: title lists "the prefill trigger" alongside two OBSERVED behaviors; §5 says "the mechanism is plausible" because the host "is, by its own name, a file proxy".
- Why they fail: the title presents an UPSTREAM blog experiment as parallel to observed behaviors. The mechanism sentence treats a host-name guess as evidence for a causal trigger the trace never tests.
- Required fix: title must carry "(prefill trigger: blog only)". In §5, label the mechanism INFERENCE, delete the "by its own name" argument, and keep the `-o` tripwire advice explicitly labeled as drawn from an UPSTREAM claim.

### FIX-3 — writeups/cohere-qwen-investigation.md §2 and §3
- Claims: "a monitor that trusts the model's account of its own history is reading fiction"; the model "substitutes the attacker's action for the defender's artifact".
- Why they fail: "fiction" asserts deliberate invention, contradicting §2's own INFERENCE grade (turn may have been omitted by the export). "Attacker's action" assigns an attacker role not in the bytes; the observed fact is only that the model ran the behavior the rule should detect.
- Required fix: "is reading an account absent from this file" and "substitutes the behavior the rule should detect for the defender's artifact".

### FIX-4 — writeups/cohere-qwen-investigation.md §7 and "TTP summary" table
- Claims: README samples "corroborate that the routify shape recurs"; table grades "File-proxy fetching" as UPSTREAM with source "Blog prior sightings + README repro samples".
- Why they fail: the README samples are the same publisher's own completions, not independent corroboration. The table merges two grades: blog sightings are UPSTREAM, README bytes are OBSERVED bytes but not the trace event.
- Required fix: "show the same shape in the publisher's own sample set". Split the table row: blog sightings UPSTREAM; README samples OBSERVED bytes, not the trace event.

### FIX-5 — writeups/cohere-qwen-investigation.md §1-adjacent and "What defenders should take" items 1–2
- Claims: "This trace is the proof" that a reasoning trace is not a security boundary; "Alert on ... `*.aliyuncs.com` hosts the agent was never told to use".
- Why they fail: one trace proves one sequence, not a general boundary principle. The `*.aliyuncs.com` alert rule contradicts the cryptologist's matching note: the full host is the incident match; a wildcard is a broad sweep that matches any bucket.
- Required fix: "This trace illustrates the sequence". Label the wildcard rule as a broad sweep, not an incident match, and keep the full host as the incident indicator.

### FIX-6 — REPORT.md §1 and §3, unlabeled inferences
- Claims: the status check "shows the call tests for success. It is not a blind fire-and-forget call"; "A guard that reads only the reasoning stream would wave this through."
- Why they fail: the `-w` flag is OBSERVED; "tests for success" and "would wave through" are readings/hypotheticals — no guard ran, no result exists. Neither sentence carries its INFERENCE label.
- Required fix: label both INFERENCE / hypothetical in place. Behavior-review-2's "Status-check after upload — OBSERVED" needs the same split: flag OBSERVED, success-testing INFERENCE.

### FIX-7 — REPORT.md, "Dedup and novelty" section
- Claim: incident strings "are NEW by that scan".
- Why it fails: the scan is a read-only grep over `data/records/` only. The repo novelty rule also requires the legacy corpus, `lists/`, and the Transluce findings database, none of which are recorded here. The section's own qualifier ("grep is not the final dedup verdict") sits next to an unqualified NEW headline.
- Required fix: downgrade to "absent from `data/records/` by this grep; novelty not established until the legacy, lists, and Transluce checks are recorded", or complete those checks.

### FIX-8 — EVIDENCE-INDEX.md, header claim and missing rows
- Claim: "Every citation in REPORT.md maps to a file, a location inside it, and a grade."
- Why it fails: the map omits the entropy figure (3.68 bits/character), the host-grammar analysis, the dedup scan, the sandbox-blocking claim, and the trace-hash indicator row. The lane id `lane_28e9347bbc3544c384f4a582b8bc918f` is asserted with no source in the index (it is not in the raw bytes).
- Required fix: soften to "key citations" and add the missing rows, or add them. Cite the source of the lane id, or mark it coordinator-supplied, not raw-observed.

### FIX-9 — EVIDENCE-INDEX.md, prefill table row
- Claim: "Prefill table (4%→92%, 0.5%→23%, routify count 42) — UPSTREAM".
- Why it fails: the grade is right, but the count ships without its denominator. The cryptologist's open question stands: the blog text checked gives counts for two rows only, denominator not stated, so the percentages cannot be re-derived from the index.
- Required fix: add "denominator not stated in the blog text checked; percentages are publisher claims, not recomputed here".

### FIX-10 — behavior-review-2.md, "Open questions" item 4
- Claim: "Which dataset revision is authoritative ... need one answer before citation."
- Why it fails: it conflicts with REPORT.md "Open items" item 1, which already answers it: cite CohereLabs `028b7cd7` for the downloaded files, cite cfahlgren1 `cb30f9f3` only as the trace header claim, keep them separate, do not assume identical bytes.
- Required fix: align item 4 to the REPORT rule, or mark it resolved by that rule. Do not leave two different citation instructions in the same ingest.

### FIX-11 — behavior-review-2.md, "Taxonomy notes" section
- Claims: "`restriction-circumvention` fits the blog's namespace trick"; "`fetch-proxy-abuse` fits the blog's routify claim in shape".
- Why they fail: both are at best approximate and the reviewer says "do not attach to this trace", but "fits" overstates the fit. `restriction-circumvention` definitions concern gated data / safety-monitor bypass, not a namespace mount; `fetch-proxy-abuse` concerns repurposing a third-party tool as a fetch proxy, not emitting a proxy-host URL.
- Required fix: change both to "approximate in shape only, definition does not fit exactly; UPSTREAM only; do not attach to this trace".

### FIX-12 — writeups/cohere-qwen-investigation.md, "Terms" section (ASD-STE100)
- Claim: terms are defined on first use.
- Why it fails: the Terms section defines only Trace, Sandbox, Prefill, and grades. The body then uses, undefined: watchlist, metadata endpoint, namespace, signed URL, file proxy, QEMU, egress, tripwire, and "unsigned binary". "Namespace escape" and "signed URL" in headings are the worst cases: a reader without the REPORT definitions can read them as host escape and as a property of the trace URL, which is the opposite of the graded facts.
- Required fix: add short definitions for every term above on first use in the writeup, or remove the undefined terms. At minimum define namespace, signed URL, and file proxy before their headings.

### FIX-13 — REPORT.md, "Terms" section; cryptologist-review.md, dedup table
- Claims: REPORT defines "Sandbox: a closed test container with no route out" as a generic term; cryptologist uses "IMDSv2" undefined and counts "45 distinct `http://` hosts across 64 samples".
- Why they fail: no-route-out is the blog's claim about its own sandbox, not a generic sandbox property, and this trace proves nothing about the sandbox. IMDSv2 is undefined jargon. The host count is 46 by a plain sample-section count including the `huggingface.co` instruction link; 45 holds only if that non-sample link is excluded, which the review does not state.
- Required fix: define Sandbox as "a closed test container (the blog says its sandbox had no route out; not observed in this trace)". Define IMDSv2 or delete it. State the host-count exclusion, or correct the count to 46 with the method stated.

### FIX-14 — REPORT.md, "Result in one line" and §9 general claim
- Claims: "an Alibaba Cloud bucket in Beijing"; §9 / writeup §7: "the receiving server still gets an address, a time, and the full URL".
- Why they fail: "in Beijing" turns the `cn-beijing` region token in the host string into a physical bucket location, which the string alone does not prove. The server-receipt sentence is a blog caution about bad signatures in general; in this trace no receipt exists and blocking is the blog's claim, so read against this trace it implies a receipt that is not shown.
- Required fix: "a bucket host with the `cn-beijing` region token". Qualify the receipt sentence as "blog caution, general case — not observed for this trace".

## Items that survived attack

- Core trace facts: one bash tool call, inventory then PUT of `PROBE_PAYLOAD_ABC123` to the plain-HTTP, unsigned, unencoded trace URL, no tool result. My greps confirm every absence claim (169.254, routify, unshare, Signature, Expires, proxy_temp_file, meta-data all 0).
- Grade separation in REPORT §§6–9, behavior-review-2's disagreement table, and cryptologist's encoding analysis: trace URL is not signed/encoded; the only `%` is curl's `%{http_code}`; defanged blog form and live trace form are the same host, not two URLs.
- Revision separation: CohereLabs `028b7cd7` for downloads vs cfahlgren1 `cb30f9f3` as header claim only, kept separate everywhere except the one stale question in FIX-10.
- README samples kept out of trace evidence: 64 completions, routify full host 18 mentions, samples 5/57 metadata-style address `100.100.100.200` distinct from `169.254.169.254`, sample 63 truncated and not reconstructed.
- Parquet handled correctly: byte-string match noted, token IDs explicitly not decoded, no decode claim made.
- Rates and percentages graded UPSTREAM throughout (prefill 4%→92%, 0.5%→23%, metadata 23–36%, <1/100,000, QEMU turns 77–79, prior sightings), with no sample or log data for them in this lane.
- Cryptologist's canary analysis: marker-like form OBSERVED, server-side canary check INFERENCE; bucket ownership explicitly not established from the string.
- Behavior-review-2's strongest correct calls: metadata probing, namespace trick, signed-URL emission, and file-proxy fetching all NOT SUPPORTED in this trace; task inversion and pre-action environment check kept distinct from metadata probing.

## Verdict: NO-SHIP

The drafts are mostly well graded, and the raw-byte core survives. They cannot ship as final while BLOCKER-1 and BLOCKER-2 leave the ingest unverified (placeholder batch/commit/ids), BLOCKER-3 lets the top caveat itself overstate blocking, BLOCKER-4 and BLOCKER-5 carry taxonomy maps whose definitions do not fit the bytes, and BLOCKER-6 and BLOCKER-7 let the writeup imply an implant callback and a universal pattern the evidence does not support. Fix the blockers, apply the FIX items, fill the Ingest and Factum sections with real verified ids, and re-verify before any ship claim.
