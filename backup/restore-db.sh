#!/usr/bin/env bash
#
# restore-db.sh — Reassemble chunked database backup (deflate).
#
# Takes the gzipped chunks from backup/chunks/, reassembles them,
# decompresses, verifies the hash, and restores to data/.local/factum.db.
#
# Usage:
#   ./backup/restore-db.sh [--force]
#
# Without --force, refuses to overwrite an existing database.
# With --force, backs up the existing DB to factum.db.bak.<timestamp> first.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DB_PATH="$REPO_ROOT/data/.local/factum.db"
CHUNK_DIR="$SCRIPT_DIR/chunks"
MANIFEST="$CHUNK_DIR/MANIFEST.json"

FORCE=0
if [[ "${1:-}" == "--force" ]]; then FORCE=1; fi

if [[ ! -f "$MANIFEST" ]]; then
    echo "ERROR: Manifest not found at $MANIFEST" >&2
    echo "Run ./backup/backup-db.sh first, or clone the repo with chunks." >&2
    exit 1
fi

if [[ -f "$DB_PATH" && $FORCE -eq 0 ]]; then
    echo "ERROR: Database already exists at $DB_PATH" >&2
    echo "Use --force to overwrite (existing DB will be backed up)." >&2
    exit 1
fi

# Verify all chunks present and hashes match
echo "Verifying chunks..."
python3 - "$MANIFEST" "$CHUNK_DIR" <<'EOF'
import json, hashlib, os, sys
manifest_path, chunk_dir = sys.argv[1], sys.argv[2]
with open(manifest_path) as f:
    m = json.load(f)
for c in m["chunks"]:
    p = os.path.join(chunk_dir, c["name"])
    if not os.path.exists(p):
        print(f"MISSING: {c['name']}", file=sys.stderr)
        sys.exit(1)
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    if h.hexdigest() != c["sha256"]:
        print(f"HASH MISMATCH: {c['name']}", file=sys.stderr)
        sys.exit(1)
    print(f"  OK: {c['name']} ({c['size']} bytes)")
print(f"All {len(m['chunks'])} chunks verified.")
EOF

# Back up existing DB if forcing
if [[ -f "$DB_PATH" && $FORCE -eq 1 ]]; then
    BACKUP="$DB_PATH.bak.$(date +%Y%m%dT%H%M%S)"
    echo "Backing up existing DB to $BACKUP"
    cp "$DB_PATH" "$BACKUP"
fi

# Reassemble and decompress
echo "Reassembling..."
TMP_GZ=$(mktemp)
cat "$CHUNK_DIR"/factum.db.gz.* > "$TMP_GZ"

# Verify reassembled gzip hash
EXPECTED_GZ=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['gz_sha256'])")
ACTUAL_GZ=$(sha256sum "$TMP_GZ" | cut -d' ' -f1)
if [[ "$EXPECTED_GZ" != "$ACTUAL_GZ" ]]; then
    echo "ERROR: Reassembled gzip hash mismatch!" >&2
    echo "  Expected: $EXPECTED_GZ" >&2
    echo "  Actual:   $ACTUAL_GZ" >&2
    rm -f "$TMP_GZ"
    exit 1
fi
echo "Gzip hash verified."

echo "Decompressing to $DB_PATH..."
mkdir -p "$(dirname "$DB_PATH")"
gzip -dc "$TMP_GZ" > "$DB_PATH"
rm -f "$TMP_GZ"

# Verify final DB hash
EXPECTED_DB=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['db_sha256'])")
ACTUAL_DB=$(sha256sum "$DB_PATH" | cut -d' ' -f1)
if [[ "$EXPECTED_DB" != "$ACTUAL_DB" ]]; then
    echo "ERROR: Restored database hash mismatch!" >&2
    echo "  Expected: $EXPECTED_DB" >&2
    echo "  Actual:   $ACTUAL_DB" >&2
    exit 1
fi

DB_SIZE=$(stat -c%s "$DB_PATH")
echo ""
echo "Done. Database restored: $DB_SIZE bytes, SHA256 verified."
echo "Run factum rebuild before using match/search."
