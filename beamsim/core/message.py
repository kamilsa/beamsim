"""
Message class for the BEAMSim discrete-event simulation engine.

This module provides the base Message class, which represents a generic
message exchanged between nodes in the network simulation.
"""

class Message:
    def __init__(self, sender, recipient, timestamp, payload):
        """
        Initialize a message.

        Args:
            sender (Node): The node sending the message.
            recipient (Node): The node receiving the message.
            timestamp (int): The time the message is sent.
            payload (dict): The content of the message.
        """
        self.sender = sender
        self.recipient = recipient
        self.timestamp = timestamp
        self.payload = payload

    def __repr__(self):
        """
        Return a string representation of the message.

        Returns:
            str: A string describing the message.
        """
        return (f"Message(sender={self.sender.node_id}, "
                f"recipient={self.recipient.node_id}, "
                f"timestamp={self.timestamp}, "
                f"payload={self.payload})")