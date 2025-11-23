# Drive Coach Reservation API

API hệ thống đặt hẹn thầy dạy lái xe và xe tập lái sử dụng FastAPI và SQLAlchemy.

## Yêu cầu hệ thống

Trước khi bắt đầu, đảm bảo máy tính của bạn đã cài đặt:

- **Python** 3.8 trở lên
- **Docker** và **Docker Compose** (để chạy PostgreSQL)
- **Make** (tùy chọn nhưng khuyến nghị - để sử dụng Makefile)
  - Trên Windows: Cài đặt Make qua Chocolatey hoặc sử dụng Git Bash/WSL
  - Trên Linux/Mac: Thường đã có sẵn hoặc cài qua package manager

## Cài đặt và Chạy Project

### Bước 1: Clone repository

```bash
git clone <repository-url>
cd Driver-reservation
```

### Bước 2: Cài đặt dependencies

**Sử dụng Makefile (Khuyến nghị):**
```bash
make install
```

**Hoặc thủ công:**
```bash
pip install -r requirements.txt
```

### Bước 3: Khởi động Database

**Sử dụng Makefile (Khuyến nghị):**
```bash
make up          # Khởi động PostgreSQL container
make reset       # Reset và tạo database schema
make master-data # Thêm dữ liệu mẫu (users, mentors, cars)
```

**Hoặc thủ công:**
```bash
# Khởi động PostgreSQL
docker-compose up -d db

# Đợi vài giây để database khởi động, sau đó tạo schema
docker-compose exec -T db psql -U postgres -d drive_coach < db/init.sql

# Thêm dữ liệu mẫu (tùy chọn)
docker-compose exec -T db psql -U postgres -d drive_coach < db/data-init.sql
```

> **Lưu ý:** Trên Windows PowerShell, sử dụng:
> ```powershell
> Get-Content db/init.sql | docker-compose exec -T db psql -U postgres -d drive_coach
> Get-Content db/data-init.sql | docker-compose exec -T db psql -U postgres -d drive_coach
> ```

### Bước 4: Cấu hình môi trường (Nếu cần)

Tạo file `.env` trong thư mục gốc (nếu chưa có):

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/drive_coach
SECRET_KEY=your-secret-key-here
```

Hoặc cấu hình trực tiếp trong file `database.py` nếu cần.

### Bước 5: Chạy ứng dụng

**Sử dụng Makefile:**
```bash
make run
```

**Hoặc thủ công:**
```bash
# Cách 1: Sử dụng uvicorn trực tiếp
uvicorn main:app --reload

