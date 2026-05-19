#!/usr/bin/env bash
set -euo pipefail

# Backup script – tars a directory and rotates old backups.
SOURCE_DIR="${1:?Usage: $0 /path/to/source}"
BACKUP_DIR="./backups"
RETENTION_COUNT=5

mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

echo "Creating backup: $ARCHIVE"
tar -czf "$ARCHIVE" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"

# Rotation – keep only the newest $RETENTION_COUNT files
cd "$BACKUP_DIR"
ls -t backup_*.tar.gz | tail -n +$((RETENTION_COUNT+1)) | xargs -r rm
echo "Rotation complete, keeping last $RETENTION_COUNT backups."