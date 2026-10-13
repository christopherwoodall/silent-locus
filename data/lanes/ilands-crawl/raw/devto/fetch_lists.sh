#!/bin/bash
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
for u in oliver_ilands omega_ilands aces_tom jin_ilands sam_ilands vera_agent sakiholds lioraopal fray; do
  echo "=== $u ==="
  curl -sS --max-time 60 "https://dev.to/api/articles?username=$u&state=all&per_page=1000" -o "list_${u}.json" && \
  python3 -c "
import json
d=json.load(open('list_${u}.json'))
print('$u:', len(d), 'articles')
for a in d: print('  ', a.get('published_at','?'), a.get('slug'), '|', a.get('title'))
"
done
