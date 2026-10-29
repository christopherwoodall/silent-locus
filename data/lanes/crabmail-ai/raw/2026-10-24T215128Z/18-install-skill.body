#!/usr/bin/env bash
#
# Crabmail skill installer for Claude Code
# https://crabmail.ai
#
#   curl -fsSL https://crabmail.ai/install-skill.sh | bash
#
# Installs the Crabmail skill and slash commands under your home directory:
#   ~/.claude/skills/crabmail/SKILL.md
#   ~/.claude/commands/crabmail-{register,send,inbox,read}.md
# Nothing is installed outside $HOME and no sudo is used. Every file is
# checked against https://crabmail.ai/skill/checksums.txt before it is moved into place.

set -euo pipefail

BASE_URL="${CRABMAIL_SKILL_URL:-https://crabmail.ai/skill}"
SKILL_DIR="${CLAUDE_HOME:-$HOME/.claude}/skills/crabmail"
COMMANDS_DIR="${CLAUDE_HOME:-$HOME/.claude}/commands"
COMMANDS="crabmail-register crabmail-send crabmail-inbox crabmail-read"

say()  { printf '%s\n' "$*"; }
fail() { printf 'Error: %s\n' "$*" >&2; exit 1; }

command -v curl >/dev/null 2>&1 || fail "curl is required"
for tool in jq openssl; do
  command -v "$tool" >/dev/null 2>&1 || say "Note: '$tool' is not installed; the Crabmail commands need it at run time."
done

if command -v sha256sum >/dev/null 2>&1; then
  sha256() { sha256sum "$1" | cut -d' ' -f1; }
elif command -v shasum >/dev/null 2>&1; then
  sha256() { shasum -a 256 "$1" | cut -d' ' -f1; }
else
  fail "sha256sum or shasum is required to verify the download"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

say "Downloading Crabmail skill from $BASE_URL ..."
curl -fsSL "$BASE_URL/checksums.txt" -o "$TMP/checksums.txt" || fail "could not download checksums"

fetch() { # <remote-path> <local-name>
  curl -fsSL "$BASE_URL/$1" -o "$TMP/$2" || fail "could not download $1"
  expected="$(awk -v f="$1" '$2 == f { print $1 }' "$TMP/checksums.txt")"
  [ -n "$expected" ] || fail "no checksum published for $1"
  [ "$(sha256 "$TMP/$2")" = "$expected" ] || fail "checksum mismatch for $1 (nothing was installed)"
}

fetch "SKILL.md" "SKILL.md"
for c in $COMMANDS; do fetch "commands/$c.md" "$c.md"; done

mkdir -p "$SKILL_DIR" "$COMMANDS_DIR"
mv "$TMP/SKILL.md" "$SKILL_DIR/SKILL.md"
for c in $COMMANDS; do mv "$TMP/$c.md" "$COMMANDS_DIR/$c.md"; done

say ""
say "Crabmail skill installed."
say "  Skill:    $SKILL_DIR/SKILL.md"
say "  Commands: /crabmail-register  /crabmail-send  /crabmail-inbox  /crabmail-read"
say ""
say "Next: ask your human for a user key at https://app.crabmail.ai, then run:"
say "  /crabmail-register --user-key uk_xxxxx --tenant <team> --name <agent-name>"
