import os

if os.path.exists("memoryflow.db"):
    os.remove("memoryflow.db")




import re

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

from retrieval.retriever import (
    retrieve_memories
)


# ------------------------------------
# BASELINE RETRIEVAL
# Pure FAISS Similarity
# ------------------------------------

def retrieve_similarity_only(
    store,
    query,
    top_k=5
):

    results = store.vector_store.search(
        query,
        k=top_k
    )

    retrieved = []

    for memory_id, _ in results:

        memory = store.get_memory_by_id(
            memory_id
        )

        if memory is None:
            continue

        if not memory.active:
            continue

        retrieved.append(memory)

    return retrieved


# ------------------------------------
# EVALUATION
# ------------------------------------

def evaluate_retrieval(
    retrieved_memories,
    expected_keywords
):

    context = "\n".join(
        [
            memory.text
            for memory in retrieved_memories
        ]
    )

    found = 0

    for keyword in expected_keywords:

        if keyword.lower() in context.lower():

            found += 1

    recall = (
        found
        /
        len(expected_keywords)
    ) * 100

    return round(recall, 2)


# ------------------------------------
# TEST DATASET
# ------------------------------------

conversation = [

    "My budget is $2500",

    "I am allergic to shellfish",

    "I prefer luxury hotels",

    "Destination is Switzerland",

    "I want mountain views",

    "Search flight options",

    "Search train routes",

    "Check weather forecast",

    "Find restaurants",

    "Find museums",

    "Find attractions",

    "I need wheelchair accessibility",

    "Compare hotel prices",

    "Find local transport",

    "Check exchange rates",

    "I am vegetarian",

    "I like Marriott hotels",

    "Search nightlife options",

    "Search hiking trails",

    "Generate itinerary"
]

query = (
    "Recommend a restaurant"
)

expected = [

    "shellfish",
    "vegetarian",
    "2500",
    "Switzerland"
]


# ------------------------------------
# BUILD MEMORY STORE
# ------------------------------------

store = MemoryStore()

for sentence in conversation:

    memory = extract_memory(
        sentence
    )

    store.add_memory(
        memory
    )

memories = store.get_memories(
    active_only=False
)

# ------------------------------------
# AMIS PIPELINE
# ------------------------------------

total = len(memories)

for memory in memories:

    update_recency_score(
        memory,
        total
    )

for i in range(
    len(memories)
):

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

lifecycle = (
    MemoryLifecycleEngine()
)

lifecycle.run(
    memories
)

# ------------------------------------
# BASELINE
# ------------------------------------

baseline = retrieve_similarity_only(
    store,
    query,
    top_k=5
)

baseline_score = (
    evaluate_retrieval(
        baseline,
        expected
    )
)

# ------------------------------------
# MEMORYFLOW
# ------------------------------------

memoryflow = retrieve_memories(
    store,
    query,
    top_k=5
)

memoryflow_only = [

    memory

    for memory, score

    in memoryflow
]

memoryflow_score = (
    evaluate_retrieval(
        memoryflow_only,
        expected
    )
)

# ------------------------------------
# RESULTS
# ------------------------------------

print()
print("=" * 60)
print("AMIS vs PURE VECTOR RETRIEVAL")
print("=" * 60)

print()
print("Expected Critical Memories:")
for item in expected:
    print("-", item)

print()

print(
    "Baseline Recall:",
    baseline_score,
    "%"
)

print(
    "MemoryFlow Recall:",
    memoryflow_score,
    "%"
)

print()

print("BASELINE RETRIEVED")
print("-" * 40)

for memory in baseline:
    print(memory.text)

print()

print("MEMORYFLOW RETRIEVED")
print("-" * 40)

for memory in memoryflow_only:
    print(memory.text)

print()

improvement = (
    memoryflow_score
    -
    baseline_score
)

print(
    "Improvement:",
    round(improvement, 2),
    "%"
)