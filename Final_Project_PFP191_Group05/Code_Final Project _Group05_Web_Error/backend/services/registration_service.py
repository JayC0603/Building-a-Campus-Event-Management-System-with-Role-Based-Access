"""
Registration Service for Campus Event Management System
"""

import secrets
from typing import Dict, List, Optional

try:
    from ..models.registration import Registration, RegistrationStatus
    from ..services.event_service import EventService
    from ..utils.file_manager import FileManager
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from models.registration import Registration, RegistrationStatus
    from services.event_service import EventService
    from utils.file_manager import FileManager


class RegistrationService:
    """Dịch vụ quản lý đăng ký tham gia sự kiện"""
    
    def __init__(self):
        self.file_manager = FileManager()
        self.registrations_file = "data/registrations.json"
        self.event_service = EventService()
    
    def _generate_registration_id(self) -> str:
        """Tạo registration ID ngẫu nhiên"""
        return f"reg_{secrets.token_hex(6)}"
    
    def register_for_event(self, event_id: str, user_id: str) -> Dict:
        """Đăng ký tham gia sự kiện"""
        try:
            # Kiểm tra sự kiện có tồn tại không
            event = self.event_service.get_event_by_id(event_id)
            if not event:
                return {
                    'success': False,
                    'message': 'Không tìm thấy sự kiện'
                }
            
            # Kiểm tra sự kiện có sẵn sàng đăng ký không
            if not event.is_available_for_registration():
                return {
                    'success': False,
                    'message': 'Sự kiện không sẵn sàng để đăng ký'
                }
            
            # Kiểm tra đã đăng ký trước đó chưa
            existing_registration = self.get_registration(event_id, user_id)
            if existing_registration and existing_registration.is_active():
                return {
                    'success': False,
                    'message': 'Bạn đã đăng ký sự kiện này rồi'
                }
            
            # Kiểm tra sức chứa
            if event.is_full():
                return {
                    'success': False,
                    'message': 'Sự kiện đã đầy, không thể đăng ký thêm'
                }
            
            # Tạo đăng ký mới
            registration = Registration(
                registration_id=self._generate_registration_id(),
                event_id=event_id,
                user_id=user_id
            )
            
            # Lưu đăng ký
            registrations_data = self.file_manager.load_json(self.registrations_file, [])
            registrations_data.append(registration.to_dict())
            self.file_manager.save_json(self.registrations_file, registrations_data)
            
            # Cập nhật số lượng attendees trong event
            event.add_attendee()
            self.event_service._save_event(event)
            
            return {
                'success': True,
                'message': 'Đăng ký tham gia sự kiện thành công',
                'registration': registration
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi đăng ký: {str(e)}'
            }
    
    def cancel_registration(self, event_id: str, user_id: str, reason: str = "") -> Dict:
        """Hủy đăng ký tham gia sự kiện"""
        try:
            registration = self.get_registration(event_id, user_id)
            
            if not registration:
                return {
                    'success': False,
                    'message': 'Không tìm thấy đăng ký'
                }
            
            if not registration.is_active():
                return {
                    'success': False,
                    'message': 'Đăng ký đã được hủy hoặc không hợp lệ'
                }
            
            # Hủy đăng ký
            registration.cancel(reason)
            self._save_registration(registration)
            
            # Cập nhật số lượng attendees trong event
            event = self.event_service.get_event_by_id(event_id)
            if event:
                event.remove_attendee()
                self.event_service._save_event(event)
            
            return {
                'success': True,
                'message': 'Hủy đăng ký thành công'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi hủy đăng ký: {str(e)}'
            }
    
    def get_registration(self, event_id: str, user_id: str) -> Optional[Registration]:
        """Lấy thông tin đăng ký của user cho event cụ thể"""
        registrations_data = self.file_manager.load_json(self.registrations_file, [])
        
        for reg_data in registrations_data:
            if reg_data['event_id'] == event_id and reg_data['user_id'] == user_id:
                return Registration.from_dict(reg_data)
        
        return None
    
    def get_user_registrations(self, user_id: str) -> List[Registration]:
        """Lấy tất cả đăng ký của user"""
        registrations_data = self.file_manager.load_json(self.registrations_file, [])
        
        user_registrations = []
        for reg_data in registrations_data:
            if reg_data['user_id'] == user_id:
                user_registrations.append(Registration.from_dict(reg_data))
        
        return user_registrations
    
    def get_event_registrations(self, event_id: str) -> List[Registration]:
        """Lấy tất cả đăng ký cho một sự kiện"""
        registrations_data = self.file_manager.load_json(self.registrations_file, [])
        
        event_registrations = []
        for reg_data in registrations_data:
            if reg_data['event_id'] == event_id:
                event_registrations.append(Registration.from_dict(reg_data))
        
        return event_registrations
    
    def get_all_registrations(self) -> List[Registration]:
        """Lấy tất cả đăng ký"""
        registrations_data = self.file_manager.load_json(self.registrations_file, [])
        return [Registration.from_dict(reg_data) for reg_data in registrations_data]
    
    def _save_registration(self, registration: Registration):
        """Lưu thông tin đăng ký đã cập nhật"""
        registrations_data = self.file_manager.load_json(self.registrations_file, [])
        
        for i, reg_data in enumerate(registrations_data):
            if reg_data['registration_id'] == registration.registration_id:
                registrations_data[i] = registration.to_dict()
                break
        
        self.file_manager.save_json(self.registrations_file, registrations_data)
    
    def mark_attendance(self, registration_id: str, attended: bool = True) -> Dict:
        """Đánh dấu tham gia/không tham gia"""
        try:
            registrations_data = self.file_manager.load_json(self.registrations_file, [])
            
            for i, reg_data in enumerate(registrations_data):
                if reg_data['registration_id'] == registration_id:
                    registration = Registration.from_dict(reg_data)
                    
                    if attended:
                        registration.mark_attended()
                    else:
                        registration.mark_no_show()
                    
                    registrations_data[i] = registration.to_dict()
                    self.file_manager.save_json(self.registrations_file, registrations_data)
                    
                    return {
                        'success': True,
                        'message': f'Đã đánh dấu {"tham gia" if attended else "không tham gia"}'
                    }
            
            return {
                'success': False,
                'message': 'Không tìm thấy đăng ký'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi đánh dấu tham gia: {str(e)}'
            }
    
    def get_registration_statistics(self) -> Dict:
        """Thống kê đăng ký"""
        registrations = self.get_all_registrations()
        
        total_registrations = len(registrations)
        
        # Thống kê theo trạng thái
        status_stats = {}
        for reg in registrations:
            status = reg.status.value
            if status not in status_stats:
                status_stats[status] = 0
            status_stats[status] += 1
        
        # Thống kê theo sự kiện
        event_stats = {}
        for reg in registrations:
            event_id = reg.event_id
            if event_id not in event_stats:
                event_stats[event_id] = {
                    'total': 0,
                    'confirmed': 0,
                    'cancelled': 0,
                    'attended': 0
                }
            
            event_stats[event_id]['total'] += 1
            if reg.status == RegistrationStatus.CONFIRMED:
                event_stats[event_id]['confirmed'] += 1
            elif reg.status == RegistrationStatus.CANCELLED:
                event_stats[event_id]['cancelled'] += 1
            elif reg.status == RegistrationStatus.ATTENDED:
                event_stats[event_id]['attended'] += 1
        
        return {
            'total_registrations': total_registrations,
            'status_statistics': status_stats,
            'event_statistics': event_stats
        }
    
    def get_user_registered_events(self, user_id: str, include_cancelled: bool = False) -> List[Dict]:
        """Lấy danh sách sự kiện user đã đăng ký cùng thông tin đăng ký"""
        user_registrations = self.get_user_registrations(user_id)
        registered_events = []
        
        for registration in user_registrations:
            if not include_cancelled and not registration.is_active():
                continue
            
            event = self.event_service.get_event_by_id(registration.event_id)
            if event:
                registered_events.append({
                    'event': event,
                    'registration': registration
                })
        
        return registered_events
    
    def bulk_cancel_event_registrations(self, event_id: str, reason: str = "Event cancelled") -> Dict:
        """Hủy tất cả đăng ký của một sự kiện (khi hủy sự kiện)"""
        try:
            event_registrations = self.get_event_registrations(event_id)
            cancelled_count = 0
            
            for registration in event_registrations:
                if registration.is_active():
                    registration.cancel(reason)
                    self._save_registration(registration)
                    cancelled_count += 1
            
            return {
                'success': True,
                'message': f'Đã hủy {cancelled_count} đăng ký',
                'cancelled_count': cancelled_count
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi hủy đăng ký hàng loạt: {str(e)}'
            }