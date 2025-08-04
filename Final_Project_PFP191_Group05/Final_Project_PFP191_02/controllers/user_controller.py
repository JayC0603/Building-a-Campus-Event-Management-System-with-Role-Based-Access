"""
User Controller Module

This module handles all user-related business logic and operations.
Manages user CRUD operations, authentication support, and user statistics.
"""

from typing import List, Dict, Any, Optional
from models.user import User, Admin, EventOrganizer, Student, Visitor

class UserController:
    """Controller for managing users and user-related operations"""
    
    def __init__(self, file_manager=None):
        """
        Initialize user controller
        
        Args:
            file_manager: File manager instance for persistence
        """
        self.users = []  # List of User objects
        self.file_manager = file_manager
    
    def add_user(self, user: User) -> bool:
        """
        Add a new user to the system
        
        Args:
            user (User): User object to add
            
        Returns:
            bool: True if user added successfully
        """
        try:
            # Check for duplicate username
            if self.get_user_by_username(user.username):
                print(f"Username '{user.username}' already exists")
                return False
            
            # Check for duplicate email
            if self.get_user_by_email(user.email):
                print(f"Email '{user.email}' already exists")
                return False
            
            self.users.append(user)
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id (str): User ID to search for
            
        Returns:
            User or None: User object if found
        """
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username
        
        Args:
            username (str): Username to search for
            
        Returns:
            User or None: User object if found
        """
        for user in self.users:
            if user.username.lower() == username.lower():
                return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            email (str): Email to search for
            
        Returns:
            User or None: User object if found
        """
        for user in self.users:
            if user.email.lower() == email.lower():
                return user
        return None
    
    def get_all_users(self) -> List[User]:
        """
        Get all users in the system
        
        Returns:
            List[User]: List of all users
        """
        return self.users.copy()
    
    def get_users_by_role(self, role: str) -> List[User]:
        """
        Get all users with a specific role
        
        Args:
            role (str): Role to filter by (admin, event_organizer, student, visitor)
            
        Returns:
            List[User]: List of users with specified role
        """
        role_classes = {
            'admin': Admin,
            'event_organizer': EventOrganizer,
            'student': Student,
            'visitor': Visitor
        }
        
        target_class = role_classes.get(role.lower())
        if not target_class:
            return []
        
        return [user for user in self.users if isinstance(user, target_class)]
    
    def update_user(self, user_id: str, **updates) -> bool:
        """
        Update user details
        
        Args:
            user_id (str): User ID to update
            **updates: Fields to update
            
        Returns:
            bool: True if update successful
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        try:
            # Check for username conflicts if updating username
            if 'username' in updates:
                new_username = updates['username']
                existing_user = self.get_user_by_username(new_username)
                if existing_user and existing_user.user_id != user_id:
                    print(f"Username '{new_username}' already exists")
                    return False
            
            # Check for email conflicts if updating email
            if 'email' in updates:
                new_email = updates['email']
                existing_user = self.get_user_by_email(new_email)
                if existing_user and existing_user.user_id != user_id:
                    print(f"Email '{new_email}' already exists")
                    return False
            
            # Update allowed fields
            allowed_fields = ['username', 'name', 'email', 'password']
            
            # Add role-specific fields
            if isinstance(user, Student):
                allowed_fields.append('student_id')
            elif isinstance(user, EventOrganizer):
                allowed_fields.append('department')
            elif isinstance(user, Visitor):
                allowed_fields.append('organization')
            
            for field, value in updates.items():
                if field in allowed_fields and hasattr(user, field):
                    setattr(user, field, value)
            
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user from the system
        
        Args:
            user_id (str): User ID to delete
            
        Returns:
            bool: True if deletion successful
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        try:
            self.users.remove(user)
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            User or None: User object if authentication successful
        """
        user = self.get_user_by_username(username)
        if user and user.authenticate(password):
            return user
        return None
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """
        Change user password
        
        Args:
            user_id (str): User ID
            old_password (str): Current password
            new_password (str): New password
            
        Returns:
            bool: True if password changed successfully
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        if not user.authenticate(old_password):
            print("Current password is incorrect")
            return False
        
        if len(new_password) < 6:
            print("New password must be at least 6 characters long")
            return False
        
        user.password = new_password
        return True
    
    def get_user_statistics(self) -> Dict[str, int]:
        """
        Get user statistics by role
        
        Returns:
            dict: User count by role
        """
        stats = {
            'admin': 0,
            'event_organizer': 0,
            'student': 0,
            'visitor': 0,
            'total': len(self.users)
        }
        
        for user in self.users:
            if isinstance(user, Admin):
                stats['admin'] += 1
            elif isinstance(user, EventOrganizer):
                stats['event_organizer'] += 1
            elif isinstance(user, Student):
                stats['student'] += 1
            elif isinstance(user, Visitor):
                stats['visitor'] += 1
        
        return stats
    
    def search_users(self, query: str) -> List[User]:
        """
        Search users by name, username, or email
        
        Args:
            query (str): Search query
            
        Returns:
            List[User]: List of matching users
        """
        if not query.strip():
            return []
        
        query_lower = query.lower().strip()
        matching_users = []
        
        for user in self.users:
            if (query_lower in user.name.lower() or 
                query_lower in user.username.lower() or 
                query_lower in user.email.lower()):
                matching_users.append(user)
        
        return matching_users
    
    def get_active_users(self, days: int = 30) -> List[User]:
        """
        Get users who have registered for events recently
        
        Args:
            days (int): Number of days to look back
            
        Returns:
            List[User]: List of active users
        """
        # This would require event participation data
        # For now, return users who have registered events
        active_users = [user for user in self.users if user.registered_events]
        return active_users
    
    def get_organizers_with_events(self) -> List[EventOrganizer]:
        """
        Get event organizers who have organized events
        
        Returns:
            List[EventOrganizer]: List of organizers with events
        """
        organizers = self.get_users_by_role('event_organizer')
        active_organizers = []
        
        for organizer in organizers:
            if hasattr(organizer, 'organized_events') and organizer.organized_events:
                active_organizers.append(organizer)
        
        return active_organizers
    
    def get_user_engagement_report(self) -> Dict[str, Any]:
        """
        Generate user engagement report
        
        Returns:
            dict: User engagement statistics
        """
        total_users = len(self.users)
        users_with_registrations = len([u for u in self.users if u.registered_events])
        
        # Calculate average registrations per user
        total_registrations = sum(len(u.registered_events) for u in self.users)
        avg_registrations = total_registrations / total_users if total_users > 0 else 0
        
        # Get most active user
        most_active_user = max(self.users, 
                             key=lambda u: len(u.registered_events)) if self.users else None
        
        return {
            'total_users': total_users,
            'users_with_registrations': users_with_registrations,
            'engagement_rate': (users_with_registrations / total_users * 100) if total_users > 0 else 0,
            'total_registrations': total_registrations,
            'avg_registrations_per_user': round(avg_registrations, 2),
            'most_active_user': {
                'name': most_active_user.name,
                'registrations': len(most_active_user.registered_events)
            } if most_active_user else None
        }
    
    def validate_user_data(self, user_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Validate user data for creation/update
        
        Args:
            user_data (dict): User data to validate
            
        Returns:
            dict: Validation errors (empty if valid)
        """
        errors = {}
        
        # Required fields
        required_fields = ['username', 'password', 'name', 'email']
        for field in required_fields:
            if not user_data.get(field, '').strip():
                errors[field] = f"{field.title()} is required"
        
        # Username validation
        username = user_data.get('username', '')
        if username and len(username) < 3:
            errors['username'] = "Username must be at least 3 characters long"
        
        # Password validation
        password = user_data.get('password', '')
        if password and len(password) < 6:
            errors['password'] = "Password must be at least 6 characters long"
        
        # Email validation (basic)
        email = user_data.get('email', '')
        if email and '@' not in email:
            errors['email'] = "Invalid email format"
        
        return errors
    
    def create_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Create comprehensive user profile
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: User profile data
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return {}
        
        profile = {
            'basic_info': {
                'user_id': user.user_id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'role': user.get_role(),
                'created_at': user.created_at
            },
            'activity': {
                'registered_events_count': len(user.registered_events),
                'registered_events': user.registered_events
            }
        }
        
        # Add role-specific information
        if isinstance(user, Student):
            profile['role_info'] = {'student_id': user.student_id}
        elif isinstance(user, EventOrganizer):
            profile['role_info'] = {
                'department': user.department,
                'organized_events_count': len(getattr(user, 'organized_events', [])),
                'organized_events': getattr(user, 'organized_events', [])
            }
        elif isinstance(user, Visitor):
            profile['role_info'] = {'organization': user.organization}
        elif isinstance(user, Admin):
            profile['role_info'] = {'admin_privileges': True}
        
        return profile
    
    def bulk_import_users(self, users_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Import multiple users from data
        
        Args:
            users_data (List[dict]): List of user dictionaries
            
        Returns:
            dict: Import results with success/failure counts
        """
        results = {'success': 0, 'failed': 0, 'duplicates': 0}
        
        for user_data in users_data:
            try:
                # Validate data
                errors = self.validate_user_data(user_data)
                if errors:
                    print(f"Validation errors for user {user_data.get('username', 'unknown')}: {errors}")
                    results['failed'] += 1
                    continue
                
                # Check for duplicates
                if (self.get_user_by_username(user_data['username']) or 
                    self.get_user_by_email(user_data['email'])):
                    results['duplicates'] += 1
                    continue
                
                # Create user based on type
                user_type = user_data.get('user_type', 'student')
                if user_type == 'admin':
                    user = Admin(user_data['username'], user_data['password'],
                               user_data['name'], user_data['email'])
                elif user_type == 'event_organizer':
                    user = EventOrganizer(user_data['username'], user_data['password'],
                                        user_data['name'], user_data['email'],
                                        user_data.get('department', ''))
                elif user_type == 'student':
                    user = Student(user_data['username'], user_data['password'],
                                 user_data['name'], user_data['email'],
                                 user_data.get('student_id', ''))
                elif user_type == 'visitor':
                    user = Visitor(user_data['username'], user_data['password'],
                                 user_data['name'], user_data['email'],
                                 user_data.get('organization'))
                else:
                    print(f"Unknown user type: {user_type}")
                    results['failed'] += 1
                    continue
                
                if self.add_user(user):
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    
            except Exception as e:
                print(f"Error importing user: {e}")
                results['failed'] += 1
        
        return results
    
    def export_users_data(self) -> List[Dict[str, Any]]:
        """
        Export all users data for backup/transfer
        
        Returns:
            List[dict]: List of user dictionaries
        """
        return [user.to_dict() for user in self.users]