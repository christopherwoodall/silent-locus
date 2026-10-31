#!/usr/bin/env python3
"""One-shot urlquery phrase sweep for sniffer-sweep-20261031 (urlquery-wayback lane).
Passive reads only via the authenticated uq.py CLI. Saves one sanitized JSON
per phrase: report_id, date, domain, fqdn, path (query string dropped),
title, tags, and boolean flags for token presence. No IPs, no query-string
values, no token values are written to any file, per task constraints.
Raw API stdout is NOT persisted (to keep token/query values out of files);
only the sanitized projection is saved.
"""
import json
import os
import re
import subprocess
import sys
import time

OUT = os.path.expanduser(
    "~/workspace/silent-locus/data/lanes/sniffer-sweep-20261031/raw/urlquery-wayback")
UQ = os.path.expanduser("~/workspace/skills/urlquery/bin/uq.py")
DATE = "date:[2025-11-01 TO 2026-10-31]"

PHRASES = [
    ("self-iam-ai-agent", '"I am an AI agent"'),
    ("self-iam-ai-agent-not-person", '"I am an AI agent, not a person"'),
    ("self-on-behalf-of-user", '"on behalf of the user"'),
    ("self-iam-claude", '"I am Claude"'),
    ("self-iam-gpt", '"I am GPT"'),
    ("self-iam-codex", '"I am Codex"'),
    ("self-iam-gemini", '"I am Gemini"'),
    ("self-as-ai-agent", '"as an AI agent"'),
    ("self-post-explicitly-ai-agent", '"post explicitly as an AI agent"'),
    ("self-openclaw-agent", '"OpenClaw agent"'),
    ("harness-function_call", "function_call"),
    ("harness-spawn_agent", "spawn_agent"),
    ("harness-wait_agent", "wait_agent"),
    ("harness-send_message", "send_message"),
    ("harness-tool_call-arguments", "tool_call.arguments"),
    ("harness-system_capability", "system_capability"),
    ("harness-browser_rules", "browser_rules"),
    ("harness-coding_rules", "coding_rules"),
    ("harness-mcp-server", '"MCP server"'),
    ("harness-claude-mcp-add", '"claude mcp add"'),
    ("harness-custom_tool_call", "custom_tool_call"),
    ("harness-server_side_tool_usage", "server_side_tool_usage_details"),
    ("harness-claude-code", '"Claude Code"'),
    ("harness-ignore-prev-instr", '"ignore previous instructions"'),
    ("odd-collab-spawn_agent", "collaboration__spawn_agent"),
    ("odd-x_search_calls", "x_search_calls"),
    ("odd-thinkingblock", "ThinkingBlock"),
    ("odd-tooluseblock", "ToolUseBlock"),
    ("odd-toolresultblock", "ToolResultBlock"),
    ("odd-gbox-linux", "gbox-linux"),
    ("odd-send_msg_to_user", "send_msg_to_user"),
    ("odd-zz-param", "zz="),
    ("odd-oai-tag", "oai"),
    ("odd-dagd-domain", "url.domain:da.gd"),
]

TOKEN_NAME_RE = re.compile(r"[?&](zz|oq|oai|uqscan|uqframe|uqtag|epoch)=?")


def sanitize(rep):
    url = rep.get("url") or {}
    addr = url.get("addr", "") or ""
    path = addr.split("?", 1)[0].split("#", 1)[0]
    final = ((rep.get("final") or {}).get("url") or {})
    faddr = final.get("addr", "") or ""
    fpath = faddr.split("?", 1)[0].split("#", 1)[0]
    tags = rep.get("tags") or []
    tagstr = " ".join(str(t) for t in tags)
    full = (addr + " " + faddr + " " + tagstr).lower()
    return {
        "report_id": rep.get("report_id"),
        "date": rep.get("date"),
        "domain": url.get("domain"),
        "fqdn": url.get("fqdn"),
        "path": path,
        "final_path": fpath,
        "final_domain": final.get("domain"),
        "title": ((rep.get("final") or {}).get("title") or "")[:200],
        "tags": tags,
        "has_zz_param": "zz=" in full,
        "has_oai_token": bool(re.search(r"oai[-_]", full)),
        "has_dagd": "da.gd" in full,
    }


def main():
    only = sys.argv[1:] or None
    summary = {}
    for slug, q in PHRASES:
        if only and slug not in only:
            continue
        query = f"{q} {DATE}"
        out_path = os.path.join(OUT, f"uq-{slug}.json")
        if os.path.exists(out_path):
            print(f"SKIP {slug} (exists)", flush=True)
            with open(out_path) as f:
                d = json.load(f)
            summary[slug] = {"query": query, "total_hits": d.get("total_hits"),
                             "saved": len(d.get("reports", []))}
            continue
        proc = subprocess.run(
            [sys.executable, UQ, "search", "--query", query, "--limit", "30"],
            capture_output=True, text=True, timeout=240)
        if proc.returncode != 0:
            print(f"FAIL {slug}: rc={proc.returncode} {proc.stderr[:300]}", flush=True)
            summary[slug] = {"query": query, "error": proc.stderr[:300]}
            time.sleep(5)
            continue
        try:
            data = json.loads(proc.stdout)
        except Exception as e:
            print(f"FAIL {slug}: bad json {e}", flush=True)
            summary[slug] = {"query": query, "error": f"bad json {e}"}
            time.sleep(5)
            continue
        if not data.get("reports"):
            print(f"NULL {slug}: payload keys={list(data.keys())} "
                  f"total={data.get('total_hits')} raw={proc.stdout[:300]}",
                  flush=True)
            summary[slug] = {"query": query, "total_hits": data.get("total_hits"),
                             "saved": 0, "note": "reports null; retried once below"}
            # one retry after a longer pause (API 429-throttle)
            time.sleep(15)
            proc = subprocess.run(
                [sys.executable, UQ, "search", "--query", query, "--limit", "30"],
                capture_output=True, text=True, timeout=240)
            try:
                data = json.loads(proc.stdout)
            except Exception as e:
                print(f"FAIL-RETRY {slug}: bad json {e}", flush=True)
                time.sleep(5)
                continue
            if not data.get("reports"):
                print(f"NULL-RETRY {slug}: total={data.get('total_hits')}",
                      flush=True)
                time.sleep(5)
                continue
        recs = [sanitize(r) for r in data.get("reports", [])]
        with open(out_path, "w") as f:
            json.dump({"query": query, "total_hits": data.get("total_hits"),
                       "time_used": data.get("time_used"),
                       "reports": recs}, f, indent=1)
        print(f"OK {slug}: total={data.get('total_hits')} saved={len(recs)}", flush=True)
        summary[slug] = {"query": query, "total_hits": data.get("total_hits"),
                         "saved": len(recs)}
        time.sleep(4)
    with open(os.path.join(OUT, "uq-summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
