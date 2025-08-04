"""
Event Service for Campus Event Management System
"""

import secrets
from typing import Dict, List, Optional
from datetime import datetime, date

try:
    from ..models.event import Event, EventStatus, EventCategory
    from ..utils.file_manager import FileManager
    from ..utils.validators import EventValidator
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from models.event import Event, EventStatus, EventCategory
    from utils.file_manager import FileManager
    from utils.validators import EventValidator


class EventService:
    """Dịch vụ quản lý sự kiện"""
    
    def __init__(self):
        self.file_manager = FileManager()
        self.events_file = "data/events.json"
        self.validator = EventValidator()
    
    def _generate_event_id(self) -> str:
        """Tạo event ID ngẫu nhiên"""
        return f"event_{secrets.token_hex(6)}"
    
    def create_event(self, title: str, description: str, organizer_id: str,
                    event_date: str, location: str, max_capacity: int,
                    category: str = "other") -> Dict:
        """Tạo sự kiện mới"""
        try:
            # Validate dữ liệu đầu vào
            validation_result = self.validator.validate_event_data(
                title, description, event_date, location, max_capacity
            )
            
            if not validation_result['valid']:
                return {
                    'success': False,
                    'message': validation_result['message']
                }
            
            # Tạo event mới
            event = Event(
                event_id=self._generate_event_id(),
                title=title,
                description=description,
                organizer_id=organizer_id,
                event_date=event_date,
                location=location,
                max_capacity=max_capacity,
                category=EventCategory(category)
            )
            
            # Lưu vào file
            events_data = self.file_manager.load_json(self.events_file, [])
            events_data.append(event.to_dict())
            self.file_manager.save_json(self.events_file, events_data)
            
            return {
                'success': True,
                'message': 'Tạo sự kiện thành công',
                'event': event
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi tạo sự kiện: {str(e)}'
            }
    
    def update_event(self, event_id: str, **kwargs) -> Dict:
        """Cập nhật sự kiện"""
        try:
            event = self.get_event_by_id(event_id)
            
            if not event:
                return {
                    'success': False,
                    'message': 'Không tìm thấy sự kiện'
                }
            
            # Validate dữ liệu nếu có
            if any(key in kwargs for key in ['title', 'description', 'event_date', 'location', 'max_capacity']):
                validation_result = self.validator.validate_event_data(
                    kwargs.get('title', event.title),
                    kwargs.get('description', event.description),
                    kwargs.get('event_date', event.event_date),
                    kwargs.get('location', event.location),
                    kwargs.get('max_capacity', event.max_capacity)
                )
                
                if not validation_result['valid']:
                    return {
                        'success': False,
                        'message': validation_result['message']
                    }
            
            # Cập nhật thông tin
            event.update(**kwargs)
            self._save_event(event)
            
            return {
                'success': True,
                'message': 'Cập nhật sự kiện thành công',
                'event': event
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi cập nhật sự kiện: {str(e)}'
            }
    
    def delete_event(self, event_id: str) -> Dict:
        """Xóa sự kiện"""
        try:
            events_data = self.file_manager.load_json(self.events_file, [])
            
            for i, event_data in enumerate(events_data):
                if event_data['event_id'] == event_id:
                    del events_data[i]
                    self.file_manager.save_json(self.events_file, events_data)
                    
                    return {
                        'success': True,
                        'message': 'Xóa sự kiện thành công'
                    }
            
            return {
                'success': False,
                'message': 'Không tìm thấy sự kiện'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi xóa sự kiện: {str(e)}'
            }
    
    def get_event_by_id(self, event_id: str) -> Optional[Event]:
        """Lấy sự kiện theo ID"""
        events_data = self.file_manager.load_json(self.events_file, [])
        
        for event_data in events_data:
            if event_data['event_id'] == event_id:
                return Event.from_dict(event_data)
        
        return None
    
    def get_all_events(self) -> List[Event]:
        """Lấy tất cả sự kiện"""
        events_data = self.file_manager.load_json(self.events_file, [])
        return [Event.from_dict(event_data) for event_data in events_data]
    
    def get_events_by_organizer(self, organizer_id: str) -> List[Event]:
        """Lấy sự kiện theo organizer"""
        events_data = self.file_manager.load_json(self.events_file, [])
        
        organizer_events = []
        for event_data in events_data:
            if event_data['organizer_id'] == organizer_id:
                organizer_events.append(Event.from_dict(event_data))
        
        return organizer_events
    
    def search_events(self, query: str = "", category: str = "", 
                     status: str = "") -> List[Event]:
        """Tìm kiếm sự kiện"""
        events = self.get_all_events()
        filtered_events = []
        
        for event in events:
            # Filter theo query
            if query:
                if (query.lower() not in event.title.lower() and 
                    query.lower() not in event.description.lower() and
                    query.lower() not in event.location.lower()):
                    continue
            
            # Filter theo category
            if category and event.category.value != category:
                continue
            
            # Filter theo status
            if status and event.status.value != status:
                continue
            
            filtered_events.append(event)
        
        return filtered_events
    
    def get_upcoming_events(self) -> List[Event]:
        """Lấy các sự kiện sắp tới"""
        events = self.get_all_events()
        upcoming_events = []
        current_time = datetime.now()
        
        for event in events:
            try:
                event_datetime = datetime.fromisoformat(event.event_date)
                if event_datetime > current_time and event.status == EventStatus.ACTIVE:
                    upcoming_events.append(event)
            except:
                continue
        
        # Sắp xếp theo thời gian
        upcoming_events.sort(key=lambda x: x.event_date)
        return upcoming_events
    
    def get_popular_events(self, limit: int = 5) -> List[Event]:
        """Lấy các sự kiện phổ biến (theo số người đăng ký)"""
        events = self.get_all_events()
        
        # Sắp xếp theo số người tham gia
        popular_events = sorted(events, 
                              key=lambda x: x.current_attendees, 
                              reverse=True)
        
        return popular_events[:limit]
    
    def _save_event(self, event: Event):
        """Lưu thông tin event đã cập nhật"""
        events_data = self.file_manager.load_json(self.events_file, [])
        
        for i, event_data in enumerate(events_data):
            if event_data['event_id'] == event.event_id:
                events_data[i] = event.to_dict()
                break
        
        self.file_manager.save_json(self.events_file, events_data)
    
    def get_event_statistics(self) -> Dict:
        """Thống kê sự kiện"""
        events = self.get_all_events()
        
        total_events = len(events)
        total_attendees = sum(event.current_attendees for event in events)
        
        # Sự kiện có lượng tham gia cao nhất/thấp nhất
        if events:
            highest_attendance = max(events, key=lambda x: x.current_attendees)
            lowest_attendance = min(events, key=lambda x: x.current_attendees)
        else:
            highest_attendance = None
            lowest_attendance = None
        
        # Thống kê theo category
        category_stats = {}
        for event in events:
            category = event.category.value
            if category not in category_stats:
                category_stats[category] = {
                    'count': 0,
                    'total_attendees': 0
                }
            category_stats[category]['count'] += 1
            category_stats[category]['total_attendees'] += event.current_attendees
        
        return {
            'total_events': total_events,
            'total_attendees': total_attendees,
            'average_attendees': total_attendees / total_events if total_events > 0 else 0,
            'highest_attendance_event': highest_attendance,
            'lowest_attendance_event': lowest_attendance,
            'category_statistics': category_stats
        }
    
    def cancel_event(self, event_id: str, reason: str = "") -> Dict:
        """Hủy sự kiện"""
        try:
            event = self.get_event_by_id(event_id)
            
            if not event:
                return {
                    'success': False,
                    'message': 'Không tìm thấy sự kiện'
                }
            
            event.cancel()
            if reason:
                event.notes = reason
            
            self._save_event(event)
            
            return {
                'success': True,
                'message': 'Hủy sự kiện thành công'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi hủy sự kiện: {str(e)}'
            }
    
    def complete_event(self, event_id: str) -> Dict:
        """Đánh dấu sự kiện hoàn thành"""
        try:
            event = self.get_event_by_id(event_id)
            
            if not event:
                return {
                    'success': False,
                    'message': 'Không tìm thấy sự kiện'
                }
            
            event.complete()
            self._save_event(event)
            
            return {
                'success': True,
                'message': 'Đánh dấu hoàn thành sự kiện thành công'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi hoàn thành sự kiện: {str(e)}'
            }