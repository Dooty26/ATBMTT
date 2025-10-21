// Global variables
let currentUser = null;
let passwords = [];
let currentPasswordId = null;
let currentMasterPassword = null;

// API Base URL
const API_BASE = '/api';

// DOM elements
const authSection = document.getElementById('auth-section');
const mainSection = document.getElementById('main-section');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const passwordForm = document.getElementById('passwordForm');
const editPasswordForm = document.getElementById('editPasswordForm');
const passwordsList = document.getElementById('passwords-list');
const usernameDisplay = document.getElementById('username-display');
const passwordModal = document.getElementById('password-modal');
const editModal = document.getElementById('edit-modal');
const notification = document.getElementById('notification');

// Initialize app
document.addEventListener('DOMContentLoaded', function () {
    // Check if user is logged in
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = savedUser;
        showMainSection();
    }

    // Setup event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Auth forms
    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);

    // Password form
    passwordForm.addEventListener('submit', handleAddPassword);
    editPasswordForm.addEventListener('submit', handleEditPassword);

    // Modal close events
    window.addEventListener('click', function (event) {
        if (event.target === passwordModal) {
            closeModal();
        }
        if (event.target === editModal) {
            closeEditModal();
        }
    });
}

// Authentication functions
function switchToRegister() {
    document.getElementById('login-form').classList.remove('active');
    document.getElementById('register-form').classList.add('active');
}

function switchToLogin() {
    document.getElementById('register-form').classList.remove('active');
    document.getElementById('login-form').classList.add('active');
}

async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success) {
            currentUser = username;
            localStorage.setItem('currentUser', username);
            showNotification(data.message || 'Đăng nhập thành công!', 'success');
            showMainSection();
        } else {
            showNotification(data.message || 'Đăng nhập thất bại', 'error');
        }
    } catch (error) {
        showNotification('Lỗi kết nối: ' + error.message, 'error');
    }
}

async function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (password !== confirmPassword) {
        showNotification('Mật khẩu xác nhận không khớp', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success) {
            showNotification(data.message || 'Đăng ký thành công! Vui lòng đăng nhập.', 'success');
            switchToLogin();
            document.getElementById('login-username').value = username;
        } else {
            showNotification(data.message || 'Đăng ký thất bại', 'error');
        }
    } catch (error) {
        showNotification('Lỗi kết nối: ' + error.message, 'error');
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    showAuthSection();
    passwords = [];
    showNotification('Đăng xuất thành công!', 'success');
}

// UI functions
function showMainSection() {
    authSection.classList.add('hidden');
    mainSection.classList.remove('hidden');
    usernameDisplay.textContent = `Xin chào, ${currentUser}`;
    loadPasswords();
}

function showAuthSection() {
    mainSection.classList.add('hidden');
    authSection.classList.remove('hidden');
    // Clear forms
    document.querySelectorAll('form').forEach(form => form.reset());
}

