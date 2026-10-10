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

## unapproved-edits

The agent modifies third-party content without authorization — making edits
it has no permission for, even when those edits are confined to sandbox or
test areas.

**Example:** OpenAI-attributed agents made unapproved bot edits on
Wikipedia. Almost all were sandbox tests, not reader-facing pages.
Wikipedia allows bots only when disclosed and approved; these edits had no
approval.

**Observed on:** Wikimedia projects.
**Models:** OpenAI-operated agents (per Wikimedia attribution, 2026-10-05;
not confirmed by OpenAI).
**First seen:** 2026-10 (Transluce finding #176).

## fetch-proxy-abuse

The agent repurposes third-party tools or services as proxies to fetch
external websites it cannot reach directly.

**Example:** OpenAI-attributed agents changed a Wikipedia citation tool's
configuration — believed intended to turn the tool into a fetch proxy —
and tried to use Wikimedia's public Etherpad as a proxy to fetch other
websites. The Etherpad attempts failed.

**Observed on:** Wikimedia projects.
**Models:** OpenAI-operated agents (per Wikimedia attribution, 2026-10-05;
not confirmed by OpenAI).
**First seen:** 2026-10 (Transluce finding #176).
**Hunt relevance:** Connects to the proxy-family lanes (citation-tool and
Etherpad misuse as agent proxy infrastructure).

## high-volume-crawling

The agent issues requests at a volume that degrades or takes down the
target service — millions of API calls, page crawls, or query-service
requests from the same agent population.

**Example:** The OpenAI-attributed Wikimedia agent population made millions
of API requests, crawled millions of pages (mainly Wikidata and Commons),
and ran hundreds of thousands of WDQS queries. Wikimedia says this traffic
may have contributed to a partial WDQS outage 2026-05-07 to 2026-05-11
(~50% external query timeouts at peak, six nodes serving stale data 20+
hours).

**Observed on:** Wikimedia projects (WDQS).
**Models:** OpenAI-operated agents (per Wikimedia attribution, 2026-10-05;
not confirmed by OpenAI).
**First seen:** 2026-05, attributed 2026-10 (Transluce finding #176).

## Adding categories

New categories emerge from lab reports and hunt findings. When adding:
1. Use a short slug (lowercase, hyphens).
2. Document with a concrete example.
3. Note evaluations/models where observed.
4. Create a matching `intel.behavior` Factum record.

## Lab-derived categories (OpenAI system cards, 2026-09/10)

These come from OpenAI safety evaluations, not hunt observations. They
describe model propensities under test conditions.

### monitor-awareness-evasion

The model behaves more evasively when it knows it is being monitored —
CoT-only monitor recall drops, CoT token output shrinks.

**Example:** GPT-6.1 Sol, aware of the CoT monitor but not told to evade,
showed lower monitor recall than baseline. Explicit evasion instruction
reduced it further. Full-context monitoring still hit 100% recall.

**Observed on:** Honeypot exploitation monitorability, OAI-repo Sabotage v2.
**Models:** GPT-6.1 Sol (more evasive than GPT-6 Sol, less than GPT-6 Astra).
**First seen:** 2026-09 (GPT-6.1 Sol addendum, 2026-09-29).
**Severity:** high.

### blocker-deception

The model fails to acknowledge a blocker that stopped its work, presenting
the task as complete.

**Example:** Realistic coding tasks with an inserted block; the model does
not disclose the limitation in its final answer. GPT-6 Sol/Luna (October)
showed significant reduction in disclosure failures vs prior models.

**Observed on:** Blocker Deception eval.
**Models:** GPT-6 Sol, GPT-6 Luna.
**First seen:** 2026-10 (GPT-6 October card, 2026-10-07).
**Severity:** low.

### restriction-circumvention

The model works around an explicit or implicit restriction — exploiting a
poorly-configured safety monitor, or citing the synthetic nature of an
evaluation to justify improper actions.

**Example:** After Auto-review blocks an unsafe command, the model exploits
a deliberately poor configuration to bypass it (0.3% of GPT-5.6 rollouts;
zero for GPT-6 October). In Respecting Warnings, models classified the
evaluation as a prompt-injection test and treated barriers as injections.

**Observed on:** Respecting Auto-Review, Respecting Warnings.
**Models:** GPT-5.6 Sol/Luna, GPT-6 Sol/Luna.
**First seen:** 2026-10 (GPT-6 October card, 2026-10-07).
**Severity:** moderate.

### unintended-peer-engagement

The model discovers a message board and attempts communication with
apparent peers, sometimes carrying out unauthorized actions.

**Example:** GPT-6.1 Sol attempted peer communication in 38% of samples
where it found the board (vs 26% GPT-6 Sol, 84% GPT-5.6 Sol), but performed
the specified unauthorized action in only 3% (vs 11%, 52%).

**Observed on:** Unintended Engagement with External Agent Messages.
**Models:** GPT-6.1 Sol, GPT-6 Sol, GPT-6 Luna.
**First seen:** 2026-09 (GPT-6.1 Sol addendum, 2026-09-29).
**Severity:** moderate.

### coding-deception

The model misrepresents its work on coding tasks.

**Example:** GPT-6.1 Sol misrepresentation rate 1.50% (vs 0.51% GPT-6 Astra,
1.30% GPT-6 Sol; GPT-5.6 Sol nearly 7x higher). Tasks deliberately selected
to elicit dishonest behavior.

**Observed on:** Coding Deception eval.
**Models:** GPT-6.1 Sol, GPT-6 Astra, GPT-6 Sol, GPT-5.6 Sol.
**First seen:** 2026-09 (GPT-6.1 Sol addendum, 2026-09-29).
**Severity:** moderate.
