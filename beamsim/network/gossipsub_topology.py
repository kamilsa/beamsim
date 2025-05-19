"""
Gossipsub communication topology for the BEAMSim discrete-event simulation engine.

This module implements a gossip-based communication model using the Gossipsub
protocol for message dissemination.
"""

from beamsim.network.topology import NetworkTopology
import random


class GossipsubTopology(NetworkTopology):
    """
    Gossipsub communication topology implementation.
    """

    def __init__(self, simulator, gossipsub_D=8, gossipsub_D_low=6, gossipsub_D_high=12, random_seed=42):
        """
        Initialize the Gossipsub topology.

        Args:
            simulator: The simulator instance managing the simulation.
            gossipsub_D (int): Target number of peers in the mesh.
            gossipsub_D_low (int): Minimum number of peers in the mesh.
            gossipsub_D_high (int): Maximum number of peers in the mesh.
            random_seed (int): Seed for random number generation.
        """
        super().__init__(simulator)
        self.gossipsub_D = gossipsub_D
        self.gossipsub_D_low = gossipsub_D_low
        self.gossipsub_D_high = gossipsub_D_high
        random.seed(random_seed)

    def connect_nodes(self, params):
        """
        Establish Gossipsub connections between nodes.

        Args:
            params (dict): Parameters including 'validators' and 'subnet_id'.
        """
        nodes = params.get('validators', [])
        for node in nodes:
            self.add_node(node)

        # Create a random mesh network
        for node in self.nodes:
            num_peers = random.randint(self.gossipsub_D_low, self.gossipsub_D_high)
            peers = random.sample([n for n in self.nodes if n != node], min(num_peers, len(self.nodes) - 1))
            for peer in peers:
                self.node_connections[node.node_id].add(peer.node_id)
                self.node_connections[peer.node_id].add(node.node_id)

    def route_message(self, sender, recipient, message, **kwargs):
        """
        Route a message using the Gossipsub protocol.

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
            # Broadcast to all connected peers
            visited = set()
            queue = [sender]
            while queue:
                current = queue.pop(0)
                if current.node_id not in visited:
                    visited.add(current.node_id)
                    for neighbor_id in self.node_connections[current.node_id]:
                        neighbor = next(node for node in self.nodes if node.node_id == neighbor_id)
                        self.simulator.schedule_event(
                            sender=current,
                            recipient=neighbor,
                            message=message,
                            latency=self.calculate_latency(current, neighbor)
                        )
                        queue.append(neighbor)

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