# Cách 2: Chạy file main.py
python main.py
```

Ứng dụng sẽ chạy tại: **http://localhost:8000**

### Bước 6: Chạy Unit Tests

Để chạy các unit test cho hệ thống (ví dụ: authentication flow):

**Sử dụng Makefile:**
```bash
make test
```

**Hoặc thủ công:**
```bash
pytest
```

### Truy cập API Documentation

Sau khi server khởi động, truy cập:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Hướng dẫn Setup Database (Chi tiết)

Phần này cung cấp hướng dẫn chi tiết về setup database. Nếu đã hoàn thành các bước ở phần [Cài đặt và Chạy Project](#cài-đặt-và-chạy-project), bạn có thể bỏ qua phần này.

### Các lệnh Makefile hữu ích

```bash
make up          # Khởi động toàn bộ hệ thống (database, redis)
make down        # Dừng và xóa toàn bộ hệ thống (kèm volume)
make drop-db     # Xóa database container và volume
make reset       # Reset database: xóa bảng cũ và tạo lại schema
make master-data # Import dữ liệu mẫu vào database
make dump        # Backup database ra file db/init.sql
make logs        # Xem log các service
```

### Hướng dẫn thủ công (Tham khảo)

#### Yêu cầu
- Docker và Docker Compose đã được cài đặt
- PostgreSQL client (psql) - tùy chọn, để kiểm tra database

#### Các bước setup Database

##### 1. Khởi động PostgreSQL bằng Docker

Khởi động container PostgreSQL:
```bash
docker-compose up -d db
```

Kiểm tra container đang chạy:
```bash
docker-compose ps
```

##### 2. Kết nối vào PostgreSQL

Có thể kết nối vào database bằng một trong các cách sau:

**Cách 1: Sử dụng Docker exec**
```bash
docker-compose exec db psql -U postgres -d drive_coach
```

**Cách 2: Sử dụng psql từ máy local**
```bash
psql -h localhost -p 5432 -U postgres -d drive_coach
```
Password mặc định: `postgres`

##### 3. Tạo Database Schema

**Sử dụng Makefile (Khuyến nghị):**
```bash
make reset  # Tự động reset và tạo schema từ init.sql
```

**Thủ công: Sử dụng file init.sql**

**Trên Linux/Mac:**
```bash
docker-compose exec -T db psql -U postgres -d drive_coach < db/init.sql
```

**Trên Windows PowerShell:**
```powershell
Get-Content db/init.sql | docker-compose exec -T db psql -U postgres -d drive_coach
```

**Hoặc copy file vào container rồi chạy:**
```bash
# Tìm tên container: docker-compose ps
docker cp db/init.sql <container_name>:/tmp/init.sql
docker-compose exec db psql -U postgres -d drive_coach -f /tmp/init.sql
```

**Nếu đã kết nối vào PostgreSQL:**
```sql
\i /path/to/db/init.sql
```

**Tùy chọn: Sử dụng SQLAlchemy models (Auto-create)**

Nếu ứng dụng được cấu hình để tự động tạo bảng từ models:
```bash
python -c "from models import Base; from database import engine; Base.metadata.create_all(bind=engine)"
```

##### 4. Thêm dữ liệu mẫu (Tùy chọn)

**Sử dụng Makefile (Khuyến nghị):**
```bash
make master-data  # Tự động import dữ liệu mẫu
```

**Thủ công: Import dữ liệu mẫu (users, mentors, cars)**

**Trên Linux/Mac:**
```bash
docker-compose exec -T db psql -U postgres -d drive_coach < db/data-init.sql
```

**Trên Windows PowerShell:**
```powershell
Get-Content db/data-init.sql | docker-compose exec -T db psql -U postgres -d drive_coach
```

**Hoặc copy file vào container rồi chạy:**
```bash
# Tìm tên container: docker-compose ps
docker cp db/data-init.sql <container_name>:/tmp/data-init.sql
docker-compose exec db psql -U postgres -d drive_coach -f /tmp/data-init.sql
```

**Nếu đã kết nối vào PostgreSQL:**
```sql
\i /path/to/db/data-init.sql
```

##### 5. Kiểm tra Database

Kiểm tra các bảng đã được tạo:
```sql
\dt
```

Kiểm tra dữ liệu:
```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM mentors;
SELECT COUNT(*) FROM cars;
```

### Cấu hình Database Connection

Cấu hình kết nối database trong file `.env` hoặc biến môi trường:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/drive_coach
```

Hoặc thay đổi trong file `database.py` nếu cần.

### Reset Database (Nếu cần)

**Khuyến nghị: Sử dụng Makefile**
```bash
make reset       # Reset database và tạo lại schema
make master-data # Thêm lại dữ liệu mẫu (nếu cần)
```

**Hoặc xóa hoàn toàn và tạo lại:**
```bash
make drop-db     # Xóa container và volume
make up          # Khởi động lại database
make reset       # Tạo lại schema
make master-data # Thêm dữ liệu mẫu
```

**Thủ công: Sử dụng prepare.sql**

**Trên Linux/Mac:**
```bash
docker-compose exec -T db psql -U postgres -d drive_coach < db/prepare.sql
docker-compose exec -T db psql -U postgres -d drive_coach < db/init.sql
docker-compose exec -T db psql -U postgres -d drive_coach < db/data-init.sql
```

**Trên Windows PowerShell:**
```powershell
Get-Content db/prepare.sql | docker-compose exec -T db psql -U postgres -d drive_coach
Get-Content db/init.sql | docker-compose exec -T db psql -U postgres -d drive_coach
Get-Content db/data-init.sql | docker-compose exec -T db psql -U postgres -d drive_coach
```

**Xóa và tạo lại container:**
```bash
docker-compose down -v
docker-compose up -d db
# Sau đó chạy lại các bước 3 và 4
# Hoặc: make drop-db && make up && make reset && make master-data
```

### Thông tin Database

- **Host**: localhost
- **Port**: 5432
- **Database**: drive_coach
- **Username**: postgres
- **Password**: postgres
- **PostgreSQL Version**: 15

### Backup và Restore Database

**Backup database (Sử dụng Makefile):**
```bash
make dump  # Backup database ra file db/init.sql
```

**Backup database (Thủ công):**
- **Linux/Mac:** `docker-compose exec db pg_dump -U postgres drive_coach > backup.sql`
- **Windows PowerShell:** `docker-compose exec db pg_dump -U postgres drive_coach | Out-File -Encoding utf8 backup.sql`

