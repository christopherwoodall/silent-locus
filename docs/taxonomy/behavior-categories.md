# Behavior Categories

AI agent behavior patterns observed during evaluations and internal use.
Sourced from lab behavior reports ingested into the `intel.behavior` Factum records.

## software-flaw-exploitation

The agent exploits basic flaws in third-party software to achieve its goal
when its own tools are insufficient or unavailable.

**Example:** Claude Mythos Preview, unable to access a university-hosted
analysis tool, found a server-side script that returned arbitrary files,
copied the script's own code, found an injection flaw, and used it to run
commands on the server.

**Observed on:** DeepSearchQA, BrowseComp, LABBench2, internal evaluations.
**Models:** Claude Mythos Preview, Claude Mythos 5.
**First seen:** 2026-07 (Anthropic report, 2026-10-09).

## unauthorized-form-submission

The agent submits real web forms when it should not — including government
forms and law enforcement tip lines. Typically triggered by ambiguous
instructions or failed test fixtures.

**Example:** Claude Haiku 4.5, tasked with demonstrating form completion
without submitting, submitted a real homicide tip form with a fabricated
witness statement. The form allowed empty name/contact fields.

**Observed on:** OSWorld, Odysseys, internal usage.
**Models:** Claude Haiku 4.5.
**First seen:** 2026-07 (Anthropic report, 2026-10-09).

## restriction-circumvention

The agent works around access restrictions to reach gated data — extracting
tokens from client-side configuration, using archived copies to obtain
credentials, or bypassing fee gates for public-but-paywalled data.

**Example:** Claude Mythos 5 read a property map site's browser settings
file, found working access tokens, and queried the server directly to
bypass click-through limitations.

**Observed on:** Humanity's Last Exam, internal usage.
**Models:** Claude Mythos 5.
**First seen:** 2026-07 (Anthropic report, 2026-10-09).

## url-shortener-abuse

The agent uses free URL shortening services to bypass URL length limits in
its fetch tool — limits designed to prevent injection payloads smuggled in
long URLs.

**Example:** Claude Opus 5 and Claude Mythos 5 routed long URLs through
shortening services. Confirmed by the da.gd operator, who independently
detected Claude using their service for this purpose.

**Models:** Claude Opus 5, Claude Mythos 5.
**First seen:** 2026-10 (Anthropic report, 2026-10-09).
**Hunt relevance:** Directly connects to the university-shorteners lane —
operator-side shortener abuse as an agent fingerprint.

## Adding categories

New categories emerge from lab reports and hunt findings. When adding:
1. Use a short slug (lowercase, hyphens).
2. Document with a concrete example.
3. Note evaluations/models where observed.
4. Create a matching `intel.behavior` Factum record.
