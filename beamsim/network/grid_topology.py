"""
Grid communication topology for the BEAMSim discrete-event simulation engine.

This module implements a grid-based communication model where nodes are
organized in a 2D grid and communicate with their neighbors.
"""

from beamsim.network.topology import NetworkTopology
import math


class GridTopology(NetworkTopology):
    """
    Grid communication topology implementation.
    """

    def __init__(self, simulator, grid_size=None):
        """
        Initialize the Grid topology.

        Args:
            simulator: The simulator instance managing the simulation.
            grid_size (int): The size of the grid (number of nodes per row/column).
        """
        super().__init__(simulator)
        self.grid_size = grid_size

    def connect_nodes(self, params):
        """
        Establish grid connections between nodes.

        Args:
            params (dict): Parameters including 'validators'.
        """
        nodes = params.get('validators', [])
        for node in nodes:
            self.add_node(node)

        if not self.grid_size:
            self.grid_size = math.ceil(math.sqrt(len(self.nodes)))

        for idx, node in enumerate(self.nodes):
            row, col = divmod(idx, self.grid_size)
            neighbors = self._get_neighbors(row, col)
            for neighbor_idx in neighbors:
                neighbor = self.nodes[neighbor_idx]
                self.node_connections[node.node_id].add(neighbor.node_id)
                self.node_connections[neighbor.node_id].add(node.node_id)

    def _get_neighbors(self, row, col):
        """
        Get the indices of neighboring nodes in the grid.

        Args:
            row (int): Row index of the node.
            col (int): Column index of the node.

        Returns:
            list: Indices of neighboring nodes.
        """
        neighbors = []
        if row > 0:  # Up
            neighbors.append((row - 1) * self.grid_size + col)
        if row < self.grid_size - 1:  # Down
            neighbors.append((row + 1) * self.grid_size + col)
        if col > 0:  # Left
            neighbors.append(row * self.grid_size + col - 1)
        if col < self.grid_size - 1:  # Right
            neighbors.append(row * self.grid_size + col + 1)
        return neighbors

    def route_message(self, sender, recipient, message, **kwargs):
        """
        Route a message in the grid topology.

        Args:
            sender: The node sending the message.
            recipient: The node receiving the message, or None for broadcast.
            message: The message to be routed.
        """
        if recipient:
            # Directly send the message to the recipient
            self.simulator.schedule_event(
                sender=sender,
                recipient=recipient,
                message=message,
                latency=self.calculate_latency(sender, recipient)
            )
        else:
            # Broadcast to all connected neighbors
            visited = set()
            queue = [sender]
            while queue:
                current = queue.pop(0)
                if current.node_id not in visited:
                    visited.add(current.node_id)
                    for neighbor_id in self.node_connections[current.node_id]:
                        neighbor = next(node for node in self.nodes if node.node_id == neighbor_id)
                        self.simulator.schedule_event(
                            sender=current,
                            recipient=neighbor,
                            message=message,
                            latency=self.calculate_latency(current, neighbor)
                        )
                        queue.append(neighbor)

    def calculate_latency(self, sender, recipient):
        """
        Calculate latency between two nodes.

        Args:
            sender: The sending node.
            recipient: The receiving node.

        Returns:
            int: Latency in milliseconds.
        """
        return self.simulator.latency_model.calculate_latency(sender, recipient)

    def calculate_bandwidth_usage(self, message):
        """
        Calculate bandwidth usage for a message.

        Args:
            message: The message being sent.

        Returns:
            int: Bandwidth usage in bytes.
        """
        return len(message.payload)