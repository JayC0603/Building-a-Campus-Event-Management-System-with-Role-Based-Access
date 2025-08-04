"""
User Models Module

This module contains all user-related classes with role-based access control.
Implements inheritance hierarchy for different user types.
"""

import uuid
from datetime import datetime
from abc import ABC, abstractmethod

class User(ABC):
    """Abstract base class for all user types"""
    
    def __init__(self, username, password, name, email):
        """Initialize base user with common attributes"""
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.password = password  # In production, this should be hashed
        self.name = name
        self.email = email
        self.created_at = datetime.now().isoformat()
        self.registered_events = []  # List of event IDs user is registered for
    
    @abstractmethod
    def get_role(self):
        """Return the user's role as a string"""
        pass
    
    def can_create_events(self):
        """Check if user can create events"""
        return False
    
    def can_manage_all_events(self):
        """Check if user can manage all events"""
        return False
    
    def can_view_all_attendees(self):
        """Check if user can view all attendees"""
        return False
    
    def authenticate(self, password):
        """Authenticate user with password"""
        return self.password == password
    
    def add_registered_event(self, event_id):
        """Add event to user's registered events"""
        if event_id not in self.registered_events:
            self.registered_events.append(event_id)
            return True
        return False
    
    def remove_registered_event(self, event_id):
        """Remove event from user's registered events"""
        if event_id in self.registered_events:
            self.registered_events.remove(event_id)
            return True
        return False
    
    def to_dict(self):
        """Convert user to dictionary for serialization"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at,
            'registered_events': self.registered_events,
            'user_type': self.get_role().lower().replace(' ', '_')
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user instance from dictionary"""
        # This is overridden in child classes
        pass
    
    def __str__(self):
        return f"{self.name} ({self.username}) - {self.get_role()}"


class Admin(User):
    """Administrator user with full system access"""
    
    def __init__(self, username, password, name, email):
        super().__init__(username, password, name, email)
    
    def get_role(self):
        return "Admin"
    
    def can_create_events(self):
        return True
    
    def can_manage_all_events(self):
        return True
    
    def can_view_all_attendees(self):
        return True
    
    def can_manage_users(self):
        return True
    
    @classmethod
    def from_dict(cls, data):
        """Create Admin instance from dictionary"""
        admin = cls(data['username'], data['password'], data['name'], data['email'])
        admin.user_id = data['user_id']
        admin.created_at = data['created_at']
        admin.registered_events = data.get('registered_events', [])
        return admin


class EventOrganizer(User):
    """Event organizer with event management capabilities"""
    
    def __init__(self, username, password, name, email, department):
        super().__init__(username, password, name, email)
        self.department = department
        self.organized_events = []  # List of event IDs organized by this user
    
    def get_role(self):
        return "Event Organizer"
    
    def can_create_events(self):
        return True
    
    def can_manage_own_events(self):
        return True
    
    def add_organized_event(self, event_id):
        """Add event to organizer's organized events"""
        if event_id not in self.organized_events:
            self.organized_events.append(event_id)
            return True
        return False
    
    def remove_organized_event(self, event_id):
        """Remove event from organizer's organized events"""
        if event_id in self.organized_events:
            self.organized_events.remove(event_id)
            return True
        return False
    
    def to_dict(self):
        """Convert organizer to dictionary for serialization"""
        data = super().to_dict()
        data.update({
            'department': self.department,
            'organized_events': self.organized_events
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create EventOrganizer instance from dictionary"""
        organizer = cls(data['username'], data['password'], data['name'], 
                       data['email'], data['department'])
        organizer.user_id = data['user_id']
        organizer.created_at = data['created_at']
        organizer.registered_events = data.get('registered_events', [])
        organizer.organized_events = data.get('organized_events', [])
        return organizer


class Student(User):
    """Student user with basic event access"""
    
    def __init__(self, username, password, name, email, student_id):
        super().__init__(username, password, name, email)
        self.student_id = student_id
    
    def get_role(self):
        return "Student"
    
    def to_dict(self):
        """Convert student to dictionary for serialization"""
        data = super().to_dict()
        data['student_id'] = self.student_id
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create Student instance from dictionary"""
        student = cls(data['username'], data['password'], data['name'], 
                     data['email'], data['student_id'])
        student.user_id = data['user_id']
        student.created_at = data['created_at']
        student.registered_events = data.get('registered_events', [])
        return student


class Visitor(User):
    """Visitor user with basic event access"""
    
    def __init__(self, username, password, name, email, organization=None):
        super().__init__(username, password, name, email)
        self.organization = organization
    
    def get_role(self):
        return "Visitor"
    
    def to_dict(self):
        """Convert visitor to dictionary for serialization"""
        data = super().to_dict()
        data['organization'] = self.organization
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create Visitor instance from dictionary"""
        visitor = cls(data['username'], data['password'], data['name'], 
                     data['email'], data.get('organization'))
        visitor.user_id = data['user_id']
        visitor.created_at = data['created_at']
        visitor.registered_events = data.get('registered_events', [])
        return visitor


class UserFactory:
    """Factory class for creating user instances"""
    
    @staticmethod
    def create_user(user_type, **kwargs):
        """Create user instance based on type"""
        user_types = {
            'admin': Admin,
            'event_organizer': EventOrganizer,
            'student': Student,
            'visitor': Visitor
        }
        
        user_class = user_types.get(user_type.lower())
        if not user_class:
            raise ValueError(f"Unknown user type: {user_type}")
        
        return user_class(**kwargs)
    
    @staticmethod
    def from_dict(data):
        """Create user instance from dictionary"""
        user_type = data.get('user_type')
        
        if user_type == 'admin':
            return Admin.from_dict(data)
        elif user_type == 'event_organizer':
            return EventOrganizer.from_dict(data)
        elif user_type == 'student':
            return Student.from_dict(data)
        elif user_type == 'visitor':
            return Visitor.from_dict(data)
        else:
            raise ValueError(f"Unknown user type: {user_type}")


# Utility functions for user management
def hash_password(password):
    """Hash password for secure storage (simplified for demo)"""
    # In production, use proper hashing like bcrypt
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed