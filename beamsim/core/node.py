"""
Node class for the BEAMSim discrete-event simulation engine.

This module provides the base Node class, which represents a generic
participant in the network simulation.
"""

class Node:
    def __init__(self, node_id, simulator):
        """
        Initialize a node.

        Args:
            node_id (int): Unique identifier for the node.
            simulator (Simulator): Reference to the simulation engine.
        """
        self.node_id = node_id
        self.simulator = simulator
        self.state = {}
        self.neighbors = []

    def add_neighbor(self, neighbor):
        """
        Add a neighboring node.

        Args:
            neighbor (Node): The neighboring node to add.
        """
        self.neighbors.append(neighbor)

    def send_message(self, recipient, message, delay=0):
        """
        Send a message to a recipient.

        Args:
            recipient (Node): The recipient node.
            message (dict): The message to send.
            delay (int): Delay (in simulation time) before the message is delivered.
        """
        def deliver_message():
            recipient.receive_message(self, message)
        self.simulator.schedule_event(self.simulator.current_time + delay, deliver_message)

    def receive_message(self, sender, message):
        """
        Handle an incoming message.

        Args:
            sender (Node): The node that sent the message.
            message (dict): The received message.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def process_event(self, event):
        """
        Process an event specific to this node.

        Args:
            event (Event): The event to process.
        """
        raise NotImplementedError("Subclasses must implement this method.")