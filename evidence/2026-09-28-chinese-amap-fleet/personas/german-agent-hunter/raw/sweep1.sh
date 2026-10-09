#!/bin/bash
# German agent hunter — sweep 1: close OPEN queries + new German gov/infra pivots
BIN=~/workspace/skills/urlquery/bin/uq_htmx.py
OUT=~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/german-agent-hunter/raw
queries=(
  "httpbun aufgabe"
  "httpbun agent"
  "webhook.site aufgabe"
  "claude httpbun"
  "uqscan berlin"
  "sub_poi_navi berlin"
  "url.domain:linkvertise.com"
  "url.domain:gov.de"
  "url.domain:bund.de"
  "url.domain:destatis.de"
  "url.domain:hetzner.com"
  "url.domain:hetzner.de"
  "httpbun programm"
  "httpbin programm"
  "url.domain:pastebin.de"
  "url.domain:t1p.de"
  "agent berlin httpbun"
  "ki agent urlquery"
)
i=0
for q in "${queries[@]}"; do
  i=$((i+1))
  slug=$(echo "$q" | tr ' :./' '____')
  echo "[$i/${#queries[@]}] $q"
  python3 "$BIN" search --query "$q" --limit 30 --delay 6 > "$OUT/q_$slug.json" 2>>"$OUT/sweep1.log"
  sleep 6
done
echo DONE
