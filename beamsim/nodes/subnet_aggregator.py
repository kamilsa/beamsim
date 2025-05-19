"""
Subnet Aggregator node implementation for the BEAMSim discrete-event simulation engine.

This module defines the SubnetAggregator class, which collects signatures
from validators, aggregates them into a SNARK proof, and sends the proof
to global aggregators.
"""

from beamsim.core.node import Node
from beamsim.core.message import Message


class SubnetAggregator(Node):
    """
    A class representing a subnet aggregator node in the simulation.
    """

    def __init__(self, node_id, simulator, aggregation_rate_per_sec, snark_proof_size, subnet_signature_threshold):
        """
        Initialize a subnet aggregator node.

        Args:
            node_id (int): Unique identifier for the subnet aggregator.
            simulator: The simulator instance managing the simulation.
            aggregation_rate_per_sec (int): Rate of signature aggregation (signatures per second).
            snark_proof_size (int): Size of the SNARK proof (in bytes).
            subnet_signature_threshold (float): Percentage of signatures required to produce a SNARK proof.
        """
        super().__init__(node_id, simulator)
        self.aggregation_rate_per_sec = aggregation_rate_per_sec
        self.snark_proof_size = snark_proof_size
        self.subnet_signature_threshold = subnet_signature_threshold
        self.collected_signatures = []

    def receive_message(self, message):
        """
        Handle incoming messages (e.g., signatures from validators).

        Args:
            message (Message): The message containing a signature.
        """
        self.collected_signatures.append(message.payload)
        if self._should_aggregate():
            self._aggregate_signatures()

    def _should_aggregate(self):
        """
        Check if enough signatures have been collected to produce a SNARK proof.

        Returns:
            bool: True if aggregation should occur, False otherwise.
        """
        required_signatures = int(len(self.get_connected_nodes()) * self.subnet_signature_threshold / 100)
        return len(self.collected_signatures) >= required_signatures

    def _aggregate_signatures(self):
        """
        Aggregate collected signatures into a SNARK proof and send it to global aggregators.
        """
        aggregation_time = len(self.collected_signatures) / self.aggregation_rate_per_sec
        self.simulator.schedule_event(
            event_time=self.simulator.current_time + aggregation_time,
            event_callback=self._send_snark_proof,
        )

    def _send_snark_proof(self):
        """
        Send the SNARK proof to connected global aggregators.
        """
        snark_proof = {
            "aggregator_id": self.node_id,
            "proof_size": self.snark_proof_size,
            "signatures": len(self.collected_signatures),
        }
        message = Message(sender=self, payload=snark_proof)
        for global_aggregator in self.get_connected_nodes():
            self.simulator.schedule_event(
                event_time=self.simulator.current_time + self.simulator.latency_model.calculate_latency(self, global_aggregator),
                event_callback=global_aggregator.receive_message,
                message=message,
            )
        self.collected_signatures = []