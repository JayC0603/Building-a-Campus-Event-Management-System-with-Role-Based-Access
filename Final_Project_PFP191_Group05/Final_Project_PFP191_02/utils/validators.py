"""
Input Validation Utilities Module

This module provides validation functions for user inputs,
ensuring data integrity and security throughout the system.
"""

import re
from datetime import datetime, date
from typing import Union, List, Dict, Any

class InputValidator:
    """Static class for input validation methods"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if email format is valid
        """
        if not email or not isinstance(email, str):
            return False
        
        # Basic email pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email.strip()) is not None
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        """
        Validate date format (YYYY-MM-DD)
        
        Args:
            date_str (str): Date string to validate
            
        Returns:
            bool: True if date format is valid
        """
        if not date_str or not isinstance(date_str, str):
            return False
        
        try:
            datetime.strptime(date_str.strip(), '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_time(time_str: str) -> bool:
        """
        Validate time format (HH:MM)
        
        Args:
            time_str (str): Time string to validate
            
        Returns:
            bool: True if time format is valid
        """
        if not time_str or not isinstance(time_str, str):
            return False
        
        try:
            datetime.strptime(time_str.strip(), '%H:%M')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_username(username: str) -> Dict[str, Union[bool, str]]:
        """
        Validate username with detailed feedback
        
        Args:
            username (str): Username to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not username or not isinstance(username, str):
            return {'valid': False, 'message': 'Username is required'}
        
        username = username.strip()
        
        if len(username) < 3:
            return {'valid': False, 'message': 'Username must be at least 3 characters long'}
        
        if len(username) > 50:
            return {'valid': False, 'message': 'Username must be less than 50 characters'}
        
        # Allow letters, numbers, underscores, and hyphens
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return {'valid': False, 'message': 'Username can only contain letters, numbers, underscores, and hyphens'}
        
        # Must start with a letter
        if not username[0].isalpha():
            return {'valid': False, 'message': 'Username must start with a letter'}
        
        return {'valid': True, 'message': 'Valid username'}
    
    @staticmethod
    def validate_password(password: str) -> Dict[str, Union[bool, str, List[str]]]:
        """
        Validate password strength with detailed feedback
        
        Args:
            password (str): Password to validate
            
        Returns:
            dict: Validation result with status, message, and suggestions
        """
        if not password or not isinstance(password, str):
            return {
                'valid': False, 
                'message': 'Password is required',
                'suggestions': ['Password cannot be empty']
            }
        
        suggestions = []
        
        if len(password) < 6:
            suggestions.append('Password must be at least 6 characters long')
        
        if len(password) > 128:
            suggestions.append('Password must be less than 128 characters')
        
        if not re.search(r'[a-z]', password):
            suggestions.append('Include at least one lowercase letter')
        
        if not re.search(r'[A-Z]', password):
            suggestions.append('Include at least one uppercase letter')
        
        if not re.search(r'\d', password):
            suggestions.append('Include at least one number')
        
        # Check for common weak passwords
        weak_passwords = ['password', '123456', 'qwerty', 'admin', 'user']
        if password.lower() in weak_passwords:
            suggestions.append('Avoid common passwords')
        
        is_valid = len(suggestions) == 0
        message = 'Strong password' if is_valid else f'{len(suggestions)} issues found'
        
        return {
            'valid': is_valid,
            'message': message,
            'suggestions': suggestions
        }
    
    @staticmethod
    def validate_name(name: str) -> Dict[str, Union[bool, str]]:
        """
        Validate person's name
        
        Args:
            name (str): Name to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not name or not isinstance(name, str):
            return {'valid': False, 'message': 'Name is required'}
        
        name = name.strip()
        
        if len(name) < 2:
            return {'valid': False, 'message': 'Name must be at least 2 characters long'}
        
        if len(name) > 100:
            return {'valid': False, 'message': 'Name must be less than 100 characters'}
        
        # Allow letters, spaces, hyphens, apostrophes
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            return {'valid': False, 'message': 'Name can only contain letters, spaces, hyphens, and apostrophes'}
        
        return {'valid': True, 'message': 'Valid name'}
    
    @staticmethod
    def validate_capacity(capacity: Union[str, int]) -> Dict[str, Union[bool, str, int]]:
        """
        Validate event capacity
        
        Args:
            capacity: Capacity value to validate
            
        Returns:
            dict: Validation result with status, message, and parsed value
        """
        try:
            if isinstance(capacity, str):
                capacity_int = int(capacity.strip())
            else:
                capacity_int = int(capacity)
            
            if capacity_int <= 0:
                return {'valid': False, 'message': 'Capacity must be greater than 0', 'value': None}
            
            if capacity_int > 10000:
                return {'valid': False, 'message': 'Capacity cannot exceed 10,000', 'value': None}
            
            return {'valid': True, 'message': 'Valid capacity', 'value': capacity_int}
        
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Capacity must be a valid number', 'value': None}
    
    @staticmethod
    def validate_student_id(student_id: str) -> Dict[str, Union[bool, str]]:
        """
        Validate student ID format
        
        Args:
            student_id (str): Student ID to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not student_id or not isinstance(student_id, str):
            return {'valid': False, 'message': 'Student ID is required'}
        
        student_id = student_id.strip()
        
        if len(student_id) < 3:
            return {'valid': False, 'message': 'Student ID must be at least 3 characters long'}
        
        if len(student_id) > 20:
            return {'valid': False, 'message': 'Student ID must be less than 20 characters'}
        
        # Allow letters and numbers
        if not re.match(r'^[a-zA-Z0-9]+$', student_id):
            return {'valid': False, 'message': 'Student ID can only contain letters and numbers'}
        
        return {'valid': True, 'message': 'Valid student ID'}
    
    @staticmethod
    def validate_event_name(name: str) -> Dict[str, Union[bool, str]]:
        """
        Validate event name
        
        Args:
            name (str): Event name to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not name or not isinstance(name, str):
            return {'valid': False, 'message': 'Event name is required'}
        
        name = name.strip()
        
        if len(name) < 3:
            return {'valid': False, 'message': 'Event name must be at least 3 characters long'}
        
        if len(name) > 200:
            return {'valid': False, 'message': 'Event name must be less than 200 characters'}
        
        # Basic sanitization check
        if re.search(r'[<>"\']', name):
            return {'valid': False, 'message': 'Event name contains invalid characters'}
        
        return {'valid': True, 'message': 'Valid event name'}
    
    @staticmethod
    def validate_location(location: str) -> Dict[str, Union[bool, str]]:
        """
        Validate event location
        
        Args:
            location (str): Location to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not location or not isinstance(location, str):
            return {'valid': False, 'message': 'Location is required'}
        
        location = location.strip()
        
        if len(location) < 2:
            return {'valid': False, 'message': 'Location must be at least 2 characters long'}
        
        if len(location) > 200:
            return {'valid': False, 'message': 'Location must be less than 200 characters'}
        
        return {'valid': True, 'message': 'Valid location'}
    
    @staticmethod
    def validate_description(description: str) -> Dict[str, Union[bool, str]]:
        """
        Validate event description
        
        Args:
            description (str): Description to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not description or not isinstance(description, str):
            return {'valid': True, 'message': 'Description is optional'}  # Description is optional
        
        description = description.strip()
        
        if len(description) > 1000:
            return {'valid': False, 'message': 'Description must be less than 1000 characters'}
        
        return {'valid': True, 'message': 'Valid description'}
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Dict[str, Union[bool, str]]:
        """
        Validate date range
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            dict: Validation result with status and message
        """
        if not InputValidator.validate_date(start_date):
            return {'valid': False, 'message': 'Invalid start date format'}
        
        if not InputValidator.validate_date(end_date):
            return {'valid': False, 'message': 'Invalid end date format'}
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if start > end:
                return {'valid': False, 'message': 'Start date must be before end date'}
            
            return {'valid': True, 'message': 'Valid date range'}
        
        except ValueError:
            return {'valid': False, 'message': 'Invalid date format'}
    
    @staticmethod
    def validate_future_date(date_str: str) -> Dict[str, Union[bool, str]]:
        """
        Validate that date is in the future
        
        Args:
            date_str (str): Date string to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not InputValidator.validate_date(date_str):
            return {'valid': False, 'message': 'Invalid date format'}
        
        try:
            event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            today = date.today()
            
            if event_date < today:
                return {'valid': False, 'message': 'Event date must be in the future'}
            
            # Check if date is too far in the future (e.g., more than 2 years)
            max_future_date = date(today.year + 2, today.month, today.day)
            if event_date > max_future_date:
                return {'valid': False, 'message': 'Event date cannot be more than 2 years in the future'}
            
            return {'valid': True, 'message': 'Valid future date'}
        
        except ValueError:
            return {'valid': False, 'message': 'Invalid date format'}
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """
        Sanitize user input by removing potentially harmful characters
        
        Args:
            input_str (str): Input string to sanitize
            
        Returns:
            str: Sanitized string
        """
        if not input_str or not isinstance(input_str, str):
            return ""
        
        # Remove potentially harmful characters
        sanitized = re.sub(r'[<>"\';\\]', '', input_str)
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    @staticmethod
    def validate_search_query(query: str) -> Dict[str, Union[bool, str]]:
        """
        Validate search query
        
        Args:
            query (str): Search query to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not query or not isinstance(query, str):
            return {'valid': False, 'message': 'Search query cannot be empty'}
        
        query = query.strip()
        
        if len(query) < 1:
            return {'valid': False, 'message': 'Search query must be at least 1 character long'}
        
        if len(query) > 100:
            return {'valid': False, 'message': 'Search query must be less than 100 characters'}
        
        return {'valid': True, 'message': 'Valid search query'}
    
    @staticmethod
    def validate_phone_number(phone: str) -> Dict[str, Union[bool, str]]:
        """
        Validate phone number format (optional field)
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not phone or not isinstance(phone, str):
            return {'valid': True, 'message': 'Phone number is optional'}
        
        phone = phone.strip()
        
        # Remove common separators for validation
        phone_digits = re.sub(r'[\s\-\(\)\+]', '', phone)
        
        if not phone_digits.isdigit():
            return {'valid': False, 'message': 'Phone number can only contain digits and separators'}
        
        if len(phone_digits) < 10 or len(phone_digits) > 15:
            return {'valid': False, 'message': 'Phone number must be between 10 and 15 digits'}
        
        return {'valid': True, 'message': 'Valid phone number'}
    
    @staticmethod
    def validate_department(department: str) -> Dict[str, Union[bool, str]]:
        """
        Validate department name
        
        Args:
            department (str): Department to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not department or not isinstance(department, str):
            return {'valid': False, 'message': 'Department is required'}
        
        department = department.strip()
        
        if len(department) < 2:
            return {'valid': False, 'message': 'Department must be at least 2 characters long'}
        
        if len(department) > 100:
            return {'valid': False, 'message': 'Department must be less than 100 characters'}
        
        # Allow letters, spaces, hyphens, and ampersands
        if not re.match(r"^[a-zA-Z\s\-&]+$", department):
            return {'valid': False, 'message': 'Department can only contain letters, spaces, hyphens, and ampersands'}
        
        return {'valid': True, 'message': 'Valid department'}
    
    @staticmethod
    def validate_organization(organization: str) -> Dict[str, Union[bool, str]]:
        """
        Validate organization name (optional field)
        
        Args:
            organization (str): Organization to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not organization or not isinstance(organization, str):
            return {'valid': True, 'message': 'Organization is optional'}
        
        organization = organization.strip()
        
        if len(organization) > 100:
            return {'valid': False, 'message': 'Organization must be less than 100 characters'}
        
        return {'valid': True, 'message': 'Valid organization'}
    
    @staticmethod
    def validate_bulk_data(data: List[Dict[str, Any]], required_fields: List[str]) -> Dict[str, Any]:
        """
        Validate bulk data import
        
        Args:
            data (List[dict]): List of data dictionaries to validate
            required_fields (List[str]): List of required field names
            
        Returns:
            dict: Validation summary with errors and warnings
        """
        results = {
            'valid_count': 0,
            'invalid_count': 0,
            'errors': [],
            'warnings': []
        }
        
        for i, item in enumerate(data):
            row_errors = []
            
            # Check required fields
            for field in required_fields:
                if field not in item or not item[field]:
                    row_errors.append(f"Missing required field: {field}")
            
            # Validate specific fields if present
            if 'email' in item and item['email']:
                if not InputValidator.validate_email(item['email']):
                    row_errors.append("Invalid email format")
            
            if 'date' in item and item['date']:
                if not InputValidator.validate_date(item['date']):
                    row_errors.append("Invalid date format")
            
            if 'capacity' in item and item['capacity']:
                capacity_result = InputValidator.validate_capacity(item['capacity'])
                if not capacity_result['valid']:
                    row_errors.append(f"Invalid capacity: {capacity_result['message']}")
            
            if row_errors:
                results['invalid_count'] += 1
                results['errors'].append(f"Row {i+1}: {'; '.join(row_errors)}")
            else:
                results['valid_count'] += 1
        
        return results


class SecurityValidator:
    """Security-focused validation methods"""
    
    @staticmethod
    def check_sql_injection(input_str: str) -> bool:
        """
        Check for potential SQL injection patterns
        
        Args:
            input_str (str): Input to check
            
        Returns:
            bool: True if input appears safe
        """
        if not input_str or not isinstance(input_str, str):
            return True
        
        # Common SQL injection patterns
        dangerous_patterns = [
            r"(\bOR\b|\bAND\b).*=.*",
            r"UNION.*SELECT",
            r"DROP.*TABLE",
            r"INSERT.*INTO",
            r"DELETE.*FROM",
            r"UPDATE.*SET",
            r"--",
            r"/\*.*\*/",
            r"'.*'",
            r'".*"'
        ]
        
        input_upper = input_str.upper()
        
        for pattern in dangerous_patterns:
            if re.search(pattern, input_upper):
                return False
        
        return True
    
    @staticmethod
    def check_xss_patterns(input_str: str) -> bool:
        """
        Check for potential XSS patterns
        
        Args:
            input_str (str): Input to check
            
        Returns:
            bool: True if input appears safe
        """
        if not input_str or not isinstance(input_str, str):
            return True
        
        # Common XSS patterns
        dangerous_patterns = [
            r"<script.*?>.*?</script>",
            r"javascript:",
            r"onload\s*=",
            r"onerror\s*=",
            r"onclick\s*=",
            r"<iframe.*?>",
            r"<object.*?>",
            r"<embed.*?>"
        ]
        
        input_lower = input_str.lower()
        
        for pattern in dangerous_patterns:
            if re.search(pattern, input_lower):
                return False
        
        return True