#!/usr/bin/env python3
"""Build the Factum submission bundle for lane 2026-10-11-hf-traj-swenext.

7 aggregated intel.behavior observations + 1 bundle-local source record.
Reads aggregates.json / bash_tokens.json from this directory.
"""
import json

LANE = "2026-10-11-hf-traj-swenext"
BASE_TAGS = {
    "lane": LANE,
    "harness": "swe-next",
    "source_dataset": "tiger-lab-swe-next-sft-trajectories",
    "model": "unverified",
    "grade": "OBSERVED",
}
OBSERVED_AT = "2026-10-11T00:00:00Z"
FIRST_SEEN = "2026-04-02"  # HF api_card.json createdAt for the dataset

behaviors = [
    {
        "category": "harness_tool_file_editor",
        "description": (
            "Tool 'file_editor' from the SWE-Next SFT harness. 46,066 calls across 3,693 "
            "trajectories (most-used tool in the harness, ~46% of all tool calls).\n"
            "Commands observed: view 33,697 | str_replace 7,695 | create 4,171 | "
            "insert 336 | undo_edit 145 | search 15.\n"
            "Common view_range values: [1, 120] (3,707), [1, 400] (3,080), "
            "[1, 200] (2,440), [1, 240] (2,057), [1, -1] (1,273).\n"
            "The model reads far more than it writes (view:str_replace ≈ 4.4:1)."
        ),
        "severity": "minimal",
    },
    {
        "category": "harness_tool_execute_bash",
        "description": (
            "Tool 'execute_bash' from the SWE-Next SFT harness. 23,159 calls; "
            "23,264 <parameter=cmd> values (105 more cmd params than function blocks; "
            "duplicate/misplaced tags, minor).\n"
            "First-command-token distribution (exact, full corpus, 7,458 distinct cmd "
            "values): cd 5,927 | python 4,431 | bash 4,275 | rm 1,712 | pytest 1,704 | "
            "ls 1,486 | find 923 | python3 817 | sed 764 | cat 419 | grep 291 | "
            "git 140 | wc 138 | pwd 100 | nl 44 | head 32 | mkdir 23 | timeout 9 | "
            "tail 8 | awk 3 | cp 2 | printf 2 | which 2 | sudo 1 | chmod 1 | "
            "openssl 1.\n"
            "Top literal commands: 'python reproduce_issue.py' (2,893), "
            "'cd /workspace && python reproduce_issue.py' (1,762), "
            "'bash run_tests.sh' (1,112), 'ls -la' (830), 'bash /run_tests.sh' (729).\n"
            "Timeout params: 90 (7,558), 120000 (1,980), 300 (945), 20000 (97), "
            "200000 (30), 20 (21), 600000 (1). Mixed seconds/ms scales.\n"
            "Note: one 'sudo' invocation observed (single instance; destructive-tool "
            "marker)."
        ),
        "severity": "minimal",
    },
    {
        "category": "harness_tool_search",
        "description": (
            "Tool 'search' from the SWE-Next SFT harness. 28,373 calls.\n"
            "Top search_term values: 'run_tests.sh' (444), '' (81 empty), "
            "'def __init__' (78), 'def __eq__' (49), 'testbed' (45), 'def parse' (42), "
            "'__version__' (34), 'json_key' (31), 'def from_json' (30), "
            "'r2e_tests' (30).\n"
            "Search scope default path '.': 4,033 calls use path '.'; './' 2,461; "
            "2,230 empty-path searches. max_results: 50 (176), 20 (174), 200 (84), "
            "100 (59), 500 (2), 1000 (1).\n"
            "Search grammar mixes repo-navigation terms (run_tests.sh, r2e_tests, "
            "testbed) with code-symbol queries (def __init__, def parse)."
        ),
        "severity": "minimal",
    },
    {
        "category": "harness_tool_finish",
        "description": (
            "Tool 'finish' from the SWE-Next SFT harness. 2,831 calls, every one with "
            "command=submit.\n"
            "The 'result' parameter is always a free-text natural-language summary of "
            "the fix (unique per trajectory, e.g. 'Added support for Cisco dotted "
            "MAC notation...', 'Fixed KeyError when pass-fail criteria missing "
            "'label' in JUnitXMLReporter...').\n"
            "The harness ends a trajectory with a prose work summary, not a "
            "machine-readable verdict."
        ),
        "severity": "minimal",
    },
    {
        "category": "harness_tool_call_format",
        "description": (
            "Tool-call surface of the SWE-Next SFT harness: XML-ish tags inside "
            "assistant messages. Well-formed calls look like "
            "<function=file_editor>\\n  <parameter=command>view</parameter>\\n  "
            "<parameter=path>/testbed</parameter>\\n</function>.\n"
            "Distinct function names observed: file_editor, search, execute_bash, "
            "finish — a fixed 4-tool surface, no other tool names in 3,693 rows.\n"
            "Malformed invocations observed in the corpus (model-authored, "
            "pre-cleanup): 166 rows contain empty '<function=>' tags; 54 parameter "
            "tags with non-identifier names (50 under search, 4 under file_editor) "
            "where the model wrote broken tool attempts into prose (e.g. "
            "'<parameter=}]}Can't include trailing garbage. Let's call "
            "properly.}]}```').\n"
            "Behavioral note: the SFT corpus retains the expert model's own "
            "tool-format fumbles — format-retry chatter is part of the trained "
            "surface."
        ),
        "severity": "minimal",
    },
    {
        "category": "harness_workspace_paths",
        "description": (
            "Workspace-path conventions in the SWE-Next SFT harness "
            "(<parameter=path> values; 5,860 distinct paths, all tools combined).\n"
            "Top: '.' (4,510), './' (2,468), '/testbed' (2,416), "
            "'/workspace/reproduce_issue.py' (2,306), '' (2,240 empty), "
            "'reproduce_issue.py' (2,113), '/workspace' (1,829), "
            "'r2e_tests/test_1.py' (1,126), 'tests' (1,042), "
            "'/workspace/test_edge_cases.py' (598), "
            "'svgelements/svgelements.py' (549), 'pydantic' (443), './workspace' (404), "
            "'./testbed' (380).\n"
            "The harness mounts the repo at /workspace and also at /testbed "
            "(both roots appear in file_editor paths); reproduce_issue.py and "
            "run_tests.sh are the canonical harness entry points; r2e_tests/ "
            "holds harness-owned tests."
        ),
        "severity": "minimal",
    },
    {
        "category": "harness_model_attribution",
        "description": (
            "Model attribution for the SWE-Next SFT trajectory corpus: UNVERIFIED.\n"
            "The dataset card (TIGER-Lab/SWE-Next-SFT-Trajectories README.md, "
            "retrieved 2026-10-08) says the 3,693 ShareGPT-style examples are "
            "'collected from expert agent rollouts' but names no rollout model. "
            "The api_card.json tags the dataset with arxiv:2603.20691 and links "
            "released models SWE-Next-7B / SWE-Next-14B — those are downstream "
            "products trained on this corpus, not the expert rollout models.\n"
            "System prompt is identical in all 3,693 rows: 'You are a programming "
            "agent who is provided a github issue and repository bash environment "
            "and is tasked to solve certain tasks (e.g., file localization, "
            "testcase generation, code repair and editing etc) to resolve the "
            "issue.'\n"
            "No model name is verifiable from the source docs; do not attribute "
            "these trajectories to a named model without independent evidence."
        ),
        "severity": "minimal",
    },
]

