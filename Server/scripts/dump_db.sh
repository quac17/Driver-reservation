#!/bin/bash
set -e

CONTAINER_ID=$(docker-compose ps -q db)
echo "[1] Dump toàn bộ data ra file init.sql từ container $CONTAINER_ID..."
docker exec -t $CONTAINER_ID pg_dump -U postgres -d drive_coach > db/init.sql
echo "[2] Đã dump xong vào file init.sql!" 