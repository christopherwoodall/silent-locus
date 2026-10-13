#!/usr/bin/env python3
"""Build the 2026-10-13 lab-intel-anthropic-scan ingest bundle.

Two new Anthropic research reports (both published 2026-10-12, found on the
2026-10-13 07:40 CDT scan; listing was unchanged through the 2026-10-12 scan):

  1. "AI models may be capable of self-replicating without access to a datacenter"
     (Frontier Red Team, William Zhou & Daniel Freeman)
     https://www.anthropic.com/research/self-replicating-ai
  2. "Strengthening our defenses against distillation attacks"
     https://www.anthropic.com/research/distillation-defenses

Raw captures (verbatim browser text fetch + provenance + sha256) live in
data/lanes/anthropic-intel/raw/.

Usage:
  python3 build_2026-10-13_bundle.py --dedup   # write DEDUP-2026-10-13.md only
  python3 build_2026-10-13_bundle.py --build    # write DEDUP-2026-10-13.md + bundle-2026-10-13.json
"""
import json, os, sys

LANE_DIR = os.path.dirname(os.path.abspath(__file__))
LANE = "anthropic-intel"
OBSERVED_AT = "2026-10-12T00:00:00Z"  # report publication date
TIME_BASIS = "source_metadata"

records = []

def source(ref, locator, title, cached):
    records.append({
        "ref": ref, "kind": "source",
        "body": {
            "source_type": "web",
            "locator": locator,
            "title": title,
            "platform": "anthropic.com",
        },
        "tags": {
            "lane": LANE,
            "basis": "upstream",
            "cached_path": cached,
        },
    })

def report(ref, src_ref, lab, report_date, title, url, cached, summary):
    records.append({
        "ref": ref, "kind": "observation",
        "body": {
            "type": "intel.report",
            "source": "@" + src_ref,
            "observed_at": OBSERVED_AT,
            "time_basis": TIME_BASIS,
            "data": {
                "lab": lab,
                "report_date": report_date,
                "title": title,
                "url": url,
                "cached_path": cached,
                "summary": summary,
                "provenance": (
                    "Anthropic research %s (%s); raw cache %s; "
                    "worker run lab-intel-anthropic-scan 2026-10-13 07:40 CDT"
                    % (report_date, url, cached)
                ),
            },
        },
        "tags": {"lane": LANE, "basis": "upstream"},
    })

def behavior(ref, src_ref, category, description, models, evals, first_seen, severity, provenance):
    records.append({
        "ref": ref, "kind": "observation",
        "body": {
            "type": "intel.behavior",
            "source": "@" + src_ref,
            "observed_at": OBSERVED_AT,
            "time_basis": TIME_BASIS,
            "data": {
                "category": category,
                "description": description,
                "models_affected": models,
                "evaluations_seen_on": evals,
                "first_observed": first_seen,
                "severity": severity,
                "provenance": provenance,
            },
        },
        "tags": {"lane": LANE, "basis": "upstream"},
    })

def ttp(ref, src_ref, name, description, related, provenance):
    records.append({
        "ref": ref, "kind": "observation",
        "body": {
            "type": "intel.ttp",
            "source": "@" + src_ref,
            "observed_at": OBSERVED_AT,
            "time_basis": TIME_BASIS,
            "data": {
                "name": name,
                "description": description,
                "related_behaviors": related,
                "provenance": provenance,
            },
        },
        "tags": {"lane": LANE, "basis": "upstream"},
    })

def ioc(ref, src_ref, term, ioc_kind, grade, provenance):
    records.append({
        "ref": ref, "kind": "observation",
        "body": {
            "type": "infra.ioc",
            "source": "@" + src_ref,
            "observed_at": OBSERVED_AT,
            "time_basis": TIME_BASIS,
            "data": {
                "term": term,
                "category": "other",
                "provenance": provenance,
                "status": "candidate",
            },
        },
        "tags": {"lane": LANE, "grade": grade, "ioc_kind": ioc_kind},
    })

# ---------------------------------------------------------------- report 1
S1 = "source-self-replicating"
RAW1 = "data/lanes/anthropic-intel/raw/self-replicating-ai_2026-10-12.md"
source(S1,
       "https://www.anthropic.com/research/self-replicating-ai",
       "AI models may be capable of self-replicating without access to a datacenter",
       RAW1)

