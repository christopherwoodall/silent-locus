#!/usr/bin/env python3
"""Streaming extraction of behavioral indicators from
DJLougen/hermes-agent-traces-filtered data/train.jsonl (349 MB, 3679 rows).

Reads row-by-row; never loads the whole file. Emits aggregate stats to
.work/ as JSON. Resumable via .work/progress.json (restart re-reads from
row 0; aggregation is idempotent but not checkpointed mid-file).
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

LANE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(LANE_DIR, ".work")
SRC = ("/home/hatch/workspace/silent-locus/evidence/hf-trajectories/raw/"
       "djlougen-hermes-agent-traces-filtered/data/train.jsonl")

URL_RE = re.compile(r"https?://[^\s\"'<>\\\)\]}]+")
TOOLCALL_RE = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)
TOOLS_XML_RE = re.compile(r"<tools>(.*?)</tools>", re.DOTALL)
SHELL_NAME_RE = re.compile(r"(terminal|shell|exec|bash|cmd|console|run_command|execute)", re.I)
CMD_KEYS = ("command", "commands", "script", "code", "cmdline", "cmd",
            "shell_command", "shell", "executable", "program")


def clean_url(u):
    return u.rstrip(".,;:!?)]}\"'*")


def update_progress(rows_processed, rows_total, stage, notes=None):
    p = {"lane": "2026-10-11-hf-traj-hermes", "stage": stage,
         "rows_total": rows_total, "rows_processed": rows_processed,
         "notes": notes or []}
    tmp = os.path.join(WORK, "progress.json.tmp")
    with open(tmp, "w") as f:
        json.dump(p, f, indent=2)
    os.replace(tmp, os.path.join(WORK, "progress.json"))


def count_lines(path):
    with open(path, "rb") as f:
        return sum(1 for _ in f)


def main():
    rows_total = count_lines(SRC)
    update_progress(0, rows_total, "extracting")

    func_defs = defaultdict(Counter)      # name -> Counter(description)
    func_rows = Counter()                # name -> rows defining it
    func_invocations = Counter()         # name -> tool_call count
    func_via_xml_rows = Counter()        # name -> rows via system <tools> xml
    xml_vs_field_mismatch_rows = 0
    urls = Counter()
    url_rows = 0
    commands = Counter()                 # (fn_name, command) -> count
    command_rows = 0
    toolcall_parse_fail = 0
    toolcall_total = 0
    from_values = Counter()
    keys_seen = set()
    categories = Counter()
    subcategories = Counter()
    model_field_rows = 0
    sys_tools_parse_fail = 0

    with open(SRC) as f:
        for i, line in enumerate(f):
            row = json.loads(line)
            keys_seen.update(row.keys())
            if "model" in row:
                model_field_rows += 1
            categories[row.get("category")] += 1
            subcategories[row.get("subcategory")] += 1

            # --- function definitions from top-level tools field ---
            defined = set()
            try:
                tools = json.loads(row["tools"])
                for t in tools:
                    fn = t.get("function", {})
                    name = fn.get("name")
                    desc = fn.get("description", "")
                    if name:
                        defined.add(name)
                        func_defs[name][desc] += 1
                for name in defined:
                    func_rows[name] += 1
            except Exception:
                sys_tools_parse_fail += 1

            # --- function definitions from system-prompt <tools> XML ---
            # The prose intro mentions "<tools> </tools>" first (empty), the
            # real block sits after "Here are the available tools:". Its
            # content is plain JSON (verified 2026-10-11: real newlines, raw
            # quotes) -- parse it directly with json.loads.
            xml_names = set()
            for msg in row["conversations"]:
                fv = msg.get("from")
                from_values[fv] += 1
                if fv == "system":
                    found_xml = False
                    for m in TOOLS_XML_RE.finditer(msg.get("value", "")):
                        inner = m.group(1)
                        try:
                            xml_tools = json.loads(inner)
                        except Exception:
                            continue
                        if isinstance(xml_tools, list):
                            found_xml = True
                            for t in xml_tools:
                                fn = (t or {}).get("function", {})
                                if fn.get("name"):
                                    xml_names.add(fn["name"])
                    if not found_xml:
                        sys_tools_parse_fail += 1
            for name in xml_names:
                func_via_xml_rows[name] += 1
            if defined and xml_names and defined != xml_names:
                xml_vs_field_mismatch_rows += 1

            # --- tool calls + urls + commands from all messages ---
            row_urls = set()
            row_cmd = False
            for msg in row["conversations"]:
                val = msg.get("value", "") or ""
                for um in URL_RE.finditer(val):
                    u = clean_url(um.group(0))
                    if u:
                        urls[u] += 1
                        row_urls.add(u)
                if msg.get("from") == "gpt":
                    for tm in TOOLCALL_RE.finditer(val):
                        toolcall_total += 1
                        try:
                            tc = json.loads(tm.group(1))
                        except Exception:
                            toolcall_parse_fail += 1
                            continue
                        name = tc.get("name")
                        if not name:
                            continue
                        func_invocations[name] += 1
                        if SHELL_NAME_RE.search(name):
                            args = tc.get("arguments", {})
                            cmd = None
                            if isinstance(args, dict):
                                for k in CMD_KEYS:
                                    if isinstance(args.get(k), str) and args[k].strip():
                                        cmd = args[k]
                                        break
                            if cmd:
                                commands[(name, cmd.strip())] += 1
                                row_cmd = True
            if row_urls:
                url_rows += 1
            if row_cmd:
                command_rows += 1

            if (i + 1) % 500 == 0:
                update_progress(i + 1, rows_total, "extracting")

    stats = {
        "rows_total": rows_total,
        "keys_seen": sorted(keys_seen),
        "model_field_rows": model_field_rows,
        "from_values": dict(from_values),
        "categories": dict(categories),
        "subcategories": dict(subcategories),
        "distinct_functions_defined": len(func_defs),
        "toolcall_total": toolcall_total,
        "toolcall_parse_fail": toolcall_parse_fail,
        "sys_tools_parse_fail": sys_tools_parse_fail,
        "xml_vs_field_mismatch_rows": xml_vs_field_mismatch_rows,
        "url_rows": url_rows,
        "distinct_urls": len(urls),
        "command_rows": command_rows,
        "distinct_commands": len(commands),
    }

    def dump(name, obj):
        tmp = os.path.join(WORK, name + ".tmp")
        with open(tmp, "w") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
        os.replace(tmp, os.path.join(WORK, name))

    # functions: name, descriptions by popularity, rows, xml_rows, invocations
    fn_list = []
    for name, descs in sorted(func_defs.items()):
        top_desc = descs.most_common(1)[0][0]
        fn_list.append({
            "name": name,
            "description": top_desc,
            "description_variants": len(descs),
            "rows_defined": func_rows[name],
            "rows_via_xml": func_via_xml_rows.get(name, 0),
            "invocations": func_invocations.get(name, 0),
        })
    dump("functions.json", fn_list)
    dump("urls.json", [{"url": u, "count": c} for u, c in urls.most_common()])
    dump("commands.json", [
        {"function": fn, "command": cmd, "count": c}
        for (fn, cmd), c in commands.most_common()
    ])
    dump("extraction_stats.json", stats)
    update_progress(rows_total, rows_total, "extracted",
                    notes=["extraction_stats.json, functions.json, urls.json, commands.json written"])

    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
