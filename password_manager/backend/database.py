import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any
import json

# Load environment variables
load_dotenv()

class DatabaseManager:
    """Quản lý kết nối và thao tác với MySQL database"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'quanly_matkhau'),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True
        }
    
    def connect(self) -> bool:
        """Kết nối đến MySQL database"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            print("Kết nối MySQL thành công")
            return True
        except Error as e:
            print(f"Lỗi kết nối MySQL: {e}")
            return False
    
    def disconnect(self):
        """Ngắt kết nối database"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Đã ngắt kết nối MySQL")
    
    def execute_query(self, query: str, params: tuple = None) -> bool:
        """Thực thi query INSERT, UPDATE, DELETE"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Lỗi thực thi query: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        """Lấy một record từ database"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Lỗi fetch_one: {e}")
            return None
    
    def fetch_all(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Lấy tất cả records từ database"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return results
        except Error as e:
            print(f"Lỗi fetch_all: {e}")
            return []

    # User operations
    def create_user(self, username: str, password_hash: str) -> bool:
        """Tạo user mới"""
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        return self.execute_query(query, (username, password_hash))
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Lấy thông tin user theo username"""
        query = "SELECT * FROM users WHERE username = %s"
        return self.fetch_one(query, (username,))
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Lấy thông tin user theo ID"""
        query = "SELECT * FROM users WHERE id = %s"
        return self.fetch_one(query, (user_id,))

    # Password operations
    def add_password(self, user_id: int, website: str, username_field: str, 
                    encrypted_password: str, salt: str) -> Optional[int]:
        """Thêm password mới và trả về ID"""
        query = """
        INSERT INTO passwords (user_id, website, username_field, encrypted_password, salt) 
        VALUES (%s, %s, %s, %s, %s)
        """
        if self.execute_query(query, (user_id, website, username_field, encrypted_password, salt)):
            return self.cursor.lastrowid
        return None
    
    def get_passwords_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Lấy tất cả passwords của user"""
        query = """
        SELECT id, website, username_field, encrypted_password, salt, created_at, updated_at 
        FROM passwords WHERE user_id = %s ORDER BY updated_at DESC
        """
        return self.fetch_all(query, (user_id,))
    
    def get_password_by_id(self, password_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Lấy password cụ thể của user"""
        query = """
        SELECT * FROM passwords WHERE id = %s AND user_id = %s
        """
        return self.fetch_one(query, (password_id, user_id))
    
    def update_password(self, password_id: int, user_id: int, website: str = None, 
                       username_field: str = None, encrypted_password: str = None, 
                       salt: str = None) -> bool:
        """Cập nhật password"""
        updates = []
        params = []
        
        if website is not None:
            updates.append("website = %s")
            params.append(website)
        if username_field is not None:
            updates.append("username_field = %s")
            params.append(username_field)
        if encrypted_password is not None:
            updates.append("encrypted_password = %s")
            params.append(encrypted_password)
        if salt is not None:
            updates.append("salt = %s")
            params.append(salt)
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.extend([password_id, user_id])
        
        query = f"UPDATE passwords SET {', '.join(updates)} WHERE id = %s AND user_id = %s"
        return self.execute_query(query, tuple(params))
    
    def delete_password(self, password_id: int, user_id: int) -> bool:
        """Xóa password"""
        query = "DELETE FROM passwords WHERE id = %s AND user_id = %s"
        return self.execute_query(query, (password_id, user_id))
    
    def get_password_count(self, user_id: int) -> int:
        """Lấy số lượng passwords của user"""
        query = "SELECT COUNT(*) as count FROM passwords WHERE user_id = %s"
        result = self.fetch_one(query, (user_id,))
        return result['count'] if result else 0

# Singleton instance
db_manager = DatabaseManager()

def get_db():
    """Lấy instance database manager"""
    return db_manager