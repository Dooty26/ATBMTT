# Giải thích hoạt động chương trình Quản Lý Mật Khẩu

## Tổng quan

Đây là ứng dụng web quản lý mật khẩu, gồm backend Python Flask và frontend HTML/JS/CSS đơn giản. Người dùng có thể đăng ký, đăng nhập và lưu trữ, xem, quản lý mật khẩu các website một cách bảo mật.

## Thành phần chính
## Cơ chế mã hóa và lưu mật khẩu

- Khi người dùng thêm mật khẩu mới, chương trình sử dụng **master password** để mã hóa mật khẩu website.
- Quá trình mã hóa sử dụng thuật toán AES (qua thư viện `cryptography.fernet`), kết hợp với một chuỗi `salt` ngẫu nhiên để tăng tính bảo mật.
- Cụ thể:
    1. Sinh `salt` ngẫu nhiên cho mỗi mật khẩu.
    2. Từ master password và salt, tạo ra khóa mã hóa bằng PBKDF2 (hàm dẫn xuất khóa).
    3. Mã hóa mật khẩu website bằng khóa này.
    4. Lưu **mã hóa mật khẩu** và **salt** vào database (không lưu mật khẩu gốc).
- Khi cần giải mã, chương trình lấy lại salt, kết hợp với master password để tạo lại khóa, rồi giải mã mật khẩu đã lưu.
- Như vậy, chỉ khi có đúng master password, người dùng mới giải mã được mật khẩu website của mình.


- **Backend (`app.py` hoặc `app_simple.py`):**
  - Cung cấp API REST cho đăng ký, đăng nhập, CRUD mật khẩu, tạo master password ngẫu nhiên.
  - Lưu dữ liệu vào MySQL (hoặc file JSON ở chế độ đơn giản).
  - Mật khẩu website được mã hóa bằng master password trước khi lưu.

- **Frontend (`templates/index.html`, `static/js/script.js`, `static/css/style.css`):**
  - Giao diện web một trang cho mọi thao tác.
  - Xử lý đăng ký, đăng nhập, quản lý mật khẩu, thông báo giao diện.
  - Gọi API backend qua fetch trong JavaScript.

## Tính năng chính

- **Đăng ký & đăng nhập:** Người dùng tạo tài khoản, đăng nhập bằng tên đăng nhập và mật khẩu.
- **Master Password:** Mỗi người dùng nhập master password để mã hóa/giải mã mật khẩu lưu trữ.
- **Lưu trữ mật khẩu:** Mật khẩu website được mã hóa bằng master password và lưu vào database.
- **Sinh master password:** Có thể tạo master password ngẫu nhiên mạnh từ backend.
- **Ẩn/hiện mật khẩu:** Biểu tượng con mắt cho phép ẩn/hiện trường mật khẩu và master password.
- **Bảo mật:** Không lưu mật khẩu dạng thô, chỉ lưu dữ liệu đã mã hóa.

## Quy trình hoạt động

1. **Đăng ký** → Backend nhận dữ liệu, hash mật khẩu và lưu.
2. **Đăng nhập** → Kiểm tra thông tin với hash đã lưu.
3. **Thêm mật khẩu** → Mật khẩu được mã hóa bằng master password rồi lưu.
4. **Xem mật khẩu** → Mật khẩu được giải mã bằng master password.
5. **Sinh master password** → Backend trả về chuỗi mạnh để dùng làm master password.
6. **Giao diện** → Xử lý mọi thao tác, thông báo, ẩn/hiện trường nhạy cảm.

## Cấu trúc file

- `backend/app.py` - Backend Flask (MySQL)
- `backend/app_simple.py` - Backend đơn giản (file JSON)
- `backend/templates/index.html` - Giao diện chính
- `backend/static/js/script.js` - Logic frontend
- `backend/static/css/style.css` - Giao diện
- `database/schema.sql` - Cấu trúc MySQL
- `users.json`, `passwords.json` - Dữ liệu cho chế độ đơn giản

## Hướng dẫn sử dụng

1. Cài đặt thư viện (`pip install -r requirements.txt`)
2. Chạy backend (`python password_manager/backend/app.py`)
3. Mở trình duyệt tới http://localhost:5000
4. Đăng ký, đăng nhập và bắt đầu quản lý mật khẩu an toàn.
