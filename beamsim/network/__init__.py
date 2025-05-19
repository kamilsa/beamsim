"""
Network components for the BEAMSim discrete-event simulation engine.

This module provides implementations of different network topologies and
related utilities for modeling network communication in BEAM Chain simulations.
"""

# Import network components to make them available directly from beamsim.network
# These imports will be added as the respective modules are implemented
from beamsim.network.topology import NetworkTopology
from beamsim.network.latency import LatencyModel
from beamsim.network.bandwidth import BandwidthTracker

# Import specific topology implementations
from beamsim.network.direct_topology import DirectTopology
from beamsim.network.gossipsub_topology import GossipsubTopology
from beamsim.network.grid_topology import GridTopology

__all__ = [
    'NetworkTopology',
    'LatencyModel',
    'BandwidthTracker',
    'DirectTopology',
    'GossipsubTopology',
    'GridTopology',
]