"""
GossipSub protocol implementation for the BEAMSim discrete-event simulation engine.

This module defines the GossipSub class, which simulates the behavior of the
GossipSub protocol for message propagation in the network.
"""

import random


class GossipSub:
    """
    A class representing the GossipSub protocol for message propagation.
    """

    def __init__(self, node_id, peers, D, D_low, D_high, heartbeat_interval_ms):
        """
        Initialize the GossipSub protocol.

        Args:
            node_id (int): The ID of the node using this protocol.
            peers (list[int]): List of peer node IDs.
            D (int): Target number of peers in the mesh.
            D_low (int): Minimum number of peers in the mesh.
            D_high (int): Maximum number of peers in the mesh.
            heartbeat_interval_ms (int): Interval between heartbeat events (ms).
        """
        self.node_id = node_id
        self.peers = peers
        self.D = D
        self.D_low = D_low
        self.D_high = D_high
        self.heartbeat_interval_ms = heartbeat_interval_ms
        self.mesh = set()
        self.fanout = {}
        self.messages = set()

    def join_mesh(self):
        """
        Join the mesh by selecting peers up to the target number (D).
        """
        self.mesh = set(random.sample(self.peers, min(self.D, len(self.peers))))

    def publish_message(self, message_id, message):
        """
        Publish a message to the mesh.

        Args:
            message_id (str): Unique identifier for the message.
            message (str): The content of the message.
        """
        if message_id not in self.messages:
            self.messages.add(message_id)
            for peer in self.mesh:
                self.send_message(peer, message_id, message)

    def send_message(self, peer, message_id, message):
        """
        Simulate sending a message to a peer.

        Args:
            peer (int): The ID of the peer to send the message to.
            message_id (str): Unique identifier for the message.
            message (str): The content of the message.
        """
        # Placeholder for actual message sending logic
        print(f"Node {self.node_id} sent message {message_id} to peer {peer}")

    def heartbeat(self):
        """
        Perform a heartbeat to maintain the mesh and fanout.
        """
        if len(self.mesh) < self.D_low:
            needed_peers = self.D - len(self.mesh)
            new_peers = set(random.sample(self.peers - self.mesh, min(needed_peers, len(self.peers - self.mesh))))
            self.mesh.update(new_peers)

        if len(self.mesh) > self.D_high:
            excess_peers = len(self.mesh) - self.D_high
            for _ in range(excess_peers):
                self.mesh.pop()