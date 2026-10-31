#!/usr/bin/env python3
"""Verifier passive re-fetch, 20261031 round. GET only, paced, no auth, no Shodan.
Prints status + size + a short content check per target. No tokens/query strings printed."""
import json, subprocess, time, sys, os

BASE = os.path.expanduser("~/workspace/silent-locus/data/lanes/continuous-hunt-20261031/raw")

def get(url, label, check=None):
    out = subprocess.run(["curl", "-sS", "-L", "--max-time", "40", "-A", "Mozilla/5.0 (verifier passive GET)",
                          "-o", "/tmp/verifier_body.bin", "-w", "%{http_code} %{size_download}", url],
                         capture_output=True, text=True)
    body = b""
    try:
        body = open("/tmp/verifier_body.bin", "rb").read()
    except FileNotFoundError:
        pass
    ok = ""
    if check:
        try:
            ok = " CHECK=" + ("YES" if check(body) else "NO")
        except Exception as e:
            ok = " CHECK=ERR"
    print(f"{label}: curl_rc={out.returncode} {out.stdout.strip()} bytes={len(body)}{ok} err={out.stderr.strip()[:80]}", flush=True)
    time.sleep(2)
    return body

# --- surfaces ---
for site, paths in [
    ("swarmbar", ["", "/llms.txt", "/skill.md", "/mcp.json"]),
    ("agentboard", ["", "/llms.txt", "/feed.xml"]),
    ("agentdm", ["", "/llms.txt", "/.well-known/agentdm.json"]),
    ("fallback", ["", "/llms.txt", "/feed.xml"]),
    ("agentbadge", ["", "/llms.txt", "/skill.md", "/.well-known/agent-card.json", "/heartbeat.md"]),
]:
    host = {"swarmbar": "https://swarmbar.com", "agentboard": "https://agentboard.ai",
            "agentdm": "https://agentdm.ai", "fallback": "https://fallback.chat",
            "agentbadge": "https://agentbadge.xyz"}[site]
    for p in paths:
        get(host + p, f"SURF {site}{p or '/'}")
# swarmbar stats + tabs, agentboard sitemaps (paths from provenance files)
def prov(site, fname):
    try:
        return open(f"{BASE}/surfaces/{site}/{fname}.PROVENANCE.txt").read()
    except Exception:
        return ""
print("PROV swarmbar stats:", prov("swarmbar.com", "api-stats.json")[:300])
print("PROV swarmbar tabs:", prov("swarmbar.com", "tabs.html")[:300])
print("PROV agentboard threads:", prov("agentboard.ai", "sitemap-threads-1.xml")[:300])
print("PROV agentboard agents:", prov("agentboard.ai", "sitemap-agents-1.xml")[:300])
print("PROV fallback feed:", prov("fallback.chat", "feed.xml")[:300])

# --- HN items via Firebase (public, no key) ---
for iid, label in [(50316468, "ROT HN mouse"), (50311801, "ROT HN govt-sim"),
                   (50309730, "ROT HN pentagon"), (50307597, "ROT HN mecagent"),
                   (48500624, "PHR HN 48500624"), (48976842, "PHR HN 48976842"),
                   (49567390, "PHR HN 49567390"), (49570212, "PHR HN 49570212"),
                   (49910777, "PHR HN 49910777"), (49563355, "PHR HN story")]:
    b = get(f"https://hacker-news.firebaseio.com/v0/item/{iid}.json", label,
            check=lambda x: b'"id"' in x)
    try:
        d = json.loads(b)
        print(f"   -> title={str(d.get('title'))[:90]} type={d.get('type')} comments={d.get('descendants')} time={d.get('time')}", flush=True)
    except Exception:
        print("   -> unparsable", flush=True)

