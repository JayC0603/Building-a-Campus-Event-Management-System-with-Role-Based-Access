"""
Event model for Campus Event Management System
"""

from datetime import datetime, date
from enum import Enum
from typing import Dict, List, Optional


class EventStatus(Enum):
    """Trạng thái sự kiện"""
    DRAFT = "draft"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class EventCategory(Enum):
    """Danh mục sự kiện"""
    ACADEMIC = "academic"
    CULTURAL = "cultural"
    SPORTS = "sports"
    WORKSHOP = "workshop"
    SEMINAR = "seminar"
    COMPETITION = "competition"
    OTHER = "other"


class Event:
    """Lớp đại diện cho sự kiện"""
    
    def __init__(self, event_id: str, title: str, description: str,
                 organizer_id: str, event_date: str, location: str,
                 max_capacity: int, category: EventCategory = EventCategory.OTHER):
        self.event_id = event_id
        self.title = title
        self.description = description
        self.organizer_id = organizer_id
        self.event_date = event_date  # ISO format string
        self.location = location
        self.max_capacity = max_capacity
        self.category = category
        self.status = EventStatus.ACTIVE
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.current_attendees = 0
        self.tags = []
        
    def to_dict(self) -> Dict:
        """Chuyển đổi event object thành dictionary"""
        return {
            'event_id': self.event_id,
            'title': self.title,
            'description': self.description,
            'organizer_id': self.organizer_id,
            'event_date': self.event_date,
            'location': self.location,
            'max_capacity': self.max_capacity,
            'category': self.category.value if isinstance(self.category, EventCategory) else self.category,
            'status': self.status.value if isinstance(self.status, EventStatus) else self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'current_attendees': self.current_attendees,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Event':
        """Tạo event object từ dictionary"""
        event = cls(
            event_id=data['event_id'],
            title=data['title'],
            description=data['description'],
            organizer_id=data['organizer_id'],
            event_date=data['event_date'],
            location=data['location'],
            max_capacity=data['max_capacity'],
            category=EventCategory(data.get('category', 'other'))
        )
        event.status = EventStatus(data.get('status', 'active'))
        event.created_at = data.get('created_at', datetime.now().isoformat())
        event.updated_at = data.get('updated_at', datetime.now().isoformat())
        event.current_attendees = data.get('current_attendees', 0)
        event.tags = data.get('tags', [])
        return event
    
    def is_available_for_registration(self) -> bool:
        """Kiểm tra sự kiện có sẵn sàng đăng ký không"""
        if self.status != EventStatus.ACTIVE:
            return False
        
        if self.current_attendees >= self.max_capacity:
            return False
        
        # Kiểm tra ngày sự kiện chưa qua
        try:
            event_datetime = datetime.fromisoformat(self.event_date)
            return event_datetime > datetime.now()
        except:
            return True
    
    def add_attendee(self) -> bool:
        """Thêm người tham gia"""
        if self.current_attendees < self.max_capacity:
            self.current_attendees += 1
            self.updated_at = datetime.now().isoformat()
            return True
        return False
    
    def remove_attendee(self) -> bool:
        """Xóa người tham gia"""
        if self.current_attendees > 0:
            self.current_attendees -= 1
            self.updated_at = datetime.now().isoformat()
            return True
        return False
    
    def get_availability_percentage(self) -> float:
        """Tính phần trăm chỗ trống"""
        if self.max_capacity == 0:
            return 0.0
        return (self.current_attendees / self.max_capacity) * 100
    
    def is_full(self) -> bool:
        """Kiểm tra sự kiện đã đầy chưa"""
        return self.current_attendees >= self.max_capacity
    
    def get_remaining_slots(self) -> int:
        """Số chỗ còn lại"""
        return max(0, self.max_capacity - self.current_attendees)
    
    def update(self, **kwargs):
        """Cập nhật thông tin sự kiện"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()
    
    def cancel(self):
        """Hủy sự kiện"""
        self.status = EventStatus.CANCELLED
        self.updated_at = datetime.now().isoformat()
    
    def complete(self):
        """Đánh dấu sự kiện hoàn thành"""
        self.status = EventStatus.COMPLETED
        self.updated_at = datetime.now().isoformat()
    
    def __str__(self) -> str:
        return f"Event({self.title}, {self.event_date})"
    
    def __repr__(self) -> str:
        return self.__str__()