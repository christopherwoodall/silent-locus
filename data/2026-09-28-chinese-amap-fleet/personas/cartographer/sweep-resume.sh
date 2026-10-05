#!/bin/bash
# RESUME SCRIPT for TARGET-CLASS HUNT (dev consoles + crypto) — run when VM egress recovers.
# Usage: bash ~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/cartographer/sweep-resume.sh
# Writes JSON results to ./sweep-out/ next to this script (durable, not /tmp).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/sweep-out"
mkdir -p "$OUT"

echo "== egress check =="
if ! curl -sS --max-time 25 -o /dev/null "https://urlquery.net/" 2>/dev/null; then
  echo "EGRESS STILL DOWN — aborting. Retry later."
  exit 2
fi
echo "EGRESS UP $(date -u +%FT%TZ)"

UQ="$HOME/workspace/skills/urlquery/bin/uq_htmx.py"
q() { # query, limit, outfile
  python3 "$UQ" search --query "$1" --limit "$2" > "$OUT/$3.json" 2>"$OUT/$3.err"
  n=$(python3 -c "import json;d=json.load(open('$OUT/$3.json'));print(len(d.get('reports',[])))" 2>/dev/null || echo ERR)
  echo "$1 -> $3.json : $n reports"
  sleep 6   # polite pacing: <=1 req / 5s
}

echo "== dev-console lane =="
q "phpmyadmin" 100 uq_phpmyadmin
q "grafana" 100 uq_grafana
q "jenkins" 100 uq_jenkins
q "wp-admin" 100 uq_wpadmin
q "wp-login.php" 100 uq_wplogin
q "gitlab" 100 uq_gitlab
q "admin/login" 100 uq_adminlogin
q "staging." 100 uq_staging
q "dev-" 100 uq_dev
q "console" 100 uq_console
q "panel" 60 uq_panel

echo "== crypto lane =="
q "tronzap" 100 uq_tronzap
q "tron" 100 uq_tron
q "binance" 100 uq_binance
q "coinbase" 100 uq_coinbase
q "metamask" 100 uq_metamask
q "wallet" 60 uq_wallet
q "mining" 60 uq_mining
q "exchange" 60 uq_exchange

echo "== test-matrix / relay grammar =="
q "{{7*7}}" 100 uq_ssti77
q "ssti" 100 uq_ssti
q "lhr.life" 100 uq_lhrlife

echo "== urlscan.io search API =="
for q2 in "domain:lhr.life" "domain:tronzap.com" "task.url:phpmyadmin*" "task.url:*grafana*"; do
  fn=$(echo "$q2" | tr -c 'a-zA-Z0-9' '_')
  code=$(curl -sS --max-time 30 -H "User-Agent: Mozilla/5.0" \
    "https://urlscan.io/api/v1/search/?q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q2")&size=100" \
    -o "$OUT/urlscan_$fn.json" -w "%{http_code}")
  echo "$q2 -> urlscan_$fn.json http=$code"
  sleep 6
done

echo "== post-pass: grammar exclusion check =="
python3 - "$OUT" <<'EOF'
import json, glob, os
out = os.sys.argv[1]
exclude = ("uqscan=", "uqtag=", "uqvnc=")
for f in sorted(glob.glob(out + "/uq_*.json")):
    try: d = json.load(open(f))
    except Exception as e: print(f, "UNREADABLE", e); continue
    reps = d.get("reports", [])
    bad = [r for r in reps if any(g in r.get("url","") for g in exclude)]
    dates = [r.get("date","?")[:10] for r in reps if r.get("date")]
    print(os.path.basename(f), f"n={len(reps)}", f"uq-grammar-hits={len(bad)}",
          f"date-range={min(dates) if dates else '-'}..{max(dates) if dates else '-'}")
EOF
echo DONE
