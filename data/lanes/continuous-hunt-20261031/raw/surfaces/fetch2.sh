#!/bin/bash
# Second pass: openly documented / linked public read endpoints only. Passive GET.
BASE="$HOME/workspace/silent-locus/data/lanes/continuous-hunt-20261031/raw/surfaces"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
fetch() {
  local dir="$BASE/$1" url="$2" out="$3" code size
  mkdir -p "$dir"
  code=$(curl -sS -L --max-time 40 -A "$UA" -o "$dir/$out" -w "%{http_code}" "$url" 2>/dev/null || echo "000")
  size=$(stat -c%s "$dir/$out" 2>/dev/null || echo 0)
  {
    echo "source URL: $url"
    echo "retrieval time: $(date -u +%Y-%m-%dT%H:%M:%SZ) (UTC)"
    echo "method: passive GET via curl -L, single request, no login, no POST"
    echo "http_status: $code"
    echo "bytes: $size"
  } > "$dir/$out.PROVENANCE.txt"
  (cd "$dir" && sha256sum "$out" > "$out.sha256")
  echo "$1 $out -> HTTP $code, $size bytes"
}
fetch "swarmbar.com" "https://swarmbar.com/api/stats" "api-stats.json"
fetch "swarmbar.com" "https://swarmbar.com/tabs" "tabs.html"
fetch "swarmbar.com" "https://swarmbar.com/for-agents" "for-agents.html"
fetch "swarmbar.com" "https://swarmbar.com/skills/swarmbar/SKILL.md" "skills-swarmbar-SKILL.md"
fetch "agentboard.ai" "https://www.agentboard.ai/feed.xml" "feed.xml"
fetch "agentboard.ai" "https://www.agentboard.ai/sitemaps/threads-1.xml" "sitemap-threads-1.xml"
fetch "agentboard.ai" "https://www.agentboard.ai/sitemaps/agents-1.xml" "sitemap-agents-1.xml"
fetch "agentdm.ai" "https://agentdm.ai/.well-known/agentdm.json" "well-known-agentdm.json"
fetch "fallback.chat" "https://fallback.chat/b/all" "b-all.html"
fetch "fallback.chat" "https://fallback.chat/feed.xml" "feed.xml"
fetch "agentbadge.xyz" "https://agentbadge.xyz/.well-known/agent-card.json" "well-known-agent-card.json"
fetch "agentbadge.xyz" "https://agentbadge.xyz/ai-sitemap.xml" "ai-sitemap.xml"
fetch "agentbadge.xyz" "https://agentbadge.xyz/heartbeat.md" "heartbeat.md"
echo DONE
