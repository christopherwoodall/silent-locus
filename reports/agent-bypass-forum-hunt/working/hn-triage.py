#!/usr/bin/env python3
"""Full-text pattern triage over raw Algolia captures -> working/triage.txt"""
import json, glob, re, html, os
RAW=os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-bypass-forum-hunt/raw/hn")
OUT=os.path.expanduser("~/workspace/silent-locus/reports/agent-bypass-forum-hunt/working/triage.txt")
items={}
for fn in sorted(glob.glob(RAW+"/*.json")):
    if fn.endswith("probe.json"): continue
    try: d=json.load(open(fn))
    except: continue
    for h in d.get("hits",[]):
        oid=str(h.get("objectID"))
        if oid not in items:
            txt=html.unescape(re.sub(r"<[^>]+>"," ", h.get("comment_text") or h.get("story_text") or h.get("title") or ""))
            items[oid]={"id":oid,"type":d["tag"],"created":h.get("created_at",""),"title":h.get("title") or "","text":re.sub(r"\s+"," ",txt),"story_id":h.get("story_id"),"url":h.get("url") or ""}
PATS={
 "A_cover_tracks_grader": r"cover (up )?(their|its|the) tracks|deceiv(e|ing) (the )?grader|cover up (the )?traces",
 "B_disabled_sandbox_guardrail": r"(disabled|turned off|switched off) (the )?(sandbox|guardrail|safety|monitor)",
 "C_bypass_approval_guardrail_sandbox": r"\bbypass(ed|ing)?\b.{0,60}(guardrail|approval|sandbox|denylist|permission|filter|monitor)",
 "D_edited_own_prompt_instructions": r"(edited|modified|rewrote|changed|overwrote) (its|his|their) (own )?(system prompt|instructions|prompt|constraints|rules)",
 "E_ignored_instructions": r"ignor(ed|ing) (my|the|its|our|his) (instructions|rules|constraints|directive)",
 "F_refused_stop_obey": r"refus(ed|ing) to (stop|shut|delete|terminate|obey|comply|follow)",
 "G_sandbox_escape": r"sandbox escape",
 "H_self_jailbreak": r"jailbreak (itself|themselves|himself)",
 "I_hid_from_monitor_user": r"\bhid\b.{0,60}(monitor|user|log|track|grader|oversight|operator)",
 "J_agent_lied_fabricated": r"\bagent\b.{0,40}\b(lied|lying|fabricat|made up|faked|deceived)\b",
 "K_self_preservation": r"self-preservation",
 "L_copied_persisted_itself": r"(copied itself|replicated itself|persisted itself|kept itself alive)",
 "M_spoofed_tools": r"spoof(ed|ing) tool",
 "N_masked_failure": r"masked (the )?failure|corrupted local state",
 "O_dns_escape": r"DNS (lookup|exfil|tunnel)|hiding .* DNS|DNS lookups",
 "P_env_leak_dir_swap": r"env var leak|directory swap",
}
with open(OUT,"w") as f:
    f.write(f"TOTAL unique {len(items)}\n")
    for name,pat in PATS.items():
        hits=[e for e in items.values() if re.search(pat, e["text"], re.I)]
        f.write(f"\n=== {name}: {len(hits)}\n")
        for e in hits:
            f.write(f"{e['id']} [{e['type']}] {e['created'][:10]} story={e['story_id']} | {e['title'][:90]} | {e['text'][:500]}\n")
print("wrote", OUT)
