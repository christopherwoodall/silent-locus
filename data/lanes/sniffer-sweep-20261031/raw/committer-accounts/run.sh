#!/bin/bash
set -u
gh search commits "Co-Authored-By: Copilot" --limit 30 --json author,committer,commit,repository,sha,url > gh-commits-copilot.json 2>err-copilot.txt || echo "copilot FAIL: $(cat err-copilot.txt)"
gh search commits "Generated with Claude Code" --limit 30 --json author,committer,commit,repository,sha,url > gh-commits-claudecode-footer.json 2>err-cc.txt || echo "cc FAIL: $(cat err-cc.txt)"
gh search commits "Co-Authored-By: Devin" --limit 30 --json author,committer,commit,repository,sha,url > gh-commits-devin.json 2>err-devin.txt || echo "devin FAIL: $(cat err-devin.txt)"
gh search commits "Co-Authored-By: Codex" --limit 30 --json author,committer,commit,repository,sha,url > gh-commits-codex.json 2>err-codex.txt || echo "codex FAIL: $(cat err-codex.txt)"
gh search issues --type pr "Generated with Claude Code" --limit 30 --json author,title,url,repository,createdAt,body > gh-prs-claudecode.json 2>err-prcc.txt || echo "prcc FAIL: $(cat err-prcc.txt)"
gh search issues --type pr "agent" "harness" --limit 30 --json author,title,url,repository,createdAt > gh-prs-agent-harness.json 2>err-ah.txt || echo "ah FAIL: $(cat err-ah.txt)"
echo DONE
ls -la *.json
