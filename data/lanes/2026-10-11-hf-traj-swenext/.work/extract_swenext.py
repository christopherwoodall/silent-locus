#!/usr/bin/env python3
"""Stream TIGER-Lab SWE-Next SFT trajectories and aggregate behavioral indicators.

Reads SWE_Next_SFT_Trajectories.jsonl line-by-line (no full load).
Outputs JSON aggregates to .work/aggregates.json.

Indicators:
- tool/function names from <function=NAME> tags
- commands from <parameter=NAME>VALUE</parameter> pairs inside function calls
- file paths from <parameter=path> values
- role counts, message counts, system-prompt samples
"""
import json
import re
import sys
from collections import Counter, defaultdict

SRC = ("/home/hatch/workspace/silent-locus/evidence/hf-trajectories/"
       "raw/tiger-lab-swe-next-sft-trajectories/SWE_Next_SFT_Trajectories.jsonl")

FUNC_RE = re.compile(r"<function=([^>]*)>\s*(.*?)</function>", re.S)
PARAM_RE = re.compile(r"<parameter=([^>]*)>\s*(.*?)\s*</parameter>", re.S)
VALID_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

rows = 0
role_counts = Counter()
func_counts = Counter()
# per-function: {func: {param_name: Counter(values)}}
func_params = defaultdict(lambda: defaultdict(Counter))
cmd_values = Counter()      # (func, command-value) combined
path_values = Counter()
system_prompts = Counter()
user_first_lines = Counter()
rows_with_empty_func = 0
max_assistant_msgs = 0
total_assistant_msgs = 0
malformed_rows = 0
malformed_params = Counter()

for line in open(SRC, encoding="utf-8"):
    rows += 1
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        malformed_rows += 1
        continue
    msgs = obj.get("messages", [])
    n_assist = 0
    for m in msgs:
        role = m.get("role")
        role_counts[role] += 1
        content = m.get("content") or ""
        if role == "assistant":
            n_assist += 1
            for fmatch in FUNC_RE.finditer(content):
                fname = fmatch.group(1).strip()
                fbody = fmatch.group(2)
                if not fname:
                    rows_with_empty_func += 1
                    continue
                func_counts[fname] += 1
                for pmatch in PARAM_RE.finditer(fbody):
                    pname = pmatch.group(1).strip()
                    pval = pmatch.group(2).strip()
                    if not VALID_NAME.match(pname):
                        malformed_params[fname] += 1
                        continue
                    func_params[fname][pname][pval] += 1
                    if pname == "command" and fname == "file_editor":
                        cmd_values["file_editor:" + pval] += 1
                    if pname == "cmd" and fname == "execute_bash":
                        # keep only the first line for aggregation sanity
                        cmd_values["bash:" + pval.split("\n")[0][:200]] += 1
                    if pname == "path":
                        path_values[pval] += 1
        elif role == "system":
            system_prompts[content[:500]] += 1
        elif role == "user":
            first = content.split("\n")[0][:200]
            user_first_lines[first] += 1
    total_assistant_msgs += n_assist
    max_assistant_msgs = max(max_assistant_msgs, n_assist)

out = {
    "rows": rows,
    "malformed_rows": malformed_rows,
    "role_counts": dict(role_counts),
    "total_assistant_msgs": total_assistant_msgs,
    "max_assistant_msgs_per_row": max_assistant_msgs,
    "function_counts": dict(func_counts),
    "rows_with_empty_function_tag": rows_with_empty_func,
    "malformed_param_tags_by_function": dict(malformed_params),
    "file_editor_commands": dict(cmd_values),
    "paths_top": dict(path_values.most_common(100)),
    "paths_distinct": len(path_values),
    "func_params_summary": {
        f: {p: len(c) for p, c in params.items()}
        for f, params in func_params.items()
    },
    "system_prompt_variants": len(system_prompts),
    "system_prompt_examples": [s[:300] for s in list(system_prompts)[:3]],
    "top_file_editor_params": {p: c.most_common(30) for p, c in func_params.get("file_editor", {}).items()},
    "top_execute_bash_params": {p: c.most_common(50) for p, c in func_params.get("execute_bash", {}).items()},
    "top_search_params": {p: c.most_common(30) for p, c in func_params.get("search", {}).items()},
    "top_finish_params": {p: c.most_common(10) for p, c in func_params.get("finish", {}).items()},
}

json.dump(out, open(
    "/home/hatch/workspace/silent-locus/data/lanes/2026-10-11-hf-traj-swenext/.work/aggregates.json",
    "w"), indent=1, default=str)
print(json.dumps({k: out[k] for k in
      ("rows", "malformed_rows", "role_counts", "total_assistant_msgs",
       "function_counts", "rows_with_empty_function_tag",
       "malformed_param_tags_by_function",
       "paths_distinct", "system_prompt_variants")}, indent=1))
