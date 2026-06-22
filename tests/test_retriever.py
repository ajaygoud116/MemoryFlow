# tests/test_retriever.py

from extraction.extractor import extract_memory

from retrieval.retriever import retrieve_memories

memories = [

    extract_memory(
        "Budget is 2500 dollars"
    ),

    extract_memory(
        "Avoid seafood"
    ),

    extract_memory(
        "Need wheelchair accessibility"
    ),

    extract_memory(
        "Meeting date is June 20"
    )
]

query = "Recommend restaurant"

results = retrieve_memories(
    memories,
    query,
    top_k=3
)

for memory, score in results:

    print(
        memory.text,
        "->",
        round(score, 3)
    )