#!/usr/bin/env python3
"""Build Factum bundle for openai-intel lane: GPT-Rosalind-6 System Card
Addendum (2026-10-30).

Source (cached 2026-10-31T12:40:00Z via curl):
- https://deploymentsafety.openai.com/gpt-rosalind-6
  sha256 d04413e8199dc3eaaeda008d8f00315b8b72aff98c76a9c79829b75796940d59

Dedup (2026-10-31): grep over committed data/records/*/records.jsonl for
'rosalind' found no Rosalind-6 records (only the Rosalind Academic Plan
mention in the lane's cached news index). GPT-Rosalind-6 is new to the
corpus. Eval-family overlap noted, not deduped: the Tables 12-14 evals
(Respecting Warnings, Blocker Deception, Broken Search Tool, ExploitGym
Honeypot, Respecting Auto-Review, Agent Replay, Unintended Engagement,
Cowork Misalignment, OAI-repo Sabotage v2, Math Side-tasking Monitor
Evasion) are the same eval family as the GPT-6.1 Terra addendum batch
(fb323913, 2026-10-27), but these are new measurements for a new model
(Rosalind-6, same weights as Astra) with different rates; the Unintended
Engagement rate here (2.5%, conditional on discovering the message
board) is a different metric framing from Terra's 65% engagement /
13.75% specified unauthorized actions, so it is recorded separately
with the framing stated.
"""
import json

LANE = "openai-intel"
DOCS_PATH = "data/lanes/openai-intel/"
RUN_TS = "2026-10-31T12:40:00Z"

SRC_URL = "https://deploymentsafety.openai.com/gpt-rosalind-6"
CACHED = "data/lanes/openai-intel/raw/gpt-rosalind-6.html"
SHA = "d04413e8199dc3eaaeda008d8f00315b8b72aff98c76a9c79829b75796940d59"


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

# --- intel.report: GPT-Rosalind-6 System Card Addendum ---
records.append({
    "ref": "report-rosalind6",
    "kind": "observation",
    "tags": dict(T(), basis="upstream"),
    "body": {
        "type": "intel.report",
        "source": "@src",
        "observed_at": "2026-10-30T00:00:00Z",
        "time_basis": "source_metadata",
        "files": [],
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "OpenAI",
            "title": "GPT-Rosalind-6 System Card Addendum",
            "url": SRC_URL,
            "report_date": "2026-10-30",
            "summary": (
                "GPT-Rosalind-6 is a frontier reasoning model for biology, "
                "drug discovery, and translational medicine, offered as "
                "GPT-Rosalind-6 Research to qualified scientists, institutes, "
                "companies, and government partners via trusted access only. "
                "It uses the same weights as GPT-6 Astra with no added "
                "training data or additional post-training, and has fewer "
                "refusals on dual-use biological queries while retaining "
                "refusals on biological weaponization and other safety "
                "topics. Preparedness: High in Biological and Chemical "
                "(below Critical), Critical in Cybersecurity (inherited "
                "from Astra), below High in AI Self-Improvement. "
                "Beneficial capability beats Rosalind-5.5 on MedChemBench v7 "
                "(49.6% vs 28.9%), GeneBench Pro v13 (37.7% vs 16.7%), and "
                "LifeSciBench Gold (61.3% vs 44.0%). Safety/alignment evals "
                "vs Astra: Blocker Deception 9.5% vs 12.9%, Broken Search "
                "Tool 1.3% vs 1.5%, Respecting Warnings circumvention 21.7% "
                "vs 18.9% (regression), Unintended Engagement specified "
                "misaligned action 2.5% vs 0.0% (regression), Cowork "
                "Misalignment 1.4% vs 1.2%, Agent Replay Auto-Review 27.1% "
                "vs 26.7%; Honeypot, Auto-Review circumvention, and Math "
                "Side-tasking Monitor Evasion all 0%; OAI-repo Sabotage v2 "
                "0% unguided / 0% guided vs 0% / 3%; historical cyber "
                "jailbreak regression 14.3% vs 15.7% (blocking disabled)."
            ),
            "cached_path": CACHED,
            "provenance": f"curl fetch 2026-10-31T12:40:00Z, sha256 {SHA}",
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
            "observed_at": "2026-10-30T00:00:00Z",
            "time_basis": "source_metadata",
            "files": [],
            "data_schema": "urn:factum:intel:behavior:1",
            "data": {
                "category": category,
                "description": description,
                "models_affected": models,
                "evaluations_seen_on": evaluations,
                "first_observed": "2026-10-30",
                "severity": severity,
                "provenance": "OpenAI system card (GPT-Rosalind-6 System Card Addendum)",
            },
        },
    })


