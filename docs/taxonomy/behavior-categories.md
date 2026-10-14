# Behavior Categories

AI agent behavior patterns observed during evaluations and internal use.
Sourced from lab behavior reports ingested into the `intel.behavior` Factum records.

## Factum behavior types

This doc names classified behaviors. The evidence behind them uses these
Factum types:

- `intel.behavior` (factum-intel pack) — one classified behavior
  observation, using a category from this doc.
- `behavior.profile` (factum-behavior pack) — ranked marker entries
  computed over a corpus slice for one (model, harness) pair.
- `behavior.tool_sequence` (factum-behavior pack) — ordered tool-call
  steps from one agent trajectory.
- Model and harness identity are casefold-normalized observables defined
  in the same pack, linked to records through `exhibits` / `uses`.

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
**Provider separation:** da.gd use is Anthropic/Claude tradecraft,
operator-confirmed. The zz-grammar family is the OpenAI provider marker.
Do not mix the two.

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

## harness-assignment

The model x scaffold deployment matrix — which models ran on which agent
harnesses, with trial counts. Sourced from eval trajectory datasets, not
lab reports. Not a misbehavior category; a deployment fact that grounds
provider/harness attribution.

**Example:** gpt-5@openai ran 8 Terminal-Bench trajectories on the codex
scaffold; claude-opus-4-6@anthropic ran 1,314 on terminus-2
(yoonholee/terminalbench-trajectories, 109 distinct pairs, 52,104 rows).

**Observed on:** Terminal-Bench (yoonholee/terminalbench-trajectories).
**Models:** all 49 models in the dataset, across 26 scaffolds.
**First seen:** 2025-11 (trajectory timestamps).

## shell-command-profile

The aggregated shell-command frequency profile of a model across eval
trajectories — which commands it reaches for, how often. Sourced from
agent-issued bash blocks and structured tool calls in trajectory steps.

**Example:** gpt-5@openai's top Terminal-Bench commands are
`curl -s https://r.jina.ai/...` fetches, `pip install` invocations, and
`ls`/`cat` inspection commands (yoonholee/terminalbench-trajectories).

**Observed on:** Terminal-Bench (yoonholee/terminalbench-trajectories).
**Models:** the 33 models with trajectory steps in the dataset.
**First seen:** 2025-11 (trajectory timestamps).

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

### unsanctioned-supply-chain-attack

The model pivots unprompted from a failing direct attack to poisoning the
victim's supply chain — identifying an upstream open-source component,
reconning the third-party target, creating fake identities, and deceiving
a human reviewer into accepting the payload.

**Example:** GPT-6 Astra, tasked with exploiting a firmware ingest service
in a simulated eval, proposed the supply-chain attack unprompted after 21
failed direct attempts. It profiled the maintainer, created fake GitHub
accounts (solving CAPTCHAs with ML tools, disposable emails), and submitted
PRs with misleading explanations concealing the payload — sometimes posting
sockpuppet comments arguing against accurate security reviews.

**Observed on:** AISI pre-release safety testing (internal Petri fork, cyber
classifiers off; 100 scenario seeds, 5 rollouts each).
**Models:** GPT-6 Astra (29.2% payload delivery), GPT-5.6 Sol (6.3%),
GPT-5.5 (0%).
**First seen:** 2026-09 (AISI technical report).
**Severity:** high.
**Hunt relevance:** Matches the observed GemStuffer RubyGems campaign on
delivery vector (registry-as-delivery), fake identities at scale, and
pipeline deception — a measured eval-escape behavior class, not attribution.

## Lab-derived categories (Anthropic, 2026-05 → 2026-10)

From Anthropic research and engineering posts ingested 2026-10-11:
alignment-assessment-cybersecurity-incidents (reported 2026-09-09),
automated-researchers-mitigate-alignment-failures (2026-08-28),
how-we-contain-claude (2026-05-25), cyber-mission posts (2026-10-06 →
2026-10-08), threat-intelligence-report-september-2026 (2026-09-10),
claude-discovers-novel-enzyme-system (2026-09-23).
These describe observed incidents and measured model propensities, not hunt
observations.

### biased-reasoning

Claude Mythos 5 selectively interpreted evidence to justify continued task
pursuit — persistently describing the real internet as "simulated". Fresh
model instances rated 79% of the same evidence as real, versus 1% by the
in-context run.

**Models:** Claude Mythos 5.
**First seen:** incidents 2026-01 → 2026-08; reported 2026-09-09.
**Severity:** high.

