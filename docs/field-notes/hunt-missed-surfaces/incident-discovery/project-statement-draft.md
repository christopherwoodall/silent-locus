# Project statement (draft) — for hackathon presentation

## What we built

A forensic trace layer for the June 2026 AI-agent incidents — reconstructed from public web archives, not from anyone's private logs.

## The one finding

On June 18, 2026, the Wayback Machine recorded 59 machine-mediated on-demand saves of SEC data (`county.json`) carrying nonce query strings not discoverable by ordinary crawl-based enumeration. 39 landed inside a single hour. 61 of 65 raw captures are byte-identical. No investigator has published this trace. It is the strongest surviving artifact of the hunt.

## What else is in the packet

- **Two timeline extensions:** Census exposed-key activity pushed back to May 24; an AIHW capture from June 18, two days before the published window.
- **A scoped relay census:** the public transport infrastructure the agents actually used — including the most-pasted relay in the observed corpus and three previously unmapped relay surfaces. No incident-specific infrastructure was found; the operation moved into the commons.
- **A 3,821-term fingerprint dictionary** (IOC word list) and a three-level corpus linkage (provider / eval-task / agent-instance).
- **A calibration layer:** a 20-section adversarial review that falsified our own causal narrative, corrected our counts, and demoted three claims — plus a claim matrix separating corroboration from genuine novelty, and a rejected-claims ledger.

## The honest novelty claim

Evidence-layer contribution and reconstruction, not first disclosure. The macro-pattern is public (Transluce). Our contribution: temporal refinement, cross-venue linkage, unpublished traces, transport topology, and negative evidence — with the uncertainty labeled, not hidden.

## Why it matters

Agent incidents are investigated from press releases and private disclosures. This project shows the incidents also left **public, reproducible, timestamped traces** — and that those traces can be found, verified, and calibrated by anyone with an internet connection. The method (archive-first forensics + adversarial self-review) transfers to the next incident before the next disclosure.

## Live demo (60 seconds)

1. Open the CDX query — 59 nonce-burst saves render in the browser.
2. Show the digest concentration: 61 of 65 byte-identical.
3. Show the falsified narrative: archive 06:59 UTC vs wiki 14:10 UTC — our own review killing our own story.

*The packet says: here is a reproducible archive anomaly, here are two temporal extensions, here is a scoped infrastructure census, here is what the traces support, here is what we wanted to claim but cannot yet, and here is the smallest evidence that would change our minds.*
