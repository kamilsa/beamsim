"""
Aggregation logic for the BEAMSim discrete-event simulation engine.

This module defines the AggregationLogic class, which provides methods
for aggregating signatures into SNARK proofs and managing aggregation thresholds.
"""

from beamsim.aggregation.signature import Signature
from beamsim.aggregation.snark import SNARKProof


class AggregationLogic:
    """
    A class encapsulating the logic for aggregating signatures into SNARK proofs.
    """

    def __init__(self, aggregation_rate_per_sec, snark_proof_size, signature_threshold):
        """
        Initialize the aggregation logic.

        Args:
            aggregation_rate_per_sec (int): Rate of signature aggregation (signatures per second).
            snark_proof_size (int): Size of the SNARK proof (in bytes).
            signature_threshold (float): Percentage of signatures required to produce a SNARK proof.
        """
        self.aggregation_rate_per_sec = aggregation_rate_per_sec
        self.snark_proof_size = snark_proof_size
        self.signature_threshold = signature_threshold

    def should_aggregate(self, collected_signatures, total_signatures):
        """
        Determine if enough signatures have been collected to produce a SNARK proof.

        Args:
            collected_signatures (int): Number of collected signatures.
            total_signatures (int): Total number of signatures expected.

        Returns:
            bool: True if aggregation should occur, False otherwise.
        """
        required_signatures = int(total_signatures * self.signature_threshold / 100)
        return collected_signatures >= required_signatures

    def aggregate_signatures(self, collected_signatures, aggregator_id):
        """
        Aggregate collected signatures into a SNARK proof.

        Args:
            collected_signatures (list[Signature]): List of collected signatures.
            aggregator_id (int): ID of the aggregator performing the aggregation.

        Returns:
            SNARKProof: The resulting SNARK proof.
        """
        num_signatures = len(collected_signatures)
        aggregation_time = num_signatures / self.aggregation_rate_per_sec

        # Simulate aggregation delay (if needed, integrate with the simulator)
        # For now, we just return the proof immediately
        return SNARKProof(
            aggregator_id=aggregator_id,
            proof_size=self.snark_proof_size,
            num_signatures=num_signatures,
            metadata={"aggregation_time": aggregation_time}
        )