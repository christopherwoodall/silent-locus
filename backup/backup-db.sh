#!/usr/bin/env bash
#
# backup-db.sh — Zip and chunk the local Factum database for Git upload.
#
# GitHub rejects files over 100MB. The factum.db is ~1GB, so we gzip it
# and split into 50MB chunks that can be committed to the repo.
#
# Usage:
#   ./backup/backup-db.sh
#
# Output:
#   backup/chunks/factum.db.gz.aa, .ab, .ac, ... (50MB each)
#   backup/chunks/MANIFEST.json (chunk count, hashes, timestamp)
#
# The chunks are git-tracked. To restore, run ./backup/restore-db.sh.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DB_PATH="$REPO_ROOT/data/.local/factum.db"
CHUNK_DIR="$SCRIPT_DIR/chunks"
CHUNK_SIZE="50M"

if [[ ! -f "$DB_PATH" ]]; then
    echo "ERROR: Database not found at $DB_PATH" >&2
    exit 1
fi

DB_SIZE=$(stat -c%s "$DB_PATH")
DB_SHA=$(sha256sum "$DB_PATH" | cut -d' ' -f1)
echo "Database: $DB_PATH"
echo "Size: $DB_SIZE bytes"
echo "SHA256: $DB_SHA"

mkdir -p "$CHUNK_DIR"
# Clear old chunks
rm -f "$CHUNK_DIR"/factum.db.gz.* "$CHUNK_DIR"/MANIFEST.json

echo "Compressing..."
gzip -c "$DB_PATH" > "$CHUNK_DIR/factum.db.gz"
GZ_SIZE=$(stat -c%s "$CHUNK_DIR/factum.db.gz")
GZ_SHA=$(sha256sum "$CHUNK_DIR/factum.db.gz" | cut -d' ' -f1)
echo "Compressed: $GZ_SIZE bytes"

echo "Splitting into ${CHUNK_SIZE} chunks..."
split -b "$CHUNK_SIZE" "$CHUNK_DIR/factum.db.gz" "$CHUNK_DIR/factum.db.gz."
rm "$CHUNK_DIR/factum.db.gz"  # remove the unsplit gzip

CHUNK_COUNT=$(ls "$CHUNK_DIR"/factum.db.gz.* | wc -l)
echo "Chunks: $CHUNK_COUNT"

# Build manifest
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
{
    echo "{"
    echo "  \"created_at\": \"$TIMESTAMP\","
    echo "  \"db_path\": \"data/.local/factum.db\","
    echo "  \"db_size\": $DB_SIZE,"
    echo "  \"db_sha256\": \"$DB_SHA\","
    echo "  \"gz_size\": $GZ_SIZE,"
    echo "  \"gz_sha256\": \"$GZ_SHA\","
    echo "  \"chunk_size\": \"$CHUNK_SIZE\","
    echo "  \"chunk_count\": $CHUNK_COUNT,"
    echo "  \"chunks\": ["
    first=1
    for chunk in "$CHUNK_DIR"/factum.db.gz.*; do
        name=$(basename "$chunk")
        size=$(stat -c%s "$chunk")
        sha=$(sha256sum "$chunk" | cut -d' ' -f1)
        if [[ $first -eq 1 ]]; then first=0; else echo ","; fi
        printf '    {"name": "%s", "size": %s, "sha256": "%s"}' "$name" "$size" "$sha"
    done
    echo ""
    echo "  ]"
    echo "}"
} > "$CHUNK_DIR/MANIFEST.json"

echo ""
echo "Done. Manifest: $CHUNK_DIR/MANIFEST.json"
echo "Commit with: git add backup/chunks/ && git commit"
