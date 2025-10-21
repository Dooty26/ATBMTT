# Ứng Dụng Quản Lý Mật Khẩu

Ứng dụng web quản lý mật khẩu an toàn sử dụng mã hóa SHA-256 và AES, được xây dựng với Python Flask backend, MySQL database và HTML/CSS/JavaScript frontend.

## Tính Năng

- ✅ **Bảo mật cao**: Mã hóa mật khẩu bằng AES-256 với master password
- ✅ **Hash an toàn**: Sử dụng SHA-256 để hash mật khẩu đăng nhập
- ✅ **Giao diện thân thiện**: Responsive design, dễ sử dụng
- ✅ **Quản lý đầy đủ**: Thêm, xem, sửa, xóa mật khẩu
- ✅ **Tìm kiếm**: Tìm kiếm mật khẩu theo website
- ✅ **Tạo mật khẩu**: Tạo mật khẩu ngẫu nhiên mạnh
- ✅ **Copy clipboard**: Sao chép mật khẩu nhanh chóng

## Cấu Trúc Dự Án

```
password_manager/
├── backend/
│   ├── app.py                 # Flask server chính
│   ├── database.py            # MySQL connection manager
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Database configuration
│   ├── templates/
│   │   └── index.html        # Giao diện chính
│   └── static/
│       ├── css/
│       │   └── style.css     # Styling
│       └── js/
│           └── script.js     # JavaScript logic
├── database/
│   └── schema.sql            # MySQL database schema
├── MYSQL_SETUP.md           # Hướng dẫn cài đặt MySQL
├── MYSQL_WORKBENCH_SETUP.md # Hướng dẫn MySQL Workbench
├── CONNECTION_GUIDE.md      # Hướng dẫn quản lý kết nối
├── QUICK_START.md           # Hướng dẫn khởi động nhanh
└── README.md               # Hướng dẫn này
```

## Cài Đặt

### 1. Yêu Cầu Hệ Thống
- Python 3.7 trở lên
- MySQL Server 8.0 trở lên
- MySQL Workbench (khuyến nghị)
- pip (Python package manager)

### 2. Cài Đặt MySQL
```bash
# Tham khảo chi tiết trong MYSQL_SETUP.md
# Hoặc tải từ: https://dev.mysql.com/downloads/mysql/
```

### 3. Thiết Lập Database
```bash
# Tạo database trong MySQL
mysql -u root -p
CREATE DATABASE quanly_matkhau CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Import schema
mysql -u root -p quanly_matkhau < database/schema.sql
```

### 4. Cấu Hình Kết Nối
```bash
# Tạo file .env trong thư mục backend
cp backend/.env.example backend/.env

# Chỉnh sửa thông tin database trong .env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=quanly_matkhau
```

### 5. Cài Đặt Dependencies
```bash
# Di chuyển vào thư mục backend
cd password_manager/backend

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 6. Chạy Ứng Dụng
```bash
# Trong thư mục backend
python app.py
```

Ứng dụng sẽ chạy tại: `http://localhost:5000`

### 7. Thiết Lập MySQL Workbench (Tùy chọn)
- Tham khảo [`MYSQL_WORKBENCH_SETUP.md`](MYSQL_WORKBENCH_SETUP.md) để cài đặt và cấu hình
- Tham khảo [`CONNECTION_GUIDE.md`](CONNECTION_GUIDE.md) để quản lý kết nối

## Hướng Dẫn Sử Dụng

### 1. Đăng Ký Tài Khoản
- Truy cập `http://localhost:5000`
- Click "Đăng ký ngay"
- Nhập tên đăng nhập và mật khẩu
- Click "Đăng Ký"

### 2. Đăng Nhập
- Nhập thông tin đăng nhập
- Click "Đăng Nhập"

### 3. Thêm Mật Khẩu Mới
- Điền thông tin website
- Nhập tên đăng nhập cho website đó
- Nhập mật khẩu (hoặc click "Tạo Mật Khẩu Ngẫu Nhiên")
- **Quan trọng**: Nhập Master Password để mã hóa
- Click "Thêm Mật Khẩu"

### 4. Xem Mật Khẩu
- Click vào thẻ mật khẩu trong danh sách
- Nhập Master Password
- Mật khẩu sẽ được giải mã và hiển thị

