"""
Network topology interface for the BEAMSim discrete-event simulation engine.

This module provides the abstract base class for all network topology
implementations, defining the common interface for establishing connections
between nodes and handling message routing.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Set, Callable, Any, Optional


class NetworkTopology(ABC):
    """
    Abstract base class for network topology implementations.

    This class defines the common interface for all network topologies in the
    simulation, including methods for node connection and message routing.
    """

    def __init__(self, simulator):
        """
        Initialize a network topology.

        Args:
            simulator: The simulator instance managing the simulation.
        """
        self.simulator = simulator
        self.nodes = []
        self.node_connections = {}  # Maps node_id to a set of connected node_ids
        
    def add_node(self, node):
        """
        Add a node to the network topology.

        Args:
            node: The node to add to the network.
        """
        self.nodes.append(node)
        self.node_connections[node.node_id] = set()

    @abstractmethod
    def connect_nodes(self, params: Dict[str, Any]) -> None:
        """
        Establish connections between nodes according to the topology.

        Args:
            params: Parameters specific to the topology implementation.
        """
        pass

    @abstractmethod
    def route_message(self, sender, recipient, message, **kwargs) -> None:
        """
        Route a message from a sender to a recipient according to the topology.

        Args:
            sender: The node sending the message.
            recipient: The node receiving the message, or None for broadcast.
            message: The message to be routed.
            **kwargs: Additional routing parameters.
        """
        pass

    def are_connected(self, node1, node2) -> bool:
        """
        Check if two nodes are directly connected in the topology.

        Args:
            node1: First node to check.
            node2: Second node to check.

        Returns:
            bool: True if the nodes are directly connected, False otherwise.
        """
        return (node1.node_id in self.node_connections.get(node2.node_id, set()) or
                node2.node_id in self.node_connections.get(node1.node_id, set()))

    def get_neighbors(self, node) -> List:
        """
        Get all directly connected neighbors of a node.

        Args:
            node: The node to get neighbors for.

        Returns:
            List: List of neighboring nodes.
        """
        neighbor_ids = self.node_connections.get(node.node_id, set())
        return [n for n in self.nodes if n.node_id in neighbor_ids]

    @abstractmethod
    def calculate_latency(self, sender, recipient) -> int:
        """
        Calculate network latency between two nodes.

        Args:
            sender: The sending node.
            recipient: The receiving node.

        Returns:
            int: Latency in milliseconds.
        """
        pass

    @abstractmethod
    def calculate_bandwidth_usage(self, message) -> int:
        """
        Calculate the bandwidth usage of a message.

        Args:
            message: The message being sent.

        Returns:
            int: Bandwidth usage in bytes.
        """
        pass

    def register_metrics_collector(self, collector) -> None:
        """
        Register a metrics collector to track network statistics.

        Args:
            collector: The metrics collector to register.
        """
        self.metrics_collector = collector