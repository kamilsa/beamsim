"""
Aggregation components for the BEAMSim discrete-event simulation engine.

This module provides classes for signature generation, SNARK proof creation,
and aggregation logic needed for the BEAM Chain network simulation.
"""

# Import aggregation-related classes to make them available directly from beamsim.aggregation
from beamsim.aggregation.signature import Signature
from beamsim.aggregation.snark import SNARKProof
from beamsim.aggregation.aggregator import AggregationLogic

__all__ = [
    'Signature',
    'SNARKProof',
    'AggregationLogic',
]