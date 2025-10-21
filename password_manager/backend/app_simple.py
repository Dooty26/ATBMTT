import secrets
import string
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import hashlib
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple password storage without cryptography
USERS_FILE = 'users.json'
@app.route('/api/generate-master-password', methods=['GET'])
def generate_master_password():
    """Tạo master password ngẫu nhiên"""
    length = 16
    alphabet = string.ascii_letters + string.digits + string.punctuation
    master_password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return jsonify({'master_password': master_password})
PASSWORDS_FILE = 'passwords.json'

def load_users():
    """Tải danh sách users từ file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Lưu danh sách users vào file"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_passwords():
    """Tải danh sách passwords từ file"""
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_passwords(passwords):
    """Lưu danh sách passwords vào file"""
    with open(PASSWORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(passwords, f, ensure_ascii=False, indent=2)

def hash_password(password):
    """Hash password với SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def simple_encrypt(password, master_password):
    """Mã hóa đơn giản bằng XOR (chỉ để demo)"""
    key = hash_password(master_password)[:32]  # Lấy 32 ký tự đầu
    encrypted = ""
    for i, char in enumerate(password):
        key_char = key[i % len(key)]
        encrypted += chr(ord(char) ^ ord(key_char))
    return encrypted.encode('utf-8').hex()

