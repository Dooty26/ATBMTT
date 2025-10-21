# Hướng dẫn thiết lập kết nối MySQL Workbench

## 1. Tải và cài đặt MySQL Workbench

### Windows:
1. Truy cập: https://dev.mysql.com/downloads/workbench/
2. Chọn "MySQL Workbench 8.0.XX - Windows (x86, 64-bit), MSI Installer"
3. Tải về và cài đặt

### macOS:
1. Truy cập: https://dev.mysql.com/downloads/workbench/
2. Chọn "MySQL Workbench 8.0.XX - macOS (x86, 64-bit), DMG Archive"
3. Hoặc cài bằng Homebrew: `brew install --cask mysqlworkbench`

### Linux:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-workbench

# CentOS/RHEL
sudo yum install mysql-workbench-community
```

## 2. Tạo kết nối mới trong MySQL Workbench

### Bước 1: Mở MySQL Workbench
1. Khởi động MySQL Workbench
2. Tại màn hình Home, nhấn dấu "+" bên cạnh "MySQL Connections"

### Bước 2: Cấu hình Connection
**Thông tin kết nối cơ bản:**
```
Connection Name: Quản Lý Mật Khẩu
Connection Method: Standard (TCP/IP)
Hostname: localhost
Port: 3306
Username: root
Password: [Nhấn "Store in Vault..." để lưu mật khẩu]
Default Schema: quanly_matkhau
```

### Bước 3: Test Connection
1. Nhấn "Test Connection"
2. Nhập password MySQL nếu được yêu cầu
3. Nếu thành công sẽ hiện "Successfully made the MySQL connection"

### Bước 4: Lưu và kết nối
1. Nhấn "OK" để lưu connection
2. Double-click vào connection đã tạo để kết nối

## 3. Tạo Database và Tables

### Bước 1: Tạo Database
```sql
-- Tạo database mới
CREATE DATABASE IF NOT EXISTS quanly_matkhau 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Sử dụng database
USE quanly_matkhau;
```

### Bước 2: Chạy Schema Script
1. Mở file `database/schema.sql`
2. Copy toàn bộ nội dung
3. Paste vào MySQL Workbench Query tab
4. Nhấn Ctrl+Shift+Enter để execute toàn bộ script

### Bước 3: Kiểm tra Tables đã tạo
```sql
-- Hiển thị tất cả tables
SHOW TABLES;

-- Kiểm tra cấu trúc bảng
DESCRIBE users;
DESCRIBE passwords;

-- Xem dữ liệu
SELECT * FROM users;
SELECT * FROM passwords;
```

## 4. Cấu hình cho ứng dụng Password Manager

### Bước 1: Cập nhật file .env
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=quanly_matkhau
```

### Bước 2: Tạo User riêng (Tùy chọn - Bảo mật tốt hơn)
```sql
-- Tạo user riêng cho ứng dụng
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'secure_password123';

-- Cấp quyền cho user
GRANT SELECT, INSERT, UPDATE, DELETE ON quanly_matkhau.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;

-- Kiểm tra quyền
SHOW GRANTS FOR 'app_user'@'localhost';
```

Sau đó cập nhật file .env:
```env
DB_USER=app_user
DB_PASSWORD=secure_password123
```

## 5. Queries hữu ích cho quản lý

### Xem thống kê users và passwords:
```sql
-- Thống kê tổng quan
SELECT 
    COUNT(*) as total_users 
FROM users;

SELECT 
    u.username,
    COUNT(p.id) as total_passwords,
    MAX(p.updated_at) as last_update
FROM users u
LEFT JOIN passwords p ON u.id = p.user_id
GROUP BY u.id, u.username;
```

### Backup và restore:
```sql
-- Backup dữ liệu
SELECT * FROM users INTO OUTFILE 'users_backup.csv'
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n';

-- Backup toàn bộ database
mysqldump -u root -p quanly_matkhau > backup.sql
```

### Xóa dữ liệu test:
```sql
-- Xóa tất cả passwords (cẩn thận!)
DELETE FROM passwords;

-- Xóa tất cả users (cẩn thận!)
DELETE FROM users;

-- Reset auto increment
ALTER TABLE users AUTO_INCREMENT = 1;
ALTER TABLE passwords AUTO_INCREMENT = 1;
```

## 6. Troubleshooting

### Lỗi kết nối thường gặp:

**1. "Can't connect to MySQL server"**
- Kiểm tra MySQL service đã chạy: `sudo systemctl status mysql`
- Khởi động service: `sudo systemctl start mysql`

**2. "Access denied for user"**
- Kiểm tra username/password
- Reset password root nếu cần:
```bash
sudo mysql_secure_installation
```

**3. "Unknown database 'quanly_matkhau'"**
- Database chưa được tạo, chạy lại schema.sql

**4. "Table doesn't exist"**
- Tables chưa được tạo, chạy lại phần tạo tables trong schema.sql

### Kiểm tra kết nối từ command line:
```bash
mysql -u root -p -h localhost -P 3306 quanly_matkhau
```

## 7. Bảo mật Database

### Thay đổi password root:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_strong_password';
```

### Tạo backup tự động:
```bash
# Tạo cron job backup hàng ngày
0 2 * * * mysqldump -u root -p'password' quanly_matkhau > /backup/quanly_matkhau_$(date +\%Y\%m\%d).sql
```

### Giám sát kết nối:
```sql
-- Xem các kết nối hiện tại
SHOW PROCESSLIST;

-- Xem thống kê kết nối
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Max_used_connections';
```

Sau khi hoàn thành các bước trên, ứng dụng Password Manager sẽ kết nối thành công với MySQL database thông qua MySQL Workbench.