"""
Signature representation for the BEAMSim discrete-event simulation engine.

This module defines the Signature class, which encapsulates the properties
and behavior of post-quantum signatures in the network simulation.
"""

class Signature:
    """
    A class representing a post-quantum signature in the simulation.
    """

    def __init__(self, validator_id, size, data=None):
        """
        Initialize a signature.

        Args:
            validator_id (int): The ID of the validator that generated the signature.
            size (int): The size of the signature in bytes.
            data (str, optional): The actual signature data (default is None).
        """
        self.validator_id = validator_id
        self.size = size
        self.data = data or "signature_data"  # Placeholder for actual signature data

    def __repr__(self):
        """
        Return a string representation of the signature.

        Returns:
            str: A string describing the signature.
        """
        return f"Signature(validator_id={self.validator_id}, size={self.size})"