### 5. Chỉnh Sửa Mật Khẩu
- Mở chi tiết mật khẩu
- Click "Chỉnh Sửa"
- Cập nhật thông tin
- Nhập Master Password
- Click "Lưu Thay Đổi"

### 6. Xóa Mật Khẩu
- Mở chi tiết mật khẩu
- Click "Xóa"
- Xác nhận xóa

## Bảo Mật

### Mã Hóa SHA-256
- Mật khẩu đăng nhập được hash bằng SHA-256
- Không lưu trữ mật khẩu gốc trong database

### Mã Hóa AES-256
- Mật khẩu được mã hóa bằng AES-256
- Sử dụng PBKDF2 với 100,000 iterations
- Mỗi mật khẩu có salt riêng biệt
- Master password không được lưu trữ

### Database Security
- Sử dụng MySQL với connection pooling
- Prepared statements để tránh SQL injection
- Foreign key constraints để đảm bảo tính toàn vẹn dữ liệu
- Index tối ưu cho performance

### Best Practices
- **Master Password**: Sử dụng mật khẩu mạnh, không chia sẻ
- **Database Backup**: Định kỳ backup MySQL database
- **HTTPS**: Trong production, luôn sử dụng HTTPS
- **Firewall**: Hạn chế truy cập port 5000 và 3306 từ bên ngoài
- **User Privileges**: Tạo MySQL user riêng với quyền hạn chế

## API Endpoints

### Authentication
- `POST /api/register` - Đăng ký tài khoản
- `POST /api/login` - Đăng nhập

### Password Management
- `GET /api/passwords` - Lấy danh sách mật khẩu
- `POST /api/passwords` - Thêm mật khẩu mới
- `GET /api/passwords/{id}` - Lấy mật khẩu cụ thể (đã giải mã)
- `PUT /api/passwords/{id}` - Cập nhật mật khẩu
- `DELETE /api/passwords/{id}` - Xóa mật khẩu

### Headers Required
- `Username`: Tên đăng nhập
- `Master-Password`: Master password (chỉ khi cần mã hóa/giải mã)

## Khắc Phục Sự Cố

### Lỗi Database Connection
```bash
# Kiểm tra MySQL service
sudo systemctl status mysql
sudo systemctl start mysql

# Kiểm tra thông tin trong .env file
# Đảm bảo database đã được tạo
mysql -u root -p -e "SHOW DATABASES;"
```

### Lỗi Import Python Libraries
```bash
pip install --upgrade pip
pip install -r requirements.txt

# Nếu lỗi MySQL connector
pip install mysql-connector-python
pip install PyMySQL
```

### Lỗi Port Đã Sử Dụng
```bash
# Thay đổi port trong app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Lỗi Không Thể Giải Mã
- Kiểm tra Master Password có đúng không
- Đảm bảo không có ký tự đặc biệt trong Master Password

### Lỗi MySQL Workbench
- Tham khảo [`CONNECTION_GUIDE.md`](CONNECTION_GUIDE.md) section Troubleshooting
- Kiểm tra firewall settings
- Verify user permissions

## Phát Triển

### Thêm Tính Năng Mới
1. Fork repository
2. Tạo branch mới
3. Implement tính năng
4. Test kỹ lưỡng
5. Tạo Pull Request

### Database Schema
```sql
-- Database: quanly_matkhau

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Passwords table
CREATE TABLE passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    website VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    encrypted_password TEXT NOT NULL,
    salt VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_website (user_id, website)
);
```

### Environment Configuration
```env
# backend/.env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=quanly_matkhau
```

## Tài Liệu Kèm Theo

- [`QUICK_START.md`](QUICK_START.md) - Hướng dẫn khởi động nhanh
- [`MYSQL_SETUP.md`](MYSQL_SETUP.md) - Cài đặt và cấu hình MySQL
- [`MYSQL_WORKBENCH_SETUP.md`](MYSQL_WORKBENCH_SETUP.md) - Thiết lập MySQL Workbench
- [`CONNECTION_GUIDE.md`](CONNECTION_GUIDE.md) - Quản lý kết nối database
- [`database/schema.sql`](database/schema.sql) - Database schema

---

**Lưu ý**: Ứng dụng hiện đã được nâng cấp từ JSON file storage lên MySQL database để đảm bảo tính bảo mật, hiệu suất và khả năng mở rộng tốt hơn. Trong môi trường production, cần thêm các biện pháp bảo mật như rate limiting, session management, CSRF protection, và SSL encryption.
