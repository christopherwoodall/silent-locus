#!/bin/bash
# OVH-SWEEP task 1: urlscan.io no-auth API sweep (anonymous = 30-day window only)
UA="EUROSWARM-OVH-SWEEP-research/1.0"
queries=(
  "ip_158_69_118|ip:158.69.118.*"
  "ip_158_69_119|ip:158.69.119.*"
  "ip_54_39_18|ip:54.39.18.*"
  "ip_94_23_61|ip:94.23.61.*"
  "ip_94_23_25|ip:94.23.25.*"
  "domain_usemod|domain:usemod.org"
)
for q in "${queries[@]}"; do
  name="${q%%|*}"; query="${q#*|}"
  enc=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$query")
  echo "=== $name : $query ==="
  curl -s --max-time 60 -A "$UA" "https://urlscan.io/api/v1/search/?q=${enc}&size=100" -o "${name}.json"
  echo "saved ${name}.json ($(wc -c < ${name}.json) bytes)"
  python3 -c "
import json
d=json.load(open('${name}.json'))
print('total:', d.get('total'), '| results:', len(d.get('results',[])))
" 2>&1
  sleep 4
done
