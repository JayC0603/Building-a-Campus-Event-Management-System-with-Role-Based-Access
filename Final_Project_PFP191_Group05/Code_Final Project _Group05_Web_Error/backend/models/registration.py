"""
Registration model for Campus Event Management System
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Optional


class RegistrationStatus(Enum):
    """Trạng thái đăng ký"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    ATTENDED = "attended"
    NO_SHOW = "no_show"


class Registration:
    """Lớp đại diện cho đăng ký tham gia sự kiện"""
    
    def __init__(self, registration_id: str, event_id: str, user_id: str):
        self.registration_id = registration_id
        self.event_id = event_id
        self.user_id = user_id
        self.status = RegistrationStatus.CONFIRMED
        self.registered_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.notes = ""
        
    def to_dict(self) -> Dict:
        """Chuyển đổi registration object thành dictionary"""
        return {
            'registration_id': self.registration_id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'status': self.status.value if isinstance(self.status, RegistrationStatus) else self.status,
            'registered_at': self.registered_at,
            'updated_at': self.updated_at,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Registration':
        """Tạo registration object từ dictionary"""
        registration = cls(
            registration_id=data['registration_id'],
            event_id=data['event_id'],
            user_id=data['user_id']
        )
        registration.status = RegistrationStatus(data.get('status', 'confirmed'))
        registration.registered_at = data.get('registered_at', datetime.now().isoformat())
        registration.updated_at = data.get('updated_at', datetime.now().isoformat())
        registration.notes = data.get('notes', '')
        return registration
    
    def confirm(self):
        """Xác nhận đăng ký"""
        self.status = RegistrationStatus.CONFIRMED
        self.updated_at = datetime.now().isoformat()
    
    def cancel(self, reason: str = ""):
        """Hủy đăng ký"""
        self.status = RegistrationStatus.CANCELLED
        self.notes = reason
        self.updated_at = datetime.now().isoformat()
    
    def mark_attended(self):
        """Đánh dấu đã tham gia"""
        self.status = RegistrationStatus.ATTENDED
        self.updated_at = datetime.now().isoformat()
    
    def mark_no_show(self):
        """Đánh dấu không tham gia"""
        self.status = RegistrationStatus.NO_SHOW
        self.updated_at = datetime.now().isoformat()
    
    def is_active(self) -> bool:
        """Kiểm tra đăng ký có active không"""
        return self.status in [RegistrationStatus.PENDING, RegistrationStatus.CONFIRMED]
    
    def get_status_display(self) -> str:
        """Lấy tên trạng thái để hiển thị"""
        status_display = {
            RegistrationStatus.PENDING: "Đang chờ",
            RegistrationStatus.CONFIRMED: "Đã xác nhận",
            RegistrationStatus.CANCELLED: "Đã hủy",
            RegistrationStatus.ATTENDED: "Đã tham gia",
            RegistrationStatus.NO_SHOW: "Không tham gia"
        }
        return status_display.get(self.status, "Không xác định")
    
    def __str__(self) -> str:
        return f"Registration({self.event_id}, {self.user_id}, {self.status.value})"
    
    def __repr__(self) -> str:
        return self.__str__()