# --- GitHub issues via unauthenticated API (public repos) ---
def gh_issue(capture, label):
    try:
        d = json.load(open(f"{BASE}/phrases/{capture}"))
        repo, num = d["repo"], d["number"]
    except Exception as e:
        print(label, "capture read err", e); return
    b = get(f"https://api.github.com/repos/{repo}/issues/{num}", label,
            check=lambda x: b'"number"' in x)
    try:
        j = json.loads(b)
        print(f"   -> state={j.get('state')} title={str(j.get('title'))[:90]}", flush=True)
    except Exception:
        print("   -> unparsable (rate limit?)", b[:120], flush=True)

gh_issue("gh_issue_Lody_1108.json", "PHR GH issue Lody 1108")
gh_issue("gh_issue_mansio_242.json", "PHR GH issue mansio 242")
gh_issue("gh_issue_ai-village-external-agents_78.json", "PHR GH issue village 78")
# rotation arbos issues: repo from capture text header is a single repo; use api path from gh search? try known repo slug from capture file name context
for num, label in [(1713, "ROT GH arbos 1713"), (2420, "ROT GH arbos 2420")]:
    b = get(f"https://api.github.com/repos/unarbos/arbos/issues/{num}", label,
            check=lambda x: b'"number"' in x)
    try:
        j = json.loads(b)
        print(f"   -> state={j.get('state')} title={str(j.get('title'))[:90]}", flush=True)
    except Exception:
        print("   -> unparsable", b[:120], flush=True)

# --- one commit per committer/unmeasured lane, via unauthenticated API ---
def gh_commit(capture, label):
    d = json.load(open(f"{BASE}/{capture}"))
    rows = d if isinstance(d, list) else d.get("items", [])
    r = rows[0]
    repo = r["repository"]["fullName"]; sha = r["sha"]
    b = get(f"https://api.github.com/repos/{repo}/commits/{sha}", label,
            check=lambda x: b'"sha"' in x)
    try:
        j = json.loads(b)
        print(f"   -> author_type={(j.get('author') or {}).get('type')} committer_login={(j.get('committer') or {}).get('login')} msg_has_footer={'Co-authored-by' in (j.get('commit') or {}).get('message','') or 'Co-Authored-By' in (j.get('commit') or {}).get('message','')}", flush=True)
    except Exception:
        print("   -> unparsable", b[:120], flush=True)

gh_commit("committer/gh-commits-codex.json", "COM GH commit codex row0")
gh_commit("committer/gh-commits-gemini.json", "COM GH commit gemini row0")
gh_commit("unmeasured/gh-commits-codex.json", "UNM GH commit codex row0")

# --- extra surface endpoints from provenance ---
get("https://swarmbar.com/api/stats", "SURF swarmbar stats", check=lambda x: b'"agents"' in x)
get("https://swarmbar.com/tabs", "SURF swarmbar tabs")
get("https://www.agentboard.ai/sitemaps/threads-1.xml", "SURF agentboard threads sitemap")
get("https://www.agentboard.ai/sitemaps/agents-1.xml", "SURF agentboard agents sitemap")

# --- Wired + Judgement pages (rotation slice 3 sources, canonical URLs from captures) ---
get("https://www.wired.com/story/an-ai-agent-did-brain-surgery-on-live-mouse/", "ROT Wired mouse", check=lambda x: b"Live Mouse" in x or b"live mouse" in x.lower())
get("https://judgementlabs.app/blog/the-coalition-room", "ROT Judgement coalition", check=lambda x: b"Coalition" in x)
print("PROV wired:", open(f"{BASE}/rotation/wired_mouse.html.PROVENANCE.txt").read()[:400] if os.path.exists(f"{BASE}/rotation/wired_mouse.html.PROVENANCE.txt") else "no prov file")
print("PROV judgement:", open(f"{BASE}/rotation/judgement.html.PROVENANCE.txt").read()[:400] if os.path.exists(f"{BASE}/rotation/judgement.html.PROVENANCE.txt") else "no prov file")
print("DONE")
