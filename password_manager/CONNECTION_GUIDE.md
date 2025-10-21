# Hướng dẫn chi tiết về các kết nối MySQL Workbench

## 1. Các loại kết nối trong MySQL Workbench

### A. Standard (TCP/IP) - Kết nối cơ bản
Đây là loại kết nối phổ biến nhất cho local development:
```
Connection Method: Standard (TCP/IP)
Hostname: localhost hoặc 127.0.0.1
Port: 3306 (mặc định)
Username: root (hoặc user khác)
Password: [mật khẩu MySQL]
```

### B. Standard TCP/IP over SSH - Kết nối qua SSH
Dùng khi kết nối đến server remote qua SSH:
```
Connection Method: Standard TCP/IP over SSH
SSH Hostname: your-server.com
SSH Username: your-ssh-user
SSH Password/Key File: [SSH credentials]
MySQL Hostname: localhost
MySQL Server Port: 3306
Username: mysql-username
Password: mysql-password
```

### C. Standard (TCP/IP) SSL - Kết nối bảo mật
Kết nối với SSL encryption:
```
Connection Method: Standard (TCP/IP)
Use SSL: Required
SSL CA File: /path/to/ca-cert.pem
SSL CERT File: /path/to/client-cert.pem
SSL Key File: /path/to/client-key.pem
```

## 2. Tạo kết nối cho dự án Password Manager

### Bước 1: Mở MySQL Workbench
1. Khởi động MySQL Workbench
2. Tại trang chủ, click vào dấu "+" bên cạnh "MySQL Connections"

### Bước 2: Điền thông tin kết nối
```
Setup New Connection Dialog:
┌─────────────────────────────────────────┐
│ Connection Name: [Password Manager DB]  │
│ Connection Method: [Standard (TCP/IP)]  │
│ Parameters:                             │
│   Hostname: [localhost]                 │
│   Port: [3306]                         │
│   Username: [root]                     │
│   Password: [Store in Vault...]        │
│   Default Schema: [quanly_matkhau]     │
│                                         │
│ [Test Connection] [Cancel] [OK]         │
└─────────────────────────────────────────┘
```

### Bước 3: Lưu mật khẩu an toàn
1. Click "Store in Vault..." bên cạnh Password
2. Nhập mật khẩu MySQL root
3. Click "OK" để lưu mật khẩu được mã hóa

### Bước 4: Test kết nối
1. Click "Test Connection"
2. Nếu thành công sẽ hiện: "Successfully made the MySQL connection"
3. Click "OK" để đóng dialog test

### Bước 5: Lưu và sử dụng
1. Click "OK" để lưu connection
2. Connection mới sẽ xuất hiện trên trang chủ
3. Double-click để kết nối

## 3. Quản lý nhiều kết nối

### Tạo kết nối Development
```
Connection Name: Password Manager - Development
Hostname: localhost
Port: 3306
Username: dev_user
Default Schema: quanly_matkhau_dev
```

### Tạo kết nối Production (Remote)
```
Connection Name: Password Manager - Production
Hostname: your-production-server.com
Port: 3306
Username: prod_user
Default Schema: quanly_matkhau_prod
SSL: Required
```

### Tạo kết nối Testing
```
Connection Name: Password Manager - Testing
Hostname: localhost
Port: 3307 (instance khác)
Username: test_user
Default Schema: quanly_matkhau_test
```

## 4. Thiết lập Users và Permissions

### Tạo user riêng cho ứng dụng:
```sql
-- Kết nối với root user trước
-- Tạo user cho development
CREATE USER 'password_app_dev'@'localhost' IDENTIFIED BY 'dev_password123';
GRANT ALL PRIVILEGES ON quanly_matkhau.* TO 'password_app_dev'@'localhost';

-- Tạo user cho production (quyền hạn chế hơn)
CREATE USER 'password_app_prod'@'%' IDENTIFIED BY 'prod_password456';
GRANT SELECT, INSERT, UPDATE, DELETE ON quanly_matkhau.* TO 'password_app_prod'@'%';

-- Tạo user read-only cho backup/report
CREATE USER 'password_readonly'@'localhost' IDENTIFIED BY 'readonly_password789';
GRANT SELECT ON quanly_matkhau.* TO 'password_readonly'@'localhost';

FLUSH PRIVILEGES;
```

