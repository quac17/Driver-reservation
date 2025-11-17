.PHONY: install run test clean

# Cài đặt dependencies
install:
	pip install -r requirements.txt

# Xóa database (chỉ xóa container và volume, dữ liệu sẽ mất)
drop-db:
	docker-compose down -v

# Chạy server FastAPI ở chế độ dev
run:
	uvicorn main:app --reload

# Build Docker image
build-docker:
	docker build -t myapp .

# Chạy toàn bộ hệ thống bằng docker-compose
up:
	docker-compose up -d

# Dừng toàn bộ hệ thống docker-compose
down:
	docker-compose down -v

# Xem log các service docker-compose
logs:
	docker-compose logs -f

# Reset database: import init.sql
reset:
	./scripts/reset_db.sh
# Dump toàn bộ data ra file backup.sql
dump:
	./scripts/dump_db.sh
# Import dữ liệu master vào database
master-data:
	./scripts/master_data.sh