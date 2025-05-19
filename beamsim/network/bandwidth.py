"""
Bandwidth tracking for the BEAMSim discrete-event simulation engine.

This module provides the BandwidthTracker class, which monitors and calculates
bandwidth usage for nodes in the network simulation.
"""

class BandwidthTracker:
    """
    A class to track bandwidth usage for nodes in the simulation.
    """

    def __init__(self):
        """
        Initialize the bandwidth tracker.
        """
        self.bandwidth_usage = {}  # Maps node_id to {'sent': int, 'received': int}

    def register_node(self, node_id):
        """
        Register a node for bandwidth tracking.

        Args:
            node_id (int): The unique identifier of the node.
        """
        if node_id not in self.bandwidth_usage:
            self.bandwidth_usage[node_id] = {'sent': 0, 'received': 0}

    def record_sent(self, node_id, data_size):
        """
        Record data sent by a node.

        Args:
            node_id (int): The unique identifier of the node.
            data_size (int): The size of the data sent (in bytes).
        """
        if node_id in self.bandwidth_usage:
            self.bandwidth_usage[node_id]['sent'] += data_size

    def record_received(self, node_id, data_size):
        """
        Record data received by a node.

        Args:
            node_id (int): The unique identifier of the node.
            data_size (int): The size of the data received (in bytes).
        """
        if node_id in self.bandwidth_usage:
            self.bandwidth_usage[node_id]['received'] += data_size

    def get_bandwidth_usage(self, node_id):
        """
        Get the bandwidth usage for a specific node.

        Args:
            node_id (int): The unique identifier of the node.

        Returns:
            dict: A dictionary with 'sent' and 'received' bandwidth usage.
        """
        return self.bandwidth_usage.get(node_id, {'sent': 0, 'received': 0})

    def get_total_bandwidth_usage(self):
        """
        Get the total bandwidth usage across all nodes.

        Returns:
            dict: A dictionary with total 'sent' and 'received' bandwidth usage.
        """
        total_sent = sum(node['sent'] for node in self.bandwidth_usage.values())
        total_received = sum(node['received'] for node in self.bandwidth_usage.values())
        return {'sent': total_sent, 'received': total_received}