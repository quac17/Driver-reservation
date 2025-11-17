#!/bin/bash
set -e

CONTAINER_ID=$(docker-compose ps -q db)
echo "[1] Copy file data-init.sql vào container $CONTAINER_ID..."
docker cp ./db/data-init.sql $CONTAINER_ID:/data-init.sql

echo "[2] Import dữ liệu master từ data-init.sql vào DB..."
docker exec -i $CONTAINER_ID psql -U postgres -d drive_coach -f ./data-init.sql

echo "[3] Đã import xong dữ liệu master!" 