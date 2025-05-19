## 🔗 BEAM Chain Networking Simulator

---

### 🧩 Problem Overview

We aim to **gossip and aggregate `num_signatures` post-quantum signatures** (each of size `signature_size`) across the network **within a time limit `max_time_seconds`**.

Each signature is initially owned by one of `num_validators` validators.  
Among these validators, a subset can act as **aggregators** (`num_aggregators`) or **global aggregators** (`num_global_aggregators`), capable of performing aggregation at a rate of `aggregation_rate_per_sec` (signatures per second).

The result of each aggregation is a **recursive SNARK proof**. This allows:
- Combining multiple individual signatures into a single aggregated SNARK.
- Further aggregating those SNARKs into higher-level proofs recursively.

The final SNARK proof has a fixed size `snark_proof_size`.

The goal is to produce final SNARK as fast as possible without imposing too high hardware requirements (bandwidth, CPU) and introducing centralization risks.

### 🎯 Task

Simulate the networking behavior of the BEAM chain during signature aggregation tasks using various network topologies. Measure the bandwidth consumed by each participant and evaluate the latency introduced by the SNARK aggregation process. Tests should be deterministic and reproducible based on the randomness seed provided

---

### ⚙️ Network Parameters (common for all topologies)

| Parameter | Description | Default |
|----------|-------------|---------|
| `random_seed` | Random seed for deterministic simulation | 42        |
| `num_validators` | Total number of validators and post-quantum signatures to be aggregated.  | 16384      |
| `signature_size` | Size (in bytes) of each individual post-quantum signature | 3072 (3KB)      |
| `slot_time` | The time between starting new cycles of signature distribution (ms) | 4000       |
| `signature_aggregation_window` | Maximum allowed time (in ms) within a slot for collecting, aggregating and finalizing signatures | 3000 |
| `subnet_signature_threshold` | Percentage of subnet signatures required before an aggregator produces a SNARK proof | 90% |
| `aggregation_rate_per_sec` | Rate at which aggregators can combine signatures (signatures/sec) | 1000       |
| `snark_recursion_aggregation_rate_per_sec` | Rate at which global aggregators can aggregate snark proofs (proofs/sec) | 100       |
| `snark_proof_size` | Size (in bytes) of a single recursive SNARK proof | 131072 (128KB)     |
| `snark_proof_verification_time_ms` | Time to verify a single recursive SNARK proof | 50     |
| `pq_signature_verification_time_ms` | Time to verify a single pq signature | 50     |
| `network_latency_min_ms` | Minimum latency between any two nodes (ms) — defaults to 10 ms | 10       |
| `network_latency_max_ms` | Maximum latency between any two nodes (ms) — defaults to 100 ms | 100      |
| `network_latency_distribution` | Distribution type for latency — assumed to be normal/Gaussian | Normal/Gaussian |
| `sign_latency_min_ms` | Minimum latency for signature generation from the start of slot | 10       |
| `sign_latency_max_ms` | Maximum latency for signature generation from the start of slot | 100      |
| `sign_latency_distribution` | Signature generation latency distribution | Normal/Gaussian |

---

### 🌐 Aggregation Topology 0 (Direct Communication Model)

This topology eliminates gossip protocols in favor of direct communication channels, creating a more centralized but potentially more efficient aggregation pathway. While this topology is unlikely to be used in practice, it serves as a useful baseline for understanding the impact of gossip protocols on network performance:

1. **Validator Subnets**:
   - Validators are divided into **subnets**, each with a designated set of aggregators.
   - Validators directly send their individual signatures to their subnet's aggregators through point-to-point connections.
   - For redundancy, each validator may send its signature to multiple subnet aggregators.
      - This is controlled by the `redundancy_factor` parameter.

2. **Subnet Aggregators**:
   - A subset of validators serves as **subnet aggregators** for each subnet.
   - This subset of validators is determined using randomness obtained from the `random_seed` combined with round number
       - Current BLS scheme VRF-based lottery is used, but for simulation purpose, it is not critical to have it as well
   - These aggregators receive signatures directly from validators in their subnet.
   - Aggregators belonging to the same subnet are connected to each other, allowing them to share signatures and aggregated proofs.

3. **Local Aggregation**:
   - Aggregators in each subnet combine signatures into a **single SNARK proof**. This involves:
     - Merging aggregation bits (binary flags indicating participation).
     - Using SNARKs to prove the correctness of the aggregated signatures.
   - SNARK proof should be produced when `signatures_in_aggregation_portion` of all signatures from the subnet was collected

4. **Direct Global Transmission**:
   - Subnet aggregators directly transmit their SNARK proofs and bitfields corresponding to validators who participated in SNARK proof to one of designated **global aggregators**.
   - This creates a direct pathway for proofs without the overhead of gossip protocols.
   - Global aggregators are a designated subset of validators with a specific role in collecting, processing subnet proofs, and producing final SNARK.

