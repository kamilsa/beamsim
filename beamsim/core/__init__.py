"""
Core components for the BEAMSim discrete-event simulation engine.

This module provides the fundamental building blocks for the BEAM Chain
network simulator, including the event system, simulator, and base classes
for nodes and messages.
"""

# Import core components to make them available directly from beamsim.core
# These imports will be added as the respective modules are implemented
from beamsim.core.simulator import Simulator
from beamsim.core.event import Event, EventQueue
from beamsim.core.node import Node
from beamsim.core.message import Message

__all__ = [
    'Simulator',
    'Event',
    'EventQueue',
    'Node',
    'Message',
]