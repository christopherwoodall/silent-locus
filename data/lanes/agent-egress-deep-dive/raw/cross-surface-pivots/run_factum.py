#!/usr/bin/env python3
"""Factum novelty checks. Read-only match queries only.
--lock-timeout 5400 BEFORE the subcommand, per brief.
Idempotent: skips terms already saved. No writes, no submissions."""
import json, os, subprocess

BASE = os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-egress-deep-dive/raw/cross-surface-pivots")
REPO = os.path.expanduser("~/workspace/silent-locus")
FACTUM = os.path.join(REPO, "skills/factum/scripts/factum.py")
TERMS = {
    "amos": ["fieldeffect.com", "AMOS"],
    "zenity": ["AgentCorruption", "Bedrock AgentCore"],
    "lifesciences345": ["get_capability_snapshot", "LifeSciences"],
    "corbanu876": ["CorbanuTerminal", "bubblewrap"],
    "guidance1498": ["validate_uri", "168.63.129.16"],
    "bootstrap108": ["Project-Bootstrap-Protocol"],
    "msagent1020": ["ms-agent", "modelscope"],
    "wingman278": ["Wingman"],
    "hermes108236": ["hermes-agent"],
    "openskynet77": ["OpenSkynet", "web_extract"],
    "routify49535519": ["routify-file-proxy", "routify"],
    "mcptoolbox49429926": ["mcp-toolbox", "CVE-2026-14540"],
    "cowork46622328": ["Claude Cowork", "Cowork"],
    "sheets48349487": ["Google Sheets", "PromptArmor"],
    "gitlost48827858": ["GitLost"],
    "sharedroot": ["SharedRoot"],
    "bedrockdns": ["Bedrock DNS", "DNS exfiltration"],
}

def main():
    out = {}
    spath = os.path.join(BASE, "factum-summary.json")
    if os.path.exists(spath):
        out = json.load(open(spath))
    for iid, terms in TERMS.items():
        out.setdefault(iid, {})
        for term in terms:
            for mode in ("exact", "fuzzy"):
                key = f"{term}::{mode}"
                if key in out[iid]:
                    continue
                fn = f"factum-{iid}-{mode}-{abs(hash(term))%99999}.json"
                try:
                    r = subprocess.run(["python3", FACTUM, "--repo", REPO, "--lock-timeout", "5400",
                                        "match", "--text", term, "--mode", mode, "--limit", "5"],
                                       capture_output=True, text=True, timeout=300)
                    data = json.loads(r.stdout) if r.stdout.strip().startswith("{") else {"error": r.stderr[:300], "stdout": r.stdout[:300]}
                except Exception as e:
                    data = {"error": f"{type(e).__name__}: {e}"}
                if isinstance(data, dict) and data.get("matches") is not None:
                    ms = data["matches"]
                    lanes = sorted({(m.get("tags") or {}).get("lane") for m in ms if (m.get("tags") or {}).get("lane")})
                    vals = [str(m.get("value"))[:200] for m in ms[:3]]
                    out[iid][key] = {"status": data.get("status"), "n": len(ms), "lanes": lanes, "sample_values": vals}
                else:
                    out[iid][key] = {"status": "ERROR", "n": None, "lanes": [], "sample_values": [], "error": str(data)[:300]}
                with open(spath, "w") as f:
                    json.dump(out, f, indent=2)
                print(f"{iid} {term} {mode} -> {out[iid][key]['status']} n={out[iid][key]['n']}", flush=True)
    print("ALL DONE factum")

if __name__ == "__main__":
    main()