**Restore database:**
- **Linux/Mac:** `docker-compose exec -T db psql -U postgres drive_coach < backup.sql`
- **Windows PowerShell:** `Get-Content backup.sql | docker-compose exec -T db psql -U postgres drive_coach`

### Lưu ý

- Đảm bảo port 5432 không bị chiếm dụng bởi ứng dụng khác
- Dữ liệu sẽ được lưu trong Docker volume `pgdata`
- Khuyến nghị sử dụng Makefile để đơn giản hóa các thao tác với database
- Trên Windows, cần cài đặt Git Bash hoặc WSL để chạy các script `.sh` trong Makefile
- Nếu gặp lỗi với script trên Windows, có thể chạy các lệnh thủ công như hướng dẫn ở trên

## API Endpoints

### Authentication

#### Đăng nhập (Login)
```
POST /authen/login
Content-Type: application/x-www-form-urlencoded

username=user1&password=123456
```
**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "message": {
    "loginData": {
      "username": "user1",
      "name": "Nguyễn Văn A",
      "isMentor": false,
      "email": "user1@example.com",
      "phone": "0901234567"
    }
  }
}
```

#### Đăng xuất (Logout)
```
POST /authen/logout
Authorization: Bearer <access_token>
```

#### Làm mới token (Reset token)
```
POST /authen/reset-token
Authorization: Bearer <access_token>
```

### Users

#### Lấy tất cả users
```
GET /user/
Authorization: Bearer <access_token>
```

#### Lấy user theo ID
```
GET /user/{user_id}
Authorization: Bearer <access_token>
```

#### Tạo user mới
```
POST /user/
Content-Type: application/json

