"""
Metrics collection and visualization for the BEAMSim discrete-event simulation engine.

This module provides tools for collecting, analyzing, and visualizing metrics
from simulation runs, including bandwidth usage, aggregation progress, message counts,
and latency measurements.
"""

# Import metrics-related classes to make them available directly from beamsim.metrics
from beamsim.metrics.collector import MetricsCollector
from beamsim.metrics.visualizer import MetricsVisualizer

__all__ = [
    'MetricsCollector',
    'MetricsVisualizer',
]