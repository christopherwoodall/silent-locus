#!/bin/bash
# Pre-ingest fuzzy dedup matches for lane 2026-10-11-deepmind-interactions-api.
# Writes one line per term: <term> | <n matches> | <top lane:value snippets>
cd ~/workspace/wt-ingest-dmapi || exit 1
OUT=data/lanes/2026-10-11-deepmind-interactions-api/dedup-results.txt
: > "$OUT"
for t in "gemini-3.5-flash" "gemini-3.6-flash" "gemini-2.5-flash" "gemini-4-argon" \
         "EmbeddingGemma" "antigravity-preview" "deep-research-pro-preview" \
         "gemini-robotics" "sec-gemini" "lyria" \
         "interactions API" "gemini-cli" "webhook-signature" "hooks.json" \
         "previous_interaction_id" "computer_use" "CyberGym" "OSWorld" "Mind2Web" \
         "gemini-api-docs-mcp" "max_total_tokens" "use_interactions_api"; do
  python3 skills/factum/scripts/factum.py --repo . match --text "$t" --mode fuzzy 2>/dev/null | \
  python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except Exception: print('$t | ERROR'); sys.exit()
m=d.get('matches',[])
hits=[]
for x in m[:5]:
    tags=(x.get('tags') or {}); v=(x.get('value') or '')
    body=(x.get('body') or {}); data=(body.get('data') or {}); term=data.get('term') or data.get('value') or v
    hits.append(tags.get('lane','?')+':'+str(term)[:70])
print('$t | n='+str(len(m))+' | '+' // '.join(hits))
" >> "$OUT" 2>&1
done
echo "done -> $OUT"
