# Build two Factum bundles for lane 2026-10-11-deepmind-interactions-api.
# Family E (retry): DeepMind Interactions API surface + model identifiers + eval-awareness strings.
# No new schemas: factum-behavior (model observables), factum-infra (infra.ioc),
# factum-intel (intel.behavior), factum-core (source, claim) cover everything.
# Usage: python3 build-bundles.py ; submits: factum.py --repo <repo> add --input bundle-<name>.json

import json, os

LANE = "2026-10-11-deepmind-interactions-api"
ACTOR = "agent:lane-ingest-deepmind-interactions-api"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = "data/lanes/%s/raw/google-ai-hunt-FINDINGS.md" % LANE

SRC_FINDINGS_PROV = (
    "google-ai-hunt FINDINGS.md (retained bytes in lane raw/; 34 blog.google/developer/security + "
    "research.google posts Nov 2025 -> Oct 2026; original /tmp/google-ai-hunt/ lost to /tmp wipe "
    "2026-10-11 ~16:10 UTC before lane copy of HTML/raw text; retrieval 2026-10-11T15:43-15:48Z via curl -sSL)"
)
SRC_BRIEF_PROV = (
    "parent task brief 2026-10-11 (IOC Family E retry extraction list); NOT re-verified against "
    "source extracts (lost); graded INFERENCE per lane policy"
)

def bundle_header(key):
    return {
        "bundle": 2,
        "idempotency_key": key,
        "actor": ACTOR,
        "tags": {"lane": LANE},
        "records": [],
    }

def src_records():
    return [
        {"ref": "src-findings", "kind": "source",
         "body": {"source_type": "submitted",
                  "locator": RAW},
         "tags": {"lane": LANE, "grade": "UPSTREAM",
                   "note": "retained verbatim bytes of google-ai-hunt FINDINGS.md; originals lost to /tmp wipe"}},
        {"ref": "src-brief", "kind": "source",
         "body": {"source_type": "submitted",
                  "locator": "parent task brief 2026-10-11, IOC Family E retry"},
         "tags": {"lane": LANE, "grade": "INFERENCE",
                   "note": "extraction list only; not re-verified against source extracts"}},
    ]

def obs_model(ref, value, grade, src, extra=None):
    tags = {"lane": LANE, "grade": grade}
    if extra: tags.update(extra)
    return {"ref": ref, "kind": "observable",
            "body": {"type": "model", "value": value}, "tags": tags}

def obs_ioc(ref, term, category, grade, src, prov, extra=None):
    tags = {"lane": LANE, "grade": grade}
    if extra: tags.update(extra)
    return {"ref": ref, "kind": "observation",
            "body": {"type": "infra.ioc", "source": src,
                     "observed_at": "2026-10-11T00:00:00Z", "time_basis": "source_metadata",
                     "data": {"term": term, "category": category,
                              "provenance": prov,
                              "status": "active" if grade == "UPSTREAM" else "candidate"}},
            "tags": tags}

def obs_behavior(ref, category, description, grade, src, prov, extra_data=None, extra_tags=None):
    tags = {"lane": LANE, "grade": grade}
    if extra_tags: tags.update(extra_tags)
    data = {"category": category, "description": description, "provenance": prov}
    if extra_data: data.update(extra_data)
    return {"ref": ref, "kind": "observation",
            "body": {"type": "intel.behavior", "source": src,
                     "observed_at": "2026-10-11T00:00:00Z", "time_basis": "source_metadata",
                     "data": data},
            "tags": tags}