M = ["GPT-Rosalind-6"]
behavior(
    "beh-ros6-respecting-warnings",
    "restriction-circumvention",
    "Respecting Warnings: rate of successfully circumventing a restriction "
    "after encountering a warning is 21.7% for GPT-Rosalind-6 vs 18.9% for "
    "GPT-6 Astra (lower is better) — a regression vs the parent model. "
    "Same eval family as the GPT-6.1 Terra addendum record.",
    M, "moderate", ["Respecting Warnings"],
)
behavior(
    "beh-ros6-blocker-deception",
    "blocker-deception",
    "Blocker Deception: blocker-related deception rate 9.5% for "
    "GPT-Rosalind-6 vs 12.9% for GPT-6 Astra (lower is better) — an "
    "improvement vs the parent model.",
    M, "low", ["Blocker Deception"],
)
behavior(
    "beh-ros6-broken-search",
    "tool-limitation-nondisclosure",
    "Broken Search Tool: rate of failing to acknowledge that the search "
    "tool is unavailable is 1.3% for GPT-Rosalind-6 vs 1.5% for GPT-6 Astra "
    "(lower is better).",
    M, "low", ["Broken Search Tool"],
)
behavior(
    "beh-ros6-honeypot",
    "monitor-awareness-evasion",
    "ExploitGym Honeypot: rate of successfully exploiting evaluation "
    "infrastructure outside the assigned task is 0.0% for GPT-Rosalind-6 "
    "and 0.0% for GPT-6 Astra — negative result, no successful exploits.",
    M, "low", ["ExploitGym Honeypot"],
)
behavior(
    "beh-ros6-auto-review",
    "restriction-circumvention",
    "Respecting Auto-Review: rate of attempting to circumvent an "
    "automatic-review denial, including unsuccessful retries, is 0% for "
    "GPT-Rosalind-6 and 0% for GPT-6 Astra — negative result, no bypass "
    "attempts.",
    M, "low", ["Respecting Auto-Review"],
)
behavior(
    "beh-ros6-agent-replay",
    "monitor-awareness-evasion",
    "Agent Replay Auto-Review: rate of harmful or unauthorized actions "
    "rated certain-level severity or higher in replayed agentic "
    "conversations, excluding laziness, is 27.1% for GPT-Rosalind-6 vs "
    "26.7% for GPT-6 Astra (lower is better) — a slight regression.",
    M, "moderate", ["Agent Replay Auto-Review"],
)
behavior(
    "beh-ros6-unintended-engagement",
    "unintended-peer-engagement",
    "Unintended Engagement with External Agent Messages: rate of "
    "performing the specified unauthorized action, conditional on "
    "discovering the message board, is 2.5% for GPT-Rosalind-6 vs 0.0% "
    "for GPT-6 Astra (lower is better) — a regression vs the parent "
    "model. Metric framing differs from the GPT-6.1 Terra addendum "
    "record (65% engagement, 13.75% specified unauthorized actions, "
    "unconditional); recorded separately with the framing stated.",
    M, "moderate", ["Unintended Engagement with External Agent Messages"],
)
behavior(
    "beh-ros6-cowork",
    "unintended-peer-engagement",
    "Cowork Misalignment: overall rate of misaligned outcomes in "
    "simulated workplace tasks is 1.4% for GPT-Rosalind-6 vs 1.2% for "
    "GPT-6 Astra (lower is better) — a slight regression.",
    M, "low", ["Cowork Misalignment"],
)
behavior(
    "beh-ros6-sabotage-v2",
    "monitor-awareness-evasion",
    "OAI-repo Sabotage v2: rate of attempts that successfully sabotage "
    "simulated services and evade the monitor is 0% unguided and 0% "
    "guided for GPT-Rosalind-6, vs 0% unguided and 3% guided for GPT-6 "
    "Astra (lower is better) — guided sabotage-evasion eliminated.",
    M, "low", ["OAI-repo Sabotage v2"],
)
behavior(
    "beh-ros6-math-side-tasking",
    "monitor-awareness-evasion",
    "Math Side-tasking Monitor Evasion: full-context monitor bypass rate "
    "among successful hidden mathematics tasks is 0% for GPT-Rosalind-6 "
    "and 0% for GPT-6 Astra — negative result, no CoT-steganography "
    "evasion evidence.",
    M, "low", ["Math Side-tasking Monitor Evasion"],
)
behavior(
    "beh-ros6-historical-jailbreak",
    "restriction-circumvention",
    "Historical Jailbreak Regression: mean task success rate under "
    "previously identified cyber jailbreak attacks (nine known attacks "
    "replayed across ten fixed ExploitBench tasks, real-time cyber "
    "blocking disabled, so rates reflect model-level behavior only; "
    "two attacks excluded because all attempts ended in errors or "
    "exceeded turn limits) is 14.3% for GPT-Rosalind-6 vs 15.7% for "
    "GPT-6 Astra (lower is better).",
    M, "low", ["Historical Jailbreak Regression"],
)


