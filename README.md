# Driver Reservation System

Dự án bao gồm 2 phần: Client (Frontend) và Server (Backend).

## Cấu trúc dự án

- **Client**: Source code Frontend (Next.js)
- **Server**: Source code Backend (FastAPI)

## Hướng dẫn chạy

### 1. Server (Backend)

Yêu cầu: Python 3.8+, Docker, Make (optional).

1.  Di chuyển vào thư mục Server:
    ```bash
    cd Server
    ```

2.  Cài đặt dependencies:
    ```bash
    pip install -r requirements.txt
    # Hoặc nếu dùng make
    make install
    ```

3.  Khởi động Database (PostgreSQL):
    ```bash
    make up
    make reset       # Tạo database schema
    make master-data # Import dữ liệu mẫu
    ```

4.  Chạy Server:
    ```bash
    make run
    # Hoặc
    uvicorn main:app --reload
    ```

    Server sẽ chạy tại: [http://localhost:8000](http://localhost:8000)
    API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Client (Frontend)

Yêu cầu: Node.js, Yarn (khuyến nghị) hoặc NPM.

1.  Di chuyển vào thư mục Client:
    ```bash
    cd Client
    ```

2.  Cài đặt dependencies:
    ```bash
    yarn install
    # Hoặc
    npm install
    ```

3.  Chạy ứng dụng:
    ```bash
    yarn dev
    # Hoặc
    npm run dev
    ```

    Ứng dụng sẽ chạy tại: [http://localhost:3000](http://localhost:3000)