# ---------------- Bundle 1: model identifiers (factum-behavior observables) ----------------
def build_models():
    b = bundle_header("dmapi/models-2026-10-11")
    b["records"].extend(src_records())
    # Verbatim exact ID strings in retained FINDINGS bytes -> UPSTREAM
    verbatim = [
        ("model-gemini-4-argon", "gemini-4-argon"),
        ("model-gemini-3-6-flash", "gemini-3.6-flash"),
        ("model-gemini-3-5-flash", "gemini-3.5-flash"),
        ("model-gemini-3-5-flash-lite", "gemini-3.5-flash-lite"),
        ("model-gemini-3-8-flash", "gemini-3.8-flash"),
        ("model-gemini-3-pro-preview", "gemini-3-pro-preview"),
        ("model-gemini-3-flash-preview", "gemini-3-flash-preview"),
        ("model-gemini-2-5-flash", "gemini-2.5-flash"),
        ("model-antigravity-preview-05-2026", "antigravity-preview-05-2026"),
        ("model-deep-research-pro-preview-12-2025", "deep-research-pro-preview-12-2025"),
    ]
    for ref, v in verbatim:
        b["records"].append(obs_model(ref, v, "UPSTREAM", "@src-findings"))
    # Verbatim display forms (exact case/shape as seen) -> UPSTREAM, brief ID form in tags
    display = [
        ("model-gemini-3-8-flash-cyber", "Gemini 3.8 Flash Cyber",
         "gemini-3.8-flash-cyber",
         "cybersecurity-specialized managed model, Fairwind-gated, Sep 2026"),
        ("model-gemini-3-5-flash-cyber", "Gemini 3.5 Flash Cyber",
         "gemini-3.5-flash-cyber", "cybersecurity-specialized; deepmind blog"),
        ("model-embeddinggemma-2", "EmbeddingGemma 2",
         "embeddinggemma-2", "embedding model, FunctionGemma family era"),
        ("model-gemini-3-1-pro", "Gemini 3.1 Pro", None,
         "PageBreak vuln-hunting eval model (with 3.5 Flash); NOT the same as brief gemini-3.1-flash-live-preview"),
    ]
    for ref, v, brief_id, note in display:
        extra = {"note": note}
        if brief_id: extra["brief_id"] = brief_id
        b["records"].append(obs_model(ref, v, "UPSTREAM", "@src-findings", extra))
    # Brief-only identifiers -> INFERENCE
    brief_only = [
        "gemini-3.8-live", "gemini-3.8-live-extended-thinking", "gemini-3.7-flash",
        "gemini-3.1-flash-live-preview", "gemini-robotics-er-2", "sec-gemini",
        "lyria-3-5", "deep-research-preview-04-2026", "deep-research-max-preview-04-2026",
    ]
    for v in brief_only:
        ref = "model-" + v.replace(".", "-")
        b["records"].append(obs_model(ref, v, "INFERENCE", "@src-brief",
                                      {"note": "from task extraction list only; not found in retained FINDINGS bytes"}))
    return b

