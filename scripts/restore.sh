#!/bin/bash
# ============================================================
# MT OPTIMIZER - DATABASE RESTORE SCRIPT
# ============================================================
# This script restores PostgreSQL database from backup
# Usage: ./scripts/restore.sh <backup_file.sql.gz>
# ============================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backup file is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Backup file not specified!${NC}"
    echo "Usage: ./scripts/restore.sh <backup_file.sql.gz>"
    echo "Example: ./scripts/restore.sh ./backups/daily/mt_optimizer_daily_20250113_120000.sql.gz"
    exit 1
fi

BACKUP_FILE=$1

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}Error: Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

echo -e "${RED}======================================${NC}"
echo -e "${RED}⚠️  DATABASE RESTORE WARNING ⚠️${NC}"
echo -e "${RED}======================================${NC}"
echo -e "${YELLOW}This will COMPLETELY REPLACE the current database!${NC}"
echo -e "${YELLOW}All existing data will be lost!${NC}"
echo -e "Backup file: ${YELLOW}$BACKUP_FILE${NC}"
echo ""
read -p "Are you sure you want to continue? (type 'YES' to confirm): " CONFIRM

if [ "$CONFIRM" != "YES" ]; then
    echo -e "${YELLOW}Restore cancelled.${NC}"
    exit 0
fi

# Load environment variables
if [ -f .env.prod ]; then
    source .env.prod
else
    echo -e "${RED}Error: .env.prod file not found!${NC}"
    exit 1
fi

POSTGRES_CONTAINER="mt-optimizer-db"
TEMP_FILE="/tmp/restore_$(date +%s).sql"

echo -e "\n${YELLOW}Preparing restore...${NC}"

# Decompress backup file
echo -e "${YELLOW}Decompressing backup...${NC}"
gunzip -c "$BACKUP_FILE" > "$TEMP_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backup decompressed successfully${NC}"
else
    echo -e "${RED}✗ Failed to decompress backup${NC}"
    rm -f "$TEMP_FILE"
    exit 1
fi

# Stop dependent services
echo -e "\n${YELLOW}Stopping dependent services...${NC}"
docker-compose -f docker-compose.prod.yml stop api celery-worker flower runner

# Restore database
echo -e "\n${YELLOW}Restoring database...${NC}"
docker exec -i $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d postgres < "$TEMP_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database restored successfully${NC}"

    # Cleanup temp file
    rm -f "$TEMP_FILE"

    # Restart services
    echo -e "\n${YELLOW}Restarting services...${NC}"
    docker-compose -f docker-compose.prod.yml start api celery-worker flower runner

    echo -e "\n${GREEN}======================================${NC}"
    echo -e "${GREEN}Restore completed successfully!${NC}"
    echo -e "${GREEN}======================================${NC}"

    # Log restore completion
    mkdir -p backups
    echo "$(date): Database restored from $BACKUP_FILE" >> backups/restore.log
else
    echo -e "${RED}✗ Failed to restore database${NC}"
    rm -f "$TEMP_FILE"

    # Restart services anyway
    echo -e "\n${YELLOW}Restarting services...${NC}"
    docker-compose -f docker-compose.prod.yml start api celery-worker flower runner

    exit 1
fi
