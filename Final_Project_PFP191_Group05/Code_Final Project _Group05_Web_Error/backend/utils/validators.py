"""
Validators for Campus Event Management System
"""

import re
from datetime import datetime, date
from typing import Dict


class EventValidator:
    """Validator cho dữ liệu sự kiện"""
    
    @staticmethod
    def validate_event_data(title: str, description: str, event_date: str, 
                          location: str, max_capacity: int) -> Dict:
        """Validate dữ liệu sự kiện"""
        
        # Validate title
        if not title or not title.strip():
            return {'valid': False, 'message': 'Tên sự kiện không được để trống'}
        
        if len(title.strip()) < 3:
            return {'valid': False, 'message': 'Tên sự kiện phải có ít nhất 3 ký tự'}
        
        if len(title.strip()) > 200:
            return {'valid': False, 'message': 'Tên sự kiện không được quá 200 ký tự'}
        
        # Validate description
        if not description or not description.strip():
            return {'valid': False, 'message': 'Mô tả sự kiện không được để trống'}
        
        if len(description.strip()) < 10:
            return {'valid': False, 'message': 'Mô tả sự kiện phải có ít nhất 10 ký tự'}
        
        if len(description.strip()) > 1000:
            return {'valid': False, 'message': 'Mô tả sự kiện không được quá 1000 ký tự'}
        
        # Validate event_date
        date_validation = EventValidator.validate_event_date(event_date)
        if not date_validation['valid']:
            return date_validation
        
        # Validate location
        if not location or not location.strip():
            return {'valid': False, 'message': 'Địa điểm không được để trống'}
        
        if len(location.strip()) < 3:
            return {'valid': False, 'message': 'Địa điểm phải có ít nhất 3 ký tự'}
        
        if len(location.strip()) > 200:
            return {'valid': False, 'message': 'Địa điểm không được quá 200 ký tự'}
        
        # Validate max_capacity
        capacity_validation = EventValidator.validate_capacity(max_capacity)
        if not capacity_validation['valid']:
            return capacity_validation
        
        return {'valid': True, 'message': 'Dữ liệu hợp lệ'}
    
    @staticmethod
    def validate_event_date(event_date: str) -> Dict:
        """Validate ngày sự kiện"""
        try:
            # Thử parse ngày theo format ISO
            event_datetime = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
            
            # Kiểm tra ngày không được trong quá khứ
            if event_datetime <= datetime.now():
                return {
                    'valid': False, 
                    'message': 'Ngày sự kiện phải là thời gian trong tương lai'
                }
            
            # Kiểm tra ngày không được quá xa (1 năm)
            one_year_later = datetime.now().replace(year=datetime.now().year + 1)
            if event_datetime > one_year_later:
                return {
                    'valid': False,
                    'message': 'Ngày sự kiện không được quá 1 năm từ hiện tại'
                }
            
            return {'valid': True, 'message': 'Ngày hợp lệ'}
            
        except ValueError:
            return {
                'valid': False, 
                'message': 'Định dạng ngày không hợp lệ. Vui lòng sử dụng định dạng ISO (YYYY-MM-DDTHH:MM:SS)'
            }
    
    @staticmethod
    def validate_capacity(max_capacity: int) -> Dict:
        """Validate sức chứa sự kiện"""
        if not isinstance(max_capacity, int):
            try:
                max_capacity = int(max_capacity)
            except (ValueError, TypeError):
                return {'valid': False, 'message': 'Sức chứa phải là số nguyên'}
        
        if max_capacity <= 0:
            return {'valid': False, 'message': 'Sức chứa phải lớn hơn 0'}
        
        if max_capacity > 10000:
            return {'valid': False, 'message': 'Sức chứa không được vượt quá 10,000 người'}
        
        return {'valid': True, 'message': 'Sức chứa hợp lệ'}


class UserValidator:
    """Validator cho dữ liệu người dùng"""
    
    @staticmethod
    def validate_username(username: str) -> Dict:
        """Validate username"""
        if not username or not username.strip():
            return {'valid': False, 'message': 'Tên đăng nhập không được để trống'}
        
        username = username.strip()
        
        if len(username) < 3:
            return {'valid': False, 'message': 'Tên đăng nhập phải có ít nhất 3 ký tự'}
        
        if len(username) > 50:
            return {'valid': False, 'message': 'Tên đăng nhập không được quá 50 ký tự'}
        
        # Chỉ cho phép chữ cái, số và dấu gạch dưới
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return {
                'valid': False, 
                'message': 'Tên đăng nhập chỉ được chứa chữ cái, số và dấu gạch dưới'
            }
        
        return {'valid': True, 'message': 'Tên đăng nhập hợp lệ'}
    
    @staticmethod
    def validate_email(email: str) -> Dict:
        """Validate email"""
        if not email or not email.strip():
            return {'valid': False, 'message': 'Email không được để trống'}
        
        email = email.strip()
        
        # Pattern đơn giản để validate email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return {'valid': False, 'message': 'Định dạng email không hợp lệ'}
        
        if len(email) > 100:
            return {'valid': False, 'message': 'Email không được quá 100 ký tự'}
        
        return {'valid': True, 'message': 'Email hợp lệ'}
    
    @staticmethod
    def validate_password(password: str) -> Dict:
        """Validate password"""
        if not password:
            return {'valid': False, 'message': 'Mật khẩu không được để trống'}
        
        if len(password) < 6:
            return {'valid': False, 'message': 'Mật khẩu phải có ít nhất 6 ký tự'}
        
        if len(password) > 100:
            return {'valid': False, 'message': 'Mật khẩu không được quá 100 ký tự'}
        
        # Kiểm tra có ít nhất 1 chữ cái và 1 số
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if not (has_letter and has_digit):
            return {
                'valid': False, 
                'message': 'Mật khẩu phải chứa ít nhất 1 chữ cái và 1 số'
            }
        
        return {'valid': True, 'message': 'Mật khẩu hợp lệ'}
    
    @staticmethod
    def validate_full_name(full_name: str) -> Dict:
        """Validate họ tên"""
        if not full_name or not full_name.strip():
            return {'valid': False, 'message': 'Họ tên không được để trống'}
        
        full_name = full_name.strip()
        
        if len(full_name) < 2:
            return {'valid': False, 'message': 'Họ tên phải có ít nhất 2 ký tự'}
        
        if len(full_name) > 100:
            return {'valid': False, 'message': 'Họ tên không được quá 100 ký tự'}
        
        # Chỉ cho phép chữ cái và khoảng trắng
        if not re.match(r'^[a-zA-ZÀ-ỹ\s]+$', full_name):
            return {
                'valid': False, 
                'message': 'Họ tên chỉ được chứa chữ cái và khoảng trắng'
            }
        
        return {'valid': True, 'message': 'Họ tên hợp lệ'}


class SearchValidator:
    """Validator cho tìm kiếm"""
    
    @staticmethod
    def validate_search_query(query: str) -> Dict:
        """Validate query tìm kiếm"""
        if not query:
            return {'valid': True, 'message': 'Query rỗng hợp lệ'}
        
        query = query.strip()
        
        if len(query) > 200:
            return {'valid': False, 'message': 'Từ khóa tìm kiếm không được quá 200 ký tự'}
        
        # Không cho phép các ký tự đặc biệt nguy hiểm
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
        if any(char in query for char in dangerous_chars):
            return {
                'valid': False, 
                'message': 'Từ khóa tìm kiếm chứa ký tự không hợp lệ'
            }
        
        return {'valid': True, 'message': 'Query tìm kiếm hợp lệ'}