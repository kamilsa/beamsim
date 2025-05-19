"""
Global Aggregator node implementation for the BEAMSim discrete-event simulation engine.

This module defines the GlobalAggregator class, which collects SNARK proofs
from subnet aggregators, aggregates them into a final recursive SNARK proof,
and broadcasts the result.
"""

from beamsim.core.node import Node
from beamsim.core.message import Message


class GlobalAggregator(Node):
    """
    A class representing a global aggregator node in the simulation.
    """

    def __init__(self, node_id, simulator, recursion_aggregation_rate_per_sec, snark_proof_size, finalization_threshold):
        """
        Initialize a global aggregator node.

        Args:
            node_id (int): Unique identifier for the global aggregator.
            simulator: The simulator instance managing the simulation.
            recursion_aggregation_rate_per_sec (int): Rate of recursive SNARK aggregation (proofs per second).
            snark_proof_size (int): Size of the final recursive SNARK proof (in bytes).
            finalization_threshold (float): Percentage of subnet proofs required to finalize the aggregation.
        """
        super().__init__(node_id, simulator)
        self.recursion_aggregation_rate_per_sec = recursion_aggregation_rate_per_sec
        self.snark_proof_size = snark_proof_size
        self.finalization_threshold = finalization_threshold
        self.collected_proofs = []

    def receive_message(self, message):
        """
        Handle incoming messages (e.g., SNARK proofs from subnet aggregators).

        Args:
            message (Message): The message containing a SNARK proof.
        """
        self.collected_proofs.append(message.payload)
        if self._should_finalize():
            self._finalize_aggregation()

    def _should_finalize(self):
        """
        Check if enough subnet proofs have been collected to produce the final SNARK proof.

        Returns:
            bool: True if finalization should occur, False otherwise.
        """
        required_proofs = int(len(self.get_connected_nodes()) * self.finalization_threshold / 100)
        return len(self.collected_proofs) >= required_proofs

    def _finalize_aggregation(self):
        """
        Aggregate collected subnet proofs into a final recursive SNARK proof.
        """
        aggregation_time = len(self.collected_proofs) / self.recursion_aggregation_rate_per_sec
        self.simulator.schedule_event(
            event_time=self.simulator.current_time + aggregation_time,
            event_callback=self._broadcast_final_snark,
        )

    def _broadcast_final_snark(self):
        """
        Broadcast the final recursive SNARK proof to all connected nodes.
        """
        final_snark = {
            "aggregator_id": self.node_id,
            "proof_size": self.snark_proof_size,
            "subnet_proofs": len(self.collected_proofs),
        }
        message = Message(sender=self, payload=final_snark)
        for node in self.get_connected_nodes():
            self.simulator.schedule_event(
                event_time=self.simulator.current_time + self.simulator.latency_model.calculate_latency(self, node),
                event_callback=node.receive_message,
                message=message,
            )
        self.collected_proofs = []