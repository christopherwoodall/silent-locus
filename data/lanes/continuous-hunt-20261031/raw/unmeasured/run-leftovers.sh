#!/bin/bash
# UNMEASURED-LEFTOVERS lane, continuous hunt 20261031.
# Read-only GET via existing gh CLI auth only. No POST, no fresh login.
# Pacing: 55s sleep between search calls (starts >30s apart per brief).
# Guard: on any rate-limit/403 response, STOP immediately, record stopping
# point in STOPPED.txt, do not retry.
set -u
cd "$(dirname "$0")"
LOG=run.log
: > "$LOG"
echo "run start: $(date -u +%Y-%m-%dT%H:%M:%SZ) (UTC)" >> "$LOG"
PACE=55
stopped=0
run_one() {
  local label="$1" out="$2" err="$3"; shift 3; shift 1
  echo "=== $label start $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
  echo "CMD: gh $*" >> "$LOG"
  gh "$@" > "$out" 2> "$err"
  local rc=$?
  echo "=== $label rc=$rc bytes=$(stat -c%s "$out" 2>/dev/null || echo '?') $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
  if grep -qiE 'rate limit|secondary rate|HTTP 403' "$err" 2>/dev/null; then
    echo "RATE GUARD FIRED at $label $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
    echo "stopped at: $label" > STOPPED.txt
    echo "time_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> STOPPED.txt
    echo "stderr:" >> STOPPED.txt
    cat "$err" >> STOPPED.txt
    stopped=1
    return 3
  fi
  if [ $rc -ne 0 ]; then
    echo "NONZERO rc=$rc at $label (not rate guard; continuing to next call)" >> "$LOG"
  fi
  {
    echo "command: gh $*"
    echo "retrieved_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "method: gh CLI search (read-only GET), existing gh auth, no fresh login"
    echo "exit_code: $rc"
  } > "$out.PROVENANCE.txt"
  sha256sum "$out" > "$out.sha256" 2>/dev/null || true
  sha256sum "$err" > "$err.sha256" 2>/dev/null || true
  return 0
}
pace() { sleep "$PACE"; }

run_one "commits-codex" gh-commits-codex.json err-codex.txt -- search commits "Co-Authored-By: Codex" --limit 30 --json author,committer,commit,repository,sha,url || exit 3
pace
run_one "prs-claudecode" gh-prs-claudecode.json err-prs-claudecode.txt -- search issues "Generated with Claude Code type:pr" --include-prs --limit 30 --json author,title,url,repository,createdAt,body || exit 3
pace
run_one "prs-agent-harness" gh-prs-agent-harness.json err-prs-agent-harness.txt -- search issues "agent harness type:pr" --include-prs --limit 30 --json author,title,url,repository,createdAt || exit 3
pace

i=0
while IFS= read -r line; do
  i=$((i+1))
  slug=$(printf '%s' "$line" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//')
  printf -v num "%02d" "$i"
  out="phrase-${num}-${slug}.json"
  err="phrase-${num}-${slug}.err.txt"
  echo "$i|$line|$out" >> phrase-map.tsv
  run_one "phrase-$num-$slug" "$out" "$err" -- search issues "$line" --limit 30 --json author,title,url,repository,createdAt || exit 3
  pace
done <<'PHRASES'
I am GPT
I am Codex
I am Gemini
function_call
system_capability
browser_rules
coding_rules
MCP server
claude mcp add
custom_tool_call
server_side_tool_usage_details
BOOTSTRAP.md
Claude Code
ignore previous instructions
ThinkingBlock/ToolUseBlock/ToolResultBlock
spawn_agent
wait_agent
send_message
tool_call.arguments
zz oai epoch
PHRASES

echo "run end: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
echo DONE
