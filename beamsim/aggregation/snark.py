"""
SNARK proof representation for the BEAMSim discrete-event simulation engine.

This module defines the SNARKProof class, which encapsulates the properties
and behavior of SNARK proofs in the network simulation.
"""

class SNARKProof:
    """
    A class representing a SNARK proof in the simulation.
    """

    def __init__(self, aggregator_id, proof_size, num_signatures, metadata=None):
        """
        Initialize a SNARK proof.

        Args:
            aggregator_id (int): The ID of the aggregator that generated the proof.
            proof_size (int): The size of the SNARK proof in bytes.
            num_signatures (int): The number of signatures aggregated into this proof.
            metadata (dict, optional): Additional metadata for the proof (default is None).
        """
        self.aggregator_id = aggregator_id
        self.proof_size = proof_size
        self.num_signatures = num_signatures
        self.metadata = metadata or {}

    def __repr__(self):
        """
        Return a string representation of the SNARK proof.

        Returns:
            str: A string describing the SNARK proof.
        """
        return (f"SNARKProof(aggregator_id={self.aggregator_id}, "
                f"proof_size={self.proof_size}, num_signatures={self.num_signatures})")