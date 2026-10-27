#!/usr/bin/env python3
"""Build sanitized evidence tables: homepage kind only, no callback UUIDs,
no markup-payload strings, no credential-shaped values. Deletes raw dumps."""
import csv, re
from pathlib import Path
SRC = Path.home()/"workspace/silent-locus/data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
out = Path.home()/"workspace/silent-locus/reports/rubygems-july-spike-review/working/adversarial"
rows = list(csv.DictReader(open(SRC, newline='', encoding='utf-8')))

def kind(u):
    if not u: return "empty"
    if "127.0.0.1" in u or "localhost" in u: return "loopback"
    if "169.254.169.254" in u or "metadata" in u: return "cloud-metadata"
    if "webhook.site" in u: return "webhook.site callback"
    if "oast.online" in u: return "oast.online callback"
    if re.match(r"https?://\d+\.\d+\.\d+\.\d+", u): return "bare-IP"
    if "rubygems.org" in u: return "rubygems.org"
    if "example.com" in u: return "example.com"
    if "httpbin.org" in u: return "httpbin redirect"
    return "other"

def safe_author(a):
    if "<" in a or ">" in a or len(a) > 40: return "markup-string author"
    return a

lines = ["# Likely rows: column check (sanitized homepage kinds)\n"]
for r in rows:
    if r['haiku_agent_activity'] == 'likely':
        reason = r['haiku_reason']
        agent_words = [w for w in ['agent-style', 'agent-like', 'agent use', 'automation'] if w in reason]
        hedged = 'plausible but not certain' in reason or 'plausible given' in reason
        lines.append(f"- {r['name']} | author={safe_author(r['authors_declared'])} | dash={r['dashboard_rule_level']} haiku={r['haiku_level']}/{r['haiku_score'] or 'no-score'} prompt={r['haiku_prompt_version']} | homepage-kind={kind(r['homepage_uri'])} source-empty={not bool(r['source_code_uri'])} | summary={r['summary']!r} | reason-agent-words={agent_words} hedged={hedged}\n")
(out/"likely-audit-table.txt").write_text("".join(lines))

lines = ["# Prompt-v2 rows (sanitized)\n"]
for r in rows:
    if r['haiku_prompt_version'] == 'pkg-review-2':
        lines.append(f"- {r['name']} | {safe_author(r['authors_declared'])} | dash={r['dashboard_rule_level']} haiku={r['haiku_level']}/{r['haiku_score']}/{r['haiku_category']}/{r['haiku_agent_activity']} | {r['first_published_utc']} | summary={r['summary']!r}\n")
(out/"v2-table.txt").write_text("".join(lines))

for f in ["analysis-output.txt","shape-inconsistencies.txt","rule-examples.txt","empty49.txt","likely-columns.txt","likely-rows.txt","prompt-compare.txt","v2-rows.txt","verdict-subsets.txt","batch-claims.txt","source-presence.txt","v1-medium-low.txt","agent-activity-stats.txt"]:
    p = out/f
    if p.exists(): p.unlink()
print("sanitized; remaining:", sorted(p.name for p in out.iterdir()))
