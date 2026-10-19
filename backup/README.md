# Database Backup

Scripts to zip, chunk, and restore the local Factum database (`data/.local/factum.db`).

GitHub rejects files over 100MB. The database is ~1GB, so we gzip it and
split into 50MB chunks that can be committed.

## Backup

```bash
./backup/backup-db.sh
```

This:
1. Gzips `data/.local/factum.db`
2. Splits into 50MB chunks in `backup/chunks/`
3. Writes `backup/chunks/MANIFEST.json` with hashes and metadata

Then commit:
```bash
git add backup/chunks/
git commit -m "Database backup <date>"
git push origin main
```

## Restore (Deflate)

```bash
./backup/restore-db.sh [--force]
```

This:
1. Verifies every chunk's SHA256 against the manifest
2. Reassembles the gzip and verifies its hash
3. Decompresses to `data/.local/factum.db`
4. Verifies the final database hash

Without `--force`, refuses to overwrite an existing database.
With `--force`, backs up the existing DB first.

After restore, run `factum rebuild` before using match/search.

## Files

| File | Purpose |
|------|---------|
| `backup-db.sh` | Zip + chunk the database |
| `restore-db.sh` | Verify + reassemble + decompress (deflate) |
| `chunks/` | Gzipped 50MB chunks + MANIFEST.json (git-tracked) |

## Notes

- Chunks are deterministic: same DB bytes → same chunks → same hashes.
- The manifest records the source DB's SHA256, so restore verifies end-to-end.
- `data/.local/` is git-ignored; `backup/chunks/` is the git-tracked copy.
