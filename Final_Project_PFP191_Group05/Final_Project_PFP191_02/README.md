# Campus Event Management System

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [User Roles & Permissions](#user-roles--permissions)
- [Code Structure](#code-structure)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The Campus Event Management System is a comprehensive Python application designed to manage campus events with role-based access control. The system supports event creation, registration, capacity management, and detailed reporting capabilities.

### 🎪 Key Objectives
- **Role-Based Access Control**: Different permissions for Admins, Event Organizers, Students, and Visitors
- **Event Management**: Complete CRUD operations for campus events
- **Registration System**: Automated attendee registration with capacity management
- **Reporting & Analytics**: Comprehensive statistics and exportable reports
- **Data Persistence**: JSON and CSV file-based data storage

## ✨ Features

### 🔐 Authentication & Authorization
- Secure user login/logout system
- Account lockout protection after failed attempts
- Session management with automatic timeout
- Password strength validation

### 📅 Event Management
- Create, update, and delete events
- Capacity management with overflow protection
- Event search by name, date, and location
- Event status tracking (active, cancelled, completed)
- Automated validation for dates, times, and capacities

### 👥 User Registration
- Multi-role user registration (Student, Visitor, Event Organizer)
- Profile management and updates
- Event registration/unregistration
- Duplicate registration prevention

### 📊 Reporting & Analytics
- Attendance reports with fill rates
- User engagement statistics
- Event popularity analysis
- Exportable CSV reports
- System usage metrics

### 💾 Data Management
- JSON-based data persistence
- CSV import/export functionality
- Automated backup system
- Data validation and sanitization

## 🏗️ System Architecture

### Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │     UI      │  │   Menus     │  │    User Input       │  │
│  │  (views/)   │  │             │  │   Validation        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Event     │  │    User     │  │   Authentication    │  │
│  │ Controller  │  │ Controller  │  │    Controller       │  │
│  │(controllers)│  │             │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │    Event    │  │    User     │  │    File Manager     │  │
│  │   Models    │  │   Models    │  │   (JSON/CSV I/O)    │  │
│  │  (models/)  │  │             │  │    (utils/)         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Design Patterns Used
- **Model-View-Controller (MVC)**: Separation of concerns
- **Factory Pattern**: User creation based on roles
- **Builder Pattern**: Event creation with validation
- **Observer Pattern**: Event notifications (future enhancement)

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- No additional dependencies required (uses only Python standard library)

### Installation Steps

1. **Clone/Download the Project**
   ```bash
   # Create project directory
   mkdir campus_event_system
   cd campus_event_system
   ```

2. **Create Directory Structure**
   ```
   campus_event_system/
   ├── main.py
   ├── models/
   │   ├── __init__.py
   │   ├── user.py
   │   └── event.py
   ├── controllers/
   │   ├── __init__.py
   │   ├── event_controller.py
   │   ├── user_controller.py
   │   └── auth_controller.py
   ├── views/
   │   ├── __init__.py
   │   └── ui.py
   ├── utils/
   │   ├── __init__.py
   │   ├── file_manager.py
   │   └── validators.py
   ├── data/
   │   ├── events.json
   │   ├── users.json
   │   └── reports/
   └── README.md
   ```

3. **Create Empty __init__.py Files**
   ```bash
   # Linux/Mac
   touch models/__init__.py controllers/__init__.py views/__init__.py utils/__init__.py
   
   # Windows
   type nul > models\__init__.py
   type nul > controllers\__init__.py
   type nul > views\__init__.py
   type nul > utils\__init__.py
   ```

4. **Copy the Source Code**
   - Copy each module code to its respective file
   - Ensure all files are saved with UTF-8 encoding

5. **Run the Application**
   ```bash
   python main.py
   ```

### First Run
On first startup, the system will:
- Create data directories automatically
- Initialize with a default admin account:
  - **Username**: `admin`
  - **Password**: `admin123`
- Display the welcome screen

## 📖 Usage Guide

### Initial Login
1. Start the application: `python main.py`
2. Choose "1. Login" from the authentication menu
3. Use default admin credentials to first access
4. Change the default password immediately for security

### Creating Your First Event (Admin/Organizer)
1. Login with appropriate credentials
2. Select "Create New Event"
3. Fill in event details:
   - **Name**: Descriptive event name
   - **Description**: Event details
   - **Date**: YYYY-MM-DD format
   - **Time**: HH:MM format (24-hour)
   - **Location**: Venue information
   - **Capacity**: Maximum attendees (positive integer)

### Registering Users
1. From main menu, select "Register New Account"
2. Choose user role:
   - **Student**: Requires Student ID
   - **Visitor**: Optional organization
   - **Event Organizer**: Requires department
3. Fill in required information
4. System validates all inputs automatically

### Searching and Registering for Events
1. Login as Student or Visitor
2. Select "Search Events"
3. Choose search method:
   - View all upcoming events
   - Search by name (partial matches allowed)
   - Search by date (exact date match)
   - Search by location (partial matches allowed)
4. Note the Event ID for registration
5. Select "Register for Event" and enter Event ID

### Generating Reports (Admin Only)
1. Login as Administrator
2. Select "Generate Reports"
3. Choose report type:
   - **Overall Statistics**: System summary
   - **Event Attendance Report**: CSV export
   - **User Registration Report**: User statistics
   - **Export All Data**: Complete system backup

## 👤 User Roles & Permissions

### 🔴 Administrator
**Full System Access**
- ✅ Create, update, delete all events
- ✅ View all events and attendees
- ✅ Manage user accounts
- ✅ Generate comprehensive reports
- ✅ Access system statistics
- ✅ Export/import data
- ✅ User management functions

### 🟡 Event Organizer
**Event Management Focus**
- ✅ Create and manage own events
- ✅ View attendees for own events
- ✅ Update own event details
- ✅ Generate statistics for own events
- ✅ Register for other events
- ❌ Cannot manage other organizers' events
- ❌ Cannot access system-wide reports

### 🟢 Student
**Event Participation**
- ✅ Search all events
- ✅ Register for events
- ✅ View own registrations
- ✅ Unregister from events
- ❌ Cannot create events
- ❌ Cannot view attendee lists

### 🔵 Visitor
**Limited Event Access**
- ✅ Search public events
- ✅ Register for events
- ✅ View own registrations
- ✅ Unregister from events
- ❌ Cannot create events
- ❌ Cannot view attendee lists

## 📁 Code Structure

### Directory Overview
```
campus_event_system/
├── main.py                          # Application entry point
├── models/                          # Data models
│   ├── user.py                      # User classes & inheritance
│   └── event.py                     # Event model & utilities
├── controllers/                     # Business logic
│   ├── event_controller.py          # Event operations
│   ├── user_controller.py           # User management
│   └── auth_controller.py           # Authentication
├── views/                           # User interface
│   └── ui.py                        # Console UI components
├── utils/                           # Utilities
│   ├── file_manager.py              # File I/O operations
│   └── validators.py                # Input validation
└── data/                            # Data storage
    ├── events.json                  # Event data
    ├── users.json                   # User data
    └── reports/                     # Generated reports
```

### Key Classes

#### User Hierarchy
```python
User (Abstract Base Class)
├── Admin              # Full system access
├── EventOrganizer     # Event management capabilities
├── Student            # Basic event participation
└── Visitor            # Limited event access
```

#### Core Models
- **Event**: Event data and operations
- **EventController**: Event business logic
- **UserController**: User management logic
- **AuthController**: Authentication and authorization
- **FileManager**: Data persistence operations
- **InputValidator**: Input validation utilities

### Design Principles
- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Easy to extend with new user types
- **Liskov Substitution**: All user types work interchangeably
- **Interface Segregation**: Role-specific interfaces
- **Dependency Inversion**: Controllers depend on abstractions

## 🔧 API Documentation

### Event Controller Methods
```python
# Event CRUD Operations
add_event(event: Event) -> bool
get_event_by_id(event_id: str) -> Optional[Event]
update_event(event_id: str, **updates) -> bool
delete_event(event_id: str) -> bool

# Event Search & Filtering
search_events_by_name(name: str) -> List[Event]
search_events_by_date(date: str) -> List[Event]
search_events_by_location(location: str) -> List[Event]
get_upcoming_events() -> List[Event]

# Registration Management
register_attendee(event_id: str, user: User) -> bool
unregister_attendee(event_id: str, user: User) -> bool

# Analytics & Reporting
get_system_statistics() -> Dict[str, Any]
get_attendance_report() -> List[Dict[str, Any]]
```

### User Controller Methods
```python
# User CRUD Operations
add_user(user: User) -> bool
get_user_by_id(user_id: str) -> Optional[User]
get_user_by_username(username: str) -> Optional[User]
update_user(user_id: str, **updates) -> bool
delete_user(user_id: str) -> bool

# User Management
get_users_by_role(role: str) -> List[User]
search_users(query: str) -> List[User]
get_user_statistics() -> Dict[str, int]
```

### Authentication Controller Methods
```python
# Authentication
authenticate(username: str, password: str) -> Optional[User]
logout(user_id: str) -> bool
is_authenticated(user_id: str) -> bool

# Authorization
authorize_event_management(user: User, event_organizer_id: str) -> bool
authorize_user_management(user: User) -> bool
get_user_permissions(user: User) -> Dict[str, bool]

# Security
reset_user_password(admin_user: User, target_username: str, new_password: str) -> bool
unlock_account(admin_user: User, username: str) -> bool
```

## 📊 Data Models

### Event Data Structure
```json
{
  "event_id": "uuid-string",
  "name": "Event Name",
  "description": "Event description",
  "date": "2025-12-25",
  "time": "14:30",
  "location": "Event venue",
  "capacity": 100,
  "organizer_id": "organizer-uuid",
  "attendees": ["user-id-1", "user-id-2"],
  "created_at": "2025-07-23T10:30:00",
  "updated_at": "2025-07-23T11:00:00",
  "status": "active"
}
```

### User Data Structure
```json
{
  "user_id": "uuid-string",
  "username": "johndoe",
  "password": "hashed-password",
  "name": "John Doe",
  "email": "john@campus.edu",
  "user_type": "student",
  "created_at": "2025-07-23T09:00:00",
  "registered_events": ["event-id-1", "event-id-2"],
  "student_id": "STU123456"  // Role-specific field
}
```

## 🎨 Screenshots

### Welcome Screen
```
================================================================================
               🎓 CAMPUS EVENT MANAGEMENT SYSTEM 🎓
================================================================================

Welcome to the Campus Event Management System!
This system helps manage campus events with role-based access control.

Features:
• Event creation and management
• User registration and authentication
• Capacity management and tracking
• Comprehensive reporting system
• Role-based access control

--------------------------------------------------------------------------------

==============================
     AUTHENTICATION MENU
==============================
1. Login
2. Register New Account
3. Exit System
--------------------------------------------------------------------------------
```

### Admin Dashboard
```
========================================
         ADMINISTRATOR MENU
========================================
1. Create New Event
2. View All Events
3. Update Event
4. Delete Event
5. View All Attendees
6. Generate Reports
7. User Management
8. Logout
--------------------------------------------------------------------------------
```

### Event Display
```
📅 Tech Conference 2025
   ID: 123e4567-e89b-12d3-a456-426614174000
   📝 Annual technology conference for students and professionals
   📅 2025-08-15 at 09:00
   📍 Main Auditorium
   👥 75/150 attendees (50.0% full)
   ⭐ Status: Active
--------------------------------------------------------------------------------
```

### Statistics Report
```
📊 System Statistics
================================================================================
Total Events: 25
Total Attendees: 450
Average Attendees Per Event: 18.0
Most Popular Event:
  Name: Tech Conference 2025
  Attendees: 75
Least Popular Event:
  Name: Study Group Session
  Attendees: 5
Upcoming Events: 12
Capacity Utilization: 65.5%
--------------------------------------------------------------------------------
```

## 🧪 Testing

### Manual Testing Checklist

#### Authentication Tests
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Account lockout after multiple failed attempts
- [ ] Session timeout functionality
- [ ] Password change functionality

#### Event Management Tests
- [ ] Create event with valid data
- [ ] Create event with invalid data (validation)
- [ ] Update existing event
- [ ] Delete event
- [ ] Search events by different criteria

#### Registration Tests
- [ ] Register for available event
- [ ] Attempt to register for full event
- [ ] Attempt duplicate registration
- [ ] Unregister from event
- [ ] Register different user types

#### File Operations Tests
- [ ] Data persistence across restarts
- [ ] CSV export functionality
- [ ] Report generation
- [ ] Backup and restore

### Running Tests
```bash
# Basic functionality test
python main.py

# Test with different user roles
# 1. Login as admin (admin/admin123)
# 2. Create test events
# 3. Register as different user types
# 4. Test all menu functions
```

## 🔧 Configuration

### System Settings
The system can be configured by modifying constants in the relevant modules:

#### File Manager Settings (utils/file_manager.py)
```python
DATA_DIR = "data"                    # Data directory
BACKUP_RETENTION_DAYS = 30           # Backup retention period
MAX_EXPORT_ROWS = 10000             # Maximum rows in exports
```

#### Authentication Settings (controllers/auth_controller.py)
```python
MAX_FAILED_ATTEMPTS = 5              # Login attempt limit
LOCKOUT_DURATION = 300               # Lockout time in seconds
SESSION_DURATION = 8                 # Session duration in hours
```

#### Validation Settings (utils/validators.py)
```python
MIN_PASSWORD_LENGTH = 6              # Minimum password length
MAX_EVENT_CAPACITY = 10000           # Maximum event capacity
MAX_USERNAME_LENGTH = 50             # Maximum username length
```

## 🚨 Error Handling

### Common Error Scenarios
1. **File Permission Errors**: Ensure write permissions for data directory
2. **Invalid Date Formats**: Use YYYY-MM-DD format for dates
3. **Capacity Exceeded**: Cannot register when event is full
4. **Duplicate Registration**: User already registered for event
5. **Authentication Failures**: Invalid credentials or expired session

### Error Recovery
- Automatic session recovery on restart
- Data validation prevents corrupt entries
- Graceful degradation when files are unavailable
- Clear error messages guide user actions

## 🔐 Security Considerations

### Implemented Security Features
- Input validation and sanitization
- SQL injection prevention (though not using SQL)
- XSS pattern detection
- Account lockout protection
- Session management
- Password strength validation

### Security Recommendations
- Change default admin password immediately
- Use strong passwords for all accounts
- Regular backup of data files
- Monitor system logs for suspicious activity
- Implement HTTPS in production environments

## 📈 Performance Considerations

### Current Limitations
- In-memory data storage (suitable for small to medium datasets)
- Linear search algorithms (O(n) complexity)
- No database indexing
- Single-threaded operation

### Scalability Recommendations
- Implement database backend for large datasets
- Add caching mechanisms
- Implement pagination for large result sets
- Consider multi-threading for concurrent users

## 🛠️ Troubleshooting

### Common Issues

#### "Permission Denied" Error
```bash
# Solution: Ensure data directory is writable
chmod 755 data/
```

#### "Module Not Found" Error
```bash
# Solution: Ensure all __init__.py files exist
touch models/__init__.py controllers/__init__.py views/__init__.py utils/__init__.py
```

#### Data Not Persisting
- Check file permissions in data directory
- Ensure system exits gracefully (not force-killed)
- Verify JSON file format is valid

#### Performance Issues
- Large event lists may cause slowdowns
- Consider implementing pagination
- Regular cleanup of old data

## 🔄 Future Enhancements

### Planned Features
- [ ] Web-based interface
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Email notifications
- [ ] Calendar integration
- [ ] Multi-language support
- [ ] Mobile application
- [ ] Real-time updates
- [ ] Advanced analytics dashboard

### Technical Improvements
- [ ] Unit testing framework
- [ ] Continuous integration
- [ ] Docker containerization
- [ ] API endpoints (REST/GraphQL)
- [ ] Caching system
- [ ] Logging framework
- [ ] Configuration management

## 🤝 Contributing

### Development Guidelines
1. Follow PEP 8 style guidelines
2. Add docstrings to all functions
3. Include error handling
4. Write unit tests for new features
5. Update documentation

### Code Style
```python
# Use clear, descriptive names
def calculate_event_fill_percentage(event: Event) -> float:
    """Calculate the fill percentage for an event."""
    if event.capacity == 0:
        return 0.0
    return (len(event.attendees) / event.capacity) * 100

# Include type hints
def get_user_by_id(self, user_id: str) -> Optional[User]:
    """Get user by ID with proper type hints."""
    pass
```

### Submission Process
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 📞 Support

For technical support or questions:
- **Email**: admin@campus.edu
- **Documentation**: This README file
- **Issues**: GitHub Issues (if applicable)

## 🙏 Acknowledgments

- Python Software Foundation for the excellent programming language
- Contributors to the open-source community
- Educational institutions using this system

---

**Campus Event Management System v1.0**  
*Developed with ❤️ for educational purposes*
