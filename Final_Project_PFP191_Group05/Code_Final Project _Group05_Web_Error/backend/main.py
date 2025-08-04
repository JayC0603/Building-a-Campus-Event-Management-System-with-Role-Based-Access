"""
Main backend logic for Campus Event Management System
"""

from typing import Dict, List, Optional
from .services.auth_services import AuthService
from .services.event_service import EventService
from .services.registration_service import RegistrationService
from .models.user import UserRole
from .utils.file_manager import FileManager


class CampusEventManager:
    """Lớp chính quản lý toàn bộ hệ thống"""
    
    def __init__(self):
        self.auth_service = AuthService()
        self.event_service = EventService()
        self.registration_service = RegistrationService()
        self.file_manager = FileManager()
    
    # ================== AUTH METHODS ==================
    
    def login(self, username: str, password: str) -> Dict:
        """Đăng nhập"""
        return self.auth_service.login(username, password)
    
    def logout(self):
        """Đăng xuất"""
        self.auth_service.logout()
    
    def register_user(self, username: str, email: str, password: str, 
                     role: str, full_name: str = "") -> Dict:
        """Đăng ký user mới"""
        try:
            user_role = UserRole(role)
            return self.auth_service.register_user(username, email, password, user_role, full_name)
        except ValueError:
            return {'success': False, 'message': 'Vai trò không hợp lệ'}
    
    def get_current_user(self):
        """Lấy user hiện tại"""
        return self.auth_service.current_user
    
    def is_authenticated(self) -> bool:
        """Kiểm tra đã đăng nhập chưa"""
        return self.auth_service.is_authenticated()
    
    def has_permission(self, action: str) -> bool:
        """Kiểm tra quyền"""
        return self.auth_service.has_permission(action)
    
    # ================== EVENT METHODS ==================
    
    def create_event(self, title: str, description: str, event_date: str,
                    location: str, max_capacity: int, category: str = "other") -> Dict:
        """Tạo sự kiện mới"""
        if not self.is_authenticated():
            return {'success': False, 'message': 'Chưa đăng nhập'}
        
        if not self.has_permission('create_event'):
            return {'success': False, 'message': 'Không có quyền tạo sự kiện'}
        
        current_user = self.get_current_user()
        return self.event_service.create_event(
            title, description, current_user.user_id, 
            event_date, location, max_capacity, category
        )
    
    def update_event(self, event_id: str, **kwargs) -> Dict:
        """Cập nhật sự kiện"""
        if not self.is_authenticated():
            return {'success': False, 'message': 'Chưa đăng nhập'}
        
        # Kiểm tra quyền
        current_user = self.get_current_user()
        event = self.event_service.get_event_by_id(event_id)
        
        if not event:
            return {'success': False, 'message': 'Không tìm thấy sự kiện'}
        
        # Admin có thể sửa tất cả, Organizer chỉ sửa event của mình
        if (current_user.role == UserRole.ADMIN or 
            (current_user.role == UserRole.ORGANIZER and event.organizer_id == current_user.user_id)):
            return self.event_service.update_event(event_id, **kwargs)
        else:
            return {'success': False, 'message': 'Không có quyền sửa sự kiện này'}
    
    def delete_event(self, event_id: str) -> Dict:
        """Xóa sự kiện"""
        if not self.is_authenticated():
            return {'success': False, 'message': 'Chưa đăng nhập'}
        
        # Kiểm tra quyền
        current_user = self.get_current_user()
        event = self.event_service.get_event_by_id(event_id)
        
        if not event:
            return {'success': False, 'message': 'Không tìm thấy sự kiện'}
        
        # Admin có thể xóa tất cả, Organizer chỉ xóa event của mình
        if (current_user.role == UserRole.ADMIN or 
            (current_user.role == UserRole.ORGANIZER and event.organizer_id == current_user.user_id)):
            
            # Hủy tất cả đăng ký trước khi xóa
            self.registration_service.bulk_cancel_event_registrations(
                event_id, "Sự kiện đã bị xóa"
            )
            
            return self.event_service.delete_event(event_id)
        else:
            return {'success': False, 'message': 'Không có quyền xóa sự kiện này'}
    
    def get_events(self, filter_own: bool = False) -> List:
        """Lấy danh sách sự kiện"""
        if filter_own and self.is_authenticated():
            current_user = self.get_current_user()
            if current_user.role == UserRole.ORGANIZER:
                return self.event_service.get_events_by_organizer(current_user.user_id)
        
        return self.event_service.get_all_events()
    
    def search_events(self, query: str = "", category: str = "", status: str = "") -> List:
        """Tìm kiếm sự kiện"""
        return self.event_service.search_events(query, category, status)
    
    def get_upcoming_events(self) -> List:
        """Lấy sự kiện sắp tới"""
        return self.event_service.get_upcoming_events()
    
    def get_popular_events(self, limit: int = 5) -> List:
        """Lấy sự kiện phổ biến"""
        return self.event_service.get_popular_events(limit)
    
    # ================== REGISTRATION METHODS ==================
    
    def register_for_event(self, event_id: str) -> Dict:
        """Đăng ký tham gia sự kiện"""
        if not self.is_authenticated():
            return {'success': False, 'message': 'Chưa đăng nhập'}
        
        current_user = self.get_current_user()
        return self.registration_service.register_for_event(event_id, current_user.user_id)
    
    def cancel_registration(self, event_id: str, reason: str = "") -> Dict:
        """Hủy đăng ký"""
        if not self.is_authenticated():
            return {'success': False, 'message': 'Chưa đăng nhập'}
        
        current_user = self.get_current_user()
        return self.registration_service.cancel_registration(
            event_id, current_user.user_id, reason
        )
    
    def get_user_registrations(self, include_cancelled: bool = False) -> List:
        """Lấy đăng ký của user hiện tại"""
        if not self.is_authenticated():
            return []
        
        current_user = self.get_current_user()
        return self.registration_service.get_user_registered_events(
            current_user.user_id, include_cancelled
        )
    
    def get_event_registrations(self, event_id: str) -> List:
        """Lấy danh sách đăng ký của một sự kiện (cho organizer/admin)"""
        if not self.is_authenticated():
            return []
        
        current_user = self.get_current_user()
        
        # Admin có thể xem tất cả, Organizer chỉ xem event của mình
        if current_user.role == UserRole.ADMIN:
            return self.registration_service.get_event_registrations(event_id)
        elif current_user.role == UserRole.ORGANIZER:
            event = self.event_service.get_event_by_id(event_id)
            if event and event.organizer_id == current_user.user_id:
                return self.registration_service.get_event_registrations(event_id)
        
        return []
    
    # ================== STATISTICS AND REPORTS ==================
    
    def get_dashboard_stats(self) -> Dict:
        """Lấy thống kê cho dashboard"""
        if not self.is_authenticated():
            return {}
        
        current_user = self.get_current_user()
        stats = {}
        
        if current_user.role == UserRole.ADMIN:
            # Admin thấy tất cả thống kê
            event_stats = self.event_service.get_event_statistics()
            reg_stats = self.registration_service.get_registration_statistics()
            
            stats = {
                'total_events': event_stats['total_events'],
                'total_attendees': event_stats['total_attendees'],
                'total_users': len(self.auth_service.get_all_users()),
                'total_registrations': reg_stats['total_registrations'],
                'event_statistics': event_stats,
                'registration_statistics': reg_stats
            }
        
        elif current_user.role == UserRole.ORGANIZER:
            # Organizer chỉ thấy thống kê sự kiện của mình
            my_events = self.event_service.get_events_by_organizer(current_user.user_id)
            total_my_attendees = sum(event.current_attendees for event in my_events)
            
            stats = {
                'my_events': len(my_events),
                'my_total_attendees': total_my_attendees,
                'my_events_list': my_events
            }
        
        elif current_user.role in [UserRole.STUDENT, UserRole.VISITOR]:
            # Student/Visitor thấy thống kê cá nhân
            my_registrations = self.get_user_registrations()
            
            stats = {
                'my_registrations': len(my_registrations),
                'upcoming_events': len(self.get_upcoming_events()),
                'registered_events': my_registrations
            }
        
        return stats
    
    def export_events_report(self) -> Dict:
        """Xuất báo cáo sự kiện"""
        if not self.has_permission('generate_reports'):
            return {'success': False, 'message': 'Không có quyền tạo báo cáo'}
        
        try:
            events = self.event_service.get_all_events()
            
            # Chuẩn bị dữ liệu cho CSV
            report_data = []
            for event in events:
                organizer = self.auth_service.get_user_by_id(event.organizer_id)
                report_data.append({
                    'Event ID': event.event_id,
                    'Title': event.title,
                    'Description': event.description[:100] + '...' if len(event.description) > 100 else event.description,
                    'Organizer': organizer.full_name if organizer else 'Unknown',
                    'Date': event.event_date,
                    'Location': event.location,
                    'Category': event.category.value,
                    'Max Capacity': event.max_capacity,
                    'Current Attendees': event.current_attendees,
                    'Status': event.status.value,
                    'Availability %': f"{event.get_availability_percentage():.1f}%"
                })
            
            filename = self.file_manager.generate_report_filename('events')
            success = self.file_manager.export_to_csv(filename, report_data)
            
            return {
                'success': success,
                'message': 'Xuất báo cáo thành công' if success else 'Lỗi xuất báo cáo',
                'filename': filename if success else None
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Lỗi xuất báo cáo: {str(e)}'}
    
    def export_registrations_report(self) -> Dict:
        """Xuất báo cáo đăng ký"""
        if not self.has_permission('generate_reports'):
            return {'success': False, 'message': 'Không có quyền tạo báo cáo'}
        
        try:
            registrations = self.registration_service.get_all_registrations()
            
            # Chuẩn bị dữ liệu cho CSV
            report_data = []
            for reg in registrations:
                event = self.event_service.get_event_by_id(reg.event_id)
                user = self.auth_service.get_user_by_id(reg.user_id)
                
                report_data.append({
                    'Registration ID': reg.registration_id,
                    'Event Title': event.title if event else 'Unknown Event',
                    'User Name': user.full_name if user else 'Unknown User',
                    'User Email': user.email if user else 'Unknown',
                    'Registration Date': reg.registered_at,
                    'Status': reg.get_status_display(),
                    'Notes': reg.notes
                })
            
            filename = self.file_manager.generate_report_filename('registrations')
            success = self.file_manager.export_to_csv(filename, report_data)
            
            return {
                'success': success,
                'message': 'Xuất báo cáo thành công' if success else 'Lỗi xuất báo cáo',
                'filename': filename if success else None
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Lỗi xuất báo cáo: {str(e)}'}
    
    # ================== UTILITY METHODS ==================
    
    def backup_system_data(self) -> Dict:
        """Sao lưu dữ liệu hệ thống"""
        if not self.has_permission('generate_reports'):
            return {'success': False, 'message': 'Không có quyền sao lưu'}
        
        results = self.file_manager.backup_data()
        success = all(results.values())
        
        return {
            'success': success,
            'message': 'Sao lưu thành công' if success else 'Một số file không sao lưu được',
            'details': results
        }
    
    def get_system_info(self) -> Dict:
        """Lấy thông tin hệ thống"""
        return {
            'total_users': len(self.auth_service.get_all_users()),
            'total_events': len(self.event_service.get_all_events()),
            'total_registrations': len(self.registration_service.get_all_registrations()),
            'is_authenticated': self.is_authenticated(),
            'current_user': self.get_current_user().to_dict() if self.is_authenticated() else None
        }