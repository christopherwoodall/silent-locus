#!/bin/bash
# Crabmail-ai key-artifact captures (Factum `capture`).
# Each capture makes artifact + source + web.capture records, all tagged lane=crabmail-ai.
# The provider public key and fingerprint in the descriptor/info bodies are published
# descriptor values, never credentials. The fingerprint does NOT verify the key (C21).
# Run after `lane new crabmail-ai` completes. Sequential: each Factum write reloads
# the full corpus and rebuilds the index, so do not parallelize.
# Usage: bash capture-run.sh 2>&1 | tee capture-run.log
cd ~/workspace/silent-locus || exit 1
export PATH="$HOME/.local/bin:$PATH"
F="uv run skills/factum/scripts/factum.py --repo ~/workspace/silent-locus --lock-timeout 5400"
RAW="data/lanes/crabmail-ai/raw/2026-10-24T215128Z"
run() { # name url file observed_at
  echo "=== capture $1 $2"
  mkdir -p data/lanes/crabmail-ai/capture-logs
  $F capture --url "$2" --file "$RAW/$3" --storage git \
    --actor agent:lane-ingest-crabmail-ai --key "crabmail-ai-2026-10-24/$1" \
    --observed-at "$4" --tags '{"lane":"crabmail-ai"}' > "data/lanes/crabmail-ai/capture-logs/$1.json" 2>&1
  echo "exit=$? log=data/lanes/crabmail-ai/capture-logs/$1.json"
  python3 -c "
import json
try:
    d=json.load(open('data/lanes/crabmail-ai/capture-logs/$1.json'))
    print('ok=', d.get('ok'), 'ids=', json.dumps(d.get('ids', d.get('records', d)))[:600])
except Exception:
    print('unparsed output, tail:'); print(open('data/lanes/crabmail-ai/capture-logs/$1.json').read()[-600:])
"
}
# descriptor-api SKIPPED on resume 2026-10-25: the first chain run's background
# session died after the capture was accepted. Its pending file proves acceptance:
# data/.local/pending/20345c2ec5b245f09309557f05de2e15.json
# (artifact_a3402a15f9b24ea4b1a5565402cdedcb,
#  source_c54acfbc78124681ba0ebd007a7b821a,
#  observation_4f0e9fa631ec47dfbac71c3792ac47ad).
# Re-running it with the same idempotency key would only return those IDs, so it
# is skipped to save a full-corpus rebuild. See capture-logs/descriptor-api.RECOVERED.txt.
# run descriptor-api "https://api.crabmail.ai/.well-known/agent-messaging.json" 01-api-wellknown.body "2026-10-24T21:51:37Z"
run descriptor-root "https://crabmail.ai/.well-known/agent-messaging.json" 02-root-wellknown.body "2026-10-24T21:51:42Z"
run provider-home "https://crabmail.ai/" 05-provider-home.body "2026-10-24T21:51:52Z"
run developers-md "https://crabmail.ai/developers/index.md" 13-developers-md.body "2026-10-24T21:52:44Z"
run health "https://api.crabmail.ai/v1/health" 15-health.body "2026-10-24T21:52:56Z"
run info "https://api.crabmail.ai/v1/info" 16-info.body "2026-10-24T21:53:00Z"
run openapi "https://api.crabmail.ai/v1/openapi.json" 17-openapi.body "2026-10-24T21:53:05Z"
run install-skill "https://crabmail.ai/install-skill.sh" 18-install-skill.body "2026-10-24T21:53:26Z"
echo "=== crabmail captures done"