5. **Final Aggregation**:
   - Global aggregators receive proofs directly from all subnet aggregators.
   - Global aggregators are connected to each other, allowing them to share subnet proofs.
   - These proofs are consolidated into a **single recursive SNARK proof** for block inclusion.
   - When any of global aggregator collects enough subnet proofs (aggregating 2/3+1 of total signatures), it can produce a final proof and send it to other global aggregators.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `num_subnets` | Number of subnets to divide the validators into | 128 |
| `redundancy_factor` | Number of subnet aggregators each validator sends to | 3 |
| `num_subnet_aggregators` | Number of validators per subnet designated as subnet aggregators | 16 |
| `num_global_aggregators` | Number of validators designated as global aggregators for final proof generation | 128 |
| `num_peers_with_all_roles` | Number of peers that simultaneously act as validators, subnet aggregators, and global aggregators. These peers are a subset of `num_global_aggregators` and `num_subnet_aggregators`, meaning they do not increase the total number of aggregators but define a subset with all roles | 0      |

> Note 1: This topology reduces network congestion by eliminating gossip protocols but introduces potential single points of failure. The redundancy factor helps mitigate this risk by ensuring each signature is sent to multiple aggregators.

> Note 2: When there is only one aggregator in the subnet and one global aggregator, the topology becomes a **star topology**. In this case, the network is fully centralized, with all validators sending their signatures to a single aggregator, which then transmits the aggregated proof to the global aggregator. This setup is highly efficient but lacks redundancy and fault tolerance.

---

### 🌐 Aggregation Topology 1 (Inspired by BLS Signature Aggregation)

To ensure efficient aggregation, the network follows a **multi-layered aggregation topology**, inspired by BLS signature aggregation in Ethereum. Validators are organized into subnets, and a subset of them acts as aggregators. In contrast to Topology 0, validators do not send their signatures directly to aggregators. Instead, they use Gossgossip their signatures to everyone in the subnet, and aggregators collect these signatures from the network:

1. **Validator Subnets**:
   - Validators are divided into **subnets**, each responsible for gossiping their individual signatures.
   - Each subnet corresponds to a partition of the validators, ensuring even distribution of communication load.
   - The configuration of subnets can be adjusted using the `num_subnets` parameter.
   - Each validator in subnet gossips signature messages to `beacon_attestation_{subnet_id}` gossipsub v1.1 topic

2. **Aggregator Selection**:
   - A subset of validators serves as **subnet aggregators** for each subnet.
   - This subset of validators is determined using randomness obtained from the `random_seed` combined with the round number
   - These aggregators are responsible for collecting and combining signatures from their subnet.

3. **Local Aggregation**:
   - Aggregators in each subnet combine signatures into a **single SNARK proof**. This involves:
     - Merging aggregation bits (binary flags indicating participation).
     - Using SNARKs to prove the correctness of the aggregated signatures.
   - SNARK proof should be produced when `signatures_in_aggregation_portion` of all signatures from the subnet was collected

4. **Global Dissemination**:
   - Aggregators broadcast their aggregated SNARK proofs to a **global aggregation channel** to which **global aggregators** are subscribed to. This is analogous to the `beacon_aggregate_and_proof` topic in Ethereum.
   - Global aggregators are a designated subset of validators with a specific role in collecting, processing subnet proofs, and producing final SNARK.
   - Subnet proofs are gossiped to global aggregation channel to ensure all nodes are aware of the aggregated results.

5. **Final Aggregation**:
   - These proofs are further consolidated by any of global aggregator who collected subnet proof corresponding to `2/3 + 1` of all validators signatures into a **single recursive SNARK proof** for inclusion in the block.

| Parameter                  | Description                                   | Default       |
|----------------------------|-----------------------------------------------|---------------|
| `num_subnets`             | Number of subnets to divide the validators into | 128            |
| `signatures_in_aggregation_portion` | Percentage of signatures aggregators collect before producing a proof | 90% |
| `num_subnet_aggregators` | Number of validators per subnet designated as subnet aggregators | 16 |
| `num_global_aggregators`   | Number of aggregators in global aggregation topic | 128             |
| `num_peers_with_all_roles` | Number of peers that simultaneously act as validators, subnet aggregators, and global aggregators. These peers are a subset of `num_global_aggregators` and `num_subnet_aggregators`, meaning they do not increase the total number of aggregators but define a subset with all roles | 0      |
| `gossipsub_D`              | Number of peers each node connects to in mesh network | 8              |
| `gossipsub_D_low`          | Lower bound for number of mesh connections | 6              |
| `gossipsub_D_high`         | Upper bound for number of mesh connections | 12             |
| `gossipsub_heartbeat_interval_ms` | Interval between heartbeat events for mesh maintenance (ms) | 700           |
| `gossipsub_mesh_outbound_min` | Minimum number of outbound peers in mesh | 4              |
| `gossipsub_fanout_ttl_seconds` | Time-to-live for peers in fanout maps | 60             |