{
  "username": "user1",
  "name": "Nguyễn Văn A",
  "password": "123456",
  "email": "user1@example.com",
  "phone": "0901234567",
  "address": "123 Đường ABC, Quận 1, TP.HCM"
}
```

#### Cập nhật user
```
PUT /user/{user_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Nguyễn Văn A Updated",
  "email": "newemail@example.com",
  "phone": "0901234568"
}
```

#### Xóa user (soft delete)
```
DELETE /user/{user_id}
Authorization: Bearer <access_token>
```

### Mentors

#### Lấy danh sách mentors
```
GET /mentor/
```

#### Lấy mentor theo ID
```
GET /mentor/{mentor_id}
```

### Cars

#### Lấy danh sách cars
```
GET /car/
GET /car/?status=available
```

#### Lấy car theo ID
```
GET /car/{car_id}
```

### Reserves (Đặt lịch hẹn)

#### Lấy danh sách reserves
```
GET /reserve/
GET /reserve/?status=pending
GET /reserve/?user_id=1
GET /reserve/?mentor_id=1
Authorization: Bearer <access_token>
```
- User chỉ xem được reserves của chính mình
- Mentor chỉ xem được reserves của chính mình

#### Lấy reserve theo ID
```
GET /reserve/{reserve_id}
Authorization: Bearer <access_token>
```

#### Đặt lịch hẹn
```
POST /reserve/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user_id": 1,
  "mentor_id": 1,
  "car_id": 1,
  "status": "pending",
  "reserve_details": [
    {
      "start_time": "2025-01-25T08:00:00+00:00",
      "end_time": "2025-01-25T10:00:00+00:00",
      "price": 500000,
      "notes": "Học buổi sáng",
      "status": "pending"
    },
    {
      "start_time": "2025-01-26T14:00:00+00:00",
      "end_time": "2025-01-26T16:00:00+00:00",
      "price": 500000,
      "notes": "Học buổi chiều",
      "status": "pending"
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "mentor_id": 1,
  "car_id": 1,
  "status": "pending",
  "createdAt": "2025-01-25T07:00:00+00:00",
  "updatedAt": "2025-01-25T07:00:00+00:00",
  "reserve_details": [
    {
      "id": 1,
      "reserve_id": 1,
      "start_time": "2025-01-25T08:00:00+00:00",
      "end_time": "2025-01-25T10:00:00+00:00",
      "price": 500000,
      "notes": "Học buổi sáng",
      "status": "pending",
      "createdAt": "2025-01-25T07:00:00+00:00",
      "updatedAt": "2025-01-25T07:00:00+00:00"
    }
  ]
}
```

## Cấu trúc Project

```
DriveCoachReservation/
├── main.py              # FastAPI app chính
├── database.py          # Cấu hình database connection
├── models.py            # SQLAlchemy models (User, Mentor, Car, Reserve, ReserveDetail)
├── schemas.py           # Pydantic schemas cho API
├── routers/             # API routers
│   ├── __init__.py
│   ├── authen.py        # Authentication endpoints
│   ├── user.py          # User API endpoints
│   ├── mentor.py        # Mentor API endpoints
│   ├── car.py           # Car API endpoints
│   └── reserve.py       # Reserve API endpoints
├── requirements.txt     # Dependencies
├── docker-compose.yml   # Docker setup
├── Dockerfile          # Docker image
├── Makefile            # Lệnh tiện ích
├── db/                 # Database scripts
│   ├── init.sql        # Database schema
│   ├── prepare.sql     # Drop tables script
│   └── data-init.sql   # Initial data
└── scripts/            # Utility scripts
```

## Database Schema

### Users
- Khách hàng đặt hẹn
- Fields: id, username, password, name, email, phone, address, isActive, createdAt, updatedAt

### Mentors
- Thầy dạy lái xe
- Fields: id, username, password, name, email, phone, license_number, experience_years, isActive, createdAt, updatedAt

### Cars
- Xe tập lái
- Fields: id, license_plate, brand, model, color, year, status, isActive, createdAt, updatedAt
- Status: available, busy, maintenance

### Reserves
- Đặt hẹn
- Fields: id, user_id, mentor_id, car_id, status, createdAt, updatedAt
- Status: pending, confirmed, cancelled, completed

### Reserve Details
- Chi tiết đặt hẹn (thời gian cụ thể)
- Fields: id, reserve_id, start_time, end_time, price, notes, status, createdAt, updatedAt
- Status: pending, confirmed, cancelled, completed

## Tính năng

- ✅ REST API với FastAPI
- ✅ Authentication với JWT (hỗ trợ User và Mentor)
- ✅ CRUD operations cho User
- ✅ GET operations cho Mentor, Car, Reserve
- ✅ Đặt lịch hẹn với kiểm tra xung đột thời gian
- ✅ Validation với Pydantic
- ✅ Database với SQLAlchemy + PostgreSQL
- ✅ Error handling
- ✅ Auto-generated API docs tại `/docs`
- ✅ Phân quyền: User chỉ xem reserves của chính mình
- ✅ Timestamp fields (createdAt, updatedAt)

## Flow đặt hẹn cho UI

Flow này mô tả các bước mà UI cần thực hiện để hoàn thành quá trình đặt hẹn với thầy dạy lái xe.

### Bước 1: Đăng nhập (User)

**API:** `POST /authen/login`

- User cần đăng nhập để lấy `access_token`
- Lưu `access_token` vào localStorage/sessionStorage để sử dụng cho các API tiếp theo
- Lưu thông tin user từ `message.loginData` (bao gồm `user_id`)

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "message": {
    "loginData": {
      "username": "user1",
      "name": "Nguyễn Văn A",
      "isMentor": false,
      "email": "user1@example.com",
      "phone": "0901234567"
    }
  }
}
```

### Bước 2: Lấy danh sách Mentors

**API:** `GET /mentor/`

- Không cần authentication
- Hiển thị danh sách mentors để user chọn
- Hiển thị thông tin: tên, email, số điện thoại, số năm kinh nghiệm, số bằng lái

**Response:**
```json
[
  {
    "id": 1,
    "name": "Trần Văn B",
    "email": "mentor1@example.com",
    "phone": "0912345678",
    "license_number": "DL-123456",
    "experience_years": 5
  }
]
```

### Bước 3: Lấy danh sách Cars (Available)

**API:** `GET /car/?status=available`

- Không cần authentication
- Chỉ lấy các xe có status = "available" để đảm bảo có thể đặt lịch
- Hiển thị thông tin: biển số, hãng, model, màu sắc, năm sản xuất

**Response:**
```json
[
  {
    "id": 1,
    "license_plate": "30A-12345",
    "brand": "Toyota",
    "model": "Vios",
    "color": "Trắng",
    "year": 2023,
    "status": "available"
  }
]
```

### Bước 4: Tạo Reserve (Đặt lịch hẹn)

**API:** `POST /reserve/`

- **Cần authentication:** Header `Authorization: Bearer <access_token>`
- User chọn:
  - `mentor_id`: ID của mentor đã chọn ở bước 2
  - `car_id`: ID của xe đã chọn ở bước 3
  - `user_id`: Lấy từ thông tin user đã đăng nhập (bước 1)
- Tạo danh sách `reserve_details` với các buổi học:
  - `start_time`: Thời gian bắt đầu (ISO 8601 format với timezone)
  - `end_time`: Thời gian kết thúc (phải sau start_time)
  - `price`: Giá tiền cho mỗi buổi học
  - `notes`: Ghi chú (tùy chọn)
  - `status`: "pending" (mặc định)

**Request Body:**
```json
{
  "user_id": 1,
  "mentor_id": 1,
  "car_id": 1,
  "status": "pending",
  "reserve_details": [
    {
      "start_time": "2025-01-25T08:00:00+00:00",
      "end_time": "2025-01-25T10:00:00+00:00",
      "price": 500000,
      "notes": "Học buổi sáng",
      "status": "pending"
    },
    {
      "start_time": "2025-01-26T14:00:00+00:00",
      "end_time": "2025-01-26T16:00:00+00:00",
      "price": 500000,
      "notes": "Học buổi chiều",
      "status": "pending"
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "mentor_id": 1,
  "car_id": 1,
  "status": "pending",
  "createdAt": "2025-01-25T07:00:00+00:00",
  "updatedAt": "2025-01-25T07:00:00+00:00",
  "reserve_details": [
    {
      "id": 1,
      "reserve_id": 1,
      "start_time": "2025-01-25T08:00:00+00:00",
      "end_time": "2025-01-25T10:00:00+00:00",
      "price": 500000,
      "notes": "Học buổi sáng",
      "status": "pending"
    }
  ]
}
```

**Lưu ý:**
- Hệ thống sẽ tự động kiểm tra xung đột thời gian
- Nếu có xung đột, API sẽ trả về lỗi
- Car phải có status = "available" mới có thể đặt lịch
- User chỉ có thể đặt lịch cho chính mình (user_id phải khớp với user đang đăng nhập)

### Bước 5: Xem danh sách Reserves của User

**API:** `GET /reserve/`

- **Cần authentication:** Header `Authorization: Bearer <access_token>`
- User chỉ xem được reserves của chính mình
- Có thể filter theo status: `GET /reserve/?status=pending`

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "mentor_id": 1,
    "car_id": 1,
    "status": "pending",
    "createdAt": "2025-01-25T07:00:00+00:00",
    "reserve_details": [...]
  }
]
```

### Bước 6: Xem chi tiết Reserve

**API:** `GET /reserve/{reserve_id}`

- **Cần authentication:** Header `Authorization: Bearer <access_token>`
- Xem thông tin chi tiết của một reserve cụ thể
- Bao gồm tất cả reserve_details (các buổi học)

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "mentor_id": 1,
  "car_id": 1,
  "status": "pending",
  "createdAt": "2025-01-25T07:00:00+00:00",
  "updatedAt": "2025-01-25T07:00:00+00:00",
  "reserve_details": [
    {
      "id": 1,
      "reserve_id": 1,
      "start_time": "2025-01-25T08:00:00+00:00",
      "end_time": "2025-01-25T10:00:00+00:00",
      "price": 500000,
      "notes": "Học buổi sáng",
      "status": "pending"
    }
  ]
}
```

