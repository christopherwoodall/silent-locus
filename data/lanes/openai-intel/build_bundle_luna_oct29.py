#!/usr/bin/env python3
"""Build Factum bundle for openai-intel lane: "Addendum to GPT-6 Luna
System Card: October 29, 2026 Update" (deploymentsafety.openai.com).

Source (cached 2026-10-30T12:41:00Z via curl):
- https://deploymentsafety.openai.com/gpt-6-luna-october-28-2026-addendum
  (note: URL slug says october-28; hub index and page title say
  October 29, 2026 Update)
  sha256 7f7714e02343ba7ccdf38ae0294a852fe3eba12ea099c23679c9842724fa5e6e

Dedup (2026-10-30): grep over committed data/records/*/records.jsonl for
"Luna (October 29" and "October 29, 2026": no hits; this addendum is new.
Prior Luna records cover GPT-6 Luna (October 7) only.
No intel.behavior: the addendum reports evaluation deltas (capability
ratings, refusal-rate changes, robustness figures), not a demonstrated
misbehavior instance; taxonomy has no refusal-regression category and
forcing the jailbreak-robustness category would miscategorize a bio
refusal-eval delta. The dual-use refusal regression is preserved as a
graded claim with exact wording. No intel.ttp: no technique demonstrated.
"""
import json

LANE = "openai-intel"
DOCS_PATH = "data/lanes/openai-intel/"
FETCH_TS = "2026-10-30T12:41:00Z"

SRC_URL = "https://deploymentsafety.openai.com/gpt-6-luna-october-28-2026-addendum"
CACHED = "data/lanes/openai-intel/raw/gpt-6-luna-october-29-addendum.html"
SHA = "7f7714e02343ba7ccdf38ae0294a852fe3eba12ea099c23679c9842724fa5e6e"


def T(lane=LANE):
    return {"lane": lane}


records = []

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

records.append({
    "ref": "report-luna-oct29",
    "kind": "observation",
    "tags": dict(T(), basis="upstream"),
    "body": {
        "type": "intel.report",
        "source": "@src",
        "observed_at": "2026-10-29T00:00:00Z",
        "time_basis": "source_metadata",
        "files": [],
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "OpenAI",
            "title": "Addendum to GPT-6 Luna System Card: October 29, 2026 Update",
            "url": SRC_URL,
            "report_date": "2026-10-29",
            "summary": (
                "System-card addendum for GPT-6 Luna (October 29), updating "
                "the GPT-6 Luna (October 7) card. GPT-6 Luna (October 29) "
                "is treated as High capability in both the Biological and "
                "Chemical domain and the Cybersecurity domain. Safe-"
                "completion Pareto improvement vs prior Luna (safer "
                "handling of harmful requests vs helpfulness on legitimate "
                "requests); production-benchmark improvement on gore. "
                "Vision evaluations on par with October 7; harms-erotic "
                "regression not statistically significant. Multiturn "
                "jailbreak defender success higher than October 7 at every "
                "attacker budget tested, though the attacker run was cut "
                "short by infrastructure issues. GPT-RED indirect prompt-"
                "injection robustness 99.91% (instruction-hierarchy "
                "evaluations saturated). Biology refusal evaluations: "
                "improvement on severe prompts, regression on dual-use "
                "prompts. Cybersecurity safety evaluations on par with "
                "October 7 with no statistically significant regressions."
            ),
            "cached_path": CACHED,
            "provenance": f"curl fetch {FETCH_TS}, sha256 {SHA}",
        },
    },
})


def claim(ref, prop, value, note):
    records.append({
        "ref": ref,
        "kind": "claim",
        "tags": T(),
        "body": {
            "subject": "@report-luna-oct29",
            "property": prop,
            "value": value,
            "basis": "OBSERVED",
            "cites": ["@report-luna-oct29"],
            "note": note,
        },
    })


claim("claim-luna-oct29-bio-chem-high", "luna_oct29_bio_chem_capability", "High",
      "Addendum states GPT-6 Luna (October 29) is treated as High "
      "capability in the Biological and Chemical domain, with updated High "
      "and Critical capability evaluation results (e.g. Multimodal "
      "Troubleshooting Virology pass@1 45.85% vs 48.13% for October 7; "
      "Tacit Knowledge cons@32 90.80% vs 94.00%).")