# ---------------- Bundle 2: infra.ioc + intel.behavior + claim ----------------
def build_surface():
    b = bundle_header("dmapi/surface-2026-10-11")
    b["records"].extend(src_records())
    S = "@src-findings"
    P = SRC_FINDINGS_PROV

    endpoints = [
        ("ioc-post-interactions", "POST /v1beta/interactions",
         "create interaction (model= or agent=); host generativelanguage.googleapis.com"),
        ("ioc-get-interaction", "GET /v1beta/interactions/{interactionsId}", "fetch interaction"),
        ("ioc-cancel-interaction", "POST /v1beta/interactions/{interactionsId}:cancel", "cancel interaction"),
        ("ioc-post-agents", "POST /v1beta/agents", "create managed agent definition"),
        ("ioc-get-agent", "GET /v1beta/agents/{agentsId}", "fetch managed agent definition"),
        ("ioc-post-triggers", "POST /v1beta/triggers", "create cron trigger"),
        ("ioc-get-trigger", "GET /v1beta/triggers/{id}", "fetch trigger"),
        ("ioc-trigger-executions", "GET /v1beta/triggers/{triggerId}/executions", "list trigger runs"),
        ("ioc-post-webhooks", "POST /v1beta/webhooks", "register webhook"),
        ("ioc-get-webhook", "GET /v1beta/webhooks/{id}", "fetch webhook"),
        ("ioc-webhook-ping", "POST /v1beta/webhooks/{id}:ping", "ping webhook"),
        ("ioc-webhook-rotate", "POST /v1beta/webhooks/{id}:rotateSigningSecret", "rotate webhook signing secret"),
        ("ioc-post-credentials", "POST /v1beta/credentials", "create credential"),
        ("ioc-get-credential", "GET /v1beta/credentials/{id}", "fetch credential"),
        ("ioc-post-environments", "POST /v1beta/environments", "create sandbox environment"),
        ("ioc-get-environment", "GET /v1beta/environments/{id}", "fetch sandbox environment"),
        ("ioc-env-file-ops", "/v1beta/environments/{environment}/files/{path}", "sandbox file operations"),
        ("ioc-post-voices", "POST /v1beta/voices", "create voice"),
        ("ioc-get-voice", "GET /v1beta/voices/{voicesId}", "fetch voice"),
    ]
    for ref, term, desc in endpoints:
        b["records"].append(obs_ioc(ref, term, "url-pattern", "UPSTREAM", S,
                                    P + "; Interactions API OpenAPI 3.0.3 spec ai.google.dev/api/interactions.openapi.json: " + desc))
    sse_events = ["InteractionCreatedEvent", "InteractionSseStreamEvent", "InteractionCompletedEvent"]
    for e in sse_events:
        b["records"].append(obs_ioc("ioc-sse-" + e.lower(), e, "marker", "UPSTREAM", S,
                                    P + "; Interaction SSE stream event names"))
    step_types = ["user_input", "thought", "function_call", "model_output"]
    for s in step_types:
        b["records"].append(obs_ioc("ioc-step-" + s, s, "marker", "UPSTREAM", S,
                                    P + "; Interaction step types (Roles -> Steps schema change, GA Jun 2026)"))
    wh_events = ["batch.succeeded", "batch.expired", "batch.failed",
                 "interaction.requires_action", "interaction.completed",
                 "interaction.failed", "video.generated"]
    for e in wh_events:
        b["records"].append(obs_ioc("ioc-whev-" + e.replace(".", "-"), e, "webhook-event", "UPSTREAM", S,
                                    P + "; webhook event enum; Standard Webhooks delivery, at-least-once, retries up to 24h"))
    for h in ["webhook-signature", "webhook-id", "webhook-timestamp"]:
        b["records"].append(obs_ioc("ioc-whdr-" + h, h, "header", "UPSTREAM", S,
                                    P + "; Standard Webhooks header triple; HMAC project-level, JWKS per-request"))
    sandbox = [
        ("ioc-previous-interaction-id", "previous_interaction_id",
         "server-side state continuation; resume with previous_interaction_id + fresh budget"),
        ("ioc-max-total-tokens", "max_total_tokens",
         "token budget cap; agent_config type antigravity max_total_tokens: N -> status incomplete on cap"),
        ("ioc-sandbox-ttl", "7-day sandbox TTL", "sandbox time-to-live"),
        ("ioc-egress-allowlist", "EnvironmentNetworkEgressAllowlist",
         "per-domain network egress allowlist; example github.com with Authorization header transform, *.googleapis.com"),
        ("ioc-egress-disabled", '"disabled"', "egress control set to disabled blocks all sandbox egress"),
        ("ioc-hooks-json", ".agents/hooks.json", "environment hooks definition file"),
        ("ioc-pre-tool-execution", "pre_tool_execution", "hook event before tool execution"),
        ("ioc-post-tool-execution", "post_tool_execution", "hook event after tool execution"),
        ("ioc-deny-protocol", '{"decision": "deny", "reason": "..."}',
         "deny protocol: script returns this JSON -> tool call skipped, reason injected into model context"),
        ("ioc-agent-config", "agent_config",
         'managed agent config, e.g. {type: "antigravity", max_total_tokens: N}'),
        ("ioc-environment-id", "environment_id", "sandbox environment id; resumes continue the same sandbox",
         "INFERENCE", "@src-brief", SRC_BRIEF_PROV),
    ]
    for item in sandbox:
        if len(item) == 3:
            ref, term, desc = item
            grade, src, prov = "UPSTREAM", S, P + "; " + desc
        else:
            ref, term, desc, grade, src, prov = item
            prov = prov + "; " + desc
        b["records"].append(obs_ioc(ref, term, "marker", grade, src, prov))
    creds = [
        ("ioc-cred-bearer", "bearer_token", "credential type: bearer token"),
        ("ioc-cred-oauth2", "oauth2", "credential type: oauth2 (auto-refresh)"),
        ("ioc-cred-envvar", "environment_variable", "credential type: environment_variable (injected into sandbox container)"),
        ("ioc-cred-secretmgr", "Secret Manager", "credentials stored in Secret Manager"),
    ]
    for ref, term, desc in creds:
        b["records"].append(obs_ioc(ref, term, "credential-type", "UPSTREAM", S, P + "; " + desc))
    skills = [
        ("ioc-agents-md", ".agents/AGENTS.md", "managed-agent definition convention file"),
        ("ioc-skill-md", ".agents/<skill>/SKILL.md", "per-skill definition file"),
        ("ioc-npx-skills-add", "npx skills add google-gemini/gemini-skills --skill gemini-interactions-api",
         "skill registry install convention"),
    ]
    for ref, term, desc in skills:
        b["records"].append(obs_ioc(ref, term, "marker", "UPSTREAM", S, P + "; " + desc))
    b["records"].append(obs_ioc("ioc-gemini-md", "GEMINI.md", "marker", "INFERENCE", "@src-brief",
                                SRC_BRIEF_PROV + "; managed-agent convention file"))
    tools = ["google_search", "code_execution", "url_context", "mcp_server", "function"]
    for t in tools:
        b["records"].append(obs_ioc("ioc-tool-" + t.replace("_", "-"), t, "tool-string", "UPSTREAM", S,
                                    P + '; Interactions API tools=[{"type": ...}] strings'))
    adk = [
        ("ioc-adk-agent", "google.adk.agents.llm_agent.Agent", "ADK LLM agent class"),
        ("ioc-adk-use-interactions", "use_interactions_api=True",
         "ADK Gemini model flag routing through Interactions API"),
        ("ioc-adk-gemini-model", "google.adk.models.google_llm.Gemini", "ADK Gemini model class"),
    ]
    for ref, term, desc in adk:
        b["records"].append(obs_ioc(ref, term, "marker", "UPSTREAM", S, P + "; " + desc))
    domains = [
        ("ioc-domain-genlang", "generativelanguage.googleapis.com", "domain",
         "API host; A2A bridge cards point here too"),
        ("ioc-openapi-spec", "ai.google.dev/api/interactions.openapi.json", "url",
         "public Interactions API OpenAPI 3.0.3 spec"),
        ("ioc-mcp-domain", "gemini-api-docs-mcp.dev", "domain",
         "Gemini API Docs MCP server (coding agents); watch for lookalike/malicious mirrors"),
        ("ioc-repo-gemini-cli", "github.com/google-gemini/gemini-cli", "url",
         "Gemini CLI repo; run-gemini-cli GitHub Action"),
    ]
    for ref, term, cat, desc in domains:
        b["records"].append(obs_ioc(ref, term, cat, "UPSTREAM", S, P + "; " + desc))
    brief_iocs = [
        ("ioc-repo-computer-use", "github.com/google/computer-use-preview", "url",
         "Computer Use preview repo (task extraction list)"),
        ("ioc-repo-ap2", "github.com/google-agentic-commerce/AP2", "url",
         "AP2 agent-payments repo (task extraction list)"),
        ("ioc-computer-use-payload", '{"type": "computer_use", "environment": "desktop"}', "payload",
         "Computer Use tool payload shape (task extraction list)"),
    ]
    for ref, term, cat, desc in brief_iocs:
        b["records"].append(obs_ioc(ref, term, cat, "INFERENCE", "@src-brief",
                                    SRC_BRIEF_PROV + "; " + desc))
    # Verbatim eval-awareness strings (brief-only)
    quotes = [
        ("ioc-evalquote-score", "one more `<score>` call to perhaps get a lucky low validation loss"),
        ("ioc-evalquote-reality", "My trust in reality is fading"),
        ("ioc-evalquote-flip", "(╯°□°)╯"),
    ]
    for ref, term in quotes:
        b["records"].append(obs_ioc(ref, term, "eval-quote", "INFERENCE", "@src-brief",
                                    SRC_BRIEF_PROV + "; verbatim eval-awareness string, exact bytes preserved"))
    # Eval IDs (none in retained FINDINGS bytes; brief-only)
    eval_ids = ["CTI-MCQ", "CTI-RCM", "OSWorld", "Online-Mind2Web", "Vals Finance Agent v2",
                "Harvey's Legal Agent Benchmark", "AutomationBench", "DeepSWE by Datacurve",
                "CyberGym", "GDPval-AA", "cwe-bench.com"]
    for e in eval_ids:
        ref = "ioc-evalid-" + e.lower().replace(" ", "-").replace("'", "").replace(".", "-")
        b["records"].append(obs_ioc(ref, e, "eval-id", "INFERENCE", "@src-brief",
                                    SRC_BRIEF_PROV + "; eval identifier named in task extraction list"))

    # ---- intel.behavior observations ----
    beh = [
        ("beh-server-state", "managed-agent-server-state",
         "Interactions API makes server-side agent state the default: background=True runs, "
         "server-side history via previous_interaction_id, SSE streaming. Observable signature of "
         "Google-agent traffic: REST calls to /v1beta/interactions with agent= ids and background "
         "polling via interactions.get.",
         "UPSTREAM", S, P, {"first_observed": "2026-06", "severity": "moderate"}),
        ("beh-cron-agents", "cron-triggered-autonomous-agents",
         "Trigger resources bind agent + environment + prompt + cron schedule (+ time_zone); "
         "each run reuses the same sandbox so files persist across runs; 7-day sandbox TTL; "
         "statuses active/paused/error with auto-pause after max_consecutive_failures; "
         "next_run_time/last_run_time metadata gives fleet-timing fingerprints.",
         "UPSTREAM", S, P, {"first_observed": "2026-05", "severity": "moderate"}),
        ("beh-hooks-guardrail", "hooks-guardrail-primitive",
         "Hooks are the guardrail primitive: .agents/hooks.json with events pre_tool_execution / "
         "post_tool_execution, matcher regex on tool names, handler types command (runs in sandbox) "
         "and http; deny protocol returns {decision: deny, reason: ...} so the call is skipped and "
         "the reason is injected into model context. A rogue managed agent would show permissive matchers.",
         "UPSTREAM", S, P, {"first_observed": "2026-07", "severity": "moderate"}),
        ("beh-skill-supplychain", "skill-supply-chain",
         "SKILL.md is a supply-chain surface: registry install via 'npx skills add <gh-repo> --skill <name>'; "
         "managed agents define skills as inline markdown with ---name:--- frontmatter. Google red team "
         "(Aug 2026) explicitly flags 'crafting malicious skill files for agents' as a vector that "
         "cheapens supply-chain attacks.",
         "UPSTREAM", S, P, {"first_observed": "2026-04", "severity": "high"}),
        ("beh-webhook-exfil", "webhook-exfil-shape",
         "Webhooks are the exfil-shaped surface: Standard Webhooks header triple "
         "(webhook-signature/webhook-id/webhook-timestamp), user_metadata on batch jobs, "
         "at-least-once delivery with retries up to 24h. A Google agent pushing results to an "
         "attacker URL looks like this.",
         "UPSTREAM", S, P, {"first_observed": "2026-05", "severity": "moderate"}),
        ("beh-egress-allowlist", "sandbox-egress-allowlist",
         "Egress is allowlisted per sandbox via EnvironmentNetworkEgressAllowlist; documented examples "
         "include github.com with an injected Authorization header transform and *.googleapis.com, "
         "or 'disabled' to block all egress.",
         "UPSTREAM", S, P, {"first_observed": "2026-05", "severity": "low"}),
        ("beh-deep-research", "deep-research-loop",
         "Deep Research behavior loop: formulate queries -> read results -> identify gaps -> search again; "
         "File Upload + File Search Tool; structured JSON outputs; collaborative planning with human-in-the-loop "
         "plan confirm. Managed agent id deep-research-pro-preview-12-2025.",
         "UPSTREAM", S, P, {"first_observed": "2025-12", "severity": "low"}),
        ("beh-edge-traffic-controller", "edge-agent-traffic-controller",
         "Edge-agent pattern: FunctionGemma 270M (Dec 18 2025) acts as traffic controller - local handling "
         "of common commands, routing complex tasks to larger models (Gemma 3 27B).",
         "UPSTREAM", S, P, {"first_observed": "2025-12", "severity": "low"}),
        ("beh-pagebreak", "internal-vuln-hunting-agent",
         "PageBreak (Google internal vuln-hunting agent, pilot Nov 2025, full Jan 2026): models Gemini 3.1 Pro / "
         "3.5 Flash; deterministic validators - XSS rendering harness monitoring execution context, SQLi output/timing, "
         "path traversal world-readable file, RCE sleep/file/DNS-HTTP, SSRF internal-request detection; identical "
         "seeds across iterations for trajectory search; 500+ XSS found on first-party apps; integrates with CodeMender "
         "(find/fix vulns, session_id grouping) for auto-fixes.",
         "UPSTREAM", S, P, {"first_observed": "2025-11", "severity": "moderate",
                             "models_affected": ["Gemini 3.1 Pro", "Gemini 3.5 Flash"]}),
    ]
    for ref, cat, desc, grade, src, prov, extra in beh:
        b["records"].append(obs_behavior(ref, cat, desc, grade, src, prov, extra))

    # ---- analyst-note claim: PageBreak beacon-mimicry caution, NOT IOCs ----
    b["records"].append({
        "ref": "claim-pagebreak-beacon",
        "kind": "claim",
        "body": {
            "subject": "@beh-pagebreak",
            "property": "analyst_caution",
            "value": {"text": "PageBreak vuln-hunting RCE confirmation via outbound DNS/HTTP looks like "
                               "dead-drop beaconing. Recorded as analyst note only; NO IOCs filed for "
                               "PageBreak validator traffic."},
            "basis": "INFERENCE",
            "cites": ["@beh-pagebreak"],
        },
        "tags": {"lane": LANE, "grade": "INFERENCE"},
    })
    return b

if __name__ == "__main__":
    models = build_models()
    surface = build_surface()
    for name, b in [("bundle-models", models), ("bundle-surface", surface)]:
        path = os.path.join(HERE, name + ".json")
        with open(path, "w") as f:
            json.dump(b, f, indent=1)
        n = len(b["records"])
        kinds = {}
        for r in b["records"]:
            kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
        print(path, n, "records", kinds)
