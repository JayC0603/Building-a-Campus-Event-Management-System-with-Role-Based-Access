"""
User model for Campus Event Management System
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class UserRole(Enum):
    """Định nghĩa các vai trò người dùng"""
    ADMIN = "admin"
    ORGANIZER = "organizer"
    STUDENT = "student"
    VISITOR = "visitor"


class User:
    """Lớp đại diện cho người dùng trong hệ thống"""
    
    def __init__(self, user_id: str, username: str, email: str, 
                 password: str, role: UserRole, full_name: str = ""):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password  # Trong thực tế nên hash password
        self.role = role
        self.full_name = full_name
        self.created_at = datetime.now().isoformat()
        self.last_login = None
        self.is_active = True
        
    def to_dict(self) -> Dict:
        """Chuyển đổi user object thành dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': self.role.value if isinstance(self.role, UserRole) else self.role,
            'full_name': self.full_name,
            'created_at': self.created_at,
            'last_login': self.last_login,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Tạo user object từ dictionary"""
        user = cls(
            user_id=data['user_id'],
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=UserRole(data['role']),
            full_name=data.get('full_name', '')
        )
        user.created_at = data.get('created_at', datetime.now().isoformat())
        user.last_login = data.get('last_login')
        user.is_active = data.get('is_active', True)
        return user
    
    def has_permission(self, action: str) -> bool:
        """Kiểm tra quyền của user"""
        permissions = {
            UserRole.ADMIN: [
                'create_event', 'update_event', 'delete_event',
                'view_all_events', 'view_all_users', 'generate_reports'
            ],
            UserRole.ORGANIZER: [
                'create_event', 'update_own_event', 'delete_own_event',
                'view_own_events', 'manage_registrations'
            ],
            UserRole.STUDENT: [
                'view_events', 'register_event', 'view_own_registrations'
            ],
            UserRole.VISITOR: [
                'view_events', 'register_event'
            ]
        }
        
        return action in permissions.get(self.role, [])
    
    def update_last_login(self):
        """Cập nhật thời gian đăng nhập cuối"""
        self.last_login = datetime.now().isoformat()
    
    def __str__(self) -> str:
        return f"User({self.username}, {self.role.value})"
    
    def __repr__(self) -> str:
        return self.__str__()