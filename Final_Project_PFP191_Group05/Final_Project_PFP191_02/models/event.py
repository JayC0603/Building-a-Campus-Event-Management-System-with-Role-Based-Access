"""
Event Model Module

This module contains the Event class and related functionality
for managing campus events with capacity control and attendee tracking.
"""

import uuid
from datetime import datetime, date, time
from typing import List, Dict, Any

class Event:
    """Event class for managing campus events"""
    
    def __init__(self, name: str, description: str, date: str, time: str, 
                 location: str, capacity: int, organizer_id: str):
        """
        Initialize an event
        
        Args:
            name (str): Event name
            description (str): Event description
            date (str): Event date in YYYY-MM-DD format
            time (str): Event time in HH:MM format
            location (str): Event location
            capacity (int): Maximum number of attendees
            organizer_id (str): ID of the event organizer
        """
        self.event_id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.date = date
        self.time = time
        self.location = location
        self.capacity = capacity
        self.organizer_id = organizer_id
        self.attendees = []  # List of user IDs registered for this event
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.status = "active"  # active, cancelled, completed
    
    def add_attendee(self, user_id: str) -> bool:
        """
        Add an attendee to the event
        
        Args:
            user_id (str): ID of the user to register
            
        Returns:
            bool: True if registration successful, False otherwise
        """
        if user_id in self.attendees:
            return False  # Already registered
        
        if len(self.attendees) >= self.capacity:
            return False  # Event is full
        
        self.attendees.append(user_id)
        self.updated_at = datetime.now().isoformat()
        return True
    
    def remove_attendee(self, user_id: str) -> bool:
        """
        Remove an attendee from the event
        
        Args:
            user_id (str): ID of the user to unregister
            
        Returns:
            bool: True if unregistration successful, False otherwise
        """
        if user_id not in self.attendees:
            return False  # Not registered
        
        self.attendees.remove(user_id)
        self.updated_at = datetime.now().isoformat()
        return True
    
    def is_full(self) -> bool:
        """Check if event has reached capacity"""
        return len(self.attendees) >= self.capacity
    
    def get_available_spots(self) -> int:
        """Get number of available spots"""
        return max(0, self.capacity - len(self.attendees))
    
    def is_attendee(self, user_id: str) -> bool:
        """Check if user is registered for this event"""
        return user_id in self.attendees
    
    def get_attendee_count(self) -> int:
        """Get current number of attendees"""
        return len(self.attendees)
    
    def get_fill_percentage(self) -> float:
        """Get event fill percentage"""
        if self.capacity == 0:
            return 0.0
        return (len(self.attendees) / self.capacity) * 100
    
    def is_upcoming(self) -> bool:
        """Check if event is in the future"""
        try:
            event_datetime = datetime.strptime(f"{self.date} {self.time}", "%Y-%m-%d %H:%M")
            return event_datetime > datetime.now()
        except ValueError:
            return False
    
    def is_today(self) -> bool:
        """Check if event is today"""
        try:
            event_date = datetime.strptime(self.date, "%Y-%m-%d").date()
            return event_date == date.today()
        except ValueError:
            return False
    
    def get_datetime(self) -> datetime:
        """Get event datetime as datetime object"""
        try:
            return datetime.strptime(f"{self.date} {self.time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return datetime.now()
    
    def update_details(self, **kwargs) -> None:
        """Update event details"""
        allowed_fields = ['name', 'description', 'date', 'time', 'location', 'capacity', 'status']
        
        for field, value in kwargs.items():
            if field in allowed_fields and hasattr(self, field):
                setattr(self, field, value)
        
        self.updated_at = datetime.now().isoformat()
    
    def cancel_event(self) -> None:
        """Cancel the event"""
        self.status = "cancelled"
        self.updated_at = datetime.now().isoformat()
    
    def complete_event(self) -> None:
        """Mark event as completed"""
        self.status = "completed"
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert event to dictionary for serialization
        
        Returns:
            dict: Event data as dictionary
        """
        return {
            'event_id': self.event_id,
            'name': self.name,
            'description': self.description,
            'date': self.date,
            'time': self.time,
            'location': self.location,
            'capacity': self.capacity,
            'organizer_id': self.organizer_id,
            'attendees': self.attendees.copy(),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """
        Create Event instance from dictionary
        
        Args:
            data (dict): Event data dictionary
            
        Returns:
            Event: New event instance
        """
        event = cls(
            name=data['name'],
            description=data['description'],
            date=data['date'],
            time=data['time'],
            location=data['location'],
            capacity=data['capacity'],
            organizer_id=data['organizer_id']
        )
        
        # Set additional fields
        event.event_id = data['event_id']
        event.attendees = data.get('attendees', [])
        event.created_at = data.get('created_at', datetime.now().isoformat())
        event.updated_at = data.get('updated_at', datetime.now().isoformat())
        event.status = data.get('status', 'active')
        
        return event
    
    def __str__(self) -> str:
        """String representation of event"""
        status_indicator = ""
        if self.status == "cancelled":
            status_indicator = " [CANCELLED]"
        elif self.status == "completed":
            status_indicator = " [COMPLETED]"
        elif self.is_full():
            status_indicator = " [FULL]"
        
        return (f"Event: {self.name}{status_indicator}\n"
                f"ID: {self.event_id}\n"
                f"Description: {self.description}\n"
                f"Date & Time: {self.date} at {self.time}\n"
                f"Location: {self.location}\n"
                f"Capacity: {len(self.attendees)}/{self.capacity}")
    
    def __repr__(self) -> str:
        """Developer representation of event"""
        return f"Event(id='{self.event_id}', name='{self.name}', date='{self.date}')"
    
    def __eq__(self, other) -> bool:
        """Check equality based on event ID"""
        if not isinstance(other, Event):
            return False
        return self.event_id == other.event_id
    
    def __hash__(self) -> int:
        """Hash based on event ID"""
        return hash(self.event_id)


class EventBuilder:
    """Builder pattern for creating events with validation"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset builder state"""
        self._name = ""
        self._description = ""
        self._date = ""
        self._time = ""
        self._location = ""
        self._capacity = 0
        self._organizer_id = ""
        return self
    
    def name(self, name: str):
        """Set event name"""
        self._name = name.strip()
        return self
    
    def description(self, description: str):
        """Set event description"""
        self._description = description.strip()
        return self
    
    def date(self, date: str):
        """Set event date"""
        self._date = date.strip()
        return self
    
    def time(self, time: str):
        """Set event time"""
        self._time = time.strip()
        return self
    
    def location(self, location: str):
        """Set event location"""
        self._location = location.strip()
        return self
    
    def capacity(self, capacity: int):
        """Set event capacity"""
        self._capacity = max(1, capacity)
        return self
    
    def organizer(self, organizer_id: str):
        """Set organizer ID"""
        self._organizer_id = organizer_id.strip()
        return self
    
    def build(self) -> Event:
        """Build and return the event"""
        if not all([self._name, self._date, self._time, self._location, 
                   self._organizer_id]) or self._capacity <= 0:
            raise ValueError("Missing required event fields")
        
        event = Event(
            name=self._name,
            description=self._description,
            date=self._date,
            time=self._time,
            location=self._location,
            capacity=self._capacity,
            organizer_id=self._organizer_id
        )
        
        self.reset()
        return event


# Utility functions for event management
def sort_events_by_date(events: List[Event], reverse: bool = False) -> List[Event]:
    """Sort events by date and time"""
    return sorted(events, key=lambda e: e.get_datetime(), reverse=reverse)

def filter_upcoming_events(events: List[Event]) -> List[Event]:
    """Filter events to only include upcoming ones"""
    return [event for event in events if event.is_upcoming() and event.status == "active"]

def filter_events_by_capacity(events: List[Event], min_available: int = 1) -> List[Event]:
    """Filter events by available capacity"""
    return [event for event in events if event.get_available_spots() >= min_available]

def get_events_by_date_range(events: List[Event], start_date: str, end_date: str) -> List[Event]:
    """Get events within a date range"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        result = []
        for event in events:
            try:
                event_date = datetime.strptime(event.date, "%Y-%m-%d")
                if start <= event_date <= end:
                    result.append(event)
            except ValueError:
                continue
        
        return result
    except ValueError:
        return []