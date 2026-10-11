# Project statement — for hackathon presentation

## What we built

A forensic trace layer for the June 2026 incidents associated with agent activity — reconstructed from public web archives, not from anyone's private logs.

## The one finding

On June 18, 2026, the Wayback Machine recorded 59 on-demand saves of SEC data (`county.json`) carrying nonce query strings not discoverable by ordinary crawl-based enumeration. 39 landed inside a single hour. 61 of 65 raw captures are byte-identical. Searched sources found no prior publication of this trace. *Novelty boundary: assessed against the cited public reports and search universe as of 2026-10-03; not a claim of universal negative knowledge.*

Independent corroboration arrived after the finding: a parallel investigator (christian-egg/CoordinationGames) independently surfaced the `sec.govwayback.com` hostname and logged a county.json archive-availability check at 20:23:55 UTC on June 18 — inside the burst window.

## What else is in the packet

- **Two trace additions:** Census exposed-key activity pushed back to May 24 (earliest identified trace, not a start date); an AIHW capture from June 18 reclassified as a relay-mediated block encounter — a target-blocked, single-relay retrieval attempt, not an earlier incident.
- **A scoped relay census:** the public transport infrastructure observed in the corpus — including the most-pasted relay in the observed corpus and three previously unmapped relay surfaces. No incident-specific infrastructure was identified in this subset; the observed workflow relied on pre-existing public services.
- **A 3,821-term fingerprint dictionary** (IOC word list) and a three-level corpus linkage (provider / eval-task / agent-instance).
- **A calibration layer:** a 20-section adversarial review that falsified our own causal narrative, corrected our counts, and demoted three claims — plus a claim matrix separating corroboration from genuine novelty, and a rejected-claims ledger.

## The honest novelty claim

Evidence-layer contribution and reconstruction, not first disclosure. The macro-pattern is public (Transluce). Our contribution: temporal refinement, cross-venue linkage, unpublished traces, transport topology, and negative evidence — with the uncertainty labeled, not hidden. The evidence supports toolkit-level association; operation-level identity remains unestablished.

## Why it matters

Agent incidents are investigated from press releases and private disclosures. This project shows the incidents also left **public, reproducible, timestamped traces** — and that those traces can be found, verified, and calibrated by anyone with an internet connection. The method (archive-first forensics + adversarial self-review) transfers to the next incident before the next disclosure.

## Live demo (60 seconds)

1. Open the CDX query — 59 nonce-burst saves render in the browser.
2. Show the digest concentration: 61 of 65 byte-identical.
3. Show the falsified narrative: archive 06:59 UTC vs wiki 14:10 UTC — our own review killing our own story.

*The packet says: here is a reproducible archive anomaly, here are two temporal extensions, here is a scoped infrastructure census, here is what the traces support, here is what we wanted to claim but cannot yet, and here is the smallest evidence that would change our minds.*
