"""
File Manager Module

This module handles all file operations for data persistence.
Manages JSON and CSV file operations for events, users, and reports.
"""

import json
import csv
import os
import tempfile
import shutil
from typing import List, Dict, Any, Optional
from datetime import datetime

class FileManager:
    """File manager for handling data persistence"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize file manager
        
        Args:
            data_dir (str): Directory to store data files
        """
        self.data_dir = data_dir
        self.events_file = os.path.join(data_dir, "events.json")
        self.users_file = os.path.join(data_dir, "users.json")
        self.reports_dir = os.path.join(data_dir, "reports")
        
        # Create directories if they don't exist
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Create necessary directories if they don't exist"""
        try:
            # Tạo thư mục data
            os.makedirs(self.data_dir, exist_ok=True)
            
            # Kiểm tra nếu reports là file, xóa nó
            if os.path.isfile(self.reports_dir):
                os.remove(self.reports_dir)
                print(f"Removed file {self.reports_dir}")
            
            # Tạo thư mục reports
            os.makedirs(self.reports_dir, exist_ok=True)
            
        except PermissionError as e:
            print(f"Permission error creating directories: {e}")
            self._use_alternative_directory()
        except FileExistsError as e:
            print(f"File exists error: {e}")
            self._handle_file_exists_error()
        except Exception as e:
            print(f"Error creating directories: {e}")
            self._use_alternative_directory()
    
    def _handle_file_exists_error(self):
        """Handle file exists error by cleaning up and retrying"""
        try:
            # If reports_dir exists as a file, remove it
            if os.path.isfile(self.reports_dir):
                os.remove(self.reports_dir)
                print(f"Removed conflicting file: {self.reports_dir}")
            
            # Retry creating directories
            os.makedirs(self.reports_dir, exist_ok=True)
            print("Successfully created reports directory")
            
        except Exception as e:
            print(f"Failed to resolve file conflict: {e}")
            self._use_alternative_directory()
    
    def _use_alternative_directory(self):
        """Use alternative directory when primary fails"""
        try:
            # Tạo thư mục backup với tên khác
            self.data_dir = os.path.join(tempfile.gettempdir(), "campus_events")
            self.events_file = os.path.join(self.data_dir, "events.json")
            self.users_file = os.path.join(self.data_dir, "users.json")
            self.reports_dir = os.path.join(self.data_dir, "reports")
            
            # Clean up if exists
            if os.path.exists(self.data_dir):
                shutil.rmtree(self.data_dir)
            
            os.makedirs(self.data_dir, exist_ok=True)
            os.makedirs(self.reports_dir, exist_ok=True)
            print(f"Using alternative directory: {self.data_dir}")
            
        except Exception as e:
            print(f"Critical error: Cannot create any directories: {e}")
            # Use current directory as last resort
            self.data_dir = "."
            self.events_file = "events.json"
            self.users_file = "users.json"
            self.reports_dir = "reports_temp"
            try:
                os.makedirs(self.reports_dir, exist_ok=True)
            except:
                self.reports_dir = "."
            print(f"Using current directory as fallback")
    
    def save_events(self, events_data: List[Dict[str, Any]]) -> bool:
        """
        Save events data to JSON file
        
        Args:
            events_data (List[dict]): List of event dictionaries
            
        Returns:
            bool: True if save successful
        """
        try:
            # Ensure directory exists before saving
            os.makedirs(os.path.dirname(self.events_file), exist_ok=True)
            
            with open(self.events_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'events': events_data,
                    'last_updated': datetime.now().isoformat(),
                    'version': '1.0'
                }, f, indent=2, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"Permission denied: Cannot write to {self.events_file}")
            return self._save_to_alternative_location('events', events_data)
        except Exception as e:
            print(f"Error saving events: {e}")
            return False
    
    def load_events(self) -> List[Dict[str, Any]]:
        """
        Load events data from JSON file
        
        Returns:
            List[dict]: List of event dictionaries
        """
        try:
            if not os.path.exists(self.events_file):
                print(f"Events file not found: {self.events_file}")
                return []
            
            with open(self.events_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                events = data.get('events', [])
                print(f"Loaded {len(events)} events from {self.events_file}")
                return events
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in events file: {e}")
            return []
        except PermissionError:
            print(f"Permission denied: Cannot read {self.events_file}")
            return []
        except Exception as e:
            print(f"Error loading events: {e}")
            return []
    
    def save_users(self, users_data: List[Dict[str, Any]]) -> bool:
        """
        Save users data to JSON file
        
        Args:
            users_data (List[dict]): List of user dictionaries
            
        Returns:
            bool: True if save successful
        """
        try:
            # Ensure directory exists before saving
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'users': users_data,
                    'last_updated': datetime.now().isoformat(),
                    'version': '1.0'
                }, f, indent=2, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"Permission denied: Cannot write to {self.users_file}")
            return self._save_to_alternative_location('users', users_data)
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def load_users(self) -> List[Dict[str, Any]]:
        """
        Load users data from JSON file
        
        Returns:
            List[dict]: List of user dictionaries
        """
        try:
            if not os.path.exists(self.users_file):
                print(f"Users file not found: {self.users_file}")
                return []
            
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                users = data.get('users', [])
                print(f"Loaded {len(users)} users from {self.users_file}")
                return users
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in users file: {e}")
            return []
        except PermissionError:
            print(f"Permission denied: Cannot read {self.users_file}")
            return []
        except Exception as e:
            print(f"Error loading users: {e}")
            return []
    
    def _save_to_alternative_location(self, file_type: str, data: List[Dict[str, Any]]) -> bool:
        """
        Save to alternative location when primary fails
        
        Args:
            file_type (str): Type of file ('events' or 'users')
            data (List[dict]): Data to save
            
        Returns:
            bool: True if save successful
        """
        try:
            temp_dir = tempfile.gettempdir()
            alt_file = os.path.join(temp_dir, f"campus_{file_type}.json")
            
            with open(alt_file, 'w', encoding='utf-8') as f:
                json.dump({
                    file_type: data,
                    'last_updated': datetime.now().isoformat(),
                    'version': '1.0'
                }, f, indent=2, ensure_ascii=False)
            
            print(f"Data saved to alternative location: {alt_file}")
            return True
        except Exception as e:
            print(f"Failed to save to alternative location: {e}")
            return False
    
    def export_attendance_report(self, events: List) -> bool:
        """
        Export attendance report to CSV
        
        Args:
            events (List[Event]): List of event objects
            
        Returns:
            bool: True if export successful
        """
        try:
            # Ensure reports directory exists
            os.makedirs(self.reports_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(self.reports_dir, f"attendance_report_{timestamp}.csv")
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    'Event ID', 'Event Name', 'Date', 'Time', 'Location',
                    'Organizer ID', 'Capacity', 'Registered', 'Available',
                    'Fill Rate (%)', 'Status'
                ])
                
                # Write data
                for event in events:
                    fill_rate = (len(event.attendees) / event.capacity * 100) if event.capacity > 0 else 0
                    writer.writerow([
                        event.event_id,
                        event.name,
                        event.date,
                        event.time,
                        event.location,
                        event.organizer_id,
                        event.capacity,
                        len(event.attendees),
                        event.get_available_spots(),
                        round(fill_rate, 2),
                        event.status
                    ])
            
            print(f"Attendance report exported to: {filename}")
            return True
        except PermissionError:
            print(f"Permission denied: Cannot write to {self.reports_dir}")
            return self._export_to_alternative_location('attendance', events)
        except Exception as e:
            print(f"Error exporting attendance report: {e}")
            return False
    
    def export_events_report(self, events: List) -> bool:
        """
        Export detailed events report to CSV
        
        Args:
            events (List[Event]): List of event objects
            
        Returns:
            bool: True if export successful
        """
        try:
            # Ensure reports directory exists
            os.makedirs(self.reports_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(self.reports_dir, f"events_report_{timestamp}.csv")
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    'Event ID', 'Name', 'Description', 'Date', 'Time',
                    'Location', 'Capacity', 'Attendees', 'Organizer ID',
                    'Created At', 'Updated At', 'Status'
                ])
                
                # Write data
                for event in events:
                    writer.writerow([
                        event.event_id,
                        event.name,
                        event.description,
                        event.date,
                        event.time,
                        event.location,
                        event.capacity,
                        len(event.attendees),
                        event.organizer_id,
                        event.created_at,
                        event.updated_at,
                        event.status
                    ])
            
            print(f"Events report exported to: {filename}")
            return True
        except PermissionError:
            print(f"Permission denied: Cannot write to {self.reports_dir}")
            return self._export_to_alternative_location('events', events)
        except Exception as e:
            print(f"Error exporting events report: {e}")
            return False
    
    def _export_to_alternative_location(self, report_type: str, data: List) -> bool:
        """
        Export to alternative location when primary fails
        
        Args:
            report_type (str): Type of report
            data (List): Data to export
            
        Returns:
            bool: True if export successful
        """
        try:
            temp_dir = tempfile.gettempdir()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            alt_file = os.path.join(temp_dir, f"{report_type}_report_{timestamp}.csv")
            
            with open(alt_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                if report_type == 'attendance':
                    writer.writerow([
                        'Event ID', 'Event Name', 'Date', 'Time', 'Location',
                        'Organizer ID', 'Capacity', 'Registered', 'Available',
                        'Fill Rate (%)', 'Status'
                    ])
                    for event in data:
                        fill_rate = (len(event.attendees) / event.capacity * 100) if event.capacity > 0 else 0
                        writer.writerow([
                            event.event_id, event.name, event.date, event.time,
                            event.location, event.organizer_id, event.capacity,
                            len(event.attendees), event.get_available_spots(),
                            round(fill_rate, 2), event.status
                        ])
                elif report_type == 'events':
                    writer.writerow([
                        'Event ID', 'Name', 'Description', 'Date', 'Time',
                        'Location', 'Capacity', 'Attendees', 'Organizer ID',
                        'Created At', 'Updated At', 'Status'
                    ])
                    for event in data:
                        writer.writerow([
                            event.event_id, event.name, event.description,
                            event.date, event.time, event.location,
                            event.capacity, len(event.attendees),
                            event.organizer_id, event.created_at,
                            event.updated_at, event.status
                        ])
            
            print(f"Report exported to alternative location: {alt_file}")
            return True
        except Exception as e:
            print(f"Failed to export to alternative location: {e}")
            return False
    
    def export_users_report(self, users: List) -> bool:
        """
        Export users report to CSV
        
        Args:
            users (List[User]): List of user objects
            
        Returns:
            bool: True if export successful
        """
        try:
            # Ensure reports directory exists
            os.makedirs(self.reports_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(self.reports_dir, f"users_report_{timestamp}.csv")
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    'User ID', 'Username', 'Name', 'Email', 'Role',
                    'Registered Events', 'Created At', 'Additional Info'
                ])
                
                # Write data
                for user in users:
                    additional_info = ""
                    if hasattr(user, 'student_id'):
                        additional_info = f"Student ID: {user.student_id}"
                    elif hasattr(user, 'department'):
                        additional_info = f"Department: {user.department}"
                    elif hasattr(user, 'organization') and user.organization:
                        additional_info = f"Organization: {user.organization}"
                    
                    writer.writerow([
                        user.user_id,
                        user.username,
                        user.name,
                        user.email,
                        user.get_role(),
                        len(user.registered_events),
                        user.created_at,
                        additional_info
                    ])
            
            print(f"Users report exported to: {filename}")
            return True
        except Exception as e:
            print(f"Error exporting users report: {e}")
            return False
    
    def export_attendee_details(self, events: List, users: List) -> bool:
        """
        Export detailed attendee information to CSV
        
        Args:
            events (List[Event]): List of event objects
            users (List[User]): List of user objects
            
        Returns:
            bool: True if export successful
        """
        try:
            # Ensure reports directory exists
            os.makedirs(self.reports_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(self.reports_dir, f"attendee_details_{timestamp}.csv")
            
            # Create user lookup dictionary
            user_lookup = {user.user_id: user for user in users}
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    'Event ID', 'Event Name', 'Event Date', 'Attendee ID',
                    'Attendee Name', 'Attendee Email', 'Attendee Role',
                    'Registration Date'
                ])
                
                # Write data
                for event in events:
                    for attendee_id in event.attendees:
                        user = user_lookup.get(attendee_id)
                        if user:
                            writer.writerow([
                                event.event_id,
                                event.name,
                                event.date,
                                attendee_id,
                                user.name,
                                user.email,
                                user.get_role(),
                                event.created_at  # Approximation
                            ])
            
            print(f"Attendee details exported to: {filename}")
            return True
        except Exception as e:
            print(f"Error exporting attendee details: {e}")
            return False
    
    def backup_data(self) -> bool:
        """
        Create backup of all data files
        
        Returns:
            bool: True if backup successful
        """
        try:
            backup_dir = os.path.join(self.data_dir, "backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_subdir = os.path.join(backup_dir, f"backup_{timestamp}")
            os.makedirs(backup_subdir, exist_ok=True)
            
            # Copy events file
            if os.path.exists(self.events_file):
                shutil.copy2(self.events_file, 
                           os.path.join(backup_subdir, "events.json"))
            
            # Copy users file
            if os.path.exists(self.users_file):
                shutil.copy2(self.users_file, 
                           os.path.join(backup_subdir, "users.json"))
            
            print(f"Backup created in: {backup_subdir}")
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def restore_data(self, backup_path: str) -> bool:
        """
        Restore data from backup
        
        Args:
            backup_path (str): Path to backup directory
            
        Returns:
            bool: True if restore successful
        """
        try:
            events_backup = os.path.join(backup_path, "events.json")
            users_backup = os.path.join(backup_path, "users.json")
            
            # Create current backup before restoring
            self.backup_data()
            
            # Restore events
            if os.path.exists(events_backup):
                shutil.copy2(events_backup, self.events_file)
            
            # Restore users
            if os.path.exists(users_backup):
                shutil.copy2(users_backup, self.users_file)
            
            print(f"Data restored from: {backup_path}")
            return True
        except Exception as e:
            print(f"Error restoring data: {e}")
            return False
    
    def get_file_info(self) -> Dict[str, Any]:
        """
        Get information about data files
        
        Returns:
            dict: File information
        """
        info = {
            'data_directory': self.data_dir,
            'reports_directory': self.reports_dir,
            'files': {}
        }
        
        try:
            # Check events file
            if os.path.exists(self.events_file):
                stat = os.stat(self.events_file)
                info['files']['events'] = {
                    'path': self.events_file,
                    'size_bytes': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
            
            # Check users file
            if os.path.exists(self.users_file):
                stat = os.stat(self.users_file)
                info['files']['users'] = {
                    'path': self.users_file,
                    'size_bytes': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
            
            # Check reports directory
            if os.path.exists(self.reports_dir):
                reports = os.listdir(self.reports_dir)
                info['files']['reports_count'] = len(reports)
                info['files']['latest_reports'] = reports[-5:] if reports else []
        except Exception as e:
            print(f"Error getting file info: {e}")
        
        return info
    
    def cleanup_old_reports(self, days_old: int = 30) -> int:
        """
        Clean up old report files
        
        Args:
            days_old (int): Remove files older than this many days
            
        Returns:
            int: Number of files removed
        """
        try:
            removed_count = 0
            current_time = datetime.now()
            
            if not os.path.exists(self.reports_dir):
                return 0
            
            for filename in os.listdir(self.reports_dir):
                file_path = os.path.join(self.reports_dir, filename)
                
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    age_days = (current_time - file_time).days
                    
                    if age_days > days_old:
                        os.remove(file_path)
                        removed_count += 1
            
            print(f"Removed {removed_count} old report files")
            return removed_count
        except Exception as e:
            print(f"Error cleaning up reports: {e}")
            return 0
    
    def test_permissions(self) -> Dict[str, bool]:
        """
        Test file system permissions
        
        Returns:
            dict: Permission test results
        """
        results = {
            'data_dir_writable': False,
            'reports_dir_writable': False,
            'events_file_writable': False,
            'users_file_writable': False
        }
        
        try:
            # Test data directory
            test_file = os.path.join(self.data_dir, 'test_write.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            results['data_dir_writable'] = True
        except:
            pass
        
        try:
            # Test reports directory
            test_file = os.path.join(self.reports_dir, 'test_write.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            results['reports_dir_writable'] = True
        except:
            pass
        
        try:
            # Test events file
            if os.path.exists(self.events_file):
                results['events_file_writable'] = os.access(self.events_file, os.W_OK)
            else:
                results['events_file_writable'] = os.access(os.path.dirname(self.events_file), os.W_OK)
        except:
            pass
        
        try:
            # Test users file
            if os.path.exists(self.users_file):
                results['users_file_writable'] = os.access(self.users_file, os.W_OK)
            else:
                results['users_file_writable'] = os.access(os.path.dirname(self.users_file), os.W_OK)
        except:
            pass
        
        return results