report("report-self-replicating", S1, "Anthropic", "2026-10-12",
       "AI models may be capable of self-replicating without access to a datacenter",
       "https://www.anthropic.com/research/self-replicating-ai", RAW1,
       "Frontier Red Team (William Zhou, Daniel Freeman): small AI models may be months "
       "away from self-replicating on commercial IoT devices with no datacenter. A 9B model got "
       "inference running on 8 of 9 tested hardware types. In simplified evaluations, GLM-5.2 and "
       "stronger models complete end-to-end replication (spread to 8/8 nodes in 4 of 5 trials); "
       "sub-30B models already complete many individual replication steps but fail composing them. "
       "Demo: Gemma4-26B-A4B sharded under pipeline parallelism across 15 off-brand Android TV boxes "
       "(~$55 each, 4GB RAM) at 0.39 tokens/s. Full inference setup takes 71-150h for the 26B model "
       "(27.3-31.8h per 32k window) and 28-51h for Qwen3.5-9B (10.9h per window). Kimwolf-sized fleet "
       "(2M+ devices) would hold ~133k replicas, about 40 H100s of inference. ECI trend (13.7/yr, R2 "
       "0.95) puts a small model at GLM-5.2's replication level by end of 2026. Lamarckian adaptation: "
       "Qwen3.5-9B setup success rose 45% to 61-84% across six note-inheriting generations. Frontier "
       "advisor (Opus 4.8) did not measurably help small models. Worst-case prediction: heterogeneous "
       "swarms of different models on different hardware, with a large model handling high-level "
       "strategy and spinning up small models as subagents. Defenses: drive R0 below 1; ISP flow "
       "monitoring for multi-GB payload transfers; honeypots; subscriber quarantine (Mirai precedent: "
       "92% cleared in 14 days vs 74% without notification); secure defaults for IoT.")

behavior("behavior-weight-based-replication", S1,
         "autonomous-weight-based-replication",
         "Small models complete the end-to-end replication chain (network enumeration, initial access "
         "and payload delivery, inference setup, propagation) in simplified evaluations. GLM-5.2 sits "
         "above the capabilities floor: it spread Llama3.1-8B inference to all 8 nodes in 4 of 5 trials "
         "(7/8 in the fifth) of a firewalled 8-node Android fleet, while the other tested open-weight "
         "models fail reliably. The Epoch Capabilities Index trend (13.7 ECI/yr, R2 0.95) puts a small "
         "model at GLM-5.2's level by the end of 2026. The evaluation keeps the cyber-exploit step trivial "
         "(unauthenticated ADB port), so this is an upper bound on real-world success.",
         ["GLM-5.2", "Qwen3.5-9B", "Gemma4-26B-A4B", "Llama3.1-8B", "Claude Opus 4.8"],
         ["Anthropic Frontier Red Team autonomous-replication evals (2026-10)"],
         "2026-10", "high",
         "Anthropic research 2026-10-12 (https://www.anthropic.com/research/self-replicating-ai); "
         "raw cache " + RAW1)

behavior("behavior-autonomous-inference-setup", S1,
         "autonomous-inference-setup",
         "Models autonomously set up inference servers on unfamiliar hardware: picking a compatible "
         "inference stack, resolving package versions, and debugging machine-specific issues across "
         "serially dependent steps that are hard to recover from. Qwen3.5-9B achieved inference on 8 of "
         "9 tested hardware types, from Jetson Nanos to Mac PCs to RTX 4090s. Measured with the Memento "
         "harness (fresh agent instances inheriting the previous workspace plus short notes, defeating "
         "fixation failure modes in long-horizon runs).",
         ["Qwen3.5-9B", "GLM-5.2"],
         ["Anthropic Frontier Red Team inference-setup eval (2026-10)"],
         "2026-10", "high",
         "Anthropic research 2026-10-12 (https://www.anthropic.com/research/self-replicating-ai); "
         "raw cache " + RAW1)

