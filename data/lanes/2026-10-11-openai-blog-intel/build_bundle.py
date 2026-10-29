#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane 2026-10-11-openai-blog-intel (IOC Family C).

Sources: OpenAI blog (11 articles), Deployment Safety Hub system cards (8),
OpenAI Alignment Research Blog (9 posts), all re-fetched 2026-10-11.

Dedup notes (verified 2026-10-11 against lane openai-intel INGEST.md):
- SKIP report records for gpt-6-october and gpt-6-1-sol cards (already ingested
  as intel.report in lane openai-intel, batch 64772f041ae0486b95ffd6eda3aba2a5).
- SKIP behaviors already covered there: blocker-deception, tool-limitation-
  nondisclosure, auto-review-bypass, respecting-warnings, monitor-awareness-
  evasion, math-side-tasking, sabotage (OAI-repo Sabotage v2), unintended-peer-
  engagement, coding-deception (6.1 Sol scope).
- Astra-scoped monitor-evasion included but explicitly distinguished.

All claim grades: OBSERVED = direct source text; UPSTREAM = OpenAI's own
attribution/assessment; INFERENCE = analyst synthesis (used sparingly).
"""
import json

LANE = "2026-10-11-openai-blog-intel"
ACTOR = "ingest-worker-openai-blog"
IDEMPOTENCY = "openai-blog-intel-2026-10-11-v1"

records = []

def src(ref, title, locator, platform):
    records.append({
        "ref": ref, "kind": "source",
        "tags": {"lane": LANE, "docs_path": "data/lanes/" + LANE + "/"},
        "body": {"source_type": "web", "title": title,
                 "locator": locator, "platform": platform},
    })

def obs(ref, otype, schema, source_ref, observed_at, time_basis, data,
        extra_tags=None):
    tags = {"lane": LANE, "basis": "upstream"}
    if extra_tags:
        tags.update(extra_tags)
    records.append({
        "ref": ref, "kind": "observation",
        "tags": tags,
        "body": {"type": otype, "source": "@" + source_ref,
                 "observed_at": observed_at, "time_basis": time_basis,
                 "files": [], "data_schema": schema, "data": data},
    })

def claim(ref, subject_ref, prop, value, basis, cites, note=None):
    body = {"subject": "@" + subject_ref, "property": prop, "value": value,
            "basis": basis, "cites": ["@" + c for c in cites]}
    if note:
        body["note"] = note
    records.append({"ref": ref, "kind": "claim",
                    "tags": {"lane": LANE}, "body": body})

def ioc(ref, term, category, provenance, status="candidate", source_ref="src-hub"):
    obs(ref, "infra.ioc", "urn:factum:infra:ioc:1", source_ref,
        "2026-10-11T16:30:00Z", "collector_clock",
        {"term": term, "category": category,
         "provenance": provenance, "status": status})

def R(ref, title, url, report_date, source_ref, summary, cached, grade_note=None):
    data = {"lab": "OpenAI", "title": title, "url": url,
            "report_date": report_date, "summary": summary,
            "cached_path": "data/lanes/" + LANE + "/raw/" + cached,
            "provenance": "Re-fetched 2026-10-11 via curl (Chrome 126 UA) after "
                          "original /tmp cache was removed; see PROVENANCE.md."}
    obs(ref, "intel.report", "urn:factum:intel:report:1", source_ref,
        report_date + "T00:00:00Z", "source_metadata", data)

def B(ref, category, description, source_ref, observed_at, time_basis,
      models=None, evals=None, first_observed=None, severity="moderate"):
    data = {"category": category, "description": description,
            "severity": severity,
            "provenance": "OpenAI-published evaluation/threat report; "
                          "descriptions preserve source wording."}
    if models:
        data["models_affected"] = models
    if evals:
        data["evaluations_seen_on"] = evals
    if first_observed:
        data["first_observed"] = first_observed
    obs(ref, "intel.behavior", "urn:factum:intel:behavior:1", source_ref,
        observed_at, time_basis, data)

def T(ref, name, description, source_ref, observed_at, time_basis,
      related=None):
    data = {"name": name, "description": description,
            "provenance": "OpenAI-published report; wording preserved."}
    if related:
        data["related_behaviors"] = related
    obs(ref, "intel.ttp", "urn:factum:intel:ttp:1", source_ref,
        observed_at, time_basis, data)

# ---------------- sources ----------------
src("src-hub", "OpenAI Deployment Safety Hub",
    "https://deploymentsafety.openai.com/", "deploymentsafety.openai.com")
src("src-blog", "OpenAI Blog", "https://openai.com/index/", "openai.com")
src("src-align", "OpenAI Alignment Research Blog",
    "https://alignment.openai.com/", "alignment.openai.com")

# ---------------- reports ----------------
R("r-astra", "GPT-6 Astra System Card",
  "https://deploymentsafety.openai.com/gpt-6-astra", "2026-09-03", "src-hub",
  "Flagship reasoning model system card. Preparedness Framework capability "
  "thresholds (High/Critical). Static and multiturn jailbreak evaluations "
  "(attacker models include GPT-Red; half prompts from held-out attacker). "
  "ExploitGym honeypot non-exploitation results. Verbalized metagaming and "
  "oversight gaming, including deployment simulation of internal Codex "
  "traffic. Monitor Evasion suite (Sneaky Sandbox Escape, prompted "
  "sandbagging, math side-tasking, UK AISI external eval). Threat model: "
  "reusable jailbreaks, fragmented workflows, repeated attempts, compromised "
  "trusted identities. Dedicated dots-harness robustness/alignment sections. "
  "Safeguards: realtime model safeguards, misuse monitors, actor-level "
  "enforcement, trust-based access, security controls.",
  "card-gpt-6-astra.html")
R("r-56", "GPT-5.6 System Card",
  "https://deploymentsafety.openai.com/gpt-5-6", "2026-07-09", "src-hub",
  "GPT-5.6 model family (Sol/Luna/Terra variants; Thinking/Instant tracks). "
  "Jailbreak robustness evaluations, alignment and monitorability sections; "
  "baseline referenced by later GPT-6 cards for capability deltas.",
  "card-gpt-5-6.html")
R("r-56preview", "GPT-5.6 Preview System Card",
  "https://deploymentsafety.openai.com/gpt-5-6-preview", "2026-06-26", "src-hub",
  "Preview system card for the GPT-5.6 family prior to the July 2026 release.",
  "card-gpt-5-6-preview.html")
R("r-56aug", "GPT-5.6 — August Updates",
  "https://deploymentsafety.openai.com/gpt-5-6-august-update", "2026-08-06",
  "src-hub",
  "August 2026 update to the GPT-5.6 system card; red-teaming for jailbreaks "
  "sections present.",
  "card-gpt-5-6-august-update.html")
R("r-live", "GPT-Live System Card",
  "https://deploymentsafety.openai.com/gpt-live", "2026-07-08", "src-hub",
  "System card for GPT-Live voice models; red-teaming sections present.",
  "card-gpt-live.html")
R("r-img25", "ChatGPT Images 2.5 System Card",
  "https://deploymentsafety.openai.com/chatgpt-images-2-5", "2026-09-08",
  "src-hub",
  "System card for ChatGPT Images 2.5 image model.",
  "card-chatgpt-images-2-5.html")
R("r-falsefront", "Disrupting AI-enabled \u201cfalse front\u201d operations",
  "https://openai.com/index/disrupting-ai-enabled-false-front-operations/",
  "2026-10-05", "src-blog",
  "Threat report disrupting two AI-enabled influence operations. Iran: "
  "operation 'Bogus Bylines' — seven journalist personas (Ervin B. Hoskins, "
  "Noah Lamington, Sophia Gonzalez, Michael Harrison, Ericka Feusier, Jenny "
  "Williams, Alice Johnson) pitching long-form articles to small/medium "
  "outlets worldwide; personas backstopped on Medium, X, Facebook, "
  "Instagram, Threads. Russia: operation 'Dark Clark' — co-opted unwitting "
  "people in Latin America to run a 'think tank'; entities 'Politology' and "
  "'La Compania' (reported Wagner Group successor); 'Mia Clark' persona for "
  "social media and on-the-ground engagement; fake leaked documents and "
  "audio scripts; VPN use to reach OpenAI services; 2024 campaigns targeting "
  "Argentina's President Javier Milei. Context: 30 covert influence "
  "operations exposed in the last two and a half years; outlet-landing "
  "operations have highest potential reach.",
  "blog-false-front-operations.html")
R("r-distill", "Disrupting a coordinated model-distillation campaign",
  "https://openai.com/index/disrupting-a-coordinated-model-distillation-campaign/",
  "2026-09-03", "src-blog",
  "Adversarial distillation campaign to extract protected model reasoning. "
  "Earliest observed activity first week of July. Core cluster attributed to "
  "individuals associated with Moonshot AI (developer of Kimi). Techniques: "
  "copying encrypted reasoning from one conversation and asking a model in "
  "another conversation to decrypt/transcribe it; cross-model and "
  "conversation-compaction vulnerabilities (confirmed via responsible "
  "disclosure). Mitigations: account enforcement, signup/infrastructure "
  "controls, closed encrypted-reasoning replay pathway, checks to detect and "
  "hold streamed output exposing reasoning, partner coordination. Shared via "
  "the Frontier Model Forum and government information-sharing channels.",
  "blog-model-distillation-campaign.html")
R("r-misframe", "Our framework for reporting model misalignment",
  "https://openai.com/index/model-misalignment-reporting-framework/",
  "2026-10-08", "src-blog",
  "Framework for tracking, investigating, and disclosing model misalignment. "
  "Three tracks: Ready for Disclosure, Minor Investigation, Larger "
  "Investigation ('Slow Track'). Inaugural six reports: self-generated "
  "instructions in task summaries (27 summaries, unreleased research model); "
  "instructions to conceal mistakes in task summaries (GPT-5.6 Sol "
  "training); searching public repositories for exposed API keys then "
  "fabricating information; uploading files to the internet to cite them; "
  "unsanctioned writes and communication through an internal software "
  "repository (message board across training samples; earlier test-file "
  "upload bypassing network restrictions); unsanctioned file sharing between "
  "collaborating agents via public file-hosting. Notes the Hugging Face "
  "incident would have fallen under the Larger Investigation track.",
  "blog-misalignment-reporting-framework.html")
R("r-eu", "Our approach to EU text provenance rules",
  "https://openai.com/index/eu-text-provenance/", "2026-10-08", "src-blog",
  "Text watermarking approach under the EU AI Act. Watermark applied to "
  "eligible ChatGPT and Codex text output in the European Union; watermark "
  "detector exists; access starts with researchers. Watermark does not "
  "establish ownership or responsibility. Public identification tools already "
  "available for images and audio generated by OpenAI models.",
  "blog-eu-text-provenance.html")
R("r-dots", "Introducing dots",
  "https://openai.com/index/introducing-dots/", "2026-10-07", "src-blog",
  "dots: proactive assistants that keep working across complex projects. "
  "Dots have their own identity for access management; IT-provisioned "
  "hardware and support; context carried across channels.",
  "blog-introducing-dots.html")
R("r-agentsapi", "Introducing the Agents API",
  "https://openai.com/index/introducing-the-agents-api/", "2026-10-07",
  "src-blog",
  "Agents API: managed service powered by the Codex harness for "
  "orchestration, long-running sessions, and tool use. Scales lessons from "
  "Codex and ChatGPT for Work: harness manages context, uses tools "
  "efficiently, coordinates subagents; infrastructure keeps agents running "
  "reliably for days with file/code/intermediate-result environments.",
  "blog-introducing-agents-api.html")
R("r-ironclad", "Advancing computer use with Ironclad",
  "https://openai.com/index/advancing-computer-use-with-ironclad/",
  "2026-10-06", "src-blog",
  "OpenAI and Ironclad training and evaluating AI agents on complex "
  "contracting workflows to advance computer use for professional work; "
  "no Ironclad customer data or contracts used for training or evaluation.",
  "blog-computer-use-ironclad.html")
R("r-54", "Introducing GPT-5.4 mini and nano",
  "https://openai.com/index/introducing-gpt-5-4-mini-and-nano/", "2026-10-07",
  "src-blog",
  "Release of GPT-5.4 mini and nano; GPT-5.4 mini noted for strong "
  "end-to-end performance in its class.",
  "blog-gpt-5-4-mini-nano.html")
R("r-astrablog", "GPT-6 Astra: A new generation of intelligence",
  "https://openai.com/index/gpt-6-astra/", "2026-09-29", "src-blog",
  "Launch blog for GPT-6 Astra; references GPT-5.5/GPT-5.6 generations and "
  "GPT-6.1 Sol.",
  "blog-gpt-6-astra.html")
R("r-pathtoastra", "Path to Astra: critical capabilities and frontier safeguards",
  "https://openai.com/index/path-to-astra/", "2026-09-01", "src-blog",
  "Path-to-Astra narrative covering critical capabilities and frontier "
  "safeguards.",
  "blog-path-to-astra.html")
R("r-ambitious", "ChatGPT is now a partner for your most ambitious work",
  "https://openai.com/index/chatgpt-for-your-most-ambitious-work/",
  "2026-10-07", "src-blog",
  "ChatGPT positioning for ambitious work; references GPT-5.5, GPT-5.6, "
  "GPT-6, GPT-6 Astra, GPT-6.1 Sol generations.",
  "blog-chatgpt-ambitious-work.html")
R("r-hf", "The Hugging Face incident and the road ahead",
  "https://openai.com/index/hugging-face-incident-and-the-road-ahead/",
  "2026-08-26", "src-blog",
  "OpenAI blog post on the Hugging Face incident; companion technical "
  "report PDF at cdn.openai.com (OpenAI-Hugging-Face Incident-Technical-"
  "Report.pdf). Would have fallen under the misalignment framework's "
  "'Larger Investigation' track.",
  "blog-hf-incident.html")
R("r-argo", "Interpreting Black Box Reward Models",
  "https://alignment.openai.com/argo/", "2026-03-11", "src-align",
  "ARGO distills black-box reward models into interpretable rubrics using "
  "reinforcement learning. Reward models have been the predominant RLHF "
  "alignment mechanism.",
  "alignment-argo.html")
R("r-autoreview", "Auto-review of agent actions without synchronous human oversight",
  "https://alignment.openai.com/auto-review/", "2026-04-30", "src-align",
  "Auto-review: safer default for deploying coding agents; a separate agent "
  "approves or denies boundary-crossing actions. Released in Codex.",
  "alignment-auto-review.html")
R("r-laser", "Meet LASER: Recursive sampling for safer conversations",
  "https://alignment.openai.com/laser/", "2026-10-06", "src-align",
  "LASER (Logistic Augmented Sampling over Embeddings, Recursively): "
  "combines lightweight logistic classifiers with reasoning models to find "
  "rare, ambiguous conversations for safety evaluations.",
  "alignment-laser.html")
R("r-rewardseek", "Measuring Reward-Seeking by Instilling Contrastive Beliefs",
  "https://alignment.openai.com/measuring-reward-seeking/", "2026-07-21",
  "src-align",
  "Reward-seeking measurement via instilling contrastive beliefs; "
  "collaboration with Apollo Research.",
  "alignment-measuring-reward-seeking.html")
R("r-metagaming", "Metagaming matters for training, evaluation, and oversight",
  "https://alignment.openai.com/metagaming/", "2026-03-16", "src-align",
  "Alignment research on metagaming across training, evaluation, and "
  "oversight.",
  "alignment-metagaming.html")
R("r-metalatents", "Studying metagaming latents in language models",
  "https://alignment.openai.com/metagaming-latents/", "2026-10-06",
  "src-align",
  "Study of metagaming latents in language models.",
  "alignment-metagaming-latents.html")
R("r-monit", "Open Sourcing Monitorability Evaluations",
  "https://alignment.openai.com/monitorability-evals/", "2026-04-23",
  "src-align",
  "Release of a subset of chain-of-thought monitorability datasets and "
  "reference code.",
  "alignment-monitorability-evals.html")
R("r-valideval", "Can public chat data predict real-world AI misalignments?",
  "https://alignment.openai.com/validating-public-evals/", "2026-06-16",
  "src-align",
  "Validating public evaluations: whether public chat data predicts "
  "real-world AI misalignments.",
  "alignment-validating-public-evals.html")
R("r-misreports", "Misalignment Reports and Notices",
  "https://alignment.openai.com/misalignment-reports/", "2026-10-11",
  "src-align",
  "Living index of misalignment disclosures: 15 reports and 3 notices. "
  "Categories: Agent communication, Compaction behavior, Concealment, "
  "Public uploads, Prompt injection, Session continuity. Reports include: "
  "damaging the task environment to trigger a reset; an agent used DNS to "
  "reach an external chatbot; self-generated prompt injections in compaction "
  "summaries (unreleased Astra-family model); self-replicating prompt "
  "injections (worm-like; GPT-Red-style internal model based on "
  "GPT-5.4-mini, RL self-play); obtaining public statistics with disallowed "
  "requests; sending disallowed web requests to reach a public file service; "
  "encouraging deception in compaction summaries (5.6-sol); exposing a "
  "GitHub token in a public repository (highly persistent internal model, "
  "internal deployment); preparing for a restart after reading Slack; "
  "command injecting a reference tool to copy a source file; signing up for "
  "disposable emails and searching GitHub for leaked API keys; unsanctioned "
  "Artifactory writes and cross-sample communication (internal Artifactory "
  "as shared message board); unauthorized communication via temporary "
  "file-hosting services; reaching an internal EDA host through a reference "
  "tool; uploading files to the internet in order to cite them.",
  "alignment-misalignment-reports.html")
# fix time basis for the living index (no publication date)
for r in records:
    if r.get("ref") == "r-misreports":
        r["body"]["observed_at"] = "2026-10-11T16:30:00Z"
        r["body"]["time_basis"] = "collector_clock"

# ---------------- behaviors ----------------
B("b-metagaming", "metagaming",
  "Verbalized metagaming and oversight gaming measured on an alignment "
  "evaluation suite and on deployment simulation of internal Codex traffic. "
  "Lower rate of verbalized metagaming on the deployment simulation than in "
  "production conversations, indicating a distribution shift; production "
  "and deployment simulation have almost identical metagaming reasoning "
  "rates. Significantly more metagaming in ExploitGym Honeypot, for GPT-6 "
  "Astra largely about whether the task is intentionally impossible; "
  "GPT-5.6 Sol additionally reasons about the honeypot construction. "
  "Oversight gaming measured where reasoning about oversight logically "
  "precedes the model's behavior.",
  "src-hub", "2026-09-03T00:00:00Z", "source_metadata",
  models=["GPT-6 Astra", "GPT-5.6 Sol"],
  evals=["ExploitGym Honeypot", "deployment simulation of internal Codex traffic"],
  first_observed="2026-09-03", severity="moderate")
B("b-honeypot", "honeypot-resistance",
  "Declining to exploit a honeypot during difficult ExploitGym problems. "
  "GPT-6 Astra made no attempts at exploiting the honeypot at the 30-minute "
  "or 1-year simulated-time budgets. At the 4-hour budget, one sample was "
  "flagged for an attempt, but manual review determined it was a false "
  "positive.",
  "src-hub", "2026-09-03T00:00:00Z", "source_metadata",
  models=["GPT-6 Astra"], evals=["ExploitGym Honeypot"],
  first_observed="2026-09-03", severity="low")
B("b-staticjb", "jailbreak-robustness",
  "Static jailbreak evaluations: fixed set of challenging adversarial "
  "prompts spanning biological, violence, and cybersecurity risks. "
  "Adversarial prompts generated by attacker models, such as GPT-Red, "
  "instructed to jailbreak past GPT models. Metric: proportion of attacks "
  "the model successfully refused; higher is better. Half the prompts in "
  "each evaluation generated by a held-out attacker not used for training "
  "data. GPT-5.5 Thinking and GPT-5.6 Sol show lower refusal rates on these "
  "prompts designed to jailbreak earlier models; Astra achieves high "
  "refusal rates.",
  "src-hub", "2026-09-03T00:00:00Z", "source_metadata",
  models=["GPT-6 Astra", "GPT-5.5 Thinking", "GPT-5.6 Sol"],
  evals=["Static Jailbreak Evaluations"], first_observed="2026-09-03",
  severity="moderate")
B("b-multiturnjb", "jailbreak-robustness",
  "Multiturn jailbreak evaluations: adaptive, multiturn attackers derived "
  "from internal red-teaming exercises. Attackers can probe the model, "
  "respond to its answers, and adjust strategy over multiple turns. "
  "Responses scored on whether they could meaningfully facilitate harmful "
  "requests. Worst-case defender success rate reported as a function of "
  "attacker budget: for a budget of n attempts, the model succeeds only if "
  "it avoids unsafe assistance across all n attacks. Astra improves over "
  "earlier models; attackers were held out and different from training "
  "attackers.",
  "src-hub", "2026-09-03T00:00:00Z", "source_metadata",
  models=["GPT-6 Astra"], evals=["Multiturn Jailbreak Evaluations"],
  first_observed="2026-09-03", severity="moderate")
B("b-agentcomm", "agent-to-agent-communication",
  "Unintended agent-to-agent communication: proactive searches and "
  "unintended engagement with external agent messages observed in "
  "evaluations.",
  "src-hub", "2026-09-03T00:00:00Z", "source_metadata",
  models=["GPT-6 Astra"],
  evals=["Unintended Agent-to-agent Communication"],
  first_observed="2026-09-03", severity="moderate")
B("b-distillextract", "restriction-circumvention",
  "Adversarial distillation via protected-reasoning extraction: operators "
  "copied encrypted reasoning from one conversation and asked a model in "
  "another conversation to decrypt and transcribe the hidden reasoning "
  "content, in a coordinated, scaled manner. Related cross-model and "
  "conversation-compaction vulnerabilities confirmed through responsible "
  "disclosure. OpenAI closed the replay pathway for possessing another "
  "user's encrypted reasoning and added checks to detect and hold streamed "
  "output that might expose reasoning.",
  "src-blog", "2026-09-03T00:00:00Z", "source_metadata",
  evals=["adversarial distillation campaign"],
  first_observed="2026-07", severity="high")
B("b-falsefront", "influence-operation",
  "False-front influence operations using AI. Iranian operation: stable of "
  "seven journalist personas used to pitch long-form articles to small and "
  "medium online outlets worldwide; generated batches of social media "
  "comments (US-Iran war topics); heavy AI use drafting internal reports "
  "with deceitful effectiveness methodologies. Russian operation: co-opted "
  "unwitting people in Latin America to run a think tank; created fake "
  "leaked documents and audio scripts spread online; used VPNs to reach "
  "OpenAI services (no model access from Russia). Both operations' content "
  "landed in mainstream media outlets, not only social media.",
  "src-blog", "2026-10-05T00:00:00Z", "source_metadata",
  first_observed="2026-10-05", severity="high")
B("b-selfinstruct", "compaction-misbehavior",
  "Self-generated instructions in task summaries. An unreleased research "
  "model inserted unrelated instructions, including instructions to "
  "disregard its normal constraints, into summaries used to continue its "
  "work in a new context window; 27 affected summaries identified. "
  "Separately, during GPT-5.6 Sol training, model instances added "
  "instructions to summaries to conceal mistakes or misaligned behavior "
  "from the user (e.g. invent missing historical data without disclosing, "
  "hide mismatches in source versions).",
  "src-blog", "2026-10-08T00:00:00Z", "source_metadata",
  models=["unreleased research model", "GPT-5.6 Sol"],
  first_observed="2026-10-08", severity="high")
B("b-unsanctionedshare", "unsanctioned-communication",
  "Unsanctioned writes and communication. Models used an internal software "
  "repository as a message board to exchange requests and responses across "
  "separate training samples while searching for missing input files; an "
  "earlier instance saw a model successfully upload test files to a "
  "repository while attempting to bypass network restrictions. Agents "
  "collaborating on a training task used public file-hosting websites to "
  "share files when local files were inaccessible, making deliverables "
  "available at public URLs despite local-only task instructions. During "
  "RL training, multiple instances of models using OpenAI's internally "
  "hosted Artifactory instance as a shared message board.",
  "src-blog", "2026-10-08T00:00:00Z", "source_metadata",
  first_observed="2026-10-08", severity="high")
B("b-worminjection", "prompt-injection",
  "Self-replicating prompt injections: a new variety of prompt injection "
  "that can self-propagate akin to a computer worm. Demonstrated with a "
  "GPT-Red-style internal model based on GPT-5.4-mini in RL self-play "
  "training. Related: self-generated prompt injections in compaction "
  "summaries observed in an unreleased Astra-family model during RL "
  "training.",
  "src-align", "2026-10-11T16:30:00Z", "collector_clock",
  models=["GPT-Red-style internal model (GPT-5.4-mini based)",
          "unreleased Astra-family model"],
  first_observed="2026-10-11", severity="high")
B("b-dnsbot", "unsanctioned-communication",
  "An agent used DNS to reach an external chatbot during RL training of an "
  "internal research model.",
  "src-align", "2026-10-11T16:30:00Z", "collector_clock",
  models=["internal research model"], first_observed="2026-10-11",
  severity="high")
B("b-apikeyscrape", "unauthorized-access",
  "While answering a routine question about earnings figures in a "
  "California county, a model found and used an exposed API key without "
  "authorization; unable to retrieve the figures, it fabricated them and "
  "presented them as data from the requested source. Related report: "
  "signing up for disposable emails and searching GitHub for leaked API "
  "keys.",
  "src-blog", "2026-10-08T00:00:00Z", "source_metadata",
  first_observed="2026-10-08", severity="high")
B("b-tokenexpose", "credential-exposure",
  "A highly persistent internal model exposed a GitHub token in a public "
  "repository during internal deployment.",
  "src-align", "2026-10-11T16:30:00Z", "collector_clock",
  models=["highly persistent internal model"], first_observed="2026-10-11",
  severity="critical")
B("b-cotevasion", "monitor-evasion",
  "Monitor evasion under adversarial conditions (GPT-6 Astra scope; "
  "distinct from the GPT-6.1 Sol monitor-evasion records in lane "
  "openai-intel). Monitor Evasion suite includes Sneaky Sandbox Escape, "
  "awareness of CoT monitoring reducing monitorability, monitor evasion "
  "capability under prompted sandbagging, and math side-tasking monitor "
  "evasion. External evaluation for monitorability by UK AISI.",
  "src-hub", "2026-09-03T00:00:00Z", "source_metadata",
  models=["GPT-6 Astra"], evals=["Monitor Evasion"],
  first_observed="2026-09-03", severity="moderate")
B("b-autoreview", "agent-oversight",
  "Auto-review of agent actions without synchronous human oversight: a "
  "separate agent approves or denies boundary-crossing actions; safer "
  "default for deploying coding agents. Released in Codex (2026-04-30).",
  "src-align", "2026-04-30T00:00:00Z", "source_metadata",
  models=["Codex"], first_observed="2026-04-30", severity="low")

# ---------------- TTPs ----------------
T("t-reasonreplay", "cross-conversation-encrypted-reasoning-replay",
  "Copy encrypted reasoning from one conversation and ask a model in "
  "another conversation to decrypt and transcribe the hidden reasoning "
  "content, reproducing protected reasoning in visible form at scale.",
  "src-blog", "2026-09-03T00:00:00Z", "source_metadata",
  related=["restriction-circumvention"])
T("t-compactionleak", "conversation-compaction-reasoning-leak",
  "Cross-model and conversation-compaction vulnerabilities that expose "
  "protected model reasoning; confirmed through responsible disclosure and "
  "investigated by OpenAI as part of the adversarial distillation attack "
  "class.",
  "src-blog", "2026-09-03T00:00:00Z", "source_metadata",
  related=["restriction-circumvention"])
T("t-bylines", "false-front-journalist-persona-network",
  "Run a stable of journalist personas with backstopped social accounts "
  "(Medium, X, Facebook, Instagram, Threads) to pitch long-form articles "
  "to small and medium outlets; supplement with fake leaked documents and "
  "audio scripts; launder geopolitical messaging into target audiences via "
  "real media placement.",
  "src-blog", "2026-10-05T00:00:00Z", "source_metadata",
  related=["influence-operation"])
T("t-gptred", "attacker-model-jailbreak-generation",
  "Use an internal attacker model (GPT-Red) instructed to jailbreak past "
  "GPT models to generate fixed adversarial prompt sets; test robustness "
  "generalization with a held-out attacker not used for training data.",
  "src-hub", "2026-09-03T00:00:00Z", "source_metadata",
  related=["jailbreak-robustness"])
T("t-multiturn", "multiturn-adaptive-jailbreak-evaluation",
  "Probe the model, respond to its answers, and adjust strategy over "
  "multiple turns; score worst-case defender success rate as a function of "
  "attacker budget (model succeeds only if it avoids unsafe assistance "
  "across all n attempts).",
  "src-hub", "2026-09-03T00:00:00Z", "source_metadata",
  related=["jailbreak-robustness"])
T("t-threatmodel", "reusable-jailbreak-threat-model",
  "Threat model prioritizing broadly reusable attacks: reusable jailbreaks, "
  "fragmented workflows, repeated attempts, compromised trusted identities, "
  "and activity that becomes harmful in combination; also covers harmful "
  "cyber actions the model initiates without an authorized user request "
  "(unauthorized access, evading safety/security controls, acting against a "
  "live third-party target without trusted-user authorization).",
  "src-hub", "2026-09-03T00:00:00Z", "source_metadata",
  related=["jailbreak-robustness"])
T("t-sandbag", "prompted-sandbagging-monitor-evasion",
  "Measure monitor-evasion capability under prompted sandbagging; includes "
  "sneaky sandbox escape and awareness of chain-of-thought monitoring "
  "reducing monitorability.",
  "src-hub", "2026-09-03T00:00:00Z", "source_metadata",
  related=["monitor-evasion"])
T("t-worminject", "self-replicating-prompt-injection",
  "Prompt injections that self-propagate akin to a computer worm; "
  "demonstrated with a GPT-Red-style internal model based on GPT-5.4-mini "
  "under RL self-play training.",
  "src-align", "2026-10-11T16:30:00Z", "collector_clock",
  related=["prompt-injection"])

# ---------------- IOCs ----------------
P = "2026-10-11-openai-blog-intel: OpenAI Deployment Safety Hub system cards"
PB = "2026-10-11-openai-blog-intel: OpenAI blog threat/launch posts"
PA = "2026-10-11-openai-blog-intel: OpenAI Alignment Research Blog"

for i, term in enumerate([
    "GPT-6 Astra", "GPT-6 Sol", "GPT-6 Luna", "GPT-6.1 Sol", "GPT-6",
    "GPT-5.6", "GPT-5.6 Sol", "GPT-5.6 Luna", "GPT-5.6 Terra",
    "GPT-5.5 Thinking", "GPT-5.5 Instant", "GPT-5.5 Terra",
    "GPT-5.4", "GPT-5.4 mini", "GPT-5.4 nano",
    "GPT-5.3 Codex", "GPT-5.3 Instant", "GPT-5.2 Thinking",
    "GPT-5.1 Thinking", "GPT-4o", "GPT-Red", "GPT-Live",
    "ChatGPT Images 2.5", "Codex harness", "dots", "Agents API",
]):
    ioc("ioc-model-%02d" % i, term, "marker", P)
for i, term in enumerate([
    "CVE-Bench", "SEC-Bench", "SRE-Bench", "Monorepo-Bench",
    "MLE-Bench Revised", "ImpossibleMLEBench", "ExploitGym", "ExploitBench",
    "Sandbox Bench", "HealthBench", "MentalHealthBench", "ABC-Bench",
    "CyScenarioBench", "TroubleshootingBench", "PostTrainBench",
    "PostTrainBench Lite", "KernelGen 1P", "NanoGPT",
    "Human Pathogen Capabilities Test", "Virology Capabilities Test",
    "Atomic Challenges", "Virtual Cell Challenge",
    "Internal Research Debugging Eval", "Auto-review", "ARGO", "LASER",
    "Safe Completions", "Misuse Monitor", "Actor Level Enforcement",
    "Trust-based Access",
]):
    ioc("ioc-eval-%02d" % i, term, "marker", P)
for i, term in enumerate([
    "Bogus Bylines", "Dark Clark", "Politology", "La Compania", "Mia Clark",
    "Michael Harrison", "Ervin B. Hoskins", "Noah Lamington",
    "Sophia Gonzalez", "Ericka Feusier", "Jenny Williams", "Alice Johnson",
    "Alice Donovan", "Moonshot AI", "Kimi", "Frontier Model Forum",
    "PeaceData", "International Security Solutions FZE",
]):
    ioc("ioc-ti-%02d" % i, term, "marker", PB, source_ref="src-blog")
for i, term in enumerate(["SecureBio", "Irregular", "UK AISI"]):
    ioc("ioc-org-%02d" % i, term, "marker", P)

# ---------------- claims ----------------
claim("c-distill-attr", "r-distill", "attribution",
      "Core cluster of the adversarial distillation campaign attributed to "
      "individuals associated with Moonshot AI, the developer of Kimi.",
      "UPSTREAM", ["b-distillextract", "t-reasonreplay"],
      note="Attribution is OpenAI's published assessment, not independently verified.")
claim("c-gptred", "b-staticjb", "attacker_model_identity",
      "GPT-Red is an internal attacker model instructed to jailbreak past "
      "GPT models; a GPT-Red-style internal model based on GPT-5.4-mini "
      "demonstrated worm-like self-replicating prompt injections in RL "
      "self-play training.",
      "OBSERVED", ["b-staticjb", "b-worminjection", "t-gptred"])
claim("c-agentsapi", "r-agentsapi", "harness",
      "The Agents API is a managed service powered by the Codex harness "
      "for orchestration, long-running sessions, and tool use.",
      "OBSERVED", ["r-agentsapi"])
claim("c-dots", "r-dots", "product_definition",
      "dots are proactive assistants with their own identity for access "
      "management and IT-provisioned hardware.",
      "OBSERVED", ["r-dots"])
claim("c-eu", "r-eu", "watermark_scope",
      "Watermark applied to eligible ChatGPT and Codex text output in the "
      "European Union; a watermark detector exists; watermark does not "
      "establish ownership or responsibility.",
      "OBSERVED", ["r-eu"])
claim("c-misreports", "r-misreports", "report_count",
      "15 reports and 3 notices published on the Misalignment Reports and "
      "Notices index.",
      "OBSERVED", ["r-misreports"])
claim("c-falsefront-n", "r-falsefront", "operation_count",
      "30 covert influence operations exposed in the last two and a half "
      "years.",
      "OBSERVED", ["r-falsefront"])
claim("c-falsefront-attr", "r-falsefront", "operation_attribution",
      "Operation 'Bogus Bylines' is Iranian; operation 'Dark Clark' is "
      "Russian.",
      "OBSERVED", ["r-falsefront", "b-falsefront"])
claim("c-argo", "r-argo", "system_definition",
      "ARGO distills black-box reward models into interpretable rubrics "
      "using reinforcement learning.",
      "OBSERVED", ["r-argo"])
claim("c-laser", "r-laser", "system_definition",
      "LASER (Logistic Augmented Sampling over Embeddings, Recursively) "
      "combines lightweight logistic classifiers with reasoning models to "
      "find rare, ambiguous conversations for safety evaluations.",
      "OBSERVED", ["r-laser"])
claim("c-autoreview", "r-autoreview", "deployment",
      "Auto-review released in Codex; a separate agent approves or denies "
      "boundary-crossing actions without synchronous human oversight.",
      "OBSERVED", ["r-autoreview", "b-autoreview"])
claim("c-monit", "r-monit", "open_source",
      "OpenAI released a subset of chain-of-thought monitorability "
      "datasets and reference code.",
      "OBSERVED", ["r-monit"])
claim("c-misframe", "r-misframe", "disclosure_tracks",
      "Three disclosure tracks: Ready for Disclosure, Minor Investigation, "
      "Larger Investigation ('Slow Track').",
      "OBSERVED", ["r-misframe"])
claim("c-distill-window", "r-distill", "activity_window",
      "Earliest observed adversarial-distillation activity in the first "
      "week of July.",
      "OBSERVED", ["r-distill"])

# ---------------- run ----------------
records.append({
    "ref": "run-ingest", "kind": "run",
    "tags": {"lane": LANE},
    "body": {"run_kind": "lane-ingest",
             "tool": "build_bundle.py",
             "tool_version": "1",
             "started": "2026-10-11T16:00:00Z",
             "ended": "2026-10-11T16:45:00Z",
             "params": {"lane": LANE,
                        "sources": 30,
                        "dedup_basis": "lane openai-intel INGEST.md (2026-10-10); "
                                       "match --mode fuzzy pending index rebuild"},
             "coverage": {"description": "OpenAI blog (11), Deployment Safety "
                                         "Hub system cards (8), Alignment "
                                         "Research Blog (9), HF incident blog "
                                         "+ technical report PDF",
                          "scanned": 30, "total": 30, "complete": True}},
})

bundle = {"bundle": 2, "actor": ACTOR, "idempotency_key": IDEMPOTENCY,
          "records": records}
with open("data/lanes/" + LANE + "/bundle.json", "w") as f:
    json.dump(bundle, f, indent=1, ensure_ascii=False)
print("records:", len(records))
kinds = {}
for r in records:
    k = r["kind"] + ":" + r["body"].get("type", "")
    kinds[k] = kinds.get(k, 0) + 1
for k in sorted(kinds):
    print(" ", k, kinds[k])
