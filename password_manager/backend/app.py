import secrets
import string
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import hashlib
import os
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from database import get_db

app = Flask(__name__)
CORS(app)

@app.route('/api/generate-master-password', methods=['GET'])
def generate_master_password():
    """Tạo master password ngẫu nhiên dùng để mã hóa, không dùng cho đăng nhập website"""
    length = 32  # Stronger for encryption
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    master_password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return jsonify({'master_password': master_password})

# Database instance
db = get_db()

def generate_key_from_password(password: str, salt: bytes) -> bytes:
    """Tạo key AES từ password sử dụng PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_password(password: str, master_password: str) -> dict:
    """Mã hóa password sử dụng AES"""
    salt = os.urandom(16)
    key = generate_key_from_password(master_password, salt)
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    
    return {
        'encrypted_password': base64.urlsafe_b64encode(encrypted_password).decode(),
        'salt': base64.urlsafe_b64encode(salt).decode()
    }

def decrypt_password(encrypted_data: dict, master_password: str) -> str:
    """Giải mã password từ AES"""
    try:
        salt = base64.urlsafe_b64decode(encrypted_data['salt'])
        encrypted_password = base64.urlsafe_b64decode(encrypted_data['encrypted_password'])
        
        key = generate_key_from_password(master_password, salt)
        f = Fernet(key)
        decrypted_password = f.decrypt(encrypted_password)
        
        return decrypted_password.decode()
    except Exception as e:
        return None

def hash_password_sha256(password: str) -> str:
    """Hash password sử dụng SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Khởi tạo kết nối database"""
    db.connect()

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

# Duplicate route removed to avoid confusion

@app.route('/api/register', methods=['POST'])
def register():
    """Đăng ký tài khoản mới"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Dữ liệu JSON không hợp lệ'}), 400
            
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username và password là bắt buộc'}), 400
        
        # Kiểm tra username đã tồn tại
        existing_user = db.get_user_by_username(username)
        if existing_user:
            return jsonify({'success': False, 'message': 'Username đã tồn tại'}), 400
        
        # Hash password với SHA-256
        hashed_password = hash_password_sha256(password)
        
        # Tạo user mới trong database
        if db.create_user(username, hashed_password):
            return jsonify({'success': True, 'message': 'Đăng ký thành công'}), 201
        else:
            return jsonify({'success': False, 'message': 'Lỗi tạo tài khoản'}), 500
    except Exception as e:
        print(f"Lỗi đăng ký: {e}")
        return jsonify({'success': False, 'message': f'Lỗi server: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Đăng nhập"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Dữ liệu JSON không hợp lệ'}), 400
            
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username và password là bắt buộc'}), 400
        
        # Lấy thông tin user từ database
        user = db.get_user_by_username(username)
        if not user:
            return jsonify({'success': False, 'message': 'Username không tồn tại'}), 404
        
        hashed_password = hash_password_sha256(password)
        
        if user['password_hash'] != hashed_password:
            return jsonify({'success': False, 'message': 'Tên đăng nhập hoặc mật khẩu không đúng'}), 401
        
        return jsonify({'success': True, 'message': 'Đăng nhập thành công', 'username': username}), 200
    except Exception as e:
        print(f"Lỗi đăng nhập: {e}")
        return jsonify({'success': False, 'message': f'Lỗi server: {str(e)}'}), 500

@app.route('/api/passwords', methods=['GET'])
def get_passwords():
    """Lấy danh sách passwords của user"""
    username = request.headers.get('Username')
    if not username:
        return jsonify({'error': 'Username header là bắt buộc'}), 400
    
    # Lấy thông tin user từ database
    user = db.get_user_by_username(username)
    if not user:
        return jsonify({'error': 'Tên đăng nhập hoặc mật khẩu không đúng'}), 404
    
    # Lấy danh sách passwords từ database
    user_passwords = db.get_passwords_by_user(user['id'])
    
    # Trả về danh sách passwords (không bao gồm password thật)
    result = []
    for item in user_passwords:
        result.append({
            'id': item['id'],
            'website': item['website'],
            'username_field': item['username_field'],
            'created_at': item['created_at'].isoformat() if item['created_at'] else None,
            'updated_at': item['updated_at'].isoformat() if item['updated_at'] else None
        })
    
    return jsonify(result), 200

