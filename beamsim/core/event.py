"""
Event and EventQueue for the BEAMSim discrete-event simulation engine.

This module provides the Event class to represent individual simulation
events and the EventQueue class to manage a priority queue of events.
"""

import heapq

class Event:
    def __init__(self, timestamp, callback, *args, **kwargs):
        """
        Initialize an event.

        Args:
            timestamp (int): The time at which the event should occur.
            callback (callable): The function to execute for the event.
            *args: Positional arguments for the callback.
            **kwargs: Keyword arguments for the callback.
        """
        self.timestamp = timestamp
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __lt__(self, other):
        """Compare events based on their timestamp for priority queue ordering."""
        return self.timestamp < other.timestamp

    def execute(self):
        """Execute the event's callback function."""
        self.callback(*self.args, **self.kwargs)


class EventQueue:
    def __init__(self):
        """Initialize an empty event queue."""
        self.queue = []

    def add_event(self, event):
        """
        Add an event to the queue.

        Args:
            event (Event): The event to add.
        """
        heapq.heappush(self.queue, event)

    def pop_event(self):
        """
        Remove and return the next event from the queue.

        Returns:
            Event: The next event in the queue.
        """
        return heapq.heappop(self.queue) if self.queue else None

    def peek_next_event_time(self):
        """
        Get the timestamp of the next event without removing it.

        Returns:
            int: The timestamp of the next event, or None if the queue is empty.
        """
        return self.queue[0].timestamp if self.queue else None

    def is_empty(self):
        """
        Check if the event queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self.queue) == 0