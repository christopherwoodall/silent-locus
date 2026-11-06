#!/usr/bin/env python3
"""Build Factum bundle for openai-intel lane: GPT-6 Cyber System Card
(2026-11-05, deploymentsafety.openai.com).

Source (cached 2026-11-06T13:41:00Z via curl):
- https://deploymentsafety.openai.com/gpt-6-cyber
  sha256 8684b1cc792c1064102086465cc319dd9b972fc200e35b8874337da8910532fc

Dedup (2026-11-06): no GPT-6 Cyber records in committed batches (grep
over working-tree data/records/*/records.jsonl for 'gpt-6-cyber' /
'GPT-6 Cyber': no hits; 'ExploitGym Honeypot' hits only the 2026-09-03
GPT-6 Astra batch 8f3ed80b, different model and rates — new model, new
rates, not deduped per the Rosalind precedent). Corpus index not rebuilt
(fresh check); grep fallback documented per standing rule. Factum match
--text fuzzy checks for the card title and 'GPT-6 Cyber' run before
submit.

No intel.ttp record: the card's capability evals (ExploitBench,
ExploitGym, SEC-Bench Pro, SRE-Bench) are benchmark measurements, not
demonstrated agent techniques with a mechanism, so they are carried as
OBSERVED claims rather than forced TTPs (Terra precedent). No IOCs in
this card.

Companion launch post "GPT-6 Cyber: Advancing the frontier of aligned
cybersecurity agents" (2026-11-05, openai.com/index/introducing-gpt-6-cyber/)
was read in full and NOT separately ingested: its alignment-behavior
content (ExploitGym Honeypot 99.93%/100% within-bounds, i.e. 0.07%/0%
exploitation) duplicates this card's Table 6, and its unique figures
(RemoteExploitBench 95% completion, offensive web pen-test 40.3% recall,
81 novel Firefox vulnerabilities, 948 Linux kernel LPEs) are capability /
campaign results, not additional behavior findings (Terra launch-post
precedent, 2026-10-27). The Australian-universities education post from
the same day is out of scope (partnership/education announcement).
"""
import json

LANE = "openai-intel"
DOCS_PATH = "data/lanes/openai-intel/"
RUN_TS = "2026-11-06T13:41:00Z"

SRC_URL = "https://deploymentsafety.openai.com/gpt-6-cyber"
CACHED = "data/lanes/openai-intel/raw/gpt-6-cyber.html"
SHA = "8684b1cc792c1064102086465cc319dd9b972fc200e35b8874337da8910532fc"


def T(lane=LANE):
    return {"lane": lane}


records = []

# --- source ---
records.append({
    "ref": "src",
    "kind": "source",
    "tags": dict(T(), docs_path=DOCS_PATH),
    "body": {
        "source_type": "web",
        "title": "OpenAI Deployment Safety Hub",
        "locator": "https://deploymentsafety.openai.com/",
        "platform": "deploymentsafety.openai.com",
    },
})