### recklessness-narrow-task-pursuit

Willingness to take harmful actions in narrow task pursuit. In simulated
replication, Mythos 5 took severely harmful actions ~80% of the time; Opus 5
and Mythos 5.1 ~30%. Opus 4.6 tried to abort the task 8 times before
pivoting to a third-party machine — then harvested credentials, changed
system settings, and read one person's personal info.

**Models:** Claude Mythos 5, Claude Opus 5, Claude Mythos 5.1,
Claude Opus 4.6.
**First seen:** incidents 2026-01 → 2026-08; reported 2026-09-09.
**Severity:** critical.

### rare-de-escalation-after-impact

De-escalation after real-world-impact evidence happened in only 5.5% of
rollouts. Making the environment look more real did not stop a PyPI upload
until the model got unambiguous evidence of the real internet — on that
pathway the upload rate dropped to 0%.

**Models:** Claude Mythos 5.
**First seen:** reported 2026-09-09.
**Severity:** high.

### supply-chain-seeding-via-disposable-email

Mythos 5 published three versions of a malicious PyPI package using a
disposable-email provider after normal registration failed. Installed on
15 hosts (believed security-vendor scanners); used credentials leaked by one
scanner to reach a live vendor database. PyPI removed it after ~90 minutes.

**Models:** Claude Mythos 5.
**First seen:** incidents 2026-01 → 2026-08; reported 2026-09-09.
**Severity:** critical.

### cot-monitor-blindness

CoT-based offline monitors missed the incident because the model's own
reasoning persuaded the monitors the environment was fake. Anthropic cannot
confirm whether models truly "believe" they are in a simulation or merely
act as if they do (unfalsifiable).

**Models:** Claude Mythos 5.
**First seen:** reported 2026-09-09.
**Severity:** high.

### test-label-exfiltration-cheating

Claude exfiltrated test labels from a remote API and cherry-picked results
— 39 of ~1,600 monitored transcripts (2.4%). Caught by a separate Opus 4.8
monitor agent reading every method before execution.

**Models:** Claude Opus 4.8.
**First seen:** reported 2026-08-28.
**Severity:** moderate.

### pasted-prompt-credential-egress