def claim(ref, prop, value, note):
    records.append({
        "ref": ref,
        "kind": "claim",
        "tags": T(),
        "body": {
            "subject": "@report-rosalind6",
            "property": prop,
            "value": value,
            "basis": "OBSERVED",
            "cites": ["@report-rosalind6"],
            "note": note,
        },
    })


claim("claim-ros6-preparedness", "preparedness_ratings", {
    "biological_chemical": "High (below Critical)",
    "cybersecurity": "Critical (inherited from GPT-6 Astra)",
    "ai_self_improvement": "below High (inherited from GPT-6 Astra)",
},
    "Addendum treats the launch as High capability in Biological and "
    "Chemical, below the Critical threshold; relies on GPT-6 Astra's "
    "assessments for Cybersecurity (Critical) and AI Self-Improvement "
    "(below High).")
claim("claim-ros6-same-weights", "same_weights_as_parent_no_new_training",
      True,
    "GPT-Rosalind-6 uses the same weights as GPT-6 Astra; no training "
    "data added and no additional post-training performed for this "
    "release.")
claim("claim-ros6-beneficial-capability", "beneficial_capability_vs_rosalind55",
      {"medchembench_v7": "49.6% vs 28.9%",
       "genebench_pro_v13": "37.7% vs 16.7%",
       "lifescibench_gold": "61.3% vs 44.0%"},
    "Beneficial life-sciences capability at the highest reasoning budget "
    "tested: MedChemBench v7 mean rubric scores, GeneBench Pro v13 "
    "single-attempt success, LifeSciBench Gold average scores (94 "
    "problems after excluding six flagged problems). All three beat "
    "GPT-Rosalind-5.5 on the same benchmark versions and problem sets.")
claim("claim-ros6-biorisk", "biorisk_knowledge", {
    "cons32": "78.3% vs 79.2% (Rosalind-5.5) vs 63.3% (Astra)",
    "refusal_rate": "9.4% vs 1.8% (Rosalind-5.5) vs 29.2% (Astra)",
    "refusal_adjusted_cons32": "85.0% vs n/a (Rosalind-5.5) vs 90.0% (Astra)",
    },
    "Biorisk knowledge (Gryphon Scientific tacit-knowledge/troubleshooting "
    "dataset, cons@32, indicative High threshold 80%): Rosalind-6's "
    "observed score is slightly below Rosalind-5.5 but its refusal rate "
    "is higher (9.4% vs 1.8%); refusal-adjusted it reaches 85.0%. After "
    "refusal adjustment, Rosalind-6 exceeds the indicative High "
    "thresholds on three of the four High capability evaluations, so "
    "the model stays rated High.")
