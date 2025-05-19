#!/usr/bin/env python3
"""
A simple simulation example using the BEAMSim framework.

This script demonstrates how to set up and run a basic simulation with
the direct communication topology (Topology 0).
"""

import os
import time
import argparse
import matplotlib.pyplot as plt

from beamsim.core import Simulator
from beamsim.utils.config import ConfigManager
from beamsim.metrics.collector import MetricsCollector


# Define the visualization functions that were missing
def plot_aggregation_progress(metrics_collector):
    """
    Plot the progress of signature aggregation over time.

    Args:
        metrics_collector: The metrics collector containing aggregation data.

    Returns:
        matplotlib.figure.Figure: The figure containing the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # If metrics_collector doesn't have this data yet, create empty plot
    if not hasattr(metrics_collector, 'aggregation_progress'):
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Signatures Aggregated')
        ax.set_title('Signature Aggregation Progress')
        return fig

    times = list(metrics_collector.aggregation_progress.keys())
    counts = list(metrics_collector.aggregation_progress.values())

    ax.plot(times, counts, marker='o', linestyle='-', color='blue')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Signatures Aggregated')
    ax.set_title('Signature Aggregation Progress')
    ax.grid(True)

    return fig


def plot_bandwidth_usage(metrics_collector):
    """
    Plot bandwidth usage for each node.

    Args:
        metrics_collector: The metrics collector containing bandwidth data.

    Returns:
        matplotlib.figure.Figure: The figure containing the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # If metrics_collector doesn't have this data yet, create empty plot
    if not hasattr(metrics_collector, 'bandwidth_usage') or not metrics_collector.bandwidth_usage:
        ax.set_xlabel('Node ID')
        ax.set_ylabel('Bandwidth Usage (bytes)')
        ax.set_title('Bandwidth Usage per Node')
        return fig

    nodes = list(metrics_collector.bandwidth_usage.keys())
    usage = list(metrics_collector.bandwidth_usage.values())

    ax.bar(nodes, usage, color='blue')
    ax.set_xlabel('Node ID')
    ax.set_ylabel('Bandwidth Usage (bytes)')
    ax.set_title('Bandwidth Usage per Node')

    return fig


def plot_message_count(metrics_collector):
    """
    Plot the number of messages sent by each node.

    Args:
        metrics_collector: The metrics collector containing message count data.

    Returns:
        matplotlib.figure.Figure: The figure containing the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # If metrics_collector doesn't have this data yet, create empty plot
    if not hasattr(metrics_collector, 'message_counts') or not metrics_collector.message_counts:
        ax.set_xlabel('Node ID')
        ax.set_ylabel('Message Count')
        ax.set_title('Messages Sent per Node')
        return fig

    nodes = list(metrics_collector.message_counts.keys())
    counts = list(metrics_collector.message_counts.values())

    ax.bar(nodes, counts, color='green')
    ax.set_xlabel('Node ID')
    ax.set_ylabel('Message Count')
    ax.set_title('Messages Sent per Node')

    return fig


def run_simulation(config_path, output_dir=None):
    """
    Run a simple simulation with the specified configuration.

    Args:
        config_path (str): Path to the configuration file.
        output_dir (str, optional): Directory to save output files.
    """
    # Create output directory if needed
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load configuration
    config_manager = ConfigManager("config/default.yaml")
    config_manager.update_config(config_path)

    # Get the selected topology
    topology_number = config_manager.get("topology")
    print(f"Running simulation with Topology {topology_number}")

    # Create the appropriate topology based on configuration
    if topology_number == 0:
        from beamsim.network.direct_topology import DirectTopology
        topology = DirectTopology(config_manager)
    elif topology_number == 1:
        from beamsim.network.gossipsub_topology import GossipsubTopology
        topology = GossipsubTopology(config_manager)
    elif topology_number == 2:
        from beamsim.network.grid_topology import GridTopology
        topology = GridTopology(config_manager)
    else:
        raise ValueError(f"Unknown topology number: {topology_number}")

    # Initialize metrics collector
    metrics_collector = MetricsCollector()

    # Add required attributes to metrics_collector for the summary
    metrics_collector.total_signatures_collected = 0
    metrics_collector.total_messages_sent = 0
    metrics_collector.total_bandwidth_used = 0
    metrics_collector.aggregation_completed = False
    metrics_collector.aggregation_completion_time = 0
    metrics_collector.aggregation_progress = {}

    # Create and set up the simulator
    simulator = Simulator()

    # Store configuration, topology, and metrics as attributes
    simulator.config_manager = config_manager
    simulator.topology = topology
    simulator.metrics_collector = metrics_collector

    # Register the metrics collector with the topology
    topology.register_metrics_collector(metrics_collector)

    # Set up other necessary components based on config
    max_time = config_manager.get("simulation.max_time_seconds", 300) * 1000  # Convert to ms

    # Run the simulation with the configured max time
    print("Starting simulation...")
    start_time = time.time()
    simulator.run(max_time=max_time)
    elapsed_time = time.time() - start_time
    print(f"Simulation completed in {elapsed_time:.2f} seconds")

    # Generate plots if output directory is provided
    if output_dir:
        # Plot aggregation progress
        fig = plot_aggregation_progress(metrics_collector)
        fig.savefig(os.path.join(output_dir, "aggregation_progress.png"))
        plt.close(fig)

        # Plot bandwidth usage
        fig = plot_bandwidth_usage(metrics_collector)
        fig.savefig(os.path.join(output_dir, "bandwidth_usage.png"))
        plt.close(fig)

        # Plot message count
        fig = plot_message_count(metrics_collector)
        fig.savefig(os.path.join(output_dir, "message_count.png"))
        plt.close(fig)

        # Save metrics to CSV files
        if hasattr(metrics_collector, 'save_to_csv'):
            metrics_collector.save_to_csv(output_dir)
        else:
            print("Warning: save_to_csv method not implemented in MetricsCollector")

        print(f"Results saved to {output_dir}")

    # Return simulator and metrics for further analysis if needed
    return simulator, metrics_collector


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple BEAMSim simulation")
    parser.add_argument(
        "--config",
        default="config/topology0.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--output-dir",
        default="results",
        help="Directory to save output files"
    )
    args = parser.parse_args()

    # Run the simulation
    simulator, metrics = run_simulation(args.config, args.output_dir)

    # Print summary statistics
    print("\nSimulation Summary:")
    print(f"Total simulation time: {simulator.current_time:.2f} ms")
    print(f"Number of signatures collected: {metrics.total_signatures_collected}")
    print(f"Number of messages sent: {metrics.total_messages_sent}")
    print(f"Total bandwidth used: {metrics.total_bandwidth_used / (1024 * 1024):.2f} MB")

    # If simulation completed successfully within time limit
    if metrics.aggregation_completed:
        print(f"Aggregation completed at: {metrics.aggregation_completion_time:.2f} ms")
    else:
        print("Aggregation did not complete within the time limit")