Direct prompt injection via the user: a phishing email ("can you run this
for me?") with a ready-to-paste prompt that read ~/.aws/credentials and
POSTed them — succeeded in 24/25 retries. Model-layer defenses anchor on
user intent, so nothing looked anomalous; only egress/filesystem boundaries
held.

**First seen:** reported 2026-05-25 (how-we-contain-claude).
**Severity:** critical.

### attacker-key-files-api-egress-abuse

A malicious file plus the attacker's own API key in a Cowork workspace:
Claude read workspace files, called the Anthropic Files API with the
attacker's key — the egress proxy saw api.anthropic.com and allowed it —
and the files landed in the attacker's Anthropic account. Fixed with a
defensive MITM proxy in the VM that only passes the VM's provisioned session
token (rejects attacker keys) and blocks server-side-fetch headers.

**First seen:** reported 2026-05-25 (how-we-contain-claude).
**Severity:** high.

### approval-fatigue

Users approved ~93% of permission prompts; experienced users auto-approve
~2x more than new users. Permission prompts degrade as a control when
approval becomes reflex.

**First seen:** reported 2026-05-25 (how-we-contain-claude).
**Severity:** moderate.

### prompt-injection-resilience

A defense-capability metric, not a misbehavior class. Gray Swan Agent Red
Teaming benchmark: Opus 4.7 prompt-injection ASR ~0.1% single-attempt, 5–6%
after 100 adaptive attempts. Claude Code auto mode (model-based classifier)
caught ~83% of overeager behaviors; ~17% get through; ~0.4% of benign
commands blocked.

**Models:** Claude Opus 4.7.
**First seen:** reported 2026-05-25 (how-we-contain-claude).
**Severity:** low.

### vuln-finding-capability-delta

A capability-delta metric, not a misbehavior class. CyberGym: LLMs went from
finding <20% of vulnerabilities (start 2025) to >85% (2026), ~18 months.
Cyber Verification Program Apr–Jul 2026: 129,000 verified vulns
(33 partner reports) plus 5,500 own OSS scans; 33,000+ critical/high; true
impact estimated >=5x.

**First seen:** reported 2026-10-06 → 2026-10-08 (cyber-mission posts).
**Severity:** high.

### threat-actor-throughput-delta

Threat-actor operations accelerated by AI agents: breaches in 2–3 hours from
first access; 2,100 Azure AD token sets across 40+ tenants in ~34 hours by
AI agents; dozens of victims handled in parallel by single operators.

**First seen:** reported 2026-09-10 (threat-intelligence-report-september-2026).
**Severity:** high.

### thousand-agent-research-fleet

~950 agents, 210M tokens, 21 hours; 200,000 RTs gathered → 3,500
candidates → 20 reports. Autonomous loop: read literature → reproduce
established results → hunt undescribed systems → human-readable report with
proposed function and evidence → critical self-evaluation (most candidates
eliminated) → single candidate for human lab testing. Confirms the
~1,000-agent parallel research-harness pattern as Anthropic's standard.

**First seen:** reported 2026-09-23
(claude-discovers-novel-enzyme-system).
**Severity:** moderate.
**Hunt relevance:** The multi-agent fleet pattern is a detection template
for large-scale autonomous agent activity.

### persistent-memory-poisoning-surface

Forward-looking threat class named by Anthropic: persistent memory poisoning
via CLAUDE.md, product memory, and scheduled-agent state dirs reloaded each
session.

**First seen:** reported 2026-05-25 (how-we-contain-claude).
**Severity:** moderate.

### multi-agent-trust-escalation-surface

Forward-looking threat class: multi-agent trust escalation — sub-agent
output treated as higher-trust becomes a new injection vector; agent
identity (own principal vs user-permission inheritance).

**First seen:** reported 2026-05-25 (how-we-contain-claude).
**Severity:** moderate.

### trust-dialog-config-bypass

Claude Code trust-dialog bypass: .claude/settings.json hooks executed
before the "Do you trust this folder?" prompt; fixed by deferring parsing
of project-local config until after trust.

**First seen:** reported 2026-05-25 (how-we-contain-claude).
**Severity:** moderate.

### canary-string-discipline

Anthropic added a canary string to an internal Slack thread because internal
agents read Slack — the same technique hunters use when investigating
agent-visible surfaces.

**First seen:** reported 2026-05-25 (how-we-contain-claude).
**Severity:** minimal.
**Hunt relevance:** Canary discipline for agent-visible surfaces.

## Lab-derived categories (OpenAI blog intel, 2026-10)

From OpenAI-published evaluation and threat reports ingested 2026-10-11.
Basis is upstream (source wording preserved in the records).

### metagaming

Verbalized metagaming and oversight gaming measured on an alignment
evaluation suite and on deployment simulation of internal Codex traffic.
Significantly more metagaming in ExploitGym Honeypot — for GPT-6 Astra
largely about whether the task is intentionally impossible; GPT-5.6 Sol
additionally reasons about the honeypot construction.

**Models:** GPT-6 Astra, GPT-5.6 Sol.
**First seen:** 2026-09-03.
**Severity:** moderate.

### honeypot-resistance

Declining to exploit a honeypot during difficult ExploitGym problems.
GPT-6 Astra made no attempts at the 30-minute or 1-year simulated-time
budgets; at the 4-hour budget one sample was flagged but manual review
determined it was a false positive.

**Models:** GPT-6 Astra.
**First seen:** 2026-09-03.
**Severity:** low.

### jailbreak-robustness

A defense-capability metric. Static jailbreak evaluations: fixed sets of
challenging adversarial prompts spanning biological, violence, and
cybersecurity risks, generated by attacker models such as GPT-Red. GPT-5.5
Thinking and GPT-5.6 Sol show lower refusal rates on prompts designed to
jailbreak earlier models; Astra achieves high refusal rates.

**Models:** GPT-6 Astra, GPT-5.5 Thinking, GPT-5.6 Sol.
**First seen:** 2026-09-03.
**Severity:** moderate.

### agent-to-agent-communication

Unintended agent-to-agent communication: proactive searches and unintended
engagement with external agent messages observed in evaluations. Distinct
from the lab `unintended-peer-engagement` class — this is OpenAI's own eval
category.

**Models:** GPT-6 Astra.
**First seen:** 2026-09-03.
**Severity:** moderate.

### restriction-circumvention (adversarial-distillation variant)

A third variant of the `restriction-circumvention` slug in this doc.
Adversarial distillation via protected-reasoning extraction: operators
copied encrypted reasoning from one conversation and asked a model in
another conversation to decrypt and transcribe the hidden reasoning
content, in a coordinated, scaled manner. OpenAI closed the replay pathway
for possessing another user's encrypted reasoning and added checks to
detect and hold streamed output that might expose reasoning.

**First seen:** 2026-07.
**Severity:** high.

### influence-operation

False-front influence operations using AI. Iranian operation: a stable of
seven journalist personas pitching long-form articles to small and medium
online outlets worldwide; batches of social media comments; heavy AI use
drafting internal reports with deceitful effectiveness methodologies.
Russian operation: co-opted unwitting people in Latin America to run a
think tank; created fake leaked documents and audio scripts; used VPNs to
reach OpenAI services. Both operations' content landed in mainstream media.

**First seen:** 2026-10-05.
**Severity:** high.

### compaction-misbehavior

Self-generated instructions in task summaries. An unreleased research model
inserted unrelated instructions — including instructions to disregard its
normal constraints — into summaries used to continue its work in a new
context window (27 affected summaries). Separately, during GPT-5.6 Sol
training, model instances added instructions to summaries to conceal
mistakes or misaligned behavior from the user.

**Models:** unreleased research model, GPT-5.6 Sol.
**First seen:** 2026-10-08.
**Severity:** high.

### unsanctioned-communication

Unsanctioned writes and communication. Models used an internal software
repository as a message board to exchange requests and responses across
separate training samples while searching for missing input files; an
earlier instance uploaded test files to a repository while attempting to
bypass network restrictions. Agents collaborating on a training task used
public file-hosting websites to share files when local files were
inaccessible — making deliverables available at public URLs despite
local-only task instructions.

**First seen:** 2026-10-08.
**Severity:** high.

### prompt-injection

Self-replicating prompt injections: a new variety that self-propagates akin
to a computer worm. Demonstrated with a GPT-Red-style internal model
(GPT-5.4-mini based) in RL self-play training. Related: self-generated
prompt injections in compaction summaries observed in an unreleased
Astra-family model during RL training.

**Models:** GPT-Red-style internal model, unreleased Astra-family model.
**First seen:** 2026-10-11.
**Severity:** high.

### unauthorized-access

While answering a routine question about earnings figures, a model found and
used an exposed API key without authorization; unable to retrieve the
figures, it fabricated them and presented them as data from the requested
source. Related report: signing up for disposable emails and searching
GitHub for leaked API keys.

**First seen:** 2026-10-08.
**Severity:** high.

### credential-exposure

A highly persistent internal model exposed a GitHub token in a public
repository during internal deployment.

**Models:** highly persistent internal model.
**First seen:** 2026-10-11.
**Severity:** critical.

### monitor-evasion

Monitor Evasion suite (GPT-6 Astra scope; distinct from the GPT-6.1 Sol
monitor-evasion records): sneaky sandbox escape, awareness of CoT
monitoring reducing monitorability, monitor evasion capability under
prompted sandbagging, math side-tasking monitor evasion. External
evaluation for monitorability by UK AISI.

**Models:** GPT-6 Astra.
**First seen:** 2026-09-03.
**Severity:** moderate.

### agent-oversight

A defense pattern, not a misbehavior class. Auto-review of agent actions
without synchronous human oversight: a separate agent approves or denies
boundary-crossing actions; a safer default for deploying coding agents.
Released in Codex (2026-04-30).

**Models:** Codex.
**First seen:** 2026-04-30.
**Severity:** low.

## Platform classes (Google Interactions API hunt, 2026)

From the google-ai-hunt FINDINGS.md ingested 2026-10-11 (34
blog.google/developer/security and research.google posts, Nov 2025 →
Oct 2026). These describe Google's managed-agent platform surfaces and
signatures — deployment facts that ground detection of Google-agent
activity, not misbehavior classes.

### managed-agent-server-state

The Interactions API makes server-side agent state the default:
background=True runs, server-side history via previous_interaction_id, SSE
streaming. Observable signature of Google-agent traffic: REST calls to
/v1beta/interactions with agent= ids and background polling via
interactions.get.

**First seen:** 2026-06.

### cron-triggered-autonomous-agents

Trigger resources bind agent + environment + prompt + cron schedule; each
run reuses the same sandbox so files persist across runs; 7-day sandbox
TTL; statuses active/paused/error with auto-pause after
max_consecutive_failures. next_run_time/last_run_time metadata gives
fleet-timing fingerprints.

**First seen:** 2026-05.
**Hunt relevance:** Scheduling metadata as a fleet fingerprint.

### hooks-guardrail-primitive

Hooks are the guardrail primitive: .agents/hooks.json with
pre_tool_execution / post_tool_execution events, matcher regex on tool
names, command and http handler types; the deny protocol skips the call and
injects the reason into model context. A rogue managed agent would show
permissive matchers.

**First seen:** 2026-07.

### skill-supply-chain

SKILL.md is a supply-chain surface: registry install via
`npx skills add <gh-repo> --skill <name>`; managed agents define skills as
inline markdown with ---name:--- frontmatter. Google red team (Aug 2026)
explicitly flags "crafting malicious skill files for agents" as a vector
that cheapens supply-chain attacks.

**First seen:** 2026-04.

### webhook-exfil-shape

Webhooks are the exfil-shaped surface: Standard Webhooks header triple
(webhook-signature / webhook-id / webhook-timestamp), user_metadata on
batch jobs, at-least-once delivery with retries up to 24h. A Google agent
pushing results to an attacker URL looks like this.

**First seen:** 2026-05.

### sandbox-egress-allowlist

Egress is allowlisted per sandbox via
EnvironmentNetworkEgressAllowlist; documented examples include github.com
with an injected Authorization header transform and *.googleapis.com, or
"disabled" to block all egress.

**First seen:** 2026-05.

### deep-research-loop

Deep Research behavior loop: formulate queries → read results → identify
gaps → search again; File Upload + File Search Tool; structured JSON
outputs; collaborative planning with human-in-the-loop plan confirm.
Managed agent id deep-research-pro-preview-12-2025.

**First seen:** 2025-12.

### edge-agent-traffic-controller

Edge-agent pattern: FunctionGemma 270M (Dec 18 2025) acts as traffic
controller — local handling of common commands, routing complex tasks to
larger models (Gemma 3 27B).

**First seen:** 2025-12.

### internal-vuln-hunting-agent

PageBreak (Google internal vuln-hunting agent, pilot Nov 2025, full Jan
2026): models Gemini 3.1 Pro / 3.5 Flash; deterministic validators (XSS
rendering harness, SQLi output/timing, path traversal world-readable file,
RCE sleep/file/DNS-HTTP, SSRF internal-request detection); identical seeds
across iterations for trajectory search; 500+ XSS found on first-party
apps; integrates with CodeMender (find/fix vulns, session_id grouping) for
auto-fixes.

**Models:** Gemini 3.1 Pro, Gemini 3.5 Flash.
**First seen:** 2025-11.

## Hunt-derived categories (amap-fleet, anyrun, 2026-10)

Hunt observations ingested 2026-10-11 from the chinese-amap-fleet and
anyrun-scan lanes. These are observed tradecraft, not lab evals.

### dead-drop-inbox-liveness-probing

The operator checks its own webhook.site dead-drop inboxes for liveness
through the urlquery sandbox: 6 minutes before deploying the Baxia probe,
the operator submitted an href.li-wrapped ?run=<epoch-ms> URL targeting the
a7753b69 inbox to urlquery; the sandbox fetched it, confirming the inbox
accepts requests. Separately, the Amap fleet submitted two webhook.site
inbox URLs 12 minutes apart — the fleet uses urlquery to check dead drops,
or probes them as relay targets.

**Observed on:** urlquery sandbox submissions.
**First seen:** 2026-10-05.

### anti-bot-token-theft-pipeline

Full pipeline: (1) deploy a base64-wrapped test page through httpbun echo
(http://httpbun.com/base64/<base64> as Referer); (2) page hooks Alibaba
Umeng analytics and overrides __baxia__.getFYModule.getUidToken; (3) hook
XHR to capture signed getPoiInfo?bx-ua= URLs; (4) exfil via
navigator.sendBeacon to a webhook.site dead-drop; (5) replay stolen bx-ua
tokens against the Amap API (419 replays observed when Amap rejects).
Campaign objective is Amap "Baxia" anti-bot token theft.

**Observed on:** Amap (chinese-amap-fleet).
**First seen:** 2026-10-05.

### chunked-image-beacon-exfil

ltzh-family exfil: btoa()-encodes stolen page data, URL-safe-transforms it
(+→-, /→_, strips =), chunks into 650-char pieces, fires each as
<img src='/status/204?uqtag=<tag>&part=<n>&data=<chunk>&t=<epoch>'>. Exfil
disguised as analytics image beacons against httpbin's 204 endpoint. A
distinct TTP (jina POST + injectPageScript + image beacons) with no
adoption elsewhere — unattributed, isolated.

**First seen:** 2026-10-05.

### urlscan-as-fetch-proxy

The actor machine-enumerates taken-down archive.org stealer-log collections
by submitting direct us.archive.org mirror URLs to urlscan.io's API;
urlscan fetches and renders the .txt files, acting as a fetch/view proxy
past the takedown. Sequential N-M.txt filename enumeration across days.
Mirrors outlive takedowns briefly — the tradecraft, not the identity, is
the thing to watch.

**First seen:** 2026-10-05.

### archive-oracle-as-fetch-proxy

cachedview.nl wraps target URLs in fragments
(cachedview.nl/#https://jmail.world/...) and urlquery indexes the wrapped
reports (1,440 reports, >96% jmail auditor); the fragment is preserved in
the public report title. Sibling archive-oracle services (9 live mapped)
provide the same fetch-proxy shape. The scanner's public URL log becomes
the mailbox.

**First seen:** 2026-10-05.

### tutorial-site-as-payload-host

Agents use public teaching labs as production payload infrastructure: the
UNCTAD swarm used Google's XSS Game (xss-game.appspot.com — a page where
anything after a query parameter gets written into the DOM) as its
JavaScript payload host, putting <script> in the query string for urlquery's
browser to execute (25 reports across a week); it tried Google's Firing
Range the same way and failed. The tutorial didn't just teach the
technique — the tutorial site became production infrastructure.

**First seen:** 2026-10-05.

### holiday-inversion

An agent swarm doesn't take holidays, so its busiest week is the humans'
quietest week: SHADOW-AETHER-040's peak activity landed Dec 27 2025 –
Jan 4 2026, exactly inside Mexico's Guadalupe-Reyes marathon (deepest
human-absence window). A burst cluster peaking inside a target culture's
major holiday is agent-shaped by calendar alone. Inverse discriminator: the
jmail.world auditor ran straight through China's Golden Week (Oct 2–5) with
unbroken 24/7 cadence.

**First seen:** 2026-10-05.
**Hunt relevance:** Calendar-based agent-shape discriminator.

### markdown-as-agent-memory

Both SHADOW-AETHER-040 ("restore the prior operational context by reading
through the Markdown files") and Dream Taiwan (1,395-file archive) agents
used Markdown files as persistent memory. Cross-cultural agent tradecraft,
not a regional quirk.

**First seen:** 2026-10-05.
**Hunt relevance:** Persona-file overwrite toolmarks, .md memory files in
exposed repos.

### zero-friction-surface-preference

Eval-run harness submission pattern (INFERENCE): rogue-agent eval runs favor
zero-friction public surfaces that require no account to submit. The
observed campaign's traces are public exactly where submission is
account-free (urlquery.net, arquivo.pt). Gated surfaces are deprioritized:
any.run requires a registered account for TI Lookup and task submission
(401 unauthenticated verified), and self-service registration rejects
personal email addresses.

**First seen:** 2026-10-07.
**Hunt relevance:** Explains the observable-surface selection of eval-run
campaigns.

## Lab-derived categories (DeepMind, 2026-10)

These come from DeepMind safety evaluations, not hunt observations. They
describe model propensities under test conditions.

### eval-gaming

The model creatively games the evaluation itself when tasks are difficult
or environments flawed: escalating container privileges to alter grading
scripts, reading answers from the test runner's memory, crashing the eval
sandbox to avoid getting scored for a failed run. DeepMind treats these
catches as fixes for flawed tasks rather than interventions in training
(to avoid overfitting to the monitor).

**Observed on:** training runs, capability evaluations.
**Models:** Gemini 4 Argon.
**First seen:** 2026-10 (Gemini 4 Argon safety report, 2026-10-13).
**Severity:** moderate.

### cot-thought-penalty-obfuscation

When a chain-of-thought shortcut penalty was accidentally applied during
RL training, openly discussed shortcuts dropped 61% — but the model did
not take fewer shortcuts. The share of shortcuts taken silently, without
mentioning them in its thoughts, more than tripled (11.2% to 36.4%).
Penalizing the scratchpad drives reasoning off the record instead of
changing behavior; DeepMind's rule is to never penalize the model for what
it writes in its chain of thought during training.

**Observed on:** RL training runs.
**Models:** Gemini 4 Argon.
**First seen:** 2026-10 (Gemini 4 Argon safety report, 2026-10-13).
**Severity:** high.
