"""
Event Controller Module

This module handles all event-related business logic and operations.
Manages event CRUD operations, registration, and statistics.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
from models.event import Event, sort_events_by_date, filter_upcoming_events
from models.user import User

class EventController:
    """Controller for managing events and registrations"""
    
    def __init__(self, file_manager=None):
        """
        Initialize event controller
        
        Args:
            file_manager: File manager instance for persistence
        """
        self.events = []  # List of Event objects
        self.file_manager = file_manager
    
    def add_event(self, event: Event) -> bool:
        """
        Add a new event to the system
        
        Args:
            event (Event): Event object to add
            
        Returns:
            bool: True if event added successfully
        """
        try:
            # Check for duplicate event names on the same date
            if self._is_duplicate_event(event):
                print(f"Warning: Event '{event.name}' already exists on {event.date}")
                return False
            
            self.events.append(event)
            return True
        except Exception as e:
            print(f"Error adding event: {e}")
            return False
    
    def get_event_by_id(self, event_id: str) -> Optional[Event]:
        """
        Get event by ID
        
        Args:
            event_id (str): Event ID to search for
            
        Returns:
            Event or None: Event object if found
        """
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None
    
    def get_all_events(self) -> List[Event]:
        """
        Get all events in the system
        
        Returns:
            List[Event]: List of all events
        """
        return self.events.copy()
    
    def get_upcoming_events(self) -> List[Event]:
        """
        Get all upcoming active events
        
        Returns:
            List[Event]: List of upcoming events sorted by date
        """
        upcoming = filter_upcoming_events(self.events)
        return sort_events_by_date(upcoming)
    
    def get_events_by_organizer(self, organizer_id: str) -> List[Event]:
        """
        Get all events organized by a specific user
        
        Args:
            organizer_id (str): Organizer's user ID
            
        Returns:
            List[Event]: List of events organized by the user
        """
        organizer_events = [event for event in self.events 
                          if event.organizer_id == organizer_id]
        return sort_events_by_date(organizer_events)
    
    def get_user_events(self, user_id: str) -> List[Event]:
        """
        Get all events a user is registered for
        
        Args:
            user_id (str): User's ID
            
        Returns:
            List[Event]: List of events user is registered for
        """
        user_events = [event for event in self.events 
                      if user_id in event.attendees]
        return sort_events_by_date(user_events)
    
    def update_event(self, event_id: str, **updates) -> bool:
        """
        Update event details
        
        Args:
            event_id (str): Event ID to update
            **updates: Fields to update
            
        Returns:
            bool: True if update successful
        """
        event = self.get_event_by_id(event_id)
        if not event:
            return False
        
        try:
            # Validate capacity update
            if 'capacity' in updates:
                new_capacity = updates['capacity']
                if new_capacity < len(event.attendees):
                    print(f"Cannot reduce capacity below current attendees ({len(event.attendees)})")
                    return False
            
            event.update_details(**updates)
            return True
        except Exception as e:
            print(f"Error updating event: {e}")
            return False
    
    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event from the system
        
        Args:
            event_id (str): Event ID to delete
            
        Returns:
            bool: True if deletion successful
        """
        event = self.get_event_by_id(event_id)
        if not event:
            return False
        
        try:
            self.events.remove(event)
            return True
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False
    
    def register_attendee(self, event_id: str, user: User) -> bool:
        """
        Register a user for an event
        
        Args:
            event_id (str): Event ID
            user (User): User object to register
            
        Returns:
            bool: True if registration successful
        """
        event = self.get_event_by_id(event_id)
        if not event:
            print("Event not found.")
            return False
        
        if event.status != "active":
            print(f"Cannot register for {event.status} event.")
            return False
        
        if not event.is_upcoming():
            print("Cannot register for past events.")
            return False
        
        if event.is_full():
            print("Event is at full capacity.")
            return False
        
        if event.is_attendee(user.user_id):
            print("You are already registered for this event.")
            return False
        
        # Add attendee to event
        if event.add_attendee(user.user_id):
            # Add event to user's registered events
            user.add_registered_event(event_id)
            return True
        
        return False
    
    def unregister_attendee(self, event_id: str, user: User) -> bool:
        """
        Unregister a user from an event
        
        Args:
            event_id (str): Event ID
            user (User): User object to unregister
            
        Returns:
            bool: True if unregistration successful
        """
        event = self.get_event_by_id(event_id)
        if not event:
            print("Event not found.")
            return False
        
        if not event.is_attendee(user.user_id):
            print("You are not registered for this event.")
            return False
        
        # Remove attendee from event
        if event.remove_attendee(user.user_id):
            # Remove event from user's registered events
            user.remove_registered_event(event_id)
            return True
        
        return False
    
    def search_events_by_name(self, name: str) -> List[Event]:
        """
        Search events by name (partial match)
        
        Args:
            name (str): Name to search for
            
        Returns:
            List[Event]: List of matching events
        """
        if not name.strip():
            return []
        
        name_lower = name.lower().strip()
        matching_events = [event for event in self.events 
                         if name_lower in event.name.lower() and event.status == "active"]
        return sort_events_by_date(matching_events)
    
    def search_events_by_date(self, search_date: str) -> List[Event]:
        """
        Search events by date
        
        Args:
            search_date (str): Date in YYYY-MM-DD format
            
        Returns:
            List[Event]: List of events on that date
        """
        matching_events = [event for event in self.events 
                         if event.date == search_date and event.status == "active"]
        return sort_events_by_date(matching_events)
    
    def search_events_by_location(self, location: str) -> List[Event]:
        """
        Search events by location (partial match)
        
        Args:
            location (str): Location to search for
            
        Returns:
            List[Event]: List of matching events
        """
        if not location.strip():
            return []
        
        location_lower = location.lower().strip()
        matching_events = [event for event in self.events 
                         if location_lower in event.location.lower() and event.status == "active"]
        return sort_events_by_date(matching_events)
    
    def get_events_by_capacity(self, min_capacity: int = 0, max_capacity: int = float('inf')) -> List[Event]:
        """
        Get events within capacity range
        
        Args:
            min_capacity (int): Minimum capacity
            max_capacity (int): Maximum capacity
            
        Returns:
            List[Event]: List of events within capacity range
        """
        filtered_events = [event for event in self.events 
                         if min_capacity <= event.capacity <= max_capacity]
        return sort_events_by_date(filtered_events)
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive system statistics
        
        Returns:
            dict: System statistics
        """
        if not self.events:
            return {
                'total_events': 0,
                'total_attendees': 0,
                'avg_attendees': 0,
                'most_popular_event': None,
                'least_popular_event': None,
                'upcoming_events': 0,
                'capacity_utilization': 0
            }
        
        total_attendees = sum(len(event.attendees) for event in self.events)
        total_capacity = sum(event.capacity for event in self.events)
        
        # Find most and least popular events
        events_with_attendees = [(event, len(event.attendees)) for event in self.events]
        events_with_attendees.sort(key=lambda x: x[1])
        
        most_popular = events_with_attendees[-1] if events_with_attendees else (None, 0)
        least_popular = events_with_attendees[0] if events_with_attendees else (None, 0)
        
        upcoming_events = len(self.get_upcoming_events())
        
        return {
            'total_events': len(self.events),
            'total_attendees': total_attendees,
            'avg_attendees': total_attendees / len(self.events) if self.events else 0,
            'most_popular_event': {
                'name': most_popular[0].name,
                'attendees': most_popular[1]
            } if most_popular[0] else None,
            'least_popular_event': {
                'name': least_popular[0].name,
                'attendees': least_popular[1]
            } if least_popular[0] else None,
            'upcoming_events': upcoming_events,
            'capacity_utilization': (total_attendees / total_capacity * 100) if total_capacity > 0 else 0
        }
    
    def get_attendance_report(self) -> List[Dict[str, Any]]:
        """
        Generate attendance report for all events
        
        Returns:
            List[dict]: Attendance data for each event
        """
        report = []
        for event in self.events:
            report.append({
                'event_id': event.event_id,
                'event_name': event.name,
                'date': event.date,
                'time': event.time,
                'location': event.location,
                'capacity': event.capacity,
                'attendees_count': len(event.attendees),
                'available_spots': event.get_available_spots(),
                'fill_percentage': round(event.get_fill_percentage(), 2),
                'status': event.status,
                'organizer_id': event.organizer_id
            })
        
        return sorted(report, key=lambda x: x['date'])
    
    def get_popular_events(self, limit: int = 5) -> List[Event]:
        """
        Get most popular events by attendance
        
        Args:
            limit (int): Maximum number of events to return
            
        Returns:
            List[Event]: Most popular events
        """
        sorted_events = sorted(self.events, key=lambda e: len(e.attendees), reverse=True)
        return sorted_events[:limit]
    
    def get_events_by_status(self, status: str) -> List[Event]:
        """
        Get events by status
        
        Args:
            status (str): Event status (active, cancelled, completed)
            
        Returns:
            List[Event]: Events with specified status
        """
        return [event for event in self.events if event.status == status]
    
    def cancel_event(self, event_id: str) -> bool:
        """
        Cancel an event
        
        Args:
            event_id (str): Event ID to cancel
            
        Returns:
            bool: True if cancellation successful
        """
        event = self.get_event_by_id(event_id)
        if not event:
            return False
        
        event.cancel_event()
        return True
    
    def complete_event(self, event_id: str) -> bool:
        """
        Mark an event as completed
        
        Args:
            event_id (str): Event ID to complete
            
        Returns:
            bool: True if completion successful
        """
        event = self.get_event_by_id(event_id)
        if not event:
            return False
        
        event.complete_event()
        return True
    
    def get_events_needing_attention(self) -> List[Event]:
        """
        Get events that need organizer attention (low attendance, etc.)
        
        Returns:
            List[Event]: Events needing attention
        """
        attention_events = []
        current_date = datetime.now().date()
        
        for event in self.events:
            if event.status != "active":
                continue
            
            try:
                event_date = datetime.strptime(event.date, "%Y-%m-%d").date()
                days_until_event = (event_date - current_date).days
                
                # Events within 7 days with low attendance (less than 25% capacity)
                if (0 <= days_until_event <= 7 and 
                    event.get_fill_percentage() < 25):
                    attention_events.append(event)
                    
            except ValueError:
                continue
        
        return attention_events
    
    def _is_duplicate_event(self, new_event: Event) -> bool:
        """
        Check if event with same name exists on same date
        
        Args:
            new_event (Event): Event to check for duplicates
            
        Returns:
            bool: True if duplicate exists
        """
        for event in self.events:
            if (event.name.lower() == new_event.name.lower() and 
                event.date == new_event.date and 
                event.status == "active"):
                return True
        return False
    
    def bulk_import_events(self, events_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Import multiple events from data
        
        Args:
            events_data (List[dict]): List of event dictionaries
            
        Returns:
            dict: Import results with success/failure counts
        """
        results = {'success': 0, 'failed': 0, 'duplicates': 0}
        
        for event_data in events_data:
            try:
                event = Event.from_dict(event_data)
                
                if self._is_duplicate_event(event):
                    results['duplicates'] += 1
                    continue
                
                if self.add_event(event):
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    
            except Exception as e:
                print(f"Error importing event: {e}")
                results['failed'] += 1
        
        return results
    
    def get_capacity_analysis(self) -> Dict[str, Any]:
        """
        Analyze capacity utilization across events
        
        Returns:
            dict: Capacity analysis data
        """
        if not self.events:
            return {}
        
        fill_percentages = [event.get_fill_percentage() for event in self.events]
        
        return {
            'avg_fill_percentage': sum(fill_percentages) / len(fill_percentages),
            'max_fill_percentage': max(fill_percentages),
            'min_fill_percentage': min(fill_percentages),
            'full_events': len([e for e in self.events if e.is_full()]),
            'empty_events': len([e for e in self.events if len(e.attendees) == 0]),
            'underutilized_events': len([e for e in self.events if e.get_fill_percentage() < 50])
        }