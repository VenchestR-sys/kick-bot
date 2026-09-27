#!/bin/bash
set -euo pipefail

PROJECT_DIR="/opt/kick"
DB_FILE="$PROJECT_DIR/data/kick.db"
BACKUP_DIR="$PROJECT_DIR/data/backup"
LOG_FILE="$PROJECT_DIR/logs/backup.log"
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR" "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/kick_$TIMESTAMP.db"

sqlite3 "$DB_FILE" ".backup '$BACKUP_FILE'"

INTEGRITY=$(sqlite3 "$BACKUP_FILE" "PRAGMA integrity_check;")
if [ "$INTEGRITY" != "ok" ]; then
    echo "[$TIMESTAMP] BACKUP CORRUPTED: $INTEGRITY" >> "$LOG_FILE"
    exit 1
fi

gzip -f "$BACKUP_FILE"
find "$BACKUP_DIR" -name "kick_*.db.gz" -mtime +$RETENTION_DAYS -delete

SIZE=$(du -h "$BACKUP_FILE.gz" | cut -f1)
echo "[$TIMESTAMP] Backup: $(basename "$BACKUP_FILE.gz") ($SIZE)" >> "$LOG_FILE"
