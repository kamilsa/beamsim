"""
Metrics collection for the BEAMSim discrete-event simulation engine.

This module defines the MetricsCollector class, which collects and stores
metrics during simulation runs.
"""

class MetricsCollector:
    """
    A class for collecting and storing metrics during the simulation.
    """

    def __init__(self):
        """
        Initialize the metrics collector.
        """
        self.bandwidth_usage = {}
        self.message_counts = {}
        self.latency_measurements = []

    def record_bandwidth(self, node_id, bytes_used):
        """
        Record bandwidth usage for a node.

        Args:
            node_id (int): The ID of the node.
            bytes_used (int): The number of bytes used.
        """
        if node_id not in self.bandwidth_usage:
            self.bandwidth_usage[node_id] = 0
        self.bandwidth_usage[node_id] += bytes_used

    def record_message(self, node_id):
        """
        Record a message sent by a node.

        Args:
            node_id (int): The ID of the node.
        """
        if node_id not in self.message_counts:
            self.message_counts[node_id] = 0
        self.message_counts[node_id] += 1

    def record_latency(self, latency):
        """
        Record a latency measurement.

        Args:
            latency (float): The latency in milliseconds.
        """
        self.latency_measurements.append(latency)

    def get_metrics(self):
        """
        Retrieve all collected metrics.

        Returns:
            dict: A dictionary containing all metrics.
        """
        return {
            "bandwidth_usage": self.bandwidth_usage,
            "message_counts": self.message_counts,
            "latency_measurements": self.latency_measurements,
        }