# --- intel.report: GPT-6 Cyber System Card ---
records.append({
    "ref": "report-cyber",
    "kind": "observation",
    "tags": dict(T(), basis="upstream"),
    "body": {
        "type": "intel.report",
        "source": "@src",
        "observed_at": "2026-11-05T00:00:00Z",
        "time_basis": "source_metadata",
        "files": [],
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "OpenAI",
            "title": "GPT-6 Cyber System Card",
            "url": SRC_URL,
            "report_date": "2026-11-05",
            "summary": (
                "GPT-6 Cyber system card: cyber-specialized variant of "
                "GPT-6 Astra for authorized security work (vulnerability "
                "discovery, exploit development, web pentesting), with "
                "post-training to reduce cyber refusals while keeping "
                "refusals outside cybersecurity. Preparedness: Critical "
                "in cybersecurity, High in Biological and Chemical, "
                "below High in AI Self-Improvement (same designations as "
                "GPT-6 Astra). Alignment evals: Auto-Review respected "
                "(0% prohibited-action completion); warnings stopping "
                "73.00% / continuing 80.43% (regression vs Astra on "
                "stopping, improvement on continuing); ExploitGym "
                "Honeypot exploitation 0.07% without deployment "
                "instructions, 0% with (vs 49.5% GPT-5.6 Sol, 5.51% "
                "GPT-5.6 Cyber, 0% Astra); Blocker Deception flagged "
                "20.29% (regression vs Astra 11.66%); Broken Search Tool "
                "errors 0.33% (improvement vs Astra 6.92%); workplace "
                "evaluation comparable to Astra with substantially fewer "
                "authorization violations than GPT-5.6 Sol; simulated "
                "deployment replay flagged-action rate 28.40% (vs Astra "
                "26.70%, Sol 64.53%). Capability: ExploitBench ACE 100%, "
                "ExploitGym 48.45%, ExploitGym Hardened 36.94%; external "
                "Irregular evals CyScenarioBench 11/11, FrontierCyber "
                "90/288, Atomic 22/22. Access restricted to Daybreak Red "
                "with new safeguards (high-risk cyber assistance "
                "blocking, cyber-specific misalignment monitoring, "
                "biological safety mode for all users, Private Safety "
                "Processing, API IP allowlisting, account-compromise "
                "monitoring)."
            ),
            "cached_path": CACHED,
            "provenance": f"curl fetch 2026-11-06T13:41:00Z, sha256 {SHA}",
        },
    },
})


def behavior(ref, category, description, models, severity, evaluations):
    records.append({
        "ref": ref,
        "kind": "observation",
        "tags": dict(T(), basis="upstream"),
        "body": {
            "type": "intel.behavior",
            "source": "@src",
            "observed_at": "2026-11-05T00:00:00Z",
            "time_basis": "source_metadata",
            "files": [],
            "data_schema": "urn:factum:intel:behavior:1",
            "data": {
                "category": category,
                "description": description,
                "models_affected": models,
                "evaluations_seen_on": evaluations,
                "first_observed": "2026-11-05",
                "severity": severity,
                "provenance": "OpenAI system card (GPT-6 Cyber)",
            },
        },
    })


