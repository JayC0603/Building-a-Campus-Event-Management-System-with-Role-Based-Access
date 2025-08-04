"""
Authentication Controller Module

This module handles authentication and authorization logic.
Manages user login, session management, and access control.
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from models.user import User, Admin, EventOrganizer, Student, Visitor
from controllers.user_controller import UserController

class AuthController:
    """Controller for handling authentication and authorization"""
    
    def __init__(self, user_controller: UserController):
        """
        Initialize authentication controller
        
        Args:
            user_controller (UserController): User controller instance
        """
        self.user_controller = user_controller
        self.active_sessions = {}  # user_id -> session_info
        self.failed_attempts = {}  # username -> count and timestamp
        self.max_failed_attempts = 5
        self.lockout_duration = 300  # 5 minutes in seconds
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            User or None: User object if authentication successful
        """
        # Check if account is locked
        if self._is_account_locked(username):
            remaining_time = self._get_lockout_remaining_time(username)
            print(f"Account locked. Try again in {remaining_time} seconds.")
            return None
        
        # Attempt authentication
        user = self.user_controller.authenticate_user(username, password)
        
        if user:
            # Successful login - clear failed attempts and create session
            self._clear_failed_attempts(username)
            self._create_session(user)
            return user
        else:
            # Failed login - record attempt
            self._record_failed_attempt(username)
            return None
    
    def logout(self, user_id: str) -> bool:
        """
        Logout user and end session
        
        Args:
            user_id (str): User ID to logout
            
        Returns:
            bool: True if logout successful
        """
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
            return True
        return False
    
    def is_authenticated(self, user_id: str) -> bool:
        """
        Check if user has an active session
        
        Args:
            user_id (str): User ID to check
            
        Returns:
            bool: True if user is authenticated
        """
        if user_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[user_id]
        
        # Check if session has expired
        if self._is_session_expired(session):
            del self.active_sessions[user_id]
            return False
        
        return True
    
    def authorize_event_management(self, user: User, event_organizer_id: str = None) -> bool:
        """
        Check if user can manage events
        
        Args:
            user (User): User requesting access
            event_organizer_id (str): ID of event organizer (for checking ownership)
            
        Returns:
            bool: True if user is authorized
        """
        # Admins can manage all events
        if isinstance(user, Admin):
            return True
        
        # Event organizers can manage their own events
        if isinstance(user, EventOrganizer):
            if event_organizer_id is None or user.user_id == event_organizer_id:
                return True
        
        return False
    
    def authorize_user_management(self, user: User) -> bool:
        """
        Check if user can manage other users
        
        Args:
            user (User): User requesting access
            
        Returns:
            bool: True if user is authorized
        """
        return isinstance(user, Admin)
    
    def authorize_system_reports(self, user: User) -> bool:
        """
        Check if user can access system reports
        
        Args:
            user (User): User requesting access
            
        Returns:
            bool: True if user is authorized
        """
        return isinstance(user, Admin)
    
    def authorize_event_creation(self, user: User) -> bool:
        """
        Check if user can create events
        
        Args:
            user (User): User requesting access
            
        Returns:
            bool: True if user is authorized
        """
        return isinstance(user, (Admin, EventOrganizer))
    
    def authorize_attendee_view(self, user: User, event_organizer_id: str = None) -> bool:
        """
        Check if user can view event attendees
        
        Args:
            user (User): User requesting access
            event_organizer_id (str): ID of event organizer
            
        Returns:
            bool: True if user is authorized
        """
        # Admins can view all attendees
        if isinstance(user, Admin):
            return True
        
        # Event organizers can view their own event attendees
        if isinstance(user, EventOrganizer):
            if event_organizer_id is None or user.user_id == event_organizer_id:
                return True
        
        return False
    
    def get_user_permissions(self, user: User) -> Dict[str, bool]:
        """
        Get comprehensive permissions for a user
        
        Args:
            user (User): User to get permissions for
            
        Returns:
            dict: Dictionary of permissions
        """
        permissions = {
            'create_events': self.authorize_event_creation(user),
            'manage_all_events': isinstance(user, Admin),
            'manage_own_events': isinstance(user, (Admin, EventOrganizer)),
            'view_all_attendees': isinstance(user, Admin),
            'view_own_attendees': isinstance(user, (Admin, EventOrganizer)),
            'manage_users': self.authorize_user_management(user),
            'access_reports': self.authorize_system_reports(user),
            'register_for_events': True,  # All users can register
            'search_events': True,  # All users can search
        }
        
        return permissions
    
    def validate_session(self, user_id: str) -> bool:
        """
        Validate and refresh user session
        
        Args:
            user_id (str): User ID to validate
            
        Returns:
            bool: True if session is valid
        """
        if not self.is_authenticated(user_id):
            return False
        
        # Refresh session timestamp
        session = self.active_sessions[user_id]
        session['last_activity'] = datetime.now()
        
        return True
    
    def get_active_sessions_count(self) -> int:
        """
        Get number of active sessions
        
        Returns:
            int: Number of active sessions
        """
        # Clean expired sessions first
        self._cleanup_expired_sessions()
        return len(self.active_sessions)
    
    def get_session_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session information for a user
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict or None: Session information if exists
        """
        return self.active_sessions.get(user_id)
    
    def force_logout_all(self) -> int:
        """
        Force logout all users (admin function)
        
        Returns:
            int: Number of sessions terminated
        """
        count = len(self.active_sessions)
        self.active_sessions.clear()
        return count
    
    def force_logout_user(self, user_id: str) -> bool:
        """
        Force logout specific user (admin function)
        
        Args:
            user_id (str): User ID to logout
            
        Returns:
            bool: True if user was logged out
        """
        return self.logout(user_id)
    
    def _create_session(self, user: User) -> None:
        """
        Create session for authenticated user
        
        Args:
            user (User): Authenticated user
        """
        self.active_sessions[user.user_id] = {
            'username': user.username,
            'role': user.get_role(),
            'login_time': datetime.now(),
            'last_activity': datetime.now(),
            'session_duration': timedelta(hours=8)  # 8-hour session
        }
    
    def _is_session_expired(self, session: Dict[str, Any]) -> bool:
        """
        Check if session has expired
        
        Args:
            session (dict): Session information
            
        Returns:
            bool: True if session is expired
        """
        now = datetime.now()
        last_activity = session['last_activity']
        session_duration = session['session_duration']
        
        return (now - last_activity) > session_duration
    
    def _cleanup_expired_sessions(self) -> None:
        """Remove expired sessions from active sessions"""
        expired_sessions = []
        
        for user_id, session in self.active_sessions.items():
            if self._is_session_expired(session):
                expired_sessions.append(user_id)
        
        for user_id in expired_sessions:
            del self.active_sessions[user_id]
    
    def _record_failed_attempt(self, username: str) -> None:
        """
        Record failed login attempt
        
        Args:
            username (str): Username that failed login
        """
        now = datetime.now()
        
        if username not in self.failed_attempts:
            self.failed_attempts[username] = {
                'count': 1,
                'first_attempt': now,
                'last_attempt': now
            }
        else:
            attempt_info = self.failed_attempts[username]
            
            # Reset counter if enough time has passed
            if (now - attempt_info['last_attempt']).seconds > self.lockout_duration:
                attempt_info['count'] = 1
                attempt_info['first_attempt'] = now
            else:
                attempt_info['count'] += 1
            
            attempt_info['last_attempt'] = now
    
    def _clear_failed_attempts(self, username: str) -> None:
        """
        Clear failed login attempts for user
        
        Args:
            username (str): Username to clear attempts for
        """
        if username in self.failed_attempts:
            del self.failed_attempts[username]
    
    def _is_account_locked(self, username: str) -> bool:
        """
        Check if account is locked due to failed attempts
        
        Args:
            username (str): Username to check
            
        Returns:
            bool: True if account is locked
        """
        if username not in self.failed_attempts:
            return False
        
        attempt_info = self.failed_attempts[username]
        
        if attempt_info['count'] >= self.max_failed_attempts:
            # Check if lockout period has expired
            now = datetime.now()
            if (now - attempt_info['last_attempt']).seconds < self.lockout_duration:
                return True
            else:
                # Lockout period expired, clear attempts
                self._clear_failed_attempts(username)
                return False
        
        return False
    
    def _get_lockout_remaining_time(self, username: str) -> int:
        """
        Get remaining lockout time in seconds
        
        Args:
            username (str): Username to check
            
        Returns:
            int: Remaining lockout time in seconds
        """
        if username not in self.failed_attempts:
            return 0
        
        attempt_info = self.failed_attempts[username]
        now = datetime.now()
        elapsed = (now - attempt_info['last_attempt']).seconds
        
        return max(0, self.lockout_duration - elapsed)
    
    def get_security_stats(self) -> Dict[str, Any]:
        """
        Get security statistics
        
        Returns:
            dict: Security statistics
        """
        self._cleanup_expired_sessions()
        
        return {
            'active_sessions': len(self.active_sessions),
            'locked_accounts': len([username for username in self.failed_attempts 
                                  if self._is_account_locked(username)]),
            'failed_attempts_today': len(self.failed_attempts),
            'max_failed_attempts': self.max_failed_attempts,
            'lockout_duration_minutes': self.lockout_duration // 60
        }
    
    def reset_user_password(self, admin_user: User, target_username: str, 
                          new_password: str) -> bool:
        """
        Reset user password (admin function)
        
        Args:
            admin_user (User): Admin performing the reset
            target_username (str): Username to reset password for
            new_password (str): New password
            
        Returns:
            bool: True if password reset successful
        """
        if not isinstance(admin_user, Admin):
            print("Only administrators can reset passwords")
            return False
        
        target_user = self.user_controller.get_user_by_username(target_username)
        if not target_user:
            print(f"User '{target_username}' not found")
            return False
        
        if len(new_password) < 6:
            print("Password must be at least 6 characters long")
            return False
        
        target_user.password = new_password
        
        # Clear any failed attempts for this user
        self._clear_failed_attempts(target_username)
        
        # Force logout the user
        self.force_logout_user(target_user.user_id)
        
        return True
    
    def unlock_account(self, admin_user: User, username: str) -> bool:
        """
        Unlock a locked account (admin function)
        
        Args:
            admin_user (User): Admin performing the unlock
            username (str): Username to unlock
            
        Returns:
            bool: True if account unlocked successfully
        """
        if not isinstance(admin_user, Admin):
            print("Only administrators can unlock accounts")
            return False
        
        if username in self.failed_attempts:
            del self.failed_attempts[username]
            return True
        
        return False
    
    def get_user_activity_log(self, user_id: str) -> Dict[str, Any]:
        """
        Get user activity information
        
        Args:
            user_id (str): User ID to get activity for
            
        Returns:
            dict: User activity information
        """
        session = self.get_session_info(user_id)
        user = self.user_controller.get_user_by_id(user_id)
        
        if not user:
            return {}
        
        activity_log = {
            'user_id': user_id,
            'username': user.username,
            'current_session': session is not None,
            'failed_attempts': self.failed_attempts.get(user.username, {}).get('count', 0),
            'account_locked': self._is_account_locked(user.username)
        }
        
        if session:
            activity_log.update({
                'login_time': session['login_time'].isoformat(),
                'last_activity': session['last_activity'].isoformat(),
                'session_duration_hours': session['session_duration'].total_seconds() / 3600
            })
        
        return activity_log
    
    def extend_session(self, user_id: str, additional_hours: int = 2) -> bool:
        """
        Extend user session duration
        
        Args:
            user_id (str): User ID
            additional_hours (int): Additional hours to extend
            
        Returns:
            bool: True if session extended successfully
        """
        if user_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[user_id]
        current_duration = session['session_duration']
        session['session_duration'] = current_duration + timedelta(hours=additional_hours)
        
        return True