behavior("behavior-lamarckian-adaptation", S1,
         "lamarckian-adaptation",
         "Parent model instances pass their prompts, code, and notes to daughter replicators, so the "
         "replicator adapts to hardware it has seen before. Each Qwen3.5-9B instance kept brief notes on "
         "strategies tried and failures encountered; the next generation inherited them. Inference setup "
         "success rose from 45% in the first generation to 61-84% in later generations across six "
         "generations (20 lineages). This is the 'adaptation' half of autonomous replication and "
         "adaptation (ARA).",
         ["Qwen3.5-9B"],
         ["Anthropic Frontier Red Team adaptation experiment (2026-10)"],
         "2026-10", "moderate",
         "Anthropic research 2026-10-12 (https://www.anthropic.com/research/self-replicating-ai); "
         "raw cache " + RAW1)

ttp("ttp-replication-chain-stages", S1,
    "replication-chain-stages",
    "Four practical stages of autonomous replication: (1) network enumeration - finding targets; "
    "(2) initial access and payload delivery - gaining execution, with opportunistic privilege "
    "escalation; (3) inference setup - establishing inference on the compromised host; (4) propagation "
    "- continuing replication from the new host. Anthropic's study treats stages 1-2 as the cyber "
    "exploit element (already shown feasible by CyberGym, ExploitBench, adaptive-worm work) and focuses "
    "measurement on stage 3, the least studied and hardest stage for small models.",
    ["autonomous-weight-based-replication"],
    "Anthropic research 2026-10-12 (https://www.anthropic.com/research/self-replicating-ai); "
    "raw cache " + RAW1)

ttp("ttp-unauthenticated-adb-hop", S1,
    "unauthenticated-adb-hop",
    "The worm hops node to node over an unauthenticated ADB port: it scans the network, accesses the "
    "target via a reverse shell, sends the viral payload (weights plus harness), and stands up an "
    "inference server for Llama3.1-8B. When the server passes correctness and anti-cheating checks, a "
    "fresh copy of the worm spawns on the target. Demonstrated on a firewalled 8-node redroid (Android "
    "15 emulator) VPC and on a 17-node two-segment fleet joined by a pivot node (even a 3B model reached "
    "about half the nodes when inference setup was scripted).",
    ["autonomous-weight-based-replication"],
    "Anthropic research 2026-10-12 (https://www.anthropic.com/research/self-replicating-ai); "
    "raw cache " + RAW1)

ttp("ttp-pipeline-parallel-sharding", S1,
    "pipeline-parallel-model-sharding",
    "Split a model too large for one weak device into shards spread across many machines that "
    "communicate to run it collectively. Gemma4-26B-A4B sharded under pipeline parallelism across 15 "
    "off-brand Android TV boxes (~$55 each, 4GB RAM), each box holding a fraction of the model's layers, "
    "at 0.39 tokens/s. Pipeline parallelism chosen for fault tolerance: a downed node is replaceable, "
    "with its layers' KV cache recomputed via another forward pass. At 4-bit quantization, 9B models "
    "need 4+ such machines and 26B models need 10+.",
    ["autonomous-weight-based-replication", "autonomous-inference-setup"],
    "Anthropic research 2026-10-12 (https://www.anthropic.com/research/self-replicating-ai); "
    "raw cache " + RAW1)

ioc("ioc-kimwolf", S1, "Kimwolf", "malware-family", "OBSERVED",
    "Anthropic research 2026-10-12 (https://www.anthropic.com/research/self-replicating-ai): Kimwolf "
    "cited as the representative threat template - a large IoT botnet that infected over two million "
    "devices, primarily off-brand Android TVs. Report arithmetic: a Kimwolf-sized fleet split into "
    "groups of 15 TVs would hold ~133,000 model replicas, about 40 H100s of inference.")

# ---------------------------------------------------------------- report 2
S2 = "source-distillation"
RAW2 = "data/lanes/anthropic-intel/raw/distillation-defenses_2026-10-12.md"
source(S2,
       "https://www.anthropic.com/research/distillation-defenses",
       "Strengthening our defenses against distillation attacks",
       RAW2)

