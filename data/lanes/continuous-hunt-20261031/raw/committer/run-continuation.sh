#!/bin/bash
# COMMITTER CONTINUATION lane, continuous hunt round 20261031.
# Read-only GET via existing gh CLI auth only. No POST, no fresh login.
# Pacing: 60 s sleep between search calls (starts >60 s apart).
# Guard: on any rate-limit/403 response, STOP immediately, record stopping
# point in STOPPED.txt, do not retry in a loop.
set -u
cd "$(dirname "$0")"
LOG=run.log
: > "$LOG"
echo "run start: $(date -u +%Y-%m-%dT%H:%M:%SZ) (UTC), local CDT: $(date +%Y-%m-%dT%H:%M:%S%z)" >> "$LOG"

PACE=60
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

# ---- Pass 1: meta follow-ups ----
run_one "commits-codex" gh-commits-codex.json err-codex.txt -- search commits "Co-Authored-By: Codex" --limit 30 --json author,committer,commit,repository,sha,url || exit 3
pace
run_one "prs-claudecode" gh-prs-claudecode.json err-prs-claudecode.txt -- search issues "Generated with Claude Code type:pr" --include-prs --limit 30 --json author,title,url,repository,createdAt,body || exit 3
pace
run_one "prs-agent-harness" gh-prs-agent-harness.json err-prs-agent-harness.txt -- search issues "agent harness type:pr" --include-prs --limit 30 --json author,title,url,repository,createdAt || exit 3
pace
# ---- Pass 2: new vendor footer shapes ----
run_one "commits-cursor" gh-commits-cursor.json err-cursor.txt -- search commits "Co-Authored-By: Cursor" --limit 30 --json author,committer,commit,repository,sha,url || exit 3
pace
run_one "commits-jules" gh-commits-jules.json err-jules.txt -- search commits "Co-Authored-By: Jules" --limit 30 --json author,committer,commit,repository,sha,url || exit 3
pace
run_one "commits-gemini" gh-commits-gemini.json err-gemini.txt -- search commits "Co-Authored-By: Gemini" --limit 30 --json author,committer,commit,repository,sha,url || exit 3
pace
run_one "commits-aider" gh-commits-aider.json err-aider.txt -- search commits "Co-Authored-By: Aider" --limit 30 --json author,committer,commit,repository,sha,url || exit 3
pace
run_one "commits-codex-openai" gh-commits-codex-openai.json err-codex-openai.txt -- search commits "Co-Authored-By: OpenAI Codex" --limit 30 --json author,committer,commit,repository,sha,url || exit 3
pace
# ---- Pass 3: self-declared agent account as author ----
run_one "commits-copilot-bot" gh-commits-copilot-bot.json err-copilot-bot.txt -- search commits "author:github-copilot[bot]" --limit 30 --json author,committer,commit,repository,sha,url || exit 3

echo "run end: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
echo DONE
