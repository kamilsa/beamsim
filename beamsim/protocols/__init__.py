"""
Communication protocols for the BEAMSim discrete-event simulation engine.

This module provides implementations of different communication protocols
used for message propagation in the BEAM Chain network simulation, including
GossipSub and Grid topology protocols.
"""

# Import protocol-related classes to make them available directly from beamsim.protocols
from beamsim.protocols.gossipsub import GossipSub
from beamsim.protocols.grid_protocol import GridProtocol

__all__ = [
    'GossipSub',
    'GridProtocol',
]