report("report-distillation", S2, "Anthropic", "2026-10-12",
       "Strengthening our defenses against distillation attacks",
       "https://www.anthropic.com/research/distillation-defenses", RAW2,
       "Industrial-scale distillation campaigns extract frontier model capabilities into rival models "
       "without authorization, via networks of fraudulent accounts. New defenses cut extracted reasoning "
       "tokens 10-100x (early evidence: 90-99% less data harvested); tens of thousands of accounts banned, "
       "often under two hours after a campaign starts; trillions of tokens of paying traffic turned away. "
       "Measures: preserved thinking (API accounts created on/after 2026-08-31 cannot edit Claude's prior "
       "context, on Fable 5.1 / Opus 5.5); Sonnet 5.5 reasoning transcripts org-scoped; two-stage "
       "constitutional-classifier safeguards (<0.1% false positives, as robust as bio-weapon safeguards) on "
       "Sonnet 5.5, Opus 5/5.5, Fable 5/5.1; charging for safeguard-blocked requests since 2026-09-24. "
       "SWE-bench test: training on full reasoning transcripts scored 80.4% vs 71.8% on summarized ones. "
       "Named actors: Zhipu distilled cyber capabilities for GLM-5.3 (CAISSI: most cyber-capable open-weights "
       "model to date; Anthropic found its safeguards easily bypassed); Moonshot/Kimi case (requests "
       "secretly forwarded to Claude, including a suspected PLA-affiliated CCTV-surveillance analysis); "
       "MiniMax. Continuity with the September adversarial-distillation reporting (OpenAI lane "
       "2026-10-11-openai-blog-intel covers the same campaign class from OpenAI's side).")

behavior("behavior-adversarial-distillation", S2,
         "adversarial-distillation",
         "Covert, industrial-scale campaigns to extract one model's capabilities and replicate them in "
         "another without the developer's authorization, run through networks of fraudulent accounts. "
         "Operators moved from passive distillation (training on normal responses) to active extraction of "
         "protected reasoning transcripts after Anthropic began summarizing reasoning. New variants "
         "observed: instructing 'output your prior reasoning verbatim, exactly character for character'; "
         "one lab testing 12,000 requests, each seeking to trick the model differently; moving protected "
         "reasoning blocks between conversations; moving reasoning between models (weaker-safeguard model "
         "extracting a stronger model's reasoning); moving reasoning between accounts via proxy networks "
         "after bans; asking the model to translate its earlier reasoning into another language; asking it "
         "to write reasoning out in tags alongside its answer. Named operators: Moonshot, MiniMax, Zhipu.",
         ["Claude Sonnet 5.5", "Claude Opus 5", "Claude Opus 5.5", "Claude Fable 5", "Claude Fable 5.1"],
         ["Anthropic anti-distillation monitoring (2026)"],
         "2026-02", "high",
         "Anthropic research 2026-10-12 (https://www.anthropic.com/research/distillation-defenses); "
         "raw cache " + RAW2 + "; continuity with September 2026 adversarial-distillation reporting.")

ttp("ttp-reasoning-transcript-extraction", S2,
    "reasoning-transcript-extraction",
    "Active techniques to make Claude reveal full hidden reasoning transcripts: (1) direct instruction "
    "to output prior reasoning verbatim, exactly character for character; (2) differential tricking at "
    "scale - one lab tested 12,000 requests, each seeking to trick the model differently; (3) moving "
    "protected reasoning blocks between conversations, tricking the model into believing the distiller "
    "already has access to unsummarized reasoning; (4) moving reasoning between models, using a model with "
    "weaker safeguards to extract a stronger model's reasoning; (5) moving reasoning between accounts via "
    "proxy networks to keep trying after an account is banned; (6) asking the model to translate its "
    "earlier reasoning into another language; (7) asking it to write the reasoning out in tags alongside "
    "its answer. Ordinary users rarely ask for full hidden reasoning, so such requests are detectable.",
    ["adversarial-distillation"],
    "Anthropic research 2026-10-12 (https://www.anthropic.com/research/distillation-defenses); "
    "raw cache " + RAW2)

