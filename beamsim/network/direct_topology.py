"""
Direct communication topology for the BEAMSim discrete-event simulation engine.

This module implements a direct communication model where nodes are connected
point-to-point, eliminating gossip protocols for message dissemination.
"""

from beamsim.network.topology import NetworkTopology


class DirectTopology(NetworkTopology):
    """
    Direct communication topology implementation.
    """

    def __init__(self, simulator, redundancy_factor=1):
        """
        Initialize the direct topology.

        Args:
            simulator: The simulator instance managing the simulation.
            redundancy_factor (int): Number of aggregators each validator sends to.
        """
        super().__init__(simulator)
        self.redundancy_factor = redundancy_factor

    def connect_nodes(self, params):
        """
        Establish direct connections between nodes.

        Args:
            params (dict): Parameters including 'subnet_aggregators' and 'validators'.
        """
        validators = params.get('validators', [])
        subnet_aggregators = params.get('subnet_aggregators', [])

        for validator in validators:
            # Connect each validator to multiple aggregators
            for aggregator in subnet_aggregators[:self.redundancy_factor]:
                self.node_connections[validator.node_id].add(aggregator.node_id)
                self.node_connections[aggregator.node_id].add(validator.node_id)

    def route_message(self, sender, recipient, message, **kwargs):
        """
        Route a message directly from sender to recipient(s).

        Args:
            sender: The node sending the message.
            recipient: The node receiving the message, or None for broadcast.
            message: The message to be routed.
        """
        if recipient:
            # Directly send the message to the recipient
            self.simulator.schedule_event(
                sender=sender,
                recipient=recipient,
                message=message,
                latency=self.calculate_latency(sender, recipient)
            )
        else:
            # Broadcast to all connected nodes
            for neighbor_id in self.node_connections[sender.node_id]:
                neighbor = next(node for node in self.nodes if node.node_id == neighbor_id)
                self.simulator.schedule_event(
                    sender=sender,
                    recipient=neighbor,
                    message=message,
                    latency=self.calculate_latency(sender, neighbor)
                )

    def calculate_latency(self, sender, recipient):
        """
        Calculate latency between two nodes.

        Args:
            sender: The sending node.
            recipient: The receiving node.

        Returns:
            int: Latency in milliseconds.
        """
        return self.simulator.latency_model.calculate_latency(sender, recipient)

    def calculate_bandwidth_usage(self, message):
        """
        Calculate bandwidth usage for a message.

        Args:
            message: The message being sent.

        Returns:
            int: Bandwidth usage in bytes.
        """
        return len(message.payload)