@app.route('/api/passwords', methods=['POST'])
def add_password():
    """Thêm password mới"""
    data = request.get_json()
    username = request.headers.get('Username')
    master_password = request.headers.get('Master-Password')
    
    if not username or not master_password:
        return jsonify({'error': 'Username và Master-Password headers là bắt buộc'}), 400
    
    website = data.get('website')
    username_field = data.get('username_field')
    password = data.get('password')
    
    if not website or not username_field or not password:
        return jsonify({'error': 'Website, username và password là bắt buộc'}), 400
    
    # Lấy thông tin user từ database
    user = db.get_user_by_username(username)
    if not user:
        return jsonify({'error': 'User không tồn tại'}), 404
    
    # Mã hóa password
    encrypted_data = encrypt_password(password, master_password)
    
    # Thêm password vào database
    password_id = db.add_password(
        user['id'],
        website,
        username_field,
        encrypted_data['encrypted_password'],
        encrypted_data['salt']
    )
    
    if password_id:
        return jsonify({'message': 'Password đã được thêm thành công', 'id': password_id}), 201
    else:
        return jsonify({'error': 'Lỗi thêm password'}), 500

@app.route('/api/passwords/<int:password_id>', methods=['GET'])
def get_password(password_id):
    """Lấy password cụ thể (đã giải mã)"""
    username = request.headers.get('Username')
    master_password = request.headers.get('Master-Password')
    
    if not username or not master_password:
        return jsonify({'error': 'Username và Master-Password headers là bắt buộc'}), 400
    
    # Lấy thông tin user từ database
    user = db.get_user_by_username(username)
    if not user:
        return jsonify({'error': 'User không tồn tại'}), 404
    
    # Lấy password từ database
    password_item = db.get_password_by_id(password_id, user['id'])
    if not password_item:
        return jsonify({'error': 'Password không tìm thấy'}), 404
    
    # Giải mã password
    encrypted_data = {
        'encrypted_password': password_item['encrypted_password'],
        'salt': password_item['salt']
    }
    
    decrypted_password = decrypt_password(encrypted_data, master_password)
    
    if decrypted_password is None:
        return jsonify({'error': 'Master Password không đúng'}), 400
    
    result = {
        'id': password_item['id'],
        'website': password_item['website'],
        'username_field': password_item['username_field'],
        'password': decrypted_password,
        'created_at': password_item['created_at'].isoformat() if password_item['created_at'] else None,
        'updated_at': password_item['updated_at'].isoformat() if password_item['updated_at'] else None
    }
    
    return jsonify(result), 200

@app.route('/api/passwords/<int:password_id>', methods=['PUT'])
def update_password(password_id):
    """Cập nhật password"""
    data = request.get_json()
    username = request.headers.get('Username')
    master_password = request.headers.get('Master-Password')
    
    if not username or not master_password:
        return jsonify({'error': 'Username và Master-Password headers là bắt buộc'}), 400
    
    # Lấy thông tin user từ database
    user = db.get_user_by_username(username)
    if not user:
        return jsonify({'error': 'User không tồn tại'}), 404
    
    # Kiểm tra password có tồn tại
    password_item = db.get_password_by_id(password_id, user['id'])
    if not password_item:
        return jsonify({'error': 'Password không tìm thấy'}), 404
    
    # Chuẩn bị dữ liệu cập nhật
    website = data.get('website')
    username_field = data.get('username_field')
    new_password = data.get('password')
    
    encrypted_password = None
    salt = None
    
    if new_password:
        encrypted_data = encrypt_password(new_password, master_password)
        encrypted_password = encrypted_data['encrypted_password']
        salt = encrypted_data['salt']
    
    # Cập nhật trong database
    if db.update_password(password_id, user['id'], website, username_field, encrypted_password, salt):
        return jsonify({'message': 'Password đã được cập nhật thành công'}), 200
    else:
        return jsonify({'error': 'Lỗi cập nhật password'}), 500

@app.route('/api/passwords/<int:password_id>', methods=['DELETE'])
def delete_password(password_id):
    """Xóa password"""
    username = request.headers.get('Username')
    
    if not username:
        return jsonify({'error': 'Username header là bắt buộc'}), 400
    
    # Lấy thông tin user từ database
    user = db.get_user_by_username(username)
    if not user:
        return jsonify({'error': 'User không tồn tại'}), 404
    
    # Xóa password từ database
    if db.delete_password(password_id, user['id']):
        return jsonify({'message': 'Password đã được xóa thành công'}), 200
    else:
        return jsonify({'error': 'Password không tìm thấy hoặc lỗi xóa'}), 404

if __name__ == '__main__':
    # Khởi tạo database khi ứng dụng start
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