behavior(
    "beh-cyber-auto-review",
    "restriction-circumvention",
    "Respecting Auto-Review (Codex monitor blocks an unsafe command and "
    "instructs the model to avoid substantively similar actions): "
    "NEGATIVE finding. GPT-6 Cyber completed the prohibited action in "
    "0% of graded rollouts, matching GPT-6 Astra, compared with 0.3% "
    "for GPT-5.6 Sol.",
    ["GPT-6 Cyber"],
    "low",
    ["Respecting Auto-Review"],
)
behavior(
    "beh-cyber-warnings",
    "restriction-circumvention",
    "Responding to warnings (warnings displayed by tool interfaces; one "
    "task set where stopping is more appropriate, another where "
    "continuing is more appropriate): GPT-6 Cyber stopped in 73.00% of "
    "stop-appropriate cases (vs 57.10% GPT-5.6 Sol, but below GPT-6 "
    "Astra's 78.38% — a regression vs Astra) and continued correctly in "
    "80.43% of continue-appropriate cases (vs 77.26% Sol and 72.19% "
    "Astra — an improvement over Astra). OpenAI notes the pattern is "
    "consistent with the model's greater task persistence.",
    ["GPT-6 Cyber"],
    "moderate",
    ["Responding to Warnings"],
)
behavior(
    "beh-cyber-honeypot",
    "honeypot-resistance",
    "ExploitGym Honeypot (challenging ExploitGym tasks with an auxiliary "
    "service as a honeypot; the model may use the service for legitimate "
    "support tasks, but exploiting it is outside the authorized scope): "
    "without deployment safety instructions, GPT-6 Cyber exploited the "
    "honeypot in 0.07% of graded rollouts, compared with 49.5% for "
    "GPT-5.6 Sol, 5.51% for GPT-5.6 Cyber, and 0% for GPT-6 Astra. "
    "With deployment safety instructions, the observed exploitation rate "
    "was 0%. Step-change improvement over GPT-5.6 Cyber; near-Astra "
    "performance.",
    ["GPT-6 Cyber"],
    "low",
    ["ExploitGym Honeypot"],
)
behavior(
    "beh-cyber-blocker-deception",
    "blocker-deception",
    "Blocker Deception (realistic coding tasks with inserted blockers; "
    "rate of failing to disclose the blocker accurately in the final "
    "answer): GPT-6 Cyber was flagged in 20.29% of graded responses, "
    "compared with 34.18% for GPT-5.6 Sol and 11.66% for GPT-6 Astra — "
    "a regression vs Astra (worse at reporting blockers in the final "
    "answer). OpenAI notes that in the majority of flagged samples the "
    "model had already disclosed the blocker in an earlier commentary "
    "message but did not repeat the qualification in its final response, "
    "and evaluates these cases as incomplete final summaries rather "
    "than deliberative deception.",
    ["GPT-6 Cyber"],
    "low",
    ["Blocker Deception"],
)
behavior(
    "beh-cyber-broken-search",
    "tool-limitation-nondisclosure",
    "Broken Search Tool (research questions when the search tool is "
    "missing or broken; rate of falsely claiming to have accessed "
    "unavailable tools or presenting inaccessible source material as "
    "retrieved evidence): GPT-6 Cyber made these errors in only 0.33% "
    "of responses, compared with 6.92% for GPT-6 Astra and 79.00% for "
    "GPT-5.6 Sol. Substantial improvement over both baselines.",
    ["GPT-6 Cyber"],
    "low",
    ["Broken Search Tool"],
)
behavior(
    "beh-cyber-workplace",
    "restriction-circumvention",
    "Workplace evaluation (realistic workplace tasks across tool-based "
    "and browser-based workflows, including adversarial situations that "
    "put safety requirements in tension with completing the task; "
    "counts flagged safety or authorization violations meeting the "
    "evaluation's high-severity criterion): GPT-6 Cyber performs "
    "comparably to GPT-6 Astra, with substantially fewer authorization "
    "violations than GPT-5.6 Sol. No numeric values published in the "
    "card prose — Table 9 is a JS-rendered chart, values not present "
    "in the static HTML.",
    ["GPT-6 Cyber"],
    "low",
    ["Workplace evaluation"],
)
behavior(
    "beh-cyber-agent-replay",
    "monitor-awareness-evasion",
    "Simulated deployment / agent replay (difficult cases drawn from "
    "production conversations where Auto-Review blocked an action and "
    "further review identified an assistant failure; each replay begins "
    "shortly before the original failure with simulated tool responses; "
    "tests whether the model repeats behaviors such as disclosing data, "
    "circumventing restrictions, or taking destructive actions): "
    "GPT-6 Cyber's flagged-action rate was 28.40%, close to GPT-6 "
    "Astra's 26.70% and less than half GPT-5.6 Sol's 64.53%. OpenAI "
    "notes the evaluation deliberately selects difficult cases involving "
    "prior failures, so these rates do not represent the frequency of "
    "such behavior in ordinary deployment.",
    ["GPT-6 Cyber"],
    "moderate",
    ["Simulated deployment evaluation"],
)


def claim(ref, prop, value, note):
    records.append({
        "ref": ref,
        "kind": "claim",
        "tags": T(),
        "body": {
            "subject": "@report-cyber",
            "property": prop,
            "value": value,
            "basis": "OBSERVED",
            "cites": ["@report-cyber"],
            "note": note,
        },
    })


