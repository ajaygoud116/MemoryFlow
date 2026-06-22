from memory_store.store import MemoryStore

from benchmarking.test_cases import TEST_CASES

from benchmarking.evaluator import evaluate_retrieval

from core.memory import Memory



store = MemoryStore()



store.add_memory(
    Memory(
        text="I want to visit Switzerland",

        entities=["Switzerland"],

        numbers=[],

        noun_chunks=["visit Switzerland"],

        topic="travel",

        tier="active",

        memory_id=1
    )
)



store.add_memory(
    Memory(
        text="I prefer luxury hotels",

        entities=[],

        numbers=[],

        noun_chunks=["luxury hotels"],

        topic="hotel",

        tier="active",

        memory_id=2
    )
)



store.add_memory(
    Memory(
        text="I am allergic to shellfish",

        entities=["shellfish"],

        numbers=[],

        noun_chunks=["allergic to shellfish"],

        topic="health",

        tier="active",

        memory_id=3
    )
)



results = evaluate_retrieval(
    store,
    TEST_CASES,
    k=5
)



print("\nRETRIEVAL METRICS:\n")


for r in results:

    print("\nQUERY:", r["query"])

    print(
        "Recall@5:",
        r["recall@k"]
    )

    print(
        "Precision@5:",
        r["precision@k"]
    )

    print(
        "MRR:",
        r["mrr"]
    )

    print(
        "NDCG:",
        r["ndcg@k"]
    )

    print(
        "STORE MEMORIES:",
        [
            m.text
            for m in store.get_memories(active_only=False)
        ]
    )


    print(
        "VECTOR SEARCH TEST:",
        store.vector_store.search(
            "hotel preference",
            k=5 
        )
    )