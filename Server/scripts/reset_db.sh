#!/bin/bash
set -e

CONTAINER_ID=$(docker-compose ps -q db)
echo "[1] Copy file prepare.sql vào container $CONTAINER_ID..."
docker cp db/prepare.sql $CONTAINER_ID:/prepare.sql

echo "[2] Chạy prepare.sql để dọn sạch DB..."
docker exec -i $CONTAINER_ID psql -U postgres -d drive_coach -f ./prepare.sql

echo "[3] Import dữ liệu từ init.sql vào DB..."
cat db/init.sql | docker exec -i $CONTAINER_ID psql -U postgres -d drive_coach

echo "[4] Đã reset xong database!" 