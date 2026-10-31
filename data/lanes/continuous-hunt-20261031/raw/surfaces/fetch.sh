#!/bin/bash
# NEW-SURFACE DIVES lane, round 20261031. Passive GET only. No POST/login/sessions.
BASE="$HOME/workspace/silent-locus/data/lanes/continuous-hunt-20261031/raw/surfaces"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
fetch() { # $1=targetdir $2=url $3=outfile
  local dir="$BASE/$1" url="$2" out="$3" code size
  mkdir -p "$dir"
  code=$(curl -sS -L --max-time 40 -A "$UA" -o "$dir/$out" -w "%{http_code}" "$url" 2>"$dir/$out.curlerr" || echo "000")
  size=$(stat -c%s "$dir/$out" 2>/dev/null || echo 0)
  {
    echo "source URL: $url"
    echo "retrieval time: $(date -u +%Y-%m-%dT%H:%M:%SZ) (UTC)"
    echo "method: passive GET via curl -L, single request, no login, no POST"
    echo "http_status: $code"
    echo "bytes: $size"
  } > "$dir/$out.PROVENANCE.txt"
  rm -f "$dir/$out.curlerr"
  (cd "$dir" && sha256sum "$out" > "$out.sha256")
  echo "$1 $out -> HTTP $code, $size bytes"
}
for t in swarmbar.com agentboard.ai agentdm.ai fallback.chat agentbadge.xyz; do
  fetch "$t" "https://$t/" "homepage.html"
  fetch "$t" "https://$t/llms.txt" "llms.txt"
  fetch "$t" "https://$t/skill.md" "skill.md"
  fetch "$t" "https://$t/mcp.json" "mcp.json"
  fetch "$t" "https://$t/robots.txt" "robots.txt"
  fetch "$t" "https://$t/sitemap.xml" "sitemap.xml"
done
echo DONE
