"""
Grid protocol implementation for the BEAMSim discrete-event simulation engine.

This module defines the GridProtocol class, which simulates the behavior of a
grid-based communication protocol for message propagation in the network.
"""

class GridProtocol:
    """
    A class representing the Grid protocol for message propagation.
    """

    def __init__(self, node_id, grid_size, row_neighbors, col_neighbors):
        """
        Initialize the Grid protocol.

        Args:
            node_id (int): The ID of the node using this protocol.
            grid_size (tuple[int, int]): The dimensions of the grid (rows, columns).
            row_neighbors (list[int]): List of neighbor node IDs in the same row.
            col_neighbors (list[int]): List of neighbor node IDs in the same column.
        """
        self.node_id = node_id
        self.grid_size = grid_size
        self.row_neighbors = row_neighbors
        self.col_neighbors = col_neighbors
        self.messages = set()

    def propagate_message(self, message_id, message):
        """
        Propagate a message to row and column neighbors.

        Args:
            message_id (str): Unique identifier for the message.
            message (str): The content of the message.
        """
        if message_id not in self.messages:
            self.messages.add(message_id)
            for neighbor in self.row_neighbors + self.col_neighbors:
                self.send_message(neighbor, message_id, message)

    def send_message(self, neighbor, message_id, message):
        """
        Simulate sending a message to a neighbor.

        Args:
            neighbor (int): The ID of the neighbor to send the message to.
            message_id (str): Unique identifier for the message.
            message (str): The content of the message.
        """
        # Placeholder for actual message sending logic
        print(f"Node {self.node_id} sent message {message_id} to neighbor {neighbor}")