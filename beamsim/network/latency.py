"""
Latency model for the BEAMSim discrete-event simulation engine.

This module provides the LatencyModel class, which calculates network latency
between nodes based on configurable parameters and distributions.
"""

import random


class LatencyModel:
    """
    A model for calculating network latency between nodes.
    """

    def __init__(self, min_latency_ms=10, max_latency_ms=100, distribution="normal", random_seed=42):
        """
        Initialize the latency model.

        Args:
            min_latency_ms (int): Minimum latency in milliseconds.
            max_latency_ms (int): Maximum latency in milliseconds.
            distribution (str): Latency distribution type ("normal" or "uniform").
            random_seed (int): Seed for random number generation.
        """
        self.min_latency_ms = min_latency_ms
        self.max_latency_ms = max_latency_ms
        self.distribution = distribution
        random.seed(random_seed)

    def calculate_latency(self, sender, recipient):
        """
        Calculate the latency between two nodes.

        Args:
            sender: The sending node.
            recipient: The receiving node.

        Returns:
            int: Latency in milliseconds.
        """
        if self.distribution == "normal":
            mean = (self.min_latency_ms + self.max_latency_ms) / 2
            stddev = (self.max_latency_ms - self.min_latency_ms) / 6  # 99.7% within range
            latency = random.gauss(mean, stddev)
        elif self.distribution == "uniform":
            latency = random.uniform(self.min_latency_ms, self.max_latency_ms)
        else:
            raise ValueError(f"Unsupported distribution: {self.distribution}")

        # Clamp latency to the specified range
        return max(self.min_latency_ms, min(self.max_latency_ms, int(latency)))