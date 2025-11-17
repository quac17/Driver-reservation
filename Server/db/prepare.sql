-- Xóa các constraint, index, sequence liên quan đến các bảng cũ nếu tồn tại
DROP TABLE IF EXISTS reserve_details CASCADE;
DROP SEQUENCE IF EXISTS reserve_details_id_seq CASCADE;

DROP TABLE IF EXISTS reserves CASCADE;
DROP SEQUENCE IF EXISTS reserves_id_seq CASCADE;

DROP TABLE IF EXISTS cars CASCADE;
DROP SEQUENCE IF EXISTS cars_id_seq CASCADE;

DROP TABLE IF EXISTS mentors CASCADE;
DROP SEQUENCE IF EXISTS mentors_id_seq CASCADE;

DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_id_seq CASCADE;
DROP INDEX IF EXISTS users_username_key CASCADE;
