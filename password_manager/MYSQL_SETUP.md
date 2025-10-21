# Hướng dẫn thiết lập MySQL cho Password Manager

## 1. Cài đặt MySQL

### Windows:
1. Tải MySQL Community Server từ: https://dev.mysql.com/downloads/mysql/
2. Chạy file cài đặt và làm theo hướng dẫn
3. Ghi nhớ mật khẩu root đã đặt

### macOS:
```bash
brew install mysql
brew services start mysql
```

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

## 2. Thiết lập Database

### Bước 1: Đăng nhập MySQL
```bash
mysql -u root -p
```

### Bước 2: Tạo database và user (tùy chọn)
```sql
-- Tạo database
CREATE DATABASE quanly_matkhau CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tạo user riêng (tùy chọn, có thể dùng root)
CREATE USER 'password_user'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON quanly_matkhau.* TO 'password_user'@'localhost';
FLUSH PRIVILEGES;

-- Thoát MySQL
EXIT;
```

### Bước 3: Chạy script tạo bảng
```bash
mysql -u root -p quanly_matkhau < database/schema.sql
```

## 3. Cấu hình ứng dụng

### Bước 1: Cập nhật file .env
Chỉnh sửa file `backend/.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root                    # hoặc user bạn đã tạo
DB_PASSWORD=your_mysql_password # mật khẩu MySQL
DB_NAME=quanly_matkhau
```

### Bước 2: Cài đặt dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Bước 3: Chạy ứng dụng
```bash
python app.py
```

## 4. Kiểm tra kết nối

### Sử dụng MySQL Workbench:
1. Mở MySQL Workbench
2. Tạo kết nối mới với thông tin:
   - Host: localhost
   - Port: 3306
   - Username: root (hoặc user đã tạo)
   - Password: mật khẩu MySQL
3. Kết nối và kiểm tra database `quanly_matkhau`

### Sử dụng command line:
```bash
mysql -u root -p
USE quanly_matkhau;
SHOW TABLES;
DESCRIBE users;
DESCRIBE passwords;
```

## 5. Troubleshooting

### Lỗi kết nối:
- Kiểm tra MySQL service đã chạy chưa
- Kiểm tra thông tin đăng nhập trong file .env
- Kiểm tra firewall có chặn port 3306 không

### Lỗi permission:
```sql
GRANT ALL PRIVILEGES ON quanly_matkhau.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

### Lỗi charset:
Database đã được thiết lập với utf8mb4 để hỗ trợ đầy đủ Unicode.

## 6. Migration từ JSON

Nếu bạn có dữ liệu từ file JSON cũ, có thể tạo script migration riêng để chuyển đổi dữ liệu.