> Note, number of aggregators and validators in each subnet could be calculated by dividing the total number of **non-global aggregators** (i.e., those not participating in the global aggregate topic) and **validators** by the number of subnets.

---

### 🌐 Aggregation Topology 2 (Inspired by BLS Signature Aggregation + Grid topology)

This topology is very simillaro to topology 1, but instead of gossipsub [grid topology](https://hackmd.io/@kamilsa/rJ7SjSZaye#/3) is used:

1. **Validator Subnets**:
   - Validators are divided into **subnets**, each responsible for gossiping their individual signatures.
   - Each subnet corresponds to a partition of the validators, ensuring even distribution of communication load.
   - The configuration of subnets can be adjusted using the `num_subnets` and `validators_per_subnet` parameters.
   - Validators within each subnet follow grid topology for signatures dissemination
   - Each validator propagates signature messages to its row/column neighbors using `grid_beacon_attestation_{subnet_id}` libp2p protocol

2. **Aggregator Selection**:
   - A subset of validators serves as **subnet aggregators** for each subnet.
   - This subset of validators is determined using randomness obtained from the `random_seed` combined with round number
   - These aggregators are responsible for collecting and combining signatures from their subnet.

3. **Local Aggregation**:
   - Aggregators in each subnet combine signatures into a **single SNARK proof**. This involves:
     - Merging aggregation bits (binary flags indicating participation).
     - Using SNARKs to prove the correctness of the aggregated signatures.
   - SNARK proof should be produced when `signatures_in_aggregation_portion` of all signatures from the subnet was collected

4. **Global Dissemination**:
   - Subnet aggregators broadcast their aggregated SNARK proofs to a **global aggregation channel** to which **global aggregators** are subscribed to. This is analogous to the `beacon_aggregate_and_proof` topic in Ethereum.
   - Global aggregators are a designated subset of validators with a specific role in collecting, processing subnet proofs, and producing final SNARK.
   - Aggregators in global dissemination topic follow grid topology for dissemination of subnet proofs
   - Subnet proofs are gossiped into the grid to ensure all **global aggregators** are aware of the aggregated results from all subnets.

5. **Final Aggregation**:
   - These proofs are further consolidated by any of global aggregator who collected subnet proof corresponding to `2/3 + 1` of all validators signatures into a **single recursive SNARK proof** for inclusion in the block.

| Parameter                  | Description                                   | Default       |
|----------------------------|-----------------------------------------------|---------------|
| `num_subnets`             | Number of subnets to divide the validators into | 128            |
| `num_subnet_aggregators` | Number of validators per subnet designated as subnet aggregators | 16 |
| `num_global_aggregators` | Number of validators designated as global aggregators for final proof generation | 128 |
| `num_peers_with_all_roles` | Number of peers that simultaneously act as validators, subnet aggregators, and global aggregators. These peers are a subset of `num_global_aggregators` and `num_subnet_aggregators`, meaning they do not increase the total number of aggregators but define a subset with all roles | 0      |

---

### 🕒 Implementation Details: Leveraging ns-3 for Discrete-Event Simulation
Discrete-Event Simulation (DES) will be used to model the BEAM chain's networking behavior. Time progresses in discrete steps triggered by events like message transmissions or aggregation completions.

#### **Advantages of DES**:
1. **Scalability**: Efficiently simulate large networks (e.g., thousands of validators) without real-time constraints.
2. **Determinism**: Events are processed in a predictable order, ensuring reproducible results.
3. **Efficiency**: The simulation avoids idle CPU cycles by processing events from a queue, independent of real-time progression. This allows for simulating days of Beam chain operation within minutes.

#### Graphical Representation

Example of possible graphics of simulator's work

##### Progressive Aggregation Line Chart

Shows percentage of signatures aggregated over time

![download](https://hackmd.io/_uploads/S1oK2Byble.png)

##### Bandwidth Usage Over Time
Shows bandwidth usage of each node type over time

![download](https://hackmd.io/_uploads/HyOQ0Bkbee.png)


##### Message count cumulation
Shows total number of messages sent over time

![download](https://hackmd.io/_uploads/H1kn1UJblg.png)

## Future directions

1. Explore alternative aggregation strategies (e.g., the one that Justin Drake proposed during [BEAM call #3](https://www.youtube.com/watch?v=dJkuwuh2Nrs))
2. Extend the simulation to include events like block production
3. Introduce malicious nodes to test the robustness of the aggregation process