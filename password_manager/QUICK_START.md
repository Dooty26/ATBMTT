# Hướng Dẫn Khởi Chạy Nhanh

## 🚀 Chạy Ứng Dụng

Server Flask đang chạy tại: **http://localhost:5000**

## ✅ Test Các Tính Năng

### 1. Test Đăng Ký
- Mở trình duyệt, truy cập: `http://localhost:5000`
- Click "Đăng ký ngay"
- Nhập thông tin:
  - Tên đăng nhập: `testuser`
  - Mật khẩu: `testpassword123`
  - Xác nhận mật khẩu: `testpassword123`
- Click "Đăng Ký"

### 2. Test Đăng Nhập
- Nhập thông tin vừa đăng ký
- Click "Đăng Nhập"

### 3. Test Thêm Mật Khẩu
- Điền form thêm mật khẩu:
  - Website: `google.com`
  - Tên đăng nhập: `myemail@gmail.com`
  - Mật khẩu: `mypassword123` (hoặc click "Tạo Mật Khẩu Ngẫu Nhiên")
  - Master Password: `masterkey123`
- Click "Thêm Mật Khẩu"

### 4. Test Xem Mật Khẩu
- Click vào thẻ mật khẩu vừa tạo
- Nhập Master Password: `masterkey123`
- Click "Hiện Mật Khẩu"

### 5. Test Chức Năng Khác
- ✅ Tìm kiếm mật khẩu
- ✅ Chỉnh sửa mật khẩu
- ✅ Xóa mật khẩu
- ✅ Copy mật khẩu
- ✅ Đăng xuất

## 🔒 Bảo Mật đã Implement

- ✅ **SHA-256**: Mật khẩu đăng nhập được hash
- ✅ **AES-256**: Mật khẩu được mã hóa với master password
- ✅ **PBKDF2**: 100,000 iterations cho key derivation
- ✅ **Salt**: Mỗi mật khẩu có salt riêng biệt
- ✅ **No Storage**: Master password không được lưu trữ

## 📁 Files được tạo tự động

Khi chạy ứng dụng, các file sau sẽ được tạo tự động:
- `password_manager/backend/users.json` - Database users
- `password_manager/backend/passwords.json` - Database mật khẩu đã mã hóa

## 🛑 Dừng Server

Để dừng server, nhấn `Ctrl + C` trong terminal.

## 🎯 Tính Năng Chính

| Tính Năng | Trạng Thái | Mô Tả |
|-----------|------------|-------|
| Đăng ký/Đăng nhập | ✅ | SHA-256 hash |
| Thêm mật khẩu | ✅ | AES-256 encryption |
| Xem mật khẩu | ✅ | Giải mã với master password |
| Chỉnh sửa | ✅ | Cập nhật thông tin |
| Xóa | ✅ | Xóa an toàn |
| Tìm kiếm | ✅ | Filter theo website |
| Tạo mật khẩu | ✅ | Random generator |
| Copy clipboard | ✅ | Quick copy |
| Responsive UI | ✅ | Mobile friendly |

---

**🎉 Ứng dụng đã sẵn sàng sử dụng!**