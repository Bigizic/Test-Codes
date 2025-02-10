#!/bin/bash

CONTAINER_NAME="mongodb"
DB_NAME="MY_DB"
AUTH_DB="admin"
BACKUP_PATH="./mongo_backup/backup"
LOCAL_BACKUP_DIR="./bck"


echo -n "Enter MongoDB user: "
read -s USERNAME
echo

echo -n "Enter MongoDB password: "
read -s PASSWORD
echo


# Create a dump in the container
docker exec $CONTAINER_NAME mongodump \
  --db=$DB_NAME \
  --username=$USERNAME \
  --password=$PASSWORD \
  --authenticationDatabase=$AUTH_DB \
  --out=$BACKUP_PATH

# Copy the dump to the local machine
docker cp $CONTAINER_NAME:$BACKUP_PATH $LOCAL_BACKUP_DIR

# Clean up the backup inside the container
docker exec $CONTAINER_NAME rm -r $BACKUP_PATH

echo "Backup completed and stored in $LOCAL_BACKUP_DIR"