### Kiểm tra permissions:
```sql
-- Xem tất cả users
SELECT User, Host FROM mysql.user;

-- Xem quyền của user cụ thể
SHOW GRANTS FOR 'password_app_dev'@'localhost';
SHOW GRANTS FOR 'password_app_prod'@'%';
SHOW GRANTS FOR 'password_readonly'@'localhost';
```

## 5. Cấu hình Advanced Connection Options

### Connection Timeouts:
```
Advanced Tab:
┌──────────────────────────────────────┐
│ Default Charset: utf8mb4             │
│ SQL Mode: TRADITIONAL               │
│ Connection Timeout: 60              │
│ Read Timeout: 600                   │
│ Write Timeout: 600                  │
│ Interactive Timeout: 28800          │
│ Wait Timeout: 28800                 │
│ Max Reconnection Attempts: 5        │
└──────────────────────────────────────┘
```

### SSL Configuration:
```
SSL Tab:
┌──────────────────────────────────────┐
│ Use SSL: Required                    │
│ SSL CA File: /path/to/ca.pem        │
│ SSL CERT File: /path/to/cert.pem    │
│ SSL Key File: /path/to/key.pem      │
│ SSL Cipher: AES256-SHA              │
└──────────────────────────────────────┘
```

## 6. Import/Export Connection Settings

### Export connections:
1. File → Export → Export Connections...
2. Chọn connections cần export
3. Lưu file .json
4. Chia sẻ với team members

### Import connections:
1. File → Import → Import Connections...
2. Chọn file .json đã export
3. Chọn connections cần import
4. Connections sẽ xuất hiện trong danh sách

## 7. Troubleshooting Connections

### Lỗi "Can't connect to MySQL server":
```bash
# Kiểm tra MySQL service
sudo systemctl status mysql
sudo systemctl start mysql

# Kiểm tra port listening
netstat -tlnp | grep 3306
ss -tlnp | grep 3306
```

### Lỗi "Access denied":
```sql
-- Reset password cho root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;

-- Kiểm tra user có tồn tại không
SELECT User, Host FROM mysql.user WHERE User = 'your_username';
```

### Lỗi "Unknown database":
```sql
-- Kiểm tra databases có sẵncd
SHOW DATABASES;

-- Tạo database nếu chưa có
CREATE DATABASE quanly_matkhau 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

### Lỗi SSL:
```sql
-- Kiểm tra SSL status
SHOW STATUS LIKE 'Ssl_cipher';
SHOW VARIABLES LIKE '%ssl%';

-- Tắt SSL requirement nếu cần
ALTER USER 'username'@'host' REQUIRE NONE;
```

## 8. Best Practices

### Security:
- Sử dụng strong passwords
- Tạo users riêng cho từng ứng dụng
- Giới hạn quyền truy cập theo nhu cầu
- Bật SSL cho production
- Backup connection settings thường xuyên

### Performance:
- Tăng connection timeout cho queries phức tạp
- Sử dụng connection pooling trong ứng dụng
- Monitor connection usage
- Đóng connections không sử dụng

### Organization:
- Đặt tên connections rõ ràng
- Phân nhóm theo environment (dev/staging/prod)
- Document connection details
- Version control connection configs

## 9. Scripts hữu ích

### Kiểm tra connection status:
```sql
-- Xem tất cả connections hiện tại
SHOW PROCESSLIST;

-- Xem connection statistics
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Threads_running';

-- Xem max connections
SHOW VARIABLES LIKE 'max_connections';
```

### Monitoring queries:
```sql
-- Enable general log
SET GLOBAL general_log = 'ON';
SET GLOBAL general_log_file = '/var/log/mysql/general.log';

-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
```

Với hướng dẫn này, bạn có thể thiết lập và quản lý các kết nối MySQL Workbench một cách hiệu quả cho dự án Password Manager.