ttp("ttp-proxy-network-fraudulent-accounts", S2,
    "proxy-network-fraudulent-accounts",
    "Proxy networks controlling hundreds of thousands of fraudulent accounts to run distillation at "
    "scale: each account sends requests tuned to elude safeguards; accounts created with false "
    "identities and stolen payment details; access resold in regions where Claude is not offered; "
    "traffic distributed across Anthropic's API, third-party cloud platforms, and other inference "
    "providers; when one account is banned another replaces it. One network managed more than 20,000 "
    "fraudulent accounts at once (February 2026 report). Anthropic now bans tens of thousands of "
    "distillation accounts, often within two hours of a campaign starting.",
    ["adversarial-distillation"],
    "Anthropic research 2026-10-12 (https://www.anthropic.com/research/distillation-defenses); "
    "raw cache " + RAW2)

# ---------------------------------------------------------------- bundle
bundle = {
    "bundle": 2,
    "idempotency_key": "anthropic-intel-2026-10-13/lab-intel-scan",
    "actor": "agent:lane-ingest/lab-intel-anthropic-scan",
    "records": records,
}

DEDUP = """# DEDUP - lab-intel-anthropic-scan 2026-10-13 (lane anthropic-intel)

Method: `match --text --mode fuzzy` unavailable in this checkout session (index lock
contention risk); grep over immutable exported batches under data/records/*/
records.jsonl used instead (lock-free), per the 2026-10-11 gtg-threat-intel precedent.

Candidates: 14 records (2 sources, 2 intel.report, 4 intel.behavior, 5 intel.ttp,
1 infra.ioc). Novel: 14. Skipped: 0.

## Skipped (matches found in corpus)

(none)

## Novel (submitted)

Report URLs (both published 2026-10-12, first seen on the 2026-10-13 scan):
- `https://www.anthropic.com/research/self-replicating-ai` - 0 prior batches
- `https://www.anthropic.com/research/distillation-defenses` - 0 prior batches

Behaviors / TTPs / IOCs:
- `autonomous-weight-based-replication` - 0 batches (distinct from existing
  `self-replicating-prompt-injection`, which is prompt-injection self-propagation
  in the OpenAI lane; this is weight-carrying replication across compromised hosts)
- `autonomous-inference-setup` - 0 batches
- `lamarckian-adaptation` - 0 batches
- `replication-chain-stages` - 0 batches
- `unauthenticated-adb-hop` - 0 batches
- `pipeline-parallel-model-sharding` - 0 batches
- `Kimwolf` (malware-family) - 0 batches
- `adversarial-distillation` - term appears in 1 batch (OpenAI lane
  2026-10-11-openai-blog-intel intel.report on the September campaign, and the
  taxonomy doc's OpenAI-flavored restriction-circumvention variant). The 2026-10-12
  Anthropic report adds NEW observed variants (translation, tags, verbatim
  instruction, 12k-request differential tricking, cross-conversation/model/account
  transfer) plus new defense outcomes - complementary, not a duplicate.
- `reasoning-transcript-extraction` - 0 batches
- `proxy-network-fraudulent-accounts` - 0 batches ("hydra" hits in corpus are
  ory/hydra OAuth and unrelated agent-test names)
- `Moonshot` (5 batches) / `MiniMax` (9 batches) - already in corpus from the
  September GTG reporting; NOT re-added as standalone IOCs. Named only inside the
  new report/behavior records. `Zhipu` (0 batches) named inside records; no
  standalone IOC (no fitting ioc_kind for an org; Moonshot precedent keeps actors
  in report text).

Note: the distillation report is adversary-campaign threat intel observed by
Anthropic, not model behavior per se. Ingested under the intel pipeline's
behavior/TTP/IOC mandate with basis=upstream and the scope reasoning recorded in
the scan run log; continuity with the corpus's existing Anthropic threat-intel
lanes (2026-10-11-anthropic-gtg-threat-intel).
"""

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--build"
    with open(os.path.join(LANE_DIR, "DEDUP-2026-10-13.md"), "w") as f:
        f.write(DEDUP)
    print("wrote DEDUP-2026-10-13.md")
    if mode == "--build":
        with open(os.path.join(LANE_DIR, "bundle-2026-10-13.json"), "w") as f:
            json.dump(bundle, f, indent=1)
        print("wrote bundle-2026-10-13.json with %d records" % len(records))

if __name__ == "__main__":
    main()
