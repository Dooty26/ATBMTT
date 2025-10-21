#!/usr/bin/env python3
"""
Test kết nối MySQL
"""

from database import get_db

def test_connection():
    """Test kết nối database"""
    db = get_db()
    
    print("🔧 Testing MySQL connection...")
    success = db.connect()
    
    if success:
        print("✅ MySQL connection successful!")
        
        # Test tạo user thử
        try:
            print("🧪 Testing user creation...")
            result = db.create_user("test_user", "test_hash")
            if result:
                print("✅ User creation test successful!")
                # Xóa user test
                db.execute_query("DELETE FROM users WHERE username = %s", ("test_user",))
                print("🗑️ Cleaned up test user")
            else:
                print("❌ User creation test failed!")
        except Exception as e:
            print(f"❌ User creation error: {e}")
        
    else:
        print("❌ MySQL connection failed!")
        print("Please check:")
        print("  - MySQL service is running")
        print("  - Password in .env is correct")
        print("  - Database 'quanly_matkhau' exists")
    
    db.disconnect()
    return success

if __name__ == "__main__":
    test_connection()