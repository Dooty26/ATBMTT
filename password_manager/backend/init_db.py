#!/usr/bin/env python3
"""
Script để khởi tạo database cho Password Manager
"""

from database import get_db

def create_tables():
    """Tạo các bảng cần thiết"""
    db = get_db()
    
    if not db.connect():
        print("❌ Không thể kết nối đến MySQL")
        return False
    
    try:
        # Tạo bảng users
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(64) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        # Tạo bảng passwords
        passwords_table = """
        CREATE TABLE IF NOT EXISTS passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            website VARCHAR(255) NOT NULL,
            username_field VARCHAR(255) NOT NULL,
            encrypted_password TEXT NOT NULL,
            salt VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user_id (user_id),
            INDEX idx_website (website)
        )
        """
        
        print("🔧 Tạo bảng users...")
        if db.execute_query(users_table):
            print("✅ Bảng users đã được tạo")
        else:
            print("❌ Lỗi tạo bảng users")
            return False
        
        print("🔧 Tạo bảng passwords...")
        if db.execute_query(passwords_table):
            print("✅ Bảng passwords đã được tạo")
        else:
            print("❌ Lỗi tạo bảng passwords")
            return False
        
        # Kiểm tra tables đã tạo
        tables = db.fetch_all("SHOW TABLES")
        print(f"\n📋 Các bảng trong database quanly_matkhau:")
        for table in tables:
            table_name = list(table.values())[0]
            print(f"  - {table_name}")
        
        print("\n🎉 Database đã được khởi tạo thành công!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khởi tạo database: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    print("🚀 Khởi tạo Database cho Password Manager")
    print("=" * 50)
    create_tables()