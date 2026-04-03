# Distributed Semantic KV Store [IN PROGRESS - To be completed by Apr 6th, 2026]
- Alexandra Postolaki (posto022)
- Takuya Paipoovong (paipo001)

# Overview
A distributed semantic key-value store that uses vector embeddings for search, with dynamic partitioning and routing based on centroid similarity. The system balances search efficiency and accuracy by splitting data across nodes and performing approximate nearest-neighbor queries.

# Goals of the Assignment
The primary goals of this project are to:

    - Understand how distributed systems manage and partition data.
    - Implement routing logic using centroid-based similarity.
    - Explore the tradeoff between search efficiency (cost) and search accuracy (quality).
    - Analyze how design decisions (e.g., partition size, insertion order) affect system performance.

# Current Status
- Core system implementation: Complete
- Distributed ingestion and routing: Working (With minor adjustments for needed for Linux systems -> Debugging)
- Dynamic repartitioning: Verified
- Experimental evaluation and write up: In progress
  
[More information found in WRITEUP.md within project2]
