# Baseline Tokens
# MemoryFlow Tokens
# Token Reduction %

import os

if os.path.exists("memoryflow.db"):
    os.remove("memoryflow.db")

from extraction.extractor import extract_memory

from memory_store.store import MemoryStore

from scoring.amis import (
    compute_amis_score,
    update_recency_score
)

from scoring.redundancy import (
    compute_redundancy
)

from lifecycle.memory_lifecycle import (
    MemoryLifecycleEngine
)

from compression.compressor import (
    compress_memory
)

from benchmarking.benchmark import (
    compare_systems
)


conversation = [

    "My budget is $2500",

    "I am allergic to shellfish",

    "I prefer luxury hotels",

    "I want to travel to Switzerland",

    "Find flights",

    "Find restaurants",

    "Check weather",

    "Search activities",

    "Book hotels"
]

query = "Plan my trip"

store = MemoryStore()

for text in conversation:

    memory = extract_memory(text)

    store.add_memory(memory)

memories = store.get_memories(
    active_only=False
)

# -------------------
# AMIS
# -------------------

total = len(memories)

for memory in memories:

    update_recency_score(
        memory,
        total
    )

for i in range(len(memories)):

    memories[i].redundancy_score = (
        compute_redundancy(
            memories[i],
            memories[:i]
        )
    )

for memory in memories:

    compute_amis_score(
        memory,
        query
    )

# -------------------
# LIFECYCLE
# -------------------

lifecycle = (
    MemoryLifecycleEngine()
)

lifecycle.run(memories)
print("\nMEMORY STATES")
print("=" * 50)

for memory in memories:

    print(
        f"TEXT={memory.text}"
    )

    print(
        f"AMIS={memory.amis_score}"
    )

    print(
        f"TIER={memory.tier}"
    )

    print(
        f"ACTIVE={memory.active}"
    )

    print(
        f"COMPRESSED={memory.compressed_text}"
    )

    print("-" * 50)

print("\nbefore applying COMPRESSION...\n")
# -------------------
# COMPRESSION
# -------------------

for memory in memories:

    compress_memory(memory)

print("\nMEMORY STATES")
print("=" * 50)

for memory in memories:

    print(
        f"TEXT={memory.text}"
    )

    print(
        f"AMIS={memory.amis_score}"
    )

    print(
        f"TIER={memory.tier}"
    )

    print(
        f"ACTIVE={memory.active}"
    )

    print(
        f"COMPRESSED={memory.compressed_text}"
    )

    print("-" * 50)

print("\nAfter applying COMPRESSION\n")    
# -------------------
# BENCHMARK
# -------------------

result = compare_systems(
    conversation,
    store,query=query,
    top_k=5
)

print()
print("=" * 60)
print("COMPRESSION TEST")
print("=" * 60)

for k, v in result.items():
    print(k, ":", v)