def simple_decrypt(encrypted_hex, master_password):
    """Giải mã đơn giản"""
    try:
        encrypted = bytes.fromhex(encrypted_hex).decode('utf-8')
        key = hash_password(master_password)[:32]
        decrypted = ""
        for i, char in enumerate(encrypted):
            key_char = key[i % len(key)]
            decrypted += chr(ord(char) ^ ord(key_char))
        return decrypted
    except:
        return None

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    """Đăng ký người dùng mới"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Tên đăng nhập và mật khẩu không được để trống'}), 400
        
        users = load_users()
        
        if username in users:
            return jsonify({'success': False, 'message': 'Tên đăng nhập đã tồn tại'}), 400
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Lưu user mới
        users[username] = {
            'password': hashed_password,
            'created_at': datetime.now().isoformat()
        }
        
        save_users(users)
        
        return jsonify({'success': True, 'message': 'Đăng ký thành công'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi đăng ký: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Đăng nhập"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Tên đăng nhập và mật khẩu không được để trống'}), 400
        
        users = load_users()
        
        if username not in users:
            return jsonify({'success': False, 'message': 'Tên đăng nhập không tồn tại'}), 401
        
        # Kiểm tra password
        hashed_password = hash_password(password)
        if users[username]['password'] != hashed_password:
            return jsonify({'success': False, 'message': 'Mật khẩu không đúng'}), 401
        
        return jsonify({'success': True, 'message': 'Đăng nhập thành công'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi đăng nhập: {str(e)}'}), 500

@app.route('/api/passwords', methods=['GET'])
def get_passwords():
    """Lấy danh sách mật khẩu của user"""
    try:
        username = request.headers.get('Username')
        
        if not username:
            return jsonify({'success': False, 'message': 'Thiếu thông tin user'}), 400
        
        passwords = load_passwords()
        user_passwords = passwords.get(username, [])
        
        # Ẩn password thật, chỉ trả về thông tin cơ bản
        safe_passwords = []
        for pwd in user_passwords:
            safe_passwords.append({
                'id': pwd['id'],
                'website': pwd['website'],
                'username': pwd['username'],
                'created_at': pwd['created_at'],
                'updated_at': pwd.get('updated_at', pwd['created_at'])
            })
        
        return jsonify({'success': True, 'passwords': safe_passwords})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi lấy danh sách: {str(e)}'}), 500

@app.route('/api/passwords', methods=['POST'])
def add_password():
    """Thêm mật khẩu mới"""
    try:
        username = request.headers.get('Username')
        master_password = request.headers.get('Master-Password')
        
        if not username or not master_password:
            return jsonify({'success': False, 'message': 'Thiếu thông tin xác thực'}), 400
        
        data = request.get_json()
        website = data.get('website', '').strip()
        site_username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not website or not site_username or not password:
            return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400
        
        passwords = load_passwords()
        if username not in passwords:
            passwords[username] = []
        
        # Tạo ID mới
        new_id = len(passwords[username]) + 1
        
        # Mã hóa password
        encrypted_password = simple_encrypt(password, master_password)
        
        # Thêm password mới
        new_password = {
            'id': new_id,
            'website': website,
            'username': site_username,
            'encrypted_password': encrypted_password,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        passwords[username].append(new_password)
        save_passwords(passwords)
        
        return jsonify({'success': True, 'message': 'Thêm mật khẩu thành công'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi thêm mật khẩu: {str(e)}'}), 500

@app.route('/api/passwords/<int:password_id>', methods=['GET'])
def get_password(password_id):
    """Lấy mật khẩu cụ thể (đã giải mã)"""
    try:
        username = request.headers.get('Username')
        master_password = request.headers.get('Master-Password')
        
        if not username or not master_password:
            return jsonify({'success': False, 'message': 'Thiếu thông tin xác thực'}), 400
        
        passwords = load_passwords()
        user_passwords = passwords.get(username, [])
        
        # Tìm password theo ID
        target_password = None
        for pwd in user_passwords:
            if pwd['id'] == password_id:
                target_password = pwd
                break
        
        if not target_password:
            return jsonify({'success': False, 'message': 'Không tìm thấy mật khẩu'}), 404
        
        # Giải mã password
        decrypted_password = simple_decrypt(target_password['encrypted_password'], master_password)
        
        if decrypted_password is None:
            return jsonify({'success': False, 'message': 'Master password không đúng'}), 401
        
        result = {
            'id': target_password['id'],
            'website': target_password['website'],
            'username': target_password['username'],
            'password': decrypted_password,
            'created_at': target_password['created_at'],
            'updated_at': target_password.get('updated_at', target_password['created_at'])
        }
        
        return jsonify({'success': True, 'password': result})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi lấy mật khẩu: {str(e)}'}), 500

@app.route('/api/passwords/<int:password_id>', methods=['PUT'])
def update_password(password_id):
    """Cập nhật mật khẩu"""
    try:
        username = request.headers.get('Username')
        master_password = request.headers.get('Master-Password')
        
        if not username or not master_password:
            return jsonify({'success': False, 'message': 'Thiếu thông tin xác thực'}), 400
        
        data = request.get_json()
        website = data.get('website', '').strip()
        site_username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not website or not site_username or not password:
            return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400
        
        passwords = load_passwords()
        user_passwords = passwords.get(username, [])
        
        # Tìm và cập nhật password
        updated = False
        for i, pwd in enumerate(user_passwords):
            if pwd['id'] == password_id:
                encrypted_password = simple_encrypt(password, master_password)
                
                passwords[username][i] = {
                    'id': password_id,
                    'website': website,
                    'username': site_username,
                    'encrypted_password': encrypted_password,
                    'created_at': pwd['created_at'],
                    'updated_at': datetime.now().isoformat()
                }
                updated = True
                break
        
        if not updated:
            return jsonify({'success': False, 'message': 'Không tìm thấy mật khẩu'}), 404
        
        save_passwords(passwords)
        
        return jsonify({'success': True, 'message': 'Cập nhật mật khẩu thành công'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi cập nhật: {str(e)}'}), 500

@app.route('/api/passwords/<int:password_id>', methods=['DELETE'])
def delete_password(password_id):
    """Xóa mật khẩu"""
    try:
        username = request.headers.get('Username')
        
        if not username:
            return jsonify({'success': False, 'message': 'Thiếu thông tin user'}), 400
        
        passwords = load_passwords()
        user_passwords = passwords.get(username, [])
        
        # Tìm và xóa password
        new_passwords = [pwd for pwd in user_passwords if pwd['id'] != password_id]
        
        if len(new_passwords) == len(user_passwords):
            return jsonify({'success': False, 'message': 'Không tìm thấy mật khẩu'}), 404
        
        passwords[username] = new_passwords
        save_passwords(passwords)
        
        return jsonify({'success': True, 'message': 'Xóa mật khẩu thành công'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi xóa mật khẩu: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Đang khởi chạy Password Manager...")
    print("📝 Phiên bản đơn giản không cần MySQL")
    print("🔒 Sử dụng mã hóa XOR cơ bản (chỉ để demo)")
    print("🌐 Server sẽ chạy tại: http://localhost:5000")
    print("✅ Sẵn sàng sử dụng!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)