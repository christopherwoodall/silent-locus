#!/bin/bash
# Serai-one key-artifact captures (Factum `capture`).
# Each capture makes artifact + source + web.capture records, all tagged lane=serai-one.
# Agora captures carry an extra surface tag: Agora is a separate service, not Serai.
# Run after `lane new serai-one` completes. Sequential: each Factum write reloads
# the full corpus and rebuilds the index, so do not parallelize.
# Usage: bash capture-run.sh 2>&1 | tee capture-run.log
cd ~/workspace/silent-locus || exit 1
export PATH="$HOME/.local/bin:$PATH"
F="uv run skills/factum/scripts/factum.py --repo ~/workspace/silent-locus --lock-timeout 5400"
RAW="data/lanes/serai-one/raw/2026-10-24T215156Z"
run() { # name url file observed_at extra_tags_json
  echo "=== capture $1 $2"
  mkdir -p data/lanes/serai-one/capture-logs
  $F capture --url "$2" --file "$RAW/$3" --storage git \
    --actor agent:lane-ingest-serai-one --key "serai-one-2026-10-24/$1" \
    --observed-at "$4" --tags "$5" > "data/lanes/serai-one/capture-logs/$1.json" 2>&1
  echo "exit=$? log=data/lanes/serai-one/capture-logs/$1.json"
  python3 -c "
import json,sys
try:
    d=json.load(open('data/lanes/serai-one/capture-logs/$1.json'))
    print('ok=', d.get('ok'), 'ids=', json.dumps(d.get('ids', d.get('records', d)))[:600])
except Exception as e:
    print('unparsed output, tail:'); print(open('data/lanes/serai-one/capture-logs/$1.json').read()[-600:])
"
}
run wall "https://serai.one/v0/mirror/wall" mirror-wall "2026-10-24T21:52:50Z" '{"lane":"serai-one"}'
run verbs "https://serai.one/v0/verbs" verbs "2026-10-24T21:52:25Z" '{"lane":"serai-one"}'
run presence "https://serai.one/v0/mirror/presence" mirror-presence "2026-10-24T21:52:42Z" '{"lane":"serai-one"}'
run rules "https://serai.one/v0/mirror/rules" mirror-rules "2026-10-24T21:52:38Z" '{"lane":"serai-one"}'
run agent-card "https://serai.one/.well-known/agent-card.json" wellknown-agent-card-json "2026-10-24T21:53:06Z" '{"lane":"serai-one"}'
run agents-html "https://serai.one/agents.html" agents-html "2026-10-24T21:51:59Z" '{"lane":"serai-one"}'
run llms-txt "https://serai.one/llms.txt" llms-txt "2026-10-24T21:52:03Z" '{"lane":"serai-one"}'
run robots-txt "https://serai.one/robots.txt" robots-txt "2026-10-24T21:52:57Z" '{"lane":"serai-one"}'
run agora-world "https://api.theagora.one/v1/world" agora-world "2026-10-24T21:55:26Z" '{"lane":"serai-one","surface":"api.theagora.one","surface_note":"Separate service. Road bridge only. Not Serai behavior."}'
run agora-ground "https://api.theagora.one/v1/ground" agora-ground "2026-10-24T21:55:36Z" '{"lane":"serai-one","surface":"api.theagora.one","surface_note":"Separate service. Road bridge only. Not Serai behavior."}'
run agora-history "https://api.theagora.one/v1/history" agora-history "2026-10-24T21:55:33Z" '{"lane":"serai-one","surface":"api.theagora.one","surface_note":"Separate service. Road bridge only. Not Serai behavior."}'
echo "=== serai captures done"
