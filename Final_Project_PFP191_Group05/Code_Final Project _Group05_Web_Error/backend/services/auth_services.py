"""
Authentication Service for Campus Event Management System
"""

import hashlib
import secrets
from typing import Dict, Optional, List

try:
    from ..models.user import User, UserRole
    from ..utils.file_manager import FileManager
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from models.user import User, UserRole
    from utils.file_manager import FileManager


class AuthService:
    """Dịch vụ xác thực và quản lý người dùng"""
    
    def __init__(self):
        self.file_manager = FileManager()
        self.users_file = "data/users.json"
        self.current_user = None
        self._initialize_default_users()
    
    def _initialize_default_users(self):
        """Tạo các user mặc định nếu chưa có"""
        users = self.file_manager.load_json(self.users_file, [])
        
        if not users:
            default_users = [
                {
                    'user_id': 'admin_001',
                    'username': 'admin',
                    'email': 'admin@campus.edu',
                    'password': self._hash_password('admin123'),
                    'role': 'admin',
                    'full_name': 'System Administrator',
                    'is_active': True
                },
                {
                    'user_id': 'org_001',
                    'username': 'organizer1',
                    'email': 'organizer1@campus.edu',
                    'password': self._hash_password('org123'),
                    'role': 'organizer',
                    'full_name': 'Event Organizer 1',
                    'is_active': True
                },
                {
                    'user_id': 'std_001',
                    'username': 'student1',
                    'email': 'student1@campus.edu',
                    'password': self._hash_password('student123'),
                    'role': 'student',
                    'full_name': 'Student User 1',
                    'is_active': True
                },
                {
                    'user_id': 'vis_001',
                    'username': 'visitor1',
                    'email': 'visitor1@example.com',
                    'password': self._hash_password('visitor123'),
                    'role': 'visitor',
                    'full_name': 'Visitor User 1',
                    'is_active': True
                }
            ]
            
            self.file_manager.save_json(self.users_file, default_users)
    
    def _hash_password(self, password: str) -> str:
        """Hash mật khẩu (đơn giản - trong thực tế nên dùng bcrypt)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_user_id(self) -> str:
        """Tạo user ID ngẫu nhiên"""
        return f"user_{secrets.token_hex(4)}"
    
    def register_user(self, username: str, email: str, password: str, 
                     role: UserRole, full_name: str = "") -> Dict:
        """Đăng ký user mới"""
        try:
            # Kiểm tra username đã tồn tại
            if self.get_user_by_username(username):
                return {
                    'success': False,
                    'message': 'Tên đăng nhập đã tồn tại'
                }
            
            # Kiểm tra email đã tồn tại
            if self.get_user_by_email(email):
                return {
                    'success': False,
                    'message': 'Email đã được sử dụng'
                }
            
            # Tạo user mới
            user = User(
                user_id=self._generate_user_id(),
                username=username,
                email=email,
                password=self._hash_password(password),
                role=role,
                full_name=full_name
            )
            
            # Lưu vào file
            users_data = self.file_manager.load_json(self.users_file, [])
            users_data.append(user.to_dict())
            self.file_manager.save_json(self.users_file, users_data)
            
            return {
                'success': True,
                'message': 'Đăng ký thành công',
                'user': user
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi đăng ký: {str(e)}'
            }
    
    def login(self, username: str, password: str) -> Dict:
        """Đăng nhập"""
        try:
            user = self.get_user_by_username(username)
            
            if not user:
                return {
                    'success': False,
                    'message': 'Tên đăng nhập không tồn tại'
                }
            
            if not user.is_active:
                return {
                    'success': False,
                    'message': 'Tài khoản đã bị khóa'
                }
            
            hashed_password = self._hash_password(password)
            if user.password != hashed_password:
                return {
                    'success': False,
                    'message': 'Mật khẩu không đúng'
                }
            
            # Cập nhật last login
            user.update_last_login()
            self._update_user(user)
            self.current_user = user
            
            return {
                'success': True,
                'message': 'Đăng nhập thành công',
                'user': user
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi đăng nhập: {str(e)}'
            }
    
    def logout(self):
        """Đăng xuất"""
        self.current_user = None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Lấy user theo username"""
        users_data = self.file_manager.load_json(self.users_file, [])
        
        for user_data in users_data:
            if user_data['username'] == username:
                return User.from_dict(user_data)
        
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Lấy user theo email"""
        users_data = self.file_manager.load_json(self.users_file, [])
        
        for user_data in users_data:
            if user_data['email'] == email:
                return User.from_dict(user_data)
        
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Lấy user theo ID"""
        users_data = self.file_manager.load_json(self.users_file, [])
        
        for user_data in users_data:
            if user_data['user_id'] == user_id:
                return User.from_dict(user_data)
        
        return None
    
    def get_all_users(self) -> List[User]:
        """Lấy tất cả users"""
        users_data = self.file_manager.load_json(self.users_file, [])
        return [User.from_dict(user_data) for user_data in users_data]
    
    def _update_user(self, user: User):
        """Cập nhật thông tin user"""
        users_data = self.file_manager.load_json(self.users_file, [])
        
        for i, user_data in enumerate(users_data):
            if user_data['user_id'] == user.user_id:
                users_data[i] = user.to_dict()
                break
        
        self.file_manager.save_json(self.users_file, users_data)
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> Dict:
        """Đổi mật khẩu"""
        try:
            user = self.get_user_by_id(user_id)
            
            if not user:
                return {
                    'success': False,
                    'message': 'Không tìm thấy user'
                }
            
            if user.password != self._hash_password(old_password):
                return {
                    'success': False,
                    'message': 'Mật khẩu cũ không đúng'
                }
            
            user.password = self._hash_password(new_password)
            self._update_user(user)
            
            return {
                'success': True,
                'message': 'Đổi mật khẩu thành công'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi đổi mật khẩu: {str(e)}'
            }
    
    def is_authenticated(self) -> bool:
        """Kiểm tra user đã đăng nhập chưa"""
        return self.current_user is not None
    
    def has_permission(self, action: str) -> bool:
        """Kiểm tra quyền của user hiện tại"""
        if not self.current_user:
            return False
        return self.current_user.has_permission(action)