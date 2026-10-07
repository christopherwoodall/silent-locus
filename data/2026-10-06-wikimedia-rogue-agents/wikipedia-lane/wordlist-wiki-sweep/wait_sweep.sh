#!/bin/bash
# File-based completion check: all 9 wikis have insource-0..1147.json as valid JSON
cd ~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep
for i in $(seq 1 60); do
  missing_total=0
  for d in raw/*/; do
    for n in $(seq 0 1147); do
      f="$d/insource-$n.json"
      if [ ! -s "$f" ] || ! python3 -c "import json,sys; json.load(open('$f'))" 2>/dev/null; then
        missing_total=$((missing_total+1))
      fi
    done
  done
  if [ "$missing_total" -eq 0 ]; then echo "COMPLETE after ~$((i*3)) min"; exit 0; fi
  echo "waiting: $missing_total missing/invalid"
  sleep 180
done
echo "TIMEOUT with missing remaining"
