"""
Simulator for the BEAMSim discrete-event simulation engine.

This module provides the main simulation engine, which manages the event
queue and processes events in a time-ordered manner.
"""

import heapq

class Simulator:
    def __init__(self):
        """Initialize the simulator with an empty event queue and clock."""
        self.event_queue = []
        self.current_time = 0
        self.running = False

    def schedule_event(self, event_time, event_callback, *args, **kwargs):
        """
        Schedule an event to be executed at a specific time.

        Args:
            event_time (int): The time at which the event should occur.
            event_callback (callable): The function to execute for the event.
            *args: Positional arguments for the callback.
            **kwargs: Keyword arguments for the callback.
        """
        heapq.heappush(self.event_queue, (event_time, event_callback, args, kwargs))

    def run(self, max_time=None):
        """
        Run the simulation until the event queue is empty or max_time is reached.

        Args:
            max_time (int, optional): The maximum simulation time. Defaults to None.
        """
        self.running = True
        while self.event_queue and self.running:
            event_time, event_callback, args, kwargs = heapq.heappop(self.event_queue)
            if max_time is not None and event_time > max_time:
                break
            self.current_time = event_time
            event_callback(*args, **kwargs)

    def stop(self):
        """Stop the simulation."""
        self.running = False

    def reset(self):
        """Reset the simulation to its initial state."""
        self.event_queue = []
        self.current_time = 0
        self.running = False