-- Data Master cho hệ thống đặt hẹn thầy dạy lái xe và xe tập lái
-- Tạo dữ liệu mẫu cho users, mentors, cars

-- Xóa dữ liệu cũ (nếu có)
DELETE FROM reserve_details WHERE id > 0;
DELETE FROM reserves WHERE id > 0;
DELETE FROM cars WHERE id > 0;
DELETE FROM mentors WHERE id > 0;
DELETE FROM users WHERE id > 0;

-- Reset sequences
ALTER SEQUENCE users_id_seq RESTART WITH 1;
ALTER SEQUENCE mentors_id_seq RESTART WITH 1;
ALTER SEQUENCE cars_id_seq RESTART WITH 1;
ALTER SEQUENCE reserves_id_seq RESTART WITH 1;
ALTER SEQUENCE reserve_details_id_seq RESTART WITH 1;

-- Thêm dữ liệu master cho users
INSERT INTO users ("username", "name", "password", "email", "phone", "address", "isActive") VALUES
('user1', 'Nguyễn Văn A', '123456', 'user1@example.com', '0901234567', '123 Đường ABC, Quận 1, TP.HCM', true),
('user2', 'Trần Thị B', '123456', 'user2@example.com', '0901234568', '456 Đường XYZ, Quận 2, TP.HCM', true),
('user3', 'Lê Văn C', '123456', 'user3@example.com', '0901234569', '789 Đường DEF, Quận 3, TP.HCM', true);

-- Thêm dữ liệu master cho mentors
INSERT INTO mentors ("username", "name", "password", "email", "phone", "license_number", "experience_years", "price_per_hour", "isActive") VALUES
('mentor1', 'Trần Văn B', '123456', 'mentor1@example.com', '0912345678', 'DL-123456', 5, 200000, true),
('mentor2', 'Nguyễn Thị C', '123456', 'mentor2@example.com', '0912345679', 'DL-123457', 8, 250000, true),
('mentor3', 'Lê Văn D', '123456', 'mentor3@example.com', '0912345680', 'DL-123458', 3, 180000, true);

-- Thêm dữ liệu master cho cars
INSERT INTO cars ("license_plate", "brand", "model", "color", "year", "status", "price_per_hour", "isActive") VALUES
('30A-12345', 'Toyota', 'Vios', 'Trắng', 2023, 'available', 150000, true),
('30A-12346', 'Honda', 'City', 'Đen', 2022, 'available', 180000, true),
('30A-12347', 'Mazda', 'Mazda3', 'Xám', 2024, 'available', 200000, true);

-- Hiển thị kết quả
SELECT 'Đã thêm ' || COUNT(*) || ' users vào database' as result FROM users;
SELECT 'Đã thêm ' || COUNT(*) || ' mentors vào database' as result FROM mentors;
SELECT 'Đã thêm ' || COUNT(*) || ' cars vào database' as result FROM cars;