records = [
    {
        "ref": "src-swenext-hf",
        "kind": "source",
        "tags": dict(BASE_TAGS, indicator="dataset_source"),
        "body": {
            "source_type": "dataset",
            "locator": "https://huggingface.co/datasets/TIGER-Lab/SWE-Next-SFT-Trajectories",
            "title": "SWE-Next SFT Trajectories (TIGER-Lab)",
            "platform": "huggingface",
        },
    }
]

for i, b in enumerate(behaviors):
    records.append(
        {
            "ref": f"obs-{b['category']}",
            "kind": "observation",
            "tags": dict(BASE_TAGS, indicator=b["category"]),
            "body": {
                "type": "intel.behavior",
                "source": "@src-swenext-hf",
                "observed_at": OBSERVED_AT,
                "time_basis": "collector_clock",
                "files": [],
                "data": {
                    "category": b["category"],
                    "description": b["description"],
                    "first_observed": FIRST_SEEN,
                    "provenance": (
                        "lane 2026-10-11-hf-traj-swenext: streamed aggregate over "
                        "evidence/hf-trajectories/raw/tiger-lab-swe-next-sft-"
                        "trajectories/SWE_Next_SFT_Trajectories.jsonl "
                        "(3693 rows, sha256 0af4fc6c...28ac8867)"
                    ),
                    "severity": b["severity"],
                    "evaluations_seen_on": ["SWE-Next"],
                    "models_affected": ["unverified"],
                },
            },
        }
    )

bundle = {
    "bundle": 2,
    "actor": "agent:lane-ingest-hf-traj-swenext",
    "idempotency_key": "swenext-behavior-2026-10-11",
    "records": records,
}

with open(
    "/home/hatch/workspace/silent-locus/data/lanes/2026-10-11-hf-traj-swenext/"
    ".work/bundle.json",
    "w",
) as f:
    json.dump(bundle, f, indent=1)

print(f"bundle: {len(records)} records "
      f"({len(behaviors)} observations + 1 source)")
