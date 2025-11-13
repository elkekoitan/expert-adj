#!/bin/bash
# ============================================================
# MT OPTIMIZER - DATABASE BACKUP SCRIPT
# ============================================================
# This script creates automated backups of PostgreSQL database
# Usage: ./scripts/backup.sh [daily|weekly|monthly]
# ============================================================

set -e

# Configuration
BACKUP_DIR="./backups"
POSTGRES_CONTAINER="mt-optimizer-db"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_TYPE=${1:-daily}

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR/$BACKUP_TYPE"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}MT Optimizer Database Backup${NC}"
echo -e "${GREEN}======================================${NC}"
echo -e "Backup Type: ${YELLOW}$BACKUP_TYPE${NC}"
echo -e "Timestamp: ${YELLOW}$TIMESTAMP${NC}"

# Load environment variables
if [ -f .env.prod ]; then
    source .env.prod
else
    echo -e "${RED}Error: .env.prod file not found!${NC}"
    exit 1
fi

# Backup filename
BACKUP_FILE="$BACKUP_DIR/$BACKUP_TYPE/mt_optimizer_${BACKUP_TYPE}_${TIMESTAMP}.sql"
BACKUP_FILE_GZ="${BACKUP_FILE}.gz"

echo -e "\n${YELLOW}Creating database backup...${NC}"

# Create backup using pg_dump
docker exec -t $POSTGRES_CONTAINER pg_dump -U $POSTGRES_USER -d $POSTGRES_DB \
    --clean \
    --if-exists \
    --create \
    --no-owner \
    --no-acl \
    > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database dump created successfully${NC}"

    # Compress the backup
    echo -e "${YELLOW}Compressing backup...${NC}"
    gzip "$BACKUP_FILE"

    if [ $? -eq 0 ]; then
        BACKUP_SIZE=$(du -h "$BACKUP_FILE_GZ" | cut -f1)
        echo -e "${GREEN}✓ Backup compressed successfully${NC}"
        echo -e "Backup size: ${YELLOW}$BACKUP_SIZE${NC}"
        echo -e "Backup location: ${YELLOW}$BACKUP_FILE_GZ${NC}"
    else
        echo -e "${RED}✗ Failed to compress backup${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Failed to create database backup${NC}"
    exit 1
fi

# Cleanup old backups based on retention policy
echo -e "\n${YELLOW}Cleaning up old backups...${NC}"

case $BACKUP_TYPE in
    daily)
        RETENTION_DAYS=7
        ;;
    weekly)
        RETENTION_DAYS=30
        ;;
    monthly)
        RETENTION_DAYS=365
        ;;
    *)
        RETENTION_DAYS=7
        ;;
esac

# Remove backups older than retention period
find "$BACKUP_DIR/$BACKUP_TYPE" -name "*.gz" -type f -mtime +$RETENTION_DAYS -delete

REMAINING_BACKUPS=$(find "$BACKUP_DIR/$BACKUP_TYPE" -name "*.gz" -type f | wc -l)
echo -e "${GREEN}✓ Cleanup completed${NC}"
echo -e "Retention: ${YELLOW}$RETENTION_DAYS days${NC}"
echo -e "Remaining backups: ${YELLOW}$REMAINING_BACKUPS${NC}"

# Optional: Backup to cloud storage (S3/MinIO)
if [ "$BACKUP_TO_S3" = "true" ]; then
    echo -e "\n${YELLOW}Uploading to S3/MinIO...${NC}"
    # Add your S3/MinIO upload command here
    # Example: aws s3 cp "$BACKUP_FILE_GZ" s3://your-bucket/backups/
fi

echo -e "\n${GREEN}======================================${NC}"
echo -e "${GREEN}Backup completed successfully!${NC}"
echo -e "${GREEN}======================================${NC}"

# Log backup completion
echo "$(date): Backup completed - $BACKUP_FILE_GZ" >> "$BACKUP_DIR/backup.log"
