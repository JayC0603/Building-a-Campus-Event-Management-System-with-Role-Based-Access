#!/usr/bin/env python3
"""
Campus Event Management System
Main Application Entry Point

Author: Campus Event Management Team
Date: July 2025
Description: A comprehensive event management system with role-based access control
"""

import sys
import os
from datetime import datetime

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import User, Admin, EventOrganizer, Student, Visitor
from models.event import Event
from controllers.event_controller import EventController
from controllers.user_controller import UserController
from controllers.auth_controller import AuthController
from utils.file_manager import FileManager
from utils.validators import InputValidator
from views.ui import UI

class CampusEventManagementSystem:
    """Main application class that orchestrates the entire system"""
    
    def __init__(self):
        """Initialize the system with all controllers and utilities"""
        self.file_manager = FileManager()
        self.event_controller = EventController(self.file_manager)
        self.user_controller = UserController(self.file_manager)
        self.auth_controller = AuthController(self.user_controller)
        self.ui = UI()
        self.current_user = None
        
        # Load existing data
        self._load_system_data()
        
    def _load_system_data(self):
        """Load events and users from persistent storage"""
        try:
            # Load events
            events_data = self.file_manager.load_events()
            for event_data in events_data:
                event = Event.from_dict(event_data)
                self.event_controller.add_event(event)
            
            # Load users
            users_data = self.file_manager.load_users()
            for user_data in users_data:
                user = self._create_user_from_data(user_data)
                if user:
                    self.user_controller.add_user(user)
                    
        except Exception as e:
            print(f"Warning: Could not load system data: {e}")
            self._initialize_default_data()
    
    def _create_user_from_data(self, user_data):
        """Create appropriate user object from data dictionary"""
        user_type = user_data.get('user_type')
        if user_type == 'admin':
            return Admin.from_dict(user_data)
        elif user_type == 'event_organizer':
            return EventOrganizer.from_dict(user_data)
        elif user_type == 'student':
            return Student.from_dict(user_data)
        elif user_type == 'visitor':
            return Visitor.from_dict(user_data)
        return None
    
    def _initialize_default_data(self):
        """Initialize system with default admin account"""
        default_admin = Admin("admin", "admin123", "System Administrator", "admin@campus.edu")
        self.user_controller.add_user(default_admin)
        print("System initialized with default admin account (username: admin, password: admin123)")
    
    def run(self):
        """Main application loop"""
        self.ui.display_welcome()
        
        while True:
            try:
                if not self.current_user:
                    self._handle_authentication()
                else:
                    self._handle_main_menu()
                    
            except KeyboardInterrupt:
                print("\n\nSystem shutdown initiated...")
                self._save_and_exit()
            except Exception as e:
                print(f"An error occurred: {e}")
                input("Press Enter to continue...")
    
    def _handle_authentication(self):
        """Handle user authentication process"""
        self.ui.display_auth_menu()
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            self._login()
        elif choice == '2':
            self._register()
        elif choice == '3':
            self._save_and_exit()
        else:
            print("Invalid choice. Please try again.")
    
    def _login(self):
        """Handle user login"""
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        user = self.auth_controller.authenticate(username, password)
        if user:
            self.current_user = user
            print(f"Welcome, {user.name}! You are logged in as {user.get_role()}.")
        else:
            print("Invalid username or password.")
    
    def _register(self):
        """Handle user registration"""
        print("\n=== User Registration ===")
        print("1. Student")
        print("2. Visitor")
        print("3. Event Organizer")
        
        role_choice = input("Select your role (1-3): ").strip()
        
        # Get common user details
        username = input("Username: ").strip()
        if self.user_controller.get_user_by_username(username):
            print("Username already exists. Please choose a different one.")
            return
        
        password = input("Password: ").strip()
        name = input("Full Name: ").strip()
        email = input("Email: ").strip()
        
        # Validate inputs
        if not all([username, password, name, email]):
            print("All fields are required.")
            return
        
        if not InputValidator.validate_email(email):
            print("Invalid email format.")
            return
        
        # Create user based on role
        user = None
        if role_choice == '1':
            student_id = input("Student ID: ").strip()
            user = Student(username, password, name, email, student_id)
        elif role_choice == '2':
            organization = input("Organization (optional): ").strip()
            user = Visitor(username, password, name, email, organization or None)
        elif role_choice == '3':
            department = input("Department: ").strip()
            user = EventOrganizer(username, password, name, email, department)
        else:
            print("Invalid role selection.")
            return
        
        if user and self.user_controller.add_user(user):
            print("Registration successful! You can now login.")
        else:
            print("Registration failed. Please try again.")
    
    def _handle_main_menu(self):
        """Handle main menu based on user role"""
        if isinstance(self.current_user, Admin):
            self._admin_menu()
        elif isinstance(self.current_user, EventOrganizer):
            self._organizer_menu()
        else:  # Student or Visitor
            self._user_menu()
    
    def _admin_menu(self):
        """Admin menu and operations"""
        self.ui.display_admin_menu()
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            self._create_event()
        elif choice == '2':
            self._view_all_events()
        elif choice == '3':
            self._update_event()
        elif choice == '4':
            self._delete_event()
        elif choice == '5':
            self._view_all_attendees()
        elif choice == '6':
            self._generate_reports()
        elif choice == '7':
            self._manage_users()
        elif choice == '8':
            self._logout()
        else:
            print("Invalid choice. Please try again.")
    
    def _organizer_menu(self):
        """Event organizer menu and operations"""
        self.ui.display_organizer_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            self._create_event()
        elif choice == '2':
            self._view_my_events()
        elif choice == '3':
            self._manage_event_attendees()
        elif choice == '4':
            self._update_my_event()
        elif choice == '5':
            self._view_event_statistics()
        elif choice == '6':
            self._logout()
        else:
            print("Invalid choice. Please try again.")
    
    def _user_menu(self):
        """Student/Visitor menu and operations"""
        self.ui.display_user_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            self._search_events()
        elif choice == '2':
            self._register_for_event()
        elif choice == '3':
            self._view_my_registrations()
        elif choice == '4':
            self._unregister_from_event()
        elif choice == '5':
            self._logout()
        else:
            print("Invalid choice. Please try again.")
    
    def _create_event(self):
        """Create a new event"""
        print("\n=== Create New Event ===")
        
        # Get event details
        name = input("Event Name: ").strip()
        if not name:
            print("Event name is required.")
            return
        
        description = input("Description: ").strip()
        
        # Get and validate date
        date_str = input("Date (YYYY-MM-DD): ").strip()
        if not InputValidator.validate_date(date_str):
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
        
        # Get and validate time
        time_str = input("Time (HH:MM): ").strip()
        if not InputValidator.validate_time(time_str):
            print("Invalid time format. Please use HH:MM.")
            return
        
        location = input("Location: ").strip()
        
        # Get and validate capacity
        try:
            capacity = int(input("Maximum Capacity: ").strip())
            if capacity <= 0:
                raise ValueError("Capacity must be positive")
        except ValueError as e:
            print(f"Invalid capacity: {e}")
            return
        
        # Create event
        event = Event(
            name=name,
            description=description,
            date=date_str,
            time=time_str,
            location=location,
            capacity=capacity,
            organizer_id=self.current_user.user_id
        )
        
        if self.event_controller.add_event(event):
            print(f"Event '{name}' created successfully!")
        else:
            print("Failed to create event.")
    
    def _view_all_events(self):
        """View all events (Admin only)"""
        events = self.event_controller.get_all_events()
        if not events:
            print("No events found.")
            return
        
        print("\n=== All Events ===")
        for event in events:
            print(f"\n{event}")
            print(f"Attendees: {len(event.attendees)}/{event.capacity}")
    
    def _update_event(self):
        """Update an existing event"""
        event_id = input("Enter Event ID to update: ").strip()
        event = self.event_controller.get_event_by_id(event_id)
        
        if not event:
            print("Event not found.")
            return
        
        # Check permission (admin or organizer of the event)
        if not isinstance(self.current_user, Admin) and event.organizer_id != self.current_user.user_id:
            print("You don't have permission to update this event.")
            return
        
        print(f"\nCurrent event details:\n{event}")
        print("\nEnter new values (press Enter to keep current value):")
        
        # Update fields
        new_name = input(f"Name [{event.name}]: ").strip()
        if new_name:
            event.name = new_name
        
        new_desc = input(f"Description [{event.description}]: ").strip()
        if new_desc:
            event.description = new_desc
        
        new_date = input(f"Date [{event.date}]: ").strip()
        if new_date and InputValidator.validate_date(new_date):
            event.date = new_date
        elif new_date:
            print("Invalid date format, keeping current date.")
        
        new_time = input(f"Time [{event.time}]: ").strip()
        if new_time and InputValidator.validate_time(new_time):
            event.time = new_time
        elif new_time:
            print("Invalid time format, keeping current time.")
        
        new_location = input(f"Location [{event.location}]: ").strip()
        if new_location:
            event.location = new_location
        
        new_capacity = input(f"Capacity [{event.capacity}]: ").strip()
        if new_capacity:
            try:
                capacity = int(new_capacity)
                if capacity >= len(event.attendees):
                    event.capacity = capacity
                else:
                    print(f"Capacity cannot be less than current attendees ({len(event.attendees)})")
            except ValueError:
                print("Invalid capacity, keeping current capacity.")
        
        print("Event updated successfully!")
    
    def _delete_event(self):
        """Delete an event"""
        event_id = input("Enter Event ID to delete: ").strip()
        event = self.event_controller.get_event_by_id(event_id)
        
        if not event:
            print("Event not found.")
            return
        
        # Check permission
        if not isinstance(self.current_user, Admin) and event.organizer_id != self.current_user.user_id:
            print("You don't have permission to delete this event.")
            return
        
        print(f"Event to delete: {event.name}")
        confirm = input("Are you sure? (y/N): ").strip().lower()
        
        if confirm == 'y':
            if self.event_controller.delete_event(event_id):
                print("Event deleted successfully!")
            else:
                print("Failed to delete event.")
    
    def _search_events(self):
        """Search for events"""
        print("\n=== Search Events ===")
        print("1. View all upcoming events")
        print("2. Search by name")
        print("3. Search by date")
        print("4. Search by location")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            events = self.event_controller.get_upcoming_events()
        elif choice == '2':
            name = input("Enter event name (partial match): ").strip()
            events = self.event_controller.search_events_by_name(name)
        elif choice == '3':
            date = input("Enter date (YYYY-MM-DD): ").strip()
            if not InputValidator.validate_date(date):
                print("Invalid date format.")
                return
            events = self.event_controller.search_events_by_date(date)
        elif choice == '4':
            location = input("Enter location (partial match): ").strip()
            events = self.event_controller.search_events_by_location(location)
        else:
            print("Invalid choice.")
            return
        
        if not events:
            print("No events found.")
            return
        
        print(f"\nFound {len(events)} event(s):")
        for event in events:
            availability = event.capacity - len(event.attendees)
            status = "Available" if availability > 0 else "Full"
            print(f"\n{event}")
            print(f"Available spots: {availability} ({status})")
    
    def _register_for_event(self):
        """Register current user for an event"""
        event_id = input("Enter Event ID to register: ").strip()
        
        if self.event_controller.register_attendee(event_id, self.current_user):
            print("Registration successful!")
        else:
            print("Registration failed. Event may be full or not found.")
    
    def _view_my_registrations(self):
        """View current user's event registrations"""
        events = self.event_controller.get_user_events(self.current_user.user_id)
        
        if not events:
            print("You are not registered for any events.")
            return
        
        print(f"\n=== Your Registered Events ({len(events)}) ===")
        for event in events:
            print(f"\n{event}")
    
    def _unregister_from_event(self):
        """Unregister current user from an event"""
        event_id = input("Enter Event ID to unregister: ").strip()
        
        if self.event_controller.unregister_attendee(event_id, self.current_user):
            print("Successfully unregistered from event!")
        else:
            print("Unregistration failed. You may not be registered for this event.")
    
    def _view_my_events(self):
        """View events organized by current user"""
        events = self.event_controller.get_events_by_organizer(self.current_user.user_id)
        
        if not events:
            print("You haven't organized any events yet.")
            return
        
        print(f"\n=== Your Events ({len(events)}) ===")
        for event in events:
            print(f"\n{event}")
            print(f"Attendees: {len(event.attendees)}/{event.capacity}")
    
    def _manage_event_attendees(self):
        """Manage attendees for organizer's events"""
        events = self.event_controller.get_events_by_organizer(self.current_user.user_id)
        
        if not events:
            print("You haven't organized any events yet.")
            return
        
        print("\nYour Events:")
        for i, event in enumerate(events, 1):
            print(f"{i}. {event.name} ({len(event.attendees)}/{event.capacity} attendees)")
        
        try:
            choice = int(input("Select event number: ")) - 1
            if 0 <= choice < len(events):
                selected_event = events[choice]
                self._show_event_attendees(selected_event)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")
    
    def _show_event_attendees(self, event):
        """Show attendees for a specific event"""
        if not event.attendees:
            print(f"No attendees registered for '{event.name}' yet.")
            return
        
        print(f"\n=== Attendees for '{event.name}' ===")
        for attendee_id in event.attendees:
            user = self.user_controller.get_user_by_id(attendee_id)
            if user:
                print(f"- {user.name} ({user.email}) - {user.get_role()}")
    
    def _generate_reports(self):
        """Generate statistical reports (Admin only)"""
        print("\n=== Generate Reports ===")
        print("1. Overall Statistics")
        print("2. Event Attendance Report")
        print("3. User Registration Report")
        print("4. Export All Data")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            self._show_overall_statistics()
        elif choice == '2':
            self._export_attendance_report()
        elif choice == '3':
            self._show_user_statistics()
        elif choice == '4':
            self._export_all_data()
        else:
            print("Invalid choice.")
    
    def _show_overall_statistics(self):
        """Show overall system statistics"""
        stats = self.event_controller.get_system_statistics()
        
        print("\n=== System Statistics ===")
        print(f"Total Events: {stats['total_events']}")
        print(f"Total Registrations: {stats['total_attendees']}")
        print(f"Average Attendees per Event: {stats['avg_attendees']:.1f}")
        
        if stats['most_popular_event']:
            print(f"Most Popular Event: {stats['most_popular_event']['name']} ({stats['most_popular_event']['attendees']} attendees)")
        
        if stats['least_popular_event']:
            print(f"Least Popular Event: {stats['least_popular_event']['name']} ({stats['least_popular_event']['attendees']} attendees)")
        
        print(f"Total Users: {len(self.user_controller.users)}")
    
    def _export_attendance_report(self):
        """Export attendance report to CSV"""
        if self.file_manager.export_attendance_report(self.event_controller.events):
            print("Attendance report exported to 'attendance_report.csv'")
        else:
            print("Failed to export attendance report.")
    
    def _show_user_statistics(self):
        """Show user registration statistics"""
        user_stats = self.user_controller.get_user_statistics()
        
        print("\n=== User Statistics ===")
        for role, count in user_stats.items():
            print(f"{role.title()}s: {count}")
    
    def _export_all_data(self):
        """Export all system data"""
        try:
            # Save current data
            self._save_system_data()
            
            # Export reports
            self.file_manager.export_attendance_report(self.event_controller.events)
            self.file_manager.export_events_report(self.event_controller.events)
            
            print("All data exported successfully!")
            print("Files created:")
            print("- events.json (Event data)")
            print("- users.json (User data)")
            print("- attendance_report.csv")
            print("- events_report.csv")
            
        except Exception as e:
            print(f"Export failed: {e}")
    
    def _manage_users(self):
        """User management for admin"""
        print("\n=== User Management ===")
        print("1. View All Users")
        print("2. Create User Account")
        print("3. Delete User Account")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            self._view_all_users()
        elif choice == '2':
            self._create_user_account()
        elif choice == '3':
            self._delete_user_account()
        else:
            print("Invalid choice.")
    
    def _view_all_users(self):
        """View all system users"""
        users = self.user_controller.get_all_users()
        
        if not users:
            print("No users found.")
            return
        
        print(f"\n=== All Users ({len(users)}) ===")
        for user in users:
            print(f"ID: {user.user_id} | {user.name} ({user.username}) - {user.get_role()}")
            print(f"Email: {user.email}")
            if hasattr(user, 'student_id'):
                print(f"Student ID: {user.student_id}")
            elif hasattr(user, 'department'):
                print(f"Department: {user.department}")
            elif hasattr(user, 'organization') and user.organization:
                print(f"Organization: {user.organization}")
            print("-" * 50)
    
    def _create_user_account(self):
        """Create user account (Admin only)"""
        print("This feature redirects to the registration process...")
        self._register()
    
    def _delete_user_account(self):
        """Delete user account (Admin only)"""
        username = input("Enter username to delete: ").strip()
        user = self.user_controller.get_user_by_username(username)
        
        if not user:
            print("User not found.")
            return
        
        if user.username == self.current_user.username:
            print("You cannot delete your own account.")
            return
        
        print(f"User to delete: {user.name} ({user.username}) - {user.get_role()}")
        confirm = input("Are you sure? (y/N): ").strip().lower()
        
        if confirm == 'y':
            if self.user_controller.delete_user(user.user_id):
                print("User deleted successfully!")
            else:
                print("Failed to delete user.")
    
    def _update_my_event(self):
        """Update organizer's own event"""
        events = self.event_controller.get_events_by_organizer(self.current_user.user_id)
        
        if not events:
            print("You haven't organized any events yet.")
            return
        
        print("\nYour Events:")
        for i, event in enumerate(events, 1):
            print(f"{i}. {event.name}")
        
        try:
            choice = int(input("Select event number to update: ")) - 1
            if 0 <= choice < len(events):
                selected_event = events[choice]
                # Set the event ID and call update method
                event_id = selected_event.event_id
                print(f"Updating event: {selected_event.name}")
                # Temporarily store event ID in input buffer simulation
                import io
                import sys
                old_stdin = sys.stdin
                sys.stdin = io.StringIO(event_id + "\n")
                self._update_event()
                sys.stdin = old_stdin
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")
    
    def _view_event_statistics(self):
        """View statistics for organizer's events"""
        events = self.event_controller.get_events_by_organizer(self.current_user.user_id)
        
        if not events:
            print("You haven't organized any events yet.")
            return
        
        print(f"\n=== Your Event Statistics ===")
        total_capacity = sum(event.capacity for event in events)
        total_registered = sum(len(event.attendees) for event in events)
        
        print(f"Total Events Organized: {len(events)}")
        print(f"Total Capacity: {total_capacity}")
        print(f"Total Registered: {total_registered}")
        print(f"Overall Fill Rate: {(total_registered/total_capacity*100) if total_capacity > 0 else 0:.1f}%")
        
        print("\nEvent Details:")
        for event in events:
            fill_rate = (len(event.attendees) / event.capacity * 100) if event.capacity > 0 else 0
            print(f"- {event.name}: {len(event.attendees)}/{event.capacity} ({fill_rate:.1f}% full)")
    
    def _view_all_attendees(self):
        """View all attendees across all events (Admin only)"""
        events = self.event_controller.get_all_events()
        
        if not events:
            print("No events found.")
            return
        
        print("\n=== All Event Attendees ===")
        for event in events:
            print(f"\nEvent: {event.name}")
            if not event.attendees:
                print("  No attendees registered.")
                continue
            
            for attendee_id in event.attendees:
                user = self.user_controller.get_user_by_id(attendee_id)
                if user:
                    print(f"  - {user.name} ({user.email}) - {user.get_role()}")
    
    def _logout(self):
        """Logout current user"""
        print(f"Goodbye, {self.current_user.name}!")
        self.current_user = None
    
    def _save_system_data(self):
        """Save all system data to persistent storage"""
        try:
            # Save events
            events_data = [event.to_dict() for event in self.event_controller.events]
            self.file_manager.save_events(events_data)
            
            # Save users
            users_data = [user.to_dict() for user in self.user_controller.users]
            self.file_manager.save_users(users_data)
            
        except Exception as e:
            print(f"Warning: Could not save system data: {e}")
    
    def _save_and_exit(self):
        """Save data and exit the system"""
        print("Saving data and exiting...")
        self._save_system_data()
        print("Thank you for using Campus Event Management System!")
        sys.exit(0)

def main():
    """Main function to start the application"""
    try:
        app = CampusEventManagementSystem()
        app.run()
    except KeyboardInterrupt:
        print("\n\nSystem shutdown initiated by user.")
    except Exception as e:
        print(f"Fatal error: {e}")
        print("Please contact system administrator.")

if __name__ == "__main__":
    main()