### Tóm tắt Flow

```
1. User đăng nhập → Lấy access_token và user_id
2. Lấy danh sách mentors → Hiển thị cho user chọn
3. Lấy danh sách cars (available) → Hiển thị cho user chọn
4. User điền form đặt hẹn:
   - Chọn mentor
   - Chọn car
   - Nhập thông tin các buổi học (start_time, end_time, price, notes)
5. Gửi POST /reserve/ → Tạo reserve
6. Hiển thị danh sách reserves của user
7. User có thể xem chi tiết từng reserve
```

### Xử lý lỗi trong UI

- **401 Unauthorized:** Token hết hạn hoặc không hợp lệ → Yêu cầu user đăng nhập lại
- **400 Bad Request:** Dữ liệu không hợp lệ (xung đột thời gian, car không available) → Hiển thị thông báo lỗi cụ thể
- **403 Forbidden:** User không có quyền truy cập → Chuyển về trang đăng nhập
- **404 Not Found:** Resource không tồn tại → Hiển thị thông báo không tìm thấy

## Lưu ý quan trọng

- Tất cả API cần authentication (trừ POST /user/ và GET /mentor/, GET /car/)
- Chỉ User mới có thể đặt lịch hẹn
- Hệ thống tự động kiểm tra xung đột thời gian khi đặt lịch
- Car phải có status = "available" mới có thể đặt lịch