// Password management functions
async function handleAddPassword(event) {
    event.preventDefault();

    const website = document.getElementById('website').value;
    const usernameField = document.getElementById('username-field').value;
    const password = document.getElementById('password').value;
    const masterPassword = document.getElementById('master-password').value;

    try {
        const response = await fetch(`${API_BASE}/passwords`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Username': currentUser,
                'Master-Password': masterPassword
            },
            body: JSON.stringify({
                website,
                username_field: usernameField,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('Mật khẩu đã được thêm thành công!', 'success');
            passwordForm.reset();
            loadPasswords();
        } else {
            showNotification(data.error || 'Thêm mật khẩu thất bại', 'error');
        }
    } catch (error) {
        showNotification('Lỗi kết nối: ' + error.message, 'error');
    }
}

async function loadPasswords() {
    try {
        const response = await fetch(`${API_BASE}/passwords`, {
            headers: {
                'Username': currentUser
            }
        });

        const data = await response.json();

        if (response.ok) {
            passwords = data;
            displayPasswords(passwords);
        } else {
            showNotification(data.error || 'Không thể tải danh sách mật khẩu', 'error');
        }
    } catch (error) {
        showNotification('Lỗi kết nối: ' + error.message, 'error');
    }
}

function displayPasswords(passwordsToShow) {
    if (passwordsToShow.length === 0) {
        passwordsList.innerHTML = `
            <div class="empty-state">
                <h3>Chưa có mật khẩu nào</h3>
                <p>Thêm mật khẩu đầu tiên của bạn ở phía trên.</p>
            </div>
        `;
        return;
    }

    passwordsList.innerHTML = passwordsToShow.map(item => `
        <div class="password-item" onclick="viewPassword(${item.id})">
            <h3>${item.website}</h3>
            <p><strong>Tên đăng nhập:</strong> ${item.username_field}</p>
            <p class="date">Tạo: ${formatDate(item.created_at)}</p>
            ${item.updated_at !== item.created_at ? `<p class="date">Cập nhật: ${formatDate(item.updated_at)}</p>` : ''}
        </div>
    `).join('');
}

async function viewPassword(passwordId) {
    const masterPassword = prompt('Nhập Master Password để xem mật khẩu:');
    if (!masterPassword) return;

    try {
        const response = await fetch(`${API_BASE}/passwords/${passwordId}`, {
            headers: {
                'Username': currentUser,
                'Master-Password': masterPassword
            }
        });

        const data = await response.json();

        if (response.ok) {
            currentPasswordId = passwordId;
            // Lưu master password để sử dụng cho các thao tác khác
            currentMasterPassword = masterPassword;
            document.getElementById('modal-website').value = data.website;
            document.getElementById('modal-username').value = data.username_field;
            document.getElementById('modal-password').value = data.password;
            document.getElementById('modal-master-password').value = '';
            passwordModal.classList.remove('hidden');
        } else {
            showNotification(data.error || 'Không thể tải mật khẩu', 'error');
        }
    } catch (error) {
        showNotification('Lỗi kết nối: ' + error.message, 'error');
    }
}

async function revealPassword() {
    // Sử dụng master password đã lưu từ lần xác thực trước
    if (!currentMasterPassword) {
        showNotification('Vui lòng đóng modal và mở lại để xác thực', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/passwords/${currentPasswordId}`, {
            headers: {
                'Username': currentUser,
                'Master-Password': currentMasterPassword
            }
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('modal-password').value = data.password;
            showNotification('Mật khẩu đã được hiển thị', 'success');
        } else {
            showNotification(data.error || 'Master Password không đúng', 'error');
        }
    } catch (error) {
        showNotification('Lỗi kết nối: ' + error.message, 'error');
    }
}

function editPassword() {
    const website = document.getElementById('modal-website').value;
    const username = document.getElementById('modal-username').value;

    document.getElementById('edit-website').value = website;
    document.getElementById('edit-username').value = username;
    document.getElementById('edit-password').value = '';
    document.getElementById('edit-master-password').value = '';

    // Chỉ ẩn modal view, không reset currentPasswordId
    passwordModal.classList.add('hidden');
    editModal.classList.remove('hidden');
}

async function savePasswordEdit() {
    const website = document.getElementById('edit-website').value;
    const username = document.getElementById('edit-username').value;
    const password = document.getElementById('edit-password').value;
    const masterPassword = document.getElementById('edit-master-password').value;

    if (!masterPassword) {
        showNotification('Vui lòng nhập Master Password', 'warning');
        return;
    }

    const updateData = {
        website,
        username_field: username
    };

    if (password) {
        updateData.password = password;
    }

    try {
        const response = await fetch(`${API_BASE}/passwords/${currentPasswordId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Username': currentUser,
                'Master-Password': masterPassword
            },
            body: JSON.stringify(updateData)
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('Mật khẩu đã được cập nhật!', 'success');
            closeEditModal();
            loadPasswords();
        } else {
            showNotification(data.error || 'Cập nhật thất bại', 'error');
        }
    } catch (error) {
        showNotification('Lỗi kết nối: ' + error.message, 'error');
    }
}

async function deletePassword() {
    if (!confirm('Bạn có chắc chắn muốn xóa mật khẩu này?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/passwords/${currentPasswordId}`, {
            method: 'DELETE',
            headers: {
                'Username': currentUser
            }
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('Mật khẩu đã được xóa!', 'success');
            closeModal();
            loadPasswords();
        } else {
            showNotification(data.error || 'Xóa thất bại', 'error');
        }
    } catch (error) {
        showNotification('Lỗi kết nối: ' + error.message, 'error');
    }
}

// Utility functions
async function generatePassword() {
    try {
        const response = await fetch(`${API_BASE}/generate-master-password`);
        const data = await response.json();
        if (response.ok && data.master_password) {
            const masterInput = document.getElementById('master-password');
            masterInput.value = data.master_password;
            masterInput.type = 'password';
            showNotification('Master password ngẫu nhiên đã được tạo!', 'success');
        } else {
            showNotification('Không thể tạo master password ngẫu nhiên', 'error');
        }
    } catch (error) {
        showNotification('Lỗi khi tạo master password ngẫu nhiên', 'error');
    }
}

function filterPasswords() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const filtered = passwords.filter(item =>
        item.website.toLowerCase().includes(searchTerm) ||
        item.username_field.toLowerCase().includes(searchTerm)
    );
    displayPasswords(filtered);
}

function togglePasswordVisibility(elementId) {
    const element = document.getElementById(elementId);
    if (element.type === 'password') {
        element.type = 'text';
    } else {
        element.type = 'password';
    }
}

function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}

async function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    try {
        await navigator.clipboard.writeText(element.value);
        showNotification('Đã sao chép vào clipboard!', 'success');
    } catch (error) {
        // Fallback for older browsers
        element.select();
        document.execCommand('copy');
        showNotification('Đã sao chép vào clipboard!', 'success');
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showNotification(message, type = 'success') {
    const notificationEl = document.getElementById('notification');
    const messageEl = document.getElementById('notification-message');

    messageEl.textContent = message;
    notificationEl.className = `notification ${type} show`;

    setTimeout(() => {
        notificationEl.classList.remove('show');
    }, 4000);
}

function closeModal() {
    passwordModal.classList.add('hidden');
    currentPasswordId = null;
    currentMasterPassword = null; // Xóa master password để bảo mật
}

function closeEditModal() {
    editModal.classList.add('hidden');
    // Reset các biến khi thực sự đóng edit modal
    currentPasswordId = null;
    currentMasterPassword = null; // Xóa master password để bảo mật
}

// Handle form submission for edit password
function handleEditPassword(event) {
    event.preventDefault();
    savePasswordEdit();
}
