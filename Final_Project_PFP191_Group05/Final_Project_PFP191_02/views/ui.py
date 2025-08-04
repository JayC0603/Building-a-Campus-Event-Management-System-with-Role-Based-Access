"""
User Interface Module

This module handles all user interface elements and display logic.
Provides console-based interface for the Campus Event Management System.
"""

import os
from datetime import datetime
from typing import List, Dict, Any

class UI:
    """User Interface class for console-based interactions"""
    
    def __init__(self):
        """Initialize UI with display settings"""
        self.width = 80
        self.separator = "=" * self.width
        self.sub_separator = "-" * self.width
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_welcome(self):
        """Display welcome screen"""
        self.clear_screen()
        print(self.separator)
        print(" " * 15 + "🎓 CAMPUS EVENT MANAGEMENT SYSTEM 🎓")
        print(self.separator)
        print()
        print("Welcome to the Campus Event Management System!")
        print("This system helps manage campus events with role-based access control.")
        print()
        print("Features:")
        print("• Event creation and management")
        print("• User registration and authentication")
        print("• Capacity management and tracking")
        print("• Comprehensive reporting system")
        print("• Role-based access control")
        print()
        print(self.sub_separator)
        print()
    
    def display_auth_menu(self):
        """Display authentication menu"""
        print("\n" + "=" * 30)
        print("     AUTHENTICATION MENU")
        print("=" * 30)
        print("1. Login")
        print("2. Register New Account")
        print("3. Exit System")
        print(self.sub_separator)
    
    def display_admin_menu(self):
        """Display admin menu"""
        print("\n" + "=" * 40)
        print("         ADMINISTRATOR MENU")
        print("=" * 40)
        print("1. Create New Event")
        print("2. View All Events")
        print("3. Update Event")
        print("4. Delete Event")
        print("5. View All Attendees")
        print("6. Generate Reports")
        print("7. User Management")
        print("8. Logout")
        print(self.sub_separator)
    
    def display_organizer_menu(self):
        """Display event organizer menu"""
        print("\n" + "=" * 40)
        print("       EVENT ORGANIZER MENU")
        print("=" * 40)
        print("1. Create New Event")
        print("2. View My Events")
        print("3. Manage Event Attendees")
        print("4. Update My Event")
        print("5. View Event Statistics")
        print("6. Logout")
        print(self.sub_separator)
    
    def display_user_menu(self):
        """Display student/visitor menu"""
        print("\n" + "=" * 40)
        print("           USER MENU")
        print("=" * 40)
        print("1. Search Events")
        print("2. Register for Event")
        print("3. View My Registrations")
        print("4. Unregister from Event")
        print("5. Logout")
        print(self.sub_separator)
    
    def display_event_summary(self, event, show_attendees=False):
        """
        Display event summary in a formatted way
        
        Args:
            event: Event object to display
            show_attendees (bool): Whether to show attendee count
        """
        print(f"\n📅 {event.name}")
        print(f"   ID: {event.event_id}")
        print(f"   📝 {event.description}")
        print(f"   📅 {event.date} at {event.time}")
        print(f"   📍 {event.location}")
        
        if show_attendees:
            fill_rate = (len(event.attendees) / event.capacity * 100) if event.capacity > 0 else 0
            print(f"   👥 {len(event.attendees)}/{event.capacity} attendees ({fill_rate:.1f}% full)")
        else:
            available = event.capacity - len(event.attendees)
            status = "Available" if available > 0 else "Full"
            print(f"   🎫 {available} spots available ({status})")
        
        print(f"   ⭐ Status: {event.status.title()}")
        print(self.sub_separator)
    
    def display_events_list(self, events: List, title: str = "Events", show_attendees: bool = False):
        """
        Display a list of events
        
        Args:
            events (List): List of event objects
            title (str): Title for the list
            show_attendees (bool): Whether to show attendee information
        """
        print(f"\n{title} ({len(events)} found)")
        print(self.separator)
        
        if not events:
            print("No events found.")
            return
        
        for i, event in enumerate(events, 1):
            print(f"\n{i}. ", end="")
            self.display_event_summary(event, show_attendees)
    
    def display_user_profile(self, user):
        """
        Display user profile information
        
        Args:
            user: User object to display
        """
        print(f"\n👤 User Profile")
        print(self.separator)
        print(f"Name: {user.name}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Role: {user.get_role()}")
        print(f"Registered Events: {len(user.registered_events)}")
        
        # Role-specific information
        if hasattr(user, 'student_id'):
            print(f"Student ID: {user.student_id}")
        elif hasattr(user, 'department'):
            print(f"Department: {user.department}")
            if hasattr(user, 'organized_events'):
                print(f"Organized Events: {len(user.organized_events)}")
        elif hasattr(user, 'organization') and user.organization:
            print(f"Organization: {user.organization}")
        
        print(f"Member Since: {user.created_at[:10]}")
        print(self.sub_separator)
    
    def display_statistics(self, stats: Dict[str, Any], title: str = "Statistics"):
        """
        Display statistics in a formatted way
        
        Args:
            stats (dict): Statistics dictionary
            title (str): Title for the statistics
        """
        print(f"\n📊 {title}")
        print(self.separator)
        
        for key, value in stats.items():
            # Format key for display
            display_key = key.replace('_', ' ').title()
            
            if isinstance(value, dict):
                print(f"{display_key}:")
                for sub_key, sub_value in value.items():
                    sub_display_key = sub_key.replace('_', ' ').title()
                    print(f"  {sub_display_key}: {sub_value}")
            elif isinstance(value, float):
                print(f"{display_key}: {value:.2f}")
            else:
                print(f"{display_key}: {value}")
        
        print(self.sub_separator)
    
    def display_table(self, headers: List[str], rows: List[List], title: str = "Data Table"):
        """
        Display data in table format
        
        Args:
            headers (List[str]): Table headers
            rows (List[List]): Table rows
            title (str): Table title
        """
        print(f"\n📋 {title}")
        print(self.separator)
        
        if not rows:
            print("No data to display.")
            return
        
        # Calculate column widths
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(header)
            for row in rows:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            col_widths.append(min(max_width, 20))  # Limit column width
        
        # Display headers
        header_row = " | ".join(header.ljust(col_widths[i]) for i, header in enumerate(headers))
        print(header_row)
        print("-" * len(header_row))
        
        # Display rows
        for row in rows:
            formatted_row = []
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    cell_str = str(cell)[:col_widths[i]]  # Truncate if too long
                    formatted_row.append(cell_str.ljust(col_widths[i]))
            print(" | ".join(formatted_row))
        
        print(self.sub_separator)
    
    def display_success_message(self, message: str):
        """Display success message"""
        print(f"\n✅ SUCCESS: {message}")
    
    def display_error_message(self, message: str):
        """Display error message"""
        print(f"\n❌ ERROR: {message}")
    
    def display_warning_message(self, message: str):
        """Display warning message"""
        print(f"\n⚠️  WARNING: {message}")
    
    def display_info_message(self, message: str):
        """Display info message"""
        print(f"\nℹ️  INFO: {message}")
    
    def get_user_input(self, prompt: str, input_type: str = "string") -> str:
        """
        Get user input with validation
        
        Args:
            prompt (str): Input prompt
            input_type (str): Type of input expected
            
        Returns:
            str: User input
        """
        while True:
            try:
                user_input = input(f"{prompt}: ").strip()
                
                if input_type == "string":
                    return user_input
                elif input_type == "int":
                    return str(int(user_input))
                elif input_type == "email":
                    if "@" in user_input:
                        return user_input
                    else:
                        print("Please enter a valid email address.")
                        continue
                else:
                    return user_input
                    
            except ValueError:
                print(f"Please enter a valid {input_type}.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return ""
    
    def confirm_action(self, message: str) -> bool:
        """
        Ask for user confirmation
        
        Args:
            message (str): Confirmation message
            
        Returns:
            bool: True if confirmed
        """
        response = input(f"{message} (y/N): ").strip().lower()
        return response in ['y', 'yes']
    
    def display_progress_bar(self, current: int, total: int, prefix: str = "Progress"):
        """
        Display progress bar
        
        Args:
            current (int): Current progress
            total (int): Total items
            prefix (str): Progress description
        """
        if total == 0:
            return
        
        percent = int((current / total) * 100)
        bar_length = 40
        filled_length = int(bar_length * current // total)
        
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f'\r{prefix}: |{bar}| {percent}% ({current}/{total})', end='', flush=True)
        
        if current == total:
            print()  # New line when complete
    
    def display_menu_with_options(self, title: str, options: List[str]) -> str:
        """
        Display menu with numbered options
        
        Args:
            title (str): Menu title
            options (List[str]): List of menu options
            
        Returns:
            str: Selected option number
        """
        print(f"\n{title}")
        print("=" * len(title))
        
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        print(self.sub_separator)
        return input("Enter your choice: ").strip()
    
    def display_search_results(self, results: List, query: str):
        """
        Display search results
        
        Args:
            results (List): Search results
            query (str): Search query
        """
        print(f"\n🔍 Search Results for: '{query}'")
        print(self.separator)
        
        if not results:
            print("No results found matching your search criteria.")
            print("\nSuggestions:")
            print("• Try using different keywords")
            print("• Check spelling")
            print("• Use broader search terms")
            return
        
        print(f"Found {len(results)} result(s):")
        for i, item in enumerate(results, 1):
            if hasattr(item, 'name'):  # Event object
                print(f"\n{i}. 📅 {item.name}")
                print(f"   Date: {item.date} at {item.time}")
                print(f"   Location: {item.location}")
                available = item.capacity - len(item.attendees)
                print(f"   Available: {available}/{item.capacity} spots")
            else:  # User object
                print(f"\n{i}. 👤 {item.name} ({item.username})")
                print(f"   Role: {item.get_role()}")
                print(f"   Email: {item.email}")
        
        print(self.sub_separator)
    
    def display_loading_message(self, message: str = "Loading..."):
        """Display loading message"""
        print(f"\n⏳ {message}")
    
    def display_completion_message(self, message: str = "Operation completed!"):
        """Display completion message"""
        print(f"\n✨ {message}")
    
    def display_help(self, topic: str = "general"):
        """
        Display help information
        
        Args:
            topic (str): Help topic
        """
        print(f"\n❓ Help - {topic.title()}")
        print(self.separator)
        
        if topic == "general":
            print("Campus Event Management System Help")
            print()
            print("This system allows you to:")
            print("• Search for campus events")
            print("• Register for events")
            print("• Manage your event registrations")
            print("• Create and organize events (with proper permissions)")
            print()
            print("Navigation:")
            print("• Use numeric menu choices")
            print("• Follow prompts for input")
            print("• Press Ctrl+C to cancel operations")
            
        elif topic == "search":
            print("Event Search Help")
            print()
            print("You can search for events by:")
            print("• Event name (partial matches allowed)")
            print("• Date (YYYY-MM-DD format)")
            print("• Location (partial matches allowed)")
            print()
            print("Examples:")
            print("• Search by name: 'conference' finds 'Tech Conference'")
            print("• Search by date: '2025-08-15'")
            print("• Search by location: 'hall' finds 'Main Hall'")
            
        elif topic == "registration":
            print("Event Registration Help")
            print()
            print("To register for an event:")
            print("1. Search for events")
            print("2. Note the Event ID")
            print("3. Use 'Register for Event' option")
            print("4. Enter the Event ID")
            print()
            print("Notes:")
            print("• You cannot register for full events")
            print("• You cannot register for past events")
            print("• You cannot register twice for the same event")
            
        print(self.sub_separator)
    
    def display_system_info(self):
        """Display system information"""
        print(f"\n🖥️  System Information")
        print(self.separator)
        print("Campus Event Management System v1.0")
        print("Developed with Python")
        print("Features: Role-based access, Event management, Reporting")
        print(f"Current date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(self.sub_separator)
    
    def display_footer(self):
        """Display footer information"""
        print("\n" + self.sub_separator)
        print("Campus Event Management System © 2025")
        print("For support, contact: admin@campus.edu")
        print(self.sub_separator)
    
    def pause(self):
        """Pause execution and wait for user input"""
        input("\nPress Enter to continue...")
    
    def display_export_success(self, filename: str):
        """Display export success message"""
        print(f"\n📁 Export successful!")
        print(f"File saved as: {filename}")
        print("You can open this file with spreadsheet software.")
    
    def display_import_results(self, results: Dict[str, int]):
        """Display import results"""
        print(f"\n📥 Import Results")
        print(self.separator)
        print(f"✅ Successfully imported: {results.get('success', 0)}")
        print(f"❌ Failed to import: {results.get('failed', 0)}")
        print(f"⚠️  Duplicates skipped: {results.get('duplicates', 0)}")
        print(self.sub_separator)
    
    def display_notification(self, message: str, notification_type: str = "info"):
        """
        Display notification with appropriate icon
        
        Args:
            message (str): Notification message
            notification_type (str): Type of notification (info, success, warning, error)
        """
        icons = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }
        
        icon = icons.get(notification_type, 'ℹ️')
        print(f"\n{icon} {message}")
    
    def format_datetime(self, datetime_str: str) -> str:
        """
        Format datetime string for display
        
        Args:
            datetime_str (str): ISO datetime string
            
        Returns:
            str: Formatted datetime
        """
        try:
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return datetime_str
    
    def truncate_text(self, text: str, max_length: int = 50) -> str:
        """
        Truncate text for display
        
        Args:
            text (str): Text to truncate
            max_length (int): Maximum length
            
        Returns:
            str: Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."


class ColorUI(UI):
    """Enhanced UI with color support (optional)"""
    
    def __init__(self):
        super().__init__()
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
    
    def colored_text(self, text: str, color: str) -> str:
        """
        Return colored text
        
        Args:
            text (str): Text to color
            color (str): Color name
            
        Returns:
            str: Colored text
        """
        color_code = self.colors.get(color, '')
        end_code = self.colors['end']
        return f"{color_code}{text}{end_code}"
    
    def display_success_message(self, message: str):
        """Display colored success message"""
        print(f"\n{self.colored_text('✅ SUCCESS:', 'green')} {message}")
    
    def display_error_message(self, message: str):
        """Display colored error message"""
        print(f"\n{self.colored_text('❌ ERROR:', 'red')} {message}")
    
    def display_warning_message(self, message: str):
        """Display colored warning message"""
        print(f"\n{self.colored_text('⚠️  WARNING:', 'yellow')} {message}")
    
    def display_info_message(self, message: str):
        """Display colored info message"""
        print(f"\n{self.colored_text('ℹ️  INFO:', 'blue')} {message}")


# Utility functions for UI formatting
def format_currency(amount: float) -> str:
    """Format currency for display"""
    return f"${amount:,.2f}"

def format_percentage(value: float) -> str:
    """Format percentage for display"""
    return f"{value:.1f}%"

def format_file_size(size_bytes: int) -> str:
    """Format file size for display"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def create_box(text: str, width: int = 60) -> str:
    """Create a text box around content"""
    lines = text.split('\n')
    max_line_length = max(len(line) for line in lines) if lines else 0
    box_width = min(max(max_line_length + 4, width), 80)
    
    box = "┌" + "─" * (box_width - 2) + "┐\n"
    
    for line in lines:
        padding = box_width - len(line) - 4
        box += f"│ {line}{' ' * padding} │\n"
    
    box += "└" + "─" * (box_width - 2) + "┘"
    return box