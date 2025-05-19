"""
Metrics visualization for the BEAMSim discrete-event simulation engine.

This module defines the MetricsVisualizer class, which provides methods
to visualize metrics collected during simulation runs.
"""

import matplotlib.pyplot as plt


class MetricsVisualizer:
    """
    A class for visualizing metrics collected during the simulation.
    """

    def __init__(self, metrics_collector):
        """
        Initialize the metrics visualizer.

        Args:
            metrics_collector (MetricsCollector): The metrics collector instance.
        """
        self.metrics_collector = metrics_collector

    def plot_bandwidth_usage(self):
        """
        Plot bandwidth usage for each node.
        """
        bandwidth = self.metrics_collector.bandwidth_usage
        nodes = list(bandwidth.keys())
        usage = list(bandwidth.values())

        plt.figure(figsize=(10, 6))
        plt.bar(nodes, usage, color='blue')
        plt.xlabel('Node ID')
        plt.ylabel('Bandwidth Usage (bytes)')
        plt.title('Bandwidth Usage per Node')
        plt.show()

    def plot_message_counts(self):
        """
        Plot the number of messages sent by each node.
        """
        message_counts = self.metrics_collector.message_counts
        nodes = list(message_counts.keys())
        counts = list(message_counts.values())

        plt.figure(figsize=(10, 6))
        plt.bar(nodes, counts, color='green')
        plt.xlabel('Node ID')
        plt.ylabel('Message Count')
        plt.title('Messages Sent per Node')
        plt.show()

    def plot_latency_distribution(self):
        """
        Plot the distribution of latency measurements.
        """
        latencies = self.metrics_collector.latency_measurements

        plt.figure(figsize=(10, 6))
        plt.hist(latencies, bins=20, color='orange', edgecolor='black')
        plt.xlabel('Latency (ms)')
        plt.ylabel('Frequency')
        plt.title('Latency Distribution')
        plt.show()