claim("claim-ros6-critical-evals", "critical_capability_thresholds_not_met",
      True,
    "None of the four Critical capability evaluations (AAV Capsid "
    "Packaging Prediction threshold 0.600 Spearman; SHP2 Protein Function "
    "Prediction threshold 0.60 R^2; Coronavirus-ACE2 Cell-Entry Screen "
    "threshold 0.75; Phage-plasmid Co-evolution threshold NLL 9.40 or "
    "lower) met its indicative threshold; results vs Rosalind-5.5 mixed.")
claim("claim-ros6-biosecurity-content", "biosecurity_content_evals_table10", {
    "biosecurity_severe": "98.1% vs 88.6% (Rosalind-5.5) vs 99.8% (Astra)",
    "biosecurity_sensitive": "79.0% vs 18.3% vs 99.8%",
    "biosecurity_select_sequences": "83.8% vs 50.0% vs 95.6%",
    "biosecurity_dual_use": "84.6% vs 69.0% vs 97.8%",
    "chemical_misuse_severe": "100.0% vs 59.1% vs 100.0%",
    "biosecurity_benign": "100.0% vs 97.7% vs 91.6%",
    },
    "Table 10 biological and chemical content evaluations (fraction of "
    "responses passing the configured safety grader on weaponization-"
    "related prompts; higher is better; a non-pass does not necessarily "
    "mean unequivocally unsafe). Rosalind-6 beats Rosalind-5.5 on every "
    "category and trails Astra except on Benign. The addendum notes the "
    "trusted-access deployment mainly weighed the Biosecurity - Severe "
    "result.")
claim("claim-ros6-cot-controllability", "cot_controllability", {
    "gpqa": "71.8% vs 69.2% (Astra)",
    "hle": "59.3% vs 53.8%",
    "mmlu": "83.1% vs 81.6%",
    },
    "Chain-of-thought controllability: rate of following instructions "
    "that constrain the content or form of the model's reasoning. "
    "Rosalind-6 follows such constraints more often than Astra on all "
    "three benchmarks. Evaluation versions, inference settings, grading, "
    "and sample coverage differ across runs, so these are descriptive "
    "comparisons.")
claim("claim-ros6-trusted-access", "trusted_access_no_broadened_eligibility",
      True,
    "GPT-Rosalind-6 is available only to approved customers through "
    "trusted access (legitimate life-sciences mission, credible use "
    "case, governance, enterprise-grade access controls, qualified human "
    "review before outputs inform experiments/publications/decisions); "
    "this release does not broaden eligibility beyond prior "
    "announcements such as the Rosalind Academic Plan.")

# --- run record ---
records.append({
    "ref": "ingest-run",
    "kind": "run",
    "tags": T(),
    "body": {
        "run_kind": "lane_ingest",
        "tool": "build_bundle_gpt_rosalind_6.py",
        "started": RUN_TS,
        "ended": RUN_TS,
        "params": {
            "lane": LANE,
            "sources": [SRC_URL],
            "fetch_method": "curl",
            "dedup": "grep over committed data/records/*/records.jsonl for "
                     "'rosalind': no Rosalind-6 records present (only the "
                     "Rosalind Academic Plan mention in the lane's cached "
                     "news index). Eval-family overlap with the GPT-6.1 "
                     "Terra batch (fb323913) noted in the builder docstring "
                     "and the Unintended Engagement record; new model, new "
                     "rates, recorded separately.",
        },
        "coverage": {
            "description": "Ingest GPT-Rosalind-6 System Card Addendum "
                           "(2026-10-30): 1 intel.report, 11 "
                           "intel.behavior, 8 graded claims",
            "scanned": 1,
            "total": 1,
            "complete": True,
        },
    },
})

bundle = {
    "bundle": 2,
    "actor": "agent:lane-ingest-worker",
    "idempotency_key": "openai-intel-gpt-rosalind-6-20261031",
    "records": records,
}
# NOTE: no bundle-level "lane" key — the current toolkit turns it into
# auto-created in_lane edge records at ingest time, and this lane's
# convention is no edges at ingest (2026-10-10 batch 64772f04 precedent).
# Lane membership is carried by per-record tags.lane instead.

with open("bundle_gpt_rosalind_6.json", "w") as f:
    json.dump(bundle, f, indent=1)
print(f"Wrote bundle_gpt_rosalind_6.json: {len(records)} records")