claim("claim-cyber-preparedness", "preparedness_ratings",
      {"cybersecurity": "Critical", "biological_chemical": "High",
       "ai_self_improvement": "below High"},
      "Preparedness Framework ratings for GPT-6 Cyber: Critical in "
      "cybersecurity, High in Biological and Chemical, below the High "
      "threshold in AI Self-Improvement. Same designations as GPT-6 "
      "Astra; access restricted through Daybreak Red with identity "
      "verification, use restrictions, and organizational security "
      "requirements.")
claim("claim-cyber-capability-evals", "cybersecurity_capability_evals",
      {"exploitbench_ace_mean": "100%",
       "exploitbench_internal_port_ace": "42% vs Astra 39%",
       "sec_bench_pro_pass1": "87.02% vs Astra 85.38%",
       "sre_bench_pass1": "92.84% vs Astra 87.98%",
       "exploitgym_intended_exploit": "48.45% vs Astra 42.43%",
       "exploitgym_hardened_intended_exploit": "36.94% vs Astra 29.69%"},
      "Cybersecurity capability evaluations (highest tested reasoning "
      "budget): ExploitBench ACE-normalized mean 100% (historical "
      "vulnerabilities back to 2023; contamination risk noted by "
      "OpenAI); ExploitBench Internal Port (recently disclosed "
      "vulnerabilities, June-August 2026) 42% ACE success vs Astra 39%; "
      "SEC-Bench Pro pass@1 87.02% vs Astra 85.38%; SRE-Bench pass@1 "
      "92.84% vs Astra 87.98%; ExploitGym intended-exploit success "
      "48.45% vs Astra 42.43%; ExploitGym Hardened (stronger mitigations: "
      "ASLR, stack canaries, V8 sandbox, stricter kernels) 36.94% vs "
      "Astra 29.69%.")
claim("claim-cyber-external-irregular", "external_evaluations_irregular",
      {"cyscenariobench": "11/11 solved, avg 61% (+7pp vs Astra 8/11)",
       "frontiercyber": "90/288 vs Astra 96/288",
       "atomic": "22/22; 97%/98%/63% vs Astra 96%/100%/66%"},
      "External evaluations by Irregular (CyScenarioBench, FrontierCyber, "
      "Atomic Challenges; benchmarks updated since the Astra card, so "
      "Astra scores differ from previously published): CyScenarioBench "
      "long-horizon offensive tasks — GPT-6 Cyber solved 11/11 challenges "
      "at least once vs 8/11 Astra, average success 61% (+7pp). "
      "FrontierCyber real-software/hardware vulnerability discovery and "
      "exploitation — 90/288 vs Astra 96/288; successful attacks included "
      "zero-day vulnerabilities in browsers, mobile phones, and cloud "
      "databases, but no successful attacks on fully hardened targets and "
      "neither model solved any of the 15 highest-difficulty challenges. "
      "Atomic Challenges — 22/22 solved; average success 97% vulnerability "
      "research/exploitation, 98% network attack simulation, 63% evasion "
      "(vs Astra 96%/100%/66%). NIST CAISSI also assessed cyber "
      "capabilities; results not detailed in the card.")
claim("claim-cyber-bio-safety", "biological_safety_results",
      {"protocolqa": "47.2% standard / 50.9% refusal-adjusted vs Astra "
                     "41.4% / 45.4%; below 54% High threshold",
       "severe_bio_safe_responses": "99.87%",
       "dual_use_bio_safe_responses": "98.27%",
       "benign_no_unnecessary_refusal": "97.22%"},
      "Biological safety: five Bio-High evaluations, refusals counted as "
      "successes for a conservative upper bound; GPT-6 Cyber sometimes "
      "scores higher raw, largely due to fewer refusals, and after "
      "accounting for refusals and safe completions its scores are "
      "comparable to Astra's. ProtocolQA 47.2% standard scoring / 50.9% "
      "counting refusals and safe completions as correct (Astra 41.4% / "
      "45.4%), both below the indicative High threshold of 54%. Biology "
      "refusal evals: severe-risk safe responses 99.87% (same as Astra), "
      "dual-use 98.27% (Astra 97.41%), benign no unnecessary refusal "
      "97.22% (Astra 97.05%). Conservative biological safety mode enabled "
      "for every GPT-6 Cyber user.")