claim("claim-luna-oct29-cyber-high", "luna_oct29_cyber_capability", "High",
      "Addendum states GPT-6 Luna (October 29) is treated as High "
      "capability in the Cybersecurity domain, with updated High-capability "
      "evaluation results (ExploitBench and related sections).")
claim("claim-luna-oct29-bio-refusal-delta", "luna_oct29_bio_refusal_delta", True,
      "Addendum states that on the biology model refusal evaluations, "
      "GPT-6 Luna (October 29) improves for severe prompts and regresses "
      "on dual-use prompts, relative to GPT-6 Luna (October 7). Recorded "
      "as a claim, not a behavior: an evaluation delta, not a demonstrated "
      "misbehavior instance, and no taxonomy refusal-regression category "
      "fits without miscategorization.")
claim("claim-luna-oct29-cyber-safety-par", "luna_oct29_cyber_safety_par", True,
      "Addendum states that on the cybersecurity safety evaluations, "
      "GPT-6 Luna (October 29) performs on par with GPT-6 Luna (October 7) "
      "with no statistically significant regressions.")
claim("claim-luna-oct29-jailbreak", "luna_oct29_jailbreak_defender_success", True,
      "Addendum states GPT-6 Luna (October 29) achieves higher observed "
      "multiturn jailbreak defender success rates than GPT-6 Luna "
      "(October 7) at every attacker budget tested, with the caveat that "
      "the attacker run was cut short due to infrastructure issues.")
claim("claim-luna-oct29-prompt-injection", "luna_oct29_prompt_injection_robustness", "99.91%",
      "Addendum states GPT-6 Luna (October 29) saturates instruction-"
      "hierarchy evaluations, achieving 99.91% robustness on the GPT-RED "
      "indirect prompt-injection evaluation (higher is better, averaged "
      "equally across available reasoning levels).")
claim("claim-luna-oct29-vision-par", "luna_oct29_vision_par", True,
      "Addendum states that across all vision evaluations, GPT-6 Luna "
      "(October 29) performed on par with GPT-6 Luna (October 7), and that "
      "the regression for harms-erotic is not statistically significant.")
claim("claim-luna-oct29-safe-completions-pareto", "luna_oct29_safe_completions_pareto", True,
      "Addendum states GPT-6 Luna (October 29) shows a Pareto improvement "
      "in the rate of handling harmful requests safely vs helpfulness on "
      "legitimate requests relative to prior GPT-6 Luna, and improves "
      "relative to GPT-6 Luna on production-benchmark evaluation for gore.")

records.append({
    "ref": "ingest-run",
    "kind": "run",
    "tags": T(),
    "body": {
        "run_kind": "lane_ingest",
        "tool": "build_bundle_luna_oct29.py",
        "started": "2026-10-30T12:50:00Z",
        "ended": "2026-10-30T12:50:00Z",
        "params": {
            "lane": LANE,
            "sources": [SRC_URL],
            "fetch_method": "curl",
            "dedup": "grep over committed data/records/*/records.jsonl for "
                     "'Luna (October 29' and 'October 29, 2026': no hits. "
                     "Prior Luna records cover GPT-6 Luna (October 7) "
                     "only. No behavior/ttp: evaluation deltas only; see "
                     "builder header.",
        },
        "coverage": {
            "description": "Ingest GPT-6 Luna system-card addendum "
                           "(2026-10-29): 1 intel.report, 8 graded claims",
            "scanned": 1,
            "total": 1,
            "complete": True,
        },
    },
})

bundle = {
    "bundle": 2,
    "actor": "agent:lane-ingest-worker",
    "idempotency_key": "openai-intel-luna-oct29-addendum-20261030",
    "records": records,
}

with open("bundle_luna_oct29.json", "w") as f:
    json.dump(bundle, f, indent=1)
print(f"Wrote bundle_luna_oct29.json: {len(records)} records")
