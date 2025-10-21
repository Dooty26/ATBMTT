-- Password Manager Database Schema
-- Tạo database và tables cho ứng dụng quản lý mật khẩu

-- Tạo database (nếu chưa có)
CREATE DATABASE IF NOT EXISTS quanly_matkhau CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Sử dụng database
USE quanly_matkhau;

-- Bảng users: Lưu thông tin người dùng
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,  -- SHA-256 hash
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng passwords: Lưu mật khẩu được mã hóa
CREATE TABLE IF NOT EXISTS passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    website VARCHAR(255) NOT NULL,
    username_field VARCHAR(255) NOT NULL,
    encrypted_password TEXT NOT NULL,  -- Mật khẩu được mã hóa AES
    salt VARCHAR(255) NOT NULL,        -- Salt cho mã hóa AES
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_website (website)
);

-- Thêm một số constraints bổ sung
ALTER TABLE users 
ADD CONSTRAINT chk_username_length CHECK (CHAR_LENGTH(username) >= 3),
ADD CONSTRAINT chk_username_format CHECK (username REGEXP '^[a-zA-Z0-9_]+$');

-- Tạo view để dễ dàng truy vấn
CREATE OR REPLACE VIEW user_password_summary AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(p.id) as total_passwords,
    MAX(p.updated_at) as last_password_update
FROM users u
LEFT JOIN passwords p ON u.id = p.user_id
GROUP BY u.id, u.username;

-- Hiển thị thông tin tables đã tạo
SHOW TABLES;
DESCRIBE users;
DESCRIBE passwords;