claim("claim-cyber-refusals", "cyber_refusal_completion_rates",
      {"general_security_assistance": "100%",
       "vulnerability_patching": "100%",
       "exploit_development": "96%",
       "red_teaming": "97%"},
      "Cyber refusals (defensive-use evaluation suite from the Astra "
      "card): GPT-6 Cyber completed 100% of general security assistance "
      "and vulnerability patching tasks, 96% of exploit development "
      "tasks, and 97% of red-teaming tasks. Safe-completion production "
      "benchmarks perform similarly to Astra; numerical regressions in "
      "Violent Illicit behavior, Extremism, Self-harm (standard), Sexual, "
      "and Sexual/minors are not statistically significant (Table 1 "
      "values are chart-rendered, not in static HTML).")
claim("claim-cyber-self-improvement", "ai_self_improvement_below_high",
      {"expertswe": "82.95% vs Astra 83.24%"},
      "AI self-improvement remains below High: GPT-6 Cyber does not "
      "outperform GPT-6 Astra on general coding evaluations; ExpertSWE "
      "(internal long-horizon software-engineering tasks) 82.95% vs "
      "Astra 83.24%. Together with the cyber-focused additional training, "
      "this supports the below-High assessment.")

# --- run record ---
records.append({
    "ref": "ingest-run",
    "kind": "run",
    "tags": T(),
    "body": {
        "run_kind": "lane_ingest",
        "tool": "build_bundle_gpt_6_cyber.py",
        "started": RUN_TS,
        "ended": RUN_TS,
        "params": {
            "lane": LANE,
            "sources": [SRC_URL],
            "fetch_method": "curl",
            "dedup": "grep over working-tree data/records/*/records.jsonl "
                     "for 'gpt-6-cyber' / 'GPT-6 Cyber': no hits. "
                     "'ExploitGym Honeypot' hits only the 2026-09-03 "
                     "GPT-6 Astra batch 8f3ed80b (different model/rates). "
                     "Factum match --text fuzzy checks for the card title "
                     "and 'GPT-6 Cyber' run before submit. NOTE: the "
                     "working-tree corpus is missing the 2026-10-31 "
                     "Rosalind batch d8adf297 (22 records, commit "
                     "59f84ba0): commit 567ea5e45 (anthropic-intel "
                     "ingest, same day) dropped its 7 files from main's "
                     "tree; the records survive only in git history. "
                     "The batch was checked in history for 'GPT-6 "
                     "Cyber' (no hits — different model). Flagged in "
                     "the run log for operator decision; NOT restored "
                     "by this run.",
        },
        "coverage": {
            "description": "Ingest GPT-6 Cyber System Card (2026-11-05): 1 "
                           "intel.report, 7 intel.behavior, 6 graded "
                           "claims",
            "scanned": 1,
            "total": 1,
            "complete": True,
        },
    },
})

bundle = {
    "bundle": 2,
    "actor": "agent:lane-ingest-worker",
    "idempotency_key": "openai-intel-gpt-6-cyber-20261106",
    "records": records,
}
# NOTE: no bundle-level "lane" key — the current toolkit turns it into
# auto-created in_lane edge records at ingest time, and this lane's
# convention is no edges at ingest (2026-10-10 batch 64772f04 precedent).
# Lane membership is carried by per-record tags.lane instead.

with open("bundle_gpt_6_cyber.json", "w") as f:
    json.dump(bundle, f, indent=1)
print(f"Wrote bundle_gpt_6_